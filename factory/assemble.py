"""Dựng video 9:16 từ Bundle + audio đã tổng hợp.

KHÔNG CÓ LLM Ở ĐÂY. Cũng không có Whisper, cũng không có dịch máy.

Engine dựng là repo `video-editor` (Windows-native, ffmpeg 8.1.1 vendored có
libass + fribidi + NVENC, 68 file test). Ta KHÔNG viết lại nó -- chỉ vá đúng
ba chỗ nó buộc phải đoán hoặc đòi thứ ta không dùng, trong khi ta đã biết chắc câu trả lời.

═══ VÁ 1: TRANSCRIPT ═══
AssemblyJob gọi Whisper phiên âm NGƯỢC từ audio để lấy timing. Vô lý ở đây:
kịch bản là thứ ta vừa đưa vào TTS, và speak.py đã ghi lại timing chính xác
TRONG LÚC tổng hợp. Để Whisper đoán lại thì vừa tốn ~13 giây mỗi short, vừa
sai dấu tiếng Việt nên phụ đề lệch với lời đọc.

═══ VÁ 2: TỪ KHOÁ B-ROLL ═══
AssemblyJob tự trích từ khoá tiếng Việt rồi DỊCH MÁY sang tiếng Anh để tìm
clip. Đây là nguồn của một lớp lỗi thật đã ghi nhận ở v1: câu "cũng không
phải hình phạt của một đấng thần linh" (đang PHỦ ĐỊNH) bị dịch chữ-đúng-chữ
thành "punishment of a deity", và Pexels trả về ảnh linh mục Công giáo đứng
trước bàn thờ -- cho một video Phật giáo.

Bundle.broll_queries đã là tiếng Anh, do người/Claude viết, có ngữ cảnh.
Nên ta bỏ HẲN nhánh trích-rồi-dịch. Không phải sửa bản dịch cho khéo hơn --
là xoá cả bước đoán đi.

═══ VÁ 3: MODEL WHISPER ═══
assembly_job nạp model SỚM và fail-closed nếu thiếu file -- đúng với thiết
kế gốc của họ (không tải model lúc chạy), nhưng ta đã thay transcribe nên
model không bao giờ được dùng. Stub báo "đã nạp" để khỏi phải giữ ~500 MB
nằm im.

Cả ba vá đều là monkeypatch có phạm vi hẹp, đặt trong một context manager,
và được khẳng định lại mỗi lần chạy. Đây là nợ kỹ thuật có ý thức: cách
đúng là video-editor nhận thẳng transcript + queries qua tham số. Khi nào
thêm được tham số đó thì xoá hết phần vá này.
"""
from __future__ import annotations

import sys
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIDEO_TOOL_ROOT = ROOT.parent / "video-editor"

# Preset short-form đã tinh chỉnh và xác nhận qua 3 mẫu thật ở v1 -- giữ
# nguyên, không phát minh lại.
SHORT_WIDTH, SHORT_HEIGHT = 1080, 1920
SHORT_SCENE_SEC = 4.0
SHORT_MAX_SCENE_SEC = 8.0
SHORT_TRANSITION_SEC = 0.3
SHORT_MOTION_STRENGTH = "high"
SHORT_BROLL_SPEED = 1.6


class AssembleError(RuntimeError):
    pass


@dataclass
class AssembleResult:
    video_path: str
    duration: float
    scene_count: int
    warnings: list[str]


def _ensure_importable() -> None:
    if not VIDEO_TOOL_ROOT.exists():
        raise AssembleError(
            f"Không thấy video-editor tại {VIDEO_TOOL_ROOT}. "
            "Clone https://github.com/nguyent0810/video-editor cạnh repo này."
        )
    if str(VIDEO_TOOL_ROOT) not in sys.path:
        sys.path.insert(0, str(VIDEO_TOOL_ROOT))


def transcript_from_timing(timing: dict):
    """Dựng TranscriptResult của video-editor từ timing speak.py đã ghi.

    Timing của ta ở mức CÂU; video-editor muốn cả mức TỪ để làm caption
    karaoke. Không có mốc từng từ thật (TTS không trả về), nên ta chia đều
    theo độ dài ký tự trong câu -- xấp xỉ, nhưng xấp xỉ TRÊN văn bản ĐÚNG,
    khác hẳn Whisper đoán cả văn bản lẫn mốc thời gian. Câu đúng + mốc xấp
    xỉ thì caption vẫn đọc đúng chữ; Whisper sai chữ thì hỏng hẳn.
    """
    _ensure_importable()
    from core.subtitles.transcribe import (TranscriptResult, TranscriptSegment,
                                           WordTimestamp)

    segments = []
    for seg in timing["segments"]:
        text = seg.get("spoken") or seg["text"]
        start, end = float(seg["start"]), float(seg["end"])
        words = text.split()
        total_chars = sum(len(w) for w in words) or 1
        cursor, timed = start, []
        for w in words:
            share = (end - start) * (len(w) / total_chars)
            timed.append(WordTimestamp(word=w, start=round(cursor, 3),
                                       end=round(cursor + share, 3), probability=1.0))
            cursor += share
        if timed:  # khớp mốc cuối về đúng end, tránh trôi do làm tròn
            timed[-1].end = round(end, 3)
        segments.append(TranscriptSegment(start=start, end=end, text=text, words=timed))

    return TranscriptResult(
        segments=segments, language="vi", language_probability=1.0,
        full_text=" ".join(s.text for s in segments),
    )


@contextmanager
def _patched(timing: dict, broll_queries: list[str]):
    """Vá hai chỗ video-editor buộc phải đoán, chỉ trong phạm vi khối with."""
    _ensure_importable()
    import core.pipeline.subtitle_job as subtitle_job
    import core.stockfootage.assembly_job as assembly_job
    from core.stockfootage.models import SegmentKeywords

    transcript = transcript_from_timing(timing)
    orig_transcribe = subtitle_job.transcribe_audio
    orig_keywords = assembly_job.extract_keywords_for_segments
    orig_manager = assembly_job.SubtitleModelManager

    def _no_whisper(*_a, **_kw):
        return transcript

    def _explicit_queries(segments, top_n=5, extra_stopwords=None):
        """Xoay vòng broll_queries theo số cảnh.

        Số cảnh do video-editor tự chia theo thời lượng, không nhất thiết
        bằng số query ta viết. Xoay vòng thay vì để trống: thà lặp lại một
        cảnh hình còn hơn rơi về nhánh dịch máy đã từng gây lỗi thật."""
        if not broll_queries:
            raise AssembleError("broll_queries rỗng -- Bundle.validate() lẽ ra đã chặn")
        return [SegmentKeywords(segment=seg, keywords=[broll_queries[i % len(broll_queries)]])
                for i, seg in enumerate(segments)]

    class _NoModelNeeded:
        """Model Whisper KHÔNG bao giờ được dùng tới vì transcribe_audio đã
        bị thay. Nhưng assembly_job nạp nó SỚM (trước prepare_subtitles) và
        fail-closed nếu thiếu file model -- hợp lý với thiết kế gốc của họ
        (không tải model lúc chạy), chỉ là không áp dụng cho ta.

        Stub này báo "đã nạp rồi" để bỏ qua bước nạp. Ta không tải, không
        bundle, và cũng không cần ~500 MB model chỉ để nó nằm im."""
        is_loaded = True

        @classmethod
        def instance(cls):
            return cls()

        def get_model(self, *a, **kw):
            return None

    subtitle_job.transcribe_audio = _no_whisper
    assembly_job.extract_keywords_for_segments = _explicit_queries
    assembly_job.SubtitleModelManager = _NoModelNeeded
    try:
        yield
    finally:
        subtitle_job.transcribe_audio = orig_transcribe
        assembly_job.extract_keywords_for_segments = orig_keywords
        assembly_job.SubtitleModelManager = orig_manager


def assemble_short(bundle, wav_path: Path, timing: dict, out_path: Path,
                   pexels_key: str, bgm_path: Path | None = None,
                   logo_path: Path | None = None) -> AssembleResult:
    """Dựng một Short 9:16 hoàn chỉnh: B-roll + caption karaoke + nhạc nền."""
    _ensure_importable()
    from core.pipeline.bgm import BGMConfig
    from core.pipeline.logo_overlay import LogoConfig
    from core.pipeline.stages import ProcessingState
    from core.pipeline.subtitle_job import SubtitleConfig
    from core.pipeline.video_effects import IntensityLevel
    from core.stockfootage.assembly_job import AssemblyJob, run_assembly_job
    from core.stockfootage.providers.pexels import PexelsProvider

    out_path.parent.mkdir(parents=True, exist_ok=True)
    provider = PexelsProvider(api_key=pexels_key)
    try:
        job = AssemblyJob(
            audio_path=str(wav_path.resolve()),
            output_path=str(out_path.resolve()),
            provider=provider,
            video_width=SHORT_WIDTH,
            video_height=SHORT_HEIGHT,
            scene_target_sec=SHORT_SCENE_SEC,
            scene_max_sec=SHORT_MAX_SCENE_SEC,
            transition_sec=SHORT_TRANSITION_SEC,
            motion_mode="auto",
            motion_strength=IntensityLevel.HIGH,
            broll_speed_factor=SHORT_BROLL_SPEED,
            subtitles=SubtitleConfig(),
            bgm=BGMConfig(path=str(bgm_path.resolve())) if bgm_path else None,
            logo=LogoConfig(path=str(logo_path.resolve())) if logo_path else None,
        )
        warnings: list[str] = []
        with _patched(timing, list(bundle.broll_queries)):
            result = run_assembly_job(job, on_warning=warnings.append)
    finally:
        provider.close()

    if result.state == ProcessingState.FAILED or not result.output_path:
        raise AssembleError(f"dựng video lỗi: {result.error}")

    return AssembleResult(
        video_path=result.output_path,
        duration=float(timing.get("duration", 0.0)),
        scene_count=result.scene_count,
        warnings=warnings + list(result.warnings or []),
    )

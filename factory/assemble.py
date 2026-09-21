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


# ─── Kiểu caption ─────────────────────────────────────────────────────────
#
# TIKTOK: karaoke tô sáng từng chữ -- theo chính ghi chú thiết kế của
# video-editor, đây là đòn bẩy lớn nhất khiến phụ đề đọc ra "sinh động" thay
# vì tĩnh. Mặc định của họ TẮT nó để không đổi giao diện các render cũ; ta
# bật.
#
# RỦI RO PHẢI CANH: dấu tiếng Việt chồng tầng (ế ồ ữ ợ ẩ) nằm CAO hơn chữ
# hoa thường, nên viền quá dày hoặc cỡ chữ quá lớn sẽ cắt cụt phần dấu --
# và lỗi này chỉ lộ ra ở đúng những chữ có dấu, dễ lọt qua nếu chỉ test
# bằng chữ không dấu.
#
# Ba quyết định để tránh:
#   - outline vừa phải (4), KHÔNG dày hơn: viền dày ăn vào phần dấu phía trên
#   - KHÔNG uppercase_emphasis: chữ hoa có dấu (Ế, Ữ, Ợ) đội dấu cao hơn nữa,
#     là trường hợp dễ bị cắt nhất
#   - margin_v rộng để cả khối chữ không chạm mép dưới khi xuống 2 dòng
#
# Font Be Vietnam Pro Bold -- thiết kế riêng cho tiếng Việt, dựng sẵn trong
# video-editor/assets/fonts. Không dùng font hệ thống: phần lớn font Latin
# đặt dấu sai vị trí hoặc thiếu hẳn glyph tổ hợp.

CAPTION_OUTLINE = 5   # day hon vi da bo hop nen; da render that va kiem tra dau con nguyen
CAPTION_SHADOW = 2
HIGHLIGHT_YELLOW_BGR = "00E5FF"   # ASS là &HBBGGRR -> đây là vàng rực
HIGHLIGHT_GREEN_BGR = "7CFC00"


def tiktok_caption_config(highlight_bgr: str = HIGHLIGHT_YELLOW_BGR):
    """Caption karaoke kiểu TikTok, an toàn với dấu tiếng Việt."""
    _ensure_importable()
    from core.pipeline.subtitle_job import SubtitleConfig
    return SubtitleConfig(
        enabled=True,
        dynamic_captions_enabled=True,     # tô sáng từng chữ
        highlight_colour_bgr=highlight_bgr,
        font_weight_bold=True,
        outline_width=CAPTION_OUTLINE,
        shadow_strength=CAPTION_SHADOW,
        uppercase_emphasis=False,          # xem ghi chú về dấu ở trên
        remove_punctuation=False,
    )


# ─── Hộp nền hay chỉ viền ─────────────────────────────────────────────────
#
# video-editor hardcode BorderStyle=3 (hộp nền đen 50% alpha) với lý do ghi
# rõ trong code: "dễ đọc trên B-roll rối hơn là chữ chỉ có viền". Lý do đó
# ĐÚNG -- hộp nền thật sự dễ đọc hơn.
#
# Nhưng nó không phải look short-form hiện nay. Khảo sát 2026 về caption
# TikTok/Reels: kiểu thắng là chữ trắng (hoặc vàng) viền đen ĐẬM, KHÔNG hộp,
# tô sáng từng chữ, đặt ở khoảng một phần ba dưới. Hộp nền trông giống phụ
# đề phim, làm video "nặng" và cũ.
#
# Nên đây là LỰA CHỌN có ý thức, không phải mặc định mù: "outline" cho
# short (mặc định), "box" giữ lại cho trường hợp B-roll quá rối hoặc nội
# dung nghiêm túc cần đọc chắc.
#
# Bù lại việc bỏ hộp: viền dày hơn (5 thay vì 4) + đổ bóng mạnh hơn. Vẫn
# phải canh trần trên vì dấu tiếng Việt chồng tầng -- 5 là mức tôi đã render
# thật và kiểm tra dấu còn nguyên; đừng tăng tiếp mà không render lại.

BORDERSTYLE_INDEX = 15   # xem bảng đếm trường trong _outline_header()
CAPTION_BORDER_BOX = 3
CAPTION_BORDER_OUTLINE = 1


@contextmanager
def _caption_border(style: str):
    """Đổi BorderStyle trong dòng Style của file ASS.

    video-editor hardcode số 3 giữa một f-string dựng header, không có tham
    số nào để đổi. Thay vì sửa repo họ, ta vá đúng hàm dựng header trong
    phạm vi một lần render."""
    if style == "box":
        yield
        return
    _ensure_importable()
    import core.subtitles.ass_writer as ass_writer
    import core.subtitles.karaoke_writer as karaoke_writer

    # karaoke_writer làm `from ... import build_ass_header`, nên tên đã bind
    # sẵn trong module đó -- vá riêng ass_writer KHÔNG ăn. Phải vá cả hai
    # chỗ. (Phát hiện thật: lần đầu render vẫn ra BorderStyle=3.)
    orig = ass_writer.build_ass_header
    orig_k = karaoke_writer.build_ass_header

    def _outline_header(*a, **kw):
        header = orig(*a, **kw)
        # build_ass_header trả về LIST dòng, không phải chuỗi (caller làm
        # `lines = build_ass_header(...)` rồi tự join). Giữ nguyên kiểu trả
        # về, chỉ sửa đúng dòng Style.
        out = []
        for line in header:
            if line.startswith("Style: "):
                parts = line[len("Style: "):].split(",")
                # BorderStyle là trường thứ 16 trong Format, tức INDEX 15:
                #   0 Name  1 Fontname  2 Fontsize  3 Primary  4 Secondary
                #   5 OutlineColour  6 BackColour  7 Bold  8 Italic
                #   9 Underline  10 StrikeOut  11 ScaleX  12 ScaleY
                #   13 Spacing  14 Angle  15 BorderStyle  16 Outline  17 Shadow
                # Bản đầu tôi ghi nhầm index 16 -- và nó âm thầm ghi đè
                # Outline thay vì BorderStyle, nên caption vẫn có hộp nền mà
                # viền thì hỏng. Đếm lại từ Format thay vì đoán.
                if len(parts) > BORDERSTYLE_INDEX:
                    parts[BORDERSTYLE_INDEX] = str(CAPTION_BORDER_OUTLINE)
                    line = "Style: " + ",".join(parts)
            out.append(line)
        return out

    ass_writer.build_ass_header = _outline_header
    karaoke_writer.build_ass_header = _outline_header
    try:
        yield
    finally:
        ass_writer.build_ass_header = orig
        karaoke_writer.build_ass_header = orig_k


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
    orig_translate = assembly_job.translate_vi_to_en

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

    # LỖI THẬT (21/09/2026): assembly_job DỊCH MÁY câu thoại của từng cảnh
    # (translate_vi_to_en) và dùng làm query ƯU TIÊN; query của ta chỉ là dự
    # phòng. Hậu quả: "Can Giáp" -> lính mặc giáp cầm súng, "Bọ Cạp" -> bọ
    # ngựa, "Trời dưới" -> máy bay -- và cả 92 video Lịch đã đăng chưa từng
    # dùng broll_queries. Trả None -> đường ống rơi về sk.query = query của ta.
    def _no_translate(*_a, **_kw):
        return None

    subtitle_job.transcribe_audio = _no_whisper
    assembly_job.translate_vi_to_en = _no_translate
    assembly_job.extract_keywords_for_segments = _explicit_queries
    assembly_job.SubtitleModelManager = _NoModelNeeded
    try:
        yield
    finally:
        subtitle_job.transcribe_audio = orig_transcribe
        assembly_job.extract_keywords_for_segments = orig_keywords
        assembly_job.SubtitleModelManager = orig_manager
        assembly_job.translate_vi_to_en = orig_translate


def assemble_short(bundle, wav_path: Path, timing: dict, out_path: Path,
                   pexels_key: str, bgm_path: Path | None = None,
                   logo_path: Path | None = None, subtitles=None,
                   caption_border: str = "outline",
                   beat_text: bool = True,
                   beat_colour_bgr: str = HIGHLIGHT_YELLOW_BGR,
                   broll_pattern: str = "vpvp") -> AssembleResult:
    """Dựng một Short 9:16 hoàn chỉnh: B-roll + caption karaoke + nhạc nền."""
    _ensure_importable()
    from core.pipeline.bgm import BGMConfig
    from core.pipeline.logo_overlay import LogoConfig
    from core.pipeline.stages import ProcessingState
    from core.pipeline.video_effects import IntensityLevel
    from core.stockfootage.assembly_job import AssemblyJob, run_assembly_job
    from core.stockfootage.providers.pexels import PexelsProvider

    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Trộn video + ẢNH. Cảnh 1 (hero) luôn là video -- chuyển động ngay từ
    # khung đầu giữ người xem tốt hơn ảnh tĩnh. Các cảnh sau xen kẽ: ảnh cho
    # những hình cụ thể mà kho video mỏng (xem docstring providers.py), và
    # xen kẽ cũng tránh cả video thành chuỗi clip stock nhìn giống hệt nhau.
    from factory.providers import CompositeProvider, PexelsPhotoProvider
    provider = CompositeProvider(
        [PexelsProvider(api_key=pexels_key),
         PexelsPhotoProvider(pexels_key, width=SHORT_WIDTH, height=SHORT_HEIGHT)],
        pattern=broll_pattern,
        seed=getattr(bundle, "slug", ""),
    )
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
            subtitles=subtitles or tiktok_caption_config(),
            bgm=BGMConfig(path=str(bgm_path.resolve())) if bgm_path else None,
            logo=LogoConfig(path=str(logo_path.resolve())) if logo_path else None,
        )
        warnings: list[str] = []
        with (
            _patched(timing, list(bundle.broll_queries)),
            _caption_border(caption_border),
            _beat_text(timing, beat_colour_bgr, beat_text, getattr(bundle, "thumbnail_text", "") or ""),
        ):
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


# ─── Beat text ────────────────────────────────────────────────────────────
#
# Caption chạy dưới đáy khung suốt video. Beat text thì KHÁC HẲN: chữ rất
# to, giữa khung, chỉ xuất hiện ở đúng hai thời điểm quyết định -- câu HOOK
# (giữ người xem lại) và câu CHỐT (đọng lại sau khi xem).
#
# Vì sao chỉ hai chỗ: nếu câu nào cũng phóng to thì không câu nào còn nổi
# bật, và chữ to che mất B-roll suốt video. Nhấn mạnh chỉ có giá trị khi nó
# hiếm.
#
# Cách làm: chèn thêm dòng Dialogue vào chính file .ass mà video-editor vừa
# ghi, dùng override tag inline (\an5 = giữa khung, \fs = cỡ chữ, \bord =
# viền) thay vì khai báo Style thứ hai. Lý do: Style thứ hai phải chen vào
# đúng khối [V4+ Styles] và dễ vỡ khi họ đổi header; override tag chỉ nằm
# trong dòng Dialogue, không đụng cấu trúc file.
#
# DẤU TIẾNG VIỆT: cỡ chữ lớn + viền dày là đúng tổ hợp dễ cắt cụt dấu nhất.
# Nên beat text đặt \an5 (giữa khung theo CẢ chiều dọc) -- có không gian
# trên dưới thoải mái, khác caption bị ép sát đáy. Viền 8 ở cỡ 150 tương
# đương tỉ lệ viền 5 ở cỡ 96 của caption, tức không dày hơn về tỉ lệ.

BEAT_FONT_SIZE = 150        # cỡ TỐI ĐA; _fit_beat() co xuống nếu câu dài
BEAT_MIN_FONT_SIZE = 70
BEAT_MAX_LINES = 3
BEAT_SAFE_WIDTH = SHORT_WIDTH * 0.82   # chừa biên hai bên, xem _fit_beat()
BEAT_CHAR_RATIO = 0.52      # bề rộng TB mỗi ký tự / cỡ chữ, Be Vietnam Pro Bold
BEAT_OUTLINE = 8
BEAT_FADE_MS = 200
BEAT_POP_MS = 140           # nửa thời gian của hiệu ứng bật ra


def _ass_time(sec: float) -> str:
    cs = int(round(sec * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


def _fit_beat(text: str) -> tuple[int, str]:
    """Chọn cỡ chữ + ngắt dòng sao cho beat text KHÔNG tràn khung.

    LỖI THẬT đã sửa ở đây: bản đầu đặt cứng \\fs150 cho mọi câu. Câu hook
    dài 11 từ ở cỡ đó rộng gấp nhiều lần khung 1080px nên chữ tràn ra ngoài
    hai bên. \\an5 căn giữa nhưng KHÔNG tự xuống dòng -- ASS chỉ ngắt dòng ở
    \\N do ta đặt.

    Cách ước lượng: Be Vietnam Pro Bold rộng trung bình ~0,52 lần cỡ chữ mỗi
    ký tự. Đây là xấp xỉ, nên trừ hao biên khá rộng (BEAT_SAFE_WIDTH chỉ
    lấy 82% chiều ngang khung) thay vì tính chính xác từng glyph -- sai số
    làm chữ nhỏ hơn một chút thì không sao, tràn khung thì hỏng hẳn.
    """
    words = text.split()
    for size in range(BEAT_FONT_SIZE, BEAT_MIN_FONT_SIZE - 1, -10):
        max_chars = int(BEAT_SAFE_WIDTH / (size * BEAT_CHAR_RATIO))
        if max_chars < 6:
            continue
        lines, cur = [], ""
        for w in words:
            trial = f"{cur} {w}".strip()
            if len(trial) <= max_chars or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        if len(lines) <= BEAT_MAX_LINES and all(len(ln) <= max_chars for ln in lines):
            return size, r"\N".join(lines)
    # Không vừa ở cỡ nhỏ nhất -> cắt bớt còn hơn tràn.
    size = BEAT_MIN_FONT_SIZE
    max_chars = max(6, int(BEAT_SAFE_WIDTH / (size * BEAT_CHAR_RATIO)))
    clipped = text[: max_chars * BEAT_MAX_LINES - 1].rstrip() + "…"
    chunks = [clipped[i:i + max_chars] for i in range(0, len(clipped), max_chars)]
    return size, r"\N".join(chunks[:BEAT_MAX_LINES])


def _beat_lines(timing: dict, colour_bgr: str, hook_text: str = "") -> list[str]:
    """Dialogue beat text cho câu đầu và câu cuối.

    `hook_text` (Bundle.thumbnail_text) thay chữ của cảnh đầu nếu có. LỖI
    THẬT: hook pillar dài tới 22 từ, ở cỡ chữ nhỏ nhất vẫn không vừa 3 dòng
    nên bị cắt còn "…đứng trướ…". Tiêu đề ngắn thì vừa ở cỡ lớn."""
    segs = timing.get("segments") or []
    if len(segs) < 2:
        return []
    out = []
    for k, seg in enumerate((segs[0], segs[-1])):
        text = (hook_text if k == 0 and hook_text.strip()
                else (seg.get("spoken") or seg["text"])).strip().rstrip(".")
        text = text.replace("{", "").replace("}", "").replace("\n", " ")
        size, wrapped = _fit_beat(text)
        start, end = float(seg["start"]), float(seg["end"])

        # HIỆU ỨNG NHẤN: bật ra từ 88% -> 104% -> 100% trong ~280ms đầu.
        # Vọt quá 100% một chút rồi lùi về tạo cảm giác "đập vào" thay vì
        # phóng to đều đều. Chỉ ở lúc xuất hiện -- chữ nhúc nhích suốt thời
        # gian hiển thị thì khó đọc, phản tác dụng.
        t1, t2 = BEAT_POP_MS, BEAT_POP_MS * 2
        pop = (rf"\t(0,{t1},\fscx104\fscy104)"
               rf"\t({t1},{t2},\fscx100\fscy100)")
        # RAW STRING bắt buộc: tag ASS bắt đầu bằng \, mà \a \f \b \3 \N đều
        # là escape hợp lệ của Python -- không dùng rf"" thì Python nuốt mất
        # và libass bỏ qua cả tag. (Lỗi thật, chỉ thấy khi đọc file .ass.)
        tag = (rf"{{\an5\fs{size}\b1\bord{BEAT_OUTLINE}\shad0"
               rf"\c&H{colour_bgr}&\3c&H000000&"
               rf"\fscx88\fscy88{pop}\fad({BEAT_FADE_MS},{BEAT_FADE_MS})}}")
        out.append(f"Dialogue: 1,{_ass_time(start)},{_ass_time(end)},"
                   f"Default,,0,0,0,,{tag}{wrapped}")
    return out


@contextmanager
def _beat_text(timing: dict, colour_bgr: str, enabled: bool, hook_text: str = ""):
    """Chèn beat text vào .ass NGAY SAU khi video-editor ghi xong nó.

    Bọc prepare_subtitles: để nó chạy y như cũ, rồi nối thêm dòng vào file
    kết quả trước khi ffmpeg burn. Không đụng logic caption của họ."""
    if not enabled:
        yield
        return
    _ensure_importable()
    import core.stockfootage.assembly_job as assembly_job

    orig = assembly_job.prepare_subtitles

    def _with_beats(*a, **kw):
        artifacts = orig(*a, **kw)
        lines = _beat_lines(timing, colour_bgr, hook_text)
        if lines:
            path = Path(artifacts.ass_path)
            body = path.read_text(encoding="utf-8").rstrip("\n")
            # Layer 1 > layer 0 nên beat text luôn nằm TRÊN caption thường.
            path.write_text(body + "\n" + "\n".join(lines) + "\n", encoding="utf-8")
        return artifacts

    assembly_job.prepare_subtitles = _with_beats
    try:
        yield
    finally:
        assembly_job.prepare_subtitles = orig

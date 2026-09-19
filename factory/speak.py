"""TTS: Bundle.script -> file .wav + timing từng câu.

KHÔNG CÓ LLM Ở ĐÂY, và cũng không cần: lời đọc đã nằm sẵn trong Bundle.

VÌ SAO XUẤT TIMING: bước dựng video cần biết câu nào vang lên lúc nào để
đặt phụ đề và cắt cảnh. v1 giải bài này bằng cách cho video-editor chạy
Whisper phiên âm NGƯỢC lại từ audio -- tốn ~13 giây mỗi short, và tệ hơn,
Whisper đoán sai dấu tiếng Việt nên phụ đề lệch với lời đọc. Vô lý: ta có
sẵn văn bản gốc chính xác 100%, vì chính ta vừa đọc nó ra. Ở đây timing
được ghi lại TRONG LÚC tổng hợp, không đoán lại bao giờ.

ĐƯỜNG CPU/ONNX, CÓ CHỦ ĐÍCH: tài liệu upstream nói thẳng GPU chỉ thắng khi
có lô lớn để lấp, còn văn bản ngắn thì CPU/ONNX nhanh hơn. Short là văn bản
ngắn. Làm phép tính cho 15 short/ngày: 450 giây audio ở RTF ~0.35 là khoảng
2,6 phút máy. Để GPU rảnh cho encode video -- đó mới là chỗ nó tạo khác biệt.
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path

SAMPLE_RATE = 48_000  # v3 Turbo xuất 48 kHz

# Ngắt câu tiếng Việt. Giữ lại dấu câu vì TTS dùng nó để lấy ngữ điệu --
# bỏ đi thì giọng đọc mất chỗ ngắt nghỉ tự nhiên.
_SENTENCE_END = re.compile(r"(?<=[.!?…])\s+|\n+")

# Đánh dấu nhấn mạnh **...** dùng cho chữ trên màn hình, KHÔNG được đọc
# thành lời. v1 từng để lọt dấu sao vào TTS và giọng đọc phát ra "sao sao".
_EMPHASIS = re.compile(r"\*{1,2}(.+?)\*{1,2}")


@dataclass
class Utterance:
    """Một câu, kèm vị trí của nó trong file audio."""
    index: int
    text: str       # văn bản hiển thị, còn giữ **nhấn mạnh**
    spoken: str     # văn bản đã đưa vào TTS, đã bỏ đánh dấu
    start: float
    end: float

    @property
    def duration(self) -> float:
        return self.end - self.start


def strip_emphasis(text: str) -> str:
    """Bỏ **đánh dấu** trước khi đưa vào TTS, giữ nguyên chữ bên trong."""
    return _EMPHASIS.sub(r"\1", text)


def split_sentences(script: str) -> list[str]:
    """Tách kịch bản thành câu để tổng hợp riêng từng câu.

    Tổng hợp theo CÂU chứ không phải cả đoạn là điều kiện để có timing
    chính xác: biết độ dài từng câu thì biết mốc bắt đầu của câu kế tiếp,
    không cần căn chỉnh ngược bằng ASR."""
    parts = [s.strip() for s in _SENTENCE_END.split(script.strip()) if s.strip()]
    return parts


def _load_engine(voice_backend: str = "onnx"):
    """Nạp vieneu một lần, tái dùng cho cả lô.

    Nạp model mất khoảng 6-9 giây; với 465 short mà nạp lại mỗi lần thì
    riêng việc nạp đã hơn một giờ. Import đặt trong hàm để import module
    này không kéo theo cả stack ONNX (test không cần tới nó)."""
    from vieneu import Vieneu
    return Vieneu(backend=voice_backend)


def synthesize(script: str, voice: str, out_wav: Path, engine=None) -> list[Utterance]:
    """Đọc `script` thành `out_wav`, trả về timing từng câu.

    `engine` truyền vào từ ngoài để cả lô dùng chung một model đã nạp; None
    thì tự nạp (tiện khi chạy lẻ một file)."""
    import numpy as np
    import soundfile as sf

    eng = engine or _load_engine()
    sentences = split_sentences(script)
    if not sentences:
        raise ValueError("script rỗng sau khi tách câu")

    chunks: list = []
    utterances: list[Utterance] = []
    cursor = 0.0
    for i, sent in enumerate(sentences):
        spoken = strip_emphasis(sent)
        audio = eng.infer(spoken, voice=voice)
        dur = len(audio) / SAMPLE_RATE
        utterances.append(Utterance(index=i, text=sent, spoken=spoken,
                                    start=round(cursor, 3), end=round(cursor + dur, 3)))
        chunks.append(audio)
        cursor += dur

    out_wav.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out_wav), np.concatenate(chunks), SAMPLE_RATE)
    return utterances


def write_timing(utterances: list[Utterance], out_json: Path) -> Path:
    """Ghi timing ra JSON cho bước dựng video đọc.

    Đây là thứ thay thế hoàn toàn Whisper: bước dựng không bao giờ phải
    đoán lại xem audio đang nói gì."""
    out_json.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "sample_rate": SAMPLE_RATE,
        "duration": round(utterances[-1].end, 3) if utterances else 0.0,
        "segments": [
            {"index": u.index, "text": u.text, "spoken": u.spoken,
             "start": u.start, "end": u.end}
            for u in utterances
        ],
    }
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_json


def write_srt(utterances: list[Utterance], out_srt: Path) -> Path:
    """Phụ đề .srt chính xác 100%, vì dựng từ chính văn bản đã đọc."""
    def ts(sec: float) -> str:
        ms = int(round(sec * 1000))
        h, ms = divmod(ms, 3_600_000)
        m, ms = divmod(ms, 60_000)
        s, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    lines = []
    for u in utterances:
        lines += [str(u.index + 1), f"{ts(u.start)} --> {ts(u.end)}", strip_emphasis(u.text), ""]
    out_srt.parent.mkdir(parents=True, exist_ok=True)
    out_srt.write_text("\n".join(lines), encoding="utf-8")
    return out_srt


def speak_bundle(bundle, out_dir: Path, engine=None) -> dict:
    """Chạy TTS cho một Bundle, xuất .wav + .json + .srt cạnh nhau.

    Trả dict đường dẫn + số đo để caller ghi vào store. Đo rtf để biết máy
    đang chạy nhanh chậm thế nào mà không phải bấm giờ thủ công."""
    base = out_dir / bundle.channel / bundle.slug
    t0 = time.perf_counter()
    utterances = synthesize(bundle.script, bundle.voice, base.with_suffix(".wav"), engine=engine)
    elapsed = time.perf_counter() - t0
    audio_dur = utterances[-1].end if utterances else 0.0

    write_timing(utterances, base.with_suffix(".json"))
    write_srt(utterances, base.with_suffix(".srt"))
    return {
        "wav_path": str(base.with_suffix(".wav")),
        "timing_path": str(base.with_suffix(".json")),
        "srt_path": str(base.with_suffix(".srt")),
        "duration": round(audio_dur, 2),
        "elapsed": round(elapsed, 2),
        "rtf": round(elapsed / audio_dur, 3) if audio_dur else None,
        "n_segments": len(utterances),
    }

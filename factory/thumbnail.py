"""Thumbnail cho Long: một khung hình từ video + chữ to đè lên.

KHÔNG CÓ LLM. Chữ đã nằm sẵn trong Bundle.thumbnail_text -- đó chính là lý
do pha sản xuất không cần trí tuệ.

Short KHÔNG dùng file này: YouTube tự lấy khung hình cho Shorts, và thumbnail
tự đặt không hiển thị trong feed Shorts.

BÀI HỌC TỪ V1 ĐƯỢC SỬA Ở ĐÂY: v1 có `_font()` rơi về ImageFont.load_default()
khi thiếu file font. Bản mặc định đó là bitmap 10px không có glyph tiếng
Việt, nên phép đo bề rộng chữ sụp về gần 0, việc cắt dòng ngừng hoạt động
âm thầm, và thumbnail ra lò với dấu tiếng Việt sai -- không có lỗi nào được
ném. Ở đây thiếu font là lỗi CỨNG: thà không có thumbnail còn hơn có một
cái hỏng mà không ai biết.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIDEO_TOOL_ROOT = ROOT.parent / "video-editor"
FONT_BOLD = VIDEO_TOOL_ROOT / "assets" / "fonts" / "BeVietnamPro-Bold.ttf"
FFMPEG = VIDEO_TOOL_ROOT / "vendor" / "ffmpeg" / "ffmpeg.exe"

SIZE = (1280, 720)
MAX_LINES = 3
START_FONT_SIZE = 96
MIN_FONT_SIZE = 52
SIDE_MARGIN = 72
BAND_ALPHA = 150  # dải tối sau chữ, đủ để chữ trắng luôn đọc được


class ThumbnailError(RuntimeError):
    pass


def grab_frame(video_path: Path, out_jpg: Path, at_sec: float = 2.0) -> Path:
    """Lấy một khung hình làm nền. Dùng ffmpeg đã vendored sẵn trong
    video-editor -- không đòi ffmpeg trên PATH hệ thống."""
    if not FFMPEG.exists():
        raise ThumbnailError(f"Không thấy ffmpeg vendored tại {FFMPEG}")
    out_jpg.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [str(FFMPEG), "-y", "-ss", str(at_sec), "-i", str(video_path),
         "-frames:v", "1", "-q:v", "2", str(out_jpg)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
    )
    if proc.returncode != 0 or not out_jpg.exists():
        raise ThumbnailError(f"ffmpeg không lấy được khung hình: {proc.stderr[-500:]}")
    return out_jpg


def _font(size: int):
    """Font đậm có đủ dấu tiếng Việt. Thiếu là lỗi CỨNG -- xem docstring
    module về cách v1 hỏng âm thầm ở đúng chỗ này."""
    from PIL import ImageFont
    if not FONT_BOLD.exists():
        raise ThumbnailError(
            f"Không thấy font {FONT_BOLD}. Không tự rơi về font mặc định: "
            "bản mặc định của Pillow là bitmap 10px không có glyph tiếng Việt, "
            "sẽ cho ra thumbnail sai dấu mà không báo lỗi."
        )
    return ImageFont.truetype(str(FONT_BOLD), size)


def _wrap(draw, text: str, font, max_width: int) -> list[str]:
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _fit(draw, text: str, max_width: int):
    """Giảm cỡ chữ cho tới khi vừa MAX_LINES dòng. Vẫn không vừa ở cỡ nhỏ
    nhất thì cắt bớt và thêm dấu … -- không bao giờ trả về chữ tràn khung."""
    for size in range(START_FONT_SIZE, MIN_FONT_SIZE - 1, -4):
        font = _font(size)
        lines = _wrap(draw, text, font, max_width)
        if len(lines) <= MAX_LINES:
            return font, lines
    font = _font(MIN_FONT_SIZE)
    lines = _wrap(draw, text, font, max_width)[:MAX_LINES]
    if lines:
        last = lines[-1]
        while last and draw.textbbox((0, 0), last + "…", font=font)[2] > max_width:
            last = last[:-1].rstrip()
        lines[-1] = last + "…"
    return font, lines


def make_thumbnail(video_path: Path, text: str, out_jpg: Path, at_sec: float = 2.0) -> Path:
    """Thumbnail 1280x720: khung hình từ video + dải tối + chữ trắng."""
    from PIL import Image, ImageDraw

    if not text.strip():
        raise ThumbnailError("thumbnail_text rỗng -- Bundle.validate() lẽ ra đã chặn với kind='long'")

    frame = out_jpg.with_suffix(".frame.jpg")
    grab_frame(video_path, frame, at_sec=at_sec)
    img = Image.open(frame).convert("RGB").resize(SIZE, Image.LANCZOS)
    draw = ImageDraw.Draw(img, "RGBA")

    font, lines = _fit(draw, text, SIZE[0] - 2 * SIDE_MARGIN)
    line_h = max(draw.textbbox((0, 0), ln or "M", font=font)[3] for ln in lines) + 14
    block_h = line_h * len(lines)
    top = SIZE[1] - block_h - 96

    draw.rectangle([0, top - 32, SIZE[0], top + block_h + 32], fill=(0, 0, 0, BAND_ALPHA))
    for i, ln in enumerate(lines):
        w = draw.textbbox((0, 0), ln, font=font)[2]
        draw.text(((SIZE[0] - w) // 2, top + i * line_h), ln, font=font, fill=(255, 255, 255))

    out_jpg.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_jpg, "JPEG", quality=90)
    frame.unlink(missing_ok=True)

    # YouTube từ chối thumbnail > 2 MB. Giảm chất lượng dần thay vì để
    # upload fail ở bước cuối.
    for q in (85, 75, 65):
        if out_jpg.stat().st_size <= 2 * 1024 * 1024:
            break
        img.save(out_jpg, "JPEG", quality=q)
    if out_jpg.stat().st_size > 2 * 1024 * 1024:
        raise ThumbnailError("thumbnail vẫn > 2 MB sau khi giảm chất lượng")
    return out_jpg

r"""Đường dẫn công cụ NGOÀI repo -- một chỗ duy nhất, ghi đè được bằng biến môi trường.

Mặc định là máy sản xuất (Windows, C:\Tools\Youtuber). Máy khác (máy thứ hai,
CI) đặt YF_TOOLS_DIR cho cả gốc, hoặc từng biến riêng:

    YF_CREDS_DIR   thư mục credential YouTube (phong_thuy.json, ...)
    YF_PY_TTS      python của venv TTS (vieneu)
    YF_PY_VID      python của venv video-editor
    YF_FFMPEG_DIR  thư mục chứa ffmpeg / ffprobe

Trước đây mỗi đường dẫn viết cứng ở một file (run_pipeline, build_long,
stier/build, srt, repair_titles, channels): đổi máy là sửa sáu chỗ.
"""
from __future__ import annotations

import os
from pathlib import Path


def _env(name: str, default: Path) -> Path:
    v = os.environ.get(name)
    return Path(v) if v else default


TOOLS = _env("YF_TOOLS_DIR", Path(r"C:\Tools\Youtuber"))
CREDS_DIR = _env("YF_CREDS_DIR", TOOLS / "vietneu-tts" / ".youtube_channels")
PY_TTS = _env("YF_PY_TTS", TOOLS / "vietneu-tts" / ".venv" / "Scripts" / "python.exe")
PY_VID = _env("YF_PY_VID", TOOLS / "video-editor" / ".venv-video" / "Scripts" / "python.exe")
FFMPEG_DIR = _env("YF_FFMPEG_DIR", TOOLS / "video-editor" / "vendor" / "ffmpeg")
_EXE = ".exe" if os.name == "nt" else ""
FFMPEG = str(FFMPEG_DIR / f"ffmpeg{_EXE}")
FFPROBE = str(FFMPEG_DIR / f"ffprobe{_EXE}")

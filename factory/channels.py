"""Cấu hình 3 kênh — một chỗ duy nhất. Mọi script nhận --channel FS|CL|BUD.

Mỗi kênh: file credential YouTube, module "dòng nội dung", các tiền tố slug
được phép đăng. Ba kênh nằm trên BA Google Cloud project khác nhau (đã kiểm
21/09/2026), nên mỗi kênh có trần upload ~92/ngày riêng.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

CREDS_DIR = Path(r"C:\Tools\Youtuber\vietneu-tts\.youtube_channels")

CHANNELS = {
    "FS": {"ten": "Phong Thủy", "creds": "phong_thuy.json", "lines": "factory.pillars.topics",
           "prefixes": ("lich-", "giap-", "tru-", "dich-", "menh-")},
    "CL": {"ten": "Hình Sự", "creds": "hinh_su.json", "lines": "factory.lines.cl",
           "prefixes": ("cl-hieusai-", "cl-dieu-", "cl-luadao-", "cl-hoso-", "cl-truyen-")},
    "BUD": {"ten": "Phật Giáo", "creds": "phat_giao.json", "lines": "factory.lines.bud",
            "prefixes": ("bud-lich-", "bud-visao-", "bud-hieulam-", "bud-phapcu-", "bud-sophap-")},
}


def pick(argv: list[str] | None = None, default: str = "FS") -> str:
    """Đọc --channel X từ argv (mặc định FS để lệnh cũ chạy y như trước)."""
    argv = sys.argv if argv is None else argv
    ch = argv[argv.index("--channel") + 1] if "--channel" in argv else default
    if ch not in CHANNELS:
        sys.exit(f"kênh lạ {ch!r} (có: {', '.join(CHANNELS)})")
    return ch


def creds_path(ch: str) -> Path:
    return CREDS_DIR / CHANNELS[ch]["creds"]


def prefixes(ch: str) -> tuple[str, ...]:
    return CHANNELS[ch]["prefixes"]


def lines(ch: str):
    return importlib.import_module(CHANNELS[ch]["lines"])

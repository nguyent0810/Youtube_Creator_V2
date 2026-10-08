"""Cấu hình 3 kênh — một chỗ duy nhất. Mọi script nhận --channel FS|CL|BUD.

Mỗi kênh: file credential YouTube, module "dòng nội dung", các tiền tố slug
được phép đăng. Ba kênh nằm trên BA Google Cloud project khác nhau (đã kiểm
21/09/2026), nên mỗi kênh có trần upload ~92/ngày riêng.

HAI CHỐT AN TOÀN (audit 08/10/2026):
  - Cờ --channel đọc NGHIÊM: `--channel=BUD`, gõ nhầm `--chanel`, hay thiếu
    giá trị đều là lỗi. Bản cũ âm thầm rơi về FS -- `unschedule.py
    --channel=BUD --apply` sẽ gỡ lịch toàn bộ kênh Phong Thủy. Script ghi lên
    kênh thật gọi pick(required=True): không ghi rõ kênh thì không chạy.
  - verify_identity(): kênh mà refresh token THỰC SỰ trỏ tới phải đúng là
    kênh mong đợi. Credential được cấp lại quyền nhầm tài khoản thương hiệu
    là Shorts hình sự lên kênh Phong Thủy và tự công khai đúng giờ.
"""
from __future__ import annotations

import difflib
import importlib
import json
import sys
from pathlib import Path

from factory import paths

CREDS_DIR = paths.CREDS_DIR      # YF_CREDS_DIR / YF_TOOLS_DIR (factory/paths.py)

CHANNELS = {
    "FS": {"ten": "Phong Thủy", "creds": "phong_thuy.json", "lines": "factory.pillars.topics",
           "prefixes": ("lich-", "giap-", "tru-", "dich-", "menh-")},
    "CL": {"ten": "Hình Sự", "creds": "hinh_su.json", "lines": "factory.lines.cl",
           "prefixes": ("cl-hieusai-", "cl-dieu-", "cl-luadao-", "cl-hoso-", "cl-truyen-", "cl-hs-")},
    "BUD": {"ten": "Phật Giáo", "creds": "phat_giao.json", "lines": "factory.lines.bud",
            "prefixes": ("bud-lich-", "bud-visao-", "bud-hieulam-", "bud-phapcu-", "bud-sophap-")},
}

# Dòng CHỈ được đăng từng video một (motion/stier/upload_one.py, drip.py).
# 30/09/2026 kênh CL nhận 61 video trong một ngày và YouTube ngừng đẩy Shorts
# của kênh -- publish_batch.py không bao giờ đăng hàng loạt các dòng này.
# Chúng cũng không theo nhịp "mỗi ngày đúng một video" của các dòng khác.
DRIP_ONLY = {"CL": ("cl-hs-",)}


class ChannelMismatch(SystemExit):
    """Credential trỏ vào kênh khác kênh mong đợi. Dừng ngay, không ghi gì."""


def _channel_arg(argv: list[str]) -> str | None:
    ch = None
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--channel":
            if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
                sys.exit("--channel cần giá trị: FS | CL | BUD")
            ch = argv[i + 1]
            i += 2
            continue
        if a.startswith("--channel="):
            ch = a.split("=", 1)[1]
        elif a.startswith("--") and difflib.SequenceMatcher(None, a[2:].lower(), "channel").ratio() >= 0.75:
            sys.exit(f"cờ lạ {a!r} -- ý là --channel? Dùng đúng: --channel FS|CL|BUD")
        i += 1
    return ch


def pick(argv: list[str] | None = None, default: str | None = "FS", required: bool = False) -> str:
    """Đọc kênh từ argv (`--channel X` hoặc `--channel=X`).

    required=True cho script GHI lên kênh thật: không có --channel là dừng,
    không bao giờ đoán là FS."""
    argv = sys.argv if argv is None else argv
    ch = _channel_arg(argv)
    if ch is None:
        if required or default is None:
            sys.exit("script này thao tác trên kênh thật: phải ghi rõ --channel FS|CL|BUD")
        ch = default
    ch = ch.strip().upper()
    if ch not in CHANNELS:
        sys.exit(f"kênh lạ {ch!r} (có: {', '.join(CHANNELS)})")
    return ch


def args_without_channel(argv: list[str] | None = None) -> list[str]:
    """argv[1:] đã bỏ `--channel X` / `--channel=X` -- cho script đọc tham số vị trí."""
    argv = sys.argv if argv is None else argv
    out, i = [], 1
    while i < len(argv):
        if argv[i] == "--channel":
            i += 2
            continue
        if not argv[i].startswith("--channel="):
            out.append(argv[i])
        i += 1
    return out


def creds_path(ch: str) -> Path:
    return CREDS_DIR / CHANNELS[ch]["creds"]


def load_creds(ch: str) -> dict:
    return json.loads(creds_path(ch).read_text(encoding="utf-8"))


def prefixes(ch: str) -> tuple[str, ...]:
    return CHANNELS[ch]["prefixes"]


def drip_only(ch: str) -> tuple[str, ...]:
    return DRIP_ONLY.get(ch, ())


def bulk_prefixes(ch: str) -> tuple[str, ...]:
    """Tiền tố publish_batch được đăng hàng loạt (bỏ các dòng chỉ-đăng-lẻ)."""
    return tuple(p for p in prefixes(ch) if p not in drip_only(ch))


def lines(ch: str):
    return importlib.import_module(CHANNELS[ch]["lines"])


def verify_identity(ch: str, token: str, conn=None) -> dict:
    """Kênh mà token trỏ tới có đúng là kênh `ch` không. Trả {id, title, uploads}.

    Hai lớp, không cần cấu hình tay:
      - Ghim tay (nếu có): trường "channel_id" trong file credential.
      - Tin lần đầu, khoá về sau: lần đầu thấy kênh nào thì ghi ID vào
        state.sqlite; từ đó ID đổi là dừng. Đồng thời cấm hai kênh
        FS/CL/BUD cùng trỏ vào MỘT kênh YouTube.
    Tốn 1 đơn vị quota (channels.list)."""
    from factory import publish, store

    ident = publish.channel_identity(token)
    label = f"{ident['title']} ({ident['id']})"
    pinned = load_creds(ch).get("channel_id")
    if pinned and pinned != ident["id"]:
        raise ChannelMismatch(f"DỪNG: credential {ch} trỏ vào kênh {label}, nhưng file credential ghim "
                              f"channel_id={pinned}. Không ghi gì lên kênh.")

    def _check(c):
        rows = {r["channel"]: r for r in c.execute("SELECT channel, channel_id, title FROM channel_identity")}
        for other, r in rows.items():
            if other != ch and r["channel_id"] == ident["id"]:
                raise ChannelMismatch(f"DỪNG: credential {ch} trỏ vào kênh {label} -- kênh này đã ghi "
                                      f"nhận là của {other}. Kiểm tra lại file {CHANNELS[ch]['creds']}.")
        if ch in rows and rows[ch]["channel_id"] != ident["id"]:
            raise ChannelMismatch(
                f"DỪNG: credential {ch} giờ trỏ vào {label}, nhưng lần trước là "
                f"{rows[ch]['title']} ({rows[ch]['channel_id']}). Nếu cố ý đổi kênh: xoá dòng {ch} "
                "trong bảng channel_identity của state.sqlite rồi chạy lại.")
        if ch not in rows:
            c.execute("INSERT INTO channel_identity (channel, channel_id, title, first_seen) VALUES (?, ?, ?, ?)",
                      (ch, ident["id"], ident["title"], store._now()))
            print(f"[{ch}] ghi nhận kênh {label} -- từ nay credential trỏ sang kênh khác là dừng. "
                  f"Muốn ghim cứng: thêm \"channel_id\": \"{ident['id']}\" vào {CHANNELS[ch]['creds']}.")

    if conn is not None:
        _check(conn)
    else:
        with store.connect() as c:
            _check(c)
    return ident

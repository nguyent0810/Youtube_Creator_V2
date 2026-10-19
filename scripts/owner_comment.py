"""Đăng MỘT bình luận của chủ kênh dưới một video (để ghim tay trong Studio/trang xem).

    python scripts/owner_comment.py --channel CK <video_id> "nội dung"
    python scripts/owner_comment.py --channel CK <video_id> "nội dung" --dry

API YouTube KHÔNG có lệnh ghim: ghim phải bấm trên giao diện. Script chỉ đăng và ghi sổ
output/channels/<CH>/owner_comments.json để không đăng trùng (một video một bình luận).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, publish  # noqa: E402
from factory.console import utf8_console  # noqa: E402


def main() -> None:
    utf8_console()
    ch = channels.pick()
    pos = [a for a in sys.argv[1:] if not a.startswith("--") and a != ch]
    if len(pos) != 2:
        raise SystemExit(__doc__)
    vid, text = pos
    book = ROOT / "output" / "channels" / ch / "owner_comments.json"
    done = json.loads(book.read_text(encoding="utf-8")) if book.exists() else {}
    if vid in done:
        raise SystemExit(f"{vid}: đã có bình luận chủ kênh ({done[vid]['comment_id']})")
    if "--dry" in sys.argv:
        print(f"[dry] {ch} {vid}: {text}")
        return
    tok = publish.access_token(json.loads(channels.creds_path(ch).read_text(encoding="utf-8")))
    r = publish._api(tok, "POST", "commentThreads", {"part": "snippet"}, {
        "snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": text}}}})
    done[vid] = {"comment_id": r["id"], "text": text, "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                 "pinned": False}
    book.parent.mkdir(parents=True, exist_ok=True)
    book.write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{ch} {vid}: đã đăng {r['id']} (chưa ghim)")


if __name__ == "__main__":
    main()

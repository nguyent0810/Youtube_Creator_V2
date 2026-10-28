"""Đưa Short S-tier của kênh Biểu Đồ Biết Nói (CK, theme "ck") vào kho -- CHỈ vào kho, không upload.

    python motion/stier/enqueue_ck.py <slug> "YYYY-MM-DD HH:MM" [<slug> "..." ...]   # giờ VN

Cần output/stier/<slug>/final.mp4 (build.py không --draft). Mô tả = mô tả spec (đã gồm câu "Nội dung giáo dục,
không phải tư vấn đầu tư.") + nguồn + ghi công ảnh/clip + ghi công nhạc (CC BY, bắt buộc) + hashtag.
Script này KHÔNG gọi API YouTube; item dừng ở stage "assembled" để người duyệt trước khi đăng.
Bản gốc: enqueue_mim.py (kênh MIM).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from factory import store  # noqa: E402
from factory.bundle import Bundle  # noqa: E402

SPECS = ROOT / "data" / "stier" / "specs"
OUT = ROOT / "output" / "stier"
HASHTAGS = "#TàiChínhCáNhân #BiểuĐồBiếtNói"
DISCLAIMER = "Nội dung giáo dục, không phải tư vấn đầu tư."


def credit_lines(od: Path) -> list[str]:
    """Dòng ghi công ảnh/clip (output/stier/<slug>/credits.json do build.py ghi), không trùng, giữ thứ tự."""
    p = od / "credits.json"
    return list(dict.fromkeys(c["text"] for c in json.loads(p.read_text(encoding="utf-8")))) if p.exists() else []


def bundle_for(slug: str, when_vn: str) -> Bundle:
    spec = json.loads((SPECS / f"{slug}.json").read_text(encoding="utf-8"))
    if spec.get("theme") != "ck":
        raise SystemExit(f"{slug}: không phải spec kênh CK (theme={spec.get('theme')!r})")
    if DISCLAIMER not in spec["description"]:
        raise SystemExit(f"{slug}: mô tả thiếu câu miễn trừ \"{DISCLAIMER}\" (luật cứng kênh CK)")
    music = json.loads((OUT / slug / "music.json").read_text(encoding="utf-8"))
    when = (datetime.strptime(when_vn, "%Y-%m-%d %H:%M") - timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    media = credit_lines(OUT / slug)
    desc = "\n\n".join([spec["description"], "Nguồn:\n" + "\n".join(spec["sources"]),
                         "\n".join(media + [music["credit"]]), HASHTAGS])
    # KHÔNG cắt cụt: cắt đuôi là mất đúng dòng ghi công CC BY bắt buộc -> để validate() báo lỗi.
    return Bundle(channel="CK", kind="short", slug=slug, script=" ".join(spec["lines"]), title=spec["title"],
                  description=desc, tags=spec["tags"][:15], thumbnail_text="", publish_at=when,
                  voice=spec.get("voice", "Ngọc Huyền"), bgm=music["file"], broll_queries=[],
                  render={"engine": "casefile", "spec": f"data/stier/specs/{slug}.json", **({"profile": "bang-tra"} if spec.get("profile") == "bang-tra" else {})},
                  source_note="; ".join(spec["sources"]))


def main() -> None:
    args = sys.argv[1:]
    if not args or len(args) % 2:
        raise SystemExit(__doc__)
    with store.connect() as conn:
        for slug, when in zip(args[::2], args[1::2]):
            fin = OUT / slug / "final.mp4"
            if not fin.exists():
                raise SystemExit(f"chưa có {fin} -- chạy build.py {slug} (không --draft)")
            b = bundle_for(slug, when)
            b.validate()
            if not store.bundle_path(b).exists():
                store.save_bundle(b)
            store.enqueue(b, conn)
            row = conn.execute("SELECT stage FROM item WHERE id = ?", (b.id,)).fetchone()
            if row["stage"] != "published":
                store.mark(conn, b.id, "assembled", video_path=str(fin))
            print(f"{slug}: {row['stage']} -> assembled  hẹn {when} VN ({b.publish_at})")


if __name__ == "__main__":
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    main()

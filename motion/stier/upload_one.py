"""Đăng ĐÚNG MỘT hồ sơ S-tier lên kênh Hình Sự, với giờ hẹn chỉ định (private + publishAt).

    python motion/stier/upload_one.py <slug> "2026-10-05 18:30"     # giờ VN
    python motion/stier/upload_one.py <slug> "2026-10-05 18:30" --dry

VÌ SAO CÓ FILE NÀY (04/10/2026): ngày 30/09 kênh CL nhận 61 video trong một ngày
(~53 video trong 47 phút, lô S-tier upload hàng loạt) và 1-2 ngày sau YouTube ngừng
đẩy short của kênh lên feed. Từ nay mỗi lần chỉ upload MỘT video, cách nhau vài giờ,
thường là trong ngày phát sóng -- không bao giờ đổ cả lô lên kênh.

- Slug trong store: "cl-hs-<slug>", giống enqueue.py (không upload trùng nếu đã có video_id).
- Chống trùng tiêu đề với toàn bộ video trên kênh (publish_bundle known_titles + novelty).
- Không bao giờ public ngay.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from factory import channels, publish, store  # noqa: E402
from factory.bundle import Bundle  # noqa: E402
from factory.lines import novelty  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from enqueue import FOOT, OUT, SPECS  # noqa: E402

LOG = OUT / "uploads.json"


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    s, vn = sys.argv[1], sys.argv[2]
    dry = "--dry" in sys.argv
    when = (datetime.strptime(vn, "%Y-%m-%d %H:%M") - timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    if datetime.strptime(when, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) < \
            datetime.now(timezone.utc) + timedelta(minutes=30):
        raise SystemExit(f"giờ hẹn {vn} VN đã quá sát hoặc đã qua -- chọn giờ muộn hơn")
    spec = json.loads((SPECS / f"{s}.json").read_text(encoding="utf-8"))
    fin = OUT / s / "final.mp4"
    if not fin.exists():
        raise SystemExit(f"chưa có {fin}")
    # Video phải MỚI HƠN spec (cùng luật với enqueue.py / queue2.sh): spec vừa sửa
    # mà chưa dựng lại thì đăng là lời đọc CŨ dưới tiêu đề/mô tả MỚI. Đang dựng
    # dở (thư mục LOCK) thì có thể là MP4 viết dở.
    if fin.stat().st_mtime < (SPECS / f"{s}.json").stat().st_mtime - 5:
        raise SystemExit(f"{fin} CŨ hơn spec -- dựng lại trước khi đăng (motion/stier/build.py {s})")
    if (OUT / s / "LOCK").exists():
        raise SystemExit(f"{s} đang được dựng (có thư mục LOCK) -- chờ dựng xong")
    slug = f"cl-hs-{s}"
    with store.connect() as conn:
        row = conn.execute("SELECT stage, video_id FROM item WHERE channel='CL' AND slug=?", (slug,)).fetchone()
        if row and row["video_id"]:
            raise SystemExit(f"{slug} đã đăng rồi: {row['video_id']}")
        dup = novelty.duplicate_on_channel("CL", spec["title"])
        if dup:
            raise SystemExit(f"TRÙNG CHỦ ĐỀ với video đã có: '{dup['title']}'")
        tags = spec.get("hashtags") or FOOT.split("\n\n")[-1]
        if spec.get("fiction"):        # truyện hư cấu: không có nguồn/ảnh Commons
            desc = spec["description"] + "\n\n" + tags
        else:
            desc = (spec["description"] + "\n\nNguồn: " + "; ".join(spec.get("sources", [])) + "\n\n"
                    + FOOT.split("\n\n")[0].replace("dưới đây", "trên") + "\n\n" + tags)
        b = Bundle(channel="CL", kind="short", slug=slug, script=" ".join(spec["lines"]), title=spec["title"][:100],
                   description=desc[:5000], tags=spec.get("tags", [])[:12], thumbnail_text=spec["title"][:60],
                   publish_at=when, voice="Anh Khôi", bgm="", broll_queries=["hyperframes-casefile"],
                   source_note="; ".join(spec.get("sources", [])))
        b.validate()
        print(f"{vn} VN ({when})  {slug}  {spec['title']}")
        if dry:
            print(desc)
            print("CHẠY KHÔ: không upload")
            return
        # Bundle S-tier sinh từ spec (spec là nguồn), item chưa có video -> ghi đè
        # được; enqueue đồng bộ publish_at mới vào store (bản cũ giữ giờ cũ).
        store.save_bundle(b, overwrite=True)
        store.enqueue(b, conn)
        creds = channels.load_creds("CL")
        tok = publish.access_token(creds)
        with store.locked(conn, "publish-CL"):
            ident = channels.verify_identity("CL", tok, conn)
            store.mark(conn, b.id, "assembled", video_path=str(fin))
            titles = publish.channel_titles(ident["uploads"], tok)
            res = publish.publish_bundle(b, fin, creds, token=tok, known_titles=titles)
            store.mark(conn, b.id, "published", video_id=res.video_id)
            for w in res.warnings:
                print("cảnh báo:", w)
    log = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else []
    log.append({"slug": s, "video_id": res.video_id, "publish_at": when,
                "uploaded": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "title": spec["title"]})
    LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK {res.url}  hẹn {res.scheduled_at}")


if __name__ == "__main__":
    main()

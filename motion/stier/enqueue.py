"""Đưa các hồ sơ S-tier đã dựng (output/stier/<slug>/final.mp4) vào store để publish_batch đăng.

    python motion/stier/enqueue.py --start 2026-10-06 [--dry] [--limit N]

- Slug trên kênh: "cl-hs-<slug>". Mỗi ngày 5 khung giờ của kênh Hình Sự (giờ VN).
- Xếp xen kẽ theo nhóm chủ đề để các ngày liền nhau không lặp khuôn (YPP 07/2025).
- Chống trùng: tiêu đề so với toàn bộ video trên kênh (factory.lines.novelty); trùng thì BỎ, không đăng.
- Không bao giờ đè item đã có video_id (store.enqueue là "ON CONFLICT DO NOTHING").
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from factory import store  # noqa: E402
from factory.bundle import Bundle  # noqa: E402
from factory.lines import novelty  # noqa: E402

SPECS = ROOT / "data" / "stier" / "specs"
OUT = ROOT / "output" / "stier"
SLOTS_VN = ["07:00", "11:30", "15:00", "19:00", "22:00"]
FOOT = ("Ảnh tư liệu: Wikimedia Commons (phạm vi công cộng). Dữ kiện đối chiếu với các nguồn dưới đây; "
        "chỗ nào là diễn ý đã ghi rõ trên hình.\n\n#hồsơvụán #vụánlịchsử #hìnhsự #shorts")


def args():
    a = sys.argv[1:]
    start = a[a.index("--start") + 1] if "--start" in a else "2026-10-15"
    limit = int(a[a.index("--limit") + 1]) if "--limit" in a else 999
    only = a[a.index("--only") + 1].split(",") if "--only" in a else None
    return start, "--dry" in a, limit, only


def main():
    start, dry, limit, only = args()
    ready = []
    for f in sorted(SPECS.glob("*.json")):
        s = f.stem
        if only and s not in only:
            continue
        fin = OUT / s / "final.mp4"
        if s == "monalisa":
            fin = OUT / "monalisa_stier.mp4"
        if fin.exists() and fin.stat().st_mtime >= f.stat().st_mtime - 5:
            ready.append((s, json.loads(f.read_text(encoding="utf-8")), fin))
    # Xen kẽ: thứ tự đã trộn sẵn theo tên để tránh các vụ cùng loại liền nhau
    order = sorted(ready, key=lambda r: (sum(ord(c) * (i + 3) for i, c in enumerate(r[0])) % 97, r[0]))
    with store.connect() as conn:
        used = {r[0] for r in conn.execute("SELECT publish_at FROM item WHERE channel='CL' AND publish_at IS NOT NULL")}
    day = datetime.strptime(start, "%Y-%m-%d")
    slots = []
    while len(slots) < len(order) + 20:
        for hm in SLOTS_VN:
            h, m = map(int, hm.split(":"))
            utc = (day + timedelta(hours=h, minutes=m) - timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
            if utc not in used:
                slots.append(utc)
        day += timedelta(days=1)
    done, skipped = 0, []
    with store.connect() as conn:
        for s, spec, fin in order:
            if done >= limit:
                break
            slug = f"cl-hs-{s}"
            row = conn.execute("SELECT stage, video_id FROM item WHERE channel='CL' AND slug=?", (slug,)).fetchone()
            if row:
                skipped.append(f"{s}: đã có trong store ({row['stage']})")
                continue
            dup = novelty.duplicate_on_channel("CL", spec["title"])
            if dup:
                skipped.append(f"{s}: TRÙNG CHỦ ĐỀ với '{dup['title']}'")
                continue
            when = slots.pop(0)
            desc = spec["description"] + "\n\nNguồn: " + "; ".join(spec.get("sources", [])) + "\n\n" + FOOT
            b = Bundle(channel="CL", kind="short", slug=slug, script=" ".join(spec["lines"]), title=spec["title"][:100],
                       description=desc[:5000], tags=spec.get("tags", [])[:12], thumbnail_text=spec["title"][:60],
                       publish_at=when, voice="Anh Khôi", bgm="", broll_queries=["hyperframes-casefile"],
                       source_note="; ".join(spec.get("sources", [])))
            b.validate()
            vn = (datetime.strptime(when, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=7)).strftime("%d/%m %H:%M")
            print(f"  {vn} VN  {slug:28} {spec['title'][:70]}")
            if not dry:
                store.save_bundle(b)
                store.enqueue(b, conn)
                wav = OUT / s / "voice.wav"
                store.mark(conn, b.id, "assembled", video_path=str(fin), wav_path=str(wav) if wav.exists() else None,
                           timing_path=str(OUT / s / "timing.json"))
            done += 1
    print(f"{'CHẠY KHÔ — ' if dry else ''}xếp lịch {done} video S-tier" + (f" · bỏ {len(skipped)}:" if skipped else ""))
    for x in skipped:
        print("   -", x)


if __name__ == "__main__":
    main()

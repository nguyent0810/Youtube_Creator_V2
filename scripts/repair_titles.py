"""Sửa hậu quả của lỗi tiêu đề trùng.

BỐI CẢNH: tiêu đề sinh từ (sao, trực), mà chu kỳ sao/trực lặp đúng 12 ngày.
Tháng 10/2026 có 9 cặp ngày trùng tiêu đề. Bộ chống trùng của publish.py so
theo tiêu đề nên đã BỎ QUA 9 lần upload, và store ghi nhầm 9 ngày đó là đã
đăng — trỏ vào video_id của ngày khác.

Hai việc phải làm, theo đúng thứ tự:
  1. Đổi tiêu đề 21 video đã đăng đúng sang dạng mới (có ngày ở đầu).
     Phải làm TRƯỚC, nếu không 9 lần upload lại sẽ tiếp tục đụng tiêu đề cũ.
  2. Đưa 9 ngày bị bỏ sót về assembled để upload lại.

videos.update tốn 50 đơn vị/lần: 21 × 50 = 1.050, thừa sức trong 10.000/ngày.
"""
import collections
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import publish, store  # noqa: E402

CREDS = Path(r"C:\Tools\Youtuber\vietneu-tts\.youtube_channels\phong_thuy.json")
tok = publish.access_token(json.loads(CREDS.read_text(encoding="utf-8")))

with store.connect() as conn:
    rows = [dict(r) for r in conn.execute(
        "SELECT * FROM item WHERE slug LIKE 'lich-%' ORDER BY publish_at")]

# Ngày nào thật sự SỞ HỮU video_id đó = ngày ĐẦU TIÊN dùng nó (ngày được
# upload thật). Các ngày sau chỉ là nạn nhân của dedup.
owner: dict[str, str] = {}
for r in rows:
    owner.setdefault(r["video_id"], r["slug"])

real = [r for r in rows if owner[r["video_id"]] == r["slug"]]
orphan = [r for r in rows if owner[r["video_id"]] != r["slug"]]

print(f"{len(real)} ngày có video riêng, {len(orphan)} ngày bị bỏ sót\n")

print("=== 1. Đổi tiêu đề video đã đăng đúng ===")
for i, r in enumerate(real, 1):
    b = store.load_bundle("FS", r["slug"])
    try:
        cur = publish._api(tok, "GET", "videos",
                           {"part": "snippet,status", "id": r["video_id"]})["items"][0]
        if cur["snippet"]["title"] == b.title:
            print(f"  [{i}/{len(real)}] {r['slug']}  đã đúng, bỏ qua")
            continue
        publish._api(tok, "PUT", "videos", {"part": "snippet"}, {
            "id": r["video_id"],
            "snippet": {
                "title": b.title,
                "description": cur["snippet"].get("description", ""),
                "tags": cur["snippet"].get("tags", []),
                "categoryId": cur["snippet"].get("categoryId", "22"),
                "defaultLanguage": "vi",
            },
        })
        print(f"  [{i}/{len(real)}] {r['slug']}  -> {b.title[:55]}")
    except Exception as exc:
        print(f"  [{i}/{len(real)}] {r['slug']}  LỖI: {exc}")
    time.sleep(1)

print(f"\n=== 2. Đưa {len(orphan)} ngày bị bỏ sót về assembled ===")
with store.connect() as conn:
    for r in orphan:
        conn.execute(
            "UPDATE item SET stage='assembled', video_id=NULL, attempts=0 WHERE id=?",
            (r["id"],))
        print(f"  {r['slug']}  (trước trỏ nhầm vào {r['video_id']})")
    print("\ntrạng thái:", store.summary(conn))

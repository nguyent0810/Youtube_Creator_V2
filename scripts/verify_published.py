"""Xác minh trạng thái thật trên YouTube — không tin store.

Store chỉ ghi lại thứ ta NGHĨ đã xảy ra. Lần chạy `run` đầu tiên là ví dụ:
store ghi 30 item "đã đăng" trong khi thực tế chỉ 21 video lên kênh, 9 cái
còn lại trỏ vào video của ngày khác. Nếu không hỏi thẳng YouTube thì lỗi đó
đi thẳng lên kênh.

Thoát khác 0 nếu có bất kỳ sai lệch nào -- để bộ điều phối dừng lại.
"""
import collections
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import publish, store  # noqa: E402

CREDS = Path(r"C:\Tools\Youtuber\vietneu-tts\.youtube_channels\phong_thuy.json")
PREFIX = sys.argv[1] if len(sys.argv) > 1 else "lich-"

tok = publish.access_token(json.loads(CREDS.read_text(encoding="utf-8")))
with store.connect() as conn:
    rows = [dict(r) for r in conn.execute(
        "SELECT slug, video_id, publish_at FROM item "
        "WHERE slug LIKE ? AND video_id IS NOT NULL ORDER BY publish_at",
        (PREFIX + "%",))]

ids = [r["video_id"] for r in rows]
dup = [k for k, v in collections.Counter(ids).items() if v > 1]
print(f"{len(rows)} item · {len(set(ids))} video_id duy nhất")
if dup:
    print(f"*** TRÙNG video_id: {dup}")

problems = []
for i in range(0, len(ids), 50):
    data = publish._api(tok, "GET", "videos",
                        {"part": "snippet,status", "id": ",".join(ids[i:i + 50])})
    seen = {it["id"] for it in data["items"]}
    for vid in ids[i:i + 50]:
        if vid not in seen:
            problems.append((vid, ["KHÔNG TỒN TẠI trên kênh"]))
    for it in data["items"]:
        r = next(x for x in rows if x["video_id"] == it["id"])
        b = store.load_bundle("FS", r["slug"])
        st, sn = it["status"], it["snippet"]
        p = []
        if st["privacyStatus"] != "private":
            p.append(f"privacy={st['privacyStatus']} (phải private)")
        if st.get("publishAt") != r["publish_at"]:
            p.append(f"lịch {st.get('publishAt')} != {r['publish_at']}")
        if sn["title"] != b.title:
            p.append("tiêu đề lệch bundle")
        if p:
            problems.append((r["slug"], p))

print(f"Đúng hoàn toàn: {len(rows) - len(problems)}/{len(rows)}")
for s, p in problems[:10]:
    print(f"   {s}: {p}")

# THIẾU Ở ĐUÔI -- lỗ hổng thật của bản trước: nó chỉ soi khoảng GIỮA hai mốc
# có thật, nên khi video cuối cùng không đăng được (hết quota), dãy còn lại
# vẫn liền mạch và verify báo ĐẠT. Ngày 31/12 biến mất mà không ai biết.
#
# Đối chiếu với danh sách ngày MONG ĐỢI trong store, không chỉ với những
# ngày đã đăng được.
with store.connect() as conn:
    expected = {r[0] for r in conn.execute(
        "SELECT slug FROM item WHERE slug LIKE ?", (PREFIX + "%",))}
    # Hoãn vì hết quota là trạng thái HỢP LỆ, có mốc tự thử lại -- không
    # phải thiếu. Quá mốc mà vẫn chưa lên kênh thì mới là thiếu.
    wrows = [r for r in store.deferred(conn) if r["slug"].startswith(PREFIX)]
    waiting = {r["slug"]: r["retry_after"] for r in wrows}

# Lịch có đứt ngày nào không — với kênh đăng hằng ngày thì đứt là thấy ngay.
# Ngày đang chờ quota được tính là "có", vì nó sẽ tự lấp.
ds = sorted(datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
            for x in [r["publish_at"] for r in rows] + [r["publish_at"] for r in wrows])
gaps = [(ds[i], ds[i + 1]) for i in range(len(ds) - 1)
        if (ds[i + 1] - ds[i]) != timedelta(days=1)]
print(f"Lịch {ds[0]:%d/%m} → {ds[-1]:%d/%m} · đứt quãng: {len(gaps)}")
for a, b_ in gaps:
    print(f"   {a:%d/%m} → {b_:%d/%m}")
got = {r["slug"] for r in rows}
missing = sorted(expected - got - set(waiting))
print(f"Trong store {len(expected)} ngày · đã lên kênh {len(got)} · "
      f"chờ quota {len(waiting)} · thiếu {len(missing)}")
for s_, w in sorted(waiting.items())[:10]:
    print(f"   CHỜ QUOTA: {s_} (tự đăng sau {w})")
for m in missing[:10]:
    print(f"   THIẾU: {m}")

if problems or dup or gaps or missing:
    sys.exit(f"XÁC MINH THẤT BẠI: {len(problems)} sai lệch, {len(dup)} trùng id, "
             f"{len(gaps)} đứt quãng, {len(missing)} thiếu")
print("XÁC MINH ĐẠT")

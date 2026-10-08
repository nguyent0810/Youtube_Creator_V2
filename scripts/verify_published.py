"""Xác minh trạng thái thật trên YouTube — không tin store.

    python scripts/verify_published.py --channel FS          # mọi dòng
    python scripts/verify_published.py giap- --channel FS    # một dòng

Store chỉ ghi lại thứ ta NGHĨ đã xảy ra. Lần chạy `run` đầu tiên là ví dụ:
store ghi 30 item "đã đăng" trong khi thực tế chỉ 21 video lên kênh, 9 cái
còn lại trỏ vào video của ngày khác. Nếu không hỏi thẳng YouTube thì lỗi đó
đi thẳng lên kênh.

Mỗi dòng (Lịch + 4 pillar) đăng một bài mỗi ngày, nên kiểm RIÊNG từng dòng:
đúng privacy/lịch/tiêu đề, không trùng id, không đứt ngày, không thiếu đuôi.

Thoát khác 0 nếu có bất kỳ sai lệch nào -- để bộ điều phối dừng lại.

Bắt buộc --channel, và tiền tố phải là một dòng của kênh đó: bản cũ coi
`--channel=CL` là tiền tố slug, không thấy item nào, rồi in "XÁC MINH ĐẠT".
Dòng chỉ-đăng-lẻ (S-tier `cl-hs-`, nhiều video/ngày) không bị áp luật "mỗi
ngày đúng một video" -- bản cũ báo 89 "đứt quãng" nên kênh CL KHÔNG BAO GIỜ
đạt, và người vận hành quen bỏ qua cảnh báo. Dòng đó kiểm "không hai video
nào cách nhau dưới 30 phút" thay thế.
"""
import collections
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, publish, store  # noqa: E402

CH = channels.pick(required=True)
ALL = list(channels.prefixes(CH))
_args = [a for a in channels.args_without_channel() if not a.startswith("--")]
if _args and not any(_args[0].startswith(p) or p.startswith(_args[0]) for p in ALL):
    sys.exit(f"tiền tố {_args[0]!r} không thuộc kênh {CH} (có: {', '.join(ALL)})")
PREFIXES = [_args[0]] if _args else ALL
DRIP = channels.drip_only(CH)


def verify(prefix: str, tok: str) -> list[str]:
    """Trả danh sách lỗi của một dòng (rỗng = đạt)."""
    with store.connect() as conn:
        rows = [dict(r) for r in conn.execute(
            "SELECT slug, video_id, publish_at FROM item "
            "WHERE channel = ? AND slug LIKE ? AND video_id IS NOT NULL ORDER BY publish_at", (CH, prefix + "%"))]
        allrows = [dict(r) for r in conn.execute(
            "SELECT slug, stage, publish_at FROM item WHERE channel = ? AND slug LIKE ?", (CH, prefix + "%"))]
        expected = {r["slug"] for r in allrows}
        # Hoãn vì hết quota là trạng thái HỢP LỆ, có mốc tự thử lại -- không
        # phải thiếu. Quá mốc mà vẫn chưa lên kênh thì mới là thiếu.
        wrows = [dict(r) for r in store.deferred(conn) if r["slug"].startswith(prefix)]
    if not expected:
        print("   (chưa có item)")
        return []
    if not rows:
        print(f"   {len(expected)} item trong store, chưa item nào lên kênh")
        return []

    ids = [r["video_id"] for r in rows]
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    print(f"   {len(rows)} item · {len(set(ids))} video_id duy nhất")

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
            b = store.load_bundle(CH, r["slug"])
            st, sn = it["status"], it["snippet"]
            p = []
            # Trước giờ hẹn: phải private + đúng publishAt. Sau giờ hẹn YouTube
            # tự chuyển public và xoá publishAt -- đó là trạng thái đúng.
            if st.get("publishAt"):
                if st["privacyStatus"] != "private":
                    p.append(f"privacy={st['privacyStatus']} (phải private tới giờ hẹn)")
                if st["publishAt"] != r["publish_at"]:
                    p.append(f"lịch {st['publishAt']} != {r['publish_at']}")
            elif st["privacyStatus"] != "public":
                p.append("private mà không có lịch -> sẽ không bao giờ lên")
            if sn["title"] != b.title:
                p.append("tiêu đề lệch bundle")
            if p:
                problems.append((r["slug"], p))
    print(f"   Đúng hoàn toàn: {len(rows) - len(problems)}/{len(rows)}")
    for s, p in problems[:10]:
        print(f"      {s}: {p}")

    # Đứt ngày -- ngày đang chờ quota được tính là "có", vì nó sẽ tự lấp.
    ds = sorted(datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
                for x in [r["publish_at"] for r in rows] + [r["publish_at"] for r in wrows])
    is_drip = bool(DRIP) and prefix.startswith(DRIP)
    if is_drip:
        # Dòng đăng lẻ, nhiều video/ngày: chỉ cấm chồng khung giờ (< 30 phút).
        gaps = [(ds[i], ds[i + 1]) for i in range(len(ds) - 1) if (ds[i + 1] - ds[i]) < timedelta(minutes=30)]
        print(f"   Lịch {ds[0]:%d/%m} → {ds[-1]:%d/%m} · chồng khung giờ (<30'): {len(gaps)}")
    else:
        gaps = [(ds[i], ds[i + 1]) for i in range(len(ds) - 1) if (ds[i + 1] - ds[i]) != timedelta(days=1)]
        print(f"   Lịch {ds[0]:%d/%m} → {ds[-1]:%d/%m} · đứt quãng: {len(gaps)}")
    for a, b_ in gaps[:5]:
        print(f"      {a:%d/%m %H:%M} → {b_:%d/%m %H:%M}")

    # THIẾU Ở ĐUÔI -- lỗ hổng thật của bản đầu: nó chỉ soi khoảng GIỮA hai mốc
    # có thật, nên khi video cuối không đăng được (hết quota) verify vẫn ĐẠT.
    waiting = {r["slug"]: r["retry_after"] for r in wrows}
    got = {r["slug"] for r in rows}
    # "Thiếu" = đã hỏng khi đăng, hoặc nằm LỌT trước ngày cuối đã đăng. Item
    # xếp hàng phía sau (chưa tới lượt đăng) không phải thiếu.
    last = max(r["publish_at"] for r in rows)
    missing = sorted(r["slug"] for r in allrows
                     if r["slug"] not in got and r["slug"] not in waiting
                     and (r["stage"] == "failed" or r["publish_at"] <= last))
    queued = sum(1 for r in allrows if r["slug"] not in got and r["slug"] not in waiting
                 and r["slug"] not in missing)
    print(f"   Store {len(expected)} · lên kênh {len(got)} · chờ quota {len(waiting)} · "
          f"xếp hàng {queued} · thiếu {len(missing)}")
    for m in missing[:10]:
        print(f"      THIẾU: {m}")

    errs = []
    if problems:
        errs.append(f"{len(problems)} sai lệch")
    if dup:
        errs.append(f"{len(dup)} trùng id")
    if gaps:
        errs.append(f"{len(gaps)} {'chồng giờ' if is_drip else 'đứt quãng'}")
    if missing:
        errs.append(f"{len(missing)} thiếu")
    return errs


tok = publish.access_token(channels.load_creds(CH))
channels.verify_identity(CH, tok)
fails = []
for pf in PREFIXES:
    print(f"\n── {pf}")
    errs = verify(pf, tok)
    if errs:
        fails.append(f"{pf} {', '.join(errs)}")
if fails:
    sys.exit("\nXÁC MINH THẤT BẠI: " + " | ".join(fails))
print("\nXÁC MINH ĐẠT")

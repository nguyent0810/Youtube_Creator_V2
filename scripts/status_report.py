"""Sinh STATUS.md: ngày nào đủ 5 dòng, ngày nào thiếu, nội dung từng slot, việc làm tiếp.

    python scripts/status_report.py                 # CẢ 3 kênh -> STATUS.md
    python scripts/status_report.py --channel CL    # một kênh
    python scripts/status_report.py 2026-10-01 2026-11-30 --channel FS

Đọc thẳng store + bundles/, không có sổ riêng -- chạy lại lúc nào cũng
ra trạng thái thật. (Muốn chắc với YouTube thì chạy verify_published.py.)
"""
import collections
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, store  # noqa: E402

VN = timedelta(hours=7)
ICON = {"published": "✅", "assembled": "🎬", "spoken": "🔊", "pending": "📝", "failed": "❌"}
POS = [a for a in sys.argv[1:] if a[:1].isdigit()]
ALL_CH = "--channel" not in sys.argv


def lines_of(ch):
    if ch == "FS":
        return [("lich-", "Lịch Hoàng Đạo", "06:00"), ("giap-", "12 Con Giáp", "11:30"),
                ("tru-", "Lục Trụ", "15:00"), ("dich-", "Kinh Dịch", "19:00"), ("menh-", "Mệnh số", "22:00")]
    L = channels.lines(ch)
    return [(pf, feel[0].upper() + feel[1:], hh) for pf, hh, feel in L.PILLARS.values()]


def report(CH):
  LINES = lines_of(CH)
  N = len(LINES)
  with store.connect() as conn:
    rows = [dict(r) for r in conn.execute("SELECT * FROM item WHERE channel=?", (CH,))]
    deferred = {r["slug"] for r in store.deferred(conn, CH)}
  dates = [(datetime.strptime(r["publish_at"], "%Y-%m-%dT%H:%M:%SZ") + VN).date() for r in rows
           if any(r["slug"].startswith(p) for p, _, _ in LINES)]
  start = date.fromisoformat(POS[0]) if POS else (min(dates) if dates else date.today())
  end = date.fromisoformat(POS[1]) if len(POS) > 1 else (max(dates) if dates else start)

  slot = {}          # (ngày VN, prefix) -> row + title
  for r in rows:
      pf = next((p for p, _, _ in LINES if r["slug"].startswith(p)), None)
      if not pf:
          continue
      d = (datetime.strptime(r["publish_at"], "%Y-%m-%dT%H:%M:%SZ") + VN).date()
      try:
          b = json.loads((store.BUNDLE_DIR / CH / f"{r['slug']}.json").read_text(encoding="utf-8"))
          r["title"] = b["title"]
      except FileNotFoundError:
          r["title"] = "(mất bundle)"
      slot[(d, pf)] = r

  days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
  full, partial, empty = [], [], []
  for d in days:
      n = sum(1 for p, _, _ in LINES if slot.get((d, p), {}).get("stage") == "published")
      (full if n == N else empty if n == 0 else partial).append(d)

  cnt = collections.Counter((p, r["stage"]) for (d, p), r in slot.items())
  last_pub = {p: max((d for (d, pp), r in slot.items() if pp == p and r["stage"] == "published"), default=None)
              for p, _, _ in LINES}

  out = []
  out.append(f"# Trạng thái kênh Phong Thủy (FS)\n")
  out.append(f"_Cập nhật {datetime.now():%d/%m/%Y %H:%M} (giờ máy) · sinh bằng `python scripts/status_report.py`_\n")
  out.append("Giờ trong bảng là giờ Việt Nam. Mọi video đều **riêng tư + hẹn giờ**; YouTube tự công khai đúng giờ.\n")
  out.append("## Tóm tắt\n")
  out.append(f"- Khoảng {start:%d/%m} → {end:%d/%m}: **{len(full)} ngày đủ {N}/{N}**, "
             f"{len(partial)} ngày đăng dở, {len(empty)} ngày chưa có video nào.")
  out.append("- Đã lên kênh theo dòng: " + " · ".join(
      f"{name} **{cnt[(p, 'published')]}** (tới {last_pub[p]:%d/%m})" if last_pub[p] else f"{name} 0"
      for p, name, _ in LINES))
  waiting = [r["slug"] for r in rows if r["slug"] in deferred]
  queued = [r for r in rows if r["stage"] != "published" and any(r["slug"].startswith(p) for p, _, _ in LINES)]
  out.append(f"- Trong hàng đợi chưa đăng: **{len(queued)}** item"
             + (f" (trong đó {len(waiting)} đang chờ quota reset)" if waiting else ""))
  fail = [r for r in queued if r["stage"] == "failed"]
  if fail:
      out.append(f"- ❌ Hỏng cần xem: {', '.join(r['slug'] for r in fail)}")
  out.append("\nKý hiệu: ✅ đã lên kênh · 🎬 dựng xong, chờ đăng · 🔊 có giọng · 📝 có kịch bản · ⏳ chờ quota · ❌ hỏng · — chưa có\n")

  out.append("## Theo ngày\n")
  out.append("| Ngày | " + " | ".join(f"{n} ({h})" for _, n, h in LINES) + " | Đủ |")
  out.append("|---|" + "---|" * (len(LINES) + 1))
  for d in days:
      cells = []
      for p, _, _ in LINES:
          r = slot.get((d, p))
          if not r:
              cells.append("—")
          else:
              ic = "⏳" if r["slug"] in deferred else ICON.get(r["stage"], "?")
              cells.append(f"{ic} {r['title'][:38]}")
      n = sum(1 for p, _, _ in LINES if slot.get((d, p), {}).get("stage") == "published")
      out.append(f"| {d:%a %d/%m} | " + " | ".join(cells) + f" | {n}/{N} |")

  out.append("\n### Làm tiếp\n")
  nxt = min((d for d in days if d not in full), default=None)
  out.append(f"1. Ngày đầu tiên chưa đủ {N}/{N}: **{nxt:%d/%m/%Y}**." if nxt else f"1. Mọi ngày trong khoảng đã đủ {N}/{N}.")
  out.append("2. Quota upload reset **14:00 giờ VN** (07:00 UTC mùa hè, 08:00 UTC mùa đông); "
             "trần thực tế ~92 video/ngày, RIÊNG cho từng kênh.")
  if waiting:
      out.append(f"3. Có item chờ quota → sau giờ reset: `python scripts/run_pipeline.py resume --channel {CH}`")
  if CH == "FS":
      pill_last = min((last_pub[p] for p, _, _ in LINES[1:] if last_pub[p]), default=None)
      if pill_last:
          d0 = pill_last + timedelta(days=1)
          out.append(f"4. Nạp tiếp 4 dòng pillar (18 ngày ≈ 72 upload ≈ 1 ngày quota):\n"
                     f"   `python scripts/run_pipeline.py {d0:%Y-%m-%d} 18 --only pillars`")
      lich_last = last_pub["lich-"]
      if lich_last:
          out.append(f"5. Lịch đã phủ tới {lich_last:%d/%m}. Nạp tiếp tháng 1/2027:\n"
                     f"   `python scripts/run_pipeline.py 2027-01-01 31 --only lich` (Lịch đăng trước 1 ngày)")
      out.append("6. Kinh Dịch: chạy lại `python scripts/fetch_kinhdich.py` định kỳ để nhận thêm quẻ có bản dịch.")
  else:
      L = channels.lines(CH)
      from factory.lines import packs
      used = {r["slug"] for r in rows}
      left = []
      for line, (pf, hh, feel) in L.PILLARS.items():
          if line in getattr(L, "TEMPLATES", {}):
              left.append(f"{line}: khuôn tự động")
          else:
              n_left = sum(1 for e in packs.load(CH, line) if f"{pf}{e['key']}" not in used)
              left.append(f"{line}: còn {n_left} kịch bản chưa dùng")
      last_any = max((d for (d, pp), r in slot.items()), default=None)
      d0 = (last_any + timedelta(days=1)) if last_any else date.today()
      out.append(f"4. Gói kịch bản còn lại: " + " · ".join(left))
      out.append(f"   Hết gói thì viết thêm vào `data/packs/{CH}/<dòng>.json` (Claude viết trong chat), rồi chạy:\n"
                 f"   `python scripts/run_pipeline.py {d0:%Y-%m-%d} 7 --channel {CH}`")
  out.append(f"7. Sau mỗi lần đăng: `python scripts/verify_published.py --channel {CH}` phải ra XÁC MINH ĐẠT.")
  return out, (len(full), len(partial), len(empty))


NOTES = [
    "## Ghi chú kỹ thuật chung\n",
    "- **Trần upload ~92/ngày cho MỖI kênh** (3 kênh = 3 Google Cloud project riêng). Vượt trần thì item tự hoãn sang sau giờ reset (không tính là hỏng); chạy `run_pipeline.py resume --channel X`.",
    "- **Pexels ~200 lượt tìm/giờ.** Đã có cache tìm kiếm 7 ngày (`cache/pexels/`) + thử lại khi tải ảnh lỗi 5xx.",
    "- **Không bao giờ** chạy `reset_items.py` mà không có pattern (script đã chặn); item đã có video_id không bị đụng.",
    "- Bundle đã có thì không bị ghi đè; chạy lại cùng dải ngày là vô hại.",
    "- BLHS: chỉ dùng bản 2017 cho điều KHÔNG bị Luật 86/2025/QH15 sửa (48 điều bị gắn cờ, khuôn tự bỏ qua).",
    "- FS: lỗi đã chấp nhận, không sửa video đã đăng — 11 video Lịch đọc sai con vật của tú; 92 video Lịch dùng B-roll theo đường dịch máy cũ.",
]

chs = list(channels.CHANNELS) if ALL_CH else [channels.pick()]
allout = [f"# Trạng thái sản xuất — {len(chs)} kênh\n",
          f"_Cập nhật {datetime.now():%d/%m/%Y %H:%M} · `python scripts/status_report.py`_\n"]
for ch in chs:
    o, (f_, p_, e_) = report(ch)
    allout += o + ["\n---\n"]
    print(f"{ch}: {f_} ngày đủ, {p_} dở, {e_} trống")
allout += NOTES
p = ROOT / ("STATUS.md" if ALL_CH else f"STATUS_{chs[0]}.md")
p.write_text("\n".join(allout) + "\n", encoding="utf-8")
print(f"Ghi {p}")

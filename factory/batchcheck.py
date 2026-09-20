"""Kiểm CHÉO cả lô — thứ mà kiểm từng bundle riêng lẻ không bao giờ thấy.

VÌ SAO CÓ FILE NÀY: Bundle.validate() và factcheck đều soi TỪNG bundle một.
Cả hai đều cho 30/30 ĐẠT, và 9 video vẫn không lên được kênh.

Lỗi thật: tiêu đề sinh từ (sao, trực), mà chu kỳ sao và trực đều là 12 ngày
nên cứ 12 ngày lại lặp đúng một cặp. Tháng 10/2026 có 9 cặp ngày trùng tiêu
đề. Bộ chống trùng của publish.py so theo tiêu đề nên nó bỏ qua 9 lần upload
-- làm đúng việc của nó, nhưng hậu quả là 9 ngày cuối tháng không có video,
trong khi store ghi là đã đăng.

Không phép kiểm đơn-bundle nào bắt được loại lỗi này, vì mỗi bundle xét
riêng đều hoàn toàn hợp lệ. Chỉ khi đặt cạnh nhau mới thấy.

Đây cũng đúng dạng vấn đề với "lặp khuôn" mà người dùng từng chỉ ra: bộ
chấm kịch bản chấm từng bản một nên cho cả 7 bản ĐẠT, trong khi đặt cạnh
nhau thì thấy ngay cả 7 đều mở bằng "Lịch cũ gọi ngày mai là...".
"""
from __future__ import annotations

import collections
import re
from dataclasses import dataclass


@dataclass
class BatchIssue:
    ok: bool
    msg: str


# Mở bài giống nhau quá nhiều lần thì người xem hằng ngày nhận ra khuôn.
# Ngưỡng: không quá 40% số bản dùng chung một kiểu mở.
MAX_SAME_OPENING_RATIO = 0.4
OPENING_WORDS = 4

# Tỉ lệ chỉ có nghĩa khi lô đủ lớn. Lô 2 item thì mở bài nào cũng chiếm
# 50%, vượt ngưỡng ngay dù chẳng lặp gì cả. Dưới mức này thì bỏ qua phép
# kiểm tỉ lệ -- các phép kiểm trùng tuyệt đối (tiêu đề, slug, giờ đăng,
# kịch bản) vẫn chạy bình thường vì chúng không phụ thuộc cỡ lô.
MIN_BATCH_FOR_RATIO = 5


def check_batch(bundles) -> list[BatchIssue]:
    """Soi cả lô. `bundles` là list Bundle đã sắp theo publish_at."""
    out: list[BatchIssue] = []
    bs = list(bundles)
    n = len(bs)
    if n < 2:
        return [BatchIssue(True, "lô chỉ có 1 item, không có gì để so chéo")]

    # ─── TRÙNG TIÊU ĐỀ -- lỗi đã gây hậu quả thật ─────────────────────────
    # publish.py chống trùng bằng cách so tiêu đề với video đã có trên kênh.
    # Hai bundle cùng tiêu đề nghĩa là cái thứ hai SẼ BỊ BỎ QUA im lặng.
    titles = collections.Counter(b.title for b in bs)
    dup_t = {t: c for t, c in titles.items() if c > 1}
    out.append(BatchIssue(not dup_t,
                          f"TRÙNG TIÊU ĐỀ (cái sau sẽ bị dedup bỏ qua khi đăng): {dup_t}"
                          if dup_t else f"{n} tiêu đề đều duy nhất"))

    # ─── TRÙNG SLUG ───────────────────────────────────────────────────────
    slugs = collections.Counter(b.slug for b in bs)
    dup_s = {s: c for s, c in slugs.items() if c > 1}
    out.append(BatchIssue(not dup_s, f"trùng slug: {dup_s}" if dup_s else "slug đều duy nhất"))

    # ─── TRÙNG GIỜ ĐĂNG ───────────────────────────────────────────────────
    # Hai video cùng publish_at thì lên cùng lúc, chồng nhau trong feed.
    pubs = collections.Counter(b.publish_at for b in bs)
    dup_p = {p: c for p, c in pubs.items() if c > 1}
    out.append(BatchIssue(not dup_p, f"trùng giờ đăng: {dup_p}" if dup_p else "giờ đăng đều riêng"))

    # ─── TRÙNG NGUYÊN VĂN KỊCH BẢN ────────────────────────────────────────
    scripts = collections.Counter(b.script for b in bs)
    dup_sc = [s[:40] for s, c in scripts.items() if c > 1]
    out.append(BatchIssue(not dup_sc, f"kịch bản trùng nguyên văn: {dup_sc}"
                          if dup_sc else "không kịch bản nào trùng nguyên văn"))

    # ─── LẶP KHUÔN MỞ BÀI ─────────────────────────────────────────────────
    # Đây là thứ bộ chấm đơn-bundle mù hoàn toàn: từng bản đều hay, nhưng
    # xem liên tiếp thì thấy ngay công thức.
    if n >= MIN_BATCH_FOR_RATIO:
        openings = collections.Counter(
            " ".join(b.script.split()[:OPENING_WORDS]).lower() for b in bs)
        top, cnt = openings.most_common(1)[0]
        ratio = cnt / n
        out.append(BatchIssue(
            ratio <= MAX_SAME_OPENING_RATIO,
            f"mở bài {top!r} dùng {cnt}/{n} lần ({ratio:.0%}) — "
            f"quá {MAX_SAME_OPENING_RATIO:.0%} là người xem hằng ngày nhận ra khuôn"
            if ratio > MAX_SAME_OPENING_RATIO
            else f"mở bài đa dạng (kiểu lặp nhiều nhất chỉ {cnt}/{n})"))

    # ─── LẶP CÂU CHỐT ─────────────────────────────────────────────────────
    closers = collections.Counter(b.script.rsplit(".", 2)[-2].strip().lower()
                                  for b in bs if b.script.count(".") >= 2)
    if closers and n >= MIN_BATCH_FOR_RATIO:
        ctop, ccnt = closers.most_common(1)[0]
        cr = ccnt / n
        out.append(BatchIssue(
            cr <= MAX_SAME_OPENING_RATIO,
            f"câu chốt {ctop[:40]!r} dùng {ccnt}/{n} lần ({cr:.0%})"
            if cr > MAX_SAME_OPENING_RATIO else f"câu chốt đa dạng ({ccnt}/{n})"))

    return out


def report_batch(bundles, label: str = "") -> tuple[bool, str]:
    issues = check_batch(bundles)
    ok = all(i.ok for i in issues)
    head = f"{label}  {'ĐẠT' if ok else 'CẦN SỬA'}"
    body = "\n".join(f"   {'ok ' if i.ok else '>> '}{i.msg}" for i in issues)
    return ok, f"{head}\n{body}"

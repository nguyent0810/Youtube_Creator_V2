"""Gói kịch bản do Claude viết + bộ kiểm NHẸ — cho các dòng cần sáng tạo.

VÌ SAO KHÁC FS: dòng FS sinh từ khuôn trên dữ liệu tập đóng -> đúng nhưng
khô. Người dùng chốt (21/09/2026): "cần nội dung hấp dẫn chứ không phải quá
nhiều rule, nếu luật làm giới hạn thì sửa". Nên với kênh CL/BUD:

  - Dòng SÁNG TẠO (truyện đêm...) -> gói do Claude viết, gắn nhãn hư cấu,
    chỉ kiểm chất lượng (độ dài, hook, chốt, không lặp).
  - Dòng KIẾN THỨC -> gói do Claude viết, NHƯNG mọi trích dẫn kiểm được thì
    máy tự kiểm: "Điều N" phải có thật trong BLHS; điều bị Luật 86/2025 sửa
    thì không được nêu khung phạt từ bản cũ; "kệ N" phải có trong Pháp Cú.
  - Bỏ các luật "phải rào đón từng câu", "mỗi câu phải có claim" -- đó là
    thứ làm kịch bản FS cứng.

Gói: data/packs/<KÊNH>/<dòng>.json = danh sách
    {"key", "title", "script", "sources": [...], "fiction": bool,
     "broll": [...] (tuỳ chọn), "cite_ke": [số kệ] (tuỳ chọn)}
Thêm gói mới = thêm phần tử vào file. Máy tự lấy phần tử chưa dùng.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

from factory.pillars.check import Draft, Finding, OPENING_WINDOW, sentences

ROOT = Path(__file__).resolve().parents[2]
PACK_DIR = ROOT / "data" / "packs"

MIN_W, MAX_W = 60, 95
MAX_HOOK_W, MAX_CLOSER_W = 26, 16
OPENING_WORDS = 5
HOOK_MARKERS = ("?", "chưa chắc", "vậy mà", "nhưng", "lại", "tưởng", "ngược", "không phải",
                "mới là", "trong khi", "còn", "…", "...", "đừng", "bí ẩn", "không ai")
# Chỉ giữ những câu thật sự nguy hiểm với nội dung kiến thức.
BANNED_FACTUAL = (r"\b100\s*%", r"\bchắc chắn (?:giàu|khỏi|thoát|gặp)", r"khoa học (?:đã )?chứng minh",
                  r"\bđảm bảo khỏi\b")


@lru_cache(maxsize=None)
def blhs() -> dict:
    p = ROOT / "data" / "blhs.json"
    return json.loads(p.read_text(encoding="utf-8"))["dieu"] if p.exists() else {}


@lru_cache(maxsize=None)
def phapcu() -> dict:
    p = ROOT / "data" / "phapcu.json"
    return json.loads(p.read_text(encoding="utf-8"))["ke"] if p.exists() else {}


def load(channel: str, line: str) -> list[dict]:
    p = PACK_DIR / channel / f"{line}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def to_draft(e: dict, pillar: str, broll_pool: list[str]) -> Draft:
    from factory.pillars.expand import pick_broll
    broll = e.get("broll") or pick_broll(broll_pool, e["key"])
    return Draft(pillar, e["key"], e["title"], e["script"].strip(), [], list(e.get("sources", [])),
                 broll, "hư cấu" if e.get("fiction") else pillar, set())


_PENALTY = re.compile(r"(phạt tù|tù chung thân|tử hình|cải tạo không giam giữ|phạt tiền|\d+\s*năm tù)",
                      re.IGNORECASE)


def check_citations(script: str, cite_ke: list | None = None) -> list[str]:
    """Trích dẫn kiểm được thì máy kiểm. Trả danh sách lỗi.

    Siết thêm (audit 08/10/2026): "điều 999" viết thường và "Ðiều" (chữ Ð
    U+00D0 nhìn y hệt Đ) từng lọt; điều bị Luật 86/2025 sửa mà khung phạt nằm
    ở CÂU KẾ TIẾP ("Điều 353 quy định tội tham ô. Mức cao nhất vẫn là tử
    hình.") cũng lọt; số kệ đọc trong lời ("kệ 500") không được đối chiếu."""
    errs = []
    law = blhs()
    text = script.replace("\u00d0", "\u0110").replace("\u00f0", "\u0111")
    sents = sentences(text)
    for i, s in enumerate(sents):
        for so in re.findall(r"\b[Đđ]iều (\d+[a-z]?)\b", s):
            if law and so not in law:
                errs.append(f"Điều {so} không có trong BLHS")
            elif law and law[so].get("sua_2025") and _PENALTY.search(" ".join(sents[i:i + 2])):
                errs.append(f"Điều {so} bị Luật 86/2025 sửa — không nêu khung phạt từ bản 2017")
    ke = phapcu()
    said = {int(n) for n in re.findall(r"\bkệ (?:số )?(\d{1,3})\b", text, re.IGNORECASE)}
    for n in sorted(set(int(x) for x in (cite_ke or [])) | said):
        if ke and str(n) not in ke:
            errs.append(f"kệ {n} không có trong Pháp Cú")
    if said and cite_ke is not None and not said <= {int(x) for x in cite_ke}:
        errs.append(f"lời đọc nhắc kệ {sorted(said)} nhưng nguồn ghi kệ {sorted(cite_ke)}")
    return errs


def check(d: Draft, history: list[dict], fiction: bool = False, cite_ke=None) -> list[Finding]:
    out = []
    sents = sentences(d.script)
    w = len(d.script.split())
    out.append(Finding(MIN_W <= w <= MAX_W, "ĐỘ DÀI", f"{w} từ (khung {MIN_W}–{MAX_W})"))
    hook = sents[0] if sents else ""
    hm = [m for m in HOOK_MARKERS if m in hook.lower()]
    # Truyện hư cấu: câu mở đầu tự nó đã gợi tò mò, không bắt phải có "dấu hiệu hook".
    out.append(Finding((bool(hm) or fiction) and len(hook.split()) <= MAX_HOOK_W, "HOOK",
                       f"hook {len(hook.split())} từ, dấu hiệu {hm or 'không có'}"))
    closer = sents[-1] if sents else ""
    out.append(Finding(len(closer.split()) <= MAX_CLOSER_W, "CHỐT", f"chốt {len(closer.split())} từ"))
    if not fiction:
        out.append(Finding(bool(d.sources), "NGUỒN", "có nguồn" if d.sources else "kiến thức mà không ghi nguồn"))
        hits = [p for p in BANNED_FACTUAL if re.search(p, d.script, re.IGNORECASE)]
        out.append(Finding(not hits, "LOGIC", f"câu hứa hẹn tuyệt đối: {hits}" if hits else "không hứa hẹn tuyệt đối"))
        errs = check_citations(d.script, cite_ke)
        out.append(Finding(not errs, "TRÍCH DẪN", "; ".join(errs) if errs else "trích dẫn đều có thật"))
    same = [h for h in history if h["pillar"] == d.pillar]
    out.append(Finding(d.key not in {h["key"] for h in same}, "ĐỘ MỚI", "chủ đề mới"))
    op = " ".join(d.script.split()[:OPENING_WORDS]).lower()
    dup = [h["key"] for h in history[-OPENING_WINDOW:]
           if " ".join(h["script"].split()[:OPENING_WORDS]).lower() == op]
    out.append(Finding(not dup, "ĐỘ MỚI", f"mở bài trùng: {dup}" if dup else "mở bài chưa dùng"))
    return out

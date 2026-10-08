"""Kênh Hình Sự (CL) — "Into the Killer's Mind". 5 dòng, mỗi dòng 1 short/ngày.

Chọn theo số liệu thật của kênh (21/09/2026):
  - Truyện kinh dị: nhóm nhiều view nhất (1,7–3k)      -> cl-truyen (HƯ CẤU, gắn nhãn)
  - Hội kín/tổ chức tội phạm: top kênh (Tam Hoàng 3,6k) -> cl-hoso
  - "Án treo có phải trắng án?": 1.835 view            -> cl-hieusai
  - "Ponzi và hạt gạo": 1.011 view                     -> cl-luadao
  - BLHS 426 điều, không bản quyền                      -> cl-dieu (khuôn tự động, >1 năm)
Luật quốc tế khô (CITES, UNCLOS: 2–212 view) bị bỏ.
"""
from __future__ import annotations

import hashlib
import re

from factory.lines import base, packs
from factory.pillars.check import Draft

CHANNEL = "CL"
PILLARS = {
    "hieusai": ("cl-hieusai-", "07:00", "hỏi đáp luật, bẻ hiểu lầm"),
    "dieu":    ("cl-dieu-", "11:30", "một điều luật trong 60 giây"),
    "luadao":  ("cl-luadao-", "15:00", "nhận diện lừa đảo"),
    "hoso":    ("cl-hoso-", "19:00", "hồ sơ tổ chức tội phạm, vụ án lịch sử"),
    "truyen":  ("cl-truyen-", "22:00", "truyện đêm (hư cấu)"),
}
FICTION = {"truyen"}
STYLE = {
    "hieusai": ("Minh Triết", "deliberate_thought.mp3"),
    "dieu":    ("Minh Đức", "thinking_music.mp3"),
    "luadao":  ("Mai Anh", "deliberate_thought.mp3"),
    "hoso":    ("Thanh Bình", "comfortable_mystery_4.mp3"),
    "truyen":  ("Anh Khôi", "comfortable_mystery_4.mp3"),
}
TAGS = {
    "hieusai": ["phap luat", "hieu dung luat", "bo luat hinh su", "hinh su"],
    "dieu":    ["bo luat hinh su", "dieu luat", "khung hinh phat", "phap luat"],
    "luadao":  ["lua dao", "canh bao lua dao", "phong chong lua dao", "hinh su"],
    "hoso":    ["ho so toi pham", "to chuc toi pham", "vu an", "lich su toi pham"],
    "truyen":  ["truyen kinh di", "truyen ma", "chuyen dem khuya", "truyen hu cau"],
}
BROLL = {
    "hieusai": ["courtroom gavel", "law books library", "judge bench wood", "scales of justice statue",
                "handcuffs on table", "police lights night", "courthouse columns", "legal documents desk",
                "prison bars shadow", "lawyer reading file", "city street night", "fingerprint close up",
                "notebook pen desk", "old typewriter"],
    "dieu":    ["law books library", "courtroom gavel", "legal documents desk", "courthouse columns",
                "scales of justice statue", "pen signing document", "stamp on paper", "archive folders",
                "reading glasses on book", "gavel close up", "office desk lamp night", "old paper pages",
                "hand writing notes", "library shelves"],
    "luadao":  ["smartphone scam call", "hacker keyboard dark", "credit card fraud", "counting money hands",
                "phone notification", "laptop code screen", "worried woman phone", "bank card close up",
                "online banking app", "padlock security", "email inbox laptop", "cash stack table",
                "anonymous hoodie", "warning sign"],
    "hoso":    ["old newspaper archive", "vintage photograph", "dark alley night", "hong kong street night",
                "detective board strings", "film noir shadow", "smoke dark room", "old police car",
                "evidence bag", "vintage typewriter", "chinatown lanterns night", "city skyline night",
                "rain window night", "old map desk"],
    "truyen":  ["abandoned house night", "dark forest fog", "flickering light bulb", "empty corridor",
                "mountain road night fog", "old tv static", "door creaking dark", "moon behind clouds",
                "candle dark room", "rain window night", "old staircase", "shadow on wall",
                "empty playground night", "old mirror"],
}


# ─── Khuôn "một điều luật trong 60 giây" ─────────────────────────────────

def _speak(s: str) -> str:
    """Số trong luật -> cách đọc: '06 tháng' -> '6 tháng', '2.000.000 đồng' -> '2 triệu đồng'."""
    def money(m):
        n = int(m.group(1).replace(".", ""))
        if n >= 1_000_000_000:
            v, u = n / 1_000_000_000, "tỷ"
        elif n >= 1_000_000:
            v, u = n / 1_000_000, "triệu"
        else:
            return f"{n:,}".replace(",", ".") + " đồng"
        return f"{v:g} {u} đồng".replace(".", ",")
    s = re.sub(r"(\d{1,3}(?:\.\d{3})+) đồng", money, s)
    return re.sub(r"\b0(\d)\b", r"\1", s)


def _khoan(noi_dung: str) -> list[str]:
    parts = re.split(r"(?m)^(\d+)\.\s*", noi_dung)
    return [parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)]


def _phat(k: str) -> str | None:
    """Câu phạt của một khoản: "thì bị ..." trong CÂU DẪN của khoản.

    Câu dẫn = mọi dòng trước điểm a), b)... Bản cũ chỉ đọc DÒNG VẬT LÝ ĐẦU,
    mà văn bản BLHS xuống dòng giữa câu: khoản 1 Điều 301 bị bỏ, khoản 2 bị
    gọi là "khoản 1" ("mức nhẹ nhất 3–7 năm", thật là 01–04 năm) và "luật
    chia 3 khung" (thật 4) -- vẫn qua kiểm vì chốt "khoản 1 phải nhẹ nhất"
    so nhầm trên khoản 2.

    Dừng ở ":" / ";" / hết câu dẫn / ". " -- KHÔNG dừng ở mọi dấu "." vì số
    tiền "10.000.000" có dấu chấm (lỗi thật: ra "phạt tiền từ 10.")."""
    lead = []
    for ln in k.split("\n"):
        if lead and re.match(r"\s*[a-zđ]\)\s", ln):
            break
        lead.append(ln.strip())
    # Nguồn có lỗi gõ "100.000. 000 đồng" (Điều 205): nối lại số trước khi tách câu.
    text = re.sub(r"(\d)\.\s+(\d{3})\b", r"\1.\2", " ".join(lead))
    m = re.search(r"thì bị (.+?)\s*(?::|;|$|\.\s+(?=[^\d\s]))", text)
    return _speak(m.group(1).strip().rstrip(".")) if m else None


def _nang(phat: str) -> tuple:
    """Điểm mức nặng để so: tử hình > chung thân > số năm tù tối đa > cải tạo > tiền."""
    p = phat.lower()
    if "tử hình" in p:
        return (5, 0)
    if "chung thân" in p:
        return (4, 0)
    years = [int(x) for x in re.findall(r"đến (\d+) năm", p) if "tù" in p]
    if "tù" in p and years:
        return (3, max(years))
    if "cải tạo" in p:
        return (2, 0)
    return (1, 0)


def dieu_luat(history, day) -> Draft | None:
    law = packs.blhs()
    done = {h["key"] for h in history if h["pillar"] == "dieu"}
    for so in sorted((k for k in law if k.isdigit() and int(k) >= 123), key=int):
        a = law[so]
        key = so                      # slug = cl-dieu-<số điều>
        if key in done or a.get("sua_2025") or not a["ten"].startswith("Tội"):
            continue
        ks = [k for k in _khoan(a["noi_dung"]) if not k.startswith("Pháp nhân")]
        # LỖI THẬT: lấy "khoản cuối" làm khung nặng nhất -> Điều 302 (cướp biển)
        # đọc thành "nặng nhất 1–5 năm", vì khoản cuối là CHUẨN BỊ phạm tội.
        # Giờ: bỏ khoản chuẩn bị phạm tội, xếp hạng theo mức nặng thật.
        chinh = [(k, _phat(k)) for k in ks if _phat(k) and "chuẩn bị phạm tội" not in k[:80]]
        if len(chinh) < 2:
            continue
        nhe = min(chinh, key=lambda kp: _nang(kp[1]))[1]
        nang = max(chinh, key=lambda kp: _nang(kp[1]))[1]
        if chinh[0][1] != nhe:          # khoản 1 phải là khung nhẹ nhất, không thì bỏ (cấu trúc lạ)
            continue
        bosung = next((k for k in ks if "còn có thể bị" in k), None)
        ten = a["ten"][0].lower() + a["ten"][1:]
        v = int(hashlib.sha256(key.encode()).hexdigest(), 16) % 3
        hooks = [f"Điều {so} Bộ luật Hình sự, {ten}: nhẹ nhất bị phạt gì, nặng nhất đến đâu?",
                 f"Điều {so} quy định {ten}, nhưng khung phạt chênh nhau tới mức nào?",
                 f"Điều {so}, {ten}: bạn đoán mức phạt cao nhất là bao nhiêu?"]
        hook = hooks[v]
        if len(hook.split()) > packs.MAX_HOOK_W:     # tên tội dài -> dùng câu hook ngắn nhất
            hook = min(hooks, key=lambda h: len(h.split()))
        s = [hook,
             f"Theo khoản 1, mức nhẹ nhất là {nhe}.",
             f"Ở khung nặng nhất, người phạm tội có thể bị {nang}.",
             f"Luật chia {len(chinh)} khung, nặng dần theo tính chất và hậu quả."]
        if bosung:
            s.append("Ngoài ra còn có thể có hình phạt bổ sung.")
        s += ["Mức án cụ thể do tòa quyết định trong từng vụ.",
              ["Bạn thấy khung phạt này nặng hay nhẹ?", "Bạn muốn nghe điều luật nào tiếp theo?",
               "Comment điều luật bạn muốn tìm hiểu."][v]]
        script = " ".join(s)
        if not packs.MIN_W <= len(script.split()) <= packs.MAX_W:
            continue
        from factory.pillars.expand import pick_broll
        from factory.pillars.check import verdict
        d = Draft("dieu", key, f"Điều {so}: {a['ten']}", script, [],
                  [f"Bộ luật Hình sự 2015 (sửa đổi 2017), Điều {so} — vi.wikisource.org; "
                   f"điều này không bị Luật 86/2025/QH15 sửa"],
                  pick_broll(BROLL["dieu"], key), "dieu", set())
        # Điều nào không qua kiểm, hoặc kênh đã có video về điều đó, thì thử điều kế tiếp.
        from factory.lines import novelty
        if novelty.duplicate_on_channel(CHANNEL, d.title):
            continue
        if verdict(packs.check(d, history)):
            return d
    return None


TEMPLATES = {"dieu": dieu_luat}
_self = __import__(__name__, fromlist=["x"])
next_draft = base.make_next_draft(_self)
ALL_NAMES: set = set()


def load_history(bundle_dir):
    return base.load_history(bundle_dir, CHANNEL)


def check_draft(d, history):
    return base.check_draft(_self, d, history)

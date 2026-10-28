"""Sinh cảnh CK F3: Lương 12 Triệu, một năm đi đám cưới hết bao nhiêu tiền?"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
BLUE, GOLD, GREEN, VIOLET = "#38bdf8", "#fbbf24", "#22c55e", "#a78bfa"
HYP = "VÍ DỤ GIẢ ĐỊNH · CHỊ HÀ · LƯƠNG 12 TRIỆU/THÁNG"
VM = "VIDEO MINH HỌA"

# Các ID được chốt sau khi xem sheet clip trong vòng dựng này.
VIDS = ["7430218", "8086203", "6305041", "30263260", "3122106", "5466772"]
AI = [f"ai{i:02d}" for i in range(1, 7)]

def photo(i, at, move):
    d = {"type": "photo", "img": AI[i % 6], "at": at, "credit": False,
         "illus": "ẢNH MINH HỌA", "focus": [0.50, 0.18]}
    if move == "reveal": d["reveal"] = {"kind": "circle" if i % 2 else "wipe", "at": at, "d": 0.9}
    elif move == "zoom": d["zoom"] = {"x": 0.58, "y": 0.40, "z": 1.35, "at": at, "d": 1.2}
    else: d["move"] = move
    return d

def heat(at, limit, title, calls):
    vals = R["heat_monthly_million"][:limit]
    cells = [{"k": f"T{i+1}", "v": v, "at": at} for i, v in enumerate(vals)]
    return {"type": "heat", "at": at, "title": title, "range": [0, 1.1], "unit": "TRIỆU",
            "cols": 6, "cells": cells, "total": {"label": "CẢ NĂM", "at": at}, "calls": calls}

def stack(at):
    return {"type": "stack", "at": at, "title": "BẢY ĐÁM CƯỚI", "range": [0, 1.7], "unit": "TRIỆU",
            "keys": [{"k": "SỐ ĐÁM"}, {"k": "MỨC PHONG BÌ"}, {"k": "TỔNG"}],
            "groups": [{"k": "BẠN THÂN", "vals": [2, .7, 1.4], "at": at},
                       {"k": "ĐỒNG NGHIỆP", "vals": [3, .5, 1.5], "at": at},
                       {"k": "HỌ HÀNG", "vals": [2, .3, .6], "at": at}],
            "calls": [{"i": 1, "text": "1,5 TRIỆU", "at": at}]}

def bars(at, title, items, call=0):
    return {"type": "bars", "at": at, "title": title, "unit": "VÍ DỤ GIẢ ĐỊNH",
            "items": items, "calls": [{"i": call, "text": items[call]["lbl"], "at": at}]}

CH = {}
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "LỊCH PHONG BÌ CẢ NĂM"}, "bgm": {"mood": "curious", "gain": .10}, "scenes": [
    heat(0, 12, "LỊCH 12 THÁNG", [{"i": 11, "text": "5,6 TRIỆU", "at": 0}]),
    {"type": "counter", "at": 0, "from": 0, "to": R["annual_total_million"], "suffix": " TRIỆU", "label": "CẢ NĂM · " + HYP, "calls": [{"i": 0, "text": "5,6 TRIỆU", "at": 0}]},
    photo(0, 1, "reveal"), {"type": "broll", "vid": VIDS[0], "at": 2, "veil": .55, "illus": VM},
    bars(3, "14 DỊP TRONG NĂM", [{"k": "ĐÁM CƯỚI", "v": 7, "lbl": "7", "at": 3}, {"k": "DỊP KHÁC", "v": 7, "lbl": "7", "at": 3}], 0),
    {"type": "ledger", "at": 4, "title": "LỊCH VÍ DỤ GIẢ ĐỊNH", "rows": [{"k": "CƯỚI", "v": "7 DỊP", "at": 4}, {"k": "DỊP KHÁC", "v": "7 DỊP", "at": 4}]},
    {"type": "question", "at": 6, "text": "Một năm, những phong bì nhỏ\ncộng thành bao nhiêu?"},
    {"type": "counter", "at": 8, "from": 0, "to": R["share_of_monthly_wage_pct"], "suffix": "%", "label": "SO VỚI LƯƠNG THÁNG", "calls": [{"i": 0, "text": "46,67%", "at": 8}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "NHÌN ĐƯỜNG ĐI CỦA BỘ ĐẾM", "at": 10, "acc": True}]}
]}
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "PHONG BÌ LÀ MỘT DÒNG CHI"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "PHONG BÌ LÀ\nMỘT DÒNG CHI", "sub": HYP, "vid": VIDS[1], "illus": VM, "titleAt": 0},
    photo(1, 1, "zoom"),
    bars(2, "LƯƠNG VÀ PHONG BÌ", [{"k": "LƯƠNG THÁNG", "v": 12, "lbl": "12", "at": 2}, {"k": "MỘT PHONG BÌ", "v": .5, "lbl": "0,5", "at": 2}], 1),
    {"type": "counter", "at": 2, "from": 0, "to": R["envelope_500k_share_pct"], "suffix": "%", "label": "MỘT PHONG BÌ / LƯƠNG", "calls": [{"i": 0, "text": "4,17%", "at": 2}]},
    {"type": "broll", "vid": VIDS[2], "at": 4, "veil": .55, "illus": VM},
    {"type": "ledger", "at": 7, "title": "BA Ô GIẢ ĐỊNH", "rows": [{"k": "300", "v": "NGHÌN", "at": 7}, {"k": "500", "v": "NGHÌN", "at": 7}, {"k": "700", "v": "NGHÌN", "at": 7}]},
    bars(10, "MỘT LẦN VÀ CẢ NĂM", [{"k": "MỘT LẦN", "v": .5, "lbl": "0,5", "at": 10}, {"k": "CẢ NĂM", "v": 5.6, "lbl": "5,6", "at": 10}], 0),
    {"type": "question", "at": 14, "text": "Nếu lịch không chỉ có một lần\nthì sao?"},
    {"type": "kinetic", "at": 18, "items": [{"text": "NHÌN TỔNG TRƯỚC KHI BẤT NGỜ", "at": 18, "acc": True}]}
]}
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "BA Ô QUAN HỆ"}, "bgm": {"mood": "curious", "gain": .10}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "BA Ô\nQUAN HỆ", "sub": "VÍ DỤ GIẢ ĐỊNH", "vid": VIDS[3], "illus": VM, "titleAt": 0}, photo(2, 1, "out"), stack(3),
    bars(4, "TỔNG BA NHÓM", [{"k": "BẠN THÂN", "v": 1.4, "lbl": "1,4", "at": 4}, {"k": "ĐỒNG NGHIỆP", "v": 1.5, "lbl": "1,5", "at": 4}, {"k": "HỌ HÀNG", "v": .6, "lbl": "0,6", "at": 4}], 1),
    {"type": "broll", "vid": VIDS[4], "at": 8, "veil": .55, "illus": VM},
    {"type": "counter", "at": 9, "from": 0, "to": R["wedding_total_million"], "suffix": " TRIỆU", "label": "BẢY ĐÁM CƯỚI", "calls": [{"i": 0, "text": "3,5 TRIỆU", "at": 9}]},
    {"type": "ledger", "at": 14, "title": "PHÉP NHÂN", "rows": [{"k": "SỐ DỊP", "v": "× MỨC", "at": 14}, {"k": "KẾT QUẢ", "v": "CỘNG LẠI", "at": 14}]},
    {"type": "question", "at": 22, "text": "Khoản nào đến sớm,\nkhoản nào đến muộn?"},
    heat(23, 2, "LỊCH BẮT ĐẦU", [{"i": 1, "text": "0,8 TRIỆU", "at": 23}]),
    {"type": "kinetic", "at": 24, "items": [{"text": "LẬT LỊCH THEO THÁNG", "at": 24, "acc": True}]}
]}
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "LẬT LỊCH MƯỜI HAI THÁNG"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "LẬT LỊCH\nMƯỜI HAI THÁNG", "sub": "NĂM 2027 · VÍ DỤ GIẢ ĐỊNH", "vid": VIDS[5], "illus": VM, "titleAt": 0}, photo(3, 1, "reveal"),
    heat(2, 3, "LỊCH TỪ THÁNG 1", [{"i": 1, "text": "0,8 TRIỆU", "at": 2}]), heat(9, 8, "LỊCH TỚI THÁNG 8", [{"i": 7, "text": "2,8 TRIỆU", "at": 9}]),
    {"type": "broll", "vid": VIDS[1], "at": 15, "veil": .55, "illus": VM}, heat(17, 12, "LỊCH ĐỦ CẢ NĂM", [{"i": 11, "text": "5,6 TRIỆU", "at": 17}]),
    {"type": "counter", "at": 22, "from": 0, "to": R["annual_total_million"], "suffix": " TRIỆU", "label": "BỘ ĐẾM KHÉP LẠI", "calls": [{"i": 0, "text": "5,6 TRIỆU", "at": 22}]},
    {"type": "ledger", "at": 25, "title": "BỐN THÁNG TRỐNG", "rows": [{"k": "T1 · T3", "v": "0", "at": 25}, {"k": "T6 · T9", "v": "0", "at": 25}]},
    {"type": "question", "at": 29, "text": "Phần lớn tổng năm\nđến từ đâu?"}, {"type": "kinetic", "at": 30, "items": [{"text": "MỞ RIÊNG BẢY ĐÁM CƯỚI", "at": 30, "acc": True}]}
]}
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "BẢY ĐÁM CƯỚI TRÊN LỊCH"}, "bgm": {"mood": "curious", "gain": .10}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "BẢY ĐÁM CƯỚI\nTRÊN LỊCH", "sub": "3,5 TRIỆU · VÍ DỤ GIẢ ĐỊNH", "vid": VIDS[2], "illus": VM, "titleAt": 0}, photo(4, 1, "pan"), stack(3),
    bars(4, "BA NHÓM CƯỚI", [{"k": "BẠN THÂN", "v": 1.4, "lbl": "1,4", "at": 4}, {"k": "ĐỒNG NGHIỆP", "v": 1.5, "lbl": "1,5", "at": 4}, {"k": "HỌ HÀNG", "v": .6, "lbl": "0,6", "at": 4}], 0),
    {"type": "broll", "vid": VIDS[3], "at": 8, "veil": .55, "illus": VM}, {"type": "counter", "at": 7, "from": 0, "to": 3.5, "suffix": " TRIỆU", "label": "BẢY ĐÁM CƯỚI", "calls": [{"i": 0, "text": "3,5 TRIỆU", "at": 7}]},
    heat(21, 12, "CƯỚI RẢI QUA NĂM", [{"i": 11, "text": "3,5 TRIỆU", "at": 21}]),
    {"type": "ledger", "at": 18, "title": "KHÔNG PHẢI CHUẨN XÃ HỘI", "rows": [{"k": "MỖI NƠI", "v": "MỖI KHÁC", "at": 18}]},
    {"type": "question", "at": 26, "text": "Phần còn lại của lịch\nlà gì?"}, {"type": "kinetic", "at": 28, "items": [{"text": "BẢY DỊP KHÁC", "at": 28, "acc": True}]}
]}
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "BẢY DỊP KHÔNG PHẢI CƯỚI"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "BẢY DỊP\nKHÔNG PHẢI CƯỚI", "sub": "2,1 TRIỆU · VÍ DỤ GIẢ ĐỊNH", "vid": VIDS[4], "illus": VM, "titleAt": 0}, photo(5, 1, "zoom"),
    bars(2, "BỐN KHOẢN KHÁC", [{"k": "LÌ XÌ", "v": .8, "lbl": "0,8", "at": 2}, {"k": "TÂN GIA", "v": .5, "lbl": "0,5", "at": 2}, {"k": "ĐẦY THÁNG", "v": .3, "lbl": "0,3", "at": 2}, {"k": "ĐÁM HIẾU", "v": .5, "lbl": "0,5", "at": 2}], 0),
    {"type": "counter", "at": 5, "from": 0, "to": R["other_total_million"], "suffix": " TRIỆU", "label": "BẢY DỊP KHÁC", "calls": [{"i": 0, "text": "2,1 TRIỆU", "at": 5}]},
    {"type": "broll", "vid": VIDS[5], "at": 9, "veil": .55, "illus": VM}, heat(13, 8, "LỊCH CÁC DỊP KHÁC", [{"i": 1, "text": "0,8 TRIỆU", "at": 13}]),
    {"type": "ledger", "at": 15, "title": "CÁC SỐ HẠNG", "rows": [{"k": "0,8", "v": "LÌ XÌ", "at": 15}, {"k": "1,3", "v": "BA DỊP CÒN LẠI", "at": 15}]},
    bars(16, "CƯỚI VÀ DỊP KHÁC", [{"k": "CƯỚI", "v": 3.5, "lbl": "3,5", "at": 16}, {"k": "DỊP KHÁC", "v": 2.1, "lbl": "2,1", "at": 16}], 1),
    {"type": "question", "at": 20, "text": "Hai nhóm ghép lại\nra con số nào?"}, {"type": "kinetic", "at": 24, "items": [{"text": "TRỞ LẠI TỔNG NĂM", "at": 24, "acc": True}]}
]}
CH["ch06"] = {"hud": {"k": "PHẦN CUỐI", "t": "KHÓA LỊCH, MỞ KHUNG TÍNH"}, "bgm": {"mood": "calm", "gain": .11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "PHẦN CUỐI", "title": "KHÓA LỊCH,\nMỞ KHUNG TÍNH", "sub": "5,6 TRIỆU · VÍ DỤ GIẢ ĐỊNH", "vid": VIDS[0], "illus": VM, "titleAt": 0}, photo(0, 1, "out"),
    {"type": "waterfall", "at": 3, "title": "TỪ LƯƠNG TỚI PHONG BÌ", "range": [0, 12], "unit": "TRIỆU", "start": {"k": "LƯƠNG", "v": 12, "at": 3}, "steps": [{"k": "CƯỚI", "v": -3.5, "at": 3}, {"k": "DỊP KHÁC", "v": -2.1, "at": 3}], "end": {"k": "PHONG BÌ", "at": 3}, "calls": [{"i": 3, "text": "5,6 TRIỆU", "at": 3}]},
    {"type": "counter", "at": 10, "from": 0, "to": R["annual_total_million"], "suffix": " TRIỆU", "label": "TỔNG PHONG BÌ CẢ NĂM", "calls": [{"i": 0, "text": "5,6 TRIỆU", "at": 10}]},
    heat(12, 12, "LỊCH KHÉP LẠI", [{"i": 11, "text": "5,6 TRIỆU", "at": 12}]),
    bars(14, "TỔNG / LƯƠNG THÁNG", [{"k": "TỔNG NĂM", "v": 5.6, "lbl": "5,6", "at": 14}, {"k": "LƯƠNG THÁNG", "v": 12, "lbl": "12", "at": 14}], 0),
    {"type": "ledger", "at": 19, "title": "KHUNG TÍNH", "rows": [{"k": "SỐ DỊP", "v": "× MỨC", "at": 19}, {"k": "CỘNG", "v": "CÁC DỊP KHÁC", "at": 19}]},
    {"type": "question", "at": 23, "text": "Bạn thay số nào\ntrong lịch của mình?"},
    {"type": "kinetic", "at": 25, "items": [{"text": "ĐÓ LÀ LỊCH CỦA BẠN", "at": 25, "acc": True}]},
    {"type": "brand", "at": 25, "sub": "NỘI DUNG GIÁO DỤC · KHÔNG PHẢI TƯ VẤN ĐẦU TƯ"}
]}

TITLE = "Lương 12 Triệu: Một Năm Đi Đám Cưới Hết Bao Nhiêu Tiền?"
SOURCES = [
 "https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2026/03/ket-qua-khao-sat-muc-song-dan-cu-viet-nam-nam-2024/",
 "https://vnexpress.net/nghi-tet-am-lich-2027-tu-28-thang-chap-5127753.html", "https://amlich.org/xem-lich-nam/2027",
 "https://www.pexels.com/photo/woman-in-yellow-dress-handing-envelopes-to-a-group-of-men-10568551/",
 "https://www.nso.gov.vn/", "https://vanban.chinhphu.vn/", "https://xaydungchinhsach.chinhphu.vn/", "https://moj.gov.vn/"
]
SPEC = {"title": TITLE, "channel": "CK", "accent": GOLD, "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True, "chart_rules": True,
 "acc": ["lương", "phong bì", "năm", "triệu", "lịch"], "say": {}, "imgs": {k: f"EXT:ai:ai_{i:02d}" for i,k in enumerate(AI,1)}, "chapters": list(CH),
 "youtube": {"titles": [TITLE], "publish_at": "2026-11-24T12:00:00+07:00", "playlist": "Tài chính cá nhân", "category": "Education", "thumb": "t1.jpg",
 "summary": "Ví dụ giả định về lịch phong bì một năm của chị Hà, với lương mười hai triệu đồng mỗi tháng.",
 "more": ["Nội dung giáo dục, không phải tư vấn đầu tư.", "Mọi khoản tiền, số dịp và mức phong bì trong video là VÍ DỤ GIẢ ĐỊNH; mỗi nơi mỗi khác."],
 "chapter_titles": {k: v["hud"]["t"] for k,v in CH.items()}, "sources": SOURCES, "tags": ["tiền mừng cưới", "quản lý chi tiêu", "tài chính cá nhân"], "hashtags": ["TàiChínhCáNhân", "ChiTiêu"], "video_credits": "Clip minh họa: Pexels. Ảnh minh họa: AI."}}

def main():
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, content in CH.items():
        p = D / f"{name}.json"; data = json.loads(p.read_text(encoding="utf-8")); data.update(content)
        p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec +", len(CH), "chương")

if __name__ == "__main__": main()

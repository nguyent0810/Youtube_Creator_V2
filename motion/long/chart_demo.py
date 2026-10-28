"""Bản rời một cảnh biểu đồ nến (theme "chart") để duyệt engine: VN-Index thật, nến hiện dần, MA tự vẽ, mốc đánh dấu.

    python motion/long/chart_demo.py   -> output/long/_chart_demo/demo.mp4 (không tiếng)
    python motion/long/chart_demo.py race [--gold]
    python motion/long/chart_demo.py breadth | breadth-anim | basket | basket-pct
        -> output/long/_chart_demo_<chế độ>/demo.mp4 (độ rộng / treemap vốn hoá HOSE, dữ liệu data/ck/breadth_2026/)
    python motion/long/chart_demo.py breadth-day | book | book-queue
        -> độ rộng theo % trong ngày (09/03/2026, base "prev") / sổ lệnh giả định (bảng giá ATO, hàng đợi ở giá sàn)
    python motion/long/chart_demo.py waterfall | heat | stack | line-calls
        -> ba cảnh mới 27/10/2026 (thác tiền, lịch nhiệt, cột xếp chồng) + khoanh điểm trên đường (race abs + calls)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / "motion"), str(ROOT)]

import build_long as BL  # noqa: E402
import chartdata  # noqa: E402
import variety  # noqa: E402

MODES = ("breadth", "breadth-anim", "basket", "basket-pct", "breadth-day", "book", "book-queue", "waterfall", "heat", "stack", "line-calls")

def main() -> None:
    mode = next((a for a in sys.argv[1:] if a in MODES), None)
    key = "_chart_demo" + (f"_{mode}" if mode else "")
    od = ROOT / "output" / "long" / key
    od.mkdir(parents=True, exist_ok=True)
    dur = 9.0
    if mode == "breadth":
        sc = chartdata.attach_breadth({"type": "breadth", "t0": 0.0, "t1": dur, "date": "2026-09-30", "drawAt": 0.5, "until": 3.3,
                                       "countAt": 3.6, "chipAt": 5.2, "medianAt": 6.4})
    elif mode == "breadth-anim":
        dur = 11.0
        sc = chartdata.attach_breadth({"type": "breadth", "t0": 0.0, "t1": dur, "date": "2026-09-30", "drawAt": 0.4, "until": 2.6,
                                       "countAt": 2.8, "chipAt": 3.2, "range": "31/12/2025 → 30/09/2026",
                                       "animate": {"from": "2026-01-05", "to": "2026-09-30", "every": 4, "at": 4.0, "until": 9.6}})
    elif mode == "breadth-day":
        sc = chartdata.attach_breadth({"type": "breadth", "t0": 0.0, "t1": dur, "date": "2026-03-09", "base": "prev", "drawAt": 0.4,
                                       "until": 2.8, "chipAt": 3.4, "chip": "XANH LƠ = GIÁ SÀN", "medianAt": 5.0,
                                       "medianText": "TRUNG VỊ −6,8% · SÀN = −7%", "range": "09/03/2026 · SO VỚI PHIÊN TRƯỚC"})
    elif mode == "book":
        rows = [{"side": "buy", "price": p, "qty": q, "at": 0.6 + 0.2 * k} for k, (p, q) in enumerate([(20100, 300), (20000, 500), (19900, 700)])]
        rows += [{"side": "sell", "price": p, "qty": q, "at": 1.4 + 0.2 * k} for k, (p, q) in enumerate([(19900, 400), (20000, 600), (20100, 800)])]
        sc = {"type": "book", "t0": 0.0, "t1": dur, "title": "SỔ LỆNH GIẢ ĐỊNH · PHIÊN ATO", "ref": 20000, "ceil": 21400, "floor": 18600,
              "rows": rows, "match": {"price": 20000, "at": 3.4, "text": "GIÁ MỞ CỬA 20.000 · KHỚP 800 CỔ PHIẾU",
                                      "sub": {"text": "ĐẶT MUA 20.100 CŨNG CHỈ TRẢ 20.000", "at": 5.0}}}
    elif mode == "book-queue":
        sc = {"type": "book", "t0": 0.0, "t1": dur, "title": "HÀNG ĐỢI Ở GIÁ SÀN", "range": "THAM CHIẾU 20.000 · SÀN 18.600",
              "ref": 20000, "floor": 18600,
              "queue": {"price": 18600, "times": ["09:00", "09:00", "09:03", "09:07", "09:12", "09:16", "09:21", "09:30", "09:42", "09:55", "10:08", "10:20"],
                        "mine": 9, "at": 0.6, "until": 2.4, "labelAt": 2.8, "hlAt": 3.4, "buy": {"text": "BÊN MUA Ở GIÁ SÀN: RẤT ÍT", "at": 4.2},
                        "eat": [{"at": 5.4, "k": 2}, {"at": 7.4, "k": 1}]}}
    elif mode == "waterfall":
        sc = {"type": "waterfall", "t0": 0.0, "t1": dur, "title": "7 NGÀY NẰM VIỆN CỦA ANH MINH", "range": "VÍ DỤ GIẢ ĐỊNH · TRIỆU ĐỒNG", "unit": "TRIỆU",
              "start": {"k": "HOÁ ĐƠN", "v": 30, "at": 0.5}, "steps": [{"k": "QUỸ TRẢ", "v": -16, "at": 1.6}, {"k": "NGOÀI HOÁ ĐƠN", "v": 2, "at": 2.8}],
              "end": {"k": "TỰ GÁNH", "at": 4.0}, "calls": [{"i": 3, "text": "16 TRIỆU TỰ TRẢ", "at": 5.4}]}
    elif mode == "heat":
        vals = [0.5, 1.0, 0, 0.5, 0.3, 0, 0, 0.3, 0.5, 0.8, 1.0, 0.7]
        sc = {"type": "heat", "t0": 0.0, "t1": dur, "title": "MỘT NĂM PHONG BÌ CỦA CHỊ HÀ", "range": "VÍ DỤ GIẢ ĐỊNH", "unit": "TRIỆU",
              "cells": [{"k": f"T{i + 1}", "v": v, "note": "TẾT" if i == 1 else None} for i, v in enumerate(vals)], "drawAt": 0.5, "until": 5.0,
              "total": {"label": "CẢ NĂM", "at": 5.6}, "calls": [{"i": 10, "text": "MÙA CƯỚI", "at": 6.6}]}
    elif mode == "stack":
        sc = {"type": "stack", "t0": 0.0, "t1": dur, "title": "SAU 12 THÁNG, TIỀN CỦA AI?", "range": "VÍ DỤ GIẢ ĐỊNH · TRIỆU ĐỒNG", "unit": "TRIỆU",
              "keys": [{"k": "THẢO"}, {"k": "NAM"}, {"k": "QUỸ CHUNG"}],
              "groups": [{"k": "50/50", "vals": [24, 144, 0], "at": 0.8}, {"k": "THEO LƯƠNG", "vals": [63, 105, 0], "at": 2.2},
                         {"k": "GỘP + RIÊNG", "vals": [42, 42, 84], "at": 3.6}], "calls": [{"i": 0, "text": "THẢO CÒN 24", "at": 5.6}]}
    elif mode == "line-calls":
        yrs = [str(i) for i in range(8)]
        sc = chartdata.attach_race({"type": "race", "t0": 0.0, "t1": dur, "abs": True, "unit": "TRIỆU", "xlab": "THÁNG ", "xstep": 1, "dates": yrs,
                                    "title": "KHOẢN THIẾU CỘNG DỒN CỦA CHỊ LAN", "range": "VÍ DỤ GIẢ ĐỊNH",
                                    "series": [{"label": "THIẾU", "color": "#f87171", "vals": [0, 4, 8, 12, 16, 20, 24, 28]}],
                                    "drawAt": 0.6, "until": 4.6, "calls": [{"i": 7, "text": "THIẾU 28 TRIỆU", "at": 5.4}, {"i": 1, "text": "THÁNG ĐẦU", "at": 7.0}]})
    elif mode == "basket":
        sc = chartdata.attach_basket({"type": "basket", "t0": 0.0, "t1": dur, "date": "2026-09-30", "groupSmall": 200, "labels": 10,
                                      "drawAt": 0.4, "until": 2.6, "highlight": ["VIC", "VHM", "VRE", "VPL"], "hlAt": 7.6,
                                      "captions": [{"text": "VIC ≈ 21%", "at": 3.2, "mark": ["VIC"]},
                                                   {"text": "TOP 10 ≈ 52%", "at": 4.6, "mark": "top10", "tone": "blue"},
                                                   {"text": "200 MÃ NHỎ NHẤT ≈ 1,3%", "at": 6.0, "mark": "group", "tone": "down"}]})
    elif mode == "basket-pct":
        sc = chartdata.attach_basket({"type": "basket", "t0": 0.0, "t1": dur, "date": "2026-09-30", "groupSmall": 200, "labels": ["VIC"],
                                      "tileInfo": "pct", "color": "pct", "colorAt": 3.0, "drawAt": 0.4, "until": 2.4,
                                      "highlight": ["VIC"], "hlAt": 5.0,
                                      "captions": [{"k": "VIC · TỪ 31/12/2025", "v": "+34,4%", "at": 5.4, "tone": "up"}]})
    elif "race" in sys.argv:
        series = [{"key": "vnindex", "label": "CHỨNG KHOÁN", "color": "#38bdf8"}, {"key": "btc", "label": "BITCOIN", "color": "#f97316"},
                  {"key": "deposit", "rate": 0.068, "label": "TIẾT KIỆM 6,8%", "color": "#4ade80"}]
        if (chartdata.DATA / "sjc_1d.csv").exists() and "--gold" in sys.argv:
            series.insert(1, {"key": "sjc", "label": "VÀNG SJC", "color": "#fbbf24"})
        sc = chartdata.attach_race({"type": "race", "t0": 0.0, "t1": dur, "from": "2026-01-02", "to": "2026-10-06", "series": series,
                                    "money": 20, "range": "02/01 → 06/10/2026", "drawAt": 0.8, "until": 6.8})
    else:
        sc = chartdata.attach({"type": "candles", "t0": 0.0, "t1": dur, "series": "vnindex", "from": "2025-01-20", "to": "2025-06-10",
                             "title": "VN-INDEX · KHUNG NGÀY", "range": "01/2025 – 06/2025", "drawAt": 0.5, "until": 4.4,
                             "ind": [{"k": "sma", "n": 20, "label": "MA20"}, {"k": "sma", "n": 50, "label": "MA50"}],
                             "marks": [{"date": "2025-04-03", "text": "03/04: −6,68%", "pos": "above", "tone": "down", "at": 6.2, "dx": -260, "dy": -40},
                                       {"date": "2025-04-09", "text": "09/04: đáy 1.073", "pos": "below", "tone": "gold", "at": 7.2, "dx": 260, "dy": 20}]})
    case = {"topic": key, "ch": "demo", "dur": dur, "seed": 7, "accent": "#fbbf24", "look": variety.look(None), "theme": "chart",
            "brand": "BIỂU ĐỒ BIẾT NÓI", "hud": {"k": "DEMO", "t": "CẢNH " + (mode or "BIỂU ĐỒ NẾN").upper()}, "acc": [], "lines": [], "imgs": {},
            "geo": None, "scenes": [sc], "prog0": 0, "prog1": 0}
    (od / "data.js").write_text("window.CASE = " + json.dumps(case, ensure_ascii=False) + ";\n", encoding="utf-8")
    comp = BL.HF / "compositions" / "long" / f"{key}.html"
    comp.write_text(BL.HTML.replace("{fonts}", variety.fonts_url(None)).replace("{data}", f"assets/long/{key}/data.js")
                    .replace("{dur}", f"{dur:.3f}").replace("{title}", "demo").replace("{videos}", ""), encoding="utf-8")
    out = od / "demo.mp4"
    from factory.render_lock import render_lock      # một render một lúc trên cả máy
    with render_lock(f"chart_demo {key}"):
        r = BL.subprocess.run(["npx.cmd", "-y", "-p", "node@22", "-p", "hyperframes@0.8.75", "hyperframes", "render", ".", "-c",
                               f"compositions/long/{key}.html", "-o", str(out), "--fps", "30", "--quiet", "--crf", "18"],
                              cwd=BL.HF, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or not out.exists():
        raise SystemExit(f"render hỏng\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
    print(out)


if __name__ == "__main__":
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    main()

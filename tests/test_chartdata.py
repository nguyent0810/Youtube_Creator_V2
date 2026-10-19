"""Chỉ báo cho cảnh biểu đồ kênh Biểu Đồ Biết Nói: tính đúng công thức, tính trên toàn lịch sử rồi mới cắt cửa sổ."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "motion" / "long"))
import chartdata as CD  # noqa: E402


def test_sma_is_the_plain_average_of_the_last_n_closes():
    assert CD.sma([1, 2, 3, 4, 5], 3) == [None, None, 2, 3, 4]


def test_ema_seeds_with_the_sma_then_weights_2_over_n_plus_1():
    e = CD.ema([1, 2, 3, 4, 5], 3)          # k = 0.5; mồi = (1+2+3)/3 = 2
    assert e[:2] == [None, None] and e[2] == 2 and e[3] == 3.0 and e[4] == 4.0


def test_window_indicators_already_have_history_behind_them(tmp_path, monkeypatch):
    rows = ["time,open,high,low,close,volume"] + [f"2025-01-{d:02d},{d},{d},{d},{d},1" for d in range(1, 31)]
    (tmp_path / "x_1d.csv").write_text("\n".join(rows), encoding="utf-8")
    monkeypatch.setattr(CD, "DATA", tmp_path)
    s = CD.attach({"series": "x", "from": "2025-01-25", "to": "2025-01-30", "ind": [{"k": "sma", "n": 20}]})
    assert [b[0] for b in s["bars"]] == [f"2025-01-{d}" for d in range(25, 31)]
    assert s["lines"][0]["vals"][0] == pytest.approx(sum(range(6, 26)) / 20)   # MA20 ngày 25 = TB ngày 6..25


def test_weekly_candles_resample_daily_ohlc_per_iso_week(tmp_path, monkeypatch):
    # T6 02/01/2026 (tuần ISO 1 bắt đầu 29/12/2025), rồi tuần 05–09/01 thiếu thứ Hai (nghỉ), rồi một phiên lẻ 12/01
    days = [("2026-01-02", 10, 12, 9, 11), ("2026-01-06", 11, 15, 10, 14), ("2026-01-07", 14, 14, 8, 9),
            ("2026-01-09", 9, 13, 9, 12), ("2026-01-12", 12, 12, 11, 11.5)]
    rows = ["time,open,high,low,close,volume"] + [f"{t},{o},{h},{lo},{c},100" for t, o, h, lo, c in days]
    (tmp_path / "x_1d.csv").write_text("\n".join(rows), encoding="utf-8")
    monkeypatch.setattr(CD, "DATA", tmp_path)
    w = CD.weekly(CD.load("x"))
    assert [(r["t"], r["o"], r["h"], r["l"], r["c"], r["v"], r["days"]) for r in w] == [
        ("2026-01-02", 10, 12, 9, 11, 100, 1),
        ("2026-01-06", 11, 15, 8, 12, 300, 3),     # mở = phiên đầu (thứ Ba), cao/thấp = max/min, đóng = phiên cuối
        ("2026-01-12", 12, 12, 11, 11.5, 100, 1)]
    s = CD.attach({"series": "x", "tf": "1w", "from": "2026-01-08", "to": "2026-01-09"})   # `from` giữa tuần -> lấy cả tuần
    assert s["bars"] == [["2026-01-06", 11, 15, 8, 12, 300]] and s["from"] == "2026-01-08"
    with pytest.raises(ValueError):
        CD.attach({"series": "x", "tf": "1M", "from": "2026-01-01", "to": "2026-01-31"})


def test_real_weekly_candle_09_13_03_2026_matches_analysis_csv():
    s = CD.attach({"series": "vnindex", "tf": "1w", "from": "2026-03-09", "to": "2026-03-13"})
    assert s["bars"] == [["2026-03-09", 1757.73, 1757.73, 1650.75, 1696.24, 5895324946.0]]   # = vnindex_1w_2026.csv (C3)
    yr = [b for b in CD.attach({"series": "vnindex", "tf": "1w", "from": "2026-01-05", "to": "2026-10-06"})["bars"]]
    assert len(yr) == 39                                                                    # "khoảng ba mươi chín cây nến tuần"


def test_real_vnindex_matches_the_published_record_drop():
    rows = {r["t"]: r for r in CD.load("vnindex")}
    assert rows["2025-04-03"]["c"] == 1229.84 and round(rows["2025-04-02"]["c"] - rows["2025-04-03"]["c"], 2) == 87.99


def test_race_gold_starts_at_minus_the_spread_and_deposit_accrues_daily(tmp_path, monkeypatch):
    (tmp_path / "vnindex_1d.csv").write_text("time,open,high,low,close,volume\n2026-01-02,1,1,1,100,1\n2026-07-02,1,1,1,90,1\n",
                                             encoding="utf-8")
    (tmp_path / "sjc_1d.csv").write_text("time,buy,sell\n2026-01-02,98,100\n2026-07-01,108,110\n", encoding="utf-8")
    monkeypatch.setattr(CD, "DATA", tmp_path)
    s = CD.attach_race({"from": "2026-01-02", "to": "2026-12-31", "series": [
        {"key": "vnindex"}, {"key": "sjc"}, {"key": "deposit", "rate": 0.073}]})
    vn, gold, dep = (x["vals"] for x in s["series"])
    assert vn == [0.0, -10.0]
    assert gold == [-2.0, 8.0]                      # mua 100 (giá bán ra), bán lại 98 / 108 (giá mua vào)
    assert dep[0] == 0 and dep[1] == pytest.approx(7.3 * 181 / 365, abs=0.01)


def test_race_keeps_precomputed_series_of_a_hypothetical_example(tmp_path, monkeypatch):
    monkeypatch.setattr(CD, "DATA", tmp_path)          # không đọc dữ liệu thị trường nào
    sc = {"dates": ["a", "b", "c"], "series": [{"label": "THUÊ", "vals": [0, 1.5, 3]}, {"label": "MUA", "vals": [-7, -5, 2]}]}
    assert CD.attach_race(sc)["series"][1]["vals"] == [-7, -5, 2]
    with pytest.raises(ValueError):
        CD.attach_race({"dates": ["a", "b"], "series": [{"label": "X", "vals": [0, 1, 2]}]})


def test_despike_drops_the_sjc_fallback_days_but_keeps_real_moves():
    s = {"d1": (100, 0), "d2": (101, 0), "d3": (80, 0), "d4": (80, 0), "d5": (100.5, 0), "d6": (88, 0), "d7": (87, 0)}
    out = CD.despike(s)
    assert "d3" not in out and "d4" not in out           # 2 ngày "giá hôm nay" rồi quay lại -> gai giả
    assert "d6" in out and "d7" in out                    # giảm thật và ở lại -> giữ


def test_rolled_deposit_compounds_yearly_with_each_years_rate():
    s = {"rates": [["2018-10-01", 0.10], ["2019-10-01", 0.05]]}
    assert CD._deposit(s, "2018-10-01", "2019-10-01") == pytest.approx(1.10)
    assert CD._deposit(s, "2018-10-01", "2020-10-01") == pytest.approx(1.10 * 1.05)


def test_outliers_drop_a_lone_fallback_price_between_two_agreeing_neighbours():
    s = {"a": (42.0, 0), "b": (140.5, 0), "c": (43.0, 0), "d": (70.0, 0)}
    assert set(CD.outliers(s)) == {"a", "c", "d"}            # d: neighbour gap is real (c->d), only b is dropped


def test_fallbacks_drop_copied_prices_but_keep_real_spikes():
    s = {"2020-07-02": (49.26, 49.64), "2020-07-20": (50.2, 50.6), "2020-07-27": (55.45, 56.9),
         "2020-08-03": (56.75, 57.9), "2020-08-04": (49.26, 49.64), "2020-08-10": (56.65, 58.28),
         "2020-08-17": (56.65, 58.28), "2020-08-24": (55.45, 56.55)}
    out = CD.fallbacks(s)
    assert "2020-08-04" not in out                        # bản sao y hệt 02/07 giữa đỉnh tháng 8 -> ngày giả
    assert {"2020-07-02", "2020-07-27", "2020-08-03"} <= set(out)   # cú tăng thật cuối tháng 7 vẫn giữ
    assert "2020-08-17" in out                            # trùng giá ngày KỀ (giá đứng) -> không phải ngày giả


def test_fallbacks_keep_a_flat_price_that_matches_its_neighbours():
    s = {"2024-10-01": (79.8, 81.8), "2024-10-02": (79.0, 81.0), "2024-10-07": (79.8, 81.8),
         "2024-10-14": (79.8, 81.8), "2024-10-21": (86.0, 88.0), "2024-10-28": (87.0, 89.0),
         "2024-11-01": (79.8, 81.8), "2024-11-04": (87.0, 89.0), "2024-11-11": (81.9, 85.4)}
    out = CD.fallbacks(s)
    assert "2024-11-01" not in out                        # quay về đúng giá 01/10 giữa vùng 86–89 -> giả
    assert {"2024-10-01", "2024-10-07", "2024-10-14"} <= set(out)


def test_overrides_replace_or_drop_days(tmp_path, monkeypatch):
    monkeypatch.setattr(CD, "DATA", tmp_path)
    (tmp_path / "sjc_overrides.csv").write_text("time,buy,sell,source\n2026-09-30,141.1,144.1,x\n2026-10-01,,,y\n",
                                                encoding="utf-8")
    out = CD.overrides({"2026-09-29": (139.5, 142.5), "2026-09-30": (139.5, 142.5), "2026-10-01": (139.5, 142.5)})
    assert out == {"2026-09-29": (139.5, 142.5), "2026-09-30": (141.1, 144.1)}


# ---------- breadth / basket (độ rộng & treemap vốn hoá HOSE, data/ck/breadth_2026/) ----------
def test_bucket_colours_split_by_sign_then_magnitude():
    assert [CD.bucket(x) for x in (-45, -30, -29.99, -15, -5, -0.01, 0, 0.01, 4.99, 5, 15, 30, 80)] == \
        [-4, -4, -3, -3, -2, -1, 0, 1, 1, 2, 3, 4, 4]


def test_vn_num_uses_vietnamese_separators_and_a_real_minus():
    assert CD.vn_num(-0.89) == "−0,9" and CD.vn_num(1234.5) == "+1.234,5" and CD.vn_num(0, 2) == "0,00"


def _area(r):
    return r[2] * r[3]


def test_squarify_areas_are_proportional_and_tile_the_box_without_overlap():
    vals = [50, 20, 10, 8, 5, 3, 2, 1, 0.5, 0.5]
    box = (100.0, 50.0, 800.0, 400.0)
    rs = CD.squarify(vals, *box)
    tot = box[2] * box[3]
    for v, r in zip(vals, rs):
        assert _area(r) == pytest.approx(tot * v / sum(vals), rel=1e-9)
        assert box[0] - 1e-6 <= r[0] and r[0] + r[2] <= box[0] + box[2] + 1e-6
        assert box[1] - 1e-6 <= r[1] and r[1] + r[3] <= box[1] + box[3] + 1e-6
    for i, a in enumerate(rs):
        for b in rs[i + 1:]:
            ox = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
            oy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
            assert ox <= 1e-6 or oy <= 1e-6
    assert sum(map(_area, rs)) == pytest.approx(tot)
    assert max(r[2] / r[3] if r[2] > r[3] else r[3] / r[2] for r in rs[:3]) < 3      # ô lớn gần vuông


def test_squarify_is_deterministic():
    vals = [9, 7, 7, 4, 2, 1]
    assert CD.squarify(vals, 0, 0, 300, 200) == CD.squarify(vals, 0, 0, 300, 200)


def test_breadth_on_30_09_matches_summary_json_291_of_400_below():
    s = CD.attach_breadth({"date": "2026-09-30"})
    summ = json.loads((CD.DATA / "breadth_2026" / "summary.json").read_text(encoding="utf-8"))["ytd_q3"]
    st = s["stats"]
    assert (st["n"], st["below"], st["flat"], st["above"]) == (400, 291, 1, 108)
    assert (st["n"], st["below"], st["flat"], st["above"], st["median"]) == \
        (summ["n"], summ["below"], summ["flat"], summ["above"], summ["median_pct"])
    assert st["vni"] == -0.89
    b = [d[1] for d in s["dots"]]
    assert sum(x < 0 for x in b) == 291 and sum(x > 0 for x in b) == 108          # số chấm đỏ = số mã giảm
    assert [d[0] for d in s["dots"]] == sorted(d[0] for d in s["dots"])            # xếp giảm mạnh -> tăng mạnh


def test_breadth_frames_agree_with_breadth_daily_pct_below():
    s = CD.attach_breadth({"date": "2026-09-30", "animate": {"from": "2026-05-18", "to": "2026-09-30", "every": 20}})
    daily = {r["date"]: float(r["pct_below"]) for r in CD._csv(CD.DATA / "breadth_2026" / "breadth_daily.csv")}
    assert s["frames"][0]["d"] == "2026-05-18" and s["frames"][-1]["d"] == "2026-09-30"
    for f in s["frames"]:
        assert len(f["b"]) == 400 and f["pb"] == pytest.approx(daily[f["d"]], abs=0.3)
    assert s["frames"][0]["below"] == 256 and s["frames"][-1]["b"] == [d[1] for d in s["dots"]]


def test_basket_concentration_on_30_09():
    s = CD.attach_basket({"date": "2026-09-30", "groupSmall": 200})
    st = s["stats"]
    assert st["n"] == 400 and st["top"][0][0] == "VIC"
    assert st["top"][0][1] == pytest.approx(21.45, abs=0.05)
    assert st["top10"] == pytest.approx(52.2, abs=0.1) and st["group"] == pytest.approx(1.28, abs=0.02)
    rs = s["rects"]
    assert len(rs) == 201 and sum(r[0] == "*" for r in rs) == 1
    assert sum(r[5] for r in rs) == pytest.approx(100, abs=0.01)
    box_area = CD.BASKET_BOX[2] * CD.BASKET_BOX[3]
    for r in rs:                                                                    # diện tích ô = tỉ trọng vốn hoá
        assert r[3] * r[4] == pytest.approx(box_area * r[5] / 100, rel=1e-3, abs=6)   # tỉ trọng làm tròn 3 số lẻ
    assert s["labels"][:3] == ["VIC", "VHM", "VCB"] and len(s["labels"]) == 10


def test_basket_at_year_start_matches_w0_pct_column():
    s = CD.attach_basket({"date": "2025-12-31", "labels": ["VIC"]})
    w0 = {r["symbol"]: float(r["w0_pct"]) for r in CD._csv(CD.DATA / "breadth_2026" / "breadth_2026.csv") if r["w0_pct"]}
    for sym, share in s["stats"]["top"]:
        assert share == pytest.approx(w0[sym], abs=0.01)
    assert s["labels"] == ["VIC"]


# ---------- breadth theo % trong ngày (base "prev") + cảnh sổ lệnh giả định (chart.js B.book), video C2 ----------
def test_breadth_prev_on_09_03_matches_the_c2_factcheck():
    s = CD.attach_breadth({"date": "2026-03-09", "base": "prev"})
    st = s["stats"]
    assert (st["n"], st["below"], st["above"], st["flat"]) == (395, 368, 11, 16)
    assert st["median"] == -6.8 and st["vni"] == -6.51 and st["base"] == "prev"
    assert s["palette"] == "board" and s["legend"]["lo"] == "≤ −6,5%"
    assert [d[0] for d in s["dots"]] == sorted(d[0] for d in s["dots"])
    assert sum(d[1] == -4 for d in s["dots"]) == sum(d[0] <= -6.5 for d in s["dots"])   # bậc −4 = sát sàn


def test_bucket_day_splits_a_7pct_band():
    assert [CD.bucket_day(p) for p in (-7, -6.5, -6.49, -3, -0.5, 0, 0.5, 2.9, 6.9)] == [-4, -4, -3, -3, -1, 0, 1, 2, 4]


def test_breadth_prev_rejects_animate_and_missing_date():
    with pytest.raises(ValueError):
        CD.attach_breadth({"base": "prev"})
    with pytest.raises(ValueError):
        CD.attach_breadth({"date": "2026-03-09", "base": "prev", "animate": {"from": "2026-03-02"}})


def test_chart_js_book_scene_is_additive_and_always_labels_hypothetical():
    js = (Path(__file__).resolve().parents[1] / "motion" / "hf" / "assets" / "engine" / "chart.js").read_text(encoding="utf-8")
    css = (Path(__file__).resolve().parents[1] / "motion" / "hf" / "assets" / "engine" / "casewide.css").read_text(encoding="utf-8")
    assert "B.book = " in js and 'if (C.theme !== "chart") return;' in js          # chỉ theme chart
    assert '"VÍ DỤ GIẢ ĐỊNH"' in js and "s.hypo !== false" in js                    # nhãn giả định mặc định bật
    for cls in (".obhypo", ".obo", ".obrow", ".obbar", ".obm", ".obtag", ".obme", ".obcnt"):
        assert cls in css
    ob = [ln for ln in css.splitlines() if ln.startswith(".ob")]
    assert ob and not any("overflow" in ln for ln in ob)                             # không cắt dấu tiếng Việt

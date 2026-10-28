"""webauto studio: gộp CSV xuất từ YouTube Studio và các hàm thuần của bộ thu thập. Không trình duyệt, không mạng.

Dữ liệu giả có đúng cấu trúc bản xuất thật (tiêu đề tiếng Anh, dòng Total, dòng chú thích
"Showing top 500 results"), nên đây cũng là tài liệu về định dạng đầu vào.
"""
import csv
import io
import json
import zipfile
from datetime import date, timedelta

import pytest

from webauto import studio, studio_summary as ss

TODAY = date(2026, 10, 28)
HEAD = ["Content", "Video title", "Video publish time", "Duration", "Views", "Watch time (hours)", "Subscribers",
        "Thumbnail impressions", "Thumbnail click-through rate (%)", "Average view duration",
        "Average percentage viewed (%)"]


def csv_text(header, rows):
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows([header] + rows)  # quotes "Oct 20, 2026" like the real export
    return buf.getvalue()


def videos_table(scale, footer):
    rows = [
        ["Total", "", "", "", 1000 * scale, 50 * scale, 20 * scale, 9000 * scale, 3.0, 20, 70],
        ["vidA", "Short thắng lớn", "Oct 20, 2026", 25, 600 * scale, 20 * scale, 12 * scale, 4000 * scale, 5.0, 18, 80],
        ["vidB", "Long ít người xem", "Sep 01, 2026", 600, 300 * scale, 25 * scale, 6 * scale, 4000 * scale, 1.0, 120, 30],
        ["vidC", "Short thường", "Aug 01, 2025", 30, 100 * scale, 5 * scale, 2 * scale, 1000 * scale, 2.0, 15, 60],
    ]
    out = csv_text(HEAD, rows)
    return out + ("Showing top 500 results\n" if footer else "")


def daily_table():
    start = TODAY - timedelta(days=55)
    rows = []
    for i in range(56):
        d = (start + timedelta(days=i)).isoformat()
        rows.append([d, 10 if i < 28 else 20, 1, 0])
    return csv_text(["Date", "Views", "Watch time (hours)", "Subscribers"], rows)


def make_folder(tmp_path, footer=True):
    files = {
        "videos__28d": {"table": videos_table(1, footer)},
        "videos__lifetime": {"table": videos_table(10, False)},
        "daily__28d": {"table": daily_table()},
        "traffic_source__28d": {"table": csv_text(
            ["Traffic source", "Views", "Watch time (hours)"],
            [["Total", 1000, 50], ["Shorts feed", 800, 30], ["Search", 200, 20]])},
        "traffic_source__lifetime": {"table": csv_text(
            ["Traffic source", "Views", "Watch time (hours)"],
            [["Total", 5000, 300], ["Shorts feed", 3000, 100], ["Search", 1500, 150], ["Browse", 500, 50]])},
    }
    reports = []
    for key, kinds in files.items():
        rep, per = key.split("__")
        rels = {}
        for kind, text in kinds.items():
            p = tmp_path / "raw" / key / f"{kind}.csv"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
            rels[kind] = f"raw/{key}/{kind}.csv"
        reports.append({"report": rep, "period": per, "status": "ok", "files": rels})
    reports.append({"report": "age", "period": "28d", "status": "failed", "reason": "no candidate id rendered"})
    (tmp_path / "manifest.json").write_text(json.dumps(
        {"channel_id": "UCxxxxxxxxxxxxxxxxxxxxxx", "channel_name": "Kênh thử", "collected": "2026-10-28T10:00:00",
         "reports": reports}), encoding="utf-8")
    return tmp_path


def test_num_va_ngay():
    assert ss.num("1,234") == 1234 and ss.num("3.2") == 3.2
    assert ss.num("—") is None and ss.num("") is None and ss.num(None) is None
    assert ss.parse_date("Oct 20, 2026") == date(2026, 10, 20)
    assert ss.parse_date("2026-10-20") == date(2026, 10, 20) and ss.parse_date("lạ") is None


def test_summarize_gop_video_va_chi_so_dan_xuat(tmp_path):
    s, videos = ss.summarize(make_folder(tmp_path), TODAY)
    assert s["main_period"] == "28d" and s["video_count"] == 3  # dòng Total và dòng chú thích không phải video
    assert s["truncated_at_500_videos"] == ["28d"]
    a = videos["vidA"]
    assert a["format"] == "short" and videos["vidB"]["format"] == "long"
    assert a["age_days"] == 8
    assert a["28d"]["subs_per_1k_views"] == 20.0  # 12 sub / 600 views
    assert a["lifetime"]["views"] == 6000
    assert s["top_views"][0]["id"] == "vidA" and s["bottom_views"][0]["id"] == "vidC"
    assert s["best_ctr"][0]["id"] == "vidA" and s["worst_ctr"][0]["id"] == "vidB"
    assert s["channel_totals"]["lifetime"]["views"] == 10000


def test_theo_dinh_dang_va_tuoi(tmp_path):
    s, _ = ss.summarize(make_folder(tmp_path), TODAY)
    f = s["by_format"]["28d"]
    assert f["short"]["videos"] == 2 and f["short"]["views"] == 700 and f["long"]["views"] == 300
    ages = {x["age"]: x for x in s["by_age"]}
    assert (ages["0-7d"]["videos"], ages["0-7d"]["views"]) == (0, 0)
    assert (ages["8-28d"]["videos"], ages["8-28d"]["views"]) == (1, 600)   # vidA: 8 ngày tuổi
    assert (ages["29-90d"]["videos"], ages["29-90d"]["views"]) == (1, 300)  # vidB: 57 ngày
    assert (ages["91-365d"]["videos"], ages["91-365d"]["views"]) == (0, 0)
    assert (ages[">365d"]["videos"], ages[">365d"]["views"]) == (1, 100)   # vidC: hơn một năm
    assert sum(a["share_pct"] for a in s["by_age"]) == pytest.approx(100.0, abs=0.2)


def test_xu_huong_ngay_va_chieu_phan_tich(tmp_path):
    s, _ = ss.summarize(make_folder(tmp_path), TODAY)
    d = s["daily"]["28d"]
    assert d["days"] == 56 and d["change_28d_pct"]["views"] == 100.0
    assert d["last_28d"]["views"] == 560 and d["prev_28d"]["views"] == 280
    t = s["dimensions"]["traffic_source"]["28d"]
    assert t["column"] == "Traffic source" and t["rows"][0]["name"] == "Shorts feed" and t["rows"][0]["share_pct"] == 80.0


def test_bang_chieu_khong_co_cot_views_van_chon_cot_chinh(tmp_path):
    header, rows = ["Subscription source", "Subscribers", "Subscribers gained", "Subscribers lost"], [
        ["Total", "10", "14", "4"], ["Shorts feed", "8", "10", "2"], ["Channel page", "2", "4", "2"]]
    f = tmp_path / "t.csv"
    f.write_text(csv_text(header, rows), encoding="utf-8")
    out = ss.dimension_table({"table": ss.read_csv(f)})
    assert out["primary"] == "Subscribers" and out["rows"][0]["name"] == "Shorts feed"
    assert out["rows"][0]["share_pct"] == 80.0 and out["rows"][1]["Subscribers lost"] == 2


def test_markdown_va_file_dau_ra(tmp_path):
    out = tmp_path / "out"
    md, js, vcsv = ss.write_outputs(make_folder(tmp_path), out, TODAY)
    text = md.read_text(encoding="utf-8")
    assert "Kênh thử" in text and "bị Studio cắt ở 500 dòng" in text and "Shorts feed" in text
    assert "- Traffic source (lifetime): Shorts feed 60%; Search 30%; Browse 10%" in text  # kỳ phụ: một dòng
    assert text.count("## Traffic source") == 1  # chỉ kỳ chính có bảng đầy đủ
    assert text.count("## Xu hướng theo ngày") == 1  # một mục xu hướng, không lặp theo từng kỳ
    header_row = next(l for l in text.split("## Top lượt xem")[1].splitlines() if l.startswith("| id"))
    assert header_row.count("views") == 1  # không có hai cột views trùng nhau
    assert "age/28d: no candidate id rendered" in text  # báo cáo không lấy được vẫn được liệt kê
    assert len(text) < 8000  # đủ gọn để đưa cho LLM
    assert json.loads(js.read_text(encoding="utf-8"))["video_count"] == 3
    header = vcsv.read_text(encoding="utf-8-sig").splitlines()[0].split(",")
    assert "28d_views" in header and "lifetime_subs_per_1k_views" in header


def test_build_url_co_du_tham_so():
    u = studio.build_url("UCabc", "4_weeks", "VIDEO", studio.METRICS_MIN)
    assert u.startswith("https://studio.youtube.com/channel/UCabc/analytics/") and "explore?" in u
    assert u.count("t_metrics=") == 2 and "dimension=VIDEO" in u and "time_period=4_weeks" in u
    assert "metric=EXTERNAL_VIEWS" in u


def test_classify_theo_tieu_de():
    entries = [(0, ["Content", "Views"]), (1, ["Date", "Content", "Views"]), (2, ["Date", "Views"])]
    assert studio.classify(entries, "videos") == {0: "table", 1: "chart", 2: "totals"}
    daily = [(0, ["Date", "Views"]), (1, ["Date", "Views", "Watch time (hours)", "Subscribers"])]
    assert studio.classify(daily, "daily") == {1: "table", 0: "totals"}


def test_extract_dat_ten_theo_loai_khong_theo_ten_trong_zip(tmp_path):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("Dữ liệu trong bảng.csv", "Content,Views\nTotal,5\n")
        z.writestr("../evil.csv", "Date,Content,Views\n2026-10-01,a,1\n")
        z.writestr("Tổng số.csv", "Date,Views\n2026-10-01,5\n")
        z.writestr("readme.txt", "bỏ qua")
    zp = tmp_path / "x.zip"
    zp.write_bytes(buf.getvalue())
    got = studio.extract(zp, tmp_path / "dest", "videos")
    assert set(got) == {"table", "chart", "totals"}
    assert all(p.parent == tmp_path / "dest" for p in got.values())
    assert not (tmp_path / "evil.csv").exists()


def test_plan_gioi_han_ky_cho_bao_cao_chieu():
    p = studio.plan(["videos", "geography"], ["7d", "28d", "lifetime"])
    assert p == [("videos", "28d"), ("videos", "lifetime"), ("videos", "7d"), ("geography", "28d"), ("geography", "lifetime")]
    assert ("geography", "7d") not in p


def test_catalog_luu_va_doc(monkeypatch, tmp_path):
    monkeypatch.setenv("WEBAUTO_HOME", str(tmp_path))
    cat = studio.load_catalog()
    assert cat == {"periods": {}, "dimensions": {}, "metric_sets": {}}
    cat["dimensions"]["age"] = "VIEWER_AGE"
    studio.save_catalog(cat)
    assert studio.load_catalog()["dimensions"]["age"] == "VIEWER_AGE"
    assert studio.load_catalog(refresh=True)["dimensions"] == {}


def test_moi_chieu_co_ma_va_bo_chi_so_hop_le():
    """Mọi báo cáo đều có ứng viên; bộ chỉ số riêng của từng báo cáo trỏ đúng vào METRIC_SETS."""
    assert set(studio.DIMENSION_CANDIDATES) >= set(studio.REPORT_METRIC_SETS)
    for rep, order in studio.REPORT_METRIC_SETS.items():
        assert all(0 <= i < len(studio.METRIC_SETS) for i in order), rep
    assert studio.DIMENSION_CANDIDATES["subscription_source"] == ["SUBSCRIPTION_SOURCE_TYPE"]
    assert studio.METRIC_SETS[studio.REPORT_METRIC_SETS["subscription_source"][0]][0] == "SUBSCRIBERS_NET_CHANGE"
    for p in ("7d", "28d", "90d", "365d", "lifetime"):
        assert studio.PERIOD_CANDIDATES[p]

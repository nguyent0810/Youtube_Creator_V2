"""Trend Engine cho FS/BUD: danh sách chặn, kênh theo keywords.json, TREND_CONTACT, lịch sử signal."""
from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

import pytest

from factory.trend import report as report_module
from factory.trend.cluster import cluster_db
from factory.trend.report import _belongs, _deny, _keywords, configured_channels, deny_reason, write_report
from factory.trend.scan import TrendContactMissing, _article, init_db, scan_sources, signal_history, user_agent
from factory.trend.sources import load_sources

NOW = datetime(2026, 11, 3, 12, tzinfo=UTC)


def src(source_id: str, channels: list[str]) -> dict[str, object]:
    return {"id": source_id, "url": f"https://{source_id}.test/rss", "kind": "rss", "role": "article", "lang": "vi",
            "owner_group": source_id, "channels": channels, "tos_status": "ok", "tos_note": "fixture", "trial": "internal"}


def test_deny_json_covers_required_groups_and_distinguishes_diacritics() -> None:
    deny = _deny()
    labels = {group["label"] for group in deny["groups"].values()}
    for needed in ("thiên tai", "tai nạn", "người chết/tang", "chính trị/bầu cử", "tội phạm", "dịch bệnh", "tin đồn/chưa kiểm chứng", "doạ/xui rủi", "hứa tiền/làm giàu"):
        assert needed in labels
    assert deny_reason("Bão số 9 đổ bộ miền Trung", deny, "FS") == "thiên tai: bão"
    assert deny_reason("Báo Giác Ngộ đăng lịch lễ Vu Lan", deny, "BUD") is None  # báo != bão
    assert deny_reason("Sao hạn 2027: điềm báo xấu cho tuổi Mùi", deny, "FS") == "doạ/xui rủi: điềm báo"
    assert deny_reason("Bão số 9 đổ bộ miền Trung", deny, "MIM") is None  # MIM/CK không áp danh sách chặn


BLOCK = [
    "Bão số 9 đổ bộ miền Trung", "Sập cầu khiến nhiều người thiệt mạng", "Nghệ sĩ qua đời, tang lễ tổ chức sáng mai",
    "Bầu cử Mỹ: kết quả mới nhất", "Khởi tố vụ án lừa đảo tại chùa", "Ổ dịch sốt xuất huyết lan rộng",
    "Tin đồn chưa kiểm chứng về ngày tận thế", "Sao hạn 2027: điềm báo xấu cho tuổi Mùi", "Cách làm giàu nhanh theo phong thủy",
    "Trúng số nhờ đặt tượng Phật hướng này",
]
ALLOW = [
    "Lễ Vu Lan báo hiếu tại chùa", "Sinh tử luân hồi trong lời Phật dạy", "Rằm tháng Mười 2026 cúng gì",
    "Giá vàng hôm nay", "Ngày tốt tháng 11 âm lịch để xuất hành", "Hiểu về cái chết trong thiền định",
    "Chùa cổ sập sệ cần trùng tu, Phật tử góp công", "Mưa sao băng Song Tử đêm nay", "Báo Giác Ngộ giới thiệu kinh Kim Cang",
    "Tết Đinh Mùi 2027 mùng 1 là ngày nào",
]


def test_deny_two_way_titles() -> None:
    deny = _deny()
    for title in BLOCK:
        assert deny_reason(title, deny, "FS") and deny_reason(title, deny, "BUD"), title
    for title in ALLOW:
        assert deny_reason(title, deny, "FS") is None, title
        assert deny_reason(title, deny, "BUD") is None, title


def test_configured_channels_ignore_unknown_metadata_keys() -> None:
    keywords = {"channels": ["MIM", "FS"], "MIM": ["ai"], "FS": ["rằm"], "_ghi_chu": "x", "vn_impact": {}, "version": ["1"]}
    assert configured_channels(keywords) == ["MIM", "FS"]
    assert configured_channels({"MIM": ["ai"]}) == []


def _db_with(conn, items: list[tuple[str, str, str]]) -> None:
    for n, (source_id, title, summary) in enumerate(items):
        article = _article(f"https://{source_id}.test/{n}", title, summary, NOW.isoformat(), src(source_id, ["FS", "BUD"]), NOW)
        conn.execute("INSERT INTO article(url,title,summary,published_at,source_id,owner_group,fetched_at,undated,trend_title) VALUES(:url,:title,:summary,:published_at,:source_id,:owner_group,:fetched_at,:undated,:trend_title)", article)
    conn.commit()


def test_report_blocks_denied_cluster_but_records_reason(tmp_path, monkeypatch) -> None:
    sources = [src("kv", ["FS", "BUD"])]
    path = tmp_path / "sources.json"; path.write_text(json.dumps(sources), encoding="utf-8")
    db = tmp_path / "t.sqlite"
    conn = init_db(db)
    _db_with(conn, [("kv", "Lịch âm tháng Mười một: ngày tốt Rằm 2026 cho Tết Đinh Mùi", ""),
                    ("kv", "Bão lớn khiến chùa Rằm bị sập, nhiều người tử vong", "")])
    conn.close()
    cluster_db(db, sources_path=path, now=NOW)
    out = write_report(db, tmp_path / "out", sources_path=path, now=NOW).read_text(encoding="utf-8")
    fs = out.split("## FS")[1].split("## BUD")[0]
    assert "ngày tốt Rằm 2026" in fs.split("#### ĐÃ CHẶN")[0]
    assert "Bão lớn" not in fs.split("#### ĐÃ CHẶN")[0]
    assert "lý do: thiên tai: bão" in fs.split("#### ĐÃ CHẶN")[1]
    assert "## MIM" in out and "#### ĐÃ CHẶN" in out


def test_channels_come_from_keywords_and_fs_bud_work() -> None:
    keywords = _keywords()
    assert configured_channels(keywords)[:2] == ["MIM", "CK"] and {"FS", "BUD"} <= set(configured_channels(keywords))
    for channel in ("FS", "BUD"):
        assert 0 < len(keywords[channel]) <= 15
    sources = {"s": src("s", ["FS", "BUD"])}
    assert _belongs({"source_id": "s", "title": "Rằm tháng Mười: lịch cúng", "summary": ""}, "FS", sources, keywords)
    assert _belongs({"source_id": "s", "title": "Lễ Phật đản tại chùa lớn", "summary": ""}, "BUD", sources, keywords)
    assert not _belongs({"source_id": "s", "title": "Giá điện tăng", "summary": ""}, "BUD", sources, keywords)


def test_mim_ck_output_identical_with_and_without_new_sources(tmp_path) -> None:
    core = src("kv", ["MIM", "CK"])
    gtrends = {**src("google_trends_vn", ["FS", "BUD"]), "role": "article+signal"}
    off = tmp_path / "off.json"; off.write_text(json.dumps([core]), encoding="utf-8")
    on = tmp_path / "on.json"; on.write_text(json.dumps([core, gtrends]), encoding="utf-8")
    items = [("kv", "OpenAI ra mắt chip AI mới tại Việt Nam", ""), ("kv", "EVN giảm giá điện, lãi suất giữ nguyên", "")]
    extra = [("google_trends_vn", "OpenAI chip AI Việt Nam rằm tháng Mười", ""), ("google_trends_vn", "Rằm tháng Mười 2026 cúng gì", "")]

    def run(sources_path, rows, name: str) -> str:
        db = tmp_path / f"{name}.sqlite"
        conn = init_db(db)
        _db_with(conn, rows)
        conn.execute("INSERT INTO signal(source_id,title,normalized_title,observed_at,value,baseline,kind,run_id) VALUES('google_trends_vn','openai chip','openai chip',?,500,NULL,'trends',?)", (NOW.isoformat(), NOW.isoformat()))
        conn.commit(); conn.close()
        cluster_db(db, sources_path=sources_path, now=NOW)
        text = write_report(db, tmp_path / name, sources_path=sources_path, now=NOW).read_text(encoding="utf-8")
        return text.split("## FS")[0]

    before = run(off, items, "off")
    after = run(on, items + extra, "on")
    assert before == after and "## MIM" in before and "## CK" in before


def test_trial_sources_enabled_without_blocked_ones() -> None:
    enabled = {s["id"] for s in load_sources() if s.get("trial") == "internal"}
    assert {"google_trends_vn", "wikipedia_pageviews_vi"} <= enabled
    assert all(s["tos_status"] == "ok" for s in load_sources() if s.get("trial") == "internal")
    fs_sources = [s for s in load_sources() if "FS" in s["channels"]]
    assert {s["id"] for s in fs_sources} == {"google_trends_vn", "wikipedia_pageviews_vi"}
    assert all(set(s["channels"]) == {"FS", "BUD"} for s in fs_sources)  # không đụng MIM/CK


def test_user_agent_requires_real_contact(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("TREND_CONTACT", raising=False)
    with pytest.raises(TrendContactMissing):
        user_agent()
    with pytest.raises(TrendContactMissing):  # quét thật (không có fetch giả) bị chặn trước khi gọi mạng
        scan_sources(tmp_path / "x.sqlite")
    monkeypatch.setenv("TREND_CONTACT", "po@kenh.test")
    assert user_agent().endswith("po@kenh.test") and "example" not in user_agent()
    # Có fetch giả (test/fixture) thì vẫn chạy khi thiếu contact.
    monkeypatch.delenv("TREND_CONTACT")
    empty = tmp_path / "empty.json"; empty.write_text("[]", encoding="utf-8")
    assert scan_sources(tmp_path / "y.sqlite", sources_path=empty, fetch=lambda _u: b"", now=NOW)["errors"] == 0


def test_signals_kept_per_run_and_cluster_uses_latest(tmp_path) -> None:
    path = tmp_path / "sources.json"
    wiki = {**src("wiki", ["FS"]), "kind": "wiki_pageviews", "role": "signal", "url": "https://wiki.test/{YYYY}/{MM}/{DD}"}
    path.write_text(json.dumps([wiki]), encoding="utf-8")
    db = tmp_path / "t.sqlite"

    def fetch_for(views: int):
        def fetch(url: str) -> bytes:
            if url.endswith("robots.txt"):
                return b""
            return json.dumps({"items": [{"articles": [{"article": "Âm lịch", "views": views}]}]}).encode()
        return fetch

    first = scan_sources(db, sources_path=path, fetch=fetch_for(100), pause_seconds=0, now=NOW)
    second = scan_sources(db, sources_path=path, fetch=fetch_for(300), pause_seconds=0, now=NOW + timedelta(days=1))
    assert first["signals"] == 1 and second["signals"] == 1
    conn = init_db(db)
    history = signal_history(conn, "am lich", "wiki")
    assert [value for _run, value in history] == [100.0, 300.0]
    # Hết hạn sau 30 ngày
    scan_sources(db, sources_path=path, fetch=fetch_for(1), pause_seconds=0, now=NOW + timedelta(days=40))
    assert [value for _run, value in signal_history(init_db(db), "am lich")] == [1.0]

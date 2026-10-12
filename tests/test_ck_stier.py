"""S-tier 9:16 cho kênh Biểu Đồ Biết Nói (CK, theme "ck"): theme, khoảng lặng giữa câu, vào kho, luật cứng spec.

Định vị + 7 luật cứng: docs/channels/chung-khoan/2026-10-06-positioning.md. Theme "case"/"mim" phải giữ nguyên.
"""
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "stier"), str(ROOT / "motion")]

import themes  # noqa: E402

SPECS = ROOT / "data" / "stier" / "specs"
CK_SPECS = sorted(SPECS.glob("ck-*.json"))


# ── 1. Theme: CK thêm vào, MIM/CL không đổi ───────────────────────────────

def test_ck_theme_has_its_own_voice_tracks_ledger_and_css():
    t = themes.THEMES["ck"]
    assert (t["voice"], t["accent"], t["sound"], t["img_license"]) == ("Ngọc Huyền", "#fbbf24", "music", "by")   # giọng Short CK từ 12/10/2026
    assert t["js"]["cls"] == "theme-ck" and t["js"]["css"] == "theme-ck.css"
    assert (ROOT / "motion" / "hf" / "assets" / "engine" / "theme-ck.css").exists()
    assert t["ledger"] != themes.MUSIC_LEDGER                          # không xoay vòng chung sổ với MIM
    assert not set(themes.tracks(t)) & set(themes.MIM_TRACKS)           # thư viện nhạc riêng, không lặp nhạc kênh MIM
    assert all((themes.ROOT / "output" / "music" / f).exists() for f in themes.tracks(t))
    assert not {"glitch", "flicker", "type"} & {fx for k in "NASDX" for fx in t["pools"][k]}   # tiền bạc: không giật gân


def test_mim_and_case_keep_the_old_music_and_html():
    assert themes.tracks(themes.THEMES["mim"]) is themes.MIM_TRACKS
    assert "css" not in themes.THEMES["mim"]["js"] and themes.THEMES["case"]["js"] == {}
    assert themes.music_credit("bit_shift.mp3").startswith('Music: "Bit Shift" by Kevin MacLeod')
    import build
    assert build.HTML.count("{css}") == 1                               # theme không khai báo css -> thay bằng ""


# ── 2. Khoảng lặng giữa câu (gap) ─────────────────────────────────────────

class Engine:
    def infer(self, text, voice=None):
        import numpy as np
        return np.zeros(4800, dtype="float32")


def test_gap_adds_silence_between_lines_only_and_is_part_of_the_cache_key(monkeypatch, tmp_path):
    import build
    from factory import speak as SP
    monkeypatch.setattr(build, "_engine", Engine())
    d = 4800 / SP.SAMPLE_RATE
    t0 = build.speak(["Một.", "Hai.", "Ba."], tmp_path / "v.wav", tmp_path / "t.json", voice="Xuân Vĩnh")
    assert "gap" not in t0 and t0["segments"][1]["start"] == pytest.approx(d, abs=1e-3)
    t1 = build.speak(["Một.", "Hai.", "Ba."], tmp_path / "v.wav", tmp_path / "t.json", voice="Xuân Vĩnh", gap=0.5)
    assert t1["gap"] == 0.5
    assert t1["segments"][1]["start"] == pytest.approx(d + 0.5, abs=1e-3)
    assert t1["duration"] == pytest.approx(3 * d + 2 * 0.5, abs=1e-3)   # không lặng sau câu cuối


# ── 3. Spec CK: luật cứng ─────────────────────────────────────────────────

BANKS = r"vietcombank|vietinbank|bidv|agribank|techcombank|vpbank|acb\b|sacombank|mb ?bank|tpbank|hdbank|shb\b|" \
        r"timo|cake\b|vikki|ncb\b|gpbank|lpbank|hose|hnx|upcom|binance|okx|bybit"


@pytest.mark.parametrize("p", CK_SPECS, ids=lambda p: p.stem)
def test_ck_specs_follow_the_hard_rules(p):
    s = json.loads(p.read_text(encoding="utf-8"))
    assert s["theme"] == "ck"
    assert "Nội dung giáo dục, không phải tư vấn đầu tư." in s["description"]
    shown = json.dumps({k: s[k] for k in ("title", "description", "lines", "scenes", "tags")}, ensure_ascii=False).lower()
    assert not re.search(BANKS, shown), "không nêu tên ngân hàng / sàn"
    assert not re.search(r"nên mua|nên bán|nên giữ|sẽ tăng|sắp tăng|sẽ giảm|sắp giảm", shown), "không khuyến nghị, không dự báo"
    if s.get("rules", 1) < 2:   # bộ luật 1 (06/10): kết bằng câu hỏi. Bộ luật 2 (12/10, docs/pm/2026-10-12-shorts-analysis.md mục 7):
        assert s["lines"][-1].rstrip().endswith("?") and s["scenes"][-1]["type"] == "question"
    else:                       # kết ở câu chốt -- không câu hỏi cuối, không mời xem video dài trong lời đọc
        assert not s["lines"][-1].rstrip().endswith("?") and s["scenes"][-1]["type"] != "question"
        assert not re.search(r"video dài|trên kênh", " ".join(s["lines"]).lower())
    assert s["sources"] and all(u.startswith("https://") for u in s["sources"])
    assert 55 <= sum(len(x.split()) for x in s["lines"]) <= 135


# ── 4. Vào kho (không upload) ─────────────────────────────────────────────

def test_a_ck_bundle_carries_disclaimer_sources_music_credit_and_utc_time(monkeypatch, tmp_path):
    import enqueue_ck as E
    spec = json.loads(CK_SPECS[0].read_text(encoding="utf-8"))
    (tmp_path / "specs").mkdir()
    (tmp_path / "specs" / "ck-x.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    (tmp_path / "out" / "ck-x").mkdir(parents=True)
    (tmp_path / "out" / "ck-x" / "music.json").write_text(json.dumps(
        {"file": "chill_wave.mp3", "credit": themes.music_credit("chill_wave.mp3")}), encoding="utf-8")
    monkeypatch.setattr(E, "SPECS", tmp_path / "specs")
    monkeypatch.setattr(E, "OUT", tmp_path / "out")
    b = E.bundle_for("ck-x", "2026-10-11 19:00")
    b.validate()
    assert (b.channel, b.engine, b.publish_at, b.voice) == ("CK", "casefile", "2026-10-11T12:00:00Z", spec.get("voice", "Ngọc Huyền"))
    assert "Kevin MacLeod" in b.description and "#TàiChínhCáNhân #BiểuĐồBiếtNói" in b.description
    assert "Nội dung giáo dục, không phải tư vấn đầu tư." in b.description
    assert all(u in b.description for u in spec["sources"])


def test_a_mim_spec_is_refused_by_the_ck_enqueue(monkeypatch, tmp_path):
    import enqueue_ck as E
    (tmp_path / "x.json").write_text(json.dumps({"theme": "mim", "title": "t"}), encoding="utf-8")
    monkeypatch.setattr(E, "SPECS", tmp_path)
    with pytest.raises(SystemExit):
        E.bundle_for("x", "2026-10-09 19:00")

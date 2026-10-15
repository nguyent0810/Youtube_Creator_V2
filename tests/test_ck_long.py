"""Kênh Biểu Đồ Biết Nói (CK) trên bộ dựng video dài: giọng "người hỏi" + theme chart. Kênh khác giữ nguyên."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "long"), str(ROOT / "motion"), str(ROOT / "motion" / "stier")]

import build_long as BL  # noqa: E402
import script_lines as SL  # noqa: E402


def topic(tmp_path, monkeypatch, spec):
    sd, od = tmp_path / "data", tmp_path / "out"
    sd.mkdir(exist_ok=True)
    (sd / "spec.json").write_text(json.dumps({"title": "t", "chapters": [], **spec}, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(BL, "paths", lambda t: (sd, od))
    return BL.load("x")[0]


def test_ck_routes_narrator_asker_and_quote_to_three_voices(tmp_path, monkeypatch):
    topic(tmp_path, monkeypatch, {"channel": "CK"})
    assert BL.THEME["name"] == "chart" and BL.CHAN["brand"] == "BIỂU ĐỒ BIẾT NÓI"
    assert BL.line_voice("Câu kể.") == "Ngọc Huyền"
    assert BL.line_voice({"t": "Vậy gửi tiết kiệm là thắng à?", "ask": 1}) == "Phạm Tuyên"
    assert BL.line_voice({"t": "Lời trích.", "q": 1}) == "Xuân Vĩnh"


def test_channels_without_an_asker_read_ask_lines_with_the_narrator(tmp_path, monkeypatch):
    topic(tmp_path, monkeypatch, {"channel": "MIM"})
    assert BL.line_voice({"t": "Hỏi?", "ask": 1}) == "Thanh Bình"   # giọng MIM từ 12/10/2026


def test_script_marks_viewer_questions():
    chs = SL.parse("## CH00 · Mở đầu\nCâu kể.\nHỎI: Vậy gửi tiết kiệm là thắng à?\n")
    assert chs[0]["lines"][1] == {"t": "Vậy gửi tiết kiệm là thắng à?", "ask": 1}


def test_a_track_can_be_shared_by_several_channels_but_never_leaks_to_others():
    import variety
    assert variety._chans({"channel": ["MIM", "CK"]}) == ("MIM", "CK")
    assert variety._chans({}) == ("CL",)


def test_sync_gives_every_on_screen_token_a_time_even_symbols():
    """beat.js tách chữ theo dấu cách: "→", "·" cũng là một ô chữ -> wt phải đủ số ô, không thì chữ cuối không hiện (C2)."""
    import beatfx
    words = [{"w": w, "t": t} for w, t in [("qua", 1.0), ("công", 1.2), ("ty", 1.4), ("chứng", 1.6), ("khoán,", 1.8)]]
    sc = [{"type": "kinetic", "t0": 0.5, "t1": 3.0, "items": [{"text": "→ CÔNG TY CHỨNG KHOÁN", "at": 1.2}]}]
    beatfx.apply_sync(sc, [{"words": words}])
    q = sc[0]["items"][0]
    assert q["fx"] == "sync" and q["wt"] == [1.2, 1.2, 1.4, 1.6, 1.8]
    assert beatfx._per_token("KHÔNG SỬA · KHÔNG HUỶ", [1, 2, 3, 4]) == [1, 2, 3, 3, 4]
    assert beatfx._per_token("ĐƯỜNG · CỘT ·", [1, 2]) == [1, 2, 2, 2]
    assert beatfx._per_token("HAI CHỮ", [1, 2]) == [1, 2]

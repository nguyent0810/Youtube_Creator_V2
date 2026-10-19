"""S-tier cho kênh MIM: giao diện + giọng + nhạc nền + Beat Text theo kênh.

Thiết kế (2 vòng Grok): docs/channels/mind-in-the-machine/2026-10-06-stier-design.md.
Đường kênh Hình Sự (theme "case") phải giữ NGUYÊN hành vi.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "stier"), str(ROOT / "motion")]

import beatfx  # noqa: E402
import themes  # noqa: E402


def scenes():
    return [{"type": "kinetic", "items": [{"text": "TRÍ TUỆ NHÂN TẠO", "at": 1.0},
                                          {"text": "KHÔNG BIẾT NGHĨ", "at": 1.6},
                                          {"text": "CHỈ ĐOÁN CHỮ", "at": 2.2},
                                          {"text": "1969", "at": 2.8},
                                          {"text": "ĐOÁN", "acc": True, "at": 3.1},
                                          {"text": "nhỏ", "sm": True, "at": 3.4}]},
            {"type": "slam", "text": "LO", "at": 4.0}]


# ── 1. Beat Text: kênh Hình Sự không đổi một byte ─────────────────────────

def test_default_pools_give_exactly_the_old_assignment():
    old = subprocess.run(["git", "show", "HEAD:motion/beatfx.py"], cwd=ROOT, capture_output=True,
                         text=True, encoding="utf-8").stdout
    ns = {}
    exec(compile(old, "beatfx_old", "exec"), ns)
    a, b = scenes(), scenes()
    ns["assign_beats"](a, "Ba cái đầu trên gối", boxed_max=12)
    beatfx.assign_beats(b, "Ba cái đầu trên gối", boxed_max=12)
    assert a == b


def test_mim_cycles_effects_line_by_line_and_never_types_a_big_line():
    sc = scenes()
    beatfx.assign_beats(sc, "mim-x", boxed_max=12, pools=themes.THEMES["mim"]["pools"])
    big = [q["fx"] for q in sc[0]["items"][:3]]
    assert len(set(big)) == 3                                   # mỗi dòng một kiểu, không dùng chung cả cảnh
    assert not {"type", "scramble"} & set(big)                  # type/scramble đổi font, nhảy tâm dòng
    assert sc[1]["fx"] != "glitch"                              # glitch rung #stage, đánh nhau với con dấu


def test_every_mim_effect_exists_in_the_engine_and_has_its_own_sound():
    js = (ROOT / "motion" / "hf" / "assets" / "engine" / "beat.js").read_text(encoding="utf-8")
    src = (ROOT / "motion" / "beatfx.py").read_text(encoding="utf-8")
    p = themes.THEMES["mim"]["pools"]
    for fx in set(p["N"] + p["A"] + p["S"] + p["D"]):
        assert f"{fx}:" in js or f'"{fx}"' in js, fx
        assert f'"{fx}"' in src.split("def beat_sfx")[1], fx    # không rơi vào nhánh "pop"
    for fx in p["X"]:
        assert fx == "punch" or f"{fx}:" in js, fx


# ── 2. Giọng đọc: cache theo giọng ────────────────────────────────────────

class Engine:
    def __init__(self):
        self.voices = []

    def infer(self, text, voice=None):
        import numpy as np
        self.voices.append(voice)
        return np.zeros(4800, dtype="float32")


def test_changing_the_voice_resynthesises_instead_of_reusing_the_old_wav(monkeypatch, tmp_path):
    import build
    eng = Engine()
    monkeypatch.setattr(build, "_engine", eng)
    build.speak(["Một câu."], tmp_path / "v.wav", tmp_path / "t.json", voice="Anh Khôi")
    build.speak(["Một câu."], tmp_path / "v.wav", tmp_path / "t.json", voice="Hải Đăng")
    build.speak(["Một câu."], tmp_path / "v.wav", tmp_path / "t.json", voice="Hải Đăng")
    assert eng.voices == ["Anh Khôi", "Hải Đăng"]


def test_an_old_timing_file_without_a_voice_still_counts_as_anh_khoi(monkeypatch, tmp_path):
    import build
    eng = Engine()
    monkeypatch.setattr(build, "_engine", eng)
    build.speak(["Một câu."], tmp_path / "v.wav", tmp_path / "t.json", voice="Anh Khôi")
    t = json.loads((tmp_path / "t.json").read_text(encoding="utf-8"))
    t.pop("voice")
    (tmp_path / "t.json").write_text(json.dumps(t), encoding="utf-8")
    build.speak(["Một câu."], tmp_path / "v.wav", tmp_path / "t.json", voice="Anh Khôi")
    assert eng.voices == ["Anh Khôi"]                         # cache CL cũ vẫn dùng được


# ── 3. Nhạc nền ───────────────────────────────────────────────────────────

def test_tracks_are_picked_least_recently_used_and_each_pick_is_written(tmp_path):
    led = tmp_path / "mim_music.json"
    pool = ["a.mp3", "b.mp3", "c.mp3"]
    got = [themes.pick_track("mim-1", pool, led), themes.pick_track("mim-2", pool, led),
           themes.pick_track("mim-3", pool, led), themes.pick_track("mim-4", pool, led)]
    assert got[:3] == ["a.mp3", "b.mp3", "c.mp3"] and got[3] == "a.mp3"
    assert themes.pick_track("mim-2", pool, led) == "b.mp3"     # dựng lại cùng video: cùng nhạc


def test_music_mix_ducks_under_the_voice_and_drops_in_question_scenes():
    fc = themes.music_filter(gain=0.16, quiet=[(10.0, 12.5)])
    assert "sidechaincompress=threshold=0.03:ratio=6:attack=40:release=600" in fc
    assert "volume=0.16" in fc
    assert "between(t,9.90,12.50)" in fc
    assert "loudnorm=I=-14" in fc


def test_case_theme_keeps_the_crime_channel_defaults():
    t = themes.THEMES["case"]
    assert (t["voice"], t["accent"], t["sound"]) == ("Anh Khôi", "#e2402d", "drone")
    assert t.get("pools") is None and t["js"] == {}


# ── 4. Vào kho cho upload tay ─────────────────────────────────────────────

def test_a_mim_bundle_carries_sources_the_music_credit_and_utc_time(monkeypatch, tmp_path):
    import enqueue_mim as E
    spec = json.loads((ROOT / "data" / "stier" / "specs" / "mim-youtube-20-nam.json").read_text(encoding="utf-8"))
    (tmp_path / "specs").mkdir()
    (tmp_path / "specs" / "mim-x.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    (tmp_path / "out" / "mim-x").mkdir(parents=True)
    (tmp_path / "out" / "mim-x" / "music.json").write_text(json.dumps(
        {"file": "bit_shift.mp3", "credit": themes.music_credit("bit_shift.mp3")}), encoding="utf-8")
    monkeypatch.setattr(E, "SPECS", tmp_path / "specs")
    monkeypatch.setattr(E, "OUT", tmp_path / "out")
    b = E.bundle_for("mim-x", "2026-10-09 07:00")
    b.validate()
    assert (b.channel, b.engine, b.publish_at) == ("MIM", "casefile", "2026-10-09T00:00:00Z")
    assert "Kevin MacLeod" in b.description and "CC" not in b.title
    assert all(u in b.description for u in spec["sources"])


def test_a_crime_spec_is_refused_by_the_mim_enqueue(monkeypatch, tmp_path):
    import enqueue_mim as E
    (tmp_path / "x.json").write_text(json.dumps({"title": "t"}), encoding="utf-8")
    monkeypatch.setattr(E, "SPECS", tmp_path)
    with pytest.raises(SystemExit):
        E.bundle_for("x", "2026-10-09 07:00")


# ── 5. Pexels key ─────────────────────────────────────────────────────────

def test_pexels_key_is_read_from_local_env_under_either_name(monkeypatch, tmp_path):
    sys.path.insert(0, str(ROOT / "motion" / "long"))
    import pexels
    monkeypatch.delenv("PEXELS_API_KEY", raising=False)
    f = tmp_path / ".local.env"
    f.write_text("OTHER=1\nPEXEL_KEY=abc123\n", encoding="utf-8")
    assert pexels.key((f,)) == "abc123"
    f.write_text("PEXELS_API_KEY = \"xyz\"\n", encoding="utf-8")
    assert pexels.key((f,)) == "xyz"
    with pytest.raises(SystemExit):
        pexels.key((tmp_path / "none.env",))


# ── 6. Beat Text v2: chữ to hiện theo giọng (sync) ────────────────────────

SPOKEN = [{"w": w, "t": t} for w, t in [("Hai", 10.0), ("mươi", 10.2), ("năm", 10.4), ("sau,", 10.6),
                                         ("YouTube", 11.0), ("là", 11.4), ("nơi", 11.6), ("bạn", 11.8),
                                         ("đang", 12.0), ("xem", 12.2), ("video", 12.4), ("này.", 12.6)]]


def test_sync_times_needs_every_word_spoken_in_order_inside_the_scene():
    st = beatfx.SyncCursor(SPOKEN, t0=10.0, t1=13.0)
    assert st.take("NĂM SAU", at=10.4) == [10.4, 10.6]
    assert st.take("BẠN ĐANG Ở ĐÂY", at=11.8) is None           # "ở đây" không được đọc -> không sync
    assert st.take("BẠN ĐANG XEM", at=11.8) == [11.8, 12.0, 12.2]
    assert st.take("NĂM", at=10.4) is None                       # chữ đã dùng không dùng lại


def test_sync_never_binds_a_word_from_the_previous_scene():
    st = beatfx.SyncCursor(SPOKEN, t0=11.0, t1=13.0)
    assert st.take("SAU YOUTUBE", at=11.1) is None               # "sau" ở 10.6 < t0


def test_mim_kinetic_lines_that_are_fully_spoken_become_sync_with_word_times():
    sc = [{"type": "kinetic", "t0": 10.0, "t1": 13.0,
           "items": [{"text": "20 NĂM SAU", "at": 10.0, "acc": True},
                     {"text": "BẠN ĐANG XEM", "at": 11.8},
                     {"text": "trên điện thoại", "at": 12.5, "sm": True}]}]
    beatfx.apply_sync(sc, [{"words": SPOKEN}])                    # trước assign_beats, như build.plan
    beatfx.assign_beats(sc, "k", pools=themes.THEMES["mim"]["pools"])
    a, b, c = sc[0]["items"]
    assert a["fx"] != "sync"                                    # "20" là số, lời đọc là "Hai mươi"
    assert b["fx"] == "sync" and b["wt"] == [11.8, 12.0, 12.2]
    assert b["t0"] == 10.0                                      # beat.js: chữ đầu đọc muộn -> hiện mờ trước (không "màn chết")
    assert c["fx"] != "sync"                                    # không được đọc


def test_sync_ticks_land_on_each_word_not_on_the_line_start():
    class M:
        def __init__(self):
            self.at = []

        def put(self, t, *a):
            self.at.append(round(t, 2))

        def tick(self, *a):
            return None
    m = M()
    beatfx.beat_sfx(m, {"fx": "sync", "at": 11.8, "wt": [11.8, 12.0, 12.2]})
    assert m.at == [11.78, 11.98, 12.18]


def test_the_opening_line_is_never_synced_so_frame_zero_has_text():
    # Khung 0 là hook + thumbnail: dòng mở đầu phải hiện ngay, không chờ chữ được đọc.
    sc = [{"type": "kinetic", "t0": 0.0, "t1": 3.0, "items": [{"text": "HAI MƯƠI", "at": 0.0}]}]
    beatfx.apply_sync(sc, [{"words": [{"w": "Hai", "t": 0.5}, {"w": "mươi", "t": 0.7}]}])
    assert "fx" not in sc[0]["items"][0]


def test_mim_never_turns_an_ordinary_line_into_a_terminal_command():
    # "type" ở MIM hiện dấu nhắc "> " -- chỉ dòng lệnh ghi rõ "fx":"type" trong spec.
    p = themes.THEMES["mim"]["pools"]
    assert "type" not in p["N"] + p["A"] + p["S"] + p["D"]

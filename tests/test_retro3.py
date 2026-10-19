"""Chốt bằng máy của retro 3 (10/10/2026) — docs/pm/2026-10-10-retro-3.md.

  mục 13  mốc cảnh trùng thẻ chương ("cảnh 0 (chapter) quá ngắn" ×3 trong một ngày)  -> build_long.chapter_collisions + lỗi rõ ở plan()
  mục 2   chuỗi gọi publish cho > 1 kênh (final_r4/r6 kẹt CK ~18 h sau lượt MIM)     -> run_chain.check từ chối
  mục 16  chuỗi đăng không gọi playlists.py sync                                       -> run_chain.check WARNING
  mục 7/14 qa_blank báo giả ở biểu đồ đang vẽ / thẻ có khung                           -> qa_blank --topic (classify/spans)
  mục 9   nhạc nền MIM trùng 64–70% (chọn "ít dùng nhất" từng ô)                        -> variety.optimise_picks
  mục 15  tràn chữ beat2 (D2, C4 lên kênh mang lỗi)                                    -> beatfx.overflow_lines
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "long"), str(ROOT / "motion"), str(ROOT / "motion" / "stier"), str(ROOT), str(ROOT / "scripts")]
import beatfx  # noqa: E402
import build_long as BL  # noqa: E402
import qa_blank as QB  # noqa: E402
import variety as V  # noqa: E402

_s = importlib.util.spec_from_file_location("run_chain_r3", ROOT / "scripts" / "run_chain.py")
RC = importlib.util.module_from_spec(_s)
_s.loader.exec_module(RC)


# ---------------- mục 13: cảnh trùng mốc thẻ chương ----------------
def _ch(at, line0="Ở Việt Nam từ ngày một tháng một luật có hiệu lực"):
    return {"lines": [line0, "Câu thứ hai."], "scenes": [{"type": "chapter", "title": "X", "titleAt": [0, "ở"]},
                                                          {"type": "kinetic", "at": at, "items": [{"text": "A"}]}]}


@pytest.mark.parametrize("at", [0, 0.0, 0.4, [0], [0, "ở"], [0, "Việt"], [0, None]])
def test_scene_anchored_on_chapter_card_is_flagged(at):
    bad = BL.chapter_collisions([("ch06", _ch(at))])
    assert len(bad) == 1 and "ch06 cảnh 1 (kinetic)" in bad[0] and "thẻ chương" in bad[0]
    with pytest.raises(SystemExit, match="ch06 cảnh 1"):
        BL.scene_gate([("ch06", _ch(at))])


@pytest.mark.parametrize("at", [1, 2.5, [0, "luật"], [0, "ở", 0, 0.8], [1, "câu"]])
def test_scene_anchored_later_passes(at):
    assert BL.chapter_collisions([("ch06", _ch(at))]) == []


def test_no_chapter_card_no_check():
    ch = _ch(0)
    ch["scenes"][0]["type"] = "kinetic"
    assert BL.chapter_collisions([("ch00", ch)]) == []


def test_every_current_topic_passes_the_lint():
    """Hiệu chỉnh: mọi topic đang có (đều đã dựng được) không bị báo giả."""
    bad = []
    for d in sorted((ROOT / "data" / "long").iterdir()):
        if (d / "spec.json").exists():
            spec = json.loads((d / "spec.json").read_text(encoding="utf-8"))
            chs = [(c, json.loads((d / f"{c}.json").read_text(encoding="utf-8"))) for c in spec.get("chapters", []) if (d / f"{c}.json").exists()]
            bad += BL.chapter_collisions(chs)
    assert bad == []


def test_plan_error_names_the_scene_that_collides():
    words = lambda txt, t0: [{"w": w, "t": t0 + 0.3 * k, "d": 0.25} for k, w in enumerate(txt.split())]
    lines = [{"text": "Một hai ba bốn.", "start": 0.0, "end": 1.5, "words": words("Một hai ba bốn.", 0.0)},
             {"text": "Năm sáu.", "start": 2.0, "end": 3.0, "words": words("Năm sáu.", 2.0)}]
    ch = {"scenes": [{"type": "chapter", "title": "X"}, {"type": "slam", "at": 0, "text": "A"}]}
    with pytest.raises(ValueError) as e:
        BL.plan(ch, lines, 5.0)
    msg = str(e.value)
    assert "quá ngắn" in msg and "cảnh 1 (slam) neo at=0" in msg and "thẻ chương" in msg


# ---------------- mục 2 + 16: run_chain một kênh mỗi chuỗi ----------------
MULTI = """#!/bin/bash
one() {
  T=$1; CH=$2; AT=$3
  python motion/long/publish_long.py $T $CH $AT --wait
}
one mim-ai-hallucinate MIM 2026-11-02T13:00:00Z
one ck-c3-bieu-do-nen CK 2026-11-14T13:00:00Z
"""


def test_chain_publishing_two_channels_is_refused():
    assert RC.publish_channels(MULTI) == {"MIM", "CK"}
    with pytest.raises(SystemExit, match="MỘT kênh mỗi chuỗi"):
        RC.check(MULTI)
    RC.check(MULTI, multi=True)        # cố ý: cho qua


def test_single_channel_chain_passes_and_comments_echo_do_not_count():
    sh = ("# MIM #6 -> CK D2 (chú thích nhắc kênh khác)\n"
          "python motion/long/publish_long.py ck-d2-fomo CK 2026-11-21T13:00:00Z --wait\n"
          "echo \"=== MIM xong\"\npython scripts/playlists.py sync --channel CK\n")
    assert RC.publish_channels(sh) == {"CK"}
    assert RC.check(sh) == []


def test_chain_without_publish_is_not_checked():
    assert RC.publish_channels("python motion/long/build_long.py mim-ai-gpu render  # MIM CK\nsleep 1\n") == set()


def test_publish_long_without_playlist_sync_warns():
    w = RC.check("python motion/long/publish_long.py ck-c4 CK 2026-11-28T13:00:00Z --wait\n")
    assert len(w) == 1 and "playlists.py sync" in w[0]


def test_run_refuses_before_snapshot_or_lock(tmp_path):
    sh, base = tmp_path / "multi.sh", tmp_path / "chains"
    sh.write_text(MULTI, encoding="utf-8", newline="\n")
    with pytest.raises(SystemExit, match="MỘT kênh"):
        RC.run(sh, None, base)
    assert not base.exists() or not list(base.glob("multi.*.sh"))


def _snap(name):
    snaps = sorted((ROOT / "output" / ".chains").glob(f"{name}.*.sh"))
    if not snaps:
        pytest.skip("không có bản chụp chuỗi")
    return snaps[-1].read_text(encoding="utf-8")


@pytest.mark.parametrize("name,ok", [("final_r4", False), ("final_r6", False), ("final_r7_d2", True), ("final_r7_gpu", True)])
def test_calibrated_on_real_chains_of_this_batch(name, ok):
    text = _snap(name)
    if ok:
        RC.check(text, unchecked=True)
    else:
        with pytest.raises(SystemExit, match="MỘT kênh"):
            RC.check(text, unchecked=True)


# ---------------- mục 13: bước dựng qua ống mà không kiểm mã thoát ----------------
def test_piped_html_without_exit_check_is_refused():
    sh = 'python motion/long/build_long.py $T html 2>&1 | grep -E "WARN" | tail -5\npython motion/long/build_long.py $T render\n'
    assert len(RC.swallowed_steps(sh)) == 1
    with pytest.raises(SystemExit, match="mã thoát"):
        RC.check(sh)
    assert RC.check(sh, unchecked=True) == []


@pytest.mark.parametrize("sh", [
    'python motion/long/build_long.py $T render 2>&1 | tail -12\n[ "${PIPESTATUS[0]}" = 0 ] || exit 1\n',
    'python motion/long/build_long.py $T html > /tmp/h.log 2>&1 || { tail -5 /tmp/h.log; return 1; }\n',
    'set -o pipefail\npython motion/long/build_long.py $T html 2>&1 | tail -5\n',
    'python motion/long/build_long.py $T final 2>&1 | tail -3\n[ -f final.mp4 ] || exit 1\n',
])
def test_checked_steps_pass(sh):
    assert RC.swallowed_steps(sh) == []


@pytest.mark.parametrize("name,bad", [("final_r4", 1), ("final_r9_gpu", 1), ("b1_final", 2), ("final_r10_m7", 0), ("final_r12_feed", 0)])
def test_pipe_check_calibrated_on_real_chains(name, bad):
    assert len(RC.swallowed_steps(_snap(name))) == bad      # r10 trở đi (mẫu đã sửa) qua; r4–r9 là đúng lỗi MIM #7 r8


def test_beat2_advice_for_new_channels_only():
    assert BL.beat2_advice({"channel": "MIM"}) and BL.beat2_advice({"channel": "CK", "beat2": False})
    assert BL.beat2_advice({"channel": "MIM", "beat2": True}) is None and BL.beat2_advice({}) is None


# ---------------- mục 7 + 14: qa_blank phân biệt biểu đồ đang vẽ ----------------
def test_classify_soft_only_inside_chart_or_card_and_short():
    sp = [(0.0, 12.0, "candles"), (20.0, 30.0, "quote"), (40.0, 60.0, "race")]
    runs = [(0.0, 3.2), (21.0, 24.0), (13.0, 15.0), (11.0, 13.5), (41.0, 47.0)]
    hard, soft = QB.classify(runs, sp)
    assert [(s, e) for s, e, _ in soft] == [(0.0, 3.2), (21.0, 24.0)]
    assert hard == [(13.0, 15.0), (11.0, 13.5), (41.0, 47.0)]      # ngoài cảnh / vắt qua mép / dài hơn SOFT_MAX: vẫn TRỐNG


def test_spans_offsets_chapters_in_spec_order(tmp_path):
    (tmp_path / "data" / "long" / "t").mkdir(parents=True)
    (tmp_path / "data" / "long" / "t" / "spec.json").write_text(json.dumps({"chapters": ["ch00", "ch01"]}), encoding="utf-8")
    for name, dur, sc in (("ch00", 10.0, [{"type": "chapter", "t0": 0, "t1": 4}, {"type": "ledger", "t0": 4, "t1": 10}]),
                          ("ch01", 8.0, [{"type": "kinetic", "t0": 0, "t1": 2}, {"type": "candles", "t0": 2, "t1": 8}])):
        d = tmp_path / "output" / "long" / "t" / name
        d.mkdir(parents=True)
        (d / "data.js").write_text("window.CASE = " + json.dumps({"dur": dur, "scenes": sc}) + ";\n", encoding="utf-8")
    assert QB.spans("t", tmp_path) == [(4, 10, "ledger"), (12.0, 18.0, "candles")]


def test_cli_last_line_backward_compatible(monkeypatch, capsys):
    monkeypatch.setattr(QB, "scan", lambda v, mn, fps: [(0.0, 3.0), (50.0, 52.0)])
    monkeypatch.setattr(sys, "argv", ["qa_blank.py", "x/final.mp4"])
    QB.main()
    assert capsys.readouterr().out.strip().splitlines()[-1] == "final.mp4: 2 đoạn trống ≥ 1.0s"
    monkeypatch.setattr(QB, "spans", lambda topic: [(0.0, 10.0, "candles")])
    monkeypatch.setattr(sys, "argv", ["qa_blank.py", "x/final.mp4", "--topic", "t"])
    QB.main()
    out = capsys.readouterr().out.strip().splitlines()
    assert "ĐANG HIỆN DẦN (chart candles)" in out[1] and out[0].startswith("TRỐNG 00:50")
    assert out[-1].startswith("final.mp4: 1 đoạn trống ≥ 1.0s")


# ---------------- mục 9: nhạc nền tối thiểu Jaccard ----------------
def _baseline(slots, fixed, prev):
    """Cách cũ: từng ô chọn bài ít dùng gần đây nhất (không nhìn cả bộ)."""
    uses, got, inv = {}, {}, set(fixed)
    for p in prev:
        for t in p:
            uses[t] = uses.get(t, 0) + 1
    for k, c in slots:
        got[k] = min(c, key=lambda t: (t in inv, uses.get(t, 0), t))
        inv.add(got[k])
    return got


def test_optimiser_minimises_max_jaccard_against_recent_videos():
    lib = [f"t{i:02d}" for i in range(14)]
    prev = [set(lib[0:5]), set(lib[3:8]), set(lib[6:11])]
    slots = [(f"ch0{i}.0", lib[(i * 3) % 14:(i * 3) % 14 + 6] or lib[:6]) for i in range(8)]
    got = V.optimise_picks(slots, set(), prev, salt="x")
    s = set(got.values())
    worst = max(V._jac(s, p) for p in prev)
    base = set(_baseline(slots, set(), prev).values())
    assert worst <= max(V._jac(base, p) for p in prev)
    assert len(s) == len(slots)                           # không lặp bài trong video khi đủ bài
    assert got == V.optimise_picks(slots, set(), prev, salt="x")      # tất định


def test_existing_bgm_picks_are_authoritative(tmp_path, monkeypatch):
    lib = tmp_path / "music"
    lib.mkdir()
    for n in ("a", "b", "c"):
        (lib / f"{n}.mp3").write_bytes(b"x")
    monkeypatch.setattr(V, "LIB", lib)
    monkeypatch.setattr(V, "catalog", lambda: {"tracks": {n: {"file": f"{n}.mp3", "mood": ["tense"], "channel": "MIM"} for n in "abc"}})
    monkeypatch.setattr(V, "recent", lambda ch, ex, n=3: [{"bgm": ["a"]}])
    pp = tmp_path / "bgm_picks.json"
    monkeypatch.setattr(V, "_picks_path", lambda topic: pp)
    pp.write_text(json.dumps({"ch00.0": "a.mp3"}), encoding="utf-8")       # chọn tay, dù "a" trùng video trước
    chs = [("ch00", {"bgm": {"mood": "tense"}}), ("ch01", {"bgm": {"mood": "tense"}})]
    V.resolve_bgm("t", {"channel": "MIM"}, chs, tmp_path / "od")
    assert chs[0][1]["bgm"]["file"] == "a.mp3"                              # giữ nguyên
    assert chs[1][1]["bgm"]["file"] in ("b.mp3", "c.mp3")                  # ô thiếu: chọn mới, khác "a"
    assert json.loads(pp.read_text(encoding="utf-8"))["ch00.0"] == "a.mp3"


def test_fully_picked_video_is_untouched(tmp_path, monkeypatch):
    lib = tmp_path / "music"
    lib.mkdir()
    (lib / "a.mp3").write_bytes(b"x")
    monkeypatch.setattr(V, "LIB", lib)
    monkeypatch.setattr(V, "catalog", lambda: pytest.fail("không được đọc danh mục khi mọi ô đã chọn"))
    monkeypatch.setattr(V, "recent", lambda ch, ex, n=3: [])
    pp = tmp_path / "bgm_picks.json"
    pp.write_text(json.dumps({"ch00.0": "a.mp3"}), encoding="utf-8")
    before = pp.read_bytes()
    monkeypatch.setattr(V, "_picks_path", lambda topic: pp)
    chs = [("ch00", {"bgm": {"mood": "tense"}})]
    V.resolve_bgm("t", {"channel": "MIM"}, chs, tmp_path / "od")
    assert chs[0][1]["bgm"]["file"] == "a.mp3" and pp.read_bytes() == before


# ---------------- mục 15: tràn chữ beat2 ----------------
def _line(text, fs, cls=None, left=None):
    st = {"top": "400px", "fontSize": f"{fs}px", **({"left": f"{left}px"} if left else {})}
    return {"type": "kinetic", "lay": "split", "t0": 0, "t1": 3, "items": [{"text": text, "at": 0.3, "L": {"cls": cls, "style": st}}]}


def test_overflow_flags_the_published_defect_sizes():
    # "KHÔNG THAY ĐỔI" với hệ số cũ 0,62: ô split 740 px -> 85 px; ô hero 1640 px -> 188 px. Cả hai tràn (MIM #7 09/10).
    assert beatfx.overflow_lines([_line("KHÔNG THAY ĐỔI", 85, "kL")], "ch01")
    assert beatfx.overflow_lines([{**_line("KHÔNG THAY ĐỔI", 188), "lay": "hero"}])
    assert not beatfx.overflow_lines([_line("KHÔNG THAY ĐỔI", 73, "kL")])      # K_CAPS 0,72 -> vừa


def test_overflow_ladder_box_shrinks_with_left():
    assert beatfx.overflow_lines([_line("MỘT DÒNG KHÁ DÀI Ở BẬC CUỐI", 104, "kC", left=650)])
    assert not beatfx.overflow_lines([_line("NGẮN", 104, "kC", left=650)])


def test_render_gate_refuses_certain_clipping(tmp_path, monkeypatch):
    """Tràn vượt cả mức co 40% của beat2.js -> late_report (render từ chối trừ --allow-late); tràn nhẹ chỉ WARNING ở html."""
    (tmp_path / "ch00").mkdir()
    sc = [_line("MỘT DÒNG RẤT RẤT DÀI KHÔNG THỂ NÀO VỪA NỔI Ô CHIA ĐÔI", 120, "kL"), _line("KHÔNG THAY ĐỔI", 85, "kR")]
    (tmp_path / "ch00" / "data.js").write_text("window.CASE = " + json.dumps({"dur": 9, "scenes": sc}) + ";\n", encoding="utf-8")
    monkeypatch.setattr(BL, "load", lambda topic: ({}, [("ch00", {})], tmp_path))
    monkeypatch.setitem(BL.BEAT2, "on", True)
    out = BL.late_report("t")
    assert len(out) == 1 and "CẮT MÉP" in out[0] and "RẤT RẤT" in out[0]


def test_chain_qa_blank_without_topic_warns():
    w = RC.check('B=$(python scripts/qa_blank.py $O/final.mp4 | tail -1)\n')
    assert any("--topic" in x for x in w)
    assert RC.check('B=$(python scripts/qa_blank.py $O/final.mp4 --topic $T | tail -1)\n') == []


@pytest.mark.parametrize("texts", [["KHÔNG THAY ĐỔI", "NHANH · MƯỢT"], ["ĐẮT HAY RẺ?", "→ LÀM GIỐNG HỌ"], ["ĐỘ DỐC MA200"],
                                   ["nhãn nhỏ", "MỘT CHIẾC CARD", "BA DÒNG"]])
def test_auto_layout_never_overflows(texts):
    for lay in ("hero", "split", "corner", "ladder", "frame"):
        r = {"type": "kinetic", "lay": lay, "t0": 0, "t1": 4, "items": [{"text": t, "at": 0.3 + k} for k, t in enumerate(texts)]}
        if lay == "split" and len(texts) != 2:
            continue
        beatfx.layout_items([r])
        assert beatfx.overflow_lines([r]) == [], (lay, texts)

"""Short 9:16 (motion/stier) bắt kịp video dài -- retro 2026-10-06 mục 8.

1. casefile.js: cảnh kinetic tôn trọng "sm": true (dòng phụ nhỏ, như casewide.js), dòng không "sm" giữ nguyên.
2. build.speak: bảng đọc "say" của spec chỉ đổi lời đưa vào TTS; phụ đề/mốc chữ giữ chữ gốc; cache giọng cũ
   (spec không "say") vẫn dùng được; thêm "say" chỉ đọc lại câu đổi cách đọc.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "stier"), str(ROOT / "motion")]
ENGINE = ROOT / "motion" / "hf" / "assets" / "engine"


# ── 1. kinetic "sm" trong engine Short ────────────────────────────────────

# DOM giả tối thiểu: chạy beat.js + casefile.js trong node vm, in class + cỡ chữ của mọi .kin
HARNESS = r"""
const fs = require("fs"), vm = require("vm");
const [beatP, engP, dataP] = process.argv.slice(2);
function mk(tag) {
  const e = { tag, className: "", style: {}, innerHTML: "", children: [] };
  e.style.setProperty = () => {};
  Object.assign(e, { appendChild: (c) => (e.children.push(c), c), insertBefore: (c) => (e.children.unshift(c), c),
    setAttribute: () => {}, querySelector: () => mk("q"), querySelectorAll: () => [],
    classList: { add: (c) => { e.className += " " + c; }, remove: () => {}, contains: () => false } });
  return e;
}
const sel = {};
const document = { documentElement: mk("html"), createElement: mk, createElementNS: (n, t) => mk(t),
  querySelector: (s) => (sel[s] = sel[s] || mk(s)), querySelectorAll: () => [], getElementById: (s) => mk(s) };
const tl = new Proxy({}, { get: () => () => tl });
const ctx = { document, gsap: { timeline: () => tl, set: () => {} }, getComputedStyle: () => ({ color: "#fff" }), console };
ctx.window = ctx; vm.createContext(ctx);
for (const p of [dataP, beatP, engP]) vm.runInContext(fs.readFileSync(p, "utf8"), ctx);
const out = [], walk = (e) => { if (/^kin\b/.test(e.className)) out.push({ cls: e.className, size: e.style.fontSize, text: e.innerHTML }); e.children.forEach(walk); };
walk(sel["#stage"]);
process.stdout.write(JSON.stringify(out));
"""


def _kin(tmp_path, items):
    if not shutil.which("node"):
        pytest.skip("không có node")
    case = {"slug": "t", "dur": 5.0, "seed": 7, "accent": "#e2402d", "kicker": "K", "sub": "", "acc": [],
            "lines": [{"text": "Một câu.", "start": 0.0, "end": 1.0, "words": [{"w": "Một", "t": 0.1, "d": 0.3},
                                                                               {"w": "câu.", "t": 0.5, "d": 0.4}]}],
            "imgs": {}, "geo": None, "theme": {},
            "scenes": [{"type": "kinetic", "t0": 0.0, "t1": 5.0, "items": items}]}
    (tmp_path / "data.js").write_text("window.CASE = " + json.dumps(case, ensure_ascii=False) + ";\n", encoding="utf-8")
    (tmp_path / "h.js").write_text(HARNESS, encoding="utf-8")
    r = subprocess.run(["node", str(tmp_path / "h.js"), str(ENGINE / "beat.js"), str(ENGINE / "casefile.js"),
                        str(tmp_path / "data.js")], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_kinetic_sm_item_gets_the_sm_class_and_a_small_cap(tmp_path):
    out = _kin(tmp_path, [{"text": "AI", "at": 0.5, "fx": "pop"},
                          {"text": "dòng phụ", "at": 1.0, "fx": "pop", "sm": True},
                          {"text": "NHẤN", "at": 1.5, "fx": "pop", "acc": True}])
    big, sm, acc = out
    assert big == {"cls": "kin", "size": "150px", "text": "AI"}          # không "sm": như cũ
    assert sm["cls"] == "kin sm" and sm["size"] == "64px"               # trần 64 (casewide: 56/130 -> dọc 150)
    assert acc["cls"] == "kin acc" and acc["size"] == "150px"


def test_kinetic_sm_explicit_size_still_wins_and_long_sm_lines_shrink(tmp_path):
    out = _kin(tmp_path, [{"text": "x", "at": 0.5, "fx": "pop", "sm": True, "size": 90},
                          {"text": "một dòng phụ rất rất dài cần thu nhỏ lại", "at": 1.0, "fx": "pop", "sm": True}])
    assert out[0]["size"] == "90px"
    assert int(out[1]["size"][:-2]) < 64


def test_sm_style_exists_and_accent_still_wins():
    css = (ENGINE / "casefile.css").read_text(encoding="utf-8")
    assert ".kin.sm {" in css and ".kin.sm.acc { color:var(--red); }" in css


# ── 2. bảng đọc "say" ─────────────────────────────────────────────────────

SAY = {"=ELIZA": "Ê-li-dơ", "seoul": "Xơ-un"}


def test_spoken_maps_case_insensitive_and_exact_keys_and_keeps_punctuation():
    import build
    assert build.spoken("ELIZA ở Seoul, rồi “SEOUL”.", SAY) == "Ê-li-dơ ở Xơ-un, rồi “Xơ-un”."
    assert build.spoken("Eliza ở đây.", SAY) == "Eliza ở đây."             # "=ELIZA" chỉ khớp đúng hoa/thường
    s = "Câu  không   đổi."                                                # không chữ nào khớp -> trả NGUYÊN câu
    assert build.spoken(s, SAY) is s and build.spoken(s, None) is s


class Engine:
    def __init__(self):
        self.calls = []

    def infer(self, text, voice=None):
        import numpy as np
        self.calls.append(text)
        return np.full(4800, 0.1, dtype="float32")


LINES = ["ELIZA ra đời năm 1966.", "Ở Seoul, người ta dùng nó.", "Hết."]


def test_say_changes_tts_input_but_not_captions_or_word_anchors(monkeypatch, tmp_path):
    import build
    eng = Engine()
    monkeypatch.setattr(build, "_engine", eng)
    t = build.speak(LINES, tmp_path / "v.wav", tmp_path / "t.json", voice="Hải Đăng", say=SAY)
    assert eng.calls == ["Ê-li-dơ ra đời năm 1966.", "Ở Xơ-un, người ta dùng nó.", "Hết."]
    assert [s["text"] for s in t["segments"]] == LINES                     # phụ đề: chữ gốc
    assert [s.get("say") for s in t["segments"]] == [eng.calls[0], eng.calls[1], None]
    ws = build.word_lines(t, tmp_path / "v.wav", SAY)
    assert [w["w"] for w in ws[0]["words"]] == LINES[0].split()            # karaoke/phụ đề dùng chữ gốc
    assert build.Anchors(ws)([1, "Seoul"]) >= ws[1]["start"]               # neo theo chữ gốc
    build.speak(LINES, tmp_path / "v.wav", tmp_path / "t.json", voice="Hải Đăng", say=SAY)
    assert len(eng.calls) == 3                                             # lần 2: cache


def test_say_weights_count_spoken_syllables():
    import build
    assert build._weight("ELIZA", SAY) == 3.0                              # Ê-li-dơ
    assert build._weight("Seoul,", SAY) == pytest.approx(2.6)              # Xơ-un + nghỉ dấu phẩy
    assert build._weight("COVID-19", SAY) == build.hf_align.token_weight("COVID-19")   # không trong bảng: như cũ


def test_without_say_the_old_cache_and_timing_file_stay_valid(monkeypatch, tmp_path):
    import build
    eng = Engine()
    monkeypatch.setattr(build, "_engine", eng)
    t = build.speak(LINES, tmp_path / "v.wav", tmp_path / "t.json", voice="Anh Khôi")
    assert eng.calls == LINES and not any("say" in s for s in t["segments"])
    # bảng không đụng câu nào / bảng rỗng -> vẫn trúng cache, không đọc lại
    build.speak(LINES, tmp_path / "v.wav", tmp_path / "t.json", voice="Anh Khôi", say={"tokyo": "Tô-ki-ô"})
    build.speak(LINES, tmp_path / "v.wav", tmp_path / "t.json", voice="Anh Khôi", say={})
    assert eng.calls == LINES


def test_adding_say_only_respeaks_the_lines_whose_spoken_text_changed(monkeypatch, tmp_path):
    import build
    import numpy as np
    import soundfile as sf
    eng = Engine()
    monkeypatch.setattr(build, "_engine", eng)
    t0 = build.speak(LINES, tmp_path / "v.wav", tmp_path / "t.json", voice="Anh Khôi")
    t1 = build.speak(LINES, tmp_path / "v.wav", tmp_path / "t.json", voice="Anh Khôi", say={"seoul": "Xơ-un"})
    assert eng.calls == LINES + ["Ở Xơ-un, người ta dùng nó."]
    assert t1["duration"] == t0["duration"]
    a, _ = sf.read(str(tmp_path / "v.wav"), dtype="float32")
    assert len(a) == 3 * 4800 and np.allclose(a, 0.1, atol=1e-3)            # câu 0 và 2 cắt lại từ wav cũ
    # đổi giọng thì không tái dùng câu nào
    build.speak(LINES, tmp_path / "v.wav", tmp_path / "t.json", voice="Hải Đăng", say={"seoul": "Xơ-un"})
    assert len(eng.calls) == 4 + 3

"""Khoá các lỗi pipeline motion/ tìm thấy trong audit 08/10/2026 (T13–T15, L16, L17).

Không test nào gọi mạng hay render: mọi lời gọi ra ngoài đều bị thay bằng bản giả.
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HF = ROOT / "motion" / "hf"
VENDOR_GSAP = HF / "assets" / "vendor" / "gsap.min.js"
sys.path.insert(0, str(ROOT / "motion" / "long"))


# ─── T15: GSAP lấy từ repo, không tải CDN lúc render ──────────────────────

def _pages():
    yield from HF.glob("*.html")
    yield from (HF / "compositions").glob("*.html")
    yield from (ROOT / "motion" / "long" / "thumbs").glob("*.html")
    yield ROOT / "motion" / "long" / "build_long.py"       # mẫu HTML của video dài
    yield ROOT / "motion" / "stier" / "build.py"           # mẫu HTML của S-tier


def test_no_page_loads_gsap_from_a_cdn():
    bad = [p.name for p in _pages() if "cdn.jsdelivr.net/npm/gsap" in p.read_text(encoding="utf-8")]
    assert bad == []


def test_every_gsap_reference_points_at_the_vendored_file():
    for p in _pages():
        for src in re.findall(r'src="([^"]*gsap[^"]*)"', p.read_text(encoding="utf-8")):
            # trang trong compositions/ nạp tương đối theo chính nó; mẫu render và thumbnail nạp từ gốc motion/hf
            base = p.parent if src.startswith("../") else HF
            assert (base / src).resolve() == VENDOR_GSAP.resolve(), (p.name, src)


def test_vendored_gsap_matches_the_recorded_hash():
    readme = (VENDOR_GSAP.parent / "README.md").read_text(encoding="utf-8")
    assert hashlib.sha256(VENDOR_GSAP.read_bytes()).hexdigest() in readme
    assert VENDOR_GSAP.read_text(encoding="utf-8").lstrip().startswith("/*!\n * GSAP 3.14.2")


# ─── T14: thời điểm âm không được dời cả timeline ─────────────────────────

CLAMP_PROBE = r"""
const { gsap } = require(process.argv[2]);
const tl = gsap.timeline({ paused: true });
%s
const zoom = { s: 1 }, cap = { o: 0 };
// Đúng thứ tự engine: phụ đề được thêm TRƯỚC, phần tử âm thêm SAU (casewide.js: tl.set("#caps", ..., s.t0 - 0.01)
// ở cuối file). Lần thêm kế tiếp GSAP mới xử lý phần tử âm và dời MỌI thứ đã có, kể cả phụ đề.
tl.set(cap, { o: 1 }, 1.0);                                                                           // phụ đề phải hiện ở 1,00 s
tl.fromTo(zoom, { s: 1 }, { s: 1.1, duration: 5, ease: "none", immediateRender: false }, 0 - 0.15);  // s.t0 - 0.15 với t0 = 0
tl.set(zoom, { s: 1 }, 6.0);
tl.duration(); tl.seek(0.999); const a = cap.o; tl.seek(1.001);
console.log(JSON.stringify([a, cap.o]));
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="cần node để chạy GSAP thật")
@pytest.mark.parametrize("engine", ["casewide.js", "casefile.js"])
def test_negative_positions_do_not_shift_the_timeline(engine, tmp_path):
    src = (HF / "assets" / "engine" / engine).read_text(encoding="utf-8")
    m = re.search(r"\n(  for \(const \[m, i\] of .*?\n  \})\n", src, re.S)
    assert m, f"{engine}: thiếu đoạn kẹp vị trí >= 0 ngay sau gsap.timeline()"
    assert src.index(m.group(1)) < src.index("tl.to(") and src.index(m.group(1)) < src.index("tl.set(")
    probe, lib = tmp_path / "probe.cjs", tmp_path / "gsap.cjs"   # motion/hf là package "type": "module" -> nạp bản sao CommonJS
    shutil.copyfile(VENDOR_GSAP, lib)
    probe.write_text(CLAMP_PROBE % m.group(1), encoding="utf-8")
    out = subprocess.run(["node", str(probe), str(lib)], capture_output=True, text=True, check=True).stdout
    assert json.loads(out) == [0, 1]     # chưa hiện ở 0,999 s, đã hiện ở 1,001 s (không kẹp: dời tới 1,15 s)


def test_late_first_kinetic_line_is_moved_where_sfx_can_see_it():
    """casewide.js kéo dòng đầu lên t0+0.5 nhưng sfx_long.py vẫn đặt tiếng ở mốc cũ."""
    pytest.importorskip("scipy")
    pytest.importorskip("soundfile")
    import build_long
    words = [{"w": w, "t": 0.5 + 0.4 * k, "d": 0.3} for k, w in enumerate("một hai ba bốn năm sáu bảy tám chín mười".split())]
    lines = [{"text": " ".join(x["w"] for x in words), "start": 0.5, "end": 4.5, "words": words}]

    def items(first_at):
        ch = {"title": "Thử", "scenes": [{"type": "kinetic", "at": 0, "items": [
            {"text": "Dòng một", "at": first_at}, {"text": "Dòng hai", "at": 3.4}]}]}
        return [q["at"] for q in build_long.plan(ch, lines, 6.0)[0]["items"]]

    assert items(3.0) == [0.5, 3.4]      # đến muộn > 2 s -> dời ngay trong dữ liệu (data.js + sfx dùng chung)
    assert items(1.0) == [1.0, 3.4]      # đến sớm -> giữ nguyên


# ─── C6: nhãn biên tập không được đọc thành tiếng ─────────────────────────

def test_plain_dien_y_label_is_stripped_and_marked():
    import script_lines
    md = "## CH01 · Thử\nCâu mở.\nMột nhà sử học nhận xét: ai cũng có thể bị buộc tội. [DIỄN Ý]\n**[DIỄN Ý]** Câu in đậm.\n"
    lines = script_lines.parse(md)[0]["lines"]
    assert all("DIỄN" not in (x if isinstance(x, str) else x["t"]) for x in lines)
    assert [x.get("diy") for x in lines if isinstance(x, dict) and "diy" in x] == [1, 1]


def test_unknown_editorial_markup_stops_the_build():
    import script_lines
    with pytest.raises(SystemExit, match="dòng 3"):
        script_lines.parse("## CH01 · Thử\nCâu mở.\nCâu có [CẦN KIỂM] nhãn lạ.\n")


def test_chapter_lines_match_their_script():
    """chNN.json phải là đúng script.md đã duyệt (ripper ch12 từng giữ nhãn [DIỄN Ý] trong câu đọc)."""
    import script_lines
    for sd in sorted((ROOT / "data" / "long").glob("*/")):
        if not (sd / "script.md").exists():
            continue
        for c in script_lines.parse((sd / "script.md").read_text(encoding="utf-8")):
            have = json.loads((sd / f"{c['name']}.json").read_text(encoding="utf-8"))["lines"]
            assert have == c["lines"], f"{sd.name}/{c['name']}: chạy lại motion/long/script_lines.py {sd.name}"


# ─── L16: ảnh cache theo khoá phải đúng file spec yêu cầu ──────────────────

def _no_network(monkeypatch, module):
    calls = []

    def boom(*a, **k):
        calls.append(a)
        raise OSError("không được gọi mạng")
    monkeypatch.setattr(module.urllib.request, "urlopen", boom)
    monkeypatch.setattr(module.time, "sleep", lambda s: None)
    return calls


def test_long_video_refetches_when_spec_changes_the_image(monkeypatch, tmp_path):
    pytest.importorskip("scipy")
    pytest.importorskip("soundfile")
    import build_long
    dst = tmp_path / "ripper1.jpg"
    dst.write_bytes(b"anh cu")
    dst.with_suffix(".json").write_text(json.dumps({"file": "File:Old.jpg", "license": "CC BY 4.0", "artist": "A"}))
    calls = _no_network(monkeypatch, build_long)
    with pytest.raises(OSError):
        build_long.fetch_img("File:New.jpg", dst, {})
    assert calls and not dst.exists()          # không dùng ảnh cũ (người khác, ghi công sai)


def test_long_video_external_image_mismatch_is_loud(tmp_path):
    pytest.importorskip("scipy")
    pytest.importorskip("soundfile")
    import build_long
    dst = tmp_path / "k.jpg"
    dst.write_bytes(b"x")
    dst.with_suffix(".json").write_text(json.dumps({"file": "EXT:wellcome:A", "license": "CC0", "artist": ""}))
    with pytest.raises(SystemExit, match="media_search"):
        build_long.fetch_img("EXT:wellcome:B", dst, {})


def test_stier_image_cache_records_and_checks_its_source(monkeypatch, tmp_path):
    pytest.importorskip("scipy")
    pytest.importorskip("soundfile")
    sys.path.insert(0, str(ROOT / "motion" / "stier"))
    import build as stier_build
    dst = tmp_path / "a.jpg"
    dst.write_bytes(b"anh cu khong ro nguon")
    calls = _no_network(monkeypatch, stier_build)
    with pytest.raises(OSError):
        stier_build.fetch_img("File:New.jpg", dst)
    assert calls and not dst.exists()


def test_final_refuses_chapters_whose_render_is_stale(monkeypatch, tmp_path):
    """`html` dựng lại tiếng (mix.wav) nhưng không render hình: ghép lại là lệch hình-tiếng."""
    pytest.importorskip("scipy")
    pytest.importorskip("soundfile")
    import build_long
    for n in ("ch00", "ch01"):
        (tmp_path / n).mkdir()
    (tmp_path / "ch00" / "silent.key").write_text("MOI")
    (tmp_path / "ch01" / "silent.key").write_text("CU")
    monkeypatch.setattr(build_long, "load", lambda topic: ({}, [("ch00", {}), ("ch01", {})], tmp_path))
    monkeypatch.setattr(build_long, "render_key", lambda topic, name, od, draft: "MOI")
    with pytest.raises(SystemExit, match="ch01"):
        build_long.do_final("t")


# ─── T13: mô tả video dài theo giới hạn YouTube ───────────────────────────

def _describe_topic(root: Path, summary: str, img_file="File:A.jpg", cached_file="File:A.jpg"):
    sd, od = root / "data" / "long" / "t", root / "output" / "long" / "t"
    (od / "ch00").mkdir(parents=True)
    (od / "img").mkdir()
    sd.mkdir(parents=True)
    (sd / "spec.json").write_text(json.dumps({"chapters": ["ch00"], "imgs": {"a": img_file},
                                              "youtube": {"summary": summary, "hashtags": ["x"]}}), encoding="utf-8")
    (sd / "ch00.json").write_text(json.dumps({"hud": {"t": "mở"}, "scenes": [{"img": "a"}]}), encoding="utf-8")
    (od / "ch00" / "timing.json").write_text(json.dumps({"duration": 12.0}))
    (od / "img" / "a.json").write_text(json.dumps({"file": cached_file, "license": "Public domain", "artist": ""}))


def test_description_over_5000_bytes_stops_before_upload(monkeypatch, tmp_path):
    import describe
    _describe_topic(tmp_path, "ệ" * 1700)              # 1.700 ký tự nhưng 5.100 byte
    monkeypatch.setattr(describe, "ROOT", tmp_path)
    with pytest.raises(SystemExit, match="byte"):
        describe.main("t")


def test_description_with_angle_brackets_is_refused(monkeypatch, tmp_path):
    import describe
    _describe_topic(tmp_path, "Lãi > 30%/tháng")
    monkeypatch.setattr(describe, "ROOT", tmp_path)
    with pytest.raises(SystemExit, match="<"):
        describe.main("t")


def test_credit_for_a_stale_cached_image_is_refused(monkeypatch, tmp_path):
    import describe
    _describe_topic(tmp_path, "Tóm tắt.", img_file="File:New.jpg", cached_file="File:Old.jpg")
    monkeypatch.setattr(describe, "ROOT", tmp_path)
    with pytest.raises(SystemExit, match="cache"):
        describe.main("t")


def test_normal_description_passes(monkeypatch, tmp_path, capsys):
    import describe
    _describe_topic(tmp_path, "Tóm tắt ngắn.")
    monkeypatch.setattr(describe, "ROOT", tmp_path)
    describe.main("t")
    assert "OK:" in capsys.readouterr().out


# ─── L17 + T13: tải tư liệu ───────────────────────────────────────────────

def test_europeana_key_never_reaches_the_screen(monkeypatch):
    requests = pytest.importorskip("requests")
    import media_search

    def fail(*a, **k):
        raise requests.HTTPError("403 Client Error: Forbidden for url: "
                                 "https://api.europeana.eu/record/v2/search.json?wskey=BI-MAT-123&query=x")
    monkeypatch.setattr(media_search.requests, "get", fail)
    monkeypatch.setattr(media_search.time, "sleep", lambda s: None)
    with pytest.raises(RuntimeError) as e:
        media_search.s_europeana("x")
    assert "BI-MAT-123" not in str(e.value) and "wskey=***" in str(e.value)


def test_rate_limited_search_is_an_error_not_none(monkeypatch):
    pytest.importorskip("requests")
    import media_search

    class R:
        status_code = 429
    monkeypatch.setattr(media_search.requests, "get", lambda *a, **k: R())
    monkeypatch.setattr(media_search.time, "sleep", lambda s: None)
    with pytest.raises(RuntimeError, match="429"):
        media_search.jget("https://example.invalid/x")


class _Stream:
    def __init__(self, chunks, fail_after=None):
        self.chunks, self.fail_after, self.kwargs = chunks, fail_after, None

    def __call__(self, method, url, **kwargs):
        self.kwargs = kwargs
        return self

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def raise_for_status(self):
        pass

    def iter_bytes(self):
        for k, c in enumerate(self.chunks):
            if self.fail_after is not None and k == self.fail_after:
                raise OSError("đứt mạng")
            yield c


def _pexels(monkeypatch, tmp_path, stream):
    import pexels
    monkeypatch.setattr(pexels, "ROOT", tmp_path)
    monkeypatch.setattr(pexels.httpx, "stream", stream)
    (pexels.out("t") / "index.json").write_text(json.dumps({"7": {"dur": 9, "slug": "s", "files": [
        {"w": 1920, "h": 1080, "link": "https://videos.pexels.com/x"}]}}))
    return pexels, pexels.out("t") / "7.mp4"


def test_pexels_download_follows_redirects(monkeypatch, tmp_path):
    stream = _Stream([b"ab", b"cd"])
    pexels, dst = _pexels(monkeypatch, tmp_path, stream)
    pexels.get("t", ["7"])
    assert stream.kwargs.get("follow_redirects") is True and "allow_redirects" not in stream.kwargs
    assert dst.read_bytes() == b"abcd" and not list(dst.parent.glob("*.part"))


def test_interrupted_pexels_download_leaves_no_fake_finished_file(monkeypatch, tmp_path):
    pexels, dst = _pexels(monkeypatch, tmp_path, _Stream([b"ab", b"cd"], fail_after=1))
    with pytest.raises(OSError):
        pexels.get("t", ["7"])
    assert not dst.exists()            # bản cũ: .mp4 cụt, lần sau tưởng đã tải xong


# ─── Đăng video dài: tham số ──────────────────────────────────────────────

def test_publish_long_playlist_and_add_to_are_parsed_apart():
    import publish_long
    got = publish_long.parse_args(["golden", "cl", "2026-10-17T12:00:00Z", "--playlist", "Tên", "mô tả", "id1", "id2",
                                   "--add-to", "PLX"])
    assert got == ("golden", "CL", "2026-10-17T12:00:00Z", ("Tên", "mô tả", ["id1", "id2"]), ["PLX"])

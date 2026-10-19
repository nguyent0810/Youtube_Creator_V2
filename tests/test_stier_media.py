"""Clip nền + ảnh có ghi công cho Short S-tier (kênh MIM, 06/10/2026).

Clip: Pexels / Coverr -> cắt sẵn 1080x1920, 30 fps, không tiếng (Chrome giải mã nhẹ) -> thẻ <video>
nướng tĩnh vào HTML như video dài (HyperFrames chỉ đếm media khai báo tĩnh).
Ảnh: Commons nhận thêm CC BY (KHÔNG BY-SA) cho theme cho phép; NASA; mọi ảnh/clip có dòng ghi công.
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "stier"), str(ROOT / "motion")]

import clips  # noqa: E402


def test_clip_refs_name_a_provider_and_an_id():
    assert clips.parse("pexels:12345") == ("pexels", "12345")
    assert clips.parse("coverr:AbC-9") == ("coverr", "AbC-9")
    with pytest.raises(ValueError):
        clips.parse("youtube:xyz")
    with pytest.raises(ValueError):
        clips.parse("pexels:../../x")


def test_transcode_crops_to_portrait_without_audio():
    cmd = clips.transcode_cmd("ffmpeg", Path("in.mp4"), Path("out.mp4"), seconds=14)
    s = " ".join(cmd)
    assert "crop=1080:1920" in s and "force_original_aspect_ratio=increase" in s
    assert "-an" in cmd and "-t" in cmd and "14" in cmd


def test_video_tags_start_a_little_before_the_scene_and_cover_it():
    tags, sc = clips.video_tags([{"type": "kinetic", "t0": 2.0, "t1": 5.0, "clip": "pexels:1", "ms": 1.5},
                                 {"type": "slam", "t0": 5.0, "t1": 6.0}],
                                {"pexels:1": {"src": "assets/clips/pexels-1.mp4", "dur": 12.0}}, dur=8.0)
    assert len(tags) == 1 and sc[0]["vid"] == "v0" and "vid" not in sc[1]
    t = tags[0]
    assert 'data-start="1.800"' in t and 'data-media-start="1.50"' in t and 'src="assets/clips/pexels-1.mp4"' in t
    assert 'data-duration="3.500"' in t and "muted" in t


def test_a_clip_too_short_for_its_scene_is_refused():
    with pytest.raises(SystemExit):
        clips.video_tags([{"type": "kinetic", "t0": 0.0, "t1": 9.0, "clip": "coverr:a", "ms": 2}],
                         {"coverr:a": {"src": "assets/clips/coverr-a.mp4", "dur": 8.0}}, dur=10.0)


def test_commons_license_gate_by_theme():
    import build
    assert build.license_ok("Public domain", "pd")
    assert build.license_ok("CC0", "pd")
    assert not build.license_ok("CC BY 4.0", "pd")                 # kênh Hình Sự: như cũ
    assert build.license_ok("CC BY 4.0", "by")
    assert build.license_ok("CC BY 2.0", "by")
    assert not build.license_ok("CC BY-SA 4.0", "by")              # share-alike: ghi công trong mô tả là không đủ
    assert not build.license_ok("CC BY-NC 2.0", "by")


def test_credit_lines_cover_every_image_and_clip(tmp_path):
    (tmp_path / "credits.json").write_text(json.dumps([
        {"kind": "image", "text": "Ảnh: Arpanet map — Eric Fischer, CC BY 2.0, via Wikimedia Commons"},
        {"kind": "clip", "text": "Video: Pexels — Jane Doe"},
        {"kind": "clip", "text": "Video: Pexels — Jane Doe"}]), encoding="utf-8")
    import enqueue_mim as E
    lines = E.credit_lines(tmp_path)
    assert lines == ["Ảnh: Arpanet map — Eric Fischer, CC BY 2.0, via Wikimedia Commons", "Video: Pexels — Jane Doe"]


def test_ffprobe_is_looked_up_next_to_the_ffmpeg_we_were_given(tmp_path):
    # Review: máy sản xuất chỉ có ffmpeg/ffprobe trong thư mục vendor, không có trong PATH.
    assert clips.ffprobe_for(str(tmp_path / "vendor" / "ffmpeg")) == str(tmp_path / "vendor" / "ffprobe")


def test_a_failed_transcode_never_leaves_a_file_that_looks_finished(monkeypatch, tmp_path):
    monkeypatch.setattr(clips, "CLIPS", tmp_path)
    src, dst = tmp_path / "s.mp4", tmp_path / "d.mp4"
    src.write_bytes(b"x")

    def broken(cmd, **kw):
        Path(cmd[-1]).write_bytes(b"half")                       # ffmpeg ghi dở rồi chết
        return type("P", (), {"returncode": 1, "stderr": "boom"})()
    monkeypatch.setattr(clips.subprocess, "run", broken)
    with pytest.raises(SystemExit):
        clips.transcode("ffmpeg", src, dst)
    assert not dst.exists()


def test_commons_artist_html_entities_are_decoded():
    import build
    assert build._plain("Tom &amp; Jerry &#039;s <a href='x'>lab</a>") == "Tom & Jerry 's lab"


def test_smithsonian_key_goes_in_a_header_not_the_url(monkeypatch):
    sys.path.insert(0, str(ROOT / "motion" / "long"))
    import media_search as M
    seen = {}
    monkeypatch.setattr(M, "si_key", lambda: "SECRET")
    monkeypatch.setattr(M, "jget", lambda url, headers=None, **kw: seen.update(headers=headers, params=kw.get("params")) or {})
    M.s_smithsonian("ipod")
    assert "SECRET" not in str(seen["params"]) and seen["headers"]["X-Api-Key"] == "SECRET"


def test_enqueue_never_truncates_away_the_music_credit(monkeypatch, tmp_path):
    import enqueue_mim as E
    spec = json.loads((ROOT / "data" / "stier" / "specs" / "mim-youtube-20-nam.json").read_text(encoding="utf-8"))
    spec["description"] = "x" * 4990
    (tmp_path / "specs").mkdir()
    (tmp_path / "specs" / "mim-x.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    (tmp_path / "out" / "mim-x").mkdir(parents=True)
    (tmp_path / "out" / "mim-x" / "music.json").write_text(json.dumps({"file": "a.mp3", "credit": "Music: A by Kevin MacLeod"}), encoding="utf-8")
    monkeypatch.setattr(E, "SPECS", tmp_path / "specs")
    monkeypatch.setattr(E, "OUT", tmp_path / "out")
    from factory.bundle import BundleInvalid
    with pytest.raises(BundleInvalid):
        E.bundle_for("mim-x", "2026-10-09 07:00").validate()

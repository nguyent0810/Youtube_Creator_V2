"""Video dài 16:9 cho kênh MIM (Grok vòng 1, 06/10/2026): một bảng kênh trong build_long.load(), kênh Hình Sự
(spec không ghi "channel") giữ NGUYÊN hành vi. Thiết kế: docs/channels/mind-in-the-machine/2026-10-06-long-design.md.
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "long"), str(ROOT / "motion"), str(ROOT / "motion" / "stier")]

import beatfx  # noqa: E402
import build_long as BL  # noqa: E402
import variety  # noqa: E402


def topic(tmp_path, monkeypatch, spec):
    sd, od = tmp_path / "data", tmp_path / "out"
    sd.mkdir(exist_ok=True)
    (sd / "spec.json").write_text(json.dumps({"title": "t", "chapters": [], **spec}, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(BL, "paths", lambda t: (sd, od))
    return BL.load("x")[0]


def test_crime_channel_keeps_its_voices_theme_and_no_brand(tmp_path, monkeypatch):
    topic(tmp_path, monkeypatch, {"theme": "noir"})
    assert (BL.VOICE, BL.QUOTE_VOICE, BL.THEME["name"]) == ("Anh Khôi", "Minh Đức", "noir")
    assert BL.CHAN.get("brand") is None and BL.CHAN.get("pools") is None


def test_mim_channel_gets_its_voice_lab_theme_brand_and_pools(tmp_path, monkeypatch):
    topic(tmp_path, monkeypatch, {"channel": "MIM"})
    assert (BL.VOICE, BL.QUOTE_VOICE, BL.THEME["name"]) == ("Thanh Bình", "Ngọc Huyền", "lab")
    assert BL.CHAN["brand"] == "MIND IN THE MACHINE" and BL.CHAN["pools"]["sync"]
    topic(tmp_path, monkeypatch, {})                       # nạp lại spec CL: không dính trạng thái MIM
    assert BL.VOICE == "Anh Khôi" and BL.THEME["name"] == ""


def test_mim_refuses_share_alike_images(tmp_path, monkeypatch):
    topic(tmp_path, monkeypatch, {"channel": "MIM"})
    assert BL.license_allowed("CC BY 2.0") and BL.license_allowed("Public domain")
    assert not BL.license_allowed("CC BY-SA 4.0")
    topic(tmp_path, monkeypatch, {})
    assert BL.license_allowed("CC BY-SA 4.0")                 # kênh Hình Sự: như cũ


def test_sync_covers_kin_overlays_and_respects_a_min_time():
    words = [{"w": "Mùa", "t": 0.1}, {"w": "hè", "t": 0.3}, {"w": "năm", "t": 0.5}]
    sc = [{"type": "photo", "t0": 0.0, "t1": 2.0, "kin": [{"text": "MÙA HÈ", "at": 0.1}]}]
    beatfx.apply_sync(sc, [{"words": words}], min_at=0.0)
    assert sc[0]["kin"][0]["fx"] == "sync"
    sc = [{"type": "photo", "t0": 0.0, "t1": 2.0, "kin": [{"text": "MÙA HÈ", "at": 0.1}]}]
    beatfx.apply_sync(sc, [{"words": words}])                  # mặc định: khung 0 phải có chữ
    assert "fx" not in sc[0]["kin"][0]


def test_bgm_picker_never_crosses_channels(tmp_path, monkeypatch):
    lib = tmp_path / "music"
    lib.mkdir()
    for f in ("dark.mp3", "lab.mp3"):
        (lib / f).write_bytes(b"x")
    monkeypatch.setattr(variety, "LIB", lib)
    monkeypatch.setattr(variety, "catalog", lambda: {"tracks": {
        "dark": {"file": "dark.mp3", "mood": ["epic"]},
        "lab": {"file": "lab.mp3", "mood": ["epic"], "channel": "MIM"}}})
    monkeypatch.setattr(variety, "_picks_path", lambda t: tmp_path / f"{t}.json")
    monkeypatch.setattr(variety, "recent", lambda *a, **k: [])
    for ch, want in (("MIM", "lab.mp3"), ("CL", "dark.mp3")):
        chs = [("ch00", {"bgm": {"mood": "epic"}})]
        variety.resolve_bgm(f"t-{ch}", {"channel": ch} if ch == "MIM" else {}, chs, tmp_path / ch)
        assert chs[0][1]["bgm"]["file"] == want


def test_lab_theme_is_exempt_from_the_look_rule(monkeypatch):
    monkeypatch.setattr(variety, "profile", lambda t: {"topic": t, "channel": "MIM", "theme": "lab", "look": "classic", "bgm": []})
    monkeypatch.setattr(variety, "recent", lambda *a, **k: [{"topic": "p", "look": "classic", "bgm": ["z"]}])
    assert variety.audit("x") == []


def test_mim_long_slugs_are_exportable_for_manual_upload():
    from factory import channels
    assert "long-" in channels.prefixes("MIM")
    assert "long-" not in channels.prefixes("CL")             # CL: publish_batch không bao giờ đụng video dài


def test_long_bundle_uses_the_channel_voice(tmp_path):
    import publish_long as PL
    sd, od = tmp_path / "d", tmp_path / "o"
    sd.mkdir()
    od.mkdir()
    (sd / "spec.json").write_text(json.dumps({"title": "AI đã chết hai lần", "chapters": [], "channel": "MIM",
                                              "youtube": {"tags": ["ai"]}}, ensure_ascii=False), encoding="utf-8")
    (od / "description.txt").write_text("mô tả", encoding="utf-8")
    assert PL.long_bundle("mim-ai-70", "MIM", "2026-10-25T12:00:00Z", sd, od).voice == "Thanh Bình"


def test_mim_description_links_cc_by_licence():
    import describe
    assert describe._lic_url("CC BY 2.0") == "https://creativecommons.org/licenses/by/2.0/"
    assert describe._lic_url("Public domain") == ""

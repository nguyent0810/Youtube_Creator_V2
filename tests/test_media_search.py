"""Nguồn tư liệu ngoài Commons (motion/long/media_search.py) -- sửa Openverse, Art Institute of Chicago;
thêm NASA, Smithsonian Open Access (06/10/2026, docs/channels/mind-in-the-machine/2026-10-06-media-sources.md).

Không gọi mạng: jget / requests.get được thay bằng dữ liệu mẫu đúng định dạng API thật.
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "motion" / "long"))
import media_search as M  # noqa: E402


def test_openverse_asks_for_at_most_20_results(monkeypatch):
    # Phiên ẩn danh của Openverse trả 401 khi page_size > 20 (v1 đã gặp) -> nguồn này đang chết.
    seen = {}
    monkeypatch.setattr(M, "jget", lambda url, **kw: seen.update(kw["params"]) or {"results": []})
    M.s_openverse("arpanet")
    assert seen["page_size"] <= 20


def test_openverse_download_rechecks_the_license_and_refuses_if_it_changed(monkeypatch, tmp_path):
    monkeypatch.setattr(M, "ROOT", tmp_path)
    od = tmp_path / "output" / "long" / "t"
    od.mkdir(parents=True)
    (od / "ext.json").write_text('[{"x": "X0", "src": "openverse:flickr", "id": "abc", "full": "http://f", '
                                 '"license": "CC BY 2.0", "artist": "a", "title": "t", "page": "p"}]', encoding="utf-8")
    monkeypatch.setattr(M, "jget", lambda url, **kw: {"license": "by-nc", "license_version": "2.0"})
    with pytest.raises(SystemExit):
        M.cmd_get("t", "k", "X0")


def test_artic_sends_its_required_header_and_asks_for_the_843px_iiif_size(monkeypatch):
    seen = {}

    def fake(url, **kw):
        seen["headers"] = kw.get("headers") or {}
        return {"data": [{"id": 1, "title": "Phật", "image_id": "IMG", "is_public_domain": True, "artist_display": "x",
                          "thumbnail": {"width": 2000, "height": 1500}}]}
    monkeypatch.setattr(M, "jget", fake)
    got = M.s_artic("buddha")
    assert "AIC-User-Agent" in seen["headers"]
    assert got[0]["full"].endswith("/full/843,/0/default.jpg")          # 1686 -> 403 (v1 đã gặp)


def test_nasa_needs_no_key_and_labels_everything_public_domain_with_the_center(monkeypatch):
    monkeypatch.setattr(M, "jget", lambda url, **kw: {"collection": {"items": [
        {"href": "https://images-assets.nasa.gov/image/iss050e031340/collection.json",
         "data": [{"nasa_id": "iss050e031340", "title": "J-SSOD-6 Deployment", "center": "JSC",
                   "photographer": "Peggy Whitson", "media_type": "image"}],
         "links": [{"href": "https://images-assets.nasa.gov/image/iss050e031340/iss050e031340~medium.jpg"}]}]}})
    got = M.s_nasa("gps satellite")
    assert got[0]["license"] == "Public domain (NASA)"
    assert got[0]["artist"] == "NASA/JSC — Peggy Whitson"
    assert got[0]["full"].endswith("~large.jpg")


def test_smithsonian_keeps_only_cc0_media_and_needs_a_key(monkeypatch):
    monkeypatch.setattr(M, "si_key", lambda: "K")
    monkeypatch.setattr(M, "jget", lambda url, **kw: {"response": {"rows": [{"id": "r1", "title": "Apple iPod", "content": {
        "freetext": {"name": [{"content": "Apple Computer, Inc."}]},
        "descriptiveNonRepeating": {"record_link": "https://www.si.edu/object/x", "online_media": {"media": [
            {"idsId": "A1", "content": "https://ids.si.edu/ids/deliveryService?id=A1", "thumbnail": "https://ids.si.edu/t/A1",
             "usage": {"access": "CC0"}},
            {"idsId": "A2", "content": "https://ids.si.edu/ids/deliveryService?id=A2", "thumbnail": "https://ids.si.edu/t/A2",
             "usage": {"access": "Usage conditions apply"}}]}}}}]}})
    got = M.s_smithsonian("ipod")
    assert [c["id"] for c in got] == ["A1"] and got[0]["license"] == "CC0"


def test_smithsonian_without_a_key_says_how_to_get_one(monkeypatch, tmp_path):
    monkeypatch.delenv("SI_API_KEY", raising=False)
    monkeypatch.delenv("DATA_GOV_API_KEY", raising=False)
    monkeypatch.setattr(M, "KEY_FILES", (tmp_path / "none.env",))
    with pytest.raises(SystemExit, match="api.data.gov"):
        M.si_key()

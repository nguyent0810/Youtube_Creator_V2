import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import long_gate as LG  # noqa: E402


def test_portrait_without_focus_is_a_blocking_error(tmp_path, monkeypatch):
    Image = pytest.importorskip("PIL.Image")
    topic = "mim-focus"
    data = tmp_path / "data" / "long" / topic
    out = tmp_path / "output" / "long" / topic / "img"
    data.mkdir(parents=True)
    out.mkdir(parents=True)
    (data / "spec.json").write_text(json.dumps({"chapters": ["ch00"]}), encoding="utf-8")
    (data / "ch00.json").write_text(json.dumps({"hud": {"t": "T"}, "lines": [], "scenes": [
        {"type": "photo", "img": "portrait"}, {"type": "map"}, {"type": "ledger"},
        {"type": "counter"}, {"type": "kinetic"}
    ]}), encoding="utf-8")
    Image.new("RGB", (100, 200)).save(out / "portrait.jpg")
    monkeypatch.setattr(LG, "ROOT", tmp_path)
    err, warn, _ = LG.gate(topic, min_syl=0)
    assert any("ảnh dọc 'portrait'" in x for x in err)
    assert not any("ảnh dọc 'portrait'" in x for x in warn)

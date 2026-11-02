import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "long"), str(ROOT / "motion"), str(ROOT / "motion" / "stier"), str(ROOT)]
import build_long as BL  # noqa: E402
import clip_sheet as CS  # noqa: E402
import img_sheet as IS  # noqa: E402


class Mark:
    def __init__(self, value=""):
        self.value = value

    def exists(self):
        return bool(self.value)

    def read_text(self, encoding="utf-8"):
        return self.value


def _gate(monkeypatch, images, clips, image_mark="", clip_mark=""):
    monkeypatch.setattr(BL, "paths", lambda topic: (Path("data"), Path("out")))
    monkeypatch.setattr(IS, "image_uses", lambda data: images)
    monkeypatch.setattr(CS, "clip_uses", lambda data: clips)
    monkeypatch.setattr(IS, "ok_path", lambda out: Mark(image_mark))
    monkeypatch.setattr(CS, "ok_path", lambda out: Mark(clip_mark))


def test_gate_blocks_missing_and_accepts_matching_marks(monkeypatch):
    images = [{"key": "hero", "focus": [0.5, 0.2]}]
    clips = [{"id": "12", "ms": 3.0}]
    _gate(monkeypatch, images, clips)
    with pytest.raises(SystemExit, match="img_sheet.py demo"):
        BL._refuse_unreviewed_sheets("demo")
    _gate(monkeypatch, images, clips, IS.uses_hash(images), CS.uses_hash(clips))
    BL._refuse_unreviewed_sheets("demo")


def test_gate_rejects_old_focus_or_clip_mark(monkeypatch):
    images = [{"key": "hero", "focus": [0.5, 0.2]}]
    clips = [{"id": "12", "ms": 3.0}]
    _gate(monkeypatch, [{"key": "hero", "focus": [0.7, 0.2]}], clips, IS.uses_hash(images), CS.uses_hash(clips))
    with pytest.raises(SystemExit, match="ảnh: dấu đã cũ"):
        BL._refuse_unreviewed_sheets("demo")
    _gate(monkeypatch, images, [{"id": "12", "ms": 4.0}], IS.uses_hash(images), CS.uses_hash(clips))
    with pytest.raises(SystemExit, match="clip: dấu đã cũ"):
        BL._refuse_unreviewed_sheets("demo")


@pytest.mark.parametrize("fn", ["do_render", "do_final"])
def test_render_and_final_enter_the_sheet_gate_first(monkeypatch, fn):
    monkeypatch.setattr(BL.branch_gate, "refuse", lambda root: None)
    monkeypatch.setattr(BL, "_refuse_unreviewed_sheets", lambda topic: (_ for _ in ()).throw(SystemExit("blocked")))
    with pytest.raises(SystemExit, match="blocked"):
        getattr(BL, fn)("demo")


def test_real_render_checks_branch_but_draft_does_not(monkeypatch):
    monkeypatch.setattr(BL.branch_gate, "refuse", lambda root: (_ for _ in ()).throw(SystemExit("branch")))
    with pytest.raises(SystemExit, match="branch"):
        BL.do_render("demo")
    monkeypatch.setattr(BL, "_refuse_unreviewed_sheets", lambda topic: (_ for _ in ()).throw(SystemExit("sheets")))
    with pytest.raises(SystemExit, match="sheets"):
        BL.do_render("demo", draft=True)

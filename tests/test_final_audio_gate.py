from types import SimpleNamespace
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "long"), str(ROOT / "motion"), str(ROOT / "motion" / "stier")]
import audio_lint as AL  # noqa: E402
import build_long as BL  # noqa: E402


def _prepare_final(monkeypatch, tmp_path, channel="MIM", final_errors=()):
    od = tmp_path / "out"
    (od / "ch00").mkdir(parents=True)
    monkeypatch.setattr(BL.branch_gate, "refuse", lambda root: None)
    monkeypatch.setattr(BL, "_refuse_unreviewed_sheets", lambda topic: None)
    monkeypatch.setattr(BL, "_refuse_floor", lambda topic, chs: None)
    monkeypatch.setattr(BL, "_refuse_craft", lambda topic, spec, chs: None)
    monkeypatch.setattr(BL, "load", lambda topic: ({"channel": channel, "master": True}, [("ch00", {})], od))
    monkeypatch.setattr(BL, "probe_dur", lambda p: 60.0)
    monkeypatch.setattr(BL, "_write_final_commit", lambda out: None)
    monkeypatch.setattr(AL, "check_parts", lambda parts, sfx: [])
    monkeypatch.setattr(AL, "check_final", lambda p, ff: (list(final_errors), {"tp": -1.5, "lufs": -14.0}))

    def fake_run(cmd, **kwargs):
        if str(cmd[0]).endswith("python.exe") or Path(str(cmd[1])).name == "srt.py":
            (od / "captions.vi.srt").write_text("srt", encoding="utf-8")
        else:
            Path(cmd[-1]).write_bytes(b"final" if str(cmd[-1]).endswith("final.mp4") else b"mix")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(BL, "run", fake_run)
    return od


def test_mim_voice_buzz_warns_but_technical_checks_still_block(monkeypatch, tmp_path):
    _prepare_final(monkeypatch, tmp_path)
    monkeypatch.setattr(AL, "check_voices", lambda *args: (["buzz"], ["voice warning"], {}))
    reports = []
    monkeypatch.setattr(AL, "report", lambda tag, err, warn, block: reports.append((err, warn, block)))
    BL.do_final("demo")
    assert reports == [([], [], True), (["buzz"], ["voice warning"], False), ([], [], True)]


def test_true_peak_failure_deletes_final_for_every_channel(monkeypatch, tmp_path):
    od = _prepare_final(monkeypatch, tmp_path, channel="CK", final_errors=["true peak"])
    monkeypatch.setattr(AL, "check_voices", lambda *args: ([], [], {}))
    with pytest.raises(SystemExit, match="audio_lint chặn"):
        BL.do_final("demo")
    assert not (od / "final.mp4").exists()

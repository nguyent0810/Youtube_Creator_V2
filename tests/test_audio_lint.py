"""23/10/2026: CL "sẹt sẹt" (docs/pm/2026-10-22-cl-am-thanh-set-set.md) -- khoá các chỗ sửa để không tái phát."""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "motion" / "stier"))
sys.path.append(str(ROOT / "motion" / "long"))
import sfx  # noqa: E402
import themes  # noqa: E402
import audio_lint as AL  # noqa: E402


def test_put_cut_at_start_fades_in_no_click():
    M = sfx.Mix(1.0, 1)
    M.put(-0.35, np.ones(int(0.8 * sfx.SR)), 0.5)     # whoosh thẻ chương ở T0 - 0.35 với T0 = 0
    assert abs(M.bed[0, 0]) < 1e-9 and AL.n_jumps(M.bed) == 0
    assert abs(M.bed[sfx.FADE_CUT + 10, 0] - 0.5) < 1e-9   # sau 5 ms: mức cũ


def test_put_cut_at_end_fades_out():
    M = sfx.Mix(1.0, 1)
    M.put(0.9, np.ones(sfx.SR), 0.5)
    assert abs(M.bed[-1, 0]) < 1e-9


def test_soft_clip_keeps_level_below_knee_and_never_hits_ceiling():
    x = np.array([0.1, -0.5, 0.79, 1.4, -3.0])
    y = sfx.soft_clip(x, 0.8, 1.0)
    assert np.array_equal(y[:3], x[:3])
    assert np.all(np.abs(y) <= 1.0) and abs(y[3]) > 0.8 and y[4] < -0.8


def test_jump_detector_flags_step_not_ramp():
    a = np.zeros(48000); a[10000:10100] = 0.2
    b = np.zeros(48000); b[10000:10240] = np.linspace(0, 0.5, 240); b[10240:11000] = 0.5
    assert AL.n_jumps(a) == 1 and AL.n_jumps(b) == 0


def test_cl_voice_fx_only_on_case_theme():
    assert themes.THEMES["case"]["voice_fx"] == themes.VOICE_FX_CL
    assert "equalizer=f=3200" not in themes.VOICE_FX_CL and "highshelf=f=5000:g=-5" in themes.VOICE_FX_CL
    assert "attack=15" in themes.VOICE_FX_CL and "lowpass=f=9000" in themes.VOICE_FX_CL
    assert all("voice_fx" not in t for k, t in themes.THEMES.items() if k != "case")

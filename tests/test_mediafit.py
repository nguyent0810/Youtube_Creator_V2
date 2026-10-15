"""motion/mediafit.py: quyết định phủ kín / đặt trọn hình theo tỉ lệ nguồn so với ô."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "motion"))
import mediafit  # noqa: E402


def test_same_ratio_no_loss():
    assert mediafit.crop_loss(1080, 1920, 1080, 1920) == 0
    assert mediafit.decide(2160, 3840, 1080, 1920) == "cover"


def test_landscape_into_short_is_not_cropped():
    assert mediafit.crop_loss(1920, 1080, 1080, 1920) > 0.6
    assert mediafit.decide(1920, 1080, 1080, 1920) == "blur"


def test_portrait_into_long_is_not_cropped():
    assert mediafit.decide(1080, 1920, 1920, 1080) == "blur"


def test_landscape_into_window_slots():
    assert mediafit.decide(1920, 1080, 968, 795) == "cover"     # cửa sổ "top": mất ~31%
    assert mediafit.decide(1920, 1080, 1080, 600) == "cover"    # dải ngang
    assert mediafit.decide(1080, 1920, 1080, 600) == "blur"     # clip dọc vào dải ngang


def test_vf_pads_window_onto_canvas():
    g = mediafit.vf("cover", 968, 795, canvas=(1080, 1920), pos=(56, 215))
    assert "pad=1080:1920:56:215" in g and "crop=968:794" in g
    assert "overlay" in mediafit.vf("blur", 1080, 1920)

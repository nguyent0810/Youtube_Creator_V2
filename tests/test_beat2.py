"""beat2 (PM 09/10/2026): bố cục cảnh chữ không lặp, "stack" có trần, từ nhấn, giới hạn sync, đo chữ chép nguyên lời đọc."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "motion"))

import beatfx  # noqa: E402


def _kin(texts, t0=0.0):
    return {"type": "kinetic", "t0": t0, "t1": t0 + 3, "items": [{"text": t, "at": t0 + 0.5 + k} for k, t in enumerate(texts)]}


def test_layouts_no_repeat_and_stack_cap():
    sc = [_kin(["NHÃN NHỎ", f"MỘT DÒNG CHỮ KHÁ DÀI SỐ {i}"], i * 4.0) for i in range(30)]
    for r in sc:
        r["items"][0]["sm"] = True
    beatfx.assign_layouts(sc, "lab|test")
    lays = [r["lay"] for r in sc]
    assert all(a != b for a, b in zip(lays, lays[1:]))
    assert lays.count("stack") <= beatfx.STACK_MAX * len(sc)
    assert len(set(lays)) >= 4


def test_layout_fits_content():
    sc = [_kin(["MỘT CHIẾC CARD CHƠI GAME DÀI DÀI DÀI DÀI DÀI DÀI DÀI", "VÀ MỘT DÒNG KHÁC CŨNG RẤT DÀI DÀI DÀI DÀI DÀI DÀI"])]
    beatfx.assign_layouts(sc, "k")
    assert sc[0]["lay"] not in ("split", "hero", "frame")


def test_preset_layout_kept():
    sc = [_kin(["A", "B"])]
    sc[0]["lay"] = "corner"
    beatfx.assign_layouts(sc, "k")
    assert sc[0]["lay"] == "corner"


def test_pick_em_prefers_numbers():
    sc = [_kin(["HAI CHIẾC CARD 512 LÕI"]), _kin(["VẼ MỘT KHUNG HÌNH"]), _kin(["NGẮN QUÁ"])]
    beatfx.pick_em(sc)
    assert sc[0]["items"][0]["em"] == "512"
    assert sc[1]["items"][0]["em"] == "KHUNG"
    assert "em" not in sc[2]["items"][0]


def test_sync_every_third_scene():
    words = []
    sc = []
    for i in range(6):
        t0 = i * 4.0
        sc.append(_kin(["CHÍN MƯƠI NGÀY"], t0))
        words += [{"w": w, "t": t0 + 0.6 + 0.2 * k} for k, w in enumerate(["chín", "mươi", "ngày"])]
    beatfx.apply_sync(sc, [{"words": words}], every=3)
    synced = [i for i, r in enumerate(sc) if r["items"][0].get("fx") == "sync"]
    assert synced == [0, 3]


def test_sync_skipped_when_first_word_late():
    sc = [_kin(["CHÍN MƯƠI NGÀY"], 0.0)]
    words = [{"w": w, "t": 2.0 + 0.2 * k} for k, w in enumerate(["chín", "mươi", "ngày"])]
    beatfx.apply_sync(sc, [{"words": words}], max_lead=1.2)
    assert sc[0]["items"][0].get("fx") != "sync"
    beatfx.apply_sync(sc, [{"words": words}])          # không giới hạn (video cũ): vẫn sync
    assert sc[0]["items"][0].get("fx") == "sync"


def test_light_start_flags_small_only_opening():
    r = _kin(["chưa ai nhắc tới", "TRÍ TUỆ NHÂN TẠO?"], 0.0)
    r["items"][0].update(sm=True, at=0.3)
    r["items"][1]["at"] = 1.9
    assert beatfx.light_start([r], "ch01")
    r["items"][1]["at"] = 0.6
    assert not beatfx.light_start([r], "ch01")


def test_pull_main_fixes_light_start():
    r = _kin(["chưa ai nhắc tới", "TRÍ TUỆ NHÂN TẠO?"], 0.0)
    r["items"][0].update(sm=True, at=0.3)
    r["items"][1].update(at=1.9, fx="sync", wt=[1.9, 2.0, 2.1, 2.2], t0=0.0)
    beatfx.pull_main([r])
    assert not beatfx.light_start([r])
    assert r["items"][1]["fx"] != "sync" and "wt" not in r["items"][1]


def test_layout_blocks_stay_above_captions():
    """Mọi bố cục beat2: đáy dòng cuối (top + cỡ chữ) <= 860 px (vùng phụ đề bắt đầu ~880)."""
    for texts in (["MÈO", "NẤM", "XE CỨU HOẢ"], ["MỘT VIỆC ĐƠN GIẢN", "THÁI HÀNH", "chú thích dưới"], ["A", "B"]):
        for lay in ("hero", "corner", "ladder", "frame"):
            r = _kin(texts)
            r["lay"] = lay
            beatfx.layout_items([r])
            for q in r["items"]:
                if q.get("L"):
                    top, fs = float(q["L"]["style"]["top"][:-2]), float(q["L"]["style"]["fontSize"][:-2])
                    assert top + fs <= 860, (lay, texts, q["text"], top, fs)


def test_hero_rejects_four_lines():
    main = [{"text": "MÈO"}, {"text": "NẤM"}, {"text": "XE"}, {"text": "VE"}]
    assert not beatfx._fits("hero", main, main)


def test_verbatim_share():
    lines = [{"words": [{"w": w, "t": k} for k, w in enumerate("hai chiếc card trong phòng ngủ".split())]}]
    sc = [_kin(["HAI CHIẾC CARD"]), _kin(["MỘT NÚI PHÉP NHÂN"])]
    assert beatfx.verbatim_share(sc, lines) == (1, 2)

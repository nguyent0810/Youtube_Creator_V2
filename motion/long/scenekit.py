"""Bộ đồ nghề viết cảnh tay cho data/long/<topic>/gen_scenes.py (rút từ golden/kowloon, dùng chung).

    from scenekit import sc, kin, chapter, write, FILMV
    CH = {"ch00": dict(hud={...}, bgm={"mood": "tense", "gain": .13}, scenes=[sc("date", None, ...), ...]), ...}
    write(__file__, CH, IMGS, GEO)

Cảnh vẫn do người viết: mỗi câu gắn với ảnh, bản đồ, hồ sơ, biểu đồ, sketch hoặc b-roll.
IMGS ghi thẳng tên "File:… .jpg" trên Commons (hoặc "EXT:<nguồn>:<id>"), KHÔNG ghi số thứ tự trong
research.json: chạy lại research thì số đổi, tên thì không.
"""
import json
from pathlib import Path

FILMV = "VIDEO MINH HỌA"


def sc(t, at=None, **k):
    d = {"type": t}
    if at is not None:
        d["at"] = at
    d.update(k)
    if t == "photo" and d.get("kin"):   # chữ đè lên ảnh: phủ tối tối thiểu để đọc được
        d["veil"] = max(d.get("veil", 0), 0.52)
    return d


def kin(*items):
    """("CHỮ", mốc, *cờ) — cờ: "acc" (màu nhấn), "sm" (nhỏ), "serif"."""
    out = []
    for it in items:
        text, at, *rest = it
        e = {"text": text, "at": at}
        for r in rest:
            e[r] = True
        out.append(e)
    return out


def chapter(no, k, title, sub, word, **bg):
    return sc("chapter", None, no=no, k=k, title=title, sub=sub, titleAt=[0, word], **bg)


def write(gen_file, CH: dict, IMGS: dict, GEO: dict, **spec_extra) -> None:
    """Ghi imgs/geo vào spec.json và hud/bgm/scenes vào từng chNN.json (giữ nguyên "lines")."""
    D = Path(gen_file).resolve().parent
    spec = json.loads((D / "spec.json").read_text(encoding="utf-8"))
    spec["imgs"], spec["geo"] = IMGS, GEO
    spec.update(spec_extra)
    (D / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, v in CH.items():
        f = D / f"{name}.json"
        d = json.loads(f.read_text(encoding="utf-8"))
        d.pop("marks", None)
        d.update(v)
        for x in d["scenes"]:
            if x["type"] == "file" and x.get("stamp"):   # con dấu trên thẻ giấy: mực (multiply), nằm trong thẻ
                x["stamp"].setdefault("ink", True)
                if not x.get("img"):   # thẻ không ảnh nằm ở x 450–1485: dấu dài thì lùi sang trái cho vừa thẻ (lint_html kiểm lại)
                    x["stamp"].setdefault("x", max(520, 1350 - 62 * len(x["stamp"]["text"])))
                    x["stamp"].setdefault("y", 550)
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(name, len(d["lines"]), "câu", len(d["scenes"]), "cảnh")

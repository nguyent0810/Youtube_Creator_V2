"""Phần chung cho module dòng nội dung của các kênh mới (CL, BUD).

Mỗi module kênh khai: CHANNEL, PILLARS {dòng: (tiền tố, "HH:MM", cảm giác)},
STYLE {dòng: (giọng, nhạc)}, TAGS, BROLL {dòng: [từ khoá]}, FICTION {dòng},
TEMPLATES {dòng: hàm(history, day) -> Draft|None}. Phần còn lại ở đây.
"""
from __future__ import annotations

import json
from pathlib import Path

from factory.lines import packs
from factory.pillars.check import verdict


def load_history(bundle_dir: Path, channel: str) -> list[dict]:
    out = []
    d = bundle_dir / channel
    if not d.exists():
        return out
    for f in sorted(d.glob("*.json")):
        b = json.loads(f.read_text(encoding="utf-8"))
        note = b.get("source_note", "")
        if note.startswith("pillar="):
            meta = dict(kv.split("=", 1) for kv in note.split(" | ")[0].split(";"))
            out.append({"pillar": meta["pillar"], "key": meta["key"], "angle": meta.get("angle", ""),
                        "script": b["script"], "publish_at": b["publish_at"]})
    return sorted(out, key=lambda h: h["publish_at"])


def make_next_draft(mod):
    """Tạo hàm next_draft(dòng, lịch sử, ngày) cho một module kênh."""

    def next_draft(pillar, history, day=None):
        done = {h["key"] for h in history if h["pillar"] == pillar}
        fiction = pillar in mod.FICTION
        if pillar in mod.TEMPLATES:
            d = mod.TEMPLATES[pillar](history, day)
            if d is not None and d.key not in done and verdict(check_draft(mod, d, history)):
                return d, []
            return None, [f"{mod.CHANNEL}/{pillar}: khuôn không cho bài hợp lệ ngày {day}"]
        from factory.lines import novelty
        for e in packs.load(mod.CHANNEL, pillar):
            if e["key"] in done:
                continue
            # Trùng chủ đề với video BẤT KỲ trên kênh (kể cả nguồn khác) -> bỏ.
            if novelty.duplicate_on_channel(mod.CHANNEL, e["title"]):
                continue
            d = packs.to_draft(e, pillar, mod.BROLL[pillar])
            d.cite_ke = e.get("cite_ke")
            if verdict(packs.check(d, history, fiction=fiction, cite_ke=e.get("cite_ke"))):
                return d, []
        return None, [f"{mod.CHANNEL}/{pillar}: hết gói kịch bản hợp lệ — cần viết thêm "
                      f"(data/packs/{mod.CHANNEL}/{pillar}.json)"]

    return next_draft


def check_draft(mod, d, history):
    return packs.check(d, history, fiction=d.pillar in mod.FICTION, cite_ke=getattr(d, "cite_ke", None))

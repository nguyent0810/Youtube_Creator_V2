"""Tiếng động cho video dài 16:9 — tổng hợp thủ tục, bám CÙNG mốc với casewide.js.

Khác Short: không có nền trầm tự tổng hợp (nhạc nền thật lo không khí, mix trong build_long.mix_chapter);
ở đây chỉ còn các "điểm chạm" — màn trập khi ảnh hiện, thud khi chữ đập, tick khi dòng hồ sơ hiện,
boom ở thẻ chương và cú slam. Tiết chế: video 30+ phút mà cảnh nào cũng đập thì tai mỏi -> gain thấp hơn Short.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "stier"))
from sfx import Mix, SR  # noqa: E402


def build(case: dict, dst: Path) -> None:
    dur = case["dur"]
    M = Mix(dur, case.get("seed", 1995))
    for i, s in enumerate(case["scenes"]):
        T0, T1, ty = s["t0"], s["t1"], s["type"]
        if i > 0 and ty not in ("question", "broll", "chapter"):
            M.put(T0 - 0.3, M.whoosh(0.45), 0.16, 0.3 if i % 2 else -0.3)
        for q in s.get("kin") or []:
            M.put(q["at"] - 0.02, M.thud(0.35), 0.3)
        if isinstance(s.get("label"), dict):
            M.put(s["label"]["at"], M.tick(2600, 0.04), 0.35)
        if s.get("stamp"):
            M.put(s["stamp"]["at"] + 0.16, M.thud(0.6), 0.8)
            M.put(s["stamp"]["at"] + 0.16, M.boom(1.2, 70, 40), 0.4)
        if ty == "chapter":
            M.put(T0 - 0.35, M.whoosh(0.8), 0.45)
            M.put(T0 + 0.05, M.boom(2.4, 52, 30), 0.9)
            M.put(s.get("titleAt", T0 + 0.35) - 0.02, M.thud(0.5), 0.5)
        elif ty in ("photo", "evidence"):
            M.put(T0, M.shutter(), 0.35)
            M.put(T0 + 0.02, M.boom(1.2, 50, 32), 0.25)
            for c in s.get("circles") or []:
                M.put(c["at"], M.scratch(0.22), 0.45)
            for c in s.get("callouts") or []:
                M.put(c["at"], M.tick(3000, 0.04), 0.5)
        elif ty == "print":
            M.put(T0 - 0.1, M.whoosh(0.4), 0.3, -0.2)
            M.put(T0 + 0.35, M.thud(0.35), 0.35)
            for q in (s.get("side") or {}).get("lines") or []:
                M.put(q["at"], M.tick(2400, 0.035), 0.3)
            for c in s.get("circles") or []:
                M.put(c["at"], M.scratch(0.22), 0.45)
        elif ty == "file":
            M.put(T0 - 0.1, M.whoosh(0.5), 0.3, -0.2)
            for r in s.get("rows") or []:
                for k in range(2):
                    M.put(r["at"] + k * 0.06, M.key(), 0.3)
        elif ty == "kinetic":
            for q in s["items"]:
                M.put(q["at"] - 0.02, M.thud(0.4), 0.42)
        elif ty == "slam":
            M.put(s["at"] + 0.05, M.boom(1.8), 0.85)
        elif ty == "counter":
            n = 28
            span = s["until"] - s["at"]
            for m in range(n):
                M.put(s["at"] + span * (1 - (1 - (m + 1) / n) ** 0.5), M.tick(2200 + m * 30, 0.03), 0.28)
            M.put(s["until"], M.thud(0.6), 0.7)
        elif ty == "bars":
            for q in s["items"]:
                M.put(q["at"], M.tone(0.45, 180, 360), 0.8)
                M.put(q["at"] + 0.45, M.thud(0.3), 0.3)
        elif ty == "timeline":
            for q in s["items"]:
                M.put(q["at"], M.tick(2400, 0.04), 0.5)
                M.put(q["at"], M.thud(0.3), 0.25)
        elif ty == "map":
            M.put(T0 - 0.3, M.whoosh(0.6), 0.3)
            for r in s.get("routes") or []:
                M.put(r["at"], M.tone(max(0.3, r["until"] - r["at"])), 0.9)
            for p in s.get("pins") or []:
                M.put(p["at"] + 0.25, M.blip(), 0.5, 0.3)
        elif ty == "quote":
            L = len(s["text"])
            n = min(40, L)
            for k in range(n):
                M.put(s["at"] + (k / n) * s["typeDur"], M.key(), 0.3, ((k % 5) - 2) * 0.08)
        elif ty == "org":
            for q in s["nodes"]:
                M.put(q["at"], M.tick(2800, 0.04), 0.45)
                M.put(q["at"] + 0.02, M.thud(0.3), 0.22)
        elif ty == "ledger":
            for r in s.get("rows") or []:
                for k in range(3):
                    M.put(r["at"] + k * 0.05, M.key(), 0.35)
            if s.get("total"):
                M.put(s["total"]["at"], M.thud(0.6), 0.8)
        elif ty == "split":
            M.put(s["a"]["at"], M.thud(0.4), 0.5, -0.3)
            M.put(s["b"]["at"], M.thud(0.4), 0.5, 0.3)
            if s.get("sign"):
                M.put(s["signAt"] + 0.05, M.boom(1.4, 60, 36), 0.7)
        elif ty == "date":
            for k in range(len(s.get("day") or "")):
                M.put(s["dayAt"] + k * 0.045, M.key(), 0.35, (k - 3) * 0.04)
            groups = "".join(c if c.isdigit() else " " for c in s["date"]).split()
            for gi, grp in enumerate(groups):
                for j in range(len(grp)):
                    for m in range(8):
                        M.put(s["groupAt"][gi] - 0.05 + j * 0.07 + 0.55 * (1 - (1 - m / 8) ** 2.2), M.tick(2600 + 200 * j), 0.22, 0.1 * (j - 1))
        elif ty == "cards":
            for k, f in enumerate(s["flips"]):
                M.put(f - 0.05, M.whoosh(0.3), 0.35, (k - 1) * 0.4)
                M.put(f + 0.4, M.tick(1800, 0.05), 0.5, (k - 1) * 0.4)
            if s.get("sumAt") is not None:
                M.put(s["sumAt"], M.thud(0.5), 0.6)
            if s.get("zeroAt") is not None:
                M.put(s["zeroAt"] + 0.05, M.boom(2.0), 0.9)
    # KHÔNG chuẩn hoá theo đỉnh như Short: mỗi chương phải cùng một mức, chương ít tiếng động không được to lên
    import wave
    out = (np.clip(M.bed * 0.5, -1, 1) * 32767).astype("<i2")
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())

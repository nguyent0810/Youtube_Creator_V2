"""Static contract checks for Long scene dictionaries.

``casewide.js`` deliberately ignores unknown properties.  That is friendly for
experimentation but disastrous in production: a misspelt visual instruction
silently becomes a blank or incomplete frame.  This module is intentionally
dependency-free so it can also audit archived specs without rendering them.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from factory.console import utf8_console


MIN_SHOT_S = 2.5
MAX_SHOT_S = 9.0

# These are read before casewide builds the scene, rather than by a B.<type>
# renderer.  Keep this small and explicit: it must not become a loophole for
# arbitrary misspellings.
COMMON = {
    "type", "at", "t0", "t1", "tr", "fade", "nocaps",
    "label", "tag", "credit", "illus", "srcnote", "stamp", "film", "focus",
    "bg", "vid", "ms", "loop", "sfx", "tone", "veil", "pan", "z0", "z1",
}

# Keys read by B.<type> in motion/hf/assets/engine/casewide.js.  Theme-owned
# types (lab.js/chart.js) are deliberately not guessed; they produce a review
# warning, not a false block, until their own contract is added here.
SCENE_KEYS: dict[str, set[str]] = {
    "chapter": {"no", "k", "title", "sub", "titleAt", "num", "classic"},
    "broll": {"kin", "align"},
    "photo": {"img", "focus", "frame", "circles", "move", "reveal", "zoom", "kin", "align"},
    "print": {"img", "right", "maxW", "maxH", "pos", "caption", "circles", "rot", "side", "head"},
    "file": {"img", "pos", "cap", "name", "k", "desc", "rows"},
    "kinetic": {"items", "align", "accent", "lay"},
    "slam": {"text", "fx", "sub", "white"},
    "brand": {"name", "sub"},
    "endcard": {"sub"},
    "question": {"text", "showAt"},
    "counter": {"from", "to", "prefix", "suffix", "year", "countAt", "until", "calls", "sub", "label", "img"},
    "bars": {"title", "unit", "max", "items", "calls"},
    "myth": {"mythLab", "myth", "truthLab", "truth", "strikeAt", "truthAt"},
    "source": {"source", "ref", "snippet", "hlAt", "seal", "sealAt"},
    "units": {"title", "total", "cols", "lit", "litAt", "unitLabel"},
    "timeline": {"title", "items"},
    "map": {"geo", "routes", "pins", "zoom", "zoomK"},
    "quote": {"text", "at", "typeDur", "by", "dy", "lbl", "radio", "voiceAt", "voiceEnd", "qline"},
    "org": {"nodes", "y0"},
    "ledger": {"title", "rows", "total"},
    "split": {"title", "a", "b", "sign", "signAt"},
    "date": {"day", "dayAt", "date", "groupAt", "sub"},
    "cards": {"cards", "flips", "reads", "readAt", "sum", "sumAt", "zero", "zeroAt"},
    "evidence": {"img", "maxW", "maxH", "callouts"},
    "seismo": {"read", "hit", "hitAt"},
    "saint": {"img", "pos", "burnAt", "burnDur", "burnTo", "kin", "align"},
    "paper": {"mast", "date", "ed", "head", "vi", "img"},
    "pizzini": {"notes", "cipher"},
    "dots": {"total", "cols", "gh", "y0", "appearDur", "title", "groups"},
    "board": {"pins", "links"},
    "memorial": {"title", "names", "fs"},
    "calendar": {"from", "days", "endAt", "label", "months"},
    "sticker": {"items"},
    "sketch": {"art", "drawDur", "title"},
}

# casewide.css: #caps starts at 930px (1004px in noir); ledger starts at
# y=150 with 46px/54px vertical padding, title ~= 72px plus its 18px margin,
# and rows at the listed line-height.  Count includes ``total``.
LEDGER_LIMITS = {
    "lab": (96, 6, 930),
    "chart": (96, 6, 930),
    "noir": (76, 8, 1004),
    "default": (76, 7, 930),
}


def _issue(ch: str, index: int, scene: dict[str, Any], text: str) -> str:
    return f"{ch}#{index} {scene.get('type', '?')}: {text}"


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_anchor(value: Any) -> bool:
    """Raw specs use a list anchor; planned scenes use a resolved number."""
    return _is_number(value) or (isinstance(value, (list, tuple)) and len(value) >= 1)


def _image_refs(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"img", "bg"} and isinstance(child, str):
                yield child
            yield from _image_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from _image_refs(child)


def _validate_types(ch: str, index: int, scene: dict[str, Any], errors: list[str]) -> None:
    for key in ("pos",):
        if key in scene and not isinstance(scene[key], str):
            errors.append(_issue(ch, index, scene, f"{key} phải là chuỗi CSS, không phải {type(scene[key]).__name__}"))
    if "focus" in scene:
        focus = scene["focus"]
        if not (isinstance(focus, (list, tuple)) and len(focus) == 2 and all(_is_number(x) for x in focus)):
            errors.append(_issue(ch, index, scene, "focus phải là [x, y] gồm hai số"))
    for key in ("maxW", "maxH"):
        if key in scene and (not _is_number(scene[key]) or scene[key] < 50):
            errors.append(_issue(ch, index, scene, f"{key} phải là số pixel >= 50"))
    if scene.get("type") == "print" and scene.get("head") and not (isinstance(scene.get("side"), dict) and scene["side"].get("h")):
        errors.append(_issue(ch, index, scene, "head của print bị engine bỏ qua; dùng side.h"))
    if scene.get("type") == "quote":
        if "lbl" in scene and not isinstance(scene["lbl"], str):
            errors.append(_issue(ch, index, scene, "lbl của quote phải là nhãn chuỗi mà engine hiển thị"))
        if "dy" in scene and not isinstance(scene["dy"], bool):
            errors.append(_issue(ch, index, scene, "dy của quote phải là true/false"))
    if ("label" in scene and scene.get("type") not in {"counter", "calendar", "seismo"}
            and not isinstance(scene["label"], dict)):
        errors.append(_issue(ch, index, scene, "label phải là object {k, v, s, at}; nhãn quote hiển thị dùng lbl hoặc dy"))


def _validate_kinetic(ch: str, index: int, scene: dict[str, Any], errors: list[str]) -> None:
    if scene.get("type") != "kinetic":
        return
    text = " ".join(str(item.get("text", "")) for item in scene.get("items", []) if isinstance(item, dict)).casefold()
    accents: list[Any] = [scene["accent"]] if "accent" in scene else []
    accents.extend(item.get("acc") for item in scene.get("items", []) if isinstance(item, dict) and isinstance(item.get("acc"), str))
    for accent in accents:
        values = accent if isinstance(accent, (list, tuple, set)) else [accent]
        for value in values:
            if isinstance(value, str) and value.casefold() not in text:
                errors.append(_issue(ch, index, scene, f"accent kinetic {value!r} không khớp chữ nào trong dòng"))


def _validate_duration(ch: str, index: int, scene: dict[str, Any], errors: list[str]) -> None:
    if not (_is_number(scene.get("t0")) and _is_number(scene.get("t1"))):
        return
    duration = scene["t1"] - scene["t0"]
    if duration < MIN_SHOT_S or duration > MAX_SHOT_S:
        errors.append(_issue(ch, index, scene, f"thời lượng {duration:.2f}s ngoài [{MIN_SHOT_S:.1f}s, {MAX_SHOT_S:.1f}s]"))


def _validate_ledger(ch: str, index: int, scene: dict[str, Any], theme: str | None, errors: list[str]) -> None:
    if scene.get("type") != "ledger":
        return
    row_height, limit, caps_top = LEDGER_LIMITS.get(theme or "", LEDGER_LIMITS["default"])
    count = len(scene.get("rows") or []) + (1 if scene.get("total") else 0)
    if count > limit:
        errors.append(_issue(ch, index, scene, f"ledger có {count} dòng (rows + total), tối đa {limit}; CSS row {row_height}px, #caps y={caps_top}px"))


def validate_topic(
    chapters: Iterable[tuple[str, list[dict[str, Any]]]], imgs: dict[str, Any] | None = None, theme: str | None = None,
    check_scenes: bool = True,
) -> dict[str, Any]:
    """Validate planned or raw scenes; return machine-readable errors/warnings."""
    errors: list[str] = []
    warnings: list[str] = []
    uses: Counter[str] = Counter()
    for ch, scenes in chapters:
        for index, scene in enumerate(scenes):
            if not isinstance(scene, dict):
                errors.append(f"{ch}#{index} ?: cảnh phải là object")
                continue
            if check_scenes:
                typ = scene.get("type")
                if typ not in SCENE_KEYS:
                    warnings.append(_issue(ch, index, scene, "loại cảnh do theme/engine ngoài casewide.js; chưa đủ chứng cứ để kiểm key"))
                else:
                    allowed = COMMON | SCENE_KEYS[typ]
                    for key in scene:
                        if key not in allowed:
                            errors.append(_issue(ch, index, scene, f"key {key!r} không được engine đọc"))
                _validate_types(ch, index, scene, errors)
                _validate_kinetic(ch, index, scene, errors)
                _validate_duration(ch, index, scene, errors)
                _validate_ledger(ch, index, scene, theme, errors)
            uses.update(_image_refs(scene))
    declared = set((imgs or {}).keys())
    for key in sorted(declared - set(uses)):
        errors.append(f"spec.imgs: ảnh {key!r} không có cảnh nào dùng")
    counts = Counter()
    for message in errors:
        if "thời lượng" in message:
            counts["A7"] += 1
        elif "ledger có" in message:
            counts["A9"] += 1
        elif message.startswith("spec.imgs") or "ảnh " in message and "không có cảnh" in message:
            counts["A8"] += 1
        else:
            counts["A1"] += 1
    return {"errors": errors, "warnings": warnings, "counts": dict(counts), "image_uses": dict(uses)}


def _read_case(path: Path) -> dict[str, Any] | None:
    try:
        raw = path.read_text(encoding="utf-8")
        return json.loads(raw.split("=", 1)[1].strip().rstrip(";"))
    except (OSError, IndexError, json.JSONDecodeError):
        return None


def audit_topic(topic_dir: Path, output_root: Path) -> dict[str, Any]:
    """Audit source keys plus any already-built plans; never writes files."""
    spec = json.loads((topic_dir / "spec.json").read_text(encoding="utf-8"))
    theme = spec.get("theme") or {"MIM": "lab", "CK": "chart"}.get(spec.get("channel", "CL"))
    raw_chapters = []
    for path in sorted(topic_dir.glob("ch*.json")):
        raw_chapters.append((path.stem, json.loads(path.read_text(encoding="utf-8")).get("scenes") or []))
    # ``plan()`` resolves and renames cue aliases (for example hitAt -> at).
    # Only audit declarations in source scenes; validate the contract on the
    # exact planned scene dictionaries that the engine will receive.
    source = validate_topic(raw_chapters, spec.get("imgs") or {}, theme, check_scenes=False)
    planned_chapters = []
    for chapter, _ in raw_chapters:
        case = _read_case(output_root / topic_dir.name / chapter / "data.js")
        if case:
            planned_chapters.append((chapter, case.get("scenes") or []))
    planned = validate_topic(planned_chapters, None, theme)
    errors = source["errors"] + planned["errors"]
    counts = Counter(source["counts"])
    counts.update(planned["counts"])
    return {
        "topic": topic_dir.name,
        "channel": spec.get("channel", "CL"),
        "chapters": len(raw_chapters),
        "planned_chapters": len(planned_chapters),
        "errors": errors,
        "warnings": source["warnings"] + planned["warnings"],
        "counts": {rule: counts.get(rule, 0) for rule in ("A1", "A7", "A8", "A9")},
    }


def main(argv: list[str] | None = None) -> int:
    utf8_console()
    parser = argparse.ArgumentParser(description="Audit Long scene parameters without rendering")
    parser.add_argument("topics", nargs="*", help="topic directory names")
    parser.add_argument("--all", action="store_true", help="audit all MIM and CK topics")
    parser.add_argument("--cl", nargs="*", default=[], help="additional CL topic names")
    args = parser.parse_args(argv)
    if not args.all and not args.topics and not args.cl:
        parser.error("pass topics, --all, or --cl")
    root = Path(__file__).resolve().parents[2]
    data_root, output_root = root / "data" / "long", root / "output" / "long"
    names = list(args.topics) + list(args.cl)
    if args.all:
        names += [p.name for p in data_root.iterdir() if p.is_dir() and (p / "spec.json").is_file()
                  and p.name.startswith(("mim-", "ck-"))]
    results = [audit_topic(data_root / name, output_root) for name in sorted(set(names))]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 1 if any(result["errors"] for result in results) else 0


if __name__ == "__main__":  # pragma: no cover - exercised as a production CLI
    raise SystemExit(main())


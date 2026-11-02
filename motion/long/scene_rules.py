#!/usr/bin/env python3
"""Audit Long scene plans and propose copy-ready still-image improvements.

The tool never changes ``data/long``. Its JSON is a review queue whose patch
payloads use only fields read by Long's casewide engine. A ``photo`` has an
effective ``move`` of ``in`` when the optional field is omitted, so a missing
``move`` is not itself a defect.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from factory.console import utf8_console
STILL_TYPES = {"photo", "print"}
MOVE_PRESETS = ("in", "out", "pan")
LONG_STILL_S = 8.0
SPLIT_STILL_S = 12.0
MIN_SHOT_S = 2.5
MAX_SHOTS = 3


def _as_int(value: Any) -> int | None:
    if isinstance(value, (list, tuple)) and value:
        value = value[0]
    if isinstance(value, bool):
        return None
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number if number >= 0 else None


def scene_at(scene: dict[str, Any]) -> int | None:
    for key in ("at", "countAt", "drawAt", "titleAt", "until"):
        number = _as_int(scene.get(key))
        if number is not None:
            return number
    return None


def media_id(scene: dict[str, Any]) -> str | None:
    for key in ("img", "image", "src", "media", "asset"):
        value = scene.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def effective_effect(scene: dict[str, Any]) -> str | None:
    """Return a visible base effect, including casewide's photo default."""
    scene_type = str(scene.get("type") or "")
    if scene_type == "photo":
        move = scene.get("move")
        return move.strip() if isinstance(move, str) and move.strip() else "in"
    if scene_type == "print":
        return "print"  # B.print has a fixed entrance plus gentle scale-up.
    return None


def _segments(timing: dict[str, Any]) -> list[dict[str, Any]]:
    raw = timing.get("segments") or timing.get("lines") or []
    if not isinstance(raw, list):
        return []
    out: list[dict[str, Any]] = []
    for fallback, item in enumerate(raw):
        if not isinstance(item, dict):
            continue
        index = _as_int(item.get("index"))
        if index is None:
            index = _as_int(item.get("sentence_id"))
            if index is not None and "sentence_id" in item:
                index -= 1
        if index is None:
            index = fallback
        try:
            start, end = float(item["start"]), float(item["end"])
        except (KeyError, TypeError, ValueError):
            continue
        if end >= start:
            out.append({"index": index, "start": start, "end": end})
    return sorted(out, key=lambda entry: entry["index"])


def _time_for_sentence(segments: list[dict[str, Any]], sentence: int | None) -> float | None:
    if sentence is None:
        return None
    for segment in segments:
        if segment["index"] == sentence:
            return segment["start"]
    return None


def _chapter_end(timing: dict[str, Any], segments: list[dict[str, Any]]) -> float | None:
    try:
        return float(timing["duration"])
    except (KeyError, TypeError, ValueError):
        return max((segment["end"] for segment in segments), default=None)


def _cut_sentences(
    segments: list[dict[str, Any]], start_at: int, end_at: int | None,
    start_s: float, end_s: float,
) -> list[int]:
    return [
        segment["index"] for segment in segments
        if segment["index"] > start_at
        and (end_at is None or segment["index"] < end_at)
        and segment["start"] - start_s >= MIN_SHOT_S
        and end_s - segment["start"] >= MIN_SHOT_S
    ]


def _sample_cuts(cuts: list[int], count: int) -> list[int]:
    if count <= 0 or not cuts:
        return []
    if len(cuts) <= count:
        return list(cuts)
    return [cuts[min(len(cuts) - 1, int((i + 0.5) * len(cuts) / count))] for i in range(count)]


def _choose_move(previous: str | None) -> str:
    """Choose a valid ``photo.move`` different from the preceding effect."""
    return next((move for move in MOVE_PRESETS if move != previous), MOVE_PRESETS[0])


def _mid_sentence(
    segments: list[dict[str, Any]], start_at: int, end_at: int | None,
    start_s: float, end_s: float,
) -> int | None:
    candidates = [
        segment for segment in segments
        if segment["index"] > start_at and (end_at is None or segment["index"] < end_at)
    ]
    if not candidates:
        return None
    midpoint = (start_s + end_s) / 2
    return min(candidates, key=lambda segment: abs(segment["start"] - midpoint))["index"]


def _zoom_patch(at: int) -> dict[str, Any]:
    return {"zoom": {"x": 0.5, "y": 0.5, "z": 1.35, "at": at, "d": 1.2}}


def _reveal_patch(at: int) -> dict[str, Any]:
    return {"reveal": {"kind": "wipe", "at": at, "d": 0.9}}


def _circles_patch(at: int) -> dict[str, Any]:
    return {"circles": [{"x": 0.5, "y": 0.5, "r": 0.16, "at": at}]}


def _replacement_stills(
    scene: dict[str, Any], starts: list[int], prior_effect: str | None,
) -> list[dict[str, Any]]:
    """Duplicate a valid scene into sentence-anchored, copy-ready shots."""
    replacements: list[dict[str, Any]] = []
    effect = prior_effect
    for shot_index, at in enumerate(starts):
        replacement = dict(scene)
        replacement["at"] = at
        if replacement.get("type") == "photo":
            if shot_index == 0:
                effect = effective_effect(scene)
            else:
                effect = _choose_move(effect)
                replacement["move"] = effect
        replacements.append(replacement)
    return replacements


def _long_still_proposals(
    scene: dict[str, Any], index: int, start_at: int, next_at: int | None,
    start_s: float, end_s: float, duration: float, segments: list[dict[str, Any]],
    prior_effect: str | None,
) -> list[dict[str, Any]]:
    """Propose effect fields over 8 seconds and a split only over 12."""
    scene_type = str(scene.get("type") or "")
    base = {
        "scene_index": index, "at": start_at, "type": scene_type,
        "media": media_id(scene), "duration_s": duration,
    }
    proposals: list[dict[str, Any]] = []
    middle_at = _mid_sentence(segments, start_at, next_at, start_s, end_s)
    if middle_at is None:
        proposals.append({
            "kind": "long_still_no_mid_sentence", **base,
            "reason": "ảnh tĩnh quá 8 giây nhưng không có đầu câu ở giữa cảnh để đặt hiệu ứng",
        })
    elif scene_type == "print":
        proposals.append({
            "kind": "long_print_circles", **base, "patch": _circles_patch(middle_at),
            "reason": "print dài quá 8 giây; khoanh chi tiết ở đầu câu giữa cảnh",
        })
    elif scene.get("zoom") is None:
        proposals.append({
            "kind": "long_photo_zoom", **base, "patch": _zoom_patch(middle_at),
            "reason": "ảnh dài quá 8 giây; zoom vào chi tiết ở đầu câu giữa cảnh",
        })
    else:
        proposals.append({
            "kind": "long_photo_reveal", **base, "patch": _reveal_patch(middle_at),
            "reason": "ảnh dài quá 8 giây đã có zoom; thêm reveal ở đầu câu giữa cảnh",
        })

    if duration <= SPLIT_STILL_S:
        return proposals
    cuts = _cut_sentences(segments, start_at, next_at, start_s, end_s)
    requested = 3 if len(cuts) >= 2 else 2
    starts = [start_at] + _sample_cuts(cuts, min(MAX_SHOTS, requested) - 1)
    if len(starts) > 1:
        proposals.append({
            "kind": "split_still", **base,
            "replacement_scenes": _replacement_stills(scene, starts, prior_effect),
            "reason": "ảnh tĩnh dài quá 12 giây; chỉ chia tại đầu câu và mỗi shot có ít nhất 2,5 giây",
        })
    else:
        proposals.append({
            "kind": "long_still_no_split_boundary", **base,
            "reason": "ảnh tĩnh dài quá 12 giây nhưng không có ranh giới câu đủ 2,5 giây mỗi phía để chia shot",
        })
    return proposals


def analyze_chapter(
    chapter: str, scenes: list[dict[str, Any]], timing: dict[str, Any],
) -> dict[str, Any]:
    """Return warnings and review-only proposals for one chapter."""
    segments = _segments(timing)
    end_of_chapter = _chapter_end(timing, segments)
    warnings: list[dict[str, Any]] = []
    proposals: list[dict[str, Any]] = []
    anchors = [scene_at(scene) for scene in scenes]
    for index, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            continue
        scene_type = str(scene.get("type") or "")
        current_media = media_id(scene)
        prior = scenes[index - 1] if index else None
        if isinstance(prior, dict):
            prior_type = str(prior.get("type") or "")
            if scene_type and scene_type == prior_type:
                warnings.append({"kind": "adjacent_type", "scene_index": index, "at": anchors[index], "reason": f"cảnh liền kề cùng loại: {scene_type}"})
            if current_media and current_media == media_id(prior):
                warnings.append({"kind": "adjacent_media", "scene_index": index, "at": anchors[index], "media": current_media, "reason": "cảnh liền kề dùng cùng media"})
        if scene_type not in STILL_TYPES:
            continue

        effect = effective_effect(scene)
        prior_effect = effective_effect(prior) if isinstance(prior, dict) else None
        start_at = anchors[index]
        if prior_effect == effect:
            patch = {"move": _choose_move(effect)} if scene_type == "photo" else {"type": "photo", "move": _choose_move(None)}
            proposals.append({
                "kind": "same_still_effect", "scene_index": index, "at": start_at,
                "type": scene_type, "media": current_media,
                "effective_effect": effect, "previous_effect": prior_effect, "patch": patch,
                "reason": "hai ảnh liền nhau cùng hiệu ứng thực tế; đổi hiệu ứng cảnh sau",
            })

        start_s = _time_for_sentence(segments, start_at)
        next_at = next((anchor for anchor in anchors[index + 1:] if anchor is not None), None)
        end_s = _time_for_sentence(segments, next_at) if next_at is not None else end_of_chapter
        if start_at is None or start_s is None or end_s is None:
            continue
        duration = round(end_s - start_s, 3)
        if duration > LONG_STILL_S:
            proposals.extend(_long_still_proposals(
                scene, index, start_at, next_at, start_s, end_s, duration, segments, prior_effect,
            ))
    return {"chapter": chapter, "timing_found": bool(segments), "scene_count": len(scenes), "warnings": warnings, "proposals": proposals}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _topic_chapters(topic: str) -> Iterable[tuple[str, Path]]:
    topic_dir = ROOT / "data" / "long" / topic
    yield from ((path.stem, path) for path in sorted(topic_dir.glob("ch*.json")))


def analyze_topic(topic: str) -> dict[str, Any]:
    chapters: list[dict[str, Any]] = []
    missing_timing: list[str] = []
    for chapter, scene_path in _topic_chapters(topic):
        timing_path = ROOT / "output" / "long" / topic / chapter / "timing.json"
        if not timing_path.is_file():
            missing_timing.append(chapter)
            continue
        scene_data = _load_json(scene_path)
        scenes = scene_data.get("scenes", []) if isinstance(scene_data, dict) else []
        chapters.append(analyze_chapter(chapter, scenes if isinstance(scenes, list) else [], _load_json(timing_path)))
    warnings = sum(len(chapter["warnings"]) for chapter in chapters)
    proposals = sum(len(chapter["proposals"]) for chapter in chapters)
    return {
        "topic": topic,
        "source": {"spec": f"data/long/{topic}/chNN.json", "timing": f"output/long/{topic}/chNN/timing.json"},
        "rules": {"still_types": sorted(STILL_TYPES), "long_still_s": LONG_STILL_S, "split_still_s": SPLIT_STILL_S, "min_shot_s": MIN_SHOT_S, "move_presets": list(MOVE_PRESETS), "photo_default_move": "in"},
        "chapters": chapters, "missing_timing": missing_timing,
        "summary": {"chapters": len(chapters), "warnings": warnings, "proposals": proposals, "missing_timing": len(missing_timing)},
    }


def write_topic(topic: str) -> dict[str, Any]:
    result = analyze_topic(topic)
    destination = ROOT / "output" / "long" / topic / "scene_rules.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def _all_topics() -> list[str]:
    base = ROOT / "data" / "long"
    return sorted(path.name for path in base.iterdir() if path.is_dir() and path.name.startswith(("mim-", "ck-")))


def main(argv: list[str] | None = None) -> int:
    utf8_console()
    parser = argparse.ArgumentParser(description="Audit Long scene repetition and still-image motion.")
    parser.add_argument("topic", nargs="?", help="a mim-* or ck-* topic")
    parser.add_argument("--all", action="store_true", help="analyse only mim-* and ck-* topics")
    args = parser.parse_args(argv)
    if bool(args.topic) == bool(args.all):
        parser.error("pass one topic or --all")
    topics = _all_topics() if args.all else [args.topic]
    if args.topic and not args.topic.startswith(("mim-", "ck-")):
        parser.error("topic must start with mim- or ck-")
    for topic in topics:
        if not (ROOT / "data" / "long" / topic).is_dir():
            parser.error(f"topic not found: {topic}")
    results = [write_topic(topic) for topic in topics]
    ranking = sorted(({"topic": result["topic"], **result["summary"]} for result in results), key=lambda item: (-item["proposals"], -item["warnings"], item["topic"]))
    print(json.dumps({"topics": len(results), "top": ranking[:10]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

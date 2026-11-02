#!/usr/bin/env python3
"""Kiểm độ phủ ảnh/clip của Long MIM và CK.

Dữ liệu cảnh dùng ``at`` là số câu (0-based); ``timing.json`` cho giây bắt
đầu từng câu. Một cảnh kéo dài đến cảnh neo tiếp theo. Công cụ này chỉ đọc
dữ liệu, không sửa bài Long.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

# Ngưỡng đề xuất sau đợt đo vòng 2; hai cổng này cùng phải đạt.
MAX_TEXT_ONLY_PERCENT = 22.0
MAX_CONSECUTIVE_TEXT_ONLY_SECONDS = 17.0
# Chỉ số tham khảo: đồ họa động không phải là cảnh khô, nên không dùng để chặn.
MAX_NO_IMAGE_SECONDS = 25.0
MAX_STATIC_IMAGE_SECONDS = 8.0

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from factory.console import utf8_console
DATA_LONG = ROOT / "data" / "long"
OUTPUT_LONG = ROOT / "output" / "long"
TEXT_TYPES = {"kinetic", "slam", "question", "quote", "myth", "brand"}
STATIC_TYPES = {"photo", "print"}
MEDIA_KEYS = {"img", "vid", "bg"}


@dataclass(frozen=True)
class Interval:
    chapter: str
    start: float
    end: float
    start_line: int
    end_line: int
    has_image: bool
    text_only: bool
    static_image: bool
    scene_type: str
    visual_class: str = "animated_graphics"

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)


def _load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _at_line(value: Any) -> int:
    """Read integer or an anchor such as ``'12 rồi'`` into a line number."""
    # ``a(line, word)`` is serialized by existing Longs as [line, word].
    if isinstance(value, (list, tuple)):
        return _at_line(value[0] if value else 0)
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return max(0, value)
    if isinstance(value, float):
        return max(0, int(value))
    match = re.match(r"\s*(\d+)", str(value or ""))
    return int(match.group(1)) if match else 0


def _scene_has_image(scene: dict[str, Any]) -> bool:
    kind = str(scene.get("type") or "").lower()
    return kind in STATIC_TYPES or any(scene.get(key) for key in MEDIA_KEYS)


def _scene_text_only(scene: dict[str, Any]) -> bool:
    kind = str(scene.get("type") or "").lower()
    return kind in TEXT_TYPES and not _scene_has_image(scene)


def _visual_class(scenes: list[dict[str, Any]]) -> str:
    """Classify an anchored scene group into exactly one visual layer.

    Image/clip wins when several scene declarations share an anchor.  A group is
    text-only only when every declaration is an unaccompanied TEXT_TYPES scene;
    everything else is moving graphics (charts, maps, counters, diagrams, ...).
    """
    if any(_scene_has_image(scene) for scene in scenes):
        return "image_or_clip"
    if scenes and all(_scene_text_only(scene) for scene in scenes):
        return "text_only"
    return "animated_graphics"


def _interval_visual_class(interval: Interval) -> str:
    """Read the class from an interval, including legacy synthetic test fixtures."""
    if interval.has_image:
        return "image_or_clip"
    if interval.text_only:
        return "text_only"
    return "animated_graphics"


def _line_text(line: Any) -> str:
    return str(line.get("t", "")) if isinstance(line, dict) else str(line or "")


def _timing_data(path: Path) -> tuple[list[dict[str, Any]], float]:
    data = _load_json(path)
    segments = list(data.get("segments") or [])
    if not segments:
        raise ValueError(f"{path}: thiếu segments")
    duration = float(data.get("duration") or segments[-1].get("end") or 0)
    if duration <= 0:
        raise ValueError(f"{path}: duration không hợp lệ")
    return segments, duration


def chapter_intervals(topic: str, chapter_path: Path, offset: float = 0.0) -> tuple[list[Interval], list[str], float]:
    """Return visual intervals and narration lines for one chapter."""
    chapter = chapter_path.stem
    timing_path = OUTPUT_LONG / topic / chapter / "timing.json"
    if not timing_path.is_file():
        raise FileNotFoundError(f"thiếu {timing_path.relative_to(ROOT)}")
    data = _load_json(chapter_path)
    if not isinstance(data, dict):
        raise ValueError(f"{chapter_path}: chương phải là object JSON")
    lines = [_line_text(line) for line in data.get("lines") or []]
    segments, duration = _timing_data(timing_path)
    if not lines:
        lines = [str(item.get("text") or "") for item in segments]
    starts = [float(item.get("start") or 0.0) for item in segments]
    scene_groups: dict[int, list[dict[str, Any]]] = {}
    for item in data.get("scenes") or []:
        if isinstance(item, dict):
            line = min(_at_line(item.get("at", 0)), max(0, len(starts) - 1))
            scene_groups.setdefault(line, []).append(item)
    if not scene_groups:
        scene_groups = {0: [{}]}

    anchors = sorted(scene_groups)
    intervals: list[Interval] = []
    for index, line in enumerate(anchors):
        next_line = anchors[index + 1] if index + 1 < len(anchors) else len(starts)
        start = starts[min(line, len(starts) - 1)]
        end = starts[next_line] if next_line < len(starts) else duration
        scenes = scene_groups[line]
        visual_class = _visual_class(scenes)
        kinds = "/".join(sorted({str(scene.get("type") or "unknown") for scene in scenes}))
        intervals.append(Interval(
            chapter=chapter,
            start=offset + start,
            end=offset + max(start, end),
            start_line=line,
            end_line=max(line, next_line - 1),
            has_image=visual_class == "image_or_clip",
            text_only=visual_class == "text_only",
            static_image=any(str(scene.get("type") or "").lower() in STATIC_TYPES for scene in scenes),
            scene_type=kinds,
            visual_class=visual_class,
        ))
    return intervals, lines, duration


def collect(topic: str) -> tuple[list[Interval], dict[str, list[str]], float]:
    folder = DATA_LONG / topic
    if not folder.is_dir():
        raise FileNotFoundError(f"không có {folder.relative_to(ROOT)}")
    paths = sorted(folder.glob("ch*.json"))
    if not paths:
        raise FileNotFoundError(f"{folder.relative_to(ROOT)} không có chNN.json")
    intervals: list[Interval] = []
    narration: dict[str, list[str]] = {}
    offset = 0.0
    for path in paths:
        items, lines, duration = chapter_intervals(topic, path, offset)
        intervals.extend(items)
        narration[path.stem] = lines
        offset += duration
    return intervals, narration, offset


def _merge_consecutive(intervals: Iterable[Interval], predicate: Any) -> list[list[Interval]]:
    """Merge qualifying intervals, never across a chapter boundary."""
    groups: list[list[Interval]] = []
    for interval in intervals:
        if not predicate(interval):
            continue
        if (groups and groups[-1][-1].chapter == interval.chapter
                and abs(groups[-1][-1].end - interval.start) < 0.02):
            groups[-1].append(interval)
        else:
            groups.append([interval])
    return groups


def _sentence(lines: dict[str, list[str]], interval: Interval, *, end: bool = False) -> str:
    chapter_lines = lines.get(interval.chapter, [])
    index = interval.end_line if end else interval.start_line
    return chapter_lines[index] if 0 <= index < len(chapter_lines) else ""


def analyse(topic: str) -> dict[str, Any]:
    intervals, narration, duration = collect(topic)
    text_seconds = sum(item.duration for item in intervals if item.text_only)
    static = [item for item in intervals if item.static_image]
    visual_seconds = {
        "image_or_clip": round(sum(item.duration for item in intervals if _interval_visual_class(item) == "image_or_clip"), 2),
        "animated_graphics": round(sum(item.duration for item in intervals if _interval_visual_class(item) == "animated_graphics"), 2),
        "text_only": round(text_seconds, 2),
    }
    text_runs = _merge_consecutive(intervals, lambda item: item.text_only)
    no_image_runs = _merge_consecutive(intervals, lambda item: not item.has_image)
    longest_text_run = max((sum(item.duration for item in group) for group in text_runs), default=0.0)
    longest_no_image_gap = max((sum(item.duration for item in group) for group in no_image_runs), default=0.0)
    text_only_gaps: list[dict[str, Any]] = []
    for group in text_runs:
        seconds = sum(item.duration for item in group)
        if seconds > MAX_CONSECUTIVE_TEXT_ONLY_SECONDS:
            first, last = group[0], group[-1]
            text_only_gaps.append({
                "chapter": first.chapter, "start_s": round(first.start, 2), "end_s": round(last.end, 2),
                "duration_s": round(seconds, 2),
                "start": {"sentence": first.start_line + 1, "narration": _sentence(narration, first)},
                "end": {"sentence": last.end_line + 1, "narration": _sentence(narration, last, end=True)},
            })
    no_image: list[dict[str, Any]] = []
    for group in no_image_runs:
        seconds = sum(item.duration for item in group)
        if seconds > MAX_NO_IMAGE_SECONDS:
            first, last = group[0], group[-1]
            no_image.append({
                "chapters": sorted({item.chapter for item in group}),
                "start_s": round(first.start, 2), "end_s": round(last.end, 2),
                "duration_s": round(seconds, 2),
                "start": {"chapter": first.chapter, "sentence": first.start_line + 1,
                          "narration": _sentence(narration, first)},
                "end": {"chapter": last.chapter, "sentence": last.end_line + 1,
                        "narration": _sentence(narration, last, end=True)},
            })
    long_static = [
        {"chapter": item.chapter, "sentence": item.start_line + 1,
         "duration_s": round(item.duration, 2), "type": item.scene_type,
         "narration": _sentence(narration, item)}
        for item in static if item.duration > MAX_STATIC_IMAGE_SECONDS
    ]
    text_percent = (100 * text_seconds / duration) if duration else 0.0
    return {
        "topic": topic,
        "duration_s": round(duration, 2),
        "text_only_s": round(text_seconds, 2),
        "text_only_percent": round(text_percent, 2),
        "visual_seconds": visual_seconds,
        "longest_text_only_run_s": round(longest_text_run, 2),
        "text_only_gaps": text_only_gaps,
        "longest_no_image_gap_s": round(longest_no_image_gap, 2),
        "no_image_gaps": no_image,
        "long_static_images": long_static,
        "thresholds": {"max_no_image_seconds": MAX_NO_IMAGE_SECONDS,
                       "max_text_only_percent": MAX_TEXT_ONLY_PERCENT,
                       "max_consecutive_text_only_seconds": MAX_CONSECUTIVE_TEXT_ONLY_SECONDS,
                       "max_static_image_seconds": MAX_STATIC_IMAGE_SECONDS},
    }


def violations(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if report["text_only_percent"] > MAX_TEXT_ONLY_PERCENT:
        errors.append(f"chỉ chữ {report['text_only_percent']:.2f}% > {MAX_TEXT_ONLY_PERCENT:.0f}%")
    if report["longest_text_only_run_s"] > MAX_CONSECUTIVE_TEXT_ONLY_SECONDS:
        errors.append("chuỗi chỉ chữ "
                      f"{report['longest_text_only_run_s']:.2f}s > {MAX_CONSECUTIVE_TEXT_ONLY_SECONDS:.0f}s")
    return errors


def _topics() -> list[str]:
    """Return completed Longs only; work-in-progress topics have no full timing."""
    result: list[str] = []
    for folder in sorted(DATA_LONG.iterdir()):
        if not folder.is_dir() or not re.match(r"^(mim|ck)-", folder.name):
            continue
        chapters = list(folder.glob("ch*.json"))
        if chapters and all((OUTPUT_LONG / folder.name / path.stem / "timing.json").is_file() for path in chapters):
            result.append(folder.name)
    return result


def print_report(report: dict[str, Any]) -> None:
    print(f"{report['topic']}: text-only {report['text_only_percent']:.2f}% ({report['text_only_s']:.2f}s/{report['duration_s']:.2f}s)")
    print("  longest text-only run: "
          f"{report['longest_text_only_run_s']:.2f}s; longest no-image/clip gap (reference): "
          f"{report['longest_no_image_gap_s']:.2f}s")
    print(f"  static images > {MAX_STATIC_IMAGE_SECONDS:.0f}s (reference): {len(report['long_static_images'])}")
    for message in violations(report):
        print(f"  FAIL: {message}")


def main(argv: list[str] | None = None) -> int:
    utf8_console()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", nargs="?", help="mim-* hoặc ck-*")
    parser.add_argument("--all", action="store_true", help="đo tất cả Long MIM/CK")
    parser.add_argument("--json", action="store_true", help="in dữ liệu JSON")
    args = parser.parse_args(argv)
    if bool(args.topic) == bool(args.all):
        parser.error("chọn đúng một: <topic> hoặc --all")
    topics = _topics() if args.all else [args.topic]
    reports: list[dict[str, Any]] = []
    try:
        for topic in topics:
            if not re.match(r"^(mim|ck)-", topic or ""):
                raise ValueError("chỉ áp dụng topic mim-* hoặc ck-*")
            reports.append(analyse(topic))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(reports if args.all else reports[0], ensure_ascii=False, indent=2))
    else:
        for report in reports:
            print_report(report)
    return 1 if any(violations(report) for report in reports) else 0


if __name__ == "__main__":
    raise SystemExit(main())

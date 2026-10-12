"""Hai kiểm tra thêm ngày 12/10/2026: nhãn bản đồ khi zoom và bề rộng chữ kinetic theo font của look."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "motion" / "long"))

import lint_html

PINS = {"Medellín": (850.0, "MEDELLÍN"), "Envigado": (852.0, "ENVIGADO"), "Bogotá": (790.0, "BOGOTÁ"), "Soacha": (800.0, "SOACHA")}   # x trên sân khấu 1920


def _map(label, name, zoom, k):
    return {"type": "map", "geo": "co", "zoom": zoom, "zoomK": k, "pins": [{"name": name, "label": label}]}


def test_zoomed_map_label_that_was_clipped_in_escobar_is_flagged():
    scenes = [_map("ENVIGADO · LA CATEDRAL", "Envigado", "Medellín", 2.4), _map("SOACHA · NƠI GALÁN NGÃ XUỐNG", "Soacha", "Bogotá", 2.4)]
    out = lint_html.check_scenes("ch10", scenes, {"co": PINS})
    assert len(out) == 2 and all("(map)" in m for m in out)


def test_short_label_and_unzoomed_map_pass():
    scenes = [_map("LA CATEDRAL", "Envigado", "Medellín", 2.4), _map("SOACHA · 18.08.1989", "Soacha", "Bogotá", 2.4),
              {"type": "map", "geo": "co", "pins": [{"name": "Soacha", "label": "SOACHA · CẠNH BOGOTÁ · 18.08.1989"}]}]
    assert lint_html.check_scenes("ch07", scenes, {"co": PINS}) == []


def test_map_lint_is_skipped_without_pin_positions():
    assert lint_html.check_scenes("ch07", [_map("X" * 80, "Soacha", "Bogotá", 2.4)]) == []


def test_kinetic_line_wider_than_box_is_flagged_for_wide_font_only():
    if not (lint_html.FONT_DIR / "Montserrat-900.ttf").exists():   # motion/long/fonts bị .gitignore: máy mới chưa tải font thì bỏ qua
        pytest.skip("chưa có font Montserrat trong motion/long/fonts")
    scenes = [{"type": "kinetic", "items": [{"text": "KHÔNG NƯỚC NÀO MUỐN NHẬN"}]}]
    assert lint_html.kinetic_problems("ch13", scenes, "Montserrat", 1.0)        # lỗi Escobar ch13 trước khi có kw
    assert lint_html.kinetic_problems("ch13", scenes, "Montserrat", 1.07) == []   # kw của look amber
    assert lint_html.kinetic_problems("ch13", scenes, "Barlow Condensed", 0.74) == []


def test_kinetic_lint_ignores_unknown_font_and_serif_lines():
    scenes = [{"type": "kinetic", "items": [{"text": "M" * 60, "serif": True}]}]
    assert lint_html.kinetic_problems("ch00", scenes, "Montserrat", 1.0) == []
    assert lint_html.kinetic_problems("ch00", [{"type": "kinetic", "items": [{"text": "M" * 60}]}], "Font Không Có", 1.0) == []

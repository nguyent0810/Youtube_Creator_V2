"""Dữ liệu giả cho coverage_lint và prompt ảnh dự phòng."""
from __future__ import annotations

import unittest
from unittest.mock import patch

from motion.long import ai_prompt, coverage_lint


class CoverageLintTest(unittest.TestCase):
    def test_measures_text_gap_and_static_hold(self) -> None:
        # Synthetic three-scene chapter: two text scenes, then a 10-second photo.
        intervals = [
            coverage_lint.Interval("ch00", 0, 10, 0, 0, False, True, False, "kinetic"),
            coverage_lint.Interval("ch00", 10, 20, 1, 1, False, True, False, "question"),
            coverage_lint.Interval("ch00", 20, 30, 2, 2, True, False, True, "photo"),
        ]
        narration = {"ch00": ["Câu một.", "Câu hai.", "Câu ba."]}
        with patch.object(coverage_lint, "collect", return_value=(intervals, narration, 30)):
            report = coverage_lint.analyse("mim-demo")
        self.assertEqual(report["text_only_percent"], 66.67)
        self.assertEqual(len(report["no_image_gaps"]), 0)  # exactly 20 s stays under the 25 s draft gate
        self.assertEqual(report["long_static_images"][0]["duration_s"], 10.0)
        self.assertEqual(report["longest_text_only_run_s"], 20.0)
        self.assertEqual(report["visual_seconds"]["animated_graphics"], 0)
        self.assertNotIn("ảnh tĩnh", " ".join(coverage_lint.violations(report)))

    def test_reads_serialized_word_anchor(self) -> None:
        self.assertEqual(coverage_lint._at_line([12, "từ"]), 12)


class AiPromptTest(unittest.TestCase):
    def test_uses_longest_matching_lexicon_subject(self) -> None:
        profile = {"assets": {
            "phong_cach": "editorial illustration",
            "fallback_subject": "fallback scene",
            "cam_cum": ["readable text"],
        }}
        entries = [{"vi": "máy", "en": "a machine"}, {"vi": "máy tính", "en": "a vintage computer"}]
        with patch.object(ai_prompt, "_lexicon_entries", return_value=entries):
            prompt = ai_prompt.generate_prompt("Chiếc máy tính cũ đang chạy.", profile)
        self.assertIn("a vintage computer", prompt)
        self.assertIn("Avoid readable text", prompt)

    def test_channel_lexicon_and_adjacent_subjects(self) -> None:
        profile = {"kenh": "mim", "assets": {"phong_cach": "editorial illustration",
                   "fallback_subject": "fallback scene", "cam_cum": []}}
        entries = [{"vi": "chip", "en": "a silicon chip"}, {"vi": "dữ liệu", "en": "a data archive"}]
        with patch.object(ai_prompt, "_lexicon_entries", return_value=entries):
            first = ai_prompt.generate_prompt_details("Con chip xử lý dữ liệu.", profile)
            second = ai_prompt.generate_prompt_details("Con chip lại nóng lên.", profile,
                                                       previous_subject=first["subject"])
        self.assertEqual(first["subject"], "a data archive")
        self.assertNotEqual(first["subject"], second["subject"])


if __name__ == "__main__":
    unittest.main()

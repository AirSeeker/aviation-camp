import unittest

from scripts.generate_content import (
    build_system_prompt,
    contains_non_english_text,
    estimate_read_time_minutes,
    generate_fallback_mdx,
    infer_title_from_chapter,
    load_chapter_files,
    source_book_title,
    translation_key_for,
)


class GenerateContentTests(unittest.TestCase):
    def test_loads_parsed_markdown_with_legacy_text_fallback(self) -> None:
        from pathlib import Path
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            chapter_dir = Path(directory) / "ch01"
            chapter_dir.mkdir()
            (chapter_dir / "content.md").write_text("Markdown source content", encoding="utf-8")
            self.assertEqual(load_chapter_files(Path(directory), "ch01")["content"], "Markdown source content")

    def test_fallback_mdx_uses_english_frontmatter_and_i18n_fields(self) -> None:
        mdx = generate_fallback_mdx(
            "PHAK",
            "ch01",
            "This chapter explains lift, drag, and stall in a steady climb profile.",
            [],
            "Principles of Flight",
        )

        self.assertIn('lang: "en"', mdx)
        self.assertIn('translationKey: "phak-ch01"', mdx)
        self.assertIn('subject: "Principles of Flight"', mdx)
        self.assertIn('chapterNumber: 1', mdx)
        self.assertIn('readTimeMinutes: 8', mdx)
        self.assertIn('This chapter explains lift, drag, and stall', mdx)
        self.assertNotIn('Ключові', mdx)
        self.assertNotIn('Увага:', mdx)

    def test_system_prompt_requires_english_output_and_i18n_metadata(self) -> None:
        prompt = build_system_prompt("Principles of Flight")

        self.assertIn('English', prompt)
        self.assertIn('lang: "en"', prompt)
        self.assertIn('translationKey', prompt)
        self.assertIn('FAA', prompt)

    def test_translation_key_is_stable_and_normalized(self) -> None:
        self.assertEqual(translation_key_for("PHAK", "ch01"), "phak-ch01")
        self.assertEqual(translation_key_for("WeightBalance", "ch03"), "weightbalance-ch03")

    def test_infer_title_uses_subject_context(self) -> None:
        self.assertEqual(infer_title_from_chapter("Weather", "ch01", "Meteorology", "stall recovery and wind"), "Meteorology — Chapter 1")
        self.assertEqual(infer_title_from_chapter("WeightBalance", "ch02", "Flight Performance and Planning", "weight and balance"), "Flight Performance and Planning — Chapter 2")

    def test_book_title_uses_the_actual_handbook_name(self) -> None:
        self.assertEqual(source_book_title("AFH"), "Airplane Flying Handbook")
        self.assertEqual(source_book_title("PHAK"), "Pilot's Handbook of Aeronautical Knowledge")
        self.assertEqual(source_book_title("WeightBalance"), "Aircraft Weight and Balance Handbook")

    def test_unknown_book_has_no_guessed_subject(self) -> None:
        with self.assertRaisesRegex(ValueError, "No display title"):
            source_book_title("UnknownBook")

    def test_english_guardrails_detect_non_english_text(self) -> None:
        self.assertTrue(contains_non_english_text("Ключові принципи і правила польотів"))
        self.assertFalse(contains_non_english_text("The four forces are lift, thrust, drag, and weight."))

    def test_read_time_estimate_is_reasonable(self) -> None:
        self.assertGreaterEqual(estimate_read_time_minutes("This chapter covers lift drag and stall in detail for student pilots."), 4)


if __name__ == "__main__":
    unittest.main()

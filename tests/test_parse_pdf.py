import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

import fitz

from scripts.parse_pdf import (
    clean_text_lines,
    collect_page_text,
    cleanup_stale_outputs,
    deduplicate_repeated_header_footer,
    detect_chapter_ranges,
    extract_chapter_title,
    extract_images_for_chapter,
    extract_layout_lines,
    find_book_output_collisions,
    infer_image_kind,
    load_appendix_ranges,
    load_chapter_overrides,
    load_chapter_ranges,
    load_section_ranges,
    main,
    open_pdf_document,
    parse_book,
    process_pdf_batch,
    publish_staged_outputs,
    validate_chapter_ranges,
)


class DetectChapterRangesTests(unittest.TestCase):
    def test_prefers_chapter_entries_over_nested_sections(self) -> None:
        doc = fitz.open()
        for _ in range(6):
            doc.new_page()
        doc.set_toc(
            [
                [1, "Chapter 1: Basics", 1],
                [2, "Section 1.1: Airframes", 2],
                [2, "Section 1.2: Systems", 3],
                [1, "Chapter 2: Flight", 4],
                [2, "Section 2.1: Control", 5],
            ]
        )

        try:
            self.assertEqual(detect_chapter_ranges(doc, doc.page_count), [(1, 3), (4, 6)])
        finally:
            doc.close()

    def test_applies_explicit_chapter_start_pages(self) -> None:
        doc = fitz.open()
        for _ in range(8):
            doc.new_page()

        try:
            self.assertEqual(detect_chapter_ranges(doc, 8, [2, 4, 7]), [(2, 3), (4, 6), (7, 8)])
        finally:
            doc.close()

    def test_applies_explicit_ranges_and_skips_pages_outside_chapters(self) -> None:
        doc = fitz.open()
        for _ in range(8):
            doc.new_page()

        try:
            self.assertEqual(
                detect_chapter_ranges(doc, doc.page_count, chapter_ranges=[(2, 3), (5, 7)]),
                [(2, 3), (5, 7)],
            )
        finally:
            doc.close()

    def test_rejects_overlapping_explicit_ranges(self) -> None:
        doc = fitz.open()
        for _ in range(5):
            doc.new_page()

        try:
            with self.assertRaisesRegex(ValueError, "cannot overlap"):
                detect_chapter_ranges(doc, doc.page_count, chapter_ranges=[(1, 3), (3, 5)])
        finally:
            doc.close()

    def test_excludes_front_and_back_matter_around_chapters(self) -> None:
        doc = fitz.open()
        for _ in range(10):
            doc.new_page()
        doc.set_toc(
            [
                [1, "Preface", 2],
                [1, "Table of Contents", 5],
                [1, "Chapter 1: Basics", 6],
                [1, "Chapter 2: Flight", 9],
                [1, "Glossary", 10],
            ]
        )

        try:
            self.assertEqual(detect_chapter_ranges(doc, doc.page_count), [(6, 8), (9, 9)])
        finally:
            doc.close()

    def test_rejects_chapter_start_outside_document(self) -> None:
        doc = fitz.open()
        doc.new_page()

        try:
            with self.assertRaisesRegex(ValueError, "between 1 and 1"):
                detect_chapter_ranges(doc, 1, [2])
        finally:
            doc.close()

    def test_rejects_gaps_between_chapter_ranges(self) -> None:
        with self.assertRaisesRegex(ValueError, "contiguous"):
            validate_chapter_ranges([(2, 3), (5, 7)], 7)

    def test_uses_shallowest_matching_level_without_chapter_entries(self) -> None:
        doc = fitz.open()
        for _ in range(5):
            doc.new_page()
        doc.set_toc(
            [
                [1, "Section 1: Weather", 1],
                [2, "Lesson 1.1: Clouds", 2],
                [1, "Section 2: Wind", 3],
                [2, "Lesson 2.1: Gusts", 4],
            ]
        )

        try:
            self.assertEqual(detect_chapter_ranges(doc, doc.page_count), [(1, 2), (3, 5)])
        finally:
            doc.close()

    def test_uses_printed_chapter_page_labels_instead_of_contents_entries(self) -> None:
        doc = fitz.open()
        doc.new_page().insert_text((72, 72), "Table of Contents\nChapter 1: Basics\nChapter 2: Flight")
        doc.new_page().insert_text((72, 72), "Chapter 2: Flight")
        doc.new_page().insert_text((72, 72), "1-1\nIntroduction\nChapter 1 material")
        doc.new_page().insert_text((72, 72), "Chapter 1 material continues")
        doc.new_page().insert_text((72, 72), "2-1\nIntroduction\nChapter 2 material")
        doc.new_page().insert_text((72, 72), "Chapter 2 material continues")

        try:
            self.assertEqual(detect_chapter_ranges(doc, doc.page_count), [(3, 4), (5, 6)])
        finally:
            doc.close()

    def test_uses_numbered_top_level_bookmarks_as_chapters(self) -> None:
        doc = fitz.open()
        for _ in range(7):
            doc.new_page()
        doc.set_toc(
            [
                [1, "1 Introduction", 2],
                [1, "2 Aviation Weather", 4],
                [2, "2.1 Forecasts", 5],
                [1, "A Appendix A", 6],
            ]
        )

        try:
            self.assertEqual(detect_chapter_ranges(doc, doc.page_count), [(2, 3), (4, 5)])
        finally:
            doc.close()

    def test_excludes_supplemental_pages_without_toc(self) -> None:
        doc = fitz.open()
        doc.new_page().insert_text((72, 72), "Chapter 1: Basics")
        doc.new_page().insert_text((72, 72), "Basic training principles")
        doc.new_page().insert_text((72, 72), "Chapter 2: Flight")
        doc.new_page().insert_text((72, 72), "Appendix A")

        try:
            self.assertEqual(detect_chapter_ranges(doc, doc.page_count), [(1, 2), (3, 3)])
        finally:
            doc.close()

    def test_excludes_lettered_appendix_without_heading(self) -> None:
        doc = fitz.open()
        doc.new_page().insert_text((72, 72), "Chapter 1: Basics")
        doc.new_page().insert_text((72, 72), "Chapter content")
        doc.new_page().insert_text((72, 72), "B-1\nAppendix material without a heading")
        doc.new_page().insert_text((72, 72), "More appendix material")

        try:
            self.assertEqual(detect_chapter_ranges(doc, doc.page_count), [(1, 2)])
        finally:
            doc.close()

    def test_does_not_treat_body_references_as_supplemental(self) -> None:
        doc = fitz.open()
        doc.new_page().insert_text((72, 72), "Chapter 1: Basics")
        doc.new_page().insert_text((72, 72), "References to medication usage are discussed in this chapter.")
        doc.new_page().insert_text((72, 72), "Chapter content continues.")

        try:
            self.assertEqual(detect_chapter_ranges(doc, doc.page_count), [(1, 3)])
        finally:
            doc.close()

    def test_requires_detectable_chapters_or_overrides(self) -> None:
        doc = fitz.open()
        doc.new_page().insert_text((72, 72), "General reference material")

        try:
            with self.assertRaisesRegex(ValueError, "No educational chapter starts detected"):
                detect_chapter_ranges(doc, doc.page_count)
        finally:
            doc.close()


class CleanTextLinesTests(unittest.TestCase):
    def test_preserves_numbered_content_labels(self) -> None:
        self.assertEqual(
            clean_text_lines(["Figure 1", "Table 2", "Page 4", "4", "1-2"], "Test Book"),
            ["Figure 1", "Table 2", "1-2"],
        )


class RepeatedHeaderFooterTests(unittest.TestCase):
    def test_removes_repeated_page_edge_text_but_keeps_body_text(self) -> None:
        doc = fitz.open()
        for page_number in range(3):
            page = doc.new_page()
            page.insert_text((72, 25), "Repeated Header")
            page.insert_text((72, 200), "Repeated Body")
            page.insert_text((72, 800), f"Footer {page_number}")

        try:
            page_text, edge_lines = collect_page_text(doc, "Test Book")
            cleaned = deduplicate_repeated_header_footer(page_text, edge_lines)
        finally:
            doc.close()

        for lines in cleaned.values():
            self.assertNotIn("Repeated Header", lines)
            self.assertIn("Repeated Body", lines)
        self.assertTrue(any("Footer 0" in lines for lines in cleaned.values()))


class LayoutExtractionTests(unittest.TestCase):
    def test_reads_two_columns_in_column_order(self) -> None:
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((60, 80), "Left column first")
        page.insert_text((320, 80), "Right column first")
        page.insert_text((60, 120), "Left column second")
        page.insert_text((320, 120), "Right column second")

        try:
            lines = [line[4] for line in extract_layout_lines(page)]
        finally:
            doc.close()

        self.assertEqual(
            lines,
            ["Left column first", "Left column second", "Right column first", "Right column second"],
        )

    def test_omits_text_inside_an_embedded_figure(self) -> None:
        doc = fitz.open()
        page = doc.new_page()
        pixmap = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 8, 8))
        pixmap.set_rect(fitz.IRect(0, 0, 8, 8), (220, 40, 40))
        page.insert_image(fitz.Rect(100, 100, 300, 300), stream=pixmap.tobytes("png"))
        page.insert_text((120, 150), "Figure label")
        page.insert_text((72, 350), "Figure caption")

        try:
            lines = [line[4] for line in extract_layout_lines(page)]
        finally:
            doc.close()

        self.assertNotIn("Figure label", lines)
        self.assertIn("Figure caption", lines)

    def test_keeps_text_over_a_full_page_image(self) -> None:
        doc = fitz.open()
        page = doc.new_page()
        pixmap = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 8, 8))
        pixmap.set_rect(fitz.IRect(0, 0, 8, 8), (220, 40, 40))
        page.insert_image(page.rect, stream=pixmap.tobytes("png"))
        page.insert_text((72, 100), "Recognized page text")

        try:
            lines = [line[4] for line in extract_layout_lines(page)]
        finally:
            doc.close()

        self.assertIn("Recognized page text", lines)


class ChapterTitleExtractionTests(unittest.TestCase):
    def test_extracts_inline_chapter_title(self) -> None:
        self.assertEqual(
            extract_chapter_title(["Chapter 2: Ground Operations", "Introduction"], 2),
            "Ground Operations",
        )

    def test_extracts_multiline_chapter_title_and_skips_duplicates(self) -> None:
        self.assertEqual(
            extract_chapter_title(
                ["Chapter 1", "The National", "The National", "Airspace System", "Airspace System", "Introduction"],
                1,
            ),
            "The National Airspace System",
        )


class ExtractImagesTests(unittest.TestCase):
    def test_deduplicates_reused_image_and_records_placements(self) -> None:
        doc = fitz.open()
        pixmap = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 8, 8))
        pixmap.set_rect(fitz.IRect(0, 0, 8, 8), (220, 40, 40))
        image_bytes = pixmap.tobytes("png")
        for _ in range(2):
            page = doc.new_page()
            page.insert_image(fitz.Rect(72, 120, 160, 208), stream=image_bytes)

        try:
            with TemporaryDirectory() as directory:
                images = extract_images_for_chapter(doc, Path(directory), "TestBook", "ch01", 1, 2)
                self.assertEqual(len(images), 1)
                self.assertEqual([item["page"] for item in images[0]["placements"]], [1, 2])
                self.assertTrue((Path(directory) / images[0]["file"]).is_file())
        finally:
            doc.close()


class OpenPdfDocumentTests(unittest.TestCase):
    def test_reports_corrupt_pdf_path(self) -> None:
        with TemporaryDirectory() as directory:
            pdf_path = Path(directory) / "corrupt.pdf"
            pdf_path.write_bytes(b"not a PDF")

            with self.assertRaisesRegex(ValueError, "Unable to open PDF"):
                with open_pdf_document(pdf_path):
                    self.fail("Corrupt PDF should not be opened")

    def test_rejects_empty_pdf(self) -> None:
        empty_doc = Mock(is_encrypted=False, page_count=0)
        with patch("scripts.parse_pdf.fitz.open", return_value=empty_doc):
            with self.assertRaisesRegex(ValueError, "contains no pages"):
                with open_pdf_document(Path("empty.pdf")):
                    self.fail("Empty PDF should not be parsed")
        empty_doc.close.assert_called_once()


class OriginalTextIntegrityTests(unittest.TestCase):
    def test_preserves_original_words_and_ignores_page_numbers(self) -> None:
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Chapter 1: Basics")
        page.insert_text((72, 110), "Aviation study text")
        page.insert_text((72, 760), "Page 1")

        try:
            page_text, _ = collect_page_text(doc, "Test Book")
        finally:
            doc.close()

        self.assertEqual(page_text[1], ["Chapter 1: Basics", "Aviation study text"])

    def test_classifies_figure_and_table_captions(self) -> None:
        self.assertEqual(infer_image_kind("Figure 3.1 Wake turbulence"), "figure")
        self.assertEqual(infer_image_kind("Table 2.1 Required airspeeds"), "table")
        self.assertEqual(infer_image_kind("Unlabeled illustration"), "figure")
        self.assertEqual(infer_image_kind("Diagram of the fuel system"), "figure")


class ParallelBatchTests(unittest.TestCase):
    def test_processes_multiple_books_in_a_worker_pool(self) -> None:
        pdf_files = [Path("library/BookA/one.pdf"), Path("library/BookB/two.pdf")]
        calls = []

        def fake_parse_book(pdf_path, output_root, public_images_root, **kwargs):
            calls.append((pdf_path, kwargs.get("chapter_starts")))
            return {"chapters": [{"startPage": 1, "endPage": 1, "images": []}]}

        with patch("scripts.parse_pdf.parse_book", side_effect=fake_parse_book):
            with patch("scripts.parse_pdf.ThreadPoolExecutor") as mock_executor:
                executor = Mock()
                executor.__enter__ = Mock(return_value=executor)
                executor.__exit__ = Mock(return_value=False)

                def submit_side_effect(fn, *args, **kwargs):
                    result = fn(*args, **kwargs)
                    return Mock(result=lambda: result)

                executor.submit.side_effect = submit_side_effect
                mock_executor.return_value = executor

                process_pdf_batch(pdf_files, Path("/tmp/out"), Path("/tmp/images"), chapter_overrides={}, workers=2)

        self.assertEqual(len(calls), 2)
        self.assertEqual(sorted(str(path) for path, _ in calls), ["library/BookA/one.pdf", "library/BookB/two.pdf"])


class SkipWithoutChapterManifestTests(unittest.TestCase):
    def test_skips_books_without_a_chapter_manifest(self) -> None:
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            root = Path(directory)
            source_dir = root / "UnconfiguredBook"
            source_dir.mkdir()
            pdf_path = source_dir / "source.pdf"
            doc = fitz.open()
            page = doc.new_page()
            page.insert_text((72, 72), "Chapter 1: Basics")
            page.insert_text((72, 100), "Aviation study text")
            doc.save(pdf_path)
            doc.close()

            results = process_pdf_batch([pdf_path], root / "parsed", root / "images", {}, workers=1)
            self.assertEqual(results, [])
            self.assertFalse((root / "parsed" / "UnconfiguredBook").exists())


class OverrideAndIdentityTests(unittest.TestCase):
    def test_loads_per_book_chapter_overrides(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "chapter_overrides.json"
            path.write_text('{"Air Flight Handbook": [1, 12, 24]}', encoding="utf-8")
            self.assertEqual(load_chapter_overrides(path), {"Air_Flight_Handbook": [1, 12, 24]})

    def test_loads_explicit_chapter_ranges_from_sidecar(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "chapters.json"
            path.write_text('{"chapters": [{"startPage": 2, "endPage": 8}]}', encoding="utf-8")
            self.assertEqual(load_chapter_ranges(path), [(2, 8)])

    def test_loads_optional_section_ranges_from_sidecar(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "chapters.json"
            path.write_text(
                '{"glossary": {"startPage": 9, "endPage": 10}, "acronyms": null, '
                '"emergencyProcedures": {"startPage": 11, "endPage": 12}}',
                encoding="utf-8",
            )
            self.assertEqual(
                load_section_ranges(path),
                {"glossary": (9, 10), "emergencyProcedures": (11, 12)},
            )

    def test_loads_named_appendices_and_preserves_their_names(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "chapters.json"
            path.write_text(
                '{"appendices": [{"name": "Appendix A - Flight Plan Shorthand", '
                '"startPage": 10, "endPage": 11}]}',
                encoding="utf-8",
            )
            self.assertEqual(
                load_appendix_ranges(path),
                [{
                    "name": "Appendix A - Flight Plan Shorthand",
                    "key": "appendix-a-flight-plan-shorthand",
                    "startPage": 10,
                    "endPage": 11,
                }],
            )

    def test_detects_pdfs_sharing_an_output_folder(self) -> None:
        collisions = find_book_output_collisions(
            [Path("library/Book/first.pdf"), Path("library/Book/second.pdf"), Path("library/Other/book.pdf")]
        )
        self.assertEqual(collisions, {"Book": [Path("library/Book/first.pdf"), Path("library/Book/second.pdf")]})


class CleanupStaleOutputsTests(unittest.TestCase):
    def test_removes_only_manifested_stale_outputs(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            book_dir = root / "parsed" / "TestBook"
            image_book_dir = root / "images" / "TestBook"
            old_chapter_dir = book_dir / "ch02"
            old_image_dir = image_book_dir / "ch02"
            active_image_dir = image_book_dir / "ch01"
            old_acronyms_dir = book_dir / "sections" / "acronyms"
            active_glossary_dir = book_dir / "sections" / "glossary"
            old_appendix_dir = book_dir / "appendices" / "appendix-a-old-reference"
            active_appendix_dir = book_dir / "appendices" / "appendix-b-current-reference"
            old_chapter_dir.mkdir(parents=True)
            old_image_dir.mkdir(parents=True)
            active_image_dir.mkdir(parents=True)
            old_acronyms_dir.mkdir(parents=True)
            active_glossary_dir.mkdir(parents=True)
            old_appendix_dir.mkdir(parents=True)
            active_appendix_dir.mkdir(parents=True)
            (old_chapter_dir / "content_raw.txt").write_text("old generated text", encoding="utf-8")
            (old_chapter_dir / "custom.txt").write_text("keep", encoding="utf-8")
            (old_image_dir / "img_p2_1.png").write_bytes(b"stale")
            (old_image_dir / "custom.png").write_bytes(b"keep")
            (active_image_dir / "img_p1_2.png").write_bytes(b"stale")
            (old_acronyms_dir / "content.md").write_text("stale section", encoding="utf-8")
            (old_acronyms_dir / "custom.md").write_text("keep", encoding="utf-8")
            (active_glossary_dir / "content.md").write_text("current section", encoding="utf-8")
            (old_appendix_dir / "content.md").write_text("stale appendix", encoding="utf-8")
            (active_appendix_dir / "content.md").write_text("current appendix", encoding="utf-8")

            previous = {
                "chapters": [
                    {"chapter": "ch01", "images": [{"file": "img_p1_2.png"}]},
                    {"chapter": "ch02", "images": [{"file": "img_p2_1.png"}]},
                ],
                "sections": {"acronyms": {}, "glossary": {}},
                "appendices": [{"key": "appendix-a-old-reference"}],
            }
            current = {
                "chapters": [{"chapter": "ch01", "images": [{"file": "img_p1_1.png"}]}],
                "sections": {"glossary": {}},
                "appendices": [{"key": "appendix-b-current-reference"}],
            }

            cleanup_stale_outputs(book_dir, image_book_dir, previous, current)

            self.assertFalse((active_image_dir / "img_p1_2.png").exists())
            self.assertFalse((old_chapter_dir / "content_raw.txt").exists())
            self.assertTrue((old_chapter_dir / "custom.txt").exists())
            self.assertFalse((old_image_dir / "img_p2_1.png").exists())
            self.assertTrue((old_image_dir / "custom.png").exists())
            self.assertFalse((old_acronyms_dir / "content.md").exists())
            self.assertTrue((old_acronyms_dir / "custom.md").exists())
            self.assertTrue((active_glossary_dir / "content.md").is_file())
            self.assertFalse((old_appendix_dir / "content.md").exists())
            self.assertTrue((active_appendix_dir / "content.md").is_file())


class PublishStagedOutputsTests(unittest.TestCase):
    def test_publishes_new_files_and_keeps_untracked_files(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            staged_book = root / "staged-book"
            staged_images = root / "staged-images"
            output_book = root / "output-book"
            output_images = root / "output-images"
            for path in (staged_book / "ch01", staged_images / "ch01", output_book / "ch01"):
                path.mkdir(parents=True)
            (staged_book / "ch01" / "content_raw.txt").write_text("new", encoding="utf-8")
            (staged_book / "book_manifest.json").write_text("{}", encoding="utf-8")
            (staged_images / "ch01" / "img_p1_1.png").write_bytes(b"image")
            (output_book / "ch01" / "custom.txt").write_text("keep", encoding="utf-8")

            publish_staged_outputs(staged_book, staged_images, output_book, output_images)

            self.assertEqual((output_book / "ch01" / "content_raw.txt").read_text(encoding="utf-8"), "new")
            self.assertTrue((output_book / "book_manifest.json").is_file())
            self.assertEqual((output_book / "ch01" / "custom.txt").read_text(encoding="utf-8"), "keep")
            self.assertEqual((output_images / "ch01" / "img_p1_1.png").read_bytes(), b"image")

    def test_rolls_back_replacements_when_publish_fails(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            staged_book = root / "staged-book"
            staged_images = root / "staged-images"
            output_book = root / "output-book"
            output_images = root / "output-images"
            (staged_book / "ch01").mkdir(parents=True)
            (staged_images / "ch01").mkdir(parents=True)
            (output_book / "ch01").mkdir(parents=True)
            (output_images / "ch01").mkdir(parents=True)
            (staged_book / "ch01" / "content_raw.txt").write_text("new", encoding="utf-8")
            (staged_book / "ch01" / "images_manifest.json").write_text("{}", encoding="utf-8")
            (staged_images / "ch01" / "img_p1_1.png").write_bytes(b"new image")
            (output_book / "ch01" / "content_raw.txt").write_text("old", encoding="utf-8")
            (output_images / "ch01" / "img_p1_1.png").write_bytes(b"old image")
            (output_book / "ch01" / "images_manifest.json").symlink_to(root / "missing-target")

            with self.assertRaisesRegex(ValueError, "symlink output"):
                publish_staged_outputs(staged_book, staged_images, output_book, output_images)

            self.assertEqual((output_book / "ch01" / "content_raw.txt").read_text(encoding="utf-8"), "old")
            self.assertEqual((output_images / "ch01" / "img_p1_1.png").read_bytes(), b"old image")


class ParseBookIntegrationTests(unittest.TestCase):
    def test_stages_and_publishes_a_complete_book(self) -> None:
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            root = Path(directory)
            source_dir = root / "TestBook"
            source_dir.mkdir()
            pdf_path = source_dir / "source.pdf"
            doc = fitz.open()
            page = doc.new_page()
            page.insert_text((72, 72), "Chapter 1: Basics")
            page.insert_text((72, 100), "Aviation study text")
            doc.save(pdf_path)
            doc.close()
            (source_dir / "chapters.json").write_text(
                '{"chapters": [{"number": 1, "startPage": 1, "endPage": 1}]}',
                encoding="utf-8",
            )

            output_root = root / "parsed"
            images_root = root / "images"
            manifest = parse_book(pdf_path, output_root, images_root)

            self.assertEqual(len(manifest["chapters"]), 1)
            self.assertEqual(manifest["chapters"][0]["title"], "Basics")
            self.assertEqual(
                (output_root / "TestBook" / "ch01" / "content.md").read_text(encoding="utf-8"),
                "Chapter 1: Basics\nAviation study text",
            )
            self.assertFalse((output_root / "TestBook" / "ch01" / "content_raw.txt").exists())
            self.assertTrue((output_root / "TestBook" / "book_manifest.json").is_file())
            self.assertEqual(list(output_root.glob(".TestBook-parse-*")), [])
            self.assertEqual(list(images_root.glob(".TestBook-images-*")), [])

    def test_uses_per_book_configured_ranges(self) -> None:
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            root = Path(directory)
            source_dir = root / "ConfiguredBook"
            source_dir.mkdir()
            pdf_path = source_dir / "source.pdf"
            doc = fitz.open()
            for index in range(5):
                doc.new_page().insert_text((72, 72), f"Page {index + 1} content")
            doc.save(pdf_path)
            doc.close()
            (source_dir / "chapters.json").write_text(
                '{"version": 1, "chapters": [{"number": 1, "startPage": 2, "endPage": 3}, '
                '{"number": 2, "startPage": 5, "endPage": 5}]}',
                encoding="utf-8",
            )

            output_root = root / "parsed"
            manifest = parse_book(pdf_path, output_root, root / "images")

            self.assertEqual(
                [(chapter["startPage"], chapter["endPage"]) for chapter in manifest["chapters"]],
                [(2, 3), (5, 5)],
            )
            self.assertEqual(
                (output_root / "ConfiguredBook" / "ch01" / "content.md").read_text(encoding="utf-8"),
                "Page 2 content\n\nPage 3 content",
            )

    def test_parses_glossary_acronyms_and_emergency_procedures_separately(self) -> None:
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            root = Path(directory)
            source_dir = root / "ConfiguredBook"
            source_dir.mkdir()
            pdf_path = source_dir / "source.pdf"
            doc = fitz.open()
            page_texts = [
                "Chapter 1: Basics\nChapter lesson content",
                "More chapter lesson content",
                "Glossary terminology",
                "Acronym definitions",
                "Emergency procedure steps",
                "Appendix A reference content",
            ]
            for text in page_texts:
                doc.new_page().insert_text((72, 72), text)
            doc.save(pdf_path)
            doc.close()
            (source_dir / "chapters.json").write_text(
                '{"chapters": [{"number": 1, "startPage": 1, "endPage": 2}], '
                '"glossary": {"startPage": 3, "endPage": 3}, '
                '"acronyms": {"startPage": 4, "endPage": 4}, '
                '"emergencyProcedures": {"startPage": 5, "endPage": 5}, '
                '"appendices": [{"name": "Appendix A - Reference Material", '
                '"startPage": 6, "endPage": 6}]}',
                encoding="utf-8",
            )

            output_root = root / "parsed"
            manifest = parse_book(pdf_path, output_root, root / "images")
            sections = manifest["sections"]

            self.assertEqual(set(sections), {"glossary", "acronyms", "emergencyProcedures"})
            appendix = manifest["appendices"][0]
            self.assertEqual(appendix["name"], "Appendix A - Reference Material")
            appendix_path = output_root / "ConfiguredBook" / appendix["contentPath"]
            self.assertEqual(appendix_path.read_text(encoding="utf-8"), "Appendix A reference content")
            for section_type, expected_text in (
                ("glossary", "Glossary terminology"),
                ("acronyms", "Acronym definitions"),
                ("emergencyProcedures", "Emergency procedure steps"),
            ):
                section_path = output_root / "ConfiguredBook" / sections[section_type]["contentPath"]
                self.assertEqual(section_path.read_text(encoding="utf-8"), expected_text)

    def test_skips_reparsing_when_pdf_hash_is_unchanged(self) -> None:
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            root = Path(directory)
            source_dir = root / "TestBook"
            source_dir.mkdir()
            pdf_path = source_dir / "source.pdf"
            doc = fitz.open()
            page = doc.new_page()
            page.insert_text((72, 72), "Chapter 1: Basics")
            page.insert_text((72, 100), "Aviation study text")
            doc.save(pdf_path)
            doc.close()
            (source_dir / "chapters.json").write_text(
                '{"chapters": [{"number": 1, "startPage": 1, "endPage": 1}]}',
                encoding="utf-8",
            )

            output_root = root / "parsed"
            images_root = root / "images"
            first_manifest = parse_book(pdf_path, output_root, images_root)
            second_manifest = parse_book(pdf_path, output_root, images_root)

            self.assertEqual(first_manifest, second_manifest)
            self.assertTrue((output_root / "TestBook" / "book_manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
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
    extract_images_for_chapter,
    extract_layout_lines,
    find_book_output_collisions,
    infer_image_kind,
    load_chapter_overrides,
    load_chapter_ranges,
    main,
    needs_ocr_retry,
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


class OcrQualityTests(unittest.TestCase):
    def test_marks_sparse_pages_for_ocr_retry(self) -> None:
        self.assertTrue(needs_ocr_retry(["Figure 1", "Page 3"]))
        self.assertFalse(
            needs_ocr_retry([
                "Introduction",
                "This page contains real explanatory text about aircraft control and attitude instrument flying.",
            ])
        )

    def test_retries_ocr_when_initial_extract_is_sparse(self) -> None:
        doc = fitz.open()
        doc.new_page().insert_text((72, 72), "Aviation study text")

        with patch("scripts.parse_pdf.create_ocr_textpage", side_effect=[None, Mock()]) as create_ocr:
            with patch("scripts.parse_pdf.extract_layout_lines", side_effect=[[(0, 0, 10, 10, "Figure 1")], [(0, 0, 10, 10, "Aviation study text")]]):
                page_text, _ = collect_page_text(doc, "Test Book", ocr=True, ocr_language="eng", ocr_dpi=300)

        self.assertEqual(page_text[1], ["Aviation study text"])
        self.assertEqual(create_ocr.call_count, 2)

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


class OcrCliTests(unittest.TestCase):
    def test_requires_tesseract_when_ocr_is_requested(self) -> None:
        with patch("scripts.parse_pdf.sys.argv", ["parse_pdf.py", "--ocr"]):
            with patch("scripts.parse_pdf.shutil.which", return_value=None):
                with self.assertRaisesRegex(SystemExit, "requires the Tesseract executable"):
                    main()

    def test_uses_configured_worker_count(self) -> None:
        with patch("scripts.parse_pdf.sys.argv", ["parse_pdf.py", "--workers", "8"]):
            with patch("scripts.parse_pdf.iter_pdf_files", return_value=[Path("library/BookA/sample.pdf")]):
                with patch("scripts.parse_pdf.process_pdf_batch") as process_batch:
                    process_batch.return_value = []
                    with patch("scripts.parse_pdf.shutil.which", return_value="/usr/bin/tesseract"):
                        main()

        self.assertEqual(process_batch.call_args.kwargs["workers"], 1)

    def test_uses_configured_retry_dpi(self) -> None:
        with patch("scripts.parse_pdf.sys.argv", ["parse_pdf.py", "--ocr", "--ocr-retry-dpi", "600"]):
            with patch("scripts.parse_pdf.shutil.which", return_value="/usr/bin/tesseract"):
                with patch("scripts.parse_pdf.iter_pdf_files", return_value=[Path("library/BookA/sample.pdf")]):
                    with patch("scripts.parse_pdf.process_pdf_batch") as process_batch:
                        process_batch.return_value = []
                        main()

        self.assertEqual(process_batch.call_args.kwargs["ocr_retry_dpi"], 600)


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
            old_chapter_dir.mkdir(parents=True)
            old_image_dir.mkdir(parents=True)
            active_image_dir.mkdir(parents=True)
            (old_chapter_dir / "content_raw.txt").write_text("old generated text", encoding="utf-8")
            (old_chapter_dir / "custom.txt").write_text("keep", encoding="utf-8")
            (old_image_dir / "img_p2_1.png").write_bytes(b"stale")
            (old_image_dir / "custom.png").write_bytes(b"keep")
            (active_image_dir / "img_p1_2.png").write_bytes(b"stale")

            previous = {
                "chapters": [
                    {"chapter": "ch01", "images": [{"file": "img_p1_2.png"}]},
                    {"chapter": "ch02", "images": [{"file": "img_p2_1.png"}]},
                ]
            }
            current = {"chapters": [{"chapter": "ch01", "images": [{"file": "img_p1_1.png"}]}]}

            cleanup_stale_outputs(book_dir, image_book_dir, previous, current)

            self.assertFalse((active_image_dir / "img_p1_2.png").exists())
            self.assertFalse((old_chapter_dir / "content_raw.txt").exists())
            self.assertTrue((old_chapter_dir / "custom.txt").exists())
            self.assertFalse((old_image_dir / "img_p2_1.png").exists())
            self.assertTrue((old_image_dir / "custom.png").exists())


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

            output_root = root / "parsed"
            images_root = root / "images"
            manifest = parse_book(pdf_path, output_root, images_root)

            self.assertEqual(len(manifest["chapters"]), 1)
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

            output_root = root / "parsed"
            images_root = root / "images"
            first_manifest = parse_book(pdf_path, output_root, images_root)
            second_manifest = parse_book(pdf_path, output_root, images_root)

            self.assertEqual(first_manifest, second_manifest)
            self.assertTrue((output_root / "TestBook" / "book_manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
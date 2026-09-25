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
    load_chapter_overrides,
    main,
    open_pdf_document,
    parse_book,
    publish_staged_outputs,
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
            self.assertEqual(detect_chapter_ranges(doc, 8, [1, 4, 7]), [(1, 3), (4, 6), (7, 8)])
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


class OcrCliTests(unittest.TestCase):
    def test_requires_tesseract_when_ocr_is_requested(self) -> None:
        with patch("scripts.parse_pdf.sys.argv", ["parse_pdf.py", "--ocr"]):
            with patch("scripts.parse_pdf.shutil.which", return_value=None):
                with self.assertRaisesRegex(SystemExit, "requires the Tesseract executable"):
                    main()


class OverrideAndIdentityTests(unittest.TestCase):
    def test_loads_per_book_chapter_overrides(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "chapter_overrides.json"
            path.write_text('{"Air Flight Handbook": [1, 12, 24]}', encoding="utf-8")
            self.assertEqual(load_chapter_overrides(path), {"Air_Flight_Handbook": [1, 12, 24]})

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
            doc.new_page().insert_text((72, 72), "Aviation study text")
            doc.save(pdf_path)
            doc.close()

            output_root = root / "parsed"
            images_root = root / "images"
            manifest = parse_book(pdf_path, output_root, images_root)

            self.assertEqual(len(manifest["chapters"]), 1)
            self.assertEqual(
                (output_root / "TestBook" / "ch01" / "content_raw.txt").read_text(encoding="utf-8"),
                "Aviation study text",
            )
            self.assertTrue((output_root / "TestBook" / "book_manifest.json").is_file())
            self.assertEqual(list(output_root.glob(".TestBook-parse-*")), [])
            self.assertEqual(list(images_root.glob(".TestBook-images-*")), [])


if __name__ == "__main__":
    unittest.main()
import json
import unittest
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import fitz

from scripts.parser_library import (
    extract_page,
    download_pdf,
    filter_books,
    key_value_from_lines,
    load_config,
    process_book,
    span_is_in_table,
    validate_book_config,
)


class ConfigValidationTests(unittest.TestCase):
    def test_rejects_path_traversal_book_ids(self) -> None:
        with self.assertRaisesRegex(ValueError, "Invalid book_id"):
            validate_book_config(
                {
                    "book_id": "../unsafe",
                    "pdf_url": "https://example.test/book.pdf",
                    "boundaries": [{"type": "chapter", "title": "One", "start_page": 1, "end_page": 1}],
                }
            )

    def test_rejects_page_zero(self) -> None:
        with self.assertRaisesRegex(ValueError, "valid 1-based"):
            validate_book_config(
                {
                    "book_id": "book",
                    "title": "Book",
                    "pdf_url": "https://example.test/book.pdf",
                    "pdf_path": "resources/library/book/book.pdf",
                    "boundaries": [{"type": "chapter", "title": "One", "start_page": 0, "end_page": 1}],
                }
            )

    def test_rejects_json_array(self) -> None:
        with TemporaryDirectory() as directory:
            config_path = Path(directory) / "config.json"
            config_path.write_text(
                json.dumps(
                    [{
                        "book_id": "book",
                        "title": "Book",
                        "pdf_url": "https://example.test/book.pdf",
                        "pdf_path": "resources/library/book/book.pdf",
                        "boundaries": [
                            {"type": "chapter", "title": "One", "start_page": 1, "end_page": 1}
                        ],
                    }]
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "version 1 library manifest"):
                load_config(config_path)

    def test_loads_versioned_library_manifest(self) -> None:
        with TemporaryDirectory() as directory:
            manifest_path = Path(directory) / "library_manifest.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "books": [
                            {
                                "book_id": "book",
                                "title": "Book",
                                "pdf_url": "https://example.test/book.pdf",
                                "pdf_path": "resources/library/book/book.pdf",
                                "sha256": "abc123",
                                "boundaries": [
                                    {
                                        "type": "chapter",
                                        "title": "Chapter 1",
                                        "start_page": 1,
                                        "end_page": 2,
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            book = load_config(manifest_path)[0]
            self.assertEqual(book["pdf_path"], "resources/library/book/book.pdf")
            self.assertEqual(book["boundaries"][0]["end_page"], 2)

    def test_repository_library_manifest_contains_merged_sections_and_download_metadata(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        books = load_config(repo_root / "resources/library/library_manifest.json")
        self.assertEqual(len(books), 11)
        afh = next(book for book in books if book["book_id"] == "AFH")
        self.assertEqual(afh["title"], "Airplane Flying Handbook")
        self.assertEqual(afh["pdf_url"], "https://www.faa.gov/sites/faa.gov/files/regulations_policies/handbooks_manuals/aviation/airplane_handbook/00_afh_full.pdf")
        self.assertEqual(afh["pdf_path"], "resources/library/AFH/AFH.pdf")
        self.assertEqual(
            afh["boundaries"][0],
            {
                "type": "chapter",
                "title": "Chapter 1",
                "start_page": 22,
                "end_page": 37,
            },
        )
        instructor = next(book for book in books if book["book_id"] == "Instructor")
        self.assertIn("lastModified", instructor)
        self.assertTrue(any(
            boundary["type"] == "glossary"
            for book in books
            for boundary in book["boundaries"]
        ))

    def test_filters_book_ids_case_insensitively_and_trims_whitespace(self) -> None:
        books = [
            {"book_id": "AFH", "title": "Airplane Flying Handbook", "pdf_url": "https://example.test/afh.pdf", "pdf_path": "resources/library/AFH/AFH.pdf", "boundaries": [{"type": "chapter", "title": "Chapter 1", "start_page": 1, "end_page": 1}]},
            {"book_id": "PHAK", "title": "Pilot's Handbook", "pdf_url": "https://example.test/phak.pdf", "pdf_path": "resources/library/PHAK/PHAK.pdf", "boundaries": [{"type": "chapter", "title": "Chapter 1", "start_page": 1, "end_page": 1}]},
        ]
        filtered = filter_books(books, [" afh ", "PHAK"])
        self.assertEqual([book["book_id"] for book in filtered], ["AFH", "PHAK"])

    def test_download_retries_timeout_and_streams_response(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory) / "book.pdf"
            with (
                patch(
                    "scripts.parser_library.urlopen",
                    side_effect=[TimeoutError("slow response"), BytesIO(b"%PDF-1.7\nsample")],
                ) as open_url,
                patch("scripts.parser_library.time.sleep") as sleep,
            ):
                download_pdf("https://example.test/book.pdf", target, timeout=1, retries=1)

            self.assertEqual(target.read_bytes(), b"%PDF-1.7\nsample")
            self.assertEqual(open_url.call_count, 2)
            sleep.assert_called_once_with(1)


class ExtractionTests(unittest.TestCase):
    def test_detects_span_center_inside_table(self) -> None:
        self.assertTrue(
            span_is_in_table(
                fitz.Rect(8, 8, 12, 12),
                [fitz.Rect(0, 0, 11, 11)],
            )
        )

    def test_extracts_style_columns_and_skips_page_edges(self) -> None:
        doc = fitz.open()
        page = doc.new_page(width=600, height=800)
        page.insert_text((40, 25), "Running header")
        page.insert_text((40, 100), "Left first", fontname="hebo", color=(1, 0, 0))
        page.insert_text((320, 100), "Right first")
        page.insert_text((40, 130), "Left second")
        page.insert_text((40, 780), "Running footer")
        try:
            with TemporaryDirectory() as directory:
                elements, _ = extract_page(
                    page, "book", 1, Path(directory) / "images"
                )
        finally:
            doc.close()

        texts = [item["text"] for item in elements if item["type"] == "text"]
        self.assertEqual(texts, ["Left first", "Left second", "Right first"])
        self.assertTrue(elements[0]["is_bold"])
        self.assertEqual(elements[0]["font_name"], "Helvetica-Bold")
        self.assertRegex(elements[0]["color"], r"^#[0-9A-F]{6}$")
        self.assertEqual(len(elements[0]["bbox"]), 4)

    def test_cleans_word_split_at_line_boundary(self) -> None:
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 100), "navi-")
        page.insert_text((72, 120), "gation")
        try:
            elements, _ = extract_page(page, "book", 1)
        finally:
            doc.close()
        self.assertEqual([item["text"] for item in elements if item["type"] == "text"], ["navigation"])

    def test_extracts_tables_without_duplicating_cell_text(self) -> None:
        doc = fitz.open()
        page = doc.new_page(width=600, height=800)
        for y in (100, 130, 160):
            page.draw_line((50, y), (400, y), width=1)
        for x in (50, 200, 400):
            page.draw_line((x, 100), (x, 160), width=1)
        page.insert_text((60, 120), "Class")
        page.insert_text((210, 120), "Rules")
        page.insert_text((60, 150), "A")
        page.insert_text((210, 150), "IFR Only")
        try:
            elements, _ = extract_page(page, "book", 1)
        finally:
            doc.close()

        tables = [item for item in elements if item["type"] == "table"]
        text = [item["text"] for item in elements if item["type"] == "text"]
        self.assertEqual(tables[0]["data"], [["Class", "Rules"], ["A", "IFR Only"]])
        self.assertEqual(text, [])

    def test_parses_glossary_and_acronym_key_value_lines(self) -> None:
        lines = [
            {"elements": [{"text": "QNH - Altimeter setting", "is_bold": False}]},
            {"elements": [{"text": "VFR", "is_bold": True}, {"text": "Visual Flight Rules", "is_bold": False}]},
        ]
        self.assertEqual(
            key_value_from_lines(lines, "Abbreviations"),
            {"QNH": "Altimeter setting", "VFR": "Visual Flight Rules"},
        )

    def test_process_book_writes_output_shape_and_image_bbox(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.pdf"
            output_root = root / "output"
            image_root = root / "public" / "images"
            doc = fitz.open()
            page = doc.new_page(width=600, height=800)
            page.insert_text((72, 100), "Chapter content")
            pixmap = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 8, 8))
            pixmap.set_rect(fitz.IRect(0, 0, 8, 8), (220, 40, 40))
            page.insert_image(fitz.Rect(70, 150, 200, 250), stream=pixmap.tobytes("png"))
            doc.save(source)
            doc.close()

            config = {
                "book_id": "book",
                "title": "Book",
                "pdf_url": "https://example.test/book.pdf",
                "pdf_path": str(root / "library" / "book.pdf"),
                "boundaries": [
                    {"type": "chapter", "title": "Chapter 1", "start_page": 1, "end_page": 1},
                    {"type": "glossary", "title": "Glossary", "start_page": 1, "end_page": 1},
                ],
            }

            def copy_fixture(_url: str, target: Path, _timeout: float, _retries: int) -> None:
                del _url, _timeout, _retries
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())

            with patch("scripts.parser_library.download_pdf", side_effect=copy_fixture):
                output_path = process_book(config, output_root, image_root=image_root)

            manifest = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(output_path.name, "parser_manifest.json")
            self.assertEqual(manifest["book_id"], "book")
            self.assertEqual(manifest["title"], "Book")
            self.assertEqual(manifest["pdf_path"], config["pdf_path"])
            self.assertEqual(manifest["sections"][0]["content_path"], "ch01.json")

            section_path = output_root / "book" / manifest["sections"][0]["content_path"]
            output = json.loads(section_path.read_text(encoding="utf-8"))
            page_data = output["section"]["pages"][0]
            image = next(item for item in page_data["elements"] if item["type"] == "image")
            self.assertEqual(output["book_id"], "book")
            self.assertEqual(output["book_title"], "Book")
            self.assertEqual(output["pdf_path"], config["pdf_path"])
            self.assertEqual(Path(config["pdf_path"]).read_bytes(), source.read_bytes())
            self.assertEqual(page_data["page_number"], 1)
            self.assertEqual(image["bbox"], [70.0, 150.0, 200.0, 250.0])
            self.assertEqual(image["image_path"], "/images/book_p1_b1.png")
            self.assertTrue((image_root / "book_p1_b1.png").is_file())
            self.assertEqual(manifest["sections"][1]["content_path"], "section_002_glossary.json")
            glossary_path = output_root / "book" / manifest["sections"][1]["content_path"]
            glossary = json.loads(glossary_path.read_text(encoding="utf-8"))
            self.assertEqual(glossary["section"]["title"], "Glossary")
            self.assertEqual(len(glossary["section"]["images"]), 1)

            second_config = {
                **config,
                "book_id": "book-two",
                "pdf_path": str(root / "library" / "book-two.pdf"),
            }
            with patch("scripts.parser_library.download_pdf", side_effect=copy_fixture):
                second_output_path = process_book(second_config, output_root, image_root=image_root)
            second_manifest = json.loads(second_output_path.read_text(encoding="utf-8"))
            second_section_path = output_root / "book-two" / second_manifest["sections"][0]["content_path"]
            second_content = json.loads(second_section_path.read_text(encoding="utf-8"))
            second_image = second_content["section"]["pages"][0]["elements"][1]
            self.assertEqual(second_image["image_path"], "/images/book-two_p1_b1.png")
            self.assertTrue((image_root / "book-two_p1_b1.png").is_file())


if __name__ == "__main__":
    unittest.main()

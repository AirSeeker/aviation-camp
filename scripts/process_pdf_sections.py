#!/usr/bin/env python3
"""Download configured aviation PDFs and extract their sections as structured JSON."""

from __future__ import annotations

import argparse
import http.client
import json
import logging
import re
import time
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

import fitz

LOGGER = logging.getLogger("process_pdf_sections")
DOWNLOAD_CHUNK_SIZE = 1024 * 1024
HEADER_FOOTER_FRACTION = 0.05


def safe_book_id(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("book_id must be a non-empty string.")
    if value in {".", ".."} or Path(value).name != value or not re.fullmatch(r"[A-Za-z0-9._-]+", value):
        raise ValueError(f"Invalid book_id {value!r}; use letters, numbers, '.', '_' or '-'.")
    return value


def validate_book_config(config: Any) -> dict[str, Any]:
    if not isinstance(config, dict):
        raise ValueError("Each book configuration must be a JSON object.")
    book_id = safe_book_id(config.get("book_id"))
    pdf_url = config.get("pdf_url")
    if not isinstance(pdf_url, str) or not pdf_url.strip():
        raise ValueError(f"{book_id}: pdf_url must be a non-empty URL.")
    if not pdf_url.lower().startswith(("http://", "https://")):
        raise ValueError(f"{book_id}: pdf_url must use http or https.")

    boundaries = config.get("boundaries")
    if not isinstance(boundaries, list) or not boundaries:
        raise ValueError(f"{book_id}: boundaries must be a non-empty list.")
    seen_sections: set[tuple[str, str]] = set()
    for boundary in boundaries:
        if not isinstance(boundary, dict):
            raise ValueError(f"{book_id}: each boundary must be an object.")
        section_type = boundary.get("type")
        title = boundary.get("title")
        if not isinstance(section_type, str) or not section_type.strip():
            raise ValueError(f"{book_id}: every boundary needs a non-empty type.")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"{book_id}: every boundary needs a non-empty title.")
        start_page = boundary.get("start_page")
        end_page = boundary.get("end_page")
        if (
            not isinstance(start_page, int)
            or isinstance(start_page, bool)
            or not isinstance(end_page, int)
            or isinstance(end_page, bool)
            or start_page < 1
            or end_page < start_page
        ):
            raise ValueError(f"{book_id}: {title!r} must have valid 1-based start_page/end_page values.")
        section_key = (section_type.strip().lower(), title.strip().lower())
        if section_key in seen_sections:
            raise ValueError(f"{book_id}: duplicate section boundary {title!r}.")
        seen_sections.add(section_key)

    return config


def load_config(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Unable to read configuration {path}: {error}") from error
    if isinstance(data, dict) and isinstance(data.get("books"), list):
        books = data["books"]
    elif isinstance(data, list):
        books = data
    else:
        raise ValueError("Configuration must be a JSON array or an object containing a 'books' array.")
    if not books:
        raise ValueError("Configuration must contain at least one book.")
    validated = [validate_book_config(item) for item in books]
    book_ids = [safe_book_id(item["book_id"]) for item in validated]
    if len(book_ids) != len(set(book_ids)):
        raise ValueError("Configuration contains duplicate book_id values.")
    return validated


def download_pdf(url: str, target: Path, timeout: float, retries: int) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = target.with_name(f".{target.name}.part")
    request = Request(url, headers={"User-Agent": "aviation-camp-pdf-processor/1.0"})
    for attempt in range(retries + 1):
        try:
            temporary_path.unlink(missing_ok=True)
            with urlopen(request, timeout=timeout) as response, temporary_path.open("wb") as output:
                while chunk := response.read(DOWNLOAD_CHUNK_SIZE):
                    output.write(chunk)
            if temporary_path.stat().st_size == 0:
                raise OSError("Downloaded file is empty.")
            temporary_path.replace(target)
            return
        except (OSError, http.client.HTTPException, URLError) as error:
            temporary_path.unlink(missing_ok=True)
            if attempt == retries:
                raise RuntimeError(f"Failed to download {url!r} after {retries + 1} attempt(s): {error}") from error
            delay = min(2**attempt, 8)
            LOGGER.warning("Download attempt %s/%s failed for %s: %s; retrying in %ss",
                           attempt + 1, retries + 1, url, error, delay)
            time.sleep(delay)


def open_pdf(path: Path) -> fitz.Document:
    try:
        document = fitz.open(path)
    except (fitz.FileDataError, RuntimeError, ValueError) as error:
        raise ValueError(f"Unable to open PDF {path}: {error}") from error
    if document.is_encrypted and not document.authenticate(""):
        document.close()
        raise ValueError(f"PDF is password-protected: {path}")
    if document.page_count < 1:
        document.close()
        raise ValueError(f"PDF contains no pages: {path}")
    return document


def float_bbox(rect: Any) -> list[float]:
    return [float(value) for value in rect]


def is_in_body(rect: fitz.Rect, page_height: float) -> bool:
    return (
        rect.y0 >= page_height * HEADER_FOOTER_FRACTION
        and rect.y1 <= page_height * (1 - HEADER_FOOTER_FRACTION)
    )


def span_style(span: dict[str, Any], bbox: list[float]) -> dict[str, Any]:
    font_name = str(span.get("font", ""))
    font_flags = int(span.get("flags", 0))
    color_value = int(span.get("color", 0)) & 0xFFFFFF
    return {
        "type": "text",
        "text": str(span.get("text", "")),
        "font_name": font_name,
        "font_size": float(span.get("size", 0.0)),
        "color": f"#{color_value:06X}",
        "is_bold": "bold" in font_name.lower() or bool(font_flags & 16),
        "is_italic": any(style in font_name.lower() for style in ("italic", "oblique"))
        or bool(font_flags & 2),
        "bbox": bbox,
    }


def extract_tables(page: fitz.Page) -> tuple[list[dict[str, Any]], list[fitz.Rect]]:
    table_elements: list[dict[str, Any]] = []
    table_rects: list[fitz.Rect] = []
    finder = page.find_tables()
    for table in finder.tables:
        rect = fitz.Rect(table.bbox)
        if not is_in_body(rect, page.rect.height):
            continue
        table_rects.append(rect)
        table_elements.append({"type": "table", "data": table.extract(), "bbox": float_bbox(rect)})
    return table_elements, table_rects


def span_is_in_table(bbox: fitz.Rect, table_rects: list[fitz.Rect]) -> bool:
    return any(table_rect.contains(bbox.tl) and table_rect.contains(bbox.br) for table_rect in table_rects) or any(
        table_rect.contains((bbox.x0 + bbox.x1) / 2, (bbox.y0 + bbox.y1) / 2)
        for table_rect in table_rects
    )


def save_image_block(
    block: dict[str, Any], book_dir: Path, output_root: Path, book_id: str, page_number: int, block_index: int
) -> dict[str, Any] | None:
    image_bytes = block.get("image")
    if not isinstance(image_bytes, bytes) or not image_bytes:
        LOGGER.warning("%s page %s image block %s had no embedded image data", book_id, page_number, block_index)
        return None
    extension = str(block.get("ext") or "png").lower()
    if not re.fullmatch(r"[a-z0-9]{1,8}", extension):
        extension = "png"
    filename = f"p{page_number}_b{block_index}.{extension}"
    image_path = book_dir / "images" / filename
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.write_bytes(image_bytes)
    try:
        stored_path = image_path.relative_to(output_root.parent)
    except ValueError:
        stored_path = image_path
    return {
        "type": "image",
        "image_path": stored_path.as_posix(),
        "bbox": float_bbox(block["bbox"]),
    }


def line_column(bbox: list[float], midpoint: float) -> int:
    return 0 if bbox[0] < midpoint else 1


def extract_page(
    page: fitz.Page, book_dir: Path, output_root: Path, book_id: str, page_number: int
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    page_dict = page.get_text("dict")
    table_elements, table_rects = extract_tables(page)
    text_lines: list[dict[str, Any]] = []
    other_elements: list[dict[str, Any]] = list(table_elements)
    midpoint = page.rect.width / 2

    for block_index, block in enumerate(page_dict.get("blocks", [])):
        block_type = block.get("type")
        if block_type == 1:
            image_rect = fitz.Rect(block["bbox"])
            if is_in_body(image_rect, page.rect.height):
                try:
                    image_element = save_image_block(
                        block, book_dir, output_root, book_id, page_number, block_index
                    )
                except OSError:
                    LOGGER.exception("%s page %s could not save image block %s", book_id, page_number, block_index)
                    continue
                if image_element:
                    other_elements.append(image_element)
            continue
        if block_type != 0:
            continue

        for line in block.get("lines", []):
            line_bbox = float_bbox(line.get("bbox", block["bbox"]))
            line_rect = fitz.Rect(line_bbox)
            if not is_in_body(line_rect, page.rect.height):
                continue
            line_elements: list[dict[str, Any]] = []
            for span in line.get("spans", []):
                text = str(span.get("text", ""))
                if not text.strip():
                    continue
                span_bbox = float_bbox(span.get("bbox", line_bbox))
                rect = fitz.Rect(span_bbox)
                if not is_in_body(rect, page.rect.height) or span_is_in_table(rect, table_rects):
                    continue
                line_elements.append(span_style(span, span_bbox))
            if line_elements:
                text_lines.append(
                    {
                        "bbox": line_bbox,
                        "column": line_column(line_bbox, midpoint),
                        "elements": line_elements,
                    }
                )

    text_lines.sort(key=lambda item: (item["column"], item["bbox"][1], item["bbox"][0]))
    clean_hyphenated_lines(text_lines)
    for line in text_lines:
        other_elements.extend(line["elements"])

    other_elements.sort(
        key=lambda element: (
            line_column(element["bbox"], midpoint),
            element["bbox"][1],
            element["bbox"][0],
            {"text": 0, "table": 1, "image": 2}.get(element["type"], 3),
        )
    )
    return other_elements, text_lines


def clean_hyphenated_lines(lines: list[dict[str, Any]]) -> None:
    for index in range(len(lines) - 1):
        current = lines[index]
        following = lines[index + 1]
        if (
            current["column"] != following["column"]
            or not current["elements"]
            or not following["elements"]
        ):
            continue
        previous_span = current["elements"][-1]
        next_span = following["elements"][0]
        if (
            previous_span["text"].rstrip().endswith("-")
            and next_span["text"][:1].islower()
            and abs(current["bbox"][0] - following["bbox"][0]) <= 36
            and following["bbox"][1] > current["bbox"][1]
        ):
            previous_span["text"] = previous_span["text"].rstrip()[:-1] + next_span["text"].lstrip()
            following["elements"].pop(0)


def line_text(line: dict[str, Any]) -> str:
    return re.sub(r"\s+", " ", "".join(element["text"] for element in line["elements"])).strip()


def key_value_from_lines(lines: list[dict[str, Any]], title: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    current_key: str | None = None
    heading = title.strip().lower()
    separator = re.compile(r"^(.{1,100}?)(?:\s+[—–-]\s+|:\s*)(\S.*)$")
    acronym_line = re.compile(r"^([A-Z][A-Z0-9./-]{0,19})\s+(.{2,})$")

    for line in lines:
        text = line_text(line)
        if not text or text.lower() == heading:
            continue
        spans = line["elements"]
        bold_prefix: list[str] = []
        non_bold_suffix: list[str] = []
        found_plain = False
        for span in spans:
            if span["is_bold"] and not found_plain:
                bold_prefix.append(span["text"])
            else:
                found_plain = True
                non_bold_suffix.append(span["text"])
        key: str | None = None
        definition: str | None = None

        if bold_prefix and "".join(non_bold_suffix).strip():
            key = re.sub(r"\s+", " ", "".join(bold_prefix)).strip(" :.-")
            definition = re.sub(r"\s+", " ", "".join(non_bold_suffix)).strip()
        else:
            match = separator.match(text)
            if match:
                key, definition = match.group(1).strip(" :.-"), match.group(2).strip()
            elif (match := acronym_line.match(text)) and len(match.group(1)) <= 15:
                key, definition = match.group(1), match.group(2).strip()

        if key and definition and key.lower() != heading:
            entries[key] = " ".join(filter(None, (entries.get(key), definition)))
            current_key = key
        elif bold_prefix and not "".join(non_bold_suffix).strip():
            key = re.sub(r"\s+", " ", "".join(bold_prefix)).strip(" :.-")
            if key and key.lower() != heading:
                current_key = key
                entries.setdefault(key, "")
        elif current_key:
            entries[current_key] = " ".join(filter(None, (entries[current_key], text)))

    return {key: value for key, value in entries.items() if value}


def extract_boundary(
    document: fitz.Document,
    book_dir: Path,
    output_root: Path,
    book_id: str,
    boundary: dict[str, Any],
) -> dict[str, Any]:
    start_page = boundary["start_page"]
    end_page = boundary["end_page"]
    if end_page > document.page_count:
        raise ValueError(
            f"{book_id}: section {boundary['title']!r} ends at page {end_page}, "
            f"but the PDF has {document.page_count} page(s)."
        )
    section: dict[str, Any] = {
        "type": boundary["type"],
        "title": boundary["title"],
        "start_page": start_page,
        "end_page": end_page,
    }
    structured = boundary["type"].lower() in {"glossary", "acronyms"}
    pages: list[dict[str, Any]] = []
    structured_lines: list[dict[str, Any]] = []
    for page_number in range(start_page, end_page + 1):
        try:
            page = document.load_page(page_number - 1)
            elements, lines = extract_page(page, book_dir, output_root, book_id, page_number)
        except Exception:
            LOGGER.exception("%s: failed to process PDF page %s; emitting an empty page", book_id, page_number)
            elements, lines = [], []
        pages.append({"page_number": page_number, "elements": elements})
        structured_lines.extend(lines)
    if structured:
        section["structured_data"] = key_value_from_lines(structured_lines, boundary["title"])
    else:
        section["pages"] = pages
    return section


def process_book(
    config: dict[str, Any], output_root: Path, timeout: float = 30.0, retries: int = 3
) -> Path:
    book_id = safe_book_id(config["book_id"])
    book_dir = output_root / book_id
    book_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = book_dir / f"{book_id}.pdf"
    download_pdf(config["pdf_url"], pdf_path, timeout, retries)

    document = open_pdf(pdf_path)
    try:
        sections = [
            extract_boundary(document, book_dir, output_root, book_id, boundary)
            for boundary in config["boundaries"]
        ]
    finally:
        document.close()

    result = {"book_id": book_id, "sections": sections}
    output_path = book_dir / "parsed_content.json"
    temporary_output = output_path.with_name(f".{output_path.name}.tmp")
    temporary_output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_output.replace(output_path)
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "config",
        type=Path,
        help="JSON array or library manifest containing book URLs and section page boundaries",
    )
    parser.add_argument("--output-root", type=Path, default=Path("output"), help="Output directory (default: output)")
    parser.add_argument("--timeout", type=float, default=30.0, help="Network timeout in seconds (default: 30)")
    parser.add_argument("--retries", type=int, default=3, help="Download retry count (default: 3)")
    args = parser.parse_args(argv)
    if args.timeout <= 0 or args.retries < 0:
        parser.error("--timeout must be positive and --retries must be non-negative")

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        books = load_config(args.config)
    except ValueError as error:
        parser.error(str(error))
    failed = False
    for book in books:
        book_id = book["book_id"]
        try:
            output_path = process_book(book, args.output_root, args.timeout, args.retries)
            LOGGER.info("%s: wrote %s", book_id, output_path)
        except (OSError, RuntimeError, ValueError, URLError) as error:
            failed = True
            LOGGER.error("%s: processing failed: %s", book_id, error)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

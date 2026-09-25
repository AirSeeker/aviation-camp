#!/usr/bin/env python3
"""Parse PDF textbooks into chapter-level text and image assets."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import fitz

ROOT = Path(__file__).resolve().parents[1]
LIBRARY_ROOT = ROOT / "resources" / "library"
PARSED_ROOT = ROOT / "resources" / "parsed"
PUBLIC_IMAGES_ROOT = ROOT / "public" / "images"


def sanitize_book_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")
    return cleaned or "book"


def normalize_line(raw_line: str) -> str:
    return re.sub(r"\s+", " ", raw_line.strip())


def chapter_title_matches(title: str) -> bool:
    return bool(re.search(r"(?:^|\s)(?:chapter|part|section|lesson)\b", title.strip(), re.I))


def detect_chapter_ranges(doc: fitz.Document, page_count: int) -> List[Tuple[int, int]]:
    toc = doc.get_toc(simple=False)
    starts: List[int] = []

    if toc:
        for item in toc:
            if len(item) < 3:
                continue
            level, title, page_num = item[:3]
            if page_num and chapter_title_matches(str(title)):
                if int(page_num) <= page_count:
                    starts.append(int(page_num))

    if not starts:
        for page_idx in range(page_count):
            page = doc.load_page(page_idx)
            text = page.get_text("text")
            if re.search(r"(?im)^(?:chapter|part|section|lesson)\s+[\d\.IVX]+", text):
                starts.append(page_idx + 1)

    if not starts:
        return [(1, page_count)]

    starts = sorted(set(starts))
    ranges: List[Tuple[int, int]] = []
    for index, start in enumerate(starts):
        end = starts[index + 1] - 1 if index + 1 < len(starts) else page_count
        if end >= start:
            ranges.append((start, end))

    return ranges


def clean_text_lines(page_lines: Iterable[str], book_name: str) -> List[str]:
    cleaned: List[str] = []
    for raw in page_lines:
        line = normalize_line(raw)
        if not line:
            continue
        lowered = line.lower()
        if lowered == book_name.lower():
            continue
        if re.fullmatch(r"(?:page\s*)?\d+", line, flags=re.I):
            continue
        if re.fullmatch(r"\d+\s*(?:[-/]|\.|:)\s*\d+", line):
            continue
        if re.fullmatch(r"[A-Za-z0-9\s&'()-]{0,30}\d{1,4}", line):
            if re.search(r"\d", line) and len(line.split()) <= 4:
                continue
        cleaned.append(line)
    return cleaned


def collect_page_text(doc: fitz.Document, book_name: str) -> Dict[int, List[str]]:
    page_text_by_num: Dict[int, List[str]] = {}
    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        raw_text = page.get_text("text")
        lines = raw_text.splitlines()
        page_text_by_num[page_index + 1] = clean_text_lines(lines, book_name)
    return page_text_by_num


def deduplicate_repeated_header_footer(page_text_by_num: Dict[int, List[str]], book_name: str) -> Dict[int, List[str]]:
    flattened: Counter[str] = Counter()
    for page_lines in page_text_by_num.values():
        for line in page_lines:
            flattened[line] += 1

    repeated: set[str] = set()
    total_pages = len(page_text_by_num)
    for line, count in flattened.items():
        if not line:
            continue
        if count >= max(2, total_pages // 3):
            repeated.add(line)
        if line.lower() == book_name.lower():
            repeated.add(line)

    cleaned: Dict[int, List[str]] = {}
    for page_num, page_lines in page_text_by_num.items():
        cleaned[page_num] = [line for line in page_lines if line not in repeated]
    return cleaned


def chapter_text_from_range(page_text_by_num: Dict[int, List[str]], start_page: int, end_page: int) -> str:
    chunks: List[str] = []
    for page_num in range(start_page, end_page + 1):
        lines = page_text_by_num.get(page_num, [])
        if lines:
            chunks.append("\n".join(lines))
    return "\n\n".join(chunks).strip()


def image_extension_for_pixmap(pix: fitz.Pixmap) -> str:
    return "png"


def extract_images_for_chapter(doc: fitz.Document, chapter_dir: Path, book_name: str, chapter_key: str, start_page: int, end_page: int) -> List[Dict[str, Any]]:
    manifest: List[Dict[str, Any]] = []
    image_counter = 0

    for page_num in range(start_page, end_page + 1):
        page = doc.load_page(page_num - 1)
        for item in page.get_images(full=True):
            image_counter += 1
            xref = item[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.colorspace is None:
                continue
            if pix.colorspace.n != 3 or pix.alpha:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            file_name = f"img_p{page_num}_{image_counter}.png"
            target_path = chapter_dir / file_name
            pix.save(str(target_path))
            rel_path = f"/images/{book_name}/{chapter_key}/{file_name}"
            manifest.append(
                {
                    "page": page_num,
                    "file": file_name,
                    "relativePath": rel_path,
                    "figureRef": f"Figure {page_num}-{image_counter}",
                    "index": image_counter,
                }
            )
            pix = None

    return manifest


def parse_book(pdf_path: Path, output_root: Path, public_images_root: Path) -> Dict[str, Any]:
    book_name = sanitize_book_name(pdf_path.parent.name)
    book_out_dir = output_root / book_name
    book_out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    page_count = doc.page_count
    page_text_by_num = collect_page_text(doc, book_name)
    page_text_by_num = deduplicate_repeated_header_footer(page_text_by_num, book_name)
    chapter_ranges = detect_chapter_ranges(doc, page_count)

    chapter_manifest: List[Dict[str, Any]] = []
    for index, (start_page, end_page) in enumerate(chapter_ranges, start=1):
        chapter_key = f"ch{index:02d}"
        chapter_dir = book_out_dir / chapter_key
        chapter_dir.mkdir(parents=True, exist_ok=True)

        raw_text = chapter_text_from_range(page_text_by_num, start_page, end_page)
        (chapter_dir / "content_raw.txt").write_text(raw_text, encoding="utf-8")

        image_dir = public_images_root / book_name / chapter_key
        image_dir.mkdir(parents=True, exist_ok=True)

        images = extract_images_for_chapter(doc, image_dir, book_name, chapter_key, start_page, end_page)
        (chapter_dir / "images_manifest.json").write_text(
            json.dumps({"chapter": chapter_key, "images": images}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        chapter_manifest.append(
            {
                "chapter": chapter_key,
                "startPage": start_page,
                "endPage": end_page,
                "images": images,
            }
        )

    book_manifest = {
        "bookName": book_name,
        "sourcePdf": str(pdf_path.relative_to(ROOT)),
        "chapters": chapter_manifest,
    }
    (book_out_dir / "book_manifest.json").write_text(json.dumps(book_manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    return book_manifest


def iter_pdf_files(book_filter: str | None = None) -> List[Path]:
    roots = [LIBRARY_ROOT]
    pdf_files: List[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for pdf_path in sorted(root.rglob("*.pdf")):
            if book_filter:
                if pdf_path.parent.name.lower() == book_filter.lower():
                    pdf_files.append(pdf_path)
            else:
                pdf_files.append(pdf_path)
    return pdf_files


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse aviation PDF textbooks into chapter text and images")
    parser.add_argument("--book", help="Optional book folder name under resources/library")
    args = parser.parse_args()

    PARSED_ROOT.mkdir(parents=True, exist_ok=True)
    PUBLIC_IMAGES_ROOT.mkdir(parents=True, exist_ok=True)

    pdf_files = iter_pdf_files(args.book)
    if not pdf_files:
        raise SystemExit(f"No PDF files found in {LIBRARY_ROOT}.")

    for pdf_path in pdf_files:
        parse_book(pdf_path, PARSED_ROOT, PUBLIC_IMAGES_ROOT)
        print(f"Processed: {pdf_path.parent.name}")


if __name__ == "__main__":
    main()

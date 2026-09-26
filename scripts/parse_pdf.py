#!/usr/bin/env python3
"""Parse PDF textbooks into chapter-level text and image assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from collections import Counter
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Tuple

import fitz

ROOT = Path(__file__).resolve().parents[1]
LIBRARY_ROOT = ROOT / "resources" / "library"
PARSED_ROOT = ROOT / "resources" / "parsed"
PUBLIC_IMAGES_ROOT = ROOT / "public" / "images"
CHAPTER_OVERRIDES_PATH = LIBRARY_ROOT / "chapter_overrides.json"


@contextmanager
def open_pdf_document(pdf_path: Path) -> Iterator[fitz.Document]:
    try:
        doc = fitz.open(str(pdf_path))
    except Exception as error:
        raise ValueError(f"Unable to open PDF '{pdf_path}': {error}") from error

    try:
        if doc.is_encrypted and not doc.authenticate(""):
            raise ValueError(f"PDF is password-protected: {pdf_path}")
        if doc.page_count == 0:
            raise ValueError(f"PDF contains no pages: {pdf_path}")
        yield doc
    finally:
        doc.close()


def sanitize_book_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")
    return cleaned or "book"


def normalize_line(raw_line: str) -> str:
    return re.sub(r"\s+", " ", raw_line.strip())


def chapter_title_matches(title: str) -> bool:
    return bool(re.search(r"(?:^|\s)(?:chapter|part|section|lesson)\b", title.strip(), re.I))


def supplemental_title_matches(title: str) -> bool:
    return bool(
        re.match(
            r"^(?:appendix(?:es)?|glossary|(?:subject |name )?index|references|bibliography|"
            r"answer key|answers to (?:the )?(?:review )?questions|acknowledgments?|acknowledgements?|credits)\b",
            normalize_line(title),
            re.I,
        )
    )


def infer_image_kind(text: str) -> str:
    value = normalize_line(text or "")
    lowered = value.lower()
    if re.search(r"\b(?:figure|fig\.|diagram|illustration|photo|image|drawing)\b", lowered):
        return "figure"
    if re.search(r"\b(?:table|chart|graph|matrix|schedule)\b", lowered):
        return "table"
    return "figure"


def needs_ocr_retry(lines: Iterable[str]) -> bool:
    cleaned = [normalize_line(line) for line in lines if normalize_line(line)]
    if not cleaned:
        return True

    meaningful = [
        line for line in cleaned
        if not re.fullmatch(r"(?:page\s*)?\d+", line, flags=re.I)
        and not re.fullmatch(r"(?:figure|table|chart|image)\s*\d+.*", line, flags=re.I)
        and len(line) > 2
    ]
    if not meaningful:
        return True

    word_count = sum(len(re.findall(r"\b\w+\b", line)) for line in meaningful)
    return word_count < 10


def ranges_from_starts(starts: Iterable[int], page_count: int) -> List[Tuple[int, int]]:
    ordered_starts = sorted(set(starts))
    if any(start < 1 or start > page_count for start in ordered_starts):
        raise ValueError(f"Chapter start pages must be between 1 and {page_count}.")

    return [
        (start, ordered_starts[index + 1] - 1 if index + 1 < len(ordered_starts) else page_count)
        for index, start in enumerate(ordered_starts)
    ]


def validate_chapter_ranges(chapter_ranges: List[Tuple[int, int]], page_count: int) -> None:
    if not chapter_ranges:
        raise ValueError("Chapter ranges cannot be empty.")

    validated: List[Tuple[int, int]] = []
    for start, end in chapter_ranges:
        if not isinstance(start, int) or not isinstance(end, int) or isinstance(start, bool) or isinstance(end, bool):
            raise ValueError("Each chapter range must contain integer page numbers.")
        if start < 1 or end < start or end > page_count:
            raise ValueError(f"Chapter range ({start}, {end}) is outside the document bounds 1..{page_count}.")
        validated.append((start, end))

    validated.sort()
    expected_start: int | None = None
    for start, end in validated:
        if expected_start is not None and start != expected_start:
            raise ValueError(
                f"Chapter ranges must be contiguous without gaps or overlaps; "
                f"expected next chapter to begin at page {expected_start}, found {start}."
            )
        expected_start = end + 1


def detect_chapter_ranges(
    doc: fitz.Document, page_count: int, chapter_starts: List[int] | None = None
) -> List[Tuple[int, int]]:
    if chapter_starts is not None:
        if not chapter_starts or any(not isinstance(start, int) or isinstance(start, bool) for start in chapter_starts):
            raise ValueError("Chapter overrides must be a non-empty list of integer page numbers.")
        return ranges_from_starts(chapter_starts, page_count)

    toc = doc.get_toc(simple=False)
    toc_entries: List[Tuple[int, str, int]] = []

    if toc:
        for item in toc:
            if len(item) < 3:
                continue
            level, title, page_num = item[:3]
            if page_num and 1 <= int(page_num) <= page_count:
                toc_entries.append((int(level), str(title), int(page_num)))

    chapter_entries = [
        entry
        for entry in toc_entries
        if re.search(r"(?:^|\s)(?:chapter|part)\b", entry[1].strip(), re.I)
    ]
    selected_entries = chapter_entries or [
        entry for entry in toc_entries if chapter_title_matches(entry[1])
    ]
    if chapter_starts is not None:
        starts = list(chapter_starts)
    elif selected_entries:
        shallowest_level = min(level for level, _, _ in selected_entries)
        starts = [
            page_num
            for level, _, page_num in selected_entries
            if level == shallowest_level and 1 <= page_num <= page_count
        ]
    else:
        starts = []

    if not starts:
        for page_idx in range(page_count):
            page = doc.load_page(page_idx)
            text = page.get_text("text")
            if re.search(r"(?im)^(?:chapter|part|section|lesson)\s+[\d\.IVX]+", text):
                starts.append(page_idx + 1)

    if not starts:
        raise ValueError(
            "No educational chapter starts detected; add the book to chapter_overrides.json with 1-based PDF page numbers."
        )

    ranges = ranges_from_starts(starts, page_count)
    last_chapter_start = max(starts)
    last_chapter_end = page_count
    if selected_entries:
        chapter_level = min(level for level, _, _ in selected_entries)
        non_chapter_pages = [
            page_num
            for level, title, page_num in toc_entries
            if page_num > last_chapter_start
            and level <= chapter_level
            and not chapter_title_matches(title)
        ]
        if non_chapter_pages:
            last_chapter_end = min(non_chapter_pages) - 1

    supplemental_pages = []
    for page_num in range(last_chapter_start + 1, page_count + 1):
        page_lines = [normalize_line(line) for line in doc.load_page(page_num - 1).get_text("text").splitlines()]
        if any(supplemental_title_matches(line) for line in page_lines[:8]):
            supplemental_pages.append(page_num)
    if supplemental_pages:
        last_chapter_end = min(last_chapter_end, min(supplemental_pages) - 1)

    if last_chapter_end >= ranges[-1][0]:
        ranges[-1] = (ranges[-1][0], last_chapter_end)
    validate_chapter_ranges(ranges, page_count)
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
        cleaned.append(line)
    return cleaned


def create_ocr_textpage(page: fitz.Page, language: str, dpi: int) -> fitz.TextPage:
    return page.get_textpage_ocr(language=language, dpi=dpi, full=False)


def extract_layout_lines(page: fitz.Page, textpage: fitz.TextPage | None = None) -> List[Tuple[float, float, float, float, str]]:
    page_dict = page.get_text("dict", textpage=textpage) if textpage is not None else page.get_text("dict")
    lines: List[Tuple[float, float, float, float, str]] = []
    for block in page_dict["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            text = "".join(span.get("text", "") for span in spans)
            if not text.strip():
                continue
            x0, y0, x1, y1 = line.get("bbox", block["bbox"])
            lines.append((float(x0), float(y0), float(x1), float(y1), text))

    if not lines:
        return []

    column_gap = page.rect.width * 0.15
    column_starts = sorted({line[0] for line in lines})
    columns: List[List[float]] = []
    for x_start in column_starts:
        if not columns or x_start - columns[-1][-1] > column_gap:
            columns.append([x_start])
        else:
            columns[-1].append(x_start)

    def column_for(x_start: float) -> int:
        return min(
            range(len(columns)),
            key=lambda index: min(abs(x_start - candidate) for candidate in columns[index]),
        )

    return sorted(lines, key=lambda line: (column_for(line[0]), line[1], line[0]))


def collect_page_text(
    doc: fitz.Document,
    book_name: str,
    ocr: bool = False,
    ocr_language: str = "eng",
    ocr_dpi: int = 300,
    ocr_retry_dpi: int | None = None,
) -> Tuple[Dict[int, List[str]], Dict[int, set[str]]]:
    page_text_by_num: Dict[int, List[str]] = {}
    edge_lines_by_num: Dict[int, set[str]] = {}
    retry_dpi = ocr_retry_dpi if ocr_retry_dpi is not None else max(ocr_dpi, 400)
    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        textpage = create_ocr_textpage(page, ocr_language, ocr_dpi) if ocr else None
        layout_lines = extract_layout_lines(page, textpage)
        if ocr and needs_ocr_retry([line[4] for line in layout_lines]):
            retry_textpage = create_ocr_textpage(page, ocr_language, retry_dpi)
            layout_lines = extract_layout_lines(page, retry_textpage)
        lines = [line[4] for line in layout_lines]
        page_num = page_index + 1
        page_text_by_num[page_num] = clean_text_lines(lines, book_name)

        edge_lines: set[str] = set()
        page_height = page.rect.height
        for _, y0, _, y1, text in layout_lines:
            if y0 <= page_height * 0.08 or y1 >= page_height * 0.92:
                edge_lines.update(clean_text_lines([text], book_name))
        edge_lines_by_num[page_num] = edge_lines

    return page_text_by_num, edge_lines_by_num


def deduplicate_repeated_header_footer(
    page_text_by_num: Dict[int, List[str]], edge_lines_by_num: Dict[int, set[str]]
) -> Dict[int, List[str]]:
    edge_page_counts: Counter[str] = Counter()
    for edge_lines in edge_lines_by_num.values():
        edge_page_counts.update(edge_lines)

    total_pages = len(page_text_by_num)
    threshold = max(2, (total_pages + 1) // 2)
    repeated = {line for line, count in edge_page_counts.items() if count >= threshold}

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
    images_by_xref: Dict[int, Dict[str, Any]] = {}
    image_counter = 0

    for page_num in range(start_page, end_page + 1):
        page = doc.load_page(page_num - 1)
        seen_page_xrefs: set[int] = set()
        for item in page.get_images(full=True):
            xref = item[0]
            if xref in seen_page_xrefs:
                continue
            seen_page_xrefs.add(xref)

            placements = [
                {"page": page_num, "bbox": [float(value) for value in rect]}
                for rect in page.get_image_rects(xref)
            ]
            if xref in images_by_xref:
                images_by_xref[xref]["placements"].extend(placements)
                continue

            pix = fitz.Pixmap(doc, xref)
            if pix.colorspace is None:
                continue
            if pix.colorspace.n != 3 or pix.alpha:
                pix = fitz.Pixmap(fitz.csRGB, pix)

            image_counter += 1
            file_name = f"img_p{page_num}_{image_counter}.png"
            target_path = chapter_dir / file_name
            pix.save(str(target_path))
            rel_path = f"/images/{book_name}/{chapter_key}/{file_name}"
            figure_ref = f"Figure {page_num}-{image_counter}"
            image_entry = {
                "page": page_num,
                "file": file_name,
                "relativePath": rel_path,
                "figureRef": figure_ref,
                "kind": infer_image_kind(figure_ref),
                "index": image_counter,
                "placements": placements,
            }
            manifest.append(image_entry)
            images_by_xref[xref] = image_entry

    return manifest


def read_existing_manifest(manifest_path: Path) -> Dict[str, Any]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return manifest if isinstance(manifest, dict) else {}


def build_parse_cache_key(
    pdf_path: Path,
    ocr: bool,
    ocr_language: str,
    ocr_dpi: int,
    chapter_starts: List[int] | None,
    ocr_retry_dpi: int | None = None,
) -> str:
    payload = {
        "parser_version": 2,
        "pdf": str(pdf_path.resolve()),
        "ocr": bool(ocr),
        "ocr_language": ocr_language,
        "ocr_dpi": int(ocr_dpi),
        "ocr_retry_dpi": int(ocr_retry_dpi) if ocr_retry_dpi is not None else None,
        "chapter_starts": chapter_starts or [],
    }
    digest = hashlib.sha256()
    digest.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    return digest.hexdigest()


def load_chapter_overrides(overrides_path: Path) -> Dict[str, List[int]]:
    if not overrides_path.exists():
        return {}
    try:
        raw_overrides = json.loads(overrides_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Unable to read chapter overrides from {overrides_path}: {error}") from error
    if not isinstance(raw_overrides, dict):
        raise ValueError("Chapter overrides must be a JSON object keyed by book folder name.")

    overrides: Dict[str, List[int]] = {}
    for book_name, starts in raw_overrides.items():
        if not isinstance(book_name, str) or not isinstance(starts, list):
            raise ValueError("Each chapter override must map a book folder name to a list of page numbers.")
        if not starts or any(not isinstance(start, int) or isinstance(start, bool) for start in starts):
            raise ValueError(f"Chapter override for {book_name!r} must contain integer page numbers.")
        if len(set(starts)) != len(starts) or any(start < 1 for start in starts):
            raise ValueError(f"Chapter override for {book_name!r} has duplicate or non-positive page numbers.")
        overrides[sanitize_book_name(book_name)] = starts
    return overrides


def find_book_output_collisions(pdf_files: Iterable[Path]) -> Dict[str, List[Path]]:
    paths_by_book: Dict[str, List[Path]] = {}
    for pdf_path in pdf_files:
        book_name = sanitize_book_name(pdf_path.parent.name)
        paths_by_book.setdefault(book_name, []).append(pdf_path)
    return {book_name: paths for book_name, paths in paths_by_book.items() if len(paths) > 1}


def cleanup_stale_outputs(
    book_out_dir: Path,
    image_book_dir: Path,
    previous_manifest: Dict[str, Any],
    current_manifest: Dict[str, Any],
) -> None:
    current_chapters = {
        chapter.get("chapter"): chapter
        for chapter in current_manifest.get("chapters", [])
        if isinstance(chapter, dict) and isinstance(chapter.get("chapter"), str)
    }

    for previous_chapter in previous_manifest.get("chapters", []):
        if not isinstance(previous_chapter, dict):
            continue
        chapter_key = previous_chapter.get("chapter")
        if not isinstance(chapter_key, str) or not re.fullmatch(r"ch\d+", chapter_key):
            continue

        current_chapter = current_chapters.get(chapter_key)
        current_files = {
            image.get("file")
            for image in (current_chapter or {}).get("images", [])
            if isinstance(image, dict) and isinstance(image.get("file"), str)
        }
        stale_files = {
            image.get("file")
            for image in previous_chapter.get("images", [])
            if isinstance(image, dict) and isinstance(image.get("file"), str)
        } - current_files

        image_dir = image_book_dir / chapter_key
        for file_name in stale_files:
            if Path(file_name).name != file_name or not file_name.startswith("img_p") or not file_name.endswith(".png"):
                continue
            image_path = image_dir / file_name
            if image_path.is_file() and not image_path.is_symlink():
                image_path.unlink()

        if current_chapter is None:
            chapter_dir = book_out_dir / chapter_key
            for generated_name in ("content_raw.txt", "images_manifest.json"):
                generated_path = chapter_dir / generated_name
                if generated_path.is_file() and not generated_path.is_symlink():
                    generated_path.unlink()
            for directory in (chapter_dir, image_dir):
                try:
                    directory.rmdir()
                except OSError:
                    pass


def publish_staged_outputs(
    staged_book_dir: Path,
    staged_image_book_dir: Path,
    book_out_dir: Path,
    image_book_dir: Path,
) -> None:
    staged_image_files = sorted(path for path in staged_image_book_dir.rglob("*") if path.is_file())
    staged_book_files = sorted(
        (path for path in staged_book_dir.rglob("*") if path.is_file() and path.name != "book_manifest.json"),
        key=lambda path: path.relative_to(staged_book_dir).as_posix(),
    )
    manifest_path = staged_book_dir / "book_manifest.json"
    staged_files = staged_image_files + staged_book_files
    if manifest_path.is_file():
        staged_files.append(manifest_path)

    installed: List[Tuple[Path, Path | None]] = []
    try:
        for staged_path in staged_files:
            if staged_path.is_relative_to(staged_image_book_dir):
                target_path = image_book_dir / staged_path.relative_to(staged_image_book_dir)
            else:
                target_path = book_out_dir / staged_path.relative_to(staged_book_dir)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            if target_path.is_symlink():
                raise ValueError(f"Refusing to replace symlink output: {target_path}")

            backup_path = None
            if target_path.exists():
                descriptor, backup_name = tempfile.mkstemp(prefix=".parse-backup-", dir=target_path.parent)
                os.close(descriptor)
                backup_path = Path(backup_name)
                backup_path.unlink()
                try:
                    os.link(target_path, backup_path)
                except OSError:
                    shutil.copy2(target_path, backup_path)

            try:
                os.replace(staged_path, target_path)
            except Exception:
                if backup_path is not None:
                    os.replace(backup_path, target_path)
                raise
            installed.append((target_path, backup_path))
    except Exception:
        for target_path, backup_path in reversed(installed):
            if backup_path is None:
                target_path.unlink(missing_ok=True)
            else:
                os.replace(backup_path, target_path)
        raise
    else:
        for _, backup_path in installed:
            if backup_path is not None:
                backup_path.unlink(missing_ok=True)


def parse_book(
    pdf_path: Path,
    output_root: Path,
    public_images_root: Path,
    ocr: bool = False,
    ocr_language: str = "eng",
    ocr_dpi: int = 300,
    ocr_retry_dpi: int | None = None,
    chapter_starts: List[int] | None = None,
) -> Dict[str, Any]:
    book_name = sanitize_book_name(pdf_path.parent.name)
    book_out_dir = output_root / book_name
    image_book_dir = public_images_root / book_name
    manifest_path = book_out_dir / "book_manifest.json"
    previous_manifest = read_existing_manifest(manifest_path)
    output_root.mkdir(parents=True, exist_ok=True)
    public_images_root.mkdir(parents=True, exist_ok=True)

    cache_key = build_parse_cache_key(pdf_path, ocr, ocr_language, ocr_dpi, chapter_starts, ocr_retry_dpi)
    if previous_manifest.get("cacheKey") == cache_key and manifest_path.exists():
        return previous_manifest

    with open_pdf_document(pdf_path) as doc:
        with tempfile.TemporaryDirectory(prefix=f".{book_name}-parse-", dir=output_root) as staged_output_root:
            with tempfile.TemporaryDirectory(prefix=f".{book_name}-images-", dir=public_images_root) as staged_images_root:
                staged_book_dir = Path(staged_output_root) / book_name
                staged_image_book_dir = Path(staged_images_root) / book_name
                staged_book_dir.mkdir()
                staged_image_book_dir.mkdir()

                page_count = doc.page_count
                page_text_by_num, edge_lines_by_num = collect_page_text(
                    doc,
                    book_name,
                    ocr=ocr,
                    ocr_language=ocr_language,
                    ocr_dpi=ocr_dpi,
                    ocr_retry_dpi=ocr_retry_dpi,
                )
                pages_without_text = [page_num for page_num, lines in page_text_by_num.items() if not lines or needs_ocr_retry(lines)]
                if pages_without_text:
                    page_list = ", ".join(str(page_num) for page_num in pages_without_text)
                    print(f"Warning: low-quality text extraction in {pdf_path} on page(s): {page_list}; OCR may be needed.", file=sys.stderr)
                page_text_by_num = deduplicate_repeated_header_footer(page_text_by_num, edge_lines_by_num)
                chapter_ranges = detect_chapter_ranges(doc, page_count, chapter_starts)
                validate_chapter_ranges(chapter_ranges, page_count)

                chapter_manifest: List[Dict[str, Any]] = []
                for index, (start_page, end_page) in enumerate(chapter_ranges, start=1):
                    chapter_key = f"ch{index:02d}"
                    chapter_dir = staged_book_dir / chapter_key
                    chapter_dir.mkdir(parents=True, exist_ok=True)

                    raw_text = chapter_text_from_range(page_text_by_num, start_page, end_page)
                    (chapter_dir / "content_raw.txt").write_text(raw_text, encoding="utf-8")

                    image_dir = staged_image_book_dir / chapter_key
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
                    "cacheKey": cache_key,
                    "chapters": chapter_manifest,
                }
                (staged_book_dir / "book_manifest.json").write_text(
                    json.dumps(book_manifest, ensure_ascii=False, indent=2), encoding="utf-8"
                )
                publish_staged_outputs(staged_book_dir, staged_image_book_dir, book_out_dir, image_book_dir)

    cleanup_stale_outputs(book_out_dir, image_book_dir, previous_manifest, book_manifest)
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


def process_pdf_batch(
    pdf_files: Iterable[Path],
    output_root: Path,
    public_images_root: Path,
    chapter_overrides: Dict[str, List[int]],
    ocr: bool = False,
    ocr_language: str = "eng",
    ocr_dpi: int = 300,
    ocr_retry_dpi: int | None = None,
    workers: int = 4,
) -> List[Tuple[Path, Dict[str, Any]]]:
    book_files = list(pdf_files)
    if not book_files:
        return []

    max_workers = max(1, min(workers, len(book_files)))
    ordered_results: List[Tuple[Path, Dict[str, Any]]] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for pdf_path in book_files:
            futures.append(
                (
                    pdf_path,
                    executor.submit(
                        parse_book,
                        pdf_path,
                        output_root,
                        public_images_root,
                        ocr=ocr,
                        ocr_language=ocr_language,
                        ocr_dpi=ocr_dpi,
                        ocr_retry_dpi=ocr_retry_dpi,
                        chapter_starts=chapter_overrides.get(sanitize_book_name(pdf_path.parent.name)),
                    ),
                )
            )

        for pdf_path, future in futures:
            ordered_results.append((pdf_path, future.result()))

    return ordered_results


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse aviation PDF textbooks into chapter text and images")
    parser.add_argument("--book", help="Optional book folder name under resources/library")
    parser.add_argument("--ocr", action="store_true", help="OCR pages with Tesseract for scanned or image-based text")
    parser.add_argument("--ocr-language", default="eng", help="Tesseract language code (default: eng)")
    parser.add_argument("--ocr-dpi", type=int, default=300, help="OCR render resolution (default: 300)")
    parser.add_argument("--ocr-retry-dpi", type=int, default=400, help="OCR retry resolution for sparse pages (default: 400)")
    parser.add_argument("--workers", type=int, default=4, help="Number of PDF books to process in parallel (default: 4)")
    parser.add_argument(
        "--chapter-overrides",
        type=Path,
        default=CHAPTER_OVERRIDES_PATH,
        help="JSON map of book folder names to 1-based chapter start pages",
    )
    args = parser.parse_args()

    if args.ocr and not shutil.which("tesseract"):
        raise SystemExit("--ocr requires the Tesseract executable on PATH.")
    if args.ocr_dpi < 72:
        raise SystemExit("--ocr-dpi must be at least 72.")
    if args.ocr_retry_dpi < 72:
        raise SystemExit("--ocr-retry-dpi must be at least 72.")
    if args.workers < 1:
        raise SystemExit("--workers must be at least 1.")

    try:
        chapter_overrides = load_chapter_overrides(args.chapter_overrides)
    except ValueError as error:
        raise SystemExit(str(error)) from error

    pdf_files = iter_pdf_files(args.book)
    if not pdf_files:
        raise SystemExit(f"No PDF files found in {LIBRARY_ROOT}.")
    collisions = find_book_output_collisions(pdf_files)
    if collisions:
        collision_text = "; ".join(
            f"{book_name}: {', '.join(str(path) for path in paths)}"
            for book_name, paths in collisions.items()
        )
        raise SystemExit(f"Multiple PDFs map to the same output folder: {collision_text}. Put each PDF in its own folder.")

    PARSED_ROOT.mkdir(parents=True, exist_ok=True)
    PUBLIC_IMAGES_ROOT.mkdir(parents=True, exist_ok=True)

    results = process_pdf_batch(
        pdf_files=pdf_files,
        output_root=PARSED_ROOT,
        public_images_root=PUBLIC_IMAGES_ROOT,
        chapter_overrides=chapter_overrides,
        ocr=args.ocr,
        ocr_language=args.ocr_language,
        ocr_dpi=args.ocr_dpi,
        ocr_retry_dpi=args.ocr_retry_dpi,
        workers=max(1, min(args.workers, len(pdf_files))),
    )
    failures = 0
    for pdf_path, book_manifest in results:
        try:
            chapters = book_manifest["chapters"]
            page_count = sum(chapter["endPage"] - chapter["startPage"] + 1 for chapter in chapters)
            image_count = sum(len(chapter["images"]) for chapter in chapters)
            print(f"Processed: {pdf_path.parent.name} ({page_count} pages, {len(chapters)} chapters, {image_count} images)")
        except Exception as error:
            failures += 1
            print(f"Failed: {pdf_path}: {error}", file=sys.stderr)
            continue

    if failures:
        raise SystemExit(f"Failed to parse {failures} PDF file(s).")


if __name__ == "__main__":
    main()

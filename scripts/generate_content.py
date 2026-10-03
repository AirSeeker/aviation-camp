#!/usr/bin/env python3
"""Generate static MDX chapter pages from parsed PDF chapters without AI or quiz generation."""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
PARSED_ROOT = ROOT / "resources" / "parsed"
DOCS_OUTPUT_ROOT = ROOT / "src" / "content" / "docs"

GLOSSARY = {
    "Angle of Attack": "Angle of Attack",
    "Stall": "Stall",
    "Indicated Airspeed": "Indicated Airspeed (IAS)",
    "True Airspeed": "True Airspeed (TAS)",
    "Groundspeed": "Groundspeed",
    "Lift": "Lift",
    "Drag": "Drag",
    "Thrust": "Thrust",
    "Weight": "Weight",
    "Yaw": "Yaw",
    "Pitch": "Pitch",
    "Bank": "Bank",
    "Heading": "Heading",
    "Trim": "Trim",
    "Glide": "Glide",
    "VFR": "Visual Flight Rules (VFR)",
    "IFR": "Instrument Flight Rules (IFR)",
    "Holding Pattern": "Holding Pattern",
    "Crosswind": "Crosswind",
    "Tailwind": "Tailwind",
    "Headwind": "Headwind",
    "Density Altitude": "Density Altitude",
    "Pressure Altitude": "Pressure Altitude",
    "Mach Number": "Mach Number",
    "Minimum Safe Altitude": "Minimum Safe Altitude",
    "Aviation Weather": "Aviation Weather",
}

REQUIRED_FRONTMATTER_FIELDS = [
    "title",
    "description",
    "subject",
    "chapterNumber",
    "readTimeMinutes",
    "lang",
    "translationKey",
]


def normalize_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def translation_key_for(book_name: str, chapter_name: str) -> str:
    book_slug = normalize_slug(book_name or "chapter")
    chapter_slug = normalize_slug(chapter_name or "chapter")
    return f"{book_slug}-{chapter_slug}"


def contains_non_english_text(value: str) -> bool:
    if not value:
        return False
    if re.search(r"[\u0400-\u04FF]", value):
        return True
    forbidden = [
        "Ключові",
        "Увага",
        "Розумійте",
        "Польоти",
        "Що є",
        "Чому",
        "Яке",
    ]
    return any(term.lower() in value.lower() for term in forbidden)


def estimate_read_time_minutes(content: str) -> int:
    words = re.findall(r"\b\w+\b", content or "")
    count = len(words)
    minutes = max(8, int((count / 180) + 1))
    return min(20, minutes)


def infer_title_from_chapter(book_name: str, chapter_name: str, subject: str, content: str = "") -> str:
    chapter_num = maybe_infer_chapter_number(chapter_name)
    return f"{subject} — Chapter {chapter_num}"


def source_book_title(book_name: str) -> str:
    lower_name = book_name.lower()
    titles = {
        "afh": "Airplane Flying Handbook",
        "instrument": "Instrument Flying Handbook",
        "instrumentprocedures": "Instrument Procedures Handbook",
        "weather": "Aviation Weather Handbook",
        "weightbalance": "Aircraft Weight and Balance Handbook",
        "riskmanagement": "Risk Management Handbook",
        "phak": "Pilot's Handbook of Aeronautical Knowledge",
    }
    try:
        return titles[lower_name]
    except KeyError as exc:
        raise ValueError(f"No display title exists for book {book_name!r}") from exc


def normalize_text(raw_text: str) -> str:
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u2022", "-")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"(?<!\n)\n(?=[a-z])", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_parsed_body(text: str) -> str:
    cleaned = normalize_text(text)
    cleaned = re.sub(r"<figure\b.*?</figure>", " ", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"<img\s+[^>]*src=[\"']([^\"']+)[\"'][^>]*>", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"(?i)\bFigure\s+\d+(?:-\d+)?\.?\s*", " ", cleaned)
    cleaned = re.sub(r"\[\s*Figure\s+\d+(?:-\d+)?\s*\]", " ", cleaned)
    cleaned = re.sub(r"\[\s*\]\s*", " ", cleaned)
    cleaned = re.sub(r"[•⦁]\s*", "\n- ", cleaned)
    cleaned = re.sub(r"(?i)\bChapter\s+\d+\s+Introduction\s+To\s+Flying\s+Introduction\b", "", cleaned)
    cleaned = re.sub(r"(?i)\b(?:Chapter\s+\d+\s*)?(?:Introduction\s+To\s+Flying|Introduction)\b", "", cleaned)
    cleaned = re.sub(r"(?i)\bThe\s+following\s+In\s+2004\b", "In 2004", cleaned)
    cleaned = re.sub(r"(?i)\bFlight\s+information\s+publications\s+outlining\s+baseline\s+data:\s*", "", cleaned)
    cleaned = re.sub(r"(?i)\bThe\s+following\s+are\s+two\s+examples\s+of\s+how\s+the\s+time\s+would\s+be\s+presented:\b", "Examples of time notation:", cleaned)
    cleaned = re.sub(r"(?i)\bThe\s+FAA\s+selects\s+highly\s+qualified\s+individuals\s+to\s+be\s+DPEs\.?\b", "The FAA selects highly qualified individuals to be DPEs.", cleaned)
    cleaned = re.sub(r"(?i)\bA\s+FSDO\s+inspector\s+is\s+assigned\b", "A FSDO inspector is assigned", cleaned)
    cleaned = re.sub(r"(?i)\bRole\s+of\s+the\s+FAA\s+The\s+Federal\s+Aviation\s+Administration\s*\(FAA\)\b", "The Federal Aviation Administration (FAA)", cleaned)
    cleaned = re.sub(r"(?<=\.)\s+(?=-\s+[A-Z])", "\n\n", cleaned)
    cleaned = re.sub(r"\s*[-–—]{2,}\s*", "\n- ", cleaned)
    cleaned = re.sub(r"\s+-\s+(?=[A-Z])", "\n- ", cleaned)
    cleaned = re.sub(r"(?i)\bLocal\s+(?=\d)", "", cleaned)
    cleaned = re.sub(r"\b(websites|website)\.\s+", "", cleaned)
    cleaned = re.sub(r"\s+([,.;:!?])", r"\1", cleaned)
    cleaned = re.sub(r"(?i)\b(?:no\s+)?figure\s+\d+(?:-\d+)?\b", " ", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    chunks = [chunk.strip() for chunk in re.split(r"(?<=[.!?])\s+(?=[A-Z])", cleaned) if chunk.strip()]
    if not chunks:
        return cleaned.strip()
    paragraphs = []
    current = ""
    for chunk in chunks:
        if not current:
            current = chunk
            continue
        if len(current) + 1 + len(chunk) <= 220:
            current = f"{current} {chunk}".strip()
        else:
            paragraphs.append(current)
            current = chunk
    if current:
        paragraphs.append(current)

    sanitized = []
    for para in paragraphs:
        text = re.sub(r"\s+", " ", para).strip()
        if text:
            sanitized.append(text)
    return "\n\n".join(sanitized)


def chunk_text(text: str, chunk_size: int = 1800) -> List[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
    chunks: List[str] = []
    current: List[str] = []
    current_len = 0
    for paragraph in paragraphs:
        if not paragraph:
            continue
        if current_len + len(paragraph) > chunk_size and current:
            chunks.append("\n\n".join(current))
            current = []
            current_len = 0
        current.append(paragraph)
        current_len += len(paragraph)
    if current:
        chunks.append("\n\n".join(current))
    return chunks or [text[:chunk_size]]


def load_book_manifest(book_dir: Path) -> Dict[str, Any]:
    manifest_paths = [book_dir / "parser_manifest.json", book_dir / "book_manifest.json"]
    for manifest_path in manifest_paths:
        if manifest_path.exists():
            try:
                return json.loads(manifest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return {}
    return {}


def load_chapter_files(book_dir: Path, chapter_name: str) -> Dict[str, Any]:
    chapter_dir = book_dir / chapter_name
    content_path = chapter_dir / "content.md"
    if not content_path.exists():
        content_path = chapter_dir / "content_raw.txt"
    texts = content_path.read_text(encoding="utf-8") if content_path.exists() else ""
    manifest_path = chapter_dir / "images_manifest.json"
    images = []
    if manifest_path.exists():
        try:
            images = json.loads(manifest_path.read_text(encoding="utf-8")).get("images", [])
        except json.JSONDecodeError:
            images = []

    parsed_file = book_dir / f"{chapter_name}.json"
    if parsed_file.exists():
        try:
            payload = json.loads(parsed_file.read_text(encoding="utf-8"))
            section = payload.get("section", {})
            if isinstance(section, dict):
                element_text: List[str] = []
                image_entries: List[Dict[str, Any]] = []
                for page in section.get("pages", []):
                    for element in page.get("elements", []):
                        if element.get("type") == "text":
                            text = str(element.get("text", "")).strip()
                            if text:
                                element_text.append(text)
                        elif element.get("type") == "image":
                            image_path = str(element.get("image_path") or "").strip()
                            if image_path:
                                image_entries.append({"relativePath": image_path})
                if element_text:
                    return {
                        "content": normalize_text("\n\n".join(element_text)),
                        "images": image_entries or images,
                        "book_title": payload.get("book_title", book_dir.name),
                        "section": section,
                    }
        except json.JSONDecodeError:
            pass

    return {
        "content": normalize_text(texts),
        "images": images,
    }


def maybe_infer_chapter_number(chapter_name: str) -> int:
    match = re.search(r"(\d+)", chapter_name)
    return int(match.group(1)) if match else 1


def build_glossary_prompt() -> str:
    items = [f"- {term}: {translation}" for term, translation in GLOSSARY.items()]
    return "\n".join(items)


def build_system_prompt(subject: str) -> str:
    return f"""
Create a static English-language MDX chapter page from the supplied source text using FAA-style training wording.

Rules:
- Write every title and heading in English only.
- Preserve the source chapter content as faithfully as possible.
- Keep valid frontmatter fields: title, description, subject, chapterNumber, readTimeMinutes, lang: "en", translationKey.
- Use the handbook subject passed in as the subject value.
- Keep figures and emphasis tags already present in the source.
- Do not invent facts, add quiz questions, or generate AI-style rewrites.
- Do not add any <Quiz /> marker.
- The generated chapter must match the FAA subject: {subject}.

Glossary:
{build_glossary_prompt()}
"""


def build_user_prompt(book_name: str, chapter_name: str, content: str, images: List[Dict[str, Any]], subject: str) -> str:
    image_block = ""
    if images:
        image_block = "\n\nAvailable images:\n" + "\n".join(
            f"- {img.get('figureRef', 'Figure')}: {img.get('relativePath', '')}" for img in images[:8]
        )

    translation_key = translation_key_for(book_name, chapter_name)

    return f"""
Create a static MDX chapter page for {chapter_name} from the book {book_name}.
Subject: {subject}
Translation key: {translation_key}

Source text:
{content[:8000]}

{image_block}

Requirements:
1. Use YAML frontmatter with fields: title, description, subject, chapterNumber, readTimeMinutes, lang, translationKey.
2. Set lang to "en" and use a stable translationKey value matching the chapter, such as "phak-ch01".
3. Keep the lesson content in English and preserve the source text without rewriting it into new AI-generated prose.
4. Use Markdown headings with ## and ###.
5. Preserve any <strong>, <em>, and <figure> markup from the source, including its position in the chapter. Add image placeholders only for images not already embedded there.
6. Do not create any quiz questions, answer keys, or <Quiz /> markers.
7. Keep the chapter concise, practical, and suitable for a PPL student.
"""


def validate_mdx_frontmatter(mdx: str, book_name: str, chapter_name: str, subject: str) -> str:
    if "---" not in mdx:
        raise ValueError(f"MDX output for {book_name}/{chapter_name} is missing frontmatter")

    if contains_non_english_text(mdx):
        raise ValueError(f"MDX output for {book_name}/{chapter_name} contains non-English text")

    required_pairs = {
        "title:": "title",
        "description:": "description",
        "subject:": "subject",
        "chapterNumber:": "chapterNumber",
        "readTimeMinutes:": "readTimeMinutes",
        'lang: "en"': "lang",
        "translationKey:": "translationKey",
    }

    missing = [key for key in required_pairs if key not in mdx]
    if missing:
        raise ValueError(f"MDX output for {book_name}/{chapter_name} is missing required fields: {missing}")

    if f'subject: "{subject}"' not in mdx:
        raise ValueError(f"MDX output for {book_name}/{chapter_name} has an unexpected subject value")

    expected_key = translation_key_for(book_name, chapter_name)
    if f'translationKey: "{expected_key}"' not in mdx:
        raise ValueError(f"MDX output for {book_name}/{chapter_name} has an unexpected translationKey: {expected_key}")

    return mdx


def sanitize_images(images: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    valid: List[Dict[str, Any]] = []
    for img in images:
        rel_path = str(img.get("relativePath") or "").strip()
        if not rel_path:
            continue
        if rel_path.startswith("/images/"):
            valid.append({**img, "relativePath": rel_path})
            continue
        absolute_path = (ROOT / rel_path.lstrip("/")).resolve()
        if absolute_path.exists():
            valid.append(img)
        else:
            public_candidate = (ROOT / "public" / rel_path.lstrip("/")).resolve()
            if public_candidate.exists():
                valid.append({**img, "relativePath": f"/images/{Path(rel_path).name}"})
    return valid


def generate_fallback_mdx(
    book_name: str,
    chapter_name: str,
    content: str,
    images: List[Dict[str, Any]],
    subject: str,
    explicit_title: str | None = None,
) -> str:
    chapter_num = maybe_infer_chapter_number(chapter_name)
    title = explicit_title or infer_title_from_chapter(book_name, chapter_name, subject, content)
    description = f"Reference material for {subject.lower()} chapter {chapter_num}."
    body = normalize_parsed_body(content)
    if not body:
        body = "This chapter introduces the related aircraft principles and operating context."

    read_time = estimate_read_time_minutes(body)
    valid_images = sanitize_images(images)
    image_snippet = ""
    if valid_images:
        top_image = valid_images[0]
        image_path = str(top_image.get("relativePath") or "/images/placeholder.png")
        image_alt = str(top_image.get("figureRef") or "Chapter figure")
        image_snippet = f'\n\n<img src="{image_path}" alt="{image_alt}" />\n\n'

    chapter_key = translation_key_for(book_name, chapter_name)

    mdx = f"""---
title: "{title}"
description: "{description}"
subject: "{subject}"
chapterNumber: {chapter_num}
readTimeMinutes: {read_time}
lang: "en"
translationKey: "{chapter_key}"
---

# {title}

{body}

{image_snippet}
"""

    return validate_mdx_frontmatter(mdx, book_name, chapter_name, subject)


def generate_mdx_for_chapter(book_name: str, chapter_name: str, chapter_payload: Dict[str, Any], subject: str) -> str:
    content = chapter_payload.get("content", "")
    images = chapter_payload.get("images", [])
    explicit_title = chapter_payload.get("title") or (chapter_payload.get("section", {}) or {}).get("title")
    return generate_fallback_mdx(book_name, chapter_name, content, images, subject, explicit_title=explicit_title)


def process_book(book_dir: Path, dry_run: bool = False, serial: bool = False, delay_seconds: float = 0.0) -> None:
    book_name = book_dir.name
    manifest = load_book_manifest(book_dir)
    sections = manifest.get("sections", [])

    if not sections and manifest.get("chapters"):
        sections = manifest["chapters"]

    if not sections:
        chapter_files = sorted(p for p in book_dir.iterdir() if p.is_file() and p.suffix == ".json" and p.name != "parser_manifest.json")
        sections = [{"title": f"Chapter {chapter_file.stem[2:] if chapter_file.stem.startswith('ch') else chapter_file.stem}", "content_path": chapter_file.name} for chapter_file in chapter_files]

    output_dir = DOCS_OUTPUT_ROOT / book_name
    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    default_subject = manifest.get("title") or book_name
    for i, section in enumerate(sections, start=1):
        content_path = str(section.get("content_path") or "")
        chapter_name = Path(content_path).stem if content_path else f"ch{i:02d}"
        payload = load_chapter_files(book_dir, chapter_name)
        payload["title"] = section.get("title") or chapter_name
        payload["book_title"] = payload.get("book_title") or manifest.get("title") or default_subject
        subject = payload.get("book_title") or default_subject
        mdx = generate_mdx_for_chapter(book_name, chapter_name, payload, subject)
        target_path = output_dir / f"{chapter_name}.mdx"
        if dry_run:
            print(f"Dry run: {book_name}/{chapter_name} -> {translation_key_for(book_name, chapter_name)}")
            continue
        target_path.write_text(mdx, encoding="utf-8")
        print(f"Generated: {target_path}")
        if serial and i < len(sections) and delay_seconds > 0:
            time.sleep(delay_seconds)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate MDX lesson pages from parsed PDF chapters")
    parser.add_argument("--book", help="Optional book folder name under resources/parsed")
    parser.add_argument("--dry-run", action="store_true", help="Preview generated chapter metadata without writing MDX files")
    parser.add_argument("--serial", action="store_true", help="Process one chapter at a time with a small delay between chapters to respect quota limits")
    parser.add_argument("--delay-seconds", type=float, default=5.0, help="Seconds to wait between chapters when serial mode is enabled")
    args = parser.parse_args()

    root = PARSED_ROOT
    if not root.exists():
        raise SystemExit(f"Parsed data folder missing: {root}")

    book_dirs = sorted([p for p in root.iterdir() if p.is_dir()])
    if args.book:
        book_dirs = [root / args.book] if (root / args.book).exists() else []

    if not book_dirs:
        raise SystemExit(f"No parsed books found in {root}")

    for book_dir in book_dirs:
        process_book(book_dir, dry_run=args.dry_run, serial=args.serial, delay_seconds=args.delay_seconds)


if __name__ == "__main__":
    main()

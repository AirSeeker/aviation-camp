#!/usr/bin/env python3
"""Generate MDX content from parsed PDF chapters using the Gemini API."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List

from dotenv import load_dotenv
from google import genai
from google.genai import types

ROOT = Path(__file__).resolve().parents[1]
PARSED_ROOT = ROOT / "resources" / "parsed"
DOCS_OUTPUT_ROOT = ROOT / "src" / "content" / "docs"

load_dotenv(ROOT / ".env")

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

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
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
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text.strip()


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
    manifest_path = book_dir / "book_manifest.json"
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
You are a Senior Technical Writer and Certified Flight Instructor (CFI) creating English-language MDX study content grounded in a named FAA reference handbook.

Your task is to convert raw PDF text into clear, accurate MDX study pages. Do not claim that one handbook covers an entire EASA syllabus subject.

Required rules:
- Write all output in English only, including titles, headings, explanations, callouts, and quiz questions.
- Use standard FAA/EASA aviation terminology throughout.
- Do not invent facts that are not supported by the source text.
- Use the supplied handbook name as the subject and use a neutral chapter title unless the source clearly provides a chapter title.
- Preserve operational accuracy and safe training context.
- Use the glossary below when relevant terms appear in the source text.
- Structure the page with a clear progression: introduction, core concepts, practical application, safety considerations, and summary.
- Include short callout blocks in Markdown format such as: > **Attention:** ...
- For images, use JSX tags in the form <img src="/images/..." alt="..." /> when appropriate.
- At the end of the file, include a Quiz JSX component in this exact format:
    <Quiz questions={{[{{ question: '...', options: ['...','...','...','...'], correctAnswer: 0, explanation: '...' }}]}} />
- The content must match the subject: {subject}.
- Every chapter frontmatter must include the required metadata fields: title, description, subject, chapterNumber, readTimeMinutes, lang: "en", translationKey.
- Translation-ready structure: use stable English title text and a unique translationKey such as "phak-ch01".
- Keep jargon accessible to student pilots while retaining correct technical meaning.

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
Create an MDX chapter page for {chapter_name} from the book {book_name}.
Subject: {subject}
Translation key: {translation_key}

Source text:
{content[:8000]}

{image_block}

Output requirements:
1. Use YAML frontmatter with fields: title, description, subject, chapterNumber, readTimeMinutes, lang, translationKey.
2. Set lang to "en" and use a stable translationKey value matching the chapter, such as "phak-ch01".
3. Write the full lesson in English only, including headings, paragraphs, callouts, and quiz questions.
4. Use Markdown headings with ## and ###.
5. Include 2–4 callouts in the form > **Attention:** ...
6. Insert image placeholders in appropriate places using JSX <img src="..." alt="..." />.
7. End the page with a JSX Quiz block containing 3–5 questions.
8. Keep the chapter concise, practical, and suitable for a PPL student.
9. Use standard FAA terminology such as Angle of Attack, Stall, Indicated Airspeed (IAS), and Center of Gravity (CG).
"""


def gemini_client() -> genai.Client:
    api_key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY or GOOGLE_API_KEY is not set")
    return genai.Client(api_key=api_key)


def extract_retry_delay_seconds(exc: Exception) -> float:
    message = str(exc)
    match = re.search(r"Please retry in\s+([0-9.]+)s", message)
    if match:
        return max(1.0, float(match.group(1))) + 1.0
    if "RESOURCE_EXHAUSTED" in message or "UNAVAILABLE" in message:
        return 10.0
    return 0.0


def call_gemini(messages: List[Dict[str, str]], model: str = DEFAULT_MODEL) -> str:
    client = gemini_client()
    system_prompt = next((item["content"] for item in messages if item["role"] == "system"), "")
    user_prompt = "\n\n".join(item["content"] for item in messages if item["role"] == "user")
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.2,
    )
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model,
                contents=user_prompt,
                config=config,
            )
            return response.text or ""
        except Exception as exc:
            delay = extract_retry_delay_seconds(exc)
            if attempt == 2:
                raise
            if delay > 0:
                time.sleep(delay)
            else:
                time.sleep(2 ** attempt)

    return ""


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
        absolute_path = (ROOT / rel_path.lstrip("/")).resolve()
        if absolute_path.exists():
            valid.append(img)
    return valid


def generate_fallback_mdx(book_name: str, chapter_name: str, content: str, images: List[Dict[str, Any]], subject: str) -> str:
    chapter_num = maybe_infer_chapter_number(chapter_name)
    title = infer_title_from_chapter(book_name, chapter_name, subject, content)
    description = f"Learn the key concepts and practical considerations covered in {subject.lower()} for this chapter."
    body = normalize_text(content)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", body) if p.strip()][:6]
    summary = "\n\n".join(paragraphs) if paragraphs else "This chapter introduces the core principles and operational context relevant to the lesson topic."
    read_time = estimate_read_time_minutes(summary)

    valid_images = sanitize_images(images)
    image_snippet = ""
    if valid_images:
        top_image = valid_images[0]
        image_snippet = f'\n\n<img src="{top_image.get("relativePath", "/images/placeholder.png")}" alt="{top_image.get("figureRef", "Illustration")}" />\n\n'

    chapter_key = translation_key_for(book_name, chapter_name)

    quiz = """
<Quiz questions={[
  { question: 'What is the primary purpose of this chapter?', options: ['To explain the core principles and safe operating concepts', 'To replace preflight planning with guesswork', 'To remove the need for checklists', 'To avoid aircraft performance calculations'], correctAnswer: 0, explanation: 'This chapter introduces the foundations needed to understand and apply safe flight concepts correctly.' },
  { question: 'Why is it important to apply these concepts in practice?', options: ['They reduce the risk of errors during flight operations', 'They increase fuel burn without benefit', 'They eliminate the need for situational awareness', 'They make every flight identical'], correctAnswer: 0, explanation: 'Theory becomes useful when it informs decision making, aircraft control, and safe operating habits.' },
  { question: 'Which action best reflects sound flight discipline?', options: ['Follow procedures, verify the conditions, and make informed decisions', 'Ignore changes in flight conditions', 'Rely on memory without checking instruments', 'Disregard the aircraft configuration'], correctAnswer: 0, explanation: 'Sound pilot technique depends on accurate information, disciplined procedures, and clear judgment.' }
]} />
"""

    mdx = f"""---
title: "{title}"
description: "{description}"
subject: "{subject}"
chapterNumber: {chapter_num}
readTimeMinutes: {read_time}
lang: "en"
translationKey: "{chapter_key}"
---

## {title}

{summary}

{image_snippet}

## Key principles

- Understand the core definitions and terminology used in the subject.
- Apply the information to realistic flight scenarios and normal operating conditions.
- Cross-check critical parameters before making decisions during flight.

> **Attention:** Each flight requires continuous attention to aircraft state, environment, and procedural compliance.

> **Remember:** When uncertain, prioritize the safest and most conservative course of action.

## Practical application

- These concepts help you interpret aircraft performance and flight conditions.
- They support sound decision making during normal and abnormal operations.
- They reinforce disciplined, safe, and consistent pilot technique.

{quiz}
"""

    return validate_mdx_frontmatter(mdx, book_name, chapter_name, subject)


def generate_mdx_for_chapter(book_name: str, chapter_name: str, chapter_payload: Dict[str, Any], subject: str) -> str:
    content = chapter_payload.get("content", "")
    images = chapter_payload.get("images", [])
    if not content:
        return generate_fallback_mdx(book_name, chapter_name, "", images, subject)

    try:
        system_prompt = build_system_prompt(subject)
        user_prompt = build_user_prompt(book_name, chapter_name, content, images, subject)
        response = call_gemini([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ])
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:mdx|markdown)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        if "---" in cleaned and "title:" in cleaned:
            if "lang: \"en\"" not in cleaned:
                cleaned = cleaned.replace("readTimeMinutes: ", "readTimeMinutes: ")
                cleaned = cleaned.replace("---\n\n", "---\nlang: \"en\"\ntranslationKey: \"" + translation_key_for(book_name, chapter_name) + "\"\n---\n\n", 1)
            if "translationKey:" not in cleaned:
                cleaned = cleaned.replace("---\n\n", "---\ntranslationKey: \"" + translation_key_for(book_name, chapter_name) + "\"\n---\n\n", 1)
            if "readTimeMinutes:" in cleaned:
                read_minutes = estimate_read_time_minutes(cleaned)
                cleaned = re.sub(r"readTimeMinutes:\s*\d+", f"readTimeMinutes: {read_minutes}", cleaned, count=1)
            if contains_non_english_text(cleaned):
                raise ValueError(f"Generated MDX for {book_name}/{chapter_name} contains non-English text")
            return validate_mdx_frontmatter(cleaned, book_name, chapter_name, subject)
    except Exception as exc:
        print(f"Gemini generation failed for {book_name}/{chapter_name}: {exc}")

    return generate_fallback_mdx(book_name, chapter_name, content, images, subject)


def process_book(book_dir: Path, dry_run: bool = False, serial: bool = False, delay_seconds: float = 0.0) -> None:
    book_name = book_dir.name
    manifest = load_book_manifest(book_dir)
    chapters = manifest.get("chapters", [])
    if not chapters:
        chapter_dirs = sorted([p for p in book_dir.iterdir() if p.is_dir() and p.name.startswith("ch")])
        chapters = [{"chapter": p.name, "startPage": 1, "endPage": 1} for p in chapter_dirs]

    output_dir = DOCS_OUTPUT_ROOT / book_name
    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    for i, chapter in enumerate(chapters, start=1):
        chapter_name = chapter.get("chapter", "ch01")
        chapter_path = book_dir / chapter_name
        payload = load_chapter_files(book_dir, chapter_name)
        subject = source_book_title(book_name)
        mdx = generate_mdx_for_chapter(book_name, chapter_name, payload, subject)
        target_path = output_dir / f"{chapter_name}.mdx"
        if dry_run:
            print(f"Dry run: {book_name}/{chapter_name} -> {translation_key_for(book_name, chapter_name)}")
            continue
        target_path.write_text(mdx, encoding="utf-8")
        print(f"Generated: {target_path}")
        if serial and i < len(chapters) and delay_seconds > 0:
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

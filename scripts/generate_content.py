#!/usr/bin/env python3
"""Generate MDX content from parsed PDF chapters using OpenAI API."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List

from openai import OpenAI
from openai import RateLimitError

ROOT = Path(__file__).resolve().parents[1]
PARSED_ROOT = ROOT / "resources" / "parsed"
DOCS_OUTPUT_ROOT = ROOT / "src" / "content" / "docs"

EASA_SUBJECTS = [
    "Air Law",
    "Aircraft General Knowledge",
    "Flight Performance and Planning",
    "Human Performance",
    "Meteorology",
    "Navigation",
    "Operational Procedures",
    "Principles of Flight",
    "Communications",
]

GLOSSARY = {
    "Angle of Attack": "Кут атаки",
    "Stall": "Звалювання",
    "Indicated Airspeed": "Приладова швидкість (IAS)",
    "True Airspeed": "Дійсна швидкість (TAS)",
    "Groundspeed": "Швидкість над землею",
    "Lift": "Підйомна сила",
    "Drag": "Опір",
    "Thrust": "Тяга",
    "Weight": "Вага",
    "Yaw": "Рискання",
    "Pitch": "Крен/тангаж",
    "Bank": "Крен",
    "Heading": "Курс",
    "Trim": "Тримування",
    "Glide": "Планування",
    "VFR": "Візуальні польоти (VFR)",
    "IFR": "Прилади (IFR)",
    "Holding Pattern": "Петля витримки",
    "Crosswind": "Поперечний вітер",
    "Tailwind": "Попутний вітер",
    "Headwind": "Назустрічний вітер",
    "Density Altitude": "Щільнісна висота",
    "Pressure Altitude": "Барометрична висота",
    "Mach Number": "Число Маха",
    "Minimum Safe Altitude": "Мінімальна безпечна висота",
    "Aviation Weather": "Авіаційна погода",
}

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def subject_for_book(book_name: str) -> str:
    lower_name = book_name.lower()
    mapping = {
        "ppl": "Principles of Flight",
        "afh": "Air Law",
        "instrument": "Navigation",
        "instrumentprocedures": "Operational Procedures",
        "weather": "Meteorology",
        "weightbalance": "Aircraft General Knowledge",
        "riskmanagement": "Human Performance",
        "phak": "Principles of Flight",
        "navigation": "Navigation",
    }
    return mapping.get(lower_name, "Principles of Flight")


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
Ты — опытный редактор авіаційного навчального контенту для EASA PPL. Пиши чітко, доступно та на українській мові.
Твоя задача: перетворити сирий текст PDF на структурований MDX для навчального курсy.

Обов'язкові правила:
- Пиши тільки українською мовою.
- Зберігай авіаційно-технічну точність.
- Не вигадуй факти, які відсутні у тексті.
- Використовуй глосарій нижче, якщо в тексті є відповідні терміни.
- Структуруй текст на рівні: вступ, основні принципи, практичні наслідки, ключові правила, підсумок.
- Додавай короткі інфо-блоки з формулами або правилами у форматі Markdown: > **Увага:** ...
- Для зображень використовуй JSX тег <img src="/images/..." alt="..." /> в тих місцях, де це доречно.
- Для quiz вставляй JSX-компонент у кінці файлу у форматі:
    <Quiz questions={{[{{ question: '...', options: ['...','...','...','...'], correctAnswer: 0, explanation: '...' }}]}} />
- Підтримуй предмет: {subject}.

Глосарій:
{build_glossary_prompt()}
"""


def build_user_prompt(book_name: str, chapter_name: str, content: str, images: List[Dict[str, Any]], subject: str) -> str:
    image_block = ""
    if images:
        image_block = "\n\nНаявні зображення:\n" + "\n".join(
            f"- {img.get('figureRef', 'Figure')}: {img.get('relativePath', '')}" for img in images[:8]
        )

    return f"""
Створи MDX-сторінку для розділу {chapter_name} книги {book_name}.
Предмет: {subject}

Вхідний текст:
{content[:8000]}

{image_block}

Вимоги до результату:
1. Frontmatter у YAML форматі з полями: title, description, subject, chapterNumber, readTimeMinutes.
2. Вміст у Markdown розмітці з заголовками ##, ###.
3. Обов'язково додай 2–4 інфо-блоки > **Увага:** ...
4. Встав різні місця для зображень через JSX вставки <img src="..." />.
5. Наприкінці додай block з 3–5 питань у форматі Quiz у JSX.
6. Створи короткий, але навчально корисний текст, що можна використовувати у PPL-курсі.
7. Пиши в стилі понятному для початківців, але без спрощення авіаційних вимог.
"""


def openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return OpenAI(api_key=api_key)


def call_openai(messages: List[Dict[str, str]], model: str = DEFAULT_MODEL) -> str:
    client = openai_client()
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=messages,
    )
    return response.choices[0].message.content or ""


def generate_fallback_mdx(book_name: str, chapter_name: str, content: str, images: List[Dict[str, Any]], subject: str) -> str:
    chapter_num = maybe_infer_chapter_number(chapter_name)
    title = f"{chapter_name.replace('ch', 'Chapter ').replace('_', ' ').title()}"
    description = f"Навчальний матеріал з {subject.lower()} для розділу {chapter_name}."
    body = normalize_text(content)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", body) if p.strip()][:6]
    summary = "\n\n".join(paragraphs)

    image_snippet = ""
    if images:
        top_image = images[0]
        image_snippet = f'\n\n<img src="{top_image.get("relativePath", "/images/placeholder.png")}" alt="{top_image.get("figureRef", "Illustration")}" />\n\n'

    quiz = """
<Quiz questions={[
  { question: 'Що є ключовим принципом цього розділу?', options: ['Розуміння основних правил і процедур', 'Пропускання перевірки вогню', 'Заміна дисципліни', 'Відмова від обчислень'], correctAnswer: 0, explanation: 'Розділ пояснює основні принципи, які є базою для безпечного виконання польотів.' },
  { question: 'Чому важливо застосовувати отримані знання в практиці?', options: ['Щоб зменшити ризик помилок під час польоту', 'Щоб збільшити витрати пального', 'Щоб уникати перевірок', 'Щоб обмежити навігаційні процедури'], correctAnswer: 0, explanation: 'Теоретичні знання стають корисними лише в поєднанні з практичним застосуванням.' },
  { question: 'Яке правило є найбільш релевантним?', options: ['Дотримуватися процедур і вміти пояснити причину дії', 'Ігнорувати зміни в умовах польоту', 'Спірити з диспетчером', 'Розраховувати без перевірки'], correctAnswer: 0, explanation: 'Ключовий принцип навчання в авіації — надійність процедур та усвідомлення їхнього сенсу.' }
]} />
"""

    return f"""---
title: "{title}"
description: "{description}"
subject: "{subject}"
chapterNumber: {chapter_num}
readTimeMinutes: 8
---

## {title}

{summary}

{image_snippet}

## Ключові принципи

- Розумійте основні дефініції й терміни.
- Застосовуйте правила у реальних польотних сценаріях.
- Контролюйте ризики та перевіряйте важливі параметри перед виконанням маневру.

> **Увага:** Кожен політ вимагає постійного контролю за станом повітряного судна, обстановкою та виконанням процедур.

> **Увача:** У разі невизначеності завжди застосовуйте найбільш безпечні й консервативні рішення.

## Практичні наслідки

- Ці знання допомагають оцінити ситуацію в польоті.
- Вони формують основу для прийняття правильних рішень.
- Вони підтримують безпечну організацію польотів.

{quiz}
"""


def generate_mdx_for_chapter(book_name: str, chapter_name: str, chapter_payload: Dict[str, Any], subject: str) -> str:
    content = chapter_payload.get("content", "")
    images = chapter_payload.get("images", [])
    if not content:
        return generate_fallback_mdx(book_name, chapter_name, "", images, subject)

    try:
        system_prompt = build_system_prompt(subject)
        user_prompt = build_user_prompt(book_name, chapter_name, content, images, subject)
        response = call_openai([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ])
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:mdx|markdown)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        if "---" in cleaned and "title:" in cleaned:
            return cleaned
    except (RuntimeError, RateLimitError, Exception) as exc:
        print(f"OpenAI generation failed for {book_name}/{chapter_name}: {exc}")

    return generate_fallback_mdx(book_name, chapter_name, content, images, subject)


def process_book(book_dir: Path) -> None:
    book_name = book_dir.name
    manifest = load_book_manifest(book_dir)
    chapters = manifest.get("chapters", [])
    if not chapters:
        chapter_dirs = sorted([p for p in book_dir.iterdir() if p.is_dir() and p.name.startswith("ch")])
        chapters = [{"chapter": p.name, "startPage": 1, "endPage": 1} for p in chapter_dirs]

    output_dir = DOCS_OUTPUT_ROOT / book_name
    output_dir.mkdir(parents=True, exist_ok=True)

    for chapter in chapters:
        chapter_name = chapter.get("chapter", "ch01")
        chapter_path = book_dir / chapter_name
        payload = load_chapter_files(book_dir, chapter_name)
        subject = subject_for_book(book_name)
        mdx = generate_mdx_for_chapter(book_name, chapter_name, payload, subject)
        target_path = output_dir / f"{chapter_name}.mdx"
        target_path.write_text(mdx, encoding="utf-8")
        print(f"Generated: {target_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate MDX lesson pages from parsed PDF chapters")
    parser.add_argument("--book", help="Optional book folder name under resources/parsed")
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
        process_book(book_dir)


if __name__ == "__main__":
    main()

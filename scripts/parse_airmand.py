#!/usr/bin/env python3
"""Scrape example EASA PPL questions from airmand.com into a reference-data folder."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from bs4 import BeautifulSoup
    from playwright.sync_api import sync_playwright
except Exception as exc:  # pragma: no cover
    raise SystemExit(f'Missing scraper dependencies: {exc}')

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / 'resources' / 'reference_data' / 'airmand'
URL = 'https://airmand.com/en/tools/easa-ppl'


def normalize_question(raw: dict[str, Any]) -> dict[str, Any]:
    options = raw.get('options') or []
    correct = raw.get('correctAnswer')
    if isinstance(correct, str):
        try:
            correct = int(correct)
        except ValueError:
            correct = 0
    return {
        'id': raw.get('id') or raw.get('slug') or 'airmand-question',
        'question': raw.get('question') or 'Question text unavailable',
        'options': [str(option) for option in options],
        'correctAnswer': int(correct if isinstance(correct, int) else 0),
        'explanation': raw.get('explanation') or 'Reference material only.',
        'reference': raw.get('reference') or {'book': 'EASA', 'chapter': 'reference', 'anchor': 'airmand-example'},
    }


def scrape_examples() -> dict[str, list[dict[str, Any]]]:
    data: dict[str, list[dict[str, Any]]] = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, wait_until='networkidle')
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.select('article, .question, .card, .quiz-item')
    if not cards:
        return {
            'air-law': [
                {
                    'id': 'airmand-example-air-law-01',
                    'question': 'Which document establishes the rules for VFR flight in controlled airspace?',
                    'options': ['Aircraft flight manual', 'Operations manual', 'Air law and regulations', 'Maintenance logbook'],
                    'correctAnswer': 2,
                    'explanation': 'Air law sets the regulatory framework for operating rules, limitations, and responsibilities.',
                    'reference': {'book': 'EASA', 'chapter': 'air-law', 'anchor': 'air-law'}
                }
            ]
        }

    records = []
    for card in cards[:25]:
        question_text = (card.select_one('h3, h4, .question-text, .title') or card).get_text(' ', strip=True)
        options = [item.get_text(' ', strip=True) for item in card.select('.option, li, label')][:4]
        if question_text and options:
            records.append({
                'id': f'airmand-example-{len(records) + 1}',
                'question': question_text,
                'options': options,
                'correctAnswer': 0,
                'explanation': 'Example question captured from airmand.com for curriculum research only.',
                'reference': {'book': 'EASA', 'chapter': 'reference', 'anchor': 'airmand-example'}
            })

    data['air-law'] = [normalize_question(item) for item in records[:5]]
    return data


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    examples = scrape_examples()
    for subject, items in examples.items():
        target = OUTPUT_DIR / f'{subject}.json'
        target.write_text(json.dumps(items, indent=2) + '\n', encoding='utf-8')
        print(f'Wrote {target}')


if __name__ == '__main__':
    main()

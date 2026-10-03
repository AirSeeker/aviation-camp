# Aviation Camp

This project collects, parses, and organizes aviation training manuals into chapter-level content and image assets.

It now includes a polished learning dashboard, dark mode, subject and chapter reader pages, exam practice flow, glossary, and flashcards, all built with a consistent visual system.

For a complete architecture, data-flow, feature, setup, and validation guide, see [PROJECT_GUIDE.md](PROJECT_GUIDE.md).

## Current product highlights

- Modern landing page with handbook cards, quick actions, progress summary, and library navigation
- Dark / light mode toggle with saved preference in local storage
- Unified styling across the home page, subject pages, lesson pages, exam, glossary, and flashcards
- Chapter-based study flow with lesson completion tracking and local progress persistence
- Exam simulator, glossary, and flashcard practice modes for revision and recall

## Included documents

The library includes FAA training material under `resources/library`, including:

- AFH
- Instrument
- InstrumentProcedures
- PHAK
- RiskManagement
- Weather
- WeightBalance

## Parser Library

The PDF processing pipeline lives in:

- `scripts/parser_library.py`

It reads book titles, source URLs, local PDF paths, and section boundaries from
the versioned library manifest, then writes structured output under:

- `output/<book_id>`

The manifest defaults to `resources/library/library_manifest.json`; it can be
provided explicitly when running the processor.

For full parser documentation, see:

- [README_parser.md](README_parser.md)

## Content generator

The content generation pipeline lives in:

- `scripts/generate_content.py`

It uses parsed chapters and the Gemini API to create validated English MDX lessons with quizzes and metadata under `src/content/docs`.

For setup, workflow, CLI options, fallback behavior, and validation, see:

- [README_generator.md](README_generator.md)

## Quiz question banks

Quiz questions live in chapter-scoped JSON files under `content/quizzes/<book>/<chapter>.json`. MDX chapters contain only a self-closing `<Quiz />` marker; the static renderer loads the matching JSON bank automatically.

Each question uses this shape:

```json
{
	"id": "phak-chapter-12-q-01",
	"question": "What is the primary cause of all weather patterns on Earth?",
	"options": ["...", "...", "...", "..."],
	"correctAnswer": 0,
	"explanation": "...",
	"reference": {
		"book": "phak",
		"chapter": "chapter-12",
		"anchor": "earth-atmosphere"
	}
}
```

Run `npm run verify:quizzes` after adding or editing a question. IDs must be unique, `correctAnswer` must point to an option, and every question must include an explanation and source reference.

## Common commands

Activate the environment:

```bash
source .venv/bin/activate
```

Run the PDF processor:

```bash
python scripts/parser_library.py resources/library/library_manifest.json
```

Run the PDF processor tests:

```bash
python -m unittest tests.test_parser_library -v
```

## Notes

- `resources/library/library_manifest.json` is the source of PDF URLs and section page boundaries.
- The existing content generator still reads `resources/parsed`; connecting it to the new processor output is a separate follow-up.

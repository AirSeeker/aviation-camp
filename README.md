# Aviation Camp

This project collects, parses, and organizes aviation training manuals into chapter-level content and image assets.

For a complete architecture, data-flow, feature, setup, and validation guide, see [PROJECT_GUIDE.md](PROJECT_GUIDE.md).

## Included documents

The library includes FAA training material under `resources/library`, including:

- AFH
- Instrument
- InstrumentProcedures
- PHAK
- RiskManagement
- Weather
- WeightBalance

## Parser

The PDF processing pipeline lives in:

- `scripts/parse_pdf.py`

It converts each manual into structured parsed output under:

- `resources/parsed`
- `public/images`

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

Run the parser with the current manifest-based workflow:

```bash
python scripts/parse_pdf.py --workers 1
```

Run the regression tests:

```bash
python -m unittest tests.test_parse_pdf -v
```

## Notes

- Books without a valid `chapters.json` or explicit chapter overrides are skipped rather than auto-split.
- The parser validates document structure, removes repeated page artifacts, deduplicates images, and stages output before publishing it.

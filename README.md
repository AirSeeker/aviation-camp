# Aviation Camp

This project collects, parses, and organizes aviation training manuals into chapter-level content and image assets.

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

## Common commands

Activate the environment:

```bash
source .venv/bin/activate
```

Run the parser in OCR mode:

```bash
python scripts/parse_pdf.py --ocr --workers 1
```

Run the regression tests:

```bash
python -m unittest tests.test_parse_pdf -v
```

## Notes

- OCR requires Tesseract to be installed and available on PATH.
- The parser validates document structure, cleans repeated page artifacts, deduplicates images, and stages output before publishing it.

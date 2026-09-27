# PDF Parser for Aviation Manuals

This project parses FAA aviation manuals from the library folder into chapter-level text files and image manifests.

## Purpose

The parser reads PDFs from `resources/library`, extracts chapter/page structure, captures text content, identifies reusable images, and writes the processed output into `resources/parsed` and `public/images`.

It is designed for training and reference books such as:

- AFH
- Instrument
- InstrumentProcedures
- PHAK
- RiskManagement
- Weather
- WeightBalance

## Main script

- `scripts/parse_pdf.py`

## How it works

The parser performs the following steps:

1. Discovers PDF files under `resources/library`
2. Validates input PDFs and rejects empty or corrupt files
3. Reads explicit chapter page ranges from `chapters.json` next to each PDF, falling back to PDF bookmarks and heading detection when no config exists
4. Excludes pages before the first educational chapter and supplemental sections after the last chapter
5. Extracts text page-by-page
6. Uses OCR fallback when extraction is sparse or weak
7. Cleans repeated header/footer noise
8. Extracts images and deduplicates reused figures
9. Groups pages into chapter output folders
10. Publishes staged output atomically into the final parsed directories

## OCR behavior

OCR is optional and enabled with:

```bash
source .venv/bin/activate
python scripts/parse_pdf.py --ocr
```

The script checks for `tesseract` on the PATH and exits early if it is missing.

Additional OCR tuning options:

```bash
python scripts/parse_pdf.py --ocr --ocr-dpi 300 --ocr-retry-dpi 400 --workers 4
```

- `--ocr-dpi`: main OCR rendering resolution
- `--ocr-retry-dpi`: higher DPI used when sparse pages are retried
- `--workers`: number of PDF books processed in parallel

## Per-book chapter ranges

Each book folder can contain a `chapters.json` file next to its PDF. Ranges use 1-based PDF page numbers and include both endpoints. Pages outside configured ranges, such as the table of contents and appendices, are not parsed as chapter content:

```json
{
  "version": 1,
  "chapters": [
    { "number": 1, "startPage": 22, "endPage": 37 },
    { "number": 2, "startPage": 38, "endPage": 61 }
  ],
  "glossary": { "startPage": 373, "endPage": 391 },
  "acronyms": null,
  "emergencyProcedures": { "startPage": 350, "endPage": 372 },
  "appendices": [
    { "name": "Appendix A - Cloud Types", "startPage": 473, "endPage": 484 }
  ]
}
```

Section ranges are optional; use `null` when a book has no separate section. Appendices are a list of named ranges; use an empty list when a book has no appendices. The parser writes configured sections to `sections/<section>/content.md` and each appendix to `appendices/<name-slug>/content.md`, preserving its display name and page range in `book_manifest.json`. Section ranges and appendix ranges are validated against the PDF; appendices cannot overlap each other. Pages may be skipped between chapter ranges. When a per-book config exists, it takes precedence over automatic detection and the legacy global overrides.

For compatibility, `resources/library/chapter_overrides.json` remains supported as a fallback for PDFs without a local `chapters.json`.

If neither config exists, the parser falls back to PDF bookmarks and chapter-page headings.

## Output structure

### Parsed text

```text
resources/parsed/<BookName>/
  book_manifest.json
  ch01/
    content.md
    images_manifest.json
  ch02/
    content.md
    images_manifest.json
  sections/
    glossary/content.md
    acronyms/content.md
    emergencyProcedures/content.md
  appendices/
    appendix-a-cloud-types/content.md
```

### Images

```text
public/images/<BookName>/
  ch01/
    img_p0001.png
    img_p0002.png
```

## Safety features

The parser includes several safeguards:

- rejects empty or corrupt PDFs
- prevents multiple PDFs from writing to the same output folder
- stages output before publishing
- rolls back on publish failures
- removes stale files after re-runs
- caches parse results by PDF identity and settings

## Running the parser

From the project root:

```bash
source .venv/bin/activate
python scripts/parse_pdf.py --ocr --workers 1
```

To process a single book folder:

```bash
python scripts/parse_pdf.py --book "AFH" --ocr
```

## Validation

The project includes regression tests in:

- `tests/test_parse_pdf.py`

Run them with:

```bash
source .venv/bin/activate
python -m unittest tests.test_parse_pdf -v
```

## Notes

- OCR can be slow, especially for large manuals.
- Some PDFs produce warning messages about sparse extraction; the parser will retry OCR at a higher DPI when appropriate.
- The parser is tuned for high-volume aviation manuals and favors robust parsing over fragile assumptions.

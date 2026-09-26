# PDF Library

Put each source PDF in its own folder under `resources/library`. The folder name is used as the book's output identity.

Add a `chapters.json` file beside each PDF to define exact chapter ranges. Page numbers are 1-based PDF pages and both endpoints are included. Pages outside the ranges (for example, the table of contents and appendices) are excluded:

```json
{
  "version": 1,
  "chapters": [
    { "number": 1, "startPage": 16, "endPage": 39 },
    { "number": 2, "startPage": 40, "endPage": 71 }
  ]
}
```

Ranges must be ordered, within the PDF, and non-overlapping. Gaps between ranges are allowed. The legacy `resources/library/chapter_overrides.json` can still supply chapter start pages when no per-book config exists.

Scanned PDFs can be processed with `--ocr`. This requires Tesseract on `PATH` and the requested language data; set the language with `--ocr-language` and rendering resolution with `--ocr-dpi`.
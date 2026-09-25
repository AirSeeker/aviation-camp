# PDF Library

Put each source PDF in its own folder under `resources/library`. The folder name is used as the book's output identity.

For PDFs whose table of contents does not identify chapters correctly, create `resources/library/chapter_overrides.json` with 1-based PDF page numbers:

```json
{
  "BookFolderName": [1, 14, 27]
}
```

The default file can be overridden with `--chapter-overrides PATH` when running `scripts/parse_pdf.py`.

Scanned PDFs can be processed with `--ocr`. This requires Tesseract on `PATH` and the requested language data; set the language with `--ocr-language` and rendering resolution with `--ocr-dpi`.
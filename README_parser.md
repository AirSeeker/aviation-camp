# PDF Processing

The active PDF pipeline is `scripts/process_pdf_sections.py`. Its input is
`resources/library/library_manifest.json`, a versioned manifest that combines
the download metadata and page boundaries for every library book.

## Run

From the repository root:

```bash
python scripts/process_pdf_sections.py resources/library/library_manifest.json
```

The processor downloads each configured PDF and writes:

```text
output/<book_id>/
  <book_id>.pdf
  parsed_content.json
  images/
```

The manifest records book IDs, PDF URLs and local library paths, SHA-256 hashes,
download metadata, and section boundaries. Chapter, glossary, acronym,
emergency-procedure, and appendix ranges use 1-based PDF page numbers with
inclusive endpoints. Update the boundaries directly in the library manifest.

The processor retries failed downloads and accepts `--timeout`, `--retries`,
and `--output-root` options. It filters content in the top and bottom 5% of
pages, extracts styled text, tables, and images with bounding boxes, and
produces key-value data for glossary and acronym sections.

## Page generator compatibility

The existing `scripts/generate_content.py` still consumes the older
`resources/parsed/<book>/` layout. Wiring its inputs to `parsed_content.json`
under `output/<book_id>/` has not been done yet; update the generator before
using this PDF output to regenerate site pages.

## Tests

```bash
python -m unittest tests.test_process_pdf_sections -v
```

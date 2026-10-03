# Parser Library

The active PDF pipeline is `scripts/parser_library.py`. Its input is
`resources/library/library_manifest.json`, a versioned manifest that combines
the download metadata and page boundaries for every library book.

## Run

From the repository root:

```bash
python scripts/parser_library.py resources/library/library_manifest.json
```

The processor reads all per-book configuration from the version 1 library
manifest. If no manifest path is passed, it uses
`resources/library/library_manifest.json`. For every book, it downloads the PDF
to the manifest's `pdf_path` and writes each parsed section and its extracted
content under `resources/parsed/<book_id>/` and extracted images directly
under `public/images/`.

You can limit the run to a subset of books and process several books at once:

```bash
python scripts/parser_library.py resources/library/library_manifest.json --book AFH --book PHAK --book Weather --jobs 3
```

```text
resources/parsed/<book_id>/
  parser_manifest.json
  ch01.json
  section_002_glossary.json

public/images/
  AFH_p22_b1.png
  PHAK_p1_b1.png
```

Each book folder contains one JSON file per section. Chapters use `chNN.json`
names when the boundary title contains a chapter number; other sections use
numbered, descriptive filenames. Each section file contains book metadata and
that section's content. `parser_manifest.json` indexes the section files and
their page ranges.
Every image filename includes its book ID, PDF page, and image-block number so
names are unique across books. Image paths in section content are web paths in
the form `/images/<filename>`.
The manifest records PDF URLs and local library paths, optional SHA-256 hashes,
download metadata, and section boundaries. Chapter, glossary, acronym,
emergency-procedure, and appendix ranges use 1-based PDF page numbers with
inclusive endpoints. Update the boundaries directly in the library manifest.

The processor retries failed downloads and accepts an optional manifest path,
`--timeout`, `--retries`, `--output-root`, and `--image-root` options. The
output roots default to `resources/parsed` and `public/images`. It filters
content in the top and bottom 5% of pages, extracts styled text, tables, and
images with bounding boxes, and produces key-value data for glossary and
acronym sections.

## Page generator compatibility

The existing `scripts/generate_content.py` still consumes the older
`resources/parsed/<book>/` layout. Wiring its inputs to `parsed_content.json`
under `output/<book_id>/` has not been done yet; update the generator before
using this PDF output to regenerate site pages.

## Tests

```bash
python -m unittest tests.test_parser_library -v
```

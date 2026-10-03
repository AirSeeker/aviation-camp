# PDF Library

`library_manifest.json` is the single source of truth for PDF download
metadata and page boundaries. Each entry includes the book ID, source URL,
local PDF path, optional download metadata, and all chapter/section/appendix
ranges.

Run the processor from the repository root:

```bash
python scripts/parser_library.py resources/library/library_manifest.json
```

Boundary page numbers refer to 1-based PDF pages and include both endpoints.
Edit `library_manifest.json` when updating book metadata or ranges; separate
per-book chapter files and the old download manifest are no longer used.
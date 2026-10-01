#!/usr/bin/env python3
"""Download and refresh aviation reference PDFs when the upstream source changes."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from urllib import request, error

ROOT = Path(__file__).resolve().parent.parent
LIBRARY_DIR = ROOT / 'resources' / 'library'
MANIFEST_PATH = LIBRARY_DIR / 'download_manifest.json'

BOOKS = {
    'PHAK': 'https://www.faa.gov/sites/faa.gov/files/regulations_policies/handbooks_manuals/aviation/phak_full.pdf',
    'AFH': 'https://www.faa.gov/sites/faa.gov/files/10_afh_full_book.pdf',
    'Weather': 'https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-28B.pdf',
    'Instrument': 'https://www.faa.gov/sites/faa.gov/files/regulations_policies/handbooks_manuals/aviation/FAA-H-8083-15B.pdf',
    'InstrumentProcedures': 'https://www.faa.gov/sites/faa.gov/files/regulations_policies/handbooks_manuals/aviation/instrument_procedures_handbook/FAA-H-8083-16B.pdf',
    'RiskManagement': 'https://www.faa.gov/sites/faa.gov/files/regulations_policies/handbooks_manuals/aviation/risk_management_handbook/FAA-H-8083-2A.pdf',
    'WeightBalance': 'https://www.faa.gov/sites/faa.gov/files/regulations_policies/handbooks_manuals/aviation/FAA-H-8083-1A.pdf',
    'Instructor': 'https://www.faa.gov/sites/faa.gov/files/regulations_policies/handbooks_manuals/aviation/aviation_instructors_handbook/faa-h-8083-9b.pdf',
    'EASA_Aircrew': 'https://www.easa.europa.eu/en/downloads/138128/en',
    'EASA_SERA': 'https://www.easa.europa.eu/en/downloads/115485/en',
    'EASA_AirOps': 'https://www.easa.europa.eu/en/downloads/138804/en',
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(65536), b''):
            digest.update(chunk)
    return digest.hexdigest()


def existing_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        return {}
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {}


def is_newer_or_missing(book: str, url: str, file_path: Path, manifest: dict) -> bool:
    previous = manifest.get(book, {})
    if not file_path.exists():
        return True
    if previous.get('sha256') and previous.get('url') == url:
        current_hash = sha256(file_path)
        return current_hash != previous['sha256']
    return True


def fetch_metadata(url: str) -> tuple[str, str]:
    req = request.Request(url, method='HEAD', headers={'User-Agent': 'AviationCampDownloader/1.0'})
    try:
        with request.urlopen(req, timeout=30) as response:
            etag = response.headers.get('ETag', '')
            last_modified = response.headers.get('Last-Modified', '')
            return etag, last_modified
    except Exception:
        return '', ''


def download_pdf(url: str, destination: Path) -> None:
    req = request.Request(url, headers={'User-Agent': 'AviationCampDownloader/1.0'})
    with request.urlopen(req, timeout=60) as response, destination.open('wb') as handle:
        while True:
            chunk = response.read(65536)
            if not chunk:
                break
            handle.write(chunk)


def main() -> None:
    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    manifest = existing_manifest()
    refreshed = dict(manifest)

    for book, url in BOOKS.items():
        book_dir = LIBRARY_DIR / book
        book_dir.mkdir(parents=True, exist_ok=True)
        target = book_dir / f'{book}.pdf'
        etag, last_modified = fetch_metadata(url)
        should_update = is_newer_or_missing(book, url, target, refreshed)

        if should_update:
            try:
                download_pdf(url, target)
            except error.HTTPError as exc:
                print(f'Failed to download {book}: {exc}')
                continue

        final_hash = sha256(target) if target.exists() else ''
        refreshed[book] = {
            'url': url,
            'etag': etag,
            'lastModified': last_modified,
            'sha256': final_hash,
            'path': str(target.relative_to(ROOT)),
        }

    MANIFEST_PATH.write_text(json.dumps(refreshed, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(f'Updated library manifest at {MANIFEST_PATH}')


if __name__ == '__main__':
    main()

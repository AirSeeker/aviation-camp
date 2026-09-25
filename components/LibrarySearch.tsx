'use client';

import Link from 'next/link';
import { Search, X } from 'lucide-react';
import { useDeferredValue, useEffect, useRef, useState } from 'react';

type SearchEntry = {
  book: string;
  chapter: number;
  href: string;
  sourcePageStart?: number;
  sourcePageEnd?: number;
  text: string;
};

export default function LibrarySearch({ basePath }: { basePath: string }) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [entries, setEntries] = useState<SearchEntry[] | null>(null);
  const [loadError, setLoadError] = useState(false);
  const deferredQuery = useDeferredValue(query.trim().toLowerCase());
  const dialogRef = useRef<HTMLDialogElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (open && !dialog.open) {
      dialog.showModal();
      inputRef.current?.focus();
    } else if (!open && dialog.open) {
      dialog.close();
    }
  }, [open]);

  useEffect(() => {
    const handleShortcut = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        setOpen(true);
      }
    };
    window.addEventListener('keydown', handleShortcut);
    return () => window.removeEventListener('keydown', handleShortcut);
  }, []);

  useEffect(() => {
    if (!open || entries) return;
    let cancelled = false;
    fetch(`${basePath}/search-index.json`)
      .then((response) => {
        if (!response.ok) throw new Error('Search index request failed');
        return response.json() as Promise<SearchEntry[]>;
      })
      .then((data) => {
        if (!cancelled) setEntries(data);
      })
      .catch(() => {
        if (!cancelled) setLoadError(true);
      });
    return () => { cancelled = true; };
  }, [open, entries, basePath]);

  const results = deferredQuery && entries
    ? entries.filter((entry) => `${entry.book} chapter ${entry.chapter} ${entry.text}`.toLowerCase().includes(deferredQuery)).slice(0, 12)
    : [];

  return <>
    <button className="search-button" type="button" aria-label="Пошук" onClick={() => setOpen(true)}>
      <Search size={17} /> Пошук <kbd>⌘ K</kbd>
    </button>
    <dialog
      className="search-dialog"
      ref={dialogRef}
      aria-label="Пошук у бібліотеці"
      onCancel={(event) => { event.preventDefault(); setOpen(false); }}
      onClose={() => setOpen(false)}
      onClick={(event) => { if (event.target === dialogRef.current) setOpen(false); }}
    >
      <div className="search-panel">
        <div className="search-input-row">
          <Search size={18} aria-hidden="true" />
          <input
            ref={inputRef}
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Назва довідника, тема або термін"
            aria-label="Пошуковий запит"
          />
          <button className="search-close" type="button" aria-label="Закрити пошук" onClick={() => setOpen(false)}><X size={18} /></button>
        </div>
        <div className="search-results" aria-live="polite">
          {loadError && <p className="search-state">Не вдалося завантажити індекс пошуку.</p>}
          {!entries && !loadError && <p className="search-state">Завантаження бібліотеки…</p>}
          {entries && !deferredQuery && <p className="search-state">Введіть тему, термін або назву довідника.</p>}
          {entries && deferredQuery && results.length === 0 && <p className="search-state">Нічого не знайдено.</p>}
          {results.map((entry) => {
            const matchIndex = entry.text.toLowerCase().indexOf(deferredQuery);
            const start = matchIndex < 0 ? 0 : Math.max(0, matchIndex - 48);
            const excerpt = entry.text.slice(start, start + 150);
            return <Link className="search-result" href={entry.href} key={entry.href} onClick={() => setOpen(false)}>
              <span>{entry.book}{entry.sourcePageStart && entry.sourcePageEnd ? ` · PDF pp. ${entry.sourcePageStart}–${entry.sourcePageEnd}` : ''}</span>
              <strong>Chapter {entry.chapter}</strong>
              <p>{start > 0 ? '…' : ''}{excerpt}{start + 150 < entry.text.length ? '…' : ''}</p>
            </Link>;
          })}
        </div>
      </div>
    </dialog>
  </>;
}
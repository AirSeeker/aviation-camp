'use client';

import { useState } from 'react';

export function TermTooltip({ term, definition }: { term: string; definition: string }) {
  const [open, setOpen] = useState(false);

  return (
    <span className="term-tooltip-shell">
      <button
        type="button"
        className="term-tooltip-trigger"
        onClick={() => setOpen((current) => !current)}
        onMouseEnter={() => setOpen(true)}
        onMouseLeave={() => setOpen(false)}
        onFocus={() => setOpen(true)}
        onBlur={() => setOpen(false)}
      >
        {term}
      </button>
      {open ? (
        <span className="term-tooltip" role="tooltip">
          <strong>{term}</strong>
          <span>{definition}</span>
        </span>
      ) : null}
    </span>
  );
}

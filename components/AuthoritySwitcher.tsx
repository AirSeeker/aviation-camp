'use client';

import { useEffect, useState } from 'react';

export type Authority = 'FAA' | 'EASA';
const STORAGE_KEY = 'aviation-camp:authority';

export function AuthoritySwitcher({ className = '' }: { className?: string }) {
  const [authority, setAuthority] = useState<Authority>('FAA');

  useEffect(() => {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (stored === 'FAA' || stored === 'EASA') setAuthority(stored);
  }, []);

  useEffect(() => {
    window.localStorage.setItem(STORAGE_KEY, authority);
  }, [authority]);

  return (
    <div className={`authority-switcher ${className}`.trim()} aria-label="Authority switcher">
      {(['FAA', 'EASA'] as const).map((value) => (
        <button
          key={value}
          type="button"
          className={authority === value ? 'active' : ''}
          onClick={() => setAuthority(value)}
        >
          {value === 'FAA' ? 'FAA (USA)' : 'EASA (Europe)'}
        </button>
      ))}
    </div>
  );
}

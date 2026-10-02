'use client';

import { MoonStar, SunMedium } from 'lucide-react';
import { useEffect, useState } from 'react';

export function ThemeToggle() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    const savedTheme = window.localStorage.getItem('theme');
    const preferredTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const resolvedTheme = savedTheme === 'light' || savedTheme === 'dark' ? savedTheme : preferredTheme;

    setTheme(resolvedTheme);
    document.documentElement.dataset.theme = resolvedTheme;
  }, []);

  const toggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    document.documentElement.dataset.theme = nextTheme;
    window.localStorage.setItem('theme', nextTheme);
  };

  return (
    <button
      type="button"
      className={`theme-toggle ${theme === 'dark' ? 'is-dark' : ''}`}
      onClick={toggleTheme}
      aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
      title={theme === 'dark' ? 'Light mode' : 'Dark mode'}
    >
      {theme === 'dark' ? <SunMedium size={14} /> : <MoonStar size={14} />}
      <span>{theme === 'dark' ? 'Light' : 'Night'}</span>
    </button>
  );
}

'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Plane } from 'lucide-react';
import terms from '../../../content/dictionary/terms.json';
import abbreviations from '../../../content/dictionary/abbreviations.json';

const STORAGE_KEY = 'aviation-camp:flashcards';
type FlashcardStatus = 'learned' | 'review';
type FlashcardEntry = { term: string; definition: string; category: string };

const entries = [...(terms as FlashcardEntry[]), ...(abbreviations as FlashcardEntry[])].sort((left, right) => left.term.localeCompare(right.term));

export default function FlashcardsPage() {
  const [selected, setSelected] = useState<Record<string, FlashcardStatus>>({});
  const [flipped, setFlipped] = useState<Record<string, boolean>>({});

  useEffect(() => {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (!stored) return;
    try {
      setSelected(JSON.parse(stored));
    } catch {
      window.localStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  useEffect(() => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(selected));
  }, [selected]);

  const stats = useMemo(() => {
    const learned = Object.values(selected).filter((value) => value === 'learned').length;
    const review = Object.values(selected).filter((value) => value === 'review').length;
    return { learned, review, total: entries.length };
  }, [selected]);

  return (
    <main className="reader-shell">
      <header className="reader-topbar">
        <Link className="brand" href="/"><span className="brand-mark"><Plane size={19} /></span><span>Aviation <b>Camp</b></span></Link>
        <Link className="reader-back" href="/glossary/"><ArrowLeft size={15} /> Glossary</Link>
      </header>
      <section className="reader-main">
        <div className="eyebrow muted"><span /> FLASHCARDS / REVISION</div>
        <h1 className="reader-title">Aviation flashcards</h1>
        <p className="reader-summary">Review important terms and abbreviations using spaced repetition. Your progress is saved locally in the browser.</p>
        <div className="flashcard-stats">
          <div><strong>{stats.learned}</strong><span>Learned</span></div>
          <div><strong>{stats.review}</strong><span>Review</span></div>
          <div><strong>{stats.total}</strong><span>Total</span></div>
        </div>
        <div className="flashcard-grid">
          {entries.map((entry) => {
            const status = selected[entry.term] || 'review';
            const isFlipped = flipped[entry.term];

            return (
              <div key={entry.term} className={`flashcard ${isFlipped ? 'flipped' : ''} ${status}`}>
                <button type="button" className="flashcard-face" onClick={() => setFlipped((current) => ({ ...current, [entry.term]: !current[entry.term] }))}>
                  <span className="flashcard-tag">{entry.category}</span>
                  <strong>{entry.term}</strong>
                  <small>{isFlipped ? 'Tap to see term' : 'Tap to reveal definition'}</small>
                </button>
                <div className="flashcard-back">
                  <span className="flashcard-tag">Definition</span>
                  <p>{entry.definition}</p>
                  <div className="flashcard-actions">
                    <button type="button" className={status === 'learned' ? 'active' : ''} onClick={() => setSelected((current) => ({ ...current, [entry.term]: 'learned' }))}>Learned</button>
                    <button type="button" className={status === 'review' ? 'active' : ''} onClick={() => setSelected((current) => ({ ...current, [entry.term]: 'review' }))}>Review</button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>
    </main>
  );
}

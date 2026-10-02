import Link from 'next/link';
import { ArrowLeft, Plane } from 'lucide-react';
import { AuthoritySwitcher } from '../../components/AuthoritySwitcher';
import ExamMode from '../../components/ExamMode';
import { ThemeToggle } from '../../components/ThemeToggle';

export const metadata = {
  title: 'PPL Exam Mode | Aviation Camp',
  description: 'Timed FAA private pilot practice exam.',
};

export default function ExamPage() {
  return (
    <main className="reader-shell">
      <header className="reader-topbar">
        <div className="brand-stack">
          <Link className="brand" href="/">
            <span className="brand-mark"><Plane size={19} /></span>
            <span>Aviation <b>Camp</b></span>
          </Link>
          <AuthoritySwitcher className="inline-authority" />
        </div>

        <div className="reader-nav">
          <ThemeToggle />
          <Link className="reader-back" href="/glossary/">Glossary</Link>
          <Link className="reader-back" href="/glossary/flashcards/">Flashcards</Link>
          <Link className="reader-back" href="/">
            <ArrowLeft size={15} /> Library
          </Link>
        </div>
      </header>

      <section className="reader-main">
        <div className="eyebrow muted"><span /> PPL / PRACTICE</div>
        <h1 className="reader-title">Exam mode</h1>
        <p className="reader-summary">Timed practice with a 70% passing score and source-linked explanations for both FAA and EASA pathways.</p>
        <ExamMode />
      </section>
    </main>
  );
}

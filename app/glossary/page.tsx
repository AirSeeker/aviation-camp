import Link from 'next/link';
import { ArrowLeft, Plane } from 'lucide-react';
import { AuthoritySwitcher } from '../../components/AuthoritySwitcher';
import terms from '../../content/dictionary/terms.json';
import abbreviations from '../../content/dictionary/abbreviations.json';

export const metadata = {
  title: 'Glossary | Aviation Camp',
  description: 'English aviation terms and FAA abbreviations.',
};

const entries = [...terms, ...abbreviations].sort((left, right) => left.term.localeCompare(right.term));

export default function GlossaryPage() {
  return <main className="reader-shell">
    <header className="reader-topbar"><div className="brand-stack"><Link className="brand" href="/"><span className="brand-mark"><Plane size={19} /></span><span>Aviation <b>Camp</b></span></Link><AuthoritySwitcher className="inline-authority" /></div><div className="reader-nav"><Link className="reader-back" href="/exam/">Exam Simulator</Link><Link className="reader-back" href="/glossary/flashcards/">Flashcards</Link><Link className="reader-back" href="/"><ArrowLeft size={15} /> Library</Link></div></header>
    <section className="reader-main"><div className="eyebrow muted"><span /> REFERENCE / GLOSSARY</div><h1 className="reader-title">Glossary</h1><p className="reader-summary">English terms and abbreviations used throughout the study library. Terms have been expanded for both FAA and EASA references.</p><dl className="glossary-list">{entries.map((entry) => <div className="glossary-entry" key={`${entry.category}-${entry.term}`}><dt>{entry.term}<span>{entry.category}</span></dt><dd>{entry.definition}</dd></div>)}</dl></section>
  </main>;
}

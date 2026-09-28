import Link from 'next/link';
import { ArrowLeft, Plane } from 'lucide-react';
import ExamMode from '../../components/ExamMode';

export const metadata = {
  title: 'PPL Exam Mode | Aviation Camp',
  description: 'Timed FAA private pilot practice exam.',
};

export default function ExamPage() {
  return <main className="reader-shell">
    <header className="reader-topbar"><Link className="brand" href="/"><span className="brand-mark"><Plane size={19} /></span><span>Aviation <b>Camp</b></span></Link><Link className="reader-back" href="/"><ArrowLeft size={15} /> Library</Link></header>
    <section className="reader-main"><div className="eyebrow muted"><span /> FAA PPL / PRACTICE</div><h1 className="reader-title">Exam mode</h1><p className="reader-summary">Timed practice with a 70% passing score and source-linked explanations.</p><ExamMode /></section>
  </main>;
}

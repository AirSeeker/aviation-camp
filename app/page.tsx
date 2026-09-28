import Link from 'next/link';
import { ArrowRight, BookOpen, Compass, Plane, ShieldCheck } from 'lucide-react';
import LibrarySearch from '../components/LibrarySearch';
import { StudyProgress } from '../components/StudyProgress';
import { getLessons, pplCategories } from '../src/content/subjects';

const subjects = [
  ['01', 'AFH', 'Airplane Flying Handbook', 'Maneuvers, flight technique, and operating procedures', 'gold', Plane],
  ['02', 'Instrument', 'Instrument Flying Handbook', 'Instrument flight, navigation, and aircraft control', 'blue', Compass],
  ['03', 'InstrumentProcedures', 'Instrument Procedures Handbook', 'Routes, holding patterns, and instrument approaches', 'green', Compass],
  ['04', 'PHAK', "Pilot's Handbook of Aeronautical Knowledge", 'Aircraft, flight, and the national aviation system', 'coral', BookOpen],
  ['05', 'RiskManagement', 'Risk Management Handbook', 'Risk assessment and aeronautical decision-making', 'sky', ShieldCheck],
  ['06', 'Weather', 'Aviation Weather Handbook', 'Atmosphere, forecasts, METAR/TAF, and icing', 'violet', Compass],
  ['07', 'WeightBalance', 'Aircraft Weight and Balance Handbook', 'Aircraft loading, balance, and performance', 'orange', BookOpen],
] as const;

export default async function HomePage() {
  const repositoryName = process.env.GITHUB_REPOSITORY?.split('/')[1] || 'aviation-camp';
  const basePath = process.env.NEXT_PUBLIC_BASE_PATH || (process.env.NODE_ENV === 'production' ? `/${repositoryName}` : '');
  const totalLessons = (await getLessons()).length;

  return <main className="site-shell">
    <aside className="sidebar">
      <Link className="brand" href="/"><span className="brand-mark"><Plane size={19} /></span><span>Aviation <b>Camp</b></span></Link>
      <div className="sidebar-label">FAA / REFERENCE LIBRARY</div>
      <nav className="subject-nav" aria-label="FAA handbooks">{subjects.map(([number, id, title]) => <Link className={`nav-item ${number === '01' ? 'active' : ''}`} href={`/subjects/${id}`} key={id}><span className="nav-number">{number}</span><span>{title}</span></Link>)}</nav>
      <StudyProgress totalLessons={totalLessons} />
    </aside>
    <section className="content">
      <header className="topbar"><div className="breadcrumb"><span>LIBRARY</span><i>/</i> FAA HANDBOOKS</div><LibrarySearch basePath={basePath} /></header>
      <div className="hero"><div className="eyebrow"><span /> FAA PPL STUDY LIBRARY</div><h1>Study with<br /><em>purpose.</em></h1><p className="hero-copy">Free English study material from seven FAA handbooks, organized for private pilot knowledge test preparation.</p><div className="hero-actions"><Link className="primary-action" href="#subjects">Browse handbooks <ArrowRight size={17} /></Link><span className="source-note">FAA source material · {totalLessons} chapters</span></div><div className="hero-stats"><div><strong>07</strong><span>handbooks</span></div><div><strong>{totalLessons}</strong><span>chapters</span></div><div><strong>∞</strong><span>your pace</span></div></div></div>
      <section className="subjects-section" id="ppl-categories"><div className="section-heading"><div><div className="eyebrow muted"><span /> KNOWLEDGE TEST</div><h2>PPL subject areas</h2></div><span className="section-count">09 PPL SUBJECTS</span></div><div className="subject-grid">{pplCategories.map((category, index) => <Link className="subject-card" href={`/subjects/${category.bookId}`} key={category.id}><div className="card-icon sky"><BookOpen size={20} /></div><span className="card-number">{String(index + 1).padStart(2, '0')}</span><h3>{category.title}</h3><p>{category.description}</p><span className="card-arrow"><ArrowRight size={16} /></span></Link>)}</div></section>
      <section className="subjects-section" id="subjects"><div className="section-heading"><div><div className="eyebrow muted"><span /> HANDBOOKS</div><h2>Choose a handbook</h2></div><span className="section-count">07 FAA HANDBOOKS</span></div><div className="subject-grid">{subjects.map(([number, id, title, description, tone, Icon]) => <Link className="subject-card" href={`/subjects/${id}`} key={id}><div className={`card-icon ${tone}`}><Icon size={20} /></div><span className="card-number">{number}</span><h3>{title}</h3><p>{description}</p><span className="card-arrow"><ArrowRight size={16} /></span></Link>)}</div></section>
      <footer className="footer">AVIATION CAMP <span>·</span> STUDY WITH PURPOSE <a href={`${basePath}/content-review-report.json`}>CONTENT REVIEW REPORT</a></footer>
    </section>
  </main>;
}
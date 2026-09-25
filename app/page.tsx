import Link from 'next/link';
import { ArrowRight, BookOpen, Compass, Plane, ShieldCheck } from 'lucide-react';
import LibrarySearch from '../components/LibrarySearch';
import { StudyProgress } from '../components/StudyProgress';
import { getLessons } from '../src/content/subjects';

const subjects = [
  ['01', 'AFH', 'Airplane Flying Handbook', 'Маневрування, техніка пілотування та процедури', 'gold', Plane],
  ['02', 'Instrument', 'Instrument Flying Handbook', 'Приладовий політ, навігація та контроль повітряного судна', 'blue', Compass],
  ['03', 'InstrumentProcedures', 'Instrument Procedures Handbook', 'Маршрути, схеми очікування та заходи на посадку', 'green', Compass],
  ['04', 'PHAK', "Pilot's Handbook of Aeronautical Knowledge", 'Базові знання про літак, політ та авіаційну систему', 'coral', BookOpen],
  ['05', 'RiskManagement', 'Risk Management Handbook', 'Оцінювання ризиків та прийняття рішень пілотом', 'sky', ShieldCheck],
  ['06', 'Weather', 'Aviation Weather Handbook', 'Атмосфера, прогнози, METAR/TAF та обледеніння', 'violet', Compass],
  ['07', 'WeightBalance', 'Aircraft Weight and Balance Handbook', 'Завантаження, центрування та маса літака', 'orange', BookOpen],
] as const;

export default async function HomePage() {
  const repositoryName = process.env.GITHUB_REPOSITORY?.split('/')[1] || 'aviation-camp';
  const basePath = process.env.NEXT_PUBLIC_BASE_PATH || (process.env.NODE_ENV === 'production' ? `/${repositoryName}` : '');
  const totalLessons = (await getLessons()).length;

  return <main className="site-shell">
    <aside className="sidebar">
      <Link className="brand" href="/"><span className="brand-mark"><Plane size={19} /></span><span>Aviation <b>Camp</b></span></Link>
      <div className="sidebar-label">FAA / REFERENCE LIBRARY</div>
      <nav className="subject-nav" aria-label="Довідники FAA">{subjects.map(([number, id, title]) => <Link className={`nav-item ${number === '01' ? 'active' : ''}`} href={`/subjects/${id}`} key={id}><span className="nav-number">{number}</span><span>{title}</span></Link>)}</nav>
      <StudyProgress totalLessons={totalLessons} />
    </aside>
    <section className="content">
      <header className="topbar"><div className="breadcrumb"><span>LIBRARY</span><i>/</i> FAA HANDBOOKS</div><LibrarySearch basePath={basePath} /></header>
      <div className="hero"><div className="eyebrow"><span /> АВІАЦІЙНІ ДОВІДНИКИ FAA</div><h1>Курс, який тримає<br /><em>висоту.</em></h1><p className="hero-copy">Навчальні матеріали з семи довідників FAA: від техніки пілотування та навігації до погоди, ризиків і центрування літака.</p><div className="hero-actions"><Link className="primary-action" href="#subjects">Переглянути довідники <ArrowRight size={17} /></Link><span className="source-note">Оригінальні джерела FAA · 125 розділів</span></div><div className="hero-stats"><div><strong>07</strong><span>довідників</span></div><div><strong>125</strong><span>розділів</span></div><div><strong>∞</strong><span>у вашому темпі</span></div></div></div>
      <section className="subjects-section" id="subjects"><div className="section-heading"><div><div className="eyebrow muted"><span /> БІБЛІОТЕКА ДЖЕРЕЛ</div><h2>Оберіть довідник</h2></div><span className="section-count">07 FAA HANDBOOKS</span></div><div className="subject-grid">{subjects.map(([number, id, title, description, tone, Icon]) => <Link className="subject-card" href={`/subjects/${id}`} key={id}><div className={`card-icon ${tone}`}><Icon size={20} /></div><span className="card-number">{number}</span><h3>{title}</h3><p>{description}</p><span className="card-arrow"><ArrowRight size={16} /></span></Link>)}</div></section>
      <footer className="footer">AVIATION CAMP <span>·</span> STUDY WITH PURPOSE <a href={`${basePath}/content-review-report.json`}>ЗВІТ ПЕРЕВІРКИ МАТЕРІАЛІВ</a></footer>
    </section>
  </main>;
}
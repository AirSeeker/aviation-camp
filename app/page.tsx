import Link from 'next/link';
import { ArrowRight, BookOpen, CheckCircle2, Compass, Plane, Radio, Search } from 'lucide-react';

const subjects = [
  ['01', 'Air Law', 'SERA, класи повітряного простору та документація', 'gold', Compass],
  ['02', 'Aircraft General Knowledge', 'Планер, двигун, системи та авіаційні прилади', 'blue', Plane],
  ['03', 'Flight Performance & Planning', 'Центрування, завантаження та льотні характеристики', 'green', BookOpen],
  ['04', 'Human Performance', 'Фізіологія, ADM та обмеження пілота', 'coral', CheckCircle2],
  ['05', 'Meteorology', 'Атмосфера, фронти, METAR/TAF та обледеніння', 'sky', Compass],
  ['06', 'Navigation', 'Карти, VOR/NDB/GPS, вітер і E6B', 'violet', Compass],
  ['07', 'Operational Procedures', 'Відмови, аварійні та особливі процедури', 'orange', BookOpen],
  ['08', 'Principles of Flight', 'Підйомна сила, опір, stall і стабільність', 'teal', Plane],
  ['09', 'Communications', 'VFR-фразеологія, Pan-Pan та Mayday', 'red', Radio],
] as const;

export default function HomePage() {
  return <main className="site-shell">
    <aside className="sidebar">
      <Link className="brand" href="/"><span className="brand-mark"><Plane size={19} /></span><span>Aviation <b>Camp</b></span></Link>
      <div className="sidebar-label">EASA PPL / GROUND SCHOOL</div>
      <nav className="subject-nav" aria-label="Предмети курсу">{subjects.map(([number, title]) => <Link className={`nav-item ${number === '01' ? 'active' : ''}`} href={`/#${title.toLowerCase().replaceAll(' ', '-')}`} key={number}><span className="nav-number">{number}</span><span>{title}</span></Link>)}</nav>
      <div className="sidebar-footer"><div className="progress-meta"><span>Ваш прогрес</span><strong>0%</strong></div><div className="progress-track"><span /></div><p>Почніть з будь-якого предмета. Результати зберігаються у цьому браузері.</p></div>
    </aside>
    <section className="content">
      <header className="topbar"><div className="breadcrumb"><span>КУРС</span><i>/</i> EASA PRIVATE PILOT LICENCE</div><button className="search-button" type="button" aria-label="Пошук"><Search size={17} /> Пошук <kbd>⌘ K</kbd></button></header>
      <div className="hero"><div className="eyebrow"><span /> ПІДГОТОВКА ДО ТЕОРЕТИЧНОГО ІСПИТУ</div><h1>Курс, який тримає<br /><em>висоту.</em></h1><p className="hero-copy">Дев’ять офіційних предметів EASA PPL, інтерактивні пояснення та практика, що перетворює знання на впевнені рішення в польоті.</p><div className="hero-actions"><Link className="primary-action" href="#subjects">Розпочати навчання <ArrowRight size={17} /></Link><span className="source-note">На основі Part-FCL · SERA · PHAK</span></div><div className="hero-stats"><div><strong>09</strong><span>предметів</span></div><div><strong>100%</strong><span>у вашому темпі</span></div><div><strong>∞</strong><span>спроб тестів</span></div></div></div>
      <section className="subjects-section" id="subjects"><div className="section-heading"><div><div className="eyebrow muted"><span /> НАВЧАЛЬНА ПРОГРАМА</div><h2>Оберіть предмет</h2></div><span className="section-count">09 MODULES / 2026</span></div><div className="subject-grid">{subjects.map(([number, title, description, tone, Icon]) => <Link className="subject-card" id={title.toLowerCase().replaceAll(' ', '-')} href={`/subjects/${number}`} key={number}><div className={`card-icon ${tone}`}><Icon size={20} /></div><span className="card-number">{number}</span><h3>{title}</h3><p>{description}</p><span className="card-arrow"><ArrowRight size={16} /></span></Link>)}</div></section>
      <footer className="footer">AVIATION CAMP <span>·</span> STUDY WITH PURPOSE</footer>
    </section>
  </main>;
}
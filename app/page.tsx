import Link from 'next/link';
import { ArrowRight, BookOpen, ClipboardCheck, Compass, NotebookPen, Plane, ShieldCheck, Sparkles } from 'lucide-react';
import { AuthoritySwitcher } from '../components/AuthoritySwitcher';
import LibrarySearch from '../components/LibrarySearch';
import { StudyProgress } from '../components/StudyProgress';
import { ThemeToggle } from '../components/ThemeToggle';
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

const quickActions = [
  { title: 'Start learning', description: 'Jump into the core FAA handbook sequence.', href: '/subjects/AFH', icon: Sparkles },
  { title: 'Practice exam', description: 'Test your recall with the simulator.', href: '/exam/', icon: ClipboardCheck },
  { title: 'Glossary', description: 'Refresh terms and acronyms in a minute.', href: '/glossary/', icon: NotebookPen },
] as const;

export default async function HomePage() {
  const repositoryName = process.env.GITHUB_REPOSITORY?.split('/')[1] || 'aviation-camp';
  const basePath = process.env.NEXT_PUBLIC_BASE_PATH || (process.env.NODE_ENV === 'production' ? `/${repositoryName}` : '');
  const totalLessons = (await getLessons()).length;

  return (
    <main className="site-shell home-shell">
      <aside className="sidebar">
        <div className="brand-row">
          <Link className="brand" href="/">
            <span className="brand-mark"><Plane size={19} /></span>
            <span>Aviation <b>Camp</b></span>
          </Link>
        </div>

        <AuthoritySwitcher className="sidebar-authority" />

        <div className="sidebar-label">FAA / EASA / REFERENCE LIBRARY</div>

        <nav className="subject-nav" aria-label="Study paths">
          {subjects.map(([number, id, title]) => (
            <Link className={`nav-item ${number === '01' ? 'active' : ''}`} href={`/subjects/${id}`} key={id}>
              <span className="nav-number">{number}</span>
              <span>{title}</span>
            </Link>
          ))}
        </nav>

        <div className="utility-nav">
          <Link className="nav-item" href="/exam/">Exam Simulator</Link>
          <Link className="nav-item" href="/glossary/">Glossary</Link>
          <Link className="nav-item" href="/glossary/flashcards/">Flashcards</Link>
        </div>

        <StudyProgress totalLessons={totalLessons} />
      </aside>

      <section className="content">
        <header className="topbar">
          <div className="breadcrumb"><span>LIBRARY</span><i>/</i> FAA / EASA HANDBOOKS</div>
          <div className="topbar-tools">
            <ThemeToggle />
            <AuthoritySwitcher className="inline-authority" />
            <LibrarySearch basePath={basePath} />
          </div>
        </header>

        <div className="dashboard-body">
          <section className="hero hero-modern">
            <div className="hero-copy">
              <div className="eyebrow"><span /> PRACTICE WITH PURPOSE</div>
              <h1>
                Build your pilot knowledge
                <em>without the chaos.</em>
              </h1>
              <p className="hero-copy-text">
                Clear, structured study material from FAA and EASA references, designed to help you prepare for
                PPL knowledge tests and fly with more confidence.
              </p>

              <div className="hero-actions">
                <Link className="primary-action" href="#subjects">Browse handbooks <ArrowRight size={17} /></Link>
                <Link className="secondary-action" href="/exam/">Exam simulator</Link>
              </div>

              <div className="hero-meta">
                <span>07 handbooks</span>
                <span>{totalLessons} chapter groups</span>
                <span>Flexible pace</span>
              </div>
            </div>

            <div className="hero-panel">
              <div className="panel-header">
                <span>Today&apos;s focus</span>
                <strong>Study flow</strong>
              </div>

              <div className="focus-score">
                <strong>82%</strong>
                <small>core knowledge coverage</small>
              </div>

              <ul className="focus-list">
                <li><span className="dot success" /> Aircraft systems</li>
                <li><span className="dot success" /> Weather interpretation</li>
                <li><span className="dot accent" /> Airspace and procedures</li>
              </ul>
            </div>
          </section>

          <section className="feature-grid" aria-label="Quick actions">
            {quickActions.map(({ title, description, href, icon: Icon }) => (
              <Link className="feature-card" href={href} key={title}>
                <div className="feature-card__icon">
                  <Icon size={18} />
                </div>
                <h3>{title}</h3>
                <p>{description}</p>
                <span className="feature-card__link">
                  Open <ArrowRight size={14} />
                </span>
              </Link>
            ))}
          </section>

          <section className="subjects-section" id="ppl-categories">
            <div className="section-heading">
              <div>
                <div className="eyebrow muted"><span /> KNOWLEDGE TEST</div>
                <h2>PPL subject areas</h2>
              </div>
              <span className="section-count">09 PPL SUBJECTS</span>
            </div>
            <div className="subject-grid">
              {pplCategories.map((category, index) => (
                <Link className="subject-card" href={`/subjects/${category.bookId}`} key={category.id}>
                  <div className="card-icon sky"><BookOpen size={20} /></div>
                  <span className="card-number">{String(index + 1).padStart(2, '0')}</span>
                  <h3>{category.title}</h3>
                  <p>{category.description}</p>
                  <span className="card-arrow"><ArrowRight size={16} /></span>
                </Link>
              ))}
            </div>
          </section>

          <section className="subjects-section" id="subjects">
            <div className="section-heading">
              <div>
                <div className="eyebrow muted"><span /> HANDBOOKS</div>
                <h2>Choose a handbook</h2>
              </div>
              <span className="section-count">07 FAA HANDBOOKS</span>
            </div>

            <div className="subject-grid">
              {subjects.map(([number, id, title, description, tone, Icon]) => (
                <Link className="subject-card" href={`/subjects/${id}`} key={id}>
                  <div className={`card-icon ${tone}`}><Icon size={20} /></div>
                  <span className="card-number">{number}</span>
                  <h3>{title}</h3>
                  <p>{description}</p>
                  <span className="card-arrow"><ArrowRight size={16} /></span>
                </Link>
              ))}
            </div>
          </section>
        </div>

        <footer className="footer">
          AVIATION CAMP <span>·</span> STUDY WITH PURPOSE
          <a href={`${basePath}/content-review-report.json`}>CONTENT REVIEW REPORT</a>
        </footer>
      </section>
    </main>
  );
}

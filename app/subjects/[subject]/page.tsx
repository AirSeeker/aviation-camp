import Link from 'next/link';
import { ArrowLeft, ArrowRight, BookOpen, Plane } from 'lucide-react';
import { ThemeToggle } from '../../../components/ThemeToggle';
import { getLessonsForBook, subjects } from '../../../src/content/subjects';

export const dynamicParams = false;

export function generateStaticParams() {
  return subjects.map(({ id }) => ({ subject: id }));
}

export default async function SubjectPage({ params }: { params: { subject: string } }) {
  const subject = subjects.find((item) => item.id === params.subject);
  if (!subject) return null;
  const lessons = await getLessonsForBook(subject.id);

  return (
    <main className="reader-shell">
      <header className="reader-topbar">
        <Link className="brand" href="/">
          <span className="brand-mark"><Plane size={19} /></span>
          <span>Aviation <b>Camp</b></span>
        </Link>

        <div className="reader-nav">
          <ThemeToggle />
          <Link className="reader-back" href="/">
            <ArrowLeft size={15} /> All subjects
          </Link>
        </div>
      </header>

      <section className="reader-main subject-panel">
        <div className="eyebrow muted"><span /> FAA HANDBOOK / REFERENCE LIBRARY</div>

        <div className="subject-hero">
          <div>
            <h1 className="reader-title">{subject.title}</h1>
            <p className="reader-summary">{lessons.length} chapters in this handbook</p>
          </div>
          <div className="subject-hero-stat">
            <strong>{lessons.length}</strong>
            <span>Lessons</span>
          </div>
        </div>

        {lessons.length > 0 && (
          <ol className="lesson-list">
            {lessons.map((lesson) => (
              <li key={`${lesson.book}-${lesson.slug}`}>
                <Link href={`/subjects/${subject.id}/${lesson.slug}`}>
                  <span className="lesson-icon"><BookOpen size={18} /></span>
                  <span className="lesson-details">
                    <strong>Chapter {lesson.chapterNumber}</strong>
                    <small>{lesson.readTimeMinutes} MIN READ</small>
                  </span>
                  <ArrowRight className="lesson-arrow" size={17} />
                </Link>
              </li>
            ))}
          </ol>
        )}
      </section>
    </main>
  );
}
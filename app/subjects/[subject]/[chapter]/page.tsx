import Link from 'next/link';
import { compileMDX } from 'next-mdx-remote/rsc';
import { existsSync } from 'node:fs';
import { readFile } from 'node:fs/promises';
import type { ReactNode } from 'react';
import path from 'node:path';
import { ArrowLeft, Plane } from 'lucide-react';
import Quiz from '../../../../components/Quiz';
import { LessonCompletion } from '../../../../components/StudyProgress';
import { getLessons, subjects } from '../../../../src/content/subjects';

export const dynamicParams = false;

type LessonFigure = { relativePath: string; figureRef?: string; page?: number };

async function getLessonFigures(book: string, chapter: string, source: string): Promise<LessonFigure[]> {
  try {
    const manifestPath = path.join(process.cwd(), 'resources', 'parsed', book, chapter, 'images_manifest.json');
    const manifest = JSON.parse(await readFile(manifestPath, 'utf8')) as { images?: LessonFigure[] };
    return (manifest.images || [])
      .filter((image) => image.relativePath?.startsWith('/images/') && !source.includes(image.relativePath))
      .slice(0, 8);
  } catch {
    return [];
  }
}

function LessonImage({ src, alt }: { src?: string; alt?: string }) {
  const imagesRoot = path.resolve(process.cwd(), 'public', 'images');
  const imagePath = src?.startsWith('/images/') ? path.resolve(process.cwd(), 'public', src.slice(1)) : '';
  if (!imagePath || !imagePath.startsWith(`${imagesRoot}${path.sep}`) || !existsSync(imagePath)) {
    return alt ? <p className="image-unavailable">Illustration unavailable: {alt}</p> : null;
  }

  const repositoryName = process.env.GITHUB_REPOSITORY?.split('/')[1] || 'aviation-camp';
  const basePath = process.env.NEXT_PUBLIC_BASE_PATH || (process.env.NODE_ENV === 'production' ? `/${repositoryName}` : '');
  return <img src={`${basePath}${src}`} alt={alt || ''} loading="lazy" />;
}

export async function generateStaticParams() {
  const lessons = await getLessons();
  return lessons.flatMap((lesson) => {
    const subject = subjects.find((item) => item.id === lesson.book);
    return subject ? [{ subject: subject.id, chapter: lesson.slug }] : [];
  });
}

export default async function LessonPage({ params }: { params: { subject: string; chapter: string } }) {
  const subject = subjects.find((item) => item.id === params.subject);
  const lesson = (await getLessons()).find((item) => item.slug === params.chapter && item.book === subject?.id);
  if (!subject || !lesson) return null;

  const figures = await getLessonFigures(subject.id, lesson.slug, lesson.source);
  let content: ReactNode;
  const lessonId = `${subject.id}/${lesson.slug}`;
  try {
    const source = lesson.source.replace(/\{([A-Za-z][A-Za-z ]*)\}/g, '$1');
    ({ content } = await compileMDX({
      source,
      components: {
        Quiz: (props: { questions: Parameters<typeof Quiz>[0]['questions'] }) => <Quiz {...props} lessonId={lessonId} />,
        img: LessonImage,
      },
    }));
  } catch {
    const paragraphs = lesson.source.replace(/<Quiz\b[\s\S]*?\/>/g, '')
      .replace(/<img\b[^>]*\/?\s*>/g, '').replace(/^#{1,6}\s*/gm, '').replace(/^\s*[-*>]\s*/gm, '').replace(/[*_`]/g, '')
      .split(/\n\s*\n/).map((paragraph) => paragraph.trim()).filter(Boolean);
    content = <div>{paragraphs.map((paragraph, index) => <p key={index}>{paragraph.replace(/\n/g, ' ')}</p>)}</div>;
  }

  return <main className="reader-shell">
    <header className="reader-topbar">
      <Link className="brand" href="/"><span className="brand-mark"><Plane size={19} /></span><span>Aviation <b>Camp</b></span></Link>
      <Link className="reader-back" href={`/subjects/${subject.id}/`}><ArrowLeft size={15} /> {subject.title}</Link>
    </header>
    <article className="reader-main lesson-article">
      <div className="eyebrow muted"><span /> {subject.title.toUpperCase()} / CHAPTER {String(lesson.chapterNumber).padStart(2, '0')}</div>
      <h1 className="reader-title">Chapter {lesson.chapterNumber}</h1>
      <p className="reader-summary">{lesson.readTimeMinutes} min read</p>
      {lesson.sourcePageStart && lesson.sourcePageEnd && <p className="source-citation">Source: {subject.title}, PDF pp. {lesson.sourcePageStart}–{lesson.sourcePageEnd}</p>}
      <LessonCompletion lessonId={lessonId} />
      <div className="lesson-content">{content}</div>
      {figures.length > 0 && <section className="lesson-figures" aria-label="Chapter illustrations">
        {figures.map((figure, index) => <figure key={figure.relativePath}>
          <LessonImage src={figure.relativePath} alt={figure.figureRef || `Illustration ${index + 1}`} />
          <figcaption>{figure.figureRef || `Illustration ${index + 1}`}{figure.page ? ` · PDF p. ${figure.page}` : ''}</figcaption>
        </figure>)}
      </section>}
    </article>
  </main>;
}
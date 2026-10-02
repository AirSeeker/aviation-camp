import Link from 'next/link';
import { compileMDX } from 'next-mdx-remote/rsc';
import { existsSync } from 'node:fs';
import { readFile } from 'node:fs/promises';
import type { ReactNode } from 'react';
import path from 'node:path';
import { ArrowLeft, Plane } from 'lucide-react';
import { ThemeToggle } from '../../../../components/ThemeToggle';
import { TermTooltip } from '../../../../components/TermTooltip';
import Quiz from '../../../../components/Quiz';
import { VoiceReader } from '../../../../components/VoiceReader';
import { LessonCompletion } from '../../../../components/StudyProgress';
import terms from '../../../../content/dictionary/terms.json';
import abbreviations from '../../../../content/dictionary/abbreviations.json';
import { getLessons, subjects } from '../../../../src/content/subjects';

export const dynamicParams = false;

type LessonFigure = { relativePath: string; figureRef?: string; page?: number; placements?: { renderInContent?: boolean }[] };
type QuizQuestion = { id?: string; question: string; options: string[]; correctAnswer: number; explanation: string; reference?: { book: string; chapter: string; anchor: string } };

async function getLessonQuiz(book: string, chapter: string): Promise<QuizQuestion[]> {
  try {
    const quizPath = path.join(process.cwd(), 'content', 'quizzes', book, `${chapter}.json`);
    return JSON.parse(await readFile(quizPath, 'utf8')) as QuizQuestion[];
  } catch {
    return [];
  }
}

async function getLessonFigures(book: string, chapter: string, source: string): Promise<LessonFigure[]> {
  try {
    const manifestPath = path.join(process.cwd(), 'resources', 'parsed', book, chapter, 'images_manifest.json');
    const manifest = JSON.parse(await readFile(manifestPath, 'utf8')) as { images?: LessonFigure[] };
    return (manifest.images || [])
      .filter((image) => image.relativePath?.startsWith('/images/') && !source.includes(image.relativePath)
        && (!image.placements?.length || image.placements.some((placement) => placement.renderInContent !== false)))
  } catch {
    return [];
  }
}

function insertLessonFigures(source: string, figures: LessonFigure[], startPage?: number, endPage?: number): string {
  if (figures.length === 0) return source;

  const frontmatter = source.match(/^---\s*\n[\s\S]*?\n---\s*/);
  const prefix = frontmatter?.[0] || '';
  const remaining = source.slice(prefix.length);
  const quizStart = remaining.search(/<Quiz\b/);
  const body = quizStart < 0 ? remaining : remaining.slice(0, quizStart);
  const quiz = quizStart < 0 ? '' : remaining.slice(quizStart);
  const blocks = body.split(/\n\s*\n/);
  const textBlockIndexes = blocks.flatMap((block, index) => {
    const text = block.replace(/<[^>]+>/g, '').replace(/[#>*_`~\-\d.]/g, '').trim();
    return text ? [index] : [];
  });
  if (textBlockIndexes.length === 0) return source;

  const insertions = new Map<number, string[]>();
  figures.forEach((figure, index) => {
    const pageProgress = figure.page && startPage && endPage && endPage >= startPage
      ? Math.max(0, Math.min(1, (figure.page - startPage + 1) / (endPage - startPage + 1)))
      : (index + 1) / (figures.length + 1);
    const targetIndex = textBlockIndexes[Math.max(0, Math.ceil(pageProgress * textBlockIndexes.length) - 1)] ?? textBlockIndexes.at(-1)!;
    const label = figure.figureRef || `Illustration ${index + 1}`;
    const pageLabel = figure.page ? ` · PDF p. ${figure.page}` : '';
    const figureMarkup = `<figure>\n<img src="${figure.relativePath}" alt="${label}" />\n<figcaption>${label}${pageLabel}</figcaption>\n</figure>`;
    insertions.set(targetIndex, [...(insertions.get(targetIndex) || []), figureMarkup]);
  });

  const content = blocks.flatMap((block, index) => [block, ...(insertions.get(index) || [])]).join('\n\n');
  return `${prefix}${content}${quiz}`;
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

function escapeRegExp(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function applyTermTooltips(source: string): string {
  const glossary = [...(terms as Array<{ term: string; definition: string }>), ...(abbreviations as Array<{ term: string; definition: string }>)];
  const entries = glossary.filter((entry) => entry.term && entry.definition).sort((left, right) => right.term.length - left.term.length);

  let result = source;
  for (const entry of entries) {
    const expression = new RegExp(`\\b${escapeRegExp(entry.term)}\\b`, 'gi');
    result = result.replace(expression, (match) => `<TermTooltip term="${match.replace(/"/g, '&quot;')}" definition="${entry.definition.replace(/"/g, '&quot;')}" />`);
  }
  return result;
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
  const quizQuestions = await getLessonQuiz(subject.id, lesson.slug);
  let content: ReactNode;
  const lessonId = `${subject.id}/${lesson.slug}`;
  const source = applyTermTooltips(insertLessonFigures(lesson.source, figures, lesson.sourcePageStart, lesson.sourcePageEnd)
    .replace(/\{([A-Za-z][A-Za-z ]*)\}/g, '$1'));
  try {
    ({ content } = await compileMDX({
      source,
      components: {
        Quiz: () => quizQuestions.length > 0 ? <Quiz questions={quizQuestions} lessonId={lessonId} /> : null,
        TermTooltip,
        img: LessonImage,
      },
    }));
  } catch {
    const fallbackContent = source.replace(/<Quiz\b[\s\S]*?\/>/g, '');
    const contentParts = fallbackContent.split(/(<figure\b[\s\S]*?<\/figure>|<img\b[^>]*\/?\s*>)/g);
    const fallbackBlocks: ReactNode[] = [];
    contentParts.forEach((part, index) => {
      const image = part.match(/<img\b[^>]*\bsrc="([^"]+)"[^>]*>/);
      if (image) {
        const alt = part.match(/\balt="([^"]*)"/)?.[1] || '';
        const caption = part.match(/<figcaption>([\s\S]*?)<\/figcaption>/)?.[1];
        fallbackBlocks.push(<figure key={`figure-${index}`}><LessonImage src={image[1]} alt={alt} />{caption && <figcaption>{caption}</figcaption>}</figure>);
        return;
      }

      const paragraphs = part.replace(/^#{1,6}\s*/gm, '').replace(/^\s*[-*>]\s*/gm, '').replace(/[*_`]/g, '')
        .split(/\n\s*\n/).map((paragraph) => paragraph.trim()).filter(Boolean);
      fallbackBlocks.push(...paragraphs.map((paragraph, paragraphIndex) => <p key={`paragraph-${index}-${paragraphIndex}`}>{paragraph.replace(/\n/g, ' ')}</p>));
    });

    let fallbackQuiz: ReactNode = null;
    if (quizQuestions.length > 0) fallbackQuiz = <Quiz questions={quizQuestions} lessonId={lessonId} />;

    content = <div>
      {fallbackBlocks}
      {fallbackQuiz ? <div>{fallbackQuiz}</div> : null}
    </div>;
  }

  return (
    <main className="reader-shell">
      <header className="reader-topbar">
        <Link className="brand" href="/">
          <span className="brand-mark"><Plane size={19} /></span>
          <span>Aviation <b>Camp</b></span>
        </Link>

        <div className="reader-nav">
          <ThemeToggle />
          <Link className="reader-back" href={`/subjects/${subject.id}/`}>
            <ArrowLeft size={15} /> {subject.title}
          </Link>
        </div>
      </header>

      <article className="reader-main lesson-article">
        <div className="eyebrow muted"><span /> {subject.title.toUpperCase()} / CHAPTER {String(lesson.chapterNumber).padStart(2, '0')}</div>

        <div className="lesson-header">
          <div>
            <h1 className="reader-title">Chapter {lesson.chapterNumber}: {lesson.title}</h1>
            <p className="reader-summary">{lesson.readTimeMinutes} min read</p>
          </div>
          <div className="subject-hero-stat">
            <strong>{lesson.readTimeMinutes}</strong>
            <span>mins</span>
          </div>
        </div>

        {lesson.sourcePageStart && lesson.sourcePageEnd && (
          <p className="source-citation">Source: {subject.title}, PDF pp. {lesson.sourcePageStart}–{lesson.sourcePageEnd}</p>
        )}

        <div className="lesson-toolbar">
          <LessonCompletion lessonId={lessonId} />
          <VoiceReader text={lesson.source} label="Read chapter aloud" />
        </div>

        <div className="lesson-content">{content}</div>
      </article>
    </main>
  );
}
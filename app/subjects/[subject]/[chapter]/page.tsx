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
import { getLessons, getParsedSection, subjects, type ParsedElement, type ParsedPage, type ParsedTextElement } from '../../../../src/content/subjects';

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

type ParsedLine = {
  spans: ParsedTextElement[];
  top: number;
  bottom: number;
  left: number;
  fontSize: number;
  column: number;
};

type ParsedBlock = ParsedLine | Exclude<ParsedElement, ParsedTextElement>;

function isTextElement(element: ParsedElement): element is ParsedTextElement {
  return element.type === 'text';
}

function parsedLines(page: ParsedPage): ParsedBlock[] {
  const midpoint = Math.max(...page.elements.map((element) => element.bbox[2]), 1) / 2;
  const result: ParsedBlock[] = [];

  for (const element of page.elements) {
    if (!isTextElement(element)) {
      result.push(element);
      continue;
    }

    const [x0, y0, , y1] = element.bbox;
    const column = x0 < midpoint ? 0 : 1;
    const previous = result.at(-1);
    if (
      previous &&
      'spans' in previous &&
      previous.column === column &&
      Math.abs(previous.top - y0) <= 2.5 &&
      x0 - previous.spans.at(-1)!.bbox[2] <= Math.max(36, element.font_size * 4)
    ) {
      previous.spans.push(element);
      previous.top = Math.min(previous.top, y0);
      previous.bottom = Math.max(previous.bottom, y1);
      previous.fontSize = Math.max(previous.fontSize, element.font_size);
    } else {
      result.push({ spans: [element], top: y0, bottom: y1, left: x0, fontSize: element.font_size, column });
    }
  }

  return result;
}

function ParsedTextLine({ line }: { line: ParsedLine }) {
  return <>{line.spans.map((span, index) => {
    const previous = line.spans[index - 1];
    const needsSpace = previous && span.bbox[0] - previous.bbox[2] > Math.max(1, span.font_size * 0.16);
    const color = /^#[0-9a-f]{6}$/i.test(span.color) ? span.color : undefined;
    const fontSize = Number.isFinite(span.font_size) ? Math.min(32, Math.max(9, span.font_size * 1.5)) : undefined;
    return <span key={`${index}-${span.bbox[0]}`} style={{
      color,
      fontSize,
      fontWeight: span.is_bold ? 700 : undefined,
      fontStyle: span.is_italic ? 'italic' : undefined,
    }}>{needsSpace ? ' ' : null}{span.text}</span>;
  })}</>;
}

function ParsedPdfContent({ pages }: { pages: ParsedPage[] }) {
  return <div className="parsed-pdf-content">
    {pages.map((page) => {
      const blocks = parsedLines(page);
      const rendered: ReactNode[] = [];
      let paragraph: ParsedLine[] = [];

      const flushParagraph = () => {
        if (!paragraph.length) return;
        const lines = paragraph;
        const isHeading = lines.length === 1 && lines[0].fontSize >= 11.5 && lines[0].spans.some((span) => span.is_bold);
        const content = lines.map((line, index) => <span key={index}>
          {index > 0 ? ' ' : null}<ParsedTextLine line={line} />
        </span>);
        rendered.push(isHeading
          ? <h2 key={`heading-${rendered.length}`}>{content}</h2>
          : <p key={`paragraph-${rendered.length}`}>{content}</p>);
        paragraph = [];
      };

      for (const block of blocks) {
        if ('spans' in block) {
          const previous = paragraph.at(-1);
          const verticalGap = previous ? block.top - previous.top : 0;
          const sameParagraph = previous
            && block.column === previous.column
            && Math.abs(block.fontSize - previous.fontSize) < 1
            && Math.abs(block.left - previous.left) < 24
            && verticalGap <= Math.max(18, block.fontSize * 1.8);
          if (paragraph.length && !sameParagraph) flushParagraph();
          paragraph.push(block);
          continue;
        }

        flushParagraph();
        if (block.type === 'image') {
          rendered.push(<figure key={`image-${rendered.length}`}>
            <LessonImage src={block.image_path} alt={`PDF page ${page.page_number} illustration`} />
          </figure>);
        } else {
          rendered.push(<div className="parsed-table-scroll" key={`table-${rendered.length}`}>
            <table><tbody>{block.data.map((row, rowIndex) => <tr key={rowIndex}>
              {row.map((cell, cellIndex) => rowIndex === 0
                ? <th key={cellIndex}>{cell ?? ''}</th>
                : <td key={cellIndex}>{cell ?? ''}</td>)}
            </tr>)}</tbody></table>
          </div>);
        }
      }
      flushParagraph();

      return <section className="parsed-pdf-page" key={page.page_number} aria-label={`PDF page ${page.page_number}`}>
        <div className="parsed-pdf-page-label">PDF page {page.page_number}</div>
        {rendered}
      </section>;
    })}
  </div>;
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

  const parsedSection = await getParsedSection(subject.id, lesson.slug);
  const figures = await getLessonFigures(subject.id, lesson.slug, lesson.source);
  const quizQuestions = await getLessonQuiz(subject.id, lesson.slug);
  let content: ReactNode;
  const lessonId = `${subject.id}/${lesson.slug}`;
  const parsedText = parsedSection?.pages
    .flatMap((page) => page.elements.filter(isTextElement).map((element) => element.text))
    .join(' ') || '';
  const source = applyTermTooltips(insertLessonFigures(lesson.source, figures, lesson.sourcePageStart, lesson.sourcePageEnd)
    .replace(/\{([A-Za-z][A-Za-z ]*)\}/g, '$1'));
  const sourceWithQuiz = quizQuestions.length > 0 && !/<Quiz\b/.test(source)
    ? `${source}\n\n<Quiz />`
    : source;
  if (parsedSection) {
    content = <>
      <ParsedPdfContent pages={parsedSection.pages} />
      {quizQuestions.length > 0 && <Quiz questions={quizQuestions} lessonId={lessonId} />}
    </>;
  } else {
    try {
      ({ content } = await compileMDX({
        source: sourceWithQuiz,
        components: {
          Quiz: () => quizQuestions.length > 0 ? <Quiz questions={quizQuestions} lessonId={lessonId} /> : null,
          TermTooltip,
          img: LessonImage,
        },
      }));
    } catch {
      const fallbackContent = sourceWithQuiz.replace(/<Quiz\b[\s\S]*?\/>/g, '');
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

      content = <div>
        {fallbackBlocks}
        {quizQuestions.length > 0 && <Quiz questions={quizQuestions} lessonId={lessonId} />}
      </div>;
    }
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
          <VoiceReader text={parsedText || lesson.source} label="Read chapter aloud" />
        </div>

        <div className="lesson-content">{content}</div>
      </article>
    </main>
  );
}
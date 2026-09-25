import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';

export const subjects = [
  { id: 'AFH', title: 'Airplane Flying Handbook' },
  { id: 'Instrument', title: 'Instrument Flying Handbook' },
  { id: 'InstrumentProcedures', title: 'Instrument Procedures Handbook' },
  { id: 'PHAK', title: "Pilot's Handbook of Aeronautical Knowledge" },
  { id: 'RiskManagement', title: 'Risk Management Handbook' },
  { id: 'Weather', title: 'Aviation Weather Handbook' },
  { id: 'WeightBalance', title: 'Aircraft Weight and Balance Handbook' },
] as const;

export type Lesson = {
  slug: string;
  title: string;
  book: string;
  chapterNumber: number;
  readTimeMinutes: number;
  sourcePageStart: number | undefined;
  sourcePageEnd: number | undefined;
  source: string;
};

const docsRoot = path.join(process.cwd(), 'src', 'content', 'docs');
const parsedRoot = path.join(process.cwd(), 'resources', 'parsed');

function frontmatterValue(source: string, key: string): string | undefined {
  const match = source.match(new RegExp(`^${key}:\\s*(.*)$`, 'm'));
  return match?.[1]?.trim().replace(/^(?:"(.*)"|'(.*)')$/, '$1$2');
}

export async function getLessons(): Promise<Lesson[]> {
  const books = await readdir(docsRoot, { withFileTypes: true });
  const lessons = await Promise.all(books.filter((book) => book.isDirectory()).map(async (book) => {
    const directory = path.join(docsRoot, book.name);
    const [files, manifestText] = await Promise.all([
      readdir(directory),
      readFile(path.join(parsedRoot, book.name, 'book_manifest.json'), 'utf8'),
    ]);
    const manifest = JSON.parse(manifestText) as { chapters: Array<{ chapter: string; startPage: number; endPage: number }> };
    const pageRanges = new Map(manifest.chapters.map((chapter) => [chapter.chapter, chapter]));
    return Promise.all(files.filter((file) => file.endsWith('.mdx')).map(async (file) => {
      const source = await readFile(path.join(directory, file), 'utf8');
      const title = frontmatterValue(source, 'title');
      if (!title) return null;
      const pageRange = pageRanges.get(file.replace(/\.mdx$/, ''));
      return {
        slug: file.replace(/\.mdx$/, ''),
        title,
        book: book.name,
        chapterNumber: Number(frontmatterValue(source, 'chapterNumber')) || 0,
        readTimeMinutes: Number(frontmatterValue(source, 'readTimeMinutes')) || 0,
        sourcePageStart: pageRange?.startPage,
        sourcePageEnd: pageRange?.endPage,
        source: source.replace(/^---[\s\S]*?---\s*/, ''),
      };
    }));
  }));

  return lessons.flat().filter((lesson): lesson is Lesson => lesson !== null)
    .sort((left, right) => left.chapterNumber - right.chapterNumber || left.title.localeCompare(right.title));
}

export async function getLessonsForBook(book: string): Promise<Lesson[]> {
  return (await getLessons()).filter((lesson) => lesson.book === book);
}
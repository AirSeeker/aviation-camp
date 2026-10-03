import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';

export const subjects = [
  { id: 'AFH', title: 'Airplane Flying Handbook' },
  { id: 'EASA_AirOps', title: 'Easy Access Rules for Air Operations' },
  { id: 'EASA_Aircrew', title: 'Easy Access Rules for Aircrew (Regulation (EU) No 1178/2011)' },
  { id: 'EASA_SERA', title: 'Easy Access Rules for Standardised European Rules of the Air (SERA)' },
  { id: 'Instructor', title: "Aviation Instructor's Handbook" },
  { id: 'Instrument', title: 'Instrument Flying Handbook' },
  { id: 'InstrumentProcedures', title: 'Instrument Procedures Handbook' },
  { id: 'PHAK', title: "Pilot's Handbook of Aeronautical Knowledge" },
  { id: 'RiskManagement', title: 'Risk Management Handbook' },
  { id: 'Weather', title: 'Aviation Weather Handbook' },
  { id: 'WeightBalance', title: 'Aircraft Weight and Balance Handbook' },
] as const;

export const pplCategories = [
  { id: 'air-law', title: 'Air Law', description: 'Flight rules, pilot responsibilities, and airspace', bookId: 'PHAK' },
  { id: 'human-performance', title: 'Human Performance', description: 'Physiology, fatigue, stress, and decision-making', bookId: 'RiskManagement' },
  { id: 'meteorology', title: 'Meteorology', description: 'Atmosphere, weather, METAR, TAF, and icing', bookId: 'Weather' },
  { id: 'communications', title: 'Communications', description: 'Phraseology, clearances, and ATC communication', bookId: 'InstrumentProcedures' },
  { id: 'principles-of-flight', title: 'Principles of Flight', description: 'Aerodynamics, stability, control, and stalls', bookId: 'AFH' },
  { id: 'operational-procedures', title: 'Operational Procedures', description: 'Preparation, safety, emergencies, and abnormal situations', bookId: 'AFH' },
  { id: 'flight-performance', title: 'Flight Performance and Planning', description: 'Takeoff, landing, range, fuel, and loading', bookId: 'WeightBalance' },
  { id: 'aircraft-general-knowledge', title: 'Aircraft General Knowledge', description: 'Systems, engines, instruments, and equipment', bookId: 'PHAK' },
  { id: 'navigation', title: 'Navigation', description: 'Charts, courses, altitudes, time, and navigation aids', bookId: 'Instrument' },
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

async function readBookManifest(bookName: string): Promise<Map<string, { chapter: string; title?: string; startPage?: number; endPage?: number }>> {
  const bookPath = path.join(parsedRoot, bookName);
  const candidates = ['parser_manifest.json', 'book_manifest.json'];

  for (const fileName of candidates) {
    try {
      const text = await readFile(path.join(bookPath, fileName), 'utf8');
      const manifest = JSON.parse(text) as {
        chapters?: Array<{ chapter: string; title?: string; startPage?: number; endPage?: number }>;
        sections?: Array<{ type?: string; title?: string; start_page?: number; end_page?: number; content_path?: string; chapter?: string; startPage?: number; endPage?: number }>;
      };

      if (Array.isArray(manifest.chapters)) {
        return new Map(manifest.chapters.map((chapter) => [chapter.chapter, chapter]));
      }

      if (Array.isArray(manifest.sections)) {
        const entries: Array<[string, { chapter: string; title?: string; startPage?: number; endPage?: number }]> = [];
        for (const section of manifest.sections) {
          if (section.type !== 'chapter' && !section.content_path) continue;
          const chapterKey = section.chapter || (section.content_path ? path.basename(section.content_path, '.json') : undefined);
          if (!chapterKey) continue;
          entries.push([chapterKey, {
            chapter: chapterKey,
            title: section.title,
            startPage: section.start_page ?? section.startPage,
            endPage: section.end_page ?? section.endPage,
          }]);
        }
        return new Map(entries);
      }
    } catch {
      // Fall through to the next manifest filename.
    }
  }

  return new Map();
}

export async function getLessons(): Promise<Lesson[]> {
  const books = await readdir(docsRoot, { withFileTypes: true });
  const lessons = await Promise.all(books.filter((book) => book.isDirectory()).map(async (book) => {
    const directory = path.join(docsRoot, book.name);
    const [files, pageRanges] = await Promise.all([
      readdir(directory),
      readBookManifest(book.name),
    ]);
    return Promise.all(files.filter((file) => file.endsWith('.mdx')).map(async (file) => {
      const source = await readFile(path.join(directory, file), 'utf8');
      const slug = file.replace(/\.mdx$/, '');
      let parsedSource: string | undefined;
      try {
        parsedSource = await readFile(path.join(parsedRoot, book.name, slug, 'content.md'), 'utf8');
      } catch {
        parsedSource = undefined;
      }
      const title = frontmatterValue(source, 'title');
      if (!title) return null;
      const pageRange = pageRanges.get(slug);
      const lessonSource = parsedSource?.trim()
        ? `${parsedSource.trim()}\n\n<Quiz />`
        : source.replace(/^---[\s\S]*?---\s*/, '');
      return {
        slug,
        title: pageRange?.title || title,
        book: book.name,
        chapterNumber: Number(frontmatterValue(source, 'chapterNumber')) || 0,
        readTimeMinutes: Number(frontmatterValue(source, 'readTimeMinutes')) || 0,
        sourcePageStart: pageRange?.startPage,
        sourcePageEnd: pageRange?.endPage,
        source: lessonSource,
      };
    }));
  }));

  return lessons.flat().filter((lesson): lesson is Lesson => lesson !== null)
    .sort((left, right) => left.chapterNumber - right.chapterNumber || left.title.localeCompare(right.title));
}

export async function getLessonsForBook(book: string): Promise<Lesson[]> {
  return (await getLessons()).filter((lesson) => lesson.book === book);
}
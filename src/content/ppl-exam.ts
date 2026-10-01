import questions from '../../content/quizzes/ppl/aerodynamics.json';

export type ExamQuestion = {
  id: string;
  question: string;
  options: string[];
  correctAnswer: number;
  explanation: string;
  source?: string;
  reference?: { book: string; chapter: string; anchor: string };
};

export type Authority = 'FAA' | 'EASA';

export const EASA_DISCIPLINES = [
  { id: 'air-law', label: 'Air Law' },
  { id: 'human-performance', label: 'Human Performance & Limitations' },
  { id: 'meteorology', label: 'Meteorology' },
  { id: 'vfr-communications', label: 'VFR Communications' },
  { id: 'principles-of-flight', label: 'Principles of Flight' },
  { id: 'operational-procedures', label: 'Operational Procedures' },
  { id: 'flight-performance', label: 'Flight Performance & Planning' },
  { id: 'aircraft-general-knowledge', label: 'Aircraft General Knowledge' },
  { id: 'navigation', label: 'Navigation' },
] as const;

const quizContext = (path: string) => {
  try {
    return (require as any).context(path, true, /\.json$/);
  } catch {
    return null;
  }
};

function normalizeQuestionList(raw: unknown): ExamQuestion[] {
  if (!Array.isArray(raw)) return [];
  return raw.filter((entry): entry is ExamQuestion => !!entry && typeof entry === 'object' && 'question' in entry && 'options' in entry);
}

function collectQuestionsFromContext(context: any): ExamQuestion[] {
  if (!context) return [];
  return context.keys().flatMap((key: string) => normalizeQuestionList(context(key).default ?? context(key)));
}

function shuffleArray<T>(values: T[]): T[] {
  const next = [...values];
  for (let index = next.length - 1; index > 0; index -= 1) {
    const swapIndex = Math.floor(Math.random() * (index + 1));
    [next[index], next[swapIndex]] = [next[swapIndex], next[index]];
  }
  return next;
}

export function getExamQuestions(authority: Authority = 'FAA', discipline: string = 'all'): ExamQuestion[] {
  if (authority === 'EASA') {
    const context = quizContext('../../content/quizzes/easa');
    const pool = collectQuestionsFromContext(context);

    if (!discipline || discipline === 'all') {
      return shuffleArray(pool).slice(0, Math.min(12, pool.length || 1));
    }

    const filtered = pool.filter((question) => {
      const chapter = question.reference?.chapter?.toLowerCase() ?? '';
      return chapter.includes(discipline.replace(/-/g, ' ')) || chapter.includes(discipline.replace(/-/g, '-')) || question.id?.includes(discipline);
    });

    return shuffleArray(filtered.length ? filtered : pool).slice(0, Math.min(12, filtered.length || pool.length || 1));
  }

  const context = quizContext('../../content/quizzes');
  const pool = collectQuestionsFromContext(context).filter((question) => !question.id?.startsWith('easa-'));

  return shuffleArray(pool.length ? pool : Array.isArray(questions) ? questions : []).slice(0, Math.min(12, (pool.length || (Array.isArray(questions) ? questions.length : 0)) || 1));
}

export const pplExamQuestions: ExamQuestion[] = getExamQuestions();
export const examDurationSeconds = 30 * 60;
export const passingPercent = 70;

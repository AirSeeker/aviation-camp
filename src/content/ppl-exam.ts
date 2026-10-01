import { easaQuizQuestions, fallbackQuizQuestions, faaQuizQuestions, type ExamQuestion } from './quiz-bank';

export type { ExamQuestion };
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
    const pool = easaQuizQuestions;

    if (!discipline || discipline === 'all') {
      return shuffleArray(pool).slice(0, Math.min(12, pool.length || 1));
    }

    const filtered = pool.filter((question) => {
      const chapter = question.reference?.chapter?.toLowerCase() ?? '';
      return chapter.includes(discipline.replace(/-/g, ' ')) || chapter.includes(discipline.replace(/-/g, '-')) || question.id?.includes(discipline);
    });

    return shuffleArray(filtered.length ? filtered : pool).slice(0, Math.min(12, filtered.length || pool.length || 1));
  }

  const pool = faaQuizQuestions.length ? faaQuizQuestions : fallbackQuizQuestions;
  return shuffleArray(pool).slice(0, Math.min(12, pool.length || 1));
}

export const pplExamQuestions: ExamQuestion[] = getExamQuestions();
export const examDurationSeconds = 30 * 60;
export const passingPercent = 70;

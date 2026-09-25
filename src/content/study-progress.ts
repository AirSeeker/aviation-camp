export type QuizResult = {
  answers: Record<number, number>;
  score: number;
  total: number;
  completedAt: string;
};

export type StudyProgressState = {
  completedLessons: string[];
  quizResults: Record<string, QuizResult>;
};

const STORAGE_KEY = 'aviation-camp:study-progress';
export const STUDY_PROGRESS_EVENT = 'aviation-camp:study-progress-change';

const emptyProgress = (): StudyProgressState => ({ completedLessons: [], quizResults: {} });

export function readStudyProgress(): StudyProgressState {
  if (typeof window === 'undefined') return emptyProgress();
  try {
    const value = JSON.parse(window.localStorage.getItem(STORAGE_KEY) || 'null');
    if (!value || !Array.isArray(value.completedLessons) || !value.quizResults || typeof value.quizResults !== 'object' || Array.isArray(value.quizResults)) return emptyProgress();
    return {
      completedLessons: value.completedLessons.filter((item: unknown): item is string => typeof item === 'string'),
      quizResults: value.quizResults as Record<string, QuizResult>,
    };
  } catch {
    return emptyProgress();
  }
}

export function updateStudyProgress(update: (current: StudyProgressState) => StudyProgressState): StudyProgressState {
  const next = update(readStudyProgress());
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    window.dispatchEvent(new Event(STUDY_PROGRESS_EVENT));
  } catch {
    return next;
  }
  return next;
}
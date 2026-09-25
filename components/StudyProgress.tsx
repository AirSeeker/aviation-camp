'use client';

import { Check, Circle, CircleCheck } from 'lucide-react';
import { useEffect, useState } from 'react';
import { readStudyProgress, STUDY_PROGRESS_EVENT, updateStudyProgress } from '../src/content/study-progress';

export function StudyProgress({ totalLessons }: { totalLessons: number }) {
  const [completedCount, setCompletedCount] = useState(0);

  useEffect(() => {
    const update = () => setCompletedCount(readStudyProgress().completedLessons.length);
    update();
    window.addEventListener(STUDY_PROGRESS_EVENT, update);
    window.addEventListener('storage', update);
    return () => {
      window.removeEventListener(STUDY_PROGRESS_EVENT, update);
      window.removeEventListener('storage', update);
    };
  }, []);

  const percentage = totalLessons ? Math.min(100, Math.round((completedCount / totalLessons) * 100)) : 0;

  return <div className="sidebar-footer">
    <div className="progress-meta"><span>Ваш прогрес</span><strong>{percentage}%</strong></div>
    <div className="progress-track" role="progressbar" aria-label="Завершені розділи" aria-valuemin={0} aria-valuemax={totalLessons} aria-valuenow={completedCount}>
      <span style={{ width: `${percentage}%` }} />
    </div>
    <p>{completedCount} із {totalLessons} розділів завершено</p>
  </div>;
}

export function LessonCompletion({ lessonId }: { lessonId: string }) {
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    const update = () => setCompleted(readStudyProgress().completedLessons.includes(lessonId));
    update();
    window.addEventListener(STUDY_PROGRESS_EVENT, update);
    return () => window.removeEventListener(STUDY_PROGRESS_EVENT, update);
  }, [lessonId]);

  function toggleCompletion() {
    const next = !completed;
    setCompleted(next);
    updateStudyProgress((current) => ({
      ...current,
      completedLessons: next
        ? Array.from(new Set([...current.completedLessons, lessonId]))
        : current.completedLessons.filter((item) => item !== lessonId),
    }));
  }

  return <button className={`lesson-completion ${completed ? 'completed' : ''}`} type="button" onClick={toggleCompletion} aria-pressed={completed}>
    {completed ? <CircleCheck size={17} /> : <Circle size={17} />}
    {completed ? 'Завершено' : 'Позначити завершеним'}
    <Check className="completion-check" size={14} />
  </button>;
}
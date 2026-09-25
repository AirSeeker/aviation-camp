'use client';

import { useState } from 'react';
import { useEffect } from 'react';
import { readStudyProgress, updateStudyProgress } from '../src/content/study-progress';

type QuizQuestion = {
  question: string;
  options: string[];
  correctAnswer: number;
  explanation: string;
};

export default function Quiz({ questions, lessonId }: { questions: QuizQuestion[]; lessonId: string }) {
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [submitted, setSubmitted] = useState(false);
  const answeredCount = Object.keys(answers).length;
  const score = questions.reduce((total, question, index) => total + Number(answers[index] === question.correctAnswer), 0);

  useEffect(() => {
    const result = readStudyProgress().quizResults[lessonId];
    if (result) {
      setAnswers(result.answers);
      setSubmitted(true);
    }
  }, [lessonId]);

  function submitQuiz() {
    setSubmitted(true);
    updateStudyProgress((current) => ({
      ...current,
      completedLessons: Array.from(new Set([...current.completedLessons, lessonId])),
      quizResults: {
        ...current.quizResults,
        [lessonId]: { answers, score, total: questions.length, completedAt: new Date().toISOString() },
      },
    }));
  }

  return <section className="lesson-quiz" aria-label="Knowledge check">
    <h2>Knowledge check</h2>
    {questions.map((question, index) => <fieldset className="quiz-question" key={`${index}-${question.question}`}>
      <legend>{index + 1}. {question.question}</legend>
      {question.options.map((option, optionIndex) => <label className="quiz-option" key={option}>
        <input
          type="radio"
          name={`quiz-${index}`}
          checked={answers[index] === optionIndex}
          onChange={() => {
            setAnswers((current) => ({ ...current, [index]: optionIndex }));
            setSubmitted(false);
          }}
        />
        <span>{option}</span>
      </label>)}
      {submitted && <p className={answers[index] === question.correctAnswer ? 'quiz-feedback correct' : 'quiz-feedback'}>
        {answers[index] === question.correctAnswer ? 'Correct. ' : 'Review this one. '}{question.explanation}
      </p>}
    </fieldset>)}
    <button className="quiz-submit" type="button" disabled={answeredCount !== questions.length} onClick={submitQuiz}>
      Check answers
    </button>
    {submitted && <p className="quiz-score">Score: {score} / {questions.length}</p>}
  </section>;
}
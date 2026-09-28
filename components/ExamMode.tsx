'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { examDurationSeconds, passingPercent, pplExamQuestions, type ExamQuestion } from '../src/content/ppl-exam';

type ExamState = 'ready' | 'active' | 'submitted';

function getQuestionHref(question: ExamQuestion) {
  if (question.source) return question.source;
  const bookMap: Record<string, string> = {
    afh: 'AFH',
    phak: 'PHAK',
    instrument: 'Instrument',
    instrumentprocedures: 'InstrumentProcedures',
    riskmanagement: 'RiskManagement',
    weather: 'Weather',
    weightbalance: 'WeightBalance',
  };
  const book = question.reference ? bookMap[question.reference.book.toLowerCase()] : undefined;
  const chapter = question.reference?.chapter.match(/(?:chapter-|ch)?(\d+)/i)?.[1];
  return book && chapter ? `/subjects/${book}/ch${chapter.padStart(2, '0')}/#${question.reference?.anchor}` : '/';
}

export default function ExamMode() {
  const [state, setState] = useState<ExamState>('ready');
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [remaining, setRemaining] = useState(examDurationSeconds);
  const score = pplExamQuestions.reduce((total, question, index) => total + Number(answers[index] === question.correctAnswer), 0);
  const percent = pplExamQuestions.length ? Math.round((score / pplExamQuestions.length) * 100) : 0;

  useEffect(() => {
    if (state !== 'active') return;
    const timer = window.setInterval(() => {
      setRemaining((value) => {
        if (value <= 1) {
          window.clearInterval(timer);
          setState('submitted');
          return 0;
        }
        return value - 1;
      });
    }, 1000);
    return () => window.clearInterval(timer);
  }, [state]);

  function startExam() {
    setAnswers({});
    setRemaining(examDurationSeconds);
    setState('active');
  }

  const minutes = Math.floor(remaining / 60).toString().padStart(2, '0');
  const seconds = (remaining % 60).toString().padStart(2, '0');

  return <section className="exam-panel">
    <div className="exam-meta"><span>FAA PPL practice exam</span><strong>{state === 'active' ? `${minutes}:${seconds}` : '30:00'}</strong></div>
    {state === 'ready' && <div><h2>Test your knowledge</h2><p>Answer every question before the timer expires. A score of {passingPercent}% or higher is a pass.</p><button className="quiz-submit" type="button" onClick={startExam}>Start exam</button></div>}
    {state !== 'ready' && <>
      {pplExamQuestions.map((question, index) => <fieldset className="quiz-question" key={question.id}>
        <legend>{index + 1}. {question.question}</legend>
        {question.options.map((option, optionIndex) => <label className="quiz-option" key={option}><input type="radio" name={`exam-${index}`} checked={answers[index] === optionIndex} onChange={() => setAnswers((current) => ({ ...current, [index]: optionIndex }))} /><span>{option}</span></label>)}
        {state === 'submitted' && <p className={answers[index] === question.correctAnswer ? 'quiz-feedback correct' : 'quiz-feedback'}>{answers[index] === question.correctAnswer ? 'Correct. ' : 'Review this one. '}{question.explanation} <Link href={getQuestionHref(question)}>Open source chapter</Link></p>}
      </fieldset>)}
      {state === 'active' && <button className="quiz-submit" type="button" disabled={Object.keys(answers).length !== pplExamQuestions.length} onClick={() => setState('submitted')}>Submit exam</button>}
      {state === 'submitted' && <><p className="quiz-score">Score: {score} / {pplExamQuestions.length} ({percent}%) - {percent >= passingPercent ? 'Pass' : 'Not yet passed'}</p><button className="quiz-submit" type="button" onClick={startExam}>Retake exam</button></>}
    </>}
  </section>;
}

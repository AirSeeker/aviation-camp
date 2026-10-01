'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import { EASA_DISCIPLINES, examDurationSeconds, getExamQuestions, passingPercent, type Authority, type ExamQuestion } from '../src/content/ppl-exam';

type ExamState = 'ready' | 'active' | 'submitted';
const AUTHORITY_STORAGE_KEY = 'aviation-camp:authority';
const EXAM_DISCIPLINE_KEY = 'aviation-camp:exam-discipline';
const EXAM_RESULTS_KEY = 'aviation-camp:exam-results';

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
    easa: 'EASA',
  };
  const book = question.reference ? bookMap[question.reference.book.toLowerCase()] : undefined;
  const chapter = question.reference?.chapter.match(/(?:chapter-|ch)?(\d+)/i)?.[1];
  if (book && chapter) return `/subjects/${book}/ch${chapter.padStart(2, '0')}/#${question.reference?.anchor}`;
  return question.reference?.book ? `/glossary/` : '/';
}

export default function ExamMode() {
  const [authority, setAuthority] = useState<Authority>('FAA');
  const [discipline, setDiscipline] = useState('all');
  const [state, setState] = useState<ExamState>('ready');
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [remaining, setRemaining] = useState(examDurationSeconds);

  useEffect(() => {
    const storedAuthority = window.localStorage.getItem(AUTHORITY_STORAGE_KEY);
    if (storedAuthority === 'FAA' || storedAuthority === 'EASA') setAuthority(storedAuthority);
    const storedDiscipline = window.localStorage.getItem(EXAM_DISCIPLINE_KEY);
    if (storedDiscipline) setDiscipline(storedDiscipline);
  }, []);

  useEffect(() => {
    window.localStorage.setItem(AUTHORITY_STORAGE_KEY, authority);
    if (authority !== 'EASA') setDiscipline('all');
  }, [authority]);

  useEffect(() => {
    window.localStorage.setItem(EXAM_DISCIPLINE_KEY, discipline);
  }, [discipline]);

  const examQuestions = useMemo(() => getExamQuestions(authority, discipline), [authority, discipline]);
  const score = examQuestions.reduce((total, question, index) => total + Number(answers[index] === question.correctAnswer), 0);
  const percent = examQuestions.length ? Math.round((score / examQuestions.length) * 100) : 0;

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

  useEffect(() => {
    if (state !== 'submitted') return;
    window.localStorage.setItem(EXAM_RESULTS_KEY, JSON.stringify({ authority, discipline, percent, score, total: examQuestions.length, timestamp: Date.now() }));
  }, [authority, discipline, examQuestions.length, percent, score, state]);

  function startExam() {
    setAnswers({});
    setRemaining(examDurationSeconds);
    setState('active');
  }

  const minutes = Math.floor(remaining / 60).toString().padStart(2, '0');
  const seconds = (remaining % 60).toString().padStart(2, '0');

  return <section className="exam-panel">
    <div className="exam-meta"><span>{authority === 'EASA' ? 'EASA practice exam' : 'FAA PPL practice exam'}</span><strong>{state === 'active' ? `${minutes}:${seconds}` : '30:00'}</strong></div>
    {authority === 'EASA' && <div className="exam-discipline-picker"><label htmlFor="exam-discipline">Subject</label><select id="exam-discipline" value={discipline} onChange={(event) => setDiscipline(event.target.value)}><option value="all">All disciplines (mock exam)</option>{EASA_DISCIPLINES.map((item) => <option key={item.id} value={item.id}>{item.label}</option>)}</select></div>}
    {state === 'ready' && <div><h2>Test your knowledge</h2><p>Answer every question before the timer expires. A score of {passingPercent}% or higher is a pass.</p><button className="quiz-submit" type="button" onClick={startExam}>Start exam</button></div>}
    {state !== 'ready' && <>
      {examQuestions.map((question, index) => <fieldset className="quiz-question" key={`${authority}-${discipline}-${question.id}-${index}`}>
        <legend>{index + 1}. {question.question}</legend>
        {question.options.map((option, optionIndex) => <label className="quiz-option" key={`${question.id}-${option}`}><input type="radio" name={`exam-${authority}-${discipline}-${index}`} checked={answers[index] === optionIndex} onChange={() => setAnswers((current) => ({ ...current, [index]: optionIndex }))} /><span>{option}</span></label>)}
        {state === 'submitted' && <p className={answers[index] === question.correctAnswer ? 'quiz-feedback correct' : 'quiz-feedback'}>{answers[index] === question.correctAnswer ? 'Correct. ' : 'Review this one. '}{question.explanation} <Link href={getQuestionHref(question)}>Open source chapter</Link></p>}
      </fieldset>)}
      {state === 'active' && <button className="quiz-submit" type="button" disabled={Object.keys(answers).length !== examQuestions.length} onClick={() => setState('submitted')}>Submit exam</button>}
      {state === 'submitted' && <><p className="quiz-score">Score: {score} / {examQuestions.length} ({percent}%) - {percent >= passingPercent ? 'Pass' : 'Not yet passed'}</p><button className="quiz-submit" type="button" onClick={startExam}>Retake exam</button></>}
    </>}
  </section>;
}

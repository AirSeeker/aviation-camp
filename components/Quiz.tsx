'use client';

import { useEffect, useRef, useState } from 'react';
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
  const [voiceState, setVoiceState] = useState<Record<number, 'idle' | 'speaking' | 'paused'>>({});
  const voiceRefs = useRef<Record<number, SpeechSynthesisUtterance | null>>({});
  const answeredCount = Object.keys(answers).length;
  const score = questions.reduce((total, question, index) => total + Number(answers[index] === question.correctAnswer), 0);

  useEffect(() => {
    const result = readStudyProgress().quizResults[lessonId];
    if (result) {
      setAnswers(result.answers);
      setSubmitted(true);
    }
  }, [lessonId]);

  useEffect(() => {
    return () => {
      if (typeof window !== 'undefined') {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  function speakQuestion(question: QuizQuestion, index: number) {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) return;

    window.speechSynthesis.cancel();

    const text = [
      `Question ${index + 1}. ${question.question}`,
      ...question.options.map((option, optionIndex) => `Option ${optionIndex + 1}. ${option}`),
      `Correct answer: ${question.options[question.correctAnswer]}`,
      `Explanation: ${question.explanation}`,
    ].join('. ');

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.onstart = () => setVoiceState((current) => ({ ...current, [index]: 'speaking' }));
    utterance.onpause = () => setVoiceState((current) => ({ ...current, [index]: 'paused' }));
    utterance.onresume = () => setVoiceState((current) => ({ ...current, [index]: 'speaking' }));
    utterance.onend = () => setVoiceState((current) => ({ ...current, [index]: 'idle' }));
    utterance.onerror = () => setVoiceState((current) => ({ ...current, [index]: 'idle' }));

    voiceRefs.current[index] = utterance;
    window.speechSynthesis.speak(utterance);
  }

  function stopQuestionVoice(index: number) {
    if (typeof window === 'undefined') return;
    window.speechSynthesis.cancel();
    voiceRefs.current[index] = null;
    setVoiceState((current) => ({ ...current, [index]: 'idle' }));
  }

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
    <div className="voice-reader" aria-live="polite">
      <button type="button" className="voice-reader-button" onClick={() => { if (questions.length > 0) speakQuestion(questions[0], 0); }}>
        Read quiz aloud
      </button>
    </div>
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
      <div className="voice-reader" aria-live="polite">
        <button type="button" className="voice-reader-button" onClick={() => speakQuestion(question, index)}>
          {voiceState[index] === 'speaking' ? 'Pause audio' : voiceState[index] === 'paused' ? 'Resume audio' : 'Read question aloud'}
        </button>
        {(voiceState[index] === 'speaking' || voiceState[index] === 'paused') && (
          <button type="button" className="voice-reader-button secondary" onClick={() => stopQuestionVoice(index)}>
            Stop
          </button>
        )}
      </div>
      {submitted && <>
        <p className={answers[index] === question.correctAnswer ? 'quiz-feedback correct' : 'quiz-feedback'}>
          {answers[index] === question.correctAnswer ? 'Correct. ' : 'Review this one. '}{question.explanation}
        </p>
        <div className="voice-reader" aria-live="polite">
          <button type="button" className="voice-reader-button" onClick={() => speakQuestion(question, index)}>
            {voiceState[index] === 'speaking' ? 'Pause explanation audio' : voiceState[index] === 'paused' ? 'Resume explanation audio' : 'Read explanation aloud'}
          </button>
          {(voiceState[index] === 'speaking' || voiceState[index] === 'paused') && (
            <button type="button" className="voice-reader-button secondary" onClick={() => stopQuestionVoice(index)}>
              Stop
            </button>
          )}
        </div>
      </>}
    </fieldset>)}
    <button className="quiz-submit" type="button" disabled={answeredCount !== questions.length} onClick={submitQuiz}>
      Check answers
    </button>
    {submitted && <p className="quiz-score">Score: {score} / {questions.length}</p>}
  </section>;
}
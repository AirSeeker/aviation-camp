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

export const pplExamQuestions: ExamQuestion[] = questions;
export const examDurationSeconds = 30 * 60;
export const passingPercent = 70;

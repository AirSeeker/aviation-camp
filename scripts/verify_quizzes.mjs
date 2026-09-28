import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';

const root = path.join(process.cwd(), 'content', 'quizzes');

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const nested = await Promise.all(entries.map(async (entry) => {
    const entryPath = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(entryPath) : [entryPath];
  }));
  return nested.flat();
}

const files = (await walk(root)).filter((file) => file.endsWith('.json'));
const ids = new Set();
let questionCount = 0;

for (const file of files) {
  const questions = JSON.parse(await readFile(file, 'utf8'));
  if (!Array.isArray(questions) || questions.length === 0) throw new Error(`Quiz bank must be a non-empty array: ${file}`);
  for (const question of questions) {
    if (!question.id || ids.has(question.id)) throw new Error(`Missing or duplicate question id: ${file}`);
    if (typeof question.question !== 'string' || !Array.isArray(question.options) || question.options.length < 2) throw new Error(`Invalid question options: ${file}#${question.id}`);
    if (!Number.isInteger(question.correctAnswer) || question.correctAnswer < 0 || question.correctAnswer >= question.options.length) throw new Error(`Invalid correctAnswer: ${file}#${question.id}`);
    if (typeof question.explanation !== 'string' || !question.reference?.book || !question.reference.chapter || !question.reference.anchor) throw new Error(`Missing explanation or reference: ${file}#${question.id}`);
    ids.add(question.id);
    questionCount += 1;
  }
}

console.log(`Verified ${questionCount} questions across ${files.length} JSON banks.`);

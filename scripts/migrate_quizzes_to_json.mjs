import { mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const docsRoot = path.join(root, 'src', 'content', 'docs');
const quizRoot = path.join(root, 'content', 'quizzes');

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const nested = await Promise.all(entries.map(async (entry) => {
    const entryPath = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(entryPath) : [entryPath];
  }));
  return nested.flat();
}

const files = (await walk(docsRoot)).filter((file) => file.endsWith('.mdx'));
let migrated = 0;
let questionCount = 0;

for (const file of files) {
  const source = await readFile(file, 'utf8');
  const match = source.match(/<Quiz\s+questions=\{([\s\S]*?)\}\s*\/>/);
  if (!match) continue;

  const book = path.basename(path.dirname(file));
  const chapter = path.basename(file, '.mdx');
  const questions = Function(`"use strict"; return (${match[1]});`)();
  if (!Array.isArray(questions)) throw new Error(`Quiz payload is not an array: ${file}`);

  const chapterNumber = Number(chapter.replace(/^ch/, ''));
  const normalized = questions.map((question, index) => ({
    id: question.id || `${book.toLowerCase()}-${chapter}-q-${String(index + 1).padStart(2, '0')}`,
    question: question.question,
    options: question.options,
    correctAnswer: question.correctAnswer,
    explanation: question.explanation,
    reference: question.reference || {
      book: book.toLowerCase(),
      chapter: `chapter-${chapterNumber}`,
      anchor: `chapter-${chapterNumber}`,
    },
  }));

  const outputDirectory = path.join(quizRoot, book);
  await mkdir(outputDirectory, { recursive: true });
  await writeFile(path.join(outputDirectory, `${chapter}.json`), `${JSON.stringify(normalized, null, 2)}\n`);
  await writeFile(file, source.replace(match[0], '<Quiz />'));
  migrated += 1;
  questionCount += normalized.length;
}

console.log(`Migrated ${questionCount} questions from ${migrated} chapters.`);

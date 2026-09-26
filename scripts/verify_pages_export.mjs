import { cp, mkdir, readFile, readdir, rm, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const docsRoot = path.join(root, 'src', 'content', 'docs');
const publicRoot = path.join(root, 'public');
const outRoot = path.join(root, 'out');
const bookTitles = {
  AFH: 'Airplane Flying Handbook',
  Instrument: 'Instrument Flying Handbook',
  InstrumentProcedures: 'Instrument Procedures Handbook',
  PHAK: "Pilot's Handbook of Aeronautical Knowledge",
  RiskManagement: 'Risk Management Handbook',
  Weather: 'Aviation Weather Handbook',
  WeightBalance: 'Aircraft Weight and Balance Handbook',
};
const parsedRoot = path.join(root, 'resources', 'parsed');
const repositoryName = process.env.GITHUB_REPOSITORY?.split('/')[1] || 'aviation-camp';
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || `/${repositoryName}`;

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const nested = await Promise.all(entries.map((entry) => {
    const entryPath = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(entryPath) : [entryPath];
  }));
  return nested.flat();
}

async function fileExists(filePath) {
  try {
    return (await stat(filePath)).isFile();
  } catch {
    return false;
  }
}

async function localTargetExists(urlPath) {
  let relative = decodeURIComponent(urlPath);
  if (relative === basePath || relative === `${basePath}/`) relative = '/';
  else if (relative.startsWith(`${basePath}/`)) relative = relative.slice(basePath.length);
  const cleanPath = relative.replace(/^\/+/, '');
  const directPath = path.join(outRoot, cleanPath);
  const candidates = relative.endsWith('/')
    ? [path.join(directPath, 'index.html')]
    : [directPath, `${directPath}.html`, path.join(directPath, 'index.html')];
  for (const candidate of candidates) {
    if (candidate.startsWith(`${outRoot}${path.sep}`) && await fileExists(candidate)) return true;
  }
  return false;
}

const referencedImages = new Set();
const reviewFindings = [];
const lessonFiles = (await walk(docsRoot)).filter((file) => file.endsWith('.mdx'));
const searchEntries = [];
const sourcePageRanges = new Map();
for (const book of Object.keys(bookTitles)) {
  const manifest = JSON.parse(await readFile(path.join(parsedRoot, book, 'book_manifest.json'), 'utf8'));
  sourcePageRanges.set(book, new Map(manifest.chapters.map((chapter) => [chapter.chapter, chapter])));
}
for (const file of lessonFiles) {
  const source = await readFile(file, 'utf8');
  const book = path.basename(path.dirname(file));
  const subjectValue = source.match(/^subject:\s*(.*?)\s*$/m)?.[1];
  const subject = subjectValue?.replace(/^(?:"(.*)"|'(.*)')$/, '$1$2');
  const titleValue = source.match(/^title:\s*(.*?)\s*$/m)?.[1];
  const title = titleValue?.replace(/^(?:"(.*)"|'(.*)')$/, '$1$2');
  const chapterNumber = source.match(/^chapterNumber:\s*(\d+)\s*$/m)?.[1];
  const relativeFile = path.relative(root, file);
  if (subject !== bookTitles[book]) reviewFindings.push({ file: relativeFile, issue: 'Handbook metadata does not match its source folder' });
  if (title !== `${bookTitles[book]} — Chapter ${chapterNumber}`) reviewFindings.push({ file: relativeFile, issue: 'Chapter title is not the neutral handbook title' });
  if (!/^lang:\s*["']?en["']?\s*$/m.test(source)) reviewFindings.push({ file: relativeFile, issue: 'Missing or non-English lang frontmatter' });
  if (!/^translationKey:\s*\S+/m.test(source)) reviewFindings.push({ file: relativeFile, issue: 'Missing translationKey frontmatter' });
  const sourcePages = sourcePageRanges.get(book)?.get(path.basename(file, '.mdx'));
  if (!sourcePages) reviewFindings.push({ file: relativeFile, issue: 'Missing source PDF page range' });

  const body = source.replace(/^---[\s\S]*?---\s*/, '');
  const text = body
    .replace(/<Quiz\b[\s\S]*?\/>/g, ' ')
    .replace(/<img\b[^>]*\/>/g, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/[#>*_`~]/g, ' ')
    .replace(/\s+/g, ' ').trim();
  searchEntries.push({
    book: bookTitles[book],
    chapter: Number(chapterNumber),
    href: `/subjects/${book}/${path.basename(file, '.mdx')}/`,
    sourcePageStart: sourcePages?.startPage,
    sourcePageEnd: sourcePages?.endPage,
    text,
  });

  if (/[\u0400-\u04FF]/.test(body)) reviewFindings.push({ file: relativeFile, issue: 'Cyrillic text found in an English handbook lesson' });
  if (/[\uFFFD\u25A0\u25A1]{2,}|\{(?:TAF text|[^}]{1,40})\}/i.test(body.replace(/<Quiz\b[\s\S]*?\/>/g, ''))) {
    reviewFindings.push({ file: relativeFile, issue: 'Possible OCR corruption or unresolved placeholder' });
  }

  for (const match of source.matchAll(/<img\b[^>]*\bsrc=["']([^"']+)["']/g)) {
    const imageUrl = match[1];
    if (!imageUrl.startsWith('/images/')) throw new Error(`Image must use a local /images URL in ${path.relative(root, file)}`);
    const imagePath = path.resolve(publicRoot, imageUrl.slice(1));
    if (!imagePath.startsWith(`${path.join(publicRoot, 'images')}${path.sep}`)) throw new Error(`Invalid image path ${imageUrl}`);
    if (!(await fileExists(imagePath))) throw new Error(`Missing lesson image ${imageUrl} in ${path.relative(root, file)}`);
    referencedImages.add(imageUrl);
  }

  const imageManifestPath = path.join(parsedRoot, book, path.basename(file, '.mdx'), 'images_manifest.json');
  try {
    const imageManifest = JSON.parse(await readFile(imageManifestPath, 'utf8'));
    const lessonFigures = [];
    for (const image of imageManifest.images || []) {
      const imageUrl = image.relativePath;
      if (typeof imageUrl !== 'string' || !imageUrl.startsWith('/images/') || source.includes(imageUrl)) continue;
      const imagePath = path.resolve(publicRoot, imageUrl.slice(1));
      if (imagePath.startsWith(`${path.join(publicRoot, 'images')}${path.sep}`) && await fileExists(imagePath)) {
        lessonFigures.push(imageUrl);
      }
      if (lessonFigures.length === 8) break;
    }
    lessonFigures.forEach((imageUrl) => referencedImages.add(imageUrl));
  } catch {
    // Some chapters may not have an image manifest.
  }
}

const searchIndexPath = path.join(outRoot, 'search-index.json');
await writeFile(searchIndexPath, JSON.stringify(searchEntries), 'utf8');
if (JSON.parse(await readFile(searchIndexPath, 'utf8')).length !== lessonFiles.length) {
  throw new Error('Search index does not contain every lesson');
}
await writeFile(path.join(outRoot, 'content-review-report.json'), JSON.stringify({ lessonCount: lessonFiles.length, findings: reviewFindings }, null, 2), 'utf8');

const outputImages = path.join(outRoot, 'images');
await rm(outputImages, { recursive: true, force: true });
for (const imageUrl of referencedImages) {
  const relative = imageUrl.slice(1);
  const destinationPath = path.join(outRoot, relative);
  await mkdir(path.dirname(destinationPath), { recursive: true });
  await cp(path.join(publicRoot, relative), destinationPath);
}

for (const book of Object.keys(bookTitles)) {
  await stat(path.join(outRoot, 'subjects', book, 'index.html'));
  const chapters = lessonFiles.filter((file) => path.basename(path.dirname(file)) === book);
  for (const file of chapters) {
    const chapter = path.basename(file, '.mdx');
    await stat(path.join(outRoot, 'subjects', book, chapter, 'index.html'));
  }
}
for (const entry of searchEntries) {
  if (!(await localTargetExists(new URL(`${basePath}${entry.href}`, 'https://pages.local').pathname))) {
    throw new Error(`Search result does not resolve to an exported lesson: ${entry.href}`);
  }
}

const htmlFiles = (await walk(outRoot)).filter((file) => file.endsWith('.html'));
const missingLinks = new Set();
for (const file of htmlFiles) {
  const html = await readFile(file, 'utf8');
  for (const match of html.matchAll(/(?:href|src)=["']([^"']+)["']/g)) {
    const urlValue = match[1];
    if (!urlValue.startsWith('/') || urlValue.startsWith('//')) continue;
    const url = new URL(urlValue, 'https://pages.local');
    if (!(await localTargetExists(url.pathname))) missingLinks.add(`${path.relative(outRoot, file)} -> ${urlValue}`);
  }
}
if (missingLinks.size) throw new Error(`Broken local links or assets:\n${[...missingLinks].slice(0, 30).join('\n')}`);

const quizPage = await readFile(path.join(outRoot, 'subjects', 'PHAK', 'ch01', 'index.html'), 'utf8');
if (!quizPage.includes('Knowledge check')) throw new Error('The sample chapter quiz was not rendered in the static export');

console.log(`Verified ${lessonFiles.length} lessons, ${htmlFiles.length} HTML pages, and ${referencedImages.size} referenced images.`);
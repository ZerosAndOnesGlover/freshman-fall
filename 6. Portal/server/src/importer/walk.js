import fs from 'node:fs';
import path from 'node:path';
import { VAULT_ROOT } from '../paths.js';

export const YEAR_DIRS = [
  { dir: '0. Freshman', yearNum: 1, label: 'Freshman' },
  { dir: '1. Sophomore', yearNum: 2, label: 'Sophomore' },
  { dir: '2. Junior', yearNum: 3, label: 'Junior' },
  { dir: '3. Senior', yearNum: 4, label: 'Senior' },
];

export const rel = (full) => path.relative(VAULT_ROOT, full).split(path.sep).join('/');

export function readIfExists(full) {
  try {
    return fs.readFileSync(full, 'utf8');
  } catch {
    return null;
  }
}

export function listDirs(full) {
  try {
    return fs.readdirSync(full, { withFileTypes: true })
      .filter((e) => e.isDirectory() && !e.name.startsWith('.'))
      .map((e) => e.name)
      .sort((a, b) => a.localeCompare(b, 'en', { numeric: true }));
  } catch {
    return [];
  }
}

export function listFiles(full) {
  try {
    return fs.readdirSync(full, { withFileTypes: true })
      .filter((e) => e.isFile() && !e.name.startsWith('.'))
      .map((e) => e.name)
      .sort((a, b) => a.localeCompare(b, 'en', { numeric: true }));
  } catch {
    return [];
  }
}

/**
 * Course folders are named "0. CS 101 - Computer Science I: Foundations..."
 * Returns the code, the title, and the subtitle after the colon.
 */
export function parseCourseFolder(name) {
  const m = /^(\d+)\.\s+([A-Z]{2,4}\s?\d{3})\s*[-–—]\s*(.+)$/.exec(name);
  if (!m) return null;
  const code = m[2].replace(/\s+/g, ' ').trim();
  const rest = m[3].trim();
  const colon = rest.indexOf(':');
  return {
    order: Number(m[1]),
    code: /\s/.test(code) ? code : code.replace(/([A-Z]+)(\d+)/, '$1 $2'),
    title: colon > 0 ? rest.slice(0, colon).trim() : rest,
    subtitle: colon > 0 ? rest.slice(colon + 1).trim() : null,
  };
}

/** Week folders are named "CS101 Week3". */
export function parseWeekFolder(name) {
  const m = /Week\s*(\d+)/i.exec(name);
  return m ? Number(m[1]) : null;
}

/** Which bucket a week-folder subdirectory maps to. */
export const MATERIAL_KINDS = {
  lectures: 'lecture',
  assignments: 'assignment',
  lab: 'lab',
  labs: 'lab',
  quiz: 'quiz',
  quizzes: 'quiz',
  resources: 'resource',
  ps0: 'assignment',
  solutions_instructor: 'solution',
};

export function titleFromFilename(filename) {
  return filename
    .replace(/\.[A-Za-z0-9]+$/, '')
    .replace(/[_-]+/g, ' ')
    .replace(/\s{2,}/g, ' ')
    .trim();
}

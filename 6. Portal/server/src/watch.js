#!/usr/bin/env node
/**
 * Watches the vault and re-imports when course material changes.
 *
 * Lecture and material *bodies* are always read live from disk, so editing an
 * existing file shows up on the next page load with no import at all. What the
 * database holds is the index: which courses, weeks, lectures and assessments
 * exist. A NEW file, week or course only appears once that index is rebuilt —
 * which is what this does.
 *
 * The import is an upsert, so re-running it is safe: submissions, uploads and
 * grades entered in the portal are preserved.
 *
 *   npm run watch          (also started by `npm run dev`)
 */
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { VAULT_ROOT } from './paths.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const IMPORTER = path.join(HERE, 'importer', 'run.js');

/** Only these carry course content; everything else is noise. */
const WATCHED_EXT = new Set(['.md', '.py', '.c', '.h', '.cpp', '.js', '.sql', '.txt', '.csv']);

/** Directories that change constantly and never feed the import. */
const IGNORED = [
  `${path.sep}6. Portal${path.sep}`,
  `${path.sep}.git${path.sep}`,
  `${path.sep}node_modules${path.sep}`,
  `${path.sep}.obsidian${path.sep}`,
  `${path.sep}__pycache__${path.sep}`,
  `${path.sep}Submissions${path.sep}`,
];

const DEBOUNCE_MS = 1500;

let timer = null;
let running = false;
let queued = false;
let pending = new Set();

function interesting(file) {
  if (!file) return false;
  const full = path.join(VAULT_ROOT, file);
  if (IGNORED.some((frag) => `${path.sep}${file}`.includes(frag))) return false;
  // Editors write swap and temp files constantly.
  const base = path.basename(file);
  if (base.startsWith('.') || base.startsWith('~') || base.endsWith('~')) return false;
  return WATCHED_EXT.has(path.extname(full).toLowerCase());
}

function runImport() {
  if (running) { queued = true; return; }
  running = true;

  const changed = [...pending];
  pending = new Set();
  const summary = changed.length === 1
    ? path.basename(changed[0])
    : `${changed.length} files`;
  console.log(`\n· vault changed (${summary}) — re-importing`);

  const child = spawn(process.execPath, [IMPORTER], { stdio: ['ignore', 'pipe', 'pipe'] });
  let out = '';
  child.stdout.on('data', (d) => { out += d.toString(); });
  child.stderr.on('data', (d) => process.stderr.write(d));

  child.on('exit', (code) => {
    running = false;
    if (code === 0) {
      const line = out.split('\n').find((l) => l.includes('courses ·')) || '';
      console.log(`· import complete${line ? ` —${line.replace('·', '')}` : ''}`);
    } else {
      console.error(`· import failed (exit ${code})`);
    }
    if (queued) { queued = false; schedule(); }
  });
}

function schedule() {
  clearTimeout(timer);
  timer = setTimeout(runImport, DEBOUNCE_MS);
}

console.log(`  watching ${VAULT_ROOT}`);
console.log('  new lectures, weeks and courses are indexed automatically\n');

try {
  fs.watch(VAULT_ROOT, { recursive: true }, (_event, file) => {
    if (!interesting(file)) return;
    pending.add(file);
    schedule();
  });
} catch (err) {
  console.error('  could not watch the vault:', err.message);
  console.error('  run `npm run import` by hand after adding material.');
  process.exit(1);
}

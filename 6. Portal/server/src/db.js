import fs from 'node:fs';
import path from 'node:path';
import Database from 'better-sqlite3';
import { DB_PATH, SCHEMA_PATH } from './paths.js';

fs.mkdirSync(path.dirname(DB_PATH), { recursive: true });

/**
 * The drop has to happen here, before the connection is opened. ESM hoists
 * every `import` above the importing module's own statements, so a `--reset`
 * handled in run.js would unlink a file this module already had open — writes
 * would land in the unlinked inode and disappear when the process exits.
 */
export const wasReset = process.argv.includes('--reset') || process.env.PORTAL_RESET === '1';
if (wasReset) {
  for (const suffix of ['', '-wal', '-shm']) {
    try { fs.unlinkSync(DB_PATH + suffix); } catch { /* not there */ }
  }
}

export const db = new Database(DB_PATH);
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');

/** Idempotent: schema.sql is all CREATE ... IF NOT EXISTS. */
export function migrate() {
  db.exec(fs.readFileSync(SCHEMA_PATH, 'utf8'));
}

migrate();

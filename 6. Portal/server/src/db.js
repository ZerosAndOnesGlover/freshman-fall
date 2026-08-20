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

/**
 * Columns added to a table that already exists.
 *
 * schema.sql is all `CREATE TABLE IF NOT EXISTS`, which does nothing to a
 * table that is already there. Adding a column to an existing database
 * therefore needs an explicit ALTER, or an upgrade would silently require a
 * full re-import and lose submissions.
 */
const ADDED_COLUMNS = [
  ['lectures', 'start_time', 'TEXT'],
  ['lectures', 'end_time', 'TEXT'],
  // Plain INTEGER, no REFERENCES: SQLite cannot add a foreign key to an
  // existing table with ALTER TABLE, and a column added this way would leave
  // the schema and the constraint out of step. The cohort link is enforced in
  // the admin routes instead.
  ['users', 'cohort_id', 'INTEGER'],
  ['users', 'status', "TEXT NOT NULL DEFAULT 'active'"],
  ['users', 'must_change_password', 'INTEGER NOT NULL DEFAULT 0'],
];

function addMissingColumns() {
  for (const [table, column, ddl] of ADDED_COLUMNS) {
    const exists = db.prepare(`SELECT 1 FROM pragma_table_info(?) WHERE name = ?`).get(table, column);
    if (!exists) db.exec(`ALTER TABLE ${table} ADD COLUMN ${column} ${ddl}`);
  }
}

/** Idempotent: schema.sql is all CREATE ... IF NOT EXISTS, then ALTERs. */
export function migrate() {
  db.exec(fs.readFileSync(SCHEMA_PATH, 'utf8'));
  addMissingColumns();
}

migrate();

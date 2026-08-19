/**
 * Reading vault files back off disk.
 *
 * Lecture and material bodies are NOT copied into the database — the markdown
 * on disk stays the single source of truth, and the portal renders it live.
 * Every path stored in the database is vault-relative and every read goes
 * through resolveVaultPath(), which refuses anything outside the vault.
 */
import fs from 'node:fs';
import path from 'node:path';
import { resolveVaultPath } from './paths.js';

const TEXT_EXT = new Set(['.md', '.markdown', '.txt', '.py', '.c', '.h', '.cpp', '.js', '.ts',
  '.java', '.sql', '.sh', '.csv', '.json', '.yml', '.yaml', '.html', '.css', '.rs', '.go']);

export function isTextFile(p) {
  return TEXT_EXT.has(path.extname(p || '').toLowerCase());
}

/** Returns { text, bytes, mtime } or null when the file is gone or out of bounds. */
export function readVaultFile(relative) {
  const full = resolveVaultPath(relative);
  if (!full) return null;
  let stat;
  try {
    stat = fs.statSync(full);
  } catch {
    return null;
  }
  if (!stat.isFile()) return null;
  return {
    text: fs.readFileSync(full, 'utf8'),
    bytes: stat.size,
    mtime: stat.mtime.toISOString(),
    full,
  };
}

/** Strips a YAML frontmatter block, returning just the body. */
export function stripFrontmatter(text) {
  const m = /^---\n([\s\S]*?)\n---\n?/.exec(text);
  return m ? text.slice(m[0].length) : text;
}

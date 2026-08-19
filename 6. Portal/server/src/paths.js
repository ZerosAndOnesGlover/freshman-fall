import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));

/** server/src -> server */
export const SERVER_ROOT = path.resolve(here, '..');
/** server -> 6. Portal */
export const PORTAL_ROOT = path.resolve(SERVER_ROOT, '..');
/** 6. Portal -> the vault itself */
export const VAULT_ROOT = process.env.VAULT_ROOT
  ? path.resolve(process.env.VAULT_ROOT)
  : path.resolve(PORTAL_ROOT, '..');

export const DB_PATH = process.env.PORTAL_DB
  ? path.resolve(process.env.PORTAL_DB)
  : path.join(SERVER_ROOT, 'data', 'portal.db');

export const UPLOAD_DIR = process.env.PORTAL_UPLOADS
  ? path.resolve(process.env.PORTAL_UPLOADS)
  : path.join(SERVER_ROOT, 'uploads');

export const SCHEMA_PATH = path.join(here, 'schema.sql');

/**
 * Vault paths are stored relative to VAULT_ROOT so the database stays portable.
 * Resolving one back to disk must never escape the vault — every path that
 * reaches the filesystem goes through here.
 */
export function resolveVaultPath(relative) {
  if (typeof relative !== 'string' || relative.length === 0) return null;
  const full = path.resolve(VAULT_ROOT, relative);
  const boundary = VAULT_ROOT.endsWith(path.sep) ? VAULT_ROOT : VAULT_ROOT + path.sep;
  if (full !== VAULT_ROOT && !full.startsWith(boundary)) return null;
  return full;
}

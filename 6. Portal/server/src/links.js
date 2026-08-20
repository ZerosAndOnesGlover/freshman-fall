/**
 * Obsidian wikilinks.
 *
 * The vault cross-references itself with `[[L02 Python Environment and REPL]]`
 * and `[[full/path/to/file|Display text]]`. Those are meaningless to a markdown
 * renderer, so they were being printed with their brackets showing.
 *
 * Resolution happens here, on the server, because only the server knows what
 * the vault contains. A target is turned into a link ONLY when it matches
 * something real; anything else is left exactly as written. That matters
 * because the notes also contain things like `[[lst[0]]` — array syntax that
 * merely looks like a wikilink, and must not be mangled.
 */
import { db } from './db.js';

const WIKILINK = /\[\[([^\]\n|]+)(?:\|([^\]\n]+))?\]\]/g;

const byLecturePath = db.prepare(
  "SELECT id, title, course_id FROM lectures WHERE path LIKE '%/' || ? || '.md' LIMIT 1");
const byLectureTitle = db.prepare(
  'SELECT id, title, course_id FROM lectures WHERE title = ? COLLATE NOCASE LIMIT 1');
const byMaterialPath = db.prepare(
  "SELECT id, title, course_id, kind FROM materials WHERE path LIKE '%/' || ? || '.%' LIMIT 1");
const byMaterialTitle = db.prepare(
  'SELECT id, title, course_id, kind FROM materials WHERE title = ? COLLATE NOCASE LIMIT 1');
const assessmentByLabel = db.prepare(
  'SELECT id, label FROM assessments WHERE course_id = ? AND label = ? COLLATE NOCASE LIMIT 1');

/** "0. Freshman/Fall/CS 101/x/LAB 0 Setup" -> "LAB 0 Setup" */
function basename(target) {
  const cut = target.split(/[\\/]/).pop() || target;
  return cut.replace(/\.(md|markdown)$/i, '').trim();
}

function lookup(target, courseId) {
  const name = basename(target);
  if (!name || name.length < 2) return null;

  const lecture = byLecturePath.get(name) || byLectureTitle.get(name);
  if (lecture) return { kind: 'lecture', id: lecture.id, title: lecture.title };

  const material = byMaterialPath.get(name) || byMaterialTitle.get(name);
  if (material) return { kind: 'material', id: material.id, title: material.title };

  if (courseId) {
    const a = assessmentByLabel.get(courseId, name);
    if (a) return { kind: 'assessment', id: a.id, title: a.label };
  }
  return null;
}

/**
 * Scans a body and returns { "<raw target>": {kind, id, title} } for every
 * wikilink that resolves. Targets that resolve to nothing are simply absent,
 * and the client leaves those untouched.
 */
export function resolveWikilinks(body, courseId = null) {
  if (!body || !body.includes('[[')) return {};

  // Fenced code is off limits — a wikilink-looking token there is code.
  const withoutFences = body.replace(/(^|\n)\s*(```|~~~)[\s\S]*?\n\s*\2/g, '\n');

  const out = {};
  const seen = new Set();
  let m;
  WIKILINK.lastIndex = 0;
  while ((m = WIKILINK.exec(withoutFences)) !== null) {
    const target = m[1].trim();
    if (seen.has(target)) continue;
    seen.add(target);
    const hit = lookup(target, courseId);
    if (hit) out[target] = hit;
  }
  return out;
}

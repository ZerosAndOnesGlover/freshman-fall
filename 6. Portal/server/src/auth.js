import crypto from 'node:crypto';
import { db } from './db.js';

const SCRYPT = { N: 16384, r: 8, p: 1, keylen: 64 };
const SESSION_DAYS = 14;
export const SESSION_COOKIE = 'ist_session';

/** scrypt is in Node's stdlib, so the portal needs no native crypto dependency. */
export function hashPassword(plain) {
  const salt = crypto.randomBytes(16);
  const key = crypto.scryptSync(plain, salt, SCRYPT.keylen, SCRYPT);
  return `scrypt$${SCRYPT.N}$${SCRYPT.r}$${SCRYPT.p}$${salt.toString('hex')}$${key.toString('hex')}`;
}

export function verifyPassword(plain, stored) {
  try {
    const [scheme, N, r, p, saltHex, keyHex] = String(stored).split('$');
    if (scheme !== 'scrypt') return false;
    const salt = Buffer.from(saltHex, 'hex');
    const expected = Buffer.from(keyHex, 'hex');
    const actual = crypto.scryptSync(plain, salt, expected.length, {
      N: Number(N), r: Number(r), p: Number(p),
    });
    return crypto.timingSafeEqual(actual, expected);
  } catch {
    return false;
  }
}

export function createSession(userId) {
  const token = crypto.randomBytes(32).toString('hex');
  const expires = new Date(Date.now() + SESSION_DAYS * 86400_000).toISOString();
  db.prepare('INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)')
    .run(token, userId, expires);
  return { token, expires };
}

export function destroySession(token) {
  if (token) db.prepare('DELETE FROM sessions WHERE token = ?').run(token);
}

export function userForToken(token) {
  if (!token) return null;
  const row = db.prepare(`
    SELECT u.id, u.email, u.role, u.full_name, u.student_id, u.title, u.programme,
           u.year_level, u.cohort_id, u.status, u.must_change_password
      FROM sessions s JOIN users u ON u.id = s.user_id
     WHERE s.token = ? AND s.expires_at > datetime('now')
  `).get(token);
  if (!row) return null;
  if (row.status && row.status !== 'active') return null;
  return row;
}

export function purgeExpiredSessions() {
  db.prepare("DELETE FROM sessions WHERE expires_at <= datetime('now')").run();
}

// ─── Express middleware ────────────────────────────────────────────────

export function attachUser(req, _res, next) {
  req.user = userForToken(req.cookies?.[SESSION_COOKIE]);
  next();
}

export function requireAuth(req, res, next) {
  if (!req.user) return res.status(401).json({ error: 'Not signed in' });
  next();
}

export function requireRole(...roles) {
  return (req, res, next) => {
    if (!req.user) return res.status(401).json({ error: 'Not signed in' });
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'You do not have access to this area' });
    }
    next();
  };
}

/** True when the user teaches (or assists) the course, or is an admin. */
export function teaches(user, courseId) {
  if (!user) return false;
  if (user.role === 'admin') return true;
  const row = db.prepare('SELECT 1 FROM course_staff WHERE course_id = ? AND user_id = ?')
    .get(courseId, user.id);
  return Boolean(row);
}

export function isEnrolled(user, courseId) {
  if (!user) return false;
  const row = db.prepare("SELECT 1 FROM enrollments WHERE course_id = ? AND user_id = ? AND status = 'enrolled'")
    .get(courseId, user.id);
  return Boolean(row);
}

import express from 'express';
import { db } from '../db.js';
import {
  SESSION_COOKIE, verifyPassword, hashPassword, createSession, destroySession, requireAuth,
} from '../auth.js';

const router = express.Router();

const COOKIE_OPTS = {
  httpOnly: true,
  sameSite: 'lax',
  path: '/',
  // The portal is served over http on localhost by design; flip this on behind TLS.
  secure: process.env.NODE_ENV === 'production',
};

router.post('/login', (req, res) => {
  const { email, password } = req.body || {};
  if (!email || !password) return res.status(400).json({ error: 'Email and password are required' });

  const row = db.prepare('SELECT * FROM users WHERE email = ?').get(String(email).trim());
  // Same message either way — a wrong email must not be distinguishable from a
  // wrong password.
  if (!row || !verifyPassword(password, row.password_hash)) {
    return res.status(401).json({ error: 'Those credentials were not recognised' });
  }

  const { token, expires } = createSession(row.id);
  res.cookie(SESSION_COOKIE, token, { ...COOKIE_OPTS, expires: new Date(expires) });
  res.json({ user: publicUser(row) });
});

router.post('/logout', (req, res) => {
  destroySession(req.cookies?.[SESSION_COOKIE]);
  res.clearCookie(SESSION_COOKIE, COOKIE_OPTS);
  res.json({ ok: true });
});

router.get('/me', (req, res) => {
  if (!req.user) return res.json({ user: null });
  res.json({ user: req.user });
});

router.get('/me/profile', requireAuth, (req, res) => {
  const staff = db.prepare(`
    SELECT c.code, c.title, cs.staff_role, cs.office_hours
      FROM course_staff cs JOIN courses c ON c.id = cs.course_id
     WHERE cs.user_id = ?
  `).all(req.user.id);
  res.json({ user: req.user, staff });
});

/**
 * Change your own password.
 *
 * Students admitted by the registrar start with a temporary password and are
 * flagged to change it. Every other signed-in session for that account is
 * ended, so a shared temporary password stops working everywhere at once.
 */
router.post('/password', requireAuth, (req, res) => {
  const { current_password: current, new_password: next } = req.body || {};
  if (!next || String(next).length < 8) {
    return res.status(400).json({ error: 'Choose a password of at least 8 characters' });
  }

  const row = db.prepare('SELECT * FROM users WHERE id = ?').get(req.user.id);
  if (!verifyPassword(current || '', row.password_hash)) {
    return res.status(401).json({ error: 'That is not your current password' });
  }

  const keep = req.cookies?.[SESSION_COOKIE];
  db.transaction(() => {
    db.prepare('UPDATE users SET password_hash = ?, must_change_password = 0 WHERE id = ?')
      .run(hashPassword(next), row.id);
    db.prepare('DELETE FROM sessions WHERE user_id = ? AND token <> ?').run(row.id, keep || '');
  })();

  res.json({ ok: true });
});

function publicUser(row) {
  const { password_hash, ...rest } = row;
  return rest;
}

export default router;

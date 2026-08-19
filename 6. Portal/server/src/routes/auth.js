import express from 'express';
import { db } from '../db.js';
import {
  SESSION_COOKIE, verifyPassword, createSession, destroySession, requireAuth,
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

function publicUser(row) {
  const { password_hash, ...rest } = row;
  return rest;
}

export default router;

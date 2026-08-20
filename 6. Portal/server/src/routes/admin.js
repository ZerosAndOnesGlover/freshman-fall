/**
 * Registry administration: academic sessions, intakes and student records.
 *
 * A *session* is a calendar academic year ("2027/2028"). A student's *cohort*
 * is the session they were admitted in. Terms in this database stay
 * degree-relative ("Year 1 Fall"), so a cohort is what maps them onto real
 * calendar years — which is what lets a second intake run alongside the first.
 */
import crypto from 'node:crypto';
import express from 'express';
import { db } from '../db.js';
import { requireAuth, requireRole, hashPassword } from '../auth.js';

const router = express.Router();
router.use(requireAuth, requireRole('admin'));

// ─── Overview ──────────────────────────────────────────────────────────

router.get('/overview', (_req, res) => {
  const current = db.prepare('SELECT * FROM academic_sessions WHERE is_current = 1').get() || null;
  res.json({
    current_session: current,
    sessions: db.prepare('SELECT COUNT(*) n FROM academic_sessions').get().n,
    students: db.prepare("SELECT COUNT(*) n FROM users WHERE role = 'student' AND status = 'active'").get().n,
    staff: db.prepare("SELECT COUNT(*) n FROM users WHERE role IN ('instructor','admin')").get().n,
    courses: db.prepare('SELECT COUNT(*) n FROM courses').get().n,
    enrolments: db.prepare("SELECT COUNT(*) n FROM enrollments WHERE status = 'enrolled'").get().n,
    submissions: db.prepare('SELECT COUNT(*) n FROM submissions').get().n,
    intakes: db.prepare(`
      SELECT s.id, s.label, s.start_year, s.is_current, COUNT(u.id) AS students
        FROM academic_sessions s
        LEFT JOIN users u ON u.cohort_id = s.id AND u.role = 'student' AND u.status = 'active'
       GROUP BY s.id ORDER BY s.start_year
    `).all(),
  });
});

// ─── Sessions ──────────────────────────────────────────────────────────

router.get('/sessions', (_req, res) => {
  res.json(db.prepare(`
    SELECT s.*, COUNT(u.id) AS students
      FROM academic_sessions s
      LEFT JOIN users u ON u.cohort_id = s.id AND u.role = 'student' AND u.status = 'active'
     GROUP BY s.id ORDER BY s.start_year
  `).all());
});

router.post('/sessions', (req, res) => {
  const startYear = Number(req.body?.start_year);
  if (!Number.isInteger(startYear) || startYear < 2000 || startYear > 2100) {
    return res.status(400).json({ error: 'Give a starting year between 2000 and 2100' });
  }
  if (db.prepare('SELECT 1 FROM academic_sessions WHERE start_year = ?').get(startYear)) {
    return res.status(409).json({ error: `The ${startYear}/${startYear + 1} session already exists` });
  }

  const label = `${startYear}/${startYear + 1}`;
  const info = db.prepare(`
    INSERT INTO academic_sessions (label, start_year, end_year, starts_on, ends_on, note)
    VALUES (?, ?, ?, ?, ?, ?)
  `).run(label, startYear, startYear + 1,
    req.body?.starts_on || null, req.body?.ends_on || null, req.body?.note || null);

  res.status(201).json(db.prepare('SELECT * FROM academic_sessions WHERE id = ?').get(info.lastInsertRowid));
});

router.patch('/sessions/:id', (req, res) => {
  const s = db.prepare('SELECT * FROM academic_sessions WHERE id = ?').get(Number(req.params.id));
  if (!s) return res.status(404).json({ error: 'No such session' });

  const { starts_on, ends_on, note, is_current } = req.body || {};
  db.prepare(`
    UPDATE academic_sessions
       SET starts_on = COALESCE(?, starts_on), ends_on = COALESCE(?, ends_on),
           note = COALESCE(?, note)
     WHERE id = ?
  `).run(starts_on ?? null, ends_on ?? null, note ?? null, s.id);

  // Exactly one session is current at a time.
  if (is_current) {
    db.transaction(() => {
      db.prepare('UPDATE academic_sessions SET is_current = 0').run();
      db.prepare('UPDATE academic_sessions SET is_current = 1 WHERE id = ?').run(s.id);
    })();
  }
  res.json(db.prepare('SELECT * FROM academic_sessions WHERE id = ?').get(s.id));
});

router.delete('/sessions/:id', (req, res) => {
  const id = Number(req.params.id);
  const s = db.prepare('SELECT * FROM academic_sessions WHERE id = ?').get(id);
  if (!s) return res.status(404).json({ error: 'No such session' });
  if (s.is_current) return res.status(409).json({ error: 'Make another session current first' });

  const holds = db.prepare("SELECT COUNT(*) n FROM users WHERE cohort_id = ? AND role = 'student'").get(id).n;
  if (holds) return res.status(409).json({ error: `${holds} student(s) are in this intake` });

  db.prepare('DELETE FROM academic_sessions WHERE id = ?').run(id);
  res.json({ ok: true });
});

// ─── People ────────────────────────────────────────────────────────────

router.get('/students', (req, res) => {
  const where = [];
  const args = [];
  if (req.query.cohort) { where.push('u.cohort_id = ?'); args.push(Number(req.query.cohort)); }
  if (req.query.q) { where.push('(u.full_name LIKE ? OR u.email LIKE ? OR u.student_id LIKE ?)');
    const like = `%${req.query.q}%`; args.push(like, like, like); }

  res.json(db.prepare(`
    SELECT u.id, u.full_name, u.email, u.student_id, u.year_level, u.status, u.programme,
           u.cohort_id, s.label AS cohort,
           (SELECT COUNT(*) FROM enrollments e WHERE e.user_id = u.id AND e.status = 'enrolled') AS courses,
           (SELECT COUNT(*) FROM submissions sub WHERE sub.user_id = u.id) AS submissions
      FROM users u
      LEFT JOIN academic_sessions s ON s.id = u.cohort_id
     WHERE u.role = 'student' ${where.length ? 'AND ' + where.join(' AND ') : ''}
     ORDER BY u.status, u.full_name
  `).all(...args));
});

/**
 * Admit a student. The temporary password is generated here and returned once,
 * for the registrar to pass on; only its hash is stored.
 */
router.post('/students', (req, res) => {
  const fullName = String(req.body?.full_name || '').trim();
  const email = String(req.body?.email || '').trim().toLowerCase();
  const cohortId = Number(req.body?.cohort_id);
  const yearLevel = Number(req.body?.year_level) || 1;

  if (!fullName) return res.status(400).json({ error: 'A name is required' });
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return res.status(400).json({ error: 'That is not a valid email address' });
  if (db.prepare('SELECT 1 FROM users WHERE email = ?').get(email)) {
    return res.status(409).json({ error: 'Someone already has that email address' });
  }
  const cohort = db.prepare('SELECT * FROM academic_sessions WHERE id = ?').get(cohortId);
  if (!cohort) return res.status(400).json({ error: 'Choose the session they are joining' });

  const studentId = req.body?.student_id?.trim() || nextStudentId(cohort.start_year);
  if (db.prepare('SELECT 1 FROM users WHERE student_id = ?').get(studentId)) {
    return res.status(409).json({ error: `Registry number ${studentId} is taken` });
  }

  const password = temporaryPassword();
  const info = db.prepare(`
    INSERT INTO users (email, password_hash, role, full_name, student_id, programme,
                       year_level, cohort_id, status, must_change_password)
    VALUES (?, ?, 'student', ?, ?, ?, ?, ?, 'active', 1)
  `).run(email, hashPassword(password), fullName, studentId,
    req.body?.programme || 'B.Sc. Computer Science & Engineering', yearLevel, cohortId);

  res.status(201).json({
    student: db.prepare('SELECT id, full_name, email, student_id, year_level, cohort_id FROM users WHERE id = ?')
      .get(info.lastInsertRowid),
    temporary_password: password,
  });
});

router.patch('/students/:id', (req, res) => {
  const u = db.prepare("SELECT * FROM users WHERE id = ? AND role = 'student'").get(Number(req.params.id));
  if (!u) return res.status(404).json({ error: 'No such student' });

  const { full_name, year_level, cohort_id, status, programme } = req.body || {};
  if (status && !['active', 'inactive'].includes(status)) {
    return res.status(400).json({ error: 'Status must be active or inactive' });
  }
  db.prepare(`
    UPDATE users SET full_name = COALESCE(?, full_name),
                     year_level = COALESCE(?, year_level),
                     cohort_id = COALESCE(?, cohort_id),
                     programme = COALESCE(?, programme),
                     status = COALESCE(?, status)
     WHERE id = ?
  `).run(full_name ?? null, year_level ?? null, cohort_id ?? null, programme ?? null, status ?? null, u.id);

  res.json(db.prepare('SELECT id, full_name, email, student_id, year_level, cohort_id, status FROM users WHERE id = ?').get(u.id));
});

/** Issue a fresh temporary password and end any signed-in sessions. */
router.post('/students/:id/reset-password', (req, res) => {
  const u = db.prepare("SELECT * FROM users WHERE id = ? AND role = 'student'").get(Number(req.params.id));
  if (!u) return res.status(404).json({ error: 'No such student' });

  const password = temporaryPassword();
  db.transaction(() => {
    db.prepare('UPDATE users SET password_hash = ?, must_change_password = 1 WHERE id = ?')
      .run(hashPassword(password), u.id);
    db.prepare('DELETE FROM sessions WHERE user_id = ?').run(u.id);
  })();
  res.json({ temporary_password: password });
});

// ─── Enrolment ─────────────────────────────────────────────────────────

/** The courses that make up one year of the degree. */
router.get('/year-courses/:yearNum', (req, res) => {
  res.json(db.prepare(`
    SELECT c.id, c.code, c.title, c.credits, t.label AS term, t.semester
      FROM courses c JOIN terms t ON t.id = c.term_id
     WHERE t.year_num = ?
     ORDER BY CASE t.semester WHEN 'Fall' THEN 0 ELSE 1 END, c.code
  `).all(Number(req.params.yearNum)));
});

/**
 * Enrol a student in every course of a degree year. Existing enrolments are
 * left alone, so this is safe to run twice.
 */
router.post('/students/:id/enrol', (req, res) => {
  const u = db.prepare("SELECT * FROM users WHERE id = ? AND role = 'student'").get(Number(req.params.id));
  if (!u) return res.status(404).json({ error: 'No such student' });

  const yearNum = Number(req.body?.year_num);
  const semester = req.body?.semester || null;   // optional: "Fall" | "Spring"
  if (!Number.isInteger(yearNum) || yearNum < 1 || yearNum > 4) {
    return res.status(400).json({ error: 'Choose a year between 1 and 4' });
  }

  const courses = db.prepare(`
    SELECT c.id FROM courses c JOIN terms t ON t.id = c.term_id
     WHERE t.year_num = ? ${semester ? 'AND t.semester = ?' : ''}
  `).all(...(semester ? [yearNum, semester] : [yearNum]));

  const ins = db.prepare(`
    INSERT INTO enrollments (user_id, course_id, status) VALUES (?, ?, 'enrolled')
    ON CONFLICT (user_id, course_id) DO UPDATE SET status = 'enrolled'
  `);
  db.transaction(() => { for (const c of courses) ins.run(u.id, c.id); })();

  res.json({ enrolled: courses.length, year_num: yearNum, semester });
});

router.delete('/students/:id/enrolments', (req, res) => {
  const id = Number(req.params.id);
  const yearNum = Number(req.query.year_num);
  if (!Number.isInteger(yearNum)) return res.status(400).json({ error: 'Which year?' });

  const info = db.prepare(`
    DELETE FROM enrollments WHERE user_id = ? AND course_id IN
      (SELECT c.id FROM courses c JOIN terms t ON t.id = c.term_id WHERE t.year_num = ?)
  `).run(id, yearNum);
  res.json({ removed: info.changes });
});

// ─── helpers ───────────────────────────────────────────────────────────

/** "IST-2027-0001", counting within the intake year. */
function nextStudentId(startYear) {
  const row = db.prepare(
    "SELECT student_id FROM users WHERE student_id LIKE ? ORDER BY student_id DESC LIMIT 1"
  ).get(`IST-${startYear}-%`);
  const last = row ? Number(row.student_id.split('-').pop()) : 0;
  return `IST-${startYear}-${String(last + 1).padStart(4, '0')}`;
}

/**
 * A temporary password that can be read down a phone: no ambiguous characters,
 * and enough entropy that it cannot be guessed before it is changed.
 */
function temporaryPassword() {
  const alphabet = 'abcdefghjkmnpqrstuvwxyz23456789';
  const bytes = crypto.randomBytes(12);
  let out = '';
  for (let i = 0; i < 12; i += 1) {
    out += alphabet[bytes[i] % alphabet.length];
    if (i === 3 || i === 7) out += '-';
  }
  return out;
}

export default router;

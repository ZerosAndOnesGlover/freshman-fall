/**
 * The teaching timetable: what a student has on a given day.
 *
 * Built from the dates the importer read out of each lecture's own header, so
 * it reflects the vault rather than a separately maintained schedule.
 */
import express from 'express';
import { db } from '../db.js';
import { requireAuth } from '../auth.js';

const router = express.Router();

const ISO = /^\d{4}-\d{2}-\d{2}$/;

/**
 * Courses the user is attached to, either enrolled or teaching.
 *
 * The registrar is attached to nothing, so restricting by enrolment would show
 * them an empty timetable. Administrators see the whole institution instead,
 * which is the view that is actually useful to them.
 */
const MINE = `
  (SELECT course_id FROM enrollments WHERE user_id = ? AND status = 'enrolled'
   UNION SELECT course_id FROM course_staff WHERE user_id = ?)
`;
const ALL_COURSES = '(SELECT id FROM courses)';

/** Returns [scopeSql, args] for the signed-in user. */
function scope(user) {
  return user.role === 'admin'
    ? [ALL_COURSES, []]
    : [MINE, [user.id, user.id]];
}

function lecturesOn(user, date) {
  const [where, args] = scope(user);
  return db.prepare(`
    SELECT l.id, l.code, l.title, l.subtitle, l.date_iso, l.date_text,
           l.start_time, l.end_time, l.week_id,
           c.id AS course_id, c.code AS course_code, c.title AS course_title,
           c.room, c.schedule, w.week_num,
           (SELECT u.full_name FROM course_staff cs JOIN users u ON u.id = cs.user_id
             WHERE cs.course_id = c.id AND cs.staff_role = 'instructor' LIMIT 1) AS instructor
      FROM lectures l
      JOIN courses c ON c.id = l.course_id
      LEFT JOIN weeks w ON w.id = l.week_id
     WHERE l.date_iso = ? AND l.course_id IN ${where}
     ORDER BY l.start_time IS NULL, l.start_time, c.code
  `).all(date, ...args);
}

function dueOn(user, date) {
  const [where, args] = scope(user);
  return db.prepare(`
    SELECT a.id, a.label, a.kind, a.possible, a.due_date, a.due_time, a.accepts_upload,
           c.id AS course_id, c.code AS course_code,
           s.status AS submission_status, g.score
      FROM assessments a
      JOIN courses c ON c.id = a.course_id
      LEFT JOIN submissions s ON s.assessment_id = a.id AND s.user_id = ?
      LEFT JOIN grades g ON g.assessment_id = a.id AND g.user_id = ?
     WHERE a.due_date = ? AND a.course_id IN ${where}
     ORDER BY a.due_time, c.code
  `).all(user.id, user.id, date, ...args);
}

function eventsOn(date) {
  return db.prepare(
    'SELECT id, title, kind, course_code, detail FROM calendar_events WHERE date_iso = ? ORDER BY kind'
  ).all(date);
}

/** One day. `date` defaults to the server's today; the client sends its own. */
router.get('/day', requireAuth, (req, res) => {
  const date = ISO.test(req.query.date || '') ? req.query.date : today();
  res.json({
    date,
    lectures: lecturesOn(req.user, date),
    due: dueOn(req.user, date),
    events: eventsOn(date),
  });
});

/**
 * A span of days, for the week strip. Counts only — enough to show which days
 * have something on them without loading every lecture.
 */
router.get('/range', requireAuth, (req, res) => {
  const from = ISO.test(req.query.from || '') ? req.query.from : today();
  const to = ISO.test(req.query.to || '') ? req.query.to : from;

  const [where, args] = scope(req.user);

  const lectures = db.prepare(`
    SELECT date_iso AS date, COUNT(*) AS n FROM lectures
     WHERE date_iso BETWEEN ? AND ? AND course_id IN ${where}
     GROUP BY date_iso
  `).all(from, to, ...args);

  const due = db.prepare(`
    SELECT due_date AS date, COUNT(*) AS n FROM assessments
     WHERE due_date BETWEEN ? AND ? AND course_id IN ${where}
     GROUP BY due_date
  `).all(from, to, ...args);

  const byDate = {};
  for (const r of lectures) byDate[r.date] = { ...(byDate[r.date] || {}), lectures: r.n };
  for (const r of due) byDate[r.date] = { ...(byDate[r.date] || {}), due: r.n };
  res.json({ from, to, days: byDate });
});

/** The next day at or after `date` that has anything on it. */
router.get('/next', requireAuth, (req, res) => {
  const from = ISO.test(req.query.from || '') ? req.query.from : today();
  const [where, args] = scope(req.user);
  const row = db.prepare(`
    SELECT MIN(date_iso) AS date FROM lectures
     WHERE date_iso > ? AND course_id IN ${where}
  `).get(from, ...args);
  res.json({ date: row?.date || null });
});

/** The weekly pattern, for a "usual week" view: which weekday, which time. */
router.get('/pattern', requireAuth, (req, res) => {
  const [scopeSql, scopeArgs] = scope(req.user);
  const rows = db.prepare(`
    SELECT c.id AS course_id, c.code AS course_code, c.title AS course_title, c.schedule,
           l.start_time, l.end_time,
           CAST(strftime('%w', l.date_iso) AS INTEGER) AS weekday,
           COUNT(*) AS occurrences
      FROM lectures l
      JOIN courses c ON c.id = l.course_id
      JOIN terms t ON t.id = c.term_id
     WHERE l.date_iso IS NOT NULL AND l.start_time IS NOT NULL
       AND t.is_current = 1 AND l.course_id IN ${scopeSql}
     GROUP BY c.id, l.start_time, weekday
     ORDER BY weekday, l.start_time, c.code
  `).all(...scopeArgs);
  res.json(rows);
});

function today() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

export default router;

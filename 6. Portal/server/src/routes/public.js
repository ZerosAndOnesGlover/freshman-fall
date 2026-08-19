/** Everything the public site shows — no sign-in required. */
import express from 'express';
import { db } from '../db.js';

const router = express.Router();

router.get('/institution', (_req, res) => {
  const terms = db.prepare(
    "SELECT * FROM terms ORDER BY year_num, CASE semester WHEN 'Fall' THEN 0 ELSE 1 END"
  ).all();
  const stats = {
    courses: db.prepare('SELECT COUNT(*) AS n FROM courses').get().n,
    lectures: db.prepare('SELECT COUNT(*) AS n FROM lectures').get().n,
    materials: db.prepare('SELECT COUNT(*) AS n FROM materials').get().n,
    faculty: db.prepare("SELECT COUNT(DISTINCT user_id) AS n FROM course_staff WHERE staff_role = 'instructor'").get().n,
  };
  res.json({
    name: 'Institute of Science & Technology',
    school: 'School of Computer Science & Engineering',
    degree: 'B.Sc. Computer Science & Engineering',
    terms,
    stats,
  });
});

router.get('/pages', (_req, res) => {
  res.json(db.prepare('SELECT slug, title, summary, nav_group FROM pages ORDER BY nav_group, title').all());
});

router.get('/pages/:slug', (req, res) => {
  const page = db.prepare('SELECT * FROM pages WHERE slug = ?').get(req.params.slug);
  if (!page) return res.status(404).json({ error: 'No such page' });
  res.json(page);
});

/** The full four-year catalogue, grouped by term. */
router.get('/catalog', (_req, res) => {
  const rows = db.prepare(`
    SELECT c.id, c.code, c.title, c.subtitle, c.credits, c.schedule, c.has_material,
           t.id AS term_id, t.label AS term, t.year_num, t.year_label, t.semester, t.is_current,
           (SELECT u.full_name FROM course_staff cs JOIN users u ON u.id = cs.user_id
             WHERE cs.course_id = c.id AND cs.staff_role = 'instructor' LIMIT 1) AS instructor,
           (SELECT COUNT(*) FROM weeks w WHERE w.course_id = c.id) AS week_count,
           (SELECT COUNT(*) FROM lectures l WHERE l.course_id = c.id) AS lecture_count
      FROM courses c LEFT JOIN terms t ON t.id = c.term_id
     ORDER BY t.year_num, CASE t.semester WHEN 'Fall' THEN 0 ELSE 1 END, c.code
  `).all();

  const terms = [];
  const index = new Map();
  for (const r of rows) {
    const key = r.term_id ?? 'none';
    if (!index.has(key)) {
      index.set(key, { term_id: r.term_id, label: r.term, year_num: r.year_num, year_label: r.year_label, semester: r.semester, is_current: r.is_current, courses: [] });
      terms.push(index.get(key));
    }
    index.get(key).courses.push(r);
  }
  res.json(terms);
});

router.get('/calendar', (req, res) => {
  const { term, from, to, limit } = req.query;
  const where = [];
  const args = [];
  if (term) { where.push('e.term_id = ?'); args.push(Number(term)); }
  if (from) { where.push('e.date_iso >= ?'); args.push(String(from)); }
  if (to) { where.push('e.date_iso <= ?'); args.push(String(to)); }
  const events = db.prepare(`
    SELECT e.*, t.label AS term_label FROM calendar_events e
      LEFT JOIN terms t ON t.id = e.term_id
    ${where.length ? 'WHERE ' + where.join(' AND ') : ''}
     ORDER BY e.date_iso LIMIT ?
  `).all(...args, Number(limit) || 500);
  res.json(events);
});

router.get('/announcements', (_req, res) => {
  res.json(db.prepare(`
    SELECT a.*, c.code AS course_code FROM announcements a
      LEFT JOIN courses c ON c.id = a.course_id
     WHERE a.course_id IS NULL
     ORDER BY a.pinned DESC, a.created_at DESC LIMIT 20
  `).all());
});

router.get('/grade-scale', (_req, res) => {
  res.json(db.prepare('SELECT letter, points, low, high, descriptor FROM grade_scale ORDER BY low DESC').all());
});

/** Faculty directory, built from the office-hours file the importer read. */
router.get('/faculty', (_req, res) => {
  res.json(db.prepare(`
    SELECT u.id, u.full_name, u.title, u.email, cs.staff_role,
           GROUP_CONCAT(c.code, ' · ') AS courses,
           MAX(cs.office_hours) AS office_hours
      FROM course_staff cs
      JOIN users u ON u.id = cs.user_id
      JOIN courses c ON c.id = cs.course_id
     GROUP BY u.id, cs.staff_role
     ORDER BY cs.staff_role, u.full_name
  `).all());
});

export default router;

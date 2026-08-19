/** Courses, weeks, lectures and materials — the course browser. */
import express from 'express';
import { db } from '../db.js';
import { requireAuth, teaches, isEnrolled } from '../auth.js';
import { readVaultFile, isTextFile } from '../vault.js';
import { resolveVaultPath } from '../paths.js';

const router = express.Router();

/** Courses the signed-in user is attached to, as student or as staff. */
router.get('/mine', requireAuth, (req, res) => {
  const rows = db.prepare(`
    SELECT c.id, c.code, c.title, c.subtitle, c.credits, c.schedule, c.room, c.status,
           c.has_material, t.label AS term, t.year_num, t.semester, t.is_current,
           CASE WHEN cs.id IS NOT NULL THEN cs.staff_role ELSE 'student' END AS my_role,
           (SELECT COUNT(*) FROM weeks w WHERE w.course_id = c.id) AS week_count,
           (SELECT COUNT(*) FROM lectures l WHERE l.course_id = c.id) AS lecture_count,
           (SELECT COUNT(*) FROM assessments a WHERE a.course_id = c.id) AS assessment_count,
           (SELECT u.full_name FROM course_staff s2 JOIN users u ON u.id = s2.user_id
             WHERE s2.course_id = c.id AND s2.staff_role = 'instructor' LIMIT 1) AS instructor
      FROM courses c
      LEFT JOIN terms t ON t.id = c.term_id
      LEFT JOIN enrollments e ON e.course_id = c.id AND e.user_id = ? AND e.status = 'enrolled'
      LEFT JOIN course_staff cs ON cs.course_id = c.id AND cs.user_id = ?
     WHERE e.id IS NOT NULL OR cs.id IS NOT NULL
     ORDER BY t.is_current DESC, t.year_num DESC, CASE t.semester WHEN 'Spring' THEN 0 ELSE 1 END, c.code
  `).all(req.user.id, req.user.id);
  res.json(rows);
});

router.get('/:id', (req, res) => {
  const id = Number(req.params.id);
  const course = db.prepare(`
    SELECT c.*, t.label AS term, t.year_num, t.year_label, t.semester, t.is_current
      FROM courses c LEFT JOIN terms t ON t.id = c.term_id WHERE c.id = ?
  `).get(id);
  if (!course) return res.status(404).json({ error: 'No such course' });

  course.staff = db.prepare(`
    SELECT u.id, u.full_name, u.title, u.email, cs.staff_role, cs.office_hours
      FROM course_staff cs JOIN users u ON u.id = cs.user_id
     WHERE cs.course_id = ? ORDER BY cs.staff_role, u.full_name
  `).all(id);

  course.components = db.prepare(
    'SELECT id, name, weight, drop_lowest, formative FROM components WHERE course_id = ? ORDER BY formative, position, name'
  ).all(id);

  course.weeks = db.prepare(`
    SELECT w.*, (SELECT COUNT(*) FROM lectures l WHERE l.week_id = w.id) AS lecture_count,
           (SELECT COUNT(*) FROM materials m WHERE m.week_id = w.id) AS material_count
      FROM weeks w WHERE w.course_id = ? ORDER BY w.week_num
  `).all(id);

  course.announcements = db.prepare(
    'SELECT * FROM announcements WHERE course_id = ? ORDER BY pinned DESC, created_at DESC LIMIT 10'
  ).all(id);

  course.my_role = req.user
    ? (teaches(req.user, id) ? 'staff' : (isEnrolled(req.user, id) ? 'student' : null))
    : null;

  res.json(course);
});

router.get('/:id/weeks/:num', (req, res) => {
  const courseId = Number(req.params.id);
  const week = db.prepare('SELECT * FROM weeks WHERE course_id = ? AND week_num = ?')
    .get(courseId, Number(req.params.num));
  if (!week) return res.status(404).json({ error: 'No such week' });

  week.lectures = db.prepare(
    'SELECT id, seq, code, title, subtitle, date_text, date_iso FROM lectures WHERE week_id = ? ORDER BY seq, id'
  ).all(week.id);
  week.materials = db.prepare(
    'SELECT id, kind, title, filename, ext FROM materials WHERE week_id = ? ORDER BY kind, title'
  ).all(week.id);
  week.assessments = db.prepare(`
    SELECT id, label, topic, kind, possible, due_date, due_time, accepts_upload
      FROM assessments WHERE week_id = ? ORDER BY position, label
  `).all(week.id);

  if (week.readme_path) {
    const file = readVaultFile(week.readme_path);
    week.readme = file ? file.text : null;
  }
  res.json(week);
});

export default router;

// Lectures and materials get their own routers: they are addressed by their own
// id, not through a course, so /api/lectures/12 reads better than
// /api/courses/lectures/12.
export const lectureRouter = express.Router();
export const materialRouter = express.Router();

/** A lecture, rendered live from the markdown on disk. */
lectureRouter.get('/:id', (req, res) => {
  const lecture = db.prepare(`
    SELECT l.*, c.code AS course_code, c.title AS course_title, w.week_num
      FROM lectures l
      JOIN courses c ON c.id = l.course_id
      LEFT JOIN weeks w ON w.id = l.week_id
     WHERE l.id = ?
  `).get(Number(req.params.id));
  if (!lecture) return res.status(404).json({ error: 'No such lecture' });

  const file = readVaultFile(lecture.path);
  if (!file) return res.status(410).json({ error: 'The source file is no longer in the vault', lecture });

  // Previous/next within the course, by the same ordering the browser uses.
  const siblings = db.prepare(
    'SELECT id, seq, code, title FROM lectures WHERE course_id = ? ORDER BY seq, id'
  ).all(lecture.course_id);
  const i = siblings.findIndex((s) => s.id === lecture.id);

  res.json({
    ...lecture,
    body_md: file.text,
    mtime: file.mtime,
    prev: i > 0 ? siblings[i - 1] : null,
    next: i >= 0 && i < siblings.length - 1 ? siblings[i + 1] : null,
  });
});

/** A material file: markdown/text inline, anything else as a download. */
materialRouter.get('/:id', (req, res) => {
  const m = db.prepare(`
    SELECT m.*, c.code AS course_code FROM materials m
      JOIN courses c ON c.id = m.course_id WHERE m.id = ?
  `).get(Number(req.params.id));
  if (!m) return res.status(404).json({ error: 'No such material' });

  if (req.query.download === '1' || !isTextFile(m.path)) {
    const full = resolveVaultPath(m.path);
    if (!full) return res.status(404).json({ error: 'File not available' });
    return res.download(full, m.filename);
  }

  const file = readVaultFile(m.path);
  if (!file) return res.status(410).json({ error: 'The source file is no longer in the vault' });
  res.json({ ...m, body_md: file.text, mtime: file.mtime });
});

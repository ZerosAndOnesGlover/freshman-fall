/** Instructor side: the submission queue, marking, and announcements. */
import express from 'express';
import { db } from '../db.js';
import { requireAuth, requireRole, teaches } from '../auth.js';

const router = express.Router();

router.use(requireAuth, requireRole('instructor', 'admin'));

/** Courses this member of staff teaches, with a count of work waiting. */
router.get('/courses', (req, res) => {
  const rows = db.prepare(`
    SELECT c.id, c.code, c.title, c.credits, cs.staff_role, t.label AS term, t.is_current,
           (SELECT COUNT(*) FROM enrollments e WHERE e.course_id = c.id AND e.status = 'enrolled') AS students,
           (SELECT COUNT(*) FROM submissions s JOIN assessments a ON a.id = s.assessment_id
             WHERE a.course_id = c.id AND s.status IN ('submitted','late')) AS awaiting
      FROM course_staff cs
      JOIN courses c ON c.id = cs.course_id
      LEFT JOIN terms t ON t.id = c.term_id
     WHERE cs.user_id = ?
     ORDER BY t.is_current DESC, c.code
  `).all(req.user.id);
  res.json(rows);
});

/** Everything handed in and not yet marked, across this user's courses. */
router.get('/queue', (req, res) => {
  const rows = db.prepare(`
    SELECT s.id AS submission_id, s.status, s.submitted_at, s.comment,
           a.id AS assessment_id, a.label, a.kind, a.possible, a.due_date,
           c.id AS course_id, c.code AS course_code,
           u.id AS student_id, u.full_name AS student_name, u.student_id AS student_number,
           g.score,
           (SELECT COUNT(*) FROM submission_files f WHERE f.submission_id = s.id) AS file_count
      FROM submissions s
      JOIN assessments a ON a.id = s.assessment_id
      JOIN courses c ON c.id = a.course_id
      JOIN course_staff cs ON cs.course_id = c.id AND cs.user_id = ?
      JOIN users u ON u.id = s.user_id
      LEFT JOIN grades g ON g.assessment_id = a.id AND g.user_id = s.user_id
     WHERE s.status IN ('submitted','late')
     ORDER BY s.submitted_at
  `).all(req.user.id);
  res.json(rows);
});

/** Every student's standing on one assessment — the marking screen. */
router.get('/assessments/:id/submissions', (req, res) => {
  const a = db.prepare(`
    SELECT a.*, c.code AS course_code, c.title AS course_title
      FROM assessments a JOIN courses c ON c.id = a.course_id WHERE a.id = ?
  `).get(Number(req.params.id));
  if (!a) return res.status(404).json({ error: 'No such assessment' });
  if (!teaches(req.user, a.course_id)) return res.status(403).json({ error: 'Not your course' });

  const rows = db.prepare(`
    SELECT u.id AS student_id, u.full_name, u.student_id AS student_number,
           s.id AS submission_id, s.status, s.submitted_at, s.body_text, s.comment,
           g.score, g.excused, g.feedback, g.graded_at
      FROM enrollments e
      JOIN users u ON u.id = e.user_id
      LEFT JOIN submissions s ON s.assessment_id = ? AND s.user_id = u.id
      LEFT JOIN grades g ON g.assessment_id = ? AND g.user_id = u.id
     WHERE e.course_id = ? AND e.status = 'enrolled'
     ORDER BY u.full_name
  `).all(a.id, a.id, a.course_id);

  const files = db.prepare(`
    SELECT f.id, f.original_name, f.size_bytes, f.submission_id, s.user_id
      FROM submission_files f JOIN submissions s ON s.id = f.submission_id
     WHERE s.assessment_id = ?
  `).all(a.id);
  const byUser = new Map();
  for (const f of files) {
    if (!byUser.has(f.user_id)) byUser.set(f.user_id, []);
    byUser.get(f.user_id).push(f);
  }

  res.json({ assessment: a, students: rows.map((r) => ({ ...r, files: byUser.get(r.student_id) || [] })) });
});

/** Record a mark. Writing a grade here always claims it for the portal. */
router.post('/assessments/:id/grade', (req, res) => {
  const a = db.prepare('SELECT * FROM assessments WHERE id = ?').get(Number(req.params.id));
  if (!a) return res.status(404).json({ error: 'No such assessment' });
  if (!teaches(req.user, a.course_id)) return res.status(403).json({ error: 'Not your course' });

  const { student_id, score, excused = 0, feedback = null } = req.body || {};
  if (!student_id) return res.status(400).json({ error: 'Which student?' });

  const numeric = score === null || score === undefined || score === '' ? null : Number(score);
  if (numeric !== null && (Number.isNaN(numeric) || numeric < 0)) {
    return res.status(400).json({ error: 'A score must be a number, or blank' });
  }
  if (numeric !== null && a.possible && numeric > a.possible * 1.5) {
    return res.status(400).json({ error: `That is more than 150% of the ${a.possible} available` });
  }

  const sub = db.prepare(
    'SELECT id FROM submissions WHERE assessment_id = ? AND user_id = ? ORDER BY attempt DESC LIMIT 1'
  ).get(a.id, student_id);

  db.prepare(`
    INSERT INTO grades (assessment_id, user_id, submission_id, score, excused, feedback, graded_by, graded_at, source)
    VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), 'portal')
    ON CONFLICT (assessment_id, user_id) DO UPDATE SET
      submission_id = excluded.submission_id, score = excluded.score,
      excused = excluded.excused, feedback = excluded.feedback,
      graded_by = excluded.graded_by, graded_at = excluded.graded_at,
      source = 'portal'
  `).run(a.id, student_id, sub?.id ?? null, numeric, excused ? 1 : 0, feedback, req.user.id);

  if (sub) db.prepare("UPDATE submissions SET status = 'graded' WHERE id = ?").run(sub.id);

  res.json(db.prepare('SELECT * FROM grades WHERE assessment_id = ? AND user_id = ?').get(a.id, student_id));
});

/** Post an announcement to a course. */
router.post('/courses/:id/announcements', (req, res) => {
  const courseId = Number(req.params.id);
  if (!teaches(req.user, courseId)) return res.status(403).json({ error: 'Not your course' });
  const { title, body, category = 'notice', pinned = 0 } = req.body || {};
  if (!title || !body) return res.status(400).json({ error: 'A title and a body are required' });

  const info = db.prepare(
    'INSERT INTO announcements (course_id, author_id, title, body, category, pinned) VALUES (?, ?, ?, ?, ?, ?)'
  ).run(courseId, req.user.id, title, body, category, pinned ? 1 : 0);
  res.status(201).json(db.prepare('SELECT * FROM announcements WHERE id = ?').get(info.lastInsertRowid));
});

export default router;

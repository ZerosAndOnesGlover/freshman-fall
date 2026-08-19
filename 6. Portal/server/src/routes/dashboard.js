/** One call that fills the portal home page. */
import express from 'express';
import { db } from '../db.js';
import { requireAuth } from '../auth.js';
import { transcript } from '../grading.js';

const router = express.Router();

router.get('/', requireAuth, (req, res) => {
  const uid = req.user.id;
  const term = db.prepare('SELECT * FROM terms WHERE is_current = 1').get()
    || db.prepare('SELECT * FROM terms ORDER BY year_num DESC, semester LIMIT 1').get();

  if (req.user.role !== 'student') {
    const courses = db.prepare(`
      SELECT c.id, c.code, c.title, cs.staff_role,
             (SELECT COUNT(*) FROM enrollments e WHERE e.course_id = c.id AND e.status = 'enrolled') AS students,
             (SELECT COUNT(*) FROM submissions s JOIN assessments a ON a.id = s.assessment_id
               WHERE a.course_id = c.id AND s.status IN ('submitted','late')) AS awaiting
        FROM course_staff cs JOIN courses c ON c.id = cs.course_id
       WHERE cs.user_id = ? ORDER BY c.code
    `).all(uid);
    return res.json({ role: req.user.role, term, courses, announcements: announcements(uid) });
  }

  const courses = db.prepare(`
    SELECT c.id, c.code, c.title, c.subtitle, c.credits, c.schedule, c.has_material,
           t.label AS term, t.is_current,
           (SELECT u.full_name FROM course_staff cs JOIN users u ON u.id = cs.user_id
             WHERE cs.course_id = c.id AND cs.staff_role = 'instructor' LIMIT 1) AS instructor
      FROM enrollments e JOIN courses c ON c.id = e.course_id
      LEFT JOIN terms t ON t.id = c.term_id
     WHERE e.user_id = ? AND e.status = 'enrolled'
       AND (t.is_current = 1 OR t.id IS NULL)
     ORDER BY c.code
  `).all(uid);

  const otherCourses = db.prepare(`
    SELECT COUNT(*) AS n FROM enrollments e
      JOIN courses c ON c.id = e.course_id
      LEFT JOIN terms t ON t.id = c.term_id
     WHERE e.user_id = ? AND e.status = 'enrolled' AND COALESCE(t.is_current, 0) = 0
  `).get(uid).n;

  const upcoming = db.prepare(`
    SELECT a.id, a.label, a.kind, a.possible, a.due_date, a.due_time, a.accepts_upload,
           c.id AS course_id, c.code AS course_code,
           s.status AS submission_status
      FROM assessments a
      JOIN courses c ON c.id = a.course_id
      JOIN enrollments e ON e.course_id = c.id AND e.user_id = ? AND e.status = 'enrolled'
      LEFT JOIN submissions s ON s.assessment_id = a.id AND s.user_id = ?
     WHERE a.due_date IS NOT NULL AND a.due_date >= date('now')
     ORDER BY a.due_date, a.due_time LIMIT 8
  `).all(uid, uid);

  const recentGrades = db.prepare(`
    SELECT g.score, g.excused, g.graded_at, a.label, a.possible, a.kind,
           c.id AS course_id, c.code AS course_code
      FROM grades g
      JOIN assessments a ON a.id = g.assessment_id
      JOIN courses c ON c.id = a.course_id
     WHERE g.user_id = ? AND g.score IS NOT NULL
     ORDER BY g.graded_at IS NULL, g.graded_at DESC, a.due_date DESC LIMIT 6
  `).all(uid);

  const t = transcript(uid);
  const currentTerm = t.terms.find((x) => x.is_current) || null;

  res.json({
    role: 'student',
    term,
    courses,
    other_course_count: otherCourses,
    upcoming,
    recent_grades: recentGrades,
    standing: {
      cumulative_gpa: t.cumulative,
      term_gpa: currentTerm?.gpa ?? null,
      credits_earned: t.credits_earned,
      credits_enrolled: t.credits_enrolled,
      courses_in_progress: t.courses_in_progress,
    },
    announcements: announcements(uid),
  });
});

/** University-wide notices, plus anything posted to the user's own courses. */
function announcements(uid) {
  return db.prepare(`
    SELECT a.*, c.code AS course_code FROM announcements a
      LEFT JOIN courses c ON c.id = a.course_id
     WHERE a.course_id IS NULL
        OR a.course_id IN (SELECT course_id FROM enrollments WHERE user_id = ? AND status = 'enrolled')
        OR a.course_id IN (SELECT course_id FROM course_staff WHERE user_id = ?)
     ORDER BY a.pinned DESC, a.created_at DESC LIMIT 8
  `).all(uid, uid);
}

export default router;

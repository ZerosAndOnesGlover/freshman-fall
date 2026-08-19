/** Gradebook and transcript views. */
import express from 'express';
import { db } from '../db.js';
import { requireAuth, teaches, isEnrolled } from '../auth.js';
import { courseGrade, transcript, gradeScale } from '../grading.js';

const router = express.Router();

/** One line per enrolled course: the grades landing page. */
router.get('/summary', requireAuth, (req, res) => {
  res.json(transcript(req.user.id));
});

router.get('/transcript', requireAuth, (req, res) => {
  const t = transcript(req.user.id);
  res.json({
    student: req.user,
    scale: gradeScale(),
    ...t,
  });
});

/** The full component-by-component gradebook for one course. */
router.get('/course/:courseId', requireAuth, (req, res) => {
  const courseId = Number(req.params.courseId);
  const course = db.prepare(`
    SELECT c.id, c.code, c.title, c.subtitle, c.credits, t.label AS term
      FROM courses c LEFT JOIN terms t ON t.id = c.term_id WHERE c.id = ?
  `).get(courseId);
  if (!course) return res.status(404).json({ error: 'No such course' });

  // A member of staff may look at any enrolled student; a student only at their own.
  let userId = req.user.id;
  if (req.query.student) {
    if (!teaches(req.user, courseId)) return res.status(403).json({ error: 'Not your course' });
    userId = Number(req.query.student);
  } else if (!isEnrolled(req.user, courseId) && !teaches(req.user, courseId)) {
    return res.status(403).json({ error: 'You are not enrolled in this course' });
  }

  res.json({ course, student_id: userId, ...courseGrade(courseId, userId) });
});

export default router;

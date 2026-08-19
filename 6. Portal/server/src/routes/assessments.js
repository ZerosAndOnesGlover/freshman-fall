/** Assessments, and the student submission flow. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import express from 'express';
import multer from 'multer';
import { db } from '../db.js';
import { requireAuth, teaches, isEnrolled } from '../auth.js';
import { readVaultFile } from '../vault.js';
import { UPLOAD_DIR } from '../paths.js';

const router = express.Router();

fs.mkdirSync(UPLOAD_DIR, { recursive: true });

const upload = multer({
  storage: multer.diskStorage({
    destination: (_req, _file, cb) => cb(null, UPLOAD_DIR),
    // Never trust the client's filename on disk: store under a random name and
    // keep the original only as a label in the database.
    filename: (_req, file, cb) =>
      cb(null, `${crypto.randomBytes(12).toString('hex')}${path.extname(file.originalname).slice(0, 10)}`),
  }),
  limits: { fileSize: 25 * 1024 * 1024, files: 10 },
});

const nowIso = () => new Date().toISOString().replace('T', ' ').slice(0, 19);

/** Everything due soon across the student's courses. */
router.get('/upcoming', requireAuth, (req, res) => {
  const days = Number(req.query.days) || 45;
  const rows = db.prepare(`
    SELECT a.id, a.label, a.topic, a.kind, a.possible, a.due_date, a.due_time,
           a.accepts_upload, a.room,
           c.id AS course_id, c.code AS course_code, c.title AS course_title,
           s.status AS submission_status, s.submitted_at,
           g.score, g.excused
      FROM assessments a
      JOIN courses c ON c.id = a.course_id
      JOIN enrollments e ON e.course_id = c.id AND e.user_id = ? AND e.status = 'enrolled'
      LEFT JOIN submissions s ON s.assessment_id = a.id AND s.user_id = ?
      LEFT JOIN grades g ON g.assessment_id = a.id AND g.user_id = ?
     WHERE a.due_date IS NOT NULL
       AND a.due_date >= date('now')
       AND a.due_date <= date('now', ?)
     ORDER BY a.due_date, a.due_time
  `).all(req.user.id, req.user.id, req.user.id, `+${days} days`);
  res.json(rows);
});

/** Anything past its due date that was never submitted. */
router.get('/outstanding', requireAuth, (req, res) => {
  const rows = db.prepare(`
    SELECT a.id, a.label, a.kind, a.possible, a.due_date, a.due_time,
           c.id AS course_id, c.code AS course_code
      FROM assessments a
      JOIN courses c ON c.id = a.course_id
      JOIN enrollments e ON e.course_id = c.id AND e.user_id = ? AND e.status = 'enrolled'
      LEFT JOIN submissions s ON s.assessment_id = a.id AND s.user_id = ?
      LEFT JOIN grades g ON g.assessment_id = a.id AND g.user_id = ?
     WHERE a.accepts_upload = 1
       AND a.due_date IS NOT NULL AND a.due_date < date('now')
       AND (s.id IS NULL OR s.status = 'draft')
       AND g.score IS NULL
     ORDER BY a.due_date DESC
  `).all(req.user.id, req.user.id, req.user.id);
  res.json(rows);
});

router.get('/course/:courseId', requireAuth, (req, res) => {
  const courseId = Number(req.params.courseId);
  const rows = db.prepare(`
    SELECT a.*, cp.name AS component, cp.weight AS component_weight, w.week_num,
           s.id AS submission_id, s.status AS submission_status, s.submitted_at,
           g.score, g.excused, g.feedback
      FROM assessments a
      LEFT JOIN components cp ON cp.id = a.component_id
      LEFT JOIN weeks w ON w.id = a.week_id
      LEFT JOIN submissions s ON s.assessment_id = a.id AND s.user_id = ?
      LEFT JOIN grades g ON g.assessment_id = a.id AND g.user_id = ?
     WHERE a.course_id = ?
     ORDER BY a.due_date IS NULL, a.due_date, a.position, a.label
  `).all(req.user.id, req.user.id, courseId);
  res.json(rows);
});

router.get('/:id', requireAuth, (req, res) => {
  const a = loadAssessment(Number(req.params.id));
  if (!a) return res.status(404).json({ error: 'No such assessment' });

  const staff = teaches(req.user, a.course_id);
  if (!staff && !isEnrolled(req.user, a.course_id)) {
    return res.status(403).json({ error: 'You are not enrolled in this course' });
  }

  // The brief itself is the vault markdown, read live.
  if (a.doc_path) {
    const file = readVaultFile(a.doc_path);
    a.brief_md = file ? file.text : null;
  }

  a.submission = db.prepare(
    'SELECT * FROM submissions WHERE assessment_id = ? AND user_id = ? ORDER BY attempt DESC LIMIT 1'
  ).get(a.id, req.user.id) || null;
  if (a.submission) a.submission.files = filesFor(a.submission.id);

  a.grade = db.prepare(`
    SELECT g.score, g.excused, g.feedback, g.graded_at, g.source, u.full_name AS graded_by_name
      FROM grades g LEFT JOIN users u ON u.id = g.graded_by
     WHERE g.assessment_id = ? AND g.user_id = ?
  `).get(a.id, req.user.id) || null;

  a.can_submit = Boolean(a.accepts_upload) && !staff;
  res.json(a);
});

// ─── Submitting ────────────────────────────────────────────────────────

/** Create or update the working draft. Idempotent — one draft per assessment. */
router.put('/:id/submission', requireAuth, (req, res) => {
  const a = loadAssessment(Number(req.params.id));
  if (!a) return res.status(404).json({ error: 'No such assessment' });
  const guard = submitGuard(req.user, a);
  if (guard) return res.status(guard.status).json({ error: guard.error });

  const { body_text = null, comment = null } = req.body || {};
  const existing = currentSubmission(a.id, req.user.id);

  if (existing && existing.status !== 'draft') {
    return res.status(409).json({ error: 'This work has already been submitted' });
  }

  if (existing) {
    db.prepare("UPDATE submissions SET body_text = ?, comment = ?, updated_at = datetime('now') WHERE id = ?")
      .run(body_text, comment, existing.id);
  } else {
    db.prepare('INSERT INTO submissions (assessment_id, user_id, body_text, comment, status) VALUES (?, ?, ?, ?, ?)')
      .run(a.id, req.user.id, body_text, comment, 'draft');
  }
  res.json(withFiles(currentSubmission(a.id, req.user.id)));
});

/** Hand it in. A draft past its due date is recorded as late, not refused. */
router.post('/:id/submit', requireAuth, (req, res) => {
  const a = loadAssessment(Number(req.params.id));
  if (!a) return res.status(404).json({ error: 'No such assessment' });
  const guard = submitGuard(req.user, a);
  if (guard) return res.status(guard.status).json({ error: guard.error });

  const { body_text = null, comment = null } = req.body || {};
  let sub = currentSubmission(a.id, req.user.id);
  if (!sub) {
    db.prepare('INSERT INTO submissions (assessment_id, user_id, body_text, comment, status) VALUES (?, ?, ?, ?, ?)')
      .run(a.id, req.user.id, body_text, comment, 'draft');
    sub = currentSubmission(a.id, req.user.id);
  }
  if (sub.status !== 'draft') {
    return res.status(409).json({ error: 'This work has already been submitted' });
  }

  const files = filesFor(sub.id);
  if (!files.length && !(body_text ?? sub.body_text)) {
    return res.status(400).json({ error: 'Attach a file or write something before submitting' });
  }

  const late = isLate(a);
  db.prepare(`
    UPDATE submissions
       SET body_text = COALESCE(?, body_text), comment = COALESCE(?, comment),
           status = ?, submitted_at = ?, updated_at = datetime('now')
     WHERE id = ?
  `).run(body_text, comment, late ? 'late' : 'submitted', nowIso(), sub.id);

  res.json(withFiles(currentSubmission(a.id, req.user.id)));
});

/** Withdraw a submission back to draft, while it is still unmarked. */
router.post('/:id/unsubmit', requireAuth, (req, res) => {
  const a = loadAssessment(Number(req.params.id));
  if (!a) return res.status(404).json({ error: 'No such assessment' });
  const sub = currentSubmission(a.id, req.user.id);
  if (!sub) return res.status(404).json({ error: 'Nothing submitted yet' });
  if (sub.status === 'graded' || sub.status === 'returned') {
    return res.status(409).json({ error: 'This has already been marked' });
  }
  db.prepare("UPDATE submissions SET status = 'draft', submitted_at = NULL, updated_at = datetime('now') WHERE id = ?")
    .run(sub.id);
  res.json(withFiles(currentSubmission(a.id, req.user.id)));
});

router.post('/:id/files', requireAuth, upload.array('files', 10), (req, res) => {
  const a = loadAssessment(Number(req.params.id));
  if (!a) return res.status(404).json({ error: 'No such assessment' });
  const guard = submitGuard(req.user, a);
  if (guard) {
    cleanup(req.files);
    return res.status(guard.status).json({ error: guard.error });
  }

  let sub = currentSubmission(a.id, req.user.id);
  if (!sub) {
    db.prepare('INSERT INTO submissions (assessment_id, user_id, status) VALUES (?, ?, ?)')
      .run(a.id, req.user.id, 'draft');
    sub = currentSubmission(a.id, req.user.id);
  }
  if (sub.status !== 'draft') {
    cleanup(req.files);
    return res.status(409).json({ error: 'Withdraw the submission before changing its files' });
  }

  const ins = db.prepare(
    'INSERT INTO submission_files (submission_id, original_name, stored_name, size_bytes, mime) VALUES (?, ?, ?, ?, ?)'
  );
  for (const f of req.files || []) ins.run(sub.id, f.originalname, f.filename, f.size, f.mimetype);
  res.json(withFiles(currentSubmission(a.id, req.user.id)));
});

router.delete('/files/:fileId', requireAuth, (req, res) => {
  const row = db.prepare(`
    SELECT f.*, s.user_id, s.status FROM submission_files f
      JOIN submissions s ON s.id = f.submission_id WHERE f.id = ?
  `).get(Number(req.params.fileId));
  if (!row) return res.status(404).json({ error: 'No such file' });
  if (row.user_id !== req.user.id) return res.status(403).json({ error: 'That is not your file' });
  if (row.status !== 'draft') return res.status(409).json({ error: 'Withdraw the submission first' });

  db.prepare('DELETE FROM submission_files WHERE id = ?').run(row.id);
  try { fs.unlinkSync(path.join(UPLOAD_DIR, row.stored_name)); } catch { /* already gone */ }
  res.json({ ok: true });
});

/** Download an uploaded file — the owner, or staff on that course. */
router.get('/files/:fileId', requireAuth, (req, res) => {
  const row = db.prepare(`
    SELECT f.*, s.user_id, a.course_id FROM submission_files f
      JOIN submissions s ON s.id = f.submission_id
      JOIN assessments a ON a.id = s.assessment_id
     WHERE f.id = ?
  `).get(Number(req.params.fileId));
  if (!row) return res.status(404).json({ error: 'No such file' });
  if (row.user_id !== req.user.id && !teaches(req.user, row.course_id)) {
    return res.status(403).json({ error: 'You cannot see that file' });
  }
  res.download(path.join(UPLOAD_DIR, row.stored_name), row.original_name);
});

// ─── helpers ───────────────────────────────────────────────────────────

function loadAssessment(id) {
  return db.prepare(`
    SELECT a.*, c.code AS course_code, c.title AS course_title, cp.name AS component,
           cp.weight AS component_weight, w.week_num
      FROM assessments a
      JOIN courses c ON c.id = a.course_id
      LEFT JOIN components cp ON cp.id = a.component_id
      LEFT JOIN weeks w ON w.id = a.week_id
     WHERE a.id = ?
  `).get(id);
}

function currentSubmission(assessmentId, userId) {
  return db.prepare(
    'SELECT * FROM submissions WHERE assessment_id = ? AND user_id = ? ORDER BY attempt DESC LIMIT 1'
  ).get(assessmentId, userId);
}

function filesFor(submissionId) {
  return db.prepare(
    'SELECT id, original_name, size_bytes, mime, uploaded_at FROM submission_files WHERE submission_id = ? ORDER BY id'
  ).all(submissionId);
}

function withFiles(sub) {
  return sub ? { ...sub, files: filesFor(sub.id) } : null;
}

function submitGuard(user, a) {
  if (user.role !== 'student') return { status: 403, error: 'Only students submit work' };
  if (!isEnrolled(user, a.course_id)) return { status: 403, error: 'You are not enrolled in this course' };
  if (!a.accepts_upload) return { status: 400, error: 'This assessment is not submitted through the portal' };
  return null;
}

function isLate(a) {
  if (!a.due_date) return false;
  const due = new Date(`${a.due_date}T${a.due_time || '23:59'}:00`);
  return Date.now() > due.getTime();
}

function cleanup(files) {
  for (const f of files || []) {
    try { fs.unlinkSync(f.path); } catch { /* nothing to do */ }
  }
}

export default router;

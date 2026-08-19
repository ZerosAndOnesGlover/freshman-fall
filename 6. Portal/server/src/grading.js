/**
 * Course-grade computation.
 *
 * This is a deliberate port of `5. Academic Registry/tools/gpa.py` — the
 * registry's own calculator. The portal and the registry must never disagree
 * about a student's mark, so the three rules below are copied, not reinvented:
 *
 *   1. A component's percentage is the mean of its per-item RATIOS (not the
 *      sum of points over the sum of possible), after dropping the lowest N —
 *      but never dropping the only remaining score.
 *   2. A course percentage is the weighted mean over the components that have
 *      any marks at all, so an in-progress course reports a meaningful figure.
 *   3. A percentage maps to the highest band whose FLOOR it reaches. The
 *      published bands are integer ranges and leave gaps (92.4 sits between
 *      the A− and A bands); 92.99 is an A−, never a fall-through to F.
 */
import { db } from './db.js';

let scaleCache = null;
export function gradeScale() {
  if (!scaleCache) {
    scaleCache = db.prepare('SELECT letter, points, low, high, descriptor FROM grade_scale ORDER BY low DESC').all();
  }
  return scaleCache;
}

export function pctToLetter(pct) {
  if (pct === null || pct === undefined) return null;
  const scale = gradeScale();
  if (!scale.length) return null;
  const p = Math.round(pct * 100) / 100;
  for (const band of scale) if (p >= band.low) return { letter: band.letter, points: band.points, descriptor: band.descriptor };
  const last = scale[scale.length - 1];
  return { letter: last.letter, points: last.points, descriptor: last.descriptor };
}

/** Component percentage from graded items, or null when nothing is marked. */
export function componentPercent(items, dropLowest = 0) {
  const graded = items.filter((i) => i.score !== null && i.score !== undefined && !i.excused);
  if (!graded.length) return null;
  const ratios = graded.map((i) => (i.possible ? i.score / i.possible : 0)).sort((a, b) => a - b);
  const drop = Math.min(dropLowest, Math.max(0, ratios.length - 1));
  const kept = ratios.slice(drop);
  return (100 * kept.reduce((a, b) => a + b, 0)) / kept.length;
}

/**
 * Full gradebook for one student in one course: every component, every item,
 * the component and course percentages, and the letter grade.
 */
export function courseGrade(courseId, userId) {
  const components = db.prepare(`
    SELECT id, name, weight, drop_lowest, formative, position
      FROM components WHERE course_id = ? ORDER BY formative, position, name
  `).all(courseId);

  const items = db.prepare(`
    SELECT a.id, a.component_id, a.label, a.topic, a.kind, a.possible,
           a.due_date, a.due_time, a.accepts_upload, a.doc_path, a.position,
           g.score, g.excused, g.feedback, g.graded_at, g.source,
           s.id AS submission_id, s.status AS submission_status, s.submitted_at
      FROM assessments a
      LEFT JOIN grades g ON g.assessment_id = a.id AND g.user_id = ?
      LEFT JOIN submissions s ON s.assessment_id = a.id AND s.user_id = ?
     WHERE a.course_id = ?
     ORDER BY a.position, a.due_date IS NULL, a.due_date, a.label
  `).all(userId, userId, courseId);

  const byComponent = new Map(components.map((c) => [c.id, []]));
  const orphans = [];
  for (const it of items) {
    const bucket = byComponent.get(it.component_id);
    (bucket || orphans).push(it);
  }

  let num = 0;
  let den = 0;
  const out = components.map((c) => {
    const list = byComponent.get(c.id) || [];
    const pct = componentPercent(list, c.drop_lowest);
    if (pct !== null && !c.formative && c.weight > 0) {
      num += pct * c.weight;
      den += c.weight;
    }
    return {
      ...c,
      drop_lowest: c.drop_lowest,
      percent: pct,
      graded_count: list.filter((i) => i.score !== null && !i.excused).length,
      item_count: list.length,
      items: list,
    };
  });

  const percent = den ? num / den : null;
  const totalWeight = components.filter((c) => !c.formative).reduce((a, c) => a + c.weight, 0);

  return {
    components: out,
    unassigned: orphans,
    percent,
    letter: pctToLetter(percent),
    graded_weight: den,
    total_weight: totalWeight,
    complete: Boolean(out.length) && out.every((c) => c.formative || (c.item_count > 0 && c.graded_count === c.item_count)),
  };
}

/** Every enrolled course for a student, with its current mark. */
export function transcript(userId) {
  const courses = db.prepare(`
    SELECT c.id, c.code, c.title, c.subtitle, c.credits, c.status,
           t.id AS term_id, t.label AS term, t.year_num, t.semester, t.is_current
      FROM enrollments e
      JOIN courses c ON c.id = e.course_id
      LEFT JOIN terms t ON t.id = c.term_id
     WHERE e.user_id = ? AND e.status = 'enrolled'
     ORDER BY t.year_num, t.semester DESC, c.code
  `).all(userId);

  const rows = courses.map((c) => {
    const g = courseGrade(c.id, userId);
    return {
      ...c,
      percent: g.percent,
      letter: g.letter?.letter ?? null,
      points: g.letter?.points ?? null,
      graded_weight: g.graded_weight,
      total_weight: g.total_weight,
      complete: g.complete,
    };
  });

  // GPA counts only courses that are FULLY graded. gpa.py takes the same line
  // ("Semester GPA: --  (no course fully graded yet)") and a partial course
  // must not be allowed to masquerade as a settled grade.
  const terms = new Map();
  for (const r of rows) {
    const key = r.term_id ?? 'none';
    if (!terms.has(key)) terms.set(key, { term_id: r.term_id, term: r.term, year_num: r.year_num, semester: r.semester, is_current: r.is_current, courses: [] });
    terms.get(key).courses.push(r);
  }

  const gpaOf = (list) => {
    let qp = 0;
    let cr = 0;
    for (const r of list) {
      if (!r.complete || r.points === null || !r.credits) continue;
      qp += r.points * r.credits;
      cr += r.credits;
    }
    return cr ? { gpa: qp / cr, credits_completed: cr } : { gpa: null, credits_completed: 0 };
  };

  const termList = [...terms.values()].map((t) => ({
    ...t,
    ...gpaOf(t.courses),
    credits_enrolled: t.courses.reduce((a, r) => a + (r.credits || 0), 0),
  }));
  const cumulative = gpaOf(rows);

  return {
    terms: termList,
    cumulative: cumulative.gpa,
    credits_earned: cumulative.credits_completed,
    credits_enrolled: rows.reduce((a, r) => a + (r.credits || 0), 0),
    courses_in_progress: rows.filter((r) => !r.complete && r.percent !== null).length,
  };
}

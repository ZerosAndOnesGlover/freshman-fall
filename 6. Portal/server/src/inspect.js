// Dev tool: print a health report of the imported database.
// Usage: npm run inspect
import { db } from './db.js';

const line = (s) => console.log(s);
const rule = (t) => { line(''); line(`── ${t} ${'─'.repeat(Math.max(0, 60 - t.length))}`); };

function table(rows) {
  if (!rows.length) { line('   (none)'); return; }
  const cols = Object.keys(rows[0]);
  const w = cols.map((c) => Math.max(c.length, ...rows.map((r) => String(r[c] ?? '').length)));
  line('   ' + cols.map((c, i) => c.padEnd(w[i])).join('  '));
  line('   ' + w.map((n) => '-'.repeat(n)).join('  '));
  for (const r of rows) line('   ' + cols.map((c, i) => String(r[c] ?? '').padEnd(w[i])).join('  '));
}

rule('Courses by term');
table(db.prepare(`
  SELECT t.label AS term, COUNT(c.id) AS courses, SUM(c.credits) AS credits
  FROM terms t LEFT JOIN courses c ON c.term_id = t.id
  GROUP BY t.id ORDER BY t.year_num, CASE t.semester WHEN 'Fall' THEN 0 ELSE 1 END
`).all());

rule('Assessment coverage');
table(db.prepare(`
  SELECT COUNT(*) AS total,
         SUM(due_date IS NOT NULL) AS with_due_date,
         SUM(doc_path IS NOT NULL) AS with_brief,
         SUM(week_id IS NOT NULL) AS with_week,
         SUM(accepts_upload) AS submittable
  FROM assessments
`).all());

rule('Coverage by assessment kind');
table(db.prepare(`
  SELECT kind, COUNT(*) AS n,
         SUM(due_date IS NOT NULL) AS due,
         SUM(doc_path IS NOT NULL) AS brief,
         SUM(accepts_upload) AS upload
  FROM assessments GROUP BY kind ORDER BY n DESC
`).all());

rule('Courses missing due dates (top 12)');
table(db.prepare(`
  SELECT c.code, t.label AS term, COUNT(*) AS missing
  FROM assessments a JOIN courses c ON c.id = a.course_id JOIN terms t ON t.id = c.term_id
  WHERE a.due_date IS NULL
  GROUP BY c.id ORDER BY missing DESC LIMIT 12
`).all());

rule('Sample · CS 101 assessments');
table(db.prepare(`
  SELECT a.label, a.kind, a.possible, a.due_date, a.accepts_upload AS up,
         CASE WHEN a.doc_path IS NULL THEN '' ELSE 'yes' END AS brief
  FROM assessments a JOIN courses c ON c.id = a.course_id JOIN terms t ON t.id = c.term_id
  WHERE c.code = 'CS 101' AND t.year_num = 1 AND t.semester = 'Fall'
  ORDER BY a.due_date IS NULL, a.due_date LIMIT 20
`).all());

rule('Components · CS 101');
table(db.prepare(`
  SELECT cp.name, cp.weight, cp.drop_lowest, cp.formative
  FROM components cp JOIN courses c ON c.id = cp.course_id JOIN terms t ON t.id = c.term_id
  WHERE c.code = 'CS 101' AND t.year_num = 1 AND t.semester = 'Fall'
`).all());

rule('Weight sums per course (should be 100)');
table(db.prepare(`
  SELECT c.code, t.label AS term, SUM(cp.weight) AS total_weight
  FROM components cp JOIN courses c ON c.id = cp.course_id JOIN terms t ON t.id = c.term_id
  GROUP BY c.id HAVING total_weight <> 100 ORDER BY c.code
`).all());

rule('Teaching staff');
table(db.prepare(`
  SELECT u.full_name, u.email, cs.staff_role AS role, GROUP_CONCAT(c.code, ', ') AS courses
  FROM course_staff cs JOIN users u ON u.id = cs.user_id JOIN courses c ON c.id = cs.course_id
  GROUP BY u.id, cs.staff_role ORDER BY cs.staff_role, u.full_name
`).all());

rule('Material by kind');
table(db.prepare(`SELECT kind, COUNT(*) AS n FROM materials GROUP BY kind ORDER BY n DESC`).all());

rule('Totals');
for (const t of ['users', 'terms', 'courses', 'weeks', 'lectures', 'materials', 'components',
                 'assessments', 'enrollments', 'grades', 'calendar_events', 'pages', 'announcements']) {
  try {
    const { n } = db.prepare(`SELECT COUNT(*) AS n FROM ${t}`).get();
    line(`   ${t.padEnd(18)} ${n}`);
  } catch { line(`   ${t.padEnd(18)} (no such table)`); }
}
line('');

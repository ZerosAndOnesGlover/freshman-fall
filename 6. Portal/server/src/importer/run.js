/**
 * Rebuilds the portal database from the vault.
 *
 * The import is an upsert, not a wipe: rows are matched on their natural keys
 * (course code + term, assessment label + course) so that primary keys stay
 * stable and student submissions, uploads and portal-entered grades survive a
 * re-import. Rows that vanish from the vault are deleted afterwards, which
 * cascades to work attached to them — that is intended.
 *
 *   node src/importer/run.js            re-import over the existing database
 *   node src/importer/run.js --reset    drop the database first
 */

import fs from 'node:fs';
import path from 'node:path';
import { db, migrate, wasReset } from '../db.js';
import { DB_PATH, VAULT_ROOT } from '../paths.js';
import { hashPassword } from '../auth.js';
import {
  parseGradebook, parseAssessmentCalendar, parseMasterTimetable, parseOfficeHours,
  parseLecture, parseWeekSummary, parseAcademicCalendar, parseFrontmatter,
  classifyAssessment, stripMarkup, parseGradeScale, parseTimeRange,
} from './parsers.js';
import {
  YEAR_DIRS, rel, readIfExists, listDirs, listFiles,
  parseCourseFolder, parseWeekFolder, MATERIAL_KINDS, titleFromFilename,
} from './walk.js';

const REGISTRY = path.join(VAULT_ROOT, '5. Academic Registry');
const log = (...a) => console.log(...a);

// The drop itself happens in db.js, which must see --reset before it opens
// the connection; this only reports it.
if (wasReset) log('· dropped existing database');
migrate();

const stats = {
  terms: 0, courses: 0, weeks: 0, lectures: 0, materials: 0,
  components: 0, assessments: 0, staff: 0, events: 0, pages: 0, grades: 0,
};

// Track what this run touched so stale rows can be cleared at the end.
const seen = { courses: new Set(), weeks: new Set(), lectures: new Set(), materials: new Set(), assessments: new Set(), components: new Set() };

// ─── 1. Terms ──────────────────────────────────────────────────────────

const termId = new Map();  // "1|Fall" -> id

function upsertTerm(yearNum, label, semester) {
  const key = `${yearNum}|${semester}`;
  if (termId.has(key)) return termId.get(key);
  db.prepare(`
    INSERT INTO terms (year_num, year_label, semester, label)
    VALUES (?, ?, ?, ?)
    ON CONFLICT (year_num, semester) DO UPDATE SET year_label = excluded.year_label
  `).run(yearNum, label, semester, `Year ${yearNum} ${semester}`);
  const id = db.prepare('SELECT id FROM terms WHERE year_num = ? AND semester = ?').get(yearNum, semester).id;
  termId.set(key, id);
  stats.terms += 1;
  return id;
}

for (const y of YEAR_DIRS) {
  for (const semester of ['Fall', 'Spring']) {
    if (fs.existsSync(path.join(VAULT_ROOT, y.dir, semester))) {
      upsertTerm(y.yearNum, y.label, semester);
    }
  }
}

// ─── 2. Week maps and assessment due dates ─────────────────────────────

const timetableRows = [];

/** (courseCode|label) -> calendar row, per term id. */
const dueByTerm = new Map();
const weekMapByTerm = new Map();

const schedulingRoot = path.join(REGISTRY, '1. Scheduling');
for (const yearDir of listDirs(schedulingRoot)) {
  const yn = /Year\s*(\d+)/i.exec(yearDir);
  if (!yn) continue;
  const yearNum = Number(yn[1]);

  const calText = readIfExists(path.join(schedulingRoot, yearDir, 'ASSESSMENT CALENDAR.md'));
  if (calText) {
    for (const sem of parseAssessmentCalendar(calText)) {
      const tid = termId.get(`${yearNum}|${sem.semester}`);
      if (!tid) continue;

      const insertWeek = db.prepare(`
        INSERT INTO term_weeks (term_id, week_num, monday, friday) VALUES (?, ?, ?, ?)
        ON CONFLICT (term_id, week_num) DO UPDATE SET monday = excluded.monday, friday = excluded.friday
      `);
      const map = new Map();
      for (const w of sem.weekMap) {
        if (w.weekNum === null) continue;
        insertWeek.run(tid, w.weekNum, w.monday, w.friday);
        map.set(w.weekNum, w);
      }
      weekMapByTerm.set(tid, map);

      const due = dueByTerm.get(tid) || new Map();
      for (const row of sem.rows) due.set(`${row.courseCode}|${row.label}`, row);
      dueByTerm.set(tid, due);

      // Term bounds: Week 0 Monday through the last listed Friday.
      const mondays = sem.weekMap.map((w) => w.monday).filter(Boolean).sort();
      const fridays = sem.weekMap.map((w) => w.friday).filter(Boolean).sort();
      if (mondays.length && fridays.length) {
        db.prepare('UPDATE terms SET start_date = ?, end_date = ? WHERE id = ?')
          .run(mondays[0], fridays[fridays.length - 1], tid);
      }
    }
  }

  // Master timetable: credits, meeting pattern.
  const ttText = readIfExists(path.join(schedulingRoot, yearDir, 'MASTER TIMETABLE.md'));
  if (ttText) {
    for (const row of parseMasterTimetable(ttText)) {
      const tid = termId.get(`${yearNum}|${row.semester}`);
      if (tid) timetableRows.push({ ...row, termId: tid });
    }
  }
}

// ─── 3. Courses, from the gradebooks ───────────────────────────────────

const courseId = new Map();   // "CS 101|termId" -> id
const courseByCode = new Map();

function upsertCourse(c) {
  db.prepare(`
    INSERT INTO courses (code, title, subtitle, credits, term_id, status, schedule, description, vault_path, has_material)
    VALUES (@code, @title, @subtitle, @credits, @termId, @status, @schedule, @description, @vaultPath, @hasMaterial)
    ON CONFLICT (code, term_id) DO UPDATE SET
      title = excluded.title,
      subtitle = COALESCE(excluded.subtitle, courses.subtitle),
      credits = CASE WHEN excluded.credits > 0 THEN excluded.credits ELSE courses.credits END,
      status = excluded.status,
      schedule = COALESCE(excluded.schedule, courses.schedule),
      description = COALESCE(excluded.description, courses.description),
      vault_path = COALESCE(excluded.vault_path, courses.vault_path),
      has_material = MAX(excluded.has_material, courses.has_material)
  `).run({
    code: c.code, title: c.title, subtitle: c.subtitle ?? null,
    credits: c.credits ?? 0, termId: c.termId, status: c.status ?? 'in-progress',
    schedule: c.schedule ?? null, description: c.description ?? null,
    vaultPath: c.vaultPath ?? null, hasMaterial: c.hasMaterial ? 1 : 0,
  });
  const row = db.prepare('SELECT id FROM courses WHERE code = ? AND term_id IS ?').get(c.code, c.termId);
  courseId.set(`${c.code}|${c.termId}`, row.id);
  courseByCode.set(c.code, row.id);
  seen.courses.add(row.id);
  return row.id;
}

const gradebookRoot = path.join(REGISTRY, '2. Gradebook');
const gradebooks = [];
for (const yearDir of listDirs(gradebookRoot)) {
  const yn = /Year\s*(\d+)/i.exec(yearDir);
  if (!yn) continue;
  for (const semDir of listDirs(path.join(gradebookRoot, yearDir))) {
    for (const file of listFiles(path.join(gradebookRoot, yearDir, semDir))) {
      if (!file.endsWith('.md') || file.startsWith('_')) continue;  // _X Quiz Record are supplements
      const full = path.join(gradebookRoot, yearDir, semDir, file);
      const parsed = parseGradebook(readIfExists(full) || '');
      if (parsed) gradebooks.push({ ...parsed, yearNum: Number(yn[1]), path: rel(full) });
    }
  }
}
log(`· read ${gradebooks.length} gradebooks`);

for (const gb of gradebooks) {
  const tid = termId.get(`${gb.year || gb.yearNum}|${gb.semester}`);
  if (!tid) continue;
  // "Computer Science I · Foundations of Computation" -> title + subtitle
  const bits = gb.fullTitle.split('·').map((s) => s.trim()).filter(Boolean);
  const tt = timetableRows.find((r) => r.code === gb.code && r.termId === tid);
  upsertCourse({
    code: gb.code,
    title: bits[0] || gb.code,
    subtitle: bits.slice(1).join(' · ') || null,
    credits: gb.credits,
    termId: tid,
    status: gb.status,
    schedule: tt ? tt.schedule : null,
    termGb: gb,
  });
}

// Courses that appear on the timetable but have no gradebook yet.
for (const row of timetableRows) {
  if (courseId.has(`${row.code}|${row.termId}`)) continue;
  const bits = row.title.split('·').map((s) => s.trim()).filter(Boolean);
  upsertCourse({
    code: row.code,
    title: bits[0] || row.code,
    subtitle: bits.slice(1).join(' · ') || null,
    credits: row.credits,
    termId: row.termId,
    status: 'planned',
    schedule: row.schedule,
  });
}

// ─── 4. Course material, from the year folders ─────────────────────────

const upsertWeek = db.prepare(`
  INSERT INTO weeks (course_id, week_num, title, topic, takeaway, next_up, work, monday_date, friday_date, readme_path, summary_path)
  VALUES (@courseId, @weekNum, @title, @topic, @takeaway, @nextUp, @work, @monday, @friday, @readme, @summary)
  ON CONFLICT (course_id, week_num) DO UPDATE SET
    title = COALESCE(excluded.title, weeks.title),
    topic = COALESCE(excluded.topic, weeks.topic),
    takeaway = COALESCE(excluded.takeaway, weeks.takeaway),
    next_up = COALESCE(excluded.next_up, weeks.next_up),
    work = COALESCE(excluded.work, weeks.work),
    monday_date = COALESCE(excluded.monday_date, weeks.monday_date),
    friday_date = COALESCE(excluded.friday_date, weeks.friday_date),
    readme_path = COALESCE(excluded.readme_path, weeks.readme_path),
    summary_path = COALESCE(excluded.summary_path, weeks.summary_path)
`);

const upsertLecture = db.prepare(`
  INSERT INTO lectures (course_id, week_id, seq, code, title, subtitle, date_text, date_iso,
                        start_time, end_time, path)
  VALUES (@courseId, @weekId, @seq, @code, @title, @subtitle, @dateText, @dateIso,
          @startTime, @endTime, @path)
  ON CONFLICT (course_id, path) DO UPDATE SET
    week_id = excluded.week_id, seq = excluded.seq, code = excluded.code,
    title = excluded.title, subtitle = excluded.subtitle,
    date_text = excluded.date_text, date_iso = excluded.date_iso,
    start_time = excluded.start_time, end_time = excluded.end_time
`);

const upsertMaterial = db.prepare(`
  INSERT INTO materials (course_id, week_id, kind, title, filename, ext, path)
  VALUES (@courseId, @weekId, @kind, @title, @filename, @ext, @path)
  ON CONFLICT (course_id, path) DO UPDATE SET
    week_id = excluded.week_id, kind = excluded.kind, title = excluded.title
`);

/** Every material row for a course, so assessments can be linked to their brief. */
const materialsByCourse = new Map();

for (const y of YEAR_DIRS) {
  for (const semester of ['Fall', 'Spring']) {
    const semDir = path.join(VAULT_ROOT, y.dir, semester);
    if (!fs.existsSync(semDir)) continue;
    const tid = termId.get(`${y.yearNum}|${semester}`);
    if (!tid) continue;
    const weekMap = weekMapByTerm.get(tid) || new Map();

    for (const folder of listDirs(semDir)) {
      const info = parseCourseFolder(folder);
      if (!info) continue;
      const courseDir = path.join(semDir, folder);

      const cid = upsertCourse({
        code: info.code,
        title: info.title,
        subtitle: info.subtitle,
        credits: 0,                     // the gradebook is authoritative for credits
        termId: tid,
        status: 'in-progress',
        vaultPath: rel(courseDir),
        hasMaterial: true,
      });

      for (const weekFolder of listDirs(courseDir)) {
        const weekNum = parseWeekFolder(weekFolder);
        if (weekNum === null) continue;
        const weekDir = path.join(courseDir, weekFolder);

        const summaryText = readIfExists(path.join(weekDir, 'summary.md'));
        const summary = summaryText ? parseWeekSummary(summaryText) : {};
        const readmeText = readIfExists(path.join(weekDir, 'README.md'));
        const readmeTitle = readmeText ? (/^#\s+(.+)$/m.exec(readmeText) || [])[1] : null;
        const wm = weekMap.get(weekNum);

        upsertWeek.run({
          courseId: cid,
          weekNum,
          title: summary.heading || (readmeTitle ? stripMarkup(readmeTitle) : null),
          topic: summary.topic || null,
          takeaway: summary.takeaway || null,
          nextUp: summary.next || null,
          work: summary.work || null,
          monday: wm ? wm.monday : null,
          friday: wm ? wm.friday : null,
          readme: readmeText ? rel(path.join(weekDir, 'README.md')) : null,
          summary: summaryText ? rel(path.join(weekDir, 'summary.md')) : null,
        });
        const weekId = db.prepare('SELECT id FROM weeks WHERE course_id = ? AND week_num = ?')
          .get(cid, weekNum).id;
        seen.weeks.add(weekId);
        stats.weeks += 1;

        for (const sub of listDirs(weekDir)) {
          const kind = MATERIAL_KINDS[sub.toLowerCase()] || 'resource';
          for (const file of listFiles(path.join(weekDir, sub))) {
            const full = path.join(weekDir, sub, file);
            const relPath = rel(full);
            const ext = (path.extname(file) || '').replace('.', '').toLowerCase();

            if (kind === 'lecture' && ext === 'md') {
              const parsed = parseLecture(readIfExists(full) || '', file);
              const time = parseTimeRange(parsed.dateText);
              upsertLecture.run({
                courseId: cid, weekId, seq: parsed.seq ?? 0, code: parsed.code,
                title: parsed.title, subtitle: parsed.subtitle,
                dateText: parsed.dateText, dateIso: parsed.dateIso,
                startTime: time.start, endTime: time.end, path: relPath,
              });
              const lid = db.prepare('SELECT id FROM lectures WHERE course_id = ? AND path = ?')
                .get(cid, relPath).id;
              seen.lectures.add(lid);
              stats.lectures += 1;
              continue;
            }

            upsertMaterial.run({
              courseId: cid, weekId, kind,
              title: titleFromFilename(file), filename: file, ext, path: relPath,
            });
            const mid = db.prepare('SELECT id FROM materials WHERE course_id = ? AND path = ?')
              .get(cid, relPath).id;
            seen.materials.add(mid);
            stats.materials += 1;

            if (!materialsByCourse.has(cid)) materialsByCourse.set(cid, []);
            materialsByCourse.get(cid).push({ id: mid, kind, filename: file, path: relPath, weekId, weekNum, ext });
          }
        }

        // README.md and summary.md sit at the week root, not in a subfolder.
        for (const rootFile of ['README.md', 'summary.md']) {
          const full = path.join(weekDir, rootFile);
          if (!fs.existsSync(full)) continue;
          const relPath = rel(full);
          upsertMaterial.run({
            courseId: cid, weekId, kind: 'readme',
            title: rootFile === 'README.md' ? `Week ${weekNum} Overview` : `Week ${weekNum} Summary`,
            filename: rootFile, ext: 'md', path: relPath,
          });
          seen.materials.add(db.prepare('SELECT id FROM materials WHERE course_id = ? AND path = ?').get(cid, relPath).id);
        }
      }
    }
  }
}
stats.courses = seen.courses.size;
log(`· ${stats.courses} courses · ${stats.weeks} weeks · ${stats.lectures} lectures · ${stats.materials} materials`);

// ─── 5. People ─────────────────────────────────────────────────────────
//
// Dev credentials are fixed and printed at the end of the run. This database
// is local by design; change the passwords before it ever leaves the machine.

const DEV_STUDENT_PASSWORD = 'student2026';
const DEV_STAFF_PASSWORD = 'teach2026';

function upsertUser({ email, fullName, role, title = null, studentId = null, programme = null, yearLevel = null, password }) {
  const existing = db.prepare('SELECT id FROM users WHERE email = ?').get(email);
  if (existing) {
    db.prepare(`
      UPDATE users SET full_name = ?, role = ?, title = ?, student_id = ?, programme = ?, year_level = ?
       WHERE id = ?
    `).run(fullName, role, title, studentId, programme, yearLevel, existing.id);
    return existing.id;
  }
  const info = db.prepare(`
    INSERT INTO users (email, password_hash, role, full_name, title, student_id, programme, year_level)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `).run(email, hashPassword(password), role, fullName, title, studentId, programme, yearLevel);
  return Number(info.lastInsertRowid);
}

const studentUserId = upsertUser({
  email: 'adebayo.glover@ist.edu',
  fullName: 'Adebayo Glover',
  role: 'student',
  studentId: 'IST-2026-0114',
  programme: 'B.Sc. Computer Science & Engineering',
  yearLevel: 1,
  password: DEV_STUDENT_PASSWORD,
});

const registrarUserId = upsertUser({
  email: 'registrar@ist.edu',
  fullName: 'Office of the Registrar',
  role: 'admin',
  title: null,
  password: DEV_STAFF_PASSWORD,
});

/** Staff from the office-hours files, attached to the courses they teach. */
const staffEmail = (name) => `${name.toLowerCase().replace(/[^a-z\s]/g, '').trim().replace(/\s+/g, '.')}@ist.edu`;

for (const yearDir of listDirs(schedulingRoot)) {
  const ohText = readIfExists(path.join(schedulingRoot, yearDir, 'OFFICE HOURS.md'));
  if (!ohText) continue;
  for (const person of parseOfficeHours(ohText)) {
    const uid = upsertUser({
      email: staffEmail(person.name),
      fullName: person.name,
      role: 'instructor',
      title: person.title,
      password: DEV_STAFF_PASSWORD,
    });
    for (const code of person.courses) {
      for (const [key, cid] of courseId.entries()) {
        if (!key.startsWith(`${code}|`)) continue;
        db.prepare(`
          INSERT INTO course_staff (course_id, user_id, staff_role, office_hours)
          VALUES (?, ?, ?, ?)
          ON CONFLICT (course_id, user_id) DO UPDATE SET
            staff_role = excluded.staff_role, office_hours = excluded.office_hours
        `).run(cid, uid, person.role, person.officeHours);
        stats.staff += 1;
      }
    }
  }
}

// The student is enrolled in every course that has a gradebook — those are the
// courses actually being taken, as opposed to catalogue entries.
for (const gb of gradebooks) {
  const tid = termId.get(`${gb.year || gb.yearNum}|${gb.semester}`);
  const cid = tid ? courseId.get(`${gb.code}|${tid}`) : null;
  if (!cid) continue;
  db.prepare(`
    INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)
    ON CONFLICT (user_id, course_id) DO NOTHING
  `).run(studentUserId, cid);
}

// ─── 6. Components and assessments, from the gradebooks ────────────────

const upsertComponent = db.prepare(`
  INSERT INTO components (course_id, name, weight, drop_lowest, formative, position)
  VALUES (@courseId, @name, @weight, @dropLowest, @formative, @position)
  ON CONFLICT (course_id, name) DO UPDATE SET
    weight = excluded.weight, drop_lowest = excluded.drop_lowest,
    formative = excluded.formative, position = excluded.position
`);

const upsertAssessment = db.prepare(`
  INSERT INTO assessments (course_id, component_id, week_id, label, topic, kind, possible,
                           due_date, due_time, notes, room, doc_path, accepts_upload, position)
  VALUES (@courseId, @componentId, @weekId, @label, @topic, @kind, @possible,
          @dueDate, @dueTime, @notes, @room, @docPath, @acceptsUpload, @position)
  ON CONFLICT (course_id, label) DO UPDATE SET
    component_id = excluded.component_id,
    week_id = COALESCE(excluded.week_id, assessments.week_id),
    topic = COALESCE(excluded.topic, assessments.topic),
    kind = excluded.kind,
    possible = excluded.possible,
    due_date = COALESCE(excluded.due_date, assessments.due_date),
    due_time = COALESCE(excluded.due_time, assessments.due_time),
    notes = COALESCE(excluded.notes, assessments.notes),
    room = COALESCE(excluded.room, assessments.room),
    doc_path = COALESCE(excluded.doc_path, assessments.doc_path),
    accepts_upload = excluded.accepts_upload,
    position = excluded.position
`);

const upsertRegistryGrade = db.prepare(`
  INSERT INTO grades (assessment_id, user_id, score, excused, source, graded_at)
  VALUES (?, ?, ?, ?, 'registry', datetime('now'))
  ON CONFLICT (assessment_id, user_id) DO UPDATE SET
    score   = CASE WHEN grades.source = 'registry' THEN excluded.score   ELSE grades.score   END,
    excused = CASE WHEN grades.source = 'registry' THEN excluded.excused ELSE grades.excused END
`);

/**
 * Finds the brief for an assessment among a course's material files.
 * "PS 1" must not match "PS 10 ...", so the number is anchored against a
 * following digit.
 */
const BRIEF_ALIASES = {
  PS: ['PS', 'Problem Set'],
  Lab: ['LAB', 'Lab'],
  Quiz: ['QUIZ', 'Quiz'],
  Midterm: ['MIDTERM', 'Midterm'],
  Project: ['PROJECT', 'Project'],
  Paper: ['PAPER', 'Paper', 'Position Paper'],
  Prep: ['PREP', 'Prep', 'Seminar Prep'],
};

function findBrief(materials, label, kind) {
  if (!materials) return null;
  const numbered = /^([A-Za-z]+)\s*(\d+)$/.exec(label);
  const patterns = [];
  if (numbered) {
    const [, word, num] = numbered;
    for (const alias of BRIEF_ALIASES[word] || [word]) {
      patterns.push(new RegExp(`^${alias}\\s*0*${num}(?!\\d)`, 'i'));
    }
  } else {
    patterns.push(new RegExp(`^${label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?!\\w)`, 'i'));
  }

  const wanted = kind === 'lab' ? ['lab', 'assignment']
    : kind === 'quiz' ? ['quiz', 'assignment']
    : ['assignment', 'lab', 'quiz', 'resource'];
  const candidates = materials.filter((f) => f.ext === 'md' && wanted.includes(f.kind));
  for (const pattern of patterns) {
    const hit = candidates.find((f) => pattern.test(f.filename));
    if (hit) return hit;
  }
  return null;
}

/** Sat in a hall or judged by the instructor — nothing for a student to upload. */
const NON_UPLOAD = new Set(['midterm', 'final', 'quiz', 'participation']);

for (const gb of gradebooks) {
  const tid = termId.get(`${gb.year || gb.yearNum}|${gb.semester}`);
  if (!tid) continue;
  const cid = courseId.get(`${gb.code}|${tid}`);
  if (!cid) continue;

  const due = dueByTerm.get(tid) || new Map();
  const materials = materialsByCourse.get(cid);
  const weekIdByNum = new Map(
    db.prepare('SELECT id, week_num FROM weeks WHERE course_id = ?').all(cid)
      .map((w) => [w.week_num, w.id]),
  );

  let position = 0;
  for (const comp of gb.components) {
    upsertComponent.run({
      courseId: cid, name: comp.name, weight: comp.weight,
      dropLowest: comp.dropLowest, formative: comp.formative ? 1 : 0, position: comp.position,
    });
    const compId = db.prepare('SELECT id FROM components WHERE course_id = ? AND name = ?')
      .get(cid, comp.name).id;
    seen.components.add(compId);
    stats.components += 1;

    for (const item of comp.items) {
      position += 1;
      // The calendar carries a row per course, plus "ALL" rows that apply to
      // every course in the term.
      const row = due.get(`${gb.code}|${item.label}`) || due.get(`ALL|${item.label}`) || null;
      const brief = findBrief(materials, item.label, item.kind);
      const weekNum = row?.weekNum ?? brief?.weekNum ?? null;

      upsertAssessment.run({
        courseId: cid,
        componentId: compId,
        weekId: weekNum === null ? null : (weekIdByNum.get(weekNum) ?? null),
        label: item.label,
        topic: item.topic,
        kind: item.kind,
        possible: item.possible,
        dueDate: row?.date ?? null,
        dueTime: row?.time ?? null,
        notes: row?.notes ?? null,
        room: row?.room ?? null,
        docPath: brief?.path ?? null,
        acceptsUpload: NON_UPLOAD.has(item.kind) ? 0 : 1,
        position,
      });
      const aid = db.prepare('SELECT id FROM assessments WHERE course_id = ? AND label = ?')
        .get(cid, item.label).id;
      seen.assessments.add(aid);
      stats.assessments += 1;

      if (item.earned !== null || item.excused) {
        upsertRegistryGrade.run(aid, studentUserId, item.earned, item.excused ? 1 : 0);
        stats.grades += 1;
      }
    }
  }
}
log(`· ${stats.components} components · ${stats.assessments} assessments · ${stats.grades} registry marks`);

// ─── 7. Institution documents ──────────────────────────────────────────

const INSTITUTION_PAGES = [
  { file: 'ACADEMIC CALENDAR.md', slug: 'academic-calendar', title: 'Academic Calendar', group: 'Academics',
    summary: 'Term dates, assessment weeks and finals for the full four-year programme.' },
  { file: 'DEGREE REQUIREMENTS.md', slug: 'degree-requirements', title: 'Degree Requirements', group: 'Academics',
    summary: 'The credit-by-credit audit checklist for the B.Sc. in Computer Science & Engineering.' },
  { file: 'GRADING STANDARDS.md', slug: 'grading-standards', title: 'Grading Standards', group: 'Academics',
    summary: 'Letter grades, grade points, and how a course grade is computed from its components.' },
  { file: 'UNIVERSITY POLICIES.md', slug: 'university-policies', title: 'University Policies', group: 'About',
    summary: 'Academic integrity, attendance, accommodations, and the policies governing coursework.' },
];

const upsertPage = db.prepare(`
  INSERT INTO pages (slug, title, summary, body_md, path, nav_group)
  VALUES (?, ?, ?, ?, ?, ?)
  ON CONFLICT (slug) DO UPDATE SET
    title = excluded.title, summary = excluded.summary,
    body_md = excluded.body_md, path = excluded.path, nav_group = excluded.nav_group
`);

const institutionDir = path.join(REGISTRY, '0. Institution');
for (const page of INSTITUTION_PAGES) {
  const full = path.join(institutionDir, page.file);
  const text = readIfExists(full);
  if (!text) continue;
  upsertPage.run(page.slug, page.title, page.summary, parseFrontmatter(text).body, rel(full), page.group);
  stats.pages += 1;
}

// The letter scale is read from the policy file, not hardcoded here.
const policyText = readIfExists(path.join(institutionDir, 'UNIVERSITY POLICIES.md'));
if (policyText) {
  const scale = parseGradeScale(policyText);
  if (scale.length) {
    db.prepare('DELETE FROM grade_scale').run();
    const insScale = db.prepare(
      'INSERT INTO grade_scale (letter, points, low, high, descriptor) VALUES (?, ?, ?, ?, ?)');
    for (const b of scale) insScale.run(b.letter, b.points, b.low, b.high, b.descriptor);
    log(`\u00b7 grade scale: ${scale.length} bands from UNIVERSITY POLICIES.md`);
  }
}

// ─── 8. Calendar events ────────────────────────────────────────────────

db.prepare('DELETE FROM calendar_events').run();
const insertEvent = db.prepare(`
  INSERT INTO calendar_events (term_id, date_iso, title, kind, course_code, detail)
  VALUES (?, ?, ?, ?, ?, ?)
`);

const acText = readIfExists(path.join(institutionDir, 'ACADEMIC CALENDAR.md'));
if (acText) {
  for (const ev of parseAcademicCalendar(acText)) {
    const tid = termId.get(`${ev.yearNum}|${ev.semester}`) ?? null;
    insertEvent.run(tid, ev.date, ev.title, ev.kind, null, null);
    stats.events += 1;
  }
}

// Every dated assessment is also a calendar event, so one feed covers both.
for (const row of db.prepare(`
  SELECT a.due_date, a.due_time, a.label, a.topic, a.room, c.code, c.term_id
    FROM assessments a JOIN courses c ON c.id = a.course_id
   WHERE a.due_date IS NOT NULL
`).all()) {
  insertEvent.run(
    row.term_id, row.due_date, `${row.code} · ${row.label}`, 'assessment', row.code,
    [row.topic, row.due_time, row.room].filter(Boolean).join(' · ') || null,
  );
  stats.events += 1;
}

// ─── 9. Announcements ──────────────────────────────────────────────────
//
// Seeded once from the calendar so the portal has something real to show;
// anything an instructor posts later is left alone.

if (db.prepare('SELECT COUNT(*) AS n FROM announcements').get().n === 0) {
  const insertAnnouncement = db.prepare(`
    INSERT INTO announcements (course_id, author_id, title, body, category, pinned)
    VALUES (?, ?, ?, ?, ?, ?)
  `);
  insertAnnouncement.run(null, registrarUserId,
    'Portal submissions are now open',
    'Coursework for every enrolled course can be submitted through the portal. Uploads are accepted up to the deadline shown on each assessment; after that a submission is still accepted but is recorded as late.',
    'notice', 1);
  insertAnnouncement.run(null, registrarUserId,
    'Check your degree audit before add/drop closes',
    'Your progress against the B.Sc. Computer Science & Engineering requirements is available under Academics. Raise any discrepancy with the Office of the Registrar before the add/drop deadline.',
    'academic', 0);

  const nextExam = db.prepare(`
    SELECT c.id AS course_id, c.code, a.label, a.due_date, a.room
      FROM assessments a JOIN courses c ON c.id = a.course_id
     WHERE a.kind IN ('midterm','final') AND a.due_date IS NOT NULL
     ORDER BY a.due_date LIMIT 1
  `).get();
  if (nextExam) {
    insertAnnouncement.run(nextExam.course_id, registrarUserId,
      `${nextExam.code} ${nextExam.label} — room and seating`,
      `${nextExam.label} is scheduled for ${nextExam.due_date}${nextExam.room ? ` in ${nextExam.room}` : ''}. Bring your student ID. Permitted materials are listed on the course policy page.`,
      'exam', 0);
  }
}

// ─── 10. Clear rows the vault no longer has ────────────────────────────

function prune(table, keep) {
  const ids = [...keep];
  const rows = db.prepare(`SELECT id FROM ${table}`).all().map((r) => r.id);
  const stale = rows.filter((id) => !keep.has(id));
  if (stale.length === 0) return 0;
  const del = db.prepare(`DELETE FROM ${table} WHERE id = ?`);
  for (const id of stale) del.run(id);
  void ids;
  return stale.length;
}

const pruned = {
  lectures: prune('lectures', seen.lectures),
  materials: prune('materials', seen.materials),
  assessments: prune('assessments', seen.assessments),
  weeks: prune('weeks', seen.weeks),
  components: prune('components', seen.components),
  courses: prune('courses', seen.courses),
};
const prunedTotal = Object.values(pruned).reduce((a, b) => a + b, 0);
if (prunedTotal > 0) log(`· pruned ${prunedTotal} rows no longer in the vault`);

// Mark the term the vault is currently in as the active one.
db.prepare('UPDATE terms SET is_current = 0').run();
const current = db.prepare(`
  SELECT id FROM terms WHERE start_date IS NOT NULL
   ORDER BY ABS(julianday(start_date) - julianday('now')) LIMIT 1
`).get();
if (current) db.prepare('UPDATE terms SET is_current = 1 WHERE id = ?').run(current.id);

db.prepare('ANALYZE').run();

log('');
log('  Import complete.');
log(`  Database  ${DB_PATH}`);
log(`  Vault     ${VAULT_ROOT}`);
log('');
log(`  ${stats.courses} courses · ${stats.weeks} weeks · ${stats.lectures} lectures`);
log(`  ${stats.assessments} assessments · ${stats.materials} materials · ${stats.events} calendar events`);
log('');
log('  Sign in with:');
log(`    student     adebayo.glover@ist.edu / ${DEV_STUDENT_PASSWORD}`);
log(`    instructor  <first>.<last>@ist.edu / ${DEV_STAFF_PASSWORD}   (e.g. david.malan@ist.edu)`);
log(`    registrar   registrar@ist.edu / ${DEV_STAFF_PASSWORD}`);
log('');

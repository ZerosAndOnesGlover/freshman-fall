/**
 * Parsers for the vault's markdown conventions.
 *
 * Every format here is one the vault already uses; nothing is invented. The
 * registry files (gradebooks, the assessment calendar, the master timetable)
 * are the authority for structure and points, and the course folders are the
 * authority for teaching material.
 */

const MONTHS = {
  jan: 1, feb: 2, mar: 3, apr: 4, may: 5, jun: 6,
  jul: 7, aug: 8, sep: 9, oct: 10, nov: 11, dec: 12,
};

/** Heading separators used across the vault: en/em dash, hyphen, colon, or `·`. */
const SEP = /\s*[—–\-:·]\s*/;

export function stripMarkup(s) {
  return String(s ?? '')
    .replace(/\*\*/g, '')
    .replace(/(^|\s)\*(\S[^*]*?)\*/g, '$1$2')
    .replace(/`/g, '')
    .replace(/\[\[([^\]|]+)(\|[^\]]+)?\]\]/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .trim();
}

/** Drop leading emoji/pictographs the calendar uses as assessment icons. */
export function stripEmoji(s) {
  return String(s ?? '')
    .replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}\u{2190}-\u{21FF}]/gu, '')
    .trim();
}

export function toIsoDate(year, monthName, day) {
  const m = MONTHS[String(monthName).slice(0, 3).toLowerCase()];
  if (!m || !year || !day) return null;
  return `${year}-${String(m).padStart(2, '0')}-${String(Number(day)).padStart(2, '0')}`;
}

// ─── Frontmatter ───────────────────────────────────────────────────────

export function parseFrontmatter(text) {
  const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(text);
  if (!match) return { data: {}, body: text };
  const data = {};
  for (const line of match[1].split(/\r?\n/)) {
    const kv = /^([A-Za-z_][\w-]*):\s*(.*)$/.exec(line);
    if (!kv) continue;
    let value = kv[2].trim();
    if ((value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    data[kv[1]] = value;
  }
  return { data, body: text.slice(match[0].length) };
}

// ─── Markdown tables ───────────────────────────────────────────────────

function splitRow(line) {
  return line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map((c) => c.trim());
}

const isSeparatorRow = (line) => /^\|?[\s:|-]+\|[\s:|-]*$/.test(line.trim());

/**
 * Reads the markdown table that starts at or after `from`.
 * Returns { headers, rows, end } with rows as arrays of cell strings.
 */
export function readTable(lines, from) {
  let i = from;
  while (i < lines.length && !lines[i].trim().startsWith('|')) {
    if (lines[i].trim().startsWith('#')) return null;  // ran into the next section
    i += 1;
  }
  if (i >= lines.length) return null;

  const headers = splitRow(lines[i]).map(stripMarkup);
  i += 1;
  if (i < lines.length && isSeparatorRow(lines[i])) i += 1;

  const rows = [];
  while (i < lines.length && lines[i].trim().startsWith('|')) {
    if (!isSeparatorRow(lines[i])) rows.push(splitRow(lines[i]));
    i += 1;
  }
  return { headers, rows, end: i };
}

// ─── Gradebook ─────────────────────────────────────────────────────────

const RESERVED_SECTIONS = new Set(['component weights', 'computed', 'notes', 'how to use this file']);

/** "PS 1" -> ps, "Midterm 2" -> midterm, and so on. */
export function classifyAssessment(label, componentName = '') {
  const l = label.toLowerCase();
  const c = componentName.toLowerCase();
  if (/^ps\b|problem set/.test(l)) return 'ps';
  if (/^lab\b/.test(l)) return 'lab';
  if (/^quiz\b/.test(l)) return 'quiz';
  if (/^midterm\b/.test(l)) return 'midterm';
  if (/final (exam|examination)/.test(l)) return 'final';
  if (/^project\b|milestone/.test(l)) return 'project';
  if (/paper|essay|reflection/.test(l)) return 'paper';
  if (/^prep\b|preparation/.test(l)) return 'prep';
  if (/presentation|talk/.test(l)) return 'presentation';
  if (/contribution|participation|attendance/.test(l)) return 'participation';
  if (/peer/.test(l)) return 'peer';
  if (/exam/.test(c)) return 'midterm';
  return 'other';
}

/**
 * Parses one gradebook file into a course with weighted components and items.
 * Mirrors the contract in `5. Academic Registry/tools/GRADEBOOK SCHEMA.md`.
 */
export function parseGradebook(text) {
  const { data, body } = parseFrontmatter(text);
  if (!data.course) return null;

  const lines = body.split(/\r?\n/);
  const components = [];
  let position = 0;

  for (let i = 0; i < lines.length; i += 1) {
    const heading = /^##\s+(.+?)\s*$/.exec(lines[i]);
    if (!heading) continue;

    const raw = stripMarkup(heading[1]);
    if (RESERVED_SECTIONS.has(raw.toLowerCase())) continue;

    // A component heading carries its weight as a qualifier: "Labs — 20%".
    // The `%` is what separates it from a plain titled heading.
    const parts = raw.split(SEP);
    if (parts.length < 2) continue;
    const name = parts[0].trim();
    const qualifier = parts.slice(1).join(' — ');
    const pct = /(\d+(?:\.\d+)?)\s*%/.exec(qualifier);
    if (!pct) continue;

    const weight = Number(pct[1]);
    const table = readTable(lines, i + 1);
    if (!table) continue;

    const idx = {
      item: table.headers.findIndex((h) => /^item$/i.test(h)),
      topic: table.headers.findIndex((h) => /^topic$/i.test(h)),
      possible: table.headers.findIndex((h) => /^possible$/i.test(h)),
      earned: table.headers.findIndex((h) => /^earned$/i.test(h)),
    };
    if (idx.item < 0 || idx.possible < 0) continue;

    const items = [];
    for (const row of table.rows) {
      const label = stripMarkup(row[idx.item] ?? '');
      if (!label || /^item$/i.test(label)) continue;
      const possible = Number(stripMarkup(row[idx.possible] ?? ''));
      if (!Number.isFinite(possible)) continue;

      const earnedRaw = stripMarkup(row[idx.earned] ?? '');
      const excused = /^ex$/i.test(earnedRaw);
      const earned = excused || earnedRaw === '' ? null : Number(earnedRaw);

      items.push({
        label,
        topic: stripMarkup(row[idx.topic] ?? '') || null,
        possible,
        earned: Number.isFinite(earned) ? earned : null,
        excused,
        kind: classifyAssessment(label, name),
      });
    }

    position += 1;
    components.push({
      name,
      weight,
      formative: weight === 0 || /formative/i.test(qualifier),
      dropLowest: /lowest\s+\d+\s+dropped/i.test(qualifier) ? 1 : 0,
      position,
      items,
    });
    i = table.end - 1;
  }

  return {
    code: data.course.trim(),
    fullTitle: (data.title || '').trim(),
    credits: Number(data.credits) || 0,
    year: Number(data.year) || null,
    semester: (data.semester || '').trim(),
    status: (data.status || 'in-progress').trim(),
    components,
  };
}

// ─── Assessment calendar ───────────────────────────────────────────────

/**
 * Normalises a calendar assessment name onto the gradebook's Item label, which
 * is the registry join key: "📝 Problem Set 1" -> "PS 1", "📋 Project 1 Due"
 * -> "Project 1".
 */
export function normaliseAssessmentLabel(raw) {
  let s = stripEmoji(stripMarkup(raw));
  s = s.replace(/\s+Due$/i, '').replace(/\s+Deadline$/i, '').trim();
  s = s.replace(/^Problem Set\s+/i, 'PS ');
  s = s.replace(/^Lab Report\s+/i, 'Lab ');
  s = s.replace(/^Position Paper\s+/i, 'Paper ');
  s = s.replace(/^Final Paper$/i, 'Paper 3');
  s = s.replace(/^Midterm Exam\s+/i, 'Midterm ');
  s = s.replace(/^Final Examination$/i, 'Final Exam');
  return s.replace(/\s{2,}/g, ' ').trim();
}

/** "18:00–19:15 · VNC 100 · Weeks 0–5" -> { time: "18:00", room: "VNC 100" } */
function readNotes(notes) {
  const clean = stripMarkup(notes || '');
  const time = /(\d{1,2}:\d{2})/.exec(clean);
  const room = /\b([A-Z]{2,4}\s?\d{2,4}[A-Z]?)\b/.exec(clean);
  return { time: time ? time[1] : null, room: room ? room[1].trim() : null, text: clean || null };
}

/**
 * Reads the year's ASSESSMENT CALENDAR into per-semester week maps and rows.
 * Returns [{ semester, year, weekMap: [...], rows: [...] }].
 */
export function parseAssessmentCalendar(text) {
  const lines = text.split(/\r?\n/);
  const semesters = [];
  let current = null;

  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];

    const semHeading = /^##\s+(FALL|SPRING)\s+SEMESTER\s+ASSESSMENTS/i.exec(stripMarkup(line));
    if (semHeading) {
      current = {
        semester: semHeading[1][0].toUpperCase() + semHeading[1].slice(1).toLowerCase(),
        year: null,
        weekMap: [],
        rows: [],
      };
      semesters.push(current);
      continue;
    }
    if (!current) continue;

    if (/^###\s+Week-to-Date Map/i.test(line)) {
      const year = /(20\d{2})/.exec(line);
      if (year) current.year = Number(year[1]);
      const table = readTable(lines, i + 1);
      if (table) {
        for (const row of table.rows) {
          const weekCell = stripMarkup(row[0] ?? '');
          const w = /^W(\d+)$/i.exec(weekCell);
          const mon = /([A-Za-z]{3,})\s+(\d{1,2})/.exec(stripMarkup(row[1] ?? ''));
          const fri = /([A-Za-z]{3,})\s+(\d{1,2})/.exec(stripMarkup(row[2] ?? ''));
          if (!mon || !fri) continue;
          // Spring terms run Jan–May of the following calendar year; the map
          // heading already carries that year, so no roll-over is needed.
          const monday = toIsoDate(current.year, mon[1], mon[2]);
          const friday = toIsoDate(current.year, fri[1], fri[2]);
          if (!monday || !friday) continue;
          current.weekMap.push({
            weekNum: w ? Number(w[1]) : null,
            isFinals: /finals/i.test(weekCell),
            monday,
            friday,
          });
        }
        i = table.end - 1;
      }
      continue;
    }

    if (/^###\s+Graded Work/i.test(line)) {
      const table = readTable(lines, i + 1);
      if (table) {
        const col = (name) => table.headers.findIndex((h) => new RegExp(`^${name}$`, 'i').test(h));
        const ci = {
          week: col('Week'), date: col('Date'), course: col('Course'),
          assessment: col('Assessment'), weight: col('Weight'), notes: col('Notes'),
        };
        for (const row of table.rows) {
          const courseCell = stripMarkup(row[ci.course] ?? '');
          const label = normaliseAssessmentLabel(row[ci.assessment] ?? '');
          if (!courseCell || !label) continue;

          const dateCell = stripMarkup(row[ci.date] ?? '');
          const d = /([A-Za-z]{3,})\s+(\d{1,2})/.exec(dateCell);
          const weekCell = stripMarkup(row[ci.week] ?? '');
          const w = /^W(\d+)$/i.exec(weekCell);
          const notes = readNotes(row[ci.notes]);

          current.rows.push({
            courseCode: courseCell,          // may be the literal "ALL"
            label,
            weekNum: w ? Number(w[1]) : null,
            date: d ? toIsoDate(current.year, d[1], d[2]) : null,
            time: notes.time || '17:00',     // the calendar's stated default
            room: notes.room,
            weightNote: stripMarkup(row[ci.weight] ?? '') || null,
            notes: notes.text,
          });
        }
        i = table.end - 1;
      }
    }
  }
  return semesters;
}

// ─── Master timetable ──────────────────────────────────────────────────

/** Course code, credits, meeting pattern per semester. */
export function parseMasterTimetable(text) {
  const lines = text.split(/\r?\n/);
  const out = [];
  let semester = null;

  for (let i = 0; i < lines.length; i += 1) {
    const sem = /^###\s+(Fall|Spring)\s+Semester/i.exec(stripMarkup(lines[i]));
    if (sem) {
      semester = sem[1][0].toUpperCase() + sem[1].slice(1).toLowerCase();
      const table = readTable(lines, i + 1);
      if (!table) continue;
      const col = (re) => table.headers.findIndex((h) => re.test(h));
      const ci = {
        code: col(/^code$/i), title: col(/title/i), credits: col(/credits/i),
        schedule: col(/schedule/i), assessment: col(/assessment/i),
      };
      for (const row of table.rows) {
        const code = stripMarkup(row[ci.code] ?? '');
        if (!code || /^total/i.test(code)) continue;
        out.push({
          semester,
          code,
          title: stripMarkup(row[ci.title] ?? ''),
          credits: Number(stripMarkup(row[ci.credits] ?? '')) || 0,
          schedule: stripMarkup(row[ci.schedule] ?? '') || null,
          assessmentSummary: stripMarkup(row[ci.assessment] ?? '') || null,
        });
      }
      i = table.end - 1;
    }
  }
  return out;
}

// ─── Office hours ──────────────────────────────────────────────────────

/**
 * "### Prof. David Malan (CS 101)" and "### Kwame Asante (CS 101 TA)".
 * Returns staff with the courses they are attached to.
 */
export function parseOfficeHours(text) {
  const lines = text.split(/\r?\n/);
  const staff = [];
  let section = null;

  for (let i = 0; i < lines.length; i += 1) {
    const h2 = /^##\s+(.+)$/.exec(lines[i]);
    if (h2) section = stripMarkup(h2[1]).toLowerCase();

    const h3 = /^###\s+(.+)$/.exec(lines[i]);
    if (!h3) continue;
    const heading = stripMarkup(h3[1]);
    const m = /^((?:Prof\.|Dr\.|Mr\.|Ms\.|Mrs\.)?\s*[^(]+?)\s*\(([^)]*)\)\s*$/.exec(heading);
    if (!m) continue;

    const nameWithTitle = m[1].trim();
    const paren = m[2].trim();
    const codes = [...paren.matchAll(/\b([A-Z]{2,4})\s?(\d{3})\b/g)].map((c) => `${c[1]} ${c[2]}`);
    if (codes.length === 0) continue;

    const isTa = /\bTA\b/i.test(paren) || /teaching assistant/i.test(section || '');
    const titleMatch = /^(Prof\.|Dr\.|Mr\.|Ms\.|Mrs\.)\s*/.exec(nameWithTitle);

    // Collect the hours lines until the next heading.
    const hours = [];
    for (let j = i + 1; j < lines.length && !/^#{1,3}\s/.test(lines[j]); j += 1) {
      const t = lines[j].trim();
      if (t) hours.push(stripMarkup(t));
    }

    staff.push({
      name: titleMatch ? nameWithTitle.slice(titleMatch[0].length).trim() : nameWithTitle,
      title: titleMatch ? titleMatch[1] : null,
      role: isTa ? 'ta' : 'instructor',
      courses: codes,
      officeHours: hours.slice(0, 6).join('\n') || null,
    });
  }
  return staff;
}

// ─── Lecture files ─────────────────────────────────────────────────────

/**
 * Lecture headers look like:
 *   # CS 101 · Lecture 4 (Week 1, Lecture 1)
 *   ## Data, Types, and Variables (The Full Picture)
 *   **Date:** Wednesday 26 August 2026 · 09:00–09:50 · Week 1
 */
export function parseLecture(text, filename) {
  const { body } = parseFrontmatter(text);
  const lines = body.split(/\r?\n/);

  let h1 = null;
  let h2 = null;
  for (const line of lines.slice(0, 40)) {
    if (h1 === null && /^#\s+/.test(line)) h1 = stripMarkup(line.replace(/^#\s+/, ''));
    else if (h1 !== null && h2 === null && /^##\s+/.test(line)) {
      h2 = stripMarkup(line.replace(/^##\s+/, ''));
      break;
    }
  }

  const head = body.slice(0, 2000);
  const dateLine = /\*\*Date:\*\*\s*(.+)/.exec(head);
  const dateText = dateLine ? stripMarkup(dateLine[1]) : null;

  let dateIso = null;
  if (dateText) {
    const d = /(\d{1,2})\s+([A-Za-z]{3,})\s+(\d{4})/.exec(dateText);
    if (d) dateIso = toIsoDate(Number(d[3]), d[2], d[1]);
  }

  const weekFromText = /Week\s+(\d+)/i.exec(dateText || h1 || '');
  const seqFromTitle = /Lecture\s+(\d+)/i.exec(h1 || '');
  const codeFromFile = /^([A-Z]+\s?\d+)\b/.exec(filename.replace(/\.md$/i, ''));

  // The H1 is "CS 101 · Lecture 4 (Week 1, Lecture 1)"; the H2 carries the
  // real subject, so that is what the portal shows as the lecture title.
  const title = h2 || (h1 ? h1.split('·').slice(-1)[0].trim() : filename.replace(/\.md$/i, ''));

  return {
    title,
    subtitle: h1 || null,
    code: codeFromFile ? codeFromFile[1].replace(/\s+/g, '') : null,
    seq: seqFromTitle ? Number(seqFromTitle[1]) : null,
    weekNum: weekFromText ? Number(weekFromText[1]) : null,
    dateText,
    dateIso,
  };
}

// ─── Week summary ──────────────────────────────────────────────────────

/** The five-line summary.md every week folder carries. */
export function parseWeekSummary(text) {
  const { body } = parseFrontmatter(text);
  const field = (name) => {
    const re = new RegExp(`^\\*\\*${name}\\s*[—–\\-:]?\\*\\*\\s*(.+)$`, 'im');
    const m = re.exec(body);
    return m ? stripMarkup(m[1]) : null;
  };
  const h1 = /^#\s+(.+)$/m.exec(body);
  return {
    heading: h1 ? stripMarkup(h1[1]) : null,
    topic: field('Topic'),
    lectures: field('Lectures'),
    work: field('Work'),
    takeaway: field('Takeaway'),
    next: field('Next'),
  };
}

// ─── Academic calendar ─────────────────────────────────────────────────

/**
 * The institution-wide calendar: "### Fall Semester, Year 1" followed by a
 * | Date | Event | table whose dates carry no year, so the year comes from
 * the prose note above the table.
 */
export function parseAcademicCalendar(text) {
  const lines = text.split(/\r?\n/);
  const events = [];
  let yearNum = null;
  let semester = null;
  let calYear = null;

  for (let i = 0; i < lines.length; i += 1) {
    const clean = stripMarkup(lines[i]);

    const yearHeading = /^YEAR\s+(\d+):/i.exec(clean);
    if (yearHeading) yearNum = Number(yearHeading[1]);

    const semHeading = /^###\s+(Fall|Spring)\s+Semester,\s*Year\s*(\d+)/i.exec(clean);
    if (semHeading) {
      semester = semHeading[1][0].toUpperCase() + semHeading[1].slice(1).toLowerCase();
      yearNum = Number(semHeading[2]);
      calYear = null;
      continue;
    }
    if (!semester) continue;

    const dated = /Dated for (20\d{2})/i.exec(clean);
    if (dated) calYear = Number(dated[1]);

    if (lines[i].trim().startsWith('|') && /\|\s*Date\s*\|/i.test(lines[i])) {
      const table = readTable(lines, i);
      if (table) {
        for (const row of table.rows) {
          const dateCell = stripMarkup(row[0] ?? '');
          const d = /([A-Za-z]{3,})\s+(\d{1,2})/.exec(dateCell);
          const event = stripMarkup(row[1] ?? '');
          if (!d || !event) continue;
          // Spring events fall in the calendar year after the term opens.
          const month = MONTHS[d[1].slice(0, 3).toLowerCase()];
          const y = semester === 'Spring' && month && month <= 6 && calYear
            ? calYear
            : calYear;
          const iso = toIsoDate(y, d[1], d[2]);
          if (!iso) continue;
          events.push({
            yearNum,
            semester,
            date: iso,
            title: event,
            kind: /holiday|break|labor day|veterans/i.test(event) ? 'holiday'
              : /exam|due|quiz|midterm|final/i.test(event) ? 'assessment'
              : 'academic',
          });
        }
        i = table.end - 1;
      }
    }
  }
  return events;
}

/**
 * The letter-grade scale lives in UNIVERSITY POLICIES.md and is read from
 * there, never duplicated — the registry's own gpa.py takes the same line.
 *   | A- | 3.7 | 90-92% | Excellent |      (hyphen, en dash or minus accepted)
 *   | F  | 0.0 | < 60%  | Failing   |
 */
export function parseGradeScale(text) {
  const re = /^\|\s*([A-F][+\u2212\u2013-]?)\s*\|\s*([0-9.]+)\s*\|\s*(?:(\d+)\s*[\u2013\u2212-]\s*(\d+)|<\s*(\d+))\s*%?\s*\|\s*([^|]*)\|/gm;
  const rows = [];
  let m;
  while ((m = re.exec(text)) !== null) {
    const letter = m[1].replace(/[\u2212\u2013]/g, '-');
    const points = Number(m[2]);
    const low = m[5] !== undefined ? 0 : Number(m[3]);
    const high = m[5] !== undefined ? Number(m[5]) - 1e-9 : Number(m[4]);
    rows.push({ letter, points, low, high, descriptor: (m[6] || '').trim() });
  }
  rows.sort((a, b) => b.low - a.low);
  return rows;
}

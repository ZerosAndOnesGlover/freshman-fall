-- Institute of Science & Technology — portal schema
-- Rebuilt from the vault by `npm run import`. Student-generated data
-- (submissions, uploads, grades entered here) is preserved across re-imports;
-- see importer/run.js for how it is carried over.

PRAGMA foreign_keys = ON;

-- ─── People ──────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS users (
  id            INTEGER PRIMARY KEY,
  email         TEXT NOT NULL UNIQUE COLLATE NOCASE,
  password_hash TEXT NOT NULL,
  role          TEXT NOT NULL CHECK (role IN ('student','instructor','admin')),
  full_name     TEXT NOT NULL,
  student_id    TEXT UNIQUE,          -- registry number, students only
  title         TEXT,                 -- "Prof.", "Dr.", NULL for students
  programme     TEXT,
  year_level    INTEGER,
  created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS sessions (
  token      TEXT PRIMARY KEY,
  user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  expires_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);

-- ─── Academic structure ──────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS terms (
  id         INTEGER PRIMARY KEY,
  year_num   INTEGER NOT NULL,        -- 1..4
  year_label TEXT NOT NULL,           -- "Freshman"
  semester   TEXT NOT NULL,           -- "Fall" | "Spring"
  label      TEXT NOT NULL,           -- "Year 1 Fall"
  start_date TEXT,                    -- ISO, Monday of Week 0
  end_date   TEXT,
  is_current INTEGER NOT NULL DEFAULT 0,
  UNIQUE (year_num, semester)
);

CREATE TABLE IF NOT EXISTS courses (
  id          INTEGER PRIMARY KEY,
  code        TEXT NOT NULL,          -- "CS 101"
  title       TEXT NOT NULL,          -- "Computer Science I"
  subtitle    TEXT,                   -- "Foundations of Computation"
  credits     REAL NOT NULL DEFAULT 0,
  term_id     INTEGER REFERENCES terms(id) ON DELETE SET NULL,
  status      TEXT NOT NULL DEFAULT 'in-progress',
  schedule    TEXT,                   -- "Wed/Thu/Fri 09:00 + Tue Lab 15:00"
  room        TEXT,
  description TEXT,
  vault_path  TEXT,                   -- folder under the vault, if material exists
  has_material INTEGER NOT NULL DEFAULT 0,
  UNIQUE (code, term_id)
);
CREATE INDEX IF NOT EXISTS idx_courses_term ON courses(term_id);

CREATE TABLE IF NOT EXISTS course_staff (
  id         INTEGER PRIMARY KEY,
  course_id  INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  staff_role TEXT NOT NULL CHECK (staff_role IN ('instructor','ta')),
  office_hours TEXT,
  UNIQUE (course_id, user_id)
);

CREATE TABLE IF NOT EXISTS enrollments (
  id          INTEGER PRIMARY KEY,
  user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  course_id   INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  status      TEXT NOT NULL DEFAULT 'enrolled',
  enrolled_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (user_id, course_id)
);

-- ─── Course material ─────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS weeks (
  id           INTEGER PRIMARY KEY,
  course_id    INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  week_num     INTEGER NOT NULL,
  title        TEXT,
  topic        TEXT,
  takeaway     TEXT,
  next_up      TEXT,
  work         TEXT,
  monday_date  TEXT,
  friday_date  TEXT,
  readme_path  TEXT,
  summary_path TEXT,
  UNIQUE (course_id, week_num)
);

CREATE TABLE IF NOT EXISTS lectures (
  id         INTEGER PRIMARY KEY,
  course_id  INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  week_id    INTEGER REFERENCES weeks(id) ON DELETE CASCADE,
  seq        INTEGER NOT NULL DEFAULT 0,   -- lecture number within the course
  code       TEXT,                          -- "L04"
  title      TEXT NOT NULL,
  subtitle   TEXT,
  date_text  TEXT,                          -- "Wednesday 26 August 2026 · 09:00-09:50"
  date_iso   TEXT,
  start_time TEXT,                         -- "09:00", parsed out of date_text
  end_time   TEXT,                         -- "09:50"
  path       TEXT NOT NULL,                 -- vault-relative
  UNIQUE (course_id, path)
);
CREATE INDEX IF NOT EXISTS idx_lectures_week ON lectures(week_id);

-- Everything else in a week folder: labs, resources, starters, handouts.
CREATE TABLE IF NOT EXISTS materials (
  id        INTEGER PRIMARY KEY,
  course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  week_id   INTEGER REFERENCES weeks(id) ON DELETE CASCADE,
  kind      TEXT NOT NULL,   -- lab | resource | assignment | starter | readme | quiz
  title     TEXT NOT NULL,
  filename  TEXT NOT NULL,
  ext       TEXT,
  path      TEXT NOT NULL,
  UNIQUE (course_id, path)
);
CREATE INDEX IF NOT EXISTS idx_materials_week ON materials(week_id);

-- ─── Assessment ──────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS components (
  id          INTEGER PRIMARY KEY,
  course_id   INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  name        TEXT NOT NULL,         -- "Problem Sets"
  weight      REAL NOT NULL,         -- 30 = 30%; 0 = formative
  drop_lowest INTEGER NOT NULL DEFAULT 0,
  formative   INTEGER NOT NULL DEFAULT 0,
  position    INTEGER NOT NULL DEFAULT 0,
  UNIQUE (course_id, name)
);

CREATE TABLE IF NOT EXISTS assessments (
  id           INTEGER PRIMARY KEY,
  course_id    INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  component_id INTEGER REFERENCES components(id) ON DELETE SET NULL,
  week_id      INTEGER REFERENCES weeks(id) ON DELETE SET NULL,
  label        TEXT NOT NULL,        -- "PS 1" — the registry join key
  topic        TEXT,
  kind         TEXT NOT NULL,        -- ps|lab|quiz|midterm|final|project|paper|other
  possible     REAL NOT NULL DEFAULT 0,
  due_date     TEXT,                 -- ISO date
  due_time     TEXT,                 -- "17:00"
  notes        TEXT,
  room         TEXT,
  doc_path     TEXT,                 -- the assessment markdown in the vault
  accepts_upload INTEGER NOT NULL DEFAULT 1,
  position     INTEGER NOT NULL DEFAULT 0,
  UNIQUE (course_id, label)
);
CREATE INDEX IF NOT EXISTS idx_assessments_course ON assessments(course_id);
CREATE INDEX IF NOT EXISTS idx_assessments_due ON assessments(due_date);

-- ─── Student work ────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS submissions (
  id            INTEGER PRIMARY KEY,
  assessment_id INTEGER NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
  user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  attempt       INTEGER NOT NULL DEFAULT 1,
  body_text     TEXT,
  comment       TEXT,                -- note to the instructor
  status        TEXT NOT NULL DEFAULT 'draft'
                CHECK (status IN ('draft','submitted','late','graded','returned')),
  submitted_at  TEXT,
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at    TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (assessment_id, user_id, attempt)
);
CREATE INDEX IF NOT EXISTS idx_submissions_user ON submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_submissions_assessment ON submissions(assessment_id);

CREATE TABLE IF NOT EXISTS submission_files (
  id            INTEGER PRIMARY KEY,
  submission_id INTEGER NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
  original_name TEXT NOT NULL,
  stored_name   TEXT NOT NULL,
  size_bytes    INTEGER NOT NULL,
  mime          TEXT,
  uploaded_at   TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_files_submission ON submission_files(submission_id);

-- A grade can exist without a submission (exams sat in a hall, imported marks).
CREATE TABLE IF NOT EXISTS grades (
  id            INTEGER PRIMARY KEY,
  assessment_id INTEGER NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
  user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  submission_id INTEGER REFERENCES submissions(id) ON DELETE SET NULL,
  score         REAL,                -- NULL = not yet marked
  excused       INTEGER NOT NULL DEFAULT 0,
  feedback      TEXT,
  graded_by     INTEGER REFERENCES users(id) ON DELETE SET NULL,
  graded_at     TEXT,
  source        TEXT NOT NULL DEFAULT 'portal',  -- portal | registry
  UNIQUE (assessment_id, user_id)
);
CREATE INDEX IF NOT EXISTS idx_grades_user ON grades(user_id);

-- ─── Institutional content ───────────────────────────────────────────

CREATE TABLE IF NOT EXISTS announcements (
  id         INTEGER PRIMARY KEY,
  course_id  INTEGER REFERENCES courses(id) ON DELETE CASCADE,  -- NULL = university-wide
  author_id  INTEGER REFERENCES users(id) ON DELETE SET NULL,
  title      TEXT NOT NULL,
  body       TEXT NOT NULL,
  category   TEXT NOT NULL DEFAULT 'notice',
  pinned     INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_announcements_course ON announcements(course_id);

CREATE TABLE IF NOT EXISTS calendar_events (
  id          INTEGER PRIMARY KEY,
  term_id     INTEGER REFERENCES terms(id) ON DELETE CASCADE,
  date_iso    TEXT NOT NULL,
  title       TEXT NOT NULL,
  kind        TEXT NOT NULL DEFAULT 'academic',  -- academic | assessment | holiday
  course_code TEXT,
  detail      TEXT
);
CREATE INDEX IF NOT EXISTS idx_events_date ON calendar_events(date_iso);

-- Institution documents (policies, degree requirements) for the public site.
CREATE TABLE IF NOT EXISTS pages (
  id      INTEGER PRIMARY KEY,
  slug    TEXT NOT NULL UNIQUE,
  title   TEXT NOT NULL,
  summary TEXT,
  body_md TEXT NOT NULL,
  path    TEXT,
  nav_group TEXT
);

-- Week ↔ date map, per term, from the ASSESSMENT CALENDAR tables.
CREATE TABLE IF NOT EXISTS term_weeks (
  id       INTEGER PRIMARY KEY,
  term_id  INTEGER NOT NULL REFERENCES terms(id) ON DELETE CASCADE,
  week_num INTEGER NOT NULL,
  monday   TEXT NOT NULL,
  friday   TEXT NOT NULL,
  UNIQUE (term_id, week_num)
);

-- The letter-grade scale, parsed from UNIVERSITY POLICIES.md at import time.
-- That file is the vault's single source of truth for the scale; it is read,
-- never duplicated in code.
CREATE TABLE IF NOT EXISTS grade_scale (
  id      INTEGER PRIMARY KEY,
  letter  TEXT NOT NULL UNIQUE,
  points  REAL NOT NULL,
  low     REAL NOT NULL,
  high    REAL NOT NULL,
  descriptor TEXT
);

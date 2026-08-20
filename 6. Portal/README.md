# Institute of Science & Technology — Portal

A public university site and a student/faculty portal, built on top of this vault.
Course material is **read live from the markdown on disk**; submissions, grades and
accounts live in a local SQLite database. **The portal never writes to the vault.**

## Running it

```bash
cd "6. Portal"
npm run setup      # installs both packages and imports the vault into SQLite
npm run dev        # API on :4000, web on :5173
```

Then open **http://localhost:5173**.

Development sign-ins (printed by the importer, and listed on the sign-in page):

| Role | Email | Password |
|---|---|---|
| Student | `adebayo.glover@ist.edu` | `student2026` |
| Instructor | `david.malan@ist.edu` | `teach2026` |
| Registry (admin) | `registrar@ist.edu` | `teach2026` |

These exist because the database is local by design. Change them before this is
served anywhere but this machine.

## What is where

```
6. Portal/
  server/            Node + Express + better-sqlite3, plain SQL, no ORM
    src/schema.sql   19 tables
    src/importer/    reads the vault -> SQLite
    src/grading.js   course %, letter grade, GPA — ported from tools/gpa.py
    src/routes/      auth · public · dashboard · courses · assessments · grades · instructor
  web/               React 18 + Vite, vanilla CSS
    dev/             viewport harness for checking responsive layout
    src/styles/      tokens · base · components · prose · pages
    src/markdown.jsx marked + KaTeX + highlight.js, for vault markdown
```

## Commands

| Command | What it does |
|---|---|
| `npm run setup` | install everything, then import |
| `npm run dev` | run API and web together |
| `npm run import` | re-import the vault (keeps student work) |
| `npm run watch` | watch the vault and re-import on change (started by `dev`) |
|  `npm run import:reset` | drop the database and rebuild from scratch |
| `npm run build` | production build of the web app |
| `npm run inspect` | print a health report of the imported data |

## Do I need to re-import when I add content?

Mostly no — and never while `npm run dev` is running.

There are two different things going on:

- **The text of a lecture, lab or handout is read live from disk** every time
  a page is opened. Editing an existing file shows up on the next page load.
  Nothing to run, nothing to rebuild.
- **The index is in the database**: which courses, weeks, lectures and
  assessments exist, and their dates and point values. A *new* file, week or
  course only appears once that index is rebuilt.

`npm run dev` starts a watcher alongside the two servers, so new material is
indexed a second or two after you save it. If you are running the API on its
own, either run `npm run watch` beside it or `npm run import` when you are
done writing.

Re-importing is safe to do at any time: it is an upsert on natural keys, so
submissions, uploaded files and grades entered in the portal all survive it.

Years 3 and 4 have no material yet. Their courses still appear — the master
timetable knows their codes, titles and credits — and they are marked as not
yet published. They will fill in on their own as weeks are written.

## How the import works

The importer reads the registry as the authority, in this order:

1. **Gradebooks** (`5. Academic Registry/2. Gradebook/**`) — courses, components,
   weights, drop-lowest rules, every assessment and its point value.
2. **`ASSESSMENT CALENDAR.md`** — due dates and the week-to-date map.
3. **`MASTER TIMETABLE.md`** — credits, schedules, courses with no gradebook yet.
4. **`OFFICE HOURS.md`** — teaching staff and their hours.
5. **Course folders** (`0. Freshman/…`, `1. Sophomore/…`) — weeks, lectures, materials.
6. **`0. Institution/*.md`** — the public policy pages and the letter-grade scale.

It is an **upsert on natural keys** (course code + term, assessment label + course),
so re-importing preserves submissions, uploads and portal-entered grades. Rows that
disappear from the vault are pruned afterwards.

Two deliberate properties:

- **Registry marks never clobber portal marks.** A grade imported from a gradebook
  is written with `source = 'registry'` and is only overwritten by a later import if
  it is still registry-sourced. Anything an instructor enters here wins.
- **Vault paths are stored relative and resolved through a guard.** `resolveVaultPath()`
  refuses any path that escapes the vault root.

## Sessions, intakes and the registry

The registry account gets a **Registry** area in the portal, at
`/portal/registry`, with three tabs:

- **Overview** — the current session, headcounts, and every intake.
- **Sessions** — create an academic session (e.g. `2027/2028`), set which one
  is current, remove an empty one.
- **Students** — admit a student, enrol them in a year's courses, reset a
  password, deactivate a leaver.

An **academic session** is a calendar year pair. A student's **cohort** is the
session they were admitted in. Terms in this database stay degree-relative
("Year 1 Fall"), and the cohort is what maps them onto real calendar years —
which is what lets a 2027/2028 intake sit in Year 1 while the 2026/2027 intake
carries on into Year 2, against the same course structure.

Admitting a student issues a registry number automatically (`IST-2027-0001`,
counted within the intake year) and shows a temporary password **once**. Only
its hash is stored. They are prompted to choose their own password on first
sign-in, and doing so ends every other signed-in session for that account.

## Grading

`server/src/grading.js` is a port of the registry's `tools/gpa.py`, and produces
identical numbers. The three rules that matter:

1. A component's percentage is the **mean of its per-item ratios**, after dropping
   the lowest N — but never dropping the only remaining score.
2. A course percentage is the **weighted mean over components that have any marks**,
   so a course in progress still reports a meaningful figure.
3. A percentage maps to the **highest band whose floor it reaches**. 92.99 is an A−,
   not an A, and not a fall-through to F.

**GPA counts only fully-graded courses.** A course in progress shows a running
percentage and a letter marked *(partial)*, but contributes no grade points —
the same line `gpa.py` takes.

The letter scale itself is parsed from `0. Institution/UNIVERSITY POLICIES.md` at
import time. It is not duplicated in code.

## Timetable

Lecture headers carry their own time ("Wednesday 26 August 2026 · 09:00–09:50"),
which the importer parses into `start_time` / `end_time` — 340 of 391 lectures
have one. `/portal/timetable` shows a day at a time with a week strip and a date
picker, and the dashboard shows today's lectures.

Both take "today" from the **browser**, not the server, so it means today where
the student is, and both highlight the lecture running right now.

## Known data notes

- **116 of 492 assessments carry a due date.** The assessment calendar lists 151
  dated rows and does not enumerate every weekly item — lab reports are governed by
  a grade-*release* rule rather than a deadline. Where there is no date the UI shows
  the week instead.
- **CS 212's component weights sum to 90%, not 100%.** `gpa.py` warns about this
  too. It is a vault question, so the portal reports it rather than papering over it.

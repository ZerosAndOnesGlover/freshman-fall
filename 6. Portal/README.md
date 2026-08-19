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
| Registrar | `registrar@ist.edu` | `teach2026` |

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
    src/styles/      tokens · base · components · prose · pages
    src/markdown.jsx marked + KaTeX + highlight.js, for vault markdown
```

## Commands

| Command | What it does |
|---|---|
| `npm run setup` | install everything, then import |
| `npm run dev` | run API and web together |
| `npm run import` | re-import the vault (keeps student work) |
|  `npm run import:reset` | drop the database and rebuild from scratch |
| `npm run build` | production build of the web app |
| `npm run inspect` | print a health report of the imported data |

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

## Known data notes

- **116 of 492 assessments carry a due date.** The assessment calendar lists 151
  dated rows and does not enumerate every weekly item — lab reports are governed by
  a grade-*release* rule rather than a deadline. Where there is no date the UI shows
  the week instead.
- **CS 212's component weights sum to 90%, not 100%.** `gpa.py` warns about this
  too. It is a vault question, so the portal reports it rather than papering over it.

# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics

Answer sheets for PHYS 141, filed by teaching week. Repository-level conventions (submission
lifecycle, frontmatter, what git ignores) live in the Fall root `README.md`; this file covers
only this course.

**Source:** `4. PHYS 141 - Physics I: Mechanics, Waves, and Thermodynamics`

## Layout

Each teaching week `week0/` … `week12/` holds that week's answer sheets. A sheet sits in the week
its assessment was **set**.

| Pattern | What it is |
|---|---|
| `weekN/PS N.md` | Problem-set answer sheet |
| `weekN/Lab N.md` | Lab report, including the data tables and analysis |
| `weekN/Quiz N.md` | Quiz answer sheet |

**Quiz placement:** unlike PROG 101, PHYS 141 quizzes are filed in the week of their *material*
(Quiz N in `weekN/`), matching the course's own layout.

PHYS 141 is non-coding: lab reports carry their own representative measurements in tables, and
a plot is described where one is required (label, fit equation, R²). No code is submitted.

## Components

| Component | Points | Sheets | Naming |
|---|---|---|---|
| Problem Sets | 100 | PS 0 – PS 12 | `weekN/PS N.md` |
| Labs | 100 | Lab 0 – Lab 12 | `weekN/Lab N.md` |
| Quizzes | 25 | Quiz 0 – Quiz 12 | `weekN/Quiz N.md` |

## Progress

| | |
|---|---|
| Sheets written | 12 — Weeks 0–3 (PS 0–3, Lab 0–3, Quiz 0–3) |
| Graded | 12 |
| Remaining weeks | 4 – 12 not yet written |

## Conventions

- Frontmatter drives the lifecycle: `status: not-started` → `submitted` → `graded`, with
  `possible:`, `score:`, `started:`, `submitted:` and `graded:` filled in as work progresses.
- Every sheet carries **Marks** lines and a **Grading Summary** table filled in during marking;
  leave them alone until then.
- LaTeX is wrapped in `$…$` / `$$…$$`; keep non-ASCII characters (such as `°`, `·`, `–`) out of
  math mode — use `^\circ`, `\cdot`, `\text{--}` instead.
- `weekN/practice/` is ignored by git and never submitted — anything meant for grading goes in
  `weekN/` itself.

---
*Year 1 · Fall 2026 · Adebayo Glover*

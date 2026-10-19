# PROG 101 · Programming I: Structured Programming in C

Answer sheets and C source for PROG 101, filed by teaching week. Repository-level conventions
(submission lifecycle, frontmatter, what git ignores) live in the Fall root `README.md`; this
file covers only this course.

**Source:** `1. PROG 101 - Programming I: Structured Programming in C`

## Layout

Each teaching week `week0/` … `week12/` holds that week's answer sheet, its code sub-folder, and
any quiz. A sheet sits in the week its assessment was **set**.

| Pattern | What it is |
|---|---|
| `weekN/PS N.md` | Problem-set answer sheet |
| `weekN/Lab N.md` | Lab answer sheet |
| `weekN/Quiz N.md` | Quiz answer sheet |
| `weekN/psN/` | Problem-set code, `Makefile` and write-up |
| `weekN/labN/` | Lab code and notes |

**Quiz placement quirk:** PROG 101 quizzes are filed in the week *after* the material is
covered, so Quiz 0 sits in `week0/` but Quiz 1 and Quiz 2 sit in `week2/` and `week3/`.

## Components

| Component | Points | Sheets | Naming |
|---|---|---|---|
| Problem Sets | 100 | PS 0 – PS 12 | `weekN/PS N.md` |
| Labs | 100 | Lab 0 – Lab 3 | `weekN/Lab N.md` |
| Quizzes | 20 | Quiz 0 – Quiz 2 | `weekN/Quiz N.md` (see quirk) |

## Code

Every program is plain C11 and builds with `make`. Default flags are
`-Wall -Wextra -g -std=c11` (later weeks add `-Werror -pedantic`). Compiled artifacts
(`*.o`, `*.out`, `a.out`, and the extensionless binaries `make` produces) are gitignored — only
the `.c`, `.h`, `Makefile` and write-up `.md` are tracked.

## Progress

| | |
|---|---|
| Sheets | 20 |
| Graded | 11 — PS 0–3, Lab 0–3, Quiz 0–2 (Weeks 0–3) |
| Not started | 9 — PS 4 – PS 12 |

## Conventions

- Frontmatter drives the lifecycle: `status: not-started` → `submitted` → `graded`, with
  `possible:`, `score:`, `started:`, `submitted:` and `graded:` filled in as work progresses.
- Every sheet carries **Marks** lines and a **Grading Summary** table filled in during marking;
  leave them alone until then.
- `weekN/practice/` is ignored by git and never submitted — anything meant for grading goes in
  `weekN/` itself.

---
*Year 1 · Fall 2026 · Adebayo Glover*

# Year 1 · Fall 2026 · Submissions

**Student:** Adebayo Glover
**Programme:** B.Sc. Computer Science and Engineering, Year 1 (Freshman)
**Semester:** Fall 2026: Monday 21 September to Friday 25 December 2026 (finals 21–25 December)

This repository holds everything submitted for the Fall semester: one answer sheet per assessment,
and the code written for each lab and problem set.

---

## Courses

| Folder | Course | Sheets |
|---|---|---|
| `0. CS 101/` | Computer Science I: Foundations of Computation | 40 |
| `1. PROG 101/` | Programming I: Structured Programming in C | 40 |
| `2. MATH 141/` | Calculus I: Limits, Derivatives, and Integrals | 40 |
| `3. MATH 151/` | Discrete Mathematics for Computer Science | 39 |
| `4. PHYS 141/` | Physics I: Mechanics, Waves, and Thermodynamics | 41 |
| `5. CS 190/` | CS Seminar: Profession, Ethics & Culture | 20 |

Each course folder has `week0/` … `week12/`, one per teaching week. A sheet sits in the week its
assessment was **set**, so a quiz on Week 10 material given on the Monday of Week 11 lives in
`week11/`. Each course folder has its own README with a week-by-week breakdown.

Every `weekN/` also has a `practice/` folder for classwork practice, test code and
experiments. It is ignored by git and never submitted, so anything meant for grading goes in
`weekN/` itself.

---

## How each assessment is submitted

1. The answer is written under each heading of the answer sheet; any code goes in the same
   `weekN/` folder.
2. The sheet's frontmatter is set to `status: submitted`.
3. The work is committed and pushed.
4. After grading, the sheet's `score:` is filled in and its status set to `graded`.

---

## What is ignored

- `.gitignore` at the semester root applies to every course: OS files, editor files and stray
  Obsidian folders.
- Every course `.gitignore` ends with `practice/`, so each week's practice folder stays local.
- Each course folder has its own `.gitignore` for the output of its own tools:

| File | Ignores |
|---|---|
| `0. CS 101/.gitignore` | Python bytecode, virtual environments, test and notebook caches |
| `1. PROG 101/.gitignore` | everything except C sources, headers, Makefiles, scripts and Markdown, so binaries and object files never get committed |
| `2. MATH 141/.gitignore` | Python bytecode, virtual environments, test and notebook caches |
| `3. MATH 151/.gitignore` | Python bytecode, virtual environments, test and notebook caches |
| `4. PHYS 141/.gitignore` | Python bytecode, virtual environments, notebook caches, office lock files (lab data is kept) |
| `5. CS 190/.gitignore` | office lock files (drafts and the presentation are kept) |

---

## Key dates

| Date | |
|---|---|
| Mon 21 Sep | Classes begin (Week 0) |
| Mon 2 – Fri 6 Nov | Midterm 1 week |
| Mon 30 Nov – Wed 2 Dec | Midterm 2 week |
| Fri 18 Dec | Last day of instruction |
| Mon 21 – Fri 25 Dec | Finals |

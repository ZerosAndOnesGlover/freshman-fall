# Year 1 · Fall 2026 · Submissions

**Student:** Adebayo Glover
**Programme:** B.Sc. Computer Science and Engineering, Year 1 (Freshman)
**Semester:** Fall 2026: Monday 21 September to Friday 18 December 2026 (finals 21–25 December)

This repository holds everything submitted for the Fall semester: one answer sheet per assessment,
and the code written for each lab and problem set.

---

## Courses

| Folder | Course | Sheets |
|---|---|---|
| `0. CS 101/` | Computer Science I: Foundations of Computation | 11 |
| `1. PROG 101/` | Programming I: Structured Programming in C | 12 |
| `2. MATH 141/` | Calculus I: Limits, Derivatives, and Integrals | 24 |
| `3. MATH 151/` | Discrete Mathematics for Computer Science | 11 |
| `4. PHYS 141/` | Physics I: Mechanics, Waves & Thermodynamics | — |
| `5. CS 190/` | CS Seminar: Profession, Ethics & Culture | — |

Each course folder has `week0/` … `week12/`, one per teaching week. A sheet sits in the week its
assessment was **set**, so a quiz on Week 10 material given on the Monday of Week 11 lives in
`week11/`. PHYS 141 and CS 190 are scaffolded but their answer sheets are not written yet.

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

- `.gitignore` at the repo root applies to every course: OS files, editor files, Python bytecode,
  Obsidian workspace state and compiled C output.
- The final rule, `practice/`, ignores every week's practice folder, so classwork practice, test
  code and experiments stay local. Anything meant for grading goes in `weekN/` itself.
- Compiled C artifacts (`*.o`, `*.out`, `*.exe`, `a.out`) built by the PROG 101 labs are ignored.

---

## Key dates

| Date | |
|---|---|
| Thu 17 Sep | Freshman Orientation begins |
| Mon 21 Sep | Classes begin (Week 0) |
| Fri 25 Sep | Add/Drop deadline |
| Mon 28 Sep | Week 1 begins; first quizzes |
| Mon 2 Nov | Midterm 1 week begins (Week 6) |
| Mon 30 Nov | Midterm 2 week begins (Week 10) |
| Fri 18 Dec | Last day of instruction |
| Mon 21 – Fri 25 Dec | Finals |

# MATH 141 · Calculus I: Limits, Derivatives, and Integrals

**Course:** MATH 141 — Calculus I: Limits, Derivatives, and Integrals
**Programme:** B.Sc. Computer Science and Engineering, Year 1 (Freshman)
**Semester:** Fall 2026: Monday 21 September to Friday 18 December 2026 (finals 21–25 December)
**Source materials:** `2. MATH 141 - Calculus I: Limits, Derivatives, and Integrals`

MATH 141 is the first calculus course: limits and continuity, the derivative and its rules,
applications of differentiation, and integration with the Fundamental Theorem of Calculus and
its applications. Assessment is by problem set, computer lab and quiz.

---

## Topics

| Week | Topic |
|---|---|
| 0 | Algebra and functions review |
| 1 | Limits |
| 2 | Continuity and the Intermediate Value Theorem |
| 3 | The definition of the derivative |
| 4 | Differentiation rules and the chain rule |
| 5 | Implicit differentiation, logarithmic differentiation and related rates |
| 6 | Extrema, the Mean Value Theorem and L'Hôpital's rule |
| 7 | Curve shape, curve sketching and applied optimisation |
| 8 | Riemann sums and the definite integral |
| 9 | The Fundamental Theorem of Calculus |
| 10 | Substitution, symmetry and integration by parts |
| 11 | Applications of integration |
| 12 | Review and a Taylor-polynomial preview |

Each course folder has `week0/` … `week12/`, one per teaching week, and each `weekN/` also has a
`practice/` folder for classwork, test code and experiments that is never submitted.

---

## Assessment

| Component | Weight | Points each | Naming |
|---|---|---|---|
| Problem Sets | 30% | 100 | `weekN/PS N.md` |
| Midterm 1 | 15% | 100 | `week6/Midterm 1.md` |
| Midterm 2 | 15% | 100 | `week10/Midterm 2.md` |
| Final Exam | 20% | 100 | `week12/Final Exam.md` |
| Labs | 10% | 20 or 100 | `weekN/Lab N.md` |
| Quizzes | 10% | 20 | `weekN/Quiz NN.md` |

MATH 141 has twelve graded problem sets (PS 0–11, lowest one dropped; PS 12 is an ungraded revision
set with no sheet), twelve graded quizzes (Quiz 01–12, lowest one dropped; the Week 0 diagnostic is
ungraded and has no sheet) and graded labs 1–11. Lab 0 and Lab 12 are ungraded and their sheets stay blank. Lab points vary by
lab (20 or 100), as the gradebook lists them. A quiz is filed in the week it is sat, so Quiz *NN*
(which covers Week *N−1*) lives in `weekN/`; a lab meets on the Friday of its own week and lives in
`weekN/`. Quiz sheets are zero-padded (`Quiz 01.md`, `Quiz 02.md`). Labs use plain Python (Desmos for
graphs) and only what CS 101 has taught by the lab's date. Problem sets, labs, quizzes and exams are
all answer sheets in the same layout.

Midterm 1 is sat on Thursday 5 November 2026, 18:00–19:15 in VNC 200, and covers Weeks 0–5. Midterm 2
is on Wednesday 2 December 2026, 18:00–19:15 in VNC 200, and covers Weeks 6–9. The Final Exam is on
Wednesday 23 December 2026, 09:00–11:30 in VNC 200 (150 minutes, a 2-page cheat sheet allowed), and
covers Weeks 0–12. No exam papers exist in the course materials yet, so each exam sheet has a single
answer block.

---

## How each assessment is submitted

1. The answer is written under each heading of the answer sheet.
2. The sheet's frontmatter is set to `status: submitted`.
3. The work is committed and pushed.
4. After grading, the sheet's `score:` is filled in and its status set to `graded`.

---

## What is ignored

- `.gitignore` at the repo root applies to every course: OS files, editor files, Python bytecode
  and Obsidian workspace state.
- The final rule, `practice/`, ignores every week's practice folder, so classwork, test code and
  experiments stay local. Anything meant for grading goes in `weekN/` itself.

---

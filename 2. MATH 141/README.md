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

| Component | Points | Naming |
|---|---|---|
| Problem Sets | 100 | `weekN/PS N.md` |
| Labs | 100 | `weekN/Lab N.md` |
| Quizzes | 20 | `weekN/Quiz NN.md` |

Quiz sheets are zero-padded (`Quiz 01.md`, `Quiz 02.md`). Labs are written for the Friday
session, with computation in plain Python (Desmos for graphs) using only what CS 101 has taught
by the lab's date.

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

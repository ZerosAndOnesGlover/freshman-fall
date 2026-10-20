# MATH 151 · Discrete Mathematics for Computer Science

**Course:** MATH 151 — Discrete Mathematics for Computer Science
**Programme:** B.Sc. Computer Science and Engineering, Year 1 (Freshman)
**Semester:** Fall 2026: Monday 21 September to Friday 18 December 2026 (finals 21–25 December)
**Source materials:** `3. MATH 151 - Discrete Mathematics for Computer Science`

MATH 151 covers the discrete mathematics that underpins computer science: logic and proof, sets,
functions and relations, counting, recurrences, graphs, trees and number theory. It is assessed
by problem sets, weekly quizzes and completion-checked labs.

---

## Topics

| Week | Topic |
|---|---|
| 0 | Propositional logic |
| 1 | Predicates and quantifiers |
| 2 | Proof techniques |
| 3 | Induction |
| 4 | Sets |
| 5 | Functions |
| 6 | Relations |
| 7 | Counting |
| 8 | Advanced counting |
| 9 | Recurrences |
| 10 | Graphs |
| 11 | Trees |
| 12 | Number theory |

Each course folder has `week0/` … `week12/`, one per teaching week, and each `weekN/` also has a
`practice/` folder for classwork, test code and experiments that is never submitted.

---

## Assessment

| Component | Points | Naming |
|---|---|---|
| Problem Sets | 100 | `weekN/PS N.md` |
| Labs | completion | `weekN/Lab N.md` |
| Quizzes | 20 | `weekN/Quiz N.md` |

MATH 151 has thirteen problem sets (PS 0–12, lowest one dropped), twelve weekly quizzes (Quiz 1–12,
lowest one dropped) and thirteen labs (Lab 0–12, graded on completion). A quiz is filed in the week
it is administered, so Quiz *N* (which covers Week *N−1*) lives in `weekN/`. Each lab meets the
Wednesday after its material but is filed with that material, so Lab *N* lives in `weekN/`.
Problem sets, labs and quizzes are all answer sheets in the same layout.

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

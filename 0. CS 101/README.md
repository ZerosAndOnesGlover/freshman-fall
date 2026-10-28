# CS 101 · Computer Science I: Foundations of Computation

**Course:** CS 101 — Computer Science I: Foundations of Computation
**Programme:** B.Sc. Computer Science and Engineering, Year 1 (Freshman)
**Semester:** Fall 2026: Monday 21 September to Friday 18 December 2026 (finals 21–25 December)
**Source materials:** `0. CS 101 - Computer Science I: Foundations of Computation`

CS 101 is the first programming course of the programme, taught in Python. It moves from
expressions and control flow through functions and recursion, algorithms and data structures,
and closes with models of computation. Assessment is by problem set, lab, two midterms, two
projects and a final exam; the code written for a week sits alongside that week's answer sheets.

---

## Topics

| Week | Topic |
|---|---|
| 0 | What computer science is; the Python environment and REPL; values, types and expressions |
| 1 | Data types, variables, expressions and operators |
| 2 | Conditionals and loops |
| 3 | Functions, scope and the call stack |
| 4 | Recursion |
| 5 | Searching and sorting |
| 6 | Algorithm analysis: Big-O and recurrences |
| 7 | Abstract data types: dynamic arrays, linked lists, stacks and queues |
| 8 | Hash tables, dictionaries and sets |
| 9 | Strings, text processing and regular expressions |
| 10 | Files, exceptions and structured I/O (CSV and JSON) |
| 11 | Models of computation: automata, decidability and the halting problem |
| 12 | Synthesis and review |

Each course folder has `week0/` … `week12/`, one per teaching week, and each `weekN/` also has a
`practice/` folder for classwork, test code and experiments that is never submitted.

---

## Assessment

| Component | Weight | Sheets |
|---|---|---|
| Problem Sets (PS 1–11, lowest dropped) | 30% | `weekN/PS N.md` |
| Midterm 1 (Weeks 0–5) | 15% | `week6/Midterm 1.md` |
| Midterm 2 (Weeks 6–9) | 15% | `week10/Midterm 2.md` |
| Final Exam (Weeks 0–11) | 20% | `week12/Final Exam.md` |
| Labs (Lab 0–11) | 10% | `weekN/Lab N.md` |
| Projects 1–2 | 10% | `week7/Project 1.md`, `week12/Project 2.md` |
| Quizzes (Quiz 0–11) | formative, 0% | `weekN/Quiz N.md` |

Week 0 has the graded Lab 0 and the ungraded Quiz 0 self-assessment. Each sheet is filed in the
same week as its handout: Lab N in `weekN/` although it meets on the Tuesday of week N + 1, Quiz N
in `weekN/` although it covers week N − 1, the midterms in `week6/` and `week10/`, and the final in
`week12/`. The code sits flat in `weekN/` beside the sheets,
under the file names the handouts give (`ps1.py`, `scope_bugs.py`, …). All code is Python, and only
what the lectures have taught by the work's date is used.

---

## How each assessment is submitted

1. The answer is written under each heading of the answer sheet; any code goes in `weekN/`
   beside it.
2. The sheet's frontmatter is set to `status: submitted`.
3. The work is committed and pushed.
4. After grading, the sheet's `score:` is filled in and its status set to `graded`.

---

## What is ignored

- `.gitignore` at the repo root applies to every course: OS files, editor files, Python bytecode,
  compiled C output and Obsidian workspace state.
- The final rule, `practice/`, ignores every week's practice folder, so classwork, test code and
  experiments stay local. Anything meant for grading goes in `weekN/` itself.

---

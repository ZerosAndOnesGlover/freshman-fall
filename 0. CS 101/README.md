# CS 101 · Computer Science I: Foundations of Computation

**Course:** CS 101 — Computer Science I: Foundations of Computation
**Programme:** B.Sc. Computer Science and Engineering, Year 1 (Freshman)
**Semester:** Fall 2026: Monday 21 September to Friday 18 December 2026 (finals 21–25 December)
**Source materials:** `0. CS 101 - Computer Science I: Foundations of Computation`

CS 101 is the first programming course of the programme, taught in Python. It moves from
expressions and control flow through functions and recursion, algorithms and data structures,
and closes with models of computation. Assessment is by problem set, lab and quiz; the code
written for a week sits alongside that week's answer sheets.

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

| Component | Points | Naming |
|---|---|---|
| Problem Sets | 100 | `weekN/PS N.md` |
| Labs | 100 | `weekN/Lab N.md` |
| Quizzes | 10 | `weekN/Quiz N.md` |

CS 101 has no Week 0 assessment; sheets begin in `week1/`. Every problem set and lab has a
`weekN/psN/` or `weekN/labN/` folder holding the code and a short write-up. Sheets are written in
Python; only what the lectures have taught by the work's date is used.

---

## How each assessment is submitted

1. The answer is written under each heading of the answer sheet; any code goes in the week's
   `weekN/psN/` or `weekN/labN/` folder.
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

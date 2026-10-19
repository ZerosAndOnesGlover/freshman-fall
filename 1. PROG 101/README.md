# PROG 101 · Programming I: Structured Programming in C

**Course:** PROG 101 — Programming I: Structured Programming in C
**Programme:** B.Sc. Computer Science and Engineering, Year 1 (Freshman)
**Semester:** Fall 2026: Monday 21 September to Friday 18 December 2026 (finals 21–25 December)
**Source materials:** `1. PROG 101 - Programming I: Structured Programming in C`

PROG 101 covers structured programming in C, from the compilation model and types through
pointers, dynamic memory and data structures, the preprocessor and generic programming, ending
with engineering practice. Assessment is by problem set, lab and quiz; each week's C source and
`Makefile` sit alongside that week's answer sheets.

---

## Topics

| Week | Topic |
|---|---|
| 0 | The compilation model, tool-chain (gcc, make, GDB) and a first C program |
| 1 | Types, variables, memory and number representation |
| 2 | Operators, expressions, evaluation order and control flow |
| 3 | Functions, pass-by-value, the call stack and multi-file programs |
| 4 | Arrays, strings and bounded string functions |
| 5 | Pointers: pass-by-pointer, arithmetic, `NULL` and `const` |
| 6 | The process memory map, dynamic memory and ownership |
| 7 | Structures, unions, enums, bitfields and linked lists |
| 8 | File I/O, the Unix file model and binary serialisation |
| 9 | Recursion, divide-and-conquer and binary trees |
| 10 | The C preprocessor and macros |
| 11 | Function pointers, generic programming with `void *` and callbacks |
| 12 | Style, testing and debugging |

Each course folder has `week0/` … `week12/`, one per teaching week, and each `weekN/` also has a
`practice/` folder for classwork, test code and experiments that is never submitted.

---

## Assessment

| Component | Points | Naming |
|---|---|---|
| Problem Sets | 100 | `weekN/PS N.md` |
| Labs | 100 | `weekN/Lab N.md` |
| Quizzes | 20 | `weekN/Quiz N.md` |

Every program is plain C11 and builds with `make`; default flags are `-Wall -Wextra -g -std=c11`,
with later weeks adding `-Werror -pedantic`. Lab N meets in the week after its material is
covered. Quizzes are filed in the week *after* the material, so Quiz 0 is in `week0/` but Quiz 1
and Quiz 2 are in `week2/` and `week3/`.

---

## How each assessment is submitted

1. The answer is written under each heading of the answer sheet; the code goes in the week's
   `weekN/psN/` or `weekN/labN/` folder with a `Makefile`.
2. The sheet's frontmatter is set to `status: submitted`.
3. The work is committed and pushed.
4. After grading, the sheet's `score:` is filled in and its status set to `graded`.

---

## What is ignored

- `.gitignore` at the repo root applies to every course: OS files, editor files, Python bytecode,
  Obsidian workspace state and compiled C output.
- The final rule, `practice/`, ignores every week's practice folder, so classwork, test code and
  experiments stay local. Anything meant for grading goes in `weekN/` itself.
- Compiled C artifacts (`*.o`, `*.out`, `*.exe`, `a.out`) and the extensionless binaries built by
  the labs are ignored; only the `.c`, `.h`, `Makefile` and write-up `.md` are tracked.

---

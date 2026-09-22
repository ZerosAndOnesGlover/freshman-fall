# PROG 101 - Programming I: Structured Programming in C

**Student:** Adebayo Glover
**Year:** Freshman
**Institution:** Institute of Science and Technology (IST)

## Course Overview

This folder holds all labs, problem sets and quizzes for PROG 101. It is part of the Fall 2026 submissions repo (see `../README.md`) — there is no separate repository here.

## Structure

One folder per teaching week (`week0/` … `week12/`). Each holds that
week's answer sheets alongside any C code written for it.

| Week | Topic | Sheets |
|---|---|---|
| `week0/` | Orientation & tool-chain setup | PS 0, Quiz 0 |
| `week1/` | Data representation — integers, floating point | PS 1, Lab 1 |
| `week2/` | Operators, expressions & control flow | PS 2, Lab 2, Quiz 1 |
| `week3/` | Functions & structured programming | PS 3, Lab 3, Quiz 2 |
| `week4/` | Arrays & strings | PS 4, Lab 4, Quiz 3 |
| `week5/` | Pointers I — the fundamental abstraction | PS 5, Lab 5, Quiz 4 |
| `week6/` | Pointers II — dynamic memory | PS 6, Lab 6, Quiz 5, **Midterm 1** |
| `week7/` | Composite types, tagged unions, data structures | PS 7, Lab 7, Quiz 6 |
| `week8/` | Files — text, binary, a small database | PS 8, Lab 8, Quiz 7 |
| `week9/` | Induction in code, sorting, recursive structures | PS 9, Lab 9, Quiz 8 |
| `week10/` | The C preprocessor & macros | PS 10, Lab 10, Quiz 9, **Midterm 2** |
| `week11/` | The standard library & a systems preview | PS 11, Lab 11, Quiz 10 |
| `week12/` | Software engineering in C — style, testing, debugging | PS 12, Lab 12, Quiz 11, **Final Exam** |

40 sheets in total. Lab N meets on the Monday of Week N+1, so `Lab 1` sits in `week1/` although it runs on Monday 5 October. Quizzes cover the previous week, so `Quiz 11` sits in `week12/` and examines Week 11.

Build output is never committed: `.gitignore` here ignores everything except `*.c`, `*.h`,
`Makefile`, `*.sh` and `*.md`.

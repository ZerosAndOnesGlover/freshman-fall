---
course: PROG 201
title: "Systems Programming in C"
credits: 4
year: 2
semester: Fall
status: in-progress
---

# PROG 201 · Gradebook
## Systems Programming in C · 4 credits · Year 2 Fall

> **How to use this file.** Enter a number in the **Earned** column only. Everything else —
> percentages, component subtotals, the course grade, the letter, and the GPA points — is computed by
> `tools/gpa.py`. Do not hand-edit the Computed block; it is overwritten on every run.
>
> Leave **Earned** blank for anything not yet marked. Blank rows are excluded from the average rather
> than counted as zero, so partial-term percentages stay meaningful. Enter `0` for a genuine zero and
> `EX` to excuse an item.

> **Weights come from the curriculum docx** — *Problem Sets 35%, Projects 25%, Midterms 25%,
> Final 15%* — which sums to 100% without a laboratory line. Labs are checked off in the session and
> quizzes are unmarked; both live in [[_PROG 201 Lab and Quiz Record]].

---

## Component Weights

| Component | Weight | Rule |
|---|---|---|
| Problem Sets | 35% | Lowest 1 dropped |
| Midterm Exam 1 | 12.5% | Week 4, covers Weeks 0–3 |
| Midterm Exam 2 | 12.5% | Week 8, covers Weeks 4–7 |
| Project 1 | 12.5% | Unix shell (tsh), due Week 9 |
| Project 2 | 12.5% | Networked multi-threaded server |
| Final Exam | 15% | Comprehensive |
| **Total** | **100%** | |

---

## Problem Sets — 35%, lowest 1 dropped

| Item | Topic | Possible | Earned |
|---|---|---|---|
| PS 0 | The Unix process model: fork, exec, wait, zombies | 100 | |
| PS 1 | Implement I/O redirection (pipe and redirect operators) | 100 | |
| PS 2 | A producer-consumer pipeline using pipes and shared memory | 100 | |
| PS 3 | Implement a thread pool | 100 | |
| PS 4 | Implement a basic malloc/free using mmap | 100 | |
| PS 5 | Build a concurrent HTTP/1.0 server | 100 | |
| PS 6 | Implement a shell (tsh) with pipelines, redirection, background jobs | 100 | |
| PS 7 | Implement a simple file system in C over a disk image | 100 | |
| PS 8 | Use LD_PRELOAD to intercept malloc() for profiling | 100 | |
| PS 9 | Optimize a provided slow program — 5× by analysis, not guessing | 100 | |
| PS 10 | Build a working ROP chain exploit (sandboxed) | 100 | |
| PS 11 | A mini-container using clone() with CLONE_NEWPID|CLONE_NEWNET | 100 | |
| PS 12 | Synthesis: a production-quality daemon | 100 | |

---

## Midterm Exam 1 — 12.5%

| Item | Coverage | Possible | Earned |
|---|---|---|---|
| Midterm 1 | Weeks 0–3, Week 4, 90 min | 100 | |

---

## Midterm Exam 2 — 12.5%

| Item | Coverage | Possible | Earned |
|---|---|---|---|
| Midterm 2 | Weeks 4–7, Week 8, 90 min | 100 | |

---

## Project 1 — 12.5%

| Item | Coverage | Possible | Earned |
|---|---|---|---|
| Project 1 | Unix shell (tsh), assigned Week 6, due Week 9 | 100 | |

---

## Project 2 — 12.5%

| Item | Coverage | Possible | Earned |
|---|---|---|---|
| Project 2 | Networked, multi-threaded server | 100 | |

---

## Final Exam — 15%

| Item | Coverage | Possible | Earned |
|---|---|---|---|
| Final Exam | Weeks 0–12, comprehensive, 150 min | 100 | |

---

<!-- BEGIN COMPUTED -->
## Computed

*Not yet calculated. Run `python3 tools/gpa.py` from the Academic Registry root.*
<!-- END COMPUTED -->

---

*PROG 201 · Gradebook · Year 2 Fall*

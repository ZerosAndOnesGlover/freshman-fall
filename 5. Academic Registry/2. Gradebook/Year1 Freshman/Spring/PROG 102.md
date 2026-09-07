---
course: PROG 102
title: "Programming II · Object-Oriented Design & Data Structures in C++"
credits: 4
year: 1
semester: Spring
status: in-progress
---

# PROG 102 · Gradebook
## Programming II · Object-Oriented Design & Data Structures in C++ · 4 credits · Year 1 Spring

> Enter a number in **Earned** only. Percentages, the course grade, the letter and the GPA points
> are computed by `tools/gpa.py`. Blank = not yet marked (excluded, not zero). `EX` = excused.
>
> **Weights are taken directly from the Year 1 curriculum document** — *Labs 20%, Problem Sets 30%,
> Midterms 25%, Final 15%, Projects 10%*. The only elaboration is splitting Midterms into two equal
> halves and Projects into two equal halves. **No component was added or removed, and there is no
> deviation to document for this course.**
>
> **Note the difference from CS 102: labs are weighted here.** They are a graded component at 20%,
> not a completion gate, so they live in this file rather than in a separate record. **Quizzes** carry
> no weight and are tracked in [[_PROG 102 Quiz Record]].

---

## Component Weights

| Component | Weight | Rule |
|---|---|---|
| Labs | 20% | 13 labs, lowest 1 dropped |
| Problem Sets | 30% | 12 problem sets, lowest 1 dropped |
| Midterm Exam 1 | 12.5% | Weeks 0–4 |
| Midterm Exam 2 | 12.5% | Weeks 5–9 |
| Final Exam | 15% | Comprehensive |
| Project 1 | 5% | Assigned Week 6, due Week 9 |
| Project 2 | 5% | Due Week 12 |
| **Total** | **100%** | |

---

## Labs — 20%, lowest 1 dropped

*One lab every week, Weeks 0–12. Marked on an in-lab checkoff by the TA.*

| Item | Topic | Possible | Earned |
|---|---|---|---|
| Lab 0 | Port a C program to C++ using classes | 40 | |
| Lab 1 | Debug copy vs shallow copy issues | 40 | |
| Lab 2 | Compile time vs runtime trade-offs of templates | 40 | |
| Lab 3 | Profile STL container operations | 40 | |
| Lab 4 | Inspect vtable layout with GDB | 40 | |
| Lab 5 | Memory leak detection with AddressSanitizer | 40 | |
| Lab 6 | Benchmark a custom list against std::list | 40 | |
| Lab 7 | Refactor a messy class hierarchy using patterns | 40 | |
| Lab 8 | Build a simple event system using Observer | 40 | |
| Lab 9 | Comprehensive tests with a C++ testing framework | 40 | |
| Lab 10 | Find and fix race conditions with ThreadSanitizer | 40 | |
| Lab 11 | Profile lambda overhead | 40 | |
| Lab 12 | Final project demo and code review | 40 | |

---

## Problem Sets — 30%, lowest 1 dropped

*Released Friday, due the following Friday. No problem set in Week 12.*

| Item | Topic | Possible | Earned |
|---|---|---|---|
| PS 0 | Classes, constructors, destructors, const-correctness | 100 | |
| PS 1 | A Vector3D class with a full operator set | 100 | |
| PS 2 | A generic `Stack<T>` template | 100 | |
| PS 3 | Ten problems using only STL containers and algorithms | 100 | |
| PS 4 | A Shape hierarchy with polymorphic area and draw | 100 | |
| PS 5 | Rewrite a raw-pointer program using smart pointers | 100 | |
| PS 6 | A templated doubly linked list with bidirectional iterators | 100 | |
| PS 7 | Factory Method and Decorator | 100 | |
| PS 8 | Observer and Strategy | 100 | |
| PS 9 | Make a data structure exception-safe | 100 | |
| PS 10 | A thread-safe bounded queue | 100 | |
| PS 11 | Imperative algorithms rewritten in functional style | 100 | |

---

## Midterm Exam 1 — 12.5%

| Item | Topic | Possible | Earned |
|---|---|---|---|
| Midterm 1 | Weeks 0–4: classes, operators, templates, STL, polymorphism | 100 | |

---

## Midterm Exam 2 — 12.5%

| Item | Topic | Possible | Earned |
|---|---|---|---|
| Midterm 2 | Weeks 5–9: RAII, data structures, design patterns, exceptions | 100 | |

---

## Final Exam — 15%

| Item | Topic | Possible | Earned |
|---|---|---|---|
| Final Exam | Comprehensive, Weeks 0–12 | 180 | |

---

## Project 1 — 5%

| Item | Topic | Possible | Earned |
|---|---|---|---|
| Project 1 | Assigned Week 6, due Week 9 | 100 | |

---

## Project 2 — 5%

| Item | Topic | Possible | Earned |
|---|---|---|---|
| Project 2 | Data structure library with tests, due Week 12 | 100 | |

---

---

> **Quizzes are tracked separately** in [[_PROG 102 Quiz Record]], deliberately kept out of this
> file. They carry no weight, so including them here would add rows beneath the last weighted
> component that the parser reads as belonging to it — the failure mode documented in CS 102's
> record. The leading underscore keeps that file out of `tools/gpa.py`'s course scan.

---

<!-- BEGIN COMPUTED -->
## Computed

*Not yet calculated. Run `python3 tools/gpa.py`.*
<!-- END COMPUTED -->

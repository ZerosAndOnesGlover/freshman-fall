# CS 101 · Week 12
## Synthesis, Review, Path Forward

---

## Overview

The final week. No new technical material: Week 12 closes the course by showing that its eleven
topics were **one idea applied eleven times** — build an abstraction, then find where it leaks — and
maps what was deliberately left out.

It also carries the two heaviest remaining assessments: the **Final Exam** (25%) and **Project 2**
(5%).

---

## Contents

```
CS101 Week12/
├── lectures/
│   ├── L37 Synthesis The Whole Stack.md
│   ├── L38 What Comes Next.md
│   └── L39 Reading Code and the Practice of Programming.md
├── assignments/
│   ├── FINAL EXAM Review and Practice Exam.md
│   ├── PROJECT 2 Algorithm Visualizer.md
│   └── project2_starter.py
├── resources/
│   └── Reading Guide Week 12.md
└── solutions_instructor/
    ├── PROJECT 2 Instructor Guide.md
    └── project2_reference.py
```

The Final Exam document contains its own answer key (Part III), matching the Week 6 midterm
convention.

---

## Schedule

| Day | Session | Topic |
|---|---|---|
| Tue 15 Dec | Lab 11 | Turing machine simulator (covers Week 11) |
| Wed 16 Dec | L37 | Synthesis — the abstraction stack, four threads, one worked problem using seven weeks at once |
| Thu 17 Dec | L38 | What comes next — concurrency, the layers above and below, how to choose |
| Fri 18 Dec | L39 | Reading code, judgement, and the practice of programming |

**Project 2 due** Friday 18 December, 17:00. **Final Exam** Tuesday 22 December, 09:00–11:30, VNC 100.

There is no Quiz 12 and no PS 12.

---

## Learning Objectives

By the end of Week 12 you should be able to:

1. Describe the course as a stack of abstractions and name where each one leaks
2. Trace a single realistic problem through seven weeks of course material
3. State honestly what you know, what you have only touched, and what you have not met
4. Explain why concurrency was excluded, and recognise the read-modify-write race
5. Read an unfamiliar codebase methodically rather than linearly
6. Exercise judgement about when a technique is worth its cost

---

## Assessment Summary

| Item | Weight | Due |
|---|---|---|
| **Project 2** — Algorithm Visualizer | 5% | Friday 18 December, 17:00 |
| **Final Exam** — covers Weeks 1–11 | 25% | Tuesday 22 December, 09:00–11:30 |

Project 2 was **assigned Friday 4 December (Week 10)**; the specification lives here in Week 12 with the rest of the
final-week material.

---

## Verification

All code and quantitative claims were verified by execution:

- `project2_starter.py` → **3/15** (bubble sort worked, two frame-contract tests pass)
- `project2_reference.py` → **15/15**
- All four sorts verified correct across 4 input shapes × 6 sizes including n = 0 and n = 1
- **Selection sort: exactly n(n−1)/2 comparisons**, identical on random, sorted, and reversed input
- **Bubble swaps = insertion swaps = inversion count**, exactly, at n = 5, 10, 20, 40, 64, 100, plus
  sorted and reversed
- **Bubble and insertion: 63 comparisons at n = 64 on sorted input** (n−1, the Θ(n) best case)
- Growth ratios measured n = 16→256: bubble converges to **4.0**, merge to **~2.3**
- Bubble at n = 100: **7,474 frames × 100-element snapshots ≈ 5.7 MB**; delta encoding is ~33× smaller
- Every Final Exam answer-key claim verified: float non-associativity, `len("👋🏽") == 2`, mutable
  default sharing, naive `fib(20) == 21891` calls, `⌊log₂10⁶⌋+1 == 20`, greedy vs lazy regex,
  `"w"` truncation at open, `KeyboardInterrupt` outside `Exception`

---

## Connections

**This week closes:**
- **Week 9's L30** — "regex cannot parse nested structure" became a theorem in Week 11 and an
  engineering consequence in L38 §2 (why compilers layer regex under grammars)
- **Week 10's atomic write** — generalised in L38 §3 to database transactions and write-ahead logs
- **Week 7's aliasing lesson** — reappears in Project 2, where a non-copying snapshot silently
  breaks every frame
- **Week 11's undecidability** — becomes L39 §5's professional skill: reframing "no" as "not that,
  but here is what is possible"

**Forward:** CS 102, CS 210, CS 230, CS 250, CS 301 — mapped in L38.

---

*CS 101 · Week 12 · © CSE Department*

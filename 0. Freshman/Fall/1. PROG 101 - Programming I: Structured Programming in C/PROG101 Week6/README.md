# PROG 101 · Week 6
## Pointers II: Dynamic Memory

---

## This Week

Week 5's pointers all referred to storage that already existed. This week the program *creates*
storage at run time — and takes on the obligation to release it. Every data structure from Week 7
onward depends on this, and so does every memory bug you will spend an evening chasing.

| Day | Session | Topic |
|---|---|---|
| Tue | Lecture 1 | The Process Memory Map and `malloc` |
| Wed | Lecture 2 | `realloc`, `free`, and Ownership |
| Thu | Lecture 3 | Valgrind and the Dynamic Array |
| Mon | Lab 6 | The Heap and a Dynamic Array (2 hrs, BH 215) |

**Quiz 5** at the start of Tuesday's lecture, covering **Week 5**.
**Midterm 1** Thursday 18:00–19:30, VNC 100 — covers **Weeks 0–5**, worth **12%**.
**Problem Set 6** released Friday, due Friday of Week 7.

> **From this week on, every submission must be Valgrind-clean.** Zero errors, zero bytes
> definitely lost. A leak is a defect and is graded as one.

---

## Contents

```
PROG101 Week6/
├── lectures/
│   ├── Lecture 01 The Process Memory Map and malloc.md
│   ├── Lecture 02 realloc free and Ownership.md
│   └── Lecture 03 Valgrind and the Dynamic Array.md
├── assignments/
│   ├── Problem Set 6.md
│   └── MIDTERM 1 Review and Practice Exam.md
├── lab/LAB 6 Heap and Dynamic Array.md
├── quizzes/QUIZ 5.md
├── resources/Week 6 Heap Reference.md
└── solutions_instructor/LAB 6 Solutions.md
```

---

## Learning Objectives

1. Name the regions of a process's address space and what lives in each
2. Use `malloc`, `calloc`, `realloc` and `free` correctly, checking every return
3. Explain why `p = realloc(p, n)` is a bug, and what to write instead
4. State an ownership contract and honour it, including on error paths
5. Read Valgrind's output and act on each category
6. Build a growable container with correct failure handling

---

## Key Facts

| | |
|---|---|
| `malloc` does **not** zero | Verified: 5 of 16 bytes nonzero |
| `calloc` zeroes **and** checks `n × size` | `SIZE_MAX/4+1 × 4` wraps to **exactly 0** |
| `realloc(NULL, n)` | Behaves as `malloc` |
| **Never** `p = realloc(p, n)` | On failure you leak the original and lose your only pointer |
| `free(NULL)` | Guaranteed safe no-op |
| `free(p); p = NULL;` | Turns silent corruption into an immediate fault |
| Doubling growth | Amortised O(1); total copying < 2n, verified to n = 100,000 |
| Pointers dangle after growth | Keep **indices**, not pointers |
| **ASan misses uninitialised reads** | Valgrind catches them — run both |

---

## Connections

**Back:** Week 5's write-back rule explains why `str_release` needs `char **`. Week 3's stack
frames explain why heap allocation exists at all.

**Forward:** Week 7's structures own strings and lists, which is where ownership stops being
theoretical. Week 11's generic containers hand the `destroy` responsibility back to the caller.

---

*PROG 101 · Week 6 · © CSE Department*

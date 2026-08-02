# PROG 101 — Week 11
## The C Standard Library and System Programming Preview

---

## This Week

C has no templates, no generics, and no closures. What it has is `void *` and function pointers —
and this week shows how far that gets you. By Friday you will have built a container that holds any
type, and understood exactly what you gave up to get it.

| Day | Session | Topic |
|---|---|---|
| Tue | Lecture 1 | Function Pointers — Code as Data |
| Wed | Lecture 2 | Generic Programming with `void *` |
| Thu | Lecture 3 | Callbacks and Generic Containers |
| Mon | Lab 11 | Generic Programming in C (2 hrs, BH 215) |

**Quiz 10** at the start of Tuesday's lecture, covering **Week 10**.
**Problem Set 11** released Friday, due Friday of Week 12.

---

## Contents

```
PROG101 Week11/
├── lectures/
│   ├── Lecture 01 Function Pointers.md
│   ├── Lecture 02 Generic Programming with void Pointers.md
│   └── Lecture 03 Callbacks and Generic Containers.md
├── assignments/Problem Set 11.md
├── lab/LAB 11 Generic Programming.md
├── quizzes/QUIZ 10.md
├── resources/Week 11 Generic Programming Reference.md
└── solutions_instructor/LAB 11 Solutions.md
```

---

## Learning Objectives

1. Read and write function-pointer declarations without guessing
2. Build a dispatch table, and say when it beats a `switch`
3. Explain what `void *` guarantees and what it destroys
4. Write comparators correct for **every** input, not just the tested ones
5. Use a context pointer as C's substitute for a closure
6. Reason about ownership in a container that does not know its element type

---

## Key Facts

| | |
|---|---|
| `int *f(int)` vs `int (*p)(int)` | Function returning a pointer vs pointer to function |
| `add` == `&add` | Function names decay, like arrays |
| `sizeof` any function pointer | **8** — but conversion to `void *` is **not** guaranteed |
| `return *a - *b;` in a comparator | **Undefined behaviour**; leaves `{INT_MAX,-2}` unsorted |
| Correct idiom | `(l > r) - (l < r)` — no arithmetic on the values |
| Comparator for `char*` elements | Receives `const char *const *` |
| `qsort` stability | **Not guaranteed** — encode the index if you need it |
| Dispatch table indexing | **Must** be bounds-checked, or it is a wild jump |
| A function pointer captures | **Nothing.** Pass a context pointer |

---

## Connections

**Back:** Week 5's pointers and Week 6's ownership are both prerequisites — a generic container
allocates, copies, and must be told how to destroy. Week 10's macros are the *other* route to
type-genericity, with a different set of costs.

**Forward:** Week 12 uses these patterns in a test framework, and CS 102 replaces them with real
generics.

---

*PROG 101 · Week 11 · © CSE Department*

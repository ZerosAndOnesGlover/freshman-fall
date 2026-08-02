# PROG 101 — Week 5
## Pointers I: The Fundamental Abstraction

---

## This Week

Week 4 showed that arrays decay into something when passed to a function. This week names that
something. A pointer is a variable holding an address — and that one idea underpins write-back,
array traversal, and every data structure from Week 7 onward.

| Day | Session | Topic |
|---|---|---|
| Tue | Lecture 1 | What a Pointer Is |
| Wed | Lecture 2 | Pass-by-Pointer and Pointer Arithmetic |
| Thu | Lecture 3 | NULL, `const`, and the Classic Pointer Errors |
| Mon | Lab 5 | Pointer Mechanics and Write-Back (2 hrs, BH 215) |

**Quiz 4** at the start of Tuesday's lecture, covering **Week 4**.
**Problem Set 5** released Friday, due Friday of Week 6.

> **No `malloc` this week.** Everything operates on storage you already have. The heap is Week 6.

---

## Contents

```
PROG101 Week5/
├── lectures/
│   ├── Lecture 01 What a Pointer Is.md
│   ├── Lecture 02 Pass by Pointer and Arithmetic.md
│   └── Lecture 03 NULL const and Pointer Errors.md
├── assignments/Problem Set 5.md
├── lab/LAB 5 Pointer Mechanics.md
├── quizzes/QUIZ 4.md
├── resources/Week 5 Pointer Reference.md
└── solutions_instructor/LAB 5 Solutions.md
```

---

## Learning Objectives

1. State what a pointer holds and what its type controls
2. Predict how far `p + 1` moves for any pointer type
3. Use pointer parameters to modify a caller's variables
4. Explain why `&a` and `&a[0]` share an address but not a type
5. Choose correctly among the four `const`/pointer combinations
6. Recognise the five classic pointer errors and name the tool that finds each

---

## Key Facts

| | |
|---|---|
| All object pointers | Same **size** (8 bytes), different **behaviour** |
| `p + 1` | **4 / 1 / 8** bytes for `int* / char* / double*` |
| `a + 1` vs `&a + 1` | **+4 vs +40** for `int a[10]` |
| `p2 - p1` | Element **count**, type `ptrdiff_t`, `%td` |
| `a - 1` | **Undefined**, even without dereferencing |
| `const int *p` | Repoint yes, modify no — the one you usually want |
| Returning `&local` | GCC compiles it to **`return NULL`** |
| `%p` without a cast | UB; caught only by **`-pedantic`** |

---

## Connections

**Back:** Week 3's pass-by-value is why write-back needs pointers at all. Week 4's decay is the same
mechanism seen from the array side.

**Forward:** Week 6 adds the heap, where the pointer outlives the function that made it — and
ownership becomes a question you must answer explicitly.

---

*PROG 101 · Week 5 · © CSE Department*

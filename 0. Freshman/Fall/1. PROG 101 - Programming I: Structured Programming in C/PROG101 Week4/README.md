# PROG 101 — Week 4
## Arrays and Strings

---

## This Week

Arrays are C's first data structure: contiguous storage, no bounds checking, and a decay rule that
turns them into pointers the moment they cross a function boundary. Strings are arrays of `char`
with a terminator convention — and the standard library functions for handling them are, in several
cases, actively dangerous.

| Day | Session | Topic |
|---|---|---|
| Tue | Lecture 1 | Arrays — The First Data Structure |
| Wed | Lecture 2 | Strings in Depth — Processing, Searching, Building |
| Thu | Lecture 3 | Buffer Safety and the Bounded String Functions |
| Mon | Lab 4 | Arrays, Strings, and a String Library (2 hrs, BH 215) |

**Quiz 3** at the start of Tuesday's lecture, covering **Week 3**.
**Problem Set 4** released Friday, due Friday of Week 5.

---

## Contents

```
PROG101 Week4/
├── lectures/
│   ├── Lecture 01 Arrays.md
│   ├── Lecture 02 Strings in Depth.md
│   └── Lecture 03 Buffer Safety and Bounded String Functions.md
├── assignments/Problem Set 4.md
├── lab/LAB 4 Arrays Strings Strlib.md
├── quizzes/QUIZ 3.md
├── resources/Week 4 Arrays and Strings Reference.md
└── solutions_instructor/LAB 4 Solutions.md
```

---

## Learning Objectives

By the end of Week 4 you should be able to:

1. Explain array decay and predict when `sizeof` reports the array versus a pointer
2. Distinguish `&a` from `&a[0]` by type, and predict how each behaves under `+1`
3. Implement `strlen`, `strcpy`, `strcmp` and friends from scratch
4. State exactly what `strncpy` does, and why it is not "safe `strcpy`"
5. Use `snprintf` correctly, including its return value, for copying and for sizing
6. Detect truncation — the failure mode the bounded functions introduce

---

## Key Facts

| | |
|---|---|
| `a[i]` | **Defined as** `*(a + i)` — which is why `2[a]` compiles |
| `sizeof a` in `main` vs a function | **40 vs 8** for `int a[10]` |
| `a+1` vs `&a+1` | **+4 bytes vs +40** |
| `strncpy` 10 chars into 8 | **No terminator.** Not a string |
| `strncpy "AB"` into 8 | Writes **all 8 bytes** — O(buffer), not O(strlen) |
| `snprintf` return | The length it **wanted**; `n >= (int)cap` means truncated |
| `strlcpy` | Not standard C, but **in glibc since 2.38** |

---

## Connections

**Back:** Week 3's pass-by-value explains why an array parameter cannot carry its length.
Week 2's evaluation-order rules explain why `a[i] = i++` is undefined.

**Forward:** Week 5 makes the pointer underneath the array explicit. Week 7 builds structures that
own strings, which is where the ownership question first bites.

---

*PROG 101 · Week 4 · © CSE Department*

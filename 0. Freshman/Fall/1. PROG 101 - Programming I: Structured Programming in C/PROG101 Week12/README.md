# PROG 101 · Week 12
## Software Engineering in C: Style, Testing, Debugging

---

## This Week

The last week, and the only one with no new C features. Eleven weeks taught you what the language
does; this week is about what to do with it — how to write code a stranger can change, prove it
works, and find out why when it does not.

| Day | Session | Topic |
|---|---|---|
| Tue 15 Dec | Lecture 1 | Style, Readability, and Structure |
| Wed 16 Dec | Lecture 2 | Testing in C |
| Thu 17 Dec | Lecture 3 | Debugging |
| Mon 21 Dec (Week 13) | Lab 12 | Refactor, Test, Debug (2 hrs, BH 215) |

**Quiz 11** at the start of Tuesday's lecture, covering **Week 11**.
**Problem Set 12** released Friday, due Friday of finals week.
**Final Exam** in finals week — comprehensive, 120 minutes, **20%**.

---

## Contents

```
PROG101 Week12/
├── lectures/
│   ├── Lecture 01 Style and Structure.md
│   ├── Lecture 02 Testing in C.md
│   └── Lecture 03 Debugging.md
├── assignments/
│   ├── Problem Set 12.md
│   └── FINAL EXAM Review.md
├── lab/LAB 12 Refactor Test Debug.md
├── quizzes/QUIZ 11.md
├── resources/Week 12 Engineering Reference.md
└── solutions_instructor/LAB 12 Solutions.md
```

---

## Learning Objectives

1. Justify a style rule by what it does for the reader
2. Organise a C project into modules with deliberate interfaces
3. Build a test framework, and say why it must be a macro
4. Choose test cases by boundary reasoning rather than intuition
5. Read `gcov` output and treat coverage as a diagnostic, not a target
6. Debug systematically, matching tool to symptom
7. Explain why "works at `-O0`, breaks at `-O2`" is a diagnosis

---

## Key Facts

| | |
|---|---|
| The premise | Code is read far more often than it is written |
| Boolean parameters | Usually two functions in disguise |
| `goto cleanup` | Idiomatic C — one exit path, one copy of the cleanup |
| `assert` as a test framework | **Wrong** — disabled by `-DNDEBUG`, silently passing |
| `CHECK` must be a macro | Only a macro sees the caller's `__FILE__`/`__LINE__` and `#cond` |
| `gcov`'s `#####` | Marks never-executed lines — the useful output |
| 100% coverage | Still undefined for `divide(a, 0)` |
| GDB `bt` | Gives the line **and the argument values** — `p=0x0` |
| `watch x` | Stops at the instruction that corrupts a variable |
| `-Wmaybe-uninitialized` | **Silent at `-O0`** — develop at `-O2` |
| `-O0` works, `-O2` breaks | Undefined behaviour, not a compiler bug |
| `-fno-strict-overflow` "fixes" it | That is a **diagnosis** — go remove the UB |

---

## Connections

**Back:** every practice here addresses a bug you have already met — Week 6's error-path leaks,
Week 10's macro traps, Week 2's undefined behaviour. Lecture 2's `CHECK` is Week 10's macro material
put to work.

**Forward:** CS 102 formalises testing and design; CS 210 treats software engineering as a subject in
its own right. The habits start here.

---

*PROG 101 · Week 12 · © CSE Department*

# PROG 101 — Week 10
## The C Preprocessor and Macros

---

## This Week

The preprocessor runs before the compiler sees a single line of your code, and it does not
understand C. Everything it does is textual substitution — which is exactly why macros fail in the
specific ways they do. This week also covers the things macros are genuinely *for*: header guards,
conditional compilation, and the small number of jobs a function cannot do.

| Day | Session | Topic |
|---|---|---|
| Tue | Lecture 1 | The Preprocessor |
| Wed | Lecture 2 | Macros and Their Traps |
| Thu | Lecture 3 | Conditional Compilation and Macro Idioms |
| Mon | Lab 10 | Seeing the Preprocessor (2 hrs, BH 215) |

**Quiz 9** at the start of Tuesday's lecture, covering **Week 9**.
**Midterm 2** Wednesday 18:00–19:30, VNC 100 — covers **Weeks 6–9**, worth **12%**.
**Problem Set 10** released Friday, due Friday of Week 11.

---

## Contents

```
PROG101 Week10/
├── lectures/
│   ├── Lecture 01 The Preprocessor.md
│   ├── Lecture 02 Macros and Their Traps.md
│   └── Lecture 03 Conditional Compilation and Macro Idioms.md
├── assignments/
│   ├── Problem Set 10.md
│   └── MIDTERM 2 Review and Practice Exam.md
├── lab/LAB 10 Preprocessor and Macros.md
├── quizzes/QUIZ 9.md
├── resources/Week 10 Preprocessor Reference.md
└── solutions_instructor/LAB 10 Solutions.md
```

---

## Learning Objectives

1. Describe what the preprocessor does — and what it cannot do
2. Write headers that survive double inclusion and compile standalone
3. Write function-like macros that behave correctly in any context
4. Recognise the four classic macro failures and prevent each
5. Use `#` and `##` deliberately, including the two-level stringify idiom
6. Decide when a macro is right and when a function, `enum` or `const` is better

---

## Key Facts

| | |
|---|---|
| 2-line file including `<stdio.h>` | **815** preprocessed lines |
| `SQUARE_BAD(2+3)` | **11**, not 25 — parameter unparenthesised |
| `100/SQUARE_BAD(5)` | **100**, not 4 — body unparenthesised |
| `MAX(i++, 3)` with `i=5` | Returns 6, leaves `i` at **7** |
| Multi-statement macro in `if`/`else` | `error: 'else' without a previous 'if'` |
| GCC warns | `-Wmultistatement-macros` |
| `STR(VERSION)` vs `XSTR(VERSION)` | `"VERSION"` vs `"42"` |
| `sizeof` in `#if` | **Impossible** — the preprocessor predates types |
| `assert` with a side effect | Vanishes under `-DNDEBUG` |
| `_Static_assert` | Catches table drift at compile time |

---

## Connections

**Back:** Week 0's compilation pipeline named preprocessing as stage one; this week takes it
seriously. Week 3's declaration-versus-definition rule is why a function body in a header fails at
link time.

**Forward:** Week 11's generic containers use macros for type-genericity. Week 12's testing and
debugging material builds directly on Lab 10's `CHECK` framework.

---

*PROG 101 · Week 10 · © CSE Department*

# PROG 101 — Programming I: Structured Programming in C
## Week 12 · Lab 12: Refactor, Test, Debug

**Duration:** 2 hours · **Points:** 20 · **Room:** BH 215

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`

---

## Overview

The last lab. No new C features — instead you take code that works badly and make it good, with the
tools to prove it. This is what most professional programming actually is.

---

## Part 1: Read Before You Change (4 pts)

The starter contains `tally.c`: 120 lines, one function, no comments. It works.

**Before editing anything:**

1. **Run it.** What does it do? Record the observed behaviour in `answers.md`, not your guess.
2. **Find the entry point and read outward.** What are the inputs and outputs?
3. **Identify the data structures first.** What does it operate on, and what does that shape imply?
4. Write a **three-sentence summary** of what the program does.

Only then start Part 2. *(This ordering is the point of the exercise.)*

---

## Part 2: Refactor (6 pts)

1. Split `tally.c` into at least two modules with headers. *(2 pts)*
2. Make everything not in a header `static`. *(1 pt)*
3. Apply the naming rules from Lecture 1 — record three renames and the reason for each. *(1 pt)*
4. Reduce nesting with guard clauses. *(1 pt)*
5. **Verify byte-identical output** on the supplied inputs with `diff`. Paste the command. *(1 pt)*

**If your output differs, you have introduced a bug.** Find it before continuing.

---

## Part 3: Test (5 pts)

1. Implement `check.h` from Lecture 2. *(2 pts)*
2. Write a suite for your refactored modules covering **n = 0, n = 1**, a malformed input, and a
   boundary case of your choosing. *(2 pts)*
3. Add `make test` that fails the build when a check fails. Show a passing and a failing run.
   *(1 pt)*

---

## Part 4: Measure and Debug (5 pts)

### 4A: Coverage

```bash
gcc --coverage -O0 -o test test_tally.c tally.c
./test && gcov tally.c
```

Paste the annotated listing. Identify every `#####` line and either test it or justify it. *(2 pts)*

### 4B: The three bugs

`buggy.c` in the starter has three defects: one crashes, one leaks, one gives a wrong answer without
crashing.

For each, record in `answers.md`: **which tool you reached for first and why**, the tool output, the
root cause, and the fix. *(3 pts)*

> One of the three will not be found by any sanitizer. Recognising *which* — and why — is worth more
> than fixing it.

---

## Deliverables

- The refactored modules with headers, `check.h`, the test suite, the fixed `buggy.c`
- `answers.md` with every recorded observation
- A `Makefile` with `all`, `test`, and `coverage` targets

## Grading

| Component | Points |
|---|---|
| Part 1: read and summarised **before** editing | 4 |
| Part 2: refactored, `static`, byte-identical output | 6 |
| Part 3: framework and suite; `make test` fails correctly | 5 |
| Part 4: coverage analysed; three bugs diagnosed with justified tool choice | 5 |
| **Total** | **20** |

---

*PROG 101 · Week 12 · Lab 12 · © CSE Department*

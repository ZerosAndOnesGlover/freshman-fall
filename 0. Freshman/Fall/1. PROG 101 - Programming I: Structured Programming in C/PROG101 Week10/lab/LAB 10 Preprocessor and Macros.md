# PROG 101 · Programming I: Structured Programming in C
## Week 10 · Lab 10: Seeing the Preprocessor

**Duration:** 2 hours · **Points:** 20 · **Room:** BH 215
**Lab session:** Monday of Week 11 — sat after this week's Tue–Thu lectures, and covers Week 10.

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11`

---

## Overview

The preprocessor is the one stage of the pipeline you can inspect directly. This lab is built around
`gcc -E`: you will look at expansions rather than reasoning about them, break macros deliberately to
see how the failure surfaces, and build a small test framework that could not be written as a
function.

**Rule for the whole lab:** when something surprises you, run `gcc -E -P` on it before asking why.

---

## Part 1: Looking at the Output (5 pts)

### 1A: The size of an include

```c
/* tiny.c */
#include <stdio.h>
int main(void) { printf("hi"); return 0; }
```

```bash
wc -l tiny.c
gcc -E tiny.c | wc -l
gcc -E -P tiny.c | grep -c .
```

**Record in `answers.md`:** the three numbers, and one sentence on what this implies for build times
in a project with hundreds of source files.

### 1B: Macros are text

```c
#define N 10
#define TWICE(x) ((x) + (x))
int a[N];
int b = TWICE(N);
const char *s = "N is not replaced here";
```

Run `gcc -E -P`. **Record:** what happened to `N` inside the string literal, and why.

### 1C: Predefined macros

```bash
gcc -dM -E - < /dev/null | wc -l
gcc -dM -E - < /dev/null | grep -E '__STDC_VERSION__|__GNUC__|__x86_64__'
```

**Record:** how many macros GCC predefines, and the three values.

---

## Part 2: Breaking Macros on Purpose (6 pts)

For each of the following, **predict** the output, then run it, then run `gcc -E -P` and paste the
expansion.

```c
#define SQUARE_BAD(x) x * x
#define SQUARE_OK(x)  ((x) * (x))
#define MAX(a, b)     ((a) > (b) ? (a) : (b))

printf("%d\n", SQUARE_BAD(2 + 3));      /* (a) */
printf("%d\n", 100 / SQUARE_BAD(5));    /* (b) */
printf("%d\n", SQUARE_OK(2 + 3));       /* (c) */

int i = 5;
printf("%d ", MAX(i++, 3));
printf("i = %d\n", i);                  /* (d) */
```

**In `answers.md`:**

1. For (a) and (b), give the expansion and the resulting arithmetic.
2. For (d), state the final value of `i` and name the defect. Explain why parentheses cannot fix it.
3. Write a `max` that does not have (d)'s problem, and say what you gave up.

---

## Part 3: The `if`/`else` Trap (4 pts)

```c
#define LOG_BAD(m) printf("log: %s\n", m); printf("---\n")
#define LOG_OK(m)  do { printf("log: %s\n", m); printf("---\n"); } while (0)

int c = 0;
if (c) LOG_BAD("x"); else printf("else\n");
```

1. Compile it. Paste the error **and** the GCC warning that names the problem. *(2 pts)*
2. Replace with `LOG_OK` and confirm it compiles. *(1 pt)*
3. In `answers.md`, explain why a bare `{ ... }` block does **not** solve it, and why
   `do { } while (0)` does. *(1 pt)*

---

## Part 4: A Framework You Cannot Write as a Function (5 pts)

Build `check.h` with:

```c
CHECK(cond);          /* on failure: file, line, and the CONDITION'S SOURCE TEXT */
int check_report(void);
```

1. Implement it. *(2 pts)*
2. Write `test_check.c` with three passing and two failing checks, and paste the output. *(1 pt)*
3. In `answers.md`, state the **two** things this macro does that a function called
   `check(int cond)` could not, and why. *(2 pts)*

---

## Deliverables

- `tiny.c`, the Part 2 and Part 3 programs, `check.h`, `test_check.c`
- `answers.md` with every recorded number, expansion and explanation
- A `Makefile` building everything with the required flags

## Grading

| Component | Points |
|---|---|
| Part 1: expansion sizes, string-literal behaviour, predefined macros | 5 |
| Part 2: predictions, expansions, and the double-evaluation analysis | 6 |
| Part 3: the error, the warning, and the `do/while` explanation | 4 |
| Part 4: working framework and the two function-impossible capabilities | 5 |
| **Total** | **20** |

---

*PROG 101 · Week 10 · Lab 10 · © CSE Department*

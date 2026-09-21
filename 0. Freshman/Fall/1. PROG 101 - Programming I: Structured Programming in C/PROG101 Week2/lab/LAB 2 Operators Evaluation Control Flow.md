# PROG 101 · Programming I: Structured Programming in C
## Week 2 · Lab 2: Operators, Evaluation Order, and Control Flow

**Graded: 20 points**
**Duration:** 2 hours
**Date:** Monday 12 October 2026 · 15:00–16:50 · Lab Section (Week 3) — covers Week 2 (Lectures 01–03)
**Submission:** Push to Git, show TA before leaving

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`
**Also use:** `-fsanitize=undefined`

---

## Overview

This lab is about the gap between what you *meant* and what C *parsed*. You will make precedence
visible, provoke undefined behaviour and then catch it with tools, and build a small state machine
out of nothing but `switch` and a loop.

**No pointers, no `malloc`, no arrays of structs.** Everything here uses what Week 2 gave you.

---

## Part 1: Precedence and What the Compiler Sees (5 pts)

### 1A: The Parenthesis Gallery

Create `precedence.c`. For each expression, **write down your prediction first**, then run it.

```c
#include <stdio.h>

int main(void) {
    int a = 6, b = 3, c = 2;

    printf("%d\n", a & b == c);      /* 1 */
    printf("%d\n", (a & b) == c);    /* 2 */
    printf("%d\n", 1 << 2 + 3);      /* 3 */
    printf("%d\n", (1 << 2) + 3);    /* 4 */
    printf("%d\n", a + b % c);       /* 5 */
    printf("%d\n", ~5);              /* 6 */
    printf("%d\n", 5 ^ 3);           /* 7 */

    return 0;
}
```

In `answers.md`, for each line record: your prediction, the actual value, and **how C actually
parenthesised it**. *(2 pts)*

### 1B: The Compiler Was Trying to Tell You

Build 1A with `-Wall -Wextra`. Two of those lines produce `-Wparentheses` warnings.

1. Which two, and what exactly does the warning say?
2. Why does the compiler warn about these but not about `a + b % c`, which is equally
   precedence-dependent? *(2 pts)*

### 1C: Integer Division and Remainder

Predict, then verify, all four of `-7 / 2`, `-7 % 2`, `7 / -2`, `7 % -2`.

State the C99+ rule that determines the sign of `%`, and verify that
`(a/b)*b + a%b == a` holds for all four. *(1 pt)*

---

## Part 2: Undefined Behaviour, Caught (5 pts)

Each part is its own file, so one crash does not stop the rest.

### 2A: The Sequence Point Classic

```c
int i = 5;
i = i++;
printf("%d\n", i);
```

Compile with `-Wall -Wextra`. Record the warning verbatim, including which flag produced it.
Then explain what a *sequence point* is and why this line has no defined meaning. *(2 pts)*

### 2B: Signed Overflow

```c
int x = INT_MAX;
printf("%d\n", x + 1);
```

Run it normally, then under `-fsanitize=undefined`. Record both outputs. *(1 pt)*

### 2C: Shifting Too Far

```c
int s = 1;
printf("%d\n", s << 31);
```

Run under `-fsanitize=undefined`. Why is shifting into the sign bit of a **signed** `int` undefined,
and what one-character change makes it well defined? *(1 pt)*

### 2D: Why "It Worked" Proves Nothing

2B and 2C both printed a plausible-looking number *and* were undefined. In three sentences, explain
why testing cannot establish the absence of undefined behaviour, and name the two tools from this
lab that can find it. *(1 pt)*

---

## Part 3: Control Flow (6 pts)

### 3A: Fallthrough, Deliberate and Accidental

```c
for (int n = 1; n <= 5; n++) {
    printf("n=%d: ", n);
    switch (n) {
        case 1: printf("one ");
        case 2: printf("two ");
        case 3: printf("three "); break;
        case 4: printf("four "); break;
        default: printf("other ");
    }
    printf("\n");
}
```

Put this loop in `main` in `fallthrough.c`.

1. Predict the output for `n = 1..5`, then verify. *(1 pt)*
2. Build with `-Wall -Wextra -Werror`. **It will not compile.** Record the error. *(1 pt)*
3. Make it compile *without* changing the output, and explain what you added. *(1 pt)*

### 3B: Loop Tracing by Hand

```c
int x = 27, steps = 0;
while (x != 1) {
    x = (x % 2) ? 3*x + 1 : x / 2;
    steps++;
}
```

Trace the **first eight** iterations by hand in a table (`x` before, condition, `x` after). Then run
it and report the final `steps`. *(2 pts)*

### 3C: `do-while` Is Not `while`

Write a program proving that a `do-while` body runs even when its condition is false on entry, and
state the one situation where that is the behaviour you want. *(1 pt)*

---

## Part 4: A State Machine from `switch` and a Loop (4 pts)

Create `wordcount.c`. Read `stdin` one character at a time with `getchar()` and count **words**,
using an explicit two-state machine — `IN_WORD` and `OUT_OF_WORD` — driven by a `switch`.

A word is any maximal run of non-whitespace characters. Whitespace is space, tab, or newline.

```c
#include <stdio.h>

#define OUT_OF_WORD 0
#define IN_WORD     1

int main(void) {
    int st = OUT_OF_WORD;
    long words = 0, chars = 0, lines = 0;
    int c;

    while ((c = getchar()) != EOF) {
        chars++;
        if (c == '\n') lines++;
        /* your switch on st goes here */
    }

    printf("%ld %ld %ld\n", lines, words, chars);
    return 0;
}
```

**Required tests** — verify each and record the output:

| Input | Expected `lines words chars` |
|---|---|
| `hello world\n` | `1 2 12` |
| `` (empty) | `0 0 0` |
| `   \n` | `1 0 4` |
| `a\n\n\nb\n` | `4 2 6` |

Compare your output with `wc` on the same input. *(4 pts)*

---

## Deliverables

- `precedence.c`, the four Part 2 files, `fallthrough.c`, `collatz.c`, `dowhile.c`, `wordcount.c`
- `answers.md` with every prediction, observation, and written answer
- A `Makefile` building everything with the required flags

## Grading

| Part | Points | Criteria |
|------|--------|----------|
| 1: precedence predicted, verified, warnings explained | 5 | All seven expressions, both warnings identified |
| 2: UB provoked and caught with tools | 5 | All four parts, sanitizer output pasted |
| 3: control flow traced and fallthrough fixed | 6 | Trace table correct, `-Werror` build passes |
| 4: word-count state machine | 4 | All four test cases match `wc` |
| **Total** | **20** | |
| Bonus: extend 4 to count words containing digits | 2 | |

**Automatic deductions:** any compiler warning in code not *deliberately* broken (−2 each).

---

*PROG 101 · Week 2 · Lab 2 · © CSE Department*

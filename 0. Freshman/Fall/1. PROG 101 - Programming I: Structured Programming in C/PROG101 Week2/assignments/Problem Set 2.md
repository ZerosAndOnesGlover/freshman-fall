# PROG 101 · Programming I: Structured Programming in C
## Week 2 · Problem Set 2: Operators, Evaluation Order, and Control Flow

**Released:** Friday 9 October 2026, 10:00 · Week 2 (after Thursday's Lecture 3)
**Due:** Friday 16 October 2026, 17:00 · Week 3 — late penalty from 17:01
**Submission:** Commit to the Freshman Fall repo under `"$PROG101/week2/ps2"`; submit the commit hash on the course portal.
**Total:** 100 points · **Expected time:** about 4 hours

**What this uses:** Weeks 0–2 — `#define` (Week 0), types and conversions (Week 1), and this week's operators
and bit manipulation, evaluation order and undefined behaviour, `if`/`switch`/loops and `getchar`.
**Not needed:** functions of your own (Week 3) — every program is one `main`; `enum` (Week 7).

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11`

---

## Problem 1: Precedence and Parsing (20 pts)

**1.1** *(8)* For each expression, state the value **and** rewrite it fully parenthesised to show how
C parses it. Assume `int a = 6, b = 3, c = 2;`.

(a) `a & b == c` &nbsp; (b) `1 << 2 + 3` &nbsp; (c) `a + b % c` &nbsp; (d) `!a == b`

**1.2** *(6)* `-Wall -Wextra` warns about three of the four above. Which one does it accept silently, and
what is the general rule GCC applies in deciding when a precedence question is worth warning about?

**1.3** *(6)* Evaluate `-7 / 2`, `-7 % 2`, `7 / -2`, `7 % -2`. State the C99 rule for the sign of `%`
and verify the identity `(a/b)*b + a%b == a` in all four cases.

---

## Problem 2: Bit Manipulation (30 pts)

Write `flags.c`: a file-permission set held in one `unsigned int`, all in `main`.

```c
#define PERM_READ  (1u << 0)
#define PERM_WRITE (1u << 1)
#define PERM_EXEC  (1u << 2)
```

**2.1** *(18)* Starting from `unsigned p = 0;`, use one expression each to **set** READ, **set** EXEC,
**clear** READ, and **toggle** WRITE, printing `p` after every step. Then print whether WRITE and READ are
set as **exactly `0` or `1`** (not the masked value), count the set bits with a loop that shifts `p`
right, and print `p` as `rwx`-style letters (`-wx` for 6).

**2.2** *(7)* Expected values after each step: `1, 5, 4, 6`; tests `1` and `0`; count `2`; `-wx`. Show
your output matches.

**2.3** *(5)* Explain why the flags use `1u << n` rather than `1 << n`, referring to Lecture 1's
material on shifting into the sign bit.

---

## Problem 3: Undefined and Unspecified Behaviour (25 pts)

**3.1** *(10)* Classify each as **well defined**, **unspecified**, **implementation-defined**, or
**undefined**, and justify in one sentence:

(a) `i = i++;`
(b) `f() + g();` — which of `f`, `g` runs first
(c) `INT_MAX + 1`
(d) `-1 >> 1`

**3.2** *(7)* Write the shortest program you can that exhibits (a), compile it with `-Wall -Wextra`,
and paste the exact warning including its flag name.

**3.3** *(8)* A colleague argues: "I ran it a thousand times and it always printed 5, so it's fine."
Rebut this in a short paragraph, and name two tools that address what testing alone cannot.

---

## Problem 4: Control Flow (25 pts)

(The `switch` fall-through and the word counter are done in Lab 2, Monday 12 October, so they are not
repeated here.)

**4.1** *(12)* Trace the loop below for `x = 7`, tabulating `x` and `steps` each iteration until it
terminates.

```c
while (x != 1) { x = (x % 2) ? 3*x + 1 : x / 2; steps++; }
```

**4.2** *(13)* Rewrite this `for` loop as an equivalent `while` loop, and explain the one case where
the two are **not** equivalent.

```c
for (int i = 0; i < n; i++) { if (i % 3 == 0) continue; total += i; }
```

---

## Grading

| Problem | Points | Focus |
|---|---|---|
| 1: Precedence and parsing | 20 | Reading C as the compiler reads it |
| 2: Bit manipulation | 30 | Masks, flags, unsigned discipline |
| 3: Undefined behaviour | 25 | The four categories, and why testing is not proof |
| 4: Control flow | 25 | Loop tracing, `for`/`while` equivalence |
| **Total** | **100** | |

**Automatic deductions:** any compiler warning (−3 each); any UBSan report in code not deliberately
broken (−5 each).

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Every program was built with gcc 13.3 (`-Wall -Wextra -std=c11`) and run.

### Problem 1

(a) `a & (b == c)` = `6 & 0` = **0** (b) `1 << (2 + 3)` = **32** (c) `a + (b % c)` = **7** (d) `(!a) == b` =
`0 == 3` = **0**. GCC warns on (a) and (b) with `-Wparentheses` ("suggest parentheses around comparison in
operand of '&'", "…around '+' inside '<<'") and on (d) with `-Wlogical-not-parentheses`. It is silent on (c):
it warns only where the familiar-looking reading is **not** the real one, and `%` binding tighter than `+`
matches ordinary arithmetic. 1.3: `-7/2 = -3`, `-7%2 = -1`, `7/-2 = -3`, `7%-2 = 1` — division truncates toward
zero, so `%` takes the sign of the dividend; e.g. `(-3)*2 + (-1) = -7` ✓.

### Problem 2

```c
/* flags.c — PS 2 Problem 2 (reference) */
#include <stdio.h>

#define PERM_READ  (1u << 0)
#define PERM_WRITE (1u << 1)
#define PERM_EXEC  (1u << 2)

int main(void) {
    unsigned p = 0;

    p = p | PERM_READ;                       /* set   */
    printf("set READ     -> %u\n", p);
    p = p | PERM_EXEC;
    printf("set EXEC     -> %u\n", p);
    p = p & ~PERM_READ;                      /* clear */
    printf("clear READ   -> %u\n", p);
    p = p ^ PERM_WRITE;                      /* toggle */
    printf("toggle WRITE -> %u\n", p);
    printf("test WRITE   -> %d\n", (p & PERM_WRITE) != 0);   /* exactly 0 or 1 */
    printf("test READ    -> %d\n", (p & PERM_READ) != 0);

    int count = 0;                           /* count bits set */
    for (unsigned rest = p; rest != 0; rest = rest >> 1) {
        count += rest & 1u;
    }
    printf("bits set     -> %d\n", count);

    printf("as rwx       -> %c%c%c\n",
           (p & PERM_READ)  ? 'r' : '-',
           (p & PERM_WRITE) ? 'w' : '-',
           (p & PERM_EXEC)  ? 'x' : '-');
    return 0;
}
```

Output: `1, 5, 4, 6`, `test WRITE -> 1`, `test READ -> 0`, `bits set -> 2`, `-wx`. Builds clean under
`-Werror -pedantic`. 2.3: `1 << 31` shifts into the sign bit of a signed `int` — undefined behaviour;
`1u << 31` is an unsigned shift, fully defined. *(18 / 7 / 5)*

### Problem 3

(a) **undefined** — two unsequenced modifications of `i` (gcc: `warning: operation on 'i' may be undefined
[-Wsequence-point]`). (b) **unspecified** — either order is allowed and need not be documented.
(c) **undefined** — signed overflow. (d) **implementation-defined** — right-shifting a negative value (gcc:
arithmetic shift, −1). 3.3: repeated runs sample one compiler, one flag set, one machine; UB can change with
any of them. Tools: `-fsanitize=undefined` (UBSan), `-Wall -Wextra`, Valgrind.

### Problem 4

4.1 for `x = 7`: `22 11 34 17 52 26 13 40 20 10 5 16 8 4 2 1` — **16 steps**. 4.2: `int i = 0;
while (i < n) { if (i % 3 == 0) { i++; continue; } total += i; i++; }` — the `continue` must not skip the
increment, which is the one case where a naive rewrite is **not** equivalent (it loops forever).


---

*PROG 101 · Week 2 · Problem Set 2 · Due Friday 16 October 2026, 17:00 · © CSE Department*

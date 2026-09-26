# PROG 101 · Problem Set 2 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

*(Revised 2026-09-26: old Problem 1, 3.2, 3.3 and 4.1 are no longer on the set — Lab 2 works them. Old 2 → 1
(25/10/10), old 3.1 → 2 (6/6/6/7), old 4.2 → 3 (20 rewrite, 10 non-equivalence).)*

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

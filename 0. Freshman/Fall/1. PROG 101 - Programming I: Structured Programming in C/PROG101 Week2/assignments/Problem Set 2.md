# PROG 101 · Programming I: Structured Programming in C
## Week 2 · Problem Set 2: Operators, Evaluation Order, and Control Flow

**Released:** Friday, Week 2 · **Due:** Friday, Week 3 at 17:00
**Total:** 100 points

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11`

---

## Problem 1: Precedence and Parsing (20 pts)

**1.1** *(8)* For each expression, state the value **and** rewrite it fully parenthesised to show how
C parses it. Assume `int a = 6, b = 3, c = 2;`.

(a) `a & b == c` &nbsp; (b) `1 << 2 + 3` &nbsp; (c) `a + b % c` &nbsp; (d) `!a == b`

**1.2** *(6)* `-Wall -Wextra` warns about two of the four above. Which two, and what is the general
rule GCC applies in deciding when a precedence question is worth warning about?

**1.3** *(6)* Evaluate `-7 / 2`, `-7 % 2`, `7 / -2`, `7 % -2`. State the C99 rule for the sign of `%`
and verify the identity `(a/b)*b + a%b == a` in all four cases.

---

## Problem 2: Bit Manipulation (25 pts)

Write `flags.c` implementing a file-permission set using a single `unsigned int`.

```c
enum {
    PERM_READ  = 1u << 0,
    PERM_WRITE = 1u << 1,
    PERM_EXEC  = 1u << 2
};

unsigned perm_set   (unsigned p, unsigned flag);   /* turn flag on            */
unsigned perm_clear (unsigned p, unsigned flag);   /* turn flag off           */
unsigned perm_toggle(unsigned p, unsigned flag);   /* flip flag               */
int      perm_test  (unsigned p, unsigned flag);   /* 1 if set, 0 otherwise   */
int      perm_count (unsigned p);                  /* number of bits set      */
void     perm_print (unsigned p);                  /* prints e.g. "rwx"/"r-x" */
```

**2.1** *(15)* Implement all six. `perm_test` must return exactly `0` or `1` — not the masked value.

**2.2** *(6)* Write a `main` demonstrating each function, printing the numeric value after every
operation.

**2.3** *(4)* Explain why the flags use `1u << n` rather than `1 << n`, referring to Lecture 2's
material on shifting into the sign bit.

---

## Problem 3: Undefined and Unspecified Behaviour (20 pts)

**3.1** *(8)* Classify each as **well defined**, **unspecified**, **implementation-defined**, or
**undefined**, and justify in one sentence:

(a) `i = i++;`
(b) `f() + g();` — which of `f`, `g` runs first
(c) `INT_MAX + 1`
(d) `-1 >> 1`

**3.2** *(6)* Write the shortest program you can that exhibits (a), compile it with `-Wall -Wextra`,
and paste the exact warning including its flag name.

**3.3** *(6)* A colleague argues: "I ran it a thousand times and it always printed 5, so it's fine."
Rebut this in a short paragraph, and name two tools that address what testing alone cannot.

---

## Problem 4: Control Flow (20 pts)

**4.1** *(8)* Given this function, state the output for `n = 1, 2, 3, 4, 5`:

```c
switch (n) {
    case 1: printf("one ");
    case 2: printf("two ");
    case 3: printf("three "); break;
    case 4: printf("four "); break;
    default: printf("other ");
}
```

Then state what `-Wall -Wextra -Werror` does to this code and how to keep the behaviour while
satisfying the compiler.

**4.2** *(6)* Trace the loop below for `x = 7`, tabulating `x` and `steps` each iteration until it
terminates.

```c
while (x != 1) { x = (x % 2) ? 3*x + 1 : x / 2; steps++; }
```

**4.3** *(6)* Rewrite this `for` loop as an equivalent `while` loop, and explain the one case where
the two are **not** equivalent.

```c
for (int i = 0; i < n; i++) { if (i % 3 == 0) continue; total += i; }
```

---

## Problem 5: A Character-Driven State Machine (15 pts)

Write `wordcount.c` that reads `stdin` with `getchar()` and prints `lines words chars`, matching
`wc`. Use an explicit two-state machine driven by a `switch`.

**5.1** *(10)* Implementation.

**5.2** *(5)* Test against `wc` on at least these inputs, tabulating both results:

| Input |
|---|
| `hello world\n` |
| empty input |
| `   \n` |
| `a\n\n\nb\n` |
| a source file of your choice |

---

## Grading

| Problem | Points | Focus |
|---|---|---|
| 1: Precedence and parsing | 20 | Reading C as the compiler reads it |
| 2: Bit manipulation | 25 | Masks, flags, unsigned discipline |
| 3: Undefined behaviour | 20 | The four categories, and why testing is not proof |
| 4: Control flow | 20 | `switch` semantics, loop tracing, equivalence |
| 5: State machine | 15 | Structured iteration over a character stream |
| **Total** | **100** | |

**Automatic deductions:** any compiler warning (−3 each); any UBSan report in code not deliberately
broken (−5 each).

---

*PROG 101 · Week 2 · Problem Set 2 · © CSE Department*

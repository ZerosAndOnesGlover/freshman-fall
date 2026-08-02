# PROG 101 · Programming I: Structured Programming in C
## Week 3 · Lab 3: Functions, the Call Stack, and Multi-File Programs

**Graded: 20 points**
**Duration:** 2 hours
**Submission:** Push to Git, show TA before leaving

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`
**Inspect with:** `gdb`

---

## Overview

You will make the call stack visible, prove pass-by-value by address, split a program across
translation units with a proper header, and meet the first bug that pointers make possible.

**No `malloc` and no pointer arithmetic.** Pointers arrive in Week 5; the only pointer here is the
one in Part 4, and it exists to show you why Week 5 is necessary.

---

## Part 1: Making the Call Stack Visible (5 pts)

### 1A: Frames Have Addresses

Create `stack.c`:

```c
#include <stdio.h>

static void level3(void) { int c = 3; printf("  level3  &c = %p\n", (void*)&c); }
static void level2(void) { int b = 2; printf(" level2   &b = %p\n", (void*)&b); level3(); }
static void level1(void) { int a = 1; printf("level1    &a = %p\n", (void*)&a); level2(); }

int main(void) {
    int m = 0;
    printf("main      &m = %p\n", (void*)&m);
    level1();
    return 0;
}
```

Run it and record the four addresses. In `answers.md`:

1. Do the addresses increase or decrease as the calls nest? *(1 pt)*
2. Compute the difference between consecutive frames. Is it constant? What is stored in that space
   besides the local variable? *(1 pt)*
3. Run the program twice. Do you get the same addresses? Explain what you observe. *(1 pt)*

### 1B: The Same Picture in GDB

Set a breakpoint in `level3`, run, and capture:

```
(gdb) break level3
(gdb) run
(gdb) backtrace
(gdb) info frame
(gdb) frame 1
(gdb) info locals
```

Paste the `backtrace` output and explain how each line corresponds to one of the addresses from 1A.
*(2 pts)*

---

## Part 2: Pass-by-Value and Storage Duration (5 pts)

### 2A: Pass-by-Value, Proved by Address

```c
#include <stdio.h>

static void try_modify(int x) {
    printf("  inside: &x=%p x=%d -> ", (void*)&x, x);
    x = 999;
    printf("%d\n", x);
}

int main(void) {
    int v = 42;
    printf("before: &v=%p v=%d\n", (void*)&v, v);
    try_modify(v);
    printf("after : &v=%p v=%d\n", (void*)&v, v);
    return 0;
}
```

Record the output. The argument was modified inside the function and `v` was not. Explain **using the
two addresses** — not using the phrase "pass by value", which is the thing being demonstrated. *(2 pts)*

### 2B: `static` Changes the Lifetime, Not the Scope

```c
static int counter(void)   { static int n = 0; return ++n; }
static int automatic(void) {        int n = 0; return ++n; }
```

Call each four times in a loop and tabulate the results. *(1 pt)*

Then answer: `n` is invisible outside its function in **both** cases. What exactly did `static`
change, and where does each `n` live? *(2 pts)*

---

## Part 3: A Multi-File Library (6 pts)

Split a small numeric library across translation units.

**`mathutil.h`** — the interface, with an include guard:

```c
#ifndef MATHUTIL_H
#define MATHUTIL_H

int  gcd(int a, int b);
long factorial(int n);
int  is_prime(int n);

#endif
```

**`mathutil.c`** — the implementation. It must contain one **file-private** helper:

```c
static int abs_int(int x) { return x < 0 ? -x : x; }
```

**`main.c`** — includes only `mathutil.h` and exercises all three functions.

**3A.** *(3 pts)* Implement and build as **separate compilation units**:

```
gcc -Wall -Wextra -Werror -pedantic -std=c11 -c mathutil.c -o mathutil.o
gcc -Wall -Wextra -Werror -pedantic -std=c11 -c main.c     -o main.o
gcc mathutil.o main.o -o prog
```

Required outputs to verify:

| Call | Expected |
|---|---|
| `gcd(48,18)`, `gcd(-48,18)`, `gcd(17,5)`, `gcd(0,7)` | `6 6 1 7` |
| `factorial(0..12)` | `1 1 2 6 24 120 720 5040 40320 362880 3628800 39916800 479001600` |
| primes below 30 | `2 3 5 7 11 13 17 19 23 29` |

**3B.** *(2 pts)* Write `bad.c` that declares `int abs_int(int x);` itself and calls it. Compile and
link it against `mathutil.o`. **Record the exact error.** At which stage — preprocessing,
compilation, assembly, or linking — does it fail, and why did compilation succeed?

**3C.** *(1 pt)* Write a `Makefile` that rebuilds only what changed. Demonstrate it: touch
`mathutil.h`, run `make`, and show what got recompiled.

---

## Part 4: Contracts and the First Dangling Pointer (4 pts)

**4A.** *(2 pts)* Add `assert(n >= 0)` to `factorial`. Show it firing for `factorial(-1)`, and record
the message. Then rebuild with `-DNDEBUG` and show the assertion is gone. State one thing assertions
should **never** be used for.

**4B.** *(2 pts)* Two versions of the same bug. Create `dangling.c`:

```c
/* version 1 — direct */
static int *make(void) { int x = 42; return &x; }

/* version 2 — one function further away */
static int *identity(int *p)  { return p; }
static int *make2(void) { int x = 42; return identity(&x); }
```

1. Compile version 1 **with no warning flags at all**. Record what GCC says. Which flag produced it,
   and what does it tell you that this diagnostic is on by default?
2. Now compile version 2 with the full `-Wall -Wextra -pedantic`. Record the result — it is not what
   you would hope.
3. Build version 2 with `-fsanitize=address`, dereference the returned pointer, and paste the report.
   Name the error class ASan prints.
4. Explain, in terms of your frame diagram from Part 1, why both returned addresses are worthless —
   and why the compiler could catch one but not the other.

---

## Deliverables

- `stack.c`, `pbv.c`, `duration.c`, `mathutil.{h,c}`, `main.c`, `bad.c`, `dangling.c`
- `Makefile`
- `answers.md` with all recorded output, the GDB transcript, and every written answer

## Grading

| Part | Points | Criteria |
|------|--------|----------|
| 1: call stack observed and explained | 5 | Addresses recorded, GDB backtrace matched to frames |
| 2: pass-by-value and storage duration | 5 | Explanation is address-based; `static` correctly characterised |
| 3: multi-file library | 6 | Separate compilation, all outputs match, linker error explained |
| 4: contracts and dangling pointer | 4 | Assertion demonstrated both ways; frame-based explanation |
| **Total** | **20** | |
| Bonus: add `lcm` using `gcd` without overflowing for inputs near `INT_MAX` | 2 | |

**Automatic deductions:** any compiler warning in code not *deliberately* broken (−2 each).

---

*PROG 101 · Week 3 · Lab 3 · © CSE Department*

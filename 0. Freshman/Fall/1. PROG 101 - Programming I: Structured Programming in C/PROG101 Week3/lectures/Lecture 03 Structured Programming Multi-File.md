# PROG 101 · Programming I: Structured Programming in C
## Week 3 · Lecture 3: Functions and Structured Programming

**Date:** Thursday 10 September 2026 · 10:00–10:50 · Week 3

---

## Lecture Goals

By the end of this lecture you will:
- Understand structured programming as a mathematical result, not a style choice
- Write multi-file C programs with proper header discipline
- Use function pointers to pass behavior as data
- Understand `inline`, `static`, and `extern` function qualifiers
- Design functions correct by construction using pre/postconditions

---

## 1. Structured Programming: The Theorem Behind the Practice

In 1966, Böhm and Jacopini proved that **any computable algorithm can be expressed with exactly three control structures:** sequence, selection, iteration. This is a theorem — not a preference. `goto` is never necessary. Any program using it can be rewritten without it.

C still has `goto`. One legitimate use: breaking out of deeply nested loops. In all other cases, reaching for `goto` signals a function design problem.

---

## 2. Multi-File Programs and Header Discipline

```c
/* math_utils.h — declarations only */
#ifndef MATH_UTILS_H
#define MATH_UTILS_H

long factorial(int n);
int  is_prime(long n);
void sieve_primes(long arr[], int n);

#endif /* MATH_UTILS_H */
```

```c
/* math_utils.c — definitions */
#include "math_utils.h"   /* own header first — ensures it compiles standalone */
#include <assert.h>

long factorial(int n) {
    assert(n >= 0);
    long result = 1;
    for (int i = 2; i <= n; i++) result *= i;
    return result;
}

int is_prime(long n) {
    if (n <= 1) return 0;
    if (n <= 3) return 1;
    if (n % 2 == 0 || n % 3 == 0) return 0;
    for (long i = 5; i * i <= n; i += 6)
        if (n % i == 0 || n % (i+2) == 0) return 0;
    return 1;
}
```

```c
/* main.c */
#include <stdio.h>
#include "math_utils.h"

int main(void) {
    printf("10! = %ld\n", factorial(10));
    printf("97 prime? %d\n", is_prime(97));
    return 0;
}
```

**The include guard** (`#ifndef / #define / #endif`) prevents double-inclusion: if `a.h` includes `b.h` and `main.c` includes both, without guards `b.h` is processed twice — duplicate declarations cause errors.

**The rule:** Always include your own header first in its `.c` file. This ensures the header compiles standalone — any missing `#include` inside it is caught immediately.

---

## 3. `static` Functions: File-Private Linkage

`static` on a function restricts it to the current translation unit. The linker cannot see it; other files cannot call it:

```c
/* utils.c */

/* Private — only callable within this file */
static int clamp(int x, int lo, int hi) {
    if (x < lo) return lo;
    if (x > hi) return hi;
    return x;
}

/* Public — visible to other files */
int normalize_score(int raw) {
    return clamp(raw, 0, 100);
}
```

Use `static` on every helper function that is an implementation detail. Benefits:
- No naming conflicts with identically-named functions in other files
- Signals to readers the function is internal
- Allows the compiler to inline it aggressively (no external callers)

---

## 4. Function Pointers — Moved to Week 11

Function pointers are the mechanism C uses in place of closures, and they carry enough weight to
deserve their own treatment. They are covered in **Week 11, Lecture 1**, alongside `qsort`,
generic containers, and the callback patterns built on them.

For this lecture it is enough to know that they exist and that they are what makes a *dispatch
table* possible — replacing a long `switch` with an array you index. That is a structured-
programming idea, which is why it is mentioned here; the machinery arrives in Week 11.

## 5. `extern` and `inline` — The Other Two Qualifiers

`static` (§3) restricts a name to one translation unit. The other two qualifiers go the opposite direction, or sideways.

### `extern` — "defined somewhere else"

`extern` declares that a name exists without defining it. It creates no storage; it promises the linker will find the definition in another translation unit.

```c
/* globals.c — the ONE definition */
int shared_counter = 41;

/* main.c — a declaration, not a definition */
#include <stdio.h>
extern int shared_counter;          /* no storage allocated here */

int main(void) {
    shared_counter++;
    printf("%d\n", shared_counter);  /* 42 */
    return 0;
}
```

The rule is **one definition, many declarations**. Put the `extern` declaration in a header and the definition in exactly one `.c` file. Defining the variable in the header instead gives you one copy per including file, and the linker reports a duplicate-symbol error.

Function declarations are implicitly `extern`, which is why `long factorial(int);` in a header needs no keyword — writing `extern` there is legal but redundant.

Note the symmetry with §3: `static` at file scope means *internal* linkage (invisible to other files), `extern` means *external* linkage (visible to all). They are opposites.

> **Prefer passing state as parameters.** Shared mutable globals defeat the encapsulation §3 was arguing for. `extern` is essential for constants, lookup tables, and genuinely program-wide state — but reach for a parameter first.

### `inline` — a hint, with a linkage catch

`inline` suggests the compiler substitute the function's body at the call site instead of emitting a call. It is only a *hint*: modern compilers inline aggressively based on their own analysis and routinely ignore it. Its real use today is enabling a function to be **defined in a header** without violating the one-definition rule.

That is where the trap lives. In C (unlike C++), a plain `inline` definition provides **no external definition**. If the compiler chooses not to inline a call — which is exactly what happens at `-O0` — the linker has nothing to call:

```c
/* hdr.h */
inline int square(int x) { return x * x; }
```

```
$ gcc -std=c11 -O0 main.c -o main
main.c:(.text+0xe): undefined reference to `square'
```

The fix is to give exactly one translation unit an `extern` declaration, which forces that TU to emit the callable copy:

```c
/* square.c — exactly one file does this */
#include "hdr.h"
extern int square(int x);      /* emits the external definition */
```

Now it links at every optimisation level. This build-succeeds-at-`-O2`-but-fails-at-`-O0` behaviour is one of C's most confusing failure modes, and it is pure linkage — nothing to do with performance.

**Practical advice for this course:** use `static inline` in headers. It sidesteps the whole problem by giving each translation unit its own private copy, which is what you almost always want for small helpers.

---

## 6. Assertions and Defensive Programming

```c
#include <assert.h>

double divide(double a, double b) {
    assert(b != 0.0);   /* aborts with message if false */
    return a / b;
}

int binary_search(const int arr[], int n, int target) {
    assert(arr != NULL);
    assert(n >= 0);
    /* ... */
}
```

`assert` compiles to nothing in release builds (`-DNDEBUG`) — zero runtime cost in production. Use it for every precondition during development.

**The philosophy:** A violated assertion means your mental model of the code was wrong. It fires at the source, not 500 lines later when a corrupted value finally causes a crash. Assertions turn silent corruption into loud, located failures.

---

## 7. Preconditions, Postconditions, and Loop Invariants

```c
/*
 * insertion_sort — sort arr[0..n-1] in ascending order
 *
 * Precondition:  arr != NULL, n >= 0
 * Postcondition: arr[0] <= arr[1] <= ... <= arr[n-1]
 *                The multiset of values is unchanged
 */
void insertion_sort(int arr[], int n) {
    /* INVARIANT: arr[0..i-1] is sorted at the top of each iteration */
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j+1] = arr[j];
            j--;
        }
        arr[j+1] = key;
        /* INVARIANT maintained: arr[0..i] is now sorted */
    }
    /* i == n → arr[0..n-1] is sorted */
}
```

Writing the invariant forces you to think about *why* the loop works, not just *that* it works. It is the difference between believing code is correct and being able to prove it.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Read each declaration aloud using the right-left rule, and say what it is.

```c
int *f(int);
int (*g)(int);
int (*h[4])(int);
int *(*k)(int *, int *);
```

**2. (Explain.)** This comparator has a bug that a sorted-output test will not catch. Identify it and give the correct version.

```c
int cmp(const void *a, const void *b) {
    return *(const int *)a - *(const int *)b;
}
```

**3. (Build.)** Build a dispatch table mapping operator characters to functions, and use it to write a two-operand calculator. Explain why this beats a `switch` as the operation count grows.

**4. (Stretch.)** Explain what `static` means on a function and on a file-scope variable, and why the two meanings are related. Then explain the C99 `inline` trap.


### Answers

**1.** - `int *f(int);` — **f is a function** taking `int`, returning `int *`. (Start at `f`, go right: `(int)` means function; then left: `*` means returns pointer to `int`.)
- `int (*g)(int);` — **g is a pointer to a function** taking `int` and returning `int`. The parentheses around `*g` bind the `*` to `g` before the `()` can apply, which is the entire difference from the first line.
- `int (*h[4])(int);` — **h is an array of 4 pointers to functions** taking `int`, returning `int`. Go right from `h`: `[4]` — array. Then left: `*` — of pointers. Then out: `(int)` returning `int`. This is a dispatch table.
- `int *(*k)(int *, int *);` — **k is a pointer to a function** taking two `int *`, returning `int *`. This is the shape of a `qsort`-style callback.

**The right-left rule:** start at the identifier, move right as far as you can, then left, obeying parentheses. `[]` and `()` bind tighter than `*`, which is why the parentheses around `*g` are load-bearing.

Use `typedef` to escape all of it: `typedef int (*IntFn)(int);` turns the third into `IntFn h[4];`. `cdecl` will translate any of these for you, and reaching for it is not cheating.

**2.** **Signed overflow.** When the difference exceeds `INT_MAX`, the subtraction overflows — which is undefined behaviour, and typically wraps to the wrong sign. Test it directly:

```c
int x = INT_MIN, y = 1;
cmp(&x, &y);   /* returns +2147483647 — claims INT_MIN > 1 */
```

The correct answer is negative; it returns the largest possible positive value.

The reason a sorted-output test misses it is that the bug needs operands more than `INT_MAX` apart, which requires values at the extremes of the range. Ordinary test data — small positive integers — never triggers it, and even a deliberately extreme array may sort correctly by luck depending on which pairs `qsort` happens to compare. **Test the comparator directly, not the sorted output.**

```c
int cmp(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}
```

This yields exactly −1, 0, or +1 with no arithmetic on the values, so nothing can overflow. It is also branchless.

The `const void *` parameters are `qsort`'s contract: type erasure lets one sort routine handle any element type, at the cost of the comparator having to cast — and of the compiler being unable to check that the cast matches what you actually passed.

**3.**

```c
#include <stdio.h>

typedef int (*BinOp)(int, int);

static int op_add(int a, int b) { return a + b; }
static int op_sub(int a, int b) { return a - b; }
static int op_mul(int a, int b) { return a * b; }

static const struct { char sym; BinOp fn; } TABLE[] = {
    { '+', op_add },
    { '-', op_sub },
    { '*', op_mul },
};

BinOp lookup(char sym) {
    for (size_t i = 0; i < sizeof TABLE / sizeof TABLE[0]; i++)
        if (TABLE[i].sym == sym) return TABLE[i].fn;
    return NULL;
}

int main(void) {
    BinOp f = lookup('*');
    if (!f) { fprintf(stderr, "unknown operator\n"); return 1; }
    printf("%d\n", f(6, 7));   /* 42 */
    return 0;
}
```

Against a `switch`, the table wins on **extensibility**: adding an operation is one line of *data*, in one place, and the dispatch code never changes. A `switch` must be edited every time, and in a real program the same switch tends to get duplicated — one for dispatch, one for printing names, one for precedence — which then drift apart. A table can carry all three as extra fields in the struct, keeping them adjacent and impossible to forget.

The table can also be built at **runtime**, which a `switch` cannot: plugin registration and `atexit`-style handler lists work exactly this way.

**Always check for `NULL` before calling.** Calling through a null function pointer is undefined behaviour and usually segfaults with a useless backtrace. Division would need a zero check too — which is a good reason for the struct to carry a validation function per entry.

**4.** On a **function**, `static` means **internal linkage**: the name is visible only within its translation unit. It does not appear in the object file's global symbol table (`nm` shows lowercase `t` rather than `T`), so another `.c` file cannot call it and two files may each define a `static helper()` without colliding. It also lets the compiler inline or delete it freely, since it can see every call site.

On a **file-scope variable** it means the same thing — internal linkage. (On a *local* variable inside a function, `static` means something different: static **storage duration**, so the variable persists across calls. Same keyword, two concepts, which is a genuine wart in C's design.)

The connection is that `static` is C's only encapsulation mechanism: it is the `private` keyword. A well-structured `.c` file declares everything not in its header as `static`.

**The `inline` trap.** In C99, `inline` alone on a function definition provides an *inline definition* only — it explicitly does **not** provide an external definition. If the compiler chooses not to inline a call, the linker needs one and reports `undefined reference`. Worse, it typically appears only at `-O0`, so the code builds at `-O2` and fails in a debug build.

The fix is to pick one:

- **`static inline`** in a header — one copy per translation unit, no linkage issues. This is what you want almost always.
- `inline` in the header **plus** `extern inline` in exactly one `.c` file, which emits the external definition.

Note `inline` is a *hint*; the compiler inlines on its own cost model regardless, and `-O2` inlines plenty of functions never marked with it.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Böhm-Jacopini** | Theorem: sequence + selection + iteration suffice for any algorithm |
| **Include guard** | `#ifndef/#define/#endif` — prevents double-processing a header |
| **Static linkage** | `static` on a function: visible only within the current `.c` file (internal linkage) |
| **External linkage** | `extern`: name is defined in another translation unit; one definition, many declarations |
| **`inline`** | Hint to substitute the body at the call site; in C it provides **no** external definition on its own |
| **Function pointer** | Variable holding the address of a function; lets behavior be passed as data |
| **Right-left rule** | Method for decoding a declarator: start at the identifier, alternate right and left, obey parentheses |
| **Function-to-pointer decay** | A function name in an expression converts automatically to a pointer to it — no `&` needed |
| **Type erasure** | Discarding static type information (`void *`) so one routine serves every element type, as `qsort` does |
| **Comparator** | Function returning negative / zero / positive to order two elements; magnitude is not part of the contract |
| **Dispatch table** | Array of function pointers indexed by a key; adding behavior means adding data, not editing logic |
| **`assert`** | Aborts if condition is false; documents and enforces invariants |
| **Precondition** | What must be true at function entry |
| **Postcondition** | What will be true at function exit |

---

*Next: Lecture 2 — Pointers I: The Fundamental Abstraction*

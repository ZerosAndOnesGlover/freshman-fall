---
assessment: Quiz 3
course: PROG 101
component: Quizzes
possible: 20
score: 20
status: graded
started: 2026-10-22
submitted: 2026-10-22
graded: 2026-10-22
source: "QUIZ 3.md"
---

# PROG 101 · Quiz 3
## Answer Sheet

**Assessment:** `QUIZ 3.md` (covers Week 3: functions and pass-by-value, the call stack, scope and
storage duration, multi-file programs and linkage, assertions)
**Points available:** 20 (10 questions × 2)

All code outputs verified by compiling and running with `gcc -std=c11 -Wall -Wextra`.

---

## Section A — Multiple Choice

### Question 1  (2 pts)

**`int f(void);` declared and called but never defined — which stage fails?**

**Answer: (D) The linker.** The call type-checks against the declaration, so preprocessing, compilation
and assembly all succeed; the object file simply records an external reference. `ld` then reports
`undefined reference to 'f'` when it cannot resolve that symbol.

*Marks: 2 / 2*

### Question 2  (2 pts)

**`int *get_answer(void) { int x = 42; return &x; }` — what is wrong?**

**Answer: (B)** `x` has automatic storage duration; its frame is reclaimed when the function returns, so
the returned address is **dangling** — it points at memory that is no longer reserved for `x`. Returning
a pointer is fine in general (A is false), `&x` already has type `int *` (C is false), and the code is
not valid to use (D is false).

*Marks: 2 / 2*

### Question 3  (2 pts)

**A `static` variable declared inside a function:**

**Answer: (B)** It has static storage duration — created once, initialised once, and alive for the whole
run — but **block scope**, so its name is visible only inside that function. It is not re-created per
call (A), it has no linkage and so cannot be named `extern` elsewhere (C), and it need not be `const`
(D).

*Marks: 2 / 2*

### Question 4  (2 pts)

**A function declared `static` at file level in `util.c`:**

**Answer: (B)** File-scope `static` gives the function **internal linkage**: it is callable only from
within `util.c`. Including `util.h` does not export it (A); `static` on a function says nothing about
local-variable lifetime (C); and it is not a request to inline (D).

*Marks: 2 / 2*

### Question 5  (2 pts)

**What does an include guard prevent?**

**Answer: (B)** It stops the same header's contents from being processed twice **in one translation
unit** (for example, when two other headers both include it). It has nothing to do with linking object
files (A), name collisions across files (C), or declaration-before-use (D).

*Marks: 2 / 2*

---

## Section B — Short Answer

### Question 6  (2 pts)

```c
int g = 1;
void bump(int x) { x = x + 10; g = g + 10; }
int main(void) { int a = 1; bump(a); printf("%d %d\n", a, g); return 0; }
```

**Output: `1 11`**

**Why:** C is pass-by-value. The parameter `x` is a **copy** of `a` in `bump`'s frame, so `x = x + 10`
changes only the copy and `a` stays `1`. `g` is a single object at file scope; the assignment
`g = g + 10` changes that one object, so it becomes `11`.

*Marks: 2 / 2*

### Question 7  (2 pts)

```c
int next(void) { static int n = 5; n = n + 1; return n; }
/* in main: */ next(); next(); printf("%d\n", next());
```

**Output: `8`**

`n` is initialised **once**, at program start (static storage duration), not on each call. The calls
take `n` through `6`, `7`, `8`, so the third call prints `8`.

*Marks: 2 / 2*

### Question 8  (2 pts)

```c
int x = 3;
{ int x = 7; x = x + 1; }
printf("%d\n", x);
```

**Output: `3`**   **Rule: block scope (the inner `x` shadows the outer one).**

The braces create a new block. The declaration inside declares a *different* object named `x`, local to
that block; `x = x + 1` updates the inner object to `8`, and the inner object ceases to exist at the
closing brace. The outer `x` was never touched.

*Marks: 2 / 2*

### Question 9  (2 pts)

At the moment the **inner** `twice` is running in `printf("%d\n", twice(twice(3)));` (with
`int twice(int v) { return 2 * v; }`):

```
┌──────────────────┐
│ twice  v = 3     │  ← newest (inner call)
├──────────────────┤
│ main             │
└──────────────────┘
```

**Output: `12`**

Only **two** frames are on the stack: `main` and the inner `twice` with `v = 3`. The outer call has not
started yet — C must finish evaluating the inner call to obtain its argument before it can call `twice`
again. The inner call returns `6`, and the outer call then computes `2 * 6 = 12`.

*Marks: 2 / 2*

### Question 10  (2 pts)

**Assert:** `n >= 0` in `long factorial(int n)` — a negative argument is a **programmer error** (callers
are not supposed to pass one), so an assertion documents the contract and catches the bug in development.

**Wrong tool:** validating **untrusted input** — user input or a file that might be malformed. That is
not a bug in the code but a condition the program must handle at runtime, and it must still be handled in
release builds, where assertions have been removed.

**`-DNDEBUG`:** it defines the `NDEBUG` macro, which makes `<assert.h>` compile every `assert` out — the
expressions are not evaluated and no check or message remains.

*Marks: 2 / 2*

---

## Grading Summary

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-10-22 |

**Feedback:**
Full marks. All five multiple-choice answers are correct and correctly reasoned: the linker for the
missing definition, the dangling pointer from a returned local address, `static` local as static
duration with block scope, file-scope `static` as internal linkage, and the include guard as
per-translation-unit protection. Short answers are all right and verified by running the code:
`1 11` with pass-by-value versus file scope explained, `8` from one-time static initialisation, `3` with
shadowing named, the two-frame stack diagram with the argument-evaluation ordering and output `12`, and
the assertion answer correctly separates programmer error from untrusted input and explains `-DNDEBUG`.

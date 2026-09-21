# PROG 101 · Quiz 3
## Week 4, Tuesday — In-Class Assessment

**Date:** Tuesday 20 October 2026 · 10:00–10:10 (start of Week 4, Lecture 1)
**Covers:** Week 3 material — functions and pass-by-value, the call stack, scope and storage duration,
multi-file programs and linkage, assertions
**Duration:** 10 minutes · Closed book · 20 points

> Rewritten 2026-09-21. The previous version tested `*p++`, `malloc`/`free`, Valgrind, `qsort`
> comparators and pointer swaps — Weeks 5, 6 and 11 — at the start of Week 4.

---

## Section A — Multiple Choice (2 pts each)

**1.** A program declares `int f(void);`, calls `f()`, and never defines `f`. Which stage fails?

- (A) The preprocessor
- (B) The compiler
- (C) The assembler
- (D) The linker

---

**2.** What is wrong with this function?

```c
int *get_answer(void) {
    int x = 42;
    return &x;
}
```

- (A) You cannot return a pointer from a function
- (B) `x` is destroyed when the function returns — the returned address is dangling
- (C) `&x` requires a cast to `int *` before returning
- (D) Nothing — this is valid C

---

**3.** A `static` variable declared **inside** a function:

- (A) is re-created and re-initialised on every call
- (B) exists for the whole run and is initialised once, but can only be named inside that function
- (C) can be used from any file that declares it `extern`
- (D) must be `const`

---

**4.** A function declared `static` at **file level** in `util.c`:

- (A) can be called from any file that includes `util.h`
- (B) can only be called from inside `util.c`
- (C) keeps its local variables between calls
- (D) is inlined by the compiler

---

**5.** What does an include guard (`#ifndef UTIL_H` / `#define UTIL_H` / `#endif`) prevent?

- (A) Linking the same object file twice
- (B) The same header's contents being processed twice in one translation unit
- (C) Two functions with the same name in different files
- (D) Calling a function before it is defined

---

## Section B — Short Answer (2 pts each)

**6.** What does this print, and why can `bump` change `g` but not `a`?

```c
int g = 1;
void bump(int x) { x = x + 10; g = g + 10; }

int main(void) {
    int a = 1;
    bump(a);
    printf("%d %d\n", a, g);
    return 0;
}
```

```
Output: ______   Why: ________________________________________________________
```

---

**7.** What does the third call print?

```c
int next(void) { static int n = 5; n = n + 1; return n; }
/* in main: */  next(); next(); printf("%d\n", next());
```

```
Output: ______
```

---

**8.** What does this print? Name the rule.

```c
int x = 3;
{ int x = 7; x = x + 1; }
printf("%d\n", x);
```

```
Output: ______   Rule: _______________________________________
```

---

**9.** Draw the call stack (newest frame on top) at the moment the **inner** `twice` is running in
`printf("%d\n", twice(twice(3)));`, and give the output.

```
┌──────────────┐
│              │  ← newest
├──────────────┤
│              │
└──────────────┘
Output: ______
```

---

**10.** Give one precondition of `long factorial(int n)` that should be an `assert`, and one situation where
an `assert` would be the **wrong** tool. What does compiling with `-DNDEBUG` do?

```
Assert: ______________________________________________________________
Wrong tool: __________________________________________________________
-DNDEBUG: ____________________________________________________________
```

---

## Answer Key (Instructor Copy)

Code answers checked by compiling and running (gcc 13.3, no warnings).

**1. (D)** — the call compiles against the declaration; `ld` reports `undefined reference to 'f'`.

**2. (B)** — Week 3 Lecture 02 §2: the frame is reused after return, so the address points at garbage.

**3. (B)** — static storage duration, block scope.

**4. (B)** — internal linkage.

**5. (B)** — the guard stops a second `#include` of the same header within one `.c` file; it does nothing
across files.

**6.** `1 11` — `x` is a copy of `a` in `bump`'s frame (pass-by-value); `g` is one object at file scope.

**7.** `8` — `n` goes 6, 7, 8 across the three calls; it is initialised once.

**8.** `3` — the inner `x` is a different object that **shadows** the outer one inside the braces (block scope).

**9.** Top: `twice` (v = 3); below it `main`. The outer call has not started yet — its argument is still
being evaluated. Output `12`.

**10.** Assert `n >= 0` (a programmer error to call it with a negative). Wrong tool: validating user input or
a file that might be malformed — that must be handled in release builds too. `-DNDEBUG` removes every `assert`.

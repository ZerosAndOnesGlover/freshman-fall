# PROG 101 · Programming I: Structured Programming in C
## Week 3 · Lecture 1: Functions and Pass-by-Value

**Date:** Tuesday 13 October 2026 · 10:00–10:50 · Week 3

---

## Lecture Goals

By the end of this lecture you will:
- Understand what a function *is* at the machine level — not just syntax
- Know the difference between parameters and arguments
- Understand scope rules precisely: local, global, static local, `extern`
- Visualize the call stack as a concrete data structure
- Understand pass-by-value and why it matters
- Know what a stack frame contains and how it grows/shrinks

---

## 1. Why Functions Exist

Functions serve two purposes that are inseparable from good engineering:

**1. Abstraction** — Hide complexity behind a name. A function caller doesn't need to know *how* `sqrt()` works; they only need to know *what* it does. This is the interface-implementation separation that scales software.

**2. Reuse** — Write once, call many times. Without functions, every place you need to compute a square root would contain the same 20 lines of code. A bug fix would need to be applied in 40 places. Functions are the unit of reuse.

There is a third, often forgotten purpose:

**3. Testability** — A well-designed function does exactly one thing and can be tested in isolation. Code that is not decomposed into functions cannot be unit-tested.

---

## 2. Function Anatomy

```c
return_type function_name(parameter_type param1, parameter_type param2) {
    /* body */
    return value;   /* must match return_type */
}
```

Every part has a precise meaning:

```c
/*
 * celsius_to_fahrenheit — convert a temperature
 *
 * Parameters:
 *   celsius: the temperature to convert
 *
 * Returns:
 *   the equivalent Fahrenheit temperature
 *
 * Pre-condition:  celsius >= -273.15 (absolute zero)
 * Post-condition: return value == celsius * 9/5 + 32
 */
double celsius_to_fahrenheit(double celsius) {
    return (celsius * 9.0 / 5.0) + 32.0;
}
```

**The function comment is not optional.** It is the contract between the function and its callers. Write it before you write the body — it forces you to think about what the function should do before deciding how.

---

## 3. Declaration vs. Definition (Revisited, Precisely)

You saw this in Week 0. Now let's be precise about the rules:

```c
/* DECLARATION (prototype) — tells the compiler:
 *   "a function named X exists, takes these types, returns this type"
 *   No code is generated. No memory is allocated.
 */
double celsius_to_fahrenheit(double celsius);
double celsius_to_fahrenheit(double);      /* parameter name optional */

/* DEFINITION — the actual function body.
 *   Code IS generated. The function has an address.
 *   A definition also serves as a declaration.
 */
double celsius_to_fahrenheit(double celsius) {
    return (celsius * 9.0 / 5.0) + 32.0;
}
```

**Rules:**
- A function must be **declared** before any call to it (so the compiler knows the types)
- A function must be **defined** exactly **once** across all translation units (object files)
- A declaration may appear any number of times (as long as they agree)

The typical pattern in multi-file C programs:
- Declarations go in `.h` header files
- Definitions go in `.c` source files
- `main.c` `#include`s the headers to get the declarations

---

## 4. Parameters vs. Arguments

These two words are often confused. They have distinct meanings:

| Term | When | Example |
|------|------|---------|
| **Parameter** | In the function definition — the variable name | `double celsius` |
| **Argument** | At the call site — the actual value passed | `celsius_to_fahrenheit(100.0)` |

```c
double celsius_to_fahrenheit(double celsius) { ... }
/*                           ^^^^^^^^^^^^^^
 *                           PARAMETER: the variable that receives the value */

double f = celsius_to_fahrenheit(100.0);
/*                               ^^^^^
 *                               ARGUMENT: the value passed to the function */
```

---

## 5. Pass by Value — The Most Important Rule in C

**In C, all function arguments are passed by value.**

This means: the function receives a **copy** of the argument. Modifying the parameter inside the function has **no effect** on the original variable at the call site.

```c
void try_to_modify(int x) {
    x = 999;    /* Modifies the LOCAL COPY only */
    printf("Inside: x = %d\n", x);   /* Prints 999 */
}

int main(void) {
    int a = 42;
    try_to_modify(a);
    printf("Outside: a = %d\n", a);  /* Still 42 — not 999 */
    return 0;
}
```

This is not a limitation — it is a feature. It means a function cannot accidentally corrupt its caller's variables. The function's effects are confined to:
1. Its return value
2. Any global variables it reads/writes
3. Any variables accessed via **pointers** passed to it (covered in Week 5)

**This is why `scanf` requires `&x`**: scanf needs to *write* to your variable, so it needs its address, not a copy.

---

> **Where the call stack went.** How a call is actually implemented — stack frames, the
> return address, why locals vanish on return — and the full scope rules are **Lecture 2**.
> This lecture is about the interface: what a function is, and how arguments get in and
> results get out.

## 6. Return Values and `void`

```c
/* Returns a value */
int square(int x) {
    return x * x;
}

/* Returns nothing */
void print_square(int x) {
    printf("%d² = %d\n", x, x * x);
    /* No return statement needed; or: return; */
}

/* Multiple return points */
int max(int a, int b) {
    if (a > b) return a;
    return b;
}

/* Returning a status code — idiomatic C pattern */
int read_positive(int *out) {
    int x;
    if (scanf("%d", &x) != 1) return -1;   /* error */
    if (x <= 0) return -2;                  /* invalid value */
    *out = x;
    return 0;                               /* success */
}
```

**The idiomatic C return convention:**
- Return `0` for success
- Return a negative integer or error code for failure
- Use output parameters (pointers) for values that must be returned on success

This is exactly how POSIX system calls work: `open()` returns a file descriptor (≥ 0) on success, -1 on error.

---

## 7. Function Design Principles

A function should:

**1. Do exactly one thing.** If you need the word "and" to describe what a function does, it should probably be two functions.

**2. Fit on one screen.** If you can't see the entire function at once, it is too long. (Rule of thumb: 20–30 lines maximum.)

**3. Have a clear precondition.** What must be true when the function is called?

**4. Have a clear postcondition.** What will be true when the function returns?

**5. Have meaningful parameters.** A function with more than 4–5 parameters usually has a design problem.

```c
/* BAD: does too many things, unclear parameters */
int do_stuff(int a, int b, int c, int d, int e, int *out1, int *out2) { ... }

/* GOOD: one thing, clear parameters */
double calculate_bmi(double weight_kg, double height_m) {
    return weight_kg / (height_m * height_m);
}
```

---

## 8. Recursive Functions (Preview)

A function can call itself — this is **recursion**. The call stack makes this work naturally: each recursive call gets its own stack frame with its own local variables.

```c
int factorial(int n) {
    if (n <= 1) return 1;          /* base case: stop recursion */
    return n * factorial(n - 1);   /* recursive case: call ourselves */
}
```

Call stack for `factorial(4)`:

```
factorial(4)  → 4 * factorial(3)
  factorial(3) → 3 * factorial(2)
    factorial(2) → 2 * factorial(1)
      factorial(1) → returns 1   ← base case
    factorial(2) → 2 * 1 = 2   ← returns 2
  factorial(3) → 3 * 2 = 6     ← returns 6
factorial(4) → 4 * 6 = 24       ← returns 24
```

We study recursion in depth in Week 9. For now: recognize the pattern, and know that the call stack is what makes it work — each frame stores the state needed to resume when the recursive call returns.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict the output and explain why the function cannot do what its name suggests.

```c
#include <stdio.h>
void swap(int a, int b) {
    int t = a; a = b; b = t;
}
int main(void) {
    int x = 1, y = 2;
    swap(x, y);
    printf("%d %d\n", x, y);
    return 0;
}
```

**2. (Explain.)** This function returns a pointer to a local. Explain precisely what is wrong, why it often appears to work, and give two correct alternatives.

```c
char *make_greeting(void) {
    char buf[64];
    snprintf(buf, sizeof buf, "Hello");
    return buf;
}
```

**3. (Build.)** Write a function that returns *two* values — the quotient and remainder of a division — given that C functions return only one. Show two approaches and say which you would use.

**4. (Stretch.)** Explain what a stack frame contains and why infinite recursion produces a segmentation fault rather than an error message. Estimate the recursion depth at which a simple function will crash.


### Answers

**1.** It prints **`1 2`** — unchanged.

C is **pass by value, always, with no exceptions.** `swap` receives *copies* of `x` and `y` in its own stack frame. It swaps the copies perfectly, and then the frame is destroyed on return, taking both copies with it. `main`'s variables were never reachable.

The fix is to pass the **addresses**, so the function has something that refers back to the caller's storage:

```c
void swap(int *a, int *b) {
    int t = *a; *a = *b; *b = t;
}
/* called as: */ swap(&x, &y);
```

This is still pass by value — the *pointers* are copied — but the copies point at the originals, so dereferencing reaches `main`'s memory. That distinction matters: reassigning the pointer itself (`a = &something_else`) inside the function still has no effect on the caller, which is why changing where a caller's pointer points requires a `int **`.

Everything C does that looks like pass-by-reference — arrays, output parameters, `scanf("%d", &age)` — is this same mechanism. Week 3 makes it the central topic.

**2.** `buf` lives in `make_greeting`'s **stack frame**, which is deallocated the moment the function returns. The returned pointer is *dangling*: it points at memory that is no longer reserved. Using it is **undefined behaviour**. GCC warns with `-Wreturn-local-addr`.

It often *appears* to work because deallocation does not erase anything — the stack pointer simply moves back, and the bytes sit there untouched until the next call reuses that region. So a `printf` immediately after may print `Hello` correctly, and the same code corrupts silently once another function is called in between. That intermittency is what makes the bug expensive: it survives testing and fails in production.

**Alternative 1 — caller supplies the buffer** (the C standard-library convention):

```c
void make_greeting(char *out, size_t n) {
    snprintf(out, n, "Hello");
}
```

Ownership stays with the caller, nothing is allocated, and there is nothing to free. Prefer this.

**Alternative 2 — allocate on the heap:**

```c
char *make_greeting(void) {
    char *buf = malloc(64);
    if (buf) snprintf(buf, 64, "Hello");
    return buf;   /* caller must free */
}
```

Heap memory outlives the frame, but now the **ownership contract must be documented** — every such function needs a comment saying the caller frees, or you have traded a dangling pointer for a leak. Week 3 Lecture 3 covers this.

**3.** **Approach 1 — output parameters:**

```c
int divmod(int a, int b, int *rem) {
    *rem = a % b;
    return a / b;
}
/* int r; int q = divmod(17, 5, &r);   -> q=3, r=2 */
```

**Approach 2 — return a struct:**

```c
typedef struct { int quot, rem; } DivResult;

DivResult divmod(int a, int b) {
    DivResult res = { a / b, a % b };
    return res;
}
/* DivResult d = divmod(17, 5);   -> d.quot=3, d.rem=2 */
```

**Prefer the struct.** It cannot be called wrongly: there is no address to pass, no uninitialised variable if the caller forgets, and no chance of passing the same pointer twice. The fields are *named*, so `d.rem` is self-documenting where a bare `&r` at a call site is not. And returning a small struct is not slow — two `int`s are returned in registers, exactly like two scalars.

The standard library provides precisely this as `div_t div(int, int)` in `<stdlib.h>`.

Output parameters still earn their place when the return value is reserved for an **error code** — the dominant C convention, as in `if (parse(s, &value) != 0) { ... }`. That is the real reason they are so common: C has no exceptions, so the return slot is spoken for.

**4.** A **stack frame** holds one function call's: parameters, local variables, the **return address** (where to resume in the caller), the saved frame pointer, and any registers the callee must preserve. It is pushed on call and popped on return, which is why locals vanish and why recursion works at all — each call gets its own frame.

Infinite recursion never returns, so frames accumulate. The stack is a **fixed-size region** (typically 8 MB on Linux; check with `ulimit -s`). When the stack pointer runs past its end, the next write touches an unmapped guard page and the MMU raises a fault, which the kernel delivers as **SIGSEGV**. There is no friendly message because nothing in the C runtime is checking depth — the hardware notices, not the language. This is exactly the difference from Python, whose interpreter counts frames and raises `RecursionError` at 1000.

**Estimate:** a frame for a function with a couple of `int` locals is roughly 32–48 bytes after alignment. With 8 MB of stack that is on the order of 200,000 frames. Add a `char buf[1024]` local and the frame exceeds 1 KB, dropping the limit to about 8,000 — which is why large stack arrays plus recursion is a dangerous combination.

Two caveats when measuring: `-O2` may turn a tail call into a jump, making the loop genuinely infinite instead of crashing, and `-fsanitize=address` reports a clean *stack-overflow* diagnostic rather than a bare segfault.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Function** | A named, reusable block of code that takes parameters and returns a value |
| **Parameter** | A variable in the function definition that receives an argument's value |
| **Argument** | The actual value passed to a function at the call site |
| **Pass by value** | C's default: functions receive copies of arguments |
| **Call stack** | The region of memory that stores stack frames for active function calls |
| **Stack frame** | Memory region holding one function call's locals, parameters, and return address |
| **Return address** | The instruction address where execution resumes after a function returns |
| **Stack overflow** | Exhausting the stack by pushing too many frames |
| **Scope** | The region of code where a name is visible |
| **Block scope** | Visible only within the enclosing `{ }` block |
| **File scope** | Visible throughout the `.c` file (global) |
| **Static local** | Local variable with static lifetime — persists between calls |
| **`extern`** | Declaration that a variable/function is defined in another translation unit |
| **Prototype** | A function declaration that specifies the function's signature |

---

## Reading

- **K&R Chapter 4** — Functions and Program Structure (entire chapter)
- **King Ch. 9** — Functions
- **CS:APP §3.7** — Procedures (stack frames in x86-64 assembly — optional but illuminating)

---

*Next: Lecture 2 — Arrays: The First Data Structure*

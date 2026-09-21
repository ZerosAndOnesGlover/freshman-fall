# PROG 101 · Programming I: Structured Programming in C
## Week 10 · Lecture 2: Macros and Their Traps

**Date:** Wednesday 2 December 2026 · 10:00–10:50 · Week 10

---

## Lecture Goals

By the end of this lecture you can:

- Write object-like and function-like macros that behave correctly in any context
- Predict the four classic macro failures and prevent each one
- Use `#` and `##` deliberately, including the two-level stringify idiom
- Decide when a macro is the right tool and when a function or `enum` is better

---

## 1. Object-like Macros

```c
#define BUFFER_SIZE 1024
#define PI          3.14159265358979
#define PROGRAM     "prog101"
```

The preprocessor replaces every subsequent occurrence of the name with the replacement tokens. That
is the whole mechanism.

**No semicolon.** A macro definition ends at the newline (Lecture 1), so:

```c
#define SIZE 100;          /* the semicolon is PART OF THE MACRO */
int a[SIZE];               /* expands to: int a[100;];  -- syntax error */
```

The error appears at the *use*, not the definition, which is what makes it confusing.

### Prefer `const` or `enum` for constants

```c
#define  MAX 100           /* preprocessor: no type, invisible to the debugger */
const int MAX = 100;       /* a real, typed object                            */
enum    { MAX = 100 };     /* a real, typed integer constant                  */
```

Macros are the weakest of the three:

- **No type.** The compiler cannot check anything about a macro.
- **No scope.** A macro is in force from its `#define` to the end of the file, ignoring blocks and
  functions entirely.
- **Invisible in the debugger.** GDB sees `100`, not `MAX` — unless you compile with `-g3`.
- **They collide.** A macro named `MAX` breaks anyone else's `MAX`, including in headers you did not
  write.

Use `enum` for integer constants and `const` for others. Reserve macros for things the compiler
genuinely cannot express — which is Lecture 3's subject.

---

## 2. Function-like Macros and the Parenthesis Rules

```c
#define SQUARE(x) x * x        /* broken */
```

Two failures, both verified.

**Failure 1 — the argument is not parenthesised:**

```
SQUARE_BAD(2+3) = 11
```

Expected 25. The expansion is `2+3 * 2+3`, which is `2 + 6 + 3 = 11`. The argument is pasted in as
*text*, so the surrounding `*` binds tighter than the `+` inside it.

**Failure 2 — the whole body is not parenthesised:**

```
100/SQUARE_BAD(5) = 100
```

Expected 4. The expansion is `100/5 * 5`, which is `20 * 5 = 100`. The division grabbed only the
first factor.

### The rule

**Parenthesise every parameter, and the entire body.**

```c
#define SQUARE(x) ((x) * (x))
```

Verified: `SQUARE_OK(2+3)` is 25, and `100/SQUARE_OK(5)` is 4.

Both sets of parentheses are load-bearing and they fix different bugs. Omitting either one produces a
macro that works on simple arguments and fails on compound ones — which is why the bug survives
testing.

---

## 3. Double Evaluation

Parentheses cannot fix this one.

```c
#define MAX(a, b) ((a) > (b) ? (a) : (b))

int i = 5;
int m = MAX(i++, 3);
```

`a` appears **twice** in the body, so `i++` is evaluated twice. Verified:

```
MAX(i++, 3) with i=5 -> 6, i is now 7   <- incremented TWICE
```

The result is 6 and `i` ends at 7. A function would have given 5 and 6.

**Any macro that uses a parameter more than once has this problem**, and the arguments that trigger
it are exactly the ones with side effects: `i++`, `f()`, `*p++`, `read_next()`.

Three mitigations:

1. **Use a function.** `static inline int max_int(int a, int b)` evaluates each argument once, is
   type-checked, and modern compilers inline it. This is the right answer whenever the types are
   known.
2. **Document it loudly.** If a macro must double-evaluate, say so: `/* NOTE: evaluates a and b
   twice; do not pass expressions with side effects */`.
3. **Use GCC statement expressions** — non-standard, but they solve it properly:
   ```c
   #define MAX(a, b) ({ __typeof__(a) _a = (a); __typeof__(b) _b = (b); _a > _b ? _a : _b; })
   ```
   Each argument is evaluated once into a temporary. This is a GNU extension, so it is not portable.

**By default: write a function.** The genuine reasons to prefer a macro are type-genericity and
needing `__FILE__`/`__LINE__` from the call site — Lecture 3 covers both.

---

## 4. The Multi-Statement Trap

```c
#define LOG(m) printf("log: %s\n", m); printf("---\n")
```

Looks harmless. Now:

```c
if (verbose) LOG("hi");
else         printf("quiet\n");
```

expands to:

```c
if (verbose) printf("log: %s\n", "hi"); printf("---\n");
else         printf("quiet\n");         /* ERROR: else without a matching if */
```

The first statement belongs to the `if`; the second is unconditional; the `else` is then orphaned.

**GCC catches this specific shape.** Verified:

```
warning: macro expands to multiple statements [-Wmultistatement-macros]
```

### The `do { } while (0)` idiom

```c
#define LOG(m) do { printf("log: %s\n", m); printf("---\n"); } while (0)
```

Verified: this compiles and behaves correctly inside an unbraced `if`/`else`.

**Why this specific wrapper?**

- A bare `{ ... }` block would work in the `if` but leaves a stray `;` after it, which again breaks
  `else`.
- `do { ... } while (0)` is a single statement that **requires** a trailing semicolon, so
  `LOG("hi");` reads naturally and behaves like a function call everywhere.
- The loop runs exactly once and every compiler optimises it away completely.

Use `do { } while (0)` for **any** function-like macro whose body is more than one statement. It is a
formula, not a judgement call.

---

## 5. `#` and `##`

Two operators available only inside macro bodies.

### `#` — stringify

Converts a parameter into a string literal:

```c
#define STR(x) #x
STR(hello)        /* becomes "hello" */
STR(a + b)        /* becomes "a + b" */
```

The catch: **`#` does not expand its argument first.** Verified:

```
STR(VERSION)  = "VERSION"     <- not expanded
XSTR(VERSION) = "42"          <- expanded first
```

To stringify a macro's *value* you need two levels:

```c
#define STR(x)  #x
#define XSTR(x) STR(x)
#define VERSION 42

XSTR(VERSION)     /* "42"      -- VERSION expands, then STR stringifies */
STR(VERSION)      /* "VERSION" -- STR sees the token, not its value     */
```

This is genuinely surprising and worth remembering as a pair. The reason is that arguments are macro-
expanded before substitution *except* where they are operands of `#` or `##`.

### `##` — token pasting

Joins two tokens into one:

```c
#define CAT(a, b) a##b
int CAT(my, var) = 7;      /* declares int myvar = 7; */
```

Verified: the variable `myvar` exists and holds 7.

Token pasting is used to generate families of names — `CHECK_int`, `CHECK_double` — and appears in
generic-programming tricks and X-macros (Lecture 3). It is powerful and it makes code hard to grep
for, which is a real maintenance cost: a reader searching for `myvar` will not find the line that
creates it.

**Use `##` sparingly, and comment it when you do.**

---

## 6. When to Use a Macro

| Use a macro | Use something else |
|---|---|
| You need `__FILE__` / `__LINE__` from the **call site** | Ordinary logic → function |
| Type-generic code across several types | Known types → `static inline` function |
| Conditional compilation (Lecture 3) | Integer constants → `enum` |
| Header guards | Typed constants → `const` |
| Compile-time configuration | Anything the compiler can check → let it |

**The default answer is "not a macro."** A `static inline` function in a header gives you inlining,
type checking, single evaluation, debugger visibility, and scope. Macros exist for the cases where
the compiler genuinely cannot do the job.

The two honest cases you will meet this course:

```c
/* 1. needs the CALL SITE's file and line -- a function cannot see them */
#define CHECK(cond) \
    do { if (!(cond)) fprintf(stderr, "%s:%d: check failed: %s\n", \
                              __FILE__, __LINE__, #cond); } while (0)

/* 2. type-generic -- one macro serves int, double, char... */
#define SWAP(T, a, b) do { T _t = (a); (a) = (b); (b) = _t; } while (0)
```

Note the first uses `#cond` to print the condition's *text*, which no function can do.

---

## 7. Summary

| Idea | Takeaway |
|---|---|
| No semicolon in a `#define` | `#define SIZE 100;` breaks at the **use** |
| Prefer `enum` / `const` | Macros have no type, no scope, and are invisible to the debugger |
| Parenthesise **parameters** | `SQUARE_BAD(2+3)` = **11**, not 25 |
| Parenthesise the **whole body** | `100/SQUARE_BAD(5)` = **100**, not 4 |
| Both are needed | They fix different bugs |
| Double evaluation | `MAX(i++, 3)` incremented `i` **twice** — verified |
| Fix by writing a function | `static inline` evaluates once and is type-checked |
| Multi-statement macros | Break `if`/`else`; GCC warns `-Wmultistatement-macros` |
| `do { } while (0)` | The formula for any multi-statement macro |
| `#x` stringifies | But does **not** expand — `STR(VERSION)` is `"VERSION"` |
| Two-level idiom | `XSTR(VERSION)` gives `"42"` |
| `a##b` pastes tokens | Powerful; makes code ungreppable — comment it |
| Default answer | **Not a macro.** Use one only when the compiler cannot do the job |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** With `#define HALF(x) x / 2`, give the value of each and say why:
(a) `HALF(10)`  (b) `HALF(6 + 4)`  (c) `4 * HALF(10)`  (d) `HALF(10) * 4`

**2. (Explain.)** `#define ABS(x) ((x) < 0 ? -(x) : (x))` is fully parenthesised and still has a bug.
Identify it and give an input that triggers it.

**3. (Fix.)** Four bugs.

```c
#define MAX_SIZE 100;
#define AREA(w, h) w * h
#define SWAP(a, b) int t = a; a = b; b = t
#define IS_EVEN(n) n % 2 == 0
```

**4. (Stretch.)** Write a `CHECK(cond)` macro that, when `cond` is false, prints the file, line, and
the **source text** of the condition, then returns −1 from the enclosing function. Explain the two
things it does that a function cannot, and one serious objection to macros that hide a `return`.

### Answers

**1.** `HALF(x)` expands to `x / 2` with no parentheses anywhere.

| | Expansion | Value | Why |
|---|---|---|---|
| **(a)** `HALF(10)` | `10 / 2` | **5** | Correct by luck — a simple argument |
| **(b)** `HALF(6 + 4)` | `6 + 4 / 2` | **8** | `/` binds tighter than `+`: 6 + 2. Expected 5 |
| **(c)** `4 * HALF(10)` | `4 * 10 / 2` | **20** | Correct by luck — left-to-right gives 40/2 |
| **(d)** `HALF(10) * 4` | `10 / 2 * 4` | **20** | Correct by luck again |

(b) is the only wrong one here, and that is the lesson: three of four cases work, so a test suite
built from simple arguments passes. Change `HALF` to `((x) / 2)` and all four are right.

**2.** The bug is **double evaluation** — `x` appears twice in the body.

```c
int i = -5;
int a = ABS(i++);
```

`i++` is evaluated once by the comparison `(i) < 0` and again by whichever branch is taken, so `i`
advances twice and the result is not the absolute value of anything the caller intended.

Parentheses cannot fix this; the parameter is used twice by construction. The fix is a function:

```c
static inline int abs_int(int x) { return x < 0 ? -x : x; }
```

*A second, subtler bug worth mentioning:* `-(x)` on `INT_MIN` is undefined behaviour, because
`-INT_MIN` is not representable (Week 1). `abs(INT_MIN)` has the same defect, which is why the
standard explicitly says its behaviour is undefined in that case.

**3.**

- **`#define MAX_SIZE 100;`** — the trailing semicolon becomes part of the macro. `int a[MAX_SIZE];`
  expands to `int a[100;];`. → drop the semicolon.
- **`#define AREA(w, h) w * h`** — no parentheses. `AREA(2+3, 4)` gives `2 + 3*4 = 14`, not 20; and
  `10/AREA(2,5)` gives `10/2*5 = 25`, not 1. → `((w) * (h))`.
- **`#define SWAP(a, b) int t = a; a = b; b = t`** — three problems at once: it is multi-statement
  (breaks `if`/`else`), it declares `t` in the caller's scope (which collides if the caller already
  has a `t`, and leaks a declaration), and the parameters are unparenthesised. → wrap in
  `do { } while (0)`, name the temporary something unlikely such as `_swap_tmp`, and parenthesise.
- **`#define IS_EVEN(n) n % 2 == 0`** — unparenthesised, so `IS_EVEN(4+1)` is `4 + 1%2 == 0`, which
  is `4 + 1 == 0` → false, when the intent was to test 5. Also `x % 2 == 0` is the correct evenness
  test for negatives (unlike `== 1` for oddness — Week 1), so only the parentheses need fixing.

```c
#define MAX_SIZE 100
#define AREA(w, h)   ((w) * (h))
#define IS_EVEN(n)   ((n) % 2 == 0)
#define SWAP(T, a, b) do { T _swap_tmp = (a); (a) = (b); (b) = _swap_tmp; } while (0)
```

**4.**

```c
#define CHECK(cond)                                                  \
    do {                                                             \
        if (!(cond)) {                                               \
            fprintf(stderr, "%s:%d: check failed: %s\n",              \
                    __FILE__, __LINE__, #cond);                      \
            return -1;                                               \
        }                                                            \
    } while (0)
```

**Two things a function cannot do:**

1. **Report the caller's file and line.** `__FILE__` and `__LINE__` expand where the macro is *used*.
   Inside a function they would expand at the function's own definition, naming the same line every
   time — useless. There is no portable way for a function to learn its caller's location.
2. **Print the condition's source text.** `#cond` stringifies the argument, so a failure prints
   `check failed: ptr != NULL` rather than `check failed: 0`. A function receives only the *value* of
   the condition; the text is gone by then.

*(A third, minor one: a macro can `return` from the enclosing function, which a function cannot do on
its caller's behalf.)*

**The serious objection to hiding a `return`:** it makes control flow invisible at the call site.

```c
CHECK(p != NULL);      /* looks like a statement; is actually a conditional return */
```

A reader scanning for exit points will not find this one, and — worse — it silently skips any cleanup
between here and the end of the function:

```c
FILE *f = fopen(path, "r");
CHECK(f != NULL);
char *buf = malloc(1024);
CHECK(buf != NULL);       /* returns -1 and LEAKS f */
```

That is a resource leak created by the very construct meant to improve robustness.

**Mitigations**, in order of preference: name it so the control flow is obvious (`CHECK_OR_RETURN`,
or the Linux-kernel-style `goto cleanup` pattern where the macro jumps to a single cleanup label
rather than returning); or restrict the macro to functions that own no resources; or make it *report*
without returning and let the caller decide.

*Full marks require naming the hidden-control-flow objection and connecting it to cleanup.* A student
who only says "macros are confusing" has not identified the concrete failure.

---

## Reading

- **K&R, §4.11.2** — macro substitution
- **C11 §6.10.3** — macro replacement, including the `#` and `##` rules
- **`gcc -E`** — expand any macro you are unsure about rather than reasoning about it
- **`-Wmultistatement-macros`** — on by default in `-Wall`; do not silence it

---

*PROG 101 · Week 10 · Lecture 2 · © CSE Department*

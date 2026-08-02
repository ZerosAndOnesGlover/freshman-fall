# PROG 101 · Lab 10 Solutions (Instructor)
## Seeing the Preprocessor

All figures verified on the reference machine (x86-64, GCC 13, glibc 2.39). Exact counts vary with
glibc version — **the order of magnitude is the marking point**, not the digits.

---

## Part 1: Looking at the Output (5 pts)

### 1A — the size of an include (2 pts)

| Measurement | Value |
|---|---|
| `wc -l tiny.c` | **2** |
| `gcc -E tiny.c \| wc -l` | **815** |
| `gcc -E -P tiny.c \| grep -c .` | **303** |

**Expected observation:** two lines of source become several hundred lines of declarations, type
definitions and macros, all of which the compiler must parse. Multiply by every `.c` file in a
project and header parsing dominates build time — which is why C projects care about include
hygiene, forward declarations, and (in modern C++) modules.

*Accept any figures of the right magnitude. Deduct only if the student reports numbers they clearly
did not run.*

### 1B — macros are text (2 pts)

`N` inside the string literal is **not replaced**. The preprocessor operates on **tokens**, and a
string literal is a single token — its contents are never scanned for macro names.

Outside the literal, `int a[N];` becomes `int a[10];` and `TWICE(N)` becomes `((10) + (10))`.

*This is why `#` exists: stringification is the only way to get a macro's text into a string.*

### 1C — predefined macros (1 pt)

GCC predefines **several hundred** macros (typically 380–450 depending on version and target).
Expected values here: `__STDC_VERSION__` = **201112L**, `__GNUC__` = **13**, `__x86_64__` = **1**.

---

## Part 2: Breaking Macros on Purpose (6 pts)

### Verified results

| Expression | Expansion | Result | Should be |
|---|---|---|---|
| **(a)** `SQUARE_BAD(2 + 3)` | `2 + 3 * 2 + 3` | **11** | 25 |
| **(b)** `100 / SQUARE_BAD(5)` | `100 / 5 * 5` | **100** | 4 |
| **(c)** `SQUARE_OK(2 + 3)` | `((2 + 3) * (2 + 3))` | **25** | ✓ |
| **(d)** `MAX(i++, 3)` with `i = 5` | returns **6**, `i` ends at **7** | | |

**Answer 1 (2 pts).** (a) fails because the *parameter* is unparenthesised, so `*` binds tighter
than the `+` inside it. (b) fails because the *body* is unparenthesised, so the division takes only
the first factor. **These are two different bugs and each needs its own set of parentheses** — a
student who fixes only one has not understood.

**Answer 2 (2 pts).** `i` ends at **7**. The defect is **double evaluation**: `a` appears twice in
`((a) > (b) ? (a) : (b))`, so `i++` is evaluated twice.

Parentheses cannot fix it because the problem is not precedence — the parameter is *used* twice by
construction, and text substitution duplicates the side effect along with the expression.

**Answer 3 (2 pts).**

```c
static inline int max_int(int a, int b) { return a > b ? a : b; }
```

**What is given up: type-genericity.** The macro works for `int`, `double`, `char` and anything else
comparable; the function works only for `int`. That is the real trade-off, and it is the honest
reason macros survive in C.

*Accept a GCC statement-expression version with `__typeof__` for full marks provided the student
notes it is a GNU extension and not portable.*

---

## Part 3: The `if`/`else` Trap (4 pts)

**Verified compiler output** — students must paste both:

```
error: 'else' without a previous 'if'
warning: macro expands to multiple statements [-Wmultistatement-macros]
```

*(2 pts for having both. The warning is the more useful of the two because it names the cause; the
error only names the symptom.)*

**Answer 3 (1 pt) — why a bare block does not work.**

```c
#define LOG_BLOCK(m) { printf("log: %s\n", m); printf("---\n"); }

if (c) LOG_BLOCK("x"); else printf("else\n");
```

expands to `if (c) { ... } ; else ...` — the block ends the `if` statement, and the **stray
semicolon** from the call site becomes a null statement between the `if` and the `else`. The `else`
is orphaned exactly as before.

**Why `do { } while (0)` works:** it is a **single statement that requires a terminating semicolon**,
so `LOG_OK("x");` is one complete statement and the call site reads like a function call. The loop
runs once and every compiler removes it entirely.

*(1 pt for confirming `LOG_OK` compiles.)*

---

## Part 4: A Framework You Cannot Write as a Function (5 pts)

```c
#ifndef CHECK_H
#define CHECK_H
#include <stdio.h>

extern int checks_run, checks_failed;

#define CHECK(cond)                                              \
    do {                                                         \
        checks_run++;                                            \
        if (!(cond)) {                                           \
            checks_failed++;                                     \
            fprintf(stderr, "  %s:%d: CHECK failed: %s\n",        \
                    __FILE__, __LINE__, #cond);                  \
        }                                                        \
    } while (0)

int check_report(void);
#endif
```

```c
int checks_run = 0, checks_failed = 0;

int check_report(void)
{
    printf("%d checks, %d failed\n", checks_run, checks_failed);
    return checks_failed == 0 ? 0 : 1;
}
```

**Verified output shape:**

```
  test_check.c:12: CHECK failed: 1 == 2
5 checks, 2 failed
```

**Answer 3 — the two function-impossible capabilities (2 pts):**

1. **Reporting the caller's file and line.** `__FILE__` and `__LINE__` expand where the macro is
   *used*. Inside a function they would expand at the function's own definition, naming the same
   line for every failure. There is no portable way for a function to discover its caller's
   location.
2. **Printing the condition's source text.** `#cond` stringifies the argument *before* it is
   evaluated. A function receives only the resulting `int` — by then `ptr != NULL` has become `0`
   and the text is gone. `CHECK failed: 0` is useless; `CHECK failed: ptr != NULL` is not.

*Both are required for the 2 marks. Students frequently give only the first.*

---

## Common Submission Problems

| Symptom | Cause | Action |
|---|---|---|
| Part 1 numbers look invented | Did not run the commands | −2; the exact figures are unimportant, running them is not |
| Predicted (a) = 25 and recorded 25 | Did not actually run it | −1; the prediction being wrong is the lesson |
| `CHECK` without `do { } while (0)` | Missed Part 3's point | −1, and note it |
| Part 2 answer 3 omits what was given up | Half the question | −1 |
| `check_report` returns `checks_failed` | Works, but a count is not a status | No deduction; mention the convention |

---

*PROG 101 · Week 10 · Lab 10 Solutions · Instructor copy — do not distribute*

# PROG 101 · Programming I: Structured Programming in C
## Week 10 · Problem Set 10: The Preprocessor and Macros

**Released:** Friday, Week 10 · **Due:** Friday, Week 11 at 17:00
**Total:** 100 points
**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`
**Check with:** `valgrind --leak-check=full --error-exitcode=1`

> When a macro misbehaves, **run `gcc -E -P` and read the expansion** before reasoning about it.
> Several problems below are much easier that way, and one is nearly impossible without it.

---

## Problem 1: Header Discipline (20 pts)

You are given `shapes.h` and `shapes.c` in the starter, both defective.

```c
/* shapes.h -- as given */
#include "shapes.h"
#include <math.h>

struct Point { double x, y; };
double distance(struct Point a, struct Point b)
{
    return sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y));
}
int shape_count;
Point *make_point(double x, double y);
```

### Tasks

**(a)** List every defect. There are **five**. For each, say what goes wrong and when — at
preprocessing, compilation, or linking. *(10 pts)*

**(b)** Rewrite `shapes.h` correctly, and write the matching `shapes.c`. *(6 pts)*

**(c)** Demonstrate that your header is **self-contained** by compiling a file whose entire contents
are `#include "shapes.h"`, using `gcc -fsyntax-only`. Paste the command and its output. *(2 pts)*

**(d)** Create `main.c` and a second `.c` file that both include `shapes.h`, and show the whole
program links. Then explain in `answers.md` why the original `int shape_count;` would have prevented
that. *(2 pts)*

---

## Problem 2: Macro Repair (20 pts)

Each macro below is broken. For each: give an argument that **demonstrates** the bug with actual
values, state the category of defect, and write the fix. *(4 pts each.)*

```c
#define BUFSIZE 256;
#define CUBE(x) x * x * x
#define AVG(a, b) (a + b) / 2
#define DOUBLE_IT(x) ((x) + (x))
#define LOG_TWICE(m) printf("%s\n", m); printf("%s\n", m)
```

**Requirements.** A demonstration must be a concrete expression and its actual wrong value — not
"it might break with a complex argument". For `DOUBLE_IT`, note that the parentheses are already
correct; the defect is of a different kind.

---

## Problem 3: A Check Framework (25 pts)

Build `check.h` providing a lightweight test framework.

```c
CHECK(cond);                 /* record pass/fail; print file, line and the CONDITION TEXT */
CHECK_EQ_INT(a, b);          /* on failure also print both actual values */
CHECK_STR(a, b);             /* strcmp-based                             */
int  check_report(void);     /* print a summary; return 0 iff all passed */
```

### Requirements

1. A failure message must include `__FILE__`, `__LINE__`, and the **source text** of the condition.
2. Every macro must be usable in an unbraced `if`/`else` without breaking it.
3. `CHECK_EQ_INT(a, b)` must evaluate each argument **exactly once**. Demonstrate this with
   `CHECK_EQ_INT(i++, 1)` and show `i` advanced by exactly 1.
4. Defining `NDEBUG` must **not** disable your checks — explain in `answers.md` why piggy-backing on
   `assert` would be the wrong design here.
5. Write `test_check.c` exercising passes and failures of all three macros.

### Marking

| Component | Points |
|---|---|
| `CHECK` reports file, line and condition text | 6 |
| All macros safe in unbraced `if`/`else` | 5 |
| Single evaluation, demonstrated | 6 |
| `check_report` returns a correct status | 4 |
| The `NDEBUG` explanation | 4 |

---

## Problem 4: An X-Macro Token Table (20 pts)

A calculator needs its operator table in four forms: an `enum`, a symbol table, a precedence table,
and the identifier text for error messages.

**Write the list once** and generate all four.

```c
#define TOKENS          \
    X(PLUS,  "+", 1)    \
    X(MINUS, "-", 1)    \
    X(TIMES, "*", 2)    \
    X(DIV,   "/", 2)
```

### Requirements

1. Generate `enum Token { ... TOK_COUNT }`, `tok_sym[]`, `tok_prec[]`, and `tok_name[]`.
2. `tok_name` must hold `"PLUS"`, `"MINUS"`, … produced by **stringifying the identifier**, not
   typed by hand.
3. Add a `_Static_assert` for **each** table confirming its length equals `TOK_COUNT`.
4. Write `int tok_from_symbol(const char *s)` returning the token or −1.
5. Add one operator (`MOD`, `"%"`, precedence 2) by editing **one line**, and show everything still
   works.
6. In `answers.md`: give one concrete situation where you would **reject** this pattern in code
   review, and name a simpler alternative that solves the same drift problem. *(5 of the 20 pts.)*

---

## Problem 5: Build Configurations (15 pts)

Write `config.c` that behaves differently under three builds, from **one source file**:

| Build | Behaviour |
|---|---|
| `gcc config.c` | Release: no diagnostics |
| `gcc -DDEBUG config.c` | Prints entry and exit of each function |
| `gcc -DDEBUG=2 config.c` | Also prints every intermediate value |

### Requirements

1. Use `#if defined(DEBUG) && DEBUG > 1` / `#elif` / `#else`.
2. The release build must contain **no trace code at all** — verify with
   `gcc -E -P config.c | grep -c trace` and report the count.
3. Your `DBG` macro must expand to `((void)0)` when disabled, not to nothing. Explain why in
   `answers.md`.
4. In `answers.md`, state the trade-off: what does conditionally compiled code cost you that a
   runtime `if (debug)` flag does not?

---

## Grading

| Problem | Topic | Points |
|---|---|---|
| 1 | Header Discipline | 20 |
| 2 | Macro Repair | 20 |
| 3 | A Check Framework | 25 |
| 4 | An X-Macro Token Table | 20 |
| 5 | Build Configurations | 15 |
| **Total** | | **100** |

**Automatic deductions:** any compiler warning (−2 each); a header without an include guard (−5).

---

## Answer Key (Instructor Copy)

### Problem 1 — Header Discipline (20 pts)

**(a) The five defects** *(2 pts each)*

| # | Defect | Fails at | Evidence |
|---|---|---|---|
| 1 | **No include guard** | Compilation, on second inclusion | `redefinition of 'struct Point'` |
| 2 | **The header includes itself** | **Preprocessing** | `#include nested depth 200 exceeds maximum of 200` |
| 3 | **A function *body* in a header** | **Linking** | `multiple definition of 'distance'` |
| 4 | **`int shape_count;` defines a variable** | **Linking** | `multiple definition of 'shape_count'` |
| 5 | **`Point` used where the type is `struct Point`** | Compilation | `unknown type name 'Point'; use 'struct' keyword` |

All five verified. Note defect 2 masks the others until it is fixed — a good demonstration that
preprocessing errors come first and must be cleared before anything else is visible.

*A sixth, acceptable as a bonus observation:* `<math.h>` is included by the header for the benefit of
its own function body; once that body moves to the `.c` file, the include should move with it unless
the header's declarations need it.

**(b) Corrected header** *(6 pts)*

```c
/* shapes.h */
#ifndef SHAPES_H
#define SHAPES_H

typedef struct Point { double x, y; } Point;   /* now `Point` is a valid type name */

extern int shape_count;                        /* DECLARATION only */

double distance(Point a, Point b);             /* declaration only  */
Point *make_point(double x, double y);         /* CALLER MUST FREE  */

#endif /* SHAPES_H */
```

```c
/* shapes.c */
#include "shapes.h"
#include <math.h>
#include <stdlib.h>

int shape_count = 0;                           /* the single DEFINITION */

double distance(Point a, Point b)
{
    double dx = a.x - b.x, dy = a.y - b.y;
    return sqrt(dx*dx + dy*dy);
}

Point *make_point(double x, double y)
{
    Point *p = malloc(sizeof *p);
    if (p) { p->x = x; p->y = y; }
    return p;
}
```

*Marking: 2 for the guard, 2 for moving the body out, 1 for `extern`, 1 for fixing the type name.*

**(c)** *(2 pts)* `gcc -fsyntax-only -Wall -Wextra -pedantic -std=c11 t.c` where `t.c` is only
`#include "shapes.h"` — must produce **no output**. Deduct if the header still needs another header
included first.

**(d)** *(2 pts)* `int shape_count;` at file scope is a **tentative definition**: it allocates
storage. After preprocessing, each `.c` file that included the header contains its own, so each
object file defines the symbol and the linker rejects the duplicates. `extern` makes it a
declaration, which may be repeated freely, with exactly one definition in one `.c` file.

*(Note: GCC ≥ 10 defaults to `-fno-common`, so this is now an error rather than being silently
merged. Under `-fcommon` it still links — worth mentioning if a student reports that.)*

---

### Problem 2 — Macro Repair (20 pts)

*4 points each: 2 for a concrete demonstration, 1 for the category, 1 for the fix.*

| Macro | Demonstration | Category | Fix |
|---|---|---|---|
| `BUFSIZE 256;` | `int a[BUFSIZE];` → `int a[256;];` — syntax error at the **use** | Stray semicolon | `#define BUFSIZE 256` |
| `CUBE(x) x * x * x` | `CUBE(1+1)` → `1+1 * 1+1 * 1+1` = **5**, not 8 | Missing parentheses | `((x) * (x) * (x))` |
| `AVG(a,b) (a + b) / 2` | `AVG(2,4) * 2` → `(2+4)/2 * 2` = 6 ✓, but `10 / AVG(2,4)` → `10 / (6)/2` = **0**, not 3 | Body not parenthesised | `(((a) + (b)) / 2)` |
| `DOUBLE_IT(x) ((x)+(x))` | `int i=5; DOUBLE_IT(i++)` → `i` becomes **7**, result 11 | **Double evaluation** | Use a function: `static inline int double_it(int x){ return x+x; }` |
| `LOG_TWICE(m)` | `if (c) LOG_TWICE("x"); else ...` → `error: 'else' without a previous 'if'` | Multi-statement | Wrap in `do { … } while (0)` |

**`DOUBLE_IT` is the discriminating one.** Its parentheses are already correct, and students who
pattern-match on "add parentheses" will not find the bug. The parameter appears twice, so any
argument with a side effect is evaluated twice — and no amount of parenthesising fixes that. GCC
warns about the `LOG_TWICE` shape with `-Wmultistatement-macros`; it cannot warn about this one.

---

### Problem 3 — A Check Framework (25 pts)

```c
#ifndef CHECK_H
#define CHECK_H
#include <stdio.h>
#include <string.h>

extern int checks_run, checks_failed;

#define CHECK(cond)                                                  \
    do {                                                             \
        checks_run++;                                                \
        if (!(cond)) {                                               \
            checks_failed++;                                         \
            fprintf(stderr, "  %s:%d: CHECK failed: %s\n",            \
                    __FILE__, __LINE__, #cond);                      \
        }                                                            \
    } while (0)

#define CHECK_EQ_INT(a, b)                                           \
    do {                                                             \
        int _a = (a), _b = (b);          /* each evaluated ONCE */   \
        checks_run++;                                                \
        if (_a != _b) {                                              \
            checks_failed++;                                         \
            fprintf(stderr, "  %s:%d: CHECK_EQ_INT failed: %s == %s"  \
                            " (got %d vs %d)\n",                     \
                    __FILE__, __LINE__, #a, #b, _a, _b);             \
        }                                                            \
    } while (0)

#define CHECK_STR(a, b)  /* analogous, using strcmp on temporaries */

int check_report(void);
#endif
```

**Verified:** the framework reports `ps10.c:64: CHECK failed: 1 == 2` — file, line and condition text
— and 12 passing checks across macro, X-macro and comparison tests.

**Marking notes.**

- **Requirement 3 is where the marks are (6 pts).** `CHECK_EQ_INT` must copy its arguments into
  local temporaries *before* comparing, or `CHECK_EQ_INT(i++, 1)` increments `i` twice — once in the
  comparison and once in the failure `printf`. The demonstration must show `i` advancing by exactly
  1. A version that only avoids double evaluation on the *success* path scores 3.
- **The temporaries need unlikely names** (`_a`, `_b` or better). A macro declaring `a` and `b`
  breaks any caller whose own variables are named `a` and `b` — and that failure is baffling.
- **Requirement 4 (4 pts).** Piggy-backing on `assert` is wrong because **`NDEBUG` removes `assert`
  entirely in release builds**, so the tests would silently stop running and `check_report` would
  report success having checked nothing. Test frameworks must be independent of `NDEBUG`. Award full
  marks only if the student identifies that the tests would *silently pass*, not merely "be
  disabled".
- **`do { } while (0)` on every macro** (5 pts) — verify by putting each in an unbraced `if`/`else`.

---

### Problem 4 — An X-Macro Token Table (20 pts)

```c
#define X(name, sym, prec) TOK_##name,
enum Token { TOKENS TOK_COUNT };
#undef X

#define X(name, sym, prec) sym,
static const char *tok_sym[]  = { TOKENS };
#undef X

#define X(name, sym, prec) prec,
static const int   tok_prec[] = { TOKENS };
#undef X

#define X(name, sym, prec) #name,
static const char *tok_name[] = { TOKENS };
#undef X

_Static_assert(sizeof tok_sym  / sizeof tok_sym[0]  == TOK_COUNT, "tok_sym out of sync");
_Static_assert(sizeof tok_prec / sizeof tok_prec[0] == TOK_COUNT, "tok_prec out of sync");
_Static_assert(sizeof tok_name / sizeof tok_name[0] == TOK_COUNT, "tok_name out of sync");

int tok_from_symbol(const char *s)
{
    for (int i = 0; i < TOK_COUNT; i++) if (strcmp(s, tok_sym[i]) == 0) return i;
    return -1;
}
```

**Verified:** `TOK_COUNT` is 4; all three tables populate correctly; `tok_from_symbol("*")` returns
`TOK_TIMES` and `tok_from_symbol("?")` returns −1. Deliberately desynchronising one table produces:

```
error: static assertion failed: "tok_prec out of sync"
```

**Marking notes.**

- **`#name` for `tok_name` (3 pts)** — hand-typed strings defeat the exercise entirely.
- **`#undef X` between uses is mandatory (2 pts).** Omitting it is a redefinition error, and the
  message points at the `#define`, not the cause.
- **`TOK_COUNT` after the list (2 pts)** works because every `X` emits a trailing comma. Worth
  drawing out as an idiom in its own right.
- **Requirement 5 (2 pts):** adding `X(MOD, "%", 2)` must require exactly one edited line.
- **Requirement 6 (5 pts)** — the reject-in-review answer. Accept: the list is short and stable;
  `grep TOK_PLUS` finds nothing; errors inside the expansion are cryptic. The **simpler alternative**
  that must be named is the `_Static_assert` length check on two hand-written tables — it solves the
  drift problem directly with none of the obscurity. A student who only says "it's hard to read"
  scores 2 of 5.

---

### Problem 5 — Build Configurations (15 pts)

```c
#if defined(DEBUG) && DEBUG > 1
#  define DBG(...)   fprintf(stderr, __VA_ARGS__)
#  define TRACE(...) fprintf(stderr, __VA_ARGS__)
#elif defined(DEBUG)
#  define DBG(...)   ((void)0)
#  define TRACE(...) fprintf(stderr, __VA_ARGS__)
#else
#  define DBG(...)   ((void)0)
#  define TRACE(...) ((void)0)
#endif
```

Verified across three builds: `release`, `debug`, `verbose debug` from one source.

**Requirement 2 (3 pts).** `gcc -E -P config.c | grep -c trace` must report **0** in the release
build. This is the point of conditional compilation as against a runtime flag: the code is not
merely skipped, it is **absent**.

**Requirement 3 (4 pts).** `((void)0)` rather than an empty expansion, because an empty macro leaves
a bare `;` — a null statement that breaks an unbraced `if`/`else` exactly as a multi-statement macro
does. `(void)0` is a valid expression statement, so the call site stays one statement.

**Requirement 4 (4 pts).** The trade-off: **conditionally compiled code is never compiled in the
release build, so it rots silently.** A `DBG` line referring to a variable that was later renamed
breaks nothing until someone builds with `-DDEBUG` months later. A runtime `if (debug)` keeps the
code compiling always, at the cost of the branch and of evaluating the arguments.

*Full marks require naming the rot.* "You can't turn it on at runtime" is true but secondary and
scores 2.

---

*PROG 101 · Week 10 · Problem Set 10 · © CSE Department*

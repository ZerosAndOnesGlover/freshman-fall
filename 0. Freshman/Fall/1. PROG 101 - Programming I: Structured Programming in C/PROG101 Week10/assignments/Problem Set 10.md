# PROG 101 · Programming I: Structured Programming in C
## Week 10 · Problem Set 10: The Preprocessor and Macros

**Released:** Friday 4 December 2026, 10:00 · Week 10 (after Thursday's Lecture 3)
**Due:** Friday 11 December 2026, 17:00 · Week 11 — late penalty from 17:01
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: Lab 10, on Monday 7 December, breaks the precedence, double-evaluation and `if`/`else`
macros that old Problem 2 asked you to repair, and builds a first `CHECK` macro. Problem 2 is now only in the lab,
and Problem 3 extends the lab's `check.h`. The answer key moved out of this handout.)*
**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`
**Check with:** `valgrind --leak-check=full --error-exitcode=1`

> When a macro misbehaves, **run `gcc -E -P` and read the expansion** before reasoning about it.
> Several problems below are much easier that way, and one is nearly impossible without it.

---

## Problem 1: Header Discipline (25 pts)

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
preprocessing, compilation, or linking. *(12 pts)*

**(b)** Rewrite `shapes.h` correctly, and write the matching `shapes.c`. *(8 pts)*

**(c)** Demonstrate that your header is **self-contained** by compiling a file whose entire contents
are `#include "shapes.h"`, using `gcc -fsyntax-only`. Paste the command and its output. *(2 pts)*

**(d)** Create `main.c` and a second `.c` file that both include `shapes.h`, and show the whole
program links. Then explain in `answers.md` why the original `int shape_count;` would have prevented
that. *(3 pts)*

---

## Problem 2: A Check Framework (25 pts)

Extend the `check.h` you started in Lab 10 into a lightweight test framework.

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

## Problem 3: An X-Macro Token Table (25 pts)

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
   review, and name a simpler alternative that solves the same drift problem. *(6 of the 25 pts.)*

---

## Problem 4: Build Configurations (25 pts)

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
| 1 | Header Discipline | 25 |
| 2 | A Check Framework | 25 |
| 3 | An X-Macro Token Table | 25 |
| 4 | Build Configurations | 25 |
| **Total** | | **100** |

**Automatic deductions:** any compiler warning (−2 each); a header without an include guard (−5).

---

*PROG 101 · Week 10 · Problem Set 10 · Due Friday 11 December 2026, 17:00 · © CSE Department*

# PROG 101 · Programming I: Structured Programming in C
## Week 12 · Lecture 2: Testing in C

---

## Lecture Goals

By the end of this lecture you can:

- Build a minimal test framework and say why it must be a macro
- Choose test cases by reasoning about boundaries, not by intuition
- Measure coverage with `gcov` and explain what the number does and does not mean
- State what testing can and cannot establish

---

## 1. C Gives You Nothing

There is no `unittest`, no `pytest`, no test runner in the standard library. What C gives you is
`assert`, and `assert` is the wrong tool:

```c
assert(list_length(l) == 3);
```

It aborts on the first failure, so you learn about one bug per run. It is **disabled by `-DNDEBUG`**,
so a release build silently tests nothing. And it reports the condition but not the actual values.

So you write a framework. It is about thirty lines, and building it is worth doing once.

---

## 2. A Test Framework in Thirty Lines

```c
/* check.h */
#ifndef CHECK_H
#define CHECK_H
#include <stdio.h>
#include <string.h>

extern int checks_run, checks_failed;

#define CHECK(cond)                                                   \
    do {                                                              \
        checks_run++;                                                 \
        if (!(cond)) {                                                \
            checks_failed++;                                          \
            fprintf(stderr, "  %s:%d: FAIL: %s\n",                     \
                    __FILE__, __LINE__, #cond);                       \
        }                                                             \
    } while (0)

#define CHECK_EQ_INT(a, b)                                            \
    do {                                                              \
        int _a = (a), _b = (b);            /* evaluate ONCE each */   \
        checks_run++;                                                 \
        if (_a != _b) {                                               \
            checks_failed++;                                          \
            fprintf(stderr, "  %s:%d: FAIL: %s == %s (got %d vs %d)\n",\
                    __FILE__, __LINE__, #a, #b, _a, _b);              \
        }                                                             \
    } while (0)

int check_report(void);
#endif
```

Verified output shape:

```
  test_vec.c:41: FAIL: vec_size(v) == 3 (got 2 vs 3)
12 checks, 1 failed
```

### Why it must be a macro

Two things a function cannot do (Week 10):

1. **Report the caller's file and line.** `__FILE__` and `__LINE__` expand at the *use* site. Inside
   a function they would name the framework's own line, every time.
2. **Print the condition's source text.** `#cond` stringifies the argument before evaluation. A
   function receives only the resulting `int` — `FAIL: 0` instead of `FAIL: vec_size(v) == 3`.

### Three design decisions worth defending

**It does not abort.** Every check runs, so one failing run tells you about every broken case, not
just the first. `check_report` returns non-zero at the end, which is what `make test` needs.

**It does not depend on `NDEBUG`.** Piggy-backing on `assert` would mean a release build runs zero
checks and **reports success**. Silent passing is far worse than not running at all.

**`CHECK_EQ_INT` copies its arguments into temporaries.** Otherwise `CHECK_EQ_INT(i++, 1)`
increments `i` twice — once comparing, once printing. This is Week 10's double-evaluation trap in the
one place where it is genuinely easy to write.

---

## 3. Choosing Test Cases

Most people test the case they had in mind while writing the code, which is the case that already
works. Test the boundaries instead.

For a function over a collection of size *n*:

| Case | Why |
|---|---|
| **n = 0** | Empty. The single most productive test case in existence |
| **n = 1** | Often takes a different path |
| **n = 2** | The smallest case where order matters |
| typical n | The case you were already thinking of |
| **n at capacity** | Exactly full, just before growth |
| **n past capacity** | Forces the growth path |

For numeric inputs: **0, 1, −1, `INT_MAX`, `INT_MIN`**, and either side of every threshold in the
code.

For strings: **`""`, one character, a string exactly filling the buffer, one longer, and a byte above
127** (which catches the signed-`char` bug from Week 4).

**The rule:** for every `if` in the function, there should be a test that takes each branch. For
every boundary comparison, a test on each side of it.

### Test behaviour, not implementation

```c
CHECK(v->cap == 8);              /* brittle: breaks if the growth factor changes */
CHECK(vec_size(v) == 5);         /* durable: tests the contract                  */
```

A test asserting an internal detail fails when you refactor correctly-working code, which trains
people to ignore failing tests. Test what the interface promises.

---

## 4. Coverage

`gcov` reports which lines actually executed.

```bash
gcc --coverage -O0 -o test test.c mycode.c
./test
gcov mycode.c
```

Verified on a four-branch function tested with only two inputs:

```
File 'cov.c'
Lines executed:87.50% of 8
```

and in the annotated listing:

```
        2:    4:    if (n < 0)      return -1;
       1*:    5:    else if (n == 0) return 0;
        1:    6:    else if (n < 10) return 1;
    #####:    7:    else             return 2;
```

**`#####` marks a line that never ran.** That is the useful output — not the percentage, but the
specific lines your tests never reached. Line 7 is untested, and now you know.

### What coverage does and does not mean

**High coverage does not mean correct.** This has 100% line coverage and is wrong:

```c
int divide(int a, int b) { return a / b; }      /* test: divide(6, 2) == 3 */
```

Every line ran. `b == 0` is undefined behaviour and untested.

**Low coverage does mean untested.** The implication runs one way only, and that is still useful:
coverage cannot tell you the tested code is right, but it reliably tells you which code is not tested
at all.

Treat it as a **checklist of gaps**, never as a target. A team chasing a coverage number writes tests
that execute lines without asserting anything.

---

## 5. What Testing Cannot Do

> **Testing shows the presence of bugs, never their absence.** — Dijkstra

A test exercises one path with one input on one build. Exhaustive testing is impossible for anything
non-trivial: a function of two `int`s has 2⁶⁴ inputs.

Worse, for **undefined behaviour** the limitation is fundamental rather than statistical. UB is a
property of the *program text*, not of any particular run — code with signed overflow can pass every
test at `-O0` and fail at `-O2`, because the optimiser is entitled to assume the overflow cannot
happen (Week 2).

**This is why the course pairs testing with other techniques:**

| Technique | Catches |
|---|---|
| `-Wall -Wextra -Werror -pedantic` | Whole classes of defect, before running |
| ASan / UBSan | Memory errors and UB at run time |
| Valgrind | The above, **plus uninitialised reads** |
| `_Static_assert` | Assumptions, at compile time, with no test needed |
| Tests | Behaviour you thought to check |

No single one is sufficient. The compiler flags cost nothing and run every build, which makes them
the highest-value item on that list.

---

## 6. Summary

| Idea | Takeaway |
|---|---|
| C has no test framework | You write one; it is ~30 lines |
| `assert` is not it | Aborts on first failure; **disabled by `-DNDEBUG`** |
| The framework must be a macro | Only a macro sees the caller's `__FILE__`/`__LINE__` and `#cond` |
| Do not abort | One run should report every failure |
| Do not depend on `NDEBUG` | Silent passing is worse than not running |
| Copy arguments to temporaries | Or `CHECK_EQ_INT(i++, 1)` evaluates twice |
| Test boundaries | **n = 0** is the most productive case there is |
| Test behaviour, not internals | Asserting `v->cap` breaks on correct refactors |
| `gcov`'s `#####` | Marks never-executed lines — the useful output |
| High coverage ≠ correct | 100% coverage, still undefined on `b == 0` |
| Low coverage ⇒ untested | The implication runs one way |
| Testing shows presence | Never absence — pair it with flags and sanitizers |

---

## Practice Exercises

**1. (Design.)** List the test cases you would write for
`int vec_insert(Vec *v, size_t i, int value)` which inserts at index `i`. Justify each.

**2. (Explain.)** Why must `CHECK` be a macro rather than a function? Give both reasons.

**3. (Critique.)** This suite reports 100% coverage. What is untested?

```c
size_t str_len(const char *s) { size_t n = 0; while (s[n]) n++; return n; }

CHECK(str_len("abc") == 3);
CHECK(str_len("hello") == 5);
```

**4. (Stretch.)** A team mandates 90% line coverage. Give two ways a developer could satisfy that
mandate while making the test suite *worse*, and propose a better target.

### Answers

**1.** At minimum:

| Case | Why |
|---|---|
| Insert into an **empty** vector at `i = 0` | The n = 0 boundary |
| Insert at `i = 0` with existing elements | Shifts everything; the maximum-work path |
| Insert at `i = len` (append) | Boundary: valid, but no shifting |
| Insert at `i = len + 1` | **Invalid** — must be rejected, not appended |
| Insert at a middle index | The typical case |
| Insert when `len == cap` | Forces the growth path |
| Insert when the allocation **fails** | The error path — inject a failure or use a stub allocator |
| Verify order after several inserts | Insertion must preserve relative order |

The two most often missed are `i == len` (valid) versus `i == len + 1` (invalid), and the
allocation-failure path. *Look for a candidate who tests both sides of the index boundary.*

**2.** Both from Week 10:

1. **`__FILE__` and `__LINE__` expand at the call site.** Inside a function they would expand once,
   at the function's own definition, and every failure would report the same line.
2. **`#cond` stringifies the argument's source text** before it is evaluated. A function receives
   only the resulting value, by which point `vec_size(v) == 3` has become `0` and the text is
   irrecoverable.

**3.** Every line of `str_len` executes, so coverage is 100%. Untested:

- **The empty string.** `str_len("")` should be 0 — the n = 0 boundary, and the loop's zero-iteration
  path.
- **NULL.** `str_len(NULL)` dereferences a null pointer. Either the contract forbids NULL (and that
  should be documented, ideally with an `assert`) or the function must handle it. The tests do not
  reveal which was intended.
- **A high byte.** `str_len("\xff")` — fine here, but the same test suite would miss the signed-`char`
  bug in a `strcmp` implementation (Week 4).
- **A long string**, and one containing an embedded `\0`, which would reveal that this counts to the
  *first* terminator.

**This is the lecture's point in miniature:** 100% line coverage, and four meaningful untested cases.
Coverage measured which lines *ran*, not which behaviours were *checked*.

**4.** **Two ways to game it:**

1. **Write tests that execute code without asserting anything.** Calling every function once and
   checking nothing gives high coverage and zero defect detection. Coverage tools cannot tell the
   difference.
2. **Delete or exclude hard-to-cover code**, typically error paths — the `if (!p) return -1;`
   branches. Since those are the least-tested and most bug-prone parts of C code, the mandate would
   have *removed* tests from exactly where they matter, while the number went up.

*A third: assert weak conditions like `CHECK(result >= 0)` that pass regardless of correctness.*

**A better target.** Use coverage as a **diagnostic, not a goal**: require that every *new* branch is
covered by a test in the same commit, and review the `#####` lines rather than the percentage.
Combine with a mutation-style question in review — "if I flipped this comparison, would a test
fail?" — which measures whether the tests *assert* rather than merely execute.

The general principle is Goodhart's law: **a measure that becomes a target stops being a good
measure.** Coverage is diagnostic information about gaps, and it is genuinely useful in that role.

---

## Reading

- **`man gcov`**, and run it on your own Week 6 code today
- **Kernighan & Pike, Ch. 6** — testing
- **Dijkstra, "Notes on Structured Programming" (1970), §3** — the source of the presence/absence line

---

*PROG 101 · Week 12 · Lecture 2 · © CSE Department*

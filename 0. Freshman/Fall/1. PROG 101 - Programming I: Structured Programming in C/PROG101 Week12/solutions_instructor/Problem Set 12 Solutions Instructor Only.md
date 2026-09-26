# PROG 101 · Problem Set 12 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

*(Revised 2026-09-26: old Problems 2, 3 and 5 are no longer asked — Lab 12 and PS 10 cover them. Old 4 → 2.
Marks: P1 22/9/8/7/9, P2 14/12/11/8.)*

## Answer Key (Instructor Copy)

### Problem 1 — Refactor (25 pts)

There is no single correct decomposition. Mark on **whether the interfaces are defensible**, not on
matching a model answer.

**Look for:**

- `main.c` that reads as a summary — load, filter, compute, report — with the detail elsewhere.
- Headers containing **declarations only**. A function body in a header is `multiple definition` at
  link time (Week 10) and costs the module marks.
- `static` on everything not in a header. **(b)** should say: it shrinks the interface, prevents
  other files coupling to internals, and lets the compiler optimise knowing every caller.
- **(c)** Names that state what a thing *is*, booleans reading as assertions, functions named for
  their return value.
- **(d)** The likely candidate is a `print_report(…, int verbose)` or `save(…, int as_binary)`.
  Accept a justified retention — a flag threaded through to a genuinely shared implementation is
  defensible; what is not defensible is `f(x, 1)` at the call site.
- **(e)** `echo '#include "record.h"' > t.c && gcc -fsyntax-only -Wall -Wextra t.c` must be silent.

**The byte-identical constraint is the point of the problem.** Refactoring that changes behaviour is
not refactoring. A student whose output differs has either introduced a bug or "improved" something
they were not asked to.

### Problem 2 — Framework and Tests (25 pts)

Reference `check.h` is Lecture 2's. Verified output shape:

```
  test_records.c:41: FAIL: stats_mean(s) == 3 (got 2 vs 3)
12 checks, 1 failed
```

**Marking notes.**

- **Single evaluation (3 of the 10)** — demonstrate with `CHECK_EQ_INT(i++, 1)`; `i` must advance by
  exactly 1. Copying into `int _a = (a), _b = (b);` is the fix.
- **`do { } while (0)`** on every macro (2 of the 10). Verify in an unbraced `if`/`else`.
- **Independence from `NDEBUG`** (2 of the 10). Building with `-DNDEBUG` must still run every check.
  A framework built on `assert` would report success having tested nothing — say so in feedback.
- **(b)** The five required cases map onto Lecture 2's boundary list. The two most often missed are
  the field **exactly at** the buffer limit and the one **one byte longer** — the off-by-one boundary.
- **(c)** `make test` must return non-zero on failure, which means `check_report` returns non-zero
  and `main` propagates it. A target that prints failures but exits 0 is worth 2 of the 5.

### Problem 3 — Coverage (15 pts)

Verified example of the output students should produce:

```
File 'cov.c'
Lines executed:87.50% of 8

        2:    4:    if (n < 0)      return -1;
       1*:    5:    else if (n == 0) return 0;
        1:    6:    else if (n < 10) return 1;
    #####:    7:    else             return 2;
```

**(b)** The `#####` lines are the deliverable, not the percentage. Genuinely unreachable lines do
exist — a `default:` that all enum values already cover, or an allocation-failure branch that cannot
be triggered without injection — and identifying one correctly earns full credit.

**(c) is the discriminating part (4 pts).** Expected shape of answer: a function with 100% line
coverage can still be undefined on an untested *input*, e.g. `divide(a, b)` fully covered by
`divide(6,2)` yet undefined for `b == 0`. Or: a boundary comparison `i <= n` executes on every test
while only being wrong at the boundary.

*Reject "coverage doesn't prove correctness" without a concrete bug and triggering input.*

### Problem 4 — Harden (20 pts)

**(a)** `-Wshadow` and `-Wconversion` typically produce real findings in student code: a loop
variable shadowing an outer one, and implicit narrowing in `int n = strlen(s);` (`size_t` → `int`).
Both are genuine.

**(d) is the marking point (3 pts).** The expected answer names **Valgrind detecting uninitialised
reads that ASan does not** — verified: a program reading a fresh `malloc` block produces
`Conditional jump or move depends on uninitialised value(s)` under Valgrind and nothing under ASan.

*Accept the converse too:* ASan gives far better stack and global buffer-overflow diagnostics and is
~20× faster, so the honest answer is that neither subsumes the other.

### Problem 5 — Debugging Reports (15 pts)

Mark the **process**, not the answer. Full marks require the tool choice to be *justified by the
symptom*:

| Defect | Expected first tool | Expected output |
|---|---|---|
| Crash | **GDB `bt`** | `#0 … (p=0x0) at buggy.c:N` — the argument value is the clue |
| Leak | **Valgrind** | `N bytes in 1 blocks are definitely lost` |
| Wrong answer, no crash | **Tests + `gcov`** | The untested branch; no sanitizer will fire |

The third is the discriminating one: students reach for a sanitizer reflexively, and a logic error
produces no sanitizer output at all. Reaching for tests instead is the mark of someone who has
matched tool to symptom rather than running everything.

**Requirement 6 — the regression test — is worth 1 of each 5.** A fix without a test is not finished.

---

*PROG 101 · Week 12 · Problem Set 12 · © CSE Department*

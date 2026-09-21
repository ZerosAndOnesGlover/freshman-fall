# PROG 101 · Programming I: Structured Programming in C
## Week 12 · Problem Set 12: Software Engineering in C

**Released:** Friday 18 December 2026, 10:00 · Week 12 (after Thursday's Lecture 3)
**Due:** Friday 25 December 2026, 17:00 (Friday of finals week) — ⚠️ this is Christmas Day since the term moved to 21 September; see the ACADEMIC CALENDAR's open decisions
**Total:** 100 points
**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`
**Check with:** `valgrind --leak-check=full --error-exitcode=1` and `-fsanitize=address,undefined`

> This set is a **refactoring and hardening exercise**, not a new-features exercise. You are given
> working but poor code and asked to make it good — with the tests to prove you did not break it.

---

## Problem 1: Refactor for the Reader (25 pts)

The starter contains `records.c`: a single 180-line `main` that reads a CSV, filters rows, computes
statistics, and prints a report. It works. It is also unmaintainable.

### Tasks

**(a)** Split it into modules with deliberate interfaces — at minimum `record.h/.c`, `stats.h/.c`,
and `report.h/.c`, plus a `main.c` that reads as a summary of the program. *(10 pts)*

**(b)** Every function private to a module must be `static`. In `answers.md`, list what you made
`static` and say what that buys. *(4 pts)*

**(c)** Apply the naming rules from Lecture 1. In `answers.md`, give three names you changed and the
reason for each. *(4 pts)*

**(d)** Replace at least one boolean parameter with two functions, or justify in `answers.md` why the
one you found should stay. *(3 pts)*

**(e)** Every header must have a guard and compile standalone. Demonstrate with `gcc -fsyntax-only`.
*(4 pts)*

**Constraint:** the refactored program must produce **byte-identical output** to the original on the
supplied test data. Prove it with `diff`.

---

## Problem 2: Build the Framework, Then Use It (25 pts)

**(a)** Implement `check.h` / `check.c` providing `CHECK`, `CHECK_EQ_INT`, `CHECK_STR` and
`check_report`. Requirements as Lecture 2: no abort on failure, independent of `NDEBUG`, single
evaluation of arguments, usable in an unbraced `if`/`else`. *(10 pts)*

**(b)** Write `test_records.c` testing your Problem 1 modules. Cover, at minimum: an empty input, a
single record, a malformed row, a row with a field exactly at the buffer limit, and one longer.
*(10 pts)*

**(c)** Add a `make test` target that builds and runs the suite and **fails the build** when any
check fails. Show the output of a passing run and of a deliberately broken one. *(5 pts)*

---

## Problem 3: Coverage as a Diagnostic (15 pts)

**(a)** Build with `--coverage`, run your suite, and produce `gcov` output for each module. Report
the percentage and paste the annotated listing for your least-covered file. *(5 pts)*

**(b)** Identify every line marked `#####`. For each, either write a test that reaches it or explain
in `answers.md` why it is unreachable. *(6 pts)*

**(c)** In `answers.md`: your suite now has high coverage. Give **one concrete bug** it could still
miss, with the input that would trigger it. *(4 pts)*

---

## Problem 4: Harden It (20 pts)

Run the tools against your Problem 1 code and fix what they find.

**(a)** `-Wall -Wextra -Werror -pedantic -Wshadow -Wconversion`. Report every warning the extra two
flags produced and how you fixed each. *(6 pts)*

**(b)** `-fsanitize=address,undefined`. Report and fix. *(6 pts)*

**(c)** `valgrind --leak-check=full --show-leak-kinds=all`. Must end at zero errors and zero bytes
definitely lost. *(5 pts)*

**(d)** In `answers.md`: which tool found something the others did not, and why? *(3 pts)*

---

## Problem 5: A Debugging Report (15 pts)

The starter contains `buggy.c` with three defects: one crashes, one leaks, one produces a wrong
answer without crashing.

For **each**, write a short report in `answers.md` covering:

1. The symptom as a user would see it
2. Which tool you reached for **first**, and why that one
3. The exact tool output that located it (pasted)
4. The root cause in one sentence
5. The fix
6. The test you added so it cannot return

*(5 pts each.)*

---

## Grading

| Problem | Topic | Points |
|---|---|---|
| 1 | Refactor for the Reader | 25 |
| 2 | Build the Framework, Then Use It | 25 |
| 3 | Coverage as a Diagnostic | 15 |
| 4 | Harden It | 20 |
| 5 | A Debugging Report | 15 |
| **Total** | | **100** |

**Automatic deductions:** any compiler warning (−2 each); any Valgrind error (−3 each); output not
byte-identical to the original in Problem 1 (−10).

---

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

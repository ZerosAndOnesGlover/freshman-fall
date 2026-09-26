# PROG 101 · Programming I: Structured Programming in C
## Week 12 · Problem Set 12: Software Engineering in C

**Released:** Friday 18 December 2026, 10:00 · Week 12 (after Thursday's Lecture 3)
**Due:** Friday 25 December 2026, 17:00 (Friday of finals week) — ⚠️ this is Christmas Day since the term moved to 21 September; see the ACADEMIC CALENDAR's open decisions
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: Lab 12 builds a `check.h` suite, measures coverage with gcov and writes a debugging report
on its own program, and Problem Set 10 already built the check framework. Those three problems (old 2, 3 and 5)
left this set, which keeps the refactor and the hardening. The answer key moved out of this handout.)*
**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`
**Check with:** `valgrind --leak-check=full --error-exitcode=1` and `-fsanitize=address,undefined`

> This set is a **refactoring and hardening exercise**, not a new-features exercise. You are given
> working but poor code and asked to make it good — with the tests to prove you did not break it.

---

## Problem 1: Refactor for the Reader (55 pts)

The starter contains `records.c`: a single 180-line `main` that reads a CSV, filters rows, computes
statistics, and prints a report. It works. It is also unmaintainable.

### Tasks

**(a)** Split it into modules with deliberate interfaces — at minimum `record.h/.c`, `stats.h/.c`,
and `report.h/.c`, plus a `main.c` that reads as a summary of the program. *(22 pts)*

**(b)** Every function private to a module must be `static`. In `answers.md`, list what you made
`static` and say what that buys. *(9 pts)*

**(c)** Apply the naming rules from Lecture 1. In `answers.md`, give three names you changed and the
reason for each. *(8 pts)*

**(d)** Replace at least one boolean parameter with two functions, or justify in `answers.md` why the
one you found should stay. *(7 pts)*

**(e)** Every header must have a guard and compile standalone. Demonstrate with `gcc -fsyntax-only`.
*(9 pts)*

**Constraint:** the refactored program must produce **byte-identical output** to the original on the
supplied test data. Prove it with `diff`.

---

## Problem 2: Harden It (45 pts)

Run the tools against your Problem 1 code and fix what they find.

**(a)** `-Wall -Wextra -Werror -pedantic -Wshadow -Wconversion`. Report every warning the extra two
flags produced and how you fixed each. *(14 pts)*

**(b)** `-fsanitize=address,undefined`. Report and fix. *(12 pts)*

**(c)** `valgrind --leak-check=full --show-leak-kinds=all`. Must end at zero errors and zero bytes
definitely lost. *(11 pts)*

**(d)** In `answers.md`: which tool found something the others did not, and why? *(8 pts)*

---

## Grading

| Problem | Topic | Points |
|---|---|---|
| 1 | Refactor for the Reader | 55 |
| 2 | Harden It | 45 |
| **Total** | | **100** |

**Automatic deductions:** any compiler warning (−2 each); any Valgrind error (−3 each); output not
byte-identical to the original in Problem 1 (−10).

---

*PROG 101 · Week 12 · Problem Set 12 · © CSE Department*

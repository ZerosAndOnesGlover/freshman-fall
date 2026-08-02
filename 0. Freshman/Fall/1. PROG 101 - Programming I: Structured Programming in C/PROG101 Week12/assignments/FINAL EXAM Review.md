# PROG 101 · Final Exam
## Review Guide

**Exam:** Finals week · **Duration:** 120 minutes
**Format:** Written, closed book. One handwritten A4 sheet, **both sides**.
**Covers:** Weeks 0–12, comprehensive · **Weight:** 20% of final grade

---

## Weighting

| Area | Weeks | ~Share |
|---|---|---|
| Types, integers, floating point | 1 | 12% |
| Operators, evaluation order, UB | 2 | 10% |
| Functions, call stack, scope | 3 | 10% |
| Arrays and strings | 4 | 12% |
| Pointers | 5 | 13% |
| Dynamic memory and ownership | 6 | 15% |
| Structures, unions, enums | 7 | 8% |
| File I/O | 8 | 7% |
| Recursion | 9 | 7% |
| Preprocessor and macros | 10 | 4% |
| Generic programming | 11 | 2% |

Weeks 6 and 5 together are nearly 30%. If revision time is short, that is where it goes.

---

## The Twelve Most Expensive Mistakes

1. **"Signed overflow wraps."** It is **undefined behaviour**; the compiler may delete your check.
2. **`p = realloc(p, n)`** — on failure you leak the original and lose your only pointer.
3. **Forgetting to free on an error path.** The `return` between two allocations.
4. **`strncpy` described as safe.** It does not terminate; it pads the whole buffer.
5. **`sizeof` on an array parameter.** It is the pointer size — 8.
6. **`&a` treated as `&a[0]`.** Same address, different type; `&a + 1` jumps the whole array.
7. **`while (!feof(f))`** — processes the last record twice.
8. **`return *a - *b;` in a comparator.** UB on overflow; verified to leave arrays unsorted.
9. **Assuming argument evaluation order.** It is **unspecified** — verified right-to-left here.
10. **A macro parameter used twice.** Double evaluation; parentheses cannot fix it.
11. **Confusing scope with lifetime.** A `static` local has narrow scope, program lifetime.
12. **Adding struct members to get `sizeof`.** Padding makes it larger.

---

## Verified Numbers Worth Memorising

| | |
|---|---|
| `sizeof` char/short/int/long/pointer | 1 / 2 / 4 / 8 / **8** |
| `-7 / 2`, `-7 % 2` | **−3**, **−1** |
| `char 100 + char 100` | **200**, type `int` (promotion) |
| `-1 < 1u` | **false** |
| `0.1 + 0.2 == 0.3` | **false** |
| Exact integers: `double` / `float` | 2⁵³ / 2²⁴ |
| `(int)3.99`, `(int)-3.99` | **3**, **−3** |
| `sizeof(int a[10])`: scope vs parameter | **40** vs **8** |
| `a + 1` vs `&a + 1` | **+4** vs **+40** |
| `struct {char;int;char}` | **12**; reordered **8** |
| `struct {char;double;char;short}` | **24** |
| `enum {RED, GREEN=5, BLUE}` | 0, 5, **6** |
| Naive `fib(20)` | **21,891** calls = 2·fib(21) − 1 |
| Doubling growth, 30 pushes | caps 4/8/16/32, **28** elements copied |
| `SQUARE_BAD(2+3)`, `100/SQUARE_BAD(5)` | **11**, **100** |
| `MAX(i++, 3)` with `i = 5` | returns 6, `i` ends at **7** |
| 2-line file with `<stdio.h>` | **815** preprocessed lines |

---

## The Build Line

```bash
gcc -Wall -Wextra -Werror -pedantic -std=c11 -g -O2 prog.c -o prog
gcc -fsanitize=address,undefined -g prog.c -o prog_san
valgrind --leak-check=full --show-leak-kinds=all --error-exitcode=1 ./prog
```

| Flag / tool | Catches | Note |
|---|---|---|
| `-Wsequence-point` | `i = i++ + 1` | "may be undefined" — best-effort |
| `-Wreturn-local-addr` | Returning `&local` | GCC then compiles it to `return NULL` |
| `-Wmaybe-uninitialized` | Uninitialised use | **Silent at `-O0`** — develop at `-O2` |
| `-Wsizeof-array-argument` | `sizeof` on a decayed parameter | |
| `-Wmultistatement-macros` | The `if`/`else` macro trap | |
| `-pedantic` | `%p` without `(void *)` | `-Wall -Wextra` do **not** catch this |
| ASan | Out-of-bounds, use-after-free | **Misses uninitialised reads** |
| UBSan | Overflow, bad shifts | |
| Valgrind | The above **plus uninitialised reads** | 20–50× slower |

---

## How to Revise

**Do not re-read notes.** Recognition is not recall.

1. **Work Midterm 1 and Midterm 2 cold**, under time, before looking at the keys. They are the best
   predictors of the final's shape.
2. **Redo the problem-set questions you got wrong.** Your marked copies are the highest-value
   material you own.
3. **Rebuild one thing from scratch** — a dynamic array, `strlib`, a linked list. Twenty minutes of
   this beats two hours of reading.
4. **Explain a topic aloud** without notes. Where you stall is the gap.

**The note sheet.** You get both sides this time. *Making* it is the revision. Put on it what you
cannot derive: the exact constants, the four `const` combinations, the `atomic`-style rules, the
sanitizer table above. Do not waste space on things you can reconstruct.

---

## Exam Technique

**Say "undefined behaviour" when it applies.** Several questions turn on it, and a confident numeric
answer where the standard gives none is the most expensive mistake available.

**State the case.** Signed or unsigned; in scope or as a parameter; best, average or worst.

**Name the tool.** "Valgrind reports *definitely lost*" earns more than "it would catch it".

**Show your reasoning.** Most questions award more for the argument than the answer, and a wrong
answer with sound reasoning often outscores a right answer with none.

Good luck.

---

*PROG 101 · Week 12 · Final Exam Review · © CSE Department*

# PROG 101 · Programming I: Structured Programming in C
## Week 1 · Problem Set 1: Types, Representation, and Conversions

**Released:** Thursday 1 October 2026, 11:00 (after Week 1 Lecture 3) · Week 1
**Due:** Friday 9 October 2026, 17:00 · Week 2 — late penalty from 17:01
**Submission:** Commit to the Freshman Fall repo under `"$PROG101/week1/ps1"`; submit the commit hash on the course portal.
**Points:** 100 · **Expected time:** about 3 hours

*(Revised 2026-09-26: cut to about three hours — Problem 2 item 4 and three of Problem 3's eight snippets
were removed — and the answer key moved out of this handout.)*

---

## What this problem set uses

Weeks 0–1 only: the compilation pipeline, `gcc`, `make` and `printf` (Week 0), and this week's types,
`sizeof`, `const`, `<limits.h>` (Lecture 01), two's complement, overflow, promotion and the
signed/unsigned trap, division and modulo signs (Lecture 02), floating point, `<float.h>`, `<math.h>`'s
`fabs` and `isnan`, infinity, NaN, negative zero, and conversions (Lecture 03).

**Every program is a single straight-line `main`.** No `if`, loops, `switch` or `?:` (Week 2), no functions of
your own (Week 3), no arrays or pointers (Weeks 4–5), no structs (Week 7). Where a program needs to report
a true/false result, print the comparison itself: `printf("%d\n", a < b);` prints `1` or `0`.

---

## Problem 1: Integer Types and Their Limits (20 pts)

Create `limits.c`. Print one row per type — `signed char`, `unsigned char`, `short`, `unsigned short`,
`int`, `unsigned int`, `long`, `long long` — with its `sizeof` (use `%zu`) and its minimum and maximum from
`<limits.h>`. Then print `sizeof` for `float` and `double`. Line the columns up with field widths.

In `ps1_answers.md`:

1. *(4 pts)* For a two's-complement type of `n` bits, give the formulas for its minimum and maximum. Check
   them against your `int` and `short` rows.
2. *(4 pts)* Why is the magnitude of `INT_MIN` one larger than `INT_MAX`?
3. *(4 pts)* Which of your rows does the C standard guarantee, and which only happen to hold on this
   machine? (Lecture 01 §3.)

*(8 pts for the program: correct format specifiers, `-Wall -Wextra` clean.)*

---

## Problem 2: Two's Complement by Hand (20 pts)

Answer in `ps1_answers.md`, **showing the bits**. Use 8-bit values throughout.

1. *(4 pts)* Write `42`, `-42`, `127`, `-128` and `-1` in binary. Show `-42` both ways: invert-and-add-one,
   and as `256 − 42`.
2. *(4 pts)* Add `100 + 30` in 8-bit binary. What bit pattern results, and what value does it mean as
   `unsigned char` and as `signed char`?
3. *(4 pts)* What are `(unsigned char)-1`, `(signed char)200` and `(unsigned char)300`? Which of these
   conversions does the standard define exactly, and which is implementation-defined? (Lecture 03 §4.)
4. *(8 pts)* The largest `unsigned int` plus one is `0`. The largest `int` plus one is *undefined
   behaviour*. Explain the difference in one or two sentences each (Lecture 02 §3).

---

## Problem 3: Predict, Then Run (21 pts)

Create `predictions.c` containing these snippets in one `main`. **Write your prediction in a comment above
each before you run it**, then record the real output and a one-sentence explanation in `ps1_answers.md`.

```c
/* Snippet 1 */
int a = -1;
unsigned int b = 1;
printf("1: a < b is %d\n", a < b);

/* Snippet 2 */
char c = 200;              /* char may be signed on your system */
printf("2: %d\n", c);

/* Snippet 3 */
unsigned int u = 0;
u = u - 1;
printf("3: %u\n", u);

/* Snippet 4 */
int x = (int)3.9;
int y = (int)-3.9;
printf("4: %d %d\n", x, y);

/* Snippet 5 */
printf("5: %d %d %d %d\n", 7 / 2, -7 / 2, 7 % 3, -7 % 3);
```

Compile with `-Wall -Wextra`. One snippet draws a warning: which, and what is the warning telling you?

*(4 pts per snippet — prediction, output, explanation — plus 1 for the warning.)*

---

## Problem 4: Floating Point (24 pts)

Create `floats.c`, a straight-line program that prints:

1. `0.1 + 0.2` with `%.17g`, whether it `== 0.3`, and whether `fabs(sum - 0.3) < 1e-9`
2. `DBL_EPSILON` and `FLT_EPSILON` from `<float.h>`
3. `16777216.0f + 1.0f` printed with `%.1f`
4. `DBL_MAX * 2`
5. `0.0 / 0.0` (compute it from a variable holding `0.0`), whether it equals itself, and `isnan` of it
6. `-0.0 == 0.0`, `-0.0` printed with `%f`, and `1.0 / -0.0`

Link with `-lm`. In `ps1_answers.md`, explain items 1, 3, 5 and 6 in a sentence each (Lecture 03 §2–3).

---

## Problem 5: Overflow, Seen by the Sanitizer (15 pts)

Create `overflow.c`: set `unsigned int u = UINT_MAX;` and `int i = INT_MAX;`, and print `u + 1` and `i + 1`.

1. *(5 pts)* Build with `gcc -Wall -std=c11 -fsanitize=undefined -g` and run it. Paste the runtime report.
   Which line does it name, and why only that one?
2. *(5 pts)* Build again with `-O2` and no sanitizer. What prints? Why does "it printed a number" prove
   nothing (Lecture 02 §3)?
3. *(5 pts)* Lecture 02 shows `if (x + 1 < x)` as a broken overflow check. Without writing an `if`, explain
   in two sentences why the compiler may delete it, and what the correct precondition test is.

---

## Makefile

Use this `Makefile` (TAB-indented recipes). `-Werror` is left off so that Problem 3's deliberate
warning still builds.

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -g -std=c11

PROGRAMS = limits predictions floats overflow

all: $(PROGRAMS)

floats: floats.c
	$(CC) $(CFLAGS) -o $@ $< -lm

overflow: overflow.c
	$(CC) $(CFLAGS) -fsanitize=undefined -o $@ $<

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGRAMS)

.PHONY: all clean
```

---

## Submission

- `limits.c`, `predictions.c`, `floats.c`, `overflow.c`, `Makefile`, `ps1_answers.md` in `"$PROG101/week1/ps1"`
- All four programs build with `make` and `-Wall -Wextra -std=c11` (Problem 3's one deliberate warning excepted)

## Grading

| Problem | Points |
|---|---|
| 1 Integer types and limits | 20 |
| 2 Two's complement by hand | 20 |
| 3 Predict, then run | 21 |
| 4 Floating point | 24 |
| 5 Overflow and the sanitizer | 15 |
| **Total** | **100** |

---

*PROG 101 · Week 1 · Problem Set 1 · Due Friday 9 October 2026, 17:00 · © CSE Department*

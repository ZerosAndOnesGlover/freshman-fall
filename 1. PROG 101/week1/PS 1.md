---
assessment: PS 1
course: PROG 101
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-01
submitted: 2026-10-08
graded: 2026-10-10
source: "Problem Set 1.md"
---

# PROG 101 · PS 1
## Answer Sheet

**Assessment:** `Problem Set 1.md`
**Points available:** 100

Code and the detailed write-up live in `1. PROG 101/week1/ps1/`:
`limits.c`, `predictions.c`, `floats.c`, `overflow.c`, `Makefile`, `ps1_answers.md`.

All four programs build with `make` (`gcc 15.2.0`, `-Wall -Wextra -g -std=c11`) and run; only
`predictions.c` emits the one intentional `-Wsign-compare` warning. Every output below is real.

---

### Problem 1 — Integer Types and Their Limits  (20 points)

`limits.c` prints one row per type (`sizeof` + `<limits.h>` bounds, columns field-width aligned):

```
type             bytes                    min                    max
signed char          1                   -128                    127
unsigned char        1                      0                    255
short                2                 -32768                  32767
unsigned short       2                      0                  65535
int                  4            -2147483648             2147483647
unsigned int         4                      0             4294967295
long                 8   -9223372036854775808    9223372036854775807
long long            8   -9223372036854775808    9223372036854775807
float                4
double               8
```

1. **Formulas:** min = −2ⁿ⁻¹, max = 2ⁿ⁻¹ − 1. `int` (n = 32) → −2147483648…2147483647 ✓;
   `short` (n = 16) → −32768…32767 ✓.
2. **One more negative than positive** because zero occupies one bit pattern (all zeros) in the
   non-negative half; the remaining 2ⁿ−1 patterns split into 2ⁿ⁻¹ − 1 positives and 2ⁿ⁻¹ negatives.
3. **Guaranteed:** `sizeof(char) == 1`; the minimum ranges (`int` ≥ 16 bits, `long` ≥ 32 bits);
   the ordering `short ≤ int ≤ long ≤ long long`. **Platform-specific (LP64 here):** the exact sizes
   (4-byte `int`, 8-byte `long`) and hence the exact limits — e.g. 64-bit Windows has a 4-byte `long`.

Full reasoning in `ps1_answers.md`.

*Marks: 20 / 20*

---

### Problem 2 — Two's Complement by Hand  (20 points)

1. `42 = 00101010`; `−42 = 11010110` (invert `00101010` → `11010101`, add 1; also `256 − 42 = 214`);
   `127 = 01111111`; `−128 = 10000000`; `−1 = 11111111`.
2. `01100100 + 00011110 = 10000010`. As `unsigned char` that is **130**; as `signed char` it is
   **−126** (a signed-range overflow — same bits, two meanings).
3. `(unsigned char)-1 = 255`; `(signed char)200 = −56`; `(unsigned char)300 = 44`. The two
   conversions **to unsigned** are exactly **defined** (reduce modulo 256); the conversion to a
   *signed* type out of range is **implementation-defined**.
4. `UINT_MAX + 1 == 0` is **defined** — unsigned arithmetic is modulo 2ⁿ. `INT_MAX + 1` is **undefined
   behaviour** — the standard defines no result and the compiler may assume it never happens.

*Marks: 20 / 20*

---

### Problem 3 — Predict, Then Run  (21 points)

Predictions were written as comments in `predictions.c` before running. Real output:

```
1: a < b is 0
2: -56
3: 4294967295
4: 3 -3
5: 3 -3 1 -1
```

1. `a` (`−1`) converts to unsigned `4294967295`, so `a < b` is false → `0`.
2. `char` is signed here; `200` doesn't fit → `200 − 256 = −56`.
3. Unsigned wraps modulo 2³² → `UINT_MAX`.
4. Cast truncates toward zero → `3 −3`.
5. Division truncates toward zero and `%` takes the dividend's sign → `3 −3 1 −1`.

**The warning** comes from snippet 1:
`warning: comparison of integer expressions of different signedness: 'int' and 'unsigned int'
[-Wsign-compare]`. It says C converts the `int` operand to `unsigned` before comparing, so a negative
value silently becomes huge — the comparison is not comparing what it appears to.

*Marks: 21 / 21*

---

### Problem 4 — Floating Point  (24 points)

Real output of `floats.c` (linked with `-lm`):

```
0.1 + 0.2       = 0.30000000000000004
== 0.3?           0
|sum - 0.3| < 1e-9? 1
DBL_EPSILON     = 2.22045e-16
FLT_EPSILON     = 1.19209e-07
16777216f + 1   = 16777216.0
DBL_MAX * 2     = inf
0.0 / 0.0       = -nan; nan == nan is 0; isnan is 1
-0.0 == 0.0 is 1, printed as -0.000000, 1/-0.0 = -inf
```

1. Neither `0.1` nor `0.2` is exact in binary, so the sum is the nearest double to
   `0.30000000000000004`; `== 0.3` is false — compare with a tolerance instead.
3. `16777216 = 2²⁴` is the largest integer a 24-bit-significand `float` represents exactly; above it
   the gap is ≥ 1, so `+1.0f` rounds back to `16777216.0`.
5. `0.0 / 0.0` is invalid and yields **NaN**, which is unequal to everything (incl. itself), so
   `nan == nan` is `0` and only `isnan()` (`1`) is reliable; glibc prints `-nan`.
6. `-0.0 == 0.0` is **true**, but the sign bit is kept: it prints `-0.000000` and `1.0 / -0.0 = -inf`.

*Marks: 24 / 24*

---

### Problem 5 — Overflow, Seen by the Sanitizer  (15 points)

1. **UBSan report** (`-fsanitize=undefined -g`):
   `overflow.c:16:5: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in
   type 'int'`. Only the **signed** line is named, because unsigned wrap is defined arithmetic, not an
   error.
2. **`-O2`, no sanitizer:** prints `unsigned: UINT_MAX + 1 = 0` and `signed: INT_MAX + 1 = -2147483648`.
   That proves nothing: the computation is undefined behaviour, so any result is legal. The `-O2`
   assembly shows gcc **constant-folded** `INT_MAX + 1` into a literal `movl $-2147483648, %edx` — it
   baked in one arbitrary answer; a different compiler/optimisation could as validly print anything.
3. `x + 1 < x` can only be true *after* an overflow, which a well-defined program never does, so the
   compiler may assume it is always false and delete the check. The correct test is a **precondition**
   on the operand using `<limits.h>` — e.g. `if (x > INT_MAX - 1)` — before incrementing at all.

*Marks: 15 / 15*

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-10 |

**Feedback:**
Excellent. All five problems complete and backed by real tool output. Problem 1 reproduces the
limits table with correct `%zu`/bound specifiers and separates portable guarantees from LP64
specifics; Problem 2 shows the bits for every value including `−42` both ways and correctly splits
defined-vs-implementation-defined conversions; Problem 3 gives predictions before output, correct
explanations, and the right warning (`-Wsign-compare`); Problem 4 explains rounding error, the 2²⁴
float boundary, NaN and negative zero; Problem 5 correctly identifies the signed line as the only
UBSan report and explains why `-O2` "printing a number" is luck plus the deletion of `x + 1 < x`.
Clear, precise, well-documented.

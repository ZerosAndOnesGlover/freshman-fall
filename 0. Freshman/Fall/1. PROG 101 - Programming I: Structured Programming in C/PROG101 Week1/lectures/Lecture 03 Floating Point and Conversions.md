# PROG 101 — Programming I: Structured Programming in C
## Week 1 · Lecture 3: Floating-Point and Type Conversions

---

## Lecture Goals

By the end of this lecture you can:

- Explain why `0.1 + 0.2 != 0.3`, and predict which values *are* exact
- State the precision limits of `float` and `double` in digits and in integers
- Handle infinity, NaN, and negative zero without being surprised
- Apply C's conversion rules deliberately instead of discovering them through bugs

---

## 1. Floating-Point Types

| Type | Bytes | Decimal digits | Max |
|---|---|---|---|
| `float` | 4 | ~6 | 3.40 × 10³⁸ |
| `double` | 8 | ~15 | 1.80 × 10³⁰⁸ |
| `long double` | 16 | ~18 | (larger) |

All measured on this machine via `<float.h>`.

The representation is IEEE 754: a **sign bit**, an **exponent**, and a **fraction**, encoding

```
value = ±  1.fraction  ×  2^exponent
```

For `double`: 1 sign bit, 11 exponent bits, 52 fraction bits.

**Use `double` by default.** A `float` buys you four bytes and costs you nine decimal digits, and on
modern hardware it is rarely faster for scalar code. Reach for `float` only when you have measured a
memory or bandwidth problem — large arrays, GPU data, audio buffers.

Note also that an unsuffixed literal like `3.14` is a **`double`**. Writing `float x = 3.14;`
computes in `double` and then narrows. If you really want a `float` literal, write `3.14f`.

---

## 2. Why `0.1 + 0.2 != 0.3`

Verified:

```
0.1 + 0.2 == 0.3 ?  FALSE
0.1 + 0.2 = 0.30000000000000004441
0.3       = 0.29999999999999998890
```

The cause is not sloppy hardware. It is that **0.1 has no exact binary representation**, in the same
way ⅓ has no exact decimal representation. In binary, 0.1 is the repeating fraction

```
0.0001100110011001100110011... 
```

which must be cut off at 52 fraction bits. So `0.1` is stored as *the nearest representable double*,
which is very slightly more than a tenth. Same for `0.2`. Their sum is slightly more than 0.3, and
the nearest double to `0.3` is slightly *less* than three tenths. The two differ.

### What is exact

Not everything is approximate — the rule is precise:

**Values that are exact:** any number expressible as an integer times a power of two, within range.

```
0.5 + 0.25 == 0.75 ?  true
```

`0.5`, `0.25`, `0.75`, `3.0`, `-16.0` are all stored exactly. Money in cents, halves and quarters,
and all small integers are fine.

**Integers are exact up to 2⁵³.** Verified:

```
2^53     = 9007199254740992    stored exactly
2^53 + 1 = 9007199254740992    <- the +1 is LOST
```

A `double` can hold every integer up to 9,007,199,254,740,992 exactly. Past that, consecutive
integers start sharing representations. This is why JavaScript — which has only doubles — cannot
represent large database IDs, and why JSON integers beyond 2⁵³ are a portability hazard.

For `float` the limit is far lower — 2²⁴:

```
(float)(2^24 + 1) = 16777216   <- lost at only 16.7 million
```

A `float` cannot count reliably past 16 million. Storing a large ID or a nanosecond timestamp in a
`float` silently corrupts it.

### Non-associativity

This is the consequence that breaks algorithms. Verified:

```
(1e16 + -1e16) + 1 = 1
 1e16 + (-1e16 + 1) = 0     <- different
```

**Floating-point addition is not associative.** In the second form, `-1e16 + 1` rounds back to
exactly `-1e16` — the 1 is too small to affect a number that large — so the sum is 0.

Consequences you will meet:

- Summing an array in a different order gives a different total
- Parallel reductions are non-deterministic unless the order is fixed
- The compiler may **not** reorder float arithmetic under `-O2`, because doing so would change
  results. (`-ffast-math` permits it, and thereby breaks exactly this guarantee — which is why you
  should not enable it casually.)

**Summing small values into a large accumulator loses them.** If you need accuracy over a long
array, sort by magnitude or use compensated summation (Kahan's algorithm).

### Never compare floats with `==`

```c
if (x == 0.3) ...              /* fragile */
```

Compare against a tolerance instead:

```c
#include <math.h>
if (fabs(x - y) < 1e-9) ...    /* absolute tolerance */
```

Verified: `fabs((0.1+0.2) - 0.3)` is `5.55e-17`, comfortably under `1e-9`.

**But absolute tolerance is wrong for large values.** At magnitude 10⁷, a relative error of 10⁻¹⁰ is
an absolute error of 10⁻³ — which fails a `1e-9` test while being perfectly accurate. Use a relative
test when magnitudes vary:

```c
if (fabs(x - y) <= 1e-9 * fabs(y)) ...
```

Choosing between them requires knowing your data's scale. That judgement is the actual skill.

---

## 3. Infinity, NaN, and Negative Zero

IEEE 754 defines values that are not numbers. Verified:

```
1.0/0.0 = inf     isinf = 1
0.0/0.0 = -nan    isnan = 1
```

**Division by zero does not crash** for floating point — unlike integer division by zero, which is
undefined behaviour and usually does crash. Floats produce `inf` or `NaN` and carry on.

### NaN is not equal to itself

```
nan == nan ?  FALSE
```

This is deliberate and it is the standard idiom for detecting it, though `isnan()` says it better:

```c
if (x != x) { /* x is NaN */ }     /* works, but obscure */
if (isnan(x)) { /* clearer */ }
```

The consequence that bites: **NaN poisons comparisons.** Every one of `<`, `>`, `<=`, `>=`, `==`
returns false when an operand is NaN. So `if (x < 0) … else …` takes the `else` branch for NaN, which
is usually not what the author meant. A NaN entering a sort comparator produces an inconsistent
ordering and can drive the sort out of bounds — the same hazard as the bad comparator you will meet
in Week 11.

### Negative zero

```
-0.0 == 0.0 ?  true      but signbit: 1 vs 0
```

Two distinct bit patterns that compare equal. They differ in `1.0/x` — one gives `+inf`, the other
`-inf` — and in `signbit()`. Rarely matters, but when it does it is baffling unless you know.

---

## 4. Type Conversions

C converts between types constantly, sometimes silently. There are two kinds.

### Implicit: the usual arithmetic conversions

When operands differ, C promotes to a "common" type by rank:

```
long double  >  double  >  float  >  unsigned long  >  long  >  unsigned int  >  int
```

The lower-ranked operand converts up. So:

```c
3 / 2      /* 1    -- both int: INTEGER division */
3 / 2.0    /* 1.5  -- 2.0 is double, so 3 converts to double */
```

Verified. **This is the most common beginner bug in numeric C code:**

```c
double average = sum / count;      /* if both are int, the division happens FIRST, in int */
double average = (double)sum / count;   /* correct */
```

The cast must be on an operand, not the result. Casting the result converts an already-truncated
integer.

### Explicit: casts

```c
(int)3.99   =  3      /* truncates toward zero, does NOT round */
(int)-3.99  = -3
```

Verified. To round, use `round()`, `floor()`, or `ceil()` from `<math.h>`. Note `(int)(x + 0.5)` is
the classic hand-rolled rounding and it is **wrong for negatives** — `(int)(-3.6 + 0.5)` gives `-3`,
not `-4`.

### Narrowing loses data silently

```
int 1000000001 -> float -> int = 1000000000
```

The value passed through a `float`, which has ~7 digits, and came back different. No warning by
default, no error — the low digit is simply gone.

### Out-of-range conversions are undefined

```c
double huge = 1e20;
int    x    = (int)huge;    /* UNDEFINED BEHAVIOUR -- not "some large int" */
```

Converting a floating value to an integer type is undefined when the truncated value cannot be
represented. Check the range first:

```c
if (huge >= INT_MIN && huge <= INT_MAX) x = (int)huge;
```

---

## 5. Summary

| Idea | Takeaway |
|---|---|
| Default to `double` | `float` buys 4 bytes, costs 9 digits |
| `3.14` is a `double` | Write `3.14f` for a float literal |
| `0.1` is inexact | Binary cannot represent tenths, as decimal cannot represent thirds |
| Exact values | Integer × power of two — halves, quarters, small integers |
| Integer limit | Exact to **2⁵³** in `double`, only **2²⁴** in `float` |
| Non-associative | `(a+b)+c != a+(b+c)`; summation order changes the answer |
| Never `==` | Use `fabs(x-y) < tol`; relative tolerance when magnitudes vary |
| `1.0/0.0` | `inf` — floats do not trap; integer division by zero is UB |
| NaN | Not equal to itself; poisons **every** comparison |
| `-0.0` | Equals `0.0` but has a different sign bit |
| `3/2` is `1` | Integer division happens before assignment to a `double` |
| `(int)3.99` is `3` | Truncates toward zero; does not round |
| Out-of-range cast | **Undefined behaviour**, not a large number |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** State the value and type of each: (a) `7 / 2`  (b) `7 / 2.0`  (c) `7.0 / 2`
(d) `(double)(7 / 2)`  (e) `(double)7 / 2`

**2. (Explain.)** A student writes `float total = 0.0f;` and adds `0.01f` to it 1,000,000 times,
expecting 10000.0. Explain what actually happens and why, and give two different fixes.

**3. (Fix.)** Three bugs.

```c
int    count = 7;
int    sum   = 30;
double avg   = sum / count;
if (avg == 4.285714) printf("exact\n");
int rounded = (int)(avg + 0.5);
```

**4. (Stretch.)** Write a `nearly_equal` predicate for two `double`s. Handle NaN, both infinities,
and the case where one or both values are at or near zero. Decide for yourself what parameters it
needs — the choice is part of the exercise.

### Answers

**1.**

| | Value | Type | Why |
|---|---|---|---|
| **(a)** `7 / 2` | **3** | `int` | Both operands `int` → integer division, truncates |
| **(b)** `7 / 2.0` | **3.5** | `double` | `2.0` is `double`, so `7` converts up |
| **(c)** `7.0 / 2` | **3.5** | `double` | Same, other side |
| **(d)** `(double)(7 / 2)` | **3.0** | `double` | Division happens **first** in `int`; the cast converts the already-truncated 3 |
| **(e)** `(double)7 / 2` | **3.5** | `double` | Cast binds to the operand, so the division is in `double` |

**(d) vs (e) is the whole lesson.** The cast must reach an operand *before* the division. This is
exactly the `sum / count` bug from §4.

**2.** Measured result: **9865.2236**, not 10000.0 — an error of about **1.3%**.

`0.01f` is not exactly one hundredth. It is stored as the nearest `float`, which is slightly off, and
that error compounds across a million additions. Each individual addition also rounds its result to
24 bits of precision, so error accrues from two sources at once.

**A caveat on the usual explanation.** It is often said that the sum "stalls" — that `total` grows
until `0.01f` is too small to register, after which additions do nothing. That effect is real, but it
does **not** happen here. It requires `total` to exceed roughly 2¹⁷·⁴ ≈ 170,000, and this sum only
reaches ~9,865. Instrumenting the loop confirms it: **no** addition ever left `total` unchanged. The
error here is pure accumulation, not saturation. *(Try the same loop targeting 10⁶ and you will see
the stall.)*

**Two fixes:**

**Two fixes:**

1. **Use `double`.** With 53 bits of precision instead of 24, the per-addition rounding error drops
   by a factor of ~2²⁹ and the total lands within about 10⁻⁶ of 10000. Simplest fix, and usually the
   right one.
2. **Do not accumulate at all** — compute `count * 0.01` directly, or work in integers (count
   hundredths as `int`, divide once at the end). Exact, and the correct approach for money.

*Also acceptable:* Kahan compensated summation, which tracks the lost low-order bits in a second
variable. Mention it, but note that switching to `double` is cheaper and usually sufficient.

**3.**

- **`sum / count` is integer division.** Both are `int`, so it computes `30/7 = 4`, then converts 4
  to `4.0`. The fractional part is lost before the assignment ever happens.
  → `double avg = (double)sum / count;`
- **`avg == 4.285714` will essentially never be true.** The true value is 4.2857142857…, and the
  literal is a truncation of it. Comparing floats for equality with a decimal literal is hopeless.
  → `if (fabs(avg - 4.285714) < 1e-6)`
- **`(int)(avg + 0.5)` is wrong for negative values.** It happens to work here (giving 4), but as a
  rounding idiom it fails: `(int)(-3.6 + 0.5)` is `-3`, not `-4`.
  → `int rounded = (int)round(avg);` — and `#include <math.h>`, linking with `-lm`.

**4.**

**The parameter choice is the point of the exercise: it needs *two* tolerances.**

```c
#include <math.h>

int nearly_equal(double a, double b, double rel_tol, double abs_tol)
{
    if (isnan(a) || isnan(b)) return 0;      /* NaN equals nothing, including itself */
    if (a == b) return 1;                    /* exact, and handles both infinities   */
    if (isinf(a) || isinf(b)) return 0;      /* one inf, one finite -> not equal      */

    double diff = fabs(a - b);
    if (diff <= abs_tol) return 1;           /* near-zero case                        */

    double scale = fabs(a) > fabs(b) ? fabs(a) : fabs(b);
    return diff <= rel_tol * scale;
}
```

**Why each guard is needed:**

- **NaN first.** Without it, `a == b` is false and the arithmetic below produces NaN, so the final
  comparison is false — accidentally correct, but by luck rather than design.
- **`a == b` before anything else** catches exact equality cheaply, and correctly returns 1 for
  `+inf == +inf`, which the relative test could not (`inf - inf` is NaN).
- **Scaling by the larger magnitude** makes the function symmetric: `nearly_equal(a,b)` and
  `nearly_equal(b,a)` agree. Verified over 200,000 random pairs — zero asymmetries.

**Why a relative tolerance alone cannot work.** If the true value is zero there is nothing to be
relative *to*: `rel_tol * scale` shrinks to zero alongside the values, so the test can never succeed
no matter how close the numbers get. Comparing `0.0` against `1e-300` fails a purely relative test,
because they differ by 100% relatively — which is arithmetically true and practically useless.

A tempting patch is to special-case "both smaller than `DBL_MIN`", but `DBL_MIN` ≈ 2.2 × 10⁻³⁰⁸ is
far too strict a threshold: `1e-300` sails past it and still fails. The genuine fix is a **separate
absolute tolerance**, chosen by the caller, who is the only one who knows what "close to zero" means
for their data.

That is exactly why real test frameworks take both — Python's `math.isclose` has `rel_tol` *and*
`abs_tol`, and its documentation notes that `abs_tol` defaults to `0.0`, so comparisons against zero
fail unless you supply one. Verified on 14 edge cases including both infinities, both NaN
combinations, signed zeros, and near-zero pairs: all correct.

*Reject a single-tolerance answer even if it is otherwise elegant* — discovering that one tolerance
is insufficient is the entire lesson.

---

## Reading

- **K&R, §2.7** — type conversions
- **`<float.h>`** — read it: `FLT_DIG`, `DBL_DIG`, `DBL_EPSILON`
- **Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic"** — the
  standard reference; §1–2 are enough for now
- **C11 §6.3.1.8** — the usual arithmetic conversions, in full

---

*PROG 101 · Week 1 · Lecture 3 · © CSE Department*

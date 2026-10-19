# PROG 101 · Week 1 · Problem Set 1 — Written Answers

**Name:** Adebayo Glover · **Set:** Problem Set 1 (Types, Representation, Conversions)
**Toolchain:** `gcc 15.2.0`, GNU Make 4.4.1, x86-64 Linux (LP64). Every number below is a real
output from the programs in this folder (`limits.c`, `predictions.c`, `floats.c`, `overflow.c`),
built with `make` (`-Wall -Wextra -g -std=c11`).

---

## Problem 1 — Integer Types and Their Limits

`limits.c` prints one row per type with its `sizeof` and its `<limits.h>` bounds:

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

### 1. Formulas for an `n`-bit two's-complement type

$$\text{min} = -2^{\,n-1}, \qquad \text{max} = 2^{\,n-1} - 1.$$

* `int` (n = 32): min = −2³¹ = **−2147483648**, max = 2³¹ − 1 = **2147483647** — matches the row.
* `short` (n = 16): min = −2¹⁵ = **−32768**, max = 2¹⁵ − 1 = **32767** — matches the row.

### 2. Why `|INT_MIN|` is one larger than `INT_MAX`

Zero has to occupy exactly one bit pattern (all zeros), and that pattern sits in the
non-negative half. With 2ⁿ patterns total, the split is **one** zero, **2ⁿ⁻¹ − 1** positive values,
and **2ⁿ⁻¹** negative values — so there is one more negative value than positive, and the most
negative value has no positive counterpart.

### 3. Guaranteed by the standard vs. true only on this machine

**Guaranteed (portable):**
* `sizeof(char) == 1` (a byte is a `char`).
* Minimum ranges: `signed char`/`short`/`int` at least **−127…127** (so `int` is at least 16 bits),
  and `long` at least **−2147483647…2147483647** (32 bits).
* The ordering `sizeof(short) ≤ sizeof(int) ≤ sizeof(long) ≤ sizeof(long long)`.

**Only happen on this machine (LP64):**
* The exact sizes — 4-byte `int`, 8-byte `long` — and therefore the exact limits
  (`2147483647`, `9223372036854775807`, …). A 64-bit Windows build has a 4-byte `long`, and the
  standard only fixes the *minimum* widths, not the exact ones.

---

## Problem 2 — Two's Complement by Hand (8-bit)

### 1. Values in binary

| value | 8-bit two's complement |
|---|---|
| `42` | `00101010` |
| `−42` | `11010110` |
| `127` | `01111111` |
| `−128` | `10000000` |
| `−1` | `11111111` |

`−42`, both ways:
* **Invert and add one:** `42 = 00101010` → invert → `11010101` → add `1` → **`11010110`**.
* **As 256 − 42:** `256 − 42 = 214`, and `214 = 11010110`.

### 2. `100 + 30` in 8-bit binary

```
  01100100   (100)
+ 00011110   (30)
-----------
  10000010
```

The bit pattern is **`10000010`**. It means **130** as `unsigned char`, and as `signed char` it means
**−126** (`10000010` = −(256 − 130) = −126) — a signed-range overflow, and a perfect example of the
same bits meaning two different things.

### 3. Conversions

* `(unsigned char)-1` = **255**
* `(signed char)200` = **−56** (on gcc / this machine)
* `(unsigned char)300` = **44**

**Defined exactly by the standard:** the two conversions **to unsigned** (`-1` and `300`). Converting
to an unsigned type is done modulo 2ⁿ: `−1 mod 256 = 255` and `300 mod 256 = 44`, on every conforming
implementation.

**Implementation-defined:** the conversion to a *(signed)* type when the value is out of range —
`(signed char)200`. Here gcc wraps it to `−56`, but the standard only requires the implementation to
document what it does.

### 4. Unsigned wrap vs. signed overflow

* **`UINT_MAX + 1 == 0`** — unsigned arithmetic is defined to be **modulo 2ⁿ**, so the result is
  computed by definition and is exactly `0` on every conforming compiler.
* **`INT_MAX + 1`** — signed overflow is **undefined behaviour**. The standard does not define a
  result at all; the compiler is permitted to assume overflow never happens and optimise on that
  assumption, so *any* result (or none) is legal.

---

## Problem 3 — Predict, Then Run

Refined predictions were written as comments in `predictions.c` before running. Real output:

```
1: a < b is 0
2: -56
3: 4294967295
4: 3 -3
5: 3 -3 1 -1
```

| # | Output | Explanation |
|---|---|---|
| 1 | `0` | `b` is `unsigned`, so `a` (`−1`) is **converted to unsigned** → `4294967295`; `a < b` is false. |
| 2 | `−56` | `char` is signed here; the constant `200` does not fit, so it is stored as `200 − 256 = −56`. |
| 3 | `4294967295` | Unsigned arithmetic is modulo 2³²; `0 − 1` wraps to `UINT_MAX`. |
| 4 | `3 −3` | The cast to `int` **truncates toward zero**: `3.9 → 3`, `−3.9 → −3`. |
| 5 | `3 −3 1 −1` | Integer division truncates toward zero (`−7 / 2 = −3`); `%` takes the **sign of the dividend** (`−7 % 3 = −1`). |

**The warning — Snippet 1.** It is the only snippet that warns:

```
predictions.c:15:34: warning: comparison of integer expressions of different
signedness: 'int' and 'unsigned int' [-Wsign-compare]
```

It is telling us that C's *usual arithmetic conversions* turn the `int` operand into an `unsigned int`
before comparing, so a negative value silently becomes huge. The comparison does **not** mean what the
source looks like it means — exactly the trap the runtime output (`0`) demonstrates.

---

## Problem 4 — Floating Point

Real output of `floats.c`:

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

**Item 1.** Neither `0.1` nor `0.2` is exactly representable in binary, so their sum is the nearest
`double` to the true value — `0.30000000000000004` — and therefore `sum == 0.3` is false. The fix is a
tolerance test: `fabs(sum - 0.3) < 1e-9` is true.

**Item 3.** `16777216 = 2²⁴` is the largest integer a 32-bit `float` can represent with a 24-bit
significand; above it the gap between consecutive floats is ≥ 1, so `+1.0f` rounds straight back to
`16777216.0f` and no change is visible.

**Item 5.** `0.0 / 0.0` is an invalid operation and yields **NaN**. NaN is unequal to *everything*,
including itself, so `nan == nan` is `0`; the only correct test is `isnan()` (here `1`). glibc prints
it as `-nan` because the sign bit happens to be set — accept either `nan` or `-nan`.

**Item 6.** `-0.0 == 0.0` is **true** (they compare equal), but the **sign bit is retained**:
printing gives `-0.000000`, and `1.0 / -0.0 = -inf`, which is how the sign shows up.

---

## Problem 5 — Overflow, Seen by the Sanitizer

`overflow.c` sets `unsigned int u = UINT_MAX;` and `int i = INT_MAX;` and prints `u + 1` and `i + 1`.

### 1. UBSan report

```
$ gcc -Wall -std=c11 -fsanitize=undefined -g -o overflow overflow.c && ./overflow
overflow.c:16:5: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
unsigned: UINT_MAX + 1 = 0
signed:   INT_MAX + 1  = -2147483648
```

It names the **signed** line (line 16, the `i + 1` printf) **only**, because unsigned wrap-around is
*defined* arithmetic (modulo 2ⁿ) and is not an error, while signed overflow is undefined behaviour and
UBSan reports exactly that.

### 2. `-O2`, no sanitizer

```
$ gcc -Wall -Wextra -std=c11 -O2 -o overflow_O2 overflow.c && ./overflow_O2
unsigned: UINT_MAX + 1 = 0
signed:   INT_MAX + 1  = -2147483648
```

It prints the same numbers here — but that proves nothing. This computation is **undefined behaviour**,
so the compiler is free to produce *any* value (or to delete or reorder the code); the fact that a
plausible-looking number came out is luck, not a guarantee. Looking at the `-O2` assembly shows why:
gcc **constant-folded** `INT_MAX + 1` at compile time into a literal `movl $-2147483648, %edx` — it did
the wrap itself and baked the answer in. A different compiler, or a later optimisation, could just as
validly print `0` or `0x7fffffff+1` or anything else.

### 3. Why `if (x + 1 < x)` is a broken overflow check

After a signed overflow the behaviour is undefined, so a *correct* program never overflows; the
compiler may therefore assume the overflow **never happens**. Under that assumption `x + 1 < x` can
never be true, so the optimiser is entitled to treat the condition as constant `false` and delete the
enclosed code entirely.

The right way is a **precondition test on the operand, before incrementing**, using `<limits.h>`:

```c
if (x > INT_MAX - 1) {            /* i.e. x >= INT_MAX */
    /* about to overflow — don't add */
}
```

This never performs the overflowing addition, so it stays well-defined.

---

*PROG 101 · Week 1 · Problem Set 1 · Adebayo Glover*

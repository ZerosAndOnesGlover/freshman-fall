---
assessment: Quiz 1
course: PROG 101
component: Quizzes
possible: 20
score: 20
status: graded
started: 2026-10-06
submitted: 2026-10-06
graded: 2026-10-06
source: "QUIZ 1.md"
---

# PROG 101 · Quiz 1
## Answer Sheet

**Assessment:** `QUIZ 1.md`
**Points available:** 20 (10 questions × 2)

---

## Section A — Multiple Choice

### Question 1  (2 pts)

**`sizeof(long)` on a 64-bit Linux system?**

**Answer: (B) 8.** On 64-bit Linux the model is LP64, so `long` is 8 bytes. (It is 4 bytes under the
LLP64 model used by 64-bit Windows, and on 32-bit systems.)

*Marks: 2 / 2*

### Question 2  (2 pts)

**Decimal value of the 8-bit two's complement pattern `11111110`?**

**Answer: (C) −2.** MSB weight −128 plus 64+32+16+8+4+2 = 126 → −128 + 126 = **−2**. (Or invert to
`00000001`, add 1 → 2, so the original is −2.)

*Marks: 2 / 2*

### Question 3  (2 pts)

**What does this print?**

```c
unsigned int x = 0;
x = x - 1;
printf("%u\n", x);
```

**Answer: (C) 4294967295.** Unsigned arithmetic is modular; `0 − 1` wraps to `UINT_MAX = 2³² − 1`.
This is well-defined (not UB).

*Marks: 2 / 2*

### Question 4  (2 pts)

**Which is undefined behaviour?**

**Answer: (B) `int x = INT_MAX; x = x + 1;`** — signed integer overflow is undefined. The unsigned
cases (A `UINT_MAX + 1` and C `0u - 1`) are defined modular wraparound.

*Marks: 2 / 2*

### Question 5  (2 pts)

**`(int)3.9` and `(int)-3.9`?**

**Answer: (C) `3` and `-3`.** Converting a floating value to an integer **truncates toward zero**.

*Marks: 2 / 2*

---

## Section B — Short Answer

### Question 6  (2 pts)

**`printf("%d %d\n", -7 / 2, -7 % 2);`**

**Output:** `-3 -1`
**Rule for the sign of `%`:** the sign of `a % b` follows the sign of the **dividend `a`**
(division truncates toward zero), so `(-3)*2 + (-1) == -7`.

*Marks: 2 / 2*

### Question 7  (2 pts)

**`int a = -1; unsigned int b = 1; printf("%d\n", a < b);`**

**Output:** `0`
**Why:** the signed `a` (`−1`) is converted to `unsigned` (`4294967295`) before the comparison (usual
arithmetic conversions), and `4294967295 < 1` is false.

*Marks: 2 / 2*

### Question 8  (2 pts)

**Why is `0.1 + 0.2 == 0.3` equal to `0`?**

**Reason:** neither `0.1` nor `0.2` has an exact binary representation, so their rounded sum is not the
double nearest to `0.3`.
**Instead:** compare with a tolerance — `fabs((0.1 + 0.2) - 0.3) < 1e-9`.

*Marks: 2 / 2*

### Question 9  (2 pts)

**Values and defined vs. implementation-defined.**

```
(unsigned char)300  = 44
(signed char)200    = -56   (on gcc, x86-64)
Defined exactly: (unsigned char)300    Implementation-defined: (signed char)200
```

Conversion **to an unsigned** type is defined exactly (reduce modulo 256 → `300 − 256 = 44`).
Conversion of an out-of-range value **to a signed** type is implementation-defined (gcc gives −56).

*Marks: 2 / 2*

### Question 10  (2 pts)

**What does each line print?**

```c
int a = 5, b = 3;
printf("%d\n", a / b);
printf("%f\n", (double)a / b);
printf("%d\n", a % b);
```

```
Line 1: 1         Reason: integer division truncates toward zero: 5/3 = 1.
Line 2: 1.666667  Reason: the cast promotes a to double, so the division is floating point.
Line 3: 2         Reason: remainder — 5 = 3×1 + 2, so 5 % 3 = 2.
```

*Marks: 2 / 2*

---

## Grading Summary

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-10-06 |

**Feedback:**
Full marks. All five multiple-choice answers correct with sound reasoning — LP64 `long`, two's-
complement `11111110` = −2, unsigned wraparound to `UINT_MAX`, signed overflow as the UB case, and
truncate-toward-zero casting. The short answers are all right: the `%`-sign rule (follows the dividend)
is stated, the signed→unsigned promotion explains the `a < b` result, the floating-point rounding
reason is given with the correct tolerance comparison, the defined vs implementation-defined
conversions are separated with the right values (44, −56), and the three `printf` lines are correct
including the `(double)` promotion.

---
assessment: Quiz 2
course: PROG 101
component: Quizzes
possible: 20
score: 20
status: graded
started: 2026-10-13
submitted: 2026-10-13
graded: 2026-10-13
source: "QUIZ 2.md"
---

# PROG 101 · Quiz 2
## Answer Sheet

**Assessment:** `QUIZ 2.md` (covers Week 2: operators, bit manipulation, evaluation order/UB, control flow)
**Points available:** 20 (10 questions × 2)

All values verified by compiling and running the snippets.

---

## Section A — Multiple Choice

### Question 1  (2 pts)

**`int a = 5, b = 3;` — `a > 3 && b > 3 || a == 5`?**

**Answer: (B) 1.** `&&` binds tighter than `||`, so it parses as `(5 > 3 && 3 > 3) || 5 == 5`
= `(1 && 0) || 1` = `0 || 1` = **1**.

*Marks: 2 / 2*

### Question 2  (2 pts)

**`1 << 3 + 1`?**

**Answer: (B) 16.** `+` binds tighter than `<<`, so it is `1 << (3 + 1)` = `1 << 4` = **16**.
(GCC `-Wall` warns here: `-Wparentheses` suggests parentheses around `+` inside `<<`.)

*Marks: 2 / 2*

### Question 3  (2 pts)

**Which is undefined behaviour?**

**Answer: (B) `int i = 5; i = i++;`** — `i` is modified twice with no sequence point between the two
writes, so the line has no defined meaning (GCC: `-Wsequence-point`). (A) `u = u - 1` on an `unsigned`
is defined modular wraparound; (C) `7 % -2` is `1`; (D) `(1 > 0) ? 10 : 20` is `10`.

*Marks: 2 / 2*

### Question 4  (2 pts)

**`int i = 3; int j = i++ * 2;` — `i` and `j`?**

**Answer: (C) `i = 4, j = 6`.** Post-increment yields the **old** value (3) for the multiplication, then
increments — so `j = 6` and `i = 4`.

*Marks: 2 / 2*

### Question 5  (2 pts)

**`int k = 0;` — `(k != 0) && (10 / k > 1)`?**

**Answer: (B) evaluates to `0` without dividing.** `&&` **short-circuits**: the left operand `k != 0` is
false, so the right operand (and its division by zero) is never evaluated. The whole expression is `0`.

*Marks: 2 / 2*

---

## Section B — Short Answer

### Question 6  (2 pts)

**`unsigned x = 0x5A;` (binary `0101 1010`) — decimal values:**

```
x & 0x0F = 10      (0000 1010)   keep low nibble
x | 0x0F = 95      (0101 1111)   set low nibble
x ^ 0xFF = 165     (1010 0101)   invert all eight bits
x >> 4   = 5       (0000 0101)   logical shift right by 4
```

*Marks: 2 / 2*

### Question 7  (2 pts)

```c
int n = 0;
do { n++; } while (n < 0);
printf("%d\n", n);
```

**Output:** `1`
**Why:** a `do-while` tests its condition **after** the body, so the body runs **once** even though
`n < 0` is false afterwards (the condition is never true; the loop runs exactly once).

*Marks: 2 / 2*

### Question 8  (2 pts)

```c
int total = 0;
for (int t = 0; t < 10; t++) {
    if (t % 2) continue;
    if (t > 6) break;
    total += t;
}
```

**`total = 12`.** Only even `t` survive the `continue`: `0 + 2 + 4 + 6`. At `t = 8` (even, and `8 > 6`)
the `break` fires, so nothing further is added.

*Marks: 2 / 2*

### Question 9  (2 pts)

```c
int c = 2, out = 0;
switch (c) {
    case 1: out += 1;
    case 2: out += 10;
    case 3: out += 100; break;
    default: out += 1000;
}
```

**`out = 110`** — **fall-through.** Execution enters at `case 2` (`out += 10` → 10) and runs on into
`case 3` (`out += 100` → 110) until the `break`. Without `break`s, arms cannot be skipped.

*Marks: 2 / 2*

### Question 10  (2 pts)

**From `unsigned f = 0;`, set bit 2, set bit 0, then clear bit 2:**

```
set bit 2:   f |= 1u << 2;
set bit 0:   f |= 1u << 0;
clear bit 2: f &= ~(1u << 2);
final f = 1
```

Step by step: `f = 0b100` (4) → `f = 0b101` (5) → `f = 0b001` (**1**). (`1u` keeps the shift unsigned;
using `~` on the mask clears exactly one bit.)

*Marks: 2 / 2*

---

## Grading Summary

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-10-13 |

**Feedback:**
Full marks. All five multiple-choice answers are correct with sound reasoning — `&&` over `||`,
`+` over `<<`, `i = i++` as the UB case, post-increment semantics, and `&&` short-circuiting the
division by zero. The short answers are all right: every bit-manipulation value is correct
(10, 95, 165, 5), the `do-while` runs once, the loop total is `12` with the `t = 8` break explained,
the `switch` fall-through gives `110`, and the bit set/clear sequence ends at `f = 1` using `1u`.

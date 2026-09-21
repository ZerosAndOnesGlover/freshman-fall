# PROG 101 · Quiz 2
## Week 3, Tuesday — In-Class Assessment

**Date:** Tuesday 13 October 2026 · 10:00–10:10 (start of Week 3, Lecture 1)
**Covers:** Week 2 material — operators, bit manipulation, evaluation order and undefined behaviour, control flow
**Duration:** 10 minutes · Closed book · 20 points

> Rewritten 2026-09-21. The previous version tested functions, the call stack, arrays and strings
> (Weeks 3–4) at the start of Week 3's first lecture — before any of them had been taught.

---

## Section A — Multiple Choice (2 pts each)

**1.** With `int a = 5, b = 3;`, what is `a > 3 && b > 3 || a == 5`?

- (A) 0
- (B) 1
- (C) 5
- (D) It depends on evaluation order

---

**2.** What is the value of `1 << 3 + 1`?

- (A) 9
- (B) 16
- (C) 8
- (D) 2

---

**3.** Which of these is **undefined behaviour**?

- (A) `unsigned u = 0; u = u - 1;`
- (B) `int i = 5; i = i++;`
- (C) `int r = 7 % -2;`
- (D) `int x = (1 > 0) ? 10 : 20;`

---

**4.** After `int i = 3; int j = i++ * 2;`, what are `i` and `j`?

- (A) `i = 3, j = 6`
- (B) `i = 4, j = 8`
- (C) `i = 4, j = 6`
- (D) `i = 3, j = 8`

---

**5.** With `int k = 0;`, the expression `(k != 0) && (10 / k > 1)`:

- (A) crashes with a division by zero
- (B) evaluates to `0` without dividing
- (C) is undefined behaviour
- (D) evaluates to `1`

---

## Section B — Short Answer (2 pts each)

**6.** With `unsigned x = 0x5A;` (binary `0101 1010`), give each value in decimal:

```
x & 0x0F = ______    x | 0x0F = ______    x ^ 0xFF = ______    x >> 4 = ______
```

---

**7.** What does this print? How many times does the body run, and why?

```c
int n = 0;
do { n++; } while (n < 0);
printf("%d\n", n);
```

```
Output: ______   Why: __________________________________________________
```

---

**8.** What is `total` after this loop?

```c
int total = 0;
for (int t = 0; t < 10; t++) {
    if (t % 2) continue;
    if (t > 6) break;
    total += t;
}
```

```
total = ______
```

---

**9.** What is `out`? Name the behaviour that produces it.

```c
int c = 2, out = 0;
switch (c) {
    case 1: out += 1;
    case 2: out += 10;
    case 3: out += 100; break;
    default: out += 1000;
}
```

```
out = ______   Behaviour: _____________________
```

---

**10.** Starting from `unsigned f = 0;`, write one expression each to **set** bit 2, **set** bit 0, then
**clear** bit 2. What is `f` at the end?

```
set bit 2:   ________________________
set bit 0:   ________________________
clear bit 2: ________________________
final f = ______
```

---

## Answer Key (Instructor Copy)

All values checked by compiling and running the snippets (gcc 13.3).

**1. (B) 1** — `&&` binds tighter than `||`: `(5 > 3 && 3 > 3) || 5 == 5` = `0 || 1`.

**2. (B) 16** — `+` binds tighter than `<<`: `1 << 4`. (GCC `-Wall` warns: `-Wparentheses`.)

**3. (B)** — two unsequenced modifications of `i` (`-Wsequence-point`). (A) is defined unsigned wrap, (C) is
`1`, (D) is `10`.

**4. (C) `i = 4, j = 6`** — post-increment yields the old value (3) and then increments.

**5. (B)** — `&&` short-circuits: the left side is false, so the division never happens.

**6.** `10`, `95`, `165`, `5`.

**7.** `1` — a `do-while` tests *after* the body, so the body runs once even though `n < 0` is false.

**8.** `12` — even `t` only: `0 + 2 + 4 + 6`; at `t = 8` the `break` fires.

**9.** `110` — **fall-through**: execution enters at `case 2` and runs on into `case 3` until the `break`.

**10.** `f |= 1u << 2;` `f |= 1u << 0;` `f &= ~(1u << 2);` → **`f = 1`**. Accept `1 << n` for `n < 31`, but
`1u` is the habit Lecture 1 teaches.

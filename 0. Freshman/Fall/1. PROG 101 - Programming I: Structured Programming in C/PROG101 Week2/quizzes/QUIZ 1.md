# PROG 101 · Quiz 1
## Week 2, Tuesday — In-Class Assessment

**Date:** Tuesday 6 October 2026 · 10:00–10:10 (start of Week 2, Lecture 1)
**Covers:** Week 1 material
**Duration:** 10 minutes
**Closed book, closed notes**
**Points:** 20 (2 pts each)

---

## Section A — Multiple Choice (2 pts each)

**1.** On a 64-bit Linux system, what does `sizeof(long)` return?

- (A) 4
- (B) 8
- (C) 16
- (D) It depends on the value stored

---

**2.** What is the decimal value of the 8-bit two's complement pattern `11111110`?

- (A) 254
- (B) -1
- (C) -2
- (D) 126

---

**3.** What does the following print?

```c
unsigned int x = 0;
x = x - 1;
printf("%u\n", x);
```

- (A) -1
- (B) 0
- (C) 4294967295
- (D) Undefined behavior — could be anything

---

**4.** Which of the following is **undefined behavior** in C?

- (A) `unsigned int x = UINT_MAX; x = x + 1;`
- (B) `int x = INT_MAX; x = x + 1;`
- (C) `unsigned int x = 0; x = x - 1;`
- (D) Both A and C

---

**5.** What do `(int)3.9` and `(int)-3.9` evaluate to?

- (A) `4` and `-4`
- (B) `3` and `-4`
- (C) `3` and `-3`
- (D) `4` and `-3`

---

## Section B — Short Answer (2 pts each)

**6.** What does each print?

```c
printf("%d %d\n", -7 / 2, -7 % 2);
```

Output: `______`   Rule for the sign of `%`: `_________________________________________`

---

**7.** What does this print, and why?

```c
int a = -1;
unsigned int b = 1;
printf("%d\n", a < b);
```

Output: `______`   Why: `______________________________________________________`

---

**8.** `0.1 + 0.2 == 0.3` evaluates to `0`. Give the reason in one sentence, and write the comparison you
should use instead.

```
Reason: ___________________________________________________________________
Instead: __________________________________________________________________
```

---

**9.** Give each value, and say which conversion the C standard defines exactly and which is
implementation-defined.

```
(unsigned char)300  = ______
(signed char)200    = ______   (on gcc, x86-64)
Defined exactly: __________   Implementation-defined: __________
```

---

**10.** What does the following print, and why?

```c
int a = 5, b = 3;
printf("%d\n", a / b);
printf("%f\n", (double)a / b);
printf("%d\n", a % b);
```

```
Line 1: _______  Reason: _______________________________________________
Line 2: _______  Reason: _______________________________________________
Line 3: _______  Reason: _______________________________________________
```

---

## Answer Key (Instructor Copy — Do Not Distribute)

**1. (B) 8** — On 64-bit Linux (LP64 model), `long` is 8 bytes. On Windows 64-bit (LLP64), it would be 4. On 32-bit systems, 4. The question specifies 64-bit Linux.

**2. (C) -2** — `11111110` in two's complement: MSB weight is -128. Sum: -128 + 64 + 32 + 16 + 8 + 4 + 2 + 0 = -2. Or: flip bits → `00000001`, add 1 → `00000010` = 2, so original is -2.

**3. (C) 4294967295** — Unsigned arithmetic wraps. `0 - 1` for `unsigned int` wraps to `UINT_MAX = 2^32 - 1 = 4294967295`. This is well-defined behavior (modular arithmetic) for unsigned types — not UB.

**4. (B) `int x = INT_MAX; x = x + 1;`** — Signed integer overflow is undefined behavior. Unsigned overflow (A and C) is defined as modular arithmetic. Note: A says UINT_MAX++, which wraps to 0 — defined. C says unsigned 0--, which wraps to UINT_MAX — defined.

**5. (C) `3` and `-3`** — conversion from floating to integer truncates toward zero.

**6.** `-3 -1`. Division truncates toward zero, so `%` takes the sign of the dividend: `(-3)*2 + (-1) == -7`.

**7.** `0`. The signed `-1` is converted to `unsigned` (4294967295) before the comparison, which is not less than 1.

**8.** Neither 0.1 nor 0.2 has an exact binary representation, so the rounded sum differs from the double
nearest 0.3. Use a tolerance: `fabs((0.1 + 0.2) - 0.3) < 1e-9`.

**9.** `44` (300 − 256) and `-56`. Conversion **to an unsigned** type is defined (reduce modulo 256);
conversion of an out-of-range value **to a signed** type is implementation-defined.

**10.**
- Line 1: `1` — Integer division: 5/3 = 1 (truncates toward zero).
- Line 2: `1.666667` — `(double)a` promotes `a` to double before division, giving floating-point result 1.6666...
- Line 3: `2` — Remainder: 5 = 3×1 + 2, so 5 % 3 = 2.

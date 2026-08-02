# PROG 101 — Quiz 1
## Week 2, Tuesday — In-Class Assessment

**Administered:** start of Week 2, Lecture 1 (Tuesday)
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

- (A) `unsigned int x = UINT_MAX; x++;`
- (B) `int x = INT_MAX; x++;`
- (C) `unsigned int x = 0; x--;`
- (D) Both A and C

---

**5.** What does `(x & (x - 1))` compute when `x` is a power of 2?

- (A) x doubled
- (B) x halved
- (C) 0
- (D) x - 1

---

## Section B — Short Answer (2 pts each)

**6.** Write a single C expression (no loops, no if) that tests whether bit 5 of an `unsigned int x` is set. The expression should evaluate to 1 if the bit is set, 0 if not.

```c
int result = __________________________________;
```

---

**7.** What is the output of this program? Trace it step by step.

```c
int x = 10;
int result = 0;
while (x > 0) {
    result += x % 2;
    x /= 2;
}
printf("%d\n", result);
```

Output: `______`

What does this loop compute? (one sentence): `_________________________________________________`

---

**8.** Explain what **short-circuit evaluation** means for the `&&` operator. Write one example where it prevents a runtime error:

```
Short-circuit: ___________________________________________________________

Example: _________________________________________________________________
```

---

**9.** What is the difference between these two loop conditions, given `int arr[5]`?

```c
for (int i = 0; i < 5; i++)   /* Loop A */
for (int i = 0; i <= 5; i++)  /* Loop B */
```

```
Loop A: ___________________________________________________________________

Loop B: ___________________________________________________________________

Which is correct for iterating over arr? Why? ______________________________
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

**4. (B) `int x = INT_MAX; x++;`** — Signed integer overflow is undefined behavior. Unsigned overflow (A and C) is defined as modular arithmetic. Note: A says UINT_MAX++, which wraps to 0 — defined. C says unsigned 0--, which wraps to UINT_MAX — defined.

**5. (C) 0** — A power of 2 has exactly one bit set. Subtracting 1 clears that bit and sets all lower bits. AND-ing them together gives 0. Example: x=8=1000b, x-1=7=0111b, 1000 & 0111 = 0000 = 0. This is the classic power-of-2 test.

**6.** `int result = (x >> 5) & 1;` — Right-shift bit 5 into position 0, mask with 1. Alternative: `!!(x & (1u << 5))` — but the `!!` is needed to guarantee 0 or 1 (not just non-zero).

**7.** Output: `2`. The loop extracts the binary digits of x from LSB to MSB and sums them. `10` in binary is `1010` — two 1-bits. So `result = 2`. This is the **popcount** (count of set bits) algorithm, also called Hamming weight.

**8.** Short-circuit: `&&` stops evaluating (skips the right operand) as soon as the left operand is false, since the result must be false regardless. Example: `if (ptr != NULL && *ptr > 0)` — if `ptr` is NULL, `*ptr` is never evaluated, preventing a null pointer dereference crash.

**9.** Loop A (`i < 5`): iterates with i = 0, 1, 2, 3, 4 — exactly the valid indices of `arr[5]`. Loop B (`i <= 5`): iterates with i = 0, 1, 2, 3, 4, **5** — index 5 is out of bounds for a 5-element array (valid indices are 0-4). Loop A is correct. Loop B causes undefined behavior on the last iteration (out-of-bounds access).

**10.**
- Line 1: `1` — Integer division: 5/3 = 1 (truncates toward zero).
- Line 2: `1.666667` — `(double)a` promotes `a` to double before division, giving floating-point result 1.6666...
- Line 3: `2` — Remainder: 5 = 3×1 + 2, so 5 % 3 = 2.

# CS 201 · Problem Set 1 — Solutions
## Instructor Only

---

> **Not for distribution.** All code below was compiled with `gcc -O2 -Wall -Wextra` and run on the
> lab image; every number is measured. Marking notes in blockquotes.

---

## Q1 (22) — Two's Complement and Undefined Behaviour

### (a) [4] — 1 each

| | bits | value |
|---|---|---:|
| Most positive | `01111111` | $+127$ |
| Most negative | `10000000` | $-128$ |
| $-1$ | `11111111` | $-1$ |
| Negate most negative | `10000000` | **$-128$** |

**The anomaly is the last.** $-(-128) = -128$. The range is asymmetric because there is exactly one zero, so of the 256 patterns, one is spent on 0 and the remaining 255 split 127/128 in favour of negatives. Negating $-128$ has no representable answer, so invert-and-add-one returns the input.

### (b) [6] — 3 each

**`always_true`.** Signed overflow is **undefined behaviour**. A program exhibiting UB has no defined meaning at all, so the compiler may assume it never occurs. Under that assumption `x + 1 > x` holds for every `x` the program is allowed to have, so the expression is a constant. GCC emits `mov eax,0x1; ret`. The function **cannot return 0**, even for `INT_MAX`.

**`uns`.** Unsigned arithmetic is **defined** to be modulo $2^{32}$. `UINT_MAX + 1 == 0`, and `0 > UINT_MAX` is genuinely false, so the expression is *not* constant — it is false for exactly one input. GCC must therefore test: `cmp edi,0xffffffff; setne al`.

> Full marks require the words "may assume it never happens" or equivalent. An answer that says only
> "signed overflow is undefined so anything can happen" has not explained the *specific* code
> generated, which is the question. 3 of 6.

### (c) [4]

**`always_true(INT_MAX)` returns 1** — not because the value wrapped to `INT_MIN` and the comparison then somehow succeeded, but because **the comparison is not in the binary.** The colleague's model predicts the addition happens and wraps; the disassembly shows no addition at all. Wraparound is not the risk. **Code deletion is.**

> Accept any refutation grounded in (b)'s disassembly. Reject appeals to exotic hardware — that is the
> weaker argument and concedes the colleague's framing.

### (d) [4]

```c
size_t total;
if (n < 0 || __builtin_add_overflow((size_t)n, (size_t)1, &total)) return -1;
char *buf = malloc(total);
if (!buf) return -1;
if (len < (size_t)n) memcpy(buf, src, len);
```

**Prevents:** `n == INT_MAX` making `n + 1` overflow. Because that overflow is UB, a compiler may delete a later check written to catch it, leaving an undersized allocation followed by a large `memcpy` — a heap overflow. Accept any version that computes the size in an unsigned type with a checked add, and rejects negative `n`.

> Award 2 of 4 for a version that only casts to `size_t` without checking `n < 0`: a negative `n`
> becomes enormous, which fails the allocation rather than corrupting the heap — safer, but by luck.

### (e) [4]

**Conversion:** in `i < n` with `int i` and `size_t n`, the usual arithmetic conversions promote `i` to `size_t`. A negative `i` becomes a huge positive value.

**Wrong:** `i = -1`, `n = 1`. Mathematically $-1 < 1$ is true; the comparison converts `-1` to `SIZE_MAX` and yields **false**.

**Fine:** `i = 3`, `n = 10`. Both non-negative, conversion is value-preserving, result is true.

---

## Q2 (24) — Dissecting Floats by Hand

### (a) [6] — 2 each

| | binary | hex | $s$ | $e$ | unbiased | mantissa |
|---|---|---|---|---|---|---|
| `1.5f` | `0 01111111 10000000000000000000000` | `0x3fc00000` | 0 | 127 | $0$ | `0x400000` |
| `-0.75f` | `1 01111110 10000000000000000000000` | `0xbf400000` | 1 | 126 | $-1$ | `0x400000` |
| `40.0f` | `0 10000100 01000000000000000000000` | `0x42200000` | 0 | 132 | $+5$ | `0x200000` |

*(All verified.)* Working: $1.5 = 1.1_2 \times 2^0$; $0.75 = 1.1_2 \times 2^{-1}$; $40 = 101000_2 = 1.01_2 \times 2^5$.

> `40.0f` is the discriminating one — it needs the normalisation step. Students who get 1.5 and 0.75
> and miss 40 have the formula but not the procedure.

### (b) [4]

**Negation in IEEE 754 is flipping the sign bit** — one XOR with `0x80000000`. Nothing else changes. Two's complement negation is invert-and-add-one, which touches every bit and can carry.

**Observable consequences** — any one earns the marks:

- **There are two zeros.** `0x00000000` and `0x80000000`, which compare equal but have different bits. `memcmp` on two structs holding $\pm 0$ reports them different while `==` reports them equal.
- **Negation never overflows**, unlike two's complement's $-(-128)$ anomaly. Every float has a representable negative.
- $1/(+0) = +\infty$ but $1/(-0) = -\infty$, so the sign of a zero is observable despite the equality.

### (c) [6] — 0.75 per cell

| $e$ | mantissa | meaning | why needed |
|---|---|---|---|
| 0 | 0 | **Zero**, signed | The implicit leading 1 makes zero otherwise unrepresentable |
| 0 | ≠ 0 | **Denormal**: $0.m \times 2^{-126}$, no implicit 1 | **Gradual underflow.** Without it, `a != b` could still give `a - b == 0`, so a guarded division still divides by zero |
| 255 | 0 | **±Infinity** | Overflow and $x/0$ need a result that keeps propagating meaningfully rather than trapping |
| 255 | ≠ 0 | **NaN** | $0/0$, $\sqrt{-1}$, $\infty - \infty$ have no value; NaN propagates so the error is visible at the end rather than silently plausible |

> The denormal justification is the one worth insisting on. "Represents very small numbers" is 0.25
> of the 0.75 — it does not say why the *gap* matters.

### (d) [4]

**[2]** `0x00000001` has a mantissa of `0x000001` and $e = 0$, so the value is $2^{-23} \times 2^{-126} = 2^{-149}$. **One bit of significance.**

**[2]** The next representable value is $2 \times$ larger, so the worst-case relative error is **100%** — the result could be off by a factor of two. A computation that lands here has lost essentially all precision; the value's magnitude is roughly right and its digits mean nothing. **Treat it as underflow, not as a number.**

### (e) [4]

**[2]** The exponent is **biased**, not two's complement, and it sits immediately below the sign bit and above the mantissa. So for two non-negative floats, comparing the 31 bits below the sign compares exponent first and then mantissa — lexicographic order on (exponent, mantissa) **is** numeric order, because a larger exponent always means a larger value and within one exponent the mantissa is monotonic.

**[2]** It fails for negatives because **the sign bit is the most significant bit**. Setting it makes the integer *more negative* as a signed value, which puts all negative floats below all positive ones — correct — but within the negatives, a larger magnitude means a larger unsigned pattern and therefore a *larger* signed value, so the order runs backwards.

---

## Q3 (20) — Bit-Level Manipulation

All verified with `-Wall -Wextra`, tested on $\{0, 1, -1, 5, -5, \texttt{INT\_MAX}, \texttt{INT\_MIN}\}$.

### (a) [4]

```c
int is_zero(int x) { return (~(x | -x)) >> 31 & 1; }
```

`x | -x` has its top bit set for every `x` except 0 — for any non-zero value, either `x` or `-x` is negative. Complement and extract the sign.

*Also accept* `!x`, only if the student argues that `!` is not a comparison operator. Most will not; either way, ask for a bit-level version.

### (b) [4]

```c
int sign(int x) { return (x >> 31) | (int)((unsigned)(-x) >> 31); }
```

`x >> 31` is $-1$ for negatives and 0 otherwise (arithmetic shift). `(unsigned)(-x) >> 31` is 1 when `x` is positive and 0 when `x` is 0 or negative. OR them.

### (c) [4]

```c
int abs_val(int x) { int m = x >> 31; return (x ^ m) - m; }
```

`m` is all-ones for negatives, all-zeros otherwise. For negatives this is $(\lnot x) + 1$; for non-negatives it is `x`.

**`INT_MIN`:** returns **`INT_MIN`**, i.e. still negative. *(Verified.)* **Unavoidable** — $|{\texttt{INT\_MIN}}|$ is $2^{31}$, which is not representable in a 32-bit `int`. This is Q1(a)'s anomaly again. Any implementation must either return a wrong value, widen the type, or signal an error.

> **Full marks require naming why it is unavoidable, not just reporting the value.** Students who say
> "it's a bug in my code" get 2 of 4 — the code is fine; the type is too small.

### (d) [4]

```c
int same_sign(int a, int b) { return ~((a ^ b) >> 31) & 1; }
```

`a ^ b` has its top bit set iff the signs differ. *(Verified: (3,4)→1, (3,−4)→0, (−3,−4)→1, (0,5)→1, (0,−5)→0.)*

Note zero counts as non-negative, so `same_sign(0,-5)` is 0. Accept either convention **if stated**.

### (e) [4]

```c
unsigned popcount(unsigned x) {
    x = x - ((x >> 1) & 0x55555555u);
    x = (x & 0x33333333u) + ((x >> 2) & 0x33333333u);
    x = (x + (x >> 4)) & 0x0f0f0f0fu;
    return (x * 0x01010101u) >> 24;
}
```

**Step 1** replaces each 2-bit field with the count of bits in that field. `x - ((x>>1) & 0x5555...)` works because for a 2-bit value $b_1b_0$, the count is $b_1 + b_0 = x - b_1$.

**Step 2** adds adjacent 2-bit counts into 4-bit fields, masking before *and* after to stop fields overflowing into each other.

*(Verified: popcount(0)=0, (1)=1, (−1)=32, (5)=2, (−5)=31, (INT_MAX)=31, (INT_MIN)=1.)*

> Accept a shift-and-mask chain without the final multiply. The multiply-by-`0x01010101` trick sums
> four bytes at once; a student who uses it should be able to say why.

---

## Q4 (16) — Float Ordering as Integers

### (a) [6]

```c
uint32_t total_order_key(float f) {
    uint32_t u; memcpy(&u, &f, sizeof u);
    return (u >> 31) ? ~u : (u | 0x80000000u);
}
```

**For negatives, flip every bit**; this reverses the within-negatives ordering *and* drops them below everything positive. **For non-negatives, set the top bit**, lifting them above all the flipped negatives while preserving their existing order.

### (b) [4]

*(Verified — keys monotonically increasing across the full list.)*

| value | key |
|---|---:|
| $-\infty$ | 8 388 607 |
| $-3.4\times10^{38}$ | 8 402 529 |
| $-2.0$ | 1 073 741 823 |
| $-1.5$ | 1 077 936 127 |
| $-1\times10^{-40}$ | 2 147 412 285 |
| $-0.0$ | 2 147 483 647 |
| $+0.0$ | 2 147 483 648 |
| $1\times10^{-40}$ | 2 147 555 010 |
| $1.0$ | 3 212 836 864 |
| $2.0$ | 3 221 225 472 |
| $3.4\times10^{38}$ | 4 286 564 766 |
| $+\infty$ | 4 286 578 688 |

The inverse, for (d): `(k >> 31) ? (k & 0x7fffffff) : ~k`, reinterpreted as a float. *(Verified — round-trips every value above, including both zeros and both infinities.)*

### (c) [3]

**Not a bug — a deliberate choice, and the student must defend one.**

Accept either, with reasoning:

- **Not a bug.** The function implements a *total order*, which `<` on floats is not (NaN is unordered with everything, and $\pm0$ are equal but distinguishable). IEEE 754-2008 specifies `totalOrder` with exactly this behaviour, placing $-0$ below $+0$.
- **Is a bug, for the stated contract.** The question asked for `key(a) < key(b)` iff `a < b`; since `-0.0 < 0.0` is false, the keys should be equal. Fixable by mapping $-0$ to $+0$ first.

> Award on the argument. A student who notices the tension at all has understood the question; one
> who says "no, floats are weird" has not.

### (d) [3]

**[2]** Radix sort needs keys with a monotone integer representation. Transform each float to its key, radix-sort the keys (four passes over 8 bits, or two over 16), then transform back — the inverse is `(k >> 31) ? (k & 0x7fffffff) : ~k`.

**[1]** **Cost:** one pass to encode, one to decode, and extra memory for the key array — but it buys $O(n)$ instead of $O(n \log n)$, and integer comparisons in place of floating-point ones.

---

## Q5 (18) — Summation Order

### (a) [4]

| Method | Result | Error |
|---|---|---:|
| `double`, backward | 16.695311366 | — |
| `float`, forward | 15.403682709 | $-1.292$ |
| `float`, backward | 16.686031342 | $-9.280\times10^{-3}$ |
| `float`, Kahan | 16.695310593 | $-7.732\times10^{-7}$ |

*(Verified.)* Accept small variation; the **orders of magnitude** of the errors are what is marked.

### (b) [5]

**[2] Measured:** **7 902 849 of 10 000 000 terms — 79.0% — leave the accumulator unchanged.** First absorbed index: **$i = 2\,097\,152$**.

**[3] Derived.** The accumulator is near 16, i.e. in the binade $[16, 32)$ with exponent $2^4$. The spacing of floats there is

$$16 \times 2^{-24} = 9.5367 \times 10^{-7}$$

Round-to-nearest leaves the accumulator unchanged once the addend is **at most half** a spacing:

$$\frac{1}{i} \le \frac{9.5367\times10^{-7}}{2} = 4.7684\times10^{-7} \;\Longrightarrow\; i \ge 2\,097\,152 = 2^{21}$$

**Derived and measured agree exactly**, and $1/2^{21} = 4.76837\times10^{-7}$ is precisely half the spacing. *(Verified.)*

> This is the question that separates the class. Full marks need the **binade**, the **ULP**, and the
> **factor of two from round-to-nearest**. Dropping the factor of two gives $2^{22}$ and is worth 3 of 5.

### (c) [4]

**[2] Why backward wins:** the small terms are added while the accumulator is still small, so they are within its representable resolution and accumulate among themselves. By the time the large terms arrive, the accumulated tail is big enough not to be absorbed. Forward order throws the tail away one term at a time.

**[2] Where it fails:** backward summation is not a general rule — **ascending magnitude** is what helps, and the harmonic series happens to be descending, so reversing it sorts it. For a sequence already ascending — $1, 2, 3, \ldots, n$ — reversing makes it *worse*. For alternating or randomly ordered magnitudes, reversal does nothing systematic.

> The marked insight: *reversal is not the technique; ordering by increasing magnitude is.* A student
> who says "always sum backwards" gets 2 of 4.

### (d) [5]

**[2] Measured:** with `-ffast-math`, the Kahan result becomes **15.403682709, error $-1.292$** — **bit-identical to the naive forward sum.** *(Verified.)* The compensation is gone entirely.

**[2] The assumption:** `-ffast-math` permits treating floating-point addition as **associative**. Under real-number algebra, `c = (t - s) - y` where `t = s + y` simplifies to $(s + y - s) - y = 0$. With `c` provably zero, `y = 1.0f/i - c` is just `1.0f/i`, the compensation is dead code, and it is eliminated.

**[1] Consequence:** a project with `-ffast-math` in its global flags **silently disables every compensated-summation algorithm it contains**, with no warning and no diagnostic. The code still compiles, still runs, and returns worse answers. Numerical routines must be compiled without it, or the compensation must be hidden behind `volatile` or a separate translation unit.

---

## Mark Summary

| | |
|---|---:|
| Q1 | 22 |
| Q2 | 24 |
| Q3 | 20 |
| Q4 | 16 |
| Q5 | 18 |
| **Total** | **100** |

**Where the class loses marks, in order:**

1. **Q5(b)** — omitting the factor of two from round-to-nearest, giving $2^{22}$.
2. **Q1(b)** — describing UB in general instead of explaining the two code generations.
3. **Q2(a)** — `40.0f`, because it needs an actual normalisation step.
4. **Q3(c)** — calling the `INT_MIN` result a bug in their code rather than a property of the type.
5. **Q5(c)** — concluding "always sum backwards".

Items 1 and 5 are worth five minutes at the start of Week 2; the rest can go on the forum.

---

*CS 201 · Week 1 · PS 1 Solutions · Instructor Only*

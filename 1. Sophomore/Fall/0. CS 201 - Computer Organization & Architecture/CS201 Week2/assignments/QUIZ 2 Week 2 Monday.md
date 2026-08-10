# CS 201 · Quiz 2
## Administered: Monday, Week 2 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 1** — integers and undefined behaviour, IEEE 754, and non-associativity.

**Instructions:** Closed notes. 10 minutes.

> **Unmarked, no weight.** The key is printed below. Sit it closed-book, then mark it yourself before
> you leave. Reading the key first costs you the only thing this is for.

---

**Q1.** In 8-bit two's complement, what is $-(-128)$, and why?

&nbsp;

&nbsp;

---

**Q2.** `int f(int x) { return x + 1 > x; }` compiles at `-O2` to `mov eax,0x1; ret`. The same function with `unsigned x` compiles to a real comparison. Explain the difference in one sentence.

&nbsp;

&nbsp;

---

**Q3.** Give the value of `(int)strlen("") - 1` when `strlen` returns `size_t` and the expression is used as a loop bound.

&nbsp;

&nbsp;

---

**Q4.** A `float` has 23 stored mantissa bits. How many bits of precision does it have, and why the discrepancy?

&nbsp;

&nbsp;

---

**Q5.** What do the exponent values $e = 0$ and $e = 255$ encode?

&nbsp;

&nbsp;

---

**Q6.** `(a+b)+c` gives 1.0 and `a+(b+c)` gives 0.0 for $a = 10^{16}$, $b = -10^{16}$, $c = 1$. Which addition destroyed the information?

&nbsp;

&nbsp;

---

**Q7.** Why does `-ffast-math` break Kahan summation?

&nbsp;

&nbsp;

---

<div style="page-break-after: always;"></div>

---

## Answer Key — Mark Your Own

**Q1.** **$-128$.** Invert-and-add-one on `10000000` gives `01111111 + 1 = 10000000` — the input. There is one zero, so the range is asymmetric ($-128$ to $+127$) and $+128$ has no representation.

---

**Q2.** **Signed overflow is undefined, so the compiler may assume it never happens** — making `x + 1 > x` always true, hence a constant. **Unsigned overflow is defined to wrap**, so `UINT_MAX + 1 == 0` and the comparison is genuinely false for one input, which must be tested.

*The key phrase is "may assume it never happens". "Anything can happen" is not the same claim and does not explain the code.*

---

**Q3.** **`SIZE_MAX`** — about $1.8 \times 10^{19}$, not $-1$.

`strlen("")` is `0`, an unsigned `size_t`. `0 - 1` in unsigned arithmetic wraps to the maximum. A loop bounded by it runs essentially forever, reading far past the buffer.

---

**Q4.** **24 bits.** The leading 1 of a normalised binary number is **implicit** — every normalised value starts with 1, so storing it would waste a bit. 23 stored + 1 implied = 24, or about 7.2 decimal digits.

---

**Q5.** Both are **escapes**, not values.

- **$e = 0$:** mantissa 0 → **zero** (signed, so there are two); mantissa ≠ 0 → **denormal**, with no implicit leading 1, giving gradual underflow.
- **$e = 255$:** mantissa 0 → **±infinity**; mantissa ≠ 0 → **NaN**.

---

**Q6.** **The inner one, $b + c$.**

$-10^{16} + 1$ needs $-9999999999999999$, which is not representable — near $10^{16}$ a `double`'s spacing is 2 — so it rounds back to $-10^{16}$. The 1 was absorbed **before `a` was ever involved**. Then $a + (-10^{16}) = 0$.

*Left grouping loses nothing: $a+b$ is exactly 0, and $0+1$ is exactly 1.*

---

**Q7.** **It permits treating floating-point addition as associative.**

Under that assumption, `c = (t - s) - y` with `t = s + y` is provably $(s+y-s)-y = 0$. With `c` always zero the compensation is dead code and gets eliminated — leaving the naive sum. *(Measured: the `-ffast-math` Kahan result is bit-identical to the naive forward sum.)*

---

### What to Do With Your Score

| If you missed | Reread |
|---|---|
| Q1 | L04 §1–2 |
| Q2, Q3 | L04 §3 and §6 — **the two that recur most** |
| Q4, Q5 | L05 §1 and §3 |
| Q6, Q7 | L06 §2 and §3 |

**Q2 is the one to be sure of.** Week 9's integer-overflow attacks are that question with a stack underneath, and it will be on Midterm 1.

---

*CS 201 · Week 2 · Quiz 2 · covers Week 1 · ungraded*

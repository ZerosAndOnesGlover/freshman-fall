# CS 201 · Computer Organization & Architecture
## Week 1 · Lecture 2 of 3
### IEEE 754 — Anatomy of a Float

*“The purpose of computing is insight, not numbers.”* — Richard Hamming, *Numerical Methods for Scientists and Engineers* (1962), Preface

---

**Reading:** CS:APP §2.4 · **Previous:** L04, integers and undefined behaviour

**Coursework:** 📝 **PS 1** released today, due Fri of Week 2 17:00 · 📊 **Quiz 2** Mon of Week 2 · 🔬 **Lab 1** Tue of Week 2 15:00–16:50

---

## 1. The Formula

A 32-bit IEEE 754 `float` is three fields in one word:

```
 31 30      23 22                    0
┌──┬──────────┬───────────────────────┐
│s │ exponent │       mantissa        │
└──┴──────────┴───────────────────────┘
 1      8                23
```

For a **normal** number:

$$v = (-1)^s \times 1.\text{mantissa}_2 \times 2^{\,e - 127}$$

Three design decisions are packed into that, and each is worth understanding rather than memorising.

**The leading 1 is implicit.** Every normalised binary number starts with a 1 — that is what normalised means. Storing it would waste a bit, so it is assumed. **23 stored bits therefore give 24 bits of precision**, which is about $24 \log_{10} 2 \approx 7.2$ decimal digits.

**The exponent is biased, not two's complement.** The stored 8-bit field $e$ means $e - 127$. Bias, rather than two's complement, so that **the bit pattern of a float compares in the same order as the bit pattern read as an integer** — for non-negative values. Verified:

| float | as `int32` |
|---|---:|
| 0.0 | 0 |
| 1e-40 | 71 362 |
| 1.0 | 1 065 353 216 |
| 1.5 | 1 069 547 520 |
| 2.0 | 1 073 741 824 |
| 3.4e38 | 2 139 081 118 |
| +inf | 2 139 095 040 |

*(Verified — monotonically increasing.)* This is not a curiosity: it means hardware can compare floats with integer comparators, and it is why sorting float keys as integers works. **For negatives the order reverses**, because the sign bit is the top bit — so the trick needs a fix-up, which PS 1 asks you to derive.

**The sign is a separate bit**, not part of the value. Hence two zeros.

---

## 2. Reading Real Bit Patterns

```
label                  value          hex         s   e        m
0.1f                   0.100000001    0x3dcccccd  0  123 (-4)  0x4ccccd
1.0f                   1              0x3f800000  0  127 (+0)  0x000000
2.0f                   2              0x40000000  0  128 (+1)  0x000000
-2.0f                  -2             0xc0000000  1  128 (+1)  0x000000
0.0f                   0              0x00000000  0    0       0x000000
-0.0f                  -0             0x80000000  1    0       0x000000
+inf                   inf            0x7f800000  0  255       0x000000
NaN                    nan            0x7fc00000  0  255       0x400000
FLT_MIN                1.17549435e-38 0x00800000  0    1 (-126) 0x000000
FLT_MIN/2              5.87747175e-39 0x00400000  0    0       0x400000
FLT_TRUE_MIN           1.40129846e-45 0x00000001  0    0       0x000001
```

*(All verified — printed by a C program that `memcpy`s the float into an `unsigned`.)*

**Check `1.0f` by hand.** $s = 0$, $e = 127 \Rightarrow 127 - 127 = 0$, mantissa all zero $\Rightarrow 1.0_2$. So $1.0 \times 2^0 = 1$. ✓

**Check `2.0f`.** Same mantissa, $e = 128 \Rightarrow 2^1$. So $1.0 \times 2 = 2$. ✓ Note that `-2.0f` differs from `2.0f` **in exactly one bit**.

---

## 3. The Two Reserved Exponents

$e = 0$ and $e = 255$ are not values. They are escapes.

| $e$ | mantissa | Meaning |
|---|---|---|
| 0 | 0 | **Zero** (signed — there are two) |
| 0 | ≠ 0 | **Denormal**: $0.\text{mantissa} \times 2^{-126}$, *no* implicit leading 1 |
| 1–254 | any | **Normal**: $1.\text{mantissa} \times 2^{e-127}$ |
| 255 | 0 | **±Infinity** |
| 255 | ≠ 0 | **NaN** |

**Denormals exist to make subtraction safe.** Without them, the gap between 0 and the smallest normal ($1.18 \times 10^{-38}$) would be far larger than the gap between consecutive normals near that size. So `a - b` could be non-zero mathematically yet flush to zero — meaning `if (a != b) x = 1/(a-b);` could divide by zero. **Denormals fill that gap**, at the cost of losing precision gradually rather than all at once. This is called *gradual underflow*, and it is what `FLT_TRUE_MIN = 1.4e-45` is: the smallest denormal, with just one bit of significance left.

**NaN is not equal to itself.** Verified:

```
n == n  : false
n != n  : true
0.0/0.0 : -nan       1.0/0.0 : inf
-0.0 == 0.0 : true
```

That `n != n` is the *only* portable NaN test in C without `<math.h>`. And note the last line: **the two zeros compare equal** even though their bit patterns differ. Equality on floats is not equality on bits, in both directions.

---

## 4. Why 0.1 Is Not 0.1

$0.1_{10}$ has no finite binary representation, for exactly the reason $\tfrac13$ has no finite decimal one:

$$0.1_{10} = 0.0\overline{0011}_2$$

The pattern `0011` repeats forever. *(Verified — the first 28 bits are `0001100110011001100110011001`.)*

So `0.1f` stores the nearest representable value:

$$\texttt{0.1f} = 0.100000001490116119384765625 \quad\text{(exactly)}$$

and as a `double`:

$$\texttt{0.1} = 0.1000000000000000055511151231257827021181583404541015625$$

*(Both verified — printed exactly with Python's `decimal`.)*

Hence the most famous line in computing:

```
0.1+0.2 = 0.30000000000000004441
0.3     = 0.29999999999999998890
equal?    no
```

*(Verified.)* **Two different wrong answers, and they differ.** `0.1 + 0.2` rounds up; the literal `0.3` rounds down. Neither is 0.3, and they are not each other.

> **This is not a bug and it is not fixable.** Any finite binary representation has this property. The
> question is never "how do I make floats exact" but "which representation matches my problem" —
> which is the same trade ECE 110 made with BCD, and for the same reason: a till and a ledger need
> exact decimal fractions, so they must not use binary floating point.

---

## 5. 24 Bits, and Where They Run Out

24 bits of precision means consecutive representable floats near $2^{24}$ are 1 apart, and beyond it, 2 apart:

```
2^24     = 16777216.0
2^24 + 1 = 16777216.0    <- unchanged
2^24 + 2 = 16777218.0
```

*(Verified.)* **Adding 1 to 16 777 216 in `float` does nothing.** The result is not representable, so it rounds back to where it started.

**This is the mechanism behind every "my counter stopped counting" bug.** A `float` accumulator incremented by 1 stops at $2^{24} \approx 1.7\times10^7$. A `double` has 53 bits and stops at $2^{53} \approx 9\times10^{15}$, which is why the same bug in `double` takes years to show up rather than seconds — and is correspondingly harder to find.

---

## 6. Denormals Are Slow — Measured

Denormals are handled by a slower path on most hardware, sometimes by microcode or a trap. **How much slower is a question with an answer**, so here it is on the lab machine:

```c
for (long i = 0; i < N; i++) s += A[i] * 1.0000001f;
```

with `A` filled first with values near 1.0, then with denormals:

| Array contents | Time (2 M elements) |
|---|---:|
| Normal floats | **0.0035 s** |
| Denormals | **0.1188 s** |
| | **~34× slower** |

*(Measured, `gcc -O2 -fno-tree-vectorize`, median of three: ratios 34.15, 33.70, 30.63.)*

> **A first attempt at this benchmark measured no difference at all**, because the test values decayed
> out of the denormal range within a few iterations and spent the rest of the loop as zeros — which
> are fast. The lesson is worth as much as the number: **a benchmark that measures nothing is
> usually measuring the wrong thing**, not proving the effect is absent. Week 11 is largely this.

Audio and physics code that decays toward silence or rest can drift into denormal range and slow down by an order of magnitude for no visible reason. The industry fix is a CPU mode that flushes denormals to zero (`-ffast-math` enables it, among many other things) — trading gradual underflow for speed.

---

## 7. What to Take Away

1. **$(-1)^s \times 1.m \times 2^{e-127}$**, with the leading 1 implicit — 23 stored bits, 24 bits of precision, ~7 decimal digits.
2. **The exponent is biased so that floats sort like integers**, for non-negatives.
3. **$e=0$ and $e=255$ are escapes**: zero, denormals, infinity, NaN.
4. **NaN ≠ NaN**, and `-0.0 == 0.0`. Neither follows from the bits.
5. **0.1 is not representable.** `0.1 + 0.2 != 0.3` is arithmetic working correctly.
6. **`float` stops counting at $2^{24}$.**
7. **Denormals cost ~34× on this machine.** Measured, not assumed.

---

## Exercises

1. Give the bit pattern of `1.5f` by hand, then check with a program. What is $e$, and what is the mantissa?
2. `-2.0f` is `0xc0000000` and `2.0f` is `0x40000000`. Which bit differs, and what does that tell you about negation in floating point compared with two's complement negation?
3. The float-as-int ordering trick works for non-negatives but reverses for negatives. Devise a transformation on the 32-bit pattern that makes *all* floats, including negatives, sort correctly as signed integers.
4. `FLT_TRUE_MIN` is `0x00000001`. How many bits of precision does it have? What does that mean for the relative error of a computation that produces it?
5. §6 reports a benchmark that initially measured nothing. Name one other way that benchmark could have silently measured the wrong thing, given what Week 0's Lab showed about `-O2`.

---

*Next: L06 — why the order you add numbers in changes the answer.*

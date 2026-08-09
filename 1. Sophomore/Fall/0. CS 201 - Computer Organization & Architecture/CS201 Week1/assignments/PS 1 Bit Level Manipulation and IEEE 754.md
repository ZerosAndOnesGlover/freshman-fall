# CS 201 · Problem Set 1
## Bit-Level Manipulation and IEEE 754 Dissection

---

**Released:** Week 1, Wednesday · **Due:** Week 2, Friday 17:00
**Total: 100 points** · Submit one PDF plus a `.zip` of source, `PS1_{LastName}_{StudentID}.pdf`

> Collaboration: discussing approaches is fine. The write-up and the code must be yours. State at the
> top: *"I worked on this problem set independently"* or name who you discussed which question with.
>
> **Q1 and Q2 are by hand.** Check with a program afterwards — you should — but show the working.
> **Q3–Q5 want code**, compiled with `-Wall -Wextra`, plus the output you measured.

---

### Q1: Two's Complement and Undefined Behaviour (22 points)

**(a) [4]** For 8-bit two's complement, give the bit pattern and decimal value of: the most positive value, the most negative value, $-1$, and the result of negating the most negative value. Say which of these four is the anomaly and why it exists.

**(b) [6]** These two functions differ only in the type of `x`:

```c
int      always_true(int x)      { return x + 1 > x; }
unsigned uns(unsigned x)         { return x + 1 > x; }
```

At `-O2`, GCC compiles the first to `mov eax,0x1; ret` and the second to a real comparison against `0xffffffff`.

Explain **both** code generations. Your answer must say what the standard permits in each case, not merely what the hardware does.

**(c) [4]** A colleague argues: *"Signed overflow wraps on every machine anyone uses, so undefined behaviour is a formality."* Using (b), give the shortest concrete refutation you can.

**(d) [4]** Rewrite this so it is correct for every `int` value of `n`:

```c
char *buf = malloc(n + 1);
if (len < n) memcpy(buf, src, len);
```

State which specific failure your version prevents.

**(e) [4]** For `int i` and `size_t n`, the comparison `i < n` compiles with a warning under `-Wsign-compare`. Give one pair of values for which it returns the mathematically wrong answer, and one pair for which it is fine. Show the conversion that happens.

---

### Q2: Dissecting Floats by Hand (24 points)

Single-precision IEEE 754: 1 sign bit, 8 exponent bits with bias 127, 23 stored mantissa bits.

**(a) [6]** Give the full 32-bit pattern, in binary and hex, for `1.5f`, `-0.75f` and `40.0f`. Show $s$, the stored exponent $e$, the unbiased exponent, and the mantissa for each.

**(b) [4]** These were printed by a program that `memcpy`s a float into an `unsigned`:

| value | hex |
|---|---|
| `2.0f` | `0x40000000` |
| `-2.0f` | `0xc0000000` |
| `0.0f` | `0x00000000` |
| `-0.0f` | `0x80000000` |

Negation in two's complement is invert-and-add-one. What is negation in IEEE 754? Give one consequence of the difference that a programmer can observe.

**(c) [6]** Complete this table of the reserved encodings, and give a concrete reason each escape exists:

| $e$ | mantissa | meaning | why it is needed |
|---|---|---|---|
| 0 | 0 | | |
| 0 | ≠ 0 | | |
| 255 | 0 | | |
| 255 | ≠ 0 | | |

**(d) [4]** `FLT_TRUE_MIN` is `0x00000001`, which is $1.401 \times 10^{-45}$. How many bits of significance does it carry? What is the worst-case relative error of a value at that magnitude, and what does that imply about trusting a computation that produces one?

**(e) [4]** Explain, in terms of the bit layout, why floats compare in the same order as their bit patterns read as **signed integers** — and why this holds only for non-negative values.

---

### Q3: Bit-Level Manipulation in C (20 points)

Write each of these **without** loops, without `if`, without comparison operators, and without casting to a wider type. You may use `& | ^ ~ << >> + -` and integer literals. Assume 32-bit `int` and arithmetic right shift.

Compile with `-Wall -Wextra` and include your test output.

**(a) [4]** `int is_zero(int x)` — returns 1 if `x` is 0, else 0.

**(b) [4]** `int sign(int x)` — returns $-1$, 0 or $+1$.

**(c) [4]** `int abs_val(int x)` — absolute value. State what your version does for `INT_MIN`, and why that is unavoidable.

**(d) [4]** `int same_sign(int a, int b)` — 1 if `a` and `b` have the same sign, else 0.

**(e) [4]** `unsigned popcount(unsigned x)` — count the set bits. The no-loop rule applies; use the divide-and-conquer bit trick. Explain the first two steps of your version in one sentence each.

---

### Q4: Float Ordering as Integers (16 points)

L05 showed that non-negative floats sort correctly when their bit patterns are read as signed 32-bit integers, but negatives reverse.

**(a) [6]** Write `uint32_t total_order_key(float f)` returning a key such that `key(a) < key(b)` **iff** `a < b`, for all finite floats including negatives and both zeros. Explain the transform in two sentences.

**(b) [4]** Test it on at least: $-\infty$, $-3.4\times10^{38}$, $-2.0$, $-1.5$, $-0$, $+0$, $1\times10^{-40}$, $1.0$, $2.0$, $3.4\times10^{38}$, $+\infty$. Show that the keys increase monotonically.

**(c) [3]** Your transform maps $-0$ and $+0$ to different keys, but `-0.0 == 0.0` is true in C. Is that a bug in your function? Argue a position.

**(d) [3]** Radix sort works on integers, not floats. Explain how (a) lets you radix-sort an array of floats, and what it costs.

---

### Q5: Summation Order (18 points)

Reproduce and extend the Lab 1 measurement. Sum $\sum_{i=1}^{10^7} 1/i$ in `float`, forward and backward, and with Kahan compensation, against a `double` reference.

**(a) [4]** Report your four values and the error of each. They should be close to the lab's: forward $-1.29$, backward $-9.3\times10^{-3}$, Kahan $-7.7\times10^{-7}$.

**(b) [5]** Instrument the forward loop to count terms that leave the accumulator **unchanged**, and report the first index at which that happens.

Then **derive** that index from theory: the spacing of floats near the accumulator's value, and the rounding rule. Your derived value and your measured value should agree exactly. Show both.

**(c) [4]** Backward summation is ~139× more accurate here for no extra work. Explain why in one or two sentences — then give a sequence for which backward summation is **not** better, and say what property of the harmonic series made it work.

**(d) [5]** Rebuild with `-ffast-math` and report what happens to the Kahan result. Explain precisely which algebraic assumption the compiler made and why that assumption destroys the algorithm.

State the consequence for a project whose makefile sets `-ffast-math` globally.

---

## Marks

| | |
|---|---:|
| Q1 Two's Complement and UB | 22 |
| Q2 Dissecting Floats by Hand | 24 |
| Q3 Bit-Level Manipulation | 20 |
| Q4 Float Ordering as Integers | 16 |
| Q5 Summation Order | 18 |
| **Total** | **100** |

---

*CS 201 · Week 1 · Problem Set 1*

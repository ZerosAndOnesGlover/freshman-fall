# CS 201 · Computer Organization & Architecture
## Week 1 · Lecture 3 of 3
### Why Floating-Point Addition Is Not Associative

---

**Reading:** CS:APP §2.4.4–2.4.6 · **Previous:** L05, the anatomy of a float

---

## 1. The Claim, Demonstrated

```c
double a = 1e16, b = -1e16, c = 1.0;

(a + b) + c   ->  1.0
a + (b + c)   ->  0.0
```

*(Verified.)* **Same three numbers, same operator, two different answers.**

Addition on the reals is associative. Addition on `double` is not. This is not an implementation flaw — IEEE 754 addition is *correctly rounded*, meaning each individual operation returns the nearest representable value to the exact mathematical result. **Each step is as right as it can be, and the composition is still wrong.**

---

## 2. Why

Every floating-point operation does this:

1. Compute the exact mathematical result.
2. Round it to the nearest representable value.

Step 2 is where information leaves.

**Left grouping.** $a + b = 10^{16} - 10^{16} = 0$, exactly — no rounding needed. Then $0 + 1 = 1$, also exact. Result: **1.0**.

**Right grouping.** $b + c = -10^{16} + 1$. The exact answer is $-9999999999999999$. A `double` has 53 bits of mantissa, so near $10^{16}$ the spacing between representable values is 2. **$-9999999999999999$ is not representable**, and it rounds to $-10^{16}$. Then $a + (-10^{16}) = 0$. Result: **0.0**.

**The 1 was absorbed.** It was too small relative to $10^{16}$ to change it, so adding it did nothing, and the information that it ever existed is gone.

> **The general rule.** Adding a small number to a much larger one loses the small number entirely,
> once the ratio exceeds the available precision. For `float` that ratio is about $2^{24}$; for
> `double`, about $2^{53}$.

---

## 3. Absorption at Scale — Measured

The abstract version is easy to shrug off. Here is the same effect ruining a real computation.

Sum $\sum_{i=1}^{10^7} 1/i$ four ways:

| Method | Result | Error |
|---|---|---:|
| `double`, backward *(reference)* | 16.695311366 | — |
| `float`, forward (largest first) | 15.403682709 | **−1.29** |
| `float`, backward (smallest first) | 16.686031342 | −9.3 × 10⁻³ |
| `float`, Kahan summation | 16.695310593 | −7.7 × 10⁻⁷ |

*(All verified, `gcc -O2`.)*

**The forward `float` sum is 7.7% wrong.** Not in the last digit — in the first two.

**Why.** Running forward, the accumulator reaches about 16 early. The terms keep shrinking. Once $1/i$ falls below **half** the spacing of representable floats near 16, round-to-nearest returns the accumulator unchanged and **every remaining term adds exactly nothing.**

The spacing near 16 is $16 \times 2^{-24} = 9.537 \times 10^{-7}$, so absorption begins when

$$\frac{1}{i} < \frac{9.537 \times 10^{-7}}{2} = 4.768 \times 10^{-7} \;\Longrightarrow\; i > 2\,097\,152 = 2^{21}$$

**Measured: the first absorbed term is $i = 2\,097\,152$ exactly**, where $1/i$ equals half the spacing to the bit — and **7 902 849 of the 10 000 000 terms, 79.0%, change the accumulator by nothing at all.** *(Verified.)* Four fifths of the work is discarded as it is computed.

**Running backward fixes most of it** at zero cost, because the small terms accumulate among themselves while the sum is still small enough to represent them. **139× better, for reversing a loop.**

**Kahan summation** carries a running compensation term for what was lost at each step:

```c
float s = 0, c = 0;
for (long i = 1; i <= N; i++) {
    float y = 1.0f/i - c;     /* apply last step's lost part   */
    float t = s + y;          /* this addition loses something */
    c = (t - s) - y;          /* recover exactly what it lost  */
    s = t;
}
```

**1.7 million times better than the naive forward sum**, at the cost of three extra flops per element. `(t - s) - y` looks like it should be zero, and would be in exact arithmetic — it is precisely the rounding error, recovered.

> Compilers with `-ffast-math` **delete Kahan summation**, because under real-number algebra `c` is
> always 0. If you write compensated arithmetic, you must not let the compiler assume the algebra it
> is compensating for.

---

## 4. What This Breaks

**Parallel reduction is not deterministic.** Summing an array across 8 threads and combining partial sums groups the additions differently from a serial loop — so you get a different answer. Run it again with a different thread schedule and you may get a third. **This is why a parallel program can be "correct" and still not reproducible**, and it is a genuine problem in scientific computing, where a rerun is expected to reproduce a published figure. Week 10 revisits it.

**The compiler cannot reorder your sums.** `a + b + c` may not be rearranged to `a + c + b`, because that changes the result — so the loop cannot be vectorised without permission. That permission is `-ffast-math` (or `-fassociative-math`), and it is why that flag speeds up numerical code so dramatically and why it must never be enabled thoughtlessly.

**`==` on floats is almost always wrong.** Not because floats are "imprecise", but because two computations of the same mathematical quantity by different routes give different bit patterns. Compare with a tolerance, and choose the tolerance deliberately:

```c
fabs(x - y) < eps                        /* absolute — fine near 0, useless at 1e16 */
fabs(x - y) <= eps * fmax(fabs(x),fabs(y))  /* relative — usually what you want */
```

---

## 5. Catastrophic Cancellation

The other failure direction. Subtracting two nearly equal numbers **destroys the leading digits that agreed**, and promotes whatever rounding noise was hiding below.

If $x$ and $y$ agree to 7 digits and each carries error in the 8th, then $x - y$ is *exactly* representable — but its leading digits are the errors. **The subtraction is not what went wrong; it exposed error that was already there.**

The standard case is the quadratic formula. When $b^2 \gg 4ac$, one root computes as $\dfrac{-b + \sqrt{b^2-4ac}}{2a}$ where $\sqrt{b^2-4ac} \approx |b|$ — a subtraction of near-equals. The fix is algebraic, not numerical: compute the well-conditioned root first, then get the other from $x_1 x_2 = c/a$.

**The general lesson: reformulate rather than reach for more precision.** `double` moves the problem 29 bits further away; it does not remove it.

---

## 6. When Floats Are the Wrong Tool

| Use | Instead of |
|---|---|
| Money | Integer cents, or a decimal type |
| Counters, IDs, indices | Integers |
| Exact comparison | Tolerance, or exact arithmetic |
| Accumulating many small values | Kahan, pairwise summation, or a wider type |

**Money is the one that matters commercially.** $0.10 cannot be represented, so a million transactions of \$0.10 do not total \$100 000.00. Every financial system stores integer minor units or uses a decimal type. This is the same conclusion ECE 110 reached about BCD, arrived at from the other end.

---

## 7. What to Take Away

1. **Each operation is correctly rounded; the composition is not associative.** `(a+b)+c` and `a+(b+c)` gave 1.0 and 0.0.
2. **Absorption**: adding small to large loses the small entirely past $2^{24}$ (`float`) or $2^{53}$ (`double`).
3. **Order matters, measurably.** Forward `float` summation was 7.7% wrong; reversing the loop was 139× better; Kahan, 1.7 million× better.
4. **Cancellation exposes error rather than creating it.** Reformulate.
5. **Non-associativity blocks vectorisation and makes parallel reductions non-reproducible.**
6. **Never use floats for money.**

---

## Exercises

1. Find `float` values $a, b, c$ where `(a+b)+c` and `a+(b+c)` differ, using numbers smaller than 100. Explain which addition absorbed what.
2. The forward sum lost its terms once $1/i$ fell below the spacing near 16. Estimate the $i$ at which that happens, and check it against the measured 7.7% error.
3. In the Kahan loop, `c = (t - s) - y` is zero under real arithmetic. Trace one iteration with concrete numbers and show what it actually computes.
4. `-ffast-math` deletes Kahan summation. Name two *other* things that flag permits which could change a program's output, and say why each is normally forbidden.
5. Your parallel sum over 8 threads disagrees with the serial version in the 9th digit. A colleague calls it a race condition. Explain why it is not, and how you would demonstrate that.

---

*Next week: x86-64 assembly — the instruction set, properly.*

# MATH 142 · Calculus II
## Lab 01 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures below were produced by running the lab.

> **Parts A and D must use exact rational arithmetic.** A student who computes $I_n$ in floating point
> will get the right numbers and miss the entire point of A2 — that the parity of $n$ decides whether
> $\pi$ appears. **Check for `Fraction` in their code before marking Part A.**

---

## Part A — The Recursion (25 pts)

### A1 (12) — implementation and the exact table

```python
from fractions import Fraction

def I(n):
    """Return (coeff, has_pi) with  I_n = coeff * (pi if has_pi else 1)."""
    if n == 0: return (Fraction(1, 2), True)
    if n == 1: return (Fraction(1), False)
    c, hp = I(n - 2)
    return (c * Fraction(n - 1, n), hp)
```

| $n$ | exact $I_n$ | numeric |
|---:|---|---|
| 0 | $\tfrac12\pi$ | 1.57079632679 |
| 1 | $1$ | 1.0 |
| 2 | $\tfrac14\pi$ | 0.785398163397 |
| 3 | $\tfrac23$ | 0.666666666667 |
| 4 | $\tfrac3{16}\pi$ | 0.589048622548 |
| 5 | $\tfrac8{15}$ | 0.533333333333 |
| 6 | $\tfrac5{32}\pi$ | 0.490873852123 |
| 7 | $\tfrac{16}{35}$ | 0.457142857143 |
| 8 | $\tfrac{35}{256}\pi$ | 0.429514620608 |

*Marking: 12 for a correct recursion reproducing the table. **Deduct 4 for float arithmetic** even if the numbers are right — the exactness is the point, and A2 becomes unanswerable without it. Deduct 3 for a missing or wrong base case.*

*Note $I_n$ is strictly decreasing, which Part D relies on.*

### A2 (7) — why the parity decides

The recursion reduces $n$ by 2 at each step, so **it never changes the parity of $n$.** An even $n$ therefore terminates at $I_0 = \tfrac\pi2$ and an odd $n$ at $I_1 = 1$.

$\pi$ enters the computation **only through the base case $I_0$**, and only even $n$ ever reaches it. The multiplied factors $\frac{n-1}{n}$ are all rational and cannot introduce or remove a $\pi$.

*Marking: 7. **Full marks require identifying that the recursion preserves parity** and that $\pi$ lives only in $I_0$. "Because the table alternates" earns 2 — that is the observation, not the reason.*

### A3 (6) — the call count

`I(n)` recurses down by 2 to a base case, so the number of calls is

$$\left\lfloor \frac n2\right\rfloor + 1 \quad\text{calls, i.e. } \Theta(n)$$

*(For $n=8$: calls at 8, 6, 4, 2, 0 — five calls.)*

It is a **linear recurrence with a constant decrement** — $T(n) = T(n-2) + O(1)$ — which solves to $\Theta(n)$.

*Marking: 3 for the exact count, 3 for $\Theta(n)$ with justification. **Accept $n/2$ within rounding.** A student who names it as a decrement-by-constant recurrence and cites CS 101 should be commended.*

---

## Part B — The Wallis Product (25 pts)

### B1 (10) and B2 (8) — the table

$\pi/2 = 1.5707963267948966$

| $n$ | $W_n$ | error | ratio | $n\cdot$error |
|---:|---|---|---:|---|
| 1 | 1.333333333333 | 2.3746e-01 | — | 0.23746 |
| 2 | 1.422222222222 | 1.4857e-01 | 1.598 | 0.29715 |
| 4 | 1.486077097506 | 8.4719e-02 | 1.754 | 0.33888 |
| 8 | 1.525294998028 | 4.5501e-02 | 1.862 | 0.36401 |
| 16 | 1.547179361643 | 2.3617e-02 | 1.927 | 0.37787 |
| 32 | 1.558760105320 | 1.2036e-02 | 1.962 | 0.38516 |
| 64 | 1.564719813590 | 6.0765e-03 | 1.981 | 0.38890 |
| 128 | 1.567743281368 | 3.0531e-03 | 1.990 | 0.39079 |
| 256 | 1.569266083046 | 1.5302e-03 | 1.995 | 0.39174 |
| 512 | 1.570030271664 | 7.6606e-04 | 1.998 | 0.39222 |
| 1024 | 1.570413065539 | 3.8326e-04 | 1.999 | 0.39246 |

*Marking B1: 10 for a correct table. B2: 8 for errors and ratios. **The ratios approach 2, not 4** — students who expected Lab 0's behaviour and "corrected" their code should be told their instinct was right and their conclusion wrong.*

### B3 (7) — the scaled error

The column $n\cdot|W_n - \pi/2|$ converges to approximately **0.3925**, and the constant is

$$\frac{\pi}{8} = 0.39269908\ldots$$

So the error satisfies $|W_n - \pi/2| \approx \dfrac{\pi}{8n}$.

*Marking: 4 for observing convergence to ~0.392, **3 for identifying it as $\pi/8$.** Accept $\pi/8$ or a decimal near 0.3927. A student who says only "it converges to a constant" earns 4 — the identification was requested.*

*The convergence of this column is itself slow: at $n=1024$ it reads 0.39246 against $\pi/8 = 0.39270$, still 0.06% out.*

---

## Part C — How Bad Is It? (25 pts)

### C1 (8)

The ratio tends to $2 = 2^1$, so $p = 1$: **first-order convergence**, error $\propto n^{-1}$.

**Doubling the work halves the error** — one extra correct digit costs roughly ten times the work.

*Marking: 4 for $p=1$, 4 for deriving it from the ratio (as in Lab 0, ratio $=2^p$).*

### C2 (9)

Using $|W_n - \pi/2| \approx \dfrac{\pi}{8n}$ and requiring error $< 5\times10^{-11}$:

$$n > \frac{\pi}{8\times 5\times10^{-11}} \approx \boxed{7.9\times10^{9}}$$

**About eight billion factors** for ten decimal places. This is not a practical way to compute $\pi$ — and worse, at that scale accumulated floating-point rounding would corrupt the answer well before the mathematics did.

*Marking: 6 for the estimate with working, 3 for the judgement. **Accept anything of order $10^{9}$–$10^{10}$.** A student who additionally raises floating-point accumulation deserves explicit credit — it is a genuine second obstacle and nobody was prompted to notice it.*

### C3 (8) — the contrast

| | Wallis product | Simpson (Lab 0) |
|---|---|---|
| Order | 1 | 4 |
| Error behaviour | $\propto n^{-1}$ | $\propto n^{-4}$ |
| Work for 10 digits | $\approx 8\times10^9$ | $128$ |

**Ratio of the work: about 62 million to one** ($7.9\times10^9 / 128 \approx 6.2\times10^7$).

**The property that matters is the order of convergence**, not the elegance of the formula. A method's order determines how the cost scales with the number of digits, and a first-order method is unusable for high precision no matter how beautiful it is.

*Marking: 5 for the table, 3 for the closing sentence. **The sentence must identify order/rate as the deciding property.** "Simpson is faster" earns 1 — true but not the lesson.*

---

## Part D — The Squeeze (15 pts)

### D1 (5)

On $[0,\pi/2]$ we have $0\le \sin x\le 1$, so multiplying by $\sin^n x \ge 0$ gives $\sin^{n+1}x\le\sin^n x$ pointwise. Integrating preserves the inequality (Week 0, comparison property), so $I_{n+1}\le I_n$ — the sequence is **decreasing**. Applying this twice:

$$I_{2n+1}\;\le\;I_{2n}\;\le\;I_{2n-1}$$

*Marking: 5. **The step that must appear is "integrate the pointwise inequality"** — citing the Week 0 comparison property. An assertion that "$I_n$ decreases because higher powers are smaller" without integrating earns 2.*

### D2 (6) — the identity

$$W_n = \frac\pi2\cdot\frac{I_{2n+1}}{I_{2n}}$$

| $n$ | $W_n$ | $\frac\pi2\cdot\frac{I_{2n+1}}{I_{2n}}$ |
|---|---|---|
| 1 | 1.3333333333333 | 1.3333333333333 |
| 2 | 1.4222222222222 | 1.4222222222222 |
| 4 | 1.4860770975057 | 1.4860770975057 |
| 8 | 1.5252949980278 | 1.5252949980278 |

**Agreement to all 14 digits shown.**

*Marking: 6 for the verification at all four values to the requested precision. Deduct 2 for fewer than 12 digits — the point is that this is an identity, not an approximation, and low precision hides that.*

### D3 (4) — the proof sketch

| $n$ | $I_{2n}/I_{2n+1}$ |
|---|---|
| 1 | 1.17810 |
| 2 | 1.10447 |
| 4 | 1.05701 |
| 8 | 1.02983 |

Dividing D1's inequality by $I_{2n+1}$:

$$1 \;\le\; \frac{I_{2n}}{I_{2n+1}} \;\le\; \frac{I_{2n-1}}{I_{2n+1}} = \frac{2n+1}{2n}$$

the last step by the recursion $I_{2n+1}=\frac{2n}{2n+1}I_{2n-1}$. Since $\frac{2n+1}{2n}\to1$, the **squeeze theorem** gives $\frac{I_{2n}}{I_{2n+1}}\to1$.

Combined with D2:

$$W_n = \frac\pi2\cdot\frac{I_{2n+1}}{I_{2n}} \longrightarrow \frac\pi2\cdot 1 = \frac\pi2 \qquad\blacksquare$$

*Marking: 4. **Full marks require the upper bound $\frac{2n+1}{2n}$ and the squeeze**, not merely the observation that the table approaches 1. Award 2 for the observation alone.*

*The convergence here is slow for exactly the reason Part C measured: the bound $\frac{2n+1}{2n} = 1+\frac{1}{2n}$ approaches 1 at rate $1/n$, and that rate propagates straight into $W_n$.*

---

## Part E — Reflection (10 pts)

**E1 (5).** They are the same mathematics in different representations. $I_n$ is a *finite* exact expression — a rational number times possibly $\pi$ — obtained from a recursion of $\Theta(n)$ exact steps. $W_n$ is the ratio $\frac{\pi}{2}\cdot\frac{I_{2n+1}}{I_{2n}}$ **with the $\pi$ divided out**, so it approximates $\pi/2$ only to the extent that $I_{2n+1}/I_{2n}$ approximates 1 — and that ratio converges slowly.

**The exact formula already contains $\pi$; the approximation is what remains once you refuse to write $\pi$ down.**

*Marking: 5. Accept any answer identifying that the exact form has $\pi$ built into the base case, and the product converges slowly because it is extracting $\pi$ from a slowly-converging ratio. Award 2 for a vague "they're related".*

**E2 (5).** Any two of:

- It is a **proof**, not just a computation — it establishes a nontrivial relationship between $\pi$ and the integers, which no amount of numerical evaluation could.
- It is the origin of **Stirling's formula**: the constant $\sqrt{2\pi}$ in $n!\sim\sqrt{2\pi n}(n/e)^n$ is derived from Wallis' product, and Stirling's formula is used constantly in algorithm analysis and probability.
- It is **historically decisive** — it showed that $\pi$ arises from purely rational operations taken to a limit, an idea that fed directly into the development of infinite series (Weeks 6–10).
- It is a clean, self-contained example of the **squeeze theorem** doing real work.

*Marking: 5, any two substantive points. **Answers of "it's beautiful" earn 1.** The question asked what it is good for, and there are concrete answers — the Stirling connection especially is worth telling the class about, since they will meet $\sqrt{2\pi n}$ in CS 102's analysis of sorting.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 25 |
| C | 25 |
| D | 15 |
| E | 10 |
| **Total** | **100** |

---

## Checkoff Checklist

1. **`Fraction` used in Part A** — not floats
2. Exact table reproduced for $n = 0..8$
3. A2 identifies **parity preservation**, not just the pattern
4. Wallis table with ratios approaching **2**
5. B3 identifies the constant as **$\pi/8$**
6. C2 gives an estimate of order $10^{9}$–$10^{10}$
7. C3's closing sentence names **order of convergence** as the deciding property
8. D2 verified to 12+ digits
9. D3 uses the **squeeze theorem** with the explicit upper bound

---

## Note for the Debrief

Two things to land, and the second is the one that lasts:

> **First:** you have just proved Wallis' product — a genuine theorem, found in 1656, thirty years
> before the calculus you used to prove it existed. It is exact and it is beautiful.
>
> **Second:** it is also useless. Ten decimal places would take eight billion factors. Last week
> Simpson's rule got ten decimal places from 128 evaluations. **The difference is not cleverness — it
> is order of convergence**, and it is a factor of sixty million.

Then set up Week 6:

> Every convergence question this term comes back to this. **How fast does the tail vanish?** In Week
> 6 we make that the definition of a limit, in Week 7 we build tests that answer it for infinite
> sums, and in Week 10 you will meet a series for $\pi$ that beats Wallis by a factor of billions —
> using exactly the machinery you have started here.

---

*MATH 142 · Week 1 · Lab 01 Solutions · Instructor Only*

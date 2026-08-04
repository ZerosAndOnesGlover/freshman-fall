# MATH 142 · Calculus II
## Lab 00 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All numbers below were produced by running the lab; they are reference values from one machine, in double precision.

> **Machine dependence.** Parts A–D are pure double-precision arithmetic and students should
> reproduce these figures to the digits shown. **The one place variation is legitimate is the last
> Simpson row** — at $n=256$ the error is $\sim10^{-12}$, close enough to double-precision rounding
> that summation order can move the final digit. If a student reports the Simpson ratio drifting
> *away* from 16 at the largest $n$, that is correct behaviour and worth praising, not an error.

---

## Reference Results

**Exact value:** $\displaystyle\int_0^1 e^{-x^2}dx = \frac{\sqrt\pi}{2}\operatorname{erf}(1) = 0.7468241328124270254\ldots$

### Absolute errors and consecutive ratios

| $n$ | trapezoid | ratio | midpoint | ratio | Simpson | ratio |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1.545e-02 | — | 7.774e-03 | — | 3.563e-04 | — |
| 4 | 3.840e-03 | 4.02 | 1.923e-03 | 4.04 | 3.125e-05 | **11.40** |
| 8 | 9.585e-04 | 4.01 | 4.794e-04 | 4.01 | 1.988e-06 | 15.72 |
| 16 | 2.395e-04 | 4.00 | 1.198e-04 | 4.00 | 1.246e-07 | 15.95 |
| 32 | 5.988e-05 | 4.00 | 2.994e-05 | 4.00 | 7.795e-09 | 15.99 |
| 64 | 1.497e-05 | 4.00 | 7.485e-06 | 4.00 | 4.872e-10 | 16.00 |
| 128 | 3.742e-06 | 4.00 | 1.871e-06 | 4.00 | 3.045e-11 | 16.00 |
| 256 | 9.356e-07 | 4.00 | 4.678e-07 | 4.00 | 1.904e-12 | 16.00 |

### Signed errors

| $n$ | $T_n - $ exact | $M_n - $ exact | ratio |
|---:|---:|---:|---:|
| 4 | −3.840035012e-03 | +1.922999079e-03 | −1.9969 |
| 16 | −2.395360242e-04 | +1.197797039e-04 | −1.9998 |
| 64 | −1.496917460e-05 | +7.484632981e-06 | −2.0000 |
| 256 | −9.355662745e-07 | +4.677833159e-07 | −2.0000 |

---

## Part A — Implementation (25 pts)

### A1 (8), A2 (8), A3 (9)

```python
def trap(f, a, b, n):
    h = (b-a)/n
    return h*((f(a)+f(b))/2 + sum(f(a+i*h) for i in range(1, n)))

def mid(f, a, b, n):
    h = (b-a)/n
    return h*sum(f(a+(i+0.5)*h) for i in range(n))

def simpson(f, a, b, n):            # n must be even
    h = (b-a)/n
    return h/3*(f(a)+f(b) + sum((4 if i % 2 else 2)*f(a+i*h) for i in range(1, n)))
```

*Marking A1/A2: 8 each for a correct rule. **The two classic errors:** halving both endpoints in the trapezoid rule instead of only the ends (deduct 3), and using `i` rather than `i+0.5` in the midpoint rule (deduct 4 — that is the trapezoid's left-endpoint sum, and their midpoint column will duplicate a left-Riemann sum).*

*Marking A3: 9. **The alternation is the marks.** `4 if i % 2 else 2` — a student who writes `2 if i % 2 else 4` gets a plausible-looking but wrong answer; their Simpson column will not show a ratio near 16, which they should have caught in Part B. Deduct 5, and note that Part C would have exposed it.*

### The verification table ($n=4$)

| $f$ | exact | trapezoid err | midpoint err | Simpson err |
|---|---:|---:|---:|---:|
| $x$ | 0.500000 | 0.000e+00 | 0.000e+00 | 0.000e+00 |
| $x^2$ | 0.333333 | 1.042e-02 | 5.208e-03 | 0.000e+00 |
| $x^3$ | 0.250000 | 1.562e-02 | 7.812e-03 | 0.000e+00 |
| $x^4$ | 0.200000 | 2.070e-02 | 1.030e-02 | 5.208e-04 |

**(a)** Every rule is exact on a linear function because each replaces $f$ on a subinterval by an interpolant — a chord (trapezoid), a constant through the midpoint (midpoint), a parabola (Simpson) — and **each of these reproduces a straight line exactly.** For the midpoint rule the errors on either side of the sample point cancel by symmetry.

**(b)** Simpson's rule fits a parabola, so exactness through degree 2 is expected. It is **also** exact on $x^3$ because the error term of the parabolic fit on a symmetric pair of subintervals is an *odd* function about the centre, and integrating an odd function over a symmetric interval gives zero — the cubic error cancels between the two halves.

**This "free" extra degree is why Simpson's order is 4 and not 3.** The first surviving term is the fourth derivative, giving error $O(h^4)$.

*Marking: 5 for the table, 2 for (a), 2 for (b). **(b) is the hard one** — accept any answer identifying that the cubic term cancels by symmetry. A student who only says "it happens to work" earns 1.*

---

## Part B — Measuring the Error (25 pts)

**B1 (15).** The table above. *Marking: 15 for a complete, correctly-computed table; deduct 2 per wrong rule column. Values should match to the digits shown.*

**B2 (10).** The ratio columns above.

*Marking: 10. **Deduct nothing for the blank first row** — there is no previous error at $n=2$. Deduct 4 if they computed $\frac{E(2n)}{E(n)}$ (giving 0.25 and 0.0625) without noticing the ratios are inverted; the conclusion in Part C is then stated backwards.*

---

## Part C — The Order (25 pts)

### C1 (9)

- **Trapezoid:** ratio $\to 4 = 2^2$, so $p=2$. **Order 2.**
- **Midpoint:** ratio $\to 4 = 2^2$, so $p=2$. **Order 2.**
- **Simpson:** ratio $\to 16 = 2^4$, so $p=4$. **Order 4.**

*Marking: 3 each. **Full credit requires the reasoning $2^p = \text{ratio}$, not just the number.** A student who wrote "order 2 because the textbook says so" earns 1 — the lab asked them to derive it from their data.*

### C2 (8) — the important one

At $n=4$, Simpson's measured ratio is **11.40**, not 16. It reaches 15.95 by $n=16$ and 16.00 by $n=64$.

The claim "$E \approx Ch^p$" is **asymptotic**: it says
$$\lim_{h\to0}\frac{E(h)}{h^p} = C$$
The true error is $Ch^4 + Dh^6 + \cdots$; at large $h$ the higher-order terms are not negligible and the observed ratio is contaminated by them. **Only as $h\to0$ does the leading term dominate and the ratio approach $2^4$.**

An asymptotic statement is a statement about a limit, and **a limit constrains no particular $n$.**

*Marking: 4 for identifying that the claim is asymptotic/about a limit, 4 for explaining why small $n$ deviates (higher-order terms not yet negligible).*

*Discussion point worth raising: this is exactly the same logical structure as big-$O$ in CS 102. "This algorithm is $O(n\log n)$" says nothing about $n=10$, and students who have been bitten by a "fast" algorithm losing to insertion sort on small inputs have met this before in another costume.*

### C3 (8)

**(a)** Extrapolating from $n=256$ with $E \propto n^{-p}$, to reach $|E| < 5\times10^{-11}$:

| Rule | error at $n=256$ | predicted $n$ |
|---|---:|---:|
| Trapezoid | 9.356e-07 | **≈ 35,000** |
| Midpoint | 4.678e-07 | **≈ 24,800** |
| Simpson | 1.904e-12 | **≈ 113** |

*Direct search confirms Simpson first meets the tolerance at $n=128$ (error 3.045e-11), consistent with the estimate of 113.*

**(b)** Roughly **270×** less work — about 35,000 evaluations against 128.

**(c)** Yes, in at least these circumstances (any one earns the mark):

- The integrand is **not smooth** — Simpson's $O(h^4)$ depends on $f^{(4)}$ existing and being bounded. With a kink or a discontinuous derivative, Simpson's advantage evaporates and it can be *worse*.
- The data are **samples at fixed points** and $n$ is odd, so Simpson does not apply directly.
- The data are **noisy**: fitting parabolas to noise amplifies it, and the crude rule is more robust.
- Only **low accuracy** is needed, where the simpler rule is easier to get right.

*Marking: 4 for (a) with visible working, 2 for (b), 2 for (c). **Accept any $n$ within a factor of 2 in (a)** — it is an extrapolation and the point is the method. **Deduct in (a) if they used $E\propto n^{-p}$ with the wrong $p$**, which usually traces back to a C1 error.*

---

## Part D — The Sign of the Error (15 pts)

### D1 (7)

From the signed table: **the trapezoid rule underestimates** (negative error) and **the midpoint rule overestimates** (positive error).

*Marking: 7. **The direction matters and is worth checking against their own numbers** — students who guess from the textbook rule without looking will often say the opposite. See the warning below.*

### D2 (8)

The ratio converges to **−2**: the trapezoid error is twice the midpoint error, with the opposite sign.

**Geometrically:** on a subinterval where $f$ is concave down, the chord lies *below* the curve, so the trapezoid underestimates; the midpoint tangent lies *above* the curve, so the midpoint rectangle overestimates. The two errors straddle the true value, which is why they have opposite signs — and the standard error constants ($\frac{1}{12}$ for the trapezoid, $\frac{1}{24}$ for the midpoint) give the factor of 2.

**This is the basis of Simpson's rule:** $S_{2n} = \frac{T_n + 2M_n}{3}$ is precisely the weighted combination that cancels the leading error term.

### The concavity warning

$$f(x)=e^{-x^2} \implies f''(x) = (4x^2-2)e^{-x^2}$$

which is zero at $x = \tfrac{1}{\sqrt2} \approx 0.7071$. So on $[0,1]$ the function is **concave down on $[0, 0.707)$ and concave up on $(0.707, 1]$** — the concavity is *not* constant, and the textbook rule "trapezoid overestimates when concave up" does not apply to the interval as a whole.

The observed sign is negative — the trapezoid underestimates — meaning the **concave-down portion dominates**. That portion is both wider (71% of the interval) and carries larger $|f''|$: $|f''(0)| = 2$ against $|f''(1)| = 2e^{-1} \approx 0.74$.

*Marking: 3 for the ratio −2, 3 for the geometric explanation, 2 for the concavity analysis. **Full marks on the last part require actually computing $f''$ and locating the inflection** — an assertion that "the concavity varies" without the number earns 1.*

> **Emphasise this in the debrief.** A rule stated under a hypothesis ("if $f$ is concave up…") tells
> you nothing when the hypothesis fails. The students who got this right are the ones who **looked at
> their own signed data first** and then went looking for the explanation; the ones who got it wrong
> quoted the rule and did not check. That distinction is the habit the entire course is trying to build.

---

## Part E — Reflection (10 pts)

**E1 (5).** Evaluating a definite integral and finding an antiderivative are **different problems**. The FTC links them when an antiderivative is available, but numerical methods bypass antiderivatives entirely — they approximate the *limit of Riemann sums* directly, which is what the integral was defined to be. So "unsolvable in closed form" does not mean "uncomputable"; here we got 10+ digits of a integral with no elementary antiderivative.

*Marking: 5. Accept any answer separating symbolic solution from numerical evaluation. **Deduct 2 for "the computer solved it"** — the computer did not solve it, it approximated it, and the distinction is the point.*

**E2 (5).** The midpoint rule is a Riemann sum with $x_i^*$ the midpoint. **Simpson's rule is not**: its terms carry weights $\tfrac{h}{3}$, $\tfrac{4h}{3}$, $\tfrac{2h}{3}$ — unequal, and $\tfrac{4h}{3}$ exceeds the subinterval width $h$, so no choice of $\Delta x$ makes it a sum of $f(x_i^*)\Delta x$ over a partition.

Simpson's rule is **not sampling the function — it is integrating an interpolant exactly.** It fits a parabola through three points and integrates that parabola in closed form.

*Marking: 5. The key observation is the unequal weights, one of them larger than the subinterval width. **Accept the alternative correct framing** that the trapezoid rule is also not literally a Riemann sum but is the average of the left and right ones — a student who raises that has understood the question better than it was asked, and should be told so.*

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

1. All three rules implemented and verified on $x^k$, $k=1..4$
2. Error table matches the reference to the digits shown
3. **Ratio column present** — this is the lab
4. Orders 2, 2, 4 derived *from their data*
5. **C2 answered in terms of a limit**, not a rule
6. Signed errors reported with the correct sign
7. **D2's concavity: $f''$ computed and the inflection at $1/\sqrt2$ located**

---

## Note for the Debrief

Close with the connection forward, because it motivates Week 10:

> You computed $\int_0^1 e^{-x^2}dx$ to ten decimal places today without ever finding an
> antiderivative — because none exists. You did it with 128 function evaluations.
>
> **In Week 10 you will compute the same integral to the same precision by adding 13 numbers**, from
> the series $\sum_{n\ge0}\frac{(-1)^n}{n!\,(2n+1)}$ — and the terms are simple enough to do several
> by hand. Same integral, same impossibility, a completely different way around it.

*(Verified: the 13-term partial sum is $0.746824132818$, an error of $5.6\times10^{-12}$; 12 terms
give $7.8\times10^{-11}$, just short of the tolerance. Quote the figure, not a rounder one — students
check.)*

---

*MATH 142 · Week 0 · Lab 00 Solutions · Instructor Only*

# MATH 141 · Week 8
## LAB 08 Solutions — INSTRUCTOR ONLY

**Total: 100 points.** Every figure below was produced by running the lab.

---

## Part 1 — Watching Riemann Sums Converge (25 pts)

**1a (3 pts).** The rectangles **overestimate**. $f(x)=x^2$ is increasing on $[0,1]$, so on each
subinterval the right endpoint is where $f$ is largest — every rectangle contains the region beneath
the curve and more.

*Award the full 3 only if the answer names monotonicity. "The rectangles stick out above" is the
observation, not the reason.*

**1b (2 pts).** The overshoot on each subinterval is a thin curved sliver whose height is
proportional to $\Delta x$; with $n$ of them, total error $\propto n\cdot\Delta x^2 = O(1/n)$. Visually
the staircase becomes indistinguishable from the curve by $n=50$.

**1c (6 pts).** $R_n = \dfrac{(n+1)(2n+1)}{6n^2}$, exact value $\tfrac13$:

| $n$ | $R_n$ | Error |
|-----|-------|-------|
| 4 | $0.4687500$ | $+0.1354167$ |
| 10 | $0.3850000$ | $+0.0516667$ |
| 50 | $0.3434000$ | $+0.0100667$ |
| 100 | $0.3383500$ | $+0.0050167$ |
| 1000 | $0.3338335$ | $+0.0005002$ |

*All errors positive, consistent with 1a.*

**1d (4 pts).** Doubling $n$ **halves** the error — verified: $n=10,20,40$ give
$5.17\times10^{-2}$, $2.54\times10^{-2}$, $1.26\times10^{-2}$.

That is **first-order convergence**, $O(1/n)$.

**Lab 3 connection:** the forward difference is $O(h)$ and the central difference $O(h^2)$, for the
same structural reason — a one-sided rule leaves an uncancelled first-order term, while a symmetric
rule cancels it. $L_n$ and $R_n$ are the one-sided rules here; $M_n$ is the symmetric one.

---

**1e (3 pts).** $L_n$ uses $x_{i-1}$ instead of $x_i$, i.e. $i$ runs $0..n-1$:

$$L_n=\frac{1}{n^3}\sum_{i=0}^{n-1}i^2=\frac{(n-1)(2n-1)}{6n^2}$$

*Equivalently $L_n = R_n - \tfrac1n$, since the two sums differ only by the $i=0$ and $i=n$ terms
($0$ and $1$, times $\Delta x$).*

**1f (4 pts).** With $\bar x_i=\dfrac{2i-1}{2n}$:

$$M_n=\sum_{i=1}^{n}\left(\frac{2i-1}{2n}\right)^2\frac1n=\frac{1}{4n^3}\sum_{i=1}^{n}(2i-1)^2=\frac{1}{4n^3}\cdot\frac{n(4n^2-1)}{3}=\frac{4n^2-1}{12n^2}$$

**1g (3 pts).**

| Method | Value | Error |
|--------|-------|-------|
| $L_{10}$ | $0.2850000$ | $-0.0483333$ |
| $R_{10}$ | $0.3850000$ | $+0.0516667$ |
| $M_{10}$ | $0.3325000$ | $-0.0008333$ |

$M_{10}$ is **62× more accurate** than $R_{10}$ at identical cost. Note also that $L_n$ and $R_n$
bracket the true value — a free error bound whenever $f$ is monotone.

---

## Part 2 — Sample-Point Independence (25 pts)

**2a (6 pts).** Reference implementation:

```python
import random

def riemann(f, a, b, n, rule):
    dx = (b - a) / n
    total = 0.0
    for i in range(n):
        if   rule == "left":   x = a + i * dx
        elif rule == "right":  x = a + (i + 1) * dx
        elif rule == "mid":    x = a + (i + 0.5) * dx
        elif rule == "random": x = a + (i + random.random()) * dx
        total += f(x) * dx
    return total
```

*The random rule must draw **inside each subinterval** — `a + (i + random.random())*dx`. A student
who draws uniformly from $[a,b]$ has written a Monte Carlo estimator instead, which converges at
$O(1/\sqrt n)$ and will not reproduce the table. Worth diagnosing rather than just marking wrong.*

**2b (6 pts).** $f(x)=x^2$ on $[0,1]$, exact $0.3333333333$:

| $n$ | $L_n$ | $R_n$ | $M_n$ | random (3 runs) | spread |
|---|---|---|---|---|---|
| $10$ | $0.2850000000$ | $0.3850000000$ | $0.3325000000$ | $0.3139$, $0.3350$, $0.3240$ | $2.10\times10^{-2}$ |
| $100$ | $0.3283500000$ | $0.3383500000$ | $0.3333250000$ | $0.33298$, $0.33377$, $0.33353$ | $7.87\times10^{-4}$ |
| $10^4$ | $0.3332833350$ | $0.3333833350$ | $0.3333333325$ | $0.33333353$, $0.33333296$, $0.33333318$ | $5.71\times10^{-7}$ |
| $10^6$ | $0.3333328333$ | $0.3333338333$ | $0.3333333333$ | $0.3333333334$, $0.3333333332$, $0.3333333333$ | $2.54\times10^{-10}$ |

*Student values for the random rule will differ — mark the **spread column and its trend**, not the
individual numbers.*

**2c (5 pts).** At $n=10$ the four rules disagree in the **first decimal place**
($0.285$ to $0.385$). At $n=10^6$ they agree to **six decimal places** ($0.333333$), and midpoint and
random agree to nine.

**2d (4 pts).** **Yes, it converges.** Every run gives a different value, but the *spread between
runs* collapses: $2.10\times10^{-2} \to 7.87\times10^{-4} \to 5.71\times10^{-7} \to 2.54\times10^{-10}$,
falling by roughly $10^{3}$ for each $10^2$ increase in $n$.

The sequence of random sums is not a fixed sequence of numbers at all — it is a different sequence
every time you run it — and yet **every** such sequence converges to the same limit.

**2e (4 pts).** The definition

$$\int_a^b f = \lim_{n\to\infty}\sum f(x_i^*)\Delta x, \qquad x_i^* \text{ arbitrary}$$

only names a number if all these limits coincide. If left sums went to $0.3$ and midpoint sums to
$0.35$, the notation $\int_0^1 x^2dx$ would be ambiguous and the theory would collapse.

The random rule is the sharp test: it is not one rule but infinitely many, sampled at random, and it
still lands on $\tfrac13$. **What the lab demonstrates is that the definition is well posed** — not
merely that Riemann sums are a good approximation.

*This is the conceptual centre of the lab. Award 4 only for an answer that reaches well-posedness;
"they all give the same answer so it works" earns 2.*

---

## Part 3 — Bounding an Integral You Cannot Evaluate (20 pts)

**3a (4 pts).** $g(x)=\dfrac{1}{1+x^3}$. On $[0,2]$, $x^3$ is strictly increasing, so $g$ is strictly
**decreasing**. Hence $M=g(0)=1$ and $m=g(2)=\tfrac19$.

$$\frac19(2)\le \int_0^2 g \le 1(2) \qquad\Longrightarrow\qquad \mathbf{0.2222 \le I \le 2.0000}$$

**3b (5 pts).** With $n=10^6$: $I \approx \mathbf{1.0900017}$.

It sits in the **upper half** of the bracket, and the bracket is a factor of 9 wide — nearly useless
as an estimate. Students should say so.

**3c (6 pts).** Comparison applied piecewise (using monotonicity on each piece):

| Pieces | Lower | Upper | Width |
|---|---|---|---|
| $1$ | $0.222222$ | $2.000000$ | $1.777778$ |
| $2$ | $0.611111$ | $1.500000$ | $0.888889$ |
| $4$ | $0.864286$ | $1.308730$ | $0.444444$ |
| $8$ | $0.978089$ | $1.200311$ | $0.222222$ |

**The width halves exactly each time.** (It must: for monotone $g$ the total width is
$\lvert g(2)-g(0)\rvert \cdot \Delta x$, and $\Delta x$ halves.)

**3d (5 pts).** The piecewise lower and upper bounds **are the lower and upper Riemann sums**, and
refining the partition is exactly taking $n\to\infty$.

So the comparison property is not a separate tool from the integral's definition — it is a single
crude application of it, and the definition is what you get by pushing it to the limit. The
squeeze between the two bounds is precisely the argument that makes $\int_a^b f$ well defined for
continuous $f$, which is what Part 2 observed empirically.

*Full marks require identifying them as upper/lower sums. "It's like a Riemann sum" earns 2.*

---

## Part 4 — Building a Numerical Integrator (25 pts)

**4a (4 pts).** $n=2$, $\Delta x=0.5$, midpoints $0.25$ and $0.75$:

$$M_2 = (0.0625 + 0.5625)(0.5) = \mathbf{0.3125}$$

Formula check: $M_2 = \dfrac{4(4)-1}{12(4)} = \dfrac{15}{48} = 0.3125$ ✓

**4b (5 pts).** $n=1000$ gives $\mathbf{1.7641628792}$ against the reference $1.7642$ — an error of
about $1\times10^{-7}$ relative to the accurate value $1.7641627815$.

**4c (6 pts).**

| $n$ | $M_n$ | Error |
|---|---|---|
| $10$ | $1.7650940179$ | $9.31\times10^{-4}$ |
| $10^2$ | $1.7641725453$ | $9.76\times10^{-6}$ |
| $10^3$ | $1.7641628792$ | $9.77\times10^{-8}$ |
| $10^4$ | $1.7641627825$ | $9.77\times10^{-10}$ |
| $10^5$ | $1.7641627815$ | $9.66\times10^{-12}$ |

Each $10\times$ in $n$ buys $100\times$ in accuracy — **$O(1/n^2)$ confirmed**, exactly as Part 1
predicted for the midpoint rule.

**The noise floor:** the improvement is already degrading at $n=10^5$ ($9.66$ rather than the
predicted $9.77\times10^{-12}$). Past roughly $n=10^6$, accumulated rounding in the summation
overtakes the truncation error and further refinement makes the answer *worse*. Double precision
holds about 16 significant digits, and summing $10^6$ terms spends several of them.

*Students who report monotone improvement all the way to $n=10^7$ have almost certainly used
`math.fsum` or NumPy's pairwise summation — legitimate, and worth a remark, but they should say so.*

**4d (5 pts).**

```
n ← 1
prev ← midpoint_rule(f, a, b, n)
loop:
    n ← 2n
    curr ← midpoint_rule(f, a, b, n)
    if |curr - prev| < epsilon: return curr
    prev ← curr
    if n > n_max: raise "failed to converge"
```

**If $\varepsilon$ is below the noise floor**, the difference $\lvert curr-prev\rvert$ stops shrinking
— it bottoms out at the rounding level and then wanders. The loop never satisfies its test and runs
until `n_max`, having long since passed the point of best accuracy. This is why the guard clause is
not optional, and why production integrators specify a tolerance floor near machine epsilon.

**4e (5 pts).** $e^{-x^2}$ has **no elementary antiderivative** — this is a theorem (Liouville), not
a gap in our technique. No amount of Week 9 or Week 10 method will produce a closed form.

So the two approaches are not competitors where one is a fallback for the lazy:

- **Exact methods** give a formula: valid for all limits at once, differentiable, exact, and the only
  route to a *symbolic* answer.
- **Numerical methods** give a number: available for **every** continuous integrand, including the
  ones with no formula, at a cost that buys accuracy predictably.

The FTC decides which integrals are in the first class. Everything else — the normal distribution's
CDF, Fresnel integrals, most of physics — lives permanently in the second.

*Award 5 for an answer that recognises the non-existence is a theorem. Students who write "we just
don't know the antiderivative yet" have the key point backwards — 2.*

---

## Marking Scheme Summary

| Section | Points | Watch for |
|---------|--------|-----------|
| Part 1 | 25 | 1d must identify $O(1/n)$, not just "smaller" |
| Part 2 | 25 | 2e must reach well-posedness |
| Part 3 | 20 | 3d must identify upper/lower sums |
| Part 4 | 25 | 4c must find the noise floor; 4e must know it is a theorem |
| Reflection | 5 | — |
| **Total** | **100** | |

---

*MATH 141 · Week 8 · Lab 08 Solutions · Instructor copy — do not distribute*

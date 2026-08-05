# MATH 142 · Calculus II
## Lab 06 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures produced by running the lab at 60-digit precision.

> **Check that students set `mp.mp.dps` high enough.** Part B's whole point is invisible in `float`:
> double precision runs out at 16 digits, i.e. at step 4 of 6. **A student reporting that the error
> "stops improving" has hit machine epsilon, not a mathematical limit** — that is a real and useful
> observation, and should be credited, but the table then needs rerunning at higher precision.

---

## Part A — The Babylonian Method (20 pts)

### A1 (6)

$$L = \frac12\left(L+\frac2L\right) \implies 2L^2 = L^2+2 \implies L^2=2 \implies L=\pm\sqrt2$$

From $a_0=1>0$ every term is positive, so the iteration approaches $\boxed{L=\sqrt2}$.

*Marking: 4 for the fixed points, 2 for selecting the positive one with a reason.*

### A2 (8)

$$g(x) = \frac12\left(x+\frac2x\right) \implies g'(x) = \frac12\left(1-\frac{2}{x^2}\right)$$

At $x=\sqrt2$: $\;g'(\sqrt2) = \frac12\left(1-\frac22\right) = \boxed{0}$

*Verified numerically: `mp.diff` gives $2.9\times10^{-62}$ at 60-digit precision — zero to working accuracy.*

**Prediction:** $g'(L)=0$ kills the linear error term, so $e_{n+1}\approx\frac12g''(L)e_n^2$ — **quadratic convergence.**

*Marking: 4 for $g'$, 2 for the value, 2 for the prediction.*

### A3 (6)

With $g'(L)=0$ the expansion $e_{n+1}=g(a_n)-g(L)$ has **no first-order term**, so the leading behaviour is second order in $e_n$. **The error is proportional to the square of the previous error**, which is the definition of quadratic convergence.

*Marking: 6. **The answer must reference the vanishing linear term**, not merely assert "it's fast".*

---

## Part B — Measuring Quadratic Convergence (25 pts)

### B1 (10), B2 (8), B3 (7)

$\sqrt2 = 1.41421356237309504880168872421\ldots$

| $n$ | $a_n$ | error $e_n$ | $e_n/e_{n-1}^2$ | correct digits |
|---:|---|---|---|---:|
| 0 | $1$ | $4.14214\times10^{-1}$ | — | 0 |
| 1 | $1.5$ | $8.57864\times10^{-2}$ | $0.5$ | 1 |
| 2 | $1.416666666666\ldots$ | $2.45310\times10^{-3}$ | $0.333333$ | 2 |
| 3 | $1.414215686274\ldots$ | $2.12390\times10^{-6}$ | $0.352941$ | 5 |
| 4 | $1.414213562374\ldots$ | $1.59486\times10^{-12}$ | $0.353553$ | 11 |
| 5 | $1.414213562373095048801689624$ | $8.99293\times10^{-25}$ | $0.353553$ | 24 |
| 6 | $1.414213562373095048801688724$ | $2.85928\times10^{-49}$ | $0.353553$ | **48** |

**B2 — the constant:** the ratio converges to $0.353553\ldots$, which is

$$\boxed{\frac{1}{2\sqrt2} = 0.3535533906\ldots}$$

*(Verified: the measured value agrees to $4\times10^{-7}$.)*

*This is $\frac{g''(L)}{2} = \frac{1}{L\cdot 2}\cdot\frac{1}{\ldots}$ — students need not derive it, but should recognise it as a simple expression in $\sqrt2$.*

**B3(a)** The digit count **doubles at every step**: $1,2,5,11,24,48$.

**B3(b)** From 48 digits at step 6, doubling gives $96,\ 192,\ 384,\ 768,\ 1536$ — so **11 steps** suffice for 1000 digits. *(Accept 10–12.)*

**B3(c)** Wallis needed $\sim8\times10^9$ factors for 10 digits; Babylonian needs **4 steps** for 11. **A ratio of about two billion to one**, and the gap widens without limit because one method is linear and the other doubles.

*Marking B1: 10 for the table. B2: 5 for the constant, 3 for identifying it as $\frac{1}{2\sqrt2}$. B3: 3 + 2 + 2.*

---

## Part C — Linear Convergence (20 pts)

### C1 (6)

$g(x) = x-\frac{x^2-2}{4}$. At $x=\sqrt2$: $g(\sqrt2) = \sqrt2 - 0 = \sqrt2$ ✓

$$g'(x) = 1-\frac{x}{2} \implies g'(\sqrt2) = 1-\frac{\sqrt2}{2} = \boxed{0.2928932188\ldots}$$

*Verified numerically.*

**$0<|g'|<1$, so the fixed point is attracting but the convergence is only linear.**

### C2 (8)

| $n$ | $a_n$ | error | $e_{n-1}/e_n$ |
|---:|---|---|---|
| 0 | $1$ | $4.14214\times10^{-1}$ | — |
| 1 | $1.25$ | $1.64214\times10^{-1}$ | $2.52241$ |
| 2 | $1.359375$ | $5.48386\times10^{-2}$ | $2.99449$ |
| 3 | $1.39739990234375$ | $1.68137\times10^{-2}$ | $3.26155$ |
| 4 | $1.4092182805761695$ | $4.99528\times10^{-3}$ | $3.36591$ |
| 5 | $1.4127442399986556$ | $1.46932\times10^{-3}$ | $3.39972$ |
| 6 | $1.4137826680863108$ | $4.30894\times10^{-4}$ | $3.40994$ |
| 7 | $1.4140873099409989$ | $1.26252\times10^{-4}$ | $3.41296$ |
| 8 | $1.4141765799069562$ | $3.69825\times10^{-5}$ | $3.41385$ |

**The ratio approaches $3.41421\ldots = 2+\sqrt2$**, and indeed

$$\frac{1}{|g'(\sqrt2)|} = \frac{1}{1-\frac{\sqrt2}{2}} = 2+\sqrt2 = 3.41421356\ldots \checkmark$$

*(Verified.)*

**Each step multiplies the error by about $0.293$ — a constant factor, gaining roughly half a decimal digit per step.**

### C3 (6)

**(a)** For 12 correct digits:

- **Babylonian:** error $1.6\times10^{-12}$ at step 4 — **4 steps.**
- **Linear:** gaining $\log_{10}(3.414)\approx0.53$ digits per step, from a start of ~0.4 digits, needs roughly $\frac{12}{0.53}\approx$ **23 steps.**

**(b)** **Whether $g'(L)=0$.** Both iterations converge, both use only arithmetic, and both have the same fixed point. The Babylonian map's derivative vanishes there; the other's does not. **That single number is the entire difference.**

*Marking: 3 + 3. **(b) must name the derivative at the fixed point.** "One is Newton's method" earns 2 — true, and worth noting that the Babylonian iteration *is* Newton's method applied to $x^2-2$, but the criterion is the explanation.*

---

## Part D — The Logistic Map (25 pts)

### D1 (6)

$$x = rx(1-x) \implies 1 = r(1-x) \implies x^\ast = 1-\frac1r$$

$$g(x) = rx-rx^2 \implies g'(x) = r-2rx = r(1-2x)$$

At $x^\ast$: $\;g'(x^\ast) = r\left(1-2+\frac2r\right) = r\left(\frac2r-1\right) = \boxed{2-r}$

*Verified.*

### D2 (7)

$$|2-r|<1 \iff -1<2-r<1 \iff \boxed{1<r<3}$$

*Marking: 7. The bound $r=3$ is the first period-doubling bifurcation and should be named as the threshold.*

### D3 (12)

After 2000 warm-up iterations from $x_0=0.5$:

| $r$ | behaviour | orbit (first four values) |
|---|---|---|
| $2.5$ | **fixed point** (period 1) | $0.6,\ 0.6,\ 0.6,\ 0.6$ |
| $3.2$ | **period 2** | $0.79945549,\ 0.51304451,\ \ldots$ |
| $3.5$ | **period 4** | $0.87499726,\ 0.38281968,\ 0.82694071,\ 0.50088421$ |
| $3.55$ | **period 8** | $0.8873709,\ 0.35480045,\ 0.81265567,\ 0.54047483,\ldots$ |
| $3.9$ | **no repetition — chaotic** | $0.97429573,\ 0.097669884,\ 0.34370886,\ 0.87973502,\ldots$ |

*(All verified.)*

**(a)** Only $r=2.5$ has a stable fixed point, and $1<2.5<3$ ✓ — matching D2. At $r=2.5$, $x^\ast = 0.6$ and $g'(x^\ast) = -0.5$, $|g'|<1$ ✓. At $r=3.2$ and $3.9$, $g'(x^\ast) = -1.2$ and $-1.9$, both $|g'|>1$ ✓.

**(b)** At $r=3.2$ the fixed point has become **unstable**, and the orbit settles instead into a **cycle of period 2**, alternating between two values. The fixed point still exists — it is just repelling.

**(c)** **Period doubling.** As $r$ increases past 3 the period goes $1\to2\to4\to8\to\cdots$, with each doubling occurring over a shorter interval of $r$, until the periods become infinite and the orbit never repeats.

**(d)** The rule is a **deterministic quadratic** — no randomness, no noise, four characters of arithmetic. Yet at $r=3.9$ the orbit never repeats and two nearby starting values separate exponentially fast.

**So determinism does not imply predictability.** Long-run prediction would require knowing $x_0$ to unattainable precision, and any error — including floating-point rounding — is amplified at every step. **This is chaos**, and it is why weather forecasts degrade after about a week despite the underlying physics being entirely deterministic.

*Marking: 4 (table) + 2 + 2 + 4. **(d) must separate determinism from predictability.** "It's random" earns 0 — it is emphatically not random, and that is the whole point.*

---

## Part E — Reflection (10 pts)

### E1 (5)

| $g'(L)$ | Behaviour | Evidence from this lab |
|---|---|---|
| $g'(L)=0$ | **quadratic** — digits double | Babylonian: $1,2,5,11,24,48$ digits; $e_n/e_{n-1}^2\to\frac{1}{2\sqrt2}$ |
| $0<\lvert g'(L)\rvert<1$ | **linear** — constant factor | $g'=0.2929$; error ratios $\to2+\sqrt2=3.414$ |
| $\lvert g'(L)\rvert>1$ | **repelling** — no convergence | logistic $r\ge3$: $g'=2-r$, orbits go to cycles then chaos |

*Marking: 5 for a complete table with evidence in each row.*

### E2 (5)

**This lab is the strongest case yet for numerical methods**, and it complicates the earlier framing.

Part B produced 48 correct digits of an irrational number using **six steps of elementary arithmetic** — no antiderivative, no series, no special function. That is a numerical method decisively winning.

**But the reason it wins is exact:** the quadratic rate was *predicted in advance* from $g'(\sqrt2)=0$, computed symbolically before any iteration was run. **The numerics executed; the exact analysis explained and predicted.**

*Accept either headline — "numerics wins" or "the exact criterion is what made the numerics good" — provided the interplay is identified.*

*Marking: 5. **A student who observes that the exact derivative predicted the numerical behaviour has the best available answer.** Award full marks and say so.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 20 |
| B | 25 |
| C | 20 |
| D | 25 |
| E | 10 |
| **Total** | **100** |

---

## Checkoff Checklist

1. **`mp.mp.dps` set to 50+** — otherwise Part B stops at step 4
2. A2 gives $g'(\sqrt2)=0$ **exactly, by hand**
3. B2 identifies the constant as $\frac{1}{2\sqrt2}$
4. B3 has digits doubling: $1,2,5,11,24,48$
5. C1 gives $g'(\sqrt2)=1-\frac{\sqrt2}{2}$ **exactly**
6. C2's ratio matches $1/|g'| = 2+\sqrt2$
7. **D1 derives $g'(x^\ast)=2-r$**
8. D2 gives $1<r<3$
9. **D3(d) distinguishes deterministic from predictable**

---

## Note for the Debrief

> **One number, three worlds.** Every iteration in this lab is $a_{n+1}=g(a_n)$, and the entire
> difference between them is $g'$ at the fixed point.
>
> $g'=0$: **48 correct digits in six steps.**
> $0<|g'|<1$: about half a digit per step — perfectly usable, but the gap widens without limit.
> $|g'|>1$: no convergence at all, and at $r=3.9$ a deterministic quadratic that nobody can predict.

**The middle case is worth quantifying, because the gap is not a fixed factor:**

| digits wanted | Babylonian | linear | ratio |
|---|---|---|---|
| 12 | ~5 steps | ~23 steps | 5× |
| 100 | ~8 steps | ~188 steps | 24× |
| 1000 | ~11 steps | ~1876 steps | **171×** |

*(Computed.)* **Quadratic beats linear by a margin that grows with the precision you demand** — which is exactly the Lab 3 lesson about order of convergence, now for iterations rather than quadrature.

Then the connection forward:

> **Next week the objects are infinite sums, and the same question returns immediately.** A geometric
> series $\sum r^n$ converges exactly when $|r|<1$ — and that is this lab's criterion, for the map
> $g(x)=rx$ with fixed point 0 and $g'(0)=r$.
>
> **The Ratio Test in Week 8 is nothing but this**: compute the factor by which terms shrink, and ask
> whether it is less than 1. **You have already met the idea three times — in Week 3's $p$-test, in
> today's fixed points, and in the geometric sequence.** Next week it becomes a theorem about sums.

---

*MATH 142 · Week 6 · Lab 06 Solutions · Instructor Only*

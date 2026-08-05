# MATH 142 · Calculus II
## Lab 08 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures produced by running the lab at 30-digit precision.

---

## Part A — The Leibniz Error Bound (25 pts)

### A1 (10), A2 (8)

$\ln2 = 0.693147180559945$

| $N$ | $s_N$ | true error | bound $\frac{1}{N+1}$ | error/bound |
|---:|---|---|---|---|
| $10$ | $0.645634920635$ | $4.75123\times10^{-2}$ | $9.09091\times10^{-2}$ | $0.5226$ |
| $20$ | $0.668771403175$ | $2.43758\times10^{-2}$ | $4.76190\times10^{-2}$ | $0.5119$ |
| $50$ | $0.683247160576$ | $9.90002\times10^{-3}$ | $1.96078\times10^{-2}$ | $0.5049$ |
| $100$ | $0.688172179310$ | $4.97500\times10^{-3}$ | $9.90099\times10^{-3}$ | $0.5025$ |
| $200$ | $0.690653430482$ | $2.49375\times10^{-3}$ | $4.97512\times10^{-3}$ | $0.5013$ |
| $400$ | $0.691898743055$ | $1.24844\times10^{-3}$ | $2.49377\times10^{-3}$ | $0.5006$ |

**The bound holds at every $N$** ✓

**A2 — the ratio approaches $\boxed{\tfrac12}$.**

**Geometric reason:** the sum lies **between** $s_N$ and $s_{N+1}$, and those two partial sums differ by exactly $b_{N+1}$. For a smoothly decreasing $b_n$, $S$ sits close to the **midpoint** of that interval — so the distance from either endpoint is about half the gap. **The bound measures the whole bracket; the true error is roughly half of it.**

*Marking A1: 10. A2: 4 for the constant, **4 for the geometric explanation** referring to the bracket.*

### A3 (7)

Require $\frac{1}{N+1}<\varepsilon$:

- **(a)** $\varepsilon=5\times10^{-4}$ (3 d.p.) $\implies N\approx2000$
- **(b)** $\varepsilon=5\times10^{-7}$ (6 d.p.) $\implies N\approx2\times10^{6}$

**Comment:** two million terms for six decimals of $\ln2$ — **impractical.** *(For comparison: Lab 6's Babylonian iteration gave 48 digits of $\sqrt2$ in six steps.)*

*Marking: 2 + 2 + 3. **Accept $N\approx10^3$ and $10^6$ orders of magnitude.***

---

## Part B — Rearranging to Any Target (30 pts)

### B1 (12)

With 300,000 terms:

| target $T$ | partial sum reached |
|---|---|
| $\ln2 = 0.6931471806$ | $0.693145513896$ |
| $1$ | $0.999999870696$ |
| $\pi$ | $3.14155185372$ |
| $0$ | $-1.04166015625\times10^{-6}$ |
| $-2$ | $-1.99978475893$ |

*(All verified.)*

*Marking: 12 for a working implementation reaching all five targets. **Accuracy of the last few digits will vary with the exact stopping point** — do not penalise; the algorithm halts mid-sweep.*

### B2 (8) — the crossings, for $T=\pi$

| after $n$ terms | running total |
|---:|---|
| $76$ | $3.14712528992$ |
| $77$ | $2.64712528992$ |
| $206$ | $3.14326049831$ |
| $207$ | $2.89326049831$ |
| $339$ | $3.14179666163$ |
| $340$ | $2.97512999496$ |
| $474$ | $3.14251748726$ |
| $475$ | $3.01751748726$ |

*(Verified.)*

**What is happening:** the total repeatedly overshoots $\pi$ from above, then undershoots from below, and **the size of each overshoot shrinks** — because the overshoot is at most the last term added, and those terms $\to0$.

Note the **asymmetry**: the upward sweeps take many terms (the positives $\frac{1}{2k+1}$ are small), while a single negative term drops the total a long way early on. Both sweeps lengthen as the algorithm proceeds.

*Marking: 5 table, 3 explanation. **The explanation must connect the shrinking overshoot to $b_n\to0$.***

### B3 (10)

**(a)** The positive terms $\sum\frac{1}{2k+1}$ diverge to $+\infty$, so the upward sweep must eventually exceed any $T$. The negative terms $\sum\frac{1}{2k}$ diverge to $-\infty$, so the downward sweep must eventually fall below any $T$. **Each loop terminates.**

**(b)** At the moment of each crossing, the total differs from $T$ by **at most the last term used**. Since the terms tend to 0, those discrepancies tend to 0, and **the partial sums are trapped in an interval around $T$ that shrinks to nothing.** Hence they converge to $T$.

**(c)** **Commutativity of addition fails — for infinite series.**

It is not a paradox because **a series is not an addition**: it is $\lim_{N\to\infty}s_N$. Rearranging the terms produces a **different sequence** $\{s_N\}$, and different sequences may have different limits. **Commutativity of finite addition is untouched**; what fails is the assumption that an infinite series inherits it.

**(d)** **No.** $\sum\frac{(-1)^{n+1}}{n^2}$ converges **absolutely** ($\sum\frac1{n^2}$ converges), so its positive and negative parts **each converge** — there is no $\infty-\infty$ to re-resolve, and the upward sweep would stall permanently once the remaining positives could no longer reach $T$. **Every rearrangement of an absolutely convergent series has the same sum.**

*Marking: 2 + 3 + 3 + 2. **(c) is the question.** An answer of "you can't rearrange infinite sums" earns 1 — true but not an explanation. Full marks require locating the failure in the definition.*

---

## Part C — Making It Fast (25 pts)

### C1 (10), C2 (10)

$$\widetilde S_N = \frac{s_N+s_{N+1}}{2}$$

| $N$ | raw error | **averaged error** | ratio on doubling |
|---:|---|---|---|
| $10$ | $4.75123\times10^{-2}$ | $2.05771\times10^{-3}$ | — |
| $20$ | $2.43758\times10^{-2}$ | $5.66254\times10^{-4}$ | — |
| $50$ | $9.90002\times10^{-3}$ | $9.60984\times10^{-5}$ | — |
| $100$ | $4.97500\times10^{-3}$ | $2.45062\times10^{-5}$ | $3.921$ |
| $200$ | $2.49375\times10^{-3}$ | $6.18789\times10^{-6}$ | $3.960$ |
| $400$ | $1.24844\times10^{-3}$ | $1.55471\times10^{-6}$ | $3.980$ |
| $800$ | — | $3.89650\times10^{-7}$ | $3.990$ |

**C2(a)** The ratio $\to\mathbf{4}$ on doubling $N$.

**C2(b)** $2^p = 4$ gives $p=2$: **the averaged method is order 2**, against **order 1** for the raw partial sums.

*(At $N=400$ the improvement is a factor of about $800$.)*

*Marking C1: 10. C2: 5 + 5.*

### C3 (5)

**Both improvements come from a two-sided bracket, but the brackets have different widths.**

- **Lab 7 (Integral Test):** the bracket was $\frac{1}{N+1}\le R_N\le\frac1N$, of width $\frac{1}{N(N+1)}\approx\frac{1}{N^2}$. Averaging leaves an error $O(N^{-3})$ — order **3**.
- **Lab 8 (alternating):** the bracket is $[s_N,s_{N+1}]$, of width $b_{N+1} = \frac{1}{N+1}\approx\frac1N$. Averaging leaves $O(N^{-2})$ — order **2**.

> **The gain is always "one better than the bracket width".** The Integral Test's bracket is narrower
> because it uses information about the whole tail; the alternating bracket uses only the next term.
> **Better information, better bracket, better order.**

*Marking: 5. **Full marks require comparing the two bracket widths**, not just reporting the two orders.*

---

## Part D — Reflection (20 pts)

### D1 (10)

**The structural fact:** for an alternating series with decreasing terms, **the partial sums oscillate about the limit, straddling it**, with the gap between consecutive ones equal to the next term.

- **Constructive use (Part C):** the limit is near the *midpoint* of the straddle, so averaging cancels the leading error — order 1 becomes order 2.
- **Destructive use (Part B):** the straddling means you can *steer*. Choosing which side to approach from, and when to switch, lets you park the partial sums anywhere you like.

**Both are the same oscillation.** One exploits that the limit is in the middle; the other exploits that you may choose where the middle is.

*Marking: 10 — 4 for the structural fact, 3 each for the two uses. **The unifying observation is the point**; two separate correct answers with no connection drawn earn 6.*

### D2 (10)

**Lab 8 entry: the computation was correct and the question was ill-posed.**

Every target in Part B was reached to high accuracy. **Nothing was miscomputed.** What the computation produced was **the sum of a particular rearrangement** — and for a conditionally convergent series that is a different quantity for every ordering.

**"The sum of the series" is only well defined once the order is fixed.** In natural order it is $\ln2$; the symbol $\sum a_n$ silently carries the ordering, and Riemann's theorem says the ordering is doing real work.

**Most resembles no earlier lab.** In Labs 0–7 the machine was either right, slow, or wrong. **Here it was right, fast, and answering a question the notation had failed to ask precisely.**

*Marking: 10. **Full marks require the observation that the ambiguity is in the question, not the computation.** "The computer was wrong" earns 0 — it was not. "It computed a rearrangement" earns 7 without the point about notation.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 30 |
| C | 25 |
| D | 20 |
| **Total** | **100** |

---

## Checkoff Checklist

1. A1's bound holds at **every** $N$
2. **A2 gives $\frac12$ with the bracket explanation**
3. B1 reaches all five targets
4. B2's crossings show shrinking overshoot
5. **B3(c) locates the failure in the definition of a series**
6. B3(d) says no, because absolute convergence
7. **C2 gives order 2 from the ratio 4**
8. C3 compares the two **bracket widths**
9. **D2 says the computation was correct**

---

## Note for the Debrief

> Three hundred thousand numbers. Added in one order they give $\ln 2 = 0.6931$. Added in another they
> give $\pi$. In another, $-2$. **Every one of those computations is correct.**
>
> Nothing about the numbers changed — only the order. And the reason this is possible, rather than
> absurd, is the definition you were given in Week 7: **a series is the limit of its partial sums.**
> Reorder the terms and you have a different sequence of partial sums, hence possibly a different
> limit. **The $\sum$ sign looks like addition and guarantees none of addition's properties.**

Then the constructive half:

> **And the same oscillation you exploited to break the series is what lets you accelerate it.**
> Averaging consecutive partial sums took the error from order 1 to order 2 — a factor of 800 at
> $N=400$, for one line of arithmetic. **Last week the Integral Test's bracket bought you order 3.**
> **Better information about the tail, better order. That is the whole game.**

Then set up Week 9:

> Next week we put a variable in: $\sum c_nx^n$. **The Ratio Test finds where it converges** — and at
> the two endpoints the Ratio Test gives exactly $L=1$, which you now know means *silence*. **Those
> endpoints have to be settled by hand, with the tests of Weeks 7 and 8.** Everything you have built
> over three weeks gets used at once.

---

*MATH 142 · Week 8 · Lab 08 Solutions · Instructor Only*

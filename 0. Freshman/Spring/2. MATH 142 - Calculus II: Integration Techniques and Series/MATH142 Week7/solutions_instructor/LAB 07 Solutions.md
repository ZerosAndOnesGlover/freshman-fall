# MATH 142 · Calculus II
## Lab 07 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures produced by running the lab.

> **Do not check students' work against `mpmath`'s `nsum` with an infinite upper limit.** Three
> separate failures of that routine were found while preparing this week — see the note at the end.
> **Use partial sums plus an Integral Test bracket**, which is what the lab teaches anyway.

---

## Part A — How Slowly the Harmonic Series Diverges (25 pts)

### A1 (8), A2 (7)

$\gamma = 0.577215664901533$

| $N$ | $H_N$ | $\ln N+\gamma$ | difference | $N\times$diff |
|---:|---|---|---|---|
| $10$ | $2.92896825397$ | $2.87980075790$ | $4.9167\times10^{-2}$ | $0.49167$ |
| $10^2$ | $5.18737751764$ | $5.18238585089$ | $4.9917\times10^{-3}$ | $0.49917$ |
| $10^4$ | $9.78760603604$ | $9.78755603688$ | $4.9999\times10^{-5}$ | $0.49999$ |
| $10^6$ | $14.3927267229$ | $14.3927262229$ | $5.0000\times10^{-7}$ | $0.50000$ |

**A2(a)** The difference **tends to 0** — confirming $H_N\to\ln N+\gamma$.

**A2(b)** $N\times\text{diff}\to0.5$, so $\boxed{c=\tfrac12}$ and the difference behaves like $\dfrac{1}{2N}$.

*Marking A1: 8. A2: 3 for (a), **4 for identifying $c=\frac12$ from the scaled column** — the same technique as Lab 1 B3 and Lab 3 B3.*

### A3 (10)

Solving $\ln n+\gamma = S$ gives $n\approx e^{S-\gamma}$:

| target $S$ | terms needed |
|---:|---|
| $5$ | $83$ |
| $10$ | $1.24\times10^{4}$ |
| $20$ | $2.72\times10^{8}$ |
| $50$ | $2.91\times10^{21}$ |
| $100$ | $1.51\times10^{43}$ |

*(Computed.)*

**Comment:** at one term per nanosecond, reaching a sum of 50 would take about $9\times10^{4}$ years; reaching 100 would take longer than the age of the universe by twenty-five orders of magnitude. **The series diverges, and no computation will ever witness it.**

*Marking: 6 table, 4 comment. **The comment must engage with the scale**, not merely say "that's a lot".*

---

## Part B — How Slowly Basel Converges (25 pts)

### B1 (8), B2 (8)

$\frac{\pi^2}{6} = 1.64493406684823$

| $N$ | $s_N$ | error | $N\times$error |
|---:|---|---|---|
| $10$ | $1.54976773117$ | $9.51663\times10^{-2}$ | $0.951663$ |
| $10^2$ | $1.63498390018$ | $9.95017\times10^{-3}$ | $0.995017$ |
| $10^3$ | $1.64393456668$ | $9.99500\times10^{-4}$ | $0.999500$ |
| $10^4$ | $1.64483407184$ | $9.99950\times10^{-5}$ | $0.999950$ |

**B2:** $N\times\text{error}\to\boxed{1}$, so the error behaves like $\dfrac1N$ — **order 1** convergence.

*Marking: 8 + 8. The scaled column is the point.*

### B3 (9)

**(a)** Error $\approx\frac1N$, so $D$ digits needs $N\approx10^{D}$: **$10^6$ terms for 6 digits, $10^{10}$ for 10.**

**(b)**

| method | cost for 10 digits |
|---|---|
| Basel direct summation | $10^{10}$ terms |
| Simpson (Lab 0) | 128 points |
| Babylonian (Lab 6) | 4 steps |

**(c)** **No.** $10^{10}$ terms is hours of computation for ten digits of a constant known to billions of places by other means — and accumulated floating-point rounding would corrupt the answer well before then.

*Marking: 4 + 3 + 2.*

---

## Part C — The Remainder, and a Free Improvement (30 pts)

### C1 (8)

| $N$ | $\frac{1}{N+1}$ (lower) | true $R_N$ | $\frac1N$ (upper) | holds |
|---:|---|---|---|---|
| $10$ | $0.09090909$ | $0.09516634$ | $0.10000000$ | ✓ |
| $10^2$ | $0.00990099$ | $0.00995017$ | $0.01000000$ | ✓ |
| $10^3$ | $0.00099900$ | $0.00099950$ | $0.00100000$ | ✓ |

*(Verified: both inequalities hold at every $N$.)*

*Marking: 8 for the table with both bounds verified.*

### C2 (12), C3 (10)

$$\widetilde S_N = s_N+\frac12\left(\frac{1}{N+1}+\frac1N\right)$$

| $N$ | raw error | **averaged error** | ratio per decade |
|---:|---|---|---|
| $10$ | $9.5166\times10^{-2}$ | $2.8821\times10^{-4}$ | — |
| $10^2$ | $9.9502\times10^{-3}$ | $3.2839\times10^{-7}$ | $877.7$ |
| $10^3$ | $9.9950\times10^{-4}$ | $3.3283\times10^{-10}$ | $986.6$ |
| $10^4$ | $9.9995\times10^{-5}$ | $3.3328\times10^{-13}$ | $998.7$ |

**C3(a)** The ratio $\to\mathbf{1000}$ per factor of 10 in $N$. Since $10^p = 1000$ gives $p=3$, the improved method is **order 3.**

**C3(b)** **From order 1 to order 3.**

**C3(c)** Order 3 means error $\approx\frac{C}{N^3}$ with $C\approx\frac13$; for $10^{-10}$ we need $N\approx10^{3}$ — **about a thousand terms, against $10^{10}$ for the raw sum.** *(Confirmed by the table: at $N=10^3$ the error is already $3.3\times10^{-10}$.)*

**A factor of ten million fewer terms.**

**C3(d)** **The extra accuracy came from the Integral Test**, not from more computation. The raw sum discards the tail entirely; the bracket $\frac{1}{N+1}\le R_N\le\frac1N$ **is information about the tail obtained by an exact theorem**, and averaging exploits the fact that $R_N$ sits close to the middle of a bracket of width $\frac{1}{N(N+1)}\approx\frac{1}{N^2}$.

**So the error of the average is $O(N^{-2})$ smaller than the raw error $O(N^{-1})$** — hence order 3.

*Marking C2: 12 for the table. C3: 3 + 2 + 3 + 2. **(d) must locate the source of the gain in the theorem**, not in the arithmetic.*

---

## Part D — Reflection (20 pts)

### D1 (10)

| | Divergent: $\sum\frac1n$ | Convergent: $\sum\frac1{n^2}$ |
|---|---|---|
| **Partial sums** | grow like $\ln N$ — need $10^{43}$ terms to reach 100 | error $\frac1N$ — need $10^{10}$ terms for 10 digits |
| **What settles it** | **Oresme's block argument** — five lines, no calculus | **The Integral Test bracket** — one integral |
| **Work** | trivial | trivial |

**In both cases an exact argument of a few lines settles what no computation can.**

*Marking: 10, with both rows and the "work" comparison. **The observation that both exact arguments are short is the point.***

### D2 (10)

**Lab 7 entry: numerics fails on both series, and an exact theorem rescues one of them.**

**Most resembles Lab 3**, where numerics could not decide convergence and the $p$-test settled it in a line. **But Part C adds something no earlier lab had**: the exact theorem did not merely *replace* the numerical method — it **repaired** it, raising the order from 1 to 3 and making direct summation viable.

**Which deserves the credit?** The honest answer is that neither works alone here:

- The Integral Test alone gives a bracket of width $\frac1{N(N+1)}$ but no value.
- Summation alone gives a value with error $\frac1N$.
- **Together they give order 3.**

*Marking: 10. **Full marks require recognising that Part C is a collaboration, not a competition.** A student who answers only "the theorem wins" earns 6 — it is the more common half of the answer and not wrong, but it misses that the theorem produced no number by itself.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 25 |
| C | 30 |
| D | 20 |
| **Total** | **100** |

---

## Checkoff Checklist

1. A2(b) identifies $c=\frac12$ from the **scaled** column
2. A3's term counts are of order $10^{8}$, $10^{21}$, $10^{43}$
3. **B2 gives $N\times$error $\to1$**, hence order 1
4. C1 verifies **both** inequalities
5. **C3(a) gives order 3 from the ratio 1000**
6. C3(d) attributes the gain to the theorem
7. **D2 recognises Part C as a collaboration**

---

## Appendix: Three `nsum` Failures

Preparing this week's material exposed three wrong answers from `mpmath.nsum` with an infinite upper limit. **Recorded here so TAs do not check student work against them.**

| Series | `nsum` | correct | error |
|---|---|---|---|
| $\sum\frac{\ln n}{n^2}$ | $0.936715596751$ | $0.937548254316$ *(= $-\zeta'(2)$)* | $8.3\times10^{-4}$ |
| $\sum\frac{\sin^2n}{n^2}$ | $1.07071852154$ | $1.07079632679$ *(= $\frac{\pi-1}{2}$)* | $7.8\times10^{-5}$ |
| $\sum_{n\ge2}\frac{1}{n(\ln n)^3}$ | $2.06051618$ | $2.0658865$ | $5.4\times10^{-3}$ |

**All three were caught the same way**, and the method is this lab's Part C:

> **Compute a partial sum, then bracket the tail with the Integral Test.** If the library's answer
> falls outside the bracket — or, more crudely, if it is *below a partial sum of positive terms* — it
> is wrong.

For the third, the bracket at $N=10^6$ pins the value to ten significant figures:

$$2.065886539 \le S \le 2.065886539$$

> **This is worth telling the students.** The course has spent six weeks noting that computer algebra
> systems fail in visible ways — unevaluated integrals, wrong branches, unrecognisable forms. **A
> numerical library fails differently: it returns a plausible number to twelve digits and says
> nothing.** The only defence is to know a property the answer must have. **This week you learned
> one, and it is strong enough to audit a professional library.**

---

*MATH 142 · Week 7 · Lab 07 Solutions · Instructor Only*

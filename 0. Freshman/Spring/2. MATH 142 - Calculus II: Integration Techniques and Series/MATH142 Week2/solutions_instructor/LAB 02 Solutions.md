# MATH 142 · Calculus II
## Lab 02 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All results below were produced by running the lab.

> **This lab is exact, not numerical.** Unlike Labs 0 and 1 there are no measurement tables and no
> machine-dependent figures — every number is a rational or a rational plus $\pi$, and students should
> reproduce them **exactly**. A student reporting `0.00126448926734962` where the answer is
> $\frac{22}{7}-\pi$ has evaluated rather than solved, which Part E is about.

---

## Part A — The Machinery (25 pts)

### A1 (10) — decomposition with verification

| | Expression | `sp.apart` | recombines |
|---|---|---|---|
| (i) | $\frac{x+5}{(x+1)(x-2)}$ | $-\frac{4}{3(x+1)}+\frac{7}{3(x-2)}$ | ✓ |
| (ii) | $\frac{3x+1}{(x-1)^2(x+2)}$ | $\frac{5}{9(x-1)}+\frac{4}{3(x-1)^2}-\frac{5}{9(x+2)}$ | ✓ |
| (iii) | $\frac{x^2+1}{(x+1)(x^2+4)}$ | $\frac{2}{5(x+1)}+\frac{3(x-1)}{5(x^2+4)}$ | ✓ |
| (iv) | $\frac{2x^2-x+4}{x^3+4x}$ | $\frac1x+\frac{x-1}{x^2+4}$ | ✓ |

*Marking: 10 for correct output on all four with the recombination check passing.*

> **A trap worth knowing about before the lab runs.** `sp.apart(expr)` without the variable argument
> will sometimes return the expression **unchanged**, particularly when the denominator is given in
> factored form. `sp.apart(expr, x)` works. Students who report "apart did nothing" have hit this;
> **it is not their error, and they should not lose marks for it** — tell them to pass the variable.
> This was hit while preparing the lab.

*(iv) is included because the denominator $x^3+4x$ **must be factored** as $x(x^2+4)$ first. `apart` does this automatically, which is worth pointing out: the machine does the step students forget.*

### A2 (8) — the improper case

`sp.apart((x**3+4)/(x**2+4), x)` returns

$$x - \frac{4(x-1)}{x^2+4}$$

**It still recombines correctly** — `apart` did *not* fail.

What happened: **`apart` performed the polynomial division itself**, returning (polynomial) + (proper fraction). That is exactly Step 0 of the algorithm. The answer is not "constants over factors" because the improper part contributes a polynomial term $x$, which no sum of proper fractions can produce.

*Marking: 4 for reporting the output correctly, 4 for the explanation. **Full marks require identifying that the leading $x$ is the quotient** of the division. "It did something different" earns 1.*

*This connects directly to PS 2 D2, where a student concludes the integral is impossible after skipping precisely this step. Worth mentioning that the CAS is more careful than the student was.*

### A3 (7) — antiderivatives verified by differentiation

All five verify. For reference:

| Expression | $\int$ |
|---|---|
| (i) | $\frac73\ln\lvert x-2\rvert - \frac43\ln\lvert x+1\rvert$ |
| (ii) | $\frac59\ln\left\lvert\frac{x-1}{x+2}\right\rvert - \frac{4}{3(x-1)}$ |
| (iii) | $\frac25\ln\lvert x+1\rvert+\frac3{10}\ln(x^2+4)-\frac3{10}\arctan\frac x2$ |
| (iv) | $\ln\lvert x\rvert+\frac12\ln(x^2+4)-\frac12\arctan\frac x2$ |
| (v) | $\frac{x^2}{2}-2\ln(x^2+4)+2\arctan\frac x2$ |

*Marking: 7 for running the check on all five and reporting that each verifies.*

**Point out the pattern in the debrief**: every answer is a logarithm, an arctangent, a rational function, or a polynomial — the theorem's short list, and nothing else. **(ii) is the only one with a rational term, and it is the only one with a repeated factor.**

---

## Part B — The Integral (25 pts)

### B1 (8)

$$x^4(1-x)^4 = x^8-4x^7+6x^6-4x^5+x^4$$

*Marking: 8. Straightforward; deduct for algebra slips only.*

### B2 (10) — the division

$$\text{quotient} = x^6-4x^5+5x^4-4x^2+4, \qquad \text{remainder} = -4$$

$$\frac{x^4(1-x)^4}{1+x^2} = x^6-4x^5+5x^4-4x^2+4-\frac{4}{1+x^2}$$

*Verified symbolically: the identity holds exactly.*

*Marking: 6 for quotient and remainder, 4 for verifying the identity. **Note the quotient has no $x^3$ or $x$ term** — a student who writes six terms instead of five has probably mis-divided.*

### B3 (7) — term by term

| term | $\int_0^1$ |
|---|---|
| $x^6$ | $\tfrac17$ |
| $-4x^5$ | $-\tfrac23$ |
| $5x^4$ | $1$ |
| $-4x^2$ | $-\tfrac43$ |
| $4$ | $4$ |
| $-\dfrac{4}{1+x^2}$ | $-4\arctan(1) = -\pi$ |

$$\text{Sum} = \frac17 - \frac23 + 1 - \frac43 + 4 - \pi = \frac17 + 3 - \pi = \boxed{\frac{22}{7}-\pi}$$

**Decimal:** $0.00126448926734962$

*Verified symbolically: the total equals $\frac{22}{7}-\pi$ exactly.*

*Marking: 5 for the six terms, 2 for the decimal. **The rational part collecting to exactly $\frac{22}{7}$ is the moment of the lab** — $-\frac23-\frac43 = -2$ and $1+4 = 5$, so $\frac17 - 2 + 5 = \frac17+3 = \frac{22}{7}$. Make sure they see it.*

---

## Part C — The Bounds (25 pts)

### C1 (8)

On $[0,1]$, $1\le 1+x^2\le 2$, so for the non-negative numerator $x^4(1-x)^4$:

$$\frac{x^4(1-x)^4}{2}\;\le\;\frac{x^4(1-x)^4}{1+x^2}\;\le\;x^4(1-x)^4$$

Integrating preserves the inequalities — this is the **comparison property** of the integral from **Week 0, Lecture 1 §4**.

*Marking: 5 for the chain of inequalities, **3 for naming the comparison property.** A student who inverts an inequality when dividing (forgetting the numerator is non-negative) should be shown the non-negativity requirement explicitly.*

### C2 (7)

$$\int_0^1 x^4(1-x)^4\,dx = \boxed{\frac{1}{630}}$$

*Verified symbolically.*

*Marking: 7. Expanding and integrating term by term is fine; so is recognising it as a Beta integral $B(5,5) = \frac{4!\,4!}{9!}$.*

### C3 (10) — bounds on $\pi$

From $\frac{1}{1260}\le\frac{22}{7}-\pi\le\frac{1}{630}$:

$$\frac{22}{7}-\frac{1}{630}\;\le\;\pi\;\le\;\frac{22}{7}-\frac{1}{1260}$$

$$\boxed{\frac{1979}{630}\;\le\;\pi\;\le\;\frac{3959}{1260}}$$

$$3.14126984126984 \;\le\; \pi \;\le\; 3.14206349206349$$

**(a)** $\pi = 3.14159265358979$ — inside both bounds ✓ *(verified)*

**(b)** Both bounds begin $3.141\ldots$ and then diverge ($3.1412\ldots$ vs $3.1420\ldots$), so this pins down **three decimal places**: $\pi = 3.141\ldots$

**(c)** Interval width $= \dfrac{1}{1260} \approx 0.000794$.

*Marking: 5 for the bounds (exact fractions required), 2 for (a), 2 for (b), 1 for (c). **Deduct 2 if the inequality is flipped** — subtracting the *larger* bound gives the *lower* bound on $\pi$, and this reversal is the most common error in the part.*

---

## Part D — Doing Better (15 pts)

### D1 (9)

$$\int_0^1\frac{x^8(1-x)^8(25+816x^2)}{3164(1+x^2)}\,dx = \boxed{\frac{355}{113}-\pi}$$

**It comes out as (rational) $-\pi$**, the same orientation as Part B.

*Verified symbolically.*

*Marking: 9 for the exact result **with the orientation stated correctly.** Deduct 3 for reporting $\pi - \frac{355}{113}$ — the sign is the entire content of D2, and getting it backwards there follows from getting it backwards here.*

> **A note from preparing this lab.** The direction was guessed wrong on first writing and corrected
> by computing it. **The integrand is manifestly positive, so the integral must be positive, so the
> rational number must exceed $\pi$** — the sign is forced and needs no numerical comparison. Any
> student who reasons that way rather than by comparing decimals has understood the point.

### D2 (6)

**(a)** The integrand is a product of $x^8\ge0$, $(1-x)^8\ge0$, $(25+816x^2)>0$, and $\frac{1}{3164(1+x^2)}>0$, hence **non-negative on $[0,1]$ and strictly positive on $(0,1)$.** Therefore the integral is positive, so

$$\frac{355}{113}-\pi > 0 \implies \boxed{\frac{355}{113} > \pi}$$

**No decimal comparison is used or needed.**

**(b)** The integral equals $2.66764189062422\times10^{-7}$, which **is** $\left|\pi-\frac{355}{113}\right|$ — they are the same number, since the integral *is* the difference.

*Marking: 4 for (a) — **the positivity argument must be explicit, and marks come off for arguing from decimals** — and 2 for (b), including the observation that the two quantities are identical rather than merely close.*

*$\frac{355}{113}$ is accurate to about $2.7\times10^{-7}$ — six decimal places, from a three-digit denominator.*

*Worth mentioning how good that is: **no fraction with a smaller denominator comes closer, and none does until $\frac{52163}{16604}$** — and even that only improves the error from $2.66764\times10^{-7}$ to $2.66213\times10^{-7}$, a gain of 0.2% for 147 times the denominator. (Searched exhaustively over all $q < 60000$.) The sequence of record-holders on the way up is $\frac31,\frac{13}4,\frac{16}5,\frac{19}6,\frac{22}7,\frac{179}{57},\frac{333}{106},\frac{355}{113}$ — **and $\frac{22}{7}$ is on that list**, which is why it was taught to you.*

---

## Part E — Reflection (10 pts)

**E1 (5).** A numerical evaluation gives a number with an error bar; **an exact evaluation gives an identity.**

To prove $\frac{22}{7}>\pi$ you need to know the difference is **positive**, not merely that it appears positive to fifteen digits. A numerical computation returning $0.0012644\ldots$ leaves open — in principle — that the true value is negative and the computation is wrong; you would need a rigorous error bound to close that gap, and that bound is itself extra mathematics.

The exact route closes it in one step: **the integrand is positive, therefore the integral is positive, therefore the inequality holds.** No error analysis at all.

*Marking: 5. **The key idea is that positivity of the integrand gives a proof, where numerics gives evidence.** Award 2 for "exact is more accurate" — that misses it; accuracy is not the issue, logical status is.*

**E2 (5).** Any two of:

- **You never have to wonder whether it can be done.** For a general integrand, failing to find an antiderivative leaves you unsure whether you lack skill or whether none exists. For a rational function, the answer is always yes, and failure means you made an error.
- **It is an algorithm, so it can be automated** — every CAS implements exactly this, which is why `apart` and `integrate` never fail on a rational function.
- **It tells you the shape of the answer in advance**: logarithms, arctangents, rational functions, polynomials. If your answer contains anything else, it is wrong.
- **It converts other problems into solved ones** — rationalizing substitutions (Lecture 2 §6) work precisely because *reaching* a rational integrand means you are finished.

*Marking: 5 for any two substantive points. The first and third are the ones with practical bite.*

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

1. `sp.apart(expr, **x**)` — with the variable (see the A1 note)
2. All four decompositions recombine
3. A2 identifies the leading $x$ as the **quotient**
4. Division in B2 gives quotient $x^6-4x^5+5x^4-4x^2+4$, remainder $-4$
5. B3's rational part collects to **exactly $\frac{22}{7}$**
6. C1 names the **comparison property**
7. C3's bounds are the right way round
8. **D2(a) argues from positivity, not from decimals**
9. E1 distinguishes proof from evidence

---

## Note for the Debrief

The lab has one argument and it is worth stating plainly:

> Two weeks ago you computed an integral to ten decimal places and could not have told me whether it
> was rational. Today you computed one **exactly** and it proved that a number you were taught in
> school is not $\pi$.
>
> **The difference is not precision.** Fifteen digits of $0.0012644\ldots$ is more precision than the
> proof needs. The difference is that "the integrand is positive, so the integral is positive" is a
> **proof**, and a decimal is **evidence**.

Then set up Week 3:

> Every bound in Part C came from the comparison property — squeezing an integral you cannot evaluate
> between two you can. **Next week that becomes the main technique**, when we ask whether an integral
> over an infinite interval is finite at all. And in Week 7 the same idea, applied to sums instead of
> integrals, becomes the Comparison Test.

---

*MATH 142 · Week 2 · Lab 02 Solutions · Instructor Only*

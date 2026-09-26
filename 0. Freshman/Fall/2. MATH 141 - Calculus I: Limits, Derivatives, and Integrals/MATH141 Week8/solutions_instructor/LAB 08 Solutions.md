# MATH 141 · Week 8
## LAB 08 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed in Python, not estimated.** Random-rule values will differ
> from run to run; grade the trend.

*(Revised 2026-09-26 to match the 6-question version of the lab.)*

---

## Part 1 — Watching Riemann Sums Converge

**Q1 (15).** The rectangles **overestimate**. $f$ is increasing on $[0,1]$, so on each subinterval the right
endpoint gives the largest value of $f$. Each rectangle is at least as tall as the curve across its whole
width. $R_4 = 0.46875 > \tfrac13$.

**Q2 (15).**

| n | Rₙ | error |
|---|---|---|
| 4 | 0.46875 | 0.1354167 |
| 10 | 0.385 | 0.0516667 |
| 100 | 0.33835 | 0.0050167 |
| 1000 | 0.3338335 | 0.0005002 |

Multiplying $n$ by 10 divides the error by about **10**: the error is proportional to $1/n$. That is like
the **forward** difference of Lab 03, whose error was proportional to $h$ ($h$ plays the part of $1/n$).

---

## Part 2 — Sample-Point Independence

**Q3 (15).** `x = left + dx` and `x = left + dx / 2`. `riemann(f, 0, 1, 1000, "right")` gives $0.3338335$ ✓.

**Q4 (15).** One run (random values vary):

| n | left | right | mid | random | random |
|---|---|---|---|---|---|
| 10 | 0.285 | 0.385 | 0.3325 | 0.3468 | 0.3336 |
| 100 | 0.32835 | 0.33835 | 0.333325 | 0.33313 | 0.33353 |
| 10 000 | 0.33328333 | 0.33338333 | 0.33333333 | 0.33333278 | 0.33333288 |

The midpoint rule is by far the most accurate fixed rule. At $n = 10$ the rules differ in the first
decimal place, a spread of about $0.1$. At $n = 10\,000$ they agree to about 4 decimal places.

**Q5 (15).** **Yes**, the random rule converges: the spread between runs shrinks as $n$ grows, and every rule
closes in on $\tfrac13$. The definition says $\int_a^b f$ is *the* limit for **any** choice of $x_i^*$. That
only makes sense if every choice gives the same limit. If left sums and right sums had different limits,
"the integral" would depend on an arbitrary choice and would not be well defined. For continuous $f$
they agree, and this table shows it.

---

## Part 3 — A Numerical Integral

**Q6 (25).**

| n | midpoint | error |
|---|---|---|
| 10 | 1.7650940179 | 9.31 × 10⁻⁴ |
| 100 | 1.7641725453 | 9.76 × 10⁻⁶ |
| 1000 | 1.7641628792 | 9.77 × 10⁻⁸ |

Each factor of 10 in $n$ divides the error by about **100**: the midpoint error is proportional to $1/n^2$,
like the central difference. Since $e^{-x^2}$ has no elementary antiderivative, this integral **belongs to
numerical methods**. Exact methods (the FTC, next week) own the integrals whose antiderivatives we can
write down. They also explain *why* numerical methods converge and how fast.

---

## Marking Scheme

- **Method (≈60%).** A reason for every observation. "The rules agree" is an observation; "they agree
  because the integral is defined as a limit independent of sample points" is the answer.
- **Execution (≈40%).** A working `riemann`, correct tables, and conclusions that follow from them.

---

*MATH 141 · Week 8 · Lab Solutions · Instructor Copy · © CSE Department*

# MATH 141 · Lab 02 Solutions (Instructor)
## Continuity, Discontinuity, and Bisection

All figures verified by computation. *(Revised 2026-09-26 to match the 7-question version of the lab.)*

---

## Part 1: Seeing the Types (5 pts)

**Q1 (2).**
- **1A — removable.** The graph is the line $y = x + 1$ with a hole at $(1, 2)$. The limit is $2$ but
  $f(1)$ is undefined, so **part (i)** fails.
- **1B — infinite.** The graph shoots to $+\infty$ from the right and $-\infty$ from the left. No finite
  limit, so **part (ii)** fails.
- **1C — jump.** One-sided limits $0$ and $1$ differ, so **part (ii)** fails.

**Q2 (3).**

| $x$ | $\sin(1/x)$ |
|---|---|
| $0.6366197724$ | $+1$ |
| $0.2122065908$ | $-1$ |
| $0.1273239545$ | $+1$ |
| $0.0909456818$ | $-1$ |
| $0.0707355303$ | $+1$ |
| $0.0578745248$ | $-1$ |

$x$ shrinks toward $0$ while the values **alternate exactly $\pm1$**. No one-sided limit exists, so part
(ii) fails, but for a different reason than 1B or 1C: the values neither settle nor diverge. **Essential
(oscillatory).**

*Marking: 1 for the table, 1 for the alternation, 1 for the classification.*

---

## Part 2: Repairing a Discontinuity (5 pts)

**Q3 (2).** Values approach $12$ from both sides: $11.41, 11.9401, 11.994001$ from the left and
$12.006001, 12.0601, 12.61$ from the right.

**Q4 (3).** $\dfrac{x^3-8}{x-2}=\dfrac{(x-2)(x^2+2x+4)}{x-2}=x^2+2x+4$, which at $x=2$ gives $\mathbf{12}$ ✓

$$\tilde f(x)=\begin{cases}\dfrac{x^3-8}{x-2},& x\ne2\\[4pt] 12,& x=2\end{cases}$$

**The marking point.** A limit as $x\to2$ only uses $x$ with $0<\lvert x-2\rvert$: the definition
**explicitly excludes** $x=2$. So dividing by $x-2$ is dividing by a nonzero number, and is valid.

*Students who say "we cancel because $x\ne2$" without connecting it to the $0<\lvert x-a\rvert$ in the
definition get 2 of 3.*

---

## Part 3: Bisection in Code (10 pts)

**Q5 (4).** The condition is `fa * fm < 0` (or `<= 0`). If $f(a)$ and $f(m)$ have opposite signs, $f$ is
continuous on $[a, m]$ and changes sign there, so by the IVT a root lies in $[a, m]$.

| Step | a | b | m | f(m) |
|---|---|---|---|---|
| 1 | 2.0 | 3.0 | 2.5 | 5.625 |
| 2 | 2.0 | 2.5 | 2.25 | 1.890625 |
| 3 | 2.0 | 2.25 | 2.125 | 0.345703125 |
| 4 | 2.0 | 2.125 | 2.0625 | −0.351318359375 |
| 5 | 2.0625 | 2.125 | 2.09375 | −0.008941650390625 |
| 6 | 2.09375 | 2.125 | 2.109375 | 0.166835784912 |
| 7 | 2.09375 | 2.109375 | 2.1015625 | 0.078562259674 |
| 8 | 2.09375 | 2.1015625 | 2.09765625 | 0.034714281559 |

*Marking: 2 for a correct condition with the IVT reason, 2 for the output.*

**Q6 (3).** **20 steps.** The root is $2.094552$ to six places; the true root is $2.0945514815\ldots$, so
accept $2.094551$ or $2.094552$ depending on whether the student printed `m` or `(a + b) / 2`.

**Q7 (3).**

| $\varepsilon$ | steps | $\lceil\log_2(1/\varepsilon)\rceil$ |
|---|---|---|
| $10^{-4}$ | 14 | 14 |
| $10^{-6}$ | 20 | 20 |
| $10^{-10}$ | 34 | 34 |

They match exactly. *A loop that tests `>=` instead of `>` can be one step off; accept it with a note.*

---

## Common Submission Problems

| Symptom | Cause | Action |
|---|---|---|
| Q2 sampled at arbitrary $x$ | Missed the instruction | −1; the alternation is only visible at the given points |
| Q4 says only "$x\ne2$" | No link to the definition | −1 |
| Q5 condition `fm < 0` alone | Ignores the sign of $f(a)$ | −1; it happens to work here only because $f(a) < 0$ throughout |
| Q7 off by one | `>=` vs `>` in the loop | No deduction if noted |

---

*MATH 141 · Week 2 · Lab 02 Solutions · Instructor copy — do not distribute*

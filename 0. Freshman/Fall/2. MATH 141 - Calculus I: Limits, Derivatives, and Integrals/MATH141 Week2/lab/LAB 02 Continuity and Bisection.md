# MATH 141 · Lab 02
## Continuity, Discontinuity, and Bisection

**Duration:** 2 hours · **20 points**
**Lab session:** Friday of Week 2

---

## Part 1: Seeing the Four Types (6 pts)

For each function, tabulate values approaching the point from both sides, then classify the
discontinuity and state which part of the three-part definition fails.

| | Function | Point |
|---|---|---|
| 1A | $\dfrac{x^2-1}{x-1}$ | $x=1$ |
| 1B | $\dfrac1x$ | $x=0$ |
| 1C | $f(x)=x$ for $x<0$, $x+1$ for $x\ge0$ | $x=0$ |
| 1D | $\sin(1/x)$ | $x=0$ |

For 1D, evaluate at $x=\dfrac{1}{k\pi/2}$ for $k=1,3,5,7,9,11$ and record what you see. *(1.5 pts each)*

---

## Part 2: Repairing a Discontinuity (4 pts)

**2A.** For $f(x)=\dfrac{x^3-8}{x-2}$, tabulate values near $x=2$ and conjecture the limit. *(1 pt)*

**2B.** Factor and confirm your conjecture algebraically. *(1 pt)*

**2C.** Write the continuous extension explicitly. *(1 pt)*

**2D.** Explain why the cancellation $\dfrac{(x-2)q(x)}{x-2}=q(x)$ is legitimate inside a limit even
though it is invalid at $x=2$. *(1 pt)*

---

## Part 3: Bisection (7 pts)

**3A.** Implement bisection for $f(x)=x^3-x-2$ on $[1,2]$. Print the bracket, midpoint and
$f(\text{mid})$ at each step. Run 8 steps. *(3 pts)*

**3B.** Verify your step 1–4 output against the problem set's table. *(1 pt)*

**3C.** Run to convergence and report the root to 12 decimal places, together with $f$ at that root.
*(1 pt)*

**3D.** Modify the code to take a tolerance and report the number of steps used. Check it against
$n\ge\log_2\!\big((b-a)/\varepsilon\big)$ for $\varepsilon=10^{-4},10^{-6},10^{-10}$. *(2 pts)*

---

## Part 4: The IVT Over the Rationals (3 pts)

**4A.** Run your bisection on $f(x)=x^2-2$ over $[1,2]$, printing each midpoint as a **fraction**
(use Python's `fractions.Fraction`). *(1 pt)*

**4B.** Every midpoint is rational, and the brackets shrink toward $\sqrt2$. Explain in three
sentences what this demonstrates about the IVT over $\mathbb{Q}$ versus over $\mathbb{R}$. *(2 pts)*

---

## Deliverables

Your tables, code, output, and written answers to 1D, 2D and 4B.

## Grading

| Part | Points |
|---|---|
| 1 — four types classified with evidence | 6 |
| 2 — repair, with the cancellation justified | 4 |
| 3 — working bisection, verified, with step counts | 7 |
| 4 — the rationals experiment and its interpretation | 3 |
| **Total** | **20** |

---

*MATH 141 · Week 2 · Lab 02 · © CSE Department*

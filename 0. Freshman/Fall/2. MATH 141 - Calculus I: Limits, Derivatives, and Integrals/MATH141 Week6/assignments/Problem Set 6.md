# MATH 141 · Calculus I
## Problem Set 6
### Topic: Extrema, Rolle's Theorem, the Mean Value Theorem, L'Hôpital's Rule
**Released:** Wednesday 4 November 2026, 12:00 (after Lecture 03) · Week 6
**Due:** Wednesday 11 November 2026, 11:00 (start of class) · Week 7 — late penalty after 11:00
**Total:** 100 points

**What this uses:** Week 6 only — extrema, critical numbers and the Closed Interval Method (Lecture 01),
Rolle's Theorem, the MVT and its corollaries (Lecture 02), L'Hôpital's Rule (Lecture 03) — plus the
differentiation rules of Weeks 4–5.

**Not needed, and not allowed:** concavity, inflection points, the Second Derivative Test and curve
sketching. They are Week 7.

> *Revised 2026-09-21.* The earlier version (125 + 4 bonus points) had Parts C (shape of a graph),
> D (Second Derivative Test) and E (curve sketching), all taught in Week 7, and no L'Hôpital questions
> even though Lecture 03 covers them. Those parts and the bonus were removed and a L'Hôpital part added.

---

## Part A — Absolute Extrema (24 pts)

**A1.** *(8 pts, 2 each)* Find all critical numbers:

- (a) $f(x) = x^3 - 6x^2 + 9x + 2$
- (b) $g(x) = \dfrac{x-1}{x^2+3}$
- (c) $h(x) = x^{1/3}(x+4)$
- (d) $k(x) = 2\cos x + x$ on $[0, 2\pi]$

**A2.** *(12 pts, 4 each)* Use the Closed Interval Method to find the absolute maximum and minimum values:

- (a) $f(x) = x^3 - 3x + 1$ on $[-2, 3]$
- (b) $f(x) = \dfrac{x}{x^2+4}$ on $[0, 4]$
- (c) $f(x) = x - 2\sin x$ on $[0, 2\pi]$

**A3.** *(4 pts)* A continuous function on $[0,5]$ has $f(0)=4$, $f(5)=4$, and critical numbers only at $x=2$ and $x=4$, where $f(2)=9$ and $f(4)=1$. Determine the absolute max and min values on $[0,5]$, and state which theorem guarantees these values are actually attained.

---

## Part B — Rolle's Theorem and MVT (32 pts)

**B1.** *(6 pts, 2 each)* For each function, verify whether Rolle's Theorem applies on the given interval. If it applies, find all values of $c$. If not, explain which hypothesis fails.

- (a) $f(x) = x^2 - 2x$ on $[0,2]$
- (b) $f(x) = 1 - x^{2/3}$ on $[-1,1]$
- (c) $f(x) = \tan x$ on $[0, \pi]$

**B2.** *(6 pts, 3 each)* For each function, verify the MVT applies on the given interval and find all values of $c$.

- (a) $f(x) = x^3 + x - 1$ on $[0,2]$
- (b) $f(x) = \sqrt{x+1}$ on $[0,3]$

**B3.** *(6 pts)* Use Rolle's Theorem to show that $f(x) = x^5 + 2x - 3$ has exactly one real root.

**B4.** *(6 pts)* Two towns A and B are connected by a mountain road 45 km long. A cyclist covers the distance in exactly 1.5 hours. Prove, using the MVT, that at some instant the cyclist's speed was exactly 30 km/h. State the theorem's hypotheses and verify they apply to this physical scenario.

**B5.** *(8 pts)* Use the MVT to prove that for all $x, y \in \mathbb{R}$ with $x < y$:
$$|\sin y - \sin x| \leq |y - x|$$

*(Hint: apply MVT to $f(t) = \sin t$ on $[x,y]$, and use $|\cos c| \leq 1$.)*

---

## Part C — L'Hôpital's Rule (26 pts)

**C1.** *(20 pts, 4 each)* Evaluate each limit. Name the indeterminate form before applying L'Hôpital's Rule,
and convert to $0/0$ or $\infty/\infty$ first where needed.

- (a) $\displaystyle\lim_{x\to0}\frac{e^x-1-x}{x^2}$
- (b) $\displaystyle\lim_{x\to\infty}\frac{\ln x}{\sqrt{x}}$
- (c) $\displaystyle\lim_{x\to0^+}x\ln x$
- (d) $\displaystyle\lim_{x\to0}\left(\frac{1}{x}-\frac{1}{\sin x}\right)$
- (e) $\displaystyle\lim_{x\to\infty}\left(1+\frac{3}{x}\right)^{x}$

**C2.** *(6 pts)* $\displaystyle\lim_{x\to\infty}\frac{x+\sin x}{x}$ has the form $\infty/\infty$. Show that applying
L'Hôpital's Rule once gives a limit that does not exist, explain why that does **not** mean the original
limit fails to exist, and find the original limit another way.

---

## Part D — Conceptual and Proof (18 pts, 6 each)

**D1.** A student says: "If $f'(c) = 0$, then $f$ has a local extremum at $c$." Give a specific counterexample and explain, using the definitions from Monday's lecture, exactly why the counterexample fails to be a local extremum.

**D2.** Prove: if $f$ is differentiable on $\mathbb{R}$, $f'(x) \geq 0$ for all $x$, and $f'(x) = 0$ at only finitely many points, then $f$ is strictly increasing on $\mathbb{R}$ (not just non-decreasing).

*(Hint: use the MVT on any interval $[a,b]$ and account for the finitely many zero points.)*

**D3.** Explain the logical relationship between Rolle's Theorem and the Mean Value Theorem. Is Rolle's Theorem a special case of the MVT, or is the MVT proved using Rolle's Theorem, or both? Justify with reference to the proofs given in lecture.

---

## Grading Summary

| Part | Points | Focus |
|------|--------|-------|
| A | 24 | Absolute extrema |
| B | 32 | Rolle's Theorem, MVT |
| C | 26 | L'Hôpital's Rule |
| D | 18 | Conceptual/proof |
| **Total** | **100** | |

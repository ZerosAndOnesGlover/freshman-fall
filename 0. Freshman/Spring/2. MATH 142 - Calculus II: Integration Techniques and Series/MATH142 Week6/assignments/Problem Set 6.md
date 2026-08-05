# MATH 142 · Calculus II
## Problem Set 6
### Topic: Sequences — Convergence, Divergence, Recursion
**Released:** Wednesday, Week 6 | **Due:** Wednesday, Week 7 (start of class)

---

> **Name your method.** "Divide by the dominant power", "pass to the function and apply L'Hôpital",
> "squeeze", "growth hierarchy" — the method is worth marks, and from this week onward it is worth
> more than the answer.
>
> **For every recursive sequence: prove convergence BEFORE solving for the limit.** A fixed point
> equation solved without a convergence argument earns no marks, however tidy the number.
>
> **"Diverges" includes oscillation.** Check whether a sequence settles, not merely whether it is bounded.

---

## Part A — Basic Limits (5 pts each)

**A1.** $\displaystyle\lim_{n\to\infty}\frac{3n^2-2n}{n^2+5}$

**A2.** $\displaystyle\lim_{n\to\infty}\frac{\ln n}{n^{1/3}}$

**A3.** $\displaystyle\lim_{n\to\infty}\left(1+\frac5n\right)^{n}$

**A4.** $\displaystyle\lim_{n\to\infty}\frac{(-1)^n}{n^2+1}$

---

## Part B — Techniques (6 pts each)

**B1.** $\displaystyle\lim_{n\to\infty}\left(n^2\right)^{1/n}$

**B2.** $\displaystyle\lim_{n\to\infty}\left(\sqrt{n^2+3n}-n\right)$

**B3.** $\displaystyle\lim_{n\to\infty}\frac{3^n}{n!}$

*Cite the growth hierarchy, and give the one-line reason it holds (Lecture 2 §4).*

**B4.** $\displaystyle\lim_{n\to\infty}n\sin\frac1n$

**B5.** $\displaystyle\lim_{n\to\infty}\frac{n!\,e^n}{n^n\sqrt n}$

*Use Stirling's approximation. Your answer should be a familiar constant — say which, and where it comes from.*

---

## Part C — Monotone Convergence and Recursion (6 pts each)

**C1.** Let $a_1=\sqrt6$ and $a_{n+1}=\sqrt{6+a_n}$.

- (a) Show by induction that $a_n<3$ for all $n$.
- (b) Show the sequence is increasing.
- (c) Conclude that it converges, and find the limit.

**C2.** Let $a_1=2$ and $a_{n+1}=\dfrac12\left(a_n+\dfrac{5}{a_n}\right)$.

- (a) Find the fixed points of $g(x)=\tfrac12\left(x+\tfrac5x\right)$.
- (b) Compute $g'(x)$ and evaluate it at the positive fixed point. What does the value predict about the speed of convergence?
- (c) Compute $a_2,a_3,a_4$ to as many digits as you can and confirm your prediction.

**C3.** Let $a_1=1$ and $a_{n+1} = 1+\dfrac{1}{1+a_n}$. Find the limit, having first argued that it exists.

*The answer is a number you have seen many times this term.*

**C4.** Show that $a_n = \dfrac{n!}{n^n}$ is **decreasing** and **bounded below**, and hence converges.

*Then state its limit, citing the growth hierarchy.*

**C5.** *(The trap.)* Let $a_1=2$ and $a_{n+1}=3a_n-2$.

- (a) Compute $a_1,\ldots,a_5$. What is the sequence doing?
- (b) Solve the fixed point equation $L=3L-2$. What does it give?
- (c) Explain precisely why (b) does not contradict (a), and identify which hypothesis is missing.
- (d) Compute $g'(L)$ and explain what it tells you about that fixed point.

---

## Part D — Concept (10 pts each)

**D1.** *(Completeness.)*

- (a) State the Monotone Convergence Theorem.
- (b) The sequence $1,\ 1.4,\ 1.41,\ 1.414,\ 1.4142,\ldots$ (successive decimal truncations of $\sqrt2$) is increasing and bounded above by 2. Every term is **rational**. Explain what goes wrong if we try to apply the theorem within $\mathbb{Q}$ instead of $\mathbb{R}$.
- (c) Hence explain in what sense the theorem is a statement about the real numbers rather than about sequences.
- (d) Week 3's comparison test for improper integrals was justified by an argument of exactly this shape. Identify the increasing bounded quantity in that argument.

**D2.** *(One-way streets.)*

- (a) State the theorem connecting $\lim_{x\to\infty}f(x)$ to $\lim_{n\to\infty}f(n)$, being careful about the direction of the implication.
- (b) Give the standard counterexample showing the converse fails, and explain in one sentence why the sequence "misses" the function's behaviour.
- (c) A student writes: *"$\lim_{n\to\infty}\sin(\pi n)$ does not exist, because $\lim_{x\to\infty}\sin(\pi x)$ does not exist."* Identify the error and give the correct value.
- (d) Explain why this matters practically: what may you do with L'Hôpital's rule on a sequence limit, and what may you not conclude when it fails?

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Standard limits |
| B (5 × 6) | 30 | Logs, conjugates, growth hierarchy, Stirling |
| C (5 × 6) | 30 | Monotone convergence; recursion; the fixed point trap |
| D (2 × 10) | 20 | Completeness; the one-way implication |
| **Total** | **100** | |

---

## Before You Submit

1. **Every recursive problem has a convergence argument before its limit.**
2. **Every limit names its method.**
3. **Check A4 and C5 for the traps** — one is a squeeze, one is a divergent sequence with a tidy-looking fixed point.
4. **B5 should come out to a constant you recognise.** If it does not, check your Stirling.

---

*MATH 142 · Week 6 · Problem Set 6*

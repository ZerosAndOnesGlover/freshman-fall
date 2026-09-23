# MATH 142 · Calculus II
## Week 3 · Overview
### Improper Integrals; Comparison Tests

---

**Topic:** integrals where the region is unbounded — and how to tell whether they mean anything
**Reading:** Stewart §7.8 | Apostol Ch. 10 §10.7–10.9
**Assessment this week:** PS 3, Lab 3, **Quiz 03** *(Mon 8 Feb, 11:00 — covers Week 2)*

---

## The Question Changes

For three weeks the question has been **"what is this integral?"** — a computational question, answered by technique.

This week the question becomes **"does this integral exist?"** — and it is a different kind of question, because the answer can be *no*.

$$\int_1^\infty\frac{dx}{x^2} = 1 \qquad\qquad \int_1^\infty\frac{dx}{x} = \infty$$

Both regions are infinitely long. Both integrands shrink to zero. **One has finite area and one does not**, and no amount of looking at the pictures will tell you which is which — the graphs of $1/x$ and $1/x^2$ are nearly indistinguishable to the eye for large $x$.

This is where Week 0's insistence on the *definition* pays off. If you think $\int_a^b f$ means "$F(b)-F(a)$", then $\int_1^\infty$ is meaningless — you cannot evaluate $F$ at $\infty$. **The integral was defined as a limit, and the way to handle an infinite region is to take another limit.**

---

## The Two Kinds

| Kind | What is unbounded | Example |
|---|---|---|
| **Type I** | the **interval** | $\displaystyle\int_1^\infty\frac{dx}{x^2}$ |
| **Type II** | the **integrand** | $\displaystyle\int_0^1\frac{dx}{\sqrt x}$ |

Both are handled the same way: **replace the offending endpoint with a variable, integrate normally, then take a limit.**

$$\int_1^\infty f(x)\,dx := \lim_{T\to\infty}\int_1^T f(x)\,dx$$

If the limit exists and is finite, the integral **converges**. Otherwise it **diverges**.

**Type II is the more dangerous**, because it can hide. $\int_0^3\frac{dx}{(x-1)^{2/3}}$ looks like an ordinary definite integral until you notice the integrand blows up at $x=1$, *inside* the interval. Applying the Fundamental Theorem across a singularity gives a confident, wrong answer.

---

## The Three Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Monday | Improper Integrals of Type I | Infinite interval; the $p$-test |
| **Lecture 2** | Tuesday | Improper Integrals of Type II | Unbounded integrand; singularities that hide |
| **Lecture 3** | Friday | Comparison Tests | Deciding convergence **without** evaluating |

---

## The $p$-Test, Which Is the Whole Week

$$\int_1^\infty\frac{dx}{x^p} \ \text{converges} \iff p>1 \qquad\qquad \int_0^1\frac{dx}{x^p}\ \text{converges} \iff p<1$$

**Note they point opposite ways**, and that is not a coincidence — near infinity you need the function to shrink *fast*, near a singularity you need it to blow up *slowly*. The exponent $p=1$ is the knife edge in both cases, and in both cases the boundary itself **diverges**.

Everything else this week is comparison against these.

---

## Why Lecture 3 Is the Important One

Most improper integrals cannot be evaluated. $\int_1^\infty\frac{dx}{\sqrt{x^3+1}}$ has no elementary antiderivative — Week 0's opening fact, still true.

**But you can still answer the convergence question**, by comparing with something you *can* evaluate:

$$\frac{1}{\sqrt{x^3+1}} < \frac{1}{\sqrt{x^3}} = \frac{1}{x^{3/2}} \quad\text{and}\quad \int_1^\infty\frac{dx}{x^{3/2}}\ \text{converges} \implies \text{so does ours}$$

> **This is the first time in the course you will answer a question about an integral without
> computing it.** It is a genuinely different mode of reasoning, and it is the one that dominates the
> second half of the course — every convergence test in Weeks 7 and 8 is this argument, applied to
> sums instead of integrals.

---

## What Lab 3 Will Show You

Lab 3 computes $\int_1^T\frac{dx}{x^p}$ for a range of $p$ and watches $T$ grow. Here is a preview of what you will find at $T = 10^6$ — a million, far beyond any realistic computation:

| $p$ | value at $T=10^6$ | true limit |
|---|---|---|
| $0.99$ | $14.8$ | **$\infty$** |
| $1.00$ | $13.8$ | **$\infty$** |
| $1.01$ | $12.9$ | **$100$** |

**The convergent one is the smallest of the three.** Nothing in these numbers reveals that the third row settles at 100 while the first two grow forever — and at $T = 10^{100}$, a googol, the third has only reached 90.

**Numerical evidence cannot decide convergence.** This week's exact methods can, in one line each. That is the strongest form of an argument this course has been building since Lab 0.

---

## This Week's Work

1. **Quiz 03** — Monday, 15 minutes, **covers Week 2** (trigonometric substitution, partial fractions)
2. **PS 3** — released Fri 12 Feb 12:00, due Fri 19 Feb 17:00
3. **Lab 3** — the $p$-test measured, and the limits of numerical evidence

---

## Looking Ahead: Midterm 1

**Midterm 1 is Wednesday 3 March, 18:00–19:15 (Week 6)** and covers Weeks 0–4. After this week only one topic remains on it (Week 4's applications), so this is the point to start consolidating rather than to fall behind.

---

*Next: Monday — Improper Integrals of the First Kind*

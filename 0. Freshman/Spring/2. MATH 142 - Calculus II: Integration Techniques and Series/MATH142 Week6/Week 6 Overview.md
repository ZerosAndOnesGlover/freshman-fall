# MATH 142 · Calculus II
## Week 6 · Overview
### Sequences: Convergence and Divergence

---

**Topic:** the limit of a list — and the foundation of everything remaining in the course
**Reading:** Stewart §11.1 | Apostol Ch. 10 §10.1–10.6
**Assessment this week:** PS 6, Lab 6, **Quiz 06** *(Monday — covers Week 5)*

---

## The Course Changes Here

**Weeks 0–5 are over.** You have every integration technique this course will teach, and you have applied them to areas, volumes, lengths and surfaces. That half of the course was about **evaluation**: getting a number.

**From this week to the end, the question is almost always "does this converge?"**

The syllabus warned you about this in Week 0:

> *In Week 6 it inverts again. **Series are conceptually the hardest material in the first-year
> sequence** — the computations are easy and the reasoning is subtle, which is the exact opposite of
> Weeks 1–5.*

**Expect the arithmetic to get easier and the thinking to get much harder.** Students who found Weeks 1–2 a grind often find this material a relief; students who coasted on computation often struggle for the first time. Neither reaction means anything about how the course will end.

---

## What a Sequence Is

A **sequence** is an infinite ordered list of numbers:

$$a_1,\ a_2,\ a_3,\ \ldots \qquad\text{written}\qquad \{a_n\}_{n=1}^\infty$$

Formally it is a **function whose domain is the positive integers**. That is the only difference from the functions you have been studying — the input is discrete.

**The only question we ask of a sequence is what happens at the far end.**

$$\lim_{n\to\infty}a_n = L$$

means the terms get and stay arbitrarily close to $L$. If such an $L$ exists the sequence **converges**; otherwise it **diverges**.

---

## Why This Is Not a Detour

**Everything in Weeks 7–10 is a statement about a sequence.** An infinite series

$$\sum_{n=1}^\infty a_n$$

is *defined* as the limit of its sequence of **partial sums** $s_N = a_1+\cdots+a_N$. So "does this series converge?" is literally "does this sequence converge?" — and every test you meet in Weeks 7–8 is a tool for answering it without computing the limit.

**You have done this before.** Week 3 asked whether $\int_1^\infty f$ was finite, and answered it by comparison rather than evaluation. This week asks the same kind of question about lists instead of integrals, and Week 7 will make the connection explicit with the **Integral Test**.

---

## The Three Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Monday | Sequences and Their Limits | The definition, and the function connection |
| **Lecture 2** | Tuesday | Techniques and the Growth Hierarchy | How to actually compute these limits |
| **Lecture 3** | Wednesday | Monotone Convergence; Recursive Sequences | Convergence proved **without** knowing the limit |

---

## The Week's Most Important Theorem

> **Monotone Convergence Theorem.** *A sequence that is increasing and bounded above converges.*

Notice what it does **not** require: **it does not tell you the limit, and it does not ask you to find one.** It converts a question about an infinite limit into two finite checks — is it increasing, and is it bounded?

**This is the theorem that makes the rest of the course possible.** You have already used it twice without being told:

- **Week 3:** the comparison test worked because $\int_a^T f$ is increasing in $T$ and bounded above.
- **Week 7 onwards:** every test for a positive series is this theorem in disguise.

It is also where the real numbers enter. **The rationals do not satisfy it** — the sequence $1,\ 1.4,\ 1.41,\ 1.414,\ldots$ is increasing and bounded above by 2, and its limit $\sqrt2$ is not rational. **Monotone convergence is one form of the completeness axiom**, and it is the precise sense in which $\mathbb R$ has no holes.

---

## What Lab 6 Will Show You

Lab 6 studies **recursive** sequences $a_{n+1}=g(a_n)$, and measures how fast they converge.

The Babylonian method for $\sqrt2$ — known to the Babylonians around 1700 BC, and what your computer still does — is

$$a_{n+1} = \frac12\left(a_n+\frac{2}{a_n}\right), \qquad a_0=1$$

Starting from 1, the number of correct digits goes

$$1,\quad 2,\quad 5,\quad 11,\quad 24,\quad 48$$

**It doubles every step.** Six iterations give 48 correct decimal places. *(Measured.)*

Compare with the labs so far:

| Method | Cost for ~10 digits |
|---|---|
| Wallis product (Lab 1) | $8\times10^9$ factors |
| Simpson's rule (Lab 0) | 128 points |
| **Babylonian (Lab 6)** | **4 steps** |

**The lab's question is what makes the difference**, and the answer turns out to be a single derivative: whether $g'$ vanishes at the fixed point.

---

## What Will Be Hard

**Divergence is not always dramatic.** $(-1)^n$ diverges by oscillating between $-1$ and $1$ — bounded, never blowing up, and still divergent. **"Diverges" means "fails to converge", not "goes to infinity".**

**The function connection only runs one way.** If $f(x)\to L$ then $a_n=f(n)\to L$. **The converse is false:** $a_n=\sin(\pi n)$ is identically 0 and converges, while $\sin(\pi x)$ oscillates forever. **You may use L'Hôpital on the function, then transfer — never the other way.**

**Proving convergence without finding the limit** is a new move. Lecture 3 is entirely about it, and it is the mode of reasoning the whole second half needs.

---

## This Week's Work

1. **Quiz 06** — Monday, 15 minutes, **covers Week 5** (parametric curves, polar coordinates)
2. **PS 6** — released Wednesday, due Wednesday of Week 7
3. **Lab 6** — recursion, fixed points, and why some iterations are astronomically faster than others

---

*Next: Monday — Sequences and Their Limits*

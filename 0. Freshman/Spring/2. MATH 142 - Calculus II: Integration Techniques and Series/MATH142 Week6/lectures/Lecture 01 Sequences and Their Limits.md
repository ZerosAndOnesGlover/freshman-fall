# MATH 142 · Calculus II
## Week 6 · Lecture 1 (Monday)
### Sequences and Their Limits

**Date:** Monday 22 February 2027 · 11:00–11:50 · Week 6

---

**Reading:** Stewart §11.1 | Apostol Ch. 10 §10.1–10.3
**Quiz 06** — this Monday, **covers Week 5** (parametric curves, polar coordinates)

---

## 1. Definition

A **sequence** is a function whose domain is the positive integers:

$$a:\ \mathbb{Z}^+\to\mathbb{R},\qquad n\mapsto a_n$$

We write it as a list, $\{a_n\}$, or $a_1,a_2,a_3,\ldots$

**That is the only change from everything you have studied: the input is discrete.** There is no "$a_{2.5}$", so there is no continuity, no differentiability, and no integration. **The only meaningful question is the behaviour at the far end.**

### Three ways to specify one

| Method | Example |
|---|---|
| **Formula** | $a_n = \dfrac{n}{n+1}$ |
| **Recursion** | $a_1=1$, $a_{n+1} = \tfrac12\left(a_n+\tfrac{2}{a_n}\right)$ |
| **Description** | $a_n$ = the $n$-th prime |

**Recursively-defined sequences are the interesting case** — they are what algorithms produce, and Lecture 3 and Lab 6 are about them.

---

## 2. The Limit

> **Definition.** $\displaystyle\lim_{n\to\infty}a_n = L$ means: for every $\varepsilon>0$ there exists
> $N$ such that $|a_n - L| < \varepsilon$ **for all** $n>N$.

**In words: whatever tolerance you name, the sequence eventually gets inside it and stays there.**

This is the $\varepsilon$–$\delta$ definition from MATH 141, with $N$ in place of $\delta$ — and it is genuinely simpler, because there is only one direction to go.

- If such an $L$ exists, the sequence **converges** (to $L$, which is unique).
- Otherwise it **diverges**.

### The word "diverges" is broader than you expect

| Sequence | Behaviour | Verdict |
|---|---|---|
| $\frac1n$ | $\to0$ | converges |
| $n$ | $\to\infty$ | **diverges** |
| $(-1)^n$ | oscillates $-1,1,-1,\ldots$ | **diverges** |
| $\sin n$ | wanders in $[-1,1]$ forever | **diverges** |

> **"Diverges" means "fails to converge", not "blows up".** $(-1)^n$ is perfectly bounded and still
> divergent, because it never settles. This distinction will matter enormously in Week 8.

We write $\lim a_n=\infty$ as a *description* of one kind of divergence, not as a claim that the limit exists.

---

## 3. Using the Definition Once

**Claim.** $\displaystyle\lim_{n\to\infty}\frac{n}{n+1} = 1$.

**Proof.** Given $\varepsilon>0$, we need $\left|\frac{n}{n+1}-1\right|<\varepsilon$. Now

$$\left|\frac{n}{n+1}-1\right| = \left|\frac{n-(n+1)}{n+1}\right| = \frac{1}{n+1}$$

so it suffices that $\frac{1}{n+1}<\varepsilon$, i.e. $n > \frac1\varepsilon - 1$. **Take $N = \frac1\varepsilon$.** $\blacksquare$

*(Verified: the limit is 1.)*

**We will not do many of these.** The point of doing one is that the definition is what all the theorems below are proved from — but in practice you compute limits with the tools of Lecture 2.

---

## 4. The Function Connection — and Its One-Way Street

> **Theorem.** If $f$ is defined on $[1,\infty)$ with $a_n = f(n)$, and $\displaystyle\lim_{x\to\infty}f(x)=L$,
> then $\displaystyle\lim_{n\to\infty}a_n = L$.

**This is what makes sequence limits computable.** It licenses everything from MATH 141 — L'Hôpital's rule, algebra of limits, the standard limits — provided you apply it to the *function* and then transfer to the sequence.

### Example 1

$$\lim_{n\to\infty}\frac{\ln n}{n}$$

The sequence version has no derivatives available. **Pass to the function** $f(x) = \frac{\ln x}{x}$, an $\frac\infty\infty$ form, and apply L'Hôpital:

$$\lim_{x\to\infty}\frac{\ln x}{x} = \lim_{x\to\infty}\frac{1/x}{1} = 0 \implies \lim_{n\to\infty}\frac{\ln n}{n} = 0$$

*(Verified.)*

### ⚠ The converse is false

**A sequence can converge while the function does not.**

$$a_n = \sin(\pi n)$$

Every term is **exactly 0**, because $\pi n$ is an integer multiple of $\pi$. So $a_n\to0$, trivially.

But $f(x) = \sin(\pi x)$ **oscillates forever** and has no limit at all.

**The sequence only samples the function at integers, and can miss everything interesting in between.**

> **Practical rule: the implication runs one way only.**
> **Function converges $\implies$ sequence converges.** Use this constantly.
> **Sequence converges $\;\not\!\!\!\implies$ function converges.** Never use this.
>
> In particular, **if L'Hôpital fails or the function oscillates, that tells you nothing about the
> sequence** — you must argue directly.

---

## 5. The Geometric Sequence

The single most important sequence in the rest of the course:

$$a_n = r^n$$

$$\boxed{\lim_{n\to\infty}r^n = \begin{cases} 0 & |r|<1\\ 1 & r=1\\ \text{diverges} & r\le-1 \text{ or } r>1\end{cases}}$$

*(Verified: $r=\pm0.5$ give 0; $r=1$ gives 1; $r=1.5$ diverges to $\infty$; $r=-1$ oscillates — a CAS returns `nan`, correctly reporting that no limit exists.)*

**So $r^n$ converges exactly when $-1 < r \le 1$.** Note the asymmetry: $r=1$ converges, $r=-1$ does not.

**Memorise this.** Week 7's geometric series, Week 9's radius of convergence, and every ratio test in between reduce to it.

---

## 6. The Squeeze Theorem

> **Theorem.** If $b_n \le a_n\le c_n$ for all large $n$, and $b_n\to L$ and $c_n\to L$, then $a_n\to L$.

**The workhorse for anything with a bounded oscillating factor**, where L'Hôpital cannot help.

### Example 2

$$\lim_{n\to\infty}\frac{\sin n}{n}$$

$\sin n$ has no limit. But $-1\le\sin n\le1$, so

$$-\frac1n \;\le\; \frac{\sin n}{n} \;\le\; \frac1n$$

Both bounds $\to0$, so $\boxed{\frac{\sin n}{n}\to0}$.

**The oscillation is irrelevant** once it is trapped between two things going to zero. **This is Week 3's comparison test, for sequences** — bound the thing you cannot evaluate by things you can.

### Example 3 — a useful corollary

$$\text{If } |a_n|\to0 \text{ then } a_n\to0$$

since $-|a_n|\le a_n\le|a_n|$. **This is how you handle alternating signs**, and it is the seed of absolute convergence in Week 8.

For instance $\frac{(-1)^n}{n}\to0$, because $\left|\frac{(-1)^n}{n}\right| = \frac1n\to0$.

> **Careful:** this works for limit **0** only. $(-1)^n$ has $|(-1)^n| = 1\to1$, but $(-1)^n$ itself
> diverges. **The corollary is one-directional and specific to zero.**

---

## 7. Bounded and Monotone — a Preview

Two properties that will matter on Wednesday:

**Bounded:** there is $M$ with $|a_n|\le M$ for all $n$.

**Monotone:** either $a_{n+1}\ge a_n$ for all $n$ (**increasing**) or $a_{n+1}\le a_n$ for all $n$ (**decreasing**).

| | |
|---|---|
| Convergent $\implies$ bounded | **True.** A sequence that settles cannot run away. |
| Bounded $\implies$ convergent | **False.** $(-1)^n$ is bounded and divergent. |
| **Bounded + monotone $\implies$ convergent** | **True** — Wednesday's theorem. |

**The third line is the one that does the work**, and it will let us prove convergence for sequences whose limits we cannot compute.

---

## 8. What To Take From This Lecture

1. **A sequence is a function on the positive integers.** Only the behaviour at infinity matters.
2. **$a_n\to L$** means: every tolerance is eventually met and never left.
3. **"Diverges" means "fails to converge"** — oscillation counts.
4. **Function limit $\implies$ sequence limit, never the reverse.** $\sin(\pi n)$ is the counterexample.
5. **$r^n$ converges exactly for $-1<r\le1$.** This is the most-used fact in the rest of the course.
6. **Squeeze handles bounded oscillating factors**; and $|a_n|\to0\implies a_n\to0$.

---

*Next: Tuesday — Techniques, and the Growth Hierarchy*

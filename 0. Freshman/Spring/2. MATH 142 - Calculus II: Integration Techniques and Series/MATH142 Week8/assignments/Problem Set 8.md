# MATH 142 · Calculus II
## Problem Set 8
### Topic: Alternating Series; Absolute Convergence; Ratio and Root Tests
**Released:** Wednesday, Week 8 | **Due:** Wednesday, Week 9 (start of class)

---

> **The Alternating Series Test has TWO hypotheses.** Check that $b_n$ is decreasing *and* that
> $b_n\to0$, every time. Verifying only the second is checking half a theorem.
>
> **For any series with mixed signs, test $\sum|a_n|$ first** and state whether convergence is
> **absolute** or **conditional**. The distinction is the point of the week.
>
> **"$L=1$" is not a conclusion.** If the Ratio or Root Test gives 1, say so and use another test.

---

## Part A — Alternating Series (5 pts each)

**A1.** $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{2n+1}$ — converge or diverge? Verify **both** hypotheses.

**A2.** $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n}\,n}{n^2+1}$

*Show that $b_n=\frac{n}{n^2+1}$ is decreasing. (A derivative argument is cleanest.)*

**A3.** For $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n^3}$:

- (a) How many terms guarantee an error below $10^{-3}$?
- (b) State the resulting bracket: between which two partial sums does the true sum lie?

**A4.** $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n}\,n}{2n+1}$

*The Alternating Series Test does not apply. Say why — and then give the correct verdict, naming the test that supplies it.*

---

## Part B — Absolute or Conditional? (6 pts each)

*For each: state whether the series converges **absolutely**, converges **conditionally**, or **diverges**. Show the test on $\sum|a_n|$ first.*

**B1.** $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^n}{n^{4/3}}$

**B2.** $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^n}{\ln(n+1)}$

**B3.** $\displaystyle\sum_{n=1}^{\infty}\frac{\cos n}{n^2}$

*The signs are irregular — there is no alternating structure. Which tool handles this?*

**B4.** $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^n\,n}{n^2+1}$

*Compare with your A2 answer, and say what A2 did **not** establish.*

**B5.** $\displaystyle\sum_{n=2}^{\infty}\frac{(-1)^n}{n\ln n}$

---

## Part C — Ratio and Root Tests (6 pts each)

**C1.** $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{3^n}$

**C2.** $\displaystyle\sum_{n=1}^{\infty}\frac{(n!)^2}{(2n)!}$

**C3.** $\displaystyle\sum_{n=1}^{\infty}\frac{(-3)^n\cdot 2^n}{n!}$ — state whether convergence is absolute.

**C4.** $\displaystyle\sum_{n=1}^{\infty}\left(\frac{n}{n+1}\right)^{n^2}$

*Use the Root Test. You will need a Week 6 limit.*

**C5.** $\displaystyle\sum_{n=1}^{\infty}\frac{n^2}{n^3+1}$

- (a) Apply the Ratio Test. What do you get?
- (b) Hence determine convergence by another method, naming it.

---

## Part D — Concept (10 pts each)

**D1.** *(Rearrangement.)*

- (a) Define absolute and conditional convergence.
- (b) Prove that absolute convergence implies convergence. *(Use the comparison $0\le a_n+|a_n|\le2|a_n|$.)*
- (c) For the alternating harmonic series, show that the positive terms alone and the negative terms alone **each** diverge. Explain why this makes the value $\ln 2$ depend on the ordering.
- (d) State the Riemann Rearrangement Theorem, and describe the greedy algorithm that achieves a given target $T$. Explain **why each stage terminates.**
- (e) Why does none of this threaten an absolutely convergent series?

**D2.** *(Hypotheses and silence.)*

- (a) $\sum\frac1n$ and $\sum\frac{1}{n^2}$ both have ratio limit $L=1$. Verify both limits, and state what this shows about the Ratio Test.
- (b) Explain why the Ratio Test gives $L=1$ for **every** $p$-series, and what that tells you about the kind of series it is useful for.
- (c) A student writes: *"The Ratio Test gives $L=1$, so the series diverges."* Identify the error precisely.
- (d) Consider $\displaystyle\sum_{n=1}^\infty\frac{(1+\frac1n)^{n^2}}{e^n}$. Show the Root Test gives $L=1$. Then settle the series by a cheaper test, and say which one.

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Alternating Series Test, both hypotheses; error bound |
| B (5 × 6) | 30 | Absolute vs conditional |
| C (5 × 6) | 30 | Ratio and Root, including an inconclusive case |
| D (2 × 10) | 20 | Rearrangement; the meaning of $L=1$ |
| **Total** | **100** | |

---

## Before You Submit

1. **Every alternating series has both hypotheses checked.**
2. **Every mixed-sign series is classified** as absolutely convergent, conditionally convergent, or divergent.
3. **No occurrence of "$L=1$, so it diverges."**
4. **Check A4 and C5** — in both, the first test you reach for is the wrong one.

---

*MATH 142 · Week 8 · Problem Set 8*

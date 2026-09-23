# MATH 142 · Calculus II
## Week 2 · Overview
### Trigonometric Substitution; Partial Fractions

---

**Topic:** the last two integration techniques, and the first *theorem* about which integrals are doable
**Reading:** Stewart §7.3–7.4 | Apostol Ch. 6 §6.13–6.15
**Assessment this week:** PS 2, Lab 2, **Quiz 02** *(Mon 1 Feb, 11:00 — covers Week 1)*

---

## Where This Sits

You have two general techniques: **substitution** (Week 0) and **parts** (Week 1). This week adds no third general technique. Instead it adds two *strategies* — ways of rewriting an integral so that one of the two techniques you already have becomes applicable.

| Week | Technique | Comes from |
|---|---|---|
| 0 | Substitution | the chain rule |
| 1 | Integration by parts | the product rule |
| 2 | **Trigonometric substitution** | substitution, with the substitution chosen backwards |
| 2 | **Partial fractions** | algebra, then the $\int\frac{g'}{g}$ pattern |

**After this week the toolkit is complete.** Every integral you meet for the rest of the course is either one of these, an improper integral (Week 3), or one that cannot be done at all.

---

## The Two Ideas

### Trigonometric substitution — running substitution backwards

Ordinary substitution *simplifies* by replacing a complicated inner function with $u$. Trigonometric substitution does the opposite: it **replaces the simple variable $x$ with a complicated trigonometric expression**, on purpose, because doing so kills a square root.

The three patterns, driven by the Pythagorean identities:

$$\sqrt{a^2-x^2}\ \to\ x = a\sin\theta \qquad \sqrt{a^2+x^2}\ \to\ x = a\tan\theta \qquad \sqrt{x^2-a^2}\ \to\ x = a\sec\theta$$

What comes out the other side is a **trigonometric integral** — exactly the family Lecture 3 of Week 1 taught you to handle. That is why last week's decision table mattered: this week is where it gets used.

### Partial fractions — and a genuine theorem

Every **rational function** — a ratio of polynomials — can be split into a sum of simple pieces, each of which integrates to a logarithm, an arctangent, or a power. This yields something the course has not offered before:

> **Theorem.** *Every rational function has an elementary antiderivative.*

Compare that with Week 0's opening fact, that $e^{-x^2}$ has none. **Here is an entire infinite class of functions where the answer is always yes, and there is an algorithm to find it.** Rational functions are the one place in integration where the situation is completely understood.

---

## The Three Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Monday | Trigonometric Substitution | Three patterns; and you must convert back |
| **Lecture 2** | Tuesday | Completing the Square; Rationalizing | Making an integral *fit* a pattern |
| **Lecture 3** | Friday | Partial Fractions | The algorithm, and the theorem it proves |

---

## What Will Be Hard

**Converting back to $x$.** After a trigonometric substitution you have an answer in $\theta$, and the original question was in $x$. Getting back requires a **reference triangle** and care with the sign — and on definite integrals you can avoid the whole issue by changing the limits instead. Students lose more marks here than on the substitution itself.

**Bookkeeping in partial fractions.** The method is mechanical, but a decomposition with a repeated factor and an irreducible quadratic has five or six unknown constants, and one arithmetic slip invalidates everything downstream. **The remedy is that you can always check**: recombine the fractions and confirm you get back what you started with. Lab 2 makes you do this by machine.

---

## This Week's Work

1. **Quiz 02** — Monday, 15 minutes, **covers Week 1** (parts, reduction formulas, trigonometric integrals)
2. **PS 2** — released Fri 5 Feb 12:00, due Fri 12 Feb 17:00
3. **Lab 2** — partial fractions, and a famous one-line proof that $\tfrac{22}{7} > \pi$

---

## A Preview of Lab 2

$$\int_0^1 \frac{x^4(1-x)^4}{1+x^2}\,dx \;=\; \frac{22}{7}-\pi$$

The integrand is a rational function, so by this week's theorem it has an elementary antiderivative — you find it by polynomial division and get the result exactly. And because the integrand is *strictly positive* on $(0,1)$, the integral is positive, which proves

$$\frac{22}{7} > \pi$$

**A schoolroom approximation, disproved as an equality by a Week 2 integral.** Bounding the same integral gives $\pi$ to three decimal places. This is what an exact technique buys you that a numerical one does not.

---

*Next: Monday — Trigonometric Substitution*

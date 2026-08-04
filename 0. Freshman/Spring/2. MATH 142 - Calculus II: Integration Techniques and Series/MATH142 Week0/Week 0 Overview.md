# MATH 142 · Calculus II
## Week 0 · Overview
### Review of Integration; Applications of Integration

---

**Topic:** the integral you already have, restated precisely enough to build on
**Reading:** Stewart §5.1–5.5, §6.1, §6.5 (review) | Apostol Ch. 1–2 (optional, for the definition)
**Assessment this week:** PS 0 (due **Friday of Week 0, 11:59 PM** — compressed), Lab 0, Diagnostic Quiz *(ungraded)*

---

## Why There Is a Week 0

You passed MATH 141. You can integrate. So why spend a week on review?

Because **Calculus II is not a continuation of Calculus I — it is a course about that course's limitations**, and you cannot study the limitations of a tool you only half-hold. Specifically:

- Week 3 asks what $\int_1^\infty \frac{dx}{x^2}$ means. That question is incoherent unless you know that $\int_a^b f$ was *defined* as a limit of Riemann sums, not as "the antiderivative evaluated at the ends".
- Weeks 1–2 are a catalogue of tricks for finding antiderivatives. Every one of them is the chain rule, the product rule, or an algebraic identity, run backwards. If those rules are shaky, the tricks are unlearnable — they will look like a list of 40 unrelated recipes instead of 3 ideas.
- Week 7 compares a series to an integral. That comparison only works if you can see an integral as an area.

This week re-establishes three things: **the definition**, **the technique you already have (substitution)**, and **the habit of asking what an integral is measuring**.

---

## The Three Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Monday | The Definite Integral and the Fundamental Theorem | The integral is a limit; the FTC is a theorem, not a definition |
| **Lecture 2** | Tuesday | Substitution and the Antiderivative Catalogue | The only technique you have, and its limits |
| **Lecture 3** | Wednesday | Area, Average Value, and Net Change | What an integral is *for* |

---

## The Fact This Course Is Built Around

Here is the fact that motivates the next thirteen weeks. Each of these functions is continuous, perfectly well-behaved, and has an antiderivative — by the Fundamental Theorem, $F(x)=\int_0^x f(t)\,dt$ always exists:

$$e^{-x^2} \qquad \frac{\sin x}{x} \qquad \sqrt{1+x^3}$$

**But none of their antiderivatives can be written in elementary form** — no finite combination of polynomials, roots, exponentials, logarithms, and trigonometric functions equals $\int e^{-x^2}\,dx$. This is not a gap in the textbook or a technique you have yet to learn. It is a theorem, proved by **Liouville in 1835**.

A computer algebra system confirms it by giving up in a specific way — asked for $\int e^{-x^2}dx$ it returns $\frac{\sqrt\pi}{2}\operatorname{erf}(x)$, where $\operatorname{erf}$ is *defined* as that integral. It has not solved the problem; it has named it.

So the course has two jobs:

1. **Weeks 0–5:** get very good at the integrals that *can* be done, and learn to recognise the ones that cannot.
2. **Weeks 6–12:** develop a second way to represent a function — the **infinite series** — under which every one of the three above becomes easy.

The first integral in Lab 0 this week is $\int_0^1 e^{-x^2}dx$, computed numerically. In Week 10 you will compute it again, to any precision you like, in about two lines.

---

## What You Must Already Be Able To Do

If any of these is shaky, fix it this week — not in Week 3.

- [ ] State the definition of $\int_a^b f(x)\,dx$ as a limit of Riemann sums
- [ ] State **both** parts of the Fundamental Theorem and say which one you are using
- [ ] Differentiate: product, quotient, chain rules; $e^x$, $\ln x$, all six trig, the inverse trig functions
- [ ] Integrate by substitution, **including changing the limits** on a definite integral
- [ ] Find the area between two curves, including deciding which is on top
- [ ] Recognise when a definite integral is zero by symmetry

The diagnostic quiz this week tests exactly this list. **It is ungraded.** Its only purpose is to tell you, in Week 0, what you would otherwise discover at Midterm 1.

---

## This Week's Work

1. **PS 0** — review problems, due **Friday 11:59 PM** (the compressed Week 0 deadline)
2. **Lab 0** — numerical integration, and measuring how wrong a method is
3. **Diagnostic Quiz** — ungraded, self-marked, answer key included

---

*Next: Monday — The Definite Integral and the Fundamental Theorem*

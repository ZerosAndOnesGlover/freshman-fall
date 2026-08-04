# MATH 142 · Calculus II
## Week 1 · Overview
### Integration by Parts; Trigonometric Integrals

---

**Topic:** the second integration technique, and the first family of integrals that needs a strategy
**Reading:** Stewart §7.1–7.2 | Apostol Ch. 5 §5.9
**Assessment this week:** PS 1, Lab 1, **Quiz 01** *(Monday — covers Week 0)*

---

## Where This Sits

Week 0 established that you have exactly **one** integration technique: substitution, which is the chain rule run backwards.

This week adds the second: **integration by parts**, which is the product rule run backwards. That is the entire supply of general techniques — everything in Week 2 is substitution or parts applied after an algebraic manoeuvre.

> **Two rules of differentiation, two techniques of integration.** The chain rule gives substitution; the product rule gives parts. The quotient rule gives nothing new, because it is the product rule in disguise.

**The asymmetry to notice.** Differentiation is an algorithm: given any elementary function, the rules determine the answer and a machine can follow them. Integration is a **search** — you must decide which technique to try, and the decision is not mechanical. That is why Weeks 1–2 are drill, and why the recognition question ("which kind of integral is this?") is worth more marks than any single execution.

---

## The Three Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Monday | Integration by Parts | The product rule backwards; choosing $u$ |
| **Lecture 2** | Tuesday | Repeated Parts, Reduction Formulas, Definite Parts | When once is not enough |
| **Lecture 3** | Wednesday | Trigonometric Integrals | A family with a decision procedure |

---

## Why Trigonometric Integrals Matter to You

Lecture 3 will look like the most arbitrary material in the course — a catalogue of cases for $\int\sin^m x\cos^n x\,dx$ sorted by whether the exponents are odd or even. Two reasons to take it seriously:

**1. Week 2 depends on it entirely.** Trigonometric substitution converts an algebraic integral into a trigonometric one. If you cannot do the trigonometric integral, the substitution has bought you nothing.

**2. It contains the single most important integral fact in signal processing.** At the end of Lecture 3 we compute

$$\int_0^{2\pi}\sin(mx)\sin(nx)\,dx = \begin{cases}0 & m\neq n\\ \pi & m = n\end{cases}$$

This is **orthogonality**, and it is the reason Fourier analysis works at all — it is the mechanism that lets you extract one frequency from a signal containing all of them. Every audio codec, every image compressor, and every spectrum analyser rests on that one line. We prove it with a product-to-sum identity and about three lines of integration.

---

## What Will Be Hard

**Choosing $u$.** There is a mnemonic (LIATE) and it works most of the time, but it is a heuristic, not a theorem. Some integrals need the "wrong" choice, and one important integral — $\int e^x\sin x\,dx$ — never terminates at all and must be solved by an algebraic trick instead.

**Knowing when to stop.** Integration by parts can be applied to any integral. It rarely helps. Applying it to $\int\frac{dx}{1+x^2}$ produces a more complicated integral than you started with, and students who have just learned the technique will do this. **Parts is for products of two unlike things**, one of which simplifies when differentiated.

---

## This Week's Work

1. **Quiz 01** — Monday, 15 minutes, **covers Week 0** (the FTC, substitution, applications)
2. **PS 1** — released Wednesday, due Wednesday of Week 2
3. **Lab 1** — reduction formulas, and a 300-year-old formula for $\pi$ that converges terribly

---

*Next: Monday — Integration by Parts*

# MATH 142 · Calculus II
## Week 12 · Overview
### Systems; Numerical Methods Preview; Final Review

---

**Topic:** the last week — where everything goes next
**Reading:** Stewart §9.6 | Apostol Ch. 8 §8.8
**Assessment this week:** Lab 12, **Quiz 12** *(Mon 12 Apr, 11:00 — covers Week 11)*, PS 12 *(ungraded)*, and the **FINAL EXAM**

---

## ⚠ The Final Exam

**Tuesday 20 April, 09:00–11:30 (finals week). 150 minutes. Comprehensive — Weeks 0–12. Two-page cheat sheet. No calculator. 20% of the course.**

**A full revision guide is in this week's `resources/` folder.** It contains a topic map for all thirteen weeks, the errors that have recurred all term, a two-page sheet plan, and a sample paper.

**Also in `resources/`: a Course Retrospective.** Read it **after** the exam, not before — it is not revision.

---

## This Week's Material Is Not Examined Heavily

**Week 12 exists to finish the story**, not to add to the pile. Systems and numerical methods appear on the final only in the lightest way; **the exam is weighted towards Weeks 0–11.**

**Spend your time on revision.** The lectures this week are short and the lab is a self-diagnostic.

---

## The Three Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Monday | Systems of Differential Equations | Two coupled unknowns; the phase plane |
| **Lecture 2** | Tuesday | Numerical Methods Preview | What you have been doing all term, named properly |
| **Lecture 3** | Friday | The Road Ahead | Where every thread of this course continues |

---

## Systems

**When two quantities change together, one equation is not enough:**

$$\frac{dx}{dt} = f(x,y), \qquad \frac{dy}{dt} = g(x,y)$$

**The classic example is predator and prey** — the Lotka–Volterra equations, where a fox population and a rabbit population each drive the other. **Neither can be solved in closed form**, but the system has a **conserved quantity**, and that single fact explains the whole picture: the populations cycle forever.

*(Verified: under RK4 the conserved quantity holds to 11 digits over 20 time units.)*

**And numerically, nothing changes.** RK4 applied to a system is RK4 applied componentwise — **the method you measured last week works unaltered.**

---

## Numerical Methods, Named

**You have spent twelve weeks doing numerical analysis without being told.** Lecture 2 puts names to it:

| What you did | Its name | Where |
|---|---|---|
| Trapezoid, midpoint, Simpson | **Numerical quadrature** | Lab 0 |
| The Babylonian $\sqrt2$ iteration | **Newton's method** | Lab 6 |
| Euler, RK2, RK4 | **ODE integrators** | Lab 11 |
| Taylor polynomials with bounds | **Function approximation** | Lab 10 |
| Error ratios on halving $h$ | **Order of convergence** | *every lab* |

> **A small thing worth seeing:** Lab 6's Babylonian iteration $a_{n+1}=\frac12\left(a_n+\frac2{a_n}\right)$
> — attributed to 1700 BC — **is exactly Newton's method applied to $x^2-2$.** *(Verified: they are
> algebraically identical, and both give $\sqrt2$ to 24 digits in five steps.)* You met the oldest
> algorithm in mathematics and the standard modern one, and did not notice they were the same.

---

## The One Number

**Across eleven labs, one quantity has decided every practical question:**

| method | order | consequence |
|---|---|---|
| Wallis product | 1 | $8\times10^9$ factors for 10 digits — useless |
| Basel partial sums | 1 | $10^{10}$ terms |
| Euler's method | 1 | $1.4\times10^{10}$ steps |
| Trapezoid, midpoint | 2 | usable |
| Simpson's rule | **4** | 128 points |
| RK4 | **4** | 320 steps for 12 digits |
| Newton / Babylonian | **quadratic** | 48 digits in 6 steps |

*(All measured in this course.)*

**Not elegance. Not age. Not cleverness. The exponent $p$ in $\text{error}\approx Ch^p$.**

---

## What This Week's Lab Is

**Lab 12 is a self-diagnostic**, and it is graded on completion and honesty rather than on getting everything right. **It is a fair sample of the final**, taken under exam conditions, and its purpose is to tell you what to revise while there is still time.

**PS 12 is ungraded** and carries the same purpose.

---

## This Week's Work

1. **Quiz 12** — Monday, 15 minutes, **covers Week 11** (separable and linear ODEs). *The last quiz.*
2. **Lab 12** — the self-diagnostic. **Do it under exam conditions.**
3. **PS 12** — ungraded, with answers included.
4. **The FINAL EXAM.** See the revision guide in `resources/`.

---

*Next: Monday — Systems of Differential Equations*

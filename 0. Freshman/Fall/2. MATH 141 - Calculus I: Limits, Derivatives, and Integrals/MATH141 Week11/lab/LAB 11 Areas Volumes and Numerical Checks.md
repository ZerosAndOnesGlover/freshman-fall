# MATH 141 · Lab 11
## Areas, Volumes, and Numerical Checks

**Duration:** 2 hours · **20 points**
**Date:** Friday 11 December 2026 · 15:00–16:50 · Lab Section (Week 11) — covers Week 11 (Lectures 01–03)

---

## Overview

Every formula this week can be checked numerically, and this lab builds the habit. You will sketch,
set up, evaluate by hand, and then confirm with a numerical integral — catching your own set-up
errors before they reach a problem set.

Bring a laptop. Simpson's rule in ten lines of Python is enough.

---

## Part 1: The Crossing Trap (5 pts)

**1A.** Sketch $y=\sin x$ and $y=\cos x$ on $[0,\pi/2]$ and mark the crossing. *(1 pt)*

**1B.** Compute $\int_0^{\pi/2}(\sin x-\cos x)\,dx$ **without** splitting. Record the value. *(1 pt)*

**1C.** Now compute the area correctly by splitting. Record both values side by side and explain, in
two sentences, what the first number actually measures. *(3 pts)*

---

## Part 2: Set Up, Evaluate, Verify (7 pts)

For each region: sketch it, set up the integral, evaluate by hand, then check numerically.

**2A.** Area between $y=x^2$ and $y=x^3$ on $[0,1]$. *(2 pts)*

**2B.** Volume from revolving $y=\sqrt x$ on $[0,4]$ about the $x$-axis. *(2 pts)*

**2C.** Volume from revolving the region between $y=\sqrt x$ and $y=x$ on $[0,1]$ about the
$x$-axis. *(3 pts)*

For 2C, **also** compute the incorrect $\pi\int_0^1(\sqrt x-x)^2dx$ and record how far off it is. You
should find a factor of exactly 5.

---

## Part 3: Two Methods, One Answer (5 pts)

The region under $y=x^2$ on $[0,2]$ is revolved about the $y$-axis.

**3A.** Compute the volume by **shells**. *(2 pts)*

**3B.** Compute it by **washers in $y$**, inverting to $x=\sqrt y$. *(2 pts)*

**3C.** Confirm they agree, and state in one sentence why this is a useful check rather than a
coincidence. *(1 pt)*

---

## Part 4: Build Your Own (3 pts)

Invent a solid whose cross-sections perpendicular to the $x$-axis are **equilateral triangles**, with
base the region between $y=x$ and $y=x^2$ on $[0,1]$.

Set up and evaluate the volume. State the area formula for an equilateral triangle of side $s$, and
verify your answer numerically.

---

## Deliverables

One document with sketches, set-ups, hand evaluations, numerical checks, and the written answers to
1C, 2C, 3C.

## Grading

| Part | Points |
|---|---|
| 1 — the crossing trap, with explanation | 5 |
| 2 — three set-ups verified, including the factor-of-5 error | 7 |
| 3 — both methods agreeing, with justification | 5 |
| 4 — a self-designed solid, verified | 3 |
| **Total** | **20** |

---

*MATH 141 · Week 11 · Lab 11 · © CSE Department*

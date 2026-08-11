# MATH 141 · Lab 04
## Rules, Chains, and Motion

**Duration:** 2 hours · **20 points**
**Lab session:** Friday of Week 4

---

## Overview

Three activities: verify the differentiation rules numerically, build intuition for the chain rule by
composing functions, and analyse a motion problem end to end. Bring a calculator or laptop; a short
Python or spreadsheet session will do everything needed.

---

## Part 1: Checking Rules Numerically (6 pts)

The **central difference** approximates a derivative:

$$f'(a)\approx\frac{f(a+h)-f(a-h)}{2h}$$

**1A.** For $f(x)=(3x^2+1)(x^3-2x)$ at $a=2$, compute the central difference with
$h=10^{-2},10^{-4},10^{-6},10^{-8}$. Compare with the product-rule answer $178$. *(2 pts)*

**1B.** Record what happens as $h$ shrinks past $10^{-8}$. The approximation should get *better* and
does not. Explain why, in terms of floating-point subtraction. *(2 pts)*

**1C.** Repeat 1A for $f(x)=\dfrac{x}{\sqrt{x^2+1}}$ at $a=1.2$ against the exact
$\dfrac{1}{(x^2+1)^{3/2}}$. *(2 pts)*

---

## Part 2: The Chain Rule, Seen (6 pts)

**2A.** For $f(u)=u^5$ and $u=g(x)=x^2+1$, compute $\frac{df}{du}$ at $u=g(1)$, $\frac{du}{dx}$ at
$x=1$, and their product. Verify against the direct derivative of $(x^2+1)^5$ at $x=1$. *(3 pts)*

**2B.** Build a three-fold composition — $\sqrt{1+\sin(x^2)}$ — and differentiate it. Identify the
three layers explicitly before differentiating, then verify numerically at $x=1$. *(3 pts)*

---

## Part 3: A Complete Motion Analysis (8 pts)

A particle has position $s(t)=t^4-8t^3+18t^2$ metres on $0\le t\le4$.

**3A.** Tabulate $s$, $v$ and $a$ at $t=0,1,2,3,4$. *(2 pts)*

**3B.** Find every $t$ where $v=0$, and every $t$ where $a=0$. Factor first. *(2 pts)*

**3C.** Sketch $s(t)$, $v(t)$ and $a(t)$ on the same time axis, one above the other. Mark where $v=0$
on the $s$ graph and where $a=0$ on the $v$ graph, and say what each corresponds to. *(2 pts)*

**3D.** Compute displacement and total distance. State whether they agree, and **justify from the
factored form of $v$** rather than by computing both. *(2 pts)*

---

## Deliverables

A single document with your tables, computations, sketches, and written answers to 1B, 2B, 3C and 3D.

## Grading

| Part | Points |
|---|---|
| 1 — numerical verification and the floating-point explanation | 6 |
| 2 — chain rule decomposition and verification | 6 |
| 3 — complete motion analysis with justification | 8 |
| **Total** | **20** |

---

*MATH 141 · Week 4 · Lab 04 · © CSE Department*

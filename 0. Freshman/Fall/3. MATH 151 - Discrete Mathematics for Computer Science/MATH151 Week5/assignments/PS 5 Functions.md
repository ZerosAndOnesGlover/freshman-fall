# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 5: Functions
### Released: Friday 30 October 2026, 14:00 (after the Friday lecture) | Due: Friday 6 November 2026, 17:00 (Week 6)

---

**Instructions:**
- For every injectivity/surjectivity claim: state clearly whether you are proving or disproving, and use the correct proof strategy (construction for surjectivity, algebra for injectivity, explicit counterexamples for disproof).
- Always identify the domain and codomain of every function before analyzing it.
- Show all work.
- Submit as a single PDF.

**Expected time:** about 3 hours. **Scoring:** 100 points total.

---

## Part A — Is It a Function? (21 points)

**A1.** *(9 pts)* For each relation, decide whether it is a well-defined function with the
stated domain and codomain. If not, say **which** requirement fails — totality or well-definedness.

**(a)** $\{(1,a),(2,b),(3,a),(4,c)\}$ from $\{1,2,3,4\}$ to $\{a,b,c\}$

**(b)** $\{(1,a),(1,b),(2,c),(3,a),(4,b)\}$ from $\{1,2,3,4\}$ to $\{a,b,c\}$

**(c)** $\{(1,a),(2,b),(4,c)\}$ from $\{1,2,3,4\}$ to $\{a,b,c\}$

**A2.** *(12 pts)* Let $f(x) = x^2 - 4x + 3$.

**(a)** Is $f: \mathbb{R} \to \mathbb{R}$ injective? Prove or give a counterexample.

**(b)** Show that restricting the domain to $[2,\infty)$ makes $f$ injective, with proof.

---

## Part B — Classification (20 points)

**B1.** *(20 pts)* For each function, state whether it is injective, surjective, both
(bijective), or neither. Prove each property that holds and give an explicit counterexample for each
that fails.

**(a)** $f: \mathbb{Z} \to \mathbb{Z}$, $f(x) = -2x + 7$

**(b)** $f: \mathbb{Z} \to \mathbb{N}$, $f(x) = |x|$

**(c)** $f: \mathbb{Z}^+ \to \mathbb{Z}^+$, $f(n) = n^2$

**(d)** $f: \mathbb{Z} \to \mathbb{Z}$, defined by $f(n) = n+1$ if $n$ is even, $f(n) = n-1$ if $n$ is odd

---

## Part C — Composition and Inverses (47 points)

**C1.** (10 pts) Let $f: \mathbb{Z}\to\mathbb{Z}$, $f(x)=2x-1$, and $g:\mathbb{Z}\to\mathbb{Z}$, $g(x)=x^2$.

- (a) Compute $(g\circ f)(x)$.
- (b) Compute $(f\circ g)(x)$.

---

**C2.** (12 pts) Prove: if $f: A\to B$ is injective and $g: B\to C$ is NOT injective, is $g\circ f: A \to C$ necessarily non-injective? Prove your answer, or give a counterexample showing $g\circ f$ CAN still be injective.

---

**C3.** (12 pts) Determine whether each function is invertible over the stated domain/codomain. If invertible, find the explicit formula for $f^{-1}$ and verify $f^{-1}(f(x))=x$.

- (a) $f: \mathbb{R}-\{0\}\to\mathbb{R}-\{0\}$, $f(x)=1/x$
- (b) $f: [0,\infty)\to[0,\infty)$, $f(x)=x^2$

---

**C4.** (13 pts) Prove: if $f: A\to B$ and $g: B\to C$ are both bijective, then $(g\circ f)^{-1} = f^{-1}\circ g^{-1}$.

*(This appeared as an exercise in Thursday's lecture — write the full formal proof here.)*

---

## Part D — Bijections and Cardinality (12 points)

**D1.** *(12 pts)* Exhibit an explicit bijection $\mathbb{N} \to \{1, 4, 9, 16, \ldots\}$ (the
perfect squares) and prove it is a bijection. Comment on the fact that the squares grow ever sparser
yet remain countable.

# MATH 151: Discrete Mathematics for Computer Science
## Problem Set 5: Functions
### Released: Friday, Week 5 | Due: Friday, Week 6 (11:59 PM)

---

**Instructions:**
- For every injectivity/surjectivity claim: state clearly whether you are proving or disproving, and use the correct proof strategy (construction for surjectivity, algebra for injectivity, explicit counterexamples for disproof).
- Always identify the domain and codomain of every function before analyzing it.
- Show all work.
- Submit as a single PDF.

**Scoring:** 100 points total, plus an optional 8-point bonus.

---

## Part A — Is It a Function? (20 points)

**A1.** *(2 pts each)* For each relation, decide whether it is a well-defined function with the
stated domain and codomain. If not, say **which** requirement fails — totality or well-definedness.

**(a)** $\{(1,a),(2,b),(3,a),(4,c)\}$ from $\{1,2,3,4\}$ to $\{a,b,c\}$

**(b)** $\{(1,a),(1,b),(2,c),(3,a),(4,b)\}$ from $\{1,2,3,4\}$ to $\{a,b,c\}$

**(c)** $\{(1,a),(2,b),(4,c)\}$ from $\{1,2,3,4\}$ to $\{a,b,c\}$

**(d)** $f(x) = 1/x$ from $\mathbb{R}$ to $\mathbb{R}$

**A2.** *(3 pts each)* Let $f(x) = x^2 - 4x + 3$.

**(a)** Find the range of $f: \mathbb{R} \to \mathbb{R}$. *(Hint: complete the square.)*

**(b)** Is $f: \mathbb{R} \to \mathbb{R}$ injective? Prove or give a counterexample.

**(c)** Is $f: \mathbb{R} \to \mathbb{R}$ surjective? Prove or give a counterexample.

**(d)** Show that restricting the domain to $[2,\infty)$ makes $f$ injective, with proof.

---

## Part B — Classification (28 points)

**B1.** *(4 pts each)* For each function, state whether it is injective, surjective, both
(bijective), or neither. Prove each property that holds and give an explicit counterexample for each
that fails.

**(a)** $f: \mathbb{Z} \to \mathbb{Z}$, $f(x) = -2x + 7$

**(b)** $f: \mathbb{Z} \to \mathbb{N}$, $f(x) = |x|$

**(c)** $f: \mathbb{R} \to \mathbb{R}$, $f(x) = \dfrac{1}{x^2+1}$

**(d)** $f: \mathbb{Z} \times \mathbb{Z} \to \mathbb{Z}$, $f(m,n) = m - n$

**(e)** $f: \mathbb{Z}^+ \to \mathbb{Z}^+$, $f(n) = n^2$

**(f)** $f: \mathcal{P}(\{1,2,3\}) \to \mathcal{P}(\{1,2,3\})$, $f(S) = \overline{S}$ (complement within $\{1,2,3\}$)

**(g)** $f: \mathbb{Z} \to \mathbb{Z}$, defined by $f(n) = n+1$ if $n$ is even, $f(n) = n-1$ if $n$ is odd

---

## Part C — Composition and Inverses (24 points)

**C1.** (6 pts) Let $f: \mathbb{Z}\to\mathbb{Z}$, $f(x)=2x-1$, and $g:\mathbb{Z}\to\mathbb{Z}$, $g(x)=x^2$.

- (a) Compute $(g\circ f)(x)$.
- (b) Compute $(f\circ g)(x)$.
- (c) Compute $(g\circ f)(3)$ two ways: (i) directly using your formula from (a), (ii) by first computing $f(3)$ then applying $g$. Verify they match.

---

**C2.** (6 pts) Prove: if $f: A\to B$ is injective and $g: B\to C$ is NOT injective, is $g\circ f: A \to C$ necessarily non-injective? Prove your answer, or give a counterexample showing $g\circ f$ CAN still be injective.

---

**C3.** (6 pts) Determine whether each function is invertible over the stated domain/codomain. If invertible, find the explicit formula for $f^{-1}$ and verify $f^{-1}(f(x))=x$.

- (a) $f: \mathbb{R}\to\mathbb{R}$, $f(x) = 7x+2$
- (b) $f: \mathbb{R}-\{0\}\to\mathbb{R}-\{0\}$, $f(x)=1/x$
- (c) $f: [0,\infty)\to[0,\infty)$, $f(x)=x^2$
- (d) $f: \mathbb{Z}\to\mathbb{Z}$, $f(x) = 3x$

---

**C4.** (6 pts) Prove: if $f: A\to B$ and $g: B\to C$ are both bijective, then $(g\circ f)^{-1} = f^{-1}\circ g^{-1}$.

*(This appeared as an exercise in Thursday's lecture — write the full formal proof here.)*

---

---

## Part D — Bijections and Cardinality (28 points)

**D1.** *(6 pts)* Exhibit an explicit bijection $\mathbb{N} \to \{1, 4, 9, 16, \ldots\}$ (the
perfect squares) and prove it is a bijection. Comment on the fact that the squares grow ever sparser
yet remain countable.

**D2.** *(6 pts)* Prove that the union of two countable sets is countable. *(Hint: interleave the two
listings, and say what you do about elements appearing in both.)*

**D3.** *(6 pts)* Using the Cantor pairing function $\pi(x,y) = \dfrac{(x+y)(x+y+1)}{2} + y$:

- (a) Compute $\pi(3,4)$ and $\pi(4,3)$, and explain from the diagonal walk why they differ.
- (b) Find the pair $(x,y)$ with $\pi(x,y) = 14$.

**D4.** *(5 pts)* Give a bijection between the open interval $(0,1)$ and $\mathbb{R}$, and verify it
is a bijection. What does this say about using "length" as a measure of set size?

**D5.** *(5 pts)* The set of **finite** subsets of $\mathbb{N}$ is countable, but
$\mathcal{P}(\mathbb{N})$ is not. Explain precisely where the listing argument succeeds for the
first and fails for the second.

## Bonus (8 points — optional)

**Bonus 1.** (4 pts) Prove: if $A$ and $B$ are finite sets with $|A|=|B|$, and $f:A\to B$ is injective, then $f$ is automatically surjective (and hence bijective).

*(This is the "same-size implies equivalence of injective/surjective" fact stated in Monday's lecture — prove it rigorously by counting: a list of $n$ distinct outputs drawn from an $n$-element codomain must exhaust it.)*

**Bonus 2.** (4 pts) A function $f:\{1,\ldots,n\}\to\{1,\ldots,n\}$ that is a bijection is called a **permutation** of $\{1,\ldots,n\}$. Prove: if $f$ is a permutation of $\{1,\ldots,n\}$, then $f\circ f\circ\cdots\circ f$ ($f$ composed with itself $k$ times, for large enough $k$) eventually equals $\text{id}$.

*(Hint: Consider the sequence $x, f(x), f(f(x)), \ldots$ for a fixed element $x$. Since $\{1,\ldots,n\}$ is finite, this sequence must eventually repeat a value, since $n+1$ terms cannot all be distinct in an $n$-element set. Then use injectivity of $f$ to show the repetition must cycle back to $x$ itself, not some later element.)*

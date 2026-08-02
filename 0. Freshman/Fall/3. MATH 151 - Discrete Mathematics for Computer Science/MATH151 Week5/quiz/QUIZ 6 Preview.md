# MATH 151 · Discrete Mathematics for Computer Science
## Quiz 6 — Scope Preview
### Quiz administered: Monday, Week 6 (first 15 minutes of lecture)

---

**Coverage:** Weeks 5 and 6 material:
- Week 5: Functions — injective, surjective, bijective, composition, inverses, bijections and cardinality
- Week 6: Relations — reflexive, symmetric, transitive; equivalence relations; partial orders (covered next week)

---

## What You Must Know Cold for Week 5 Material

### 1. Function Definition

A function $f:A\to B$ is a relation satisfying $\forall a\in A, \exists! b\in B, (a,b)\in f$ — totality + well-definedness.

### 2. The Three Properties — Definitions and Proof Strategies

| Property | Definition | To Prove | To Disprove |
|---|---|---|---|
| Injective | $f(a_1)=f(a_2)\to a_1=a_2$ | Assume equal outputs, derive equal inputs | Exhibit $a_1\neq a_2$ with $f(a_1)=f(a_2)$ |
| Surjective | $\forall b\exists a, f(a)=b$ | Given $b$, construct $a$ | Exhibit $b$ with no preimage |
| Bijective | Both | Prove both | Disprove either |

### 3. Counting Facts (finite sets)

- $f$ injective $\Rightarrow |A|\leq|B|$
- $f$ surjective $\Rightarrow |A|\geq|B|$
- $|A|=|B|$: injective $\iff$ surjective $\iff$ bijective (same-size shortcut)

### 4. Composition

- $(g\circ f)(a) = g(f(a))$ — apply $f$ first, then $g$
- NOT commutative in general
- IS associative
- Injective+injective → composition injective. Surjective+surjective → composition surjective.
- $g\circ f$ injective forces $f$ injective (not $g$). $g\circ f$ surjective forces $g$ surjective (not $f$).

### 5. Inverses

- $f$ invertible $\iff$ $f$ bijective (know both directions of this proof)
- $(g\circ f)^{-1} = f^{-1}\circ g^{-1}$ (order reverses!)

## Sample Quiz 6 Problems (Week 5 portion)

**Problem 1.** (4 pts) Classify $f:\mathbb{Z}\to\mathbb{Z}$, $f(x)=3x-2$ as injective/surjective/bijective with proof.

**Problem 2.** (4 pts) Given $f(x)=x+1$, $g(x)=2x$, compute $(g\circ f)(x)$ and determine if $f$ is invertible; if so find $f^{-1}$.

**Problem 4.** (4 pts) From Week 6 — relation properties (see Week 6 materials).

---

## Study Recommendations

1. **Drill the injective/surjective proof templates** until automatic — many quiz points come from correctly executing "let $a_1,a_2$ arbitrary, assume $f(a_1)=f(a_2)$..." vs "let $b$ arbitrary, construct $a$..."

2. **Practice finding inverse formulas** by solving $y=f(x)$ for $x$. This algebra must be fast and error-free.

3. **Memorize the composition preservation facts** and their asymmetry — quizzes test whether you know $g\circ f$ injective implies $f$ (not $g$) injective.


5. **Know the same-size shortcut** for finite sets — it appears in proofs throughout the rest of the course (counting, Week 6-7).

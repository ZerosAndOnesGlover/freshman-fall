# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 5.1 (L15) — Functions: Definitions and Fundamental Properties
### Monday, Week 5

**Date:** Monday 21 September 2026 · 13:00–13:50 · Week 5

---

> **Core Question:** What is a function, precisely, and what does it mean for a function to be one-to-one or onto?

---

## 1. The Formal Definition of a Function

**Definition.** A **function** $f$ from set $A$ to set $B$, written $f: A \to B$, is a relation $f \subseteq A \times B$ such that:

$$\forall a \in A, \exists! b \in B, (a,b) \in f$$

(Recall $\exists!$ from Week 1 — "there exists a unique.")

Equivalently, in the notation we're used to: for every $a \in A$, there is exactly one $b \in B$ such that $f(a) = b$.

**Terminology:**
- $A$ is the **domain** of $f$
- $B$ is the **codomain** of $f$
- For $a \in A$, $f(a)$ is the **image** of $a$ (the unique element $b$ with $(a,b) \in f$)
- The **range** (or **image**) of $f$ is $\{f(a) : a \in A\} \subseteq B$ — note the range may be a *proper subset* of the codomain

**Why this definition matters:** A function is a set of ordered pairs satisfying two conditions:
1. **Totality:** every element of $A$ appears as a first coordinate (the function is defined everywhere on $A$)
2. **Well-definedness:** no element of $A$ appears as the first coordinate of two different pairs (the output is unique)

Violating either condition means you don't have a function.

### Examples of Relations That Are NOT Functions

**Not a function (fails totality):** $R = \{(1,a), (2,b)\}$ as a relation from $\{1,2,3\}$ to $\{a,b,c\}$. Element $3 \in A$ has no image — the relation is not defined on all of $A$.

**Not a function (fails well-definedness):** $R = \{(1,a), (1,b), (2,c)\}$ as a relation from $\{1,2\}$ to $\{a,b,c\}$. Element $1$ maps to both $a$ and $b$ — not unique.

**Is a function:** $R = \{(1,a),(2,a),(3,b)\}$ as a relation from $\{1,2,3\}$ to $\{a,b\}$. Every element of the domain has exactly one image (multiple domain elements CAN map to the same codomain element — that's fine).

---

## 2. Domain, Codomain, and Range — A Critical Distinction

Consider $f: \mathbb{R} \to \mathbb{R}$ defined by $f(x) = x^2$.

- **Domain:** $\mathbb{R}$ (all reals — the function is defined for every real input)
- **Codomain:** $\mathbb{R}$ (as *declared* — this is a choice made when specifying the function)
- **Range:** $[0, \infty)$ (the actual set of outputs — a proper subset of the codomain, since no negative number is ever an output)

**The codomain is part of the specification of the function — not something you compute.** Two functions with the same domain, same rule, but different declared codomains are technically different functions (this distinction becomes essential when discussing surjectivity, below).

**In programming:** The codomain corresponds to the declared return type of a function; the range is the actual set of values the function can produce. A function declared to return `int` (codomain = all ints) might only ever actually return non-negative values (range = non-negative ints) — this gap between codomain and range is exactly the domain/codomain/range distinction.

---

## 3. Injective Functions (One-to-One)

**Definition.** A function $f: A \to B$ is **injective** (or **one-to-one**, written 1-1) if distinct inputs always produce distinct outputs:

$$\forall a_1, a_2 \in A, \quad f(a_1) = f(a_2) \rightarrow a_1 = a_2$$

**Equivalent formulation (contrapositive):**

$$\forall a_1, a_2 \in A, \quad a_1 \neq a_2 \rightarrow f(a_1) \neq f(a_2)$$

**Proof strategy for injectivity:**
- **To prove:** Assume $f(a_1) = f(a_2)$ for arbitrary $a_1, a_2 \in A$. Derive $a_1 = a_2$ (direct proof of the first formulation), OR assume $a_1 \neq a_2$ and derive $f(a_1) \neq f(a_2)$ (using contrapositive — often easier with algebra).
- **To disprove:** Exhibit specific $a_1 \neq a_2$ with $f(a_1) = f(a_2)$.

### Worked Example 1

**Claim.** $f: \mathbb{Z} \to \mathbb{Z}$ defined by $f(x) = 2x + 3$ is injective.

**Proof.** Let $a_1, a_2 \in \mathbb{Z}$ be arbitrary. Assume $f(a_1) = f(a_2)$.

Then $2a_1 + 3 = 2a_2 + 3$.

Subtracting 3: $2a_1 = 2a_2$.

Dividing by 2: $a_1 = a_2$.

Since $a_1, a_2$ were arbitrary, $f$ is injective. ∎

### Worked Example 2

**Claim.** $f: \mathbb{R} \to \mathbb{R}$ defined by $f(x) = x^2$ is **not** injective.

**Disproof.** Take $a_1 = 2$, $a_2 = -2$. Then $a_1 \neq a_2$, but $f(2) = 4 = f(-2)$.

So $f$ is not injective. ∎

**Important nuance:** If we restrict the domain to $[0, \infty)$, the function $g: [0,\infty) \to \mathbb{R}$ with $g(x) = x^2$ **IS** injective — the domain restriction eliminates the collision. This shows injectivity depends on the specific domain chosen, not just the "formula."

### Worked Example 3 — Discrete Case

**Claim.** $f: \mathbb{Z} \to \mathbb{Z}$ defined by $f(x) = x^3 - x$ is **not** injective.

**Disproof.** $f(0) = 0 - 0 = 0$. $f(1) = 1 - 1 = 0$. $f(-1) = -1-(-1) = 0$.

So $f(0) = f(1) = f(-1) = 0$, with $0, 1, -1$ all distinct.

So $f$ is not injective. ∎

---

## 4. Surjective Functions (Onto)

**Definition.** A function $f: A \to B$ is **surjective** (or **onto**) if every element of the codomain is achieved:

$$\forall b \in B, \exists a \in A, f(a) = b$$

**Proof strategy for surjectivity:**
- **To prove:** Let $b \in B$ be arbitrary. *Construct* a specific $a \in A$ (in terms of $b$) and verify $f(a) = b$.
- **To disprove:** Exhibit a specific $b \in B$ for which no $a \in A$ satisfies $f(a) = b$.

### Worked Example 4

**Claim.** $f: \mathbb{R} \to \mathbb{R}$ defined by $f(x) = 2x + 3$ is surjective.

**Proof.** Let $y \in \mathbb{R}$ be arbitrary. We seek $x \in \mathbb{R}$ with $f(x) = y$, i.e., $2x + 3 = y$.

Solving: $x = \frac{y-3}{2}$.

Since $y \in \mathbb{R}$, $\frac{y-3}{2} \in \mathbb{R}$ — this is a valid domain element.

Verify: $f\left(\frac{y-3}{2}\right) = 2 \cdot \frac{y-3}{2} + 3 = (y-3) + 3 = y$. ✓

Since $y$ was arbitrary, $f$ is surjective. ∎

**Compare with $f: \mathbb{Z} \to \mathbb{Z}$ defined by $f(x) = 2x+3$:**

**Claim.** This is **not** surjective.

**Disproof.** Take $y = 4$. We need $x \in \mathbb{Z}$ with $2x + 3 = 4$, i.e., $x = 1/2 \notin \mathbb{Z}$.

So no integer $x$ satisfies $f(x) = 4$. $f$ is not surjective. ∎

**Key lesson:** Whether a function is surjective depends critically on both the domain and codomain — the SAME formula can be surjective over $\mathbb{R}$ but not over $\mathbb{Z}$.

### Worked Example 5

**Claim.** $f: \mathbb{R} \to \mathbb{R}$ defined by $f(x) = x^2$ is **not** surjective.

**Disproof.** Take $y = -1$. We need $x \in \mathbb{R}$ with $x^2 = -1$. No real number squares to $-1$.

So $f$ is not surjective (onto $\mathbb{R}$). ∎

*(But $f: \mathbb{R} \to [0,\infty)$ with the same rule IS surjective — again, the codomain matters.)*

---

## 5. Bijective Functions (One-to-One Correspondence)

**Definition.** A function $f: A \to B$ is **bijective** if it is both injective and surjective.

A bijection establishes a perfect pairing between $A$ and $B$: every element of $A$ maps to a distinct element of $B$, and every element of $B$ is hit.

**Fact.** If $f: A \to B$ is a bijection between finite sets, then $|A| = |B|$.

This is the formal foundation of **counting by correspondence** — instead of counting a set directly, you can count a different set that is in bijection with it (essential technique in Week 6-7 combinatorics).

### Worked Example 6

**Claim.** $f: \mathbb{R} \to \mathbb{R}$ defined by $f(x) = 2x+3$ is bijective.

**Proof.** We showed injectivity (Example 1, with domain $\mathbb{Z}$, but the same algebra works over $\mathbb{R}$) and surjectivity (Example 4) above. Since both hold, $f$ is bijective. ∎

---

## 6. Summary Table — Diagnostic Techniques

| Property | Formal Definition | To Prove | To Disprove |
|---|---|---|---|
| Injective | $f(a_1)=f(a_2) \to a_1=a_2$ | Assume $f(a_1)=f(a_2)$; derive $a_1=a_2$ | Find $a_1\neq a_2$ with $f(a_1)=f(a_2)$ |
| Surjective | $\forall b\exists a, f(a)=b$ | Given arbitrary $b$; construct $a$ with $f(a)=b$ | Find $b$ with no preimage |
| Bijective | Injective AND Surjective | Prove both | Disprove either one |

---

## 7. Functions on Finite Sets — Counting Consequences

For $f: A \to B$ with $A, B$ finite:

| Condition | Consequence |
|---|---|
| $f$ injective | $|A| \leq |B|$ |
| $f$ surjective | $|A| \geq |B|$ |
| $f$ bijective | $|A| = |B|$ |
| $|A| = |B|$ and $f$ injective | $f$ is automatically bijective |
| $|A| = |B|$ and $f$ surjective | $f$ is automatically bijective |

The last two facts are extremely useful: **for functions between finite sets of the same size, injective and surjective are equivalent** — proving one gives you the other for free. This follows from a counting argument: an injective map out of an $n$-element set produces $n$ distinct outputs, which must exhaust an $n$-element codomain. Week 8 names the underlying principle.

**Warning:** This equivalence FAILS for infinite sets. Consider $f: \mathbb{Z}^+ \to \mathbb{Z}^+$ defined by $f(n) = n+1$. This is injective (distinct inputs give distinct outputs) but NOT surjective (nothing maps to 1). Infinite sets can be in bijection with proper subsets of themselves — a defining feature of infinite sets (Hilbert's Hotel; developed properly in Friday's lecture on cardinality).

---

## 8. Functions in Computer Science

**Hash functions:** A hash function $h: \text{Keys} \to \{0,\ldots,m-1\}$ is a function in the formal sense — every key must map to exactly one bucket. A "perfect hash function" is an injective (and often bijective, if $|Keys|=m$) hash function — no collisions.

**Encryption:** An encryption scheme $E_k: \text{Plaintext} \to \text{Ciphertext}$ must be injective — otherwise two different plaintexts could produce the same ciphertext, making decryption ambiguous (a fundamental security flaw). A good cipher's encryption function, for a fixed key, is in fact bijective (every ciphertext corresponds to exactly one plaintext).

**Compression:** Lossless compression functions must be injective (distinct inputs never compress to the same output — otherwise decompression is ambiguous). This is why the Pigeonhole Principle (Week 8) proves that **no lossless compression algorithm can compress every possible input** — there are more possible inputs of length $n$ than outputs of length $<n$.

**Type checking:** A well-typed total function `f: A -> B` in a language corresponds exactly to a mathematical function $A\to B$ — every value of type A produces exactly one value of type B (assuming no exceptions/non-termination, which break totality).

---

## 9. End-of-Lecture Exercises

For each function, determine domain/codomain given, and classify as injective, surjective, both, or neither. Prove your answer.

1. $f: \mathbb{Z} \to \mathbb{Z}$, $f(x) = 3x - 5$.

2. $f: \mathbb{Z} \to \mathbb{Z}$, $f(x) = x^2 + 1$.

3. $f: \mathbb{R} \to \mathbb{R}$, $f(x) = x^3$.

4. $f: \mathbb{Z}^+ \to \mathbb{Z}^+$, $f(n) = \lceil n/2 \rceil$ (ceiling of n/2).

5. $f: \mathbb{Z} \times \mathbb{Z} \to \mathbb{Z}$, $f(m,n) = m + n$.

6. $f: \mathcal{P}(\{1,2,3\}) \to \mathbb{Z}$, $f(S) = |S|$ (cardinality of subset S).

7. Let $A = \{1,2,3,4\}$ and $B = \{a,b,c\}$. Can there exist an injective function $f: A \to B$? Can there exist a surjective function $f: A \to B$? Justify each using the counting facts from Section 7.

8. **Challenge:** Many people expect $\mathbb{Z}\times\mathbb{Z}$ to be "bigger" than $\mathbb{Z}$, and so expect no surjection $\mathbb{Z}\to\mathbb{Z}\times\mathbb{Z}$ to exist. Argue informally for why that expectation is reasonable, then say what evidence would settle it. *(Friday's lecture resolves this: a bijection does exist, and the finite-counting intuition simply does not transfer to infinite sets.)*

---

*Next: Lecture 5.2 — Composition of Functions and Inverse Functions*

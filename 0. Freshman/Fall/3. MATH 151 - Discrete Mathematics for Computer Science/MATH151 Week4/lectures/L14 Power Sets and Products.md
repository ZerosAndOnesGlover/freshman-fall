# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 4.3 (L14) — Power Sets, Cartesian Products, and Inclusion-Exclusion
### Friday, Week 4

**Date:** Friday 18 September 2026 · 13:00–13:50 · Week 4

---

> **Core Question:** How do we build the set of all subsets of a set, and how do we combine two sets into ordered pairs?

---

## 1. The Power Set

**Definition.** The **power set** of a set $A$, denoted $\mathcal{P}(A)$ or $2^A$, is the set of all subsets of $A$:
$$\mathcal{P}(A) = \{S : S \subseteq A\}$$

**Key fact:** For every set $A$, both $\emptyset \in \mathcal{P}(A)$ and $A \in \mathcal{P}(A)$, since $\emptyset \subseteq A$ and $A \subseteq A$ always hold.

### Worked Examples

**Example 1:** $A = \emptyset$.
$$\mathcal{P}(\emptyset) = \{\emptyset\}$$
This has exactly one element — the empty set itself. Note $\mathcal{P}(\emptyset) \neq \emptyset$ — the power set of the empty set is NOT empty; it contains one element (the empty set).

**Example 2:** $A = \{a\}$.
$$\mathcal{P}(\{a\}) = \{\emptyset, \{a\}\}$$

**Example 3:** $A = \{a, b\}$.
$$\mathcal{P}(\{a,b\}) = \{\emptyset, \{a\}, \{b\}, \{a,b\}\}$$

**Example 4:** $A = \{a, b, c\}$.
$$\mathcal{P}(\{a,b,c\}) = \{\emptyset, \{a\},\{b\},\{c\},\{a,b\},\{a,c\},\{b,c\},\{a,b,c\}\}$$

---

## 2. The Cardinality of a Power Set

**Theorem.** For a finite set $A$ with $|A| = n$, $|\mathcal{P}(A)| = 2^n$.

**Proof.** By mathematical induction on $n$ (connecting back to Week 3!).

**Base case ($n=0$):** $A = \emptyset$. $\mathcal{P}(\emptyset) = \{\emptyset\}$, so $|\mathcal{P}(\emptyset)| = 1 = 2^0$. ✓

**Inductive step:** Assume that for any set with $k$ elements, the power set has $2^k$ elements. [IH]

Let $A$ be a set with $k+1$ elements. Fix any element $a \in A$, and let $B = A - \{a\}$, so $|B| = k$.

Every subset of $A$ either contains $a$ or does not:
- Subsets of $A$ **not** containing $a$ are exactly the subsets of $B$. By IH, there are $2^k$ of these.
- Subsets of $A$ **containing** $a$ are exactly the sets $S \cup \{a\}$ where $S$ is a subset of $B$. There are also $2^k$ of these (one for each subset of $B$).

These two categories are disjoint (a subset either contains $a$ or doesn't) and together cover all subsets of $A$.

$$|\mathcal{P}(A)| = 2^k + 2^k = 2 \cdot 2^k = 2^{k+1}$$

By induction, $|\mathcal{P}(A)| = 2^n$ for all finite $n$. ∎

**Intuitive combinatorial argument (alternative):** To build a subset of $A = \{a_1, \ldots, a_n\}$, make an independent binary choice for each element — include it or don't. There are $n$ independent binary choices, giving $2^n$ total subsets. This connects power sets directly to counting problems (Week 6).

**Why the notation $2^A$?** Each subset of $A$ corresponds to a function from $A$ to $\{0,1\}$ (1 if the element is included, 0 if not) — this is why the power set is sometimes written $2^A$, echoing the notation for "functions from $A$ to a 2-element set." We will see this connection formally in Week 5.

---

## 3. Power Sets in Computer Science

**Feature flags:** If a system has $n$ independent feature flags, there are $2^n$ possible configurations — exactly $|\mathcal{P}(\{1,\ldots,n\})|$.

**Subset-sum and knapsack problems:** These NP-complete problems (CS 301) search over the power set of a set of items — an inherently exponential search space, which is why brute-force solutions are $O(2^n)$.

**Bitmasks:** A common programming technique represents a subset of $\{0, 1, \ldots, n-1\}$ as an $n$-bit integer, where bit $i$ is 1 iff element $i$ is in the subset. This gives a natural bijection between $\mathcal{P}(\{0,\ldots,n-1\})$ and $\{0, 1, \ldots, 2^n - 1\}$.

```python
def power_set(elements):
    """Generate all subsets using bitmask technique."""
    n = len(elements)
    elements = list(elements)
    subsets = []
    for mask in range(2**n):
        subset = [elements[i] for i in range(n) if (mask >> i) & 1]
        subsets.append(subset)
    return subsets

print(power_set(['a', 'b', 'c']))
# [[], ['a'], ['b'], ['a','b'], ['c'], ['a','c'], ['b','c'], ['a','b','c']]
```

---

## 4. Ordered Pairs and Cartesian Products

Sets are unordered — $\{1,2\} = \{2,1\}$. But many mathematical structures require order. We need a new construction.

**Definition.** An **ordered pair** $(a, b)$ consists of two objects $a$ and $b$ in a specified order, with the property:
$$(a,b) = (c,d) \iff a=c \land b=d$$

(Formally, ordered pairs can be *constructed* from sets via the Kuratowski definition $(a,b) := \{\{a\},\{a,b\}\}$, but for this course we use ordered pairs as a primitive notion with the defining property above.)

**Contrast:** $\{a,b\} = \{b,a\}$ (sets), but $(a,b) \neq (b,a)$ in general (ordered pairs), unless $a=b$.

**Definition.** The **Cartesian product** of sets $A$ and $B$, denoted $A \times B$, is the set of all ordered pairs with first coordinate from $A$ and second coordinate from $B$:
$$A \times B = \{(a,b) : a \in A \land b \in B\}$$

### Worked Example

Let $A = \{1, 2\}$, $B = \{x, y, z\}$.

$$A \times B = \{(1,x),(1,y),(1,z),(2,x),(2,y),(2,z)\}$$

$$B \times A = \{(x,1),(x,2),(y,1),(y,2),(z,1),(z,2)\}$$

**Key fact:** $A \times B \neq B \times A$ in general (unless $A = \emptyset$, $B = \emptyset$, or $A = B$). Cartesian product is NOT commutative.

**Cardinality:** For finite sets, $|A \times B| = |A| \cdot |B|$.

*Proof sketch:* For each of the $|A|$ choices of first coordinate, there are $|B|$ choices of second coordinate — a direct application of the multiplication principle (formalized in Week 6).

---

## 5. Cartesian Products of More Than Two Sets

**Definition.** The Cartesian product of $n$ sets $A_1, A_2, \ldots, A_n$ is the set of ordered $n$-tuples:
$$A_1 \times A_2 \times \cdots \times A_n = \{(a_1, a_2, \ldots, a_n) : a_i \in A_i \text{ for each } i\}$$

**Special case:** $A^n = A \times A \times \cdots \times A$ ($n$ times) — the set of all ordered $n$-tuples from $A$.

**Example:** $\mathbb{R}^2 = \mathbb{R} \times \mathbb{R}$ is the Cartesian plane — every point is an ordered pair of real numbers. $\mathbb{R}^3$ is 3D space. This is precisely why we call it "Cartesian" — after Descartes, who introduced coordinate geometry.

---

## 6. Cartesian Products and Relations (Preview of Week 5)

**Definition (preview).** A **binary relation** $R$ from $A$ to $B$ is a subset of $A \times B$: $R \subseteq A \times B$.

This is the formal foundation for everything relational in mathematics and CS:
- A **function** $f: A \to B$ is a special kind of relation (a subset of $A\times B$ where each $a \in A$ appears in exactly one pair).
- A **database table** with columns of types $A$ and $B$ is (a finite subset of) $A \times B$.
- A **graph** is a relation on $V \times V$ where $V$ is the set of vertices.

We develop this fully next week, but understanding $A \times B$ now is the essential prerequisite.

---

## 7. Cartesian Products in Computer Science

**Tuples/structs:** Every tuple type in a programming language — `(int, string)` in Haskell, a `struct` in C, a `record` in Pascal — is literally an element of a Cartesian product of the component types.

**Database joins:** The Cartesian product (cross join) of two tables is the foundation of SQL joins. `SELECT * FROM A, B` computes $A \times B$; adding a `WHERE` clause filters this product down to a relation (a subset satisfying some condition).

```python
A = {1, 2}
B = {'x', 'y', 'z'}

cartesian_product = {(a, b) for a in A for b in B}
print(cartesian_product)
# {(1,'x'), (1,'y'), (1,'z'), (2,'x'), (2,'y'), (2,'z')}
```

**Nested loops:** The most direct computational realization of a Cartesian product is a pair of nested for-loops — this is precisely the loop-based interpretation of $\forall a \in A, \forall b \in B$ from Week 1.

---

## 8. Inclusion-Exclusion Principle

We saw the two-set case in Monday's lecture: $|A \cup B| = |A| + |B| - |A \cap B|$. This generalizes.

### Two Sets

$$|A \cup B| = |A| + |B| - |A \cap B|$$

### Three Sets

$$|A \cup B \cup C| = |A|+|B|+|C| - |A\cap B|-|A\cap C|-|B\cap C| + |A\cap B\cap C|$$

**Why the pattern?** Elements in exactly one set are counted once (correct). Elements in exactly two sets are counted twice in the individual terms, then subtracted once in the pairwise intersection terms — but this over-subtracts elements in all three sets, so we add back the triple intersection.

### Worked Example

In a class of 50 students: 20 take CS101, 25 take MATH151, 15 take PHYS141. 10 take both CS101 and MATH151, 8 take both CS101 and PHYS141, 5 take both MATH151 and PHYS141. 3 take all three.

How many students take at least one of these courses?

$$|CS \cup MATH \cup PHYS| = 20+25+15 - 10-8-5 + 3 = 60 - 23 + 3 = 40$$

**40 students** take at least one of the three courses; **10 students** take none.

### General ($n$ sets) — Stated Without Proof (proved in Week 8)

$$\left|\bigcup_{i=1}^{n} A_i\right| = \sum_i |A_i| - \sum_{i<j}|A_i \cap A_j| + \sum_{i<j<k}|A_i\cap A_j \cap A_k| - \cdots + (-1)^{n+1}|A_1\cap\cdots\cap A_n|$$

---

## 9. Inclusion-Exclusion in Computer Science

- **Counting problems:** How many integers from 1 to 1000 are divisible by 3 or 5? Use $|A \cup B| = |A|+|B|-|A\cap B|$ where $A$ = multiples of 3, $B$ = multiples of 5.
- **Probability:** $P(A \cup B) = P(A) + P(B) - P(A \cap B)$ (MATH 251 will build on this).
- **Database query optimization:** Estimating result sizes of OR conditions in WHERE clauses uses inclusion-exclusion-style reasoning.
- **Bloom filters / approximate counting:** Understanding overlap between sets is central to probabilistic data structure design.

---

## 10. Summary

```
Power Set:
  P(A) = {S : S ⊆ A}
  |P(A)| = 2^|A|  (for finite A)

Cartesian Product:
  A × B = {(a,b) : a∈A ∧ b∈B}
  |A × B| = |A|·|B|
  A × B ≠ B × A in general (not commutative)

Inclusion-Exclusion:
  |A∪B| = |A|+|B|-|A∩B|
  |A∪B∪C| = |A|+|B|+|C|-|A∩B|-|A∩C|-|B∩C|+|A∩B∩C|
```

---

## 11. End-of-Lecture Exercises

1. Compute $\mathcal{P}(A)$ for $A = \{1, 2, 3, 4\}$. Verify that $|\mathcal{P}(A)| = 16$.

2. Let $A = \{1,2\}$ and $B = \{2,3\}$.
   - (a) Compute $A \times B$.
   - (b) Compute $\mathcal{P}(A) \times \mathcal{P}(B)$ — how many elements does it have?
   - (c) Is $(A \times B) \subseteq (A \cup B) \times (A \cup B)$? Prove or disprove.

3. Prove: $\mathcal{P}(A) \cap \mathcal{P}(B) = \mathcal{P}(A \cap B)$ for all sets $A, B$.
   *(Contrast with Example 6 from Thursday's lecture, where $\mathcal{P}(A) \cup \mathcal{P}(B) \neq \mathcal{P}(A \cup B)$ in general.)*

4. In a survey of 100 people: 60 like coffee, 50 like tea, 30 like both. How many like neither?

5. Prove by induction on $n$: for a finite set $A$ with $|A| = n$, the number of subsets of $A$ with an **even** number of elements equals the number of subsets with an **odd** number of elements (for $n \geq 1$). *(Hint: this equals $2^{n-1}$ each — connect to the binomial theorem, which we revisit in Week 7.)*

6. A universal set has 200 elements. $|A| = 80$, $|B| = 70$, $|A \cap B| = 30$. Compute $|\overline{A} \cap \overline{B}|$.
   *(Hint: use De Morgan's Law — $\overline{A}\cap\overline{B} = \overline{A\cup B}$.)*

---

*Week 4 complete. Week 5: Functions — Injective, Surjective, Bijective; Composition and Inverses.*

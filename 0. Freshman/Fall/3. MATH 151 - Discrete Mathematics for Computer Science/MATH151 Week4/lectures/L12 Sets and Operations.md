# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 4.1 (L12) — Sets and Set Operations
### Monday, Week 4

**Date:** Monday 19 October 2026 · 13:00–13:50 · Week 4

---

> **Core Question:** What is a set, precisely, and how do we combine sets to build new ones?

---

## 1. What Is a Set?

**Definition (informal).** A **set** is an unordered collection of distinct objects, called **elements** or **members**.

This is Georg Cantor's original (1874) informal definition. It is intuitive but, as Russell's Paradox shows, not fully rigorous — a fully rigorous treatment requires axiomatic set theory (ZFC), which is beyond this course. For our purposes, the informal, "naive" definition suffices for everything we do.

**Notation:**
- $x \in A$ — "x is an element of A" / "x is a member of A" / "x belongs to A"
- $x \notin A$ — "x is not an element of A"

**Key properties of sets:**
1. **Unordered:** $\{1, 2, 3\} = \{3, 1, 2\}$ — order does not matter.
2. **No duplicates:** $\{1, 1, 2\} = \{1, 2\}$ — a set either contains an element or it doesn't; there is no notion of "twice."
3. **Extensionality:** Two sets are equal if and only if they have exactly the same elements. $A = B \iff \forall x (x \in A \leftrightarrow x \in B)$.

**Contrast with related structures (do not confuse):**

| Structure | Ordered? | Duplicates allowed? |
|---|---|---|
| Set $\{1,2,3\}$ | No | No |
| Multiset $\{1,1,2\}$ | No | Yes |
| Tuple/sequence $(1,2,3)$ | Yes | Yes |
| List (CS) | Yes | Yes |

---

## 2. Describing Sets

### Roster Method (Explicit Listing)

$$A = \{1, 2, 3, 4, 5\}$$

For infinite sets, use ellipsis with clear pattern:
$$\mathbb{N} = \{0, 1, 2, 3, \ldots\}, \qquad E = \{\ldots, -4, -2, 0, 2, 4, \ldots\}$$

### Set-Builder Notation

$$A = \{x \in D : P(x)\}$$

Read: "the set of all x in domain D such that P(x) holds."

**Examples:**

$$\{x \in \mathbb{Z} : x^2 < 10\} = \{-3, -2, -1, 0, 1, 2, 3\}$$

$$\{x \in \mathbb{R} : x^2 = 4\} = \{-2, 2\}$$

$$\{2n : n \in \mathbb{Z}\} = \text{the set of even integers}$$

**The connection to predicate logic (Week 1):** Set-builder notation is literally predicate logic in disguise. $x \in \{y \in D : P(y)\}$ is defined to mean exactly $x \in D \land P(x)$. Every set operation we define this week can be — and will be — defined in terms of the logical connectives from Week 0.

---

## 3. Standard Number Sets

| Symbol | Name | Description |
|---|---|---|
| $\emptyset$ or $\{\}$ | Empty set | Contains no elements |
| $\mathbb{N}$ | Natural numbers | $\{0, 1, 2, 3, \ldots\}$ |
| $\mathbb{Z}$ | Integers | $\{\ldots, -2,-1,0,1,2,\ldots\}$ |
| $\mathbb{Z}^+$ | Positive integers | $\{1,2,3,\ldots\}$ |
| $\mathbb{Q}$ | Rational numbers | $\{p/q : p,q\in\mathbb{Z}, q\neq0\}$ |
| $\mathbb{R}$ | Real numbers | |
| $\mathbb{C}$ | Complex numbers | |

**The empty set is unique.** There is only one set with no elements — by extensionality, any two "empty" sets are equal, since they trivially have the same (empty) collection of elements.

---

## 4. Subsets

**Definition.** $A$ is a **subset** of $B$, written $A \subseteq B$, if every element of $A$ is also an element of $B$:
$$A \subseteq B \iff \forall x (x \in A \rightarrow x \in B)$$

**Definition.** $A$ is a **proper subset** of $B$, written $A \subsetneq B$ (or $A \subset B$ in some texts), if $A \subseteq B$ and $A \neq B$.

**Key facts:**
- $\emptyset \subseteq A$ for every set $A$ (vacuously true — there is no element of $\emptyset$ to violate the condition).
- $A \subseteq A$ for every set $A$ (reflexivity).
- If $A \subseteq B$ and $B \subseteq C$, then $A \subseteq C$ (transitivity).

**Proving set equality via double inclusion:**

$$A = B \iff (A \subseteq B) \land (B \subseteq A)$$

This is one of the two standard techniques for proving two sets are equal (the other being element-chasing, covered Thursday).

---

## 5. The Power Set (Preview — full treatment Friday)

**Definition.** The **power set** of $A$, denoted $\mathcal{P}(A)$, is the set of all subsets of $A$:
$$\mathcal{P}(A) = \{S : S \subseteq A\}$$

**Example:** If $A = \{1, 2\}$, then $\mathcal{P}(A) = \{\emptyset, \{1\}, \{2\}, \{1,2\}\}$.

Note: $\emptyset \in \mathcal{P}(A)$ and $A \in \mathcal{P}(A)$ always.

---

## 6. Set Operations

Let $A$ and $B$ be sets, both subsets of some universal set $U$ (the "universe of discourse" for the sets under discussion).

### Union

$$A \cup B = \{x : x \in A \lor x \in B\}$$

Every element in $A$, in $B$, or in both.

### Intersection

$$A \cap B = \{x : x \in A \land x \in B\}$$

Only elements in both $A$ and $B$.

**Definition.** $A$ and $B$ are **disjoint** if $A \cap B = \emptyset$.

### Set Difference

$$A - B = A \setminus B = \{x : x \in A \land x \notin B\}$$

Elements in $A$ but not in $B$. (Note: $A - B \neq B - A$ in general — set difference is NOT commutative.)

### Complement

$$\overline{A} = A^c = \{x \in U : x \notin A\} = U - A$$

Everything in the universal set $U$ that is not in $A$. The complement depends on the choice of $U$ — always specify or infer $U$ from context.

### Symmetric Difference

$$A \oplus B = (A - B) \cup (B - A) = (A \cup B) - (A \cap B)$$

Elements in exactly one of $A$ or $B$, but not both. (Named for its parallel to XOR in logic.)

---

## 7. Worked Examples

Let $U = \{1,2,\ldots,10\}$, $A = \{1,2,3,4,5\}$, $B = \{4,5,6,7,8\}$.

| Operation | Result |
|---|---|
| $A \cup B$ | $\{1,2,3,4,5,6,7,8\}$ |
| $A \cap B$ | $\{4,5\}$ |
| $A - B$ | $\{1,2,3\}$ |
| $B - A$ | $\{6,7,8\}$ |
| $\overline{A}$ | $\{6,7,8,9,10\}$ |
| $\overline{B}$ | $\{1,2,3,9,10\}$ |
| $A \oplus B$ | $\{1,2,3,6,7,8\}$ |

**Verify:** $A \oplus B = (A-B) \cup (B-A) = \{1,2,3\} \cup \{6,7,8\} = \{1,2,3,6,7,8\}$. ✓

---

## 8. Set Operations and Logical Connectives — The Direct Correspondence

Every set operation corresponds exactly to a logical connective, applied to membership predicates. This is not an analogy — it is a definitional identity.

| Set Operation | Membership Condition | Logical Connective |
|---|---|---|
| $A \cup B$ | $x \in A \lor x \in B$ | Disjunction |
| $A \cap B$ | $x \in A \land x \in B$ | Conjunction |
| $\overline{A}$ | $x \notin A$ | Negation |
| $A - B$ | $x \in A \land x \notin B$ | Conjunction + Negation |
| $A \subseteq B$ | $\forall x (x \in A \rightarrow x \in B)$ | Universal + Conditional |
| $A = B$ | $\forall x (x \in A \leftrightarrow x \in B)$ | Universal + Biconditional |

**This correspondence is why the set-theoretic laws you'll prove Thursday are structurally identical to the propositional logic laws from Week 0** — De Morgan's Laws, Distributivity, Associativity, Commutativity, Idempotence all carry over exactly, with $\cup \leftrightarrow \lor$, $\cap \leftrightarrow \land$, complement $\leftrightarrow \neg$.

---

## 9. Cardinality (Finite Sets)

**Definition.** For a finite set $A$, the **cardinality** $|A|$ is the number of elements in $A$.

**Basic facts:**
- $|\emptyset| = 0$
- If $A$ and $B$ are disjoint (finite) sets, $|A \cup B| = |A| + |B|$.
- In general (not necessarily disjoint): $|A \cup B| = |A| + |B| - |A \cap B|$ (this is Inclusion-Exclusion for two sets — full treatment Friday).
- $|A - B| = |A| - |A \cap B|$

**Worked example:** With $A, B$ from Section 7: $|A|=5$, $|B|=5$, $|A\cap B|=2$.
$$|A \cup B| = 5 + 5 - 2 = 8$$
Verify against the roster: $\{1,2,3,4,5,6,7,8\}$ has 8 elements. ✓

---

## 10. Sets in Computer Science — Direct Applications

**Hash sets:** A `set` in Python, `HashSet` in Java, `unordered_set` in C++ — all directly implement the mathematical set abstraction: unordered, no duplicates, O(1) average membership testing via hashing.

```python
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7, 8}

print(A | B)   # union: {1,2,3,4,5,6,7,8}
print(A & B)   # intersection: {4,5}
print(A - B)   # difference: {1,2,3}
print(A ^ B)   # symmetric difference: {1,2,3,6,7,8}
print(A <= B)  # subset test: False
```

Python's set operators `|`, `&`, `-`, `^` are exactly $\cup$, $\cap$, $-$, $\oplus$.

**Databases:** SQL's `UNION`, `INTERSECT`, `EXCEPT` are set operations on relations (which are themselves sets of tuples — see Week 5).

**Type systems:** In some type theories, a type is modeled as the set of values that satisfy it. Union types (`int | string`) correspond to set union; intersection types correspond to set intersection.

---

## 11. Summary

```
Set operations:
  A ∪ B = {x : x∈A ∨ x∈B}         (union)
  A ∩ B = {x : x∈A ∧ x∈B}         (intersection)
  A − B = {x : x∈A ∧ x∉B}         (difference)
  A̅ = {x∈U : x∉A}                 (complement)
  A ⊕ B = (A−B) ∪ (B−A)           (symmetric difference)

Relations:
  A ⊆ B ⟺ ∀x (x∈A → x∈B)         (subset)
  A = B ⟺ ∀x (x∈A ↔ x∈B)         (equality)

Cardinality:
  |A ∪ B| = |A| + |B| − |A ∩ B|
```

---

## 12. End-of-Lecture Exercises

Let $U = \{1,2,\ldots,12\}$, $A = \{1,2,3,4,5,6\}$, $B = \{2,4,6,8,10,12\}$, $C = \{3,6,9,12\}$.

1. Compute:
   - (a) $A \cup B$
   - (b) $A \cap C$
   - (c) $B - C$
   - (d) $\overline{A \cap C}$
   - (e) $A \oplus C$
   - (f) $(A \cup B) \cap C$

2. Write each set using set-builder notation:
   - (a) The set of all integers whose square is less than 50.
   - (b) The set of all real numbers strictly between 0 and 1.
   - (c) The set of all even perfect squares.

3. Determine if each statement is true or false. If false, provide a counterexample:
   - (a) $A - B = B - A$ for all sets $A, B$.
   - (b) $A \cap \emptyset = \emptyset$ for all sets $A$.
   - (c) If $A \subseteq B$, then $A \cup B = B$.
   - (d) $A \oplus A = \emptyset$ for all sets $A$.

4. Compute $|A \cup B \cup C|$ using the given sets, first by direct enumeration, then verify using $|A|+|B|+|C|-|A\cap B|-|A\cap C|-|B\cap C|+|A\cap B\cap C|$.

5. Prove: $A \subseteq B$ if and only if $A \cap B = A$.

---

*Next: Lecture 4.2 — Set Identities and Proof Techniques*

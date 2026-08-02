# MATH 151 · Set Notation Reference
## Week 4: Sets, Operations, Power Sets, Products

---

## Basic Notation

| Symbol | Meaning |
|---|---|
| $x \in A$ | x is an element of A |
| $x \notin A$ | x is not an element of A |
| $\{a, b, c\}$ | roster notation |
| $\{x \in D : P(x)\}$ | set-builder notation |
| $\emptyset$ or $\{\}$ | empty set |
| $|A|$ | cardinality of A (number of elements) |
| $A \subseteq B$ | A is a subset of B |
| $A \subsetneq B$ | A is a proper subset of B |
| $A = B$ | set equality (same elements) |

---

## Standard Number Sets

| Symbol | Set |
|---|---|
| $\mathbb{N}$ | $\{0,1,2,3,\ldots\}$ |
| $\mathbb{Z}$ | $\{\ldots,-2,-1,0,1,2,\ldots\}$ |
| $\mathbb{Z}^+$ | $\{1,2,3,\ldots\}$ |
| $\mathbb{Q}$ | rationals |
| $\mathbb{R}$ | reals |
| $\mathbb{C}$ | complex numbers |

---

## Operations

| Operation | Notation | Membership |
|---|---|---|
| Union | $A \cup B$ | $x\in A \lor x\in B$ |
| Intersection | $A \cap B$ | $x\in A \land x\in B$ |
| Difference | $A - B$ (or $A\setminus B$) | $x\in A \land x\notin B$ |
| Complement | $\overline{A}$ (or $A^c$) | $x\in U \land x\notin A$ |
| Symmetric Difference | $A \oplus B$ | in exactly one of A, B |
| Power Set | $\mathcal{P}(A)$ | $S \subseteq A$ |
| Cartesian Product | $A \times B$ | ordered pairs $(a,b)$, $a\in A, b\in B$ |

---

## The Complete Identity Table

### Identity & Domination
$$A\cup\emptyset=A \qquad A\cap U=A \qquad A\cup U=U \qquad A\cap\emptyset=\emptyset$$

### Idempotent
$$A\cup A=A \qquad A\cap A=A$$

### Complementation
$$A\cup\overline{A}=U \qquad A\cap\overline{A}=\emptyset \qquad \overline{\overline{A}}=A \qquad \overline{U}=\emptyset \qquad \overline{\emptyset}=U$$

### Commutative
$$A\cup B=B\cup A \qquad A\cap B=B\cap A$$

### Associative
$$(A\cup B)\cup C=A\cup(B\cup C) \qquad (A\cap B)\cap C=A\cap(B\cap C)$$

### Distributive
$$A\cup(B\cap C)=(A\cup B)\cap(A\cup C) \qquad A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$$

### De Morgan's ⭐
$$\overline{A\cup B}=\overline{A}\cap\overline{B} \qquad \overline{A\cap B}=\overline{A}\cup\overline{B}$$

### Absorption
$$A\cup(A\cap B)=A \qquad A\cap(A\cup B)=A$$

### Difference Identity (bridge law)
$$A-B = A\cap\overline{B}$$

---

## Cardinality Formulas

| Formula | Condition |
|---|---|
| $|\emptyset|=0$ | |
| $|A\cup B|=|A|+|B|-|A\cap B|$ | two sets |
| $|A\cup B\cup C|=|A|+|B|+|C|-|A\cap B|-|A\cap C|-|B\cap C|+|A\cap B\cap C|$ | three sets |
| $|A-B|=|A|-|A\cap B|$ | |
| $|\mathcal{P}(A)|=2^{|A|}$ | finite A |
| $|A\times B|=|A|\cdot|B|$ | finite A, B |

---

## Proof Strategy Quick Reference

| Goal | Method |
|---|---|
| $A=B$ | Element-chase with $\iff$; or algebraic law chain; or show $A\subseteq B$ and $B\subseteq A$ |
| $A\subseteq B$ | Let $x\in A$ arbitrary; derive $x\in B$ |
| $A\neq B$ | One counterexample: specific sets where they differ |
| $A\cap B=\emptyset$ | Assume $x\in A\cap B$, derive contradiction |

### Element-Chasing Template

```
Let x be an arbitrary element [of U].
x ∈ [LHS expression]
⟺ [unpack definition]
⟺ [apply logic law]
⟺ [unpack definition]
...
⟺ x ∈ [RHS expression]

Since x was arbitrary, LHS = RHS.
```

---

## Common False "Identities" (Know These Are FALSE)

| False Claim | Counterexample Needed |
|---|---|
| $A-(B-C)=(A-B)-C$ | Try $A=\{1,2,3\}, B=\{2\}, C=\{3\}$ |
| $\mathcal{P}(A)\cup\mathcal{P}(B)=\mathcal{P}(A\cup B)$ | Try $A=\{1\},B=\{2\}$ |
| $(A\cup B)\cap C=A\cup(B\cap C)$ | Try $A=\{1\},B=\{2\},C=\{1,3\}$ |
| $A-B=B-A$ | Any $A\neq B$ with both nonempty |
| $A\times B = B\times A$ | Any $A\neq B$ |

## True Identities That Look Suspicious (But Verify!)

| Claim | Status |
|---|---|
| $\mathcal{P}(A)\cap\mathcal{P}(B)=\mathcal{P}(A\cap B)$ | TRUE |
| $A\times(B\cup C)=(A\times B)\cup(A\times C)$ | TRUE |
| $A\times(B\cap C)=(A\times B)\cap(A\times C)$ | TRUE |
| $A\times(B-C)=(A\times B)-(A\times C)$ | TRUE |

---

## Symbols Summary Table

| Symbol | Read as |
|---|---|
| $\cup$ | union / "cup" |
| $\cap$ | intersection / "cap" |
| $-$ or $\setminus$ | set difference / "minus" |
| $\overline{A}$ | complement of A |
| $\oplus$ | symmetric difference |
| $\mathcal{P}$ | power set |
| $\times$ | Cartesian product |
| $\subseteq$ | subset (or equal) |
| $\subsetneq$ | proper subset |
| $\in$ | element of |
| $\notin$ | not an element of |

# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 6.1 (L18) Relations and Their Fundamental Properties
### Monday, Week 6

**Date:** Monday 2 November 2026 · 13:00–13:50 · Week 6

---

> **Core Question:** What is a relation, in full generality, and what structural properties can it possess?

---

## 1. The Definition of a Relation

**Definition.** A (binary) **relation** $R$ from set $A$ to set $B$ is a subset of $A\times B$:
$$R \subseteq A \times B$$

If $(a,b) \in R$, we write $a\mathrel{R}b$ (read "a is related to b").

**Special case:** A relation **on** a set $A$ (rather than "from A to B") is a relation from $A$ to $A$, i.e., $R \subseteq A\times A$.

**Contrast with functions (Week 5):** A function requires *totality* (every $a\in A$ has SOME image) and *well-definedness* (every $a\in A$ has a UNIQUE image). A relation has NEITHER requirement — an element may relate to zero, one, or many elements; and some elements may relate to nothing at all. **Every function is a relation, but most relations are not functions.**

---

## 2. Examples of Relations

**Example 1:** $A=\{1,2,3,4\}$. $R=\{(1,1),(1,2),(2,3),(3,3),(4,1)\}$ is a relation on $A$.

Note: $1$ relates to both $1$ and $2$, so $R$ is **not a function**. $2$ relates only to $3$.
Every element has at least one *outgoing* pair — though nothing in the definition requires that —
but **nothing relates to $4$**: no pair in $R$ has $4$ as its second component. A relation need
not be total in either direction.

**Example 2 (Divisibility):** On $\mathbb{Z}^+$: $R = \{(a,b) : a \mid b\}$. So $1\mathrel{R}n$ for all $n$; $2\mathrel{R}4$; but $3\mathrel{R}5$ is false ($3\nmid5$).

**Example 3 (Less than or equal):** On $\mathbb{R}$: $R=\{(a,b): a\leq b\}$.

**Example 4 (Congruence mod $n$):** On $\mathbb{Z}$: $R = \{(a,b) : n \mid (a-b)\}$, written $a\equiv b\pmod n$.

**Example 5 (Database relation):** A table `Employee(ID, Name, Dept)` is literally a relation — a subset of $\text{ID}\times\text{Name}\times\text{Dept}$ (a ternary relation, generalizing binary relations to $n$-ary — see Section 7).

---

## 3. Representing Relations

### As a Set of Ordered Pairs

$R = \{(1,1),(1,2),(2,3),(3,3),(4,1)\}$ (as above).

### As a Directed Graph (Digraph)

Draw a node for each element of $A$. Draw an arrow from $a$ to $b$ whenever $(a,b)\in R$. A self-loop represents $(a,a)\in R$.

This representation makes reflexivity (self-loops everywhere), symmetry (every arrow has a matching reverse arrow), and transitivity (shortcuts always exist) visually apparent — extremely useful for building intuition.

### As a Boolean Matrix

For $A=\{a_1,\ldots,a_n\}$, the relation matrix $M_R$ is the $n\times n$ matrix with:
$$M_R[i][j] = \begin{cases}1 & \text{if }(a_i,a_j)\in R\\0&\text{otherwise}\end{cases}$$

**Example:** $A=\{1,2,3,4\}$, $R=\{(1,1),(1,2),(2,3),(3,3),(4,1)\}$:

$$M_R = \begin{pmatrix}1&1&0&0\\0&0&1&0\\0&0&1&0\\1&0&0&0\end{pmatrix}$$

(Row $i$, column $j$ — reading row 1: 1 relates to 1 and 2.)

**Why this matters for CS:** The matrix representation is exactly how adjacency matrices work for graphs (CS 102). Boolean matrix operations (AND, OR) correspond directly to relation operations (intersection, union), and matrix multiplication (with Boolean AND/OR instead of arithmetic ×/+) computes relation composition (defined in Section 6).

---

## 4. The Four Fundamental Properties

Let $R$ be a relation on a set $A$ (i.e., $R\subseteq A\times A$).

### Reflexive

**Definition.** $R$ is **reflexive** if $\forall a\in A, (a,a)\in R$.

Every element relates to itself.

**Digraph test:** every node has a self-loop.

**Examples:** $\leq$ on $\mathbb{R}$ (yes, $a\leq a$). $=$ on any set (yes). $<$ on $\mathbb{R}$ (NO — $a<a$ is false). Divisibility on $\mathbb{Z}^+$ (yes, $a\mid a$).

### Symmetric

**Definition.** $R$ is **symmetric** if $\forall a,b\in A, (a,b)\in R \rightarrow (b,a)\in R$.

**Digraph test:** every arrow has a matching reverse arrow.

**Examples:** "is a sibling of" (yes — if $a$ is a sibling of $b$, then $b$ is a sibling of $a$). $=$ on any set (yes). $\leq$ on $\mathbb{R}$ (NO — $a\leq b$ does not imply $b\leq a$ unless $a=b$). Divisibility (NO — $2\mid4$ but $4\nmid2$).

### Antisymmetric

**Definition.** $R$ is **antisymmetric** if $\forall a,b\in A, [(a,b)\in R \land (b,a)\in R] \rightarrow a=b$.

**Careful — this is NOT "not symmetric."** Antisymmetric allows $(a,a)\in R$ freely (that doesn't violate anything, since $a=a$ trivially); it forbids having BOTH $(a,b)$ and $(b,a)$ for DISTINCT $a\neq b$.

**Digraph test:** no two distinct nodes have arrows going both ways between them (self-loops are fine).

**Examples:** $\leq$ on $\mathbb{R}$ (yes — if $a\leq b$ and $b\leq a$, then $a=b$). Divisibility on $\mathbb{Z}^+$ (yes — if $a\mid b$ and $b\mid a$ with $a,b>0$, then $a=b$). Equality (yes, vacuously — and also symmetric; equality is one of the few relations that is BOTH symmetric and antisymmetric). "is a sibling of" (NO — if $a,b$ distinct siblings, $(a,b)$ and $(b,a)$ both hold with $a\neq b$).

**Key insight:** Symmetric and antisymmetric are NOT opposites. A relation can be:
- Both symmetric and antisymmetric (e.g., $=$)
- Symmetric but not antisymmetric (e.g., "sibling of," with distinct siblings)
- Antisymmetric but not symmetric (e.g., $\leq$)
- Neither (e.g., a relation with some symmetric pairs and some asymmetric ones, mixed)

### Transitive

**Definition.** $R$ is **transitive** if $\forall a,b,c\in A, [(a,b)\in R \land (b,c)\in R] \rightarrow (a,c)\in R$.

**Digraph test:** whenever there's a path of length 2 ($a\to b\to c$), there's also a direct shortcut ($a\to c$).

**Examples:** $\leq$ on $\mathbb{R}$ (yes). Divisibility (yes — if $a\mid b$ and $b\mid c$, then $a\mid c$, proved in Week 2!). "is an ancestor of" (yes). "is a parent of" (NO — your parent's parent is your grandparent, not your parent).

---

## 5. Worked Examples — Full Property Analysis

### Example 1: Congruence mod $n$

**Relation.** $R = \{(a,b)\in\mathbb{Z}\times\mathbb{Z} : n\mid(a-b)\}$, i.e., $a\equiv b\pmod n$.

**Reflexive?** Need $n\mid(a-a)=0$. Since $n\mid0$ always, YES.

**Symmetric?** Assume $n\mid(a-b)$. Then $a-b=nk$ for some $k\in\mathbb{Z}$, so $b-a=-nk=n(-k)$. Since $-k\in\mathbb{Z}$, $n\mid(b-a)$. YES.

**Transitive?** Assume $n\mid(a-b)$ and $n\mid(b-c)$. Then $a-b=nk_1$, $b-c=nk_2$. Adding: $a-c=n(k_1+k_2)$. Since $k_1+k_2\in\mathbb{Z}$, $n\mid(a-c)$. YES.

**Conclusion:** Congruence mod $n$ is reflexive, symmetric, and transitive — an **equivalence relation** (formal definition Thursday).

### Example 2: Strict Less-Than

**Relation.** $R = \{(a,b)\in\mathbb{R}\times\mathbb{R} : a<b\}$.

**Reflexive?** Need $a<a$. FALSE for all $a$. NOT reflexive. (In fact, this relation is **irreflexive**: $\forall a, (a,a)\notin R$ — a stronger, opposite condition worth naming.)

**Symmetric?** If $a<b$, is $b<a$? NO (e.g., $1<2$ but $2\not<1$). NOT symmetric.

**Antisymmetric?** Vacuously — can $(a,b)\in R$ and $(b,a)\in R$ both hold? That would need $a<b$ and $b<a$ simultaneously, impossible. So the antisymmetric condition's hypothesis is never satisfied — the implication is vacuously TRUE. YES, antisymmetric (vacuously).

**Transitive?** If $a<b$ and $b<c$, is $a<c$? YES (standard order property).

**Conclusion:** Irreflexive, not symmetric, antisymmetric (vacuously), transitive. This is called a **strict partial order** (Friday's lecture).

### Example 3: A Relation on a Finite Set

**Relation.** $A=\{1,2,3\}$, $R=\{(1,1),(2,2),(3,3),(1,2),(2,1)\}$.

**Reflexive?** $(1,1),(2,2),(3,3)$ all present. YES.

**Symmetric?** $(1,2)\in R$ and $(2,1)\in R$ — matched. All self-loops trivially symmetric. YES.

**Antisymmetric?** We have BOTH $(1,2)$ and $(2,1)$ with $1\neq2$. This VIOLATES antisymmetry (the conclusion $1=2$ is false, but the hypothesis holds). NOT antisymmetric.

**Transitive?** Check all length-2 paths: $1\to2\to1$ requires $(1,1)\in R$ — yes, present. $2\to1\to2$ requires $(2,2)\in R$ — yes. Also need to check paths through self-loops, e.g., $1\to1\to2$ requires $(1,2)$ — yes, present. All combinations check out. YES, transitive.

**Conclusion:** Reflexive, symmetric, transitive (equivalence relation), NOT antisymmetric.

---

## 6. Composition of Relations

**Definition.** For relations $R\subseteq A\times B$ and $S\subseteq B\times C$, the **composition** $S\circ R \subseteq A\times C$ is defined by:
$$S\circ R = \{(a,c) : \exists b\in B, (a,b)\in R \land (b,c)\in S\}$$

**Note the ordering convention (same as function composition):** $S\circ R$ means "first $R$, then $S$" — read right to left, matching function composition notation.

**Example:** $A=\{1,2,3\}$, $R=\{(1,2),(2,3)\}$ (relation on $A$), $S=R$.

$S\circ R = R\circ R$: pairs $(a,c)$ such that $\exists b, (a,b)\in R\land(b,c)\in R$.

Check: $(1,2)\in R$ and $(2,3)\in R$ ⟹ $(1,3)\in R\circ R$.
No other chains exist (since $3$ has no outgoing pairs in $R$, and $1\to2$ is the only length-1 step from 1).

$R\circ R = \{(1,3)\}$.

**Connection to transitivity:** $R$ is transitive if and only if $R\circ R \subseteq R$ (every 2-step relationship is already captured directly). This gives an alternative, very useful test for transitivity, especially with matrix representations (Boolean matrix multiplication $M_R \cdot M_R$, entrywise OR'd with itself, compared to $M_R$).

---

## 7. n-ary Relations and Databases

**Definition.** An **n-ary relation** on sets $A_1,\ldots,A_n$ is a subset of $A_1\times A_2\times\cdots\times A_n$.

This is the exact formal model of a database table: each row is an $n$-tuple, and the table itself is a (finite) subset of the Cartesian product of the column domains.

```
Employee(ID, Name, Dept)
```
is a ternary relation ⊆ $\text{IDs}\times\text{Names}\times\text{Depts}$.

**SQL operations as relation operations:**
- `SELECT` with a `WHERE` clause: picks a sub-relation satisfying a predicate (exactly $\{x\in R : P(x)\}$, set-builder notation from Week 4).
- `UNION`, `INTERSECT`: literal set union/intersection of relations (requires matching arity/types — "union-compatible" relations).
- `JOIN`: a generalization of relation composition, combining tuples across relations that share compatible attributes.

This is why the field is literally called the "relational model" of databases (Codd, 1970) — the mathematical object underlying every SQL table is precisely the relation of Week 4/Week 6.

---

## 8. Summary

```
Relation R ⊆ A×B (or A×A "on A")

Properties (for R on A):
  Reflexive:      ∀a, (a,a)∈R
  Symmetric:      ∀a,b, (a,b)∈R → (b,a)∈R
  Antisymmetric:  ∀a,b, (a,b)∈R ∧ (b,a)∈R → a=b
  Transitive:     ∀a,b,c, (a,b)∈R ∧ (b,c)∈R → (a,c)∈R

Representations: set of pairs | digraph | Boolean matrix

Composition: S∘R = {(a,c) : ∃b, (a,b)∈R ∧ (b,c)∈S}
Transitivity test: R transitive ⟺ R∘R ⊆ R
```

---

## 9. End-of-Lecture Exercises

For each relation, determine which of reflexive/symmetric/antisymmetric/transitive hold. Prove or give a specific counterexample for each property.

1. $R=\{(a,b)\in\mathbb{Z}\times\mathbb{Z} : a+b \text{ is even}\}$

2. $R=\{(a,b)\in\mathbb{Z}^+\times\mathbb{Z}^+ : a\mid b\}$ (divisibility)

3. $A=\{1,2,3,4\}$, $R=\{(1,1),(2,2),(3,3),(4,4),(1,2),(2,3),(1,3)\}$

4. $R=\{(A,B) : A,B\in\mathcal{P}(\{1,2,3\}), A\subseteq B\}$ (subset relation)

5. $R=\{(a,b)\in\mathbb{R}\times\mathbb{R} : |a-b|<1\}$

6. Compute $R\circ R$ for $R=\{(1,2),(2,3),(3,4)\}$ on $\{1,2,3,4\}$. Is $R$ transitive? Verify using the $R\circ R\subseteq R$ test.

7. Represent the relation from Exercise 3 as a Boolean matrix. Verify transitivity via matrix inspection.

---

*Next: Lecture 6.2 — Equivalence Relations and Equivalence Classes*

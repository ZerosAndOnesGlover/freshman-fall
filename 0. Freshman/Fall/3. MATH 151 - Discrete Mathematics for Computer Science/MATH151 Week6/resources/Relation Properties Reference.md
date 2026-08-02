# MATH 151 — Relation Properties Reference
## Week 6: Relations, Equivalence Relations, Partial Orders

---

## Core Definitions

| Term | Definition |
|---|---|
| Relation $R$ from $A$ to $B$ | $R\subseteq A\times B$ |
| Relation on $A$ | $R\subseteq A\times A$ |
| $a\mathrel{R}b$ | $(a,b)\in R$ |

---

## The Four Fundamental Properties

| Property | Formal Definition | Digraph Test |
|---|---|---|
| Reflexive | $\forall a\in A,\ (a,a)\in R$ | Every node has a self-loop |
| Symmetric | $\forall a,b,\ (a,b)\in R\to(b,a)\in R$ | Every arrow has a matching reverse |
| Antisymmetric | $\forall a,b,\ (a,b)\in R\land(b,a)\in R\to a=b$ | No two-way arrows between distinct nodes |
| Transitive | $\forall a,b,c,\ (a,b)\in R\land(b,c)\in R\to(a,c)\in R$ | Every 2-step path has a direct shortcut |

**Irreflexive** (opposite of reflexive, not just "not reflexive"): $\forall a, (a,a)\notin R$.

**Symmetric vs Antisymmetric — NOT opposites:**

| | Symmetric | Not Symmetric |
|---|---|---|
| **Antisymmetric** | $R=\{(a,a):a\in A\}$ (equality-like) | $\leq$ on $\mathbb{R}$ |
| **Not Antisymmetric** | "sibling of" | Mixed relations |

---

## Proof Templates

### Proving Reflexive
```
Let a∈A be arbitrary. [Show (a,a)∈R using the definition of R.]
Since a arbitrary, R is reflexive. ∎
```

### Proving Symmetric
```
Let a,b∈A with (a,b)∈R. [Derive (b,a)∈R using algebra/definition.]
Since a,b arbitrary, R is symmetric. ∎
```

### Proving Antisymmetric
```
Let a,b∈A with (a,b)∈R and (b,a)∈R. [Derive a=b.]
Since a,b arbitrary, R is antisymmetric. ∎
```

### Proving Transitive
```
Let a,b,c∈A with (a,b)∈R and (b,c)∈R. [Derive (a,c)∈R.]
Since a,b,c arbitrary, R is transitive. ∎
```

### Disproof Template (any property)
```
Counterexample: take a=[value], b=[value] [,c=[value] if needed].
[Show hypothesis of the property holds but conclusion fails.]
So R is NOT [property]. ∎
```

---

## Equivalence Relations

**Definition:** Reflexive + Symmetric + Transitive.

**Equivalence class:** $[a] = \{x\in A : x\sim a\}$

### Key Facts (memorize)

| Fact | Statement |
|---|---|
| Self-membership | $a\in[a]$ always |
| Class equality | $[a]=[b] \iff a\sim b$ |
| Disjoint-or-identical | $[a]\cap[b]\neq\emptyset \Rightarrow [a]=[b]$ |
| Covering | $\bigcup_{a\in A}[a] = A$ |

### The Fundamental Theorem

$$\{\text{Equivalence relations on }A\} \quad\longleftrightarrow\quad \{\text{Partitions of }A\}$$

Forward: equivalence classes of $\sim$ form a partition.
Backward: given a partition $\{A_i\}$, define $a\sim b \iff$ same part.

### Proof Template — Equivalence Relation

```
Claim: ~ is an equivalence relation on A.

Reflexive: Let a∈A. [Show a~a.]
Symmetric: Assume a~b. [Derive b~a.]
Transitive: Assume a~b and b~c. [Derive a~c.]

Since all three hold, ~ is an equivalence relation. ∎
```

---

## Partial Orders

**Definition:** Reflexive + Antisymmetric + Transitive.

**Total order:** partial order where $\forall a,b,\ a\preceq b \lor b\preceq a$.

### Poset Vocabulary

| Term | Definition |
|---|---|
| Comparable | $a\preceq b$ or $b\preceq a$ |
| Incomparable | Neither holds |
| Chain | Subset where every pair is comparable |
| Antichain | Subset where no two distinct elements are comparable |
| Covers ($a\lessdot b$) | $a\prec b$ and no $c$ with $a\prec c\prec b$ |
| Maximal | No element strictly above (may be multiple) |
| Minimal | No element strictly below (may be multiple) |
| Maximum | Dominates ALL elements (unique if exists) |
| Minimum | Dominated by ALL elements (unique if exists) |

### Hasse Diagram Rules

1. Node per element.
2. Edge (no arrow) between $a,b$ iff $b$ covers $a$; draw $b$ above $a$.
3. No self-loops (reflexivity implied).
4. No non-covering edges (transitivity implied).

---

## Quick Classification Table

| Relation | Domain | Refl | Symm | Antisymm | Trans | Category |
|---|---|---|---|---|---|---|
| $=$ | any set | Y | Y | Y | Y | Equiv. (trivial) |
| $\leq$ | $\mathbb{R}$ | Y | N | Y | Y | Total order |
| $<$ | $\mathbb{R}$ | N | N | Y* | Y | Strict order |
| $\mid$ (divides) | $\mathbb{Z}^+$ | Y | N | Y | Y | Partial order |
| $\equiv\pmod n$ | $\mathbb{Z}$ | Y | Y | N | Y | Equivalence |
| $\subseteq$ | $\mathcal{P}(S)$ | Y | N | Y | Y | Partial order |
| "sibling of" | people | N** | Y | N | N*** | Neither |
| $\neq$ | any set (|A|>1) | N | Y | N | N | Neither |

\* vacuously antisymmetric (hypothesis never satisfiable for distinct a,b since a<b and b<a can't both hold)
\** not reflexive — no one is their own sibling
\*** not transitive in the usual definition (excludes self)

---

## Composition of Relations

$$S\circ R = \{(a,c) : \exists b,\ (a,b)\in R \land (b,c)\in S\}$$

**Transitivity test:** $R$ transitive $\iff R\circ R \subseteq R$.

---

## Common Errors

| Error | Correction |
|---|---|
| Treating symmetric/antisymmetric as opposites | They are independent properties |
| Antisymmetric = "not symmetric" | Antisymmetric only restricts DISTINCT element pairs |
| Assuming reflexive+symmetric ⟹ equivalence | Must ALSO verify transitivity separately |
| Confusing maximal with maximum | Maximal: nothing above IT specifically. Maximum: above EVERYTHING |
| Drawing all edges in a Hasse diagram | Only draw COVERING relations |
| Assuming every poset is total | Most interesting posets (divisibility, subset) are NOT total |

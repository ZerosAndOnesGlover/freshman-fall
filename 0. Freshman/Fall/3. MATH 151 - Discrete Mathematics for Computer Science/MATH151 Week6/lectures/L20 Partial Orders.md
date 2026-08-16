# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 6.3 (L20) Partial Orders and Hasse Diagrams
### Friday, Week 6

**Date:** Friday 2 October 2026 · 13:00–13:50 · Week 6

---

> **Core Question:** What structure does a relation need to have to capture a meaningful notion of "ordering," and what happens when not everything can be compared?

---

## 1. The Definition

**Definition.** A relation $R$ on a set $A$ is a **partial order** if it is reflexive, antisymmetric, AND transitive.

We typically write $\preceq$ for a general partial order (evoking $\leq$), and call $(A,\preceq)$ a **partially ordered set**, or **poset**.

**Why "partial"?** Unlike the familiar ordering of real numbers, a partial order does NOT require that every pair of elements be comparable. Some pairs may simply have no relationship at all in either direction.

---

## 2. Motivating Examples

### Example 1: The Divisibility Order

On $\mathbb{Z}^+$: $a\preceq b \iff a\mid b$.

**Reflexive:** $a\mid a$. ✓
**Antisymmetric:** if $a\mid b$ and $b\mid a$ (both positive), then $a=b$. ✓ (proved in Week 2's divisibility work)
**Transitive:** if $a\mid b$ and $b\mid c$, then $a\mid c$. ✓ (Week 2!)

Partial order. ✓

**Not total:** Consider $a=4$, $b=6$. Neither $4\mid6$ nor $6\mid4$. These elements are **incomparable** — the divisibility order does not rank every pair.

### Example 2: The Subset Order

On $\mathcal{P}(S)$ for any set $S$: $A\preceq B \iff A\subseteq B$.

**Reflexive:** $A\subseteq A$. ✓
**Antisymmetric:** $A\subseteq B$ and $B\subseteq A$ implies $A=B$ (Week 4, double inclusion). ✓
**Transitive:** $A\subseteq B$ and $B\subseteq C$ implies $A\subseteq C$ (Week 4). ✓

Partial order. ✓

**Not total (for $|S|\geq2$):** $\{1\}$ and $\{2\}$ are incomparable subsets of $\{1,2,3\}$ — neither is a subset of the other.

### Example 3: The Usual Order on Reals

On $\mathbb{R}$: $a\preceq b \iff a\leq b$.

Reflexive ✓, antisymmetric ✓, transitive ✓. Partial order.

**This one IS total:** for any $a,b\in\mathbb{R}$, either $a\leq b$ or $b\leq a$ (or both, if equal). Every pair is comparable.

---

## 3. Total Orders

**Definition.** A partial order $\preceq$ on $A$ is a **total order** (or **linear order**) if every pair of elements is comparable:
$$\forall a,b\in A, \quad a\preceq b \lor b\preceq a$$

Every total order is a partial order; not every partial order is total (Examples 1 and 2 above are partial but not total).

**In CS:** Sorting algorithms rely on a total order over the elements being sorted (e.g., `<=` on numbers, lexicographic order on strings). If your comparison relation is only a *partial* order, standard sorting doesn't directly apply — you instead need topological sort (Section 6).

---

## 4. Comparability and the Structure of a Poset

**Definition.** In a poset $(A,\preceq)$, elements $a,b$ are **comparable** if $a\preceq b$ or $b\preceq a$. Otherwise they are **incomparable**.

**Definition.** A subset $C\subseteq A$ is a **chain** if every pair of elements in $C$ is comparable (i.e., $C$ is totally ordered under $\preceq$).

**Definition.** A subset $I\subseteq A$ is an **antichain** if no two distinct elements of $I$ are comparable.

**Example:** In $(\mathcal{P}(\{1,2,3\}), \subseteq)$:
- $\{\emptyset,\{1\},\{1,2\},\{1,2,3\}\}$ is a chain (each is a subset of the next).
- $\{\{1\},\{2\},\{3\}\}$ is an antichain (no two are subsets of each other).

---

## 5. Hasse Diagrams

A **Hasse diagram** is a simplified visual representation of a finite poset, showing only the "covering" relationships (direct order relationships, with redundant/implied edges removed), drawn with higher elements above lower ones.

**Definition.** In a poset $(A,\preceq)$, $b$ **covers** $a$ (written $a\lessdot b$) if $a\preceq b$, $a\neq b$, and there is no $c\in A$ with $a\prec c\prec b$ (no element strictly between them).

**Construction rules for a Hasse diagram:**
1. Draw a node for each element of $A$.
2. Draw an edge (line, no arrowhead) between $a$ and $b$ whenever $b$ covers $a$, placing $b$ physically above $a$.
3. Do NOT draw edges for non-covering relations (they are implied by transitivity — following lines upward gives you the full order).
4. Do NOT draw self-loops (reflexivity is implied).
5. Do NOT draw arrowheads (the "upward" convention encodes direction).

### Worked Example: Divisors of 12

$A = \{1,2,3,4,6,12\}$ (positive divisors of 12), ordered by divisibility.

**Covering relations:**
- $1\lessdot2$ (nothing between 1 and 2 in divisibility)
- $1\lessdot3$
- $2\lessdot4$
- $2\lessdot6$
- $3\lessdot6$
- $4\lessdot12$
- $6\lessdot12$

**Not a covering relation:** $1\lessdot4$? NO — $2$ is strictly between ($1\mid2\mid4$), so this is implied by $1\lessdot2\lessdot4$, not drawn directly.

```
          12
         /  \
        4    6
        |   / \
        |  /   \
        2       3
         \     /
          \   /
            1
```

Covering pairs: $1\lessdot2$, $1\lessdot3$, $2\lessdot4$, $2\lessdot6$, $3\lessdot6$,
$4\lessdot12$, $6\lessdot12$. Note $6$ covers **both** $2$ and $3$, which is why two edges descend
from it; and no edge is drawn from $1$ to $4$, because $1<2<4$ makes that relation implied by
transitivity rather than a covering.

Cleaner layout:
```
          12
         /  \
        4    6
        |   /|
        2  / 3
         \/ /
         1
```

(Textual Hasse diagrams are imprecise — in lecture, this is drawn on the board; the key structure is: 1 at the bottom connects up to 2 and 3; 2 connects up to 4 and 6; 3 connects up to 6; both 4 and 6 connect up to 12.)

---

## 6. Maximal, Minimal, Maximum, Minimum Elements

**Definition.** In a poset $(A,\preceq)$:
- $a$ is **maximal** if there is no $b\in A$ with $a\prec b$ (nothing is strictly above it).
- $a$ is **minimal** if there is no $b\in A$ with $b\prec a$ (nothing is strictly below it).
- $a$ is the **maximum** (greatest element) if $b\preceq a$ for ALL $b\in A$.
- $a$ is the **minimum** (least element) if $a\preceq b$ for ALL $b\in A$.

**Key distinction:** A poset can have MULTIPLE maximal elements (if they're incomparable to each other), but at most ONE maximum element (since the maximum must be comparable to, and above, everything — including other maximal elements, forcing uniqueness).

**Example:** In $(\{2,3,4,6\}, \mid)$ (divisibility): 4 and 6 are both maximal (nothing in the set is divisible by either), but there is no maximum (since 4 and 6 are incomparable — neither divides the other, so neither dominates the whole set).

**Example (from Section 5):** In the divisors-of-12 poset, 12 is both the maximum AND the unique maximal element. 1 is both minimum and unique minimal.

---

## 7. Topological Sort — Extending a Partial Order to a Total Order

**Problem.** Given a partial order (or more generally, a Directed Acyclic Graph, DAG) on a finite set, find a total order (a linear sequencing) that is *consistent* with the partial order — i.e., if $a\preceq b$ in the partial order, then $a$ comes before $b$ in the total order.

**Theorem.** Every finite poset can be extended to a total order (topological sort always succeeds on a finite poset / DAG).

**Algorithm (informal):**
1. Find a minimal element (one with no predecessors remaining).
2. Place it next in the output sequence.
3. Remove it from the poset.
4. Repeat until empty.

**Why this always works:** A finite poset always has at least one minimal element (otherwise, you could construct an infinite descending chain $a_1 \succ a_2 \succ a_3 \succ\cdots$, which is impossible in a finite set — this is essentially the Well-Ordering Principle in disguise, from Week 3!).

### Worked Example: Course Prerequisites

Consider courses with prerequisite relation ($a\preceq b$ means "$a$ is a prerequisite of $b$," so $a$ must come first):

$$\text{MATH151} \preceq \text{CS102}, \quad \text{CS101} \preceq \text{CS102}, \quad \text{CS101}\preceq\text{PROG101}$$

This is a partial order (CS102 and PROG101 are incomparable — no prerequisite relationship between them).

A valid topological sort (total order consistent with the partial order): MATH151, CS101, PROG101, CS102 — or equally valid: CS101, MATH151, CS102, PROG101 — multiple valid total orders can extend the same partial order, since incomparable elements (like PROG101 and CS102, or MATH151 and CS101) can be placed in either relative order.

**In CS:** Topological sort is a fundamental graph algorithm (CS 102) used for: task scheduling with dependencies, build systems (Makefiles — which files must be compiled before others), package manager dependency resolution, and course scheduling exactly as above.

---

## 8. Lattices (Brief Preview)

**Definition.** A poset $(A,\preceq)$ is a **lattice** if every pair of elements $a,b$ has both:
- a **least upper bound** (join, $a\lor b$) — the smallest element that is $\succeq$ both $a$ and $b$
- a **greatest lower bound** (meet, $a\land b$) — the largest element that is $\preceq$ both $a$ and $b$

**Example:** $(\mathcal{P}(S),\subseteq)$ is a lattice: $A\lor B = A\cup B$, $A\land B = A\cap B$.

**Example:** $(\mathbb{Z}^+, \mid)$ is a lattice: $a\lor b = \text{lcm}(a,b)$, $a\land b=\gcd(a,b)$.

Lattices are studied more deeply in advanced algebra and are foundational in program analysis (abstract interpretation, CS 412) and in the semantics of type systems (subtyping lattices).

---

## 9. Summary — Comparing Relation Types

| Property Set | Name | Example |
|---|---|---|
| Reflexive + Symmetric + Transitive | Equivalence Relation | Congruence mod $n$ |
| Reflexive + Antisymmetric + Transitive | Partial Order | Divisibility, subset |
| Partial Order + all pairs comparable | Total Order | $\leq$ on $\mathbb{R}$ |
| Irreflexive + Antisymmetric(vacuous) + Transitive | Strict Partial Order | $<$ on $\mathbb{R}$, $\subsetneq$ |

```
Poset (A, ⪯): reflexive + antisymmetric + transitive

Total order: poset where every pair is comparable

Hasse Diagram: covering relations only, drawn bottom-to-top

Maximal/Minimal: no element strictly above/below (may be multiple)
Maximum/Minimum: comparable to and dominates/is dominated by EVERYTHING (unique if exists)

Topological Sort: extends any finite poset to a compatible total order
```

---

## 10. End-of-Lecture Exercises

1. Determine whether each relation is a partial order. If yes, is it total?
   - (a) On $\mathbb{Z}$: $a\preceq b \iff a\leq b$
   - (b) On $\mathcal{P}(\{1,2,3,4\})$: $A\preceq B \iff A\subseteq B$
   - (c) On $\mathbb{Z}^+$: $a\preceq b \iff a\mid b$
   - (d) On $\{(x,y) : x,y\in\mathbb{R}\}$: $(x_1,y_1)\preceq(x_2,y_2) \iff x_1\leq x_2 \land y_1\leq y_2$ (the "product order")

2. Draw (describe in words, or on paper) the Hasse diagram for $(\mathcal{P}(\{a,b,c\}),\subseteq)$.

3. For the divisibility poset on $\{1,2,3,4,5,6,7,8,9,10\}$:
   - (a) List all covering relations.
   - (b) Identify all maximal elements.
   - (c) Is there a maximum element? Justify.
   - (d) Find a chain of length 4 (4 elements, all pairwise comparable).
   - (e) Find an antichain of size 4.

4. Perform a topological sort on the poset with covering relations: $a\lessdot c$, $b\lessdot c$, $c\lessdot d$, $b\lessdot e$. List all valid topological orderings.

5. Prove: in any finite poset, every chain and every antichain has size at most $|A|$ (trivial), but more importantly — prove that if $(A,\preceq)$ has NO chain of length $>k$, and you want to prove something about antichains... *(This references Dilworth's theorem territory — just prove the following simpler fact instead)*: prove that a finite poset with $n$ elements and no antichain of size $>1$ (i.e., every pair comparable) must be a total order, and conclude it has exactly one maximum and one minimum element.

---

*Week 6 complete. Week 7: Counting — Permutations, Combinations, the Multiplication and Addition Rules.*

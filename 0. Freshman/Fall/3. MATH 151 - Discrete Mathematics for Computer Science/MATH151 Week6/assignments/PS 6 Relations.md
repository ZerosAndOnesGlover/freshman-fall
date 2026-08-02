# MATH 151 — Discrete Mathematics for Computer Science
## Problem Set 6 — Relations
### Released: Friday, Week 6 | Due: Friday, Week 7 (11:59 PM)

---

**Instructions:**
- For each of the four properties (reflexive, symmetric, antisymmetric, transitive), give a direct proof if the property holds, or a specific counterexample if it fails.
- When proving a relation is an equivalence relation, verify all three properties explicitly — do not skip any.
- Show all work.
- Submit as a single PDF.

**Scoring:** 100 points total.

---

## Part A — Relation Properties (24 points)

**A1.** (6 pts each) For each relation, determine whether it is reflexive, symmetric, antisymmetric, and/or transitive. Prove each property that holds; give a specific counterexample for each that fails.

**(a)** On $\mathbb{Z}$: $R = \{(a,b) : a \geq b\}$

**(b)** On $\mathbb{Z}^+$: $R = \{(a,b) : \gcd(a,b) = 1\}$ (a and b are coprime)

**(c)** $A=\{1,2,3,4,5\}$, $R = \{(1,1),(2,2),(3,3),(4,4),(5,5),(1,2),(2,1),(3,4)\}$

**(d)** On $\mathcal{P}(\{1,2,3\})$: $R = \{(A,B) : A\cap B \neq \emptyset\}$

---

## Part B — Equivalence Relations (28 points)

**B1.** (7 pts each) Prove that each relation is an equivalence relation (verify ALL three properties explicitly), then describe the equivalence classes.

**(a)** On $\mathbb{Z}$: $a\sim b \iff a \equiv b \pmod 4$

**(b)** On $\mathbb{R}\times\mathbb{R}$ (excluding the origin from consideration for well-definedness — assume points $\neq(0,0)$): $(x_1,y_1)\sim(x_2,y_2) \iff x_1^2+y_1^2 = x_2^2+y_2^2$ (same distance from origin)

**(c)** On the set of all finite strings over $\{a,b\}$: $s\sim t \iff s$ and $t$ have the same number of $a$'s.

**(d)** On $\mathbb{Z}\times\mathbb{Z}^+$ (pairs $(a,b)$ with $b>0$, representing fractions $a/b$): $(a,b)\sim(c,d) \iff ad=bc$.
*(This is the rational number construction from Thursday's lecture — write out the full proof.)*

---

**B2.** (4 pts) For the relation in B1(a), list the 4 equivalence classes explicitly (using set-builder or roster notation with a clear pattern), and give 3 representative elements of each.

---

## Part C — The Fundamental Theorem (16 points)

**C1.** (8 pts) Let $A = \{1,2,3,4,5,6,7,8\}$ and consider the partition $\{\{1,4,7\},\{2,5\},\{3,6,8\}\}$.

- (a) Write out the corresponding equivalence relation explicitly as a set of ordered pairs.
- (b) Verify (by spot-checking at least 3 pairs) that this relation is reflexive, symmetric, and transitive.

---

**C2.** (8 pts) Prove: if $\sim$ is an equivalence relation on $A$, then for all $a, b \in A$: $a\sim b \iff [a]=[b]$.

*(This is a biconditional — prove both directions explicitly.)*

---

## Part D — Partial Orders and Hasse Diagrams (24 points)

**D1.** (6 pts each) Determine whether each relation is a partial order. If yes, determine whether it is a total order. Prove each property or give a counterexample.

**(a)** On $\mathcal{P}(\{1,2,3,4\})$: $A\preceq B \iff A\subseteq B$

**(b)** On $\mathbb{Z}^+$: $a\preceq b \iff a\mid b$

**(c)** On pairs $\mathbb{Z}\times\mathbb{Z}$: $(a,b)\preceq(c,d) \iff a\leq c$ (ignore the second coordinate entirely)

**(d)** On strings over $\{a,b,\ldots,z\}$: the standard lexicographic (dictionary) order.

---

**D2.** (Included in D1 point total — no separate points, but REQUIRED as part of this section) For the divisibility poset on $A=\{1,2,3,4,5,6,7,8,9,10,11,12\}$:

- (a) List all covering relations.
- (b) Identify all maximal elements and all minimal elements.
- (c) Does a maximum element exist? A minimum element? Justify each.
- (d) Find the longest chain in this poset. State its length.
- (e) Find an antichain of size 5.

---

## Part E — Composition and Topological Sort (8 points)

**E1.** (4 pts) Let $R = \{(1,2),(2,3),(3,1)\}$ on $A=\{1,2,3\}$. Compute $R\circ R$ and $R\circ R\circ R$. Is $R$ transitive? Justify using the $R\circ R\subseteq R$ test from Monday's lecture.

---

**E2.** (4 pts) A build system has the following file dependencies (must-compile-before relation, i.e., $a\preceq b$ means "$a$ must be compiled before $b$"):

$$\text{utils} \preceq \text{parser}, \quad \text{utils}\preceq\text{lexer}, \quad \text{lexer}\preceq\text{compiler}, \quad \text{parser}\preceq\text{compiler}$$

Find ALL valid topological sorts (complete build orders) consistent with this partial order.

---

## Bonus (8 points — optional)

**Bonus 1.** (4 pts) Prove: the relation "is isomorphic to" on the set of all finite simple graphs is an equivalence relation. (You may assume the standard definition: $G_1$ is isomorphic to $G_2$ if there is a bijection between their vertex sets that preserves adjacency.) Only prove the three defining properties — you do not need to construct explicit isomorphisms for arbitrary graphs, just argue the relation's properties abstractly using composition/inversion of bijections.

**Bonus 2.** (4 pts) A relation $R$ on $A$ is called a **strict partial order** if it is irreflexive ($\forall a, (a,a)\notin R$) and transitive. Prove: every strict partial order is automatically antisymmetric (in the vacuous sense described in Friday's Example 2), and prove that if $R$ is a strict partial order, then $R\cup\{(a,a):a\in A\}$ (adding all self-loops) is a genuine partial order (reflexive, antisymmetric, transitive).

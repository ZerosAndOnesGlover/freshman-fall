# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 6 — Relations
### Released: Friday 6 November 2026, 14:00 (after the Friday lecture) | Due: Friday 13 November 2026, 17:00 (Week 7)

---

**Instructions:**
- For each of the four properties (reflexive, symmetric, antisymmetric, transitive), give a direct proof if the property holds, or a specific counterexample if it fails.
- When proving a relation is an equivalence relation, verify all three properties explicitly — do not skip any.
- Show all work.
- Submit as a single PDF.

**Expected time:** about 3 hours. **Scoring:** 100 points total.

---

## Part A — Relation Properties (18 points)

**A1.** (6 pts each) For each relation, determine whether it is reflexive, symmetric, antisymmetric, and/or transitive. Prove each property that holds; give a specific counterexample for each that fails.

**(a)** On $\mathbb{Z}$: $R = \{(a,b) : a \geq b\}$

**(b)** $A=\{1,2,3,4,5\}$, $R = \{(1,1),(2,2),(3,3),(4,4),(5,5),(1,2),(2,1),(3,4)\}$

**(c)** On $\mathcal{P}(\{1,2,3\})$: $R = \{(A,B) : A\cap B \neq \emptyset\}$

---

## Part B — Equivalence Relations (20 points)

**B1.** (10 pts each) Prove that each relation is an equivalence relation (verify ALL three properties explicitly), then describe the equivalence classes.

**(a)** On $\mathbb{R}\times\mathbb{R}$ (excluding the origin from consideration for well-definedness — assume points $\neq(0,0)$): $(x_1,y_1)\sim(x_2,y_2) \iff x_1^2+y_1^2 = x_2^2+y_2^2$ (same distance from origin)

**(b)** On the set of all finite strings over $\{a,b\}$: $s\sim t \iff s$ and $t$ have the same number of $a$'s.

---

## Part C — The Fundamental Theorem (26 points)

**C1.** (12 pts) Let $A = \{1,2,3,4,5,6,7,8\}$ and consider the partition $\{\{1,4,7\},\{2,5\},\{3,6,8\}\}$.

- (a) Write out the corresponding equivalence relation explicitly as a set of ordered pairs.
- (b) Verify (by spot-checking at least 3 pairs) that this relation is reflexive, symmetric, and transitive.

---

**C2.** (14 pts) Prove: if $\sim$ is an equivalence relation on $A$, then for all $a, b \in A$: $a\sim b \iff [a]=[b]$.

*(This is a biconditional — prove both directions explicitly.)*

---

## Part D — Partial Orders (18 points)

**D1.** (6 pts each) Determine whether each relation is a partial order. If yes, determine whether it is a total order. Prove each property or give a counterexample.

**(a)** On $\mathbb{Z}^+$: $a\preceq b \iff a\mid b$

**(b)** On pairs $\mathbb{Z}\times\mathbb{Z}$: $(a,b)\preceq(c,d) \iff a\leq c$ (ignore the second coordinate entirely)

**(c)** On strings over $\{a,b,\ldots,z\}$: the standard lexicographic (dictionary) order.

---

## Part E — Composition and Topological Sort (18 points)

**E1.** (10 pts) Let $R = \{(1,2),(2,3),(3,1)\}$ on $A=\{1,2,3\}$. Compute $R\circ R$ and $R\circ R\circ R$. Is $R$ transitive? Justify using the $R\circ R\subseteq R$ test from Monday's lecture.

---

**E2.** (8 pts) A build system has the following file dependencies (must-compile-before relation, i.e., $a\preceq b$ means "$a$ must be compiled before $b$"):

$$\text{utils} \preceq \text{parser}, \quad \text{utils}\preceq\text{lexer}, \quad \text{lexer}\preceq\text{compiler}, \quad \text{parser}\preceq\text{compiler}$$

Find ALL valid topological sorts (complete build orders) consistent with this partial order.

# MATH 151 · Discrete Mathematics for Computer Science
## Quiz 7 — Scope Preview
### Quiz administered: Monday 9 November 2026, 13:00–13:15 (first 15 minutes of lecture) · Week 7

---

**Coverage:** Week 6 material only:
- Week 6: Relations — reflexive/symmetric/antisymmetric/transitive, equivalence relations, partial orders

*(Week 7 material is not on this quiz — it is taught after the quiz.)*

---

## What You Must Know Cold for Week 6 Material

### 1. The Four Properties — Definitions

| Property | Formal Definition |
|---|---|
| Reflexive | $\forall a, (a,a)\in R$ |
| Symmetric | $\forall a,b,\ (a,b)\in R\to(b,a)\in R$ |
| Antisymmetric | $\forall a,b,\ (a,b)\in R\land(b,a)\in R\to a=b$ |
| Transitive | $\forall a,b,c,\ (a,b)\in R\land(b,c)\in R\to(a,c)\in R$ |

**Critical:** symmetric and antisymmetric are NOT opposites — a relation can be both, neither, or just one.

### 2. Equivalence Relations

- Reflexive + Symmetric + Transitive
- Equivalence class: $[a]=\{x\in A:x\sim a\}$
- **Fundamental Theorem:** equivalence relations ↔ partitions (know both directions of this correspondence)
- Key facts: $a\in[a]$ always; $[a]=[b]\iff a\sim b$; classes are disjoint or identical, never partially overlapping

### 3. Partial Orders

- Reflexive + Antisymmetric + Transitive
- Total order: partial order where every pair is comparable
- Hasse diagram: covering relations only, drawn bottom-to-top, no self-loops, no arrowheads
- Maximal (nothing strictly above) vs Maximum (dominates everything) — a poset can have multiple maximal elements but at most one maximum
- Topological sort: always possible for finite posets

### 4. Common Examples to Recognize Instantly

| Relation | Reflexive | Symmetric | Antisymmetric | Transitive | Type |
|---|---|---|---|---|---|
| $=$ | Y | Y | Y | Y | Equiv. + trivial order |
| $\leq$ on $\mathbb{R}$ | Y | N | Y | Y | Total order |
| $<$ on $\mathbb{R}$ | N | N | Y (vacuous) | Y | Strict order |
| $\mid$ on $\mathbb{Z}^+$ | Y | N | Y | Y | Partial order (not total) |
| $\equiv\pmod n$ | Y | Y | N | Y | Equivalence |
| $\subseteq$ | Y | N | Y | Y | Partial order (not total) |

---

## Sample Quiz 7 Problems (Week 6 portion)

**Problem 1.** (5 pts) Determine all four properties for a given relation on a small finite set; prove or give counterexamples.

**Problem 2.** (5 pts) Prove a given relation is an equivalence relation; list its equivalence classes.

**Problem 3.** (4 pts) Given a partition, write the corresponding equivalence relation.

**Problem 4.** (4 pts) Determine if a relation is a partial order; if so, is it total? Draw or describe a small Hasse diagram.

**Problem 5.** (4 pts) From Week 7 — counting problem (see Week 7 materials).

---

## Study Recommendations

1. **Build a personal example bank.** For each property combination (reflexive+symmetric+transitive, reflexive+antisymmetric+transitive, etc.), have one memorized example ready.

2. **Practice the antisymmetric definition carefully.** This is the most commonly misunderstood property — remember it does NOT forbid $(a,a)$, only forbids DISTINCT $a\neq b$ with both $(a,b)$ and $(b,a)$.

3. **Drill equivalence class computation.** Given a relation, be able to quickly list out several equivalence classes.

4. **Practice the partition-to-relation direction.** Given a partition, write out the relation — this is the converse direction of the Fundamental Theorem and is tested separately from the forward direction.

5. **Practice drawing small Hasse diagrams** for divisibility and subset posets — know how to identify covering relations (no intermediate element) versus implied relations.

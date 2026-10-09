# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 19 (L19) — Equivalence Relations and Equivalence Classes
### Thursday, Week 6

*“A mathematician, like a painter or a poet, is a maker of patterns. If his patterns are more permanent than theirs, it is because they are made with ideas.”* — G. H. Hardy, *A Mathematician's Apology* (1940)

**Date:** Thursday 5 November 2026 · 13:00–13:50 · Week 6

**Reading:** Rosen, 8e §9.5 · Epp, 5e §8.3 *(details at the end of the lecture)*

**Coursework:** 📘 **Midterm 1** Fri 6 Nov 18:00–19:15 · 📝 **PS 5** due Fri 6 Nov 17:00 · 📝 **PS 6** released Fri 6 Nov 14:00, due Fri 13 Nov 17:00 · 📊 **Quiz 7** Mon 9 Nov 13:00–13:15 · 🔬 **Lab 6** Wed 11 Nov 15:00–16:50

---

> **Core Question:** What does it mean for a relation to capture a genuine notion of "sameness," and what structure does this impose on a set?

---

## 1. The Definition

**Definition.** A relation $R$ on a set $A$ is an **equivalence relation** if it is reflexive, symmetric, AND transitive.

This is the formal generalization of "equality" — an equivalence relation captures any notion of two objects being "the same" *with respect to some criterion*, even when they are not literally identical.

**Notation:** For an equivalence relation, we often write $a\sim b$ instead of $(a,b)\in R$.

---

## 2. Motivating Examples

### Example 1: Equality Itself

$R = \{(a,a) : a\in A\}$ — the most basic equivalence relation. Reflexive ✓, symmetric ✓ (vacuously, since only $a=b$ pairs exist), transitive ✓. Every set has this "trivial" equivalence relation.

### Example 2: Congruence mod $n$

Proved Monday: reflexive, symmetric, transitive. This is THE canonical example of a non-trivial equivalence relation, and underlies all of modular arithmetic (Week 12).

### Example 3: "Same Parity"

$R = \{(a,b)\in\mathbb{Z}\times\mathbb{Z} : a-b \text{ is even}\}$, i.e., $a$ and $b$ have the same parity.

**Reflexive:** $a-a=0$ is even. ✓
**Symmetric:** if $a-b$ even, then $b-a=-(a-b)$ is also even. ✓
**Transitive:** if $a-b$ even and $b-c$ even, then $(a-b)+(b-c)=a-c$ is even (sum of two evens). ✓

Equivalence relation. ✓ (This is exactly congruence mod 2.)

### Example 4: "Same Length" (Strings)

On the set of all strings: $R = \{(s,t) : |s|=|t|\}$ (same length).

Reflexive ✓, symmetric ✓, transitive ✓. Equivalence relation.

### Example 5: A Relation That Fails to Be an Equivalence Relation

$R = \{(a,b)\in\mathbb{Z}\times\mathbb{Z} : |a-b|\leq 1\}$ ("close in value").

**Reflexive:** $|a-a|=0\leq1$. ✓
**Symmetric:** $|a-b|=|b-a|$. ✓
**Transitive:** Take $a=1,b=2,c=3$. $|1-2|=1\leq1$ ✓ and $|2-3|=1\leq1$ ✓, but $|1-3|=2\not\leq1$. FAILS transitivity.

NOT an equivalence relation — despite being reflexive and symmetric, the failure of transitivity disqualifies it. **This is the most common student error: assuming reflexive+symmetric is enough. All three properties are required.**

---

## 3. Equivalence Classes

**Definition.** Given an equivalence relation $\sim$ on $A$, the **equivalence class** of an element $a\in A$ is:
$$[a] = \{x\in A : x\sim a\}$$

The equivalence class of $a$ is the set of everything "equivalent to" $a$.

### Worked Example: Congruence mod 3

On $\mathbb{Z}$, with $a\sim b \iff 3\mid(a-b)$:

$$[0] = \{\ldots,-6,-3,0,3,6,9,\ldots\}$$
$$[1] = \{\ldots,-5,-2,1,4,7,10,\ldots\}$$
$$[2] = \{\ldots,-4,-1,2,5,8,11,\ldots\}$$

Note: $[0]=[3]=[6]=[-3]=\cdots$ — the class doesn't care which representative you pick, ALL of these describe the exact same set.

### Worked Example: Same Parity

$[0] = $ all even integers. $[1] = $ all odd integers. Only two distinct classes exist.

---

## 4. The Fundamental Theorem of Equivalence Relations

This is the central result of the lecture — it reveals *why* equivalence relations matter so much: they are exactly the same thing as **partitions**.

**Definition.** A **partition** of a set $A$ is a collection of nonempty subsets $\{A_1, A_2, \ldots\}$ (possibly infinite in number) such that:
1. $A_i \cap A_j = \emptyset$ for $i\neq j$ (pairwise disjoint)
2. $\bigcup_i A_i = A$ (their union is everything)

Every element of $A$ belongs to exactly one $A_i$.

**Theorem (Fundamental Theorem of Equivalence Relations).** Let $\sim$ be an equivalence relation on $A$. Then the set of equivalence classes $\{[a] : a\in A\}$ forms a partition of $A$. Conversely, every partition of $A$ arises this way from some equivalence relation.

**Proof (equivalence relation ⟹ partition).**

*Nonempty:* For any $a\in A$, $a\in[a]$ (since $a\sim a$ by reflexivity). So every class is nonempty.

*Covers all of A:* Every $a\in A$ is in $[a]$, so $\bigcup_{a\in A}[a] = A$.

*Pairwise disjoint (or identical):* We show: if $[a]\cap[b]\neq\emptyset$, then $[a]=[b]$.

Suppose $[a]\cap[b]\neq\emptyset$. Let $c\in[a]\cap[b]$, so $c\sim a$ and $c\sim b$.

By symmetry, $a\sim c$. By transitivity (with $a\sim c$ and $c\sim b$): $a\sim b$.

Now show $[a]\subseteq[b]$: let $x\in[a]$, so $x\sim a$. Since $a\sim b$, by transitivity $x\sim b$, so $x\in[b]$.

By a symmetric argument (swapping roles of $a,b$), $[b]\subseteq[a]$.

Therefore $[a]=[b]$.

**Conclusion:** any two equivalence classes are either identical or disjoint — never partially overlapping. Combined with nonemptiness and covering all of $A$, the classes form a partition. ∎

**Proof (partition ⟹ equivalence relation) — sketch.** Given a partition $\{A_i\}$, define $a\sim b \iff a,b$ belong to the same part $A_i$. Reflexivity, symmetry, transitivity all follow immediately from "belonging to the same part" being reflexive/symmetric/transitive as a relation. (Left as an exercise.)

**This theorem is arguably the single most important structural fact in this course.** It says: *studying equivalence relations and studying partitions are literally the same activity, viewed from two different angles.* Whenever you want to partition a set into meaningful groups, define the right equivalence relation; whenever you have an equivalence relation, you automatically get a partition for free.

---

## 5. Worked Examples of the Correspondence

### Example: Congruence mod $n$ ↔ Partition into Residue Classes

The equivalence relation "$\equiv\pmod n$" on $\mathbb{Z}$ partitions $\mathbb{Z}$ into exactly $n$ classes: $[0],[1],\ldots,[n-1]$. This partition is denoted $\mathbb{Z}/n\mathbb{Z}$ or $\mathbb{Z}_n$ — the set of **residue classes** mod $n$, which becomes the foundation of modular arithmetic (Week 12) and is directly used in cryptographic algorithms (RSA, Week 8/CS 341).

### Example: Same Remainder When Divided by a Fixed Set

**Rational numbers as equivalence classes:** A rational number is *formally defined* as an equivalence class of pairs of integers! Define on $\mathbb{Z}\times(\mathbb{Z}-\{0\})$ the relation $(p,q)\sim(r,s) \iff ps=qr$. This is an equivalence relation:
**reflexive** — $(p,q)\sim(p,q)$ requires $pq=qp$, true by commutativity;
**symmetric** — $ps=qr$ rearranges directly to $rq=sp$;
**transitive** — if $ps=qr$ and $ru=st$ then $pu=qt$ follows by eliminating $r$ (legitimate because
$s\neq0$). The equivalence class $[(1,2)] = [(2,4)] = [(3,6)] = \cdots$ IS the rational number $1/2$ — "$1/2$" and "$2/4$" are different REPRESENTATIVES of the SAME equivalence class. This is precisely why $1/2=2/4$: they're literally the same equivalence class, just written with different representative pairs.

---

## 6. Choosing Representatives

Since all elements of an equivalence class are "the same" with respect to $\sim$, we often pick one **representative** from each class to work with.

**Example:** For congruence mod $n$, the standard representatives are $\{0,1,\ldots,n-1\}$ — every integer is congruent to exactly one of these.

**In CS:** Choosing canonical representatives is a common technique. Example: normalizing file paths (`./a/../b` and `b` might be equivalent — same target — and we pick a canonical form). Example: hash-consing in compilers (structurally equal expressions get mapped to the same canonical representative to save memory and enable fast equality checks via pointer comparison).

---

## 7. Proving a Relation Is an Equivalence Relation — Full Worked Proof

**Theorem.** Define $R$ on $\mathbb{Z}\times\mathbb{Z}$ (pairs of integers, thought of as fractions with the second coordinate possibly zero excluded — assume $q,s\neq0$ here) by $(p,q)\sim(r,s) \iff ps=qr$. Then $\sim$ is an equivalence relation on $\mathbb{Z}\times(\mathbb{Z}-\{0\})$.

**Proof.**

**Reflexive:** $(p,q)\sim(p,q)$ requires $pq=qp$, which holds by commutativity of multiplication in $\mathbb{Z}$. ✓

**Symmetric:** Assume $(p,q)\sim(r,s)$, i.e., $ps=qr$. We show $(r,s)\sim(p,q)$, i.e., $rq=sp$.

From $ps=qr$: rearranging (commutativity), $sp=rq$, which is exactly $rq=sp$. ✓

**Transitive:** Assume $(p,q)\sim(r,s)$ and $(r,s)\sim(t,u)$, i.e., $ps=qr$ and $ru=st$. We show $(p,q)\sim(t,u)$, i.e., $pu=qt$.

From $ps=qr$: $p = qr/s$ (assuming $s\neq0$, valid since $s$ is a "denominator").
From $ru=st$: $r = st/u$ (assuming $u\neq0$).

Substituting: $p = q(st/u)/s = qt/u$, so $pu=qt$ (multiplying both sides by $u$).

*(A cleaner algebraic path avoiding division: from $ps=qr$ and $ru=st$, multiply the first by $u$: $psu=qru$. Substitute $ru=st$: $psu=q(st)=qst$. Since $s\neq0$, divide both sides by $s$: $pu=qt$.)* ✓

Since all three properties hold, $\sim$ is an equivalence relation. ∎

**This is exactly the construction of the rational numbers** — the equivalence classes of $\sim$ are precisely the rational numbers, with $(p,q)$ representing the fraction $p/q$.

---

## 8. Equivalence Relations in Computer Science

**Type equivalence:** In type systems, two types can be considered "equivalent" (interchangeable) via an equivalence relation on types — e.g., structural equivalence in some languages considers `{x: int, y: int}` and `{y: int, x: int}` as the same type.

**Graph isomorphism:** Two graphs are equivalent if there's a structure-preserving bijection between them — this defines an equivalence relation on the set of all graphs, partitioning graphs into isomorphism classes (CS 301 studies the complexity of testing this).

**State equivalence in automata (CS 301):** Two states in a finite automaton are equivalent if they lead to identical accept/reject behavior for all future inputs — minimizing a DFA is exactly computing the partition into equivalence classes and merging each class into a single state.

**Database normalization:** Functional dependencies define equivalence-like partitions over tuples, driving normal form design (CS 321).

**Union-Find / Disjoint Set data structure (CS 102):** This data structure directly implements equivalence classes computationally — `union(a,b)` merges the classes containing $a$ and $b$; `find(a)` returns a canonical representative of $a$'s class. It is the workhorse data structure for Kruskal's MST algorithm and many other applications requiring dynamic equivalence-class tracking.

---

## 9. Summary

```
Equivalence Relation: reflexive + symmetric + transitive

Equivalence Class: [a] = {x∈A : x~a}

Fundamental Theorem:
  Equivalence relations on A  ⟺  Partitions of A
  
  Key facts about equivalence classes:
    - a ∈ [a] always (nonempty)
    - [a] = [b]  ⟺  a~b
    - [a] ∩ [b] ≠ ∅  ⟹  [a] = [b]  (classes are disjoint or identical)
    - ⋃[a] = A  (classes cover everything)
```

---

## 10. End-of-Lecture Exercises

1. Determine whether each relation is an equivalence relation. If yes, describe the equivalence classes. If no, identify which property fails with a specific counterexample.
   - (a) On $\mathbb{Z}$: $a\sim b \iff a^2=b^2$
   - (b) On $\mathbb{R}$: $a\sim b \iff a-b\in\mathbb{Q}$ (differ by a rational)
   - (c) On the set of all functions $f:\mathbb{R}\to\mathbb{R}$: $f\sim g \iff f(0)=g(0)$
   - (d) On $\mathbb{Z}^+$: $a\sim b \iff \gcd(a,b)>1$

2. Prove that "same remainder when divided by 5" is an equivalence relation on $\mathbb{Z}$. List all 5 equivalence classes and give 3 representative elements of each.

3. Let $A=\{1,2,3,4,5,6\}$ and consider the partition $\{\{1,2\},\{3,4,5\},\{6\}\}$. Write out the equivalence relation (as a set of ordered pairs) that corresponds to this partition, using the Fundamental Theorem's converse construction.

4. Prove: if $\sim$ is an equivalence relation on $A$, then for all $a,b\in A$: $a\sim b$ if and only if $[a]=[b]$. *(This was used implicitly in the Fundamental Theorem's proof — write it out explicitly as a standalone biconditional proof.)*

5. On the set of all triangles in the plane, define $T_1\sim T_2 \iff T_1$ is similar to $T_2$ (same shape, possibly different size). Argue informally that this is an equivalence relation, and describe what an equivalence class looks like.

---

## Reading

- **Rosen, 8e §9.5** — Equivalence relations
- **Epp, 5e §8.3** — Equivalence relations

*Next: Lecture 20 — Partial Orders and Hasse Diagrams*

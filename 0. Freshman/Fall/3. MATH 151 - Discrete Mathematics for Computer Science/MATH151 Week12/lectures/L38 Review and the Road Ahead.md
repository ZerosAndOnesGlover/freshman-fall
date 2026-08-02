# MATH 151 — Discrete Mathematics for Computer Science
## Lecture 12.3 (L38) — Review and the Road Ahead
### Friday, Week 12

---

## 1. What This Course Was Actually About

Thirty-nine lectures across five apparently unrelated areas: logic, proof, sets and functions,
counting, and graphs. They were not unrelated.

**The course taught one thing: how to establish that something is true.** Every technique was a way
of discharging that obligation for a different kind of claim.

| To show… | Use |
|---|---|
| A statement holds for all $n$ | **Induction** (Week 3) |
| A statement is false | A **counterexample** (Week 2) |
| Something must exist | **Pigeonhole** (Week 8) |
| Exactly how many there are | **Counting** and **inclusion–exclusion** (Weeks 7–8) |
| Two sets are the same size | A **bijection** (Week 5) |
| Two structures are the same | An **isomorphism** (Week 10) |
| Two structures differ | An **invariant** (Week 10) |
| An algorithm terminates | A decreasing quantity — Euclid, Week 12 |
| A closed form is right | **Verification against iteration** (Week 9) |

Notice how many of these are about **not** being fooled. A counterexample defeats a plausible claim;
an invariant defeats a plausible isomorphism; verifying a closed form defeats a plausible derivation.

---

## 2. The Threads That Ran Through Everything

### Equivalence relations

Week 6 defined them. Then: congruence mod $n$ partitions $\mathbb{Z}$ into residue classes
(Week 12), isomorphism partitions graphs into isomorphism classes (Week 10), and "same cardinality"
partitions sets by size (Week 5). **Every time you have said "these are the same for our purposes",
you have used an equivalence relation.**

### Bijections

Week 5's tool for equal size became: counting by bijection (Week 7), the definition of cardinality
and Cantor's diagonal argument (Week 5), and graph isomorphism (Week 10).

### Induction

Week 3's proof technique became recursive definitions (Week 9), the existence half of unique
factorisation (Week 12), and the proof that a tree has $n-1$ edges (Week 11).

### Inclusion–exclusion

Week 8's counting method reappears in Week 12 as Euler's totient
$\varphi(n)=n\prod_{p\mid n}(1-1/p)$ — the same alternating sum, over prime divisors.

### Easy versus hard

The theme that most deserves your attention:

| Easy | Hard |
|---|---|
| Euler circuit — count degrees | Hamilton cycle — NP-complete |
| Minimum spanning tree — greedy works | Travelling salesman — NP-hard |
| Multiplying primes | Factoring the product |
| Shortest path | Longest path |
| Proving a collision exists (subset-sum) | Finding it |

**Superficially similar problems can differ enormously in difficulty**, and the difference is
structural — the cut property, degree parity, locality. Not effort, not cleverness. Recognising which
side of that line a problem sits on is the most valuable judgement this course can give you.

---

## 3. Exam-Critical Facts

### Logic and proof
- Quantifier order matters: $\forall x\exists y$ is not $\exists y\forall x$
- $\neg(\forall x\,P) \equiv \exists x\,\neg P$
- Contrapositive $\neg q\to\neg p$ is equivalent to $p\to q$; the converse is not

### Sets and functions
- $\lvert\mathcal{P}(A)\rvert = 2^{\lvert A\rvert}$
- Injective, surjective, bijective; on **finite sets of equal size** injective ⟺ surjective
- $\mathbb{Q}$ is countable, $\mathbb{R}$ is not

### Counting
- $P(n,r)=\frac{n!}{(n-r)!}$, $\binom nr=\frac{n!}{r!(n-r)!}$
- $\binom nk=\binom n{n-k}$; $\sum_k\binom nk = 2^n$
- Pigeonhole: $\lceil n/m\rceil$; **name the pigeons and the pigeonholes**
- Inclusion–exclusion: intersections use **lcm**; complement for "at least one"
- $D_n = n!\sum(-1)^k/k!$; $D_1..D_6 = 0,1,2,9,44,265$; $D_n/n!\to1/e$

### Recurrences
- Distinct roots $Ar_1^n+Br_2^n$; **double root $(A+Bn)r^n$**
- Non-homogeneous: fit the particular first
- Binet: $F_n=(\varphi^n-\psi^n)/\sqrt5$

### Graphs and trees
- $\sum\deg = 2\lvert E\rvert$; odd-degree vertices come in pairs
- $K_n$: $\binom n2$ edges; $Q_n$: $2^n$ vertices, $n2^{n-1}$ edges
- Bipartite ⟺ no odd cycle
- Tree: $n-1$ edges, unique paths, every edge a bridge
- Cayley: $n^{n-2}$
- Kruskal and Prim always agree on **total**, not necessarily on edge set
- BFS gives shortest paths — **unweighted only**

### Number theory
- Division algorithm: $0\le r<d$, so $-7\bmod3=2$
- $\gcd\cdot\operatorname{lcm}=ab$
- Inverse mod $m$ exists ⟺ $\gcd(a,m)=1$
- $\varphi(pq)=(p-1)(q-1)$
- RSA correctness **is** Euler's theorem

---

## 4. The Five Most Common Exam Errors

1. **Pigeonhole without checking $n>m$.** Week 8's trap question and Quiz 9's Q5(a) both punished
   this. **Verify pigeons exceed pigeonholes before invoking the principle.**

2. **Forgetting the repeated-root case.** $Ar^n+Br^n$ collapses to one constant. Use $(A+Bn)r^n$.

3. **Using the product instead of the lcm** for an intersection in inclusion–exclusion. It works only
   when the divisors are coprime, which is why students get away with it until they do not.

4. **Claiming isomorphism from a matching degree sequence.** $C_6$ and two triangles. Every year.

5. **Asserting a closed form without checking it.** Three iterated values takes thirty seconds and
   catches nearly every sign error.

---

## 5. Where Each Thread Continues

| This course | Continues in |
|---|---|
| Induction, recurrences | **CS 102** — divide-and-conquer analysis, dynamic programming |
| Graphs, trees, BFS/DFS | **CS 102** — Dijkstra, network flow, algorithm design |
| Counting, generating functions | **MATH 251** — probability and expectation |
| Number theory, RSA | **CS 340** — cryptography and security |
| Logic, satisfiability | **CS 301** — computability and complexity; NP-completeness |
| Relations, closures | **CS 320** — databases; relational algebra |
| Set theory, cardinality | **CS 301** — undecidability by diagonalisation |

**Weeks 8 and 10 pointed repeatedly at NP-completeness without defining it.** CS 301 supplies the
definition, and you will find you already know half a dozen of its examples.

---

## 6. A Closing Thought

Week 5 proved that almost every function $\mathbb{N}\to\{0,1\}$ is uncomputable — by counting.
Programs are countable; those functions are not; therefore most functions have no program. The
argument fits in a paragraph and rules out infinitely many things you might have hoped to write.

**That is what discrete mathematics offers computer science.** Not techniques for building things —
techniques for knowing, before you start, what can be built, what it will cost, and what is
impossible. A proof that something cannot be done is worth as much as an algorithm, and it is
cheaper.

You now have the vocabulary to read a theorem, the discipline to check a claim, and the judgement to
guess whether a problem is easy. Use all three.

---

## 7. Final Exam Preparation

**Format:** 3 hours, closed book, one double-sided A4 sheet of handwritten notes.

**Coverage:** Weeks 0–12, weighted towards Weeks 3, 5, 7, 8, 10, 11 — the material other courses
depend on.

**A working method:**

1. Redo every **quiz** first — they were written to be the highest-yield revision in the course.
2. Then the **Part A** questions of each problem set: modelling and setup, not computation.
3. Then the **reference sheets**, which collect every verified value in one place.
4. Finally, one full past problem set under timed conditions.

**Bring to the exam:** the pigeonhole checklist, the two recurrence cases, the inclusion–exclusion
lcm rule, the tree facts ($n-1$ edges, degree sum $2(n-1)$), and Euler's criterion. Those five
items open more questions than anything else on the syllabus.

---

*MATH 151 · Week 12 · Lecture 12.3 · © CSE Department*

*This concludes MATH 151. Good luck.*

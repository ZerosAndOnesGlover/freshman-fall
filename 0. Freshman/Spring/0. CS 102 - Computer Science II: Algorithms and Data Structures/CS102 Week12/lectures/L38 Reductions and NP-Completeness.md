# CS 102 · Computer Science II
## Lecture 38: Reductions and NP-Completeness

*“Beware of the Turing tar-pit in which everything is possible but nothing of interest is easy.”* — Alan Perlis, "Epigrams on Programming" (1982), #54

**Date:** Wednesday 14 April 2027 · 09:00–09:50 · Week 12

**Reading:** CLRS §34.3–34.5 (in §34.5, at least vertex cover)

**Coursework:** 📋 **Project 2** due Fri 16 Apr 17:00 · 📝 **PS 11** due Fri 16 Apr 17:00 · 📕 **Final exam** Wed 21 Apr 09:00–11:30

---

## 1. Proving Hardness by Comparison

You cannot prove a problem hard by failing to solve it. What you *can* do is show it is **at least as
hard as** a problem already believed hard — and that is what a reduction does.

> A **polynomial-time reduction** from $A$ to $B$, written $A \le_p B$, is a polynomial-time
> transformation of any instance of $A$ into an instance of $B$ with the same yes/no answer.

If $A \le_p B$ then **an efficient algorithm for $B$ gives one for $A$**: transform, solve, return.
Contrapositively — and this is how it is used — **if $A$ is hard then $B$ is hard.**

> ### The direction is the whole thing
>
> To prove **$B$ is hard**, reduce a **known-hard** problem $A$ **to** $B$. You are showing that $B$ is
> at least as hard as $A$.
>
> Reducing $B$ to something known-hard proves **nothing** — it shows $B$ is no harder than a hard
> problem, which every problem satisfies vacuously.
>
> **Getting this backwards is the single most common error in the topic**, and it is worth writing the
> direction down every time before starting.

---

## 2. NP-Complete

> A problem $B$ is **NP-complete** if
> 1. $B \in NP$ — solutions are verifiable in polynomial time, **and**
> 2. every problem in NP reduces to $B$ in polynomial time.

Condition 2 makes $B$ **at least as hard as everything in NP**. So:

**If any single NP-complete problem is in P, then P = NP.** They stand or fall together — thousands of
problems, one fate.

That is a remarkable structural fact. It means the question "is my problem hard?" usually has a crisp
answer, because your problem is very likely equivalent to one of a large, well-catalogued family.

### The Cook–Levin theorem

Condition 2 quantifies over *every* problem in NP, which sounds impossible to establish for a first
example. Cook and Levin did it in 1971:

> **SAT is NP-complete.**

**SAT**: given a Boolean formula, is there an assignment making it true?

The proof simulates an arbitrary polynomial-time verifier by a Boolean formula — variables encode the
machine's state at each step, clauses enforce that each step follows the rules, and the formula is
satisfiable exactly when some certificate makes the verifier accept. The construction is intricate and
**you are not examined on it.**

What you are examined on is what it *bought*: **one** problem proved hard from first principles, after
which every further proof is a reduction from something already known.

---

## 3. The Reduction Tree

After SAT, hardness spread by reduction. Karp's 1972 paper gave 21 problems; the catalogue now runs to
thousands.

```
                          SAT   (Cook-Levin, from first principles)
                           |
                        3-SAT
                       /     \
               VERTEX COVER   CLIQUE / INDEPENDENT SET
                    |
             HAMILTONIAN CYCLE
                    |
                   TSP
```

Each arrow is a polynomial-time reduction, and **each one is a construction you could check by hand.**

### One worked reduction: 3-SAT $\le_p$ Vertex Cover

Given a 3-SAT formula with $n$ variables and $m$ clauses, build a graph:

- **Variable gadget**: for each variable $x$, two vertices $x$ and $\bar{x}$ joined by an edge. Any
  cover must include at least one — **choosing which encodes the truth assignment.**
- **Clause gadget**: for each clause, a triangle whose three vertices are its literals. Any cover must
  include at least **two** of the three.
- **Connections**: join each clause-triangle vertex to the matching literal in its variable gadget.

Ask for a cover of size $k = n + 2m$.

**Then the formula is satisfiable iff such a cover exists.** The budget $n + 2m$ is exactly one vertex
per variable edge and two per triangle, leaving no slack — so the third triangle vertex must be covered
by its connection, which forces its literal to be true.

**The construction is linear in the formula's size**, which is what makes it a *polynomial* reduction.

> **This is the shape of every reduction: gadgets that force local choices, and a budget that makes
> those choices global.** Once you have seen two you can read most of them.

---

## 4. The Catalogue Worth Knowing

| problem | question | note |
| --- | --- | --- |
| **SAT / 3-SAT** | satisfying assignment? | the root |
| **Vertex cover** | cover of size $\le k$? | 2-approximable — Lecture 39 |
| **Independent set** | independent set of size $\ge k$? | complement of vertex cover |
| **Clique** | complete subgraph of size $\ge k$? | independent set on the complement graph |
| **Hamiltonian cycle** | a cycle visiting every vertex once? | contrast Euler circuit, which is **easy** |
| **TSP** | tour of length $\le k$? | 2-approximable if metric |
| **Graph colouring** | $k$-colourable? | **2-colouring is easy** — Week 4's bipartiteness |
| **Subset sum / knapsack** | subset summing to $T$? | pseudo-polynomial — Week 7 |
| **Longest simple path** | path of length $\ge k$? | **easy on a DAG** — Week 5 |

**Read the right-hand column.** Four rows record a problem that is NP-complete in general and easy
under a restriction you have already implemented this term:

- **2-colouring** is BFS (Week 4); 3-colouring is NP-complete.
- **Longest path** is linear on a DAG (Week 5); NP-complete on a general graph.
- **Independent set** is linear on a tree (Week 8); NP-complete on a general graph.
- **Knapsack** is $\Theta(nW)$ (Week 7); NP-complete with $W$ written in binary.

> **The boundary between tractable and intractable runs through problems you have already solved.** In
> every case what changed was a restriction on the input, not the algorithm — and noticing which
> restriction your instances satisfy is worth more than any general technique.

### The neighbours

**NP-hard** — at least as hard as everything in NP, but **not necessarily in NP** itself. The
*optimisation* version of TSP is NP-hard rather than NP-complete: a claimed optimal tour has no obvious
short certificate, because verifying optimality means ruling out every shorter tour.

**Undecidable** — worse than intractable. The halting problem has **no** algorithm at any cost. This
week is about problems where an algorithm exists and is too slow; that is a different and milder
predicament.

---

## 5. How to Use This in Practice

You meet a new problem. It resists. What now?

1. **Try to solve it** for an hour. Most problems are not NP-complete.
2. **Look for it in the catalogue.** Garey and Johnson's *Computers and Intractability* (1979) lists
   several hundred, and is still the standard reference.
3. **Try a reduction from 3-SAT, vertex cover, or subset sum** — those three cover most cases. Remember
   the direction: reduce **from** a hard problem **to** yours.
4. **If it is NP-complete, say so and stop.** That is a result, not a failure — and it changes the
   conversation from "when will this be ready" to "which guarantee shall we give up".
5. **Then choose what to relax** — Lecture 37 §5's five options.

**Step 4 is the professional value of this week.** Being able to say "this is NP-complete, here is the
reduction, so here are our actual options" is a substantially more useful contribution than another
week of trying.

---

## 6. What to Do

- Read CLRS §34.3 (NP-completeness and reducibility) and §34.4 (NP-completeness proofs). §34.5 works
  through five reductions — read **at least** the vertex cover one.
- The Cook–Levin proof (§34.3) is worth reading once for the idea. **Not examinable.**
- **Lab 12** approximates TSP, which §4 lists as NP-complete.
- Next lecture: what to do about it — approximation algorithms, and the difference between a heuristic
  and a guarantee.

---

*CS 102 · Week 12 · Lecture 38 · © CSE Department*

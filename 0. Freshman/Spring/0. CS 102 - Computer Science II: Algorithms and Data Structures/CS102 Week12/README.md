# CS 102 · Computer Science II — Algorithms and Data Structures
## Week 12: NP-Completeness and the Limits of Efficiency

**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **Lab 12** — the last lab. **There is no problem set and no quiz this
week.**
**PROJECT 2 and PS 11 are both due Friday.** The **FINAL EXAM** is this week and is comprehensive —
see `resources/FINAL EXAM Revision Guide.md`.

---

### Why This Week Exists

For twelve weeks the question was *what is the best algorithm for this problem*. This week asks the
question one level up: **for which problems is there no good algorithm at all?**

Made concrete: exact TSP by Held–Karp — the best known exact algorithm, from 1962 — takes **14.8
seconds at 20 cities**, about **9.5 hours at 30**, and roughly **two years at 40**. A machine a thousand times
faster buys about **nine more cities**. That is what exponential means, and no amount of engineering
fixes it.

So the week is about three things: **recognising** that a problem is intractable, **proving** it, and
**deciding what to give up** once you have.

### Learning Objectives

By the end of Week 12, you should be able to:

1. Define P and NP precisely, and give the certificate for a problem in NP.
2. Explain why "NP" does not mean "non-polynomial", and why NP is not obviously closed under
   complement.
3. State what P vs NP asks and what a positive answer would mean.
4. Define a polynomial-time reduction and **get its direction right**.
5. State the Cook–Levin theorem and what it bought.
6. Recognise the standard NP-complete problems, and name four you have already solved efficiently
   under a restriction.
7. Prove the vertex cover 2-approximation and the metric TSP 2-approximation.
8. **Distinguish an approximation algorithm from a heuristic**, and say what each licenses you to
   claim.
9. Choose what to relax when a problem turns out to be NP-complete.

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L37 P NP and Verification.md` | The exponential wall, decision problems, P, NP, and P vs NP |
| `lectures/L38 Reductions and NP-Completeness.md` | Reductions, Cook–Levin, the catalogue, and what to do next |
| `lectures/L39 Approximation Algorithms.md` | Two proofs, one heuristic, and the landscape of approximability |
| `lab/LAB 12 A TSP Approximation.md` | The wall, the 2-approximation, breaking it, and 2-opt |
| `resources/Reading Guide Week 12.md` | CLRS Ch. 34–35, with the misreadings that matter |
| `resources/FINAL EXAM Revision Guide.md` | Format, 19 reproducible proofs, and the assumptions table |
| `resources/Course Retrospective.md` | What the twelve weeks were for — not examinable |
| `solutions_instructor/` | Lab 12 solutions — instructor only |

### The Three Ideas Most Likely to Be Missed

**1. NP means *nondeterministic polynomial*, not *non-polynomial*.** A problem is in NP if every **yes**
instance has a short certificate that can be **checked** quickly. P ⊆ NP trivially. And nothing in the
definition gives a short proof of a **no** answer — which is why co-NP exists, and why a SAT solver
reporting "unsatisfiable" is asking to be trusted.

**2. The direction of a reduction is the whole thing.** To prove **your** problem hard, reduce a
**known-hard** problem **to** it. Reducing yours to SAT proves nothing — every problem in NP does that.

**3. NP-completeness says nothing about approximability.** Knapsack and max clique are both
NP-complete. Knapsack admits an arbitrarily good approximation; max clique admits essentially none, and
that is a theorem. Equivalence for *exact* solution implies nothing about *approximate* solution.

### The Measurement That Closes the Course

Two ways to handle metric TSP, measured on 200 instances against exact Held–Karp:

| method | mean ratio | worst ratio | reached the optimum | guarantee |
| --- | --- | --- | --- | --- |
| MST 2-approximation | 1.1145 | 1.3205 | — | **provably $\le 2\times$, always** |
| 2-opt heuristic | **1.0051** | **1.1290** | **167 of 200** | **none** |

**The heuristic wins on every measurable quantity** — half a per cent above optimal, exact 84% of the
time — and you ship the other one, or both. What you can say about 2-opt is "it was good on my
sample". What you can say about the 2-approximation is *"it will never be worse than twice optimal, on
any input, ever."*

And the guarantee is not a property of the code. Remove the triangle inequality — change nothing else —
and the worst ratio goes from **1.3509** to **4.000**, with the bound violated in **42 of 2,000**
instances. For general TSP, **no constant-factor approximation exists** unless P = NP.

### The Boundary Runs Through Work You Have Already Done

Four problems are NP-complete in general and were linear or polynomial for you this term:

| problem | NP-complete in general | easy under | week |
| --- | --- | --- | --- |
| graph colouring | 3-colouring | **2**-colouring is BFS | 4 |
| longest simple path | general graphs | **DAGs** | 5 |
| independent set | general graphs | **trees** | 8 |
| knapsack | $W$ in binary | **$W$ small** — $\Theta(nW)$ | 7 |

**In every case what changed was a restriction on the input, not the algorithm.** Noticing which
restriction your instances satisfy is worth more than any general technique.

### Connections

**Back:** the whole course. Held–Karp is **Week 8**'s bitmask DP; the TSP approximation is **Week 6**'s
MST; the vertex cover bound is a **Week 9** exchange-style argument; knapsack's pseudo-polynomiality is
**Week 7**; 2-colouring is **Week 4**; longest path on a DAG is **Week 5**; independent set on a tree is
**Week 8**.

**Forward:** **CS 250** does the proof techniques properly; **CS 301 Theory of Computation** is this
week expanded into a course; **CS 401 Advanced Algorithms** takes approximation and randomisation
further. See `resources/Course Retrospective.md`.

---

*CS 102 · Week 12 · © CSE Department*

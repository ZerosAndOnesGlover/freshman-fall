# CS 102 · Reading Guide, Week 6
## Minimum Spanning Trees and Disjoint Sets

---

## Required

**CLRS, 4th ed. — Chapter 21** (Minimum Spanning Trees) — §21.1 and §21.2, about 18 pages.
**CLRS, 4th ed. — §19.1–19.3** (Disjoint Sets) — about 12 pages.

§19.4 proves the $O(m\,\alpha(n))$ bound. It is one of the hardest arguments in the book. **Read its
statement and skip the proof** — it is explicitly not examinable. Come back to it in a graduate
course, or never; you will not be worse at your job either way.

Also useful:

- **Sedgewick & Wayne §4.3** — MSTs, with the best diagrams of Prim's growing frontier and Kruskal's
  merging forest. Their union-find treatment in §1.5 is unusually good and includes the same
  measurements PS 6 asks you to make.
- **Skiena §6.1** — when an MST is and is not the right model, with war stories.

**This is a lighter reading week than Week 5.** Use the slack on PS 6 Part C, which is the largest
piece of measurement work this term.

---

## Read §21.1 Before Anything Else

Chapter 21 opens with the **generic MST algorithm**: maintain a set of edges that is a subset of some
MST, and repeatedly add a *safe* edge. Everything else in the chapter is an instantiation.

**Theorem 21.1 is the cut property**, and it is the only thing in this week that needs proving. Both
algorithms, both proofs, and every application follow from it. If you read one page of CLRS this week,
read that one.

CLRS states it with two conditions — a cut *respecting* the current edge set, and a *light* edge
crossing it. Make sure you see why the "respecting" clause is needed: without it you could pick a cut
that slices through edges you have already committed to.

---

## How to Read It

**§21.1 (8 pages).** Definitions, the generic algorithm, Theorem 21.1 and its corollary. The proof is
an **exchange argument** — assume an MST without your edge, swap your edge in, show nothing got worse.
That template is the whole of Week 9, so learn it here where the setting is concrete.

**§21.2 (10 pages).** Kruskal and Prim. Both are short. Note that CLRS presents Prim with a
`decrease_key` priority queue, whereas Lecture 20 uses lazy insertion with a `heapq` — the same trick
as Dijkstra in Week 5. The complexities are the same and the lazy version is what you will write.

**§19.1 (4 pages).** The ADT and an application that is exactly Kruskal's connectivity test.

**§19.2 (3 pages).** The linked-list representation with weighted union. Worth reading for the
amortised argument — it is much easier than §19.4's — but nobody implements it.

**§19.3 (5 pages).** The forest representation, union by rank, path compression. **This is the section
that matters**; it is the code you will write.

---

## Guiding Questions

Three of these are on MIDTERM 2.

1. §21.1, Theorem 21.1: the cut property says a light crossing edge is in **some** MST. Give a graph
   where it is not in **every** MST. What must be true of the weights for "some" and "every" to
   coincide?

2. The cut property says which edges are safe to **add**. State the dual property, which says which
   are safe to **reject**. Which of the two algorithms needs both?

3. Prim's algorithm and Dijkstra's differ in one expression. Write both keys down and say why the
   change converts one problem into the other.

4. Dijkstra requires non-negative weights; Prim and Kruskal do not. **Why not?** Your answer should
   involve a counting fact about spanning trees.

5. §19.3: union by rank alone gives $O(\log n)$ per operation; path compression alone gives
   $O(\log n)$ amortised. Together they give $O(\alpha(n))$. Why is the combination so much better
   than either — what does each optimisation prevent that the other does not?

6. A `find` on a long chain costs $\Theta(n)$. How can the amortised bound be near-constant? (Answer
   in terms of what that expensive call *changes*.)

7. The MST minimises total weight. Name a natural quantity it also minimises, and one it does **not**
   minimise despite students often assuming it does.

---

## Common Misreadings

**"The MST contains the shortest path between every pair."** No. On a triangle with weights 2, 2, 3,
the shortest $0\to2$ path is the direct edge of weight 3, but that edge is the heaviest on the cycle,
so the cycle property forbids it from any MST — the MST path costs 4. An MST is not a shortest-path
tree and does not try to be.

**"The MST minimises the maximum edge weight, so it is a shortest-path tree in disguise."** The first
half is true (and is the minimax property, Lecture 19 §5). The second does not follow — minimising the
worst edge is a different objective from minimising the sum along a route.

**"A light edge across a cut is in every MST."** Only when weights are distinct. With ties, it is in
*some* MST.

**"Distinct weights are necessary for a unique MST."** They are sufficient, not necessary — measured,
**121 of 240** random graphs with tied weights still had exactly one MST.

**"$\alpha(n)$ is a constant."** It is bounded by 4 for any $n$ that fits in memory, which makes it a
constant *in practice*. It is not a constant: it grows without bound, just extraordinarily slowly, and
$O(m\,\alpha(n))$ is a **tight** bound rather than the best analysis anyone has produced.

**"Kruskal's cost is dominated by the sort."** Asymptotically yes. Measured in CPython, the union-find
phase costs about **1.8× the sort** at every size from $E = 5{,}000$ to $E = 300{,}000$, because
`sorted()` is C and your union-find is interpreted. Both statements are true; PS 6 D3 asks you to
reconcile them.

**"Prim for dense, Kruskal for sparse."** Measured on explicit edge lists in Python, Kruskal won every
size tested, dense ones included. The advice becomes right again when the graph is *implicit* — Lab 6's
dense-Prim wins by 2.9× precisely because it never builds the edge list.

---

## If You Have Extra Time

**Borůvka's algorithm** (1926). Every component simultaneously picks its cheapest outgoing edge. The
component count halves each round, so it runs in $O(E \log V)$ — and unlike Prim and Kruskal it
**parallelises**, which is why every distributed MST algorithm descends from it. Historically it is
also the first MST algorithm, published to plan the electrification of Moravia.

**Karger–Klein–Tarjan** gives an expected **linear-time** MST algorithm using Borůvka steps and random
sampling. Chazelle's deterministic $O(E\,\alpha(V))$ is very nearly linear. Neither is used in
practice. That gap between the literature and what people write is worth thinking about.

**Second-best spanning tree.** Find the MST, then for each non-tree edge compute the heaviest edge on
the tree path it would close. The best swap gives the second-best tree, in $O(VE)$ naively or
$O(E\log V)$ with care. A good exercise in using the cycle property constructively.

**Minimum bottleneck spanning tree.** A *minimum bottleneck* spanning tree minimises the **heaviest**
edge rather than the total. Every MST is one — but **the converse fails**, and the smallest
counterexample is worth having:

```
0-1 (1),  1-2 (2),  0-2 (2),  2-3 (2)
```

The three spanning trees have totals 5, 5, 6 and all have bottleneck 2. So $\{(1,2), (0,2), (2,3)\}$
is a minimum bottleneck spanning tree with total **6** against the MST's **5** — a minimum bottleneck
tree that is not minimum.

*(Verified over 353 random graphs: "every MST is an MBST" failed **0** times; "every MBST is an MST"
failed **160** times.)*

**The implication is worth stating.** MST algorithms solve the bottleneck problem for free, so if the
bottleneck is what you care about you may use them — but you are then paying for an optimality you did
not ask for, and a cheaper bottleneck-only algorithm exists (repeatedly discard the heaviest edge while
the graph stays connected). Knowing that your tool solves a *stronger* problem than yours is as useful
as knowing it solves a weaker one.

---

*CS 102 · Week 6 · Reading Guide · © CSE Department*

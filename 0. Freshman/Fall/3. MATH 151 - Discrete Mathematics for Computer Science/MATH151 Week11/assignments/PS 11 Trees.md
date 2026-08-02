# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 11: Trees, Spanning Trees, and Traversal
### Released: Friday, Week 11 | Due: Friday, Week 12 (11:59 PM)

---

**Instructions:**
- Draw every tree you construct and label the vertices.
- For every algorithm trace, tabulate the state at each step — not just the final answer.
- Show all work. Submit as a single PDF.

**Scoring:** 100 points total, plus an optional 8-point bonus.

---

## Part A — Tree Properties (26 points)

**A1.** *(6 pts)* A tree has 15 vertices. How many edges? What is the sum of the degrees? Justify
both from the theorem, not by drawing.

**A2.** *(6 pts)* A tree has 10 vertices, of which 6 are leaves. The remaining vertices all have the
same degree. What is it? Show your working.

**A3.** *(6 pts)* Draw all non-isomorphic trees on 5 vertices, and explain how you know your list is
complete.

**A4.** *(8 pts)* Prove that every tree with $n\ge2$ vertices has at least two leaves. *(Hint: use
the degree sum.)* Then give a tree where exactly two leaves occur, for every $n$.

---

## Part B — Rooted and Binary Trees (22 points)

**B1.** *(6 pts)* Root the tree $V=\{a,\ldots,g\}$, $E=\{ab,ac,bd,be,cf,cg\}$ at $a$. Give every
vertex's depth, the height, the leaves, and the internal vertices.

**B2.** *(6 pts)* Root the same tree at $d$. Give the new depths and height, and explain in one
sentence why they differ from B1.

**B3.** *(5 pts)* State the maximum and minimum number of nodes in a binary tree of height $h$.
Verify both for $h = 0, 1, 2, 3$.

**B4.** *(5 pts)* What is the minimum possible height of a binary tree with 1000 nodes? With
$10^6$? State the general formula and explain its relevance to binary search trees.

---

## Part C — Spanning Trees and MSTs (30 points)

Use this weighted graph throughout Part C:

$$V=\{A,B,C,D,E,F\}$$

| Edge | $AB$ | $AC$ | $BC$ | $BD$ | $CD$ | $CE$ | $DE$ | $DF$ | $EF$ |
|---|---|---|---|---|---|---|---|---|---|
| Weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 3 | 2 |

**C1.** *(8 pts)* Run **Kruskal's algorithm**. Tabulate every edge considered, in order, with your
accept/reject decision and the reason. State the final tree and its total weight.

**C2.** *(8 pts)* Run **Prim's algorithm from $A$**. Tabulate the tree vertices and the edge added at
each step. State the total weight.

**C3.** *(4 pts)* Your answers to C1 and C2 should have the same total. Do they have the same edge
set? Explain what determines whether an MST is unique.

**C4.** *(5 pts)* How many labelled spanning trees does $K_7$ have? $K_{10}$? State the theorem you
are using.

**C5.** *(5 pts)* Explain why an MST can never contain the unique heaviest edge of a cycle.

---

## Part D — Traversal (22 points)

**D1.** *(6 pts)* For the tree of B1 with neighbours in alphabetical order, give the BFS and DFS
orders starting from $a$, and again starting from $b$.

**D2.** *(5 pts)* Explain why BFS computes shortest paths in an unweighted graph but DFS does not.
Then state precisely what changes when edges are weighted.

**D3.** *(6 pts)* Find **all** topological orders of the DAG $a\to b$, $a\to c$, $b\to d$,
$c\to d$, $d\to e$. Explain why there is more than one.

**D4.** *(5 pts)* Describe how to test bipartiteness with a single BFS, and state the running time.

---

## Bonus (8 points — optional)

**Bonus 1.** *(4 pts)* Prove the **cut property**: for any partition of $V$ into two non-empty sets,
the minimum-weight edge crossing the partition lies in some MST.

**Bonus 2.** *(4 pts)* Show that a directed graph has a cycle iff some DFS encounters an edge to a
vertex currently on the recursion stack. Explain why testing "already visited" is not sufficient.

---

## Grading

| Part | Topic | Points |
|---|---|---|
| A | Tree properties | 26 |
| B | Rooted and binary trees | 22 |
| C | Spanning trees and MSTs | 30 |
| D | Traversal | 22 |
| **Total** | | **100** |

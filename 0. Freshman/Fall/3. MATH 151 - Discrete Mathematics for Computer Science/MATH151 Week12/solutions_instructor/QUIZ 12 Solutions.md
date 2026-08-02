# MATH 151 · Quiz 12 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

**Total: 20 points.** All values verified.

---

**Q1. (4 pts)** A tree on $n$ vertices has exactly $n-1$ edges, so **19 edges**. By the Handshake
Theorem the degree sum is $2\lvert E\rvert = \mathbf{38}$.

*Marking: 2 each. Both must be justified — "a tree has $n-1$ edges" and "$\sum\deg = 2\lvert E\rvert$".*

---

**Q2. (4 pts)** Sorted: $AB(1)$, $BD(2)$, $BC(3)$, $AC(4)$, $CD(5)$.

| Edge | Decision |
|---|---|
| $AB(1)$ | accept |
| $BD(2)$ | accept |
| $BC(3)$ | accept — 3 edges $= n-1$, stop |

**Total: $1+2+3 = \mathbf 6$.** *(Verified.)*

$AC$ would close the cycle $A\,B\,C$ and $CD$ the cycle $B\,C\,D$; both are rejected, but the
algorithm stops before reaching them.

*Marking: 2 for the sorted order and decisions, 2 for the total. Stopping at $n-1$ edges is worth
noting in feedback — students often continue and then reject the rest.*

---

**Q3. (4 pts)** Adjacency: $a: b,c$; $b: a,d,e$; $c: a$; $d: b$; $e: b$.

| | Order |
|---|---|
| **BFS** | $a,\ b,\ c,\ d,\ e$ |
| **DFS** | $a,\ b,\ d,\ e,\ c$ |

*(Both verified.)*

*Marking: 2 each. DFS is the discriminator: it commits to $b$'s entire subtree ($d$, $e$) before
returning for $c$. Students who give $a,b,c,d,e$ for DFS have run BFS twice.*

---

**Q4. (4 pts)** $$h \ge \lceil\log_2(n+1)\rceil - 1 = \lceil\log_2 501\rceil - 1 = 9 - 1 = \mathbf 8$$

*(Verified: $2^9 = 512 \ge 501 > 256 = 2^8$.)*

A binary tree of height 8 holds at most $2^9-1 = 511$ nodes, which is enough for 500; height 7 holds
at most 255, which is not.

*Marking: 2 for the value, 2 for the formula or the equivalent $2^{h+1}-1 \ge n$ argument.*

---

**Q5. (4 pts)** Kahn's algorithm returns **`None`** (or equivalently, outputs fewer than $n$
vertices) — because after removing all vertices of in-degree 0, every remaining vertex still has an
incoming edge from within the cycle, so the queue empties early.

**For a build system** this means the dependency graph has a **circular dependency**, and therefore
**no valid build order exists** — some target would have to be built before itself. The tool reports
the cycle and stops.

**This is a correct result, not a failure of the algorithm.** A topological order exists if and only
if the graph is acyclic.

*Marking: 2 for the return value with reasoning, 2 for the build-system interpretation. Full marks
require recognising that the algorithm behaved correctly — students who call it a limitation lose 1.*

---

## Grade Distribution Notes

Q3's DFS and Q5's interpretation are the two discriminators. Both are conceptual rather than
computational, and both appear on the final in some form.

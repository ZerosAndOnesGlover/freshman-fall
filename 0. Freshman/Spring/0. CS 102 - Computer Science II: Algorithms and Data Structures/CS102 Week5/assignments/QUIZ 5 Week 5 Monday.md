# CS 102 · Quiz 5

**Date:** Monday 22 February 2027 · 09:00–09:15 (start of L16) · Week 5 · 20 points
**Covers Week 4** — graph representations, BFS, and DFS. **Not** this week's material.

Closed book. Every number here is exact.
**MIDTERM 1 is Monday 1 March, 18:00, and covers Weeks 0–4.** Treat this quiz as a rehearsal for its
Section A.

---

**Q1.** *(3)* A graph has $V = 1000$ vertices and $E = 3000$ edges.

- **(a)** How many entries does an adjacency **matrix** hold?
- **(b)** Roughly how many does an adjacency **list** hold, if the graph is undirected?
- **(c)** Which would you use, and why?

---

**Q2.** *(4)* For the undirected graph with edges $0{-}1$, $0{-}2$, $1{-}3$, $2{-}3$, $3{-}4$, run BFS
from vertex 0, taking neighbours in increasing order.

Give the distance to every vertex, and the order in which vertices are dequeued.

---

**Q3.** *(4)* For the **directed** graph $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 3$, run DFS from
vertex 0 taking neighbours in increasing order.

- **(a)** Give $d[u]$ and $f[u]$ for all four vertices.
- **(b)** Classify the edge $2 \to 3$.

---

**Q4.** *(3)* State the parenthesis theorem: for two vertices $u$ and $v$, which three cases are
possible, and which is **impossible**?

---

**Q5.** *(3)* In a DFS, a vertex is coloured **grey**. Say precisely what that means, and why the
distinction from **black** is what makes back-edge detection work.

---

**Q6.** *(3)* BFS and DFS are both $\Theta(V+E)$. Measured on this machine, BFS costs about 80 ns per
unit of $(V+E)$ at $V = 10^4$ but 399 ns at $V = 10^6$ on a random graph — and only 119 ns at
$V = 10^6$ on a grid.

**Is the $\Theta(V+E)$ bound wrong?** Answer in two sentences.

---

*20 points total. Solutions posted after Wednesday's lecture.*

*CS 102 · Week 5 · Quiz 5 · © CSE Department*

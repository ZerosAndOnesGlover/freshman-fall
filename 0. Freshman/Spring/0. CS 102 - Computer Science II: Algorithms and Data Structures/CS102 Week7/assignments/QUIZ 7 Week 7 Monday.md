# CS 102 · Quiz 7

**Week 7, Monday, first 15 minutes of lecture · 20 points**
**Covers Week 6** — minimum spanning trees, the cut property, union-find. **Not** this week's
material.

Closed book. Every number here is exact.

---

**Q1.** *(4)* For the undirected graph with edges

$$0{-}2\ (1),\quad 1{-}2\ (2),\quad 3{-}4\ (3),\quad 0{-}1\ (4),\quad 1{-}3\ (5),\quad 2{-}4\ (7),\quad 2{-}3\ (8)$$

run **Kruskal's algorithm**. List the edges in the order considered, marking each accepted or
rejected, and give the MST's total weight.

---

**Q2.** *(3)* State the **cut property**.

Your statement must make clear whether a light crossing edge is in *some* MST or in *every* MST, and
say what would have to be true of the weights for those to coincide.

---

**Q3.** *(3)* State the **cycle property**, and explain in one sentence why the word "strictly" cannot
be dropped.

---

**Q4.** *(3)* Prim's algorithm and Dijkstra's differ in one expression.

Write down what each pushes onto the priority queue, and say in one sentence what the difference
changes.

---

**Q5.** *(4)* A union-find structure with **neither** optimisation is used on $n$ elements.

- **(a)** *(2)* Describe an input on which a single `find` costs $\Theta(n)$.
- **(b)** *(2)* With **path compression and union by rank**, the same sequence of $n$ finds on that
  input costs exactly $n-1$ steps in total. Explain why the first `find` makes all the others cheap.

---

**Q6.** *(3)* True or false, with one sentence each:

- **(a)** The MST contains the shortest path between every pair of vertices.
- **(b)** MST algorithms require non-negative edge weights.
- **(c)** $\alpha(n)$, the inverse Ackermann function, is a constant.

---

*20 points total. Solutions posted after Wednesday's lecture.*

*CS 102 · Week 7 · Quiz 7 · © CSE Department*

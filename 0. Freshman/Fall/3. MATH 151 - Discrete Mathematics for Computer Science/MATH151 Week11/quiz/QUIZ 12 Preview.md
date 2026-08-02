# MATH 151 · Discrete Mathematics for Computer Science
## Quiz 12 — Scope Preview
### Quiz administered: Monday, Week 12 (first 15 minutes of lecture)

---

**Coverage:** Week 11 material — trees, spanning trees, minimum spanning trees, and traversal.

---

## What You Must Know Cold

### 1. The tree equivalences

Connected and acyclic ⟺ connected with $n-1$ edges ⟺ acyclic with $n-1$ edges ⟺ unique paths ⟺
connected with every edge a bridge.

**Know that a tree has exactly $n-1$ edges and degree sum $2(n-1)$.** Most tree questions dissolve
once you write those down.

### 2. Rooted trees

Depth, height, leaves, internal vertices. **Height depends on the root** — this is tested.

### 3. Binary tree bounds

$$\text{height } h \implies \le 2^{h+1}-1 \text{ nodes} \qquad n \text{ nodes} \implies h \ge \lceil\log_2(n+1)\rceil-1$$

Know $n=1000 \Rightarrow h\ge9$ and $n=10^6 \Rightarrow h\ge19$, and why balanced BSTs matter.

### 4. Kruskal and Prim

| | Kruskal | Prim |
|---|---|---|
| Method | Sort all edges, add if no cycle | Grow one tree by cheapest outgoing edge |
| Structure | Union–find | Heap |
| Cost | $\Theta(m\log m)$ | $\Theta(m\log n)$ |
| Intermediate state | A **forest** | A single tree |

**Both give the same total weight.** Be ready to trace either by hand, tabulating each step.

### 5. Cayley's formula

$K_n$ has $n^{n-2}$ labelled spanning trees. $K_7 = 16\,807$; $K_{10} = 10^8$.

### 6. BFS versus DFS

Queue versus stack; both $\Theta(n+m)$. **BFS gives shortest paths in unweighted graphs; DFS gives
components, cycle detection, and topological order.** Weighted graphs need Dijkstra.

A topological order exists **iff** the digraph is acyclic.

---

## Sample Quiz 12 Problems (Week 11 portion)

**Problem 1.** (4 pts) A tree has 20 vertices. How many edges? What is the degree sum?

**Problem 2.** (4 pts) Trace Kruskal on a small weighted graph and give the total.

**Problem 3.** (4 pts) Give the BFS and DFS orders from a stated vertex, with neighbours in
alphabetical order.

**Problem 4.** (4 pts) What is the minimum height of a binary tree with 500 nodes?

**Problem 5.** (4 pts) A digraph has a cycle. What does Kahn's algorithm return, and what does that
mean for a build system?

---

## Study Recommendations

1. **Trace Kruskal and Prim by hand on the PS 11 graph until both give 11 without hesitation.** Hand-tracing is the most heavily weighted skill this week.
2. **Memorise $n-1$ edges and degree sum $2(n-1)$.** They open almost every tree problem.
3. **Practise BFS and DFS on the same tree from two different starts.** The contrast is what gets examined.
4. **Do not confuse "same total weight" with "same edge set"** for MSTs — that distinction is a standard exam question.

---

*MATH 151 · Week 11 · © CSE Department*

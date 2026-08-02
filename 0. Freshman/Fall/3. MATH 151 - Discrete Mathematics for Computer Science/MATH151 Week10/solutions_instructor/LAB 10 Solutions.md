# MATH 151 — Week 10
## LAB 10 Solutions — INSTRUCTOR ONLY

All outputs below were produced by running the lab code. $G$ is $V=\{a,b,c,d,e\}$,
$E=\{ab,ac,bc,bd,cd,de\}$.

---

## Section 1 Solutions — By Hand

**1.1** Degree sequence $(1,2,3,3,3)$: $\deg a=2$, $\deg b=\deg c=\deg d=3$, $\deg e=1$.
Handshake: $2+3+3+3+1=12=2\times6$ ✓

**1.2**
$$A=\begin{pmatrix}0&1&1&0&0\\1&0&1&1&0\\1&1&0&1&0\\0&1&1&0&1\\0&0&0&1&0\end{pmatrix}
\qquad
\begin{aligned} a&: b,c\\ b&: a,c,d\\ c&: a,b,d\\ d&: b,c,e\\ e&: d\end{aligned}$$

**1.3** **$d$ is the only cut vertex**; **$de$ is the only bridge**. Removing $d$ isolates $e$. Every
other edge lies on a cycle ($abc$ or $bcd$), and no edge on a cycle is a bridge.

**1.4** Odd-degree vertices are $b,c,d,e$ — **four**. Euler requires $0$ (circuit) or exactly $2$
(trail). **Neither exists.**

*The instruction was to justify from the criterion, not to search. Students who tried to find a trail
and gave up have not answered the question.*

---

## Section 2 Solutions — Representations

**2.1** *(3 pts)* Both match the hand answers.

**2.2** *(4 pts)*

$$A^2=\begin{pmatrix}2&1&1&2&0\\1&3&2&1&1\\1&2&3&1&1\\2&1&1&3&0\\0&1&1&0&1\end{pmatrix}$$

- **Diagonal of $A^2$** is $(2,3,3,3,1)$ — the degree sequence ✓
- **$(A^2)_{ad}=2$**: the walks $a\to b\to d$ and $a\to c\to d$ ✓
- **$\operatorname{trace}(A^3)=2+4+4+2+0=12$**, so $12/6=\mathbf 2$ triangles: $\{a,b,c\}$ and
  $\{b,c,d\}$ ✓

**2.3** *(3 pts)* Handshake holds for $G$ ($12=12$), $K_5$ ($20=20$), and $C_6$ ($12=12$).

---

## Section 3 Solutions — Traversal and Connectivity

**3.1** *(5 pts)* `bfs(adj, 'a')` returns `['a','b','c','d','e']`.

Orders differ by starting vertex, and also depend on the **order neighbours appear in the adjacency
list**. A BFS order is therefore not a property of the graph — it is a property of the graph *plus*
the representation. Students should say this.

**3.2** *(4 pts)* $C_6$ → **1** component; two disjoint triangles → **2** ✓

**3.3** *(5 pts)* `cut_vertices` on $G$ returns `['d']`, confirming 1.3 ✓

**3.4** *(5 pts)*

| Graph | Bipartite? |
|---|---|
| $C_4$ | **Yes** |
| $C_5$ | **No** |
| $C_6$ | **Yes** |
| $K_{3,3}$ | **Yes** |
| $G$ | **No** |

Even cycles are bipartite, odd cycles are not — exactly the odd-cycle theorem. $G$ fails because it
contains triangles, which are 3-cycles. $K_{3,3}$ is bipartite by construction.

---

## Section 4 Solutions — Invariants and Isomorphism

**4.1–4.2** *(8 pts)*

| Graph | (V, E, degseq, components, triangles, bipartite) |
|---|---|
| $C_6$ | $(6,\,6,\,[2,2,2,2,2,2],\,1,\,0,\,\text{True})$ |
| Two triangles | $(6,\,6,\,[2,2,2,2,2,2],\,2,\,2,\,\text{False})$ |

**Agree on:** vertex count, edge count, degree sequence.
**Separated by:** component count (1 vs 2), triangle count (0 vs 2), and bipartiteness.

*Three invariants agree and three differ — a good illustration that agreement on some invariants
means nothing.*

**4.3** *(4 pts)*

- **$K_{3,3}$ vs $C_6$:** first difference is the **edge count**, 9 vs 6.
- **$C_6$ vs $Q_3$:** $Q_3$ has 8 vertices, $C_6$ has 6 — the **vertex count** separates them
  immediately.

**4.4** *(4 pts)* Brute force tries all $n!$ bijections:

| $n$ | $n!$ |
|---|---|
| 6 | 720 |
| 7 | 5,040 |
| 8 | 40,320 |

Growth is **factorial** — each increment of $n$ multiplies the work by $n$.

At $n=20$: $20! = 2{,}432{,}902{,}008{,}176{,}640{,}000 \approx 2.4\times10^{18}$. At a billion
bijections per second this is roughly **77 years**. Hopeless.

*Marking: 2 for the timing table, 2 for computing $20!$ and drawing the conclusion.*

---

## Section 5 Solutions — Euler and Hamilton

**5.1** *(3 pts)*

| Graph | Odd degrees | Result |
|---|---|---|
| $C_6$ | 0 | **circuit** |
| $K_4$ | 4 | **neither** |
| $K_5$ | 0 | **circuit** |
| $G$ | 4 | **neither** |

$K_n$ has an Euler circuit exactly when $n$ is odd, since all degrees are $n-1$.

**5.2** *(4 pts)*

- $K_4$: Hamilton cycle found, e.g. $0\to1\to2\to3\to0$ — essentially instant.
- **Petersen graph: none exists.** Exhaustive search over all $9! = 362{,}880$ vertex orderings
  returns nothing.

**5.3** *(3 pts)* `has_euler` inspects each vertex's degree once — $\Theta(n+m)$, a **counting**
procedure with a closed criterion. `hamilton_cycle` has no criterion to check, so it must **search**,
and the search space is $\Theta(n!)$.

The difference is not implementation quality. Euler has a theorem giving a locally checkable
condition; Hamilton has none, and the problem is NP-complete. **A better programmer cannot close this
gap.**

---

## Section 6 — Reflection Model Answers

1. **Invariant filtering.** Since brute force is factorial, invariants are not a convenience but the
   only practical approach: they reject non-isomorphic pairs in polynomial time, so exhaustive search
   is reached only for pairs that survive every cheap test. This is exactly how tools like `nauty`
   work — refine by invariants until the remaining search is tiny. Invariants cannot *confirm*
   isomorphism, but they eliminate almost everything.

2. **Euler vs Hamilton.** Euler's condition is **local**: it depends only on each vertex's degree, so
   it can be checked one vertex at a time and the checks compose. Hamiltonicity is **global** —
   whether a valid cycle exists depends on the whole structure at once, and no local measurement
   determines it. Locality is what makes a problem easy.

3. **$10^6$ vertices, $5\times10^6$ edges.** Use the **adjacency list**: about
   $n+2m = 1.1\times10^7$ stored references, a few hundred megabytes at worst. The matrix would need
   $10^{12}$ entries — a terabyte even at one byte each, and over 99.999% of it zero.

---

## Checkoff Summary

| Section | Watch for |
|---|---|
| 1 | 1.4 justified by degrees, not by searching |
| 2.2 | All three checks confirmed, triangles listed |
| 3.1 | Recognition that BFS order depends on the representation |
| 3.3 | `['d']` matching the hand answer |
| 3.4 | Results tied back to the odd-cycle theorem |
| 4.2 | Both the agreeing and the separating invariants named |
| 4.4 | $20!$ computed and interpreted |
| 5.2 | Petersen confirmed non-Hamiltonian |
| 6 | Q2 must reach the local-versus-global distinction |

---

*MATH 151 · Week 10 · Lab 10 Solutions · Instructor copy — do not distribute*

# MATH 151 · Quiz 11 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

**Total: 20 points.** All values verified.

---

**Q1. (4 pts)** **No.** Seven vertices of degree 3 give a degree sum of $7\times3=21$, which is
**odd**. The Handshake Theorem requires the sum to equal $2\lvert E\rvert$, which is always even. No
such graph exists.

For 12 vertices of degree 5: sum $=60$, so $\lvert E\rvert = 60/2 = \mathbf{30}$. *(This one does
exist — the parity check passes and $5 \le 11$.)*

*Marking: 3 for the impossibility with the parity argument, 1 for the 30. Students who answer "no" to
both have over-applied the first result — the second is a legitimate graph.*

---

**Q2. (4 pts)** Every vertex of $K_n$ has degree $n-1$. Euler's criterion needs **all degrees even**,
so $n-1$ must be even, i.e. **$n$ is odd** (and $n\ge3$).

*Verified: $K_3, K_5, K_7$ have Euler circuits; $K_4, K_6$ do not.*

*Marking: 2 for identifying the degree as $n-1$, 2 for the parity conclusion. An answer of "odd $n$"
without the degree argument earns 2.*

---

**Q3. (4 pts)** $C_6$ (a single 6-cycle) and **two disjoint triangles**. Both have 6 vertices, 6
edges, and every degree 2.

**The separating invariant is the number of connected components:** 1 for $C_6$, 2 for the pair of
triangles.

*(Triangle count and bipartiteness also separate them: $0$ vs $2$, and bipartite vs not.)*

*Marking: 2 for a valid pair, 2 for naming an invariant. Any one invariant suffices.*

---

**Q4. (4 pts)** Matrix: $50^2 = \mathbf{2500}$ entries, of which $2\times100 = 200$ are non-zero — 8%
occupancy. List: about $n+2m = 50+200 = \mathbf{250}$ stored references.

**Choose the adjacency list** — ten times smaller, and the gap widens as the graph grows. The matrix
would be preferable only if the dominant operation were the $\Theta(1)$ edge test.

*Marking: 1 matrix, 1 list, 1 choice, 1 justification.*

---

**Q5. (4 pts)** In $K_{2,3}$ the two vertices on the small side have degree 3; the three on the large
side have degree 2.

- **Euler circuit: no** — two vertices have odd degree, and a circuit requires all even.
- **Euler trail: yes** — there are **exactly two** odd-degree vertices, which is precisely the trail
  condition. The trail must begin at one and end at the other.

*Marking: 2 for the degree analysis, 1 for each conclusion. Answering "no" to both is the common
error — students remember the circuit rule and forget the trail rule.*

---

## Grade Distribution Notes

Q1 and Q5 both reward reading the criterion carefully rather than recalling a slogan. Expect the
second half of Q1 (where a graph *does* exist) and the trail half of Q5 to be the two most-missed
items; both are worth revisiting before the final.

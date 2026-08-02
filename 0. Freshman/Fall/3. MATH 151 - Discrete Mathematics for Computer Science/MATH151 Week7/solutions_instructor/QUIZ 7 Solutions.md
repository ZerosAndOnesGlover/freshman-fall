# MATH 151 — Week 7
## Quiz 7 Solutions — INSTRUCTOR ONLY

---

### Problem 1 (8 points) — $A=\{1,2,3,4\}$, $R=\{(1,1),(2,2),(3,3),(4,4),(1,2),(2,1),(3,4)\}$

**Reflexive?** All four self-loops $(1,1),(2,2),(3,3),(4,4)$ present. **YES.** [2 pts]

**Symmetric?** $(1,2)$ and $(2,1)$ both present ✓. $(3,4)$ present but $(4,3)$ is NOT present. **NO** — counterexample: $(3,4)\in R$ but $(4,3)\notin R$. [2 pts]

**Antisymmetric?** We have both $(1,2)\in R$ and $(2,1)\in R$ with $1\neq2$. **NO** — counterexample: $(1,2)$ and $(2,1)$ both in $R$, but $1\neq2$. [2 pts]

**Transitive?** Check: $(1,2),(2,1)\Rightarrow$ need $(1,1)$ — present ✓. $(2,1),(1,2)\Rightarrow$ need $(2,2)$ — present ✓. $(3,4)$: does 4 have any outgoing pairs besides $(4,4)$? No. So $(3,4),(4,4)\Rightarrow$ need $(3,4)$ — already present ✓. No other chains. **YES.** [2 pts]

*Grading: full credit requires both correct classification AND correct justification (proof sketch or specific counterexample) for each of the 4 properties.*

---

### Problem 2 (6 points) — $a\sim b\iff a^2\equiv b^2\pmod5$

**Proof.**

**Reflexive:** $a^2\equiv a^2\pmod5$ trivially (same value). ✓ [2 pts]

**Symmetric:** Assume $a^2\equiv b^2\pmod5$, i.e., $5\mid(a^2-b^2)$. Then $5\mid(b^2-a^2)=-(a^2-b^2)$ (negation of a multiple of 5 is still a multiple of 5). So $b^2\equiv a^2\pmod5$. ✓ [2 pts]

**Transitive:** Assume $a^2\equiv b^2\pmod5$ and $b^2\equiv c^2\pmod5$, i.e., $5\mid(a^2-b^2)$ and $5\mid(b^2-c^2)$. Adding: $5\mid[(a^2-b^2)+(b^2-c^2)]=5\mid(a^2-c^2)$. So $a^2\equiv c^2\pmod5$. ✓ [2 pts]

All three properties hold — equivalence relation. ∎

---

### Problem 3 (6 points) — Divisibility on $A=\{1,2,3,4,5,6\}$

**(a)** (2 pts) Covering relations:
$1\lessdot2,\ 1\lessdot3,\ 1\lessdot5,\ 2\lessdot4,\ 2\lessdot6,\ 3\lessdot6$

(Check: $1\lessdot4$? No — 2 intermediate. $1\lessdot6$? No — 2 or 3 intermediate.)

**(b)** (2 pts) **NOT a total order.** Counterexample: 4 and 5 are incomparable ($4\nmid5$ and $5\nmid4$). Also 4 and 6, 4 and 3, 5 and 6, 5 and 2, 5 and 3, 5 and 4 are all incomparable pairs.

**(c)** (2 pts) Maximal elements: **4, 5, 6** (nothing in $\{1,\ldots,6\}$ is divisible by 4, 5, or 6 other than the element itself — check: is anything divisible by 4? No multiple of 4 other than 4 itself is ≤6. By 5? No. By 6? No.)

*Grading: 2 pts for correct covering list (minor omissions lose partial credit), 2 pts for correct NO + valid counterexample, 2 pts for all three maximal elements identified.*

---

### Grade Distribution

| Score | Interpretation |
|---|---|
| 18–20 | Mastered relations, equivalence relations, posets |
| 14–17 | Solid; review antisymmetric vs symmetric distinction |
| 10–13 | Re-read Lectures 6.1–6.3; redo PS6 |
| < 10 | Schedule office hours before Week 7 |

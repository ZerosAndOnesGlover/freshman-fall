# MATH 151 · Week 4
## Quiz 4 Solutions — INSTRUCTOR ONLY

---

### Problem 1 — Geometric Sum (7 points)

**Proof.** By mathematical induction on n.

**Base case ($n=0$):** LHS $=2^0=1$. RHS $=2^{0+1}-1=2-1=1$. Equal. ✓ [2 pts]

**Inductive step:** Let $k\geq0$ be arbitrary.
IH: Assume $\sum_{i=0}^{k}2^i=2^{k+1}-1$. [1 pt for correctly stated IH]

Goal: Show $\sum_{i=0}^{k+1}2^i=2^{k+2}-1$.

$$\sum_{i=0}^{k+1}2^i = \left(\sum_{i=0}^{k}2^i\right)+2^{k+1} = (2^{k+1}-1)+2^{k+1} \quad\text{[by IH]}$$
$$= 2\cdot2^{k+1}-1 = 2^{k+2}-1$$

[3 pts for correct algebra with IH clearly applied]

Therefore, by the Principle of Mathematical Induction, the formula holds for all $n\geq0$. [1 pt for conclusion] ∎

---

### Problem 2 — Divisibility (6 points)

**Proof.** By mathematical induction on n.

**Base case ($n=1$):** $5^1-1=4=4\cdot1$. So $4\mid4$. ✓ [1 pt]

**Inductive step:** Assume $4\mid(5^k-1)$, so $5^k-1=4m$ for some $m\in\mathbb{Z}$, i.e., $5^k=4m+1$. [1 pt for IH]

$$5^{k+1}-1 = 5\cdot5^k-1 = 5(4m+1)-1 = 20m+5-1 = 20m+4 = 4(5m+1)$$

[3 pts for correct algebra]

Since $5m+1\in\mathbb{Z}$, $4\mid(5^{k+1}-1)$. ✓

By induction, $4\mid(5^n-1)$ for all $n\geq1$. [1 pt for conclusion] ∎

---

### Problem 3 — Error Analysis (7 points)

**(a)** (3 pts) The claim is **FALSE for $n=2$**: $2!=2$ but $2^2=4$, and $2\not\geq4$.

Checking the small cases in full:

| $n$ | $n!$ | $n^2$ | $n!\geq n^2$? |
|---|---|---|---|
| 1 | 1 | 1 | **TRUE** |
| 2 | 2 | 4 | **FALSE** |
| 3 | 6 | 9 | **FALSE** |
| 4 | 24 | 16 | **TRUE** |
| 5 | 120 | 25 | TRUE |

So the claim **fails for both $n=2$ and $n=3$**, and holds for $n=1$ and for all $n\geq4$ (from
$n=4$ onward each step multiplies the left side by $n$ and the right by less than $2$, so the gap
only widens).

*(Grading note: full credit for identifying n=2 fails; bonus recognition if student also catches n=3 fails.)*

**(b)** (2 pts) The base-case/inductive-step structure breaks because there is a **gap**: the claim is true at $n=1$ but false at $n=2$ and $n=3$, then true again from $n=4$ onward. A single inductive step cannot "skip over" false cases — induction requires an unbroken chain from the base case forward. Since $P(1)$ is true but $P(2)$ is false, the inductive step $P(1)\rightarrow P(2)$ must fail (and indeed, checking the "proof," the inductive step's derivation implicitly required $k\geq2$ for the key inequality $k^2\geq k+1$ to hold, which is exactly the condition under which the flawed proof silently smuggled in an assumption not covered by the base case).

**(c)** (2 pts) Corrected theorem: For all $n\geq4$, $n!\geq n^2$ (with base case $n=4$: $24\geq16$ ✓, and the inductive step's requirement $k^2\geq k+1$ holds for all $k\geq2$, in particular for $k\geq4$).

---

### Grade Distribution

| Score | Interpretation |
|---|---|
| 18–20 | Mastered induction structure and error diagnosis |
| 14–17 | Solid; review base case verification discipline |
| 10–13 | Re-read Lectures 3.1–3.3; redo PS3 |
| < 10 | Schedule office hours before Week 5 |

# MATH 151 · Week 5
## Quiz 5 Solutions — INSTRUCTOR ONLY

---

### Problem 1 (5 points) — $U=\{1,\ldots,10\}$, $A=\{1,2,3,4,5\}$, $B=\{4,5,6,7\}$

**(a)** $A\cap B = \{4,5\}$ [1 pt]

**(b)** $A\oplus B$: $A-B=\{1,2,3\}$, $B-A=\{6,7\}$. $A\oplus B=\{1,2,3,6,7\}$ [1 pt]

**(c)** $\overline{A\cup B}$: $A\cup B=\{1,2,3,4,5,6,7\}$. Complement in $U$: $\{8,9,10\}$ [1 pt]

**(d)** $\overline{A}=\{6,7,8,9,10\}$, $\overline{B}=\{1,2,3,8,9,10\}$. $\overline{A}\cap\overline{B}=\{8,9,10\}$.

Matches $\overline{A\cup B}=\{8,9,10\}$ from (c). ✓ De Morgan's Law confirmed. [2 pts]

---

### Problem 2 (6 points)

**Proof.** [Element-chasing]
$$x\in A\cap(B-C) \iff x\in A\land x\in(B-C)$$
$$\iff x\in A\land(x\in B\land x\notin C)$$
$$\iff (x\in A\land x\in B)\land x\notin C \quad\text{[associativity/rearranging]}$$
$$\iff x\in(A\cap B)\land x\notin C$$

Now, note we need $x\notin C$, but we want to reach $(A\cap B)-(A\cap C)$. Let's continue:

$$\iff x\in(A\cap B) \land \neg(x\in A\land x\in C)$$

Since we already have $x\in A$ (from $x\in A\cap B$), $\neg(x\in A\land x\in C)$ simplifies: given $x\in A$ is true, $\neg(x\in A\land x\in C) \iff \neg(T\land x\in C) \iff \neg(x\in C) \iff x\notin C$. So this is consistent — both forms reduce to the same condition.

$$\iff x\in(A\cap B)\land x\notin(A\cap C) \quad\text{[since }x\in A\text{ already holds]}$$
$$\iff x\in(A\cap B)-(A\cap C)$$

Since $x$ arbitrary, $A\cap(B-C)=(A\cap B)-(A\cap C)$. ∎

*Grading: 2 pts for correct unpacking of intersection/difference. 2 pts for correctly handling the "since x∈A already holds" step (this is the subtle point — many students will handle it more informally, which is fine if logically sound). 2 pts for correct conclusion.*

*Simpler acceptable proof path:* Many students will more directly write:
$$x\in A\cap(B-C) \iff x\in A\land x\in B\land x\notin C$$
$$x\in(A\cap B)-(A\cap C) \iff (x\in A\land x\in B)\land\neg(x\in A\land x\in C)$$
$$\iff (x\in A\land x\in B)\land(x\notin A\lor x\notin C)$$
$$\iff [(x\in A\land x\in B)\land x\notin A] \lor [(x\in A\land x\in B)\land x\notin C]$$
$$\iff F \lor (x\in A\land x\in B\land x\notin C) = x\in A\land x\in B\land x\notin C$$

Both match. Award full credit for either valid path.

---

### Problem 3 (5 points)

**Counterexample:** $A=\{1,2\}$, $B=\{2\}$.

$A-B = \{1\}$. $\mathcal{P}(A-B) = \mathcal{P}(\{1\}) = \{\emptyset,\{1\}\}$.

$\mathcal{P}(A) = \{\emptyset,\{1\},\{2\},\{1,2\}\}$. $\mathcal{P}(B)=\{\emptyset,\{2\}\}$.

$\mathcal{P}(A)-\mathcal{P}(B) = \{\{1\},\{1,2\}\}$ (removing $\emptyset$ and $\{2\}$ from $\mathcal{P}(A)$).

$\{\emptyset,\{1\}\} \neq \{\{1\},\{1,2\}\}$ — in fact $\emptyset\in\mathcal{P}(A-B)$ but $\emptyset\notin\mathcal{P}(A)-\mathcal{P}(B)$ (since $\emptyset\in\mathcal{P}(B)$, it gets removed).

The claim is FALSE. ∎

*Grading: 3 pts for correct sets and computation on both sides. 2 pts for identifying the specific discrepancy.*

*Note: $\emptyset$ is ALWAYS an element of $\mathcal{P}(X)-\mathcal{P}(Y)$ only if $\emptyset\notin\mathcal{P}(Y)$, but $\emptyset\in\mathcal{P}(Y)$ for every set Y (since $\emptyset\subseteq Y$ always) — so $\emptyset$ is NEVER in $\mathcal{P}(A)-\mathcal{P}(B)$ for any B, while $\emptyset$ IS always in $\mathcal{P}(A-B)$ (since $\emptyset\subseteq A-B$ always). This means the claimed identity fails for ANY nonempty B — a nice general observation for students who find it.*

---

### Problem 4 (4 points)

**(a)** (2 pts) $\mathcal{P}(\{1,2,3\}) = \{\emptyset,\{1\},\{2\},\{3\},\{1,2\},\{1,3\},\{2,3\},\{1,2,3\}\}$ — 8 elements.

**(b)** (2 pts) $|P\cup Pa| = 50+40-25=65$. Neither: $80-65=\mathbf{15}$.

---

### Grade Distribution

| Score | Interpretation |
|---|---|
| 18–20 | Mastered set theory |
| 14–17 | Solid; review element-chasing precision |
| 10–13 | Re-read Lectures 4.1–4.3; redo PS4 |
| < 10 | Schedule office hours before Week 5 |

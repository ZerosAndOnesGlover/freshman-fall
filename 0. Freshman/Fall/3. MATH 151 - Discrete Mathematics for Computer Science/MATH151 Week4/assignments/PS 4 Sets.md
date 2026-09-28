# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 4 — Sets
### Released: Friday 23 October 2026, 14:00 (after the Friday lecture) | Due: Friday 30 October 2026, 17:00 (Week 5)

---

**Instructions:**
- For proofs of set identities, choose either element-chasing or algebraic (law-based) proof, and state which you are using.
- For disproofs, provide explicit sets as counterexamples and show the computation.
- Show all work.
- Submit as a single PDF.

**Expected time:** about 3 hours. **Scoring:** 100 points total.

---

## Part A — Basic Set Operations (24 points)

**A1.** (12 pts) Let $U = \{1,\ldots,15\}$, $A = \{1,3,5,7,9,11,13,15\}$, $B = \{2,3,5,7,11,13\}$, $C = \{1,2,3,4,5,6,7\}$.

Compute:
- (a) $A \cap B$
- (b) $A - C$
- (c) $A \oplus C$
- (d) $\overline{A \cup B}$

---

**A2.** (12 pts) Determine whether each statement is TRUE or FALSE for all sets $A, B, C$. If FALSE, give a specific counterexample with explicit sets.

- (a) $A - (B - C) = (A - B) - C$
- (b) If $A \cup B = A \cup C$, then $B = C$.
- (c) If $A \cap B = A \cap C$ and $A \cup B = A \cup C$, then $B = C$.

---

## Part B — Set Identity Proofs (16 points)

**B1.** (16 pts) Prove each identity. State whether you use element-chasing or algebraic proof.

**(a)** $(A \cup B) - C = (A - C) \cup (B - C)$

**(b)** $A \cap (B \oplus C) = (A \cap B) \oplus (A \cap C)$

---

## Part C — Subset Proofs (12 points)

**C1.** (12 pts) Prove each subset relationship.

**(a)** If $A \subseteq B$ and $C \subseteq D$, then $A \cap C \subseteq B \cap D$.

**(b)** $A \times B \subseteq (A \cup C) \times (B \cup D)$

---

## Part D — Power Sets and Cartesian Products (24 points)

**D1.** (12 pts) Let $A = \{a, b, c\}$.

- (a) List all elements of $\mathcal{P}(A)$.
- (b) How many elements of $\mathcal{P}(A)$ have exactly 2 elements?
- (c) Verify $|\mathcal{P}(A)| = 2^{|A|}$.

---

**D2.** (12 pts) Prove: for any sets $A$ and $B$, $A \subseteq B$ if and only if $\mathcal{P}(A) \subseteq \mathcal{P}(B)$.

---

## Part E — Inclusion-Exclusion and Cardinality (24 points)

**E1.** (12 pts) In a group of 200 students: 120 study French, 100 study Spanish, 40 study both. How many study neither?

---

**E2.** (12 pts) Among integers from 1 to 500: how many are divisible by 2, 3, or 5?

*(Use the three-set Inclusion-Exclusion formula.)*

---

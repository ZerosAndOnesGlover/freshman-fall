# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 4 — Sets
### Released: Friday 23 October 2026, 14:00 (after the Friday lecture) | Due: Friday 30 October 2026, 17:00 (Week 5)

---

> *Revised 2026-09-21.* The optional bonus section was removed to keep the set to 100 points of
> this week's material.

**Instructions:**
- For proofs of set identities, choose either element-chasing or algebraic (law-based) proof, and state which you are using.
- For disproofs, provide explicit sets as counterexamples and show the computation.
- Show all work.
- Submit as a single PDF.

**Scoring:** 100 points total.

---

## Part A — Basic Set Operations (16 points)

**A1.** (8 pts) Let $U = \{1,\ldots,15\}$, $A = \{1,3,5,7,9,11,13,15\}$, $B = \{2,3,5,7,11,13\}$ (primes and 1 within range... actually just use as given), $C = \{1,2,3,4,5,6,7\}$.

Compute:
- (a) $A \cap B$
- (b) $B \cup C$
- (c) $A - C$
- (d) $\overline{B}$
- (e) $A \oplus C$
- (f) $(A \cap B) \cup (B \cap C)$
- (g) $\overline{A \cup B}$
- (h) $\overline{A} \cap \overline{B}$ — verify this equals your answer to (g)

---

**A2.** (8 pts) Determine whether each statement is TRUE or FALSE for all sets $A, B, C$. If FALSE, give a specific counterexample with explicit sets.

- (a) $A - (B - C) = (A - B) - C$
- (b) $A \times (B \cup C) = (A \times B) \cup (A \times C)$
- (c) If $A \cup B = A \cup C$, then $B = C$.
- (d) If $A \cap B = A \cap C$ and $A \cup B = A \cup C$, then $B = C$.

---

## Part B — Set Identity Proofs (28 points)

**B1.** (7 pts each) Prove each identity. State whether you use element-chasing or algebraic proof.

**(a)** $A \cup (A \cap B) = A$ (Absorption Law)

**(b)** $(A \cup B) - C = (A - C) \cup (B - C)$

**(c)** $A \cap (B \oplus C) = (A \cap B) \oplus (A \cap C)$

**(d)** $\overline{A - B} = \overline{A} \cup B$

---

## Part C — Subset Proofs (16 points)

**C1.** (4 pts each) Prove each subset relationship.

**(a)** $A \cap B \subseteq A$

**(b)** $A \subseteq A \cup B$

**(c)** If $A \subseteq B$ and $C \subseteq D$, then $A \cap C \subseteq B \cap D$.

**(d)** $A \times B \subseteq (A \cup C) \times (B \cup D)$

---

## Part D — Power Sets and Cartesian Products (24 points)

**D1.** (6 pts) Let $A = \{a, b, c\}$.

- (a) List all elements of $\mathcal{P}(A)$.
- (b) How many elements of $\mathcal{P}(A)$ have exactly 2 elements?
- (c) Verify $|\mathcal{P}(A)| = 2^{|A|}$.

---

**D2.** (6 pts) Prove: for any sets $A$ and $B$, $A \subseteq B$ if and only if $\mathcal{P}(A) \subseteq \mathcal{P}(B)$.

---

**D3.** (6 pts) Let $A = \{1, 2\}$ and $B = \{3, 4\}$.

- (a) Compute $A \times B$ and $B \times A$. Are they equal?
- (b) Compute $(A \times B) \cap (B \times A)$.
- (c) Compute $A \times (B \times A)$ — is this the same as $(A \times B) \times A$? Discuss (these produce different structures — nested tuples vs. flat triples — a subtlety worth understanding).

---

**D4.** (6 pts) Prove: $\mathcal{P}(A) \cap \mathcal{P}(B) = \mathcal{P}(A \cap B)$ for all sets $A, B$.

---

## Part E — Inclusion-Exclusion and Cardinality (16 points)

**E1.** (4 pts) In a group of 200 students: 120 study French, 100 study Spanish, 40 study both. How many study neither?

---

**E2.** (4 pts) Among integers from 1 to 300: how many are divisible by 3 or 5?

*(Hint: Let $A$ = multiples of 3, $B$ = multiples of 5. Compute $|A|$, $|B|$, $|A\cap B|$ using floor division.)*

---

**E3.** (4 pts) Among integers from 1 to 500: how many are divisible by 2, 3, or 5?

*(Use the three-set Inclusion-Exclusion formula.)*

---

**E4.** (4 pts) A survey of 150 people about three products A, B, C found:
- 80 use product A, 70 use product B, 60 use product C
- 30 use both A and B, 25 use both A and C, 20 use both B and C
- 10 use all three products

How many people use **exactly one** of the three products?

*(Hint: first find $|A \cup B \cup C|$, then think carefully about how to isolate "exactly one" — you may need to compute the number using exactly-two and exactly-three counts and subtract.)*

# MATH 151 — Discrete Mathematics for Computer Science
## Quiz 5 — Scope Preview
### Quiz administered: Monday, Week 5 (first 15 minutes of lecture)

---

**Coverage:** Weeks 4 and 5 material:
- Week 4: Sets — operations, identities, power sets, Cartesian products, Inclusion-Exclusion
- Week 5: Functions — injective, surjective, bijective; composition, inverse (covered next week)

---

## What You Must Know Cold for Week 4 Material

### 1. Set Operation Definitions

| Operation | Membership Condition |
|---|---|
| $A \cup B$ | $x\in A \lor x\in B$ |
| $A \cap B$ | $x\in A \land x\in B$ |
| $A - B$ | $x\in A \land x\notin B$ |
| $\overline{A}$ | $x\notin A$ |
| $A \oplus B$ | in exactly one of $A, B$ |

### 2. The Full Identity Table

Know these by heart, and know they mirror propositional logic exactly:
- Identity, Domination, Idempotent, Complementation
- Commutative, Associative, Distributive
- **De Morgan's Laws** (most commonly tested)
- Absorption
- $A - B = A \cap \overline{B}$ (difference identity — use this to reduce any difference expression)

### 3. Proof Techniques

**Element-chasing:** Let $x$ be arbitrary. Show $x\in X \iff x\in Y$ (or $\rightarrow$ for subset proofs) via a chain of logical equivalences citing set definitions and logic laws.

**Algebraic:** Chain the known identities directly.

**Disproof:** One explicit counterexample with specific sets suffices.

### 4. Power Sets

- $|\mathcal{P}(A)| = 2^{|A|}$ — know the inductive proof
- $\emptyset$ and $A$ are always elements of $\mathcal{P}(A)$
- $\mathcal{P}(A) \cap \mathcal{P}(B) = \mathcal{P}(A\cap B)$ — TRUE
- $\mathcal{P}(A) \cup \mathcal{P}(B) = \mathcal{P}(A\cup B)$ — FALSE in general

### 5. Cartesian Products

- $A \times B = \{(a,b) : a\in A, b\in B\}$
- $|A\times B| = |A|\cdot|B|$
- $A\times B \neq B\times A$ in general (NOT commutative)
- $(a,b) = (c,d) \iff a=c \land b=d$

### 6. Inclusion-Exclusion

- Two sets: $|A\cup B| = |A|+|B|-|A\cap B|$
- Three sets: $|A\cup B\cup C| = |A|+|B|+|C|-|A\cap B|-|A\cap C|-|B\cap C|+|A\cap B\cap C|$

---

## Sample Quiz 5 Problems (Week 4 portion)

**Problem 1.** (4 pts) Given specific sets, compute $A\cup B$, $A\cap C$, $\overline{A-B}$.

**Problem 2.** (5 pts) Prove by element-chasing: $A - (B\cup C) = (A-B)\cap(A-C)$.

**Problem 3.** (4 pts) Disprove: $A\times(B-C) = (A\times B) - (A\times C)$... *(actually this one is TRUE — study which product/difference identities hold!)*

**Problem 4.** (4 pts) In a group of 120: 70 like hiking, 50 like swimming, 25 like both. How many like neither?

**Problem 5.** (4 pts) From Week 5 — function properties (see Week 5 materials).

---

## Study Recommendations

1. **Memorize the identity table** — flashcard style. Given a name (e.g., "De Morgan's"), write the formula. Given a formula, name it.

2. **Practice element-chasing on 5 different identities** without looking at solutions. This is the single most tested skill.

3. **Know the difference identity** $A-B = A\cap\overline{B}$ — it's the bridge that lets you apply all the ∩/∪/complement laws to difference expressions.

4. **Practice power set size computations** for sets up to 6 elements, both by listing and by the $2^n$ formula.

5. **Do PS4 completely**, especially the disproof problems — quizzes love asking you to find counterexamples for plausible-but-false identities.

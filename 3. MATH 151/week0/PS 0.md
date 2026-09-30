---
assessment: PS 0
course: MATH 151
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-09-30
submitted: 2026-09-30
graded: 2026-09-30
source: "PS 0 Propositional Logic.md"
---

# MATH 151 · PS 0
## Answer Sheet

**Assessment:** `PS 0 Propositional Logic.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Problem 1 — Propositions  (9 points)

**Question 1(a).** "Every prime number greater than 2 is odd."

**Answer.** **A proposition, and it is TRUE.** It is a declarative sentence with a definite truth value. Proof: if a prime p > 2 were even, then 2 would divide p with 2 ≠ p and 2 ≠ 1, so p would not be prime. That is a contradiction, so every prime greater than 2 is odd.

**Question 1(b).** "x² − 4 = 0"

**Answer.** **Not a proposition.** The variable x is free (no value is assigned), so the sentence has no fixed truth value. It is true for x = 2 or x = −2 and false for every other value, for example x = 0. It becomes a proposition only after x is given a value, or after x is bound by a quantifier (Week 1: it is an open sentence, or predicate, P(x)).

**Question 1(c).** "Prove that 1 + 1 = 2."

**Answer.** **Not a proposition.** It is an imperative (a command). It asserts nothing, so it cannot be true or false. (The embedded sentence "1 + 1 = 2" *is* a proposition, and it is true, but the sentence as a whole is an instruction.)

*Marks: 9 / 9*

---

### Problem 2 — Translation and Negation  (12 points)

p = "The network is connected.", q = "The server is running.", r = "The database is reachable.", s = "The user can log in."

**Question 2(a).** "The user can log in if and only if the network is connected and the server is running."

**Answer.**
- Formula: **s ↔ (p ∧ q)**
- Negation:

```
¬(s ↔ (p ∧ q))
≡ (s ∧ ¬(p ∧ q)) ∨ (¬s ∧ (p ∧ q))      Negation of Biconditional
≡ (s ∧ (¬p ∨ ¬q)) ∨ (¬s ∧ p ∧ q)        De Morgan's Law; Associativity
```

**¬ ≡ (s ∧ (¬p ∨ ¬q)) ∨ (¬s ∧ p ∧ q)**. In English: "Either the user can log in even though the network is down or the server is not running, or the user cannot log in even though the network is connected and the server is running."

**Question 2(b).** "If the network is connected and the server is running, then the database is reachable and the user can log in."

**Answer.**
- Formula: **(p ∧ q) → (r ∧ s)**
- Negation:

```
¬((p ∧ q) → (r ∧ s))
≡ (p ∧ q) ∧ ¬(r ∧ s)          Negation of Conditional: ¬(a → b) ≡ a ∧ ¬b
≡ p ∧ q ∧ (¬r ∨ ¬s)           De Morgan's Law; Associativity
```

**¬ ≡ p ∧ q ∧ (¬r ∨ ¬s)**. In English: "The network is connected and the server is running, but the database is unreachable or the user cannot log in."

**Question 2(c).** "The user cannot log in unless the network is connected."

**Answer.** "A unless B" means ¬B → A (Lecture 0). Here A = ¬s and B = p.
- Formula: **¬p → ¬s**, which is equivalent to **s → p** (Contrapositive) and to **¬s ∨ p** (Conditional Elimination). In words: logging in requires the network to be connected.
- Negation:

```
¬(¬s ∨ p)
≡ ¬¬s ∧ ¬p        De Morgan's Law
≡ s ∧ ¬p          Double Negation
```

**¬ ≡ s ∧ ¬p**. In English: "The user can log in, but the network is not connected."

*Marks: 12 / 12*

---

### Problem 3 — Truth Tables  (18 points)

**Question 3(a).** (p → q) ∧ (q → p)

**Answer.**

| p | q | p → q | q → p | (p → q) ∧ (q → p) |
|---|---|---|---|---|
| T | T | T | T | **T** |
| T | F | F | T | **F** |
| F | T | T | F | **F** |
| F | F | T | T | **T** |

**Question 3(b).** (p ∨ q) → (p ∧ q)

**Answer.**

| p | q | p ∨ q | p ∧ q | (p ∨ q) → (p ∧ q) |
|---|---|---|---|---|
| T | T | T | T | **T** |
| T | F | T | F | **F** |
| F | T | T | F | **F** |
| F | F | F | F | **T** |

**Question 3(c).** (p → q) → ((p → ¬q) → ¬p)

**Answer.** Let A = p → q, B = p → ¬q, C = B → ¬p.

| p | q | ¬p | ¬q | A: p → q | B: p → ¬q | C: B → ¬p | A → C |
|---|---|---|---|---|---|---|---|
| T | T | F | F | T | F | T | **T** |
| T | F | F | T | F | T | F | **T** |
| F | T | T | F | T | T | T | **T** |
| F | F | T | T | T | T | T | **T** |

**Question 3(d).** Which are tautologies, contradictions, or contingencies? Which connective is (a)?

**Answer.**
- **(a) is a contingency** (T in rows 1 and 4, F in rows 2 and 3). Its column is T exactly when p and q have the same truth value, so it is the **biconditional p ↔ q**. This is the Biconditional Expansion law p ↔ q ≡ (p → q) ∧ (q → p).
- **(b) is a contingency** (same column, TFFT). So (b) is also equivalent to p ↔ q. That makes sense: "if at least one holds, then both hold" rules out exactly the rows where one is true and the other is false.
- **(c) is a tautology** (all T). It is the pattern of proof by contradiction (reductio): if p implies q and p also implies ¬q, then p must be false.
- **None of the three is a contradiction.** Every column contains at least one T.

*Marks: 18 / 18*

---

### Problem 4 — Converse, Inverse, Contrapositive  (12 points)

**Question 4(a).** "If a number is divisible by 4, then it is divisible by 2."

**Answer.** Let p = "n is divisible by 4" and q = "n is divisible by 2". The original p → q is TRUE: if n = 4k then n = 2(2k).

- (i) **Converse** (q → p): "If a number is divisible by 2, then it is divisible by 4." **FALSE.** Counterexample: n = 6 (6 = 2 · 3, but 6/4 = 1.5).
- (ii) **Inverse** (¬p → ¬q): "If a number is not divisible by 4, then it is not divisible by 2." **FALSE.** Same counterexample: 6 is not divisible by 4 but is divisible by 2.
- (iii) **Contrapositive** (¬q → ¬p): "If a number is not divisible by 2, then it is not divisible by 4." **TRUE.**

**Only the contrapositive is logically equivalent to the original** (p → q ≡ ¬q → ¬p). The converse and inverse are equivalent to *each other*, because the inverse is the contrapositive of the converse. That is why n = 6 refutes both at once.

**Question 4(b).** p → (q ∧ r)

**Answer.**
- (i) **Converse:** (q ∧ r) → p
- (ii) **Inverse:** ¬p → ¬(q ∧ r) ≡ **¬p → (¬q ∨ ¬r)** (De Morgan's Law)
- (iii) **Contrapositive:** ¬(q ∧ r) → ¬p ≡ **(¬q ∨ ¬r) → ¬p** (De Morgan's Law)

**Only the contrapositive is equivalent to p → (q ∧ r).** The converse and inverse are equivalent to each other but not to the original. Witness row: p = F, q = T, r = T. Here the original is T (false hypothesis), but the converse is T → F = F. The inverse is also F in this row: ¬p = T while ¬q ∨ ¬r = F.

*Marks: 12 / 12*

---

### Problem 5 — Proofs by Laws  (21 points)

**Question 5(a).** (p ∧ q) ∨ (p ∧ ¬q) ≡ p

**Answer.**

```
(p ∧ q) ∨ (p ∧ ¬q)
≡ p ∧ (q ∨ ¬q)        Distributivity (read right-to-left)
≡ p ∧ T               Complement Law (Excluded Middle)
≡ p                   Identity Law                          ∎
```

**Question 5(b).** (p → q) ∧ (p → ¬q) ≡ ¬p

**Answer.**

```
(p → q) ∧ (p → ¬q)
≡ (¬p ∨ q) ∧ (¬p ∨ ¬q)    Conditional Elimination (twice)
≡ ¬p ∨ (q ∧ ¬q)           Distributivity (read right-to-left)
≡ ¬p ∨ F                  Complement Law (Non-Contradiction)
≡ ¬p                      Identity Law                      ∎
```

(This is the algebraic version of the tautology in Problem 3(c): if p implies both q and ¬q, then p is false.)

**Question 5(c).** ¬(p ↔ q) ≡ (p ∧ ¬q) ∨ (¬p ∧ q)

**Answer.**

```
¬(p ↔ q)
≡ ¬((p → q) ∧ (q → p))              Biconditional Expansion
≡ ¬((¬p ∨ q) ∧ (¬q ∨ p))            Conditional Elimination (twice)
≡ ¬(¬p ∨ q) ∨ ¬(¬q ∨ p)             De Morgan's Law (∧ form)
≡ (¬¬p ∧ ¬q) ∨ (¬¬q ∧ ¬p)           De Morgan's Law (∨ form, twice)
≡ (p ∧ ¬q) ∨ (q ∧ ¬p)               Double Negation (twice)
≡ (p ∧ ¬q) ∨ (¬p ∧ q)               Commutativity                ∎
```

*Marks: 21 / 21*

---

### Problem 6 — Normal Forms  (16 points)

**Question 6(a).** Convert p → q to CNF.

**Answer.**

```
p → q
≡ ¬p ∨ q          Conditional Elimination
```

**CNF: ¬p ∨ q.** This is a conjunction of one clause, and that clause is a disjunction of the literals ¬p and q, so it is already in CNF.

**Question 6(b).** Convert p ↔ q to CNF. Show all steps.

**Answer.**

```
p ↔ q
≡ (p → q) ∧ (q → p)         Biconditional Expansion
≡ (¬p ∨ q) ∧ (¬q ∨ p)       Conditional Elimination (twice)
≡ (¬p ∨ q) ∧ (p ∨ ¬q)       Commutativity (tidy ordering)
```

**CNF: (¬p ∨ q) ∧ (p ∨ ¬q).** It has two clauses, each a disjunction of literals, joined by ∧. Check: the first clause is false only at p = T, q = F, and the second only at p = F, q = T. These are exactly the two rows where p ↔ q is false.

**Question 6(c).** Convert p ∧ (q ∨ ¬r) to DNF using the truth table method.

**Answer.**

| p | q | r | ¬r | q ∨ ¬r | p ∧ (q ∨ ¬r) | minterm |
|---|---|---|---|---|---|---|
| T | T | T | F | T | **T** | p ∧ q ∧ r |
| T | T | F | T | T | **T** | p ∧ q ∧ ¬r |
| T | F | T | F | F | F | |
| T | F | F | T | T | **T** | p ∧ ¬q ∧ ¬r |
| F | T | T | F | T | F | |
| F | T | F | T | T | F | |
| F | F | T | F | F | F | |
| F | F | F | T | T | F | |

Take one minterm per T row. Each variable appears plain if it is T in that row and negated if it is F. Then join the minterms with ∨:

**DNF: (p ∧ q ∧ r) ∨ (p ∧ q ∧ ¬r) ∨ (p ∧ ¬q ∧ ¬r)**

(Check by laws: the first two minterms combine to p ∧ q, since (p ∧ q ∧ r) ∨ (p ∧ q ∧ ¬r) ≡ (p ∧ q) ∧ (r ∨ ¬r) ≡ p ∧ q. The whole formula then simplifies to the shorter DNF (p ∧ q) ∨ (p ∧ ¬r), which is exactly Distributivity applied to p ∧ (q ∨ ¬r).)

*Marks: 16 / 16*

---

### Problem 7 — Functional Completeness  (12 points)

**Question 7(a).** Show {¬, ∨} is functionally complete: express p ∧ q using only ¬ and ∨.

**Answer.**

```
p ∧ q
≡ ¬¬(p ∧ q)          Double Negation
≡ ¬(¬p ∨ ¬q)         De Morgan's Law
```

**p ∧ q ≡ ¬(¬p ∨ ¬q)**, which uses only ¬ and ∨.

Why this proves completeness: {¬, ∧, ∨} is functionally complete, because every truth function has a DNF read off its truth table (Problem 6(c)). Rewrite that DNF, replacing every ∧ with the ¬/∨ form above. The result is an equivalent formula that uses only ¬ and ∨. So every truth function can be expressed with {¬, ∨}.

**Question 7(b).** Show {¬, →} is functionally complete: express p ∨ q using only ¬ and →.

**Answer.**

```
¬p → q
≡ ¬¬p ∨ q            Conditional Elimination
≡ p ∨ q              Double Negation
```

**p ∨ q ≡ ¬p → q**, which uses only ¬ and →.

Why this proves completeness: by (a), {¬, ∨} is functionally complete. Every ∨ can be replaced by ¬ and → using the identity above, so every truth function can be expressed with {¬, →}. Concretely, ∧ can also be written directly: p ∧ q ≡ ¬(¬p ∨ ¬q) ≡ ¬(p → ¬q), where the second step uses Conditional Elimination and Double Negation (¬p ∨ ¬q ≡ p → ¬q).

*Marks: 12 / 12*

---

## Grading Summary

| | |
|---|---|
| **Score** | **100 / 100** |
| **Percent** | 100% |
| **Graded** | 2026-09-30 |

**Feedback:**

Every problem is correct, and every proof step cites the law it uses — the two things the
handout actually asks for. Nothing was marked down.

| Problem | Marks | |
|---|---|---|
| 1 · Propositions | 9 / 9 | Classification and truth values all right, including the open-sentence point in (b) and the imperative in (c). |
| 2 · Translation and Negation | 12 / 12 | (a) (b) (c) formulas match the key; all three negations pushed inward with De Morgan as required. |
| 3 · Truth Tables | 18 / 18 | All twelve columns re-derived independently; (a) TFFT, (b) TFFT, (c) all-T. Classification and the biconditional identification correct. |
| 4 · Converse/Inverse/Contrapositive | 12 / 12 | n = 6 refutes converse and inverse together, and 4(b) gives a witness row (p=F, q=T, r=T) checked in all three readings. |
| 5 · Proofs by Laws | 21 / 21 | No truth tables used, as required; all three chains valid step by step. |
| 6 · Normal Forms | 16 / 16 | CNF and DNF both match the key; the minterm method is applied correctly in 6(c). |
| 7 · Functional Completeness | 12 / 12 | Both expressions correct, and the completeness argument is given rather than assumed. |

**The work was verified independently, then against `PS 0 Solutions.md`.** Every truth
table and every equivalence in this sheet was recomputed before the key was opened, and the
three formulas that the key carries under the old numbering — B1(a) (the truth table in
3(a)), B1(c) (the table in 3(b)) and B1(d) (the table in 3(c)) — agree row for row, as do
A1(a), A1(c), A1(f), A2(a)–(c), C1(a), C1(c), D1(a)–(c), D2(a)–(b), D3(a) and D4(a)–(b).
2(c) is the one worth naming: "A unless B" ≡ ¬B → A gives ¬p → ¬s, and the negation
s ∧ ¬p follows, which is what the key gives.

**Three places where the answer goes past the question.** 4(a) explains *why* one
counterexample kills two readings at once — the inverse is the contrapositive of the
converse — which is the reason the key only has to cite n = 6. 6(c) checks its own minterm
DNF by simplifying it back down to (p ∧ q) ∨ (p ∧ ¬r), the same independent verification
D3(a) performs. 7(a) and 7(b) do not stop at "express ∧" and "express ∨": each closes the
completeness argument by noting that every truth function has a DNF, so rewriting the ∧s is
sufficient. That is the step the exercise is actually testing, and it is the step most often
skipped.

**One note, not charged.** In 2(c) the negation is taken from the disjunctive form ¬s ∨ p
rather than from the stated ¬p → ¬s. The two are equivalent and the result is right, but
writing the bridge (¬p → ¬s ≡ ¬¬p ∨ ¬s ≡ p ∨ ¬s) would make the answer readable without the
eye doing the substitution. One line, and the answer sheet would be airtight as well as
correct.

*Graded against `PS 0 Propositional Logic.md` and `PS 0 Solutions.md`.*


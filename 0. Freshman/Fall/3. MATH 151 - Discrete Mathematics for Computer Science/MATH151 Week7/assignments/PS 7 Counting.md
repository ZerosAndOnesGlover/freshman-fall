# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 7 — Counting
### Released: Friday 13 November 2026, 14:00 (after the Friday lecture) | Due: Friday 20 November 2026, 17:00 (Week 8)

---

**Instructions:**
- For every problem, explicitly state which counting scenario applies (order? repetition?) before computing.
- Show all arithmetic — do not skip factorial simplifications.
- For "at least" problems, show the complementary counting setup explicitly.
- Submit as a single PDF.

**Expected time:** about 3 hours. **Scoring:** 100 points total.

---

## Part A — Multiplication and Addition Rules (12 points)

**A1.** (4 pts each)

**(a)** A computer password must be 6 characters: the first 2 must be uppercase letters, the last 4 must be digits. How many passwords are possible?

**(b)** How many integers from 1 to 500 are divisible by 4 or by 6? *(Careful — check for overlap using the two-set Inclusion-Exclusion formula from Week 4.)*

**(c)** A binary string has length 8. How many such strings start with "11" or end with "00" (or both)?

---

## Part B — Permutations and Combinations (20 points)

**B1.** (4 pts each) For each problem, classify the scenario (order? repetition?) and compute the answer.

**(a)** How many ways can a 4-person executive committee (President, VP, Secretary, Treasurer — all distinct roles) be selected from a 15-person board?

**(b)** How many ways can a 4-person subcommittee (no distinct roles) be selected from a 15-person board?

**(c)** How many distinct 7-character strings can be formed using only the letters A, B, C (repetition allowed)?

**(d)** How many distinct arrangements are there of the letters in "ENGINEERING"?

**(e)** How many ways can 12 identical chairs be distributed among 4 distinguishable classrooms (some classrooms may get 0 chairs)?

---

## Part C — Combined Multi-Step Problems (30 points)

**C1.** (10 pts) A 5-card poker hand is dealt from a standard 52-card deck. How many 5-card hands contain **exactly 3 kings**? *(There are 4 kings in the deck; you need exactly 3 of them, plus 2 non-king cards.)*

---

**C2.** (10 pts) A committee of 6 people is to be selected from a group of 8 men and 5 women. How many committees have **at least 4 women**?

---

**C3.** (10 pts) In how many ways can 10 people be divided into two groups of 5 for a game, if the two groups are considered **unlabeled** (i.e., "Group A vs Group B" is the same split as "Group B vs Group A")?

*(Hint: first count assuming the groups ARE labeled/distinguishable, then correct for the overcounting.)*

---

## Part D — Binomial Theorem and Identities (28 points)

**D1.** (8 pts) Find the coefficient of $x^7y^5$ in the expansion of $(2x-y)^{12}$.

---

**D2.** (8 pts) Prove using the Binomial Theorem (algebraic substitution, not induction): $\sum_{k=0}^{n}\binom{n}{k}3^k = 4^n$.

---

**D3.** (12 pts) Give a **combinatorial proof** (count the same set two ways — do NOT use algebra) of the identity: $r\binom{n}{r} = n\binom{n-1}{r-1}$.

*Hint: Consider choosing a committee of size $r$ from $n$ people, AND designating one committee member as chair. Count this two ways.*

---

## Part E — The Four-Fold Way (10 points)

**E1.** *(10 pts)* Selecting $r$ items from $n$ types splits into four cases according to whether
**order matters** and whether **repetition is allowed**. Complete the table, giving the formula and
its value for $n=5$, $r=3$.

| | No repetition | Repetition allowed |
|---|---|---|
| **Order matters** | | |
| **Order does not matter** | | |

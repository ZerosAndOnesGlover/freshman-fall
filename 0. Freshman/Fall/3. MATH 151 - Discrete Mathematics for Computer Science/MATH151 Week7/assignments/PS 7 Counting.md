# MATH 151 — Discrete Mathematics for Computer Science
## Problem Set 7 — Counting
### Released: Friday, Week 7 | Due: Friday, Week 8 (11:59 PM)

---

**Instructions:**
- For every problem, explicitly state which counting scenario applies (order? repetition?) before computing.
- Show all arithmetic — do not skip factorial simplifications.
- For "at least" problems, show the complementary counting setup explicitly.
- Submit as a single PDF.

**Scoring:** 100 points total.

---

## Part A — Multiplication and Addition Rules (20 points)

**A1.** (4 pts each)

**(a)** A restaurant offers 5 appetizers, 8 entrees, 4 desserts, and 3 drinks. How many different 4-course meals (one item from each category) are possible?

**(b)** A computer password must be 6 characters: the first 2 must be uppercase letters, the last 4 must be digits. How many passwords are possible?

**(c)** How many integers from 1 to 500 are divisible by 4 or by 6? *(Careful — check for overlap using Inclusion-Exclusion.)*

**(d)** A binary string has length 8. How many such strings start with "11" or end with "00" (or both)?

**(e)** How many 5-digit numbers (first digit cannot be 0) have at least one digit equal to 7?

---

## Part B — Permutations and Combinations (32 points)

**B1.** (4 pts each) For each problem, classify the scenario (order? repetition?) and compute the answer.

**(a)** How many ways can 6 books be arranged on a shelf?

**(b)** How many ways can a 4-person executive committee (President, VP, Secretary, Treasurer — all distinct roles) be selected from a 15-person board?

**(c)** How many ways can a 4-person subcommittee (no distinct roles) be selected from a 15-person board?

**(d)** A vending machine offers 6 snack types. How many ways can you buy a bag containing 8 snacks total, allowing repeats, where order of selection doesn't matter?

**(e)** How many distinct 7-character strings can be formed using only the letters A, B, C (repetition allowed)?

**(f)** How many distinct arrangements are there of the letters in "ENGINEERING"?

**(g)** A pizza shop offers 10 toppings. How many different pizzas can be made using exactly 3 distinct toppings (order irrelevant, no repeats)?

**(h)** How many ways can 12 identical chairs be distributed among 4 distinguishable classrooms (some classrooms may get 0 chairs)?

---

## Part C — Combined Multi-Step Problems (24 points)

**C1.** (6 pts) A 5-card poker hand is dealt from a standard 52-card deck. How many 5-card hands contain **exactly 3 kings**? *(There are 4 kings in the deck; you need exactly 3 of them, plus 2 non-king cards.)*

---

**C2.** (6 pts) A committee of 6 people is to be selected from a group of 8 men and 5 women. How many committees have **at least 4 women**?

---

**C3.** (6 pts) A license plate has 3 letters followed by 3 digits. How many license plates have **all distinct letters and all distinct digits**?

---

**C4.** (6 pts) In how many ways can 10 people be divided into two groups of 5 for a game, if the two groups are considered **unlabeled** (i.e., "Group A vs Group B" is the same split as "Group B vs Group A")?

*(Hint: first count assuming the groups ARE labeled/distinguishable, then correct for the overcounting.)*

---

## Part D — Binomial Theorem and Identities (16 points)

**D1.** (4 pts) Find the coefficient of $x^7y^5$ in the expansion of $(2x-y)^{12}$.

---

**D2.** (4 pts) Prove using the Binomial Theorem (algebraic substitution, not induction): $\sum_{k=0}^{n}\binom{n}{k}3^k = 4^n$.

---

**D3.** (4 pts) Give a **combinatorial proof** (count the same set two ways — do NOT use algebra) of the identity: $r\binom{n}{r} = n\binom{n-1}{r-1}$.

*Hint: Consider choosing a committee of size $r$ from $n$ people, AND designating one committee member as chair. Count this two ways.*

---

**D4.** (4 pts) Using Pascal's Triangle or the formula directly, verify that row 8 of Pascal's Triangle sums to $2^8=256$. Show the row explicitly and the sum.

---

---

## Part E — The Four-Fold Way (8 points)

**E1.** *(4 pts)* Selecting $r$ items from $n$ types splits into four cases according to whether
**order matters** and whether **repetition is allowed**. Complete the table, giving the formula and
its value for $n=5$, $r=3$.

| | No repetition | Repetition allowed |
|---|---|---|
| **Order matters** | | |
| **Order does not matter** | | |

**E2.** *(4 pts)* Classify each scenario into one of the four cases above, then compute it.

- (a) How many distinct arrangements of the letters of **BANANA**?
- (b) How many bit strings of length 8 contain exactly three 1s?

---

## Bonus (8 points — optional)

**Bonus 1.** (4 pts) How many ways can the letters of "COMBINATORICS" be arranged such that all the vowels (O, I, A, O, I) appear together as a contiguous block (in any order among themselves)?

*(Hint: treat the vowel-block as a single unit, arrange it with the remaining consonants, then separately count internal arrangements of the vowel block, accounting for repeated letters.)*

**Bonus 2.** (4 pts) Prove the Hockey Stick Identity $\sum_{i=r}^{n}\binom{i}{r}=\binom{n+1}{r+1}$ using **induction on $n$** (a different proof than the combinatorial one given in Friday's lecture). State your base case and inductive step clearly, citing Pascal's Rule where needed.

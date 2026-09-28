# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 8: Advanced Counting
### Released: Friday 20 November 2026, 14:00 (after the Friday lecture) | Due: Friday 27 November 2026, 17:00 (Week 9)

---

**Instructions:**
- For every Pigeonhole proof, **explicitly name the pigeons and the pigeonholes** before the argument. A proof without them scores at most half.
- For every inclusion–exclusion computation, state each intersection's size and how you obtained it.
- Show all work. Submit as a single PDF.

**Expected time:** about 3 hours. **Scoring:** 100 points total.

---

## Part A — Pigeonhole Principle (18 points)

**A1.** (6 pts each) Prove each claim using the Pigeonhole Principle. Clearly identify the "pigeons" and "pigeonholes" in your proof.

**(a)** Among any 6 integers chosen from $\{1,2,\ldots,20\}$, do two necessarily sum to 21? Determine whether this claim is true, and prove or disprove accordingly.
*(Careful: verify the pigeonhole partition is correctly sized for the claim to hold.)*

**(b)** A drawer contains 10 red socks, 10 blue socks, and 10 green socks, all mixed together (indistinguishable by touch). What is the minimum number of socks you must pull out to **guarantee** a matching pair? Prove your answer using Pigeonhole.

**(c)** Among any 100 integers, prove that some nonempty subset of them has a sum divisible by 100.
*(Hint: list the integers in any order and consider the 100 partial sums $a_1$, $a_1+a_2$, …, as in L24 Exercise 6. A block of consecutive terms is one kind of subset.)*

---

## Part B — Inclusion–Exclusion Computations (30 points)

**B1.** *(14 pts)* How many 8-character strings over the 62-character alphanumeric alphabet contain
**at least one digit and at least one uppercase letter**? Show the complement as a union and apply
inclusion–exclusion to it.

**B2.** *(16 pts)* Derive the formula for the number of **onto** functions from an $m$-set to an
$n$-set. Then compute the value for $m=6$, $n=3$ and sanity-check it against $3^6$.

---

## Part C — Derangements (28 points)

**C1.** *(8 pts)* Compute $D_4$ from the formula $D_n = n!\sum_{k=0}^{n}\frac{(-1)^k}{k!}$ and list
all $D_4$ derangements of $\{1,2,3,4\}$ explicitly to confirm the count.

**C2.** *(10 pts)* How many permutations of $\{1,\ldots,7\}$ fix **exactly two** elements?

**C3.** *(10 pts)* Verify the identity $\sum_{k=0}^{n}\binom{n}{k}D_{n-k} = n!$ for $n = 5$, using
the derangement values from Lecture 25. Explain in one sentence why the identity must hold.

---

## Part D — Choosing the Tool (24 points)

**D1.** *(12 pts)* Explain the difference between what Pigeonhole and inclusion–exclusion tell you.
Give one problem where Pigeonhole applies but inclusion–exclusion cannot, and one where the reverse
holds.

**D2.** *(12 pts)* The subset-sum argument in L24 Section 8 proves a collision exists but gives no way to find
it, and the search problem is NP-complete. Explain in a short paragraph why an existence proof can be
easy while the corresponding search is intractable.

---

## Grading

| Part | Topic | Points |
|---|---|---|
| A | Pigeonhole Principle | 18 |
| B | Inclusion–Exclusion | 30 |
| C | Derangements | 28 |
| D | Choosing the Tool | 24 |
| **Total** | | **100** |

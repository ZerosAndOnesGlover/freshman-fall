# MATH 151: Discrete Mathematics for Computer Science
## Problem Set 8: Advanced Counting
### Released: Friday, Week 8 | Due: Friday, Week 9 (11:59 PM)

---

**Instructions:**
- For every Pigeonhole proof, **explicitly name the pigeons and the pigeonholes** before the argument. A proof without them scores at most half.
- For every inclusion–exclusion computation, state each intersection's size and how you obtained it.
- Show all work. Submit as a single PDF.

**Scoring:** 100 points total, plus an optional 8-point bonus.

---

## Part A — Pigeonhole Principle (24 points)

**A1.** (4 pts each) Prove each claim using the Pigeonhole Principle. Clearly identify the "pigeons" and "pigeonholes" in your proof.

**(a)** In any group of 32 people, at least 3 share a birth month.
*(Use the Generalized Pigeonhole Principle.)*

**(b)** Among any 6 integers chosen from $\{1,2,\ldots,20\}$, do two necessarily sum to 21? Determine whether this claim is true, and prove or disprove accordingly.
*(Careful: verify the pigeonhole partition is correctly sized for the claim to hold.)*

**(c)** A drawer contains 10 red socks, 10 blue socks, and 10 green socks, all mixed together (indistinguishable by touch). What is the minimum number of socks you must pull out to **guarantee** a matching pair? Prove your answer using Pigeonhole.

**(d)** Among any 100 integers, prove that some nonempty subset of them has a sum divisible by 100.
*(Hint: consider partial sums, similar to the technique in Friday's Exercise 6, but the sum need not be over a contiguous subsequence here — reconsider what "pigeonholes" to use.)*

**(e)** Prove: in any sequence of 10 distinct integers between 1 and 100 (inclusive), there exist two disjoint nonempty subsequences (not necessarily contiguous) with the same sum. *(This is the same technique as Friday's Section 8 worked example — adapt it here with the specific numbers given, showing the full pigeonhole counting argument.)*

**(f)** A chess tournament has 17 players, and every pair of players plays exactly one game against each other (a round-robin). Prove that at least one player wins at least 8 games, OR loses at least 8 games (assume no draws — every game has a winner and loser).
*(Hint: Each player plays 16 games. Consider the number of wins for each player as a function into a set of possible win-counts.)*

---

---

## Part B — Inclusion–Exclusion Computations (28 points)

**B1.** *(6 pts)* How many integers in $\{1,\ldots,1000\}$ are divisible by 3, 5, or 7? How many by
none of them? State each intersection's divisor explicitly.

**B2.** *(6 pts)* In a group of 200 developers: 120 use Python, 90 use C, 70 use Rust; 45 use Python
and C, 30 use Python and Rust, 25 use C and Rust; 15 use all three.

- (a) How many use at least one?
- (b) How many use none?
- (c) How many use **exactly one**?

**B3.** *(8 pts)* How many 8-character strings over the 62-character alphanumeric alphabet contain
**at least one digit and at least one uppercase letter**? Show the complement as a union and apply
inclusion–exclusion to it.

**B4.** *(8 pts)* Derive the formula for the number of **onto** functions from an $m$-set to an
$n$-set. Then compute the value for $m=6$, $n=3$ and sanity-check it against $3^6$.

---

## Part C — Derangements (20 points)

**C1.** *(5 pts)* Compute $D_4$ from the formula $D_n = n!\sum_{k=0}^{n}\frac{(-1)^k}{k!}$ and list
all $D_4$ derangements of $\{1,2,3,4\}$ explicitly to confirm the count.

**C2.** *(5 pts)* How many permutations of $\{1,\ldots,7\}$ fix **exactly two** elements?

**C3.** *(5 pts)* Verify the identity $\sum_{k=0}^{n}\binom{n}{k}D_{n-k} = n!$ for $n = 5$, using
the derangement values from Lecture 8.2. Explain in one sentence why the identity must hold.

**C4.** *(5 pts)* The probability that a random permutation of $n$ objects is a derangement tends to
$1/e$. Using the table from Lecture 8.2, state the smallest $n$ for which $D_n/n!$ agrees with $1/e$
to three decimal places, and comment on how fast the convergence is.

---

## Part D — Choosing the Tool (28 points)

**D1.** *(4 pts each)* For each, state **which technique applies** and then solve it.

- (a) Show that among any 13 people, two share a birth month.
- (b) How many integers below 200 are divisible by 4 or 6?
- (c) How many 5-letter strings over $\{a,\ldots,z\}$ have no repeated letter?
- (d) Show that any 10 distinct integers from $\{1,\ldots,100\}$ contain two different non-empty subsets with the same sum.
- (e) In how many ways can $n$ hats be returned so that nobody receives their own?

**D2.** *(4 pts)* Explain the difference between what Pigeonhole and inclusion–exclusion tell you.
Give one problem where Pigeonhole applies but inclusion–exclusion cannot, and one where the reverse
holds.

**D3.** *(4 pts)* The subset-sum argument in D1(d) proves a collision exists but gives no way to find
it, and the search problem is NP-complete. Explain in a short paragraph why an existence proof can be
easy while the corresponding search is intractable.

---

## Bonus (8 points — optional)

**Bonus 1.** *(4 pts)* Prove the Ramsey result $R(3,3) = 6$: among any 6 people, three are mutual
acquaintances or three are mutual strangers. Then exhibit a 5-person configuration with neither,
showing 6 is the smallest such number.

**Bonus 2.** *(4 pts)* Prove that any 5 points inside a unit square include two within distance
$\frac{\sqrt2}{2}$. Construct the pigeonholes explicitly, and explain why the argument fails for 4
points.

---

## Grading

| Part | Topic | Points |
|---|---|---|
| A | Pigeonhole Principle | 24 |
| B | Inclusion–Exclusion | 28 |
| C | Derangements | 20 |
| D | Choosing the Tool | 28 |
| **Total** | | **100** |

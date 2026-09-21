# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 7.1 (L21) — The Multiplication Rule and Addition Rule
### Monday, Week 7

**Date:** Monday 9 November 2026 · 13:00–13:50 · Week 7

---

> **Core Question:** How do we systematically count the number of ways to perform a sequence of choices, or the number of outcomes in an "either/or" scenario?

---

## 1. The Multiplication Rule (Product Rule)

**Theorem (Multiplication Rule).** If a procedure can be broken into a sequence of $k$ independent steps, where step 1 can be done in $n_1$ ways, step 2 in $n_2$ ways, ..., step $k$ in $n_k$ ways (with the number of ways to perform each step not depending on choices made in previous steps), then the total number of ways to complete the entire procedure is:
$$n_1 \times n_2 \times \cdots \times n_k$$

**Why this is true (intuition, formalized via Cartesian products from Week 4):** Each way of completing the procedure corresponds to exactly one tuple $(x_1,x_2,\ldots,x_k)$ where $x_i$ is the choice made at step $i$. The set of all such tuples is precisely $S_1\times S_2\times\cdots\times S_k$, where $|S_i|=n_i$. By the Cartesian product cardinality formula (Week 4): $|S_1\times\cdots\times S_k|=n_1\times\cdots\times n_k$.

**This is why the Multiplication Rule is not a new axiom — it is a direct restatement of Cartesian product cardinality from Week 4, applied to a sequential-choice framing.**

---

## 2. Worked Examples — Multiplication Rule

### Example 1: License Plates

A license plate consists of 3 letters followed by 4 digits. How many distinct plates are possible?

**Solution.** 3 independent letter-choices (26 options each), then 4 independent digit-choices (10 options each):
$$26\times26\times26\times10\times10\times10\times10 = 26^3\times10^4 = 17576\times10000 = 175{,}760{,}000$$

### Example 2: Passwords

A password must be exactly 8 characters, each character being a lowercase letter, uppercase letter, or digit (62 total choices per position). How many possible passwords exist?

**Solution.** $62^8 = 218{,}340{,}105{,}584{,}896$ (about 218 trillion).

**CS connection:** This exact calculation is the basis of "keyspace size" analysis in security — it tells you how many guesses a brute-force attacker would need in the worst case, directly informing password policy design.

### Example 3: Counting Functions

How many functions $f: \{1,2,3\} \to \{a,b,c,d\}$ exist?

**Solution.** By the formal definition of function (Week 5), each of the 3 domain elements independently gets assigned one of 4 codomain elements. By the Multiplication Rule: $4\times4\times4 = 4^3 = 64$ functions.

**General fact:** the number of functions $f:A\to B$ (finite sets) is $|B|^{|A|}$.

### Example 4: Sequential Dependent Choices — When NOT to Directly Multiply

How many ways can we select a **president, vice president, and treasurer** from a group of 10 people (no one holds two positions)?

**Solution.** President: 10 choices. Vice president: 9 remaining choices (one person is already taken). Treasurer: 8 remaining choices.
$$10\times9\times8 = 720$$

**Key subtlety:** the number of choices for step 2 depends on what happened in step 1 — but it depends only on the *count* remaining (always 9, regardless of *who* was chosen first), not on the specific identity. This "conditional but count-invariant" dependency is exactly when the Multiplication Rule still applies cleanly. This calculation is a **permutation** — formalized Thursday.

---

## 3. The Addition Rule (Sum Rule)

**Theorem (Addition Rule).** If a task can be accomplished via one of $k$ mutually exclusive (disjoint) alternative methods, where method $i$ can be done in $n_i$ ways, then the total number of ways to accomplish the task is:
$$n_1+n_2+\cdots+n_k$$

**Why this is true:** This is exactly the cardinality-of-disjoint-union formula from Week 4: if $S_1,\ldots,S_k$ are pairwise disjoint finite sets representing the outcome sets of each method, $|S_1\cup\cdots\cup S_k| = |S_1|+\cdots+|S_k|$.

**Critical requirement — mutual exclusivity:** The methods must not overlap (no outcome achievable by two different methods should be double-counted). If they DO overlap, you need Inclusion-Exclusion (Week 4!) instead of simple addition.

---

## 4. Worked Examples — Addition Rule

### Example 5: Choosing a Representative

A department has 15 CS majors and 12 MATH majors (assume no student double-majors in both — mutually exclusive categories). How many ways can a single representative be chosen from either group?

**Solution.** $15+12=27$ ways (Addition Rule — the two groups are disjoint).

### Example 6: Where Overlap Breaks Simple Addition

How many integers from 1 to 100 are divisible by 3 or by 5?

**This is NOT simply $|A|+|B|$** because the categories overlap (multiples of 15 are counted in both). This is exactly the two-set Inclusion-Exclusion Principle from Week 4:
$$|A\cup B| = |A|+|B|-|A\cap B| = 33+20-6=47$$

**Lesson:** always verify mutual exclusivity before applying the plain Addition Rule. When categories overlap, fall back on Inclusion-Exclusion.

---

## 5. Combining Both Rules — Multi-Step Problems

Most real counting problems require BOTH rules together, often nested.

### Example 7: A Compound Problem

A computer science curriculum requires students to choose ONE of {2 algorithms electives} OR ONE of {3 systems electives} as their single elective requirement, AND separately choose exactly one required course from {calculus, discrete math} (both tracks always take this). How many total course-selection combinations exist?

**Solution.**
Step 1 (Addition Rule, disjoint elective categories): number of ways to satisfy the elective requirement $= 2+3=5$.
Step 2 (independent choice): number of ways to satisfy the required course $=2$.
Combine via Multiplication Rule (the two choices are made independently): $5\times2=10$.

### Example 8: Counting Strings with Restrictions

How many 5-character strings over the alphabet $\{A,B,C\}$ contain **at least one** occurrence of the letter $A$?

**Solution — indirect counting via complement (a powerful general technique):**

Total strings (no restriction): $3^5 = 243$.

Strings with **no** $A$ at all (every position is $B$ or $C$): $2^5=32$.

Strings with at least one $A$ = Total $-$ (strings with no $A$) $= 243-32=211$.

**Key technique — complementary counting:** "at least one" conditions are often easier to count via their complement ("none at all"), then subtracting from the total. This directly parallels the negation techniques from Week 1 (De Morgan's: "at least one" = ¬"none") — counting mirrors logic exactly, just as set operations did in Week 4.

### Example 9: Counting with Position-Dependent Restrictions

How many 4-digit PIN codes (digits 0-9, repetition allowed) have all four digits distinct?

**Solution.** Position 1: 10 choices. Position 2: 9 remaining (must differ from position 1). Position 3: 8 remaining. Position 4: 7 remaining.
$$10\times9\times8\times7=5040$$

---

## 6. The Bijection Principle — Counting by Correspondence

**Principle.** If there is a bijection $f:A\to B$ between finite sets, then $|A|=|B|$ (direct consequence of Week 5's bijection theory).

**Why this matters for counting:** Sometimes the SET you want to count is hard to enumerate directly, but you can find a bijection to a DIFFERENT set that's easier to count.

### Example 10

How many subsets of $\{1,2,\ldots,n\}$ exist? (We proved this in Week 4 via induction: $2^n$.)

**Bijective re-derivation:** Each subset $S\subseteq\{1,\ldots,n\}$ corresponds bijectively to a binary string of length $n$ (bit $i$ = 1 if $i\in S$, else 0). The number of binary strings of length $n$ is $2^n$ (direct Multiplication Rule: $n$ independent binary choices). By the bijection, the number of subsets is also $2^n$.

**This is exactly the "bitmask" technique from Week 4's Python examples — now you see why it works: it's a bijection-based counting argument, not just a coding trick.**

---

## 7. Common Counting Errors

### Error 1: Double-Counting Due to Overlapping Categories

Forgetting to check whether Addition Rule categories are disjoint (Example 6's lesson).

### Error 2: Treating Ordered Selections as Unordered (or vice versa)

"How many ways to choose 2 people from 5 for a committee" (unordered) vs. "How many ways to choose a president and secretary from 5 people" (ordered — these are different roles). These require DIFFERENT formulas (Thursday's lecture formalizes this distinction precisely).

### Error 3: Incorrect Independence Assumption

Applying the Multiplication Rule when steps are NOT actually independent (e.g., if the number of choices for step 2 depends on the SPECIFIC choice made in step 1, not just the count) requires more careful casework, not a blind product.

### Error 4: Forgetting Complementary Counting for "At Least" Problems

Directly counting "at least one X" is often much harder than counting "none" and subtracting from the total (Example 8).

---

## 8. Summary

```
Multiplication Rule (Product Rule):
  Sequential independent steps: n₁ × n₂ × ⋯ × n_k
  Formal basis: |S₁×S₂×⋯×S_k| = n₁×n₂×⋯×n_k (Week 4)

Addition Rule (Sum Rule):
  Mutually exclusive alternatives: n₁ + n₂ + ⋯ + n_k
  Formal basis: |S₁∪⋯∪S_k| = |S₁|+⋯+|S_k| for disjoint sets (Week 4)
  If NOT disjoint: use Inclusion-Exclusion instead

Complementary Counting:
  |A| = |Total| − |Aᶜ|
  Especially useful for "at least one" problems

Bijection Principle:
  f: A→B bijective ⟹ |A|=|B| (Week 5)
  Useful for counting hard-to-enumerate sets via easier-to-count equivalents
```

---

## 9. End-of-Lecture Exercises

1. A restaurant menu has 4 appetizers, 6 main courses, and 3 desserts. How many different 3-course meals (one from each category) are possible?

2. A committee of 3 people is to be formed by selecting 1 person from Group A (8 people), 1 from Group B (5 people), and 1 from Group C (7 people). How many committees are possible?

3. How many license plates consist of 2 letters followed by 5 digits, if the first letter cannot be 'O' or 'I' (to avoid confusion with 0 and 1)?

4. A binary string has length 10. How many such strings start with 1 OR end with 1 (or both)? *(Careful — this requires checking for overlap.)*

5. How many 6-digit strings (digits 0-9, leading zeros allowed) contain **at least one** repeated digit? *(Use complementary counting — first find how many have ALL DISTINCT digits.)*

6. How many functions $f:\{1,\ldots,5\}\to\{1,\ldots,5\}$ are there in total? How many of these are bijections (permutations of $\{1,\ldots,5\}$)? *(You'll formalize the permutation count Thursday — for now, reason it out directly using the Multiplication Rule with decreasing choices.)*

7. Prove, using a bijective argument, that the number of ways to distribute $n$ distinguishable balls into 2 distinguishable boxes equals $2^n$. *(Connect this to Exercise 6's binary string bijection.)*

---

*Next: Lecture 7.2 — Permutations and Combinations*

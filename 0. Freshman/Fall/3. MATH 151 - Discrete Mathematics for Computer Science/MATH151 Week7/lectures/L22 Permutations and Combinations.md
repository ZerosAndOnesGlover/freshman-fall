# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 22 (L22) — Permutations and Combinations
### Thursday, Week 7

**Date:** Thursday 12 November 2026 · 13:00–13:50 · Week 7

---

> **Core Question:** Does order matter, and can items repeat? These two questions determine which of four counting formulas applies.

---

## 1. The Four Fundamental Counting Scenarios

Every basic counting problem answers two binary questions:
1. **Does order matter?** (Are "AB" and "BA" different outcomes, or the same?)
2. **Is repetition allowed?** (Can the same item be chosen more than once?)

This gives **four** scenarios:

| | Order Matters | Order Doesn't Matter |
|---|---|---|
| **No Repetition** | Permutations | Combinations |
| **Repetition Allowed** | Permutations with repetition | Combinations with repetition |

We develop each in turn.

---

## 2. Permutations (Order Matters, No Repetition)

**Definition.** A **permutation** of $r$ objects chosen from a set of $n$ distinct objects (without repetition, order matters) is an ordered arrangement. The number of such permutations is denoted $P(n,r)$ or ${}_nP_r$.

**Formula:**
$$P(n,r) = n\times(n-1)\times(n-2)\times\cdots\times(n-r+1) = \frac{n!}{(n-r)!}$$

**Derivation via Multiplication Rule:** Choosing the first item: $n$ ways. Second item (excluding the first): $n-1$ ways. ... $r$-th item: $n-r+1$ ways. Multiply.

**Special case — permutations of ALL $n$ objects:** $P(n,n) = n!$

### Worked Example 1

How many ways can 5 runners finish 1st, 2nd, and 3rd place (no ties) in a race?

$$P(5,3) = 5\times4\times3 = 60 = \frac{5!}{2!} = \frac{120}{2}=60$$

### Worked Example 2

How many distinct arrangements are there of the letters in "MATH" (all 4 letters, all distinct)?

$$P(4,4)=4!=24$$

---

## 3. Combinations (Order Doesn't Matter, No Repetition)

**Definition.** A **combination** of $r$ objects chosen from $n$ distinct objects (without repetition, order irrelevant) is an unordered selection — a subset of size $r$. The number of such combinations is denoted $C(n,r)$, $\binom{n}{r}$, or "$n$ choose $r$."

**Formula:**
$$\binom{n}{r} = \frac{P(n,r)}{r!} = \frac{n!}{r!(n-r)!}$$

**Derivation:** Every unordered subset of size $r$ corresponds to exactly $r!$ different ordered arrangements (permutations) of its elements — since there are $r!$ ways to order any $r$ specific items. So the number of ordered arrangements $P(n,r)$ over-counts each combination by a factor of $r!$. Dividing corrects this.

**This derivation is itself an application of the Bijection Principle and the Multiplication Rule from Monday: $P(n,r) = \binom{n}{r}\times r!$, so $\binom{n}{r}=P(n,r)/r!$.**

### Worked Example 3

How many ways can a committee of 3 be chosen from 10 people (no distinct roles — just membership)?

$$\binom{10}{3} = \frac{10!}{3!\cdot7!} = \frac{10\times9\times8}{3\times2\times1} = \frac{720}{6}=120$$

**Contrast with Example 1 (Lecture 22) of choosing president/VP/treasurer from 10 people:** that was $P(10,3)=720$ — 6 times larger, because each committee of 3 corresponds to $3!=6$ different role-assignments.

### Worked Example 4

A standard deck has 52 cards. How many distinct 5-card poker hands are possible?

$$\binom{52}{5} = \frac{52!}{5!\cdot47!} = \frac{52\times51\times50\times49\times48}{120} = 2{,}598{,}960$$

---

## 4. Key Properties of Binomial Coefficients

| Property | Formula | Reasoning |
|---|---|---|
| Symmetry | $\binom{n}{r}=\binom{n}{n-r}$ | Choosing $r$ items to include ≡ choosing $n-r$ items to exclude |
| Boundary | $\binom{n}{0}=\binom{n}{n}=1$ | Only 1 way to choose nothing, or everything |
| Full row sum | $\sum_{r=0}^{n}\binom{n}{r}=2^n$ | Total number of subsets of an $n$-set (Week 4!) |
| Pascal's Rule | $\binom{n}{r}=\binom{n-1}{r-1}+\binom{n-1}{r}$ | Proved combinatorially below |

**Proof of Symmetry.** $\binom{n}{r}=\frac{n!}{r!(n-r)!}$ and $\binom{n}{n-r}=\frac{n!}{(n-r)!r!}$ — identical expressions (multiplication is commutative in the denominator). ∎

**Combinatorial proof of Pascal's Rule (the more illuminating style of proof — count the same thing two ways):**

Consider choosing $r$ items from $n$ items, where one specific item is labeled "special."

- **Case 1:** the special item IS included in the chosen set. Then we need to choose the remaining $r-1$ items from the other $n-1$ items: $\binom{n-1}{r-1}$ ways.
- **Case 2:** the special item is NOT included. Then we choose all $r$ items from the remaining $n-1$: $\binom{n-1}{r}$ ways.

These cases are mutually exclusive and exhaustive (the special item is either in or out), so by the Addition Rule:
$$\binom{n}{r} = \binom{n-1}{r-1}+\binom{n-1}{r}$$
∎

**This proof technique — counting the same set two different ways to derive an identity — is called a "combinatorial proof" or "bijective proof," and is one of the most elegant tools in combinatorics. We use it extensively in Friday's lecture.**

---

## 5. Permutations with Repetition

**Scenario:** Order matters, repetition IS allowed.

**Formula:** Choosing an ordered sequence of length $r$ from $n$ distinct types, with repetition allowed:
$$n^r$$

(This is exactly the Multiplication Rule applied directly: $r$ independent choices, each with $n$ options.)

### Worked Example 5

How many 4-character strings can be formed from the alphabet $\{A,B,C\}$ (repetition allowed)?
$$3^4=81$$

---

## 6. Combinations with Repetition

**Scenario:** Order doesn't matter, repetition IS allowed. (Also called "multisets" of size $r$ from $n$ types.)

**Formula:**
$$\binom{n+r-1}{r}$$

**Why this formula (the "stars and bars" argument):** Imagine choosing $r$ items from $n$ types, with repeats allowed, order irrelevant — e.g., choosing $r$ donuts from $n$ flavors, where you can pick multiple of the same flavor. Represent your choice as a sequence of $r$ stars (★) and $n-1$ bars (|), where stars between consecutive bars represent how many of each flavor you picked.

**Example:** $n=3$ flavors, $r=5$ donuts. A choice of 2 chocolate, 0 vanilla, 3 strawberry is represented as:
$$\star\star \mid \mid \star\star\star$$

This is a string of $r+n-1 = 5+2=7$ symbols total ($r$ stars, $n-1$ bars), and the number of such strings is the number of ways to choose which $r$ (or equivalently $n-1$) of the $r+n-1$ positions are stars:
$$\binom{r+n-1}{r} = \binom{n+r-1}{r}$$

### Worked Example 6

A bakery sells 4 types of donuts. How many ways can you select a box of 6 donuts (repetition allowed, order doesn't matter)?

$$\binom{4+6-1}{6}=\binom{9}{6}=\binom{9}{3}=\frac{9\times8\times7}{6}=84$$

### Worked Example 7 — Non-negative Integer Solutions

How many solutions in non-negative integers does $x_1+x_2+x_3=10$ have?

**This is exactly a stars-and-bars problem:** distribute 10 identical units among 3 variables. $n=3$ (variables/"flavors"), $r=10$ (units/"donuts").
$$\binom{3+10-1}{10}=\binom{12}{10}=\binom{12}{2}=66$$

**This connects directly to CS resource allocation problems:** distributing $r$ identical resources (memory pages, tasks) among $n$ distinguishable bins (processes, servers) with no capacity limit is exactly this formula.

---

## 7. Summary Table — The Four Scenarios

| Scenario | Order Matters? | Repetition? | Formula | Name |
|---|---|---|---|---|
| 1 | Yes | No | $P(n,r)=\dfrac{n!}{(n-r)!}$ | Permutation |
| 2 | No | No | $\dbinom{n}{r}=\dfrac{n!}{r!(n-r)!}$ | Combination |
| 3 | Yes | Yes | $n^r$ | Permutation w/ repetition |
| 4 | No | Yes | $\dbinom{n+r-1}{r}$ | Combination w/ repetition |

---

## 8. Diagnostic Questions — How to Classify a Problem

Ask, in order:

1. **"Does swapping two selected items create a different outcome?"**
   - YES → order matters (permutation-type)
   - NO → order doesn't matter (combination-type)

2. **"Can the same item/type be selected more than once?"**
   - YES → repetition allowed
   - NO → no repetition

### Worked Classification Examples

| Problem | Order? | Repetition? | Formula |
|---|---|---|---|
| Assign gold/silver/bronze medals to 8 racers | YES | NO | $P(8,3)$ |
| Choose 3 books to bring on vacation from a shelf of 10 | NO | NO | $\binom{10}{3}$ |
| Form a 6-character password from 26 letters | YES | YES | $26^6$ |
| Choose 5 scoops of ice cream from 8 flavors (can repeat a flavor) | NO | YES | $\binom{8+5-1}{5}$ |

---

## 9. Permutations with Indistinguishable Objects

**Theorem.** The number of distinct arrangements of $n$ objects, where there are $n_1$ objects of type 1, $n_2$ of type 2, ..., $n_k$ of type $k$ (with $n_1+n_2+\cdots+n_k=n$), is:
$$\frac{n!}{n_1!\,n_2!\,\cdots\,n_k!}$$

**Reasoning:** Start with $n!$ (as if all objects were distinguishable). Then divide by $n_1!$ to correct for the fact that permuting the $n_1$ identical objects among themselves produces indistinguishable arrangements — similarly for each other type.

### Worked Example 8

How many distinct arrangements of the letters in "MISSISSIPPI"?

Letters: M(1), I(4), S(4), P(2). Total letters: 11.

$$\frac{11!}{1!\,4!\,4!\,2!} = \frac{39{,}916{,}800}{1\times24\times24\times2} = \frac{39{,}916{,}800}{1152}=34{,}650$$

---

## 10. Summary

```
Four Scenarios:
  Ordered, no repeat:    P(n,r) = n!/(n-r)!
  Unordered, no repeat:  C(n,r) = n!/(r!(n-r)!)
  Ordered, repeat OK:    n^r
  Unordered, repeat OK:  C(n+r-1,r)   [stars and bars]

Key identities:
  C(n,r) = C(n,n-r)              (symmetry)
  C(n,r) = C(n-1,r-1)+C(n-1,r)   (Pascal's Rule)
  Σ C(n,r) = 2^n                 (total subsets)

Indistinguishable objects:
  n! / (n₁! n₂! ⋯ n_k!)
```

---

## 11. End-of-Lecture Exercises

1. Classify each scenario (order? repetition?) and compute the answer:
   - (a) Choosing 4 cards from a deck of 52 (a "hand," order irrelevant).
   - (b) Assigning 3 distinct prizes to 3 different winners chosen from 20 contestants.
   - (c) Rolling a 6-sided die 4 times and recording the sequence of results.
   - (d) Selecting 2 pizza toppings from 8 available, allowing the same topping twice (double portion) but order of selection irrelevant.

2. How many ways can 8 people be seated in a row of 8 chairs?

3. How many ways can a 4-person subcommittee be selected from a 12-person committee?

4. How many distinct arrangements are there of the letters in "STATISTICS"?

5. How many non-negative integer solutions does $x_1+x_2+x_3+x_4=15$ have?

6. Prove Pascal's Rule algebraically (using the factorial formula for $\binom{n}{r}$, NOT the combinatorial/counting argument from Section 4). Verify both proofs give the same identity.

7. A hash table has 8 buckets. In how many ways can 5 distinguishable keys be distributed among the buckets such that:
   - (a) any bucket can hold any number of keys (no restriction)?
   - (b) each bucket holds at most 1 key?

---

*Next: Lecture 23 — The Binomial Theorem and Pascal's Triangle*

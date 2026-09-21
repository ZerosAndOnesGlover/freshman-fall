# MATH 151 · Discrete Mathematics for Computer Science
## Quiz 8 — Scope Preview
### Quiz administered: Monday 16 November 2026, 13:00–13:15 (first 15 minutes of lecture) · Week 8

---

**Coverage:** Week 7 material only:
- Week 7: Counting — multiplication/addition rules, permutations, combinations, binomial theorem

*(Week 8 material is not on this quiz — it is taught after the quiz.)*

---

## What You Must Know Cold for Week 7 Material

### 1. The Four Counting Scenarios

| Order | Repetition | Formula |
|---|---|---|
| Yes | No | $P(n,r)=n!/(n-r)!$ |
| No | No | $C(n,r)=n!/(r!(n-r)!)$ |
| Yes | Yes | $n^r$ |
| No | Yes | $C(n+r-1,r)$ |

**The single most tested skill:** correctly classifying a word problem into one of these four scenarios BEFORE computing.

### 2. Multiplication vs Addition Rule

- Multiplication: sequential/independent steps → multiply counts
- Addition: mutually exclusive alternatives → add counts
- If categories overlap: use the two-set Inclusion–Exclusion formula (Week 4), NOT plain addition

### 3. Complementary Counting

"At least one" problems: count total, subtract "none at all."
$$|\text{at least one}| = |\text{Total}| - |\text{none}|$$

### 4. Key Binomial Facts

- $(x+y)^n = \sum_k\binom{n}{k}x^{n-k}y^k$
- $\binom{n}{k}=\binom{n}{n-k}$ (symmetry)
- $\binom{n}{r}=\binom{n-1}{r-1}+\binom{n-1}{r}$ (Pascal's Rule)
- $\sum_k\binom{n}{k}=2^n$ (row sum)
- Combinatorial proofs: count the same set two ways to derive identities

### 5. Indistinguishable Objects

$$\frac{n!}{n_1!n_2!\cdots n_k!}$$

---

## Sample Quiz 8 Problems (Week 7 portion)

**Problem 1.** (4 pts) Classify and compute a given counting scenario.

**Problem 2.** (4 pts) A multi-step problem requiring both multiplication and addition (or complementary counting).

**Problem 3.** (4 pts) Find a specific coefficient in a binomial expansion.

**Problem 4.** (4 pts) Give a combinatorial proof of a stated identity.

**Problem 5.** (4 pts) From Week 8 — an advanced counting problem (see Week 8 materials).

---

## Study Recommendations

1. **Drill the two diagnostic questions** ("does order matter?" "is repetition allowed?") on at least 15 different word problems until classification becomes automatic.

2. **Practice complementary counting** on "at least one" problems — this is one of the most common quiz question types.

3. **Memorize Pascal's Rule's combinatorial proof** — quizzes often ask you to reproduce or apply this proof technique to a new identity.

4. **Do PS7 completely**, especially Part C's multi-step problems — these combine several techniques in one problem, exactly the style tested on quizzes and exams.

5. **Practice the stars-and-bars visual argument** until you can set up the bijection (stars for items, bars for dividers) without hesitation.

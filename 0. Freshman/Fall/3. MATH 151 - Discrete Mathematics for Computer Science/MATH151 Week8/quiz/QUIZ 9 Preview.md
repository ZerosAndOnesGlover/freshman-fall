# MATH 151 · Discrete Mathematics for Computer Science
## Quiz 9 — Scope Preview
### Quiz administered: Monday 23 November 2026, 13:00–13:15 (first 15 minutes of lecture) · Week 9

---

**Coverage:** Week 8 material — the Pigeonhole Principle and Inclusion–Exclusion.

---

## What You Must Know Cold for Week 8 Material

### 1. Pigeonhole, both forms

- **Basic:** $n$ items into $m$ containers with $n > m$ ⟹ some container holds at least 2.
- **Generalised:** some container holds at least $\lceil n/m \rceil$.

You must be able to **state which objects are the pigeons and which are the pigeonholes** before
writing any proof. A proof that omits this scores at most half marks, on the quiz and on the exam.

### 2. Constructing pigeonholes

The hard problems do not hand you the containers. Practised patterns:

| Problem shape | Pigeonholes to try |
|---|---|
| Two elements summing to $k$ | Pairs $\{a, k-a\}$ |
| Two with the same remainder | Residues mod $m$ |
| Two subsets with equal sums | The range of possible sums |
| Two points close together | A grid partition of the region |

### 3. Inclusion–Exclusion

$$|A\cup B| = |A|+|B|-|A\cap B|$$
$$|A\cup B\cup C| = \textstyle\sum|A_i| - \sum|A_i\cap A_j| + |A\cap B\cap C|$$

For divisibility, **intersections use the lcm**: $|A_2 \cap A_3|$ counts multiples of 6.

### 4. The complement rule

$$\#(\text{at least one}) = \text{total} - \#(\text{none})$$

If several "at least one" conditions appear, the complement is a union and needs inclusion–exclusion
itself.

### 5. Derangements

$D_n = n!\sum_{k=0}^n \frac{(-1)^k}{k!}$. Know the small values cold:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $D_n$ | 0 | 1 | 2 | 9 | 44 | 265 |

And know that $D_n/n! \to 1/e \approx 0.368$.

### 6. Choosing the tool

**Existence ⟹ Pigeonhole. A number ⟹ Inclusion–Exclusion.** This is the single most likely thing to
be tested, because it is the skill that transfers.

---

## Sample Quiz 9 Problems (Week 8 portion)

**Problem 1.** (4 pts) Prove that among any 20 integers, two leave the same remainder on division by
19. Identify pigeons and pigeonholes explicitly.

**Problem 2.** (4 pts) How many integers in $\{1,\ldots,300\}$ are divisible by 4 or 9? State each
intersection's divisor.

**Problem 3.** (4 pts) How many 6-character strings over $\{a,\ldots,z\}$ contain at least one vowel?
Use the complement.

**Problem 4.** (4 pts) Compute $D_5$ and state the probability that a random permutation of 5 objects
is a derangement.

**Problem 5.** (4 pts) For each, name the technique only — do not solve:
(a) show that some two of 30 people share a birthday within the same week of the year;
(b) count the passwords containing at least one digit and one symbol.

---

## Study Recommendations

1. **Do every Pigeonhole problem in PS 8 Part A twice** — once for the answer, once naming pigeons and pigeonholes in a single sentence each.
2. **Redo Lab 8 Section 3** (choosing the tool) with the answers covered. It takes five minutes and is the best predictor of quiz performance.
3. **Memorise $D_1$ through $D_6$.** They appear constantly and recomputing them under time pressure wastes minutes.
4. **Practise the lcm trap.** Write out $|A_a \cap A_b| = \lfloor N/\mathrm{lcm}(a,b)\rfloor$ five times. It is the most common arithmetic error in this material.

---

*MATH 151 · Week 8 · © CSE Department*

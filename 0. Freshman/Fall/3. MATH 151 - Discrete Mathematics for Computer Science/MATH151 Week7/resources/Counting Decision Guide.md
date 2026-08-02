# MATH 151 — Counting Decision Guide
## Week 7: A Step-by-Step Framework for Classifying Counting Problems

---

## The Master Decision Tree

```
Read the problem. Identify: what are you selecting/arranging, and from what pool?
│
├─ Is this a SEQUENCE of independent choices (do task 1, THEN task 2, ...)? 
│   └─ YES → Multiplication Rule: multiply the count at each step
│
├─ Is this a choice between DISJOINT alternative methods ("either do X or do Y")?
│   └─ YES → check disjointness
│       ├─ Truly disjoint → Addition Rule: add the counts
│       └─ Overlapping → Inclusion-Exclusion: |A∪B| = |A|+|B|-|A∩B|
│
├─ Is this "how many ways to select/arrange r items from n"?
│   └─ YES → ask the two diagnostic questions:
│       │
│       ├─ Does ORDER matter?
│       │   ├─ YES + no repetition → P(n,r) = n!/(n-r)!
│       │   ├─ YES + repetition OK → n^r
│       │   ├─ NO + no repetition → C(n,r) = n!/(r!(n-r)!)
│       │   └─ NO + repetition OK → C(n+r-1,r)  [stars and bars]
│
├─ Is this "at least one" of something?
│   └─ YES → Complementary counting: Total − None
│
├─ Is this arranging objects with REPEATED/indistinguishable items?
│   └─ YES → n! / (n₁! n₂! ⋯ n_k!)
│
└─ Is this proving an IDENTITY between two counting expressions?
    └─ YES → Combinatorial proof: describe one scenario, count it two ways
```

---

## Keyword Recognition Table

| Phrase in Problem | Likely Signals |
|---|---|
| "arrange," "order," "sequence," "rank," "line up" | Order matters → Permutation |
| "select," "choose," "committee," "subset," "group" (no roles) | Order doesn't matter → Combination |
| "with repetition," "can repeat," "same item twice" | Repetition allowed |
| "distinct," "different," "no two the same," "all unique" | No repetition |
| "president/VP/secretary," "1st/2nd/3rd place," "gold/silver/bronze" | Distinct ROLES → order matters even without explicit "order" language |
| "or," "either," "at least one of two disjoint options" | Addition Rule (check disjointness!) |
| "and," "then," "each of the following steps" | Multiplication Rule |
| "at least one," "at least $k$" | Complementary counting (for "at least one") or casework (for "at least $k$" with $k>1$, often summing multiple cases) |
| "how many ways to distribute identical items" | Stars and bars |
| "how many distinct arrangements of letters in [word]" | Indistinguishable objects formula |

---

## Worked Classification Walkthrough — 10 Problems

**Problem 1:** "How many ways can you arrange 5 different books on a shelf?"
→ Order matters (arrangement), no repetition (all books used exactly once), all $n$ objects used.
→ $P(5,5) = 5! = 120$

**Problem 2:** "How many ways can you select 3 books from a shelf of 8 to take on a trip?"
→ Order doesn't matter (just which books, not their order in your bag), no repetition (each book once).
→ $\binom{8}{3}=56$

**Problem 3:** "How many 4-digit PINs are there (leading zeros OK)?"
→ Order matters (1234 ≠ 4321), repetition allowed (digits can repeat).
→ $10^4=10000$

**Problem 4:** "How many ways to select 6 fruits from 4 types, allowing repeats, order doesn't matter?"
→ Order doesn't matter, repetition allowed.
→ $\binom{4+6-1}{6}=\binom{9}{6}=84$

**Problem 5:** "In how many ways can a professor assign grades (A,B,C,D,F) to 30 students?"
→ Each of 30 students (positions) independently gets one of 5 grades (choices) — order matters in the sense that WHICH student gets WHICH grade matters, repetition allowed (many students can get the same grade).
→ $5^{30}$ (a permutation-with-repetition style count — equivalently, counting functions from students to grades)

**Problem 6:** "How many ways can 20 people be split into a group of 12 and a group of 8?"
→ This is a combination (order doesn't matter within each group), and the groups are naturally distinguishable by SIZE (12 vs 8), so no overcounting correction needed.
→ $\binom{20}{12}$ (equivalently $\binom{20}{8}$, since choosing the 12-group determines the 8-group)

**Problem 7:** "How many 7-card hands have at least one ace?"
→ "At least one" signals complementary counting.
→ $\binom{52}{7} - \binom{48}{7}$ (total hands minus hands with zero aces, choosing all 7 from the 48 non-aces)

**Problem 8:** "How many ways to arrange the letters in 'BANANA'?"
→ Indistinguishable objects: B(1), A(3), N(2).
→ $\dfrac{6!}{1!3!2!}=60$

**Problem 9:** "A password needs at least one digit and at least one letter, length 4, using 26 letters + 10 digits."
→ This combines complementary counting with careful casework (need to exclude "all letters" AND "all digits," and check they don't overlap incorrectly at the complement stage — Inclusion-Exclusion on the "bad" cases).
→ Total: $36^4$. All-letter: $26^4$. All-digit: $10^4$. These two bad cases are disjoint (can't be both all-letter and all-digit unless length 0). Valid: $36^4 - 26^4 - 10^4$.

**Problem 10:** "Prove $\binom{n}{2}=\binom{n-1}{2}+(n-1)$ combinatorially."
→ Identity-proving problem: describe choosing 2 items from $n$, split by whether a specific item is included.

---

## Multi-Step Problem Strategy

For problems combining several scenarios (common in Part C of problem sets):

1. **Break the problem into independent stages** (e.g., "choose the kings" AND "choose the non-kings").
2. **Classify EACH stage separately** using the decision tree.
3. **Combine stages with the Multiplication Rule** (if the stages are sequential/independent sub-choices of one overall selection).
4. **If the problem has mutually exclusive CASES** (e.g., "exactly 2 women" vs "exactly 3 women" vs "exactly 4 women" for an "at least 2 women" problem), compute each case separately then apply the Addition Rule across cases.

### Worked Multi-Step Example

"How many 6-person committees from 10 men and 8 women have at least 4 women?"

**Step 1 — recognize "at least 4" needs casework (not simple complementary counting, since there are multiple qualifying cases):** exactly 4 women, exactly 5 women, or exactly 6 women.

**Step 2 — classify and compute each case:**
- Exactly 4 women (+2 men): $\binom{8}{4}\binom{10}{2} = 70\times45=3150$
- Exactly 5 women (+1 man): $\binom{8}{5}\binom{10}{1}=56\times10=560$
- Exactly 6 women (+0 men): $\binom{8}{6}\binom{10}{0}=28\times1=28$

**Step 3 — combine via Addition Rule (mutually exclusive cases):**
$$3150+560+28=3738$$

**Note the distinction from Example 8 (Monday's lecture) — "at least one" complementary counting works cleanly when there's only ONE excluded case ("none"). "At least $k$" for $k>1$ typically requires summing multiple explicit cases instead**, since the complement ("fewer than $k$") itself splits into several sub-cases (0, 1, ..., k-1) that may be just as much work to enumerate as the direct cases from $k$ upward.

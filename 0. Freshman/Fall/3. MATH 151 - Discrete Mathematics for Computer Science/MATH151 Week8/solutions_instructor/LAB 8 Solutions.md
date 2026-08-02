# MATH 151 · Week 8
## LAB 8 Solutions — INSTRUCTOR ONLY

All numeric results verified by computation.

---

## Section 1 Solutions

### Exercise 1.1

**Pigeons:** 40 people. **Pigeonholes:** 7 days of the week.

Generalized Pigeonhole: $\lceil40/7\rceil=\lceil5.71\rceil=6$.

**Proof.** By the Generalized Pigeonhole Principle with 40 people distributed among 7 days, some day has at least $\lceil40/7\rceil=6$ people.

> **Grading note.** The claim only asks for "at least 4", and $6\geq4$, so this argument proves
> something **stronger** than required. Award full credit for the tight bound of 6, and equally full
> credit for a sound but looser argument reaching only $\geq4$. What must be present is the
> pigeonhole structure — 40 objects, 7 boxes, $\lceil40/7\rceil$ — not the sharpest constant.

∎

---

### Exercise 1.2

**Pigeons:** the 26 (or more) chosen elements. **Pigeonholes:** the 25 pairs summing to 51: $\{1,50\},\{2,49\},\ldots,\{25,26\}$.

**Proof.** Partition $\{1,\ldots,50\}$ into 25 pairs each summing to 51. With 26 elements chosen (pigeons) and 25 pairs (pigeonholes), $26>25$ ⟹ two chosen elements land in the same pair ⟹ their sum is 51. ∎

---

### Exercise 1.3

**Proof.** The hash function maps 1001 strings (pigeons) into 1000 buckets (pigeonholes). Since $1001>1000$, by Pigeonhole, at least two strings map to the same bucket — a collision is guaranteed.

**Does this tell us WHICH strings collide?** No. The Pigeonhole Principle is a pure existence proof — it guarantees a collision exists without identifying which specific strings are involved. Determining the actual colliding pair requires either computing all 1001 hash values and checking for duplicates (an $O(n)$ computation with a hash set) or is left unknown if we only have the counting argument. This is characteristic of Pigeonhole-style proofs: they establish existence, not identification.

---

### Exercise 1.4

**Pigeons:** the 7 integers. **Pigeonholes:** the groups $\{0\},\{1,9\},\{2,8\},\{3,7\},\{4,6\},\{5\}$ — 6 groups (by remainder mod 10, pairing $r$ with $10-r$).

**Proof.** Compute each integer's remainder mod 10. Group remainders into: $\{0\}$ (self-paired, since $10-0=10\equiv0$), $\{5\}$ (self-paired, since $10-5=5$), and $\{1,9\},\{2,8\},\{3,7\},\{4,6\}$ (proper pairs) — 6 groups total.

With 7 integers (pigeons) and 6 groups (pigeonholes), $7>6$ ⟹ two integers land in the same group.

If both are in a "self-paired" group ($\{0\}$ or $\{5\}$): they share the SAME remainder, so their DIFFERENCE is divisible by 10.

If both are in a proper pair group $\{r,10-r\}$: either they share the same remainder (difference divisible by 10), or one has remainder $r$ and the other $10-r$ (sum divisible by 10, since sum $\equiv r+(10-r)=10\equiv0\pmod{10}$).

Either way, two integers have sum or difference divisible by 10. ∎

---

---

## Section 2 Solutions — Inclusion–Exclusion

### Exercise 2.1

$|P|=120$, $|C|=90$, $|R|=70$; $|P\cap C|=45$, $|P\cap R|=30$, $|C\cap R|=25$; $|P\cap C\cap R|=15$.

**(a)** $120+90+70-45-30-25+15 = \mathbf{195}$ use at least one.

**(b)** $200-195 = \mathbf{5}$ use none.

**(c)** Exactly one:

| Region | Count |
|---|---|
| Python only | $120-45-30+15 = 60$ |
| C only | $90-45-25+15 = 35$ |
| Rust only | $70-30-25+15 = 30$ |
| **Exactly one** | $\mathbf{125}$ |

*Consistency check:* exactly-one $125$ + exactly-two $(45{-}15)+(30{-}15)+(25{-}15)=55$ + all-three
$15$ = $195$ ✓ — matches (a). **Require this check**; it catches nearly every arithmetic slip.

*Marking: 2 for (a), 1 for (b), 3 for (c). The $+15$ in each "only" formula is the discriminator — a
student subtracting both pairwise overlaps without adding the triple back gets 45/20/15 and a total
that fails the check.*

---

### Exercise 2.2

$\lfloor1000/3\rfloor=333$, $\lfloor1000/5\rfloor=200$, $\lfloor1000/7\rfloor=142$;
$\lfloor1000/15\rfloor=66$, $\lfloor1000/21\rfloor=47$, $\lfloor1000/35\rfloor=28$;
$\lfloor1000/105\rfloor=9$.

$$333+200+142-66-47-28+9 = \mathbf{543}$$

Divisible by none: $1000-543 = \mathbf{457}$.

*(Verified by direct enumeration: the union has exactly 543 elements.)*

*Marking: the intersection divisors are the point. A student writing $\lfloor1000/3\rfloor\cdot\lfloor1000/5\rfloor$
for $|A_3\cap A_5|$ loses half the marks regardless of the final number.*

---

### Exercise 2.3 — The Complement Habit

**(ii) Complement:** $62^8 - 52^8 = 218{,}340{,}105{,}584{,}896 - 53{,}459{,}728{,}531{,}456 = \mathbf{164{,}880{,}377{,}053{,}440}$.

About **75.5%** of all such passwords contain a digit.

**(i) Direct:** $\sum_{k=1}^{8}\binom{8}{k}10^k 52^{8-k}$ — eight terms, each requiring a binomial
coefficient and two powers. Same answer, roughly ten times the work.

*The pedagogical point is the time comparison, which is why the exercise asks students to record it.
Anyone who reports the direct method as quicker has not attempted it.*

---

## Section 3 Solutions — Choosing the Tool

| # | Problem | Tool | Why |
|---|---|---|---|
| 1 | 13 people, two share a birth month | **Pigeonhole** | Asks to *show* something must exist; 13 pigeons, 12 holes |
| 2 | Integers under 200 divisible by 4 or 6 | **Inclusion–Exclusion** | Asks for a count; the categories overlap (multiples of 12) |
| 3 | 5-letter strings, no repeated letter | **Multiplication rule** | Independent stages with a shrinking pool: $26\cdot25\cdot24\cdot23\cdot22$ |
| 4 | Two of 5 points in a unit square are close | **Pigeonhole** | Existence again; the pigeonholes must be *constructed* (four quadrants) |
| 5 | Return $n$ hats, nobody gets their own | **Derangements** | The defining "no element in its own place" |
| 6 | Passwords with a digit **and** a symbol | **Inclusion–Exclusion** | A count, with two "at least one" conditions ⟹ complement is a union |

*Marking: 0.5 per correct tool, 0.5 per justification. Items 2 and 6 are both inclusion–exclusion but
for different reasons — 2 because the sets overlap, 6 because the complement does. Students who spot
that distinction are ahead of the cohort.*

*Answers for reference: #2 is $49+33-16=66$; #3 is $7{,}893{,}600$.*

---

## Section 4 Solutions — Python


### Exercise 4.1

Running `simulate_pigeonhole(100, 12)` multiple times: guaranteed minimum reported as 9; observed trial maximums typically range from 9 to 15+ due to randomness, always $\geq9$.

---

---

### Exercise 4.2 — Derangements

| $n$ | brute force | formula | $D_n/n!$ |
|---|---|---|---|
| 0 | 1 | 1 | 1.000000 |
| 1 | 0 | 0 | 0.000000 |
| 2 | 1 | 1 | 0.500000 |
| 3 | 2 | 2 | 0.333333 |
| 4 | 9 | 9 | 0.375000 |
| 5 | 44 | 44 | 0.366667 |
| 6 | 265 | 265 | 0.368056 |
| 7 | 1854 | 1854 | 0.367857 |
| 8 | 14833 | 14833 | 0.367882 |

**Both columns agree for every $n \le 8$.**

The ratio converges to $1/e = 0.367879$. It is **stable to three decimal places from $n = 6$**
($0.368$), and by $n=8$ agrees to five.

*The intended surprise: the answer is essentially independent of $n$ past about 6. Whether the
cloakroom holds ten coats or ten million, roughly 37% of the time nobody gets their own.*

*Marking: 2 for the agreeing table, 1 for identifying $1/e$, 1 for the stability threshold. Note that
brute force becomes infeasible past $n\approx11$ — a student who tried $n=15$ and gave up has
learned something worth crediting.*

---

### Exercise 4.3 — Inclusion–Exclusion Cost

```python
from itertools import combinations

def count_union(sets):
    n, total = len(sets), 0
    for r in range(1, n + 1):
        for combo in combinations(range(n), r):
            inter = set(sets[combo[0]])
            for i in combo[1:]:
                inter &= sets[i]
            total += (-1) ** (r + 1) * len(inter)
    return total
```

Agrees with `len(set().union(*sets))` on every random input.

**Timing.** The term count is $2^n - 1$, so runtime **doubles with each additional set**:

| $n$ | terms |
|---|---|
| 3 | 7 |
| 5 | 31 |
| 10 | 1023 |
| 15 | 32767 |
| 20 | 1048575 |

The curve is exponential, not polynomial — the giveaway is that a log-scale plot of time against $n$
is a straight line. This is Lecture 8.2's $2^n$ cost made visible, and it is why database query
planners truncate the expansion after the pairwise terms rather than computing it exactly.

*Marking: 3 for a correct implementation agreeing with `set.union`, 3 for the timing data, and full
marks only if the student names the growth as exponential rather than "slow".*

---

## Section 5 — Reflection Model Answers

1. **Hardest to classify.** Most students name #2 and #6, because both mention overlapping conditions
   yet require inclusion–exclusion for different structural reasons. Also common is #4, whose wording
   ("two points are close") hides an existence claim behind a geometric statement.

2. **Existence vs search.** The subset-sum argument counts: 1023 non-empty subsets, at most 955
   possible sums, so two must collide. The argument never examines a single subset. Finding the
   colliding pair means searching a space of size $2^{10}$ in this instance and $2^n$ in general —
   subset-sum is NP-complete. **Counting the possibilities is cheap; locating a specific one is not.**

3. **100 sets.** $2^{100}$ terms is not computable. Practical options: truncate after the pairwise
   terms and accept a bound (Bonferroni — truncating after an odd number of terms over-estimates,
   after an even number under-estimates); use a probabilistic cardinality estimator such as
   HyperLogLog; or exploit structure if most intersections are empty.

---

## Checkoff Summary

| Section | Watch for |
|---|---|
| 1 — Pigeonhole | Pigeons and pigeonholes named in **every** proof |
| 2 — Inclusion–Exclusion | lcm used for intersections; the 2.1(c) consistency check performed |
| 3 — Choosing the tool | Justification given, not just the label |
| 4 — Python | 4.2 tables agree for all $n\le8$; 4.3 growth named as **exponential** |
| 5 — Reflection | Q2 separates counting from searching |

**Minimum for checkoff:** all four Section 1 proofs with pigeons/pigeonholes identified; Section 2
complete; at least 5 of 6 Section 3 classifications correct; both Section 4 programs running and
agreeing with the reference values.

---

*MATH 151 · Week 8 · Lab 8 Solutions · Instructor copy — do not distribute*

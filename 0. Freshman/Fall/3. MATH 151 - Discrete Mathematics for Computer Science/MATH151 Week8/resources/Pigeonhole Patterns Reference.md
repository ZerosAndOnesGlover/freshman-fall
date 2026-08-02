# MATH 151 — Pigeonhole Patterns Reference
## Week 8: Advanced Counting — Pigeonhole Patterns

---

## Pattern 1 — Direct Counting (Birthdays, Days of Week, etc.)

**Template:** $n$ people, $m$ categories (months, weekdays, etc.), $n>m$ ⟹ two people share a category.

**Generalized version:** some category has $\geq\lceil n/m\rceil$ people.

**Worked example:** 100 people, 12 months ⟹ some month has $\geq\lceil100/12\rceil=9$ people.

---

## Pattern 2 — Sum-to-Target Pairs

**Template:** Choosing $k$ numbers from $\{1,\ldots,2n\}$ where $k>n$ forces two to sum to $2n+1$.

**Construction:** Partition $\{1,\ldots,2n\}$ into $n$ pairs $\{1,2n\},\{2,2n-1\},\ldots,\{n,n+1\}$, each summing to $2n+1$. These are the pigeonholes.

**Worked example:** Choose 6 from $\{1,\ldots,10\}$ ($n=5$): pairs $\{1,10\},\{2,9\},\{3,8\},\{4,7\},\{5,6\}$. With 6 pigeons and 5 holes, two chosen numbers share a pair, hence sum to 11.

**Variant — careful counting:** If asked "must 6 numbers from $\{1,\ldots,20\}$ include two summing to 21?" — check: pairs summing to 21 are $\{1,20\},\ldots,\{10,11\}$ — 10 pairs. With only 6 numbers chosen and 10 pigeonholes, Pigeonhole does NOT force a collision (6 < 10) — the claim may be FALSE. Always verify pigeon count exceeds hole count before concluding the principle applies.

---

## Pattern 3 — Remainders (Modular Arithmetic)

**Template:** Among $n+1$ integers, two have the same remainder mod $n$ (hence their difference is divisible by $n$).

**Construction:** The $n$ possible remainders $\{0,1,\ldots,n-1\}$ are the pigeonholes.

**Worked example:** Among any 11 integers, two have a difference divisible by 10. (11 pigeons, 10 remainder-classes as holes.)

**Variant — symmetric remainder pairing:** For "sum OR difference divisible by $n$" problems, pair remainders $r$ and $n-r$ together (since if two numbers have remainders $r$ and $n-r$, their SUM is divisible by $n$; if same remainder, their DIFFERENCE is divisible by $n$). This roughly halves the number of "true" pigeonholes.

Example: among any 7 integers, two have sum or difference divisible by 10. Remainder classes mod 10: $\{0\},\{1,9\},\{2,8\},\{3,7\},\{4,6\},\{5\}$ — that's 6 groups. With 7 integers and 6 groups, two land in the same group — giving sum or difference divisible by 10 depending on whether they have the same or paired-different remainders.

---

## Pattern 4 — Divisibility via Odd Part Decomposition

**Template:** Among any $n+1$ integers chosen from $\{1,\ldots,2n\}$, two exist where one divides the other.

**Construction:** Write each integer $x = 2^k\cdot m$ where $m$ is odd. There are exactly $n$ possible odd values $m\in\{1,3,5,\ldots,2n-1\}$ — these are the pigeonholes. With $n+1$ integers chosen (pigeons), two share the same odd part $m$, say $x_1=2^{k_1}m$ and $x_2=2^{k_2}m$ with $k_1<k_2$. Then $x_1\mid x_2$.

**Worked example:** Among any 51 integers from $\{1,\ldots,100\}$, two exist where one divides the other. (50 possible odd parts as pigeonholes, 51 chosen integers as pigeons.)

---

## Pattern 5 — Geometric / Spatial Pigeonhole

**Template:** Points in a bounded region; divide the region into sub-regions (pigeonholes); points (pigeons) exceeding sub-region count force two points into the same sub-region, bounding their distance.

**Worked example:** 5 points in a unit square ⟹ two points within distance $\frac{\sqrt2}{2}$.

Divide the unit square into 4 quarter-squares (side $1/2$). With 5 points and 4 quarter-squares, two points land in the same quarter-square. The maximum distance between two points within a $1/2\times1/2$ square is its diagonal, $\frac{\sqrt2}{2}$.

---

## Pattern 6 — Function/Sequence Repetition

**Template:** A function or process with finitely many possible "states"; iterating it must eventually repeat a state.

**Worked example (permutation cycles):** For a bijection $f:\{1,\ldots,n\}\to\{1,\ldots,n\}$ and any starting element $x$, the sequence $x, f(x), f(f(x)),\ldots$ takes values in a finite set of size $n$. After at most $n+1$ terms, some value repeats (Pigeonhole: $n+1$ terms, $n$ possible values). Injectivity of $f$ then forces the repetition to cycle back to $x$ itself.

**Worked example (subset sums, Lecture 5.3 Section 8):** $2^{10}=1024$ subsets of a 10-element set; sums range over at most 1001 values ($\{0,\ldots,1000\}$ for elements up to 100 each) ⟹ two distinct subsets share a sum ⟹ (after removing common elements) two disjoint subsets with equal sums.

---

## Pattern 7 — Partial Sums (Contiguous Subsequence Divisibility)

**Template:** Given a sequence $a_1,\ldots,a_n$, find a contiguous run summing to a multiple of $n$.

**Construction:** Define partial sums $S_0=0, S_1=a_1, S_2=a_1+a_2,\ldots,S_n=a_1+\cdots+a_n$ — that's $n+1$ partial sums (pigeons). Their remainders mod $n$ take one of $n$ values (pigeonholes: $\{0,\ldots,n-1\}$). By Pigeonhole, two partial sums $S_i, S_j$ ($i<j$) share the same remainder mod $n$, so $n\mid(S_j-S_i)$. But $S_j-S_i = a_{i+1}+a_{i+2}+\cdots+a_j$ — a contiguous run summing to a multiple of $n$.

---

## Decision Guide — Which Pattern Applies?

```
Does the problem involve:
│
├─ People/objects into fixed categories? → Pattern 1 (direct counting)
│
├─ "Two numbers summing to a target"? → Pattern 2 (sum-to-target pairs)
│
├─ "Same remainder" or "difference divisible by n"? → Pattern 3 (remainders)
│
├─ "One divides the other"? → Pattern 4 (odd part decomposition)
│
├─ Points/distances in a bounded space? → Pattern 5 (geometric)
│
├─ Repeated states/values under iteration? → Pattern 6 (function repetition)
│
└─ "Contiguous run summing to a multiple of n"? → Pattern 7 (partial sums)
```

---

## Full Worked Example — Combining Techniques

**Problem:** Among any 10 distinct integers from $\{1,\ldots,100\}$, show two disjoint subsets exist with equal sums.

**Step 1 — Identify pigeons:** All $2^{10}=1024$ subsets of the 10-element set.

**Step 2 — Identify pigeonholes:** Possible subset sums. Since each of the 10 integers is $\leq100$, the maximum possible sum is at most $100\times10=1000$ (loose bound; tighter bounds possible but unnecessary). So sums range over $\{0,1,\ldots,1000\}$ — 1001 possible values.

**Step 3 — Apply Pigeonhole:** $1024>1001$ ⟹ two distinct subsets $S_1\neq S_2$ have equal sums.

**Step 4 — Disjointify:** Remove $S_1\cap S_2$ from both to get disjoint $S_1', S_2'$ with equal sums (subtracting the same amount from both preserves equality); verify at least one remains nonempty (since $S_1\neq S_2$).

**This is the archetype of a "hard" Pigeonhole proof — it requires (a) correctly counting the pigeon space (often via power sets or combinatorics), (b) correctly bounding the pigeonhole space, and (c) post-processing (like disjointifying) to get the final desired conclusion.**

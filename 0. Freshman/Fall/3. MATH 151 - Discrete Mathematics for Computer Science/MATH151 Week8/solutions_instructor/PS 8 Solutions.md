# MATH 151 — Problem Set 8 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

**Total: 100 points**, plus 8 bonus. All numeric results verified by computation.

---

## Part A — Pigeonhole Principle

### A1(a): 32 people, 12 months, share birth month ×3

Generalized Pigeonhole: $\lceil32/12\rceil=\lceil2.67\rceil=3$. So at least 3 people share a birth month. ∎

**Pigeons:** 32 people. **Pigeonholes:** 12 months.

---

### A1(b): 6 integers from $\{1,\ldots,20\}$, two sum to 21?

Pairs summing to 21: $\{1,20\},\{2,19\},\ldots,\{10,11\}$ — that's **10 pairs**.

With only 6 numbers chosen and 10 pigeonholes, $6<10$ — Pigeonhole does NOT force two numbers into the same pair.

**The claim is FALSE in general.** Counterexample: choose $\{1,2,3,4,5,6\}$ — no two of these sum to 21 (max possible sum is $5+6=11<21$).

*(This is a "trap" question testing whether students correctly verify pigeon>hole before applying the principle.)*

---

### A1(c): Socks — minimum to guarantee a matching pair

**Pigeons:** socks pulled. **Pigeonholes:** 3 colors.

By Pigeonhole, pulling 4 socks guarantees at least $\lceil4/3\rceil=2$ of the same color (since $4>3$).

Pulling only 3 socks could give one of each color (no match guaranteed).

**Answer: 4 socks.**

---

### A1(d): 100 integers, some nonempty subset sums to a multiple of 100

**Pigeons:** partial sums $S_1=a_1, S_2=a_1+a_2,\ldots,S_{100}=a_1+\cdots+a_{100}$ — 100 partial sums.

**Pigeonholes:** remainders mod 100: $\{0,1,\ldots,99\}$ — 100 values.

If any $S_i\equiv0\pmod{100}$, we're done (subset $\{a_1,\ldots,a_i\}$ works).

Otherwise, all 100 partial sums have remainders in $\{1,\ldots,99\}$ — only 99 possible values for 100 pigeons. By Pigeonhole, two partial sums $S_i,S_j$ ($i<j$) share a remainder, so $100\mid(S_j-S_i)=a_{i+1}+\cdots+a_j$ — a nonempty subset (in fact contiguous) summing to a multiple of 100. ∎

*(Note: this handles BOTH cases in one argument — either some single partial sum is ≡0, or two share a remainder.)*

---

### A1(e): 10 integers 1-100, two disjoint subsequences equal sum

Direct application of Lecture 5.3 Section 8's worked example: $2^{10}=1024$ subsets; sums range over $\{0,\ldots,1000\}$ (loose bound, 1001 values) since each of 10 integers ≤100. $1024>1001$ ⟹ two distinct subsets share a sum ⟹ disjointify to get two disjoint nonempty subsets with equal sums (as in the lecture's proof). ∎

---

### A1(f): Chess tournament, 17 players

Each player plays 16 games (against the other 16 players), so has a win-count $w\in\{0,1,\ldots,16\}$ — 17 possible values.

Suppose for contradiction no player has $\geq8$ wins AND no player has $\geq8$ losses.

"Not ≥8 wins" means $w\leq7$. "Not ≥8 losses" means losses $=16-w\leq7$, i.e., $w\geq9$.

But $w\leq7$ and $w\geq9$ cannot both hold — contradiction for EVERY player. So every player would need $w\in\emptyset$ — impossible.

**Proof.** Each player has $w\in\{0,\ldots,16\}$ wins. Either $w\geq8$ (at least 8 wins), or $w\leq7$, meaning losses $=16-w\geq9$ (at least 9, hence at least 8, losses). This covers every possible value of $w$, so every player satisfies one of the two conditions — in particular, at least one (in fact every) player does. ∎

---

---

## Part B — Inclusion–Exclusion Computations

### B1. *(6 pts)* Divisible by 3, 5, or 7 in $\{1,\ldots,1000\}$

| Term | Divisor | Count |
|---|---|---|
| $\lvert A_3\rvert$ | 3 | 333 |
| $\lvert A_5\rvert$ | 5 | 200 |
| $\lvert A_7\rvert$ | 7 | 142 |
| $\lvert A_3\cap A_5\rvert$ | $\mathrm{lcm}=15$ | 66 |
| $\lvert A_3\cap A_7\rvert$ | $\mathrm{lcm}=21$ | 47 |
| $\lvert A_5\cap A_7\rvert$ | $\mathrm{lcm}=35$ | 28 |
| $\lvert A_3\cap A_5\cap A_7\rvert$ | $\mathrm{lcm}=105$ | 9 |

$$333+200+142-66-47-28+9 = \mathbf{543}\qquad\text{none: } 1000-543=\mathbf{457}$$

*(Verified by direct enumeration.)*

*Marking: 3 for the seven counts with correct lcm divisors, 2 for the alternating sum, 1 for the
complement. Using $\lfloor1000/3\rfloor\cdot\lfloor1000/5\rfloor$ for an intersection loses 3.*

---

### B2. *(6 pts)* Developer survey

**(a)** $120+90+70-45-30-25+15 = \mathbf{195}$

**(b)** $200-195 = \mathbf{5}$

**(c)** Exactly one: Python only $=120-45-30+15=60$; C only $=90-45-25+15=35$;
Rust only $=70-30-25+15=30$. Total $\mathbf{125}$.

*Consistency check:* $125 + \underbrace{30+15+10}_{\text{exactly two}} + 15 = 195$ ✓

*Marking: 2/1/3. The $+15$ in each "only" formula is the discriminator. Require the consistency
check — it catches nearly every slip.*

---

### B3. *(8 pts)* At least one digit **and** at least one uppercase

Complement of "has a digit and has an uppercase" is "misses digits **or** misses uppercase" — a
union, so inclusion–exclusion applies to the complement:

$$62^8 - \left(52^8 + 36^8 - 26^8\right)$$

$$= 218{,}340{,}105{,}584{,}896 - \left(53{,}459{,}728{,}531{,}456 + 2{,}821{,}109{,}907{,}456 - 208{,}827{,}064{,}576\right) = \mathbf{162{,}268{,}094{,}210{,}560}$$

where $52^8$ misses digits (26+26 letters), $36^8$ misses uppercase (26 lower + 10 digits), and
$26^8$ misses both (lowercase only).

*Marking: 3 for recognising the complement is a union, 3 for the three alphabet sizes, 2 for
arithmetic. The commonest error is $62^8-52^8-36^8$, forgetting to add back the double-miss.*

---

### B4. *(8 pts)* Onto functions

Let $A_i$ be the functions missing codomain element $i$. A function missing a specified set of $k$
elements maps into the remaining $n-k$, so $\lvert\bigcap_{i\in S}A_i\rvert=(n-\lvert S\rvert)^m$.
Inclusion–exclusion on $\lvert\bigcup A_i\rvert$ and subtracting from $n^m$:

$$\#\text{onto} = \sum_{k=0}^{n}(-1)^k\binom{n}{k}(n-k)^m$$

For $m=6$, $n=3$:

$$3^6 - \binom31 2^6 + \binom32 1^6 - \binom33 0^6 = 729-192+3-0 = \mathbf{540}$$

**Sanity check:** $540 < 729 = 3^6$ ✓ — every onto function is a function, and some functions
(e.g. the constant maps) are not onto. *(Verified against exhaustive enumeration.)*

*Marking: 4 for the derivation naming $A_i$ correctly, 3 for the computation, 1 for the sanity check.*

---

## Part C — Derangements

### C1. *(5 pts)* $D_4$

$$D_4 = 4!\left(1 - 1 + \tfrac12 - \tfrac16 + \tfrac1{24}\right) = 24 \cdot \tfrac{9}{24} = \mathbf{9}$$

The nine derangements of $\{1,2,3,4\}$, in one-line notation:

$$2143,\ 2341,\ 2413,\ 3142,\ 3412,\ 3421,\ 4123,\ 4312,\ 4321$$

*(Verified by exhaustive enumeration of all 24 permutations.)*

*Marking: 3 for the formula computation, 2 for a complete and correct list. A list with 8 or 10
entries indicates a systematic error — check whether they included a permutation with a fixed point.*

---

### C2. *(5 pts)* Exactly two fixed points in $S_7$

Choose the two fixed points: $\binom72=21$. Derange the remaining five: $D_5=44$.

$$21 \times 44 = \mathbf{924}$$

*(Verified by enumerating all $5040$ permutations: exactly 924 have precisely two fixed points.)*

*Marking: 2 for $\binom72$, 2 for recognising the rest must be **deranged** (not merely permuted),
1 for arithmetic. Answering $\binom72\cdot5!=2520$ is the classic error — it permits further fixed
points, so it counts "at least two".*

---

### C3. *(5 pts)* $\sum_k\binom nk D_{n-k}=n!$ for $n=5$

$$\binom50 D_5+\binom51 D_4+\binom52 D_3+\binom53 D_2+\binom54 D_1+\binom55 D_0$$
$$= 1(44)+5(9)+10(2)+10(1)+5(0)+1(1) = 44+45+20+10+0+1 = \mathbf{120} = 5!\ \checkmark$$

**Why it must hold:** every permutation has *some* exact number of fixed points $k$, and
$\binom nk D_{n-k}$ counts precisely those with $k$. Summing over all $k$ partitions the $n!$
permutations into disjoint classes, so the total is $n!$.

*Marking: 3 for the computation, 2 for the partition argument. This is a counting-in-two-ways proof —
Week 7's technique.*

---

### C4. *(5 pts)* Convergence to $1/e$

| $n$ | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|
| $D_n/n!$ | 0.375000 | 0.366667 | 0.368056 | 0.367857 | 0.367882 |

$1/e = 0.367879$. The ratio first agrees to **three decimal places at $n=6$** ($0.368$), and by $n=8$
agrees to five.

Convergence is extremely fast because the series $\sum(-1)^k/k!$ is alternating with terms shrinking
like $1/k!$, so the error after $n$ terms is at most $1/(n+1)!$.

*Marking: 2 for the table, 1 for $n=6$, 2 for the rate explanation. Students who say only "it
converges" earn 2 of 5.*

---

## Part D — Choosing the Tool

### D1. *(4 pts each)*

**(a) Pigeonhole.** 13 people (pigeons), 12 months (pigeonholes), $13>12$ ⟹ two share a month. ∎

**(b) Inclusion–Exclusion.** Below 200: $\lfloor199/4\rfloor=49$, $\lfloor199/6\rfloor=33$,
$\lfloor199/12\rfloor=16$. Total $49+33-16=\mathbf{66}$.

**(c) Multiplication rule.** Five positions with a shrinking pool:
$26\cdot25\cdot24\cdot23\cdot22 = \mathbf{7{,}893{,}600}$.

**(d) Pigeonhole**, with constructed pigeonholes. Pigeons: the $2^{10}-1=1023$ non-empty subsets.
Pigeonholes: possible sums, at most $91+92+\cdots+100 = 955$. Since $1023>955$, two distinct subsets
share a sum. Removing their common elements leaves two *disjoint* subsets with equal sums. ∎

**(e) Derangements.** $D_n = n!\sum_{k=0}^n\frac{(-1)^k}{k!}$.

*Marking: 2 for the correct tool, 2 for the execution. (b) and (c) test whether students notice that
(b)'s categories overlap and (c)'s stages do not.*

---

### D2. *(4 pts)* The difference

**Pigeonhole answers "must one exist?" and returns a guarantee. Inclusion–exclusion answers "how
many?" and returns a number.** Pigeonhole never identifies the object; inclusion–exclusion never
proves existence (though a positive count implies it).

**Pigeonhole only:** "prove that among any 13 people two share a birth month." There is no count to
produce — the answer is a proof, and the number of such pairs depends on the particular group.

**Inclusion–exclusion only:** "how many integers below 200 are divisible by 4 or 6?" Nothing here
must be shown to exist; the task is an exact count over overlapping categories.

*Marking: 2 for the distinction, 1 for each example.*

---

### D3. *(4 pts)* Existence versus search

The subset-sum argument in D1(d) compares two *quantities* — 1023 subsets against at most 955 sums —
and concludes a collision must occur. **It never examines a single subset.** The proof's cost is
independent of the input.

Finding the colliding pair is a different problem. There are $2^{10}$ subsets to consider here, and
$2^n$ in general; subset-sum is NP-complete, so no algorithm is known that finds the pair in
polynomial time.

The general lesson: **a counting argument can establish that a solution exists without giving any
procedure to locate it.** Proofs of this kind are called *non-constructive*, and the gap between
"exists" and "can be found efficiently" is one of the central concerns of complexity theory.

*Marking: 2 for identifying the proof as non-constructive, 2 for the complexity contrast. Students
who merely restate the pigeonhole argument earn 1.*

---

## Bonus Solutions

### Bonus 1. *(4 pts)* $R(3,3)=6$

**Six suffices.** Fix a person $P$. $P$ has 5 relationships, each "acquaintance" or "stranger". By
pigeonhole, at least $\lceil5/2\rceil=3$ are of the same kind — say $P$ knows $A$, $B$, $C$.

If any two of $A,B,C$ know each other, they form a mutually-acquainted triangle with $P$. If none
do, then $A,B,C$ are mutual strangers. Either way a monochromatic triangle exists. ∎

**Five does not suffice.** Arrange 5 people in a cycle, with each person knowing their two
neighbours and being a stranger to the other two. Both the acquaintance graph ($C_5$) and the
stranger graph (also a 5-cycle) are triangle-free. *(Verified: neither $C_5$ nor its complement
contains a triangle.)* Hence $R(3,3)=6$ exactly.

*Marking: 2 for the upper bound with the pigeonhole step, 2 for the $C_5$ construction. Many
students prove only that 6 suffices, which shows $R(3,3)\le6$, not equality.*

---

### Bonus 2. *(4 pts)* Five points in a unit square

Partition the unit square into four closed sub-squares of side $\frac12$. Five points (pigeons) into
four sub-squares (pigeonholes) ⟹ some sub-square contains two points.

The greatest distance between two points of a $\frac12\times\frac12$ square is its diagonal,

$$\sqrt{\left(\tfrac12\right)^2+\left(\tfrac12\right)^2} = \frac{\sqrt2}{2} \approx 0.7071$$

so those two points are within $\frac{\sqrt2}{2}$ of each other. ∎

**Why 4 points fail.** With four points there is no forced sharing — place one at each corner of the
unit square and the minimum pairwise distance is 1, which exceeds $\frac{\sqrt2}{2}$. The argument
needs strictly more pigeons than holes.

*Marking: 2 for constructing the four sub-squares, 1 for the diagonal, 1 for the four-point
counterexample. Constructing the partition is the whole difficulty — nothing in the problem statement
mentions sub-squares.*

---

*MATH 151 · Week 8 · PS 8 Solutions · Instructor copy — do not distribute*

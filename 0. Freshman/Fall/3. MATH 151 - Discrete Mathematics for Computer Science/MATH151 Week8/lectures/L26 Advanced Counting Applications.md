# MATH 151 — Discrete Mathematics for Computer Science
## Lecture 8.3 (L26) — Advanced Counting: Choosing the Right Tool
### Friday, Week 8

---

## 1. Two Tools, Opposite Jobs

This week gave you two techniques, and students routinely reach for the wrong one because both
involve "counting things into boxes". They answer different questions.

| | **Pigeonhole** | **Inclusion–Exclusion** |
|---|---|---|
| Answers | *Does something exist?* | *How many are there?* |
| Output | An existence guarantee | An exact number |
| Tells you which one | **No** | Not directly, but the count is exact |
| Typical phrasing | "prove there must be two…" | "how many … satisfy at least one of…" |
| Cost | Free | $2^n$ terms |

**The diagnostic question: am I being asked to prove something exists, or to count?** "Show that
among any 13 people two share a birth month" is pigeonhole. "How many integers below 100 are
divisible by 2 or 3" is inclusion–exclusion. Nothing in either problem's surface wording tells you
which — the *type of the answer* does.

---

## 2. Counting the Complement

The single most useful habit in counting: **when "at least one" appears, count the opposite.**

$$\#(\text{at least one property}) = \text{total} - \#(\text{none of the properties})$$

### Worked example

How many 8-character passwords from a 62-character alphabet (26 lower, 26 upper, 10 digits) contain
**at least one digit**?

*Direct approach:* sum over passwords with exactly 1 digit, exactly 2 digits, … — eight cases, each
needing a position-choice and a multiplication. Slow and error-prone.

*Complement:* total minus those with **no** digit.

$$62^8 - 52^8 = 218{,}340{,}105{,}584{,}896 - 53{,}459{,}728{,}531{,}456 = \mathbf{164{,}880{,}377{,}053{,}440}$$

About **75.5%** of passwords contain a digit. One subtraction replaced eight cases.

### When the complement itself needs inclusion–exclusion

"At least one digit **and** at least one uppercase" — now the complement is "no digit **or** no
uppercase", which is a union, so:

$$62^8 - \left(52^8 + 36^8 - 26^8\right)$$

where $52^8$ misses digits, $36^8$ misses uppercase, and $26^8$ misses both. Verified:
$218{,}340{,}105{,}584{,}896 - (53{,}459{,}728{,}531{,}456 + 2{,}821{,}109{,}907{,}456 - 208{,}827{,}064{,}576) = \mathbf{162{,}268{,}094{,}210{,}560$}.

**The pattern to internalise:** complement turns "at least one" into "none"; if there are several
"at least one" requirements, the complement becomes a union and inclusion–exclusion handles it.

---

## 3. Pigeonhole With a Constructed Partition

Basic pigeonhole problems hand you the pigeonholes. Hard ones make you **invent** them, and that
invention is the entire difficulty.

### Worked example — the subset-sum argument

**Claim.** Any 10 distinct integers from $\{1, \ldots, 100\}$ contain two **different** non-empty
subsets with the same sum.

**Proof.** The pigeons are the non-empty subsets: $2^{10} - 1 = 1023$ of them.

The pigeonholes are the possible sums. Every subset sum is at least $1$ and at most
$91 + 92 + \cdots + 100 = 955$, so there are at most $955$ possible values.

Since $1023 > 955$, two distinct subsets share a sum. ∎

*(Verified: $2^{10}-1 = 1023$ and the largest attainable total is $955$.)*

**What made it hard.** Nothing in the statement mentions subsets. Recognising that the *pigeons*
should be subsets — not the integers themselves — is the whole insight. The pigeonholes, once you
have the pigeons, are forced.

**Note also what the proof does not give.** It does not identify the two subsets, and finding them
is genuinely hard — the subset-sum problem is NP-complete. **An existence proof can be trivial while
the corresponding search problem is intractable.** That gap is one of the deepest themes in computer
science, and here it is in one example.

---

## 4. A Combined Problem

*How many permutations of $\{1,\ldots,6\}$ fix **exactly one** element?*

Choose which element is fixed: $\binom{6}{1} = 6$ ways. Derange the other five so none of them is
fixed: $D_5 = 44$.

$$6 \times 44 = \mathbf{264}$$

*(Verified by exhaustive enumeration of all $720$ permutations: exactly 264 have precisely one fixed
point.)*

The multiplication rule (Week 7) supplies the outer structure; inclusion–exclusion (Wednesday)
supplies $D_5$. Most real counting problems are like this — a Week 7 skeleton with a Week 8 organ
inside.

**The generalisation:** the number of permutations of $n$ with exactly $k$ fixed points is
$\binom{n}{k} D_{n-k}$. Summing over $k$ recovers $n!$, which is a useful check:
$\sum_{k=0}^{6}\binom{6}{k}D_{6-k} = 720$.

---

## 5. A Decision Procedure

When a counting problem arrives, work through this in order.

1. **Am I proving existence, or counting?** Existence ⟹ pigeonhole. Counting ⟹ continue.
2. **Does "at least one" appear?** If so, count the complement.
3. **Are the categories disjoint?** Disjoint ⟹ plain addition rule. Overlapping ⟹ inclusion–exclusion.
4. **Are there independent stages?** ⟹ multiplication rule.
5. **Does order matter? Is repetition allowed?** ⟹ Week 7's four-fold classification.
6. **Is it "no element in its own place"?** ⟹ derangements.

**Steps 1 and 3 are where marks are lost.** Applying the addition rule to overlapping sets, or
reaching for a formula when the question said "prove there exist", are the two errors that recur
every year.

---

## 6. Summary

| | |
|---|---|
| Pigeonhole vs IE | existence vs exact count |
| Complement rule | "at least one" ⟹ total $-$ none |
| Several "at least one"s | complement is a union ⟹ inclusion–exclusion |
| Hard pigeonhole | you must **construct** the pigeonholes |
| Subset-sum example | $1023$ subsets, $\le 955$ sums ⟹ collision |
| Existence $\neq$ search | the collision is trivially proved, NP-hard to find |
| Exactly $k$ fixed points | $\binom nk D_{n-k}$, and $\sum_k \binom nk D_{n-k} = n!$ |

---

## 7. End-of-Lecture Exercises

1. How many 6-character strings over $\{a,\ldots,z\}$ contain at least one vowel? Use the complement.

2. How many integers in $\{1,\ldots,500\}$ are divisible by none of 2, 3, 7?

3. Prove: among any 6 people, either 3 mutually know each other or 3 are mutual strangers. *(This is the Ramsey number $R(3,3) = 6$. Fix one person; they have 5 relationships, so by pigeonhole at least 3 are of the same kind.)*

4. How many permutations of $\{1,\ldots,7\}$ fix exactly two elements?

5. Verify $\sum_{k=0}^{5}\binom{5}{k}D_{5-k} = 120$ using the derangement values from Lecture 8.2.

6. **(Stretch.)** Any 5 points placed inside a unit square have two within distance $\frac{\sqrt2}{2}$ of each other. Construct the pigeonholes, and explain why 4 points would not suffice for the argument.

---

## Reading

- **Rosen, 8e §6.2, §8.5, §8.6** — Pigeonhole, inclusion–exclusion, applications
- **Epp, 5e §9.4, §9.3** — Pigeonhole and inclusion–exclusion
- **Levin, 3e §1.6** — Advanced counting techniques

*Next: Week 9 — Recurrence Relations and Generating Functions*

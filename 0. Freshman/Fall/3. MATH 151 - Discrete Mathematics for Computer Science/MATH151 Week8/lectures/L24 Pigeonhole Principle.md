# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 24 (L24) — The Pigeonhole Principle
### Monday, Week 8

*“If numbers aren't beautiful, I don't know what is.”* — Paul Erdős, as quoted in *My Brain Is Open* (1998)

**Date:** Monday 16 November 2026 · 13:00–13:50 · Week 8

**Reading:** Rosen, 8e §6.2 · Epp, 5e §9.4 *(details at the end of the lecture)*

**Coursework:** 📊 **Quiz 8** today 13:00–13:15 · 🔬 **Lab 7** Wed 18 Nov 15:00–16:50 · 📝 **PS 7** due Fri 20 Nov 17:00 · 📝 **PS 8** released Fri 20 Nov 14:00, due Fri 27 Nov 17:00

---

> **Core Question:** What can we conclude, with certainty, just from counting — without knowing anything else about the objects involved?

---

## 1. The Principle — Simplest Form

**Theorem (Pigeonhole Principle).** If $n$ items are placed into $m$ containers, and $n > m$, then at least one container holds more than one item.

This seems almost too obvious to be a "theorem" — and yet it is one of the most powerful and widely-applied tools in discrete mathematics and computer science. Its power comes not from its proof (which is essentially immediate) but from the creativity required to correctly identify the "pigeons" and "pigeonholes" in a given problem.

**Formal statement in function language:** If $f: A \to B$ with $|A| > |B|$ (finite sets), then $f$ is not injective — i.e., there exist $a_1 \neq a_2$ with $f(a_1) = f(a_2)$.

**Proof.** [By contradiction] Suppose $f: A\to B$ is injective with $|A|>|B|$.

Since $f$ is injective, distinct elements of $A$ map to distinct elements of $B$. This means $|f(A)| = |A|$ (the image has the same size as the domain, since no two domain elements collide).

But $f(A) \subseteq B$, so $|f(A)| \leq |B|$.

Combining: $|A| = |f(A)| \leq |B|$, contradicting $|A| > |B|$.

Therefore no injective function exists from $A$ to $B$ when $|A|>|B|$ — equivalently, any function $f:A\to B$ must send at least two elements of $A$ to the same element of $B$. ∎

**Connection to Week 5's earlier material:** This proof is literally the counting consequence from Monday's lecture (Section 7 of Lecture 15) turned into a theorem: injective functions require $|A|\leq|B|$; its contrapositive is the Pigeonhole Principle.

---

## 2. Basic Applications

### Example 1

**Claim.** In any group of 13 people, at least two share a birth month.

**Proof.** There are 12 possible birth months (pigeonholes) and 13 people (pigeons). Since $13 > 12$, by the Pigeonhole Principle, at least two people must share a birth month. ∎

### Example 2

**Claim.** Among any 27 English words, at least two must start with the same letter.

**Proof.** The English alphabet has 26 letters (pigeonholes). With 27 words (pigeons) and $27 > 26$, two words must start with the same letter. ∎

### Example 3 — A Numerical Application

**Claim.** In any set of 6 integers chosen from $\{1, 2, \ldots, 10\}$, at least two of them sum to 11.

**Proof.** Partition $\{1,\ldots,10\}$ into 5 pairs, each summing to 11:
$$\{1,10\}, \{2,9\}, \{3,8\}, \{4,7\}, \{5,6\}$$

These 5 pairs are the pigeonholes. Choosing 6 integers (pigeons) from $\{1,\ldots,10\}$ means, by Pigeonhole ($6 > 5$), at least two of the chosen integers fall into the same pair.

Two integers from the same pair sum to exactly 11. ∎

**This example illustrates the key skill:** identifying the right partition into pigeonholes. The "pigeons" here are the chosen integers; the "pigeonholes" are the 5 sum-to-11 pairs — a construction that requires insight, not just mechanical application.

---

## 3. The Generalized Pigeonhole Principle

**Theorem (Generalized Pigeonhole Principle).** If $n$ items are placed into $m$ containers, then at least one container holds at least $\lceil n/m \rceil$ items.

(Here $\lceil x \rceil$ is the ceiling function — the smallest integer $\geq x$.)

**Proof.** [By contradiction] Suppose every container holds strictly fewer than $\lceil n/m\rceil$ items, i.e., at most $\lceil n/m\rceil - 1$ items each.

Total items $\leq m\cdot(\lceil n/m\rceil - 1)$.

Since $\lceil n/m \rceil < n/m + 1$, we get $\lceil n/m\rceil - 1 < n/m$, so:
$$m\cdot(\lceil n/m\rceil - 1) < m\cdot\frac{n}{m} = n$$

So the total is strictly less than $n$ — contradicting that we placed $n$ items.

Therefore some container holds at least $\lceil n/m\rceil$ items. ∎

### Example 4

**Claim.** Among any 100 people, at least $\lceil 100/12\rceil = 9$ were born in the same month.

**Proof.** By the Generalized Pigeonhole Principle with $n=100$ pigeons and $m=12$ pigeonholes: at least $\lceil 100/12\rceil = \lceil 8.33\rceil = 9$ people share a birth month. ∎

---

## 4. Application to Hash Functions and Data Structures

**Claim.** If a hash table has $m$ buckets and $n > m$ keys are inserted (using any hash function), at least one bucket contains more than one key (a collision is guaranteed).

**Proof.** Direct application of the Pigeonhole Principle: the hash function $h: \text{Keys} \to \{0,\ldots,m-1\}$ maps $n$ keys (pigeons) into $m$ buckets (pigeonholes). Since $n>m$, some bucket receives at least two keys. ∎

**Consequence for algorithm design:** No hash function can avoid collisions when the number of keys exceeds the number of buckets — collision handling (chaining, open addressing) is not an optional feature but a mathematical necessity whenever $n>m$. This directly motivates the CS 101 material on collision resolution.

### The Birthday Paradox (Preview of MATH 251)

While Pigeonhole guarantees a collision when $n>m$, in practice collisions become *likely* far before $n$ reaches $m$ — with $m=365$, only $n=23$ people are needed for a >50% chance of a shared birthday, even though Pigeonhole only *guarantees* a collision at $n=366$. This "birthday paradox" refines Pigeonhole with probability theory (MATH 251) and is the basis of birthday-attack analysis in cryptographic hash function security.

---

## 5. Application to Lossless Compression — A CS Impossibility Proof

**Theorem.** No lossless compression algorithm can compress every possible input of length $n$ bits to strictly fewer than $n$ bits.

**Proof.** Suppose, for contradiction, that a compression function $C$ maps every $n$-bit string to a string of length strictly less than $n$ bits, and that $C$ is injective (required for lossless — i.e., invertible — compression, per Thursday's lecture).

The domain has $2^n$ possible $n$-bit strings.

The codomain — strings of length $< n$ — has $\sum_{k=0}^{n-1} 2^k = 2^n - 1$ possible strings (geometric series, Week 3!).

Since $2^n > 2^n - 1$, by the Pigeonhole Principle, $C$ cannot be injective — some two distinct $n$-bit inputs must map to the same compressed output.

This contradicts the requirement that $C$ be injective (losslessness).

Therefore, no such compression algorithm exists. ∎

**Practical meaning:** Real compression algorithms (ZIP, gzip) work because most real-world data is NOT uniformly random — they exploit statistical redundancy. But this theorem proves, with mathematical certainty, that *some* inputs must get longer (or stay the same) under any lossless compression scheme — you cannot shrink every possible input. This is a foundational impossibility result in information theory (Claude Shannon, 1948).

---

## 6. Application to Sequences — The Erdős–Szekeres Theorem (Preview)

**Claim.** Among any sequence of $n^2+1$ distinct real numbers, there exists either an increasing subsequence of length $n+1$ or a decreasing subsequence of length $n+1$.

*(Full proof is more involved and typically covered in a combinatorics course — we state it here as a striking example of Pigeonhole's reach, and prove a simpler special case.)*

### A Simpler Related Result

**Claim.** Among any 5 distinct integers, some 3 of them, in the order given, are either increasing or decreasing (a monotonic subsequence of length 3).

*(This follows from Erdős–Szekeres with $n=2$: $n^2+1=5$.)*

We won't prove the general theorem here, but note the technique: assign to each element $a_i$ in the sequence a pair $(L_i, D_i)$ where $L_i$ = length of longest increasing subsequence ending at $a_i$, $D_i$ = length of longest decreasing subsequence ending at $a_i$. If no monotonic subsequence of length $n+1$ exists, then $L_i, D_i \in \{1,\ldots,n\}$ for all $i$ — giving at most $n^2$ possible pairs $(L_i,D_i)$. With $n^2+1$ elements, two elements share a pair — Pigeonhole — which leads to a contradiction (details: an involved but classic argument).

---

## 7. Application to Function Properties — Repeating Values

**Claim.** Let $f: \{1,\ldots,n+1\} \to \{1,\ldots,n\}$ be any function. Then $f$ is not injective.

**Proof.** Direct Pigeonhole: domain has $n+1$ elements, codomain has $n$ elements, $n+1>n$. ∎

**Application — proving a repeated remainder exists:**

**Claim.** Among any $n+1$ integers, at least two have the same remainder when divided by $n$.

**Proof.** Define $f: \{a_1,\ldots,a_{n+1}\} \to \{0,1,\ldots,n-1\}$ by $f(a_i) = a_i \bmod n$. The domain has $n+1$ elements; the codomain (possible remainders mod $n$) has $n$ elements. By Pigeonhole, $f$ is not injective — some $a_i, a_j$ ($i\neq j$) satisfy $f(a_i)=f(a_j)$, i.e., $a_i \equiv a_j \pmod n$. ∎

**Corollary — a classic application:** Among any $n+1$ integers, some two have a difference divisible by $n$. *(Direct from the above: if $a_i\equiv a_j\pmod n$, then $n\mid(a_i-a_j)$.)*

---

## 8. A Harder Worked Example — Subset Sums

**Claim.** Given any set of 10 distinct integers, each between 1 and 100, there exist two disjoint subsets with equal sums.

**Proof.** The given set $S$ has $|S|=10$. The number of subsets of $S$ is $|\mathcal{P}(S)| = 2^{10} = 1024$ (Week 4!).

Each subset has a sum between 0 (empty subset) and at most $100+99+\cdots+91 = 955$ (sum of the 10 largest possible values, as an upper bound — in fact any specific 10 integers from 1-100 sum to at most $100\times10=1000$, so subset sums range over $\{0,1,\ldots,1000\}$, giving at most 1001 possible sum values).

We have 1024 subsets (pigeons) but only 1001 possible sum values (pigeonholes), and $1024 > 1001$.

By Pigeonhole, two DIFFERENT subsets $S_1 \neq S_2$ have the same sum.

If $S_1$ and $S_2$ happen to overlap, remove the common elements from both: $S_1' = S_1 - (S_1\cap S_2)$ and $S_2' = S_2 - (S_1\cap S_2)$ are now disjoint, still have equal sums (equal amounts were removed from each), and are still distinct subsets (since $S_1\neq S_2$ means at least one had an element the other lacked, which survives removal of the common part) — unless one becomes empty, but since $S_1 \ne S_2$, at least one of $S_1', S_2'$ is nonempty, and if the other is empty its sum is 0, forcing the nonempty one's sum to be 0 too — only possible if all its elements are 0, impossible since elements are between 1 and 100. So both $S_1', S_2'$ are nonempty and disjoint with equal sums. ∎

**This proof exemplifies the full power of Pigeonhole reasoning: identifying an enormous but finite space (subsets), an even larger pigeon count than pigeonhole count, and then doing careful bookkeeping (disjointifying) to extract the final combinatorial conclusion.**

---

## 9. Summary

```
Pigeonhole Principle (basic):
  n items, m containers, n > m ⟹ some container has ≥ 2 items
  Equivalently: |A| > |B| ⟹ no injective f: A → B

Generalized Pigeonhole Principle:
  n items, m containers ⟹ some container has ≥ ⌈n/m⌉ items

Applications:
  - Hash collisions guaranteed when keys > buckets
  - No lossless compression works on all inputs
  - Repeated remainders among n+1 integers mod n
  - Monotonic subsequences (Erdős–Szekeres)
  - Equal subset sums
```

---

## 10. End-of-Lecture Exercises

1. Prove: in any group of 367 people, at least two share the same birthday (including Feb 29).

2. Prove: among any 51 integers chosen from $\{1,\ldots,100\}$, at least two of them differ by exactly 1, or... *(actually prove the classic version)*: among any 51 integers from $\{1,\ldots,100\}$, some two are such that one divides the other. *(Hint: write each integer as $2^k \cdot m$ with $m$ odd; there are only 50 possible odd values $m\in\{1,3,\ldots,99\}$; use Pigeonhole on the odd parts.)*

3. Prove: any 5 points chosen inside a unit square (side length 1) must include two points at distance $\leq \frac{\sqrt{2}}{2}$ from each other. *(Hint: divide the square into 4 smaller squares of side 1/2.)*

4. A computer program processes a stream of $n$ distinct integers and must determine if any two consecutive elements (in original array order, not sorted) sum to a fixed target $T$. Explain why Pigeonhole is NOT directly applicable to this problem (i.e., not every counting problem is a Pigeonhole problem) — what's different about this scenario?

5. Prove: given any 12 integers, there exist two whose difference is divisible by 11.

6. **Challenge:** Prove that in any sequence of $n$ integers $a_1, a_2, \ldots, a_n$ (not necessarily distinct), there exists a contiguous subsequence (i.e., $a_i, a_{i+1}, \ldots, a_j$ for some $i \leq j$) whose sum is divisible by $n$.

   *Hint:* Consider the partial sums $S_0 = 0, S_1 = a_1, S_2 = a_1+a_2, \ldots, S_n = a_1+\cdots+a_n$ — that's $n+1$ partial sums. Apply Pigeonhole to their remainders mod $n$.

---

## Reading

- **Rosen, 8e §6.2** — The pigeonhole principle
- **Epp, 5e §9.4** — The pigeonhole principle

*Week 5 complete. Week 6: Relations — Reflexive, Symmetric, Transitive; Equivalence Relations and Partial Orders.*

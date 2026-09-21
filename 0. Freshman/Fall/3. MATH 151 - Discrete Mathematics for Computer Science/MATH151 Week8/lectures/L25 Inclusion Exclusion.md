# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 25 (L25) — The Principle of Inclusion–Exclusion
### Thursday, Week 8

**Date:** Thursday 19 November 2026 · 13:00–13:50 · Week 8

---

## 1. The Problem With Adding

Week 7's addition rule says: if $A$ and $B$ are **disjoint**, then $|A \cup B| = |A| + |B|$.

That word *disjoint* does a great deal of work. Drop it and the rule fails immediately — count the
students taking Maths or Physics by adding the two class lists, and everyone taking both is counted
twice.

The fix is to subtract the overlap:

$$|A \cup B| = |A| + |B| - |A \cap B|$$

This is the **Principle of Inclusion–Exclusion** in its smallest case. The rest of the lecture is
what happens with three sets, with $n$ sets, and what it is good for.

---

## 2. Three Sets

$$|A \cup B \cup C| = |A| + |B| + |C| - |A\cap B| - |A\cap C| - |B\cap C| + |A\cap B\cap C|$$

**Why the last term returns.** Track an element in all three sets. The singles count it $3$ times;
the pairs remove it $3$ times, leaving $0$; so it must be added back once. Every element must end up
counted **exactly once**, and the alternating signs are precisely what achieves that.

### Worked example — verified

How many integers in $\{1, \ldots, 100\}$ are divisible by 2, 3, or 5?

| Set | Count |
|---|---|
| $\lvert A_2\rvert = \lfloor 100/2\rfloor$ | $50$ |
| $\lvert A_3\rvert = \lfloor 100/3\rfloor$ | $33$ |
| $\lvert A_5\rvert = \lfloor 100/5\rfloor$ | $20$ |
| $\lvert A_2 \cap A_3\rvert = \lfloor 100/6\rfloor$ | $16$ |
| $\lvert A_2 \cap A_5\rvert = \lfloor 100/10\rfloor$ | $10$ |
| $\lvert A_3 \cap A_5\rvert = \lfloor 100/15\rfloor$ | $6$ |
| $\lvert A_2 \cap A_3 \cap A_5\rvert = \lfloor 100/30\rfloor$ | $3$ |

$$50 + 33 + 20 - 16 - 10 - 6 + 3 = \mathbf{74}$$

*(Verified by direct enumeration: the union has exactly 74 elements.)*

**The complement is often the real prize.** Integers divisible by **none** of 2, 3, 5:
$100 - 74 = \mathbf{26}$. Counting the complement is usually far easier than counting the thing you
want, and inclusion–exclusion is the tool that makes the trade.

**Note $\lvert A_2 \cap A_3\rvert$ used $\lfloor 100/6 \rfloor$, not $\lfloor 100/2\rfloor \cdot \lfloor 100/3\rfloor$.**
The intersection of "divisible by 2" and "divisible by 3" is "divisible by $\mathrm{lcm}(2,3) = 6$".
This is the single most common error in these problems.

---

## 3. The General Statement

> **Theorem (Inclusion–Exclusion).** For finite sets $A_1, \ldots, A_n$,
>
> $$\left|\bigcup_{i=1}^{n} A_i\right| = \sum_{\emptyset \neq S \subseteq \{1,\ldots,n\}} (-1)^{|S|+1}\left|\bigcap_{i \in S} A_i\right|$$

In words: add all the singles, subtract all the pairs, add all the triples, subtract all the
quadruples, and so on.

**Proof sketch.** Take an element lying in exactly $k$ of the sets, $k \geq 1$. It is counted in
$\binom{k}{j}$ of the $j$-fold intersections, so its total contribution is

$$\sum_{j=1}^{k} (-1)^{j+1}\binom{k}{j} = 1 - \sum_{j=0}^{k}(-1)^{j}\binom{k}{j} = 1 - 0 = 1$$

using $\sum_{j=0}^{k}(-1)^j\binom{k}{j} = (1-1)^k = 0$ for $k \geq 1$ — which is Week 7's binomial
theorem doing the work. Every element is counted exactly once. ∎

**The cost.** There are $2^n - 1$ terms. Inclusion–exclusion is exact but exponential, which is why
it is a tool for small $n$ or for structured problems where most intersections vanish or coincide.

---

## 4. Counting Surjections

How many **onto** functions are there from an $m$-set to an $n$-set?

Let $A_i$ be the set of functions that **miss** element $i$ of the codomain. A function fails to be
onto exactly when it lies in some $A_i$. Any function missing a specified set of $k$ codomain
elements is a function into the remaining $n-k$, and there are $(n-k)^m$ of those. So

$$\#\text{onto} = \sum_{k=0}^{n}(-1)^k\binom{n}{k}(n-k)^m$$

**Verified against brute-force enumeration:**

| $m$ | $n$ | Formula | Enumerated |
|---|---|---|---|
| 3 | 2 | 6 | 6 ✓ |
| 4 | 2 | 14 | 14 ✓ |
| 4 | 3 | 36 | 36 ✓ |
| 5 | 3 | 150 | 150 ✓ |
| 5 | 4 | 240 | 240 ✓ |

Note this counts **surjections**, the Week 5 notion, using a Week 8 technique — and there is no
simple closed form. That absence is itself informative: surjections are genuinely harder to count
than injections, for which the answer is just the falling factorial $n(n-1)\cdots(n-m+1)$.

---

## 5. Derangements — The Classic Application

A **derangement** is a permutation with **no fixed point**: nothing stays where it started.

*The hat-check problem: $n$ people leave hats at a cloakroom and each receives a hat at random. What
is the chance nobody gets their own?*

Let $A_i$ be the permutations fixing position $i$. A permutation fixing a specified set of $k$
positions permutes the rest freely — there are $(n-k)!$ of them, and $\binom{n}{k}$ ways to choose
which $k$. Inclusion–exclusion gives

$$D_n = n!\sum_{k=0}^{n}\frac{(-1)^k}{k!}$$

**Verified against exhaustive enumeration:**

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $D_n$ | 1 | 0 | 1 | 2 | 9 | 44 | 265 | 1854 | 14833 |

Every value confirmed by generating all $n!$ permutations and counting those with no fixed point.

### The surprise

$$\frac{D_n}{n!} = \sum_{k=0}^{n}\frac{(-1)^k}{k!} \longrightarrow e^{-1} \approx 0.3679$$

**The probability that nobody gets their own hat converges to $1/e$ — and it barely moves after
$n = 4$.** With 4 people it is $9/24 = 0.375$; with 8 people, $14833/40320 = 0.3679$. Whether the
cloakroom holds ten coats or ten thousand, about 37% of the time nobody is reunited with their own.

For $n \geq 1$, $D_n$ is the **nearest integer to $n!/e$** — verified for all $n \leq 8$ above.

---

## 6. In Computer Science

**Counting with constraints.** "How many passwords of length 8 contain at least one digit, one
uppercase, and one symbol?" is inclusion–exclusion on the complements — count all strings, subtract
those missing a required class, add back those missing two, and so on.

**Database query estimation.** A query planner estimating rows matching `WHERE a OR b OR c` uses
inclusion–exclusion on the individual selectivities. It usually truncates after pairs, because the
$2^n$ term count is unaffordable and higher intersections are small — an approximation known as the
Bonferroni inequalities, where truncating after an odd number of terms over-estimates and after an
even number under-estimates.

**Sieve algorithms.** The Sieve of Eratosthenes is inclusion–exclusion made incremental, and
counting integers coprime to $n$ gives Euler's totient
$\varphi(n) = n\prod_{p \mid n}\left(1 - \frac1p\right)$ — an inclusion–exclusion over the distinct
prime divisors. Week 12 returns to this.

**Why exponential cost matters.** Because inclusion–exclusion is exact but $2^n$, practical systems
either restrict to small $n$, exploit structure that collapses terms, or accept a truncation. This
trade-off — exact and slow versus approximate and fast — recurs throughout algorithms.

---

## 7. Summary

| Idea | Statement |
|---|---|
| Two sets | $\lvert A \cup B\rvert = \lvert A\rvert + \lvert B\rvert - \lvert A\cap B\rvert$ |
| Three sets | singles $-$ pairs $+$ triple |
| General | alternating sum over all $2^n - 1$ non-empty subsets |
| Why signs alternate | so each element is counted exactly once; rests on $(1-1)^k = 0$ |
| Intersections | $\lvert A_a \cap A_b\rvert$ uses $\mathrm{lcm}(a,b)$, **not** the product |
| Complement trick | count what you don't want, subtract from the total |
| Surjections | $\sum_k (-1)^k \binom nk (n-k)^m$ |
| Derangements | $D_n = n!\sum_k \frac{(-1)^k}{k!}$, nearest integer to $n!/e$ |
| $D_n/n!$ | $\to 1/e \approx 0.368$, essentially constant from $n=4$ |
| Cost | $2^n$ terms — exact but exponential |

---

## 8. End-of-Lecture Exercises

1. How many integers in $\{1,\ldots,1000\}$ are divisible by 3, 5, or 7? How many by none of them?

2. In a class of 40, 25 take Maths, 20 take Physics, and 8 take both. How many take neither?

3. Compute the number of onto functions from a 6-set to a 3-set using the formula in §4. Sanity-check it against $3^6$, the number of functions with no onto requirement, and explain why no bijection exists in this case.

4. Compute $D_4$ directly from the formula and verify it against the value 9 in §5. Then list all 9 derangements of $\{1,2,3,4\}$ explicitly.

5. How many permutations of $\{1,\ldots,6\}$ fix **exactly one** element? *(Hint: choose the fixed point, derange the rest.)*

6. **(Stretch.)** Prove the Bonferroni inequality: truncating inclusion–exclusion after the singles gives an over-estimate of $\lvert\bigcup A_i\rvert$, and truncating after the pairs gives an under-estimate.

---

## Reading

- **Rosen, 8e §8.5, §8.6** — Inclusion–exclusion and its applications
- **Epp, 5e §9.3** — Counting with inclusion–exclusion
- **Levin, 3e §1.6** — Advanced counting

*Next: Lecture 26 — Advanced Counting: Putting Pigeonhole and Inclusion–Exclusion to Work*

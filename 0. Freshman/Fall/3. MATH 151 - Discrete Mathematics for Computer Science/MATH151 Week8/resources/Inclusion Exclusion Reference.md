# MATH 151 — Inclusion–Exclusion Reference
## Week 8: Advanced Counting

---

## The Formula

**Two sets**
$$|A \cup B| = |A| + |B| - |A \cap B|$$

**Three sets**
$$|A \cup B \cup C| = |A|+|B|+|C| - |A\cap B|-|A\cap C|-|B\cap C| + |A\cap B\cap C|$$

**General**
$$\left|\bigcup_{i=1}^{n} A_i\right| = \sum_{\emptyset \neq S \subseteq \{1..n\}} (-1)^{|S|+1}\left|\bigcap_{i\in S} A_i\right|$$

Add singles, subtract pairs, add triples, subtract quadruples, …

**Cost:** $2^n - 1$ terms. Exact but exponential.

---

## The Complement Rule

$$\#(\text{at least one}) = \text{total} - \#(\text{none})$$

**Whenever a problem says "at least one", try the complement first.** It converts a sum over many
cases into a single subtraction.

If there are *several* "at least one" requirements, the complement becomes a **union** and needs
inclusion–exclusion itself:

$$\#(\ge 1\text{ digit AND} \ge 1\text{ upper}) = 62^8 - \left(52^8 + 36^8 - 26^8\right)$$

Verified: $218{,}340{,}105{,}584{,}896 - (53{,}459{,}728{,}531{,}456 + 2{,}821{,}109{,}907{,}456 - 208{,}827{,}064{,}576) = 162{,}268{,}094{,}210{,}560$.

---

## Divisibility Problems

| Want | Use |
|---|---|
| Divisible by $a$ in $\{1..N\}$ | $\lfloor N/a \rfloor$ |
| Divisible by $a$ **and** $b$ | $\lfloor N/\mathrm{lcm}(a,b) \rfloor$ |

> **The commonest error in this entire week:** using $\lfloor N/a\rfloor \cdot \lfloor N/b\rfloor$
> for the intersection. The intersection of "divisible by $a$" and "divisible by $b$" is
> "divisible by $\mathrm{lcm}(a,b)$" — use $\lfloor N/6 \rfloor$, not $\lfloor N/2\rfloor\lfloor N/3\rfloor$.

**Verified example**, $N=100$, divisors 2, 3, 5:

$$50 + 33 + 20 - 16 - 10 - 6 + 3 = 74 \qquad \text{(none: } 100 - 74 = 26\text{)}$$

---

## Standard Applications

### Surjections (onto functions), $m$-set → $n$-set

$$\#\text{onto} = \sum_{k=0}^{n}(-1)^k\binom{n}{k}(n-k)^m$$

| $m$ | $n$ | Value |
|---|---|---|
| 3 | 2 | 6 |
| 4 | 2 | 14 |
| 4 | 3 | 36 |
| 5 | 3 | 150 |
| 5 | 4 | 240 |
| 6 | 3 | 540 |

*All verified against exhaustive enumeration.* There is no simple closed form — contrast injections,
which are just $n(n-1)\cdots(n-m+1)$.

### Derangements — permutations with no fixed point

$$D_n = n!\sum_{k=0}^{n}\frac{(-1)^k}{k!}$$

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $D_n$ | 1 | 0 | 1 | 2 | 9 | 44 | 265 | 1854 | 14833 |

*Verified by exhaustive enumeration for every $n \le 8$.*

**For $n \ge 1$, $D_n$ is the nearest integer to $n!/e$.**

$$\frac{D_n}{n!} \to \frac1e \approx 0.3679$$

Convergence is extremely fast — stable to three decimals from $n = 6$:

| $n$ | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|
| $D_n/n!$ | 0.375000 | 0.366667 | 0.368056 | 0.367857 | 0.367882 |

**Exactly $k$ fixed points:** $\binom{n}{k}D_{n-k}$, and $\sum_{k}\binom nk D_{n-k} = n!$.

---

## Pigeonhole vs Inclusion–Exclusion

| | **Pigeonhole** | **Inclusion–Exclusion** |
|---|---|---|
| Question | Does it exist? | How many? |
| Output | Existence guarantee | Exact number |
| Identifies the object | No | No, but the count is exact |
| Wording clue | "show that there must be…" | "how many … at least one of…" |
| Cost | Free | $2^n$ |

**Diagnostic: is the answer a *number* or a *guarantee*?**

---

## Decision Procedure

1. Proving existence, or counting? → existence means Pigeonhole
2. Does "at least one" appear? → count the complement
3. Are the categories disjoint? → disjoint means plain addition; overlapping means inclusion–exclusion
4. Independent stages? → multiplication rule
5. Order? Repetition? → Week 7's four-fold classification
6. "Nothing in its own place"? → derangements

---

## Common Errors

| ❌ | ✅ |
|---|---|
| $\lfloor N/a\rfloor\lfloor N/b\rfloor$ for the intersection | $\lfloor N/\mathrm{lcm}(a,b)\rfloor$ |
| Addition rule on overlapping sets | Subtract the overlap |
| Forgetting to add the triple intersection back | Signs alternate all the way up |
| Enumerating cases when "at least one" appears | Complement |
| Using Pigeonhole to produce a count | It only proves existence |
| Expecting Pigeonhole to identify the objects | It never does |

---

*MATH 151 · Week 8 · Reference · © CSE Department*

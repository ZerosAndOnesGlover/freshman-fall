# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 5.3 (L17) — Bijections and Cardinality
### Friday, Week 5

**Date:** Friday 30 October 2026 · 13:00–13:50 · Week 5

---

## 1. Counting Without Counting

How do you know two sets have the same size?

The obvious answer — count both and compare — works only for finite sets, and even then it presumes
you already know what "count" means. There is a better answer, and it is the whole content of this
lecture:

> **Definition.** Two sets $A$ and $B$ have the **same cardinality**, written $|A| = |B|$, if there
> exists a **bijection** $f: A \to B$.

No numbers appear in that definition. A shepherd who pairs each sheep with one pebble knows whether
the flock is complete without being able to count past three. Pairing is more primitive than
counting, and — as we will see in §5 — it keeps working where counting cannot follow.

This is why Monday's bijections matter beyond bookkeeping. A bijection is a **proof of equal size**.

---

## 2. Finite Sets: The Sanity Check

For finite sets, the definition agrees with counting, as it must.

**Claim.** If $|A| = n$ and $f: A \to B$ is a bijection, then $|B| = n$.

**Proof.** $f$ is injective, so the $n$ values $f(a)$ for $a \in A$ are distinct — giving at least
$n$ elements of $B$. $f$ is surjective, so every element of $B$ is one of those values — giving at
most $n$. Hence exactly $n$. ∎

**A worked example of counting by bijection.** How many subsets does an $n$-element set have?

Build a bijection from $\mathcal{P}(A)$ to the set of length-$n$ bit strings: given $S \subseteq A$,
send it to the string whose $i$-th bit is 1 exactly when the $i$-th element of $A$ lies in $S$.

- **Injective:** different subsets differ on some element, hence differ in that bit.
- **Surjective:** every bit string describes a subset — read the 1s off.

There are $2^n$ bit strings, so $|\mathcal{P}(A)| = 2^n$. Verified: $n = 0,1,2,3,4,5$ give
$1, 2, 4, 8, 16, 32$.

**Notice what happened.** We never enumerated subsets. We exhibited a bijection to something we
already knew how to count. This is the standard technique of Week 7's combinatorics, arriving two
weeks early.

---

## 3. Infinite Sets: Where Intuition Breaks

**Definition.** A set is **countably infinite** if it has the same cardinality as
$\mathbb{N} = \{0, 1, 2, \ldots\}$ — that is, if its elements can be listed as a sequence with every
element appearing exactly once. A set is **countable** if it is finite or countably infinite.

### The evens

$f: \mathbb{N} \to \{0,2,4,\ldots\}$, $f(n) = 2n$, is a bijection.

So there are **exactly as many even naturals as naturals**, even though the evens are a proper
subset. For finite sets this is impossible — a proper subset is strictly smaller. Infinite sets are
precisely the ones where it is possible; that is one standard *definition* of infinite.

### The integers

A proper subset can match the whole. Can a strictly larger-looking set match too?

$$f(n) = \begin{cases} n/2, & n \text{ even}\\[2pt] -(n+1)/2, & n \text{ odd}\end{cases}$$

Verified — the first twelve values are

$$0,\ -1,\ 1,\ -2,\ 2,\ -3,\ 3,\ -4,\ 4,\ -5,\ 5,\ -6$$

and running $n$ from $0$ to $2000$ produces exactly the integers $-1000$ through $1000$, each once.
So $|\mathbb{Z}| = |\mathbb{N}|$.

The trick is the **zig-zag**: alternate sides of zero so that every integer is reached after finitely
many steps. Listing $0, 1, 2, 3, \ldots$ first and *then* the negatives would not be a listing at all
— nothing negative would ever have a finite position.

### Pairs of naturals

$\mathbb{N} \times \mathbb{N}$ looks two-dimensional, hence much bigger. It is not. The **Cantor
pairing function**

$$\pi(x,y) = \frac{(x+y)(x+y+1)}{2} + y$$

is a bijection $\mathbb{N} \times \mathbb{N} \to \mathbb{N}$. Verified: injective on all of
$[0,60)^2$, and its values cover $\{0, 1, \ldots, 500\}$ exactly.

It walks the grid along **finite anti-diagonals** — $(0,0)$, then $(1,0), (0,1)$, then
$(2,0), (1,1), (0,2)$, and so on. Every pair sits on some diagonal, and every diagonal is finite, so
every pair gets a finite index.

**Consequence:** $\mathbb{Q}$ is countable. Write each rational as a pair (numerator, denominator),
list the pairs by the diagonal walk, and skip any fraction not in lowest terms. Countably many
items with some deleted is still countable.

---

## 4. Not Everything Is Countable

At this point the pattern suggests every infinite set is countable. It is not.

> **Theorem (Cantor).** $\mathbb{R}$ is not countable.

**Proof (diagonalisation).** It suffices to show the interval $[0,1)$ is uncountable. Suppose it were
countable, so every real in $[0,1)$ appears in a list $r_0, r_1, r_2, \ldots$, each written in decimal:

$$
\begin{aligned}
r_0 &= 0.\,\mathbf{d_{00}}\,d_{01}\,d_{02}\ldots\\
r_1 &= 0.\,d_{10}\,\mathbf{d_{11}}\,d_{12}\ldots\\
r_2 &= 0.\,d_{20}\,d_{21}\,\mathbf{d_{22}}\ldots
\end{aligned}
$$

Define a new number $x = 0.x_0x_1x_2\ldots$ by

$$x_i = \begin{cases} 5, & d_{ii} \neq 5\\ 6, & d_{ii} = 5\end{cases}$$

Then $x \in [0,1)$, but $x \neq r_i$ for every $i$, because $x$ differs from $r_i$ in the $i$-th
decimal place. So $x$ is missing from a list that was assumed to contain everything —
a contradiction. ∎

*(Digits 5 and 6 are chosen to dodge the $0.4999\ldots = 0.5000\ldots$ ambiguity: numbers built only
from 5s and 6s have exactly one decimal representation.)*

The same argument, one level up:

> **Theorem (Cantor).** For **every** set $A$, $|\mathcal{P}(A)| > |A|$.

For finite $A$ this is just $2^n > n$. For infinite $A$ it says there is no largest infinity — the
hierarchy never terminates.

---

## 5. Why a CS Student Should Care

This is not decoration. It is a hard limit on your profession, provable today.

**How many programs are there?** A program is a finite string over a finite alphabet. Strings of
length 1, then length 2, then length 3 — each block finite, blocks listed in order. That is a listing.
**The set of all programs is countable.**

**How many functions $\mathbb{N} \to \{0,1\}$ are there?** Such a function *is* an infinite bit
sequence, and the diagonal argument of §4 applies verbatim. **Uncountably many.**

A countable set cannot be mapped onto an uncountable one. Therefore:

> **Almost every function $\mathbb{N} \to \{0,1\}$ is not computed by any program** — not because we
> have not found the algorithm, but because there are not enough programs to go around.

Note how cheap this was. We did not exhibit a single uncomputable function; we counted. CS 101's
Week 11 constructs a specific one — the halting problem — by diagonalisation, which is this section's
argument applied to machines instead of digits. **Same technique, different objects.**

Two more consequences of the same flavour:

- **No lossless compressor shrinks every input.** There are $2^n$ strings of length $n$ but only
  $2^n - 1$ shorter strings, so no injective map from the former to the latter exists. Week 8 gives
  this its name.
- **Real numbers cannot all be stored.** A `double` has 64 bits, so it takes at most $2^{64}$ values;
  the reals in $[0,1)$ are uncountable. Floating-point error is not sloppy engineering — it is a
  cardinality argument.

---

## 6. Summary

| Idea | Statement |
|---|---|
| Equal cardinality | $\lvert A\rvert = \lvert B\rvert$ **iff** a bijection $A \to B$ exists |
| Counting by bijection | Map to something already counted — e.g. $\lvert\mathcal{P}(A)\rvert = 2^n$ via bit strings |
| Countably infinite | A bijection with $\mathbb{N}$ — equivalently, a listing hitting each element once |
| Evens, $\mathbb{Z}$, $\mathbb{N}\times\mathbb{N}$, $\mathbb{Q}$ | All countable |
| $\mathbb{R}$ | **Un**countable — diagonalisation |
| Cantor's theorem | $\lvert\mathcal{P}(A)\rvert > \lvert A\rvert$ always; no largest infinity |
| Programs | Countable |
| Functions $\mathbb{N}\to\{0,1\}$ | Uncountable ⟹ almost all are uncomputable |

**The one sentence to keep:** a bijection is a proof of equal size, and it is the only notion of size
that survives contact with infinity.

---

## 7. End-of-Lecture Exercises

1. Exhibit a bijection $\mathbb{N} \to \{1, 4, 9, 16, \ldots\}$ (the perfect squares) and conclude
   the squares are countable, despite becoming ever sparser.

2. Prove that the union of two countable sets is countable. *(Hint: interleave the two listings.)*

3. Compute $\pi(3,4)$ and $\pi(4,3)$ with the Cantor pairing function. Explain from the diagonal walk
   why they differ, and find which pair maps to $14$.

4. Give a bijection between $(0,1)$ and $\mathbb{R}$. *(Hint: a trigonometric or rational function
   will do.)* What does this say about "length" as a measure of size?

5. The set of **finite** subsets of $\mathbb{N}$ is countable, but $\mathcal{P}(\mathbb{N})$ is not.
   Explain precisely where the listing argument succeeds for the first and fails for the second.

6. **(Stretch.)** Adapt the diagonal argument to prove there is no surjection $A \to \mathcal{P}(A)$
   for any set $A$. *(Consider $D = \{a \in A : a \notin f(a)\}$.)*

---

## Reading

- **Rosen, 8e §2.5** — Cardinality of sets
- **Epp, 5e §7.4** — Cardinality and countability
- **Levin, 3e §1.9** — Counting and bijections

*Next: Week 6 — Relations: reflexive, symmetric, transitive; equivalence classes*

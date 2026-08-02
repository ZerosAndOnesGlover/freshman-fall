# MATH 151 · Cardinality Reference
## Week 5: Bijections and the Sizes of Infinite Sets

---

## The Definition

> $\lvert A\rvert = \lvert B\rvert$ **iff** there exists a **bijection** $f: A\to B$.

No numbers appear. Pairing is more primitive than counting, and it is the only notion of size that
survives contact with infinity.

**A bijection is a proof of equal size.** That is the whole idea of the lecture.

---

## Finite Sets

For finite $A$, a bijection to $B$ forces $\lvert B\rvert=\lvert A\rvert$ — injectivity gives at
least $n$ elements, surjectivity at most $n$.

**Counting by bijection.** $\lvert\mathcal{P}(A)\rvert = 2^n$: map each subset to the length-$n$ bit
string marking its members. Different subsets differ in some bit; every bit string names a subset.

*Verified: $n=0..5$ gives $1, 2, 4, 8, 16, 32$.*

**Nothing was enumerated.** The technique — map to something already counted — is Week 7's method,
arriving early.

---

## Countable Sets

> **Countably infinite:** in bijection with $\mathbb{N}$ — equivalently, listable as a sequence
> hitting every element exactly once.
> **Countable:** finite or countably infinite.

| Set | Bijection | Countable? |
|---|---|---|
| Evens | $n\mapsto 2n$ | **Yes** |
| $\mathbb{Z}$ | zig-zag (below) | **Yes** |
| $\mathbb{N}\times\mathbb{N}$ | Cantor pairing | **Yes** |
| $\mathbb{Q}$ | pairs, lowest terms | **Yes** |
| Perfect squares | $n\mapsto(n+1)^2$ | **Yes** |
| Finite subsets of $\mathbb{N}$ | group by maximum | **Yes** |
| $\mathbb{R}$ | — | **No** |
| $\mathcal{P}(\mathbb{N})$ | — | **No** |

### The zig-zag, $\mathbb{N}\to\mathbb{Z}$

$$f(n)=\begin{cases}n/2,&n\text{ even}\\-(n+1)/2,&n\text{ odd}\end{cases}$$

*Verified first twelve values:* $0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5, -6$. Running $n=0..2000$
produces exactly the integers $-1000..1000$, each once.

**Why alternating matters:** listing all non-negatives first and then the negatives is not a listing
at all — no negative number would ever reach a finite position.

### Cantor pairing, $\mathbb{N}\times\mathbb{N}\to\mathbb{N}$

$$\pi(x,y)=\frac{(x+y)(x+y+1)}{2}+y$$

*Verified: injective on $[0,60)^2$, and its values cover $\{0,\ldots,500\}$ exactly.*

It walks **finite anti-diagonals**: $(0,0)$; then $(1,0),(0,1)$; then $(2,0),(1,1),(0,2)$; …

| Pair | $\pi$ |
|---|---|
| $(3,4)$ | 32 |
| $(4,3)$ | 31 |
| $(0,4)$ | 14 |

**To invert:** find the diagonal $d$ with $\frac{d(d+1)}2\le N<\frac{(d+1)(d+2)}2$, then $y=N-\frac{d(d+1)}2$
and $x=d-y$.

---

## Uncountable Sets

> **Theorem (Cantor).** $\mathbb{R}$ is uncountable.

**Diagonalisation.** Given any list $r_0,r_1,\ldots$ of reals in $[0,1)$, build $x$ whose $i$-th
decimal digit differs from $r_i$'s. Then $x$ is in $[0,1)$ but on no line of the list.

*Use digits 5 and 6 only, to avoid the $0.4999\ldots = 0.5000\ldots$ ambiguity.*

> **Cantor's theorem.** $\lvert\mathcal{P}(A)\rvert>\lvert A\rvert$ for **every** set $A$.

For finite $A$ this is $2^n>n$. For infinite $A$ it says **there is no largest infinity**.

---

## The CS Payoff

| | Cardinality |
|---|---|
| Programs (finite strings over a finite alphabet) | **Countable** |
| Functions $\mathbb{N}\to\{0,1\}$ | **Uncountable** |

A countable set cannot map onto an uncountable one, so:

> **Almost every function $\mathbb{N}\to\{0,1\}$ is computed by no program.**

Not because the algorithm is undiscovered — because there are not enough programs. **The proof is
pure counting and exhibits no specific example.** CS 101's Week 11 constructs one (the halting
problem) by the same diagonal argument applied to machines.

Two more consequences:

- **No lossless compressor shrinks every input** — $2^n$ strings of length $n$, only $2^n-1$ shorter
  ones, so no injection exists. *(Week 8 names this the Pigeonhole Principle.)*
- **Floating point cannot be fixed.** A 64-bit `double` takes at most $2^{64}$ values; the reals in
  $[0,1)$ are uncountable. Rounding error is a cardinality fact, not an engineering defect.

---

## Common Errors

| ❌ | ✅ |
|---|---|
| "Infinite sets all have the same size" | $\mathbb{R}$ is strictly bigger than $\mathbb{N}$ |
| "A proper subset is smaller" | True only for **finite** sets — the evens match $\mathbb{N}$ |
| Listing $\mathbb{Z}$ as $0,1,2,\ldots$ then negatives | Not a listing; nothing negative gets a finite position |
| "Sparse ⟹ uncountable" | The squares have density zero and are countable |
| "No formula ⟹ not a function" | Notation is a convenience, not a definition |
| Confusing length with cardinality | $(0,1)$ and $\mathbb{R}$ have the same cardinality |

---

*MATH 151 · Week 5 · Reference · © CSE Department*

# CS 102 — Computer Science II
## Lecture 06: BST Height — Average and Worst Case

---

## 1. The Question

Lecture 05 established that every interesting BST operation costs $\Theta(h)$, and Lecture 04 that

$$\lceil\log_2(n+1)\rceil - 1 \;\le\; h \;\le\; n - 1.$$

The gap between those bounds is the difference between a useful data structure and a linked list.
**So which end do we actually get?**

The answer has three parts, and only the third is comfortable:

1. **Worst case:** $h = n-1$, and it arises from the most natural input there is.
2. **Average case over random insertion orders:** $h = \Theta(\log n)$ — good.
3. **But you do not control the insertion order**, which is why Week 2 exists.

---

## 2. The Worst Case Is the Common Case

Insert $1, 2, 3, \ldots, n$ into an empty BST. Each key is larger than every key present, so each
becomes the right child of the previous one:

```
1
 \
  2
   \
    3
     \
      4
```

Height $n-1$. Search is $\Theta(n)$. **Measured:** inserting $1..1000$ in order gives height exactly
999.

Descending order gives the mirror image. Alternating patterns give other degenerate shapes.

**The uncomfortable part is that sorted input is not adversarial, it is normal.** It is what arrives
from a database export ordered by primary key, a log file in timestamp order, a sorted CSV, or any
upstream stage that happened to sort. A data structure whose worst case is triggered by *tidy* input
is a hazard, because the failure appears in production on real data and not in testing on synthetic
data.

> **This is the difference between worst case and adversarial case.** Quicksort's $\Theta(n^2)$ needs
> a specific pathological pivot sequence and is avoidable by randomising. A BST's $\Theta(n)$ needs
> only sorted input.

---

## 3. The Average Case

Now assume the $n!$ insertion orders are equally likely. Two different quantities are worth knowing,
and they have different constants.

### 3.1 Average node depth — the cost of a typical search

The expected **internal path length** (the sum of all node depths) of a random BST is exactly

$$\text{IPL}(n) = 2(n+1)H_n - 4n, \qquad H_n = \sum_{i=1}^{n}\tfrac1i$$

so the expected depth of a node is

$$\frac{\text{IPL}(n)}{n} \;\approx\; 2\ln n - 4 + 2\gamma \;\approx\; 2\ln n - 2.85 \;\approx\; 1.386\log_2 n - 2.85$$

where $\gamma \approx 0.5772$ is the Euler–Mascheroni constant.

**Measured against the formula** (mean over repeated random builds):

| $n$ | formula | measured |
| --- | --- | --- |
| $1{,}000$ | 10.99 | 10.83 |
| $10{,}000$ | 15.58 | 15.61 |
| $100{,}000$ | 20.18 | 20.15 |

**A random BST is about 39% worse than a perfectly balanced one** on average search cost — the
constant $1.386 = 2\ln 2$ against $1$ — which is a very acceptable price.

### 3.2 Expected height — the cost of the worst search

Height is *not* the same question, and its constant is larger. The expected height of a random BST is

$$\mathbb{E}[h] \;\sim\; 4.311\ln n \;\approx\; 2.99\log_2 n$$

a result due to Devroye. **Convergence is notoriously slow**, so do not expect measurements at
practical $n$ to match it:

| $n$ | measured mean height | $4.311\ln n$ |
| --- | --- | --- |
| $1{,}000$ | 20.3 | 29.8 |
| $10{,}000$ | 30.2 | 39.7 |
| $100{,}000$ | 39.8 | 49.6 |

The measured values sit well below the asymptote because the next term is $-1.953\ln\ln n$ plus a
negative constant. **The point stands regardless: $\Theta(\log n)$, with a constant around 2–3.**

> **A methodological note worth absorbing.** An asymptotic result can be correct and still be a poor
> predictor at the sizes you care about. Quoting "expected height is $4.311\ln n$" for $n = 1000$
> would overstate the truth by 47%. **Check asymptotics against measurement before relying on them
> numerically** — this is the same lesson as Lab 0's D4.

---

## 4. Why "Average Case" Does Not Save You

The average-case result assumes **all insertion orders equally likely**. That assumption is usually
false.

| Source of data | Realistic order | BST outcome |
| --- | --- | --- |
| Database export by primary key | Sorted | **Degenerate** |
| Log entries | Sorted by time | **Degenerate** |
| User IDs as created | Nearly sorted | **Nearly degenerate** |
| Hash values | Effectively random | Fine |
| Shuffled input | Random | Fine |

**Three of five common cases are the bad one.**

You might propose shuffling the input before insertion. Sometimes you can, and randomised BSTs
(treaps) formalise the idea. But it fails whenever data arrives **online** — one item at a time, with
queries interleaved — which is most of the situations where you wanted a dynamic structure rather
than a sorted array in the first place. **You cannot shuffle a stream you have not finished
receiving.**

---

## 5. What Would Fix This

We need a structure that **guarantees** $h = \Theta(\log n)$ regardless of insertion order.

The idea, in one sentence: **detect when an insertion has made the tree too unbalanced, and
restructure locally to fix it.** For that we need

1. a **balance condition** that implies $h = O(\log n)$, and is cheap to check;
2. a **restructuring operation** that repairs a violation without breaking the BST invariant, in
   $O(1)$ time;
3. a proof that **$O(1)$ repairs per insertion suffice**.

Next week supplies all three: the AVL height-balance condition, the **rotation**, and the theorem
that one rotation (or a double rotation) restores balance after any single insertion.

**The BST invariant does not change.** Everything from Lecture 05 — search, inorder, successor —
carries over verbatim. Week 2 adds a *second* invariant about shape, maintained alongside the first.

---

## 6. Summary

| | Balanced | Random | Degenerate |
| --- | --- | --- | --- |
| Height | $\Theta(\log n)$ | $\Theta(\log n)$ | $\Theta(n)$ |
| Search / insert / delete | $\Theta(\log n)$ | $\Theta(\log n)$ expected | $\Theta(n)$ |
| Arises from | Deliberate balancing | Shuffled input | **Sorted input** |
| Guaranteed? | **Yes** (Week 2) | No | — |

**The one-line summary of this week:** a BST gives you sorted-order access with dynamic updates,
which no array or list can do — but its performance depends on a shape you do not control, and
fixing that is next week's subject.

---

## 7. Exercises

**1.** Give an insertion order for $\{1,\ldots,7\}$ producing a perfectly balanced BST. How many such
orders are there?

**2.** Give an insertion order for $\{1,\ldots,7\}$ other than fully ascending or descending that
still produces height 6.

**3.** Using $\text{IPL}(n) = 2(n+1)H_n - 4n$, compute the expected average node depth for
$n = 15$ exactly. Compare with the perfectly balanced tree of 15 nodes. What is the ratio?

**4.** You must store 10 million records and support lookup by key. Argue for or against a plain BST
in each case: (a) keys arrive pre-sorted, (b) keys are random UUIDs, (c) keys arrive sorted but you
may buffer all of them before building the tree.

**5.** Explain why shuffling does not rescue the online case. Give a concrete application where the
online constraint is real.

---

*CS 102 · Week 1 · Lecture 06 · © CSE Department*

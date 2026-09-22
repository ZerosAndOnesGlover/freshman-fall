# CS 102 · Computer Science II
## Lecture 02: Complexity Analysis, Reviewed and Sharpened

**Date:** Wednesday 20 January 2027 · 09:00–09:50 · Week 0

---

## 1. Why Review This

You met Big-O in CS 101. This lecture is not a repeat; it fixes the three things that CS 101
deliberately left slightly loose and that will now start to matter.

1. $O$, $\Omega$ and $\Theta$ are **different claims**, and this course will hold you to the
   difference.
2. Worst case, average case and amortised case are **three different questions**. Week 2 depends on
   the third.
3. Recurrence relations are how recursive algorithms are analysed, and from Week 5 you will be
   writing them yourself.

---

## 2. The Three Notations

For functions $f, g : \mathbb{N} \to \mathbb{R}^{\ge 0}$:

$$f(n) = O(g(n)) \iff \exists\, c > 0,\, n_0 \text{ such that } f(n) \le c\,g(n) \text{ for all } n \ge n_0$$

$$f(n) = \Omega(g(n)) \iff \exists\, c > 0,\, n_0 \text{ such that } f(n) \ge c\,g(n) \text{ for all } n \ge n_0$$

$$f(n) = \Theta(g(n)) \iff f(n) = O(g(n)) \text{ and } f(n) = \Omega(g(n))$$

In words: **$O$ is an upper bound, $\Omega$ is a lower bound, $\Theta$ is both** — a tight
characterisation.

### The distinction is not pedantry

Both of these statements are true of merge sort:

- Merge sort runs in $O(n^2)$ time.
- Merge sort runs in $\Theta(n \log n)$ time.

The first is *true* and nearly useless. $O$ is an upper bound, and $n\log n \le c\,n^2$ certainly
holds. Saying merge sort is $O(n^2)$ is like saying a lecture is under nine hours long.

**When you can state $\Theta$, state $\Theta$.** Use $O$ when you genuinely only have an upper bound
— which is common and honest, for instance when an algorithm's exact behaviour depends on the input
in a way you have not fully characterised.

> **The commonest error in this course's problem sets:** writing $O$ where the question asked you to
> show a bound is *tight*. An upper bound does not establish tightness. To show $\Theta(n\log n)$ you
> must exhibit an input family forcing $\Omega(n \log n)$ as well.

### A note on the abuse of notation

$f(n) = O(g(n))$ uses "=" for what is really set membership — $f \in O(g)$. This is universal and you
should get used to it, but remember it is **not symmetric**: $n = O(n^2)$ is true and
$n^2 = O(n)$ is false. Never chain these equalities as if they were real ones.

---

## 3. Cases: Worst, Average, Amortised

These are answers to three different questions and are routinely confused.

| Case | Question | Example |
| --- | --- | --- |
| **Worst** | Over all inputs of size $n$, what is the maximum cost? | Quicksort: $\Theta(n^2)$ |
| **Average** | Over a stated input distribution, what is the expected cost? | Quicksort: $\Theta(n\log n)$ |
| **Amortised** | Over a *sequence* of operations, what is the cost per operation? | Dynamic array append: $\Theta(1)$ |

**Average case requires you to state the distribution.** "Average case" with no stated distribution
is meaningless — quicksort's $\Theta(n\log n)$ average assumes all input orderings equally likely,
which is false for the very common case of already-sorted data.

**Amortised is not average.** Amortised analysis makes **no probabilistic assumption at all**. It is
a worst-case guarantee about a sequence: appending $n$ items to a dynamic array costs $\Theta(n)$
total, so $\Theta(1)$ each, *however the operations are ordered*. Some individual appends cost
$\Theta(n)$ — the ones that trigger a resize — but they are rare enough to pay for themselves.

You will need this properly in **Week 6**, where union-find's near-constant amortised cost is what
makes Kruskal's algorithm fast, and the guarantee is genuinely worst-case-over-sequences.

---

## 4. Analysing Loops

Counting is mechanical once you see it as summation.

```python
# (a)  Theta(n)
for i in range(n):
    work()

# (b)  Theta(n^2)
for i in range(n):
    for j in range(n):
        work()

# (c)  Theta(n^2) — NOT Theta(n^2/2); constants vanish
for i in range(n):
    for j in range(i):
        work()

# (d)  Theta(log n)
i = 1
while i < n:
    work()
    i *= 2

# (e)  Theta(n log n)
for i in range(n):
    j = 1
    while j < n:
        work()
        j *= 2
```

For (c), the count is $\sum_{i=0}^{n-1} i = \frac{n(n-1)}{2} = \Theta(n^2)$. The constant $\tfrac12$
disappears — which is the point of asymptotic notation, and also the reason it can mislead you about
real running times when the constants differ a lot.

For (d), the loop runs while $2^k < n$, so $k < \log_2 n$: $\Theta(\log n)$ iterations. **The base of
the logarithm does not matter** in asymptotic notation, since $\log_a n = \log_b n / \log_b a$ and
that is a constant factor. Inside a $\Theta$, $\log n$ is unambiguous.

---

## 5. Recurrences

A recursive algorithm's cost is described by a recurrence. Three methods, in increasing order of
power and decreasing order of convenience.

### 5.1 The Master Theorem

For $T(n) = a\,T(n/b) + f(n)$ with $a \ge 1$, $b > 1$, let $c_{\text{crit}} = \log_b a$.

| Case | Condition | Result |
| --- | --- | --- |
| 1 | $f(n) = O(n^{c})$ for some $c < c_{\text{crit}}$ | $T(n) = \Theta(n^{c_{\text{crit}}})$ |
| 2 | $f(n) = \Theta(n^{c_{\text{crit}}}\log^k n)$, $k \ge 0$ | $T(n) = \Theta(n^{c_{\text{crit}}}\log^{k+1} n)$ |
| 3 | $f(n) = \Omega(n^{c})$ for some $c > c_{\text{crit}}$, plus regularity | $T(n) = \Theta(f(n))$ |

**Worked:**

- **Merge sort:** $T(n) = 2T(n/2) + \Theta(n)$. Here $c_{\text{crit}} = \log_2 2 = 1$, and
  $f(n) = \Theta(n^1)$ — Case 2 with $k=0$. So $T(n) = \Theta(n\log n)$. ✓
- **Binary search:** $T(n) = T(n/2) + \Theta(1)$. $c_{\text{crit}} = \log_2 1 = 0$,
  $f(n) = \Theta(n^0)$ — Case 2 with $k=0$. So $T(n) = \Theta(\log n)$. ✓
- **Naive matrix multiply by blocks:** $T(n) = 8T(n/2) + \Theta(n^2)$. $c_{\text{crit}} = \log_2 8
  = 3$, and $n^2$ is $O(n^c)$ for $c=2 < 3$ — Case 1. So $T(n) = \Theta(n^3)$. ✓
- **Strassen's:** $T(n) = 7T(n/2) + \Theta(n^2)$. $c_{\text{crit}} = \log_2 7 \approx 2.807$ — Case 1
  again, giving $\Theta(n^{\log_2 7}) = \Theta(n^{2.807})$, which is why Strassen's matters.

**The Master Theorem does not always apply.** It says nothing about $T(n) = 2T(n-1) + O(1)$ — the
subproblem shrinks by *subtraction*, not division. That recurrence solves to $\Theta(2^n)$, and
recognising when the theorem is inapplicable is as important as applying it.

### 5.2 Recursion trees

Draw the tree, sum the work per level, sum the levels. This is how you *see* why merge sort is
$n \log n$: each of $\log n$ levels does $\Theta(n)$ work.

### 5.3 Substitution

Guess the answer and prove it by induction. The most powerful and the least convenient; needed in
Week 6 for union-find and in Week 8 for some DP bounds.

---

## 6. Space Complexity

Count the memory used **beyond the input**.

| Algorithm | Time | Auxiliary space |
| --- | --- | --- |
| Merge sort | $\Theta(n\log n)$ | $\Theta(n)$ |
| Heap sort | $\Theta(n\log n)$ | $\Theta(1)$ |
| Quicksort | $\Theta(n\log n)$ avg | $\Theta(\log n)$ stack, avg |
| Insertion sort | $\Theta(n^2)$ | $\Theta(1)$ |

**Heap sort's $\Theta(1)$ auxiliary space is why Week 3 exists** even though merge sort already gives
you $n\log n$. When memory is the binding constraint — and on embedded targets or with data near the
size of RAM it is — the space column decides.

Do not forget the recursion stack. A recursive function of depth $d$ uses $\Theta(d)$ space even if
it allocates nothing, which is why unbalanced recursion can exhaust memory before it exhausts time.

---

## 7. What Asymptotic Analysis Hides

Three honest caveats, because this course will otherwise teach you a slightly false picture.

1. **Constants can dominate at real sizes.** Insertion sort beats merge sort for small $n$ — real
   library sorts switch to insertion sort below a threshold of roughly 10–30 elements.
2. **The memory hierarchy is invisible to the model.** An $O(n)$ algorithm with poor locality can
   lose to an $O(n \log n)$ one with sequential access. This is why Week 3 makes a point of heaps
   being arrays rather than linked nodes.
3. **The model assumes uniform-cost operations.** Comparing two integers and comparing two long
   strings are both "one comparison" in our counting, and are not remotely the same cost.

**None of this makes asymptotic analysis wrong.** It makes it a first question rather than the only
one. You will measure the difference yourself in Lab 0.

---

*CS 102 · Week 0 · Lecture 02 · © CSE Department*

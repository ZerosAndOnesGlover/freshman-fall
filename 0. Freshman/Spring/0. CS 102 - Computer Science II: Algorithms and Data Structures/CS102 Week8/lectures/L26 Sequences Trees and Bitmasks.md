# CS 102 · Computer Science II
## Lecture 26: Sequences, Trees, and Bitmasks

**Date:** Wednesday 17 March 2027 · 09:00–09:50 · Week 8

---

## 1. Three More State Designs

Lecture 25's state was an interval. This lecture has three more shapes, chosen because each one
teaches a different lesson about state:

| problem | state | lesson |
| --- | --- | --- |
| longest increasing subsequence | "ending at $i$" | the *suffix* of the decision matters |
| coin change | the remaining amount | when greedy fails and why |
| DP on trees | a vertex, plus a flag | the recursion structure **is** the subproblem order |
| DP on bitmasks | a **set**, plus a position | $n!$ can be reduced to $2^n$ |

---

## 2. Longest Increasing Subsequence

**Problem.** The longest subsequence of an array whose values strictly increase.

### The state that works

The obvious state — "the LIS of the first $i$ elements" — **fails**, and it fails for a reason worth
naming: it does not record what the last element was, so you cannot tell whether the next element may
extend it.

The state that works is **"the longest increasing subsequence *ending at* index $i$"**:

$$L[i] = 1 + \max\{L[j] : j < i,\ a[j] < a[i]\}, \qquad \text{answer} = \max_i L[i]$$

```python
def lis(a):
    d = [1] * len(a)
    for i in range(len(a)):
        for j in range(i):
            if a[j] < a[i] and d[j] + 1 > d[i]: d[i] = d[j] + 1
    return max(d) if a else 0
```

$\Theta(n^2)$. **Note that the answer is $\max_i L[i]$, not $L[n-1]$** — the LIS need not end at the
last element, and forgetting that is the second most common error here.

> **"Ending at $i$" is the single most useful state pattern in this course.** It made maximum-subarray
> linear on PS 7, it makes LIS work here, and it is the right first guess whenever a prefix state
> refuses to yield a recurrence.

### The $O(n\log n)$ version

Keep an array `tails`, where `tails[k]` is the **smallest possible tail** of any increasing
subsequence of length $k+1$ seen so far. It is automatically sorted, so binary search applies:

```python
def lis_fast(a):
    tails = []
    for x in a:
        i = bisect.bisect_left(tails, x)
        if i == len(tails): tails.append(x)     # x extends the longest run
        else: tails[i] = x                      # x gives a better tail at that length
    return len(tails)
```

*(Verified against the $\Theta(n^2)$ version on 2,000 random arrays. **0 mismatches.**)*

| $n$ | $\Theta(n^2)$ | $O(n\log n)$ | speedup |
| --- | --- | --- | --- |
| 1,000 | 27.7 ms | 0.15 ms | 185× |
| 4,000 | 421.5 ms | 0.64 ms | 661× |
| 16,000 | 6,725.9 ms | 2.81 ms | **2,397×** |

### The trap

**`tails` is not an LIS.** It has the right *length* and is generally not a subsequence of the input at
all.

```
a     = [1, 3, 5, 2]
tails = [1, 2, 5]          <- not a subsequence: 5 appears before 2 in a
an LIS = [1, 3, 5]
```

*(Verified. The smallest counterexample is `[2, 3, 1]`, whose `tails` is `[1, 3]`. Over 3,000 random
arrays, `tails` fails to be a subsequence **47%** of the time.)*

To recover an actual LIS you must record, for each element, the index of its predecessor — the same
`parent`-array technique as every other reconstruction this term. **The fast algorithm gives you a
number; the answer costs extra bookkeeping.** This is the third time that pattern has appeared, after
rolled DP tables and rolled knapsack rows.

---

## 3. Coin Change, and Why Greedy Fails

**Problem.** Given denominations and a target $T$, use the fewest coins.

$$C[t] = 1 + \min_{c_i \le t} C[t - c_i], \qquad C[0] = 0$$

$\Theta(kT)$ — and, exactly as with knapsack, **pseudo-polynomial**, since $T$ is written in
$\log T$ bits.

### The interesting part

Everyone's instinct is greedy: take the largest coin that fits. On real currency that works:

| system | greedy failures for $T = 1 \dots 199$ |
| --- | --- |
| UK $[1,2,5,10,20,50,100,200]$ | **0** |
| US $[1,5,10,25]$ | **0** |
| $[1,5,6,9]$ | **84** |
| $[1,3,4]$ | **49** |

*(Verified.)*

The smallest failure for $[1,5,6,9]$ is $T = 11$: greedy takes $9 + 1 + 1 = $ **3 coins**, the optimum
is $5 + 6 = $ **2**. For $[1,3,4]$ it is $T = 6$: greedy $4+1+1 = 3$, optimum $3+3 = 2$.

A coin system where greedy is always optimal is called **canonical**. Real currencies are canonical
because they were designed to be — it is a property of the denominations, not of the algorithm.

> **This is Week 9's opening question in miniature.** Greedy is faster and simpler when it works, and
> it works only when the problem has a property you must *prove*. "It works on the examples I tried" is
> exactly the reasoning that fails here at $T = 11$ — and there is no way to see that from the code.

---

## 4. DP on Trees

When the input is a tree, the subproblem structure is handed to you: **a subtree is a subproblem**, and
the recursion order is the tree's own postorder. No loop bounds to get right.

### Maximum-weight independent set

**Problem.** Choose a set of vertices of maximum total weight, no two adjacent.

The state needs a flag, for the reason familiar from §2 — whether the parent may still choose itself
depends on whether this vertex was chosen:

$$\mathrm{inc}[u] = w_u + \sum_{c} \mathrm{exc}[c], \qquad
\mathrm{exc}[u] = \sum_{c} \max(\mathrm{inc}[c], \mathrm{exc}[c])$$

The answer is $\max(\mathrm{inc}[\text{root}], \mathrm{exc}[\text{root}])$.

$\Theta(V)$ — **each vertex is one subproblem with two states**, and every edge is used once.

*(Verified against $2^n$ brute-force enumeration on 300 random trees. **0 mismatches.**)*

Compare that with the general graph: **maximum independent set on an arbitrary graph is NP-complete**
(Week 12). On a tree it is linear. The difference is that a tree's subproblems are independent —
removing a vertex disconnects its subtrees from each other — and in a general graph they are not.

> **Restricting the input structure can move a problem across the tractability boundary.** You saw this
> in Week 5 with longest paths (easy on a DAG, NP-complete in general) and it will recur in Week 12.

**Implementation note.** The natural recursive version hits Python's recursion limit on a deep tree —
the same issue as Week 4 Lecture 15 §1. Use an explicit postorder: push, record the order, then
process it in reverse.

---

## 5. DP on Bitmasks

Sometimes the state genuinely must be **a set**. Encode the set as the bits of an integer.

```python
mask & (1 << i)         # is i in the set?
mask | (1 << i)         # add i
mask & ~(1 << i)        # remove i
bin(mask).count('1')    # size
```

### Travelling salesman

**Problem.** Visit all $n$ cities and return to the start, minimising total distance.

Naive enumeration is $(n-1)!$ tours. The DP state is **(set of visited cities, current city)**:

$$\mathrm{dp}[S][v] = \min_{u \in S \setminus \{v\}} \big(\mathrm{dp}[S \setminus \{v\}][u] + d(u,v)\big)$$

$2^n \cdot n$ states, $O(n)$ work each: **$O(2^n n^2)$**.

*(Verified against $(n-1)!$ brute force on 200 random instances. **0 mismatches.**)*

| $n$ | $(n-1)!$ | $2^n n^2$ | ratio |
| --- | --- | --- | --- |
| 10 | 362,880 | 102,400 | 4× |
| 15 | 87,178,291,200 | 7,372,800 | 11,824× |
| 20 | $1.2\times10^{17}$ | 419,430,400 | $2.9\times10^{8}$× |
| 25 | $6.2\times10^{23}$ | 20,971,520,000 | $3\times10^{13}$× |

**The state design that matters** is realising that the *order* in which you visited the cities is
irrelevant — only **which** you visited and **where you are now**. That collapses $n!$ paths into
$2^n \cdot n$ states, and it is the same move as knapsack's "only the total weight matters, not which
items".

### Be clear about what this is not

$O(2^n n^2)$ is **still exponential**. At $n = 25$ it is 21 billion operations — hours, and the memory
is worse. This does not make TSP tractable; it makes $n \approx 20$ possible where $n \approx 13$ was
the limit.

**TSP is NP-hard** (Week 12), and Held–Karp is the best known exact algorithm — from 1962, and still
unbeaten in the exponent. Week 12 shows the 2-approximation that Week 6's MST provides, which is what
you use when $n$ is large.

---

## 6. What to Do

- Read CLRS §14.3 again with these examples in mind, and §15.5 for the tree case.
- **PS 8** implements LIS both ways, coin change with a canonicality test, and tree DP.
- **Lab 8** is Floyd–Warshall, which is next lecture.
- **PROJECT 1 is due Friday of Week 9.**
- Next lecture: all-pairs shortest paths, whose state is "which vertices may be used as intermediates"
  — the least guessable state in the course.

---

*CS 102 · Week 8 · Lecture 26 · © CSE Department*

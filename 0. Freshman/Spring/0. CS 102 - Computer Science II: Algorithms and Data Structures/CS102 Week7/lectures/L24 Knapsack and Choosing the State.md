# CS 102 · Computer Science II
## Lecture 24: Knapsack, and How to Choose the State

---

## 1. 0/1 Knapsack

**Problem.** $n$ items, item $i$ with weight $w_i$ and value $v_i$, and a capacity $W$. Choose a subset
of maximum total value with total weight at most $W$. Each item is taken **once or not at all** — hence
0/1.

There are $2^n$ subsets. At $n = 100$ that is $10^{30}$, so enumeration is out.

### The state, and why it needs two dimensions

The instinct is to index by item only — "the best value using the first $i$ items". That fails
immediately: whether item $i$ fits depends on **how much capacity is left**, and capacity depends on
what was taken earlier. The subproblem is not determined by $i$ alone.

So the state is two-dimensional. Let $K[i][w]$ be the best value using the first $i$ items with
capacity $w$:

$$K[i][w] = \begin{cases}
0 & i = 0\\
K[i-1][w] & w_i > w \quad\text{(too heavy — skip it)}\\
\max\big(\underbrace{K[i-1][w]}_{\text{skip}},\ \underbrace{K[i-1][w - w_i] + v_i}_{\text{take}}\big) & \text{otherwise}
\end{cases}$$

```python
def knapsack(W, items):
    n = len(items)
    K = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wi, vi = items[i-1]
        for w in range(W + 1):
            K[i][w] = K[i-1][w]
            if wi <= w and K[i-1][w-wi] + vi > K[i][w]:
                K[i][w] = K[i-1][w-wi] + vi
    return K[n][W]
```

**$\Theta(nW)$** time and space. *(Verified against brute-force enumeration of all $2^n$ subsets on 300
random instances. **0 mismatches.**)*

---

## 2. $\Theta(nW)$ Is Not Polynomial

This is the most important sentence in the lecture and it is routinely misread.

$\Theta(nW)$ **looks** polynomial. It is polynomial in $n$ and in $W$ — but the *input size* is not
$W$. The input contains $W$ written down, which takes $\log_2 W$ bits. So in terms of the input size,
the running time is $\Theta(n \cdot 2^{\text{bits}})$ — **exponential.**

Measured, $n = 30$ items:

| $W$ | bits to write $W$ | table cells | time |
| --- | --- | --- | --- |
| 100 | 7 | 3,000 | 0.4 ms |
| 1,000 | 10 | 30,000 | 7.8 ms |
| 10,000 | 14 | 300,000 | 71.0 ms |
| 100,000 | 17 | 3,000,000 | **741.9 ms** |

**Add one bit to $W$ and the running time doubles.** The input grew by a single character; the work
doubled. That is the signature of exponential dependence on input size, and it is why an algorithm
like this is called **pseudo-polynomial**.

The consequence matters: **0/1 knapsack is NP-complete** (Week 12), and this algorithm does not
contradict that. It is efficient when $W$ is small and useless when $W$ is a 64-bit number, which is
exactly the behaviour NP-completeness predicts.

> **The general lesson:** when a bound mentions a *numeric value* from the input rather than a *count*
> of things, check whether that value is polynomial in the input size. Very often it is not.

---

## 3. Rolling the Table, and a One-Character Bug

Each row depends only on the row above, so one array suffices:

```python
def knapsack_1d(W, items):
    dp = [0] * (W + 1)
    for wi, vi in items:
        for w in range(W, wi - 1, -1):        # DESCENDING
            if dp[w - wi] + vi > dp[w]: dp[w] = dp[w - wi] + vi
    return dp[W]
```

$\Theta(W)$ space. *(Verified to match the 2-D table on 300 of 300 instances.)*

**The inner loop must run downwards.** Going upwards, `dp[w - wi]` has already been updated *in this
row*, so item $i$ can be taken again — and again:

```python
for wi, vi in items:
    for w in range(wi, W + 1):            # ASCENDING: a different problem entirely
        if dp[w - wi] + vi > dp[w]: dp[w] = dp[w - wi] + vi
```

*(Verified: the ascending version differs from 0/1 knapsack on **258 of 300** random instances.)*

It is not broken code. **It correctly solves the *unbounded* knapsack**, where each item may be taken
any number of times. One character — the direction of a range — separates two different problems, and
both versions run without error and return plausible numbers.

This is the most instructive bug in the course so far, because there is no way to catch it except by
knowing what the loop order *means*: descending says "the row above", ascending says "this row".

---

## 4. Choosing the State

This is the part students find hard, and it is genuinely the creative step. The recurrence is usually
easy once the state is right, and impossible when it is wrong.

> **The state must contain exactly the information needed to make the remaining decisions, and nothing
> more.**

Both failure directions are real:

- **Too little** and the recurrence is not well defined — you cannot tell whether an item fits. That
  is why knapsack needs capacity as well as item index.
- **Too much** and the table explodes. Adding "which items were taken" to the knapsack state makes it
  $2^n$ and you have re-derived brute force with extra steps.

### A checklist that works

1. **What decisions are made, in what order?** Usually one per input element.
2. **Standing at decision $k$, what must I know to decide?** *That is the state.*
3. **What do I not need to know?** Everything else is discarded — and discarding it is what makes the
   table small.
4. **Count the states.** That, times the work per state, is the running time. If the count is
   exponential, go back to 2.

Applied to knapsack: decisions are "take item $i$ or not", in index order (1). To decide, I need to
know which item I am at and how much capacity remains (2). I do **not** need to know *which* earlier
items were taken — only their total weight, which is already captured by the remaining capacity (3).
States: $n \times W$ (4).

**Step 3 is where the algorithm is born.** Realising that the *identity* of the chosen items is
irrelevant, and only their total weight matters, is what collapses $2^n$ into $nW$.

### The same question for the week's other problems

| problem | state | why that is enough |
| --- | --- | --- |
| Fibonacci | $n$ | the value depends only on the index |
| LCS / edit distance | $(i, j)$ prefix lengths | the past is summarised by how much of each string is consumed |
| knapsack | $(i, w)$ | earlier choices matter only through the weight they used |
| shortest paths (Week 5) | $(v, \text{edge count})$ | how you reached $v$ is irrelevant — only that you are at $v$ |

**The pattern is the same every time**: find what the past can be *summarised by*, and throw away the
rest. That summary is the state.

---

## 5. Recovering the Solution

The table gives the optimal *value*. For the actual items, walk back:

```python
def which_items(K, W, items):
    chosen, w = [], W
    for i in range(len(items), 0, -1):
        if K[i][w] != K[i-1][w]:              # value changed, so item i was taken
            chosen.append(i - 1)
            w -= items[i-1][0]
    return chosen[::-1]
```

$\Theta(n)$, and it needs the **full table** — the rolled 1-D version cannot do this. That is the same
trade as LCS in Lecture 23 §5, and it recurs: **you can have linear space or an easy traceback, and
getting both requires Hirschberg-style cleverness.**

---

## 6. Variants Worth Recognising

| variant | change | state |
| --- | --- | --- |
| **unbounded** knapsack | unlimited copies | same, but the inner loop ascends (§3) |
| **bounded** knapsack | at most $c_i$ copies | binary-split each item into powers of two |
| **subset sum** | values equal weights; hit $W$ exactly | booleans instead of values |
| **partition** | split into two equal halves | subset sum with $W = \frac12\sum w_i$ |
| **coin change** | fewest coins summing to $W$ | unbounded knapsack, minimising |

All five are the same table. **Recognising that a new problem is knapsack in disguise is worth more
than remembering the recurrence**, and Week 8 spends its time on exactly that skill.

---

## 7. Where Week 7 Leaves You

You have the technique and three worked examples. What you do **not** yet have is fluency in step 1 of
§4, and no amount of reading supplies it — it comes from doing problems, which is what PS 7 and
Week 8 are for.

Two forward pointers:

- **Week 8** is nothing but state design: matrix chain multiplication, optimal BSTs, longest
  increasing subsequence, DP on trees and bitmasks, and Floyd–Warshall — which is DP over "which
  vertices may be used as intermediates", a state nobody guesses first time.
- **Week 9** does the opposite. Greedy algorithms make one choice and never reconsider, which is
  faster than DP when it works — and Week 9 is about proving when it does.

**PROJECT 1 is assigned this week and due Friday of Week 9.** It builds a working `diff` from
Lecture 23, and its stretch component is Hirschberg's algorithm. Ten percent of the course; read the
brief now.

---

## 8. What to Do

- Read CLRS §14.1–14.3 again, then §14.4. Knapsack is Problem 14-2 and §15.2 covers the fractional
  variant, which is Week 9's material because it is **greedy**.
- **PS 7** implements knapsack, both loop directions, the traceback, and the pseudo-polynomial
  measurement.
- **Quiz 7 covers Week 6.**

---

*CS 102 · Week 7 · Lecture 24 · © CSE Department*

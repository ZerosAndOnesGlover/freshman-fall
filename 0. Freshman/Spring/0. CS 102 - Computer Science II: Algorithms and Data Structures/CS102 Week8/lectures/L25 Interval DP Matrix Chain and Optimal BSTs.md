# CS 102 · Computer Science II
## Lecture 25: Interval DP — Matrix Chain Multiplication and Optimal BSTs

**Date:** Monday 8 March 2027 · 09:00–09:50 · Week 8

---

## 1. A New Shape of State

Week 7's states were **prefixes**: "the first $i$ characters", "the first $i$ items". Every subproblem
was an initial segment, and the recurrence looked one step back.

This week's first family is different. The state is an **interval** $[i, j]$ — a contiguous stretch of
the input — and the recurrence splits it at every possible point:

$$\mathrm{best}[i][j] = \min_{i \le k < j}\Big(\mathrm{best}[i][k] + \mathrm{best}[k{+}1][j] + \mathrm{cost}(i,k,j)\Big)$$

Three consequences follow immediately, and they characterise the whole family:

- there are $\Theta(n^2)$ intervals, so $\Theta(n^2)$ states;
- each takes $\Theta(n)$ work, because $k$ ranges over the interval;
- so these problems are **$\Theta(n^3)$**, not $\Theta(n^2)$.

And the evaluation order changes. Prefix DP fills left to right. **Interval DP must fill by increasing
interval length**, because $[i,j]$ depends on strictly shorter intervals inside it.

```python
for length in range(2, n + 1):          # NOT for i, for j
    for i in range(1, n - length + 2):
        j = i + length - 1
        ...
```

Getting that loop structure wrong is the characteristic bug of this lecture, and it fails silently:
you read cells that have not been filled yet, which contain zeros, which look like plausible answers.

---

## 2. Matrix Chain Multiplication

**Problem.** Multiply $A_1 A_2 \cdots A_n$, where $A_i$ is $p_{i-1} \times p_i$. Matrix multiplication
is associative, so the *result* does not depend on the parenthesisation — but the **cost** does.

Multiplying a $p \times q$ by a $q \times r$ matrix costs $pqr$ scalar multiplications.

### Why it matters

Take $p = [30, 35, 15, 5, 10, 20, 25]$ — six matrices.

| parenthesisation | scalar multiplications |
| --- | --- |
| left to right, $(((((A_1A_2)A_3)A_4)A_5)A_6)$ | **40,500** |
| optimal, $((A_1(A_2A_3))((A_4A_5)A_6))$ | **15,125** |

*(Verified.)* **The naive order costs 2.68× the optimal**, and the gap grows with the chain.

### Why you cannot enumerate

The number of ways to parenthesise $n$ matrices is the Catalan number $C_{n-1}$:

| $n$ | parenthesisations | DP subproblems |
| --- | --- | --- |
| 4 | 5 | 8 |
| 8 | 429 | 32 |
| 12 | 58,786 | 72 |
| 16 | 9,694,845 | 128 |
| 20 | **1,767,263,190** | **200** |

*(Catalan numbers verified against $\binom{2n}{n}/(n+1)$.)*

**Twenty matrices: 1.8 billion orderings, 200 subproblems.** That table is the clearest statement of
what DP buys that this course has produced.

### The recurrence

Let $m[i][j]$ be the minimum cost of multiplying $A_i \cdots A_j$.

$$m[i][j] = \begin{cases}
0 & i = j\\
\displaystyle\min_{i \le k < j}\big(m[i][k] + m[k{+}1][j] + p_{i-1}p_k p_j\big) & i < j
\end{cases}$$

The term $p_{i-1}p_kp_j$ is the cost of the **final** multiplication: an $p_{i-1}\times p_k$ result
times a $p_k \times p_j$ result. **The state design step is realising that the last multiplication is
what to split on** — every parenthesisation has exactly one outermost product, and $k$ enumerates
where it is.

```python
def mcm(p):
    n = len(p) - 1
    m = [[0]*(n+1) for _ in range(n+1)]
    s = [[0]*(n+1) for _ in range(n+1)]        # split points, for reconstruction
    for L in range(2, n+1):                     # by INCREASING interval length
        for i in range(1, n-L+2):
            j = i + L - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                c = m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j]
                if c < m[i][j]: m[i][j] = c; s[i][j] = k
    return m[1][n], s
```

$\Theta(n^3)$ time, $\Theta(n^2)$ space. *(Verified against exhaustive recursion on 300 random chains.
**0 mismatches.**)*

The `s` table reconstructs the parenthesisation, exactly as `parent` did for shortest paths:

```python
def parens(s, i, j):
    if i == j: return f"A{i}"
    return f"({parens(s, i, s[i][j])}{parens(s, s[i][j]+1, j)})"
```

---

## 3. Optimal Binary Search Trees

**Problem.** Given keys $k_1 < k_2 < \dots < k_n$ and the probability $p_i$ of searching for each,
build the BST minimising the **expected number of comparisons**.

This is the first time this course has asked for a tree shaped around a *known access distribution*,
and it is the answer to a question Week 2 raised and deferred.

### Balance is the wrong objective

Week 2 spent three lectures making trees balanced. Here, balance is **not** what you want.

Take four keys with $p = [0.7, 0.1, 0.1, 0.1]$:

| tree | expected comparisons |
| --- | --- |
| perfectly balanced | **2.000** |
| optimal | **1.500** |

*(Verified.)* **The balanced tree is 33% worse.** Putting the 70%-probability key at the root costs one
comparison 70% of the time; burying it at depth 2 to keep the shape tidy is a bad trade.

> **Week 2 minimised the worst case with no knowledge of the queries. This minimises the average with
> full knowledge of them.** Different information, different objective, different answer — and neither
> algorithm is wrong.

### The recurrence

Let $C[i][j]$ be the expected cost of an optimal BST on keys $i \dots j$. If $r$ is the root, the left
and right subtrees are optimal on $[i, r-1]$ and $[r+1, j]$ — and **every key in the interval gains one
comparison**, because it now sits one level deeper:

$$C[i][j] = \min_{i \le r \le j}\Big(C[i][r-1] + C[r+1][j]\Big) + \sum_{t=i}^{j} p_t$$

*(Verified against exhaustive enumeration of all BST shapes on 200 random distributions. **0
mismatches.**)*

**That trailing sum is the whole trick.** It looks like a constant added at the end, and it is the term
that accounts for the depth increase of the entire subtree — you do not need to know the depths,
because every choice of root deepens everything by exactly one. Missing it is the standard error, and
it produces an answer that is too small and monotonically wrong.

Precompute prefix sums so $\sum_{t=i}^{j} p_t$ is $O(1)$; otherwise the algorithm is $\Theta(n^4)$.

### Where this is used

Compiler symbol tables, static dictionaries, and decision trees — anywhere the key set is fixed, the
access frequencies are measurable, and the structure is built once and queried many times.

**Knuth's optimisation** reduces this to $\Theta(n^2)$ by proving that the optimal root of $[i,j]$ lies
between the optimal roots of $[i,j-1]$ and $[i+1,j]$, which shrinks the range of $r$. The same trick
applies to a broad class of interval DPs, and it is the natural next thing to read.

---

## 4. Recognising Interval DP

The family shares a signature. You are probably looking at interval DP when:

- the input is a **sequence** and the answer concerns **contiguous stretches** of it;
- an optimal solution is determined by **one split point** or **one distinguished element**;
- combining two sub-answers costs something that depends on the interval's **endpoints**.

| problem | split on | cost of combining |
| --- | --- | --- |
| matrix chain | the last multiplication | $p_{i-1}p_kp_j$ |
| optimal BST | the root | $\sum_{t=i}^{j} p_t$ |
| longest palindromic subsequence | the two ends | 0 or 2 |
| burst balloons | the **last** balloon burst | $v_{i-1}v_kv_{j+1}$ |
| polygon triangulation | the triangle on edge $(i,j)$ | the triangle's weight |

**Burst balloons is worth a moment**, because it shows what "choose the state" means. The natural
reading is "which balloon do I burst *first*", and that state does not work — bursting a balloon
changes its neighbours, so the subproblems are not independent intervals. Splitting on the **last**
balloon burst in the interval makes the two sides independent, and the problem becomes routine.

> **When an interval DP will not decompose, try reversing the decision.** "First" and "last" are not
> symmetric, and one of them very often leaves independent subproblems where the other does not.

---

## 5. What to Do

- Read CLRS §14.2 (matrix chain) properly this week — you skimmed it in Week 7 — and §15.5 (optimal
  BSTs).
- **PS 8** implements both, reconstructs the parenthesisation, and measures the naive-versus-optimal
  gap.
- **Quiz 8 covers Week 7** — memoisation, LCS, knapsack. Not this material.
- **PROJECT 1 is due Friday of Week 9.** If Part 1 is not finished, this week is the week.
- Next lecture: sequences, trees, and bitmasks — three more state designs, one of which turns a
  factorial into an exponential.

---

*CS 102 · Week 8 · Lecture 25 · © CSE Department*

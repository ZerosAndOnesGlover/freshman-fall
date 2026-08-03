# CS 102 · Computer Science II
## Lecture 22: Optimal Substructure, Overlapping Subproblems, and Memoisation

---

## 1. You Have Already Written One

Dynamic programming has a reputation for being hard. It should not, because you wrote a dynamic
program two weeks ago and nobody called it that.

Bellman–Ford. Let $D_i[v]$ be the shortest distance to $v$ using at most $i$ edges. Then

$$D_i[v] = \min\Big(D_{i-1}[v],\ \min_{(u,v)\in E}\big(D_{i-1}[u] + w(u,v)\big)\Big)$$

**That is a dynamic program**: subproblems indexed by edge count, each defined in terms of smaller
ones, evaluated bottom-up with the rows overwritten in place. The algorithm needed no ordering
argument and no greedy insight — it worked by solving every subproblem once and reusing the answers.

This week names the technique and makes it deliberate. The definition is unglamorous:

> **Dynamic programming is recursion in which you do not recompute anything.**

Everything else — tables, orderings, state design — is bookkeeping in service of that sentence.

---

## 2. The Two Conditions

A problem yields to DP when it has both of the following. **Both are required**, and knowing which one
a problem lacks tells you what to do instead.

### Optimal substructure

An optimal solution is built from optimal solutions to subproblems.

You met this in Week 5: **any subpath of a shortest path is a shortest path**. It is what let us
compute shortest paths without enumerating paths.

**When it fails, DP does not apply.** *Longest simple path* has no optimal substructure: the longest
simple path from $a$ to $c$ through $b$ need not use the longest simple $a\rightsquigarrow b$ path,
because that path might consume vertices needed later. Week 12 explains that this failure is not an
accident of presentation — the problem is NP-complete.

### Overlapping subproblems

The naive recursion solves the *same* subproblem many times.

**When this fails, DP buys nothing.** Merge sort has beautiful optimal substructure and its two
subproblems never overlap, so memoising it is pure overhead. That is divide-and-conquer, and the
distinction is exactly this condition.

| | optimal substructure | overlapping subproblems | technique |
| --- | --- | --- | --- |
| merge sort | yes | **no** | divide and conquer |
| Fibonacci | yes | yes | **DP** |
| shortest paths | yes | yes | **DP** |
| longest simple path | **no** | yes | (NP-complete — Week 12) |

---

## 3. Fibonacci, and How Bad Recomputation Gets

```python
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)
```

Correct, and unusable. Count the calls:

| $n$ | calls |
| --- | --- |
| 5 | 15 |
| 10 | 177 |
| 15 | 1,973 |
| 20 | 21,891 |
| 25 | 242,785 |

The pattern is exact:

$$\boxed{\text{calls}(n) = 2F(n+1) - 1}$$

*(Verified for $n = 0 \dots 25$ — exact at every value.)*

Since $F(k) \approx \varphi^k/\sqrt5$, the call count is $\approx 1.447\,\varphi^{\,n}$ — verified: the
ratio calls$/\varphi^n$ is **1.439, 1.447, 1.447, 1.447** at $n = 10, 20, 30, 40$. **Exponential**, with
$\varphi \approx 1.618$.

### Where the work goes

Computing `fib(20)`, how many times is each smaller value evaluated?

| subproblem | times evaluated |
| --- | --- |
| `fib(18)` | 2 |
| `fib(15)` | 8 |
| `fib(10)` | 89 |
| `fib(5)` | 987 |
| `fib(2)` | 4,181 |
| **`fib(1)`** | **6,765** |

There are **21 distinct subproblems** and **21,891 calls**.

Look closely at those counts: 2, 8, 89, 987, 4181, 6765 are all Fibonacci numbers. The identity is

$$\text{“fib}(k)\text{ is evaluated } F(n-k+1) \text{ times''}$$

*(Verified for all $2 \le n \le 23$ and $1 \le k \le n$ — exact.)*

**The redundancy of naive Fibonacci is itself Fibonacci.** That is a pleasing fact and also the
clearest possible statement of the problem: the deeper a subproblem sits, the more times it is
recomputed, and the growth is the very quantity you are trying to compute.

---

## 4. Two Fixes

### Memoisation — top-down

Keep the recursion; cache the answers.

```python
def fib(n, memo={}):
    if n in memo: return memo[n]
    if n < 2: return n
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]
```

Each subproblem is computed once and looked up thereafter: $\Theta(n)$ time, $\Theta(n)$ space.

Python gives you this for free:

```python
@functools.lru_cache(maxsize=None)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)
```

*(Verified: a single call to `fib(100)` reports **98 hits and 101 misses** — 101 misses is exactly one
per distinct subproblem $0 \dots 100$, and every other consultation is a hit. That is memoisation
working, stated as a ratio.)*

> **A warning about `memo={}` as a default argument.** The dictionary is created **once**, when the
> function is defined, and shared by every call. Here that is exactly what you want. In general it is
> the classic Python mutable-default bug, and you should know you are exploiting it deliberately
> rather than by accident.

### Tabulation — bottom-up

Drop the recursion; fill a table in dependency order.

```python
def fib(n):
    if n < 2: return n
    a, b = 0, 1
    for _ in range(n - 1): a, b = b, a + b
    return b
```

$\Theta(n)$ time and — because each value needs only the previous two — **$\Theta(1)$ space.**

### Measured

| $n$ | naive | memoised | tabulated |
| --- | --- | --- | --- |
| 20 | 2.00 ms | 0.0045 ms | 0.00097 ms |
| 25 | 23.59 ms | 0.0063 ms | 0.00101 ms |
| 30 | 253.88 ms | 0.0068 ms | 0.00114 ms |
| 32 | **685.63 ms** | **0.0072 ms** | **0.00120 ms** |

At $n = 32$ that is **95,000×**. At $n = 40$ the naive version would take about **32 seconds**, and the
other two would still be under a millisecond.

Note also the last two columns: **tabulation is about 6× faster than memoisation** even though both
are $\Theta(n)$. Dictionary lookups and function calls are not free.

---

## 5. Choosing Between Them

The usual advice is that this is a matter of taste. It is not — it is a question about the shape of
the subproblem graph, and the difference can be three orders of magnitude.

**Memoisation computes only the subproblems reachable from the top. Tabulation fills every cell.**

Measured on 0/1 knapsack — the same instances, both methods, counting cells actually computed:

| $n$ | $W$ | top-down cells | bottom-up cells | ratio |
| --- | --- | --- | --- | --- |
| 20 | 1,000 | 5,839 | 20,020 | 3.4× |
| 20 | 10,000 | 5,839 | 200,020 | 34.3× |
| 10 | 100,000 | **636** | **1,000,010** | **1,572×** |

And when the item weights share a common factor, so that most capacities are unreachable:

| $n$ | $W$ | weights | top-down | bottom-up | ratio |
| --- | --- | --- | --- | --- | --- |
| 20 | 10,000 | multiples of 100 | 986 | 200,020 | 203× |
| 20 | 10,000 | multiples of 1000 | 161 | 200,020 | 1,242× |
| 20 | 100,000 | multiples of 1000 | 986 | 2,000,020 | **2,028×** |

*(All answers identical; only the work differs.)*

But this is **not** a general argument for memoisation. On LCS the picture reverses:

| $\lvert a\rvert$ | $\lvert b\rvert$ | top-down | bottom-up | ratio |
| --- | --- | --- | --- | --- |
| 50 | 50 | 1,829 | 2,500 | 1.37× |
| 100 | 100 | 7,432 | 10,000 | 1.35× |
| 200 | 200 | 28,739 | 40,000 | 1.39× |

**Within 40%** — and tabulation's cells are cheaper, so it wins on wall clock.

| | memoisation | tabulation |
| --- | --- | --- |
| direction | top-down | bottom-up |
| computes | only reachable subproblems | all of them |
| order | figures itself out | you must supply it |
| recursion limit | **yes** — a real constraint | no |
| space optimisation | hard | **easy** — roll the rows |
| constant factor | dict + call overhead | array indexing |

> **The decision rule.** If a large fraction of the state space is unreachable — sparse states, big
> capacities, clustered weights — **memoise**. If nearly all of it is needed, or you want the
> $\Theta(1)$-space rolling trick, **tabulate**. Deciding by preference rather than by looking at your
> subproblem graph is how you end up 2,000× slower than necessary.

### The recursion limit is not a footnote

*(Verified: `fib_memo(5000)` raises `RecursionError`; the tabulated version returns a 1,045-digit
number without difficulty.)*

Memoisation recurses to the depth of the subproblem chain. Python's default limit is 1,000, and
raising it trades an exception for a segmentation fault — the same argument as Week 4 Lecture 15 §1.
**For deep subproblem chains, tabulation is not a preference; it is the only option that works.**

---

## 6. The Recurrence Is the Program

The step that matters is not writing code. It is writing this:

$$F(n) = F(n-1) + F(n-2), \qquad F(0) = 0,\ F(1) = 1$$

A correct recurrence with correct base cases **is** the algorithm; memoisation and tabulation are two
mechanical translations of it, and either can be produced without further thought.

So the design questions are always these four, in order:

1. **What is a subproblem?** Name the state. This is the creative step and Lecture 24 is about it.
2. **What is the recurrence?** How does a subproblem decompose into smaller ones?
3. **What are the base cases?** Usually where a dimension hits zero, and usually where the bugs are.
4. **In what order must they be evaluated?** Only needed for tabulation; memoisation discovers it.

Then two questions about cost:

5. **How many subproblems are there?** That times the work per subproblem is the running time.
6. **How much of the table is live at once?** That is the space, and it is often far less than the
   whole table.

**Steps 1–3 are the algorithm. Steps 4–6 are engineering.** Students who struggle with DP are almost
always stuck on step 1 while trying to write code, and Lecture 24 addresses that directly.

---

## 7. What to Do

- Read CLRS §14.1–14.3 — rod cutting, the elements of DP, and the memoisation/tabulation comparison.
- **PS 7** implements LCS, edit distance, and knapsack, and reproduces §5's cell counts.
- **Lab 7** makes the tables visible and traces the dependency structure.
- **PROJECT 1 is assigned this week** and due Friday of Week 9 — a working `diff`. It is 10% of the
  course. Read the brief now, even if you start later.
- **Quiz 7 covers Week 6** — MSTs, the cut property, union-find. Not this material.

---

*CS 102 · Week 7 · Lecture 22 · © CSE Department*

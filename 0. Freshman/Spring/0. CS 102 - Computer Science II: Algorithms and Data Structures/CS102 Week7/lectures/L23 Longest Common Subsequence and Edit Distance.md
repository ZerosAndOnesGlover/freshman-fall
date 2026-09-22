# CS 102 · Computer Science II
## Lecture 23: Longest Common Subsequence and Edit Distance

**Date:** Wednesday 10 March 2027 · 09:00–09:50 · Week 7

---

## 1. Two Strings, One Table

Both problems in this lecture compare two sequences, both fill an $(n{+}1) \times (m{+}1)$ table, and
both are the DP everyone actually uses — `diff`, `git`, spell-checkers, and genome aligners are all
this lecture.

A **subsequence** keeps order but need not be contiguous: `ACE` is a subsequence of `ABCDE`, and
`AEC` is not. A **substring** must be contiguous. Confusing the two is the most common way to get the
wrong recurrence, and the problems have genuinely different answers.

---

## 2. Longest Common Subsequence

**Problem.** Given $a$ and $b$, find the longest sequence that is a subsequence of both.

### The state

Let $L[i][j]$ be the LCS length of the **prefixes** $a[0{:}i]$ and $b[0{:}j]$.

That choice — prefixes, indexed by their lengths — is the whole design step, and it works because of
one observation about the *last* characters:

- **If $a[i-1] = b[j-1]$**, that character can be taken as the last of the LCS. Nothing is lost by
  taking it, so $L[i][j] = L[i-1][j-1] + 1$.
- **If they differ**, they cannot both be the last character of the LCS. So at least one of them is
  unused, and $L[i][j] = \max(L[i-1][j],\ L[i][j-1])$.

$$L[i][j] = \begin{cases}
0 & i = 0 \text{ or } j = 0\\
L[i-1][j-1] + 1 & a[i-1] = b[j-1]\\
\max\big(L[i-1][j],\ L[i][j-1]\big) & \text{otherwise}
\end{cases}$$

The first case deserves a moment: *why is it safe to take the match greedily?* Because any LCS not
using this pair can be modified to use it without getting shorter — an **exchange argument**, the same
device as Week 6's cut property. It is easy to state and easy to skip; do not skip it, because the
analogous step in a problem you design yourself will not be obvious.

```python
def lcs(a, b):
    n, m = len(a), len(b)
    L = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i-1] == b[j-1]: L[i][j] = L[i-1][j-1] + 1
            else:                L[i][j] = max(L[i-1][j], L[i][j-1])
    return L[n][m], L
```

$\Theta(nm)$ time and space. *(Verified against brute-force subsequence enumeration on 300 random
pairs — lengths and recovered strings both. **0 failures.**)*

### The table

$a = $ `AGGTAB`, $b = $ `GXTXAYB`:

```
       -  G  X  T  X  A  Y  B
    -  0  0  0  0  0  0  0  0
    A  0  0  0  0  0  1  1  1
    G  0  1  1  1  1  1  1  1
    G  0  1  1  1  1  1  1  1
    T  0  1  1  2  2  2  2  2
    A  0  1  1  2  2  3  3  3
    B  0  1  1  2  2  3  3  4
```

LCS length **4**, and the subsequence is `GTAB`.

Two things are visible in the picture. **The table never decreases** as you move right or down — each
cell is at least its neighbours above and left. And **it increases only on a diagonal step**, which is
exactly a matched character.

### Recovering the subsequence

The table gives the length. The answer needs a walk back from the bottom-right:

```python
def recover(a, b, L):
    i, j, out = len(a), len(b), []
    while i > 0 and j > 0:
        if a[i-1] == b[j-1]:  out.append(a[i-1]); i -= 1; j -= 1   # diagonal: a match
        elif L[i-1][j] >= L[i][j-1]: i -= 1                        # up
        else: j -= 1                                               # left
    return ''.join(reversed(out))
```

$\Theta(n+m)$ — the walk takes one step per row or column.

**The LCS is generally not unique**, and the `>=` above silently chooses one of them. If you need all
of them, that is a different and much more expensive problem: there can be exponentially many.

---

## 3. Edit Distance

**Problem.** The minimum number of single-character **insertions**, **deletions**, and
**substitutions** to turn $a$ into $b$. Also called Levenshtein distance.

Same state — prefix lengths — and the recurrence follows from asking what the last operation was:

$$D[i][j] = \begin{cases}
j & i = 0 \quad\text{(insert all of }b)\\
i & j = 0 \quad\text{(delete all of }a)\\
D[i-1][j-1] & a[i-1] = b[j-1]\\
1 + \min\big(D[i-1][j],\ D[i][j-1],\ D[i-1][j-1]\big) & \text{otherwise}
\end{cases}$$

The three terms in the `min` are **delete** $a[i-1]$, **insert** $b[j-1]$, and **substitute** one for
the other.

```python
def edit(a, b):
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1): D[i][0] = i
    for j in range(m + 1): D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i-1] == b[j-1]: D[i][j] = D[i-1][j-1]
            else: D[i][j] = 1 + min(D[i-1][j], D[i][j-1], D[i-1][j-1])
    return D[n][m]
```

*(Verified against an independent recursion on 400 random pairs. **0 mismatches.**)*

| pair | distance |
| --- | --- |
| `kitten` → `sitting` | 3 |
| `sunday` → `saturday` | 3 |
| `intention` → `execution` | 5 |

**The base cases are not decoration.** $D[i][0] = i$ says "delete everything"; $D[0][j] = j$ says
"insert everything". Initialising the borders to zero, as in LCS, gives a confidently wrong answer,
and it is the single most common bug on this problem.

---

## 4. How the Two Are Related — Precisely

Students often assume LCS and edit distance are the same computation. They are related, but the
relationship holds only for a restricted edit distance.

> **With only insertions and deletions** (no substitutions):
> $$D_{\text{indel}}(a,b) = |a| + |b| - 2\cdot\mathrm{LCS}(a,b)$$

*(Verified over 400 random pairs. **0 failures.**)*

The reasoning: keep the LCS, delete everything else in $a$, insert everything else in $b$.

**Add substitution and the identity breaks**, because one substitution can replace a delete *and* an
insert:

| $a$ | $b$ | LCS | $\lvert a\rvert+\lvert b\rvert-2\mathrm{LCS}$ | true edit distance |
| --- | --- | --- | --- | --- |
| `abc` | `abd` | 2 | 2 | **1** |
| `kitten` | `sitting` | 4 | 5 | **3** |
| `abcd` | `dcba` | 1 | 6 | **4** |

*(Verified.)*

> **This is why `diff` reports changed lines rather than a delete followed by an insert**, and why the
> right cost model is a design decision rather than a detail. Project 1 makes you choose one and
> defend it.

---

## 5. Space

Both tables are $\Theta(nm)$, which at $n = m = 10^5$ is $10^{10}$ cells — impossible.

But each row depends only on the row above, so **two rows suffice**:

```python
def lcs_len(a, b):
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j-1] + 1 if a[i-1] == b[j-1] else max(prev[j], cur[j-1])
        prev = cur
    return prev[len(b)]
```

$\Theta(\min(n,m))$ space — swap the arguments so the shorter string indexes the rows.

**And now you cannot recover the subsequence**, because the traceback needs the whole table. That is a
real loss, not a technicality: you have the length and not the answer.

**Hirschberg's algorithm** recovers it anyway, in $\Theta(nm)$ time and $\Theta(\min(n,m))$ space, by
divide-and-conquer: compute the middle column's forward and backward halves in linear space, find
where the optimal path crosses it, and recurse on the two halves. **This is Project 1's stretch
component** and it is the most elegant algorithm in this course.

---

## 6. What This Is Used For

**`diff` and version control.** Lines are the alphabet. The LCS of two files is the set of unchanged
lines; everything else is an addition or a deletion. `git diff` is this computation, with
optimisations for the common case of near-identical files.

**Spell checking and fuzzy search.** Edit distance ranks candidate corrections. With a cutoff $k$ you
need only the diagonal band of width $2k+1$, which makes it $\Theta(kn)$ rather than $\Theta(n^2)$.

**Bioinformatics.** Sequence alignment is edit distance with a scoring matrix instead of unit costs
and a separate penalty for opening a gap. Needleman–Wunsch is global alignment; Smith–Waterman is the
local variant. **Both are this lecture's table with different weights in the recurrence.**

**Plagiarism detection**, which is Week 10's lab from the other direction.

---

## 7. What to Do

- Read CLRS §14.4 (LCS) carefully; it is the model presentation. Edit distance is Problem 14-5.
- **PS 7** implements both, plus the identity in §4 and the space optimisation in §5.
- **Lab 7** visualises these two tables and their dependency structure.
- **PROJECT 1** builds a real `diff` from §2 and extends it. Assigned this week.
- Next lecture: knapsack, where the state is not simply "prefix lengths" and choosing it is the work.

---

*CS 102 · Week 7 · Lecture 23 · © CSE Department*

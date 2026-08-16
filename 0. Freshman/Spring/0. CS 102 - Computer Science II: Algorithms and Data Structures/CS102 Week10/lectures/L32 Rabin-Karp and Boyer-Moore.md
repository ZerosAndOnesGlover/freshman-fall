# CS 102 · Computer Science II
## Lecture 32: Rabin–Karp and Boyer–Moore

**Date:** Wednesday 24 March 2027 · 09:00–09:50 · Week 10

---

## 1. Two Different Ideas

KMP avoids re-reading the text. This lecture has two algorithms that attack the problem from other
directions:

- **Rabin–Karp** compares *hashes* instead of characters, so a window costs $O(1)$ to test.
- **Boyer–Moore** compares from the *right*, which lets it skip characters entirely — and it is the
  only algorithm here that can run in **less than $n$** time.

---

## 2. Rabin–Karp

Treat a window of $m$ characters as a number in base $b$, modulo a prime $q$:

$$H(t[i..i{+}m{-}1]) = \Big(\sum_{j=0}^{m-1} t[i+j]\, b^{\,m-1-j}\Big) \bmod q$$

The point is that consecutive windows share $m-1$ characters, so the hash **rolls** in $O(1)$: remove
the leading character's contribution, shift, add the new one.

```python
def rabin_karp(t, p, base=256, mod=(1 << 61) - 1):
    n, m = len(t), len(p)
    if m == 0 or m > n: return list(range(n+1)) if m == 0 else []
    h = pow(base, m-1, mod)
    ph = th = 0
    for i in range(m):
        ph = (ph * base + ord(p[i])) % mod
        th = (th * base + ord(t[i])) % mod
    out = []
    for i in range(n - m + 1):
        if ph == th and t[i:i+m] == p:               # verify: hashes can collide
            out.append(i)
        if i < n - m:
            th = ((th - ord(t[i]) * h) * base + ord(t[i+m])) % mod
    return out
```

*(Verified against the naive algorithm on 3,000 random pairs. **0 mismatches.**)*

### The verification step is not optional

`ph == th` does **not** mean the strings are equal. A hash collision gives a **spurious hit**, and the
`t[i:i+m] == p` check is what makes the algorithm correct rather than probabilistic.

**How often that check runs decides the running time**, and it depends entirely on the modulus:

| modulus | spurious hits over 19,995 windows |
| --- | --- |
| $2^{61} - 1$ | **0** |
| 101 | **214** |

*(Verified on 20,000 characters over an 8-letter alphabet.)*

With a good modulus the algorithm is $O(n + m)$ expected. With a small one, every spurious hit costs an
$O(m)$ verification — and in the worst case the algorithm degrades to $\Theta(nm)$, which is the naive
algorithm with extra arithmetic.

> **Rabin–Karp is the first algorithm in this course whose complexity depends on a *parameter you
> choose*.** Not on the input, not on the machine — on whether you picked a good prime. That is worth
> noticing.

### Where it is actually used

Rabin–Karp is rarely the best single-pattern matcher. It wins in two places:

- **Many patterns at once.** Hash all $k$ patterns of the same length into a set, then roll one hash
  across the text and check membership. Cost is $O(n + \sum m_i)$ expected — **independent of $k$**.
  This is how a naive spam filter or a virus scanner tests thousands of signatures in one pass.
- **Two-dimensional matching**, and any setting where a substring's identity must be summarised
  cheaply.

**And it is the foundation of Lab 10.** Document fingerprinting hashes every $k$-gram of a document;
rolling makes that $O(n)$ instead of $O(nk)$.

---

## 3. Boyer–Moore

Compare the pattern **right to left**. On a mismatch, use what you learned to skip ahead.

### The bad-character rule

If text character $c$ mismatches at pattern position $j$, look up the **last** occurrence of $c$ in the
pattern:

- if $c$ does not occur at all, **no alignment containing this $c$ can match** — slide past it
  entirely, up to $m$ positions;
- otherwise slide so that occurrence lines up with $c$.

```python
def boyer_moore(t, p):
    n, m = len(t), len(p)
    if m == 0: return list(range(n+1))
    last = {c: j for j, c in enumerate(p)}          # last occurrence of each character
    out = []; i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and t[i+j] == p[j]: j -= 1
        if j < 0:
            out.append(i); i += 1
        else:
            i += max(1, j - last.get(t[i+j], -1))   # max(1, ...) prevents going backwards
    return out
```

*(Verified against naive on 3,000 random pairs. **0 mismatches.**)*

The `max(1, ...)` is essential: the bad-character rule can compute a **negative** shift when the
matched character occurs later in the pattern, and without the guard the algorithm loops forever.

### Sublinear — genuinely

$n = 200{,}000$, pattern length 8:

| alphabet size | BM comparisons | naive | KMP | **BM per text character** |
| --- | --- | --- | --- | --- |
| 2 | 298,090 | 398,942 | 276,298 | **1.490** |
| 8 | 46,211 | 228,504 | 224,801 | **0.231** |
| 26 | **28,898** | 207,977 | 207,659 | **0.144** |

*(Verified.)*

**On a 26-letter alphabet, Boyer–Moore examines about one character in seven.** It is the only
algorithm here that does not read the whole text — with a long pattern and a large alphabet, most
characters are jumped over without ever being compared.

**And on a binary alphabet it is worse than KMP** — 1.490 comparisons per character against KMP's
1.38. With two symbols the bad-character rule almost never gives a big shift, and the right-to-left
scanning costs more than it saves.

> **The algorithm's advantage is a function of the alphabet, not of the algorithm.** That is the third
> time this term — after Week 4's graph structure and Week 8's density — that "which is faster" has
> turned out to depend on a property of the input nobody mentions when quoting the complexity.

### What is missing here

The full Boyer–Moore adds a **good-suffix rule**, which uses the matched suffix the way KMP uses the
failure function, and takes the larger of the two shifts. With it, the worst case is $O(n + m)$; with
only the bad-character rule the worst case is still $\Theta(nm)$ — take `aaa…a` and pattern `baaa`.

Boyer–Moore–Horspool drops the good-suffix rule deliberately, because it is simpler and faster in
practice. **Real implementations mostly do that**, and take the quadratic worst case.

---

## 4. Choosing

| algorithm | preprocessing | search | best at |
| --- | --- | --- | --- |
| naive | none | $O(nm)$ | short patterns, ordinary text — and it is what you should write first |
| **KMP** | $\Theta(m)$ | $\Theta(n+m)$ **guaranteed** | repetitive text, streams, worst-case bounds |
| **Rabin–Karp** | $\Theta(m)$ | $O(n+m)$ expected | **many patterns at once**, fingerprinting |
| **Boyer–Moore** | $\Theta(m + \sigma)$ | $O(n/m)$ best, $\Theta(nm)$ worst | long patterns, large alphabets — the practical default |
| suffix array | $O(n\log n)$ | $O(m\log n)$ per query | **many queries against one fixed text** |

The last row is the one that changes the shape of the problem, and it is Lecture 33. Everything above
it pays per search; a suffix array pays once and then answers queries cheaply — which is the right
trade for a search engine and the wrong one for `grep`.

---

## 5. What to Do

- Read CLRS §32.2 (Rabin–Karp). Boyer–Moore is not in CLRS 4th edition; Sedgewick §5.3 covers it well.
- **PS 10** implements both, measures the spurious-hit rate against the modulus, and reproduces §3's
  alphabet table.
- **Lab 10** builds a plagiarism detector on Rabin–Karp fingerprints.
- **MIDTERM 2 is this week.**
- Next lecture: suffix arrays — preprocessing the *text* instead of the pattern.

---

*CS 102 · Week 10 · Lecture 32 · © CSE Department*

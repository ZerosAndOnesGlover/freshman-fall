# CS 102 · Computer Science II
## Lecture 30: Huffman Coding

**Date:** Friday 19 March 2027 · 09:00–09:50 · Week 9

---

## 1. The Problem

Store text using as few bits as possible, with no loss.

A **fixed-length** code gives every symbol the same number of bits — ASCII uses 8. That is wasteful
when symbols are not equally common: in English, `e` and space are hundreds of times more frequent
than `z`, and spending the same eight bits on each is the obvious inefficiency.

A **variable-length** code gives frequent symbols short codes. The difficulty is decoding: given
`0101`, where does one symbol end and the next begin?

### Prefix-free codes

> A code is **prefix-free** if no codeword is a prefix of another.

Then decoding is unambiguous and needs no separators: read bits until they match a codeword, emit it,
start again. Equivalently — and this is the useful picture — **a prefix-free code is a binary tree with
the symbols at the leaves.** The path from the root spells the codeword, and no symbol is on the path
to another because leaves have no descendants.

So the problem becomes: **which binary tree minimises $\sum_s f_s \cdot \mathrm{depth}(s)$?**

---

## 2. The Algorithm

> **Repeatedly merge the two least frequent symbols.**

```python
def huffman(freq):
    h = [(f, i, s) for i, (s, f) in enumerate(sorted(freq.items()))]
    heapq.heapify(h)                          # Week 3's priority queue
    nxt = len(h); children = {}
    while len(h) > 1:
        f1, _, a = heapq.heappop(h)
        f2, _, b = heapq.heappop(h)
        children[nxt] = (a, b)
        heapq.heappush(h, (f1 + f2, nxt, nxt)); nxt += 1
    return children, h[0][2]                   # tree and root
```

$\Theta(n\log n)$: $n-1$ merges, each two pops and a push. **The second element of each tuple is a
tie-break** — without it, Python compares the third element, which may not be orderable, and the code
raises `TypeError` on some inputs and not others.

### Worked example

CLRS's frequencies, over 100 characters:

| symbol | a | b | c | d | e | f |
| --- | --- | --- | --- | --- | --- | --- |
| frequency | 45 | 13 | 12 | 16 | 9 | 5 |
| **code length** | **1** | 3 | 3 | 3 | 4 | 4 |

| encoding | total bits |
| --- | --- |
| fixed-length (3 bits × 100) | 300 |
| **Huffman** | **224** |

*(Verified: 224 is optimal, confirmed against exhaustive search over all binary trees on six leaves.)*

**25% saved**, and the whole gain comes from `a` — 45% of the text — getting a single bit.

*(Verified more generally: over 500 random frequency distributions, the generated code was prefix-free
and matched the exhaustive optimum every time. **0 failures.**)*

---

## 3. Why It Is Optimal

The exchange argument is subtler than Lecture 29's, and it comes in two parts.

### Part 1 — the greedy choice is safe

> **Lemma.** If $x$ and $y$ are the two least frequent symbols, some optimal tree has them as siblings
> at maximum depth.

*Proof.* Take an optimal tree $T$ and let $a, b$ be two siblings at maximum depth (they exist: the
deepest internal node has two leaf children). Suppose $x \ne a$. Then $f_x \le f_a$ — $x$ is among the
least frequent — and $\mathrm{depth}(a) \ge \mathrm{depth}(x)$, since $a$ is at maximum depth.

Swap $x$ and $a$. The cost changes by

$$(f_x - f_a)\big(\mathrm{depth}(a) - \mathrm{depth}(x)\big) \le 0$$

— a product of a non-positive and a non-negative number. So the tree is no worse, and $T$ was optimal,
so it is still optimal. Repeat for $y$ and $b$. $\square$

**That single product is the entire lemma.** Read it twice: the less frequent symbol moves deeper, the
more frequent one moves shallower, and the cost cannot go up.

### Part 2 — what remains is the same problem

Merging $x$ and $y$ into one symbol $z$ with $f_z = f_x + f_y$ gives an instance with one fewer symbol.
For any tree, the cost of the original equals the cost of the merged instance plus $f_x + f_y$ —
because $x$ and $y$ sit one level below $z$.

That additive constant is independent of the tree, so **an optimal tree for the merged instance gives
an optimal tree for the original.** Induct. $\square$

> **Both parts are needed.** Part 1 is the greedy-choice property; Part 2 is optimal substructure.
> Lecture 28 §2 said greedy requires both, and Huffman is the cleanest place in the course to see them
> as two separate obligations.

---

## 4. How Good Is It?

**Shannon's entropy** is the theoretical floor for any symbol-by-symbol code:

$$H = -\sum_s p_s \log_2 p_s \text{ bits per symbol}$$

> $$H \;\le\; \text{Huffman's average length} \;<\; H + 1$$

*(Verified over 2,000 random distributions: **0** cases below $H$ and **0** cases at or above $H+1$.)*

**Within one bit per symbol of the information-theoretic optimum**, always. For a large alphabet that
is a small relative overhead.

### Where it is worst

That "+1" is not tight in general but it is nearly tight in one important case. With **two symbols**,
Huffman must give each a whole bit — there is nothing shorter:

| $P(a)$ | entropy | Huffman | overhead |
| --- | --- | --- | --- |
| 0.5 | 1.0000 | 1.0000 | 0.0000 |
| 0.7 | 0.8813 | 1.0000 | 0.1187 |
| 0.9 | 0.4690 | 1.0000 | 0.5310 |
| **0.99** | **0.0808** | **1.0000** | **0.9192** |

*(Verified.)*

At $P(a) = 0.99$ the information content is **0.08 bits** and Huffman spends **1 bit** — **twelve times
the theoretical minimum.**

**This is why arithmetic coding exists.** It encodes the whole message as a single number and is not
constrained to an integer number of bits per symbol, so it reaches the entropy bound. Modern formats
mostly use arithmetic or range coding for exactly this reason; Huffman survives where speed and
simplicity matter more than the last few per cent.

---

## 5. Practical Matters

**The code table must be transmitted.** The decoder cannot invent it. For a short message the table can
cost more than the compression saves — encoding a 100-byte file with a 256-entry table makes it larger.
Real formats use **canonical Huffman codes**, which are reconstructible from the code *lengths* alone,
so only the lengths are stored.

**The output is bits, not bytes.** You must pack them, and record how many bits of the final byte are
real. Forgetting the padding length is the classic bug and it corrupts exactly the last symbol.

**Ties give different trees.** Two symbols with equal frequency can be merged in either order, giving
different codes with **identical total cost**. Your output need not match a reference byte for byte;
the total bit count must.

**Huffman assumes symbols are independent.** It cannot exploit the fact that `q` is nearly always
followed by `u`. That is what LZ77 and its descendants do, and it is why real compressors combine them:
**DEFLATE — `gzip`, `zip`, PNG — is LZ77 followed by Huffman.** JPEG and MP3 use Huffman on quantised
coefficients.

---

## 6. Measured on Real Text

The Lab 9 corpus: 200,000 characters of Zipf-distributed English words, 19 distinct symbols.

| encoding | total | bits/char |
| --- | --- | --- |
| raw 8-bit | 1,600,000 bits | 8.000 |
| fixed-length $\lceil\log_2 19\rceil$ | 1,000,000 bits | 5.000 |
| **Huffman** | **689,088 bits** | **3.4454** |
| entropy floor | — | **3.4161** |

*(Verified.)*

**56.9% smaller than raw**, and within **0.03 bits per character** of the entropy bound — an overhead
of under 1%, far better than the guaranteed +1.

The code lengths are what you would expect:

| symbol | count | code length |
| --- | --- | --- |
| space | 55,960 | **2** |
| `t` | 24,656 | 3 |
| `h` | 20,606 | 3 |
| `e` | 18,674 | 3 |
| `o` | 16,271 | 4 |
| `a` | 13,573 | 4 |

Longest code: **9 bits**. **Frequent symbols got short codes, which is the whole idea, and the
algorithm found the assignment without being told anything about English.**

---

## 7. Where Week 9 Leaves You

Four greedy algorithms, four exchange arguments, and three heuristics that looked reasonable and were
wrong — one of which survived 2,000 random tests.

**The transferable skill is not any of the four algorithms.** It is the habit of treating a greedy rule
as a conjecture: try to break it by search, and if it survives, prove it by exchange. Both halves are
necessary and neither substitutes for the other.

**MIDTERM 2 is in Week 10** and covers Weeks 5–9. The exchange argument appears in four of those five
weeks — Dijkstra, the cut property, activity selection, Huffman — and being able to write one is the
single most examinable skill in the second half of this course.

---

## 8. What to Do

- Read CLRS §15.3. The proof there is §3 above, stated as Lemmas 15.2 and 15.3.
- **PS 9** implements Huffman with encoding and decoding, and verifies the entropy bound.
- **Lab 9** compresses a real file and reports the ratio.
- **PROJECT 1 is due Friday.**
- **Quiz 9 covers Week 8.**
- **Week 10** starts string algorithms and holds MIDTERM 2.

---

*CS 102 · Week 9 · Lecture 30 · © CSE Department*

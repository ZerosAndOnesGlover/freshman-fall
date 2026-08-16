# CS 102 · Computer Science II
## Lecture 08: AVL Trees — Insertion, the Height Bound, and Deletion

**Date:** Wednesday 27 January 2027 · 09:00–09:50 · Week 2

---

## 1. The Invariant

An **AVL tree** is a BST in which, at every node,

$$\big|\,h(\text{left}) - h(\text{right})\,\big| \le 1$$

where height counts **edges** and the empty tree has height $-1$ — the convention from Week 1, used
without exception all term.

The quantity $\mathrm{bf}(v) = h(v.\text{left}) - h(v.\text{right})$ is $v$'s **balance factor**. The
invariant says $\mathrm{bf}(v) \in \{-1, 0, +1\}$ everywhere.

Note what has *not* changed: **the BST invariant is untouched.** An AVL tree is a BST with an extra
condition. Every search you wrote last week works on an AVL tree unmodified, and searching is the
operation we are buying the guarantee for.

### Storing the height

Each node caches its own height. It could be recomputed, but recomputing $h(v)$ costs $\Theta(\text{size of } v)$,
which would make every insertion $\Theta(n)$ and defeat the point.

```python
class Node:
    __slots__ = ('key', 'left', 'right', 'height')
    def __init__(self, key):
        self.key = key
        self.left = self.right = None
        self.height = 0          # a leaf has height 0

def h(t):
    return -1 if t is None else t.height

def update_height(t):
    t.height = 1 + max(h(t.left), h(t.right))

def bf(t):
    return h(t.left) - h(t.right)
```

Writing `h(t)` as a function that handles `None` rather than reading `t.height` directly is not
stylistic. The empty tree has no node to store $-1$ on, and every off-by-one bug in this
week's problem set traces back to someone special-casing `None` inconsistently in two places.

---

## 2. Insertion

Insert exactly as in a BST, then rebalance on the way back up the recursion.

```python
def rebalance(t):
    update_height(t)
    b = bf(t)
    if b > 1:                                    # left-heavy
        if bf(t.left) < 0:
            t.left = rotate_left(t.left)         # LR → LL
        return rotate_right(t)
    if b < -1:                                   # right-heavy
        if bf(t.right) > 0:
            t.right = rotate_right(t.right)      # RL → RR
        return rotate_left(t)
    return t                                     # already balanced

def insert(t, key):
    if t is None:
        return Node(key)
    if key < t.key:
        t.left = insert(t.left, key)
    elif key > t.key:
        t.right = insert(t.right, key)
    else:
        return t                                 # duplicate: no change
    return rebalance(t)
```

Three things deserve attention.

**`rebalance` is called on every node of the search path**, not only where a violation occurred. The
`return t` branch is the common case. This is what makes the code short: there is no separate "walk
back up looking for the violation" phase, because the recursion *is* that walk.

**`update_height` runs before the balance factor is read.** The child was just modified; the cached
height at `t` is stale until this line.

**The duplicate case returns before rebalancing.** Nothing changed, so nothing needs repair. Forgetting
this is harmless here but becomes a real bug in the deletion code below.

### At most one rebalance per insertion

An insertion increases the height of a subtree by at most 1, and only along the search path. Once a
rotation has been applied at the lowest violating node $z$, the subtree rooted there has the height
it had *before* the insertion — the rotation gives back the level the insertion added. Every ancestor
therefore sees an unchanged child height and needs no repair.

So insertion performs **at most one rebalance event** — a single or a double rotation, so at most two
individual rotations — no matter how tall the tree is.

*(Verified: over 300 random AVL trees, the maximum number of individual rotations triggered by any
single insertion is 2.)*

This is the source of the standard claim that AVL insertion is cheap. **It is a claim about
insertion only**, and section 5 shows deletion does not share it.

---

## 3. The Height Bound

The invariant must actually force $h = O(\log n)$. The argument runs backwards from the shape you
would expect: instead of asking how tall a tree with $n$ nodes can be, ask **how few nodes a tree of
height $h$ can have.**

Let $N(h)$ be the minimum number of nodes in an AVL tree of height $h$. Such a tree has a root, and
one subtree of height $h-1$; the other must have height $h-2$ (it cannot be less, by the invariant,
and making it larger only adds nodes). So

$$N(h) = N(h-1) + N(h-2) + 1, \qquad N(0) = 1,\; N(1) = 2.$$

| $h$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $N(h)$ | 1 | 2 | 4 | 7 | 12 | 20 | 33 | 54 | 88 | 143 | 232 | 376 |

The trees achieving these minima are called **Fibonacci trees**, for a reason visible in the numbers:
each is one less than a Fibonacci number.

$$N(h) = F(h+3) - 1$$

*(Verified for $h = 0 \dots 35$ against $F(0)=0,\, F(1)=1$.)* The proof is a two-line induction and is
PS 2 D1.

Since $F(k) = \dfrac{\varphi^{k} - \psi^{k}}{\sqrt5}$ with $\varphi = \frac{1+\sqrt5}{2}$ and
$|\psi| = 1/\varphi < 1$, we have $F(k) > \varphi^{k}/\sqrt5 - \tfrac12$. A tree of height $h$ on $n$
nodes satisfies $n \ge N(h)$, so

$$n + 1 \;\ge\; F(h+3) \;>\; \frac{\varphi^{\,h+3}}{\sqrt5} - \frac12
\quad\Longrightarrow\quad \varphi^{\,h+3} < \sqrt5\left(n + \tfrac32\right)$$

$$\boxed{\;h \;<\; \log_\varphi (n+2) \;-\; \big(3 - \log_\varphi \sqrt5\big)
\;=\; 1.4404\log_2(n+2) - 1.3277\;}$$

**An AVL tree is at most about 44% taller than a perfect tree, and that is the worst case, not the
average.**

### A warning about that constant

The bound is very often quoted with $n+1$ inside the logarithm rather than $n+2$. **That version is
false.** It fails at exactly the sizes where the bound is tight — $n = 2, 7, 20, 54, 143, 376, \dots$,
which are precisely the values of $N(h)$.

*(Verified: checking every $n$ from 1 to 500,000, the $n+1$ form is violated 13 times, at $n = 2, 7,
20, 54, 143, 376, \dots$; the $n+1.5$ and $n+2$ forms are never violated.)*

This is worth more than the two characters it costs. A bound that holds asymptotically but fails at
small inputs is not a bound, and the sizes where it fails here are not obscure — they are the *only*
sizes at which the worst case actually occurs. When you copy a constant from a reference, check it at
the extremal cases, not at a convenient large $n$.

### How tight is it?

| worst-case height $h$ | smallest $n$ achieving it | $h / \log_2(n+1)$ |
| --- | --- | --- |
| 4 | 12 | 1.081 |
| 8 | 88 | 1.235 |
| 12 | 609 | 1.297 |
| 20 | 28,656 | 1.351 |
| 30 | 3,524,577 | 1.379 |
| 40 | 433,494,436 | 1.394 |
| 50 | 53,316,291,172 | 1.403 |

The ratio approaches $1.4404$ from below, and slowly — the same slow convergence you met in Week 1
with the expected-height constant, and for the same reason. At $n = 10^9$ the worst-case AVL height
is **41**, against **29** for a perfect tree.

**41 comparisons, guaranteed, on a billion keys.** That is the whole point of the week.

---

## 4. Measured

Building trees from the sorted keys $0, 1, \dots, n-1$ — the input that destroyed the plain BST:

| $n$ | plain BST height | AVL height | perfect height | AVL rotations |
| --- | --- | --- | --- | --- |
| $1{,}000$ | 999 | **9** | 9 | 990 |
| $10{,}000$ | 9,999 | **13** | 13 | 9,986 |
| $100{,}000$ | 99,999 | **16** | 16 | 99,983 |

*(The BST heights are exact by construction — each insertion walks the entire right spine — and were
confirmed by measurement at every size. The $n = 100{,}000$ build is $\Theta(n^2)$ and took **307
seconds**, against **1.00 s** for the AVL tree on the same keys — which is itself the point.)*

On sorted input the AVL tree does not merely stay logarithmic — it lands on **exactly the perfect
height**. Sorted input drives it into the one shape the rotations can build most evenly, so the
worst case for the BST is close to the best case for the AVL tree.

And the cost, on the same machine — build times from sorted input, best of 3 runs:

| $n$ | BST build | BST doubling ratio | AVL build | ratio BST/AVL |
| --- | --- | --- | --- | --- |
| $1{,}000$ | 36.6 ms | — | 6.4 ms | 5.7× |
| $2{,}000$ | 126.0 ms | 3.45 | 20.0 ms | 6.3× |
| $4{,}000$ | 470.2 ms | 3.73 | 27.6 ms | 17.1× |
| $8{,}000$ | 1802.4 ms | 3.83 | 61.8 ms | 29.2× |
| $16{,}000$ | 7237.0 ms | 4.02 | 138.7 ms | 52.2× |

**The BST doubling ratio converges on 4**, which is what $\Theta(n^2)$ looks like when you measure it,
and the final column doubles with $n$ because the other structure is $\Theta(n\log n)$. **Lab 2 has
you reproduce this table** and check that behaviour yourself.

---

## 5. Deletion, and the Asymmetry

Deletion follows the BST algorithm from Week 1 — three cases, with the two-child case replaced by
its inorder successor — and then rebalances on the way up:

```python
def delete(t, key):
    if t is None:
        return None
    if key < t.key:
        t.left = delete(t.left, key)
    elif key > t.key:
        t.right = delete(t.right, key)
    else:
        if t.left is None:  return t.right
        if t.right is None: return t.left
        s = min_node(t.right)
        t.key = s.key
        t.right = delete(t.right, s.key)
    return rebalance(t)
```

The code is barely longer than the BST version. **The analysis is not.**

An insertion's rotation restores the subtree's original height, so the repair stops. A deletion's
rotation can *reduce* the subtree's height by one — which is a new violation for the parent, which
may rotate, which may shorten again. **The repair can propagate all the way to the root.**

*(Verified: on Fibonacci trees, deleting the single worst key requires this many individual
rotations —)*

| tree height $h$ | $n$ | worst-case rotations for one deletion |
| --- | --- | --- |
| 4 | 12 | 2 |
| 8 | 88 | 4 |
| 12 | 609 | 6 |
| 16 | 4,180 | 8 |
| 18 | 10,945 | 9 |

Exactly $h/2$, every time, and $h \approx 1.44\log_2 n$ — so worst-case deletion needs
$\Theta(\log n)$ rotations, against insertion's $O(1)$.

**Both operations are still $\Theta(\log n)$ overall**, because you were walking the path anyway and
each rotation is $O(1)$. The asymmetry does not change the complexity. It changes the *constant*, and
it is the honest reason a real implementation might prefer red-black trees — Lecture 09.

Notice also that the Fibonacci trees, introduced as a proof device for the height bound, turn out to
be the concrete worst-case inputs. **The extremal object in a proof is usually the adversarial test
case**, and looking for it is a habit worth acquiring.

---

## 6. What to Do

- Read CLRS §13.1–13.2. CLRS covers red-black rather than AVL; the rotation code is shared and
  Lecture 09 handles the rest.
- **PS 2** implements AVL insertion with all four rotation cases. Start with the four-case diagram
  from Lecture 07 in front of you.
- **Quiz 2 covers Week 1** — trees, traversals, BSTs. Not this material.

---

*CS 102 · Week 2 · Lecture 08 · © CSE Department*

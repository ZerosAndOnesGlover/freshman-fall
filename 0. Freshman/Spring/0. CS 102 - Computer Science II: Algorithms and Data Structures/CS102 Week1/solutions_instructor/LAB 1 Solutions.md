# CS 102 — Lab 1 Solutions
## INSTRUCTOR ONLY

**Total: 40 points.** All outputs below were produced by executing the reference solution.

---

## Part A — Reference Renderer (12 pts)

```python
def render(t):
    out = []
    def walk(n, d):
        if n is None: return
        walk(n.right, d + 1)                 # reverse inorder: right, node, left
        out.append(' ' * (4 * d) + str(n.key))
        walk(n.left, d + 1)
    walk(t, 0)
    return '\n'.join(out)
```

**Marking A2 (8):** 4 for a rotated layout that is readable, 4 for depth-proportional indent being
actually correct. **Accept any orientation.** Students who attempt top-down box-drawing and produce
something half-working should get full marks if the shape is legible — the lab explicitly told them
not to, so the effort is misdirected but not wrong.

---

## Part C — Measured Results (12 pts)

### C1 — `[50, 30, 70, 20, 40, 60, 80]`

```
        80
    70
        60
50
        40
    30
        20
```

| Traversal | Output |
|---|---|
| Preorder | 50, 30, 20, 40, 70, 60, 80 |
| **Inorder** | **20, 30, 40, 50, 60, 70, 80** ← sorted ✓ |
| Postorder | 20, 40, 30, 60, 80, 70, 50 |
| Level-order | 50, 30, 70, 20, 40, 60, 80 |

Height **2** — this insertion order happens to be perfectly balanced.

### C2 — same keys, ascending

```
                        80
                    70
                60
            50
        40
    30
20
```

Height **6** ($= n-1$). The renderer shows a single descending staircase — a linked list.

| Traversal | Output |
|---|---|
| Preorder | 20, 30, 40, 50, 60, 70, 80 |
| Inorder | 20, 30, 40, 50, 60, 70, 80 |
| Postorder | 80, 70, 60, 50, 40, 30, 20 |
| Level-order | 20, 30, 40, 50, 60, 70, 80 |

**Expected answer to "which traversals are identical, and why?":**

**Preorder = inorder = level-order**, and **postorder is the exact reverse**.

Every node has an empty left subtree. Preorder is (node, left, right) and inorder is (left, node,
right) — with `left` empty these are both just (node, right), so they coincide. Level-order coincides
because each level holds exactly one node. Postorder is (left, right, node) = (right, node), which
emits the deepest node first and so reverses the order.

**This is a good discriminator.** A student who answers "they're the same because the tree is
degenerate" without identifying *which* subtree is empty has not really seen it — award 2 of 3.

### C3 — 200 random BSTs, $n = 1000$

| statistic | value |
|---|---|
| mean height | **21.20** |
| min | 16 |
| max | 30 |
| $\log_2 1000$ | 9.97 |
| $n - 1$ | 999 |

**mean / $\log_2 n$ = 2.13.** Random insertion lands very near the balanced end of the range and
nowhere near the degenerate end.

### C4 — sorted insertion, $n = 1000$

Height **999**. Exactly $n-1$.

**Expected one-sentence explanation:** every key is larger than all keys already present, so it is
inserted as the right child of the deepest node, producing a chain with no branching.

---

## Part D — Interpretation (4 pts)

### D1 *(2)* Why measurement below $4.311\ln n$ is not a contradiction

**Expected answer.** $4.311\ln n$ is an *asymptotic* statement — it describes the limit as
$n \to \infty$, with lower-order terms omitted. The next term is $-1.953\ln\ln n$ plus a negative
constant, and at $n=1000$ those corrections are large relative to the leading term. Measured 21.2
against a leading-term estimate of 29.8 is entirely consistent.

**The general lesson: an asymptotic result can be correct and still be a poor numerical predictor at
practical sizes.** Full marks require this sentence or an equivalent. This is the same point as Lab 0
D4 and it recurs in Week 6.

### D2 *(2)* Which traversal to print when debugging

**Inorder**, and check that it is **strictly increasing**.

The BST invariant is *equivalent* to inorder being sorted, so a single $\Theta(n)$ traversal
validates the entire structure — and the first position where the order breaks localises the fault.
No other traversal has this property.

**Award 1** for "inorder" with no justification; **2** for naming the sortedness check.

---

## Marking Summary

| Part | Points |
|---|---|
| A — node, builder, renderer | 12 |
| B — instrumented traversals and trace | 12 |
| C — four experiments | 12 |
| D — interpretation | 4 |
| **Total** | **40** |

> **Student numbers in C3 will differ** — mean height should land between roughly 19 and 23 for
> $n=1000$. A mean near 10 means they measured *depth* not height; a mean near 999 means they
> inserted sorted keys by mistake. Both are worth a comment rather than a deduction if the rest is
> sound.

---

*CS 102 · Week 1 · Lab 1 Solutions · © CSE Department*

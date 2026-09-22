# CS 102 · Lab 1
## Visualising Tree Traversals

**Date:** Tuesday 2 February 2027 · 15:00–16:50 · Lab section (Week 2) — covers Week 1 (L04–L06)
*2-hour lab · 40 points · in-lab checkoff*
**Deliverable:** `lab1.py` and `RESULTS.md`. In-lab checkoff by your TA.

---

## Purpose

Traversal order is the kind of thing that seems obvious in a lecture and evaporates under exam
conditions. **The fix is to see it happen** — to watch the order emerge from the recursion rather
than memorising four word-sequences.

You will also build the ASCII tree printer that you will reuse for debugging in Weeks 2, 3 and 6. It
is worth doing well now.

---

## Part A — A Tree You Can See (12 pts)

**A1.** *(4)* Implement `Node` and a builder `from_list(keys)` that inserts keys into a BST in order.

**A2.** *(8)* Implement `render(t)` returning a multi-line string showing the tree's shape. Rotated
90° is much easier than top-down and is entirely acceptable:

```
        20
    15
10
        9
    7
        3
            1
```

*(This is the Lecture 05 tree, right subtree at the top, produced by a reverse-inorder walk with
indentation proportional to depth.)*

**Hint:** reverse inorder — right, node, left — with `depth * 4` spaces of indent. Six lines of code.
Do **not** attempt top-down box drawing; it is a much harder problem and is not what is being marked.

---

## Part B — Instrumented Traversals (12 pts)

**B1.** *(8)* Implement all four traversals so that each **records the order in which nodes are
visited** rather than printing. Return a list of keys.

**B2.** *(4)* Write `trace(t)` that, for a given traversal, prints each step as it happens with the
current recursion depth:

```
enter 10
  enter 5
    enter 3
      enter 1
      visit 1
      leave 1
    visit 3
    ...
```

**The `visit` line is the traversal output.** Changing *where* the visit happens relative to the two
recursive calls is the entire difference between preorder, inorder and postorder — and this trace is
designed to make that visible.

---

## Part C — Experiments (12 pts)

Record answers in `RESULTS.md`.

**C1.** *(3)* Build a BST from `[50, 30, 70, 20, 40, 60, 80]`. Render it. Give all four traversals.
**Confirm inorder is sorted.**

**C2.** *(3)* Build a BST from the same keys **in ascending order**. Render it. What does `render`
show? Give the height. Compare the four traversals with C1 — **which traversals are now identical to
each other, and why?**

**C3.** *(3)* Generate 200 random BSTs of 1000 keys each. Record the height of each. Report the
mean, min and max. Compare against $\log_2 1000 \approx 9.97$ and against $n-1 = 999$.

**C4.** *(3)* Repeat C3 with keys inserted in sorted order. Report the height. **Explain the
difference in one sentence.**

---

## Part D — Interpret (4 pts)

**D1.** *(2)* From C3: your mean height should be roughly 2× $\log_2 n$. Lecture 06 gives the
asymptotic expected height as $4.311\ln n \approx 29.8$ for $n=1000$. **Your measurement will be
well below that.** Explain why this is not a contradiction.

**D2.** *(2)* You are debugging a BST that returns wrong results. **Which single traversal would you
print first, and what would you check about its output?** Justify in one sentence.

---

## Marking

| Part | Points |
|---|---|
| A — node, builder, renderer | 12 |
| B — instrumented traversals and trace | 12 |
| C — four experiments | 12 |
| D — interpretation | 4 |
| **Total** | **40** |

---

*CS 102 · Week 1 · Lab 1 · © CSE Department*

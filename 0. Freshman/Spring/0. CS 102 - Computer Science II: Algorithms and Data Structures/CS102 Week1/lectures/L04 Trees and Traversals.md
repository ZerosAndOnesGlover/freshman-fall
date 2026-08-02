# CS 102 · Computer Science II
## Lecture 04: Trees and Traversals

---

## 1. Why Trees

Every structure in CS 101 was linear: arrays, linked lists, stacks, queues. Linear structures force a
choice you cannot escape — **either fast search or fast insertion, never both**.

| Structure | Search | Insert | Why |
| --- | --- | --- | --- |
| Sorted array | $\Theta(\log n)$ | $\Theta(n)$ | Binary search is fast; insertion shifts elements |
| Unsorted linked list | $\Theta(n)$ | $\Theta(1)$ | Insertion is free; search must scan |

The sorted array can bisect because it has *random access*; the linked list can insert cheaply
because it has *no positional commitment*. **Trees are the structure that gets both**, and the price
is maintaining an invariant.

---

## 2. Terminology

A **tree** is a connected `acyclic` graph. A **rooted tree** designates one vertex as the root, which
orients every edge away from it.

| Term | Meaning |
| --- | --- |
| **Root** | The distinguished top node; the only node with no parent |
| **Parent / child** | Adjacent nodes, nearer to / further from the root |
| **Leaf** | A node with no children |
| **Internal node** | A node with at least one child |
| **Sibling** | Nodes sharing a parent |
| **Depth** of a node | Number of edges from the root to it — the **root has depth 0** |
| **Height** of a node | Number of edges on the longest path from it down to a leaf — **leaves have height 0** |
| **Height of a tree** | The height of its root |
| **Subtree** rooted at $v$ | $v$ together with all its descendants |

**Depth counts upward to the root; height counts downward to a leaf.** They are not the same and
confusing them is the most common source of off-by-one errors in this week's problem set.

> **Convention warning.** Some texts define height in *nodes* rather than edges, making a leaf have
> height 1. **This course counts edges throughout**, so a single-node tree has height 0 and an empty
> tree has height $-1$. `CLRS` uses the same convention. State your convention in any proof.

### Binary trees

A **binary tree** is a rooted tree in which every node has at most two children, distinguished as
**left** and **right**. The distinction matters even when a node has only one child: a left-only
child and a right-only child are different trees.

**Special shapes:**

- **Full** — every node has 0 or 2 children.
- **Complete** — every level is filled except possibly the last, which is filled left to right.
  *(This is the shape that makes Week 3's array-based heap possible.)*
- **Perfect** — all internal nodes have 2 children and all leaves are at the same depth.

### Size and height bounds

A perfect binary tree of height $h$ has exactly $2^{h+1} - 1$ nodes, with $2^{d}$ nodes at depth $d$.

For **any** binary tree with $n$ nodes and height $h$:

$$\log_2(n+1) - 1 \le h \le n - 1$$

The lower bound comes from a perfect tree — the most nodes possible for a given height. The upper
bound comes from a degenerate tree, one node per level: a linked list wearing a tree costume.

**That range is the whole story of Weeks 1–2.** A BST's operations cost $\Theta(h)$, so the same
algorithm is $\Theta(\log n)$ on a balanced tree and $\Theta(n)$ on a degenerate one. Week 2 exists
to force $h = \Theta(\log n)$.

---

## 3. Representation

```python
class Node:
    def __init__(self, key, left=None, right=None):
        self.key   = key
        self.left  = left
        self.right = right
```

An empty tree is `None`. This makes the recursive cases fall out naturally, since almost every tree
algorithm has the shape *"if the tree is empty do the trivial thing, otherwise combine results from
the two subtrees."*

```python
def size(t):
    if t is None:
        return 0
    return 1 + size(t.left) + size(t.right)

def height(t):
    if t is None:
        return -1                    # empty tree: height -1, per our convention
    return 1 + max(height(t.left), height(t.right))
```

**`height(None) == -1` is not arbitrary.** It makes a single leaf come out at
$1 + \max(-1,-1) = 0$, which is what the edge-counting convention requires. Returning `0` for the
empty tree — a tempting choice — makes every leaf have height 1 and silently shifts every bound in
this lecture by one.

---

## 4. Traversals

A traversal visits every node exactly once. For binary trees there are four standard orders, and the
first three differ only in **when the node itself is visited relative to its subtrees**.

```python
def preorder(t, visit):              # node, left, right
    if t is None: return
    visit(t.key)
    preorder(t.left, visit)
    preorder(t.right, visit)

def inorder(t, visit):               # left, node, right
    if t is None: return
    inorder(t.left, visit)
    visit(t.key)
    inorder(t.right, visit)

def postorder(t, visit):             # left, right, node
    if t is None: return
    postorder(t.left, visit)
    postorder(t.right, visit)
    visit(t.key)
```

**Level-order** (breadth-first) is different in kind — it is not a simple recursion, and it needs a
queue:

```python
from collections import deque

def level_order(t, visit):
    if t is None: return
    q = deque([t])
    while q:
        node = q.popleft()
        visit(node.key)
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
```

**That queue is the same idea as Week 4's breadth-first search on graphs.** Level-order traversal
*is* `BFS`, restricted to a tree; noticing this now makes Week 4 much easier.

### Worked example

For this tree:

```
            5
          /   \
         3     8
        / \   / \
       2   4 7   9
```

| Traversal | Output |
| --- | --- |
| Preorder | 5, 3, 2, 4, 8, 7, 9 |
| Inorder | **2, 3, 4, 5, 7, 8, 9** |
| Postorder | 2, 4, 3, 7, 9, 8, 5 |
| Level-order | 5, 3, 8, 2, 4, 7, 9 |

*(Verified by execution — see `solutions_instructor/`.)*

**The inorder output is sorted.** That is not a coincidence about this tree; it is the defining
property of a binary search tree and is the subject of Lecture 05.

### What each traversal is for

| Traversal | Natural use |
| --- | --- |
| **Preorder** | Copying a tree; serialising it; processing a node before its children |
| **Inorder** | **Retrieving BST keys in sorted order** |
| **Postorder** | Freeing a tree; evaluating an expression tree; anything needing children first |
| **Level-order** | Printing by depth; finding the shallowest node meeting a condition |

**Postorder is the deletion order.** You must free the children before the parent, because once the
parent is gone you have lost the pointers to them. In C this is the difference between correct code
and a memory leak; PROG 101 covered the mechanics.

### Complexity

All four traversals are $\Theta(n)$ time — each node is visited exactly once and does $\Theta(1)$
work.

Space differs, and it matters:

- The three recursive traversals use $\Theta(h)$ stack space. **On a degenerate tree that is
  $\Theta(n)$**, which will overflow Python's recursion limit at around 1,000 nodes.
- Level-order uses $\Theta(w)$ where $w$ is the maximum width. For a perfect tree the last level
  holds about $n/2$ nodes, so this is $\Theta(n)$ — **level-order is the most memory-hungry
  traversal on balanced trees**, which is the reverse of what most students guess.

---

## 5. Reconstruction

A single traversal does not determine a tree. Preorder `5, 3` could be either

```
    5           5
   /             \
  3               3
```

**Inorder plus one of preorder/postorder does determine it** (given distinct keys). The argument:
preorder's first element is the root; find it in the inorder sequence; everything left of it is the
left subtree and everything right is the right subtree; recurse.

```python
def build(preorder, inorder):
    if not preorder:
        return None
    root_key = preorder[0]
    k = inorder.index(root_key)              # position splits inorder into two subtrees
    left  = build(preorder[1:k+1], inorder[:k])
    right = build(preorder[k+1:], inorder[k+1:])
    return Node(root_key, left, right)
```

**Inorder plus level-order also works. Preorder plus postorder does not** — it cannot distinguish the
two single-child trees above. Problem Set 1 asks you to prove that.

> **Why distinct keys are required:** with duplicates, `inorder.index` is ambiguous and the split
> point is not determined. This is one reason BSTs usually store distinct keys, or attach a count to
> each node rather than inserting a duplicate.

---

## 6. Exercises

**1.** Draw a binary tree with 6 nodes whose height is 5, and one with 6 nodes whose height is 2.
What are the minimum and maximum heights for $n = 6$, and do your trees achieve them?

**2.** Prove by induction that a perfect binary tree of height $h$ has $2^{h+1} - 1$ nodes.

**3.** Give a tree for which preorder and inorder produce the *same* sequence. Characterise **all**
such trees.

**4.** Rewrite `inorder` iteratively using an explicit stack. Why is this worth doing in practice?

**5.** The `build` function above is $\Theta(n^2)$ in the worst case. Identify the two lines
responsible and describe how to make it $\Theta(n)$.

---

*CS 102 · Week 1 · Lecture 04 · © CSE Department*

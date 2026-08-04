# PROG 102 · Lecture 21
## Implementing a Binary Search Tree

**Week 6 · Friday · 50 minutes**
**Reading:** *C++ Primer* Ch. 12 (revisit) · **Cross-course:** CS 102 Weeks 1–2
**Assumes:** L19, L20, Week 5 (`unique_ptr`)

---

## 1. Where `unique_ptr` Is Actually Right

Lecture 19 used raw `prev`/`next` pointers, because those are *structure*, not ownership — the list
owns its nodes.

**A tree is different.** Each node genuinely owns its children: destroying a node should destroy its
subtree, and no other node points at those children. That is exclusive ownership, and it is exactly
what `unique_ptr` is for.

```cpp
template <typename T, typename Compare = std::less<T>>
class BST {
    struct Node {
        T value;
        std::unique_ptr<Node> left, right;
        explicit Node(T v) : value(std::move(v)) {}
    };
    std::unique_ptr<Node> root;
    std::size_t count = 0;
    Compare cmp;
};
```

**And this class needs none of the five special members.** The `unique_ptr`s destroy the tree, the
compiler's generated move operations work, and copying is correctly *disabled* because `unique_ptr` is
not copyable. **The Rule of Zero applies here and did not apply to the list**, which is worth pausing
on: the difference is whether a library type already models your ownership.

*(If you want a copyable BST you must write the copy constructor — a recursive clone. Project 1 asks
for it.)*

---

## 2. The Comparator as a Template Parameter

```cpp
template <typename T, typename Compare = std::less<T>>
```

`Compare` defaults to `std::less<T>`, so `BST<int>` orders ascending. Supplying another gives a
different tree from the same code:

```
descending: 8 5 3          // BST<int, std::greater<int>>
```

This is how `std::map` and `std::set` do it, and it is Week 2's non-type-parameter idea applied to a
*policy* rather than a size. **The comparator is part of the type**, so `BST<int>` and
`BST<int, std::greater<int>>` are unrelated types — which is correct, since a tree built with one
ordering is meaningless under another.

> **`Compare` must be a strict weak ordering** (L04 §6.1). The BST uses `cmp(a,b)` and `cmp(b,a)` to
> decide left, right or equal — so a comparator that says both are false for distinct values will treat
> them as duplicates and silently drop one.

---

## 3. Insert, Search, Traverse

```cpp
static void insert_at(std::unique_ptr<Node>& slot, T v, Compare& cmp,
                      std::size_t& n, bool& added) {
    if (!slot) { slot = std::make_unique<Node>(std::move(v)); ++n; added = true; return; }
    if      (cmp(v, slot->value)) insert_at(slot->left,  std::move(v), cmp, n, added);
    else if (cmp(slot->value, v)) insert_at(slot->right, std::move(v), cmp, n, added);
    else added = false;                                     // duplicate
}
```

**Note the parameter is `std::unique_ptr<Node>&` — a reference to the slot**, not to the node. That is
what lets the base case assign into the parent's `left` or `right` without the parent knowing which one
it was. It is the standard trick for tree insertion in C++ and it is worth recognising.

Search is the same descent, written iteratively because it needs no ownership manipulation:

```cpp
bool contains(const T& v) const {
    const Node* p = root.get();
    while (p) {
        if      (cmp(v, p->value)) p = p->left.get();
        else if (cmp(p->value, v)) p = p->right.get();
        else return true;
    }
    return false;
}
```

Verified on `{5,3,8,1,4,7,9,3}`:

```
size=7 height=2 (edges, empty=-1)
inorder: 1 3 4 5 7 8 9
contains(4)=yes contains(6)=no
sorted? yes
```

**Seven, not eight** — the duplicate `3` was rejected. **In-order traversal yields sorted output**,
which is the defining property of a BST and the reason `std::map` iterates in key order (L11 §5.1).

### 3.1 The Height Convention

**Height is measured in edges. An empty tree has height −1; a single node has height 0.**

```
empty tree height = -1
```

This is the convention used throughout this degree — CS 102 uses it in every week that mentions trees —
and mixing it with the node-counting convention is a reliable source of off-by-one errors in
assignments. **Edges. Empty is −1.**

### 3.2 The Degenerate Case

```
sorted input: size=10 height=9  <- a linked list
```

Inserting `0..9` in order gives a tree of height 9. **Every operation is now $O(n)$**, and the structure
is a linked list wearing a tree's interface.

This is why `std::map` is a **red-black tree** and not a plain BST — self-balancing exists precisely to
prevent this. **You are not implementing balancing this week**; CS 102 covers AVL and red-black
rotations, and Project 1 makes measuring the degeneracy a required experiment rather than a fix.

---

## 4. The Bug That Only Appears at Scale

Here is the design from §1, in its simplest form:

```cpp
struct Node { int v; std::unique_ptr<Node> next; };
```

Destroying the head runs `~Node`, which destroys `next`, which runs `~Node`, which destroys *its*
`next`… **The destructor is recursive, and recursion runs on the stack.**

Measured, on an 8 MB stack:

| chain length | destruction |
| --- | --- |
| 1,000 | fine |
| 100,000 | fine |
| 500,000 | fine |
| **1,000,000** | **segmentation fault** |

The threshold on this machine is between 500,000 and 1,000,000 nodes. **The program builds the
structure successfully and then dies while cleaning up**, with a stack overflow inside a destructor —
which is about as unhelpful a crash site as exists.

### 4.1 Why It Is Nasty

- **It is invisible in testing** at any reasonable test size.
- **The crash is in the destructor**, so the stack trace is a thousand identical frames and points at
  nothing.
- **It is not a leak**, so the sanitizers do not flag it. ASan reports a SEGV, not a diagnosis.
- **It scales with the data, not the code**, so the code that "worked fine for a year" fails when a
  customer's dataset grows.

### 4.2 The Fix

Unlink iteratively before the chain unwinds:

```cpp
~Node() {
    auto n = std::move(next);
    while (n) n = std::move(n->next);      // each iteration destroys one node, no recursion
}
```

Verified: **5,000,000 nodes destroy without trouble.**

For a *tree*, the same problem appears when the tree is degenerate (§3.2) — a sorted-input BST of a
million elements is a million-deep chain. The fix is the same in spirit: destroy iteratively, with an
explicit stack or by repeatedly detaching the leftmost node.

> **This is the first bug in this course that only exists at scale**, and the general lesson is the one
> to keep: **recursion over a data structure whose depth is controlled by input data is a bug waiting
> for a big enough input.** The same argument applies to a recursive `contains` on a degenerate tree,
> and to recursive JSON or XML parsers — a well-known source of real vulnerabilities.
>
> **Project 1 requires a one-million-element destruction test** for exactly this reason.

---

## 5. Comparing With the STL

Your `BST<T>` and `std::map<K,V>` solve overlapping problems. The differences are all deliberate:

| | your `BST` | `std::map` |
| --- | --- | --- |
| Balanced | **No** — degenerates on sorted input | Yes, red-black |
| Stores | values | key/value pairs |
| Iterators | none yet | bidirectional, in key order |
| Duplicates | rejected | rejected (`multimap` allows) |
| Lookup | $O(h)$, and $h$ can be $n$ | $O(\log n)$ **guaranteed** |

**The guarantee is the whole difference.** Yours is $O(\log n)$ on random input and $O(n)$ on the input
you are most likely to get — sorted, or nearly sorted, which is extremely common in practice.

> **This is the honest reason to use the library.** Not that your code is bad; the insert and search
> above are correct and clear. It is that **`std::map` makes a promise about the worst case and yours
> makes a promise about the average**, and the difference between those two is 500 lines of rotation
> logic that somebody has already written and tested.
>
> Week 6's value is that you now know precisely what those 500 lines buy.

---

## 6. Summary

| Idea | The point |
| --- | --- |
| `unique_ptr` children | A node genuinely owns its subtree — unlike a list's `next` |
| Rule of **Zero** applies here | Because `unique_ptr` already models the ownership |
| `Compare` as a template parameter | Policy in the type, exactly as `std::map` does it |
| `unique_ptr<Node>&` parameter | A reference to the *slot* — the standard insertion trick |
| In-order traversal is sorted | The defining property; the reason `map` iterates in order |
| Height in **edges**; empty = **−1** | The convention used across this degree |
| Sorted input → height 9 of 10 | A linked list wearing a tree's interface |
| **Recursive destructor** | 500,000 nodes fine; **1,000,000 segfaults** |
| Why it is nasty | Invisible in tests, useless stack trace, not a leak |
| The fix | Iterative unlink — verified at 5,000,000 |
| vs `std::map` | Yours promises the average; `map` promises the worst case |

---

## 7. Exercises

**1.** Implement `BST<T, Compare>` with `insert`, `contains`, `inorder` and `height`. Verify on
`{5,3,8,1,4,7,9,3}` that `size` is **7**, `height` is **2** and the traversal is sorted.

**2.** Report `height()` for an empty tree and for a single node. **State the convention you are using**
and confirm it matches this lecture.

**3.** Measure height against insertion order for n = 10, 100, 1,000 and 10,000: once with values
inserted **in sorted order**, and once **shuffled**, averaged over at least 100 trials.

Tabulate both against $\log_2 n$. **Report the ratio of the random height to $\log_2 n$** at each size
and say whether it is constant. *(It is not quite — say which way it drifts.)*

**4.** Build a `unique_ptr` chain of 1,000, 100,000 and 1,000,000 nodes and destroy each.
**Report where it breaks and what your stack limit is** (`ulimit -s`).

**5.** Fix it with an iterative destructor and confirm 5,000,000 works. **Does AddressSanitizer help you
diagnose the original?** Say what it reports and why that is unhelpful.

**6.** Write a **recursive** `contains`. Build a degenerate tree of one million elements and search it.
**Predict what happens before running it.**

**7.** Make your BST copyable with a recursive clone. Then answer: **what is the copy's height compared
to the original's, and why?**

---

## 8. Next

**Week 7** leaves data structures for **design patterns** — the named solutions to recurring structural
problems. The Iterator you implemented this week is one of them, which is a good sign that patterns are
descriptions of things that work rather than inventions.

**Project 1 is assigned this week and due in Week 9.** It is your list, your BST, a shared iterator
protocol and a test suite — including a one-million-element destruction test, for the reason in §4.

---

*PROG 102 · Week 6 · Lecture 21 · © CSE Department*

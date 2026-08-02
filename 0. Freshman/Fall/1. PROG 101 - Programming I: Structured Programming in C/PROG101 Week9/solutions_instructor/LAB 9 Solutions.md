# PROG 101 · Week 9
## LAB 9 Solutions — INSTRUCTOR ONLY

> **Every implementation below compiles under `gcc -Wall -Wextra -Werror -std=c11` and runs clean
> under `-fsanitize=address,undefined`.** Where the lab requires it, Valgrind output is quoted
> verbatim. Reject any submission that does not build warning-free — `-Werror` is not negotiable in
> this course.

---

## Part 1 — Recursion Tracing and Fundamentals

**1A — Trace tables.** Grade the per-call table, not the final value. Require the argument, the
pending operation, and the return value at each level.

**1B — Fix the Broken Recursion.** The recurring defects:

| Defect | Symptom | Fix |
|---|---|---|
| Base case tested with `==` when the parameter can overshoot | Infinite recursion → **SIGSEGV** | Use `<=` / `>=` |
| Missing base case entirely | SIGSEGV immediately | Add it |
| Recursive call does not shrink the problem | SIGSEGV | Ensure a strictly decreasing variant |
| Result not returned from the recursive call | Garbage or 0 | `return f(...)`, not bare `f(...)` |
| Accumulator initialised to the wrong identity | Wrong answer, no crash | 0 for sums, **1** for products |

**Why it is a segfault and not an error message:** each call pushes a stack frame; the stack is a
fixed ~8 MB region (`ulimit -s`); the next push past the guard page faults, and the kernel delivers
SIGSEGV. **Nothing counts depth** — the hardware notices, not the language. This is the concrete
difference from Python, whose interpreter raises `RecursionError` at 1000 frames.
`-fsanitize=address` turns the bare segfault into an explicit *stack-overflow* report.

---

## Part 2 — Sorting

Expected findings, matching CS 101 Lab 5:

- **Selection sort's comparison count is deterministic**: exactly n(n−1)/2, identical for sorted,
  reversed, and random input. Best case = worst case = Θ(n²).
- **Insertion sort is adaptive**: n−1 comparisons on already-sorted input, i.e. **Θ(n)**. This is
  why real library sorts use it for short and nearly-sorted runs.
- **Merge sort is Θ(n log n) in all cases** but needs Θ(n) extra space; quicksort sorts in place
  with Θ(log n) stack but degrades to Θ(n²) on sorted input with a naive last-element pivot.

`qsort` from `<stdlib.h>` is the baseline. Its comparator must **not subtract**:
`return (x > y) - (x < y)`, never `x - y`, which overflows for operands more than `INT_MAX` apart.
**A sorted-output test cannot catch this** — probe the comparator directly with `INT_MIN` and `1`;
the subtracting version returns `+2147483647` when the answer must be negative.

---

## Part 3 — `bst` Reference Implementation

**Valgrind-clean: 0 errors, all blocks freed.** Verified transcript:

```
tree from 50,30,70,20,40,60,80
  inorder:   20 30 40 50 60 70 80        <- sorted, the defining BST property
  preorder:  50 30 20 40 70 60 80
  postorder: 20 40 30 60 80 70 50
  height=2 size=7 sum=350 leaves=4 balanced=1 valid=1
  min=20 max=80  search(40)=found  search(99)=NULL

deletion, all three cases:
  del leaf 20:      30 40 50 60 70 80
  del one-child 30: 40 50 60 70 80
  del two-child 50: 40 60 70 80        (still a valid BST, size=4)
  del missing 999:  no-op

degenerate: ascending insert 1..7 -> height=6 (balanced would be 2), balanced=0
empty tree: height=-1 size=0 valid=1 find_min=NULL
```

### Deletion — the only hard function

```c
TreeNode *bst_delete(TreeNode *r, int v) {
    if (!r) return NULL;
    if      (v < r->value) r->left  = bst_delete(r->left,  v);
    else if (v > r->value) r->right = bst_delete(r->right, v);
    else {
        if (!r->left)  { TreeNode *t = r->right; free(r); return t; }   /* 0 or 1 child */
        if (!r->right) { TreeNode *t = r->left;  free(r); return t; }
        TreeNode *succ = bst_find_min(r->right);      /* in-order successor */
        r->value = succ->value;                       /* copy the VALUE up */
        r->right = bst_delete(r->right, succ->value); /* then delete it below */
    }
    return r;
}
```

Three cases: **leaf** (free and return NULL), **one child** (splice the child up), **two children**
(replace the value with the in-order successor — the minimum of the right subtree — then delete that
successor, which by construction has at most one child, so the recursion terminates).

The successor's value is *copied* and the node deleted recursively. Students who try to relink the
successor node directly usually corrupt the tree; the copy-then-delete form is both simpler and
correct.

### `bst_is_valid` must be a GLOBAL check

```c
static bool valid(const TreeNode *r, long lo, long hi) {
    if (!r) return true;
    if (r->value <= lo || r->value >= hi) return false;
    return valid(r->left, lo, r->value) && valid(r->right, r->value, hi);
}
bool bst_is_valid(const TreeNode *r) { return valid(r, LONG_MIN, LONG_MAX); }
```

**Checking each node against only its immediate children is wrong**, and the handout says so. The
counterexample, verified:

```
      10
     /  \
    5    20
     \
      15        <- 15 > 10 but sits in the LEFT subtree
```

Every node satisfies the local test; the tree is not a BST. The reference returns **0** for it.
Any student whose `bst_is_valid` returns true here has implemented the local check — this is the
single most valuable test case in the lab.

The bounds are `long` so that a node holding `INT_MIN` or `INT_MAX` does not falsely fail against
an `int` sentinel.

### `tree_free` must be POSTORDER

```c
void tree_free(TreeNode *r) {
    if (!r) return;
    tree_free(r->left);
    tree_free(r->right);
    free(r);                 /* node LAST */
}
```

Freeing the node first makes `r->left` a read of freed memory — the child pointers live *inside* the
node. Preorder is a use-after-free; inorder leaks half the tree *and* reads freed memory for the
other half. **Destroy children before parents**, always.

### Complexity

| Function | Balanced | Degenerate |
|---|---|---|
| `bst_search` / `insert` / `delete` | **Θ(log n)** | **Θ(n)** |
| `tree_height` / `size` / `sum` | Θ(n) time, Θ(log n) stack | Θ(n) time, **Θ(n) stack** |

The average-case Θ(log n) is taken over **random insertion orders**. Real data often arrives sorted
— from a database query, or sequential IDs — which is precisely the worst case, and nothing
probabilistic protects you. Self-balancing trees (AVL, red-black) exist for exactly this reason.

---

## Marking Scheme

Points follow the allocation printed on the handout. Within each part:

- **Correctness (≈50%).** Passes the required test cases *and* the edge cases listed above.
- **Memory discipline (≈30%).** No leaks, no invalid reads/writes, every `malloc` checked, every
  owner documented. For labs with a Valgrind requirement this is pass/fail: **0 errors, 0 leaks.**
- **Method (≈20%).** Required technique actually used, bounds asserted, `const` applied where the
  function only reads.

**Automatic deductions, regardless of output:**
- Any compiler warning under `-Wall -Wextra`.
- Unchecked `malloc`/`realloc` return.
- `realloc` result assigned directly back to the original pointer (leaks the block on failure).
- A buffer function that can leave its output unterminated.

**Carry-through.** One wrong helper used consistently downstream costs marks once.

---

*PROG 101 · Week 9 · Lab Solutions · Instructor Copy · © CSE Department*

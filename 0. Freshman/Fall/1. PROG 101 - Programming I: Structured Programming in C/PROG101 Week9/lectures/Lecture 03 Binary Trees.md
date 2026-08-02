# PROG 101 · Programming I: Structured Programming in C
## Week 9 · Lecture 3: Recursive Data Structures — Binary Trees

---

## Lecture Goals

By the end of this lecture you will:
- Understand a tree as a recursive data structure: a node plus two smaller trees
- Implement the three depth-first traversals: preorder, inorder, postorder
- Build and maintain a Binary Search Tree (BST): insert, search, delete
- Understand why BST operations are O(log n) on average but O(n) in the worst case
- Compute tree height and size recursively
- Free a tree's memory correctly with no leaks

---

## 1. A Tree Is a Recursive Definition

Just as a linked list node points to "the rest of the list" (itself a smaller linked list), a binary tree node points to two subtrees — each of which is itself a complete, smaller binary tree.

```
A binary tree is either:
  - empty (NULL), or
  - a node containing a value, a left subtree, and a right subtree
    (both of which are themselves binary trees)
```

This recursive definition is not just elegant notation — it is *exactly* why every tree algorithm is naturally written as a recursive function with the same shape:

```c
typedef struct TreeNode {
    int data;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;
```

```
        [50]
       /    \
    [30]    [70]
    /  \    /  \
 [20] [40][60] [80]
```

---

## 2. Creating Nodes

```c
TreeNode *node_create(int value) {
    TreeNode *node = malloc(sizeof(TreeNode));
    if (node == NULL) {
        fprintf(stderr, "malloc failed\n");
        exit(1);
    }
    node->data  = value;
    node->left  = NULL;
    node->right = NULL;
    return node;
}
```

---

## 3. Tree Traversals — Visiting Every Node

There are three natural orders to visit a binary tree's nodes, differing only in **when** you process the current node relative to recursing into its children. All three share the identical recursive structure — this is the pattern to internalize:

```c
/* PREORDER: process current node BEFORE its children */
void preorder(const TreeNode *root) {
    if (root == NULL) return;           /* base case: empty tree */
    printf("%d ", root->data);           /* visit current node FIRST */
    preorder(root->left);                /* then recurse left */
    preorder(root->right);               /* then recurse right */
}

/* INORDER: process current node BETWEEN its children */
void inorder(const TreeNode *root) {
    if (root == NULL) return;
    inorder(root->left);                 /* recurse left first */
    printf("%d ", root->data);           /* THEN visit current node */
    inorder(root->right);                /* then recurse right */
}

/* POSTORDER: process current node AFTER its children */
void postorder(const TreeNode *root) {
    if (root == NULL) return;
    postorder(root->left);               /* recurse left first */
    postorder(root->right);              /* then recurse right */
    printf("%d ", root->data);           /* visit current node LAST */
}
```

For the tree shown above:
```
Preorder:  50 30 20 40 70 60 80    (root, left subtree, right subtree)
Inorder:   20 30 40 50 60 70 80    (sorted order for a BST — see below!)
Postorder: 20 40 30 60 80 70 50    (children fully processed before parent)
```

**The critical insight:** for a **Binary Search Tree** specifically, inorder traversal always visits nodes in **sorted ascending order**. This is not a coincidence — it falls directly out of the BST ordering property (Section 4). This is one of the most useful facts about BSTs: sorting is "free" if your data is already organized as a BST.

### When to Use Each Traversal

- **Preorder:** copying/serializing a tree (you need the root's value before you can reconstruct its children); prefix expression notation
- **Inorder:** retrieving BST elements in sorted order
- **Postorder:** deleting a tree (you must free the children before the parent, or you'd lose your only reference to them); computing subtree-dependent values that need children's results first (e.g., subtree size, subtree height)

---

## 4. The Binary Search Tree (BST) Ordering Property

A BST adds an **invariant** on top of the general binary tree structure:

> For every node, **all values in its left subtree are less than the node's value**, and **all values in its right subtree are greater than the node's value**.

This invariant holds recursively at every single node, not just the root — this is what makes the recursive functions below correct.

### Search

```c
TreeNode *bst_search(TreeNode *root, int target) {
    if (root == NULL) return NULL;              /* base case: not found */
    if (target == root->data) return root;      /* base case: found it */
    if (target < root->data)
        return bst_search(root->left, target);   /* recurse left — smaller values live here */
    else
        return bst_search(root->right, target);  /* recurse right — larger values live here */
}
```

At each node, the ordering property lets you **eliminate an entire subtree** from consideration with a single comparison — exactly the same principle as binary search on a sorted array (Week 2), but on a tree structure instead of contiguous memory.

### Insertion

```c
TreeNode *bst_insert(TreeNode *root, int value) {
    if (root == NULL) return node_create(value);   /* base case: found the empty spot */

    if (value < root->data) {
        root->left = bst_insert(root->left, value);   /* insert into left subtree */
    } else if (value > root->data) {
        root->right = bst_insert(root->right, value); /* insert into right subtree */
    }
    /* if value == root->data: typically a no-op (no duplicates), or handle per your design */

    return root;   /* return the (possibly unchanged) subtree root, relinking as we unwind */
}
```

**Notice the pattern:** `root->left = bst_insert(root->left, value);` — this is the same "return the new head" idiom from Week 7's linked list insertion. The recursive call returns what the subtree's root *should be* after insertion, and the caller relinks it. This handles both cases uniformly: if `root->left` was `NULL`, it now becomes the newly created node; if it already existed, the subtree is unchanged and simply re-assigned to itself.

### Finding Minimum and Maximum

```c
/* The minimum value in a BST is always the leftmost node */
TreeNode *bst_find_min(TreeNode *root) {
    if (root == NULL) return NULL;
    while (root->left != NULL) {    /* iterative — no recursion needed here */
        root = root->left;
    }
    return root;
}

/* The maximum value is always the rightmost node */
TreeNode *bst_find_max(TreeNode *root) {
    if (root == NULL) return NULL;
    while (root->right != NULL) {
        root = root->right;
    }
    return root;
}
```

### Deletion — The Hardest BST Operation

Deletion has three cases, depending on how many children the node being deleted has:

```c
TreeNode *bst_delete(TreeNode *root, int value) {
    if (root == NULL) return NULL;              /* base case: value not found */

    if (value < root->data) {
        root->left = bst_delete(root->left, value);
    } else if (value > root->data) {
        root->right = bst_delete(root->right, value);
    } else {
        /* Found the node to delete — three cases: */

        /* Case 1: no children (leaf) */
        if (root->left == NULL && root->right == NULL) {
            free(root);
            return NULL;
        }

        /* Case 2: one child — replace this node with its only child */
        if (root->left == NULL) {
            TreeNode *temp = root->right;
            free(root);
            return temp;
        }
        if (root->right == NULL) {
            TreeNode *temp = root->left;
            free(root);
            return temp;
        }

        /* Case 3: two children — replace this node's VALUE with its
         * inorder successor (the smallest value in the right subtree),
         * then delete that successor node from the right subtree instead
         * (which is guaranteed to fall into Case 1 or Case 2, never Case 3
         * again, because the minimum of a subtree never has a left child) */
        TreeNode *successor = bst_find_min(root->right);
        root->data = successor->data;
        root->right = bst_delete(root->right, successor->data);
    }

    return root;
}
```

**Why the inorder successor?** It is the smallest value greater than the deleted node's value. Replacing the deleted node's value with it, then removing the (now-duplicated) successor from the right subtree, preserves the BST ordering property perfectly — everything in the left subtree is still smaller, everything remaining in the right subtree is still larger.

---

## 5. Computing Tree Properties Recursively

Every one of these follows the identical pattern: **base case for the empty tree, recursive case that combines results from both subtrees.**

```c
/* Height: the number of edges on the longest path from root to a leaf.
 * An empty tree has height -1; a single node has height 0. */
int tree_height(const TreeNode *root) {
    if (root == NULL) return -1;                 /* base case */
    int left_height  = tree_height(root->left);
    int right_height = tree_height(root->right);
    return 1 + (left_height > right_height ? left_height : right_height);
}

/* Size: total number of nodes */
int tree_size(const TreeNode *root) {
    if (root == NULL) return 0;                   /* base case */
    return 1 + tree_size(root->left) + tree_size(root->right);
}

/* Sum of all values */
int tree_sum(const TreeNode *root) {
    if (root == NULL) return 0;
    return root->data + tree_sum(root->left) + tree_sum(root->right);
}

/* Is this a valid BST? (Naive version — see the note below for a subtlety) */
int tree_max_value(const TreeNode *root) {
    if (root->right != NULL) return tree_max_value(root->right);
    return root->data;
}
int tree_min_value(const TreeNode *root) {
    if (root->left != NULL) return tree_min_value(root->left);
    return root->data;
}

/* Search for a value in ANY binary tree (not assuming BST ordering) */
int tree_contains(const TreeNode *root, int target) {
    if (root == NULL) return 0;
    if (root->data == target) return 1;
    return tree_contains(root->left, target) || tree_contains(root->right, target);
}
/* Note: this must check BOTH subtrees since there's no ordering to exploit —
 * O(n) in the worst case, unlike bst_search's O(log n) average case */
```

---

## 6. Freeing a Tree — Postorder Is Mandatory

You must free a node's children **before** freeing the node itself — otherwise you lose your only reference to them (a memory leak). This is precisely postorder traversal:

```c
void tree_free(TreeNode *root) {
    if (root == NULL) return;
    tree_free(root->left);     /* free left subtree first */
    tree_free(root->right);    /* free right subtree next */
    free(root);                 /* free THIS node LAST */
}
```

Getting the order wrong is a classic bug:
```c
/* WRONG: frees root, then tries to access root->left — use-after-free */
void tree_free_broken(TreeNode *root) {
    if (root == NULL) return;
    free(root);
    tree_free_broken(root->left);    /* root was just freed! */
    tree_free_broken(root->right);
}
```

---

## 7. Complexity: Why "Average O(log n)" but "Worst Case O(n)"

For a **balanced** BST (roughly equal numbers of nodes in every left/right subtree at each level), the height is O(log n), and since search/insert/delete all walk a single root-to-leaf path, they cost O(log n).

But nothing in the `bst_insert` code above **guarantees** balance. If you insert values in already-sorted order (`1, 2, 3, 4, 5, ...`), every new node becomes the right child of the previous one — the tree degenerates into what is structurally a linked list:

```
Balanced (height = O(log n)):        Degenerate (height = O(n)):
        [4]                          [1]
       /   \                            \
     [2]   [6]                          [2]
    /  \   /  \                            \
  [1] [3][5]  [7]                          [3]
                                               \
                                               [4]
7 nodes, height 2                             ...
                                        7 nodes, height 6
```

In the degenerate case, every operation degrades to O(n) — no better than a linked list. This is exactly why **self-balancing trees** (AVL trees, Red-Black trees — covered in your data structures course) exist: they perform additional rotation operations during insertion/deletion specifically to guarantee height stays O(log n) regardless of insertion order.

**For this course:** understand and implement the plain (unbalanced) BST correctly. Recognizing its worst-case vulnerability is itself an important engineering insight — you now know *why* production systems use balanced variants when insertion order isn't controlled.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Insert 50, 30, 70, 20, 40, 60, 80 into an empty BST in that order. Draw the tree, give the inorder traversal, and give the height. Then insert 1..7 in ascending order into a fresh tree and give that height.

**2. (Explain.)** Explain why freeing a tree must be done in **postorder**, and what goes wrong with preorder or inorder.

**3. (Build.)** Write recursive functions for tree height, node count, and a BST search. Give the complexity of each in the balanced and degenerate cases.

**4. (Stretch.)** A BST gives "average O(log n), worst case O(n)". Explain precisely what the average is taken over, and why that makes the guarantee weaker than it sounds.


### Answers

**1.**

```
            50
          /    \
        30      70
       /  \    /  \
     20   40  60   80
```

**Inorder:** `20 30 40 50 60 70 80` — sorted, which is the defining property of a BST. Inorder traversal of any BST yields its elements in ascending order, which is why building a BST and walking it is a sort.

**Height: 3** (counting nodes on the longest root-to-leaf path). This tree is perfectly balanced, so lookup costs at most 3 comparisons for 7 elements — ⌈log₂ 8⌉.

Inserting 1..7 **in ascending order** gives **height 7**: every value is larger than the current node, so each goes right and the tree degenerates into a right-leaning linked list.

That is the essential warning about plain BSTs. The O(log n) figure is the **average over random insertion orders**; sorted input — which is extremely common in practice, since data often arrives already ordered — produces the O(n) worst case. There is nothing probabilistic protecting you.

Self-balancing variants (AVL, red-black) restructure on insertion to keep the height Θ(log n) unconditionally, and every serious ordered-map implementation uses one. CS 220 covers them; here the point is to understand precisely what plain BSTs do and do not guarantee.

**2.**

```c
void free_tree(struct T *t) {
    if (!t) return;
    free_tree(t->left);    /* children first */
    free_tree(t->right);
    free(t);               /* then the node */
}
```

Postorder is the only order in which **a node is freed after everything reachable through it**. The child pointers live *inside* the node, so freeing the node first destroys the only route to its subtrees.

**Preorder** — `free(t)` then `free_tree(t->left)` — reads `t->left` from **freed memory**. That is a use-after-free, undefined behaviour, and it often appears to work because `free` does not erase the bytes; the pointers usually survive until the allocator reuses the block. Under ASan it aborts immediately with *heap-use-after-free*.

**Inorder** — `free_tree(t->left); free(t); free_tree(t->right);` — is wrong for the same reason, just half as often: the left subtree is freed correctly, then `t` is freed, then `t->right` is read from freed memory. Half the tree is leaked and half is a use-after-free, which is a particularly nasty combination to diagnose.

The rule generalises well beyond trees: **destroy in reverse dependency order, children before parents.** It is the same reason a linked-list free loop must save `next` before calling `free`, and the reason destructors in other languages run bottom-up. If you must free the node first, copy the child pointers into locals beforehand — which is exactly what postorder does implicitly.

**3.**

```c
int height(const struct T *t) {
    if (!t) return 0;
    int l = height(t->left), r = height(t->right);
    return 1 + (l > r ? l : r);
}

int count(const struct T *t) {
    return t ? 1 + count(t->left) + count(t->right) : 0;
}

const struct T *search(const struct T *t, int v) {
    if (!t || t->v == v) return t;
    return v < t->v ? search(t->left, v) : search(t->right, v);
}
```

| Function | Balanced | Degenerate |
|---|---|---|
| `height` | **Θ(n)** time, Θ(log n) stack | Θ(n) time, **Θ(n) stack** |
| `count` | **Θ(n)** time, Θ(log n) stack | Θ(n) time, Θ(n) stack |
| `search` | **Θ(log n)** | **Θ(n)** |

The key distinction: `height` and `count` must visit **every node**, so they are Θ(n) regardless of shape — balance affects only their *stack depth*. `search` discards half the remaining tree at each step, so its cost is the **height**, which is where balance decides everything.

All three follow the same recursive shape as the tree's own definition — base case for the empty tree, combine the results of the two subtrees. That correspondence is why recursion is the natural idiom here and why an iterative version needs an explicit stack.

The stack column is a real constraint: a degenerate tree of a million nodes overflows an 8 MB stack in `height`, while `search` on the same tree is merely slow. `search` is also easily made iterative, since its recursion is in tail position.

**4.** The average is taken over **all n! insertion orders, assumed equally likely**. Under that assumption the expected height of a randomly built BST is about 4.31·ln n ≈ 3·log₂ n — logarithmic, with a modest constant. The result is a theorem about a *distribution of inputs*, not about the data structure.

That is exactly what makes it weak. **Real insertion orders are not uniformly random.** Data arrives sorted from a database query, timestamps arrive in increasing order, IDs are assigned sequentially — and every one of those is a worst case, producing a linked list with Θ(n) lookups. The most common real input is the one the average explicitly does not cover.

Compare quicksort, where the same average-case reasoning applies but can be **rescued by randomising the pivot**: the algorithm makes its own random choices, so the guarantee holds for every input rather than for most inputs. A plain BST has no such lever — its shape is dictated entirely by the caller's insertion order, which you do not control. (Randomised BSTs and treaps restore it by giving each node a random priority.)

The engineering conclusion: use a **self-balancing** tree — AVL, red-black, B-tree — whenever the insertion order is not under your control. They pay a constant factor on insertion for rotations and buy Θ(log n) **worst case**, unconditionally.

The general lesson recurs throughout the course: an average-case bound assumes an input distribution, and you should always ask what it is and whether your inputs obey it. When an adversary chooses the input — the Hashtables appendix's hash-flooding attack — the answer is always no.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Binary tree** | Recursive structure: a node with a value and two subtrees (left, right) |
| **Binary Search Tree (BST)** | A binary tree with the ordering invariant: left < node < right, recursively |
| **Preorder / Inorder / Postorder** | The three depth-first traversal orders, differing in when the current node is visited |
| **Inorder successor** | The smallest value greater than a given node's value (used in BST deletion) |
| **Tree height** | Length of the longest root-to-leaf path (edges) |
| **Balanced tree** | A tree whose height is O(log n) relative to its node count |
| **Degenerate tree** | A tree that has devolved into a linked-list-like shape, height O(n) |

---

## Reading

- **King Ch. 18** — Recursion (tree recursion sections)
- **CLRS Ch. 12** — Binary Search Trees (the full formal treatment, including deletion proof)
- **Sedgewick & Wayne, Algorithms 4th ed.** — Ch. 3.2 (Binary Search Trees) — excellent visualizations

---

*Next: Lab 9 — Implementing Merge Sort, Backtracking, and a Complete BST*

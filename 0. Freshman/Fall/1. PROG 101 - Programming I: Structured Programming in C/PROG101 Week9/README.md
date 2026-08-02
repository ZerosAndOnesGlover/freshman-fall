# PROG 101 — Week 9: Recursion, Divide-and-Conquer, and Binary Trees
## Mathematical Induction in Code · Sorting · Recursive Data Structures

---

## Week Overview

Week 9 introduces recursion as a fundamental problem-solving tool — not a curiosity, but the natural expression of any problem defined in terms of smaller instances of itself. You will implement two of the most important sorting algorithms in computer science (merge sort, quicksort), master the choose/explore/unchoose backtracking template that solves an enormous class of combinatorial problems, and build your second real data structure: the Binary Search Tree, whose every operation is a direct application of the recursive thinking developed in this week.

---

## Schedule

| Day | Event | Topic | Duration |
|-----|-------|-------|----------|
| Tuesday | Lecture 1 | Recursion Fundamentals | 50 min |
| Wednesday | Lecture 2 | Divide-and-Conquer and Backtracking | 50 min |
| Thursday | Lecture 3 | Recursive Data Structures: Binary Trees | 50 min |
| Monday | **Lab 9** | Recursion + Sorting + Complete BST Library | 2 hours |

---

## Files in This Package

```
PROG101_Week6/
├── README.md
├── lectures/
│   ├── Lecture 01 Recursion Fundamentals.md         ← Base/recursive case, tracing, recursion vs iteration, tail recursion
│   ├── Lecture 02 Divide Conquer Backtracking.md     ← Merge sort, quicksort, choose/explore/unchoose, N-Queens
│   └── Lecture 03 Binary Trees.md                    ← Tree recursion, traversals, BST insert/search/delete, balance
├── lab/
│   └── LAB 9 Recursion Sorting BST.md                 ← Trace tables + sorting comparison + complete BST library
├── assignments/
│   └── Problem Set 9.md                              ← 5 problems: fast power/recursion basics, merge sort variants, quicksort engineering, backtracking, BST applications
├── quizzes/
│   └── QUIZ 6.md                                     ← 10 questions + full answer key
└── resources/
    └── Week 9 Recursion Tree Reference.md             ← Design checklist, pattern library, BST reference, complexity cheat sheet, common bugs
```

---

## Learning Objectives

After Week 9, you will be able to:

- [ ] Identify the base case and recursive case of any recursive function
- [ ] Trace recursive function calls precisely using a call-stack mental model
- [ ] Explain why unterminated or too-deep recursion causes stack overflow
- [ ] Convert between recursive and iterative implementations
- [ ] Explain tail recursion and why C doesn't guarantee tail call optimization
- [ ] Implement merge sort and analyze its O(n log n) complexity via the recursion tree
- [ ] Implement quicksort, including pivot selection strategies that avoid worst-case behavior
- [ ] Apply the choose/explore/unchoose backtracking template to permutations, subsets, and constraint-satisfaction problems
- [ ] Implement a complete Binary Search Tree: insert, search, delete (all three cases), traversals
- [ ] Explain why BST operations are O(log n) average case but O(n) worst case
- [ ] Correctly free a tree's memory using postorder traversal

---

## Textbook Reading

| Lecture | Reference |
|---------|-----------|
| L1: Recursion Fundamentals | King Ch. 18 (full chapter); SICP §1.2 |
| L2: Divide-and-Conquer/Backtracking | CLRS Ch. 2, Ch. 7; Skiena Ch. 7 |
| L3: Binary Trees | CLRS Ch. 12; Sedgewick & Wayne §3.2 |

---

## The Key Insights of This Week

### On Recursion
A recursive function is mathematical induction, executed. The base case is your induction's base; the recursive case is your inductive step. If you can write the mathematical induction proof for why an algorithm is correct, you can write the recursive function — they have exactly the same shape.

### On Divide-and-Conquer
Merge sort's O(n log n) complexity isn't magic — it falls directly out of counting the recursion tree's structure: O(log n) levels, each doing O(n) total work. Once you can read a recursion tree this way, you can derive the complexity of any divide-and-conquer algorithm yourself, rather than memorizing results.

### On Backtracking
Every backtracking algorithm — permutations, N-Queens, subset sum, maze solving — is the identical three-step template: choose, explore, unchoose. The "unchoose" step is not optional cleanup; it is what makes the algorithm correctly explore every branch of the possibility tree rather than corrupting later branches with earlier choices.

### On Binary Search Trees
A tree is a recursive data structure precisely because a subtree is itself a complete, smaller tree. This is why every tree function has the same shape: handle `NULL` (the base case), then combine the results of recursing into `left` and `right`. Once this clicks, tree algorithms stop looking like special cases and start looking like the same three lines of code, rearranged.

---

## Common Week 9 Mistakes

**Recursion with no base case, or an unreachable one:**
```c
int bad(int n) { return n * bad(n - 1); }              /* no base case */
int bad2(int n) { if (n==0) return 1; return n*bad2(n-2); }  /* skips 0 for odd n */
```

**Discarding a recursive call's return value:**
```c
int sum(int n) {
    if (n <= 0) return 0;
    sum(n - 1);        /* BUG: result thrown away */
    return n;
}
```

**Forgetting to relink after BST insert/delete:**
```c
void insert(TreeNode *root, int v) {        /* returns void — loses new nodes */
    if (v < root->data) insert(root->left, v);
}
/* FIX: return TreeNode* and do root->left = bst_insert(root->left, v); */
```

**Freeing a tree in preorder instead of postorder:**
```c
void bad_free(TreeNode *r) {
    if (!r) return;
    free(r);
    bad_free(r->left);   /* use-after-free */
}
```

**Forgetting the "unchoose" step in backtracking:**
```c
swap(&arr[start], &arr[i]);
backtrack(arr, n, start + 1);
/* missing: swap back — array stays scrambled for the next loop iteration */
```

**Checking only local parent-child ordering for BST validity, missing the transitive property:**
```c
/* Only checks immediate children — misses violations further down the tree */
if (root->left->data < root->data && root->right->data > root->data) ...
/* Correct approach: pass down a narrowing (min, max) range */
```

---

## Challenge Problems (Optional)

1. **Iterative traversals** — implement `inorder`, `preorder`, and `postorder` **without recursion**, using an explicit stack (array + top index) that you manage yourself. This reveals exactly what the call stack was doing for you all along.

2. **AVL tree rotations** — implement single and double rotations (left, right, left-right, right-left) and use them to keep a BST height-balanced after every insertion. Verify with `tree_is_balanced` from Lab 9 that the tree never degenerates, even under sorted-order insertion.

3. **Expression tree evaluator** — build a binary tree representing an arithmetic expression (operators as internal nodes, operands as leaves) from a prefix or postfix token sequence, then evaluate it recursively.

4. **The Tower of Hanoi** — implement the classic recursive solution, print the sequence of moves, and prove (by counting) that it requires exactly `2ⁿ - 1` moves for `n` disks. Then explain, using the recursion tree, why this count is unavoidable.

# PROG 101 · Programming I: Structured Programming in C
## Week 9 · Lab 9: Recursion, Sorting, and Binary Search Trees

**Graded: 20 points**
**Duration:** 2 hours
**Date:** Monday 30 November 2026 · 15:00–16:50 · Lab Section (Week 10) — covers Week 9 (Lectures 01–03)
**Submission:** Push to Git, show TA before leaving

---

## Overview

- **Part 1:** Recursion tracing and fundamentals
- **Part 2:** Merge sort and quicksort implementation with performance comparison
- **Part 3:** A complete Binary Search Tree library (the main deliverable)

---

## Part 1: Recursion Tracing and Fundamentals (5 pts)

### 1A: Trace Tables (2 pts)

Create `recursion_trace.c`. For each function, build a complete trace table (like Lecture 1's example) **by hand** in `LAB 9 Recursion Sorting BST.md` before running the code. Then verify.

```c
int mystery1(int n) {
    if (n <= 0) return 0;
    return n + mystery1(n - 1);
}
/* Trace mystery1(5) — what does it compute in general? */

int mystery2(int a, int b) {
    if (b == 0) return a;
    return mystery2(b, a % b);
}
/* Trace mystery2(48, 18) — what famous algorithm is this? */

int mystery3(int n) {
    if (n == 0) return 1;
    return 2 * mystery3(n - 1);
}
/* Trace mystery3(6) — what does it compute in general? */
```

In `LAB 9 Recursion Sorting BST.md`: full trace table for each, plus a one-sentence description of what each function computes in general (not just for the specific input).

### 1B: Fix the Broken Recursion (3 pts)

Create `fix_recursion.c`. Each function below has a bug related to base case or problem-shrinking. Identify the bug, explain it, and fix it.

```c
/* BUG A: what happens for negative input? */
long factorial_buggy(int n) {
    if (n == 0) return 1;
    return n * factorial_buggy(n - 1);
}

/* BUG B: infinite recursion for some inputs */
int count_down_buggy(int n) {
    if (n == 0) return 0;
    printf("%d\n", n);
    return 1 + count_down_buggy(n - 2);
}

/* BUG C: doesn't accumulate the result correctly */
int sum_to_n_buggy(int n) {
    if (n <= 0) return 0;
    sum_to_n_buggy(n - 1) + n;   /* result never returned! */
    return 0;
}
```

For each: write the bug type, a test input that demonstrates the failure, and the corrected function.

---

## Part 2: Sorting Algorithms (5 pts)

Create `sorting_algorithms.c` implementing:

```c
void merge_sort(int arr[], int n);
void quicksort(int arr[], int n);
void quicksort_randomized(int arr[], int n);   /* random pivot selection */

/* Instrumentation: count comparisons made during sorting.
 * Reset the counter before each sort call. */
extern long comparison_count;

/* A helper to verify correctness */
int is_sorted(const int arr[], int n);
```

### Performance Comparison

Write a `main()` that:
1. Generates arrays of size 100, 1000, 10000 with **random** values
2. Generates arrays of the same sizes that are **already sorted** (worst case for naive quicksort)
3. For each array, runs `merge_sort`, `quicksort`, and `quicksort_randomized`, resetting and recording `comparison_count` for each
4. Verifies every result with `is_sorted`
5. Prints a table:

```
=== Comparison Counts ===
Size    | Merge Sort | Quicksort | Quicksort (randomized)
--------|------------|-----------|------------------------
Random 100     |   ...      |   ...     |   ...
Random 1000    |   ...      |   ...     |   ...
Random 10000   |   ...      |   ...     |   ...
Sorted 100     |   ...      |   ...     |   ...
Sorted 1000    |   ...      |   ...     |   ...
Sorted 10000   |   ...      |   ...     |   ...
```

In `LAB 9 Recursion Sorting BST.md`, answer:
1. For sorted input, how does naive quicksort's comparison count compare to merge sort's? Does this match the O(n²) vs O(n log n) prediction?
2. Does randomized pivot selection fix the sorted-input problem? Why?
3. For random input, how do all three algorithms compare?

---

## Part 3: Binary Search Tree Library (10 pts)

Build a complete, memory-safe BST library.

### `bst.h`

```c
#ifndef BST_H
#define BST_H

#include <stdbool.h>

typedef struct TreeNode {
    int data;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

/* === Construction === */
TreeNode *node_create(int value);

/* === Core BST operations (all return the possibly-new subtree root) === */
TreeNode *bst_insert(TreeNode *root, int value);
TreeNode *bst_delete(TreeNode *root, int value);
TreeNode *bst_search(TreeNode *root, int value);   /* returns node ptr or NULL */

/* === Traversals (print space-separated values) === */
void bst_print_preorder(const TreeNode *root);
void bst_print_inorder(const TreeNode *root);
void bst_print_postorder(const TreeNode *root);

/* === Traversal into an array (for testing / further processing) === */
/* Fills out_arr with the inorder traversal. Returns the count written.
 * Caller must provide out_arr with sufficient capacity (>= tree_size). */
int  bst_inorder_to_array(const TreeNode *root, int out_arr[], int max_size);

/* === Properties === */
int  tree_height(const TreeNode *root);     /* empty tree = -1 */
int  tree_size(const TreeNode *root);
int  tree_sum(const TreeNode *root);
bool tree_contains(const TreeNode *root, int value);   /* works on ANY binary tree */

/* === BST-specific queries === */
TreeNode *bst_find_min(TreeNode *root);
TreeNode *bst_find_max(TreeNode *root);

/* Validate the BST ordering property holds for the ENTIRE tree
 * (not just each node vs its immediate children — the ordering must
 * hold transitively: every node in a left subtree must be less than
 * ALL ancestors it is a left-descendant of, not just its direct parent). */
bool bst_is_valid(const TreeNode *root);

/* Return true if the tree is height-balanced: for every node, the
 * height difference between left and right subtrees is at most 1. */
bool tree_is_balanced(const TreeNode *root);

/* Return the number of leaf nodes (nodes with no children). */
int  tree_count_leaves(const TreeNode *root);

/* === Cleanup === */
void tree_free(TreeNode *root);   /* must use postorder internally */

#endif
```

### Implementation Notes

**`bst_is_valid` — the subtle part.** A naive check ("is `left->data < root->data` and `right->data > root->data`?") is **insufficient** — it only checks immediate children, not the full transitive ordering. Consider:

```
        [10]
       /    \
    [5]     [15]
       \
       [20]     ← 20 is in the LEFT subtree of 10, but 20 > 10!
```

Here, `5 < 10` and `20 > 5` locally look fine at each parent-child pair, but `20` violates the BST property relative to the root `10` (it's in the left subtree but greater than the root). The correct approach passes down a valid `(min, max)` range that narrows at each level:

```c
bool bst_is_valid_helper(const TreeNode *root, int min, int max) {
    if (root == NULL) return true;
    if (root->data <= min || root->data >= max) return false;
    return bst_is_valid_helper(root->left,  min, root->data) &&
           bst_is_valid_helper(root->right, root->data, max);
}
/* Call with wide initial bounds, e.g. INT_MIN and INT_MAX,
 * or handle the boundary carefully with long/appropriate sentinel values */
```

Implement `bst_is_valid` using this range-based technique (adapt the sentinel handling as needed — think carefully about what happens at `INT_MIN`/`INT_MAX` boundaries).

### `test_bst.c`

Write comprehensive tests covering:

```c
void test_insert_and_search(void) {
    /* Build a tree by inserting: 50, 30, 70, 20, 40, 60, 80
     * Verify bst_search finds every inserted value
     * Verify bst_search returns NULL for values not inserted
     */
}

void test_traversals(void) {
    /* Using the same tree, verify:
     *   - inorder traversal produces sorted output (use bst_inorder_to_array)
     *   - preorder starts with the root
     *   - postorder ends with the root
     */
}

void test_deletion_all_cases(void) {
    /* Test deleting:
     *   - a leaf node
     *   - a node with only a left child
     *   - a node with only a right child
     *   - a node with two children (verify inorder successor logic)
     *   - the root itself (in each of the above configurations)
     *   - a value not in the tree (no-op, tree unchanged)
     * After each deletion, verify bst_is_valid still holds and
     * bst_search confirms the deleted value is gone.
     */
}

void test_properties(void) {
    /* Verify tree_height, tree_size, tree_sum, tree_count_leaves
     * against hand-computed expected values for a specific known tree.
     */
}

void test_balance_detection(void) {
    /* Build a balanced tree — verify tree_is_balanced returns true.
     * Build a degenerate (linked-list-like) tree by inserting sorted
     * values 1,2,3,4,5,6,7 — verify tree_is_balanced returns false.
     */
}

void test_validity_edge_case(void) {
    /* Manually construct (using node_create and direct pointer assignment,
     * NOT bst_insert) the exact "invalid BST" example from the lecture notes
     * (the one where a naive local check would incorrectly pass).
     * Verify bst_is_valid correctly returns false for it.
     */
}
```

### Valgrind Requirement

```bash
valgrind --leak-check=full ./test_bst
```

Zero errors, zero leaks. Every tree built during testing must be `tree_free`d.

---

## Deliverables

```
week6/lab6/
├── recursion_trace.c
├── fix_recursion.c
├── sorting_algorithms.c
├── bst.h
├── bst.c
├── test_bst.c
├── Makefile
└── LAB 9 Recursion Sorting BST.md
```

**Makefile:**
```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

all: recursion_trace fix_recursion sorting_algorithms test_bst

test_bst: test_bst.o bst.o
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f recursion_trace fix_recursion sorting_algorithms test_bst *.o

.PHONY: all clean
```

---

## Grading

| Part | Points | Criteria |
|------|--------|---------|
| 1A: Trace tables | 2 | Complete, accurate, correct general description |
| 1B: Fix broken recursion | 3 | Correct bug diagnosis and fixes |
| 2: Sorting implementations | 3 | Merge sort, quicksort, randomized quicksort all correct |
| 2: Performance analysis | 2 | Correct table, correct interpretation |
| 3: BST implementation | 6 | All operations correct including subtle `bst_is_valid` |
| 3: Test suite | 3 | Comprehensive, especially deletion cases and validity edge case |
| 3: Valgrind clean | 1 | 0 errors, 0 leaks |
| **Total** | **20** | |

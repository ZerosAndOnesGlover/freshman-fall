# PROG 101 · Problem Set 9 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

*(Revised 2026-09-26: old Problem 3 (quicksort — Lab 9 does it), `is_palindrome_advanced`, `print_divisors_recursive`,
the standard `merge_sort` (reused from Lab 9) and N-Queens are no longer asked. Old 4 → 3 (20), old 5 → 4 (25), P2 30.)*

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading table above (100 points).
> No errata found — the rubric's "exactly 92 for n=8" was verified independently.
> Compile/verify with `gcc 13.3.0 -Wall -Wextra -Werror -g -std=c11`; heap claims under valgrind.

---

### Problem 1 — Recursive Fundamentals (25 pts)

*`fast_power` must be O(log n) — the rubric says so explicitly. The test is structural, not empirical: it must recurse on `n/2` (squaring the half-result), not on `n-1`.*

```c
long fast_power(long b, int n) {
    if (n == 0) return 1;
    if (n % 2 == 0) { long h = fast_power(b, n / 2); return h * h; }   /* ONE call */
    return b * fast_power(b, n - 1);
}
```

*The classic defect: `return fast_power(b, n/2) * fast_power(b, n/2);` — two separate recursive calls. That is **O(n)**, not O(log n), because the work doubles at each level and cancels the halving exactly. It produces correct answers, so it only fails the complexity requirement — instrument a call counter to catch it: correct is ~log₂n calls, broken is ~n.*
*Every recursive function needs base case, progress, and self-call (cross-reference CS 101 PS 4 A1). Probe `n = 0` and `n = 1` on each.*

### Problem 2 — Merge Sort Variants (25 pts)

*Inversion counting: the whole trick is `inv += (mid - i)` when taking an element from the **right** half — every remaining element of the left half forms an inversion with it, counted in O(1) rather than one at a time. A nested-loop count inside merge is still O(n²) and defeats the exercise. *
*String version: the array holds `char *`; the merge compares with `strcmp` and moves only the pointers. (The generic `void *` version was removed 2026-09-21 — it is Week 11.)*
*Merge sort must be **stable**: when `cmp(...) == 0`, take from the **left** half (`<=`, not `<`). Test with records carrying a payload — sorting `{(1,'a'),(1,'b')}` must preserve that order. A strict `<` silently loses stability and is the most common defect here.*
*Every allocation in the merge buffer must be freed; valgrind-clean.*

### Problem 3 — Quicksort Engineering (20 pts)

*The hybrid (quicksort + insertion sort below a cutoff, typically 8–16) must sort correctly; its comparison count is usually a little lower than plain Lomuto on random input. Grade the table and the explanation, not the size of the win.*
*Already-sorted input is the adversarial case for a fixed pivot: median-of-three or a random pivot is required to avoid O(n²). Benchmark on `0..n-1` ascending to demonstrate it.*

### Problem 4 — Backtracking (15 pts)

**N-Queens — verified solution counts** (matches OEIS A000170; use as the acceptance test):

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | **8** | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| solutions | 1 | 0 | 0 | 2 | 10 | 4 | 40 | **92** | 352 | 724 |

*The rubric's "exactly 92 for n=8" is correct. The `n=2` and `n=3` zeros are good regression tests — a buggy diagonal check often reports spurious solutions there.*

```c
static int safe(int r, int c) {
    for (int i = 0; i < r; i++) {
        if (col[i] == c) return 0;                 /* same column */
        if (i - col[i] == r - c) return 0;         /* same ↘ diagonal */
        if (i + col[i] == r + c) return 0;         /* same ↙ diagonal */
    }
    return 1;
}
```

*Both diagonal tests are required — checking only one yields far too many solutions (and n=8 will not give 92). The one-array-of-columns representation implicitly enforces one queen per row, which is why no row check is needed; a student using a full 2-D board is also fine but does more work.*


### Problem 5 — BST Applications (15 pts)

Reference (compiled with `-Wall -Wextra -Werror -pedantic -std=c11` and run under Valgrind, clean):

```c
/* bst_apps.c — PS 9 Problem 5 (reference), on Lecture 03's TreeNode */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct TreeNode {
    int data;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

TreeNode *node_create(int value) {
    TreeNode *node = malloc(sizeof(TreeNode));
    if (!node) exit(1);
    node->data = value;
    node->left = node->right = NULL;
    return node;
}

TreeNode *bst_insert(TreeNode *root, int value) {
    if (root == NULL) return node_create(value);
    if (value < root->data) root->left = bst_insert(root->left, value);
    else if (value > root->data) root->right = bst_insert(root->right, value);
    return root;
}

void bst_free(TreeNode *root) {
    if (root == NULL) return;
    bst_free(root->left);
    bst_free(root->right);
    free(root);
}

/* kth smallest (k = 1 is the minimum): an inorder walk that stops once k nodes are counted.
   *count is how many nodes the walk has passed so far. Returns -1 if k is out of range. */
static int kth_walk(const TreeNode *root, int k, int *count) {
    if (root == NULL) return -1;
    int left = kth_walk(root->left, k, count);
    if (left != -1) return left;
    (*count)++;
    if (*count == k) return root->data;
    return kth_walk(root->right, k, count);
}

int bst_kth_smallest(const TreeNode *root, int k) {
    int count = 0;
    return kth_walk(root, k, &count);
}

/* Print values in [low, high] in order, skipping subtrees that cannot hold any. *visits counts nodes touched. */
void bst_print_range(const TreeNode *root, int low, int high, int *visits) {
    if (root == NULL) return;
    (*visits)++;
    if (root->data > low) bst_print_range(root->left, low, high, visits);
    if (root->data >= low && root->data <= high) printf("%d ", root->data);
    if (root->data < high) bst_print_range(root->right, low, high, visits);
}

/* Fill out[] with the inorder values; returns how many were written. */
static int to_array(const TreeNode *root, int out[], int n) {
    if (root == NULL) return n;
    n = to_array(root->left, out, n);
    out[n++] = root->data;
    return to_array(root->right, out, n);
}

bool bst_same_values(const TreeNode *a, const TreeNode *b) {
    int xa[1024], xb[1024];
    int na = to_array(a, xa, 0), nb = to_array(b, xb, 0);
    if (na != nb) return false;
    for (int i = 0; i < na; i++) if (xa[i] != xb[i]) return false;
    return true;
}

int main(void) {
    int vals[] = {50, 30, 70, 20, 40, 60, 80, 35, 45, 65};
    TreeNode *t = NULL;
    for (int i = 0; i < 10; i++) t = bst_insert(t, vals[i]);
    printf("k=1 %d, k=4 %d, k=10 %d, k=11 %d\n", bst_kth_smallest(t, 1), bst_kth_smallest(t, 4),
           bst_kth_smallest(t, 10), bst_kth_smallest(t, 11));
    int visits = 0;
    printf("range [33, 47]: ");
    bst_print_range(t, 33, 47, &visits);
    printf("(visited %d of 10)\n", visits);
    TreeNode *u = NULL;
    int other[] = {20, 35, 45, 30, 40, 80, 65, 60, 70, 50};
    for (int i = 0; i < 10; i++) u = bst_insert(u, other[i]);
    TreeNode *w = bst_insert(NULL, 1);
    printf("same(t, u) = %d, same(t, w) = %d\n", bst_same_values(t, u), bst_same_values(t, w));
    bst_free(t); bst_free(u); bst_free(w);
    return 0;
}
```

Output:

```
k=1 20, k=4 40, k=10 80, k=11 -1
range [33, 47]: 35 40 45 (visited 5 of 10)
same(t, u) = 1, same(t, w) = 0
```

*Range pruning is the item that separates marks: the visit count must be below the tree size (5 of 10 here).
A full inorder walk that filters afterwards prints the right values but visits all 10 and earns no credit for
pruning. All trees must be freed post-order; freeing a node before its children is a use-after-free.*
*(Revised 2026-09-21: LCA, sorted-array-to-balanced-BST and BST merge were removed — they are taught
nowhere in the course.)*

---

*PROG 101 · Week 9 · Problem Set 9 · © CSE Department*

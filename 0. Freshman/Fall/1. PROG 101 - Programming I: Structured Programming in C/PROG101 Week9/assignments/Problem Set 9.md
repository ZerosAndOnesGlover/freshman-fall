# PROG 101 · Programming I: Structured Programming in C
## Week 9 · Problem Set 9

**Released:** Thursday 26 November 2026, 11:00 (after Week 9 Lecture 3)
**Due:** Tuesday 1 December 2026, 10:00 (start of Week 10 Lecture 1) — late penalty from 10:01
**Directory:** `"$PROG101/week9/ps9"` in the Freshman Fall repo
**Total:** 100 points · **Expected time:** about 5 hours

**What this uses:** Weeks 0–9 — this week's recursion and memoisation (Lecture 01), merge sort, Lomuto
quicksort and backtracking (Lecture 02), and the binary search tree with its traversals (Lecture 03).
**Not needed:** `void *` generics and comparator function pointers (Week 11), Hoare partitioning, and
BST algorithms the lectures do not teach (lowest common ancestor, balanced construction, tree merging).

---

## Problem 1: Recursive Fundamentals (25 pts)

Create `recursive_basics.c`. Implement each function **recursively** (no loops allowed, except where explicitly noted).

```c
/* Return x raised to the power n (n >= 0), using recursion.
 * Must run in O(log n) time using the "fast power" technique:
 *   x^n = (x^(n/2))^2         if n is even
 *   x^n = x * (x^((n-1)/2))^2  if n is odd
 * (NOT the naive O(n) repeated multiplication.) */
long fast_power(long x, int n);

/* Return the greatest common divisor of a and b (Euclidean algorithm). */
long gcd_recursive(long a, long b);

/* Return 1 if s is a palindrome ignoring case and non-alphanumeric
 * characters (e.g., "A man, a plan, a canal: Panama" is a palindrome).
 * Use two-index recursion (left/right converging), skipping non-alphanumeric
 * characters within the recursive step itself — not a separate cleanup pass. */
int is_palindrome_advanced(const char *s);

/* Count the number of times digit 'd' appears in the decimal representation
 * of a non-negative integer n. */
int count_digit_occurrences(int n, int d);

/* Return the number of distinct ways to climb n stairs, taking either
 * 1 or 2 steps at a time. (This is the Fibonacci recurrence in disguise —
 * recognize it.) Use memoization — a naive version will be far too slow
 * for n=40 and above. */
long climb_stairs(int n);

/* Print all the divisors of n (n > 0) in ascending order, using recursion
 * to check divisor candidates from 1 up to n. (Simple linear recursion,
 * O(n) — the point here is correct recursive structure, not asymptotic
 * optimality.) */
void print_divisors_recursive(int n, int candidate);   /* start candidate at 1 */
```

Write a `main()` demonstrating each function with at least 4 test cases, including edge cases (n=0, empty string, single character, etc.).

---

## Problem 2: Merge Sort Variants (25 pts)

Create `merge_sort_variants.c`.

```c
/* Standard merge sort on an array of ints (from lecture — reimplement here) */
void merge_sort(int arr[], int n);

/* Merge sort that also counts the number of "inversions" in the array —
 * an inversion is a pair (i, j) with i < j and arr[i] > arr[j].
 * This must be computed AS A BYPRODUCT of the merge step (during merging,
 * whenever you take an element from the right half before the left half
 * is exhausted, that indicates inversions — count them without a separate
 * O(n²) pass). Target: O(n log n) total.
 * Store the total inversion count in *inversions. */
void merge_sort_count_inversions(int arr[], int n, long *inversions);

/* Merge sort for an array of C strings (char*[]), sorting lexicographically.
 * Do not modify the strings themselves — only reorder the pointers. */
void merge_sort_strings(char *arr[], int n);
```

### Requirements

- `merge_sort_count_inversions`: verify against a brute-force O(n²) inversion counter on at least 3 test arrays, confirming the counts match
- `merge_sort_strings`: sort `{"pear", "apple", "fig", "apple", "banana"}` and show the strings themselves never move
- Explain in a comment why taking from the **left** half on ties (`<=`) makes the sort stable

---

## Problem 3: Quicksort Engineering (20 pts)

Create `quicksort_engineering.c`.

```c
/* Standard Lomuto-partition quicksort (from lecture) */
void quicksort(int arr[], int n);

/* Median-of-three pivot selection: instead of always using the last
 * element, select the median of {first, middle, last} as the pivot
 * before partitioning. This defends against the sorted-input worst case
 * without the randomness of the randomized approach. */
void quicksort_median_of_three(int arr[], int n);

/* Hybrid: use quicksort for large subarrays, but switch to insertion sort
 * (Week 4) once a subarray's size falls below a threshold (e.g., 10
 * elements) — insertion sort has lower constant-factor overhead for
 * small inputs despite worse asymptotic complexity, so this hybrid is
 * often faster in practice than pure quicksort. */
#define INSERTION_THRESHOLD 10
void quicksort_hybrid(int arr[], int n);
```

### Comparison Requirement

Count comparisons in all three and tabulate them for a random array and an already-sorted array, each of
size 1000. In 2–3 sentences, explain why the sorted input hurts plain Lomuto and not median-of-three.

---

## Problem 4: Backtracking Problems (15 pts)

Create `backtracking.c`. Implement all of the following using the choose/explore/unchoose template from lecture.

```c
/* Print all permutations of the array (from lecture — reimplement) */
void print_all_permutations(int arr[], int n);

/* Print all subsets of the array whose elements sum to EXACTLY target.
 * (The classic "subset sum" problem, enumerating ALL solutions, not just
 * detecting whether one exists.) */
void print_subsets_summing_to(const int arr[], int n, int target);

/* Solve the N-Queens problem for a given n (4 <= n <= 12).
 * Print EVERY valid solution as an n x n grid of '.' and 'Q' characters,
 * separated by a blank line between solutions.
 * Also return the TOTAL count of solutions found. */
int solve_n_queens(int n);
```

### Requirements

- `solve_n_queens(8)` must correctly find all 92 solutions (a well-known value you can use to verify correctness)
- `print_subsets_summing_to({3, 1, 4, 2, 5}, 5, 5)` must print exactly `{3, 2}`, `{1, 4}` and `{5}` (any order)

---

## Problem 5: Binary Search Tree Applications (15 pts)

Create `bst_applications.c`. Start from Lecture 03's `TreeNode` (`data`, `left`, `right`) with its
`node_create`, `bst_insert` and a post-order free. Each function below is a **direct use of the lecture's
inorder traversal or the BST ordering property** — nothing new beyond that.

```c
/* The kth smallest value (k = 1 is the minimum), or -1 if k is out of range.
 * An inorder walk that stops as soon as k nodes have been counted. */
int bst_kth_smallest(const TreeNode *root, int k);

/* Print every value in [low, high] in ascending order, and add 1 to *visits for each node touched.
 * Use the ordering property to skip a subtree that cannot hold any value in range. */
void bst_print_range(const TreeNode *root, int low, int high, int *visits);

/* True if the two trees hold exactly the same values, whatever their shape. */
bool bst_same_values(const TreeNode *a, const TreeNode *b);
```

Insert `50 30 70 20 40 60 80 35 45 65`. Expected: `k = 1 → 20`, `k = 4 → 40`, `k = 10 → 80`, `k = 11 → -1`;
range `[33, 47]` prints `35 40 45` having visited **fewer than 10** nodes; the same ten values inserted in
another order give `same = 1`. Free every tree (Valgrind-clean).

---

## Makefile

```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

PROGRAMS = recursive_basics merge_sort_variants quicksort_engineering \
           backtracking bst_applications

all: $(PROGRAMS)

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGRAMS) *.o

.PHONY: all clean
```

---

## Submission

```bash
cd "$PROG101/week9/ps9"
git add .
git commit -m "PROG 101 PS 9: recursion, sorting, backtracking, BST applications"
```

All programs with dynamic allocation must be Valgrind-clean before submission.

---

## Grading

| Problem | Points | Key Criteria |
|---------|--------|-------------|
| P1: Recursive fundamentals | 25 | All functions correctly recursive, fast_power is O(log n), climb_stairs memoised |
| P2: Merge sort variants | 25 | Stable merge, inversion count from the merge step, string pointers sorted |
| P3: Quicksort engineering | 20 | Lomuto and median-of-three correct, hybrid correct, comparison table explained |
| P4: Backtracking | 15 | Permutations, subset sums, N-Queens finds exactly 92 for n = 8 |
| P5: BST applications | 15 | kth smallest stops early, range query proven to prune, same-values correct |
| **Total** | **100** | |

---

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

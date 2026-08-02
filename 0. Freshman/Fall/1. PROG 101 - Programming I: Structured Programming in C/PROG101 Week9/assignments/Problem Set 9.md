# PROG 101 — Programming I: Structured Programming in C
## Week 9 · Problem Set 9

**Released:** End of Week 9 Thursday
**Due:** Before Hashtables appendix Lecture 1
**Directory:** `~/prog101/week6/ps6/`
**Total:** 100 points

---

## Problem 1: Recursive Fundamentals (15 pts)

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

/* Flatten a singly nested structure: given an array of integers where
 * a value of INT_MIN is a sentinel meaning "the following count integers
 * are a nested group to sum before continuing" — no, skip this, too complex
 * for recursion basics; replaced below. */
```

Replace the last stub with:

```c
/* Print all the divisors of n (n > 0) in ascending order, using recursion
 * to check divisor candidates from 1 up to n. (Simple linear recursion,
 * O(n) — the point here is correct recursive structure, not asymptotic
 * optimality.) */
void print_divisors_recursive(int n, int candidate);   /* start candidate at 1 */
```

Write a `main()` demonstrating each function with at least 4 test cases, including edge cases (n=0, empty string, single character, etc.).

---

## Problem 2: Merge Sort Variants (20 pts)

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

/* Merge sort using a GENERIC comparator (like qsort's signature), operating
 * on an array of arbitrary-sized elements via void* and explicit size.
 * This generalizes the technique to work for any type. */
typedef int (*CompareFn)(const void *a, const void *b);
void merge_sort_generic(void *base, int n, size_t elem_size, CompareFn cmp);
```

### Requirements

- `merge_sort_count_inversions`: verify against a brute-force O(n²) inversion counter on at least 3 test arrays, confirming the counts match
- `merge_sort_generic`: demonstrate sorting an array of `int`, an array of `double`, and an array of a custom struct (by a chosen field) — all through the SAME generic function
- Explain in a comment: why is `merge_sort_generic` necessarily somewhat slower per-element than the `int`-specialized version, even though both are O(n log n)?

---

## Problem 3: Quicksort Engineering (15 pts)

Create `quicksort_engineering.c`.

```c
/* Standard Lomuto-partition quicksort (from lecture) */
void quicksort(int arr[], int n);

/* Quicksort using Hoare's partition scheme instead of Lomuto's.
 * Hoare's scheme uses two pointers converging from both ends and
 * generally performs fewer swaps in practice. Look up the algorithm's
 * structure, implement it correctly, and cite where you found the
 * reference (comment in your code). */
void quicksort_hoare(int arr[], int n);

/* Median-of-three pivot selection: instead of always using the last
 * element, select the median of {first, middle, last} as the pivot
 * before partitioning. This defends against the sorted-input worst case
 * without the randomness of the randomized approach. */
void quicksort_median_of_three(int arr[], int n);

/* Hybrid: use quicksort for large subarrays, but switch to insertion sort
 * (Week 2) once a subarray's size falls below a threshold (e.g., 10
 * elements) — insertion sort has lower constant-factor overhead for
 * small inputs despite worse asymptotic complexity, so this hybrid is
 * often faster in practice than pure quicksort. */
#define INSERTION_THRESHOLD 10
void quicksort_hybrid(int arr[], int n);
```

### Comparison Requirement

Instrument all four with a comparison counter (as in the lab) and benchmark against:
- Random arrays of size 1000, 10000
- Already-sorted arrays of size 1000, 10000
- Arrays with many duplicate values

Present your results in a table and write 3-4 sentences interpreting which technique performs best under which conditions, and why.

---

## Problem 4: Backtracking Problems (25 pts)

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

/* Given a string containing only digits, and a target number, insert
 * '+', '-', or nothing between digits so the resulting expression
 * evaluates to target. Print every valid expression found.
 * Example: string="123", target=6 → prints "1+2+3" (evaluates to 6)
 * This requires trying, at each position, to either extend the current
 * number or insert an operator and start a new number — classic
 * backtracking with THREE choices at each step, not two. */
void find_expressions(const char *digits, long target);

/* Solve a simple maze: given an n x n grid of 0s (open) and 1s (wall),
 * find a path from (0,0) to (n-1,n-1) moving only right or down.
 * Print the path as a sequence of 'R'/'D' moves if one exists, or
 * "No path found" otherwise. (This should backtrack on dead ends.) */
int solve_maze(int grid[][20], int n);
```

### Requirements

- `solve_n_queens(8)` must correctly find all 92 solutions (a well-known value you can use to verify correctness)
- `find_expressions`: handle multi-digit numbers correctly (e.g., "12+3" is different from "1+23") — this is the subtlety that makes this problem harder than simple permutation generation
- Provide test cases for `solve_maze` with both a solvable and an unsolvable configuration

---

## Problem 5: Binary Search Tree Applications (25 pts)

Create `bst_applications.h`/`bst_applications.c`, building on the `bst.h`/`bst.c` from Lab 9 (assume it's available in `../lab9/`).

```c
#include "../lab9/bst.h"

/* Return the lowest common ancestor (LCA) of two values known to both
 * exist in the BST. The LCA is the deepest node that has both values
 * in its subtree (one on each side, or one of them IS the LCA itself).
 * Exploit the BST ordering property for an O(height) solution —
 * do NOT search the whole tree. */
TreeNode *bst_lowest_common_ancestor(TreeNode *root, int value1, int value2);

/* Return the kth smallest value in the BST (1-indexed: k=1 returns
 * the minimum). Use inorder traversal, but do NOT build a full array
 * first — stop as soon as you've counted k nodes (early termination
 * for efficiency). Return -1 if k is out of range. */
int bst_kth_smallest(TreeNode *root, int k);

/* Convert a SORTED array into a HEIGHT-BALANCED BST.
 * (This is the inverse of inorder traversal — recursively pick the
 * middle element as the root, recurse on left and right halves.)
 * Returns the root of the new tree. */
TreeNode *sorted_array_to_bst(const int arr[], int n);

/* Given two BSTs, merge them into a single new BST containing all
 * values from both (assume no duplicate values across the two trees).
 * For a good implementation: convert both to sorted arrays via inorder
 * traversal, merge the two sorted arrays (like merge sort's merge step),
 * then build a balanced BST from the merged result using
 * sorted_array_to_bst. Do not simply insert one tree's values one-by-one
 * into the other — that risks creating an unbalanced result. */
TreeNode *bst_merge(TreeNode *root1, TreeNode *root2);

/* Print all values in the BST that fall within the range [low, high]
 * inclusive, in ascending order. Exploit the BST property to PRUNE
 * entire subtrees that cannot contain any value in range (do not
 * simply do a full inorder traversal and filter — that defeats the
 * purpose; your solution must skip visiting subtrees that are
 * provably out of range). */
void bst_print_range(const TreeNode *root, int low, int high);

/* Return true if two BSTs contain exactly the same set of values,
 * regardless of their structural shape (they may have been built via
 * different insertion orders and thus look structurally different,
 * but represent the same set). Hint: compare their inorder traversals. */
bool bst_same_values(const TreeNode *root1, const TreeNode *root2);
```

### Requirements

- `bst_lowest_common_ancestor` must be O(height), not O(n) — no full tree search
- `sorted_array_to_bst` must produce a height-balanced tree — verify with `tree_is_balanced` from Lab 9
- `bst_print_range` must demonstrably prune: add an instrumented "visit counter" and prove on a test case that fewer nodes are visited than the total tree size when the range is narrow
- Write a `main()` demonstrating every function, and free every tree you create (Valgrind-clean)

---

## Makefile

```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

PROGRAMS = recursive_basics merge_sort_variants quicksort_engineering \
           backtracking bst_applications_test

all: $(PROGRAMS)

bst_applications_test: bst_applications_test.o bst_applications.o ../lab9/bst.o
	$(CC) $(CFLAGS) -o $@ $^

../lab9/bst.o: ../lab9/bst.c ../lab9/bst.h
	$(CC) $(CFLAGS) -c $< -o $@

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGRAMS) *.o

.PHONY: all clean
```

---

## Submission

```bash
cd ~/prog101/week6/ps6
git add .
git commit -m "PS6 complete: recursion, sorting, backtracking, BST applications"
```

All programs with dynamic allocation must be Valgrind-clean before submission.

---

## Grading

| Problem | Points | Key Criteria |
|---------|--------|-------------|
| P1: Recursive fundamentals | 15 | All functions correctly recursive, fast_power is O(log n) |
| P2: Merge sort variants | 20 | Inversion counting correct, generic version works for 3+ types |
| P3: Quicksort engineering | 15 | Hoare partition correct, hybrid faster on benchmarks |
| P4: Backtracking | 25 | N-Queens finds exactly 92 for n=8, expressions handle multi-digit correctly |
| P5: BST applications | 25 | LCA is O(height), balanced construction verified, range query proven to prune |
| **Total** | **100** | |

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading table above (100 points).
> No errata found — the rubric's "exactly 92 for n=8" was verified independently.
> Compile/verify with `gcc 13.3.0 -Wall -Wextra -Werror -g -std=c11`; heap claims under valgrind.

---

### Problem 1 — Recursive Fundamentals (15 pts)

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

### Problem 2 — Merge Sort Variants (20 pts)

*Inversion counting: the whole trick is `inv += (mid - i)` when taking an element from the **right** half — every remaining element of the left half forms an inversion with it, counted in O(1) rather than one at a time. A nested-loop count inside merge is still O(n²) and defeats the exercise. (Identical to CS 101 PS 6 B2(e); reward students who notice.)*
*Generic version: `void merge_sort(void *base, size_t n, size_t size, int (*cmp)(const void*, const void*))`. Element movement must go through `memcpy` on `char *` byte arithmetic, since the type isn't known. The rubric requires 3+ types — test `int`, `double`, and `char *` (strings), where the comparator receives `char **`.*
*Merge sort must be **stable**: when `cmp(...) == 0`, take from the **left** half (`<=`, not `<`). Test with records carrying a payload — sorting `{(1,'a'),(1,'b')}` must preserve that order. A strict `<` silently loses stability and is the most common defect here.*
*Every allocation in the merge buffer must be freed; valgrind-clean.*

### Problem 3 — Quicksort Engineering (15 pts)

*Hoare partition is subtler than Lomuto and is where the marks are. Two facts to check: the pivot must **not** be `arr[hi]` with `do/while` scanning (that combination runs off the end), and Hoare returns a split point `j` such that the recursive calls are `qsort(lo, j)` and `qsort(j+1, hi)` — **not** `j-1`/`j+1` as with Lomuto. Getting this wrong causes infinite recursion or dropped elements; test with an all-equal array like `{5,5,5,5,5}`, which is the standard killer.*
*The hybrid (quicksort + insertion sort below a cutoff, typically 8–16) must be shown **faster on benchmarks**, per the rubric — require the timing table, not just the code. Expect a modest win (10–25%), not a dramatic one; a student reporting no measurable difference at n = 1000 has done nothing wrong, and should say so honestly rather than inventing numbers.*
*Already-sorted input is the adversarial case for a fixed pivot: median-of-three or a random pivot is required to avoid O(n²). Benchmark on `0..n-1` ascending to demonstrate it.*

### Problem 4 — Backtracking (25 pts)

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
*Expression generation: "multi-digit correctly" is an explicit rubric item — the tokenizer must not treat each character as a separate number. Test with operands ≥ 10.*

### Problem 5 — BST Applications (25 pts)

*LCA must be **O(height)**, which means using the BST ordering property rather than a general-tree search: descend left while both targets are smaller, right while both are larger, and the first node that splits them (or equals one of them) is the LCA. A generic post-order LCA that ignores ordering is O(n) and does not meet the rubric.*

```c
Node *lca(Node *root, int a, int b) {
    while (root) {
        if (a < root->key && b < root->key)      root = root->left;
        else if (a > root->key && b > root->key) root = root->right;
        else return root;                         /* split point */
    }
    return NULL;
}
```

*Balanced construction from a sorted array: recurse on the midpoint. **Verify the height** rather than trusting the shape — for n nodes it must be ⌈log₂(n+1)⌉. For n = 1023 that is 10; a student whose height is 1023 has built a degenerate linked list (usually by inserting in sorted order instead of splitting).*
*Range query must **prune**, per the rubric: skip the left subtree entirely when `node->key <= low`, and the right when `node->key >= high`. "Proven to prune" means instrumenting a visit counter and showing that a narrow range on a large tree visits far fewer than n nodes. A full in-order traversal that filters afterwards gives correct output and earns no credit for this item — require the counter evidence.*
*BST deletion (if assessed here) has the same three cases as always — leaf, one child, two children (replace with in-order successor, then delete that successor). Test all three plus deleting the root of a two-node tree.*
*All tree memory must be freed via a post-order teardown — freeing a node before recursing into its children is a use-after-free that valgrind reports as `Invalid read`.*

---

*PROG 101 · Week 9 · Problem Set 9 · © CSE Department*

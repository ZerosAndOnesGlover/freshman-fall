# PROG 101 · Programming I: Structured Programming in C
## Week 9 · Problem Set 9

**Released:** Thursday 26 November 2026, 11:00 (after Week 9 Lecture 3)
**Due:** Tuesday 1 December 2026, 10:00 (start of Week 10 Lecture 1) — late penalty from 10:01
**Directory:** `"$PROG101/week9/ps9"` in the Freshman Fall repo
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: cut from about five hours to three. Lab 9, on Monday 30 November, writes `merge_sort` and
`quicksort` and tabulates their comparison counts, so Quicksort Engineering (old Problem 3) is now only in the lab
and Problem 2 reuses the lab's `merge_sort`. `is_palindrome_advanced`, `print_divisors_recursive` and N-Queens
were removed too. The answer key moved out of this handout.)*

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

/* Count the number of times digit 'd' appears in the decimal representation
 * of a non-negative integer n. */
int count_digit_occurrences(int n, int d);

/* Return the number of distinct ways to climb n stairs, taking either
 * 1 or 2 steps at a time. (This is the Fibonacci recurrence in disguise —
 * recognize it.) Use memoization — a naive version will be far too slow
 * for n=40 and above. */
long climb_stairs(int n);

```

Write a `main()` demonstrating each function with at least 4 test cases, including edge cases such as n = 0.

---

## Problem 2: Merge Sort Variants (30 pts)

Create `merge_sort_variants.c`.

```c
/* Start from your Lab 9 merge_sort. */

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

## Problem 3: Backtracking Problems (20 pts)

Create `backtracking.c`. Implement all of the following using the choose/explore/unchoose template from lecture.

```c
/* Print all permutations of the array (from lecture — reimplement) */
void print_all_permutations(int arr[], int n);

/* Print all subsets of the array whose elements sum to EXACTLY target.
 * (The classic "subset sum" problem, enumerating ALL solutions, not just
 * detecting whether one exists.) */
void print_subsets_summing_to(const int arr[], int n, int target);

```

### Requirements

- `print_subsets_summing_to({3, 1, 4, 2, 5}, 5, 5)` must print exactly `{3, 2}`, `{1, 4}` and `{5}` (any order)

---

## Problem 4: Binary Search Tree Applications (25 pts)

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

PROGRAMS = recursive_basics merge_sort_variants backtracking bst_applications

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
git commit -m "PROG 101 PS 9: recursion, merge sort variants, backtracking, BST applications"
```

All programs with dynamic allocation must be Valgrind-clean before submission.

---

## Grading

| Problem | Points | Key Criteria |
|---------|--------|-------------|
| P1: Recursive fundamentals | 25 | All functions correctly recursive, fast_power is O(log n), climb_stairs memoised |
| P2: Merge sort variants | 30 | Stable merge, inversion count from the merge step, string pointers sorted |
| P3: Backtracking | 20 | Permutations and subset sums |
| P4: BST applications | 25 | kth smallest stops early, range query proven to prune, same-values correct |
| **Total** | **100** | |

---

*PROG 101 · Week 9 · Problem Set 9 · Due Tuesday 1 December 2026, 10:00 · © CSE Department*

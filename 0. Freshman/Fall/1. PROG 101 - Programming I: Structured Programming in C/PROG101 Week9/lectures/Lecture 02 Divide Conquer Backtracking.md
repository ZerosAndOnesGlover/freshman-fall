# PROG 101 Programming I: Structured Programming in C
## Week 9 · Lecture 2: Recursive Algorithms — Divide-and-Conquer and Backtracking

---

## Lecture Goals

By the end of this lecture you will:
- Implement merge sort and understand its divide-and-conquer structure
- Implement quicksort and understand partitioning
- Analyze recursive algorithm complexity informally using the recursion tree
- Implement backtracking algorithms: permutations, subsets, and combinations
- Understand the "choose, explore, unchoose" backtracking pattern

---

## 1. Divide-and-Conquer: The General Strategy

Divide-and-conquer algorithms follow a three-step template:

1. **Divide** the problem into smaller subproblems of the same type
2. **Conquer** each subproblem recursively (base case: trivially small subproblems)
3. **Combine** the subproblem solutions into the solution for the original problem

This is a more structured specialization of the general recursion pattern from Lecture 1, and it underlies some of the most important algorithms in computer science.

---

## 2. Merge Sort

**Divide:** split the array into two halves.
**Conquer:** recursively sort each half.
**Combine:** merge the two sorted halves into one sorted array.

```c
/* Merge two adjacent sorted subarrays: arr[lo..mid] and arr[mid+1..hi]
 * into a single sorted arr[lo..hi], using a temporary buffer. */
void merge(int arr[], int lo, int mid, int hi, int temp[]) {
    int i = lo;       /* pointer into left half */
    int j = mid + 1;  /* pointer into right half */
    int k = lo;       /* pointer into temp (the output) */

    while (i <= mid && j <= hi) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
        }
    }
    /* Copy any remaining elements from whichever half wasn't exhausted */
    while (i <= mid) temp[k++] = arr[i++];
    while (j <= hi)  temp[k++] = arr[j++];

    /* Copy the merged result back into the original array */
    for (int x = lo; x <= hi; x++) {
        arr[x] = temp[x];
    }
}

void merge_sort_helper(int arr[], int lo, int hi, int temp[]) {
    if (lo >= hi) return;               /* base case: 0 or 1 elements — already sorted */

    int mid = lo + (hi - lo) / 2;       /* divide */
    merge_sort_helper(arr, lo, mid, temp);       /* conquer left half */
    merge_sort_helper(arr, mid + 1, hi, temp);   /* conquer right half */
    merge(arr, lo, mid, hi, temp);               /* combine */
}

void merge_sort(int arr[], int n) {
    int *temp = malloc(n * sizeof(int));
    if (temp == NULL) { perror("malloc"); exit(1); }
    merge_sort_helper(arr, 0, n - 1, temp);
    free(temp);
}
```

### Why Merge Sort Is O(n log n)

The recursion tree has **log₂(n) levels** (each level halves the range), and at each level, the total work across all `merge` calls at that level is O(n) (every element is touched exactly once during merging at each level). Total work: O(n) per level × O(log n) levels = **O(n log n)**.

```
Level 0:                    [8 elements]                    → O(n) work to merge
Level 1:           [4 elements]   [4 elements]              → O(n) work total
Level 2:        [2][2]         [2][2]                       → O(n) work total
Level 3:      [1][1][1][1]  [1][1][1][1]                    → base cases

log₂(8) = 3 levels of splitting, O(n) work per level → O(n log n) total
```

This is asymptotically better than the O(n²) sorting algorithms (insertion sort, selection sort) you implemented in Week 2 — the difference becomes dramatic at scale: sorting 1,000,000 elements takes roughly 20,000,000 operations with merge sort versus 1,000,000,000,000 with an O(n²) sort.

---

## 3. Quicksort

**Divide:** choose a pivot element and partition the array so all elements less than the pivot come before it, and all elements greater come after.
**Conquer:** recursively sort the two partitions.
**Combine:** nothing needed — the array is already sorted in place once both partitions are sorted (partitioning did the real work).

```c
/* Partition arr[lo..hi] around a pivot (using arr[hi] as the pivot).
 * Returns the final index of the pivot after partitioning. */
int partition(int arr[], int lo, int hi) {
    int pivot = arr[hi];   /* choose the last element as pivot */
    int i = lo - 1;        /* boundary of "elements known to be < pivot" */

    for (int j = lo; j < hi; j++) {
        if (arr[j] < pivot) {
            i++;
            int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
        }
    }
    /* Place the pivot in its correct final position */
    int tmp = arr[i + 1]; arr[i + 1] = arr[hi]; arr[hi] = tmp;
    return i + 1;
}

void quicksort_helper(int arr[], int lo, int hi) {
    if (lo >= hi) return;                    /* base case: 0 or 1 elements */

    int pivot_index = partition(arr, lo, hi); /* divide (partitioning does the work) */
    quicksort_helper(arr, lo, pivot_index - 1);      /* conquer left partition */
    quicksort_helper(arr, pivot_index + 1, hi);      /* conquer right partition */
    /* no combine step needed */
}

void quicksort(int arr[], int n) {
    quicksort_helper(arr, 0, n - 1);
}
```

### Quicksort's Performance Characteristics

- **Average case:** O(n log n) — the same asymptotic class as merge sort
- **Worst case:** O(n²) — occurs when partitioning is maximally unbalanced (e.g., the array is already sorted and you always pick the last element as pivot, so every partition splits into a size-0 and a size-(n-1) piece)
- **In-place:** unlike merge sort, quicksort doesn't need an auxiliary array of size n (though it does use O(log n) stack space for recursion)

**Why the worst case matters in practice:** naive pivot selection (always the first or last element) is vulnerable to already-sorted or adversarially-constructed input. Production-quality implementations use techniques like **median-of-three** pivot selection or **randomized pivot selection** to make the worst case extremely unlikely in practice.

```c
/* Randomized pivot selection — swap a random element into the last position
 * before partitioning, to avoid worst-case behavior on sorted/adversarial input */
#include <stdlib.h>
void quicksort_helper_randomized(int arr[], int lo, int hi) {
    if (lo >= hi) return;

    int random_index = lo + rand() % (hi - lo + 1);
    int tmp = arr[random_index]; arr[random_index] = arr[hi]; arr[hi] = tmp;

    int pivot_index = partition(arr, lo, hi);
    quicksort_helper_randomized(arr, lo, pivot_index - 1);
    quicksort_helper_randomized(arr, pivot_index + 1, hi);
}
```

---

## 4. Backtracking — Systematic Trial and Error

Backtracking explores all possible configurations of a solution space by incrementally building candidates, abandoning ("backtracking from") a candidate as soon as it's determined that it cannot possibly lead to a valid solution.

The universal backtracking template:

```c
void backtrack(/* current partial solution, remaining choices */) {
    if (/* partial solution is complete */) {
        /* record or process the complete solution */
        return;
    }

    for (/* each possible next choice */) {
        /* CHOOSE: make the choice, update state */
        backtrack(/* updated partial solution */);
        /* UNCHOOSE: undo the choice, restore state (this is the "backtrack" step) */
    }
}
```

The **choose → explore → unchoose** cycle is the heart of every backtracking algorithm. Master this template and you can solve an enormous class of combinatorial problems.

### Generating All Subsets (The Power Set)

```c
#define MAX_N 20

void print_subset(const int chosen[], int count) {
    printf("{ ");
    for (int i = 0; i < count; i++) printf("%d ", chosen[i]);
    printf("}\n");
}

void subsets_helper(const int arr[], int n, int index,
                    int chosen[], int chosen_count) {
    if (index == n) {                       /* base case: considered every element */
        print_subset(chosen, chosen_count);
        return;
    }

    /* Choice 1: EXCLUDE arr[index] from the subset */
    subsets_helper(arr, n, index + 1, chosen, chosen_count);

    /* Choice 2: INCLUDE arr[index] in the subset */
    chosen[chosen_count] = arr[index];              /* CHOOSE */
    subsets_helper(arr, n, index + 1, chosen, chosen_count + 1);  /* EXPLORE */
    /* UNCHOOSE is implicit here: chosen_count+1 was only passed by value,
       so the caller's chosen_count is unaffected — no explicit undo needed
       because we didn't mutate shared state, just passed a different count */
}

void print_all_subsets(const int arr[], int n) {
    int chosen[MAX_N];
    subsets_helper(arr, n, 0, chosen, 0);
}
```

For an array of `n` elements, there are exactly `2ⁿ` subsets (each element is either included or excluded — a binary choice, repeated n times). This recursion tree has exactly `2ⁿ` leaves, matching that count precisely.

### Generating All Permutations

```c
void swap(int *a, int *b) {
    int tmp = *a; *a = *b; *b = tmp;
}

void print_array(const int arr[], int n) {
    printf("[ ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("]\n");
}

void permutations_helper(int arr[], int n, int start) {
    if (start == n) {                       /* base case: fixed every position */
        print_array(arr, n);
        return;
    }

    for (int i = start; i < n; i++) {
        swap(&arr[start], &arr[i]);              /* CHOOSE: place arr[i] at position 'start' */
        permutations_helper(arr, n, start + 1);   /* EXPLORE: recurse on the rest */
        swap(&arr[start], &arr[i]);              /* UNCHOOSE: undo the swap — restore order */
    }
}

void print_all_permutations(int arr[], int n) {
    permutations_helper(arr, n, 0);
}
```

This is the clearest illustration of **why the "unchoose" step is essential**: without swapping back, each iteration of the `for` loop would operate on an already-scrambled array from the previous iteration, producing wrong (and non-exhaustive) results. The array must be restored to its state *before* this call's choice was made, so that the next choice in the loop starts from a clean slate.

There are exactly `n!` permutations of `n` distinct elements — trace through `n=3` by hand and count the printed permutations to verify this against `3! = 6`.

### Generating Combinations (Choose k from n)

```c
void combinations_helper(const int arr[], int n, int k,
                         int start, int chosen[], int chosen_count) {
    if (chosen_count == k) {                /* base case: chosen exactly k elements */
        print_subset(chosen, chosen_count);
        return;
    }
    if (start == n) return;                  /* base case: ran out of elements */

    /* Choice: SKIP arr[start] */
    combinations_helper(arr, n, k, start + 1, chosen, chosen_count);

    /* Choice: INCLUDE arr[start] */
    chosen[chosen_count] = arr[start];
    combinations_helper(arr, n, k, start + 1, chosen, chosen_count + 1);
}
```

This computes exactly `C(n, k) = n! / (k! (n-k)!)` combinations — the binomial coefficient you may have seen in a discrete math context.

---

## 5. A Complete Backtracking Example: N-Queens (Preview)

The classic backtracking problem: place N queens on an N×N chessboard so no two threaten each other (no shared row, column, or diagonal).

```c
#define MAX_N 12

int col_used[MAX_N] = {0};
int diag1_used[2 * MAX_N] = {0};   /* row + col is constant along a "\" diagonal */
int diag2_used[2 * MAX_N] = {0};   /* row - col + n is constant along a "/" diagonal */
int solution_count = 0;

void solve_n_queens(int row, int n) {
    if (row == n) {                          /* base case: placed a queen in every row */
        solution_count++;
        return;
    }

    for (int col = 0; col < n; col++) {
        int d1 = row + col;
        int d2 = row - col + n;

        if (col_used[col] || diag1_used[d1] || diag2_used[d2]) {
            continue;   /* this column/diagonal is under attack — skip */
        }

        /* CHOOSE: place a queen at (row, col) */
        col_used[col] = diag1_used[d1] = diag2_used[d2] = 1;

        solve_n_queens(row + 1, n);           /* EXPLORE: try to place the rest */

        /* UNCHOOSE: remove the queen, restore state for the next column to try */
        col_used[col] = diag1_used[d1] = diag2_used[d2] = 0;
    }
}
```

The pruning (`if (...) continue;`) is what makes backtracking dramatically faster than brute-force enumeration: entire branches of the recursion tree are cut off the moment a partial solution is known to be invalid, without ever exploring them further. This is the essential idea behind every backtracking algorithm: **explore only promising partial solutions, abandon the rest as early as possible.**

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Trace one Lomuto partition on `{3, 7, 8, 5, 2, 1, 9, 5}` with the last element as pivot. Give the array afterwards and the pivot index.

```c
int partition(int a[], int lo, int hi) {
    int pivot = a[hi], i = lo - 1;
    for (int j = lo; j < hi; j++)
        if (a[j] <= pivot) { i++; int t=a[i]; a[i]=a[j]; a[j]=t; }
    int t = a[i+1]; a[i+1] = a[hi]; a[hi] = t;
    return i + 1;
}
```

**2. (Explain.)** Merge sort and quicksort are both divide-and-conquer and both average O(n log n). Compare them on four dimensions and say when each is preferred.

**3. (Build.)** Write `merge` for merge sort, then explain why the standard implementation allocates a temporary buffer and what goes wrong without one.

**4. (Stretch.)** Explain the choose-explore-unchoose structure of backtracking using N-Queens. Why must the "unchoose" step exist, and what is the cost of forgetting it?


### Answers

**1.** Result: **`{3, 5, 2, 1, 5, 7, 9, 8}`**, pivot index **4**, and `a[4]` is the pivot `5`. ✓

The invariant makes it readable: at the top of each `j` iteration, `a[lo..i]` holds everything examined so far that is **≤ pivot** and `a[i+1..j-1]` holds everything **> pivot**. When `a[j] <= pivot`, `i` advances and a swap moves the small element into the left region, pushing a large one right. When `a[j] > pivot` nothing moves — it is already where it belongs.

The final swap drops the pivot at `i+1`, exactly on the boundary, which puts it in its **permanent sorted position**. That is why the recursive calls exclude it: `quicksort(a, lo, p-1)` and `quicksort(a, p+1, hi)`. Including it would fail to shrink the problem and recurse forever.

Note the duplicate `5`: with `<=`, equal elements go left. Using `<` sends them right, and on an array of all-equal elements produces maximally unbalanced partitions — O(n²) on input that looks trivial. Equal-key handling is a real design decision in quicksort, not a detail; three-way partitioning (Dutch national flag) solves it properly.

**2.** | | Merge sort | Quicksort |
|---|---|---|
| **Worst case** | **Θ(n log n)** guaranteed | Θ(n²) — on sorted input with a naive pivot |
| **Extra space** | Θ(n) for the merge buffer | **Θ(log n)** for the recursion stack; sorts in place |
| **Stability** | **Stable** | Not stable — the long-range swap reorders equal keys |
| **Constant factor** | Larger — allocation, copying, two read streams | **Smaller** — in-place, sequential, cache-friendly |

**Where the work happens** is the structural difference: merge sort splits trivially and does the work in the *combine* step; quicksort does the work in the *divide* (partition) and combines trivially.

**Prefer quicksort** as a general in-memory sort — it is usually 2–3× faster in practice because it touches memory sequentially and allocates nothing. Defend the worst case with a randomised or median-of-three pivot, and, as introsort does, switch to heapsort past a depth of ~2 log n for a hard guarantee.

**Prefer merge sort** when stability is required (multi-key sorting, as in CS 101 L17), when the worst case must be bounded — real-time systems care about the tail, not the average — or when the data does not fit in memory. External sorting of a file larger than RAM is merge sort, because merging is **sequential** and works on streams, while partitioning needs random access. It is also the natural choice for linked lists, where it needs no extra space at all and quicksort's random access is O(n).

**3.**

```c
static void merge(int a[], int lo, int mid, int hi, int tmp[]) {
    int i = lo, j = mid + 1, k = lo;
    while (i <= mid && j <= hi)
        tmp[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];   /* <= keeps it stable */
    while (i <= mid) tmp[k++] = a[i++];
    while (j <= hi)  tmp[k++] = a[j++];
    for (int t = lo; t <= hi; t++) a[t] = tmp[t];
}

void merge_sort(int a[], int lo, int hi, int tmp[]) {
    if (lo >= hi) return;
    int mid = lo + (hi - lo) / 2;
    merge_sort(a, lo, mid, tmp);
    merge_sort(a, mid + 1, hi, tmp);
    merge(a, lo, mid, hi, tmp);
}
```

The buffer is needed because merging writes into the **same range it is still reading from**. Writing the smaller of `a[i]` and `a[j]` directly to `a[k]` would overwrite an element of the left half that has not been consumed yet — `k` catches up with `i` as soon as elements are taken from the right half. The temporary decouples the read and write sequences.

In-place merging without extra space is possible but genuinely hard, and the known algorithms are slow enough that no practical implementation uses them. The pragmatic compromise, used by Timsort, is a buffer the size of the **smaller half** rather than the whole array.

Two details. **Allocate `tmp` once** in a wrapper, not inside `merge` — allocating per call turns O(n) extra space into O(n log n) allocations and dominates the runtime. And **`<=` rather than `<`** in the comparison is what makes the sort stable: on a tie, the left element is taken first.

**4.**

```c
int solve(int board[], int row, int n) {
    if (row == n) return 1;              /* all placed */
    for (int col = 0; col < n; col++) {
        if (!safe(board, row, col)) continue;
        board[row] = col;                /* CHOOSE  */
        if (solve(board, row + 1, n)) return 1;   /* EXPLORE */
        board[row] = -1;                 /* UNCHOOSE */
    }
    return 0;
}
```

The three steps are: **choose** a candidate, **explore** every completion of that choice recursively, and **unchoose** — restore the state exactly as it was before the choice.

**Unchoose exists because the state is shared.** Backtracking uses one mutable structure for the whole search rather than copying it at every node, which is what makes it affordable; the price is that each branch must leave the state pristine for its siblings. Without the restore, the next `col` in the loop would explore a board still carrying the previous attempt's queen, and the search would report impossible positions or miss valid ones.

**The cost of forgetting it** is usually not a crash but *wrong answers* — solutions missed, or invalid ones accepted — which is far harder to notice than a segfault. In problems that *collect* results rather than returning the first, the classic symptom is the right **number** of results, all identical, because every recorded answer aliases the one shared buffer. Recording a result must therefore take a **copy**.

Here `safe()` is the pruning step, and it is what makes N-Queens tractable: the raw search space is nⁿ, restricting to one queen per row cuts it to n!, and pruning by column and diagonal brings 8-Queens to a few thousand nodes.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Divide-and-conquer** | Algorithm strategy: divide into subproblems, conquer recursively, combine results |
| **Merge sort** | O(n log n) divide-and-conquer sort using an auxiliary buffer to merge sorted halves |
| **Quicksort** | O(n log n) average-case, in-place divide-and-conquer sort using pivot partitioning |
| **Pivot** | The element quicksort partitions the array around |
| **Backtracking** | Systematic search that builds candidates incrementally and abandons invalid partial solutions |
| **Choose/Explore/Unchoose** | The three-step template underlying every backtracking algorithm |
| **Pruning** | Cutting off branches of the search tree known to be invalid, without exploring them |
| **Power set** | The set of all subsets of a set; has size 2ⁿ for an n-element set |

---

## Reading

- **CLRS Ch. 2** — Getting Started (insertion sort baseline) and **Ch. 7** — Quicksort
- **King Ch. 18** — Recursion (backtracking examples)
- **Skiena, The Algorithm Design Manual** — Ch. 7 (Backtracking) — the "war stories" framing is excellent motivation

---

*Next: Lecture 3 — Recursive Data Structures: Binary Trees*

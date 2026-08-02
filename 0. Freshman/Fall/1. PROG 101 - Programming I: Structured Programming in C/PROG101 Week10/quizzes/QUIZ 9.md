# PROG 101 — Quiz 9
## Week 10, Tuesday — In-Class Assessment

**Administered:** start of Week 10, Lecture 1 (Tuesday)
**Covers:** Week 9 material
**Duration:** 10 minutes · Closed book · 20 points

---

## Section A — Multiple Choice (2 pts each)

**1.** What are the two essential components of every correct recursive function?

- (A) A loop and a return statement
- (B) A base case and a recursive case that moves strictly toward it
- (C) A global variable and a local variable
- (D) An array and a pointer

---

**2.** What is the time complexity of naive (non-memoized) recursive Fibonacci, `fib(n) = fib(n-1) + fib(n-2)`?

- (A) O(n)
- (B) O(n log n)
- (C) O(n²)
- (D) O(2ⁿ)

---

**3.** In merge sort, at what step does the actual "combining" of sorted data happen?

- (A) During the recursive splitting (divide) step
- (B) During the merge step, after both halves are already sorted
- (C) Before any recursion begins
- (D) Merge sort has no separate combine step

---

**4.** For a Binary Search Tree, what traversal order visits nodes in ascending sorted order?

- (A) Preorder
- (B) Inorder
- (C) Postorder
- (D) None — BSTs don't guarantee any sorted traversal

---

**5.** Why must a tree's memory be freed using postorder traversal (children before parent), not preorder?

- (A) Postorder is faster
- (B) If you free the parent first, you lose your only pointers to its children, causing a memory leak
- (C) C requires postorder for all recursive frees
- (D) It doesn't matter — any order works correctly

---

## Section B — Short Answer (2 pts each)

**6.** Identify the bug in this recursive function and explain what happens when it runs:

```c
int count_down(int n) {
    printf("%d\n", n);
    return count_down(n - 1);
}
```

Bug: `_________________________________________________________________`

What happens when called: `_________________________________________`

---

**7.** In the backtracking permutation algorithm below, why is the second `swap` call (after the recursive call) essential?

```c
void permute(int arr[], int n, int start) {
    if (start == n) { print_array(arr, n); return; }
    for (int i = start; i < n; i++) {
        swap(&arr[start], &arr[i]);
        permute(arr, n, start + 1);
        swap(&arr[start], &arr[i]);   /* <-- why is this necessary? */
    }
}
```

```
_____________________________________________________________________

_____________________________________________________________________
```

---

**8.** Draw the tree that results from inserting these values, in this order, into an empty BST: `50, 30, 70, 20, 40`.

```



```

What is the height of this tree? `______`

---

**9.** Explain why a plain (unbalanced) BST's operations are described as "O(log n) average case, O(n) worst case." What input pattern produces the worst case?

```
Average case reasoning: _____________________________________________

Worst case reasoning: _______________________________________________

Input pattern that triggers worst case: _____________________________
```

---

**10.** What is tail recursion, and why can't you rely on C compilers to always optimize it away (unlike some other languages)?

```
Tail recursion definition: __________________________________________

Why you can't rely on it in C: ______________________________________
```

---

## Answer Key (Instructor Copy)

**1. (B)** — Every recursive function needs a base case (the simplest input(s), solved without further recursion) and a recursive case that reduces the problem to a strictly simpler subproblem, guaranteeing eventual termination.

**2. (D) O(2ⁿ)** — Naive Fibonacci recomputes overlapping subproblems exponentially many times: `fib(n)` calls `fib(n-1)` and `fib(n-2)`, but `fib(n-1)` itself calls `fib(n-2)` again, and this redundancy compounds at every level. The recursion tree has O(2ⁿ) total nodes/calls.

**3. (B)** — Divide-and-conquer's "combine" step in merge sort is the `merge` function, which runs after both recursive calls (sorting the left and right halves) have already returned fully sorted subarrays. The merge step interleaves them into one sorted result.

**4. (B) Inorder** — By visiting left subtree, then the node, then right subtree, and given the BST invariant that left < node < right at every level, inorder traversal naturally produces values in ascending sorted order.

**5. (B)** — If you `free(root)` before recursing into `root->left` and `root->right`, those pointer values become dangling references to freed memory — accessing `root->left` after freeing `root` is itself undefined behavior (use-after-free), and even if it "worked" by luck, you would have already lost the ability to properly free the children, leaking their memory. Postorder guarantees children are fully freed before their parent.

**6.** Bug: there is no base case at all — the function recurses indefinitely for any starting value of `n`, including negative numbers (it never checks for a stopping condition like `n <= 0`). What happens: it prints decreasing integers forever (or until integer underflow wraps around, which is itself undefined behavior for signed int), rapidly pushing new stack frames until the stack is exhausted, crashing with a stack overflow (segmentation fault).

**7.** The first `swap` places `arr[i]` at position `start` to explore that choice. Without the second `swap` (undoing it), the array would remain permanently altered for the rest of the `for` loop's iterations — each subsequent value of `i` would then be operating on an already-scrambled array from the previous iteration rather than the original ordering, producing incorrect and incomplete results (some permutations would be missed, others duplicated or wrong). The second `swap` restores the array to its pre-choice state so each loop iteration starts from a clean, correct baseline — this is the "unchoose" step of the choose/explore/unchoose backtracking template.

**8.**
```
        [50]
       /    \
    [30]    [70]
    /  \
 [20] [40]
```
Height: **2** (edges from root to the deepest leaf: 50→30→20 or 50→30→40, both 2 edges).

**9.**
- Average case: for a BST built from randomly-ordered insertions, the tree tends to stay roughly balanced, giving a height of O(log n); since search/insert/delete each traverse a single root-to-leaf path, their cost is proportional to height, hence O(log n) on average.
- Worst case: nothing in the plain BST insertion algorithm guarantees balance. If insertions happen in a pattern that always extends the tree in one direction, the tree degenerates into a shape with height O(n).
- Input pattern: inserting already-sorted (or already-reverse-sorted) data, e.g. `1, 2, 3, 4, 5, ...` in increasing order — every new value becomes the right child of the previous largest node, producing a structure equivalent to a linked list.

**10.** Tail recursion definition: a recursive call is "tail recursive" when it is the very last operation performed in the function — its return value is immediately returned by the caller with no further computation pending afterward. Why you can't rely on it in C: unlike languages such as Scheme that *guarantee* tail call optimization as part of the language specification, C compilers perform tail call optimization only as an *optional, opportunistic* optimization (typically at higher optimization levels like `-O2`), and only when they can prove it's safe/beneficial to do so — it is never guaranteed by the C standard. Relying on it for correctness (e.g., assuming deep tail recursion won't overflow the stack) is unsafe; if stack depth is a genuine concern, convert to an explicit loop instead.

# PROG 101 — Week 9 Resources
## Recursion Pattern Library · BST Reference · Complexity Cheat Sheet

---

## Part 1: The Recursion Design Checklist

Before writing any recursive function, answer these explicitly (write them as comments):

```
1. What is the SIMPLEST possible input? (base case)
   → What do you return/do immediately, without recursing?

2. How does a general input reduce to a SIMPLER instance of the SAME problem?
   → What is the recursive case, and what smaller subproblem does it call?

3. Does the recursive case ALWAYS move strictly closer to the base case,
   for every valid input? (Verify this — don't assume it.)

4. Are there multiple base cases needed? (e.g., empty list AND single element)

5. Does every recursive call's result actually get USED
   (returned, combined, or otherwise incorporated)?
```

---

## Part 2: Recursion Pattern Library

### Linear Recursion (1 recursive call)

```c
/* Template */
ReturnType linear_recursive(Input n) {
    if (/* base case */) return /* base result */;
    return /* combine current with */ linear_recursive(/* smaller n */);
}

/* Examples */
int sum_to_n(int n) {
    if (n <= 0) return 0;
    return n + sum_to_n(n - 1);
}

size_t str_length(const char *s) {
    if (*s == '\0') return 0;
    return 1 + str_length(s + 1);
}
```

### Binary/Multiple Recursion (2+ recursive calls)

```c
long fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);   /* two calls */
}

/* Always consider: are subproblems overlapping? If so, memoize. */
```

### Accumulator Pattern (Tail Recursion)

```c
long sum_acc(int n, long acc) {
    if (n <= 0) return acc;
    return sum_acc(n - 1, acc + n);   /* nothing pending after the call */
}
long sum_to_n_tail(int n) { return sum_acc(n, 0); }
```

### Two-Pointer / Range Recursion

```c
int is_palindrome_range(const char *s, int left, int right) {
    if (left >= right) return 1;
    if (s[left] != s[right]) return 0;
    return is_palindrome_range(s, left + 1, right - 1);
}
```

### Divide-and-Conquer Template

```c
ReturnType divide_conquer(Input problem) {
    if (/* base case: trivially small */) return /* trivial solution */;

    SubInput left_half  = /* divide */;
    SubInput right_half = /* divide */;

    Result left_result  = divide_conquer(left_half);   /* conquer */
    Result right_result = divide_conquer(right_half);  /* conquer */

    return combine(left_result, right_result);         /* combine */
}
```

### Backtracking Template

```c
void backtrack(PartialSolution partial, Choices remaining) {
    if (/* partial is complete */) {
        record_solution(partial);
        return;
    }
    for (/* each choice in remaining */) {
        make_choice(&partial, choice);       /* CHOOSE */
        backtrack(partial, updated_remaining); /* EXPLORE */
        undo_choice(&partial, choice);        /* UNCHOOSE */
    }
}
```

### Tree Recursion Template

```c
ReturnType tree_recursive(const TreeNode *root) {
    if (root == NULL) return /* base case value */;
    ReturnType left  = tree_recursive(root->left);
    ReturnType right = tree_recursive(root->right);
    return /* combine root->data with left and right */;
}
```

---

## Part 3: Binary Search Tree Quick Reference

### The Three Traversals — Same Shape, Different Visit Order

```c
void preorder(TreeNode *r)  { if(!r) return; visit(r); preorder(r->left);  preorder(r->right); }
void inorder(TreeNode *r)   { if(!r) return; inorder(r->left);  visit(r); inorder(r->right);  }
void postorder(TreeNode *r) { if(!r) return; postorder(r->left); postorder(r->right); visit(r); }
```

**Memory aid:** the traversal's name tells you WHEN "order" the root is visited relative to "pre/in/post" its children.

### BST Operations Summary

| Operation | Time (balanced) | Time (degenerate) | Pattern |
|-----------|------------------|---------------------|---------|
| Search | O(log n) | O(n) | Compare, recurse left or right |
| Insert | O(log n) | O(n) | Find empty spot, relink on unwind |
| Delete | O(log n) | O(n) | 3 cases: leaf, one child, two children |
| Min/Max | O(log n) | O(n) | Walk all the way left/right |
| Traversal (all) | O(n) always | O(n) always | Must visit every node |

### The BST Insert/Delete Relinking Pattern

```c
/* This pattern appears in EVERY BST-modifying operation: */
TreeNode *bst_operation(TreeNode *root, int value) {
    if (root == NULL) return /* new node or NULL */;

    if (value < root->data)
        root->left = bst_operation(root->left, value);
    else if (value > root->data)
        root->right = bst_operation(root->right, value);
    else
        /* found it — do the operation-specific work here */;

    return root;   /* always return root so caller can relink */
}
```

---

## Part 4: Complexity Cheat Sheet

| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quicksort (naive pivot) | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Quicksort (randomized/median-of-3) | O(n log n) | O(n log n) | O(n²)* | O(log n) |
| Insertion sort | O(n) | O(n²) | O(n²) | O(1) |
| BST search/insert/delete | O(log n) | O(log n) | O(n) | O(log n) call stack |
| Binary search (array) | O(1) | O(log n) | O(log n) | O(1) or O(log n) if recursive |
| Naive recursive Fibonacci | — | O(2ⁿ) | O(2ⁿ) | O(n) call stack |
| Memoized Fibonacci | — | O(n) | O(n) | O(n) |
| Permutations of n items | — | O(n·n!) | O(n·n!) | O(n) call stack |
| Subsets of n items | — | O(n·2ⁿ) | O(n·2ⁿ) | O(n) call stack |

*Worst case is astronomically unlikely with randomization/median-of-3 in practice, though not impossible in theory.

---

## Part 5: Common Recursion and Tree Bugs

```c
/* BUG 1: Missing base case */
int bad(int n) { return n * bad(n - 1); }   /* never stops */

/* BUG 2: Base case exists but unreachable for some inputs */
int bad2(int n) {
    if (n == 0) return 1;
    return n * bad2(n - 3);   /* skips over 0 for n not divisible by 3 */
}

/* BUG 3: Forgetting to use the recursive call's return value */
int bad3(int n) {
    if (n <= 0) return 0;
    bad3(n - 1);          /* result discarded! */
    return n;              /* wrong — doesn't accumulate */
}

/* BUG 4: Not relinking after BST insert/delete */
void bad_insert(TreeNode *root, int value) {   /* returns void — wrong! */
    if (value < root->data) bad_insert(root->left, value);
    /* if root->left was NULL, this does nothing — new node is lost */
}
/* FIX: return TreeNode* and relink: root->left = bst_insert(root->left, value); */

/* BUG 5: Freeing tree nodes in the wrong order */
void bad_free(TreeNode *root) {
    if (!root) return;
    free(root);
    bad_free(root->left);    /* use-after-free: root was just freed */
    bad_free(root->right);
}
/* FIX: postorder — free children BEFORE the node itself */

/* BUG 6: Naive BST validity check (only checks immediate children) */
bool bad_is_valid(TreeNode *root) {
    if (!root) return true;
    if (root->left && root->left->data >= root->data) return false;
    if (root->right && root->right->data <= root->data) return false;
    return bad_is_valid(root->left) && bad_is_valid(root->right);
    /* MISSES violations further down that break the FULL ancestor chain */
}
/* FIX: pass down a (min, max) range that narrows at each level */

/* BUG 7: Forgetting the "unchoose" step in backtracking */
void bad_backtrack(int arr[], int n, int start) {
    for (int i = start; i < n; i++) {
        swap(&arr[start], &arr[i]);
        bad_backtrack(arr, n, start + 1);
        /* MISSING: swap back! Array stays scrambled for next iteration */
    }
}
```

---

## Part 6: Debugging Recursion with GDB

```bash
gdb ./program
```

```
(gdb) break factorial          # break every time factorial is called
(gdb) run
(gdb) print n                  # see the current call's argument
(gdb) continue                 # continue to the NEXT recursive call
(gdb) print n                  # see it decrease each time
(gdb) backtrace                # see EVERY active stack frame at once —
                                 # this shows the full recursion depth,
                                 # one line per active call

# To see the full recursive call chain clearly:
(gdb) backtrace full           # includes local variables at each frame
```

`backtrace` is the single most useful GDB command for understanding recursion — it shows you exactly how many frames are currently on the stack and what argument each one holds, making the abstract "recursion tree" concrete and visible.

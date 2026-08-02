# CS 101 · Lecture 14 (Week 4, Lecture 2)
## Recursive Algorithms: Trees, Patterns, and Iteration Conversion

**Week 4 · Thursday**
*"The art of recursion is knowing when to stop." — anonymous*

---

## 0. From Concept to Algorithm

Wednesday established what recursion is and why it works. Today we build fluency: more recursive algorithms, how to analyze them using recursion trees, and when and how to convert recursive solutions to iterative ones.

---

## 1. Counting Recursive Calls: The Recursion Tree Method

For any recursive function, you can determine its exact call count by drawing its recursion tree and counting nodes.

**Rule:** The number of recursive calls equals the number of non-leaf nodes in the tree. Total calls (including leaves) is the total node count.

### Example: `count_calls(n)` with one recursive call

```python
def linear_recursive(n):
    if n == 0:
        return 0
    return 1 + linear_recursive(n - 1)
```

Tree for n=4:
```
linear_recursive(4)
    linear_recursive(3)
        linear_recursive(2)
            linear_recursive(1)
                linear_recursive(0)  ← leaf
```

Total calls: n+1. This is **O(n) — linear recursion**.

### Example: two recursive calls

```python
def binary_recursive(n):
    if n == 0:
        return 1
    return binary_recursive(n-1) + binary_recursive(n-1)
```

Tree for n=3:
```
                     binary(3)
                  /            \
          binary(2)           binary(2)
          /      \             /      \
      binary(1) binary(1) binary(1) binary(1)
      /\        /\         /\        /\
     0  0      0  0       0  0      0  0
```

Total calls at depth d: 2^d. Total calls: 1 + 2 + 4 + ... + 2^n = 2^(n+1) - 1 = **O(2^n) — exponential**.

### Example: splitting in half

```python
def log_recursive(lst):
    if len(lst) <= 1:
        return lst
    mid = len(lst) // 2
    left  = log_recursive(lst[:mid])
    right = log_recursive(lst[mid:])
    return left + right  # just merges — no useful computation here, but illustrates the pattern
```

Tree for n=8 elements:
```
                    [8 elements]
                /               \
         [4 elements]        [4 elements]
         /      \              /      \
    [2 elems] [2 elems]  [2 elems] [2 elems]
     /  \      /  \       /  \      /  \
   [1] [1]   [1] [1]   [1] [1]   [1] [1]
```

Depth: log₂n. Nodes at each level: 2^d (for d = 0, 1, ..., log₂n). Total nodes: 2n-1 = **O(n)**.

---

## 2. Merge Sort: A Complete Recursive Algorithm

Merge sort is one of the most important algorithms in CS. It uses the **divide and conquer** strategy:

1. **Divide:** split the list in half
2. **Conquer:** recursively sort each half
3. **Combine:** merge the two sorted halves

```python
def merge_sort(lst):
    """
    Return a new sorted list using merge sort.
    Time complexity: O(n log n).
    Space complexity: O(n).

    Correctness proof:
        Base case: list of 0 or 1 elements is already sorted.
        Inductive step: assume merge_sort correctly sorts any list of size < n.
        Then merge_sort(lst[:mid]) and merge_sort(lst[mid:]) are sorted (by IH).
        merge() of two sorted lists produces a sorted list.
        Therefore merge_sort(lst) is sorted. ✓
    """
    # Base case: 0 or 1 elements are trivially sorted
    if len(lst) <= 1:
        return lst[:]   # return a copy

    # Divide
    mid   = len(lst) // 2
    left  = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])

    # Combine
    return merge(left, right)


def merge(left, right):
    """
    Merge two sorted lists into one sorted list.
    Time complexity: O(len(left) + len(right)).

    Invariant: result contains all elements of left[:i] and right[:j],
               in sorted order, at every step.
    """
    result = []
    i = 0   # index into left
    j = 0   # index into right

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements (at most one side has any)
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# Tests:
assert merge_sort([])          == []
assert merge_sort([1])         == [1]
assert merge_sort([3, 1, 2])   == [1, 2, 3]
assert merge_sort([5,4,3,2,1]) == [1, 2, 3, 4, 5]
assert merge_sort([3,3,1,2,3]) == [1, 2, 3, 3, 3]
```

### Merge Sort Recursion Tree (n=8):

```
                         [8]
                      /       \
                   [4]          [4]
                 /    \        /    \
              [2]     [2]    [2]    [2]
             / \      / \   / \    / \
           [1] [1]  [1][1] [1][1] [1][1]
```

- **Depth:** log₂n levels
- **Work per level:** O(n) total (merging all pairs at a level touches all n elements)
- **Total work:** O(n) × O(log n) levels = **O(n log n)**

This is optimal for comparison-based sorting — no comparison sort can do better than O(n log n) in the worst case. (We'll prove this lower bound in CS 301.)

---

## 3. Recursive Descent: Parsing Expressions

A **recursive descent parser** uses mutual recursion to parse nested structures. Here is a parser for arithmetic expressions like `3 + 4 * 2`:

Grammar (informal):
```
expression = term (('+' | '-') term)*
term       = factor (('*' | '/') factor)*
factor     = number | '(' expression ')'
```

```python
def parse_expression(tokens, pos=0):
    """Parse an addition/subtraction expression."""
    value, pos = parse_term(tokens, pos)

    while pos < len(tokens) and tokens[pos] in ('+', '-'):
        op = tokens[pos]
        pos += 1
        right, pos = parse_term(tokens, pos)
        if op == '+':
            value += right
        else:
            value -= right

    return value, pos


def parse_term(tokens, pos):
    """Parse a multiplication/division expression."""
    value, pos = parse_factor(tokens, pos)

    while pos < len(tokens) and tokens[pos] in ('*', '/'):
        op = tokens[pos]
        pos += 1
        right, pos = parse_factor(tokens, pos)
        if op == '*':
            value *= right
        else:
            value /= right

    return value, pos


def parse_factor(tokens, pos):
    """Parse a number or parenthesized expression."""
    token = tokens[pos]
    if token == '(':
        value, pos = parse_expression(tokens, pos + 1)
        assert tokens[pos] == ')', f"Expected ')' at position {pos}"
        return value, pos + 1
    else:
        return float(token), pos + 1


def evaluate(expr_string):
    """Tokenize and evaluate an arithmetic expression string."""
    import re
    tokens = re.findall(r'\d+\.?\d*|[+\-*/()]', expr_string)
    result, _ = parse_expression(tokens)
    return result


print(evaluate("3 + 4 * 2"))      # 11.0  (multiplication before addition)
print(evaluate("(3 + 4) * 2"))    # 14.0  (parentheses override)
print(evaluate("10 / 2 + 3"))     # 8.0
```

This is how compilers parse source code (CS 211, Year 2). The mutual recursion (`parse_expression` calls `parse_term` which calls `parse_factor` which calls `parse_expression`) is elegantly correct because the grammar is recursive.

---

## 4. Recursive Data Structures: Binary Trees (Preview)

Recursion is natural for **recursive data structures** — structures defined in terms of themselves. A binary tree is:
- Either empty (None), OR
- A node with a value, a left subtree, and a right subtree

```python
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left  = left
        self.right = right

# Build a tree:
tree = TreeNode(4,
    left  = TreeNode(2, TreeNode(1), TreeNode(3)),
    right = TreeNode(6, TreeNode(5), TreeNode(7))
)

#        4
#       / \
#      2   6
#     / \ / \
#    1  3 5  7
```

Recursive operations on trees are naturally elegant:

```python
def tree_sum(node):
    """Sum all values in a binary tree."""
    if node is None:    # base case: empty tree
        return 0
    return node.value + tree_sum(node.left) + tree_sum(node.right)


def tree_height(node):
    """Return the height of a binary tree (0 for a leaf)."""
    if node is None:
        return -1   # height of empty tree is -1 by convention
    return 1 + max(tree_height(node.left), tree_height(node.right))


def tree_contains(node, target):
    """Return True if target exists anywhere in the tree."""
    if node is None:
        return False
    if node.value == target:
        return True
    return tree_contains(node.left, target) or tree_contains(node.right, target)


def inorder(node):
    """Return all values in sorted order (for a BST)."""
    if node is None:
        return []
    return inorder(node.left) + [node.value] + inorder(node.right)


assert tree_sum(tree)      == 28
assert tree_height(tree)   == 2
assert tree_contains(tree, 5) == True
assert tree_contains(tree, 9) == False
assert inorder(tree)       == [1, 2, 3, 4, 5, 6, 7]
```

We'll study binary trees deeply in Week 7 (Data Structures I) and in CS 102. For now: note that every tree operation follows the same recursive pattern: base case on None, then combine left result, node value, and right result.

---

## 5. Converting Recursion to Iteration

Every recursive function can be rewritten as an iterative one, using an **explicit stack**. This is important when:
- The recursion is too deep (hits Python's limit)
- Performance is critical (function call overhead is non-trivial)
- You need to pause/resume the computation

### Conversion pattern: depth-first search on a tree:

```python
# Recursive version:
def dfs_recursive(node, target):
    if node is None:
        return False
    if node.value == target:
        return True
    return dfs_recursive(node.left, target) or dfs_recursive(node.right, target)


# Iterative equivalent — use an explicit stack:
def dfs_iterative(root, target):
    stack = [root]    # initialize with the root
    while stack:
        node = stack.pop()   # pop the top node (simulates returning from recursion)
        if node is None:
            continue
        if node.value == target:
            return True
        stack.append(node.left)
        stack.append(node.right)
    return False
```

The explicit stack mimics the call stack. Pushing a node simulates a recursive call; popping simulates returning from one.

### Converting factorial:

```python
# Recursive:
def factorial_recursive(n):
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)


# Iterative (uses accumulator — no explicit stack needed for linear recursion):
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

For **linear recursion** (one recursive call), the conversion is always a simple loop. For **binary recursion** (two calls), you need an explicit stack.

---

## 6. Mutual Recursion

Two (or more) functions can be mutually recursive, each calls the other.

```python
def is_even(n):
    """Return True if n is even."""
    if n == 0:
        return True
    return is_odd(n - 1)

def is_odd(n):
    """Return True if n is odd."""
    if n == 0:
        return False
    return is_even(n - 1)

assert is_even(4) == True
assert is_odd(7)  == True
```

This is pedagogically interesting but not efficient (O(n) calls for a trivial operation). The real use case is recursive descent parsing (Section 3 above), where the mutual recursion directly encodes the grammar's recursive structure.

---

## 7. Recognizing When to Use Recursion

Recursion is the right tool when the problem has a **recursive structure** — it is naturally defined in terms of smaller versions of itself.

**Use recursion when:**
- The data structure is recursive (trees, graphs, nested lists)
- The algorithm is naturally divide-and-conquer (merge sort, binary search)
- The problem's mathematical definition is inductive (Fibonacci, factorial, GCD)
- The grammar/syntax is recursive (parsers, expression evaluators)

**Use iteration when:**
- The recursion is simple and linear (factorial, sum — just use a loop)
- Depth could be large (> 900) in Python
- Performance is the primary concern (iteration avoids function call overhead)
- The logic is inherently sequential (scanning a file, processing input line by line)

**The test:** If you find yourself writing a loop that simulates recursive calls by maintaining an explicit stack, consider whether recursion would be clearer. If the recursive version would hit Python's depth limit, keep the iterative version with the explicit stack.

---

## 8. The Power of Recursion: Thinking Differently

The deepest value of learning recursion is not practical — it is a change in how you think about problems.

**Before recursion:** "How do I process this list? I'll iterate through it."

**After recursion:** "A list is either empty, or it's a head element and a tail list. I can solve the head case and assume the tail case is solved."

This second way of thinking — **structural induction** — lets you write proofs and implementations simultaneously. It is the foundation of functional programming, type theory, and formal verification.

When you take CS 211 (Programming Languages), CS 301 (Theory of Computation), and CS 412 (Formal Methods), the recursive thinking you develop this week is the foundation.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Recursion tree | Visualizes all calls; count nodes to count calls |
| Linear recursion | One call per level → O(n) total calls |
| Binary recursion | Two calls per level → O(2^n) total calls |
| Divide-and-conquer | Split in half → O(n) calls, O(log n) depth |
| Merge sort | O(n log n); optimal for comparison-based sorting |
| Recursive descent | Mutual recursion encodes grammar structure |
| Tree recursion | Empty = base case; left + node + right = recursive case |
| Iterative conversion | Explicit stack simulates call stack for any recursion |
| Mutual recursion | Two functions that call each other; natural for grammars |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Trace merge sort on `[38, 27, 43, 3, 9, 82, 10]`, drawing the full recursion tree. State the depth of the tree and the total number of elements processed per level.

**2. (Explain.)** Both functions below compute the same thing. One is exponential and one is linear. Identify which is which and explain the difference in terms of the recursion tree.

```python
def a(n):
    if n < 2: return n
    return a(n-1) + a(n-2)

def b(n, memo={}):
    if n < 2: return n
    if n not in memo:
        memo[n] = b(n-1) + b(n-2)
    return memo[n]
```

**3. (Build.)** Convert this recursive function to an iterative one using an explicit stack. Explain what the stack replaces.

```python
def depth(node):
    if node is None:
        return 0
    return 1 + max(depth(node.left), depth(node.right))
```

**4. (Stretch.)** Predict the output, then explain why neither function can be written without the other.

```python
def is_even(n):
    return True if n == 0 else is_odd(n - 1)

def is_odd(n):
    return False if n == 0 else is_even(n - 1)

print(is_even(4), is_odd(7), is_even(7))
```


### Answers

**1.**

```
                 [38,27,43,3,9,82,10]
            /                         \
      [38,27,43,3]                    [9,82,10]
       /        \                  /       \
   [38,27]      [43,3]            [9,82]      [10]
    /    \      /    \          /    \
 [38]  [27]  [43]   [3]        [9]   [82]
```

Merging back up: `[27,38]`, `[3,43]` → `[3,27,38,43]`; `[9,82]`, `[10]` → `[9,10,82]`; final merge → **`[3, 9, 10, 27, 38, 43, 82]`**.

Depth is **⌈log₂ 7⌉ = 3** levels of splitting. At *every* level the merges together touch all 7 elements — that is the key observation, and it does not depend on how the elements are distributed between the two halves. So the total work is (elements per level) × (number of levels) = **Θ(n log n)**.

This "count the work per level, then multiply by the depth" method is the recursion-tree technique, and it is the intuition the Master Theorem in L20 makes rigorous.

**2.** `a` is **Θ(φⁿ)**, `b` is **Θ(n)**.

`a`'s recursion tree contains repeated identical subtrees: `a(5)` computes `a(3)` twice, `a(2)` three times, and so on, each time from scratch. The tree has ~φⁿ nodes because nothing is remembered between branches.

`b` records each result the first time it is computed. Every value `2..n` is computed exactly once and read thereafter, so the tree collapses to a **path** of n nodes with the second branch of each node becoming a table lookup. That is the whole of memoisation: trade Θ(n) space for an exponential reduction in time.

But `b` has a real bug — **the mutable default argument from L11**. The `memo` dict is created once and shared by every call to `b`, forever. Here it is benign, since Fibonacci values never change, but it leaks memory for the life of the process and would be a correctness bug for any function whose answers depend on anything else. Write it as `memo=None` with `if memo is None: memo = {}`, or use `@functools.cache` and let the standard library own the table.

**3.**

```python
def depth(root):
    if root is None:
        return 0
    stack = [(root, 1)]        # (node, depth-of-that-node)
    best = 0
    while stack:
        node, d = stack.pop()
        best = max(best, d)
        if node.left:
            stack.append((node.left, d + 1))
        if node.right:
            stack.append((node.right, d + 1))
    return best
```

The explicit stack replaces **the call stack**. Every recursive call was implicitly pushing a frame holding the local variables — here, which node we are on and how deep we are — and popping it on return. Making it explicit means storing exactly those values in a list you control.

That control is the reason to do it: the explicit version is bounded only by heap memory, so it handles trees far deeper than Python's 1000-frame limit. The cost is that the code no longer reads like the definition of the problem. Note also that this version accumulates a maximum as it goes rather than combining results on the way back up — converting a *post-order* recursion faithfully requires a second stack or a visited marker, which is why this rewrite is easier for some shapes than others.

**4.** `True True False`.

This is **mutual recursion**: neither function calls itself, but together they form a cycle. `is_even(4)` → `is_odd(3)` → `is_even(2)` → `is_odd(1)` → `is_even(0)` → `True`.

Two things worth noticing. First, Python resolves `is_odd` inside `is_even` at **call time**, not definition time, which is why the forward reference in the first `def` is legal even though `is_odd` does not exist yet when that line runs. In C you would need a forward declaration; PROG 101 Week 3 covers exactly this.

Second, they *can* be written separately — `n % 2 == 0` is the sane implementation — so this pair is a demonstration rather than a necessity. Mutual recursion earns its place where the *problem* is genuinely two intertwined cases, and the canonical example is recursive-descent parsing (§3): `parse_expression` calls `parse_term`, which calls `parse_factor`, which calls `parse_expression` again for a parenthesised subexpression. That cycle mirrors the grammar's own recursion and cannot be flattened without reimplementing the grammar.



---

## Reading

- **Guttag, Ch. 4.3** — Recursion (continue)
- **Guttag, Ch. 5** — Structured types (lists — useful for recursive list processing)

---

*CS 101 · Week 4 · Lecture 14 (Thu) · © CSE Department*

# CS 101 · Lecture 24 (Week 7, Lecture 3)
## Stack and Queue ADTs, Deques, and Choosing the Right Structure

**Week 7 · Friday**
*"A stack is defined by two operations: push and pop, with LIFO semantics. This is the ADT. You can implement it with an array or a linked list — both satisfy the specification." — CS 101*

**Date:** Friday 13 November 2026 · 09:00–09:50 · Week 7

---

## 0. From Building Blocks to Abstractions

Wednesday gave you Python's dynamic array. Thursday gave you linked lists built from scratch. Today we use both to implement two of the most important ADTs in computer science: the **Stack** and the **Queue**. These aren't new data — they're new *disciplines* for accessing existing data.

---

## 1. The Stack ADT — LIFO (Last In, First Out)

**Specification:**
- `push(x)`: add x to the top of the stack
- `pop()`: remove and return the top element (raises an error if empty)
- `peek()`: return the top element without removing it
- `is_empty()`: return True if the stack has no elements
- `size()`: return the number of elements

**The defining property:** the most recently pushed element is always the first one popped — Last In, First Out.

### Real-World Analogies

- A stack of plates: you add to the top, you remove from the top
- Your browser's "back" button: each page visited is pushed; going back pops
- Function call stack (Week 3!): each call pushes a frame; each return pops one

### Implementation 1: Stack Using a Python List

```python
class Stack:
    """
    Stack ADT implemented using a Python list.

    Design choice: use the END of the list as the "top" of the stack.
    Why? Because list.append() and list.pop() (no argument) are BOTH
    O(1) amortized — using the FRONT would make every operation O(n)!
    """

    def __init__(self):
        self._data = []

    def push(self, x):
        """Add x to the top. O(1) amortized."""
        self._data.append(x)

    def pop(self):
        """Remove and return the top element. O(1)."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        """Return the top element without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def __repr__(self):
        return f"Stack({self._data})"


# Tests:
s = Stack()
s.push(1)
s.push(2)
s.push(3)
print(s)             # Stack([1, 2, 3])
print(s.pop())       # 3  (last in, first out)
print(s.peek())      # 2
print(s.size())       # 2
```

**Why the end of the list, not the front?** If we used `insert(0, x)` for push and `pop(0)` for pop, both operations would be O(n) (Wednesday's lecture). By choosing the *end* as the "top," both `append()` and `pop()` are O(1) amortized. **The choice of which end of an array to treat as "the top" is a critical design decision** — get it backwards and your stack silently becomes O(n) per operation instead of O(1).

### Implementation 2: Stack Using a Linked List

```python
class LinkedStack:
    """
    Stack ADT implemented using a singly linked list.

    Design choice: use the HEAD of the linked list as the "top."
    Why? prepend/remove-from-head are BOTH O(1) for a singly linked list.
    (Using the tail would require O(n) traversal for pop, since a singly
    linked list can't efficiently find the second-to-last node.)
    """

    class _Node:
        __slots__ = ("data", "next")
        def __init__(self, data, next=None):
            self.data = data
            self.next = next

    def __init__(self):
        self._head = None
        self._size = 0

    def push(self, x):
        """O(1) — prepend to the head."""
        self._head = self._Node(x, self._head)
        self._size += 1

    def pop(self):
        """O(1) — remove from the head."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        data = self._head.data
        self._head = self._head.next
        self._size -= 1
        return data

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._head.data

    def is_empty(self):
        return self._head is None

    def size(self):
        return self._size


# Both implementations satisfy the same ADT — verify equivalent behavior:
s1 = Stack()
s2 = LinkedStack()
for x in [1, 2, 3, 4]:
    s1.push(x)
    s2.push(x)

assert s1.pop() == s2.pop() == 4
assert s1.pop() == s2.pop() == 3
print("Both implementations behave identically — same ADT, different internals.")
```

---

## 2. The Queue ADT — FIFO (First In, First Out)

**Specification:**
- `enqueue(x)`: add x to the back
- `dequeue()`: remove and return the element at the front (raises an error if empty)
- `peek()`: return the front element without removing it
- `is_empty()`: return True if empty
- `size()`: return the number of elements

**The defining property:** the first element added is always the first one removed — First In, First Out.

### Real-World Analogies

- A line at a store: first person in line is served first
- A print queue: documents print in the order they were submitted
- BFS (Breadth-First Search) in graphs (you'll formalize this in CS 102): process nodes in the order discovered

### Why a Python List Makes a BAD Queue

```python
class BadQueue:
    """DON'T DO THIS — demonstrates a naive but inefficient queue."""

    def __init__(self):
        self._data = []

    def enqueue(self, x):
        self._data.append(x)     # O(1) — fine

    def dequeue(self):
        return self._data.pop(0)  # O(n) — BAD! Must shift every remaining element!
```

Every `dequeue()` call is O(n), because removing from the **front** of a Python list requires shifting all remaining elements left by one position (Wednesday's lecture). For a queue processing n items, this makes the total cost O(n²) — often catastrophically slow for large queues.

### Implementation: Queue Using `collections.deque`

```python
from collections import deque

class Queue:
    """
    Queue ADT implemented using collections.deque.

    deque (double-ended queue) is implemented internally as a doubly
    linked list of blocks, giving O(1) operations at BOTH ends.
    """

    def __init__(self):
        self._data = deque()

    def enqueue(self, x):
        """Add to the back. O(1)."""
        self._data.append(x)

    def dequeue(self):
        """Remove and return from the front. O(1) — NOT O(n)!"""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)


q = Queue()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
print(q.dequeue())   # 1  (first in, first out)
print(q.dequeue())   # 2
print(q.size())       # 1
```

**Why does `deque` achieve O(1) at both ends?** Internally, `collections.deque` is implemented as a doubly linked list of fixed-size blocks (not individual nodes like our hand-rolled version, for better memory efficiency and cache performance) — combining the array's memory efficiency with the doubly linked list's O(1) end operations. This is exactly the tradeoff discussed in Thursday's lecture, engineered by CPython's developers for maximum practical performance.

### Implementation: Queue Using a Linked List (Educational)

```python
class LinkedQueue:
    """
    Queue ADT implemented using our own doubly linked list concept
    (a singly linked list WITH a tail pointer, since we only need
    O(1) insert-at-tail and O(1) remove-from-head — not full
    bidirectional traversal).
    """

    class _Node:
        __slots__ = ("data", "next")
        def __init__(self, data, next=None):
            self.data = data
            self.next = next

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def enqueue(self, x):
        """O(1) — append at the tail."""
        new_node = self._Node(x)
        if self._tail is None:
            self._head = new_node
        else:
            self._tail.next = new_node
        self._tail = new_node
        self._size += 1

    def dequeue(self):
        """O(1) — remove from the head."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        data = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return data

    def is_empty(self):
        return self._head is None

    def size(self):
        return self._size
```

**Why enqueue at the tail and dequeue at the head (not the reverse)?** Because a singly linked list gives us O(1) insertion at the head OR the tail (with a tail pointer), but only O(1) *removal* from the head (removal from the tail requires finding the new tail, which needs traversal — Thursday's lecture again). So: enqueue where insertion is cheap (tail), dequeue where removal is cheap (head). This asymmetric design is exactly matched to what a singly linked list can do efficiently.

---

## 3. The Deque ADT — Double-Ended Queue

A **deque** generalizes both stack and queue: you can add/remove from **either** end, all in O(1).

```python
from collections import deque

d = deque([1, 2, 3, 4, 5])

d.append(6)         # add to the right:  [1,2,3,4,5,6]
d.appendleft(0)     # add to the left:   [0,1,2,3,4,5,6]
d.pop()             # remove from right: 6, deque is [0,1,2,3,4,5]
d.popleft()         # remove from left:  0, deque is [1,2,3,4,5]

print(d)            # deque([1, 2, 3, 4, 5])
print(d[2])         # O(n) — indexing into a deque is NOT O(1)!
```

**Important caveat:** unlike a Python `list`, indexing into the *middle* of a `deque` (`d[i]` for arbitrary `i`) is **O(n)**, not O(1) — because internally it's a linked structure of blocks, not one contiguous array. Use `deque` when you need fast operations at the ends; use `list` when you need fast random access by index. Choosing wrong silently costs you an order of magnitude in performance.

A deque can implement **both** a stack (use one end consistently) and a queue (use both ends) — this is why `collections.deque` is Python's general-purpose recommendation for both use cases in practice.

---

## 4. Comparing All Implementations — Complete Decision Table

| ADT | Best Implementation | Why |
|-----|---------------------|-----|
| Stack | Python `list` (use `.append()`/`.pop()`) | Both operations O(1) amortized; simplest code |
| Queue | `collections.deque` (use `.append()`/`.popleft()`) | O(1) at both ends; avoids the O(n) `pop(0)` trap |
| Deque (need both ends) | `collections.deque` | Purpose-built for this; O(1) at both ends |
| Need fast random access by index | Python `list` | O(1) indexing; deque's indexing is O(n) |
| Need fast insert/remove anywhere given a node reference | Doubly linked list (hand-rolled or via specialized library) | O(1) given the node; searching for the node is still O(n) |

---

## 5. A Complete Application: Balanced Parentheses Checker

The Stack ADT solves a classic problem elegantly: checking whether parentheses (and brackets) are balanced.

```python
def is_balanced(expression):
    """
    Return True if all brackets in expression are balanced and properly nested.

    Supports (), [], {}.

    Algorithm:
        For each character:
            If it's an opening bracket: push it
            If it's a closing bracket: pop and check it matches the corresponding opener
        At the end: the stack must be empty (all openers matched)

    Examples:
        is_balanced("(a + b) * [c - d]")   → True
        is_balanced("(a + [b)")             → False  (wrong nesting)
        is_balanced("((a)")                 → False  (unmatched opener)
        is_balanced("a)")                   → False  (unmatched closer)
    """
    pairs = {')': '(', ']': '[', '}': '{'}
    openers = set(pairs.values())

    stack = Stack()

    for char in expression:
        if char in openers:
            stack.push(char)
        elif char in pairs:
            if stack.is_empty():
                return False           # closer with no matching opener
            top = stack.pop()
            if top != pairs[char]:
                return False           # wrong type of bracket
    return stack.is_empty()             # all openers must have been matched


assert is_balanced("(a + b) * [c - d]") == True
assert is_balanced("(a + [b)")          == False
assert is_balanced("((a)")              == False
assert is_balanced("a)")                == False
assert is_balanced("")                  == True
print("Balanced parentheses checker works correctly.")
```

This exact algorithm (stack-based bracket matching) is used inside every compiler and parser you will ever encounter — including Python's own interpreter, which must verify your code's syntax is well-formed before executing it.

---

## 6. A Complete Application: Queue-Based Task Scheduling

```python
def round_robin_schedule(tasks, time_slice):
    """
    Simulate round-robin CPU scheduling using a Queue.

    Each task is (name, remaining_time). Process each task for up to
    time_slice units; if not finished, re-enqueue it at the back.

    Returns the order in which tasks completed.

    This is EXACTLY how operating systems schedule processes on a
    single CPU core with time-sharing (you'll study this formally
    in CS 202, Operating Systems).
    """
    q = Queue()
    for task in tasks:
        q.enqueue(task)

    completion_order = []

    while not q.is_empty():
        name, remaining = q.dequeue()
        if remaining <= time_slice:
            completion_order.append(name)
        else:
            q.enqueue((name, remaining - time_slice))

    return completion_order


tasks = [("A", 5), ("B", 3), ("C", 8)]
order = round_robin_schedule(tasks, time_slice=4)
print(order)   # ['B', 'A', 'C']
```

---

## Summary

| ADT | Operations | LIFO/FIFO | Best Backing Structure |
|-----|-----------|-----------|--------------------------|
| Stack | push, pop, peek | LIFO | Python list (end as top) |
| Queue | enqueue, dequeue, peek | FIFO | `collections.deque` |
| Deque | append/pop at both ends | Neither (general) | `collections.deque` |

| Key Insight | Detail |
|-------------|--------|
| Same ADT, different implementations | Stack works identically whether backed by array or linked list |
| Choice of "which end" matters enormously | Wrong choice turns O(1) operations into O(n) |
| `deque` beats `list` for front operations | O(1) vs O(n) — use `deque` whenever you need queue behavior |
| Real applications | Bracket matching, function call stacks, undo/redo, task scheduling, BFS |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Trace the balanced-parentheses checker on `"([)]"` and on `"([])"`, showing the stack at each step. Explain why a simple counter cannot replace the stack.

**2. (Explain.)** Implementing a queue with a Python list and `pop(0)` gives O(n) dequeue. Explain what `collections.deque` does differently, and predict the speedup on 50,000 dequeue operations over a 100,000-element queue.

**3. (Build.)** Implement a queue using **two stacks**, with amortised O(1) enqueue and dequeue. Prove the amortised bound.

**4. (Stretch.)** Every recursive function can be rewritten with an explicit stack. Explain what the stack must hold, and why converting a *post-order* traversal is harder than converting a pre-order one.


### Answers

**1.** On `"([])"`: push `(` → stack `['(']`; push `[` → `['(', '[']`; see `]`, pop `[`, they match → `['(']`; see `)`, pop `(`, they match → `[]`. Stack empty at the end ⇒ **balanced**. ✓

On `"([)]"`: push `(` → `['(']`; push `[` → `['(', '[']`; see `)`, pop `[` — **mismatch**, `)` does not close `[` ⇒ **not balanced**. ✓

A counter fails because it tracks only *how many* brackets are open, not *which kinds, in what order*. Counting `(`/`)` and `[`/`]` separately, `"([)]"` gives one of each opened and one of each closed — perfectly balanced by the counts, and wrong. The counter cannot detect **interleaving**.

The stack works because it enforces the actual rule: brackets must close in **reverse order of opening**, which is precisely LIFO. This is why nesting problems and stacks are the same problem — and why the call stack is a stack, since function calls also complete in reverse order of invocation.

Note both failure modes need handling: a closer with an empty stack (`")("`) and a non-empty stack at the end (`"(("`). A checker that tests only one reports half the malformed inputs as fine.

**2.** A Python list is a contiguous array, so `pop(0)` removes the first slot and **shifts every remaining element down one** — Θ(n) per dequeue, Θ(n²) for the workload.

`collections.deque` is a **doubly linked list of fixed-size blocks** (64 slots each in CPython). It maintains pointers to both ends, so `popleft` and `appendleft` adjust an index within the leading block and occasionally unlink a whole block — **O(1) with no shifting**. The block structure is a deliberate hybrid: it keeps most of the array's cache locality while avoiding the array's front-insertion cost.

**Prediction:** roughly two to three orders of magnitude. Measured:

```python
import timeit
timeit.timeit('d.popleft(); d.append(1)',
              setup='from collections import deque; d=deque(range(100000))', number=50000)
timeit.timeit('a.pop(0); a.append(1)', setup='a=list(range(100000))', number=50000)
```

This typically shows a few hundred-fold difference. The trade: `deque` gives up O(1) random access — `d[k]` for a middle `k` is O(n), since it must walk the blocks. **Use `deque` when you touch the ends and a list when you index the middle**; `deque` is the right default for queues, BFS frontiers, and sliding windows.

**3.**

```python
class Queue:
    def __init__(self):
        self._in = []    # push here
        self._out = []   # pop here

    def enqueue(self, x):
        self._in.append(x)

    def dequeue(self):
        if not self._out:                 # only when out is empty
            while self._in:
                self._out.append(self._in.pop())
        if not self._out:
            raise IndexError("dequeue from empty queue")
        return self._out.pop()
```

Reversing the order twice — once by pushing onto `_in`, once by transferring to `_out` — turns LIFO into FIFO.

**Amortised proof (accounting method).** Charge each `enqueue` **3 units**: 1 to push onto `_in`, and 2 held in credit. Every element is moved from `_in` to `_out` **at most once in its lifetime**, and that move costs 1 pop + 1 push = 2 units, paid entirely by the stored credit. `dequeue` then costs 1 unit for the final pop. So every operation is paid for by O(1) charged at enqueue time ⇒ **O(1) amortised**. ∎

The critical detail is the guard `if not self._out`. Transferring on *every* dequeue would move elements repeatedly and give O(n) per operation; transferring only when `_out` is exhausted is what makes "at most once" true. A single `dequeue` can still cost Θ(n) — amortised is a claim about sequences, not about individual calls.

**4.** The stack must hold **everything a call frame holds**: the arguments, the local variables still needed after the recursive call returns, and — critically — a marker for **where to resume**, since a function with two recursive calls has two distinct return points.

**Pre-order is easy** because all the work happens *before* the recursion. Visit the node, then push the children; nothing needs to be remembered across the call, so the stack holds only nodes:

```python
stack = [root]
while stack:
    node = stack.pop()
    visit(node)
    if node.right: stack.append(node.right)
    if node.left:  stack.append(node.left)
```

**Post-order is harder** because the work happens *after both* recursive calls return. When you pop a node you cannot tell whether you are arriving at it for the first time (children not yet processed) or returning to it (children done). The implicit call stack knew, via the program counter; an explicit stack of bare nodes does not.

The fix is to **store the resume state alongside the node** — push `(node, visited_flag)` and re-push with the flag set, or keep a `last_visited` reference. This is exactly what a real call frame does with its return address, and building it by hand is how compilers implement recursion in the first place.

The general principle: converting recursion to iteration is mechanical, but **the amount of state the stack must carry equals the amount of work pending after the recursive call.** Tail recursion needs none, which is why it collapses to a loop with no stack at all.



---

## Reading

- **Guttag** — supplementary stack/queue material if covered in your edition
- **Python docs — collections.deque:** https://docs.python.org/3/library/collections.html#collections.deque
- **CLRS, Ch. 10.1** — Stacks and Queues (formal pseudocode treatment)

---

*CS 101 · Week 7 · Lecture 24 (Fri) · © CSE Department*

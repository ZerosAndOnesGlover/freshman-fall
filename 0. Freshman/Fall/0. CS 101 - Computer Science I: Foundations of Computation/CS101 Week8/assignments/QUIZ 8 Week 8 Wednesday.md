# CS 101 — Quiz 8
## Week 8, Wednesday — In-Class Assessment

**Duration:** 10 minutes (first 10 minutes of Wednesday lecture)
**Format:** Written — closed book, closed notes
**Covers:** Week 7 material: ADTs, dynamic arrays, linked lists, stacks, queues, deques

---

### Question 1 (2 points)

What is an Abstract Data Type? Give the Queue ADT's specification in one sentence (name its operations and its ordering discipline).

---

### Question 2 (2 points)

State the time complexity of each Python list operation:

`lst.append(x)`: O(___)
`lst.insert(0, x)`: O(___)
`lst.pop()`: O(___)
`lst.pop(0)`: O(___)

Why are the last two different from the first two?

---

### Question 3 (2 points)

A singly linked list has a `tail` pointer but each node has only a `next` pointer (no `prev`). What is the time complexity of `remove_last()` for this structure? Explain precisely why, and state what additional pointer would fix it.

---

### Question 4 (2 points)

A classmate implements a Queue using a Python list, with `enqueue` calling `lst.append(x)` and `dequeue` calling `lst.pop(0)`. Is this a VALID implementation of the Queue ADT (does it obey FIFO)? Is it a GOOD implementation? Justify both answers.

---

### Question 5 (2 points)

Why is indexing into the middle of a `collections.deque` (e.g., `d[500]` for a deque of 1000 elements) O(n) rather than O(1), unlike a Python list?

---

**Total: 10 points**

---

## Answer Key (Instructor Copy)

**Q1:** An ADT is a specification of behavior (operations and their guarantees) independent of any particular implementation. Queue ADT: `enqueue(x)` adds to the back, `dequeue()` removes and returns from the front, obeying FIFO (First In, First Out) order.

**Q2:**
`lst.append(x)`: O(1) amortized
`lst.insert(0, x)`: O(n)
`lst.pop()`: O(1)
`lst.pop(0)`: O(n)
The first two operate on the END of the list (no shifting needed — Python's dynamic array has spare capacity at the end, or a fast size decrement). The latter two operate on the FRONT, requiring every remaining element to be shifted by one position to maintain contiguous storage.

**Q3:** O(n). Removing the last node requires updating the SECOND-to-last node's `next` pointer to `None` — but with only forward (`next`) pointers, the only way to find the second-to-last node is to traverse from the head all the way to it, which is O(n). A `prev` pointer on each node (making it a doubly linked list) would let you jump directly from the tail to the second-to-last node in O(1).

**Q4:** It IS a valid implementation — it correctly obeys FIFO order (first appended is first popped). However, it is a POOR engineering choice: `lst.pop(0)` is O(n) (must shift every remaining element), so this queue's dequeue operation is O(n) instead of the O(1) achievable with `collections.deque`. For a queue processing many items, this degrades performance from O(n) total to O(n²) total.

**Q5:** `collections.deque` is NOT implemented as one contiguous array internally — it's implemented as a doubly linked structure of fixed-size blocks, optimized for O(1) operations at BOTH ends. This internal structure means there's no direct "address = base + i×size" formula for arbitrary index `i` — you must traverse from one end, which is O(n) in the worst case (though better than a plain linked list in practice due to block-based storage).

---

*CS 101 · Week 8 · Quiz 8 · © CSE Department*

# CS 102 · Quiz 4

**Date:** Monday 15 February 2027 · 09:00–09:15 (start of L13) · Week 4 · 20 points
**Covers Week 3** — heaps, the linear build, and priority queues. **Not** this week's material.

Closed book. No calculator required — every number here is exact.
All heaps are **min-heaps** and **0-indexed**. Height counts **edges**.

---

**Q1.** *(3)* For a 0-indexed binary heap, give `left(i)`, `right(i)`, and `parent(i)`.

---

**Q2.** *(3)* Is `[2, 7, 4, 9, 8, 3, 6]` a valid min-heap? If not, name **one** index that violates the
heap property and say why.

---

**Q3.** *(4)* Insert $3$ into the heap `[5, 8, 6, 12, 9]`.

- **(a)** Give the array after the insertion.
- **(b)** How many swaps did `sift_up` perform?

---

**Q4.** *(3)* Call `pop_min()` on `[1, 4, 3, 9, 7, 5]`. Give the value returned and the resulting
array.

---

**Q5.** *(4)* Building a heap from $n$ items by repeated insertion costs $\Theta(n \log n)$ in the
worst case. The bottom-up build costs $\Theta(n)$. Both call an $O(\log n)$ repair once per element.

Explain the discrepancy in **two sentences**. A complete answer says where the nodes are.

---

**Q6.** *(3)* A heap of $n$ elements. State the cost of each, with one clause of justification:

- **(a)** finding the minimum;
- **(b)** finding the **maximum**.

---

*20 points total. Solutions posted after Wednesday's lecture.*

*CS 102 · Week 4 · Quiz 4 · © CSE Department*

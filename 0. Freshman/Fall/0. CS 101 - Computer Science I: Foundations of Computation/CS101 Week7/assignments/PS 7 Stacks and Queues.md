# CS 101 · Problem Set 7
## Stacks, Queues, and Linked Structures

**Released:** Friday 13 November 2026, 10:00 (after L24) · Week 7
**Due:** Friday 20 November 2026, 17:00 · Week 8 — late penalty from 17:01
**Submission:** `ps7.py` (Part B) and your answer sheet (Part A) in `"$CS101/week7"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 3 hours

*(Revised 2026-09-26: Lab 7 (Tuesday 17 November) builds `Stack`, `Queue` and `LinkedList` classes, so
this set no longer asks for `ArrayStack` or `LinkedStack`; use your Lab 7 classes or a plain list where a
stack is needed. A3 was also removed, and the answer key moved out of this handout.)*
**Note:** Project 1 is also running (due Friday 27 November). Do this set first, in the first half of the week.

---

## What this problem set uses

Weeks 0–7, above all this week's: ADTs vs implementations and the list memory model (L22), linked
nodes, `reverse`, the tail pointer (L23), stacks, queues and `collections.deque`, balanced brackets,
and timing with `timeit` as in L22/L24's exercises (L24). Classes are used the way L23–L24 use them:
`__init__`, `__len__`, and `raise IndexError` on an empty structure.

**Not needed and not expected:** slow/fast pointers or cycle detection, merging linked lists, BFS,
dictionaries (Week 8).

Every method's docstring or comment states its cost. Test each class with `assert`s, including the
empty structure and a single element.

---

## Part A: Written (18 points)

### A1: ADT vs. Implementation (8 points)

**(a)** Explain the difference between an abstract data type and an implementation, using the Stack ADT
and two implementations that satisfy it.
**(b)** A classmate implements a stack on a Python list with `insert(0, x)` to push and `pop(0)` to pop.
Why is it still a correct stack? Why is it a poor one (L22 §5)?

### A2: Costs (10 points)

Give each operation's cost for a list-based and a linked implementation, with a one-line reason from the
memory model:

| Operation | List / deque based | Singly linked | Reason |
|---|---|---|---|
| Stack push | | | |
| Stack pop | | | |
| Queue enqueue at the back | | | |
| Queue dequeue from the front — raw list vs linked **with** a tail pointer | | | |
| Reading the k-th element | | | |

---

## Part B: Python (`ps7.py`) (82 points)

### B1: Two Array Queues (10 points)

**(a)** `ArrayQueue` on `collections.deque`: `enqueue`, `dequeue`, `is_empty`, `__len__`.
**(b)** `NaiveArrayQueue` on a raw list with `dequeue` as `pop(0)` — deliberately slow, for B4.

`dequeue` raises `IndexError` when empty.

### B2: Linked Queue (12 points)

Use a small `_Node` class (`data`, `next`) as in L23. `LinkedQueue` keeps `head` and `tail`; enqueue at
the tail, dequeue at the head. Explain in a comment why not the other way round. Watch the case where the
last item is dequeued.

### B3: More Linked-List Operations (18 points)

Start from your Lab 7 `LinkedList` (or write one with `head`, `tail`, `size`, `append(x)` and `to_list()`
as in L23), then add:

**(a)** `count(x)` — how many nodes hold `x`.
**(b)** `reverse()` — in place, re-pointing `next` (L23); update `head` **and** `tail`. After reversing
`[1, 2, 3, 4]`, `to_list()` is `[4, 3, 2, 1]` and `append(9)` must still work.
**(c)** `remove_duplicates()` — keep the first of each value, in order, **without** a `set` or `dict`
(O(n²)). `[3, 1, 3, 2, 1, 3]` → `[3, 1, 2]`, with `size` and `tail` still correct.

### B4: Timing Two Queues (14 points)

With `timeit` as in L24's exercise, time `n` enqueues followed by `n` dequeues on `ArrayQueue` and on
`NaiveArrayQueue`, for `n` = 1,000, 5,000, 20,000, 50,000, and print both times and their ratio. In a
comment, explain why the ratio **grows** with `n` instead of staying fixed (L22 §5, L24 §4).

### B5: Evaluating Expressions with Two Stacks (28 points)

**(a)** `tokenize(expression)` — numbers (several digits, decimals), operators and parentheses; spaces
ignored. `"(3 + 4) * 2"` → `['(', '3', '+', '4', ')', '*', '2']`; `"(1.5 + 2.25)"` → `['(', '1.5', '+', '2.25', ')']`.

**(b)** `evaluate(expression)` for **fully parenthesised** expressions, using one stack of operands and
one of operators (your Lab 7 `Stack`, or a list with `append` and `pop`):

```
number     -> push float(number) onto the operand stack
operator   -> push onto the operator stack
'('        -> ignore
')'        -> pop one operator and two operands (right first!), apply, push the result
at the end -> exactly one operand is left: the answer
```

`"(3 + 4)"` → `7.0`; `"((3 + 4) * 2)"` → `14.0`; `"((10 - 4) / (1 + 2))"` → `2.0`; `"(0 - 5)"` → `-5.0`.

**(c)** Test at least eight expressions: nesting, all four operators, decimals.

---

## Grading Rubric

| Problem | Points |
|---------|--------|
| A1 ADT vs implementation | 8 |
| A2 Costs | 10 |
| B1 Array queues | 10 |
| B2 Linked queue | 12 |
| B3 Linked-list operations | 18 |
| B4 Timing | 14 |
| B5 Expressions | 28 |
| **Total** | **100** |

---

*CS 101 · Week 7 · Problem Set 7 · Due Friday 20 November 2026, 17:00 · © CSE Department*

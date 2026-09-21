# CS 101 · Lab 7
## Memory Profiling: List vs. Linked List

**Date:** Tuesday 17 November 2026 · 15:00–16:50 · Lab Section (Week 8) — covers Week 7 (L22–L24)
*Duration: 2 hours · 100 points via TA checkoff, part of the Labs component (10%)*

**Tools used:** Weeks 0–7 — classes as L23–L24 write them, `sys.getsizeof` (L22), `timeit` (L22/L24
exercises), `collections.deque`. Everything goes in **one file**, `data_structures.py`: importing your
own modules is not something this course has taught.

---

## Objectives

By the end of this lab, you will:
- [ ] Measure actual memory usage of Python lists vs. hand-rolled linked lists
- [ ] Empirically verify the O(1) vs O(n) complexity claims from Wednesday/Thursday's lectures
- [ ] Implement a complete singly linked list, doubly linked list, stack, and queue
- [ ] Use `sys.getsizeof()` to measure memory
- [ ] Benchmark front/back/random-access operations across all structures
- [ ] Build and test a bracket-matching stack application

---

## Setup

```bash
cd "$CS101"        # set in ~/.bashrc -- see Lab 0
mkdir -p week7 && cd week7
```

---

## Part 1: Memory Profiling Basics (25 minutes)

### Exercise 1.1: `sys.getsizeof()` — What Does Python Actually Report?

```python
import sys

# Empty containers:
print("Empty list:      ", sys.getsizeof([]))
print("Empty tuple:      ", sys.getsizeof(()))

# A single small int (Python ints are OBJECTS, not raw machine words):
print("Int 0:            ", sys.getsizeof(0))
print("Int 1:            ", sys.getsizeof(1))
print("Int 10**100:       ", sys.getsizeof(10**100))   # much bigger — arbitrary precision!

# Lists of varying sizes:
for n in [0, 1, 10, 100, 1000]:
    lst = list(range(n))
    print(f"list(range({n:5})): {sys.getsizeof(lst):8} bytes")
```

**⚠️ Critical caveat:** `sys.getsizeof(lst)` measures the size of the **list object itself** (the array of pointers) — it does **NOT** include the size of the objects the pointers point to! For a list of large custom objects, the real memory footprint is much larger than `getsizeof` alone reports.

**Record in `LAB 7 Memory Profiling.md`:**
1. Why is `sys.getsizeof(10**100)` so much bigger than `sys.getsizeof(1)`? (Connect to Week 1's discussion of Python's arbitrary-precision integers.)
2. Does list size grow linearly with the number of elements? Compute the bytes-per-element ratio for n=1000 (getsizeof(list) / 1000) and compare to n=100.

### Exercise 1.2: Measuring TOTAL Memory Including Contents

```python
import sys

def deep_getsizeof(lst):
    """Size of the list object plus the size of every item it points to."""
    size = sys.getsizeof(lst)
    for item in lst:
        size += sys.getsizeof(item)
    return size


# Compare shallow vs deep size for a list of large integers:
lst = [10**50 + i for i in range(1000)]
print(f"Shallow size (just the array of pointers): {sys.getsizeof(lst)} bytes")
print(f"Deep size (array + all the int objects):   {deep_getsizeof(lst)} bytes")
```

**Record:** What is the ratio of deep size to shallow size? Why is the difference so large for big integers specifically?

---

## Part 2: Build the Data Structures (45 minutes)

Create `data_structures.py` — implement every class from this week's lectures.

```python
#!/usr/bin/env python3
"""
data_structures.py
CS 101 — Week 7, Lab 7

Complete implementations: Node, LinkedList, DoublyLinkedList, Stack, Queue.

Student: ____________________________
Date: ______________________________
"""


class Node:
    """A node in a singly linked list."""
    __slots__ = ("data", "next")

    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    """
    Singly linked list with head AND tail pointers (O(1) append).

    Implement every method. See Thursday's lecture for the design.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self.head is None

    def append(self, data):
        """Insert at the end. O(1) with tail pointer."""
        # TODO: implement using self.tail
        pass

    def prepend(self, data):
        """Insert at the front. O(1)."""
        # TODO: implement
        pass

    def find(self, target):
        """Return True if target is in the list. O(n)."""
        # TODO: implement
        pass

    def remove(self, target):
        """Remove first occurrence of target. Return True/False. O(n)."""
        # TODO: implement (remember to handle removing the head AND updating
        # self.tail if you remove the last element!)
        pass

    def get(self, index):
        """Return the data at position index (0-based). O(n)."""
        # TODO: traverse from head, counting positions
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        pass

    def to_list(self):
        """Convert to a Python list. O(n)."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def __repr__(self):
        return " -> ".join(str(x) for x in self.to_list()) + " -> None"


class DNode:
    """A node in a doubly linked list."""
    __slots__ = ("data", "prev", "next")

    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


class DoublyLinkedList:
    """
    Doubly linked list. Implement every method — see Thursday's lecture.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def append(self, data):
        """O(1)."""
        # TODO
        pass

    def prepend(self, data):
        """O(1)."""
        # TODO
        pass

    def remove_last(self):
        """O(1) — the key advantage of doubly linked over singly linked!"""
        # TODO
        pass

    def remove_first(self):
        """O(1)."""
        # TODO
        pass

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def to_list_reversed(self):
        result = []
        current = self.tail
        while current is not None:
            result.append(current.data)
            current = current.prev
        return result


class Stack:
    """
    Stack ADT backed by a Python list. Top = end of the list.
    """

    def __init__(self):
        self._data = []

    def push(self, x):
        # TODO
        pass

    def pop(self):
        # TODO — remember to raise IndexError on empty!
        pass

    def peek(self):
        # TODO
        pass

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)


class Queue:
    """
    Queue ADT backed by collections.deque.
    """

    def __init__(self):
        from collections import deque
        self._data = deque()

    def enqueue(self, x):
        # TODO
        pass

    def dequeue(self):
        # TODO — remember to raise IndexError on empty!
        pass

    def peek(self):
        # TODO
        pass

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)


def run_tests():
    """Verify all implementations are correct."""

    # LinkedList tests
    ll = LinkedList()
    assert ll.is_empty()
    ll.append(10); ll.append(20); ll.append(30)
    assert ll.to_list() == [10, 20, 30]
    ll.prepend(5)
    assert ll.to_list() == [5, 10, 20, 30]
    assert ll.find(20) == True
    assert ll.find(99) == False
    assert ll.get(0) == 5
    assert ll.get(2) == 20
    ll.remove(20)
    assert ll.to_list() == [5, 10, 30]
    assert len(ll) == 3
    print("✓ LinkedList")

    # DoublyLinkedList tests
    dll = DoublyLinkedList()
    dll.append(1); dll.append(2); dll.append(3)
    assert dll.to_list() == [1, 2, 3]
    assert dll.to_list_reversed() == [3, 2, 1]
    assert dll.remove_last() == 3
    assert dll.remove_first() == 1
    assert dll.to_list() == [2]
    print("✓ DoublyLinkedList")

    # Stack tests
    s = Stack()
    s.push(1); s.push(2); s.push(3)
    assert s.pop() == 3
    assert s.peek() == 2
    assert s.size() == 2
    print("✓ Stack")

    # Queue tests
    q = Queue()
    q.enqueue(1); q.enqueue(2); q.enqueue(3)
    assert q.dequeue() == 1
    assert q.peek() == 2
    assert q.size() == 2
    print("✓ Queue")

    print("\n🎉 All data structure tests passed!")


if __name__ == "__main__":
    run_tests()
```

Run it: `python3 data_structures.py` — all four should pass.

---

## Part 3: Empirical Memory Comparison (30 minutes)

Add this section to the **bottom** of `data_structures.py` (it replaces a separate `memory_comparison.py`):

```python
#!/usr/bin/env python3
"""
memory_comparison.py
CS 101 — Week 7, Lab 7

Compare memory usage: Python list vs. our LinkedList, for the same data.
"""

import sys


def measure_list_memory(n):
    """Total memory for a Python list of n integers (shallow list + int objects)."""
    lst = list(range(n))
    list_overhead = sys.getsizeof(lst)
    # Small ints (-5 to 256) are cached/interned by Python, so for a fair
    # comparison at scale, use large ints that won't be cached:
    lst_large = [i + 10**9 for i in range(n)]
    list_overhead_large = sys.getsizeof(lst_large)
    int_objects_total = sum(sys.getsizeof(x) for x in lst_large)
    return list_overhead_large + int_objects_total


def measure_linked_list_memory(n):
    """Total memory for our LinkedList of n integers."""
    ll = LinkedList()
    for i in range(n):
        ll.append(i + 10**9)   # match the "large int" choice above

    total = sys.getsizeof(ll)                    # the LinkedList object itself (head/tail/size)
    current = ll.head
    while current is not None:
        total += sys.getsizeof(current)           # the Node object (data ptr + next ptr)
        total += sys.getsizeof(current.data)       # the actual data (int object)
        current = current.next

    return total


print(f"{'n':>8} {'Python list (bytes)':>20} {'LinkedList (bytes)':>20} {'Ratio':>8}")
print("-" * 62)
for n in [10, 100, 1000, 10000]:
    list_mem   = measure_list_memory(n)
    linked_mem = measure_linked_list_memory(n)
    ratio = linked_mem / list_mem
    print(f"{n:8} {list_mem:20} {linked_mem:20} {ratio:7.2f}x")
```

Run it: `python3 data_structures.py`

**Record in `LAB 7 Memory Profiling.md`:**
1. What is the approximate ratio (LinkedList memory / Python list memory)? Does this ratio stay roughly constant as n grows, or does it change?
2. Why does the linked list use more memory per element? List the specific sources of overhead (refer to Thursday's lecture).
3. Estimate: for n = 1,000,000, roughly how much MORE memory (in MB) would the linked list use compared to the Python list, based on your measured ratio?

---

## Part 4: Benchmarking Operation Complexity (30 minutes)

Add this section to the **bottom** of `data_structures.py` (it replaces a separate `benchmark_operations.py`):

```python
#!/usr/bin/env python3
"""
benchmark_operations.py
CS 101 — Week 7, Lab 7

Empirically verify the complexity claims:
  - Python list: O(1) append/pop-end, O(n) insert(0)/pop(0)
  - LinkedList:  O(1) prepend/append (with tail), O(n) get(i) for large i
"""

import timeit


def time_op(func, repeats=100):
    """Average time of a zero-argument callable over `repeats` runs, using timeit as L24 does."""
    return timeit.timeit(func, number=repeats) / repeats


print("=" * 70)
print("PART A: Python list — front vs. back operations")
print("=" * 70)
print(f"{'n':>10} {'append (μs)':>15} {'insert(0,x) (μs)':>18} {'ratio':>8}")

for n in [1000, 10000, 100000]:
    base = list(range(n))

    # Use fresh copies to avoid growing unboundedly across iterations:
    def do_append():
        base.append(0)
        base.pop()   # undo, so list size stays constant across repeats
    def do_insert():
        base.insert(0, 0)
        base.pop(0)  # undo

    t_append = time_op(do_append) * 1e6
    t_insert = time_op(do_insert) * 1e6

    print(f"{n:10} {t_append:15.3f} {t_insert:18.3f} {t_insert/t_append:8.1f}x")


print("\n" + "=" * 70)
print("PART B: LinkedList — get(0) vs. get(n-1)")
print("=" * 70)
print(f"{'n':>10} {'get(0) (μs)':>15} {'get(n-1) (μs)':>18} {'ratio':>8}")

for n in [1000, 5000, 20000]:
    ll = LinkedList()
    for i in range(n):
        ll.append(i)

    t_get_first = time_op(lambda: ll.get(0)) * 1e6
    t_get_last  = time_op(lambda: ll.get(n - 1)) * 1e6

    print(f"{n:10} {t_get_first:15.3f} {t_get_last:18.3f} {t_get_last/t_get_first:8.1f}x")
```

Run it: `python3 data_structures.py`

**Record in `LAB 7 Memory Profiling.md`:**
1. For Part A, does the ratio (`insert(0,x)` time / `append` time) grow as n grows? Is this consistent with O(n) vs O(1)?
2. For Part B, does the ratio (`get(n-1)` time / `get(0)` time) grow as n grows? Explain why `get(0)` stays fast while `get(n-1)` gets progressively slower.
3. Extrapolate: if `insert(0,x)` on a list of 100,000 elements takes X microseconds, roughly how long would it take on 10,000,000 elements? (Use the O(n) relationship, not just guessing.)

---

## Part 5: Application — Bracket Matching and Undo/Redo (15 minutes)

Add this section to the **bottom** of `data_structures.py` (it replaces a separate `applications.py`):

```python
#!/usr/bin/env python3
"""
applications.py
CS 101 — Week 7, Lab 7

Real applications of Stack and Queue.
"""



def is_balanced(expression):
    """
    Return True if all brackets ()[]{}  are balanced and properly nested.
    See Friday's lecture for the full algorithm description.
    """
    pairs = {')': '(', ']': '[', '}': '{'}
    openers = set(pairs.values())
    stack = Stack()

    # TODO: implement using the Stack class above
    pass


assert is_balanced("(a + b) * [c - d]") == True
assert is_balanced("(a + [b)")          == False
assert is_balanced("((a)")              == False
assert is_balanced("a)")                == False
assert is_balanced("{[()()]}")          == True
print("✓ is_balanced")


class UndoRedoEditor:
    """
    A simple text editor with undo/redo, backed by two Stacks.

    Design: every edit pushes the PREVIOUS state onto undo_stack.
    Undo pops from undo_stack, pushes current state onto redo_stack.
    Redo pops from redo_stack, pushes current state onto undo_stack.
    Making a NEW edit after undoing clears the redo_stack (standard editor behavior).
    """

    def __init__(self):
        self.text = ""
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def type(self, new_text):
        """Append new_text to the current text, recording history."""
        self.undo_stack.push(self.text)
        self.text += new_text
        # TODO: clear the redo stack (a fresh Stack()) since we took a new action
        pass

    def undo(self):
        """Revert to the previous state, if any."""
        if self.undo_stack.is_empty():
            return
        # TODO: push current text to redo_stack, pop from undo_stack into self.text
        pass

    def redo(self):
        """Reapply an undone state, if any."""
        if self.redo_stack.is_empty():
            return
        # TODO: push current text to undo_stack, pop from redo_stack into self.text
        pass


editor = UndoRedoEditor()
editor.type("Hello")
editor.type(", World")
editor.type("!")
assert editor.text == "Hello, World!"

editor.undo()
assert editor.text == "Hello, World"

editor.undo()
assert editor.text == "Hello"

editor.redo()
assert editor.text == "Hello, World"

editor.type("???")   # new edit after undo — should clear redo history
assert editor.text == "Hello, World???"

editor.redo()   # nothing to redo now
assert editor.text == "Hello, World???"   # unchanged

print("✓ UndoRedoEditor")
print("\n🎉 All application tests passed!")
```

---

## Part 6: Commit and Reflection (10 minutes)

```bash
cd "$CS101/week7"
git add .
git commit -m "CS 101 Lab 7: memory, linked lists, stacks, queues, applications"
git push
```

### Reflection in `LAB 7 Memory Profiling.md`:

**Q1.** Your memory measurements showed linked lists use more memory per element than Python lists. Given this, why would anyone ever choose a linked list over a Python list in real code? Name one specific, valid reason from this week's lectures.

**Q2.** You measured that `list.insert(0, x)` gets progressively slower (relative to `append`) as the list grows. If you needed a queue that would hold millions of items with frequent enqueue/dequeue, would you use a Python list with `insert(0,x)`/`pop()`, a Python list with `append()`/`pop(0)`, or `collections.deque`? Justify using your empirical data.

**Q3.** The `UndoRedoEditor` uses TWO stacks. Why not just one? What specific behavior would break if you tried to implement redo using only the undo_stack?

**Q4.** In `measure_linked_list_memory`, we called `sys.getsizeof()` on the LinkedList object, each Node, AND each data value separately, then summed them. Why isn't `sys.getsizeof(ll)` alone (where `ll` is the LinkedList) sufficient to capture the true memory usage?

---

## TA Checkoff Criteria

| Part | Points | Show your TA |
|---|---|---|
| 1 | 15 | `getsizeof` results and the two recorded answers |
| 2 | 35 | All four classes implemented; `run_tests()` passes |
| 3 | 15 | Memory table with the ratio analysis |
| 4 | 15 | Both timing tables with the ratio analyses |
| 5 | 20 | `is_balanced` and `UndoRedoEditor` pass their asserts |
| **Total** | **100** | Reflection answered and work committed (required) |

---

*CS 101 · Week 7 · Lab 7 · Tuesday 17 November 2026 · © CSE Department*

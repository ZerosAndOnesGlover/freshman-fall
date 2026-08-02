#!/usr/bin/env python3
"""
ps7.py
CS 101 — Problem Set 7: Stacks, Queues, and Linked Structures

Student: ____________________________
Date: ______________________________

Honor pledge: I wrote this code myself and understand every line.
Signed: ____________________________
"""

import time
from collections import deque


# ══════════════════════════════════════════════════════════════════════════════
# B1: Array-Based Stack and Queue
# ══════════════════════════════════════════════════════════════════════════════

class ArrayStack:
    """
    Stack ADT backed by a Python list.

    Design choice: the END of the list is the "top", because
    list.append() and list.pop() are both O(1) amortized, whereas
    using the front would make both operations O(n).
    """

    def __init__(self):
        self._data = []

    def push(self, x):
        """Add x to the top. O(1) amortized."""
        # TODO
        pass

    def pop(self):
        """Remove and return the top element. O(1). Raise IndexError if empty."""
        # TODO
        pass

    def peek(self):
        """Return the top element without removing it. O(1). Raise IndexError if empty."""
        # TODO
        pass

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)


s = ArrayStack()
s.push(1); s.push(2); s.push(3)
assert s.pop() == 3
assert s.peek() == 2
assert s.size() == 2
try:
    ArrayStack().pop()
    assert False
except IndexError:
    pass
print("✓ ArrayStack")


class ArrayQueue:
    """
    Queue ADT backed by collections.deque — O(1) at both ends.
    """

    def __init__(self):
        self._data = deque()

    def enqueue(self, x):
        """Add to the back. O(1)."""
        # TODO
        pass

    def dequeue(self):
        """Remove and return from the front. O(1). Raise IndexError if empty."""
        # TODO
        pass

    def peek(self):
        """Return the front element. O(1). Raise IndexError if empty."""
        # TODO
        pass

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)


q = ArrayQueue()
q.enqueue(1); q.enqueue(2); q.enqueue(3)
assert q.dequeue() == 1
assert q.peek() == 2
print("✓ ArrayQueue")


class NaiveArrayQueue:
    """
    Queue ADT using ONLY a raw Python list — intentionally the "wrong" way.
    dequeue() uses pop(0), which is O(n). Used in B4 for benchmarking comparison.
    """

    def __init__(self):
        self._data = []

    def enqueue(self, x):
        """O(1) amortized."""
        self._data.append(x)

    def dequeue(self):
        """O(n) — must shift every remaining element!"""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.pop(0)

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)


nq = NaiveArrayQueue()
nq.enqueue(1); nq.enqueue(2)
assert nq.dequeue() == 1
print("✓ NaiveArrayQueue")


# ══════════════════════════════════════════════════════════════════════════════
# B2: Linked-List-Based Stack and Queue
# ══════════════════════════════════════════════════════════════════════════════

class LinkedStack:
    """
    Stack ADT backed by a singly linked list.
    Design choice: the HEAD is the "top" — prepend/remove-from-head are O(1)
    for a singly linked list (no traversal needed).
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
        """O(1)."""
        # TODO
        pass

    def pop(self):
        """O(1). Raise IndexError if empty."""
        # TODO
        pass

    def peek(self):
        """O(1). Raise IndexError if empty."""
        # TODO
        pass

    def is_empty(self):
        return self._head is None

    def size(self):
        return self._size


ls = LinkedStack()
ls.push(1); ls.push(2); ls.push(3)
assert ls.pop() == 3
assert ls.peek() == 2
assert ls.size() == 2
print("✓ LinkedStack")


class LinkedQueue:
    """
    Queue ADT backed by a singly linked list WITH a tail pointer.

    Design choice: enqueue at TAIL, dequeue from HEAD.
    Why not the reverse? Removing from the tail of a singly linked list
    requires finding the SECOND-to-last node, which needs O(n) traversal
    (no prev pointers). Removing from the head is always O(1). So we
    enqueue where insertion is cheap (tail, O(1) with tail pointer) and
    dequeue where removal is cheap (head, O(1)).
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
        # TODO
        pass

    def dequeue(self):
        """O(1) — remove from the head. Raise IndexError if empty."""
        # TODO
        pass

    def peek(self):
        """O(1). Raise IndexError if empty."""
        # TODO
        pass

    def is_empty(self):
        return self._head is None

    def size(self):
        return self._size


lq = LinkedQueue()
lq.enqueue(1); lq.enqueue(2); lq.enqueue(3)
assert lq.dequeue() == 1
assert lq.peek() == 2
print("✓ LinkedQueue")


# ══════════════════════════════════════════════════════════════════════════════
# B3: Extended Linked List Operations
# ══════════════════════════════════════════════════════════════════════════════

class Node:
    __slots__ = ("data", "next")
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    """Extended LinkedList from lab, with additional operations for PS7."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self.head is None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def reverse(self):
        """
        Reverse the linked list IN PLACE. O(n).
        Do not create new nodes — re-point existing next pointers.
        Remember to swap self.head and self.tail!
        """
        # TODO:
        # prev = None
        # current = self.head
        # while current is not None:
        #     next_node = current.next    # save before overwriting
        #     current.next = prev          # reverse the pointer
        #     prev = current
        #     current = next_node
        # self.head, self.tail = self.tail, self.head
        pass

    def middle(self):
        """
        Return the data at the middle node, using slow/fast pointers.
        Single O(n) pass — do NOT call len() and traverse again.

        For even-length lists, return the SECOND of the two middle elements.

        Examples:
            [1,2,3,4,5].middle()   → 3
            [1,2,3,4].middle()     → 3   (second of the two middle: 2,3)
        """
        if self.head is None:
            raise IndexError("middle of empty list")

        # TODO: slow/fast pointer technique
        # slow = fast = self.head
        # while fast is not None and fast.next is not None:
        #     slow = slow.next
        #     fast = fast.next.next
        # return slow.data
        pass

    def has_cycle(self):
        """
        Return True if the list contains a cycle (Floyd's algorithm).
        O(n) time, O(1) space.

        CAUTION: do not call to_list() or len() on a cyclic structure
        elsewhere in your testing — those will infinite loop!
        """
        # TODO: tortoise and hare
        # slow = fast = self.head
        # while fast is not None and fast.next is not None:
        #     slow = slow.next
        #     fast = fast.next.next
        #     if slow is fast:
        #         return True
        # return False
        pass

    def remove_duplicates(self):
        """
        Remove duplicate values, keeping only the first occurrence of each,
        preserving order. Modifies the list in place. O(n^2) without a set.

        (A set-based O(n) version would maintain a "seen" set() and skip
        nodes whose data is already in it — mention this in a comment,
        but implement the O(n^2) version here using only list/LL operations.)
        """
        if self.head is None:
            return

        # TODO: for each node, scan ALL subsequent nodes and unlink any
        # with matching data. Remember to update self.tail if you remove
        # the tail node!
        pass

    def merge_sorted(self, other):
        """
        Given self and other are both ALREADY SORTED LinkedLists,
        return a NEW sorted LinkedList containing all elements of both.
        O(n + m). Do NOT convert to Python lists.
        """
        result = LinkedList()
        p1 = self.head
        p2 = other.head

        # TODO: standard merge, using result.append() to build the answer
        # while p1 is not None and p2 is not None:
        #     if p1.data <= p2.data:
        #         result.append(p1.data); p1 = p1.next
        #     else:
        #         result.append(p2.data); p2 = p2.next
        # while p1 is not None: result.append(p1.data); p1 = p1.next
        # while p2 is not None: result.append(p2.data); p2 = p2.next

        return result


# Tests:
ll = LinkedList()
for x in [1, 2, 3, 4, 5]:
    ll.append(x)

ll.reverse()
assert ll.to_list() == [5, 4, 3, 2, 1], f"got {ll.to_list()}"
ll.reverse()   # back to original for further testing
assert ll.to_list() == [1, 2, 3, 4, 5]
print("✓ reverse")

assert ll.middle() == 3

ll_even = LinkedList()
for x in [1, 2, 3, 4]:
    ll_even.append(x)
assert ll_even.middle() == 3   # second of the two middles (2,3)
print("✓ middle")

# has_cycle test — build a cyclic structure manually:
cyclic = LinkedList()
n1 = Node(1); n2 = Node(2); n3 = Node(3)
n1.next = n2; n2.next = n3; n3.next = n1   # cycle back to n1
cyclic.head = n1
assert cyclic.has_cycle() == True

acyclic = LinkedList()
for x in [1, 2, 3]:
    acyclic.append(x)
assert acyclic.has_cycle() == False
print("✓ has_cycle")

dup_test = LinkedList()
for x in [1, 2, 2, 3, 1, 4, 3]:
    dup_test.append(x)
dup_test.remove_duplicates()
assert dup_test.to_list() == [1, 2, 3, 4], f"got {dup_test.to_list()}"
print("✓ remove_duplicates")

sorted1 = LinkedList()
for x in [1, 3, 5]:
    sorted1.append(x)
sorted2 = LinkedList()
for x in [2, 4, 6]:
    sorted2.append(x)
merged = sorted1.merge_sorted(sorted2)
assert merged.to_list() == [1, 2, 3, 4, 5, 6], f"got {merged.to_list()}"
print("✓ merge_sorted")


# ══════════════════════════════════════════════════════════════════════════════
# B4: Empirical Comparison
# ══════════════════════════════════════════════════════════════════════════════

def benchmark_queues():
    print("\n--- Queue comparison: ArrayQueue (deque) vs NaiveArrayQueue (list) ---")
    print(f"{'n':>10} {'deque-based (ms)':>18} {'list-based (ms)':>18} {'ratio':>8}")

    for n in [1000, 5000, 20000, 50000]:
        aq = ArrayQueue()
        t0 = time.perf_counter()
        for i in range(n):
            aq.enqueue(i)
        for i in range(n):
            aq.dequeue()
        t_deque = time.perf_counter() - t0

        naq = NaiveArrayQueue()
        t0 = time.perf_counter()
        for i in range(n):
            naq.enqueue(i)
        for i in range(n):
            naq.dequeue()
        t_naive = time.perf_counter() - t0

        print(f"{n:10} {t_deque*1000:18.2f} {t_naive*1000:18.2f} {t_naive/t_deque:8.1f}x")


def benchmark_stacks():
    print("\n--- Stack comparison: ArrayStack vs LinkedStack ---")
    print(f"{'n':>10} {'array-based (ms)':>18} {'linked-based (ms)':>18} {'ratio':>8}")

    for n in [1000, 5000, 20000, 50000]:
        astack = ArrayStack()
        t0 = time.perf_counter()
        for i in range(n):
            astack.push(i)
        for i in range(n):
            astack.pop()
        t_array = time.perf_counter() - t0

        lstack = LinkedStack()
        t0 = time.perf_counter()
        for i in range(n):
            lstack.push(i)
        for i in range(n):
            lstack.pop()
        t_linked = time.perf_counter() - t0

        print(f"{n:10} {t_array*1000:18.2f} {t_linked*1000:18.2f} {t_linked/t_array:8.2f}x")


benchmark_queues()
benchmark_stacks()


# ══════════════════════════════════════════════════════════════════════════════
# B5: Expression Evaluation
# ══════════════════════════════════════════════════════════════════════════════

def tokenize(expression):
    """
    Split a fully-parenthesized expression into tokens.

    Handles multi-digit numbers and decimals.

    Examples:
        tokenize("(3 + 4) * 2")   → ['(', '3', '+', '4', ')', '*', '2']
        tokenize("(1.5 + 2.25)")  → ['(', '1.5', '+', '2.25', ')']
    """
    tokens = []
    i = 0
    n = len(expression)

    while i < n:
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if char in "()+-*/":
            # TODO: handle unary minus if needed, otherwise just append the char
            tokens.append(char)
            i += 1
            continue

        if char.isdigit() or char == '.':
            # TODO: consume a full number (possibly with a decimal point)
            j = i
            while j < n and (expression[j].isdigit() or expression[j] == '.'):
                j += 1
            tokens.append(expression[i:j])
            i = j
            continue

        raise ValueError(f"Unexpected character: {char}")

    return tokens


assert tokenize("(3 + 4) * 2") == ['(', '3', '+', '4', ')', '*', '2']
assert tokenize("(1.5 + 2.25)") == ['(', '1.5', '+', '2.25', ')']
print("✓ tokenize")


def evaluate(expression):
    """
    Evaluate a fully-parenthesized arithmetic expression using the
    two-stack algorithm.

    Algorithm:
        For each token:
            number    → push onto operand stack
            operator  → push onto operator stack
            '('       → ignore
            ')'       → pop operator, pop two operands, apply, push result

    Examples:
        evaluate("(3 + 4)")             → 7.0
        evaluate("((3 + 4) * 2)")       → 14.0
        evaluate("((10 - 4) / (1 + 2))") → 2.0
    """
    tokens = tokenize(expression)
    operands  = ArrayStack()
    operators = ArrayStack()

    def apply_operator():
        op = operators.pop()
        b = operands.pop()
        a = operands.pop()
        if op == '+': result = a + b
        elif op == '-': result = a - b
        elif op == '*': result = a * b
        elif op == '/': result = a / b
        else: raise ValueError(f"Unknown operator: {op}")
        operands.push(result)

    # TODO: iterate through tokens, implementing the algorithm above
    for token in tokens:
        pass

    return operands.pop()


assert evaluate("(3 + 4)") == 7.0
assert evaluate("((3 + 4) * 2)") == 14.0
assert evaluate("((10 - 4) / (1 + 2))") == 2.0
assert evaluate("(0 - 5)") == -5.0
assert evaluate("((1 + 2) + (3 + 4))") == 10.0
assert evaluate("(100 / (2 * 5))") == 10.0
assert evaluate("((2.5 + 2.5) * 2)") == 10.0
assert evaluate("(((1 + 1) + 1) + 1)") == 4.0
print("✓ evaluate — all 8 test cases passed")


# ══════════════════════════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("All ps7.py assertions passed.")
    print("=" * 50)

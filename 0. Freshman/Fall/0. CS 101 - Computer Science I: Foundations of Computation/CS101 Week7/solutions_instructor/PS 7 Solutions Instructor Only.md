# CS 101 · Problem Set 7 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** The reference `ps7.py` below was run: every assert passes. The
> timing table is one real run; students' absolute times will differ — grade the trend.

### A1 (8)

(a) An ADT is the promised behaviour (push, pop, peek, LIFO, errors on empty); an implementation is the
data layout that delivers it — e.g. a list with the end as the top, or linked nodes with the head as the
top. *(4)* (b) The behaviour is still LIFO, so it is a correct stack; but `insert(0)`/`pop(0)` shift every
element, Θ(n) per operation instead of O(1). *(4)*

### A2 (10, 2 per row)

| Operation | List / deque | Singly linked | Reason |
|---|---|---|---|
| push | O(1) amortised (append) | O(1) (new head) | end of array / head pointer |
| pop | O(1) | O(1) | same |
| enqueue | O(1) amortised | O(1) with tail | append / tail pointer |
| dequeue | raw list Θ(n) (`pop(0)` shifts), deque O(1) | O(1) at head | shift vs re-point head |
| k-th element | O(1) | Θ(k) | address arithmetic vs walking `next` |

### Part B — reference `ps7.py`

*(Revised 2026-09-26: the set no longer asks for `ArrayStack` or `LinkedStack` — Lab 7 builds stack
classes — but they stay in this reference because B5 uses a stack. Students may use their Lab 7 `Stack` or a
plain list.)*

```python
from collections import deque
import timeit


# --- B1: Array-based ---
class ArrayStack:
    """Stack on a Python list; the END of the list is the top, so push/pop are O(1) amortised."""
    def __init__(self):
        self._items = []

    def push(self, x):          # O(1) amortised
        self._items.append(x)

    def pop(self):              # O(1)
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):             # O(1)
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self):         # O(1)
        return len(self._items) == 0

    def __len__(self):          # O(1)
        return len(self._items)


class ArrayQueue:
    """Queue on collections.deque: append at the right, popleft at the left, both O(1)."""
    def __init__(self):
        self._items = deque()

    def enqueue(self, x):
        self._items.append(x)

    def dequeue(self):
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)


class NaiveArrayQueue:
    """Queue on a raw list: dequeue is pop(0), which shifts every remaining item -- O(n)."""
    def __init__(self):
        self._items = []

    def enqueue(self, x):
        self._items.append(x)

    def dequeue(self):
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)


# --- B2: Linked ---
class _Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedStack:
    """Top = head: push and pop touch only the head, O(1)."""
    def __init__(self):
        self._head = None
        self._size = 0

    def push(self, x):
        self._head = _Node(x, self._head)
        self._size += 1

    def pop(self):
        if self._head is None:
            raise IndexError("pop from empty stack")
        x = self._head.data
        self._head = self._head.next
        self._size -= 1
        return x

    def peek(self):
        if self._head is None:
            raise IndexError("peek at empty stack")
        return self._head.data

    def is_empty(self):
        return self._head is None

    def __len__(self):
        return self._size


class LinkedQueue:
    """Enqueue at the tail, dequeue at the head: both O(1). The reverse would need the node before
    the tail to dequeue, and a singly linked list can only reach it by walking from the head -- O(n)."""
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def enqueue(self, x):
        node = _Node(x)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self):
        if self._head is None:
            raise IndexError("dequeue from empty queue")
        x = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return x

    def is_empty(self):
        return self._head is None

    def __len__(self):
        return self._size


# --- B3: More linked-list operations ---
class LinkedList:
    def __init__(self, items=()):
        self.head = None
        self.tail = None
        self.size = 0
        for x in items:
            self.append(x)

    def append(self, x):                    # O(1) with the tail pointer
        node = _Node(x)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def to_list(self):                      # O(n)
        out = []
        cur = self.head
        while cur is not None:
            out.append(cur.data)
            cur = cur.next
        return out

    def count(self, x):                     # O(n)
        n = 0
        cur = self.head
        while cur is not None:
            if cur.data == x:
                n += 1
            cur = cur.next
        return n

    def reverse(self):                      # O(n), in place (L23)
        prev = None
        cur = self.head
        self.tail = self.head
        while cur is not None:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    def remove_duplicates(self):            # O(n^2): for each node, scan the rest
        cur = self.head
        while cur is not None:
            runner = cur
            while runner.next is not None:
                if runner.next.data == cur.data:
                    runner.next = runner.next.next
                    self.size -= 1
                else:
                    runner = runner.next
            cur = cur.next
        # the tail may have been removed: find it again
        self.tail = None
        cur = self.head
        while cur is not None:
            self.tail = cur
            cur = cur.next


# --- B5: Two-stack evaluation ---
def tokenize(expression):
    """Split into numbers, operators and parentheses; handles multi-digit numbers and decimals."""
    tokens = []
    number = ""
    for ch in expression:
        if ch.isdigit() or ch == ".":
            number += ch
        else:
            if number:
                tokens.append(number)
                number = ""
            if ch in "+-*/()":
                tokens.append(ch)
    if number:
        tokens.append(number)
    return tokens


def evaluate(expression):
    """Evaluate a fully parenthesised expression with an operand stack and an operator stack."""
    operands = ArrayStack()
    operators = ArrayStack()
    for tok in tokenize(expression):
        if tok == "(":
            continue
        elif tok in "+-*/":
            operators.push(tok)
        elif tok == ")":
            op = operators.pop()
            right = operands.pop()
            left = operands.pop()
            if op == "+":
                operands.push(left + right)
            elif op == "-":
                operands.push(left - right)
            elif op == "*":
                operands.push(left * right)
            else:
                operands.push(left / right)
        else:
            operands.push(float(tok))
    result = operands.pop()
    assert operands.is_empty() and operators.is_empty(), "not fully parenthesised"
    return result


if __name__ == "__main__":
    for S in (ArrayStack, LinkedStack):
        s = S()
        assert s.is_empty() and len(s) == 0
        for x in [1, 2, 3]:
            s.push(x)
        assert s.peek() == 3 and s.pop() == 3 and s.pop() == 2 and len(s) == 1
        try:
            S().pop()
            assert False
        except IndexError:
            pass
    for Q in (ArrayQueue, NaiveArrayQueue, LinkedQueue):
        q = Q()
        for x in [1, 2, 3]:
            q.enqueue(x)
        assert q.dequeue() == 1 and q.dequeue() == 2 and len(q) == 1
        q.enqueue(4)
        assert q.dequeue() == 3 and q.dequeue() == 4 and q.is_empty()
        q.enqueue(5)
        assert q.dequeue() == 5

    ll = LinkedList([1, 2, 3, 4])
    ll.reverse()
    assert ll.to_list() == [4, 3, 2, 1] and ll.head.data == 4 and ll.tail.data == 1
    ll.append(9)
    assert ll.to_list() == [4, 3, 2, 1, 9]
    e = LinkedList(); e.reverse(); assert e.to_list() == []
    d = LinkedList([3, 1, 3, 2, 1, 3])
    d.remove_duplicates()
    assert d.to_list() == [3, 1, 2] and d.size == 3 and d.tail.data == 2
    d.append(7); assert d.to_list() == [3, 1, 2, 7]
    assert LinkedList([1, 2, 1, 1]).count(1) == 3

    assert tokenize("(3 + 4) * 2") == ["(", "3", "+", "4", ")", "*", "2"]
    assert tokenize("(1.5 + 2.25)") == ["(", "1.5", "+", "2.25", ")"]
    cases = [("(3 + 4)", 7.0), ("((3 + 4) * 2)", 14.0), ("((10 - 4) / (1 + 2))", 2.0), ("(0 - 5)", -5.0),
             ("(1.5 + 2.25)", 3.75), ("((2 * 3) - (8 / 4))", 4.0), ("(((1 + 2) * (3 + 4)) - 20)", 1.0),
             ("(100 / (5 * (2 + 2)))", 5.0)]
    for text, expected in cases:
        assert evaluate(text) == expected, (text, evaluate(text))
    print("all asserts passed")

    print(f"\n{'n':>6} {'deque queue':>12} {'list pop(0)':>12} {'ratio':>7}")
    for n in [1000, 5000, 20000, 50000]:
        def run(q):
            for i in range(n):
                q.enqueue(i)
            for i in range(n):
                q.dequeue()
        t1 = timeit.timeit(lambda: run(ArrayQueue()), number=3) / 3
        t2 = timeit.timeit(lambda: run(NaiveArrayQueue()), number=3) / 3
        print(f"{n:>6} {t1 * 1000:>10.2f}ms {t2 * 1000:>10.2f}ms {t2 / t1:>7.1f}")
```

One run of B4:

```
     n  deque queue  list pop(0)   ratio
  1000       0.16ms       0.20ms     1.2
  5000       0.87ms       2.10ms     2.4
 20000       3.18ms      29.26ms     9.2
 50000       8.34ms     229.94ms    27.6
```

`pop(0)` shifts every remaining item, so n dequeues cost about n²/2 shifts; the deque's cost is linear.
The ratio therefore grows roughly in proportion to `n` — a fixed ratio would mean only overhead was measured.

**Marking.** B1 5 each. B2 12 (LinkedQueue must reset `tail` when it empties). B3: 4 / 7 / 7 —
`reverse` must update `tail` (the `append(9)` test catches it); `remove_duplicates` must keep `size` and
`tail` right. B4: 9 table, 5 explanation. B5: 8 tokenizer, 15 evaluator (right operand popped first —
`"(10 - 4)"` giving `-6` is the classic slip), 5 tests.

---

*CS 101 · Week 7 · Problem Set 7 · Due Friday 20 November 2026, 17:00 · © CSE Department*

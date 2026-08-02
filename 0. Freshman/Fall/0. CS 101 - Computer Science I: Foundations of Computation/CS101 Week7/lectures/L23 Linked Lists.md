# CS 101 · Lecture 23 (Week 7, Lecture 2)
## Linked Lists: Singly and Doubly Linked

**Week 7 · Thursday**
*"Building your own linked list forces you to confront every design decision the underlying array-based structures made for you invisibly." — CS 101*

---

## 0. The Alternative to Contiguous Memory

Wednesday established that Python lists are contiguous dynamic arrays — great for random access (O(1)), poor for front insertion/removal (O(n)). Today we build a fundamentally different structure: one where elements are **scattered in memory**, connected by explicit pointers. This is the **linked list**.

---

## 1. The Core Idea — Nodes and Pointers

A linked list is built from **nodes**. Each node holds:
1. A piece of **data**
2. A **pointer** (reference) to the next node

```
head → [10 | •]→ [20 | •]→ [30 | •]→ [40 | None]
```

Unlike an array, these nodes are **not** stored at consecutive memory addresses. Each node can live anywhere in memory — the only thing connecting them is the explicit pointer stored inside each node.

### Implementing a Node

```python
class Node:
    """A single node in a singly linked list."""
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def __repr__(self):
        return f"Node({self.data!r})"
```

### Building a List by Hand

```python
# Manually construct: 10 -> 20 -> 30 -> None
third  = Node(30, None)
second = Node(20, third)
first  = Node(10, second)
head = first

# Traverse and print:
current = head
while current is not None:
    print(current.data)
    current = current.next
# 10
# 20
# 30
```

---

## 2. The Complete Singly Linked List Class

```python
class LinkedList:
    """
    A singly linked list implementation.

    Maintains a reference to the head node. Optionally tracks size
    and a tail reference for O(1) append (see optimization below).
    """

    def __init__(self):
        self.head = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self.head is None

    def prepend(self, data):
        """
        Insert data at the front of the list. O(1).
        """
        new_node = Node(data, self.head)
        self.head = new_node
        self._size += 1

    def append(self, data):
        """
        Insert data at the end of the list. O(n) — must traverse to find the end.
        (We will optimize this to O(1) with a tail pointer, below.)
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def find(self, target):
        """
        Return True if target is in the list. O(n).
        """
        current = self.head
        while current is not None:
            if current.data == target:
                return True
            current = current.next
        return False

    def remove(self, target):
        """
        Remove the first occurrence of target. O(n).
        Returns True if removed, False if not found.
        """
        if self.head is None:
            return False

        # Special case: removing the head
        if self.head.data == target:
            self.head = self.head.next
            self._size -= 1
            return True

        # General case: find the node BEFORE the target
        current = self.head
        while current.next is not None:
            if current.next.data == target:
                current.next = current.next.next   # unlink the target node
                self._size -= 1
                return True
            current = current.next

        return False

    def to_list(self):
        """Convert to a Python list, for easy testing/printing. O(n)."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def __repr__(self):
        return " -> ".join(str(x) for x in self.to_list()) + " -> None"


# Tests:
ll = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)
print(ll)              # 10 -> 20 -> 30 -> None
ll.prepend(5)
print(ll)              # 5 -> 10 -> 20 -> 30 -> None
print(ll.find(20))     # True
print(ll.find(99))     # False
ll.remove(20)
print(ll)              # 5 -> 10 -> 30 -> None
print(len(ll))          # 3
```

---

## 3. Analyzing Every Operation — The Complexity Table

| Operation | Singly Linked List | Python List (Array) |
|-----------|--------------------|-----------------------|
| Access by index `lst[i]` | O(n) — must traverse from head | O(1) |
| Insert at front | O(1) | O(n) |
| Insert at end (naive, no tail pointer) | O(n) | O(1) amortized |
| Insert at end (with tail pointer) | O(1) | O(1) amortized |
| Remove from front | O(1) | O(n) |
| Remove from end | O(n) — must traverse to find second-to-last | O(1) |
| Search for value | O(n) | O(n) |
| Memory overhead per element | Higher (extra pointer per node) | Lower (just the pointer to data, no extra) |

**The fundamental tradeoff, precisely stated:** linked lists trade O(1) random access (which they don't have) for O(1) front insertion/removal (which arrays don't have). Neither structure is "better" — they are optimized for different access patterns.

---

## 4. Optimizing Append with a Tail Pointer

The naive `append` above is O(n) because it must walk the entire list to find the end. We fix this by maintaining an explicit **tail** reference:

```python
class LinkedListWithTail:
    """Singly linked list with O(1) append via a tail pointer."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def append(self, data):
        """Insert at the end. O(1) — no traversal needed!"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def prepend(self, data):
        """Insert at the front. O(1)."""
        new_node = Node(data, self.head)
        self.head = new_node
        if self.tail is None:      # list was empty
            self.tail = new_node
        self._size += 1

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result
```

**The lesson:** the same ADT (a list of elements) can have wildly different performance depending on *what auxiliary information* you maintain (in this case, a tail pointer). This is a recurring theme in data structure design — small amounts of extra bookkeeping can eliminate entire classes of expensive operations.

---

## 5. Doubly Linked Lists — Pointers in Both Directions

A **doubly linked list** adds a `prev` pointer to each node, enabling traversal in both directions.

```python
class DNode:
    """A node in a doubly linked list."""
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


class DoublyLinkedList:
    """
    A doubly linked list with head and tail pointers.
    Enables O(1) removal from EITHER end (unlike singly linked lists,
    where removing from the tail is O(n)).
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def append(self, data):
        """Insert at the end. O(1)."""
        new_node = DNode(data, prev=self.tail)
        if self.tail is None:
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self._size += 1

    def prepend(self, data):
        """Insert at the front. O(1)."""
        new_node = DNode(data, next=self.head)
        if self.head is None:
            self.tail = new_node
        else:
            self.head.prev = new_node
        self.head = new_node
        self._size += 1

    def remove_last(self):
        """
        Remove and return the last element. O(1) — this is the key
        advantage over a singly linked list, where this would be O(n)!
        """
        if self.tail is None:
            raise IndexError("remove from empty list")

        data = self.tail.data
        self.tail = self.tail.prev

        if self.tail is None:      # list is now empty
            self.head = None
        else:
            self.tail.next = None

        self._size -= 1
        return data

    def remove_first(self):
        """Remove and return the first element. O(1)."""
        if self.head is None:
            raise IndexError("remove from empty list")

        data = self.head.data
        self.head = self.head.next

        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None

        self._size -= 1
        return data

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def to_list_reversed(self):
        """Traverse backward from the tail — impossible in a singly linked list!"""
        result = []
        current = self.tail
        while current is not None:
            result.append(current.data)
            current = current.prev
        return result


# Tests:
dll = DoublyLinkedList()
dll.append(1)
dll.append(2)
dll.append(3)
print(dll.to_list())            # [1, 2, 3]
print(dll.to_list_reversed())   # [3, 2, 1]
print(dll.remove_last())        # 3
print(dll.remove_first())       # 1
print(dll.to_list())            # [2]
```

### Why Doubly Linked Removal-From-Tail Is O(1)

In a **singly** linked list, removing the last node requires finding the **second-to-last** node (to set its `next` to `None`) — but you can only reach it by traversing from the head, which is O(n).

In a **doubly** linked list, the last node already has a `prev` pointer directly to the second-to-last node. No traversal needed — O(1).

This single difference — one extra pointer per node — is why Python's `collections.deque` (Friday's topic) is implemented as a doubly linked structure internally, giving it O(1) operations at **both** ends.

---

## 6. Memory Overhead — The Real Cost of Linked Structures

Every node in a linked list carries overhead beyond the data itself:

```
Singly linked node:  [data | next]              — 1 extra pointer
Doubly linked node:  [prev | data | next]        — 2 extra pointers
Python list element: [pointer to data]            — the array itself has no
                                                     per-element overhead beyond
                                                     the pointer slot
```

For a list of a million small integers:
- **Python list:** ~1,000,000 pointers in one contiguous block, plus 1,000,000 boxed integer objects (Python ints are objects, not raw machine words — this overhead exists for lists too)
- **Singly linked list:** 1,000,000 separate Node objects, each with its own memory allocation overhead, PLUS the same 1,000,000 boxed integers, PLUS 1,000,000 `next` pointers

Linked lists have significantly higher memory overhead per element due to:
1. **Non-contiguous allocation** — each node is a separate object with its own allocation bookkeeping
2. **Extra pointers** — one (or two) per node, beyond what arrays need
3. **Cache locality (relevant in CS 201/architecture)** — scattered memory means the CPU cache can't prefetch efficiently, causing real-world slowdowns beyond what Big-O captures

You will measure this difference directly in tomorrow's lab using Python's `sys.getsizeof()` and memory profiling tools.

---

## 7. When Would You Actually Use a Linked List?

Given that Python's built-in list handles most cases well (and `collections.deque` handles fast front/back operations), when does a hand-rolled linked list make sense?

**Genuine use cases:**
- **Implementing other ADTs** — stacks and queues are naturally expressed via linked lists (Friday's lecture)
- **Frequent insertion/deletion in the MIDDLE**, when you already have a reference to the node (O(1) if you have the node reference; the search to find it is still O(n))
- **Building more complex structures** — trees (Week 8+), graphs (CS 102), and skip lists all use linked-node concepts as building blocks
- **Educational value** — understanding pointers and manual memory management prepares you directly for PROG 101 (C), where you'll implement linked lists with raw pointers and manual `malloc`/`free`

**In everyday Python code:** use the built-in `list` or `collections.deque`. Hand-rolling a linked list in production Python code is rare — but the concepts here are foundational for every data structure course, systems course, and technical interview you will ever encounter.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Node | Data + pointer(s) to neighboring node(s) |
| Singly linked list | One `next` pointer per node; O(1) front ops, O(n) most else |
| Tail pointer optimization | Turns O(n) append into O(1) — small bookkeeping, big payoff |
| Doubly linked list | Adds `prev` pointer; enables O(1) removal from BOTH ends |
| Memory overhead | Linked structures cost more per element than arrays |
| Real-world usage | Rare directly in Python; foundational for stacks/queues/trees/graphs |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** This `append` walks to the end of the list each time. Give its complexity, then the complexity of building an n-element list with it, and explain how a tail pointer changes both.

```python
def append(self, value):
    node = Node(value)
    if self.head is None:
        self.head = node
        return
    cur = self.head
    while cur.next is not None:
        cur = cur.next
    cur.next = node
```

**2. (Explain.)** Linked lists have O(1) insertion and arrays O(n), yet arrays win most real benchmarks even for insertion-heavy workloads. Explain the two separate reasons.

**3. (Build.)** Write `reverse()` for a singly linked list, in place, in Θ(n) time and Θ(1) space. Explain why three pointers are needed rather than two.

**4. (Stretch.)** Doubly linked lists make deletion Θ(1) given a node reference. Name a real data structure that depends on this and explain why a singly linked list or an array could not serve.


### Answers

**1.** A single `append` is **Θ(n)** — it traverses the whole list to find the last node. Building an n-element list is therefore 0 + 1 + 2 + … + (n−1) = **Θ(n²)**.

With a `self.tail` pointer maintained alongside `self.head`, `append` becomes:

```python
def append(self, value):
    node = Node(value)
    if self.tail is None:
        self.head = self.tail = node
    else:
        self.tail.next = node
        self.tail = node
```

Now a single `append` is **Θ(1)** and building n elements is **Θ(n)** — a quadratic-to-linear improvement for the cost of one extra field.

The catch is that the tail pointer becomes an **invariant every other method must maintain**. `pop()`, `remove()`, `clear()`, and `insert_at()` must all update it, and the failure mode is nasty: a stale tail pointing at a removed node leaves `append` silently attaching to a detached fragment, so elements vanish with no error. This is the general trade of caching a derived value — the speedup is real, and so is the new class of bug. When you add such a field, enumerate every method that can invalidate it *before* writing any of them.

**2.** **1. O(1) insertion assumes you already hold the node.** Inserting into a linked list is two pointer writes *once you are at the right place* — but getting there is a **Θ(n) traversal**, because linked lists have no random access. So "insert at position k" is Θ(k) for a linked list and Θ(n−k) for an array. The array's shift is linear, but it is a `memmove` of contiguous bytes; the list's traversal is linear in *pointer dereferences*. The list only wins when you arrived at the position by other means — you already hold a reference, as in an LRU cache where the node came from a dict.

**2. Cache locality.** An array's elements are adjacent, so one cache-line fetch (64 bytes) brings in several at once and the hardware prefetcher predicts the next one. A linked list's nodes are wherever the allocator put them, so each `cur = cur.next` is a potential cache miss — and a main-memory access is on the order of 100× the cost of an L1 hit. Traversing a list can therefore be a hundred times slower than traversing an array of the same length, with identical Θ(n) complexity.

There is a memory cost too: each Python node object carries an object header plus two references, typically 50+ bytes to store one 8-byte pointer's worth of payload, versus 8 bytes per slot in a list.

This is the clearest case in the course of **Big-O being necessary but not sufficient.** Both operations are Θ(n); the constants differ by two orders of magnitude, and the constants are what you feel.

**3.**

```python
def reverse(self):
    prev = None
    cur = self.head
    while cur is not None:
        nxt = cur.next      # save before we destroy it
        cur.next = prev     # flip the link
        prev = cur          # advance
        cur = nxt
    self.head = prev
```

Three pointers are needed because **the assignment `cur.next = prev` destroys the only reference to the rest of the list**. Once that link is overwritten, everything beyond `cur` is unreachable. So `nxt` must capture it first. With only `prev` and `cur` you would flip the first link and then have no way to continue — the classic version of this bug loses the entire tail on the first iteration.

*Invariant:* at the top of each iteration, the nodes before `cur` have been reversed and `prev` is the head of that reversed portion; `cur` is the head of the not-yet-processed remainder. On exit `cur` is `None`, so everything is reversed and `prev` is the new head — which is why the final line assigns `prev` and not `cur`. Forgetting that leaves `self.head` pointing at what is now the last node, and the list appears to have one element.

Space is Θ(1): three pointers regardless of length. The recursive version is Θ(n) space and blows the stack past ~1000 nodes, which makes this one of the few places where the iterative form is strictly better.

**4.** The **LRU cache** — used in CPU caches, database buffer pools, and `functools.lru_cache`.

The structure is a dict plus a doubly linked list. The dict maps each key to its **node**, and the list maintains recency order: most-recently-used at the head, least-recently-used at the tail. On a `get`, you must move the accessed node to the front, which means **unlinking it from its current position and relinking at the head** — and the whole design needs that to be O(1), since it happens on every single access.

Unlinking a node requires updating its predecessor's `next`. A **doubly** linked node knows its predecessor directly (`node.prev.next = node.next; node.next.prev = node.prev`), so this is O(1). A **singly** linked list would have to traverse from the head to find the predecessor — Θ(n) per access, destroying the point of the cache.

An **array** fails differently: it supports random access but removing an element from the middle requires shifting everything after it, Θ(n) again. The requirement here is unusual and worth naming — **O(1) removal from an arbitrary interior position, reached by reference rather than by index** — and the doubly linked list is essentially the only structure that provides it.

The dict supplies the reference the list cannot find on its own. Neither structure could do this alone; the combination is what makes both operations O(1), and it is a good example of composing data structures so each covers the other's weakness.



---

## Reading

- **Guttag, Ch. 5** (if linked structures are covered) or supplementary handout
- **CLRS, Ch. 10.2** — Linked Lists (formal treatment with pseudocode)

---

*CS 101 · Week 7 · Lecture 23 (Thu) · © CSE Department*

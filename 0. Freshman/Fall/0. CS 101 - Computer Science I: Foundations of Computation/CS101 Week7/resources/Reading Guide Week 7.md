# CS 101 — Week 7 Reading Guide & Resources
## Data Structures I: Lists, Stacks, and Queues

---

## Required Reading

### Guttag — Introduction to Computation and Programming Using Python

**Chapter 5 — Structured Types, Mutability, and Higher-Order Functions**
- §5.1 — Tuples
- §5.2 — Lists and Mutability
- §5.3 — Functions as Objects (revisit — connects to Week 3)

Focus on the mutability discussion in §5.2 — you first saw this in Week 1, but now you understand *why* it works the way it does at the memory level.

### CLRS — Introduction to Algorithms (Supplementary)

**Chapter 10 — Elementary Data Structures**
- §10.1 — Stacks and Queues (formal pseudocode treatment)
- §10.2 — Linked Lists (formal pseudocode, including the "sentinel" technique — an advanced simplification you may find interesting, though not required for this course)

### Python Documentation

- **Time Complexity wiki:** https://wiki.python.org/moin/TimeComplexity — the authoritative reference for every built-in operation's complexity. Bookmark this permanently.
- **collections.deque docs:** https://docs.python.org/3/library/collections.html#collections.deque

---

## Focused REPL / Experimentation Sessions

### Session A: Feeling the List Resize Behavior (15 min)

```python
import sys

lst = []
last_size = sys.getsizeof(lst)
print(f"Initial (empty): {last_size} bytes")

for i in range(30):
    lst.append(i)
    size = sys.getsizeof(lst)
    if size != last_size:
        print(f"  After {i+1} appends: size jumped to {size} bytes")
        last_size = size

# Notice: Python doesn't grow the array by exactly 1 slot each time.
# It over-allocates, so most appends don't trigger a resize at all.
```

### Session B: The Front vs. Back Asymmetry, Directly Measured (15 min)

```python
import time

def time_n_operations(op, n):
    lst = list(range(n))
    start = time.perf_counter()
    op(lst)
    return time.perf_counter() - start

def append_100(lst):
    for _ in range(100):
        lst.append(0)

def insert_front_100(lst):
    for _ in range(100):
        lst.insert(0, 0)

for n in [1000, 10000, 100000, 1000000]:
    t_append = time_n_operations(append_100, n)
    t_insert = time_n_operations(insert_front_100, n)
    print(f"n={n:8}: append×100={t_append*1000:8.3f}ms  insert(0)×100={t_insert*1000:8.3f}ms  ratio={t_insert/t_append:6.1f}x")

# As n grows, insert(0,x)'s cost grows roughly linearly with n.
# append's cost stays roughly constant. This IS the O(1) vs O(n) difference,
# made completely visible.
```

### Session C: Building Intuition for Pointer-Based Structures (15 min)

```python
# Simulate what a linked list "feels like" using nested tuples,
# to build intuition before writing the full Node class.

# (data, rest) where rest is either another tuple or None
lst = (1, (2, (3, (4, None))))

def to_python_list(nested):
    """Convert the nested-tuple structure to a Python list."""
    result = []
    while nested is not None:
        data, nested = nested
        result.append(data)
    return result

print(to_python_list(lst))   # [1, 2, 3, 4]

def prepend(data, nested):
    """O(1) - just wrap in a new tuple. No copying of existing data!"""
    return (data, nested)

new_lst = prepend(0, lst)
print(to_python_list(new_lst))   # [0, 1, 2, 3, 4]
print(to_python_list(lst))       # [1, 2, 3, 4] — ORIGINAL UNCHANGED!

# This demonstrates a key property of linked structures: prepending
# doesn't require touching (or copying) any existing nodes — you just
# create ONE new node pointing to the existing structure. This is the
# foundation of "persistent" (immutable) data structures used heavily
# in functional programming languages like Haskell and Clojure.
```

---

## Conceptual Exercises (Paper and Pencil)

**Exercise 1:** Draw a diagram (boxes and arrows) of the memory layout for a Python list `[10, 20, 30]` vs. a singly linked list containing the same three values. Label every pointer.

**Exercise 2:** You need a data structure to implement a browser's "back" and "forward" navigation buttons. Which Week 7 ADT(s) would you use, and how would clicking "back" then visiting a NEW page (not using forward) affect your chosen structure(s)? (Hint: this is structurally similar to the Undo/Redo editor from Lab 7.)

**Exercise 3:** A singly linked list has a `tail` pointer but NOT a `prev` pointer on each node. Explain precisely why `remove_last()` is still O(n) for this structure, even with the tail pointer. What SPECIFIC additional pointer would make it O(1)? (This is exactly the motivation for the doubly linked list.)

**Exercise 4:** For each scenario, state which structure (Python list, `collections.deque`, hand-rolled singly linked list, hand-rolled doubly linked list) is most appropriate, and justify with a complexity argument:
- (a) A music player's "history" of recently played songs, where you frequently jump back several songs
- (b) A print spooler processing jobs in the order submitted
- (c) A dataset you need to binary search repeatedly by index
- (d) The undo history of a text editor (only ever undo the MOST RECENT action, or redo it)

---

## Complexity Reference Card

```
PYTHON LIST (Dynamic Array)
────────────────────────────
lst[i]                O(1)
lst[i] = x             O(1)
len(lst)               O(1)
lst.append(x)          O(1) amortized
lst.pop()              O(1)
lst.pop(0)             O(n)
lst.insert(0, x)       O(n)
x in lst               O(n)
lst[i:j]               O(j-i)
lst1 + lst2            O(len(lst1)+len(lst2))

SINGLY LINKED LIST (with tail pointer)
────────────────────────────────────────
prepend(x)             O(1)
append(x)              O(1)   [requires tail pointer]
remove from head       O(1)
remove from tail       O(n)   [must find new tail — no prev pointer!]
find(x)                O(n)
get(i)                 O(n)

DOUBLY LINKED LIST (with head + tail pointers)
────────────────────────────────────────────────
prepend(x)             O(1)
append(x)              O(1)
remove from head       O(1)
remove from tail       O(1)   [prev pointer makes this possible!]
find(x)                O(n)
get(i)                 O(n)

collections.deque
────────────────────
append (right)         O(1)
appendleft (left)       O(1)
pop (right)             O(1)
popleft (left)          O(1)
d[i]  (indexing)        O(n)   [NOT O(1) — internally block-linked, not contiguous!]

STACK ADT (LIFO)                QUEUE ADT (FIFO)
─────────────────                ────────────────
push    → O(1)                  enqueue → O(1)
pop     → O(1)                  dequeue → O(1)  [use deque, NOT list.pop(0)!]
peek    → O(1)                  peek    → O(1)
```

---

## Common Mistakes This Week

**Mistake 1: Building a queue with `list.pop(0)`**
```python
class BadQueue:
    def dequeue(self):
        return self._data.pop(0)   # O(n) — catastrophic for large queues!
```
Always use `collections.deque` for queue behavior, never a raw list with front operations.

**Mistake 2: Forgetting to update the tail pointer when removing the last element**
```python
def remove(self, target):
    # ... found and unlinked target ...
    # BUG: forgot to check if target WAS self.tail!
    # Now self.tail points to a node that's no longer in the list.
```
Any time you remove a node, ask: "could this have been the tail (or head)? Did I update that pointer?"

**Mistake 3: Confusing a Stack's "top" with a Queue's "front"**
Both structures conceptually have "an end you interact with," but they behave oppositely (LIFO vs FIFO). Mixing up your mental model between the two is a common source of logic errors when translating between them.

**Mistake 4: Assuming `deque` indexing is O(1) like a list**
```python
d = collections.deque(range(1000000))
x = d[500000]   # O(n), NOT O(1)! Deques are NOT arrays internally.
```
Use `deque` for its O(1) end-operations; use `list` when you need O(1) random access by index. Don't assume you get both for free.

**Mistake 5: Not testing edge cases (empty structure) for every method**
Every Stack/Queue/LinkedList method should be tested against an empty structure — this is where off-by-one and null-pointer-style bugs hide.

---

## Week 7 Self-Test

1. What is an Abstract Data Type? How does it differ from a concrete implementation?
2. Why is `lst[i]` O(1) for a Python list but O(n) for a linked list?
3. Why is `lst.append(x)` O(1) amortized but `lst.insert(0,x)` is O(n)?
4. What extra pointer does a doubly linked list have that a singly linked list doesn't? What operation does it make O(1) that would otherwise be O(n)?
5. Which end of a Python list should you use as the "top" of a stack, and why?
6. Why is a raw Python list a poor choice for implementing a queue? What should you use instead?
7. What is the complexity of indexing into the MIDDLE of a `collections.deque`? Why?
8. Name one genuine, non-Python-built-in use case where you would hand-roll a linked list instead of using a Python list.
9. In the "tortoise and hare" cycle detection algorithm, why must the fast pointer eventually catch up to the slow pointer if a cycle exists?
10. What ADT would you use for: browser history "back" button? Undo/redo? A print queue? Function call tracking?

*(Answers: 1. ADT = specification of behavior only; implementation = concrete memory representation. 2. arrays: direct address computation; linked lists: must follow pointers sequentially. 3. append writes to unused capacity (rare resizes); insert(0,x) must shift every element. 4. prev pointer; makes remove-from-tail O(1). 5. the END — append/pop are both O(1) there. 6. front removal (pop(0)) is O(n); use collections.deque instead. 7. O(n) — deque is block-linked internally, not contiguous. 8. implementing other ADTs (stacks/queues), or building trees/graphs. 9. within a cycle of length L, the fast pointer gains 1 step on the slow pointer each iteration, so it must close any gap within L iterations. 10. back button: Stack (or two stacks for back+forward); undo/redo: two Stacks; print queue: Queue; call tracking: Stack (the call stack itself!).)*

---

## Preview: Week 8

Week 8 covers **Data Structures II: Hash Tables and Sets** — arguably the single most practically important data structure in all of computer science. You'll learn exactly how Python's `dict` and `set` achieve their famous O(1) average-case lookup, what a hash function is, how collisions are resolved, and why the load factor matters.

Before Wednesday, think about this: you've been using `x in lst` (O(n)) all course. What would it take to check membership in O(1) instead? What information would you need to precompute?

---

*CS 101 · Week 7 · Reading Guide · © CSE Department*

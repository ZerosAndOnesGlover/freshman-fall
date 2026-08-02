# CS 101 — Problem Set 7
## Stacks, Queues, and Linked Structures

**Released:** Friday, Week 7
**Due:** Friday, Week 8 at 11:59 PM
**Submission:** Upload `ps7.py` and `PS 7 Stacks and Queues.md`
**Weight:** Part of the 30% Problem Sets grade

**Note:** Project 1 was assigned this week (see `PROJECT 1 Data Analysis Tool.md`) and is due Week 9. Budget your time accordingly — do not let PS7 crowd out Project 1 progress.

---

## Overview

This problem set covers:
- Implementing the Stack and Queue ADTs using BOTH array-based and linked-list-based backing
- Analyzing and justifying the complexity of every operation in each implementation
- Applying stacks and queues to solve real algorithmic problems
- Comparing implementation tradeoffs empirically and in writing
- Extending linked list operations beyond what was covered in lecture

**Every implementation must have:**
- A complete docstring stating time complexity for every method
- At least 3 `assert` tests including edge cases (empty structure, single element)

---

## Part A: Written Questions (`PS 7 Stacks and Queues.md`)

### A1: ADT vs. Implementation (6 points)

**(a)** Explain, in your own words, the difference between an Abstract Data Type and a concrete implementation. Use the Stack ADT as your example, describing at least two different implementations that satisfy it.

**(b)** A classmate implements a Stack using a Python list, but chooses to `insert(0, x)` for push and `pop(0)` for pop (using the FRONT of the list as the "top"). Explain precisely why this is a valid implementation of the Stack ADT (it still obeys LIFO) but a poor engineering choice. State the complexity of each operation in this version.

### A2: Complexity Justification (8 points)

For each operation, state its time complexity for BOTH the array-based and linked-list-based implementation, and briefly justify each answer (referencing the underlying memory model).

| Operation | Array-based | Linked-list-based | Justification |
|-----------|-------------|---------------------|----------------|
| Stack push | | | |
| Stack pop | | | |
| Queue enqueue (at back) | | | |
| Queue dequeue (from front, SINGLY linked, no tail pointer optimization for removal) | | | |

### A3: Application Design (6 points)

**(a)** Describe (in words, no code) how you would use a Stack to reverse the order of elements in a Queue, without using any other data structure besides the Queue and one Stack. What is the time complexity of your approach?

**(b)** Explain how a Queue is used in Breadth-First Search (BFS) — you don't need to know BFS formally yet (that's CS 102), but based on what you know about FIFO order, explain intuitively why a Queue (not a Stack) is the right structure for exploring a graph or tree "layer by layer."

---

## Part B: Python Implementation (`ps7.py`)

### B1: Array-Based Stack and Queue (10 points)

**(a)** `ArrayStack` — implement using a Python list. Methods: `push`, `pop`, `peek`, `is_empty`, `size`. Choose the end of the list as the top (justify this choice in a comment).

**(b)** `ArrayQueue` — implement using a Python list, but this time use `collections.deque` internally (NOT a raw list with `pop(0)`, which would be O(n)). Methods: `enqueue`, `dequeue`, `peek`, `is_empty`, `size`.

**(c)** `NaiveArrayQueue` — implement using ONLY a raw Python list (no deque), with `enqueue` appending to the end and `dequeue` using `pop(0)`. This is intentionally the "wrong" way — you will benchmark it against (b) in B4.

---

### B2: Linked-List-Based Stack and Queue (10 points)

**(a)** `LinkedStack` — implement using your own singly linked node structure (define a private `_Node` class inside, or reuse the `Node` class from lab). Top = head of the list.

**(b)** `LinkedQueue` — implement using your own singly linked node structure WITH a tail pointer. Enqueue at tail, dequeue from head (justify why this choice, not the reverse, in a comment).

---

### B3: Extended Linked List Operations (16 points)

Extend the `LinkedList` class (from lab, reproduce/import it) with these additional methods. Each must state its time complexity in the docstring.

**(a)** `reverse()` — reverse the linked list IN PLACE (don't create new nodes; just re-point the existing `next` pointers). Update `head` and `tail` accordingly.
- Time: O(n)

**(b)** `middle()` — return the data at the middle node. For even-length lists, return the second of the two middle elements. Use the "slow and fast pointer" technique: advance one pointer by 1 step and another by 2 steps each iteration; when the fast pointer reaches the end, the slow pointer is at the middle. Do NOT use `len()` and index into the middle — this must be a single O(n) pass, not O(n) to count plus O(n) to traverse again.
- Time: O(n), single pass

**(c)** `has_cycle()` — return True if the linked list contains a cycle (a node's `next` eventually points back to an earlier node, so traversal would loop forever). Use Floyd's Cycle Detection algorithm (the "tortoise and hare"): one pointer advances 1 step at a time, another advances 2 steps at a time; if they ever meet, there's a cycle; if the fast pointer reaches `None`, there isn't.
- Time: O(n)
- **Test note:** you'll need to manually construct a cyclic structure for testing (e.g., set the last node's `.next` to point back to an earlier node) — be careful not to call `to_list()` or any method that would infinite-loop on such a structure!

**(d)** `remove_duplicates()` — remove duplicate values from the list, keeping only the first occurrence of each value, preserving order. Do this WITHOUT using a Python `set` or `dict` (practice the pattern using only list/linked-list operations) — though you may discuss in a comment how a set would make this O(n) instead of O(n²).
- Time: O(n²) without a set, O(n) with one (implement the O(n²) version; mention the O(n) alternative in a comment)

**(e)** `merge_sorted(other)` — given `self` and `other` are both ALREADY SORTED linked lists, merge them into a single new sorted `LinkedList`, without converting to Python lists. This is the linked-list analog of the `merge()` function from Week 4/5's merge sort.
- Time: O(n + m) where n, m are the lengths of the two lists

---

### B4: Empirical Comparison (12 points)

**(a)** Benchmark `ArrayQueue` (using `deque`) vs. `NaiveArrayQueue` (using raw list `pop(0)`) for a sequence of n `enqueue` followed by n `dequeue` operations, at n = 1000, 5000, 20000, 50000. Print a table of timings.

**(b)** Benchmark `ArrayStack` vs. `LinkedStack` for a sequence of n `push` followed by n `pop` operations, at the same sizes. Print a table of timings. (You should find these are roughly comparable — both are O(1) per operation — unlike the queue comparison in (a).)

**(c)** In `PS 7 Stacks and Queues.md`, write a short paragraph (4-6 sentences) interpreting your results from (a) and (b): why does the queue implementation choice matter dramatically, while the stack implementation choice matters much less?

---

### B5: Application — Expression Evaluation (14 points)

Build a calculator that evaluates fully-parenthesized arithmetic expressions using TWO stacks (one for operators, one for operands) — the classic "two-stack" algorithm (a simplified form of Dijkstra's shunting-yard algorithm).

**(a)** `tokenize(expression)` — split an expression string into a list of tokens (numbers, operators, parentheses). Handle multi-digit numbers and decimals.
- `tokenize("(3 + 4) * 2")` → `['(', '3', '+', '4', ')', '*', '2']`
- `tokenize("(1.5 + 2.25)")` → `['(', '1.5', '+', '2.25', ')']`

**(b)** `evaluate(expression)` — evaluate a fully-parenthesized expression using the two-stack algorithm:
```
For each token:
    If it's a number: push onto the OPERAND stack
    If it's an operator (+, -, *, /): push onto the OPERATOR stack
    If it's '(' : ignore (or push, depending on your variant — document your choice)
    If it's ')' : pop an operator and the top two operands, apply the operator,
                  push the result back onto the operand stack
At the end: the operand stack has exactly one value — the result
```
- `evaluate("(3 + 4)")` → `7.0`
- `evaluate("((3 + 4) * 2)")` → `14.0`
- `evaluate("((10 - 4) / (1 + 2))")` → `2.0`

**(c)** Extend `evaluate` to handle unary negation, e.g. `evaluate("(0 - 5)")` → `-5.0` (this should already work with your basic operators — verify and add a specific test).

**(d)** Write a test suite with at least 8 test expressions of varying complexity (nested parentheses, all four operators, decimals).

---

## Grading Rubric

| Problem | Points | Key Criteria |
|---------|--------|--------------|
| A1 ADT vs implementation | 6 | Clear distinction; valid but poor example explained |
| A2 Complexity table | 8 | All 8 cells correct with justification |
| A3 Application design | 6 | Valid stack-reversal approach; valid BFS/queue intuition |
| B1 Array-based | 10 | All 3 classes correct, correct end-choice justified |
| B2 Linked-based | 10 | Both classes correct, correct design choices justified |
| B3 Extended operations | 16 | All 5 methods correct and within stated complexity |
| B4 Empirical comparison | 12 | Correct benchmarks; valid interpretive paragraph |
| B5 Expression evaluator | 14 | Tokenizer + evaluator correct on 8+ test cases |
| **Total** | **82** | |
| Docstring/complexity rigor | up to 5 bonus | |

---

## Part C: Challenge Problems (Ungraded)

**C1: LRU Cache**
Implement an `LRUCache` (Least Recently Used cache) with O(1) `get` and `put` operations, using a combination of a doubly linked list (to track usage order) and a dictionary (to map keys to nodes for O(1) lookup — dictionaries are covered in Week 8, so you may need to preview `dict` basics, or wait and revisit this after Week 8). This is one of the most common technical interview questions in the industry.

**C2: Min-Stack**
Implement a `MinStack` that supports `push`, `pop`, `peek`, AND `get_min()` — all in O(1). The trick: maintain a second, auxiliary stack that tracks the minimum value at each point in the main stack's history.

**C3: Sliding Window Maximum**
Given an array and a window size k, find the maximum value in each sliding window of size k as it slides across the array, in O(n) total time (not O(nk)). Use a `deque` that maintains indices in a clever monotonic order. This is a genuinely difficult but beautiful application of deques.

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading Rubric above (82 + up to 5 bonus).
> No errata found — all stated example values verified.

---

### Part A — Written (20 points)

**A1 ADT vs. Implementation (6 pts).**

**(a)** An **ADT** specifies *what* operations exist and what they mean (their contract), independent of representation. The **Stack ADT** is: `push`, `pop`, `peek`, `is_empty`, `size`, with the LIFO guarantee that `pop` returns the most recently pushed item not yet popped. Two conforming implementations: (i) a dynamic array with the top at the **end** of the array; (ii) a singly linked list with the top at the **head**. Both satisfy the identical contract; callers cannot tell them apart through the interface alone. That substitutability is the point of an ADT.

**(b)** Using `insert(0, x)` / `pop(0)` **is valid** — the last item inserted at the front is the first removed from the front, so LIFO holds and every ADT guarantee is met. But it is a poor engineering choice: a Python list is a contiguous array, so inserting or removing at index 0 must shift **every** remaining element one slot.

| Operation | This version | Standard (end-of-list) |
|---|---|---|
| push | **O(n)** | O(1) amortized |
| pop | **O(n)** | O(1) |
| peek | O(1) | O(1) |

n pushes therefore cost Θ(n²) instead of Θ(n). *This is the same defect measured empirically in B4(a).*

*Grading: 3 pts (a) — must name two distinct implementations. 3 pts (b) — 1 for "valid, LIFO still holds", 2 for the complexity table plus the memory-shifting reason. A student who says it is *invalid* loses all 3: it satisfies the contract, and distinguishing correctness from efficiency is the entire lesson.*

**A2 Complexity Table (8 pts).** 1 pt per cell.

| Operation | Array-based | Linked-list | Justification |
|---|---|---|---|
| Stack push | **O(1)** amortized | **O(1)** | Array: append at the end, no shifting; occasional O(n) resize amortizes to O(1). Linked: allocate a node, re-point head. |
| Stack pop | **O(1)** | **O(1)** | Array: remove from the end, nothing shifts. Linked: advance head, drop the old node. |
| Queue enqueue (back) | **O(1)** amortized | **O(1)** *with tail pointer* | Array: append. Linked: without a tail pointer this degrades to O(n) — the pointer is what buys O(1). |
| Queue dequeue (front) | **O(n)** with a raw list | **O(1)** | Array: `pop(0)` shifts all n−1 remaining elements. Linked: just advance head — no shifting, since nodes are independently allocated. |

*The recurring theme to look for: arrays pay for **contiguity** (cheap at the end, expensive at the front); linked lists pay for **indirection** (cheap at any held pointer, but no random access).*

**A3 Application Design (6 pts).** 3 pts each.

**(a)** Dequeue every element from the queue, pushing each onto the stack, until the queue is empty (n dequeues + n pushes). Then pop every element off the stack, enqueuing each back into the queue (n pops + n enqueues). The stack's LIFO order inverts the queue's FIFO order, so the queue ends up reversed. **Θ(n) time, Θ(n) auxiliary space.**

**(b)** BFS must finish exploring everything at distance *d* before touching anything at distance *d+1*. A queue's FIFO discipline delivers exactly that: nodes discovered earlier (nearer) are dequeued before nodes discovered later (further), so the frontier expands outward one whole layer at a time. A stack would do the opposite — the most recently discovered node is explored first, plunging down one branch before its siblings, which is depth-first, not layer-by-layer.

---

### Part B — Coding (62 points)

**B1 Array-Based (10 pts).** 3/4/3 for (a)/(b)/(c).
*(a) The end of the list must be the top — justified by A1(b). (b) must use `collections.deque` with `popleft()`. (c) is deliberately the slow version; it is only "wrong" as a queue, and must still be **correct** — verify FIFO order, not just that it is slow.*

**B2 Linked-Based (10 pts).** 5 each.
*(b) The tail pointer must serve **enqueue**, and dequeue must come from the head. The reverse (enqueue at head, dequeue at tail) is O(n) per dequeue on a singly linked list, because removing the tail requires walking the list to find the new second-to-last node — there is no back-pointer. Require this in the justification comment; it is the single most instructive design point in B2.*

**B3 Extended Operations (16 pts).** ~3 pts each.

```python
def reverse(self):                       # O(n) time, O(1) extra space
    prev, cur = None, self.head
    self.tail = self.head
    while cur:
        cur.next, prev, cur = prev, cur, cur.next   # re-point, then advance
    self.head = prev

def middle(self):                        # O(n), single pass
    slow = fast = self.head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow.data

def has_cycle(self):                     # Floyd — O(n) time, O(1) space
    slow = fast = self.head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast: return True     # identity, not equality
    return False
```

Verified: `middle` on `[1,2,3,4]` → **3** (the *second* middle, as the spec requires); on `[1,2]` → 2; on `[1,2,3,4,5]` → 3. `has_cycle` correct on acyclic, mid-list cycle, and single-node self-loop.

*Grading notes: (a) must be in-place — creating new nodes earns 1 of 3 — and must update **both** `head` and `tail`; forgetting `tail` is the most common defect and leaves the structure corrupt for later appends. (b) reject any two-pass `len()`-then-index solution, the spec forbids it explicitly. (c) `slow is fast` must use identity; `==` compares node **data** and gives false positives on lists with duplicate values — test with `[1,1,1]` acyclic, which must return `False`. (d) must be the O(n²) version per the spec, with the set-based alternative noted in a comment. (e) must build a new list by re-linking, not by round-tripping through Python lists.*

**B4 Empirical Comparison (12 pts).** 4/4/4. Measured reference (n enqueues then n dequeues):

| n | `deque` | raw list `pop(0)` | slowdown |
|---|---|---|---|
| 1,000 | 0.23 ms | 0.24 ms | 1.0× |
| 5,000 | 1.04 ms | 2.46 ms | 2.4× |
| 20,000 | 3.90 ms | 33.0 ms | 8.5× |
| 50,000 | 9.39 ms | 228 ms | **24.3×** |

The slowdown factor itself grows with n — the signature of Θ(n²) versus Θ(n). Stack timings should be broadly comparable between array and linked versions (both O(1) per op), with the array version usually modestly faster from cache locality and no per-node allocation.

*(c) A full-credit paragraph explains: the queue's problem is that a raw list forces removal from the **front**, and contiguous storage makes that O(n) — so the total becomes quadratic. A stack only ever touches **one end**, which is O(1) in both representations, so the choice is a constant-factor matter rather than a complexity-class matter. Award 2 of 4 if the student reports the numbers correctly but attributes the difference to "deque is optimised" without identifying front-removal/shifting as the mechanism.*

**B5 Expression Evaluation (14 pts).** 4/6/2/2. All verified:

| Expression | Result |
|---|---|
| `(3 + 4)` | `7.0` |
| `((3 + 4) * 2)` | `14.0` |
| `((10 - 4) / (1 + 2))` | `2.0` |
| `(0 - 5)` | `-5.0` |
| `((1.5 + 2.25) * 2)` | `7.5` |
| `(((2 + 3) * (4 - 1)) / 5)` | `3.0` |

```python
def tokenize(expression):
    toks, i = [], 0
    while i < len(expression):
        c = expression[i]
        if c.isspace(): i += 1
        elif c in "()+-*/": toks.append(c); i += 1
        else:                                        # multi-digit / decimal
            j = i
            while j < len(expression) and (expression[j].isdigit() or expression[j] == "."):
                j += 1
            toks.append(expression[i:j]); i = j
    return toks

def evaluate(expression):
    ops, vals = [], []
    for t in tokenize(expression):
        if   t == "(":       pass                    # documented choice: ignore
        elif t in "+-*/":    ops.append(t)
        elif t == ")":
            op, b, a = ops.pop(), vals.pop(), vals.pop()   # NOTE: b pops first
            if   op == "+": result = a + b
            elif op == "-": result = a - b
            elif op == "*": result = a * b
            else:
                if b == 0: raise ZeroDivisionError("division by zero in expression")
                result = a / b
            vals.append(result)
        else:                vals.append(float(t))
    return vals[-1]
```

> **Do not** compress the four cases into a dict literal such as
> `{"+": a+b, "-": a-b, "*": a*b, "/": a/b}[op]`. Python builds the whole dict
> before indexing it, so **every** branch is evaluated — including `a / b`.
> That makes `evaluate("(5 - 0)")` raise `ZeroDivisionError` even though no
> division was requested. If a student submits the dict form, this is a real
> latent bug: probe it with `(5 - 0)`.

*Critical grading point: **operand order**. The stack pops the right operand first, so it must be `b = pop(); a = pop()` and then `a − b`. Reversing this passes both commutative tests (`(3 + 4)` → 7.0 and `((3 + 4) * 2)` → 14.0 are **identical** either way) and silently fails on `−` and `/`: verified, `((10 - 4) / (1 + 2))` yields `-0.5` instead of `2.0`. A submission can therefore look correct on half the sample cases — always run a non-commutative test.*
*Note the tokenizer example `"(3 + 4) * 2"` in the prompt is **not** fully parenthesized. Tokenizing it is fine (that is all (a) asks), but feeding it to `evaluate` returns `7.0`, not 14.0 — the trailing `* 2` is never consumed because no `)` triggers it. This is correct behaviour for the stated algorithm, not a bug; mention it if a student reports it as one.*
*(c) Unary negation genuinely needs no new code — `(0 - 5)` is just binary subtraction. Award the 2 points for a student who verifies this and says so; a student who adds special-case unary handling has over-engineered but should not lose marks if it still works.*

---

### Part C — Challenge (ungraded)

- **C1 LRU Cache** — dict for O(1) lookup + doubly linked list for O(1) reordering; the dict maps key → node so a node can be unlinked without traversal. (`collections.OrderedDict` or Python 3.7+ `dict` ordering makes this much shorter, but the point is building it.)
- **C2 Min-Stack** — push the running minimum onto an auxiliary stack in lockstep, so `get_min` is a peek. Space is O(n); the optimisation of only pushing on new minima requires care on pop.
- **C3 Sliding Window Maximum** — a deque holding *indices* in decreasing-value order; pop from the back while the incoming value is larger, pop from the front once it falls outside the window. Each index enters and leaves at most once → O(n).

---

*CS 101 · Week 7 · Problem Set 7 · Due Friday Week 8 · © CSE Department*

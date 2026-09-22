# CS 102 · Computer Science II
## Lecture 12: Priority Queues, `heapq`, and What Heaps Are For

**Date:** Friday 12 February 2027 · 09:00–09:50 · Week 3

---

## 1. The ADT, Separately From the Heap

A **priority queue** is an abstract data type. It stores items with priorities and supports:

| operation | meaning |
| --- | --- |
| `insert(x, p)` | add item `x` with priority `p` |
| `find_min()` | return the item of smallest priority |
| `extract_min()` | remove and return it |
| `decrease_key(x, p)` | lower an item's priority |
| `merge(A, B)` | combine two queues |

**The ADT is not the heap.** A binary heap is one implementation, and comparing it to the obvious
alternatives shows what it is buying:

| implementation | insert | find-min | extract-min | decrease-key |
| --- | --- | --- | --- | --- |
| unsorted array | $O(1)$ | $\Theta(n)$ | $\Theta(n)$ | $O(1)$ |
| sorted array | $\Theta(n)$ | $O(1)$ | $O(1)$ | $\Theta(n)$ |
| balanced BST (Week 2) | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ |
| **binary heap** | $O(\log n)$ | $O(1)$ | $O(\log n)$ | $O(\log n)$ |
| Fibonacci heap | $O(1)$ | $O(1)$ | $O(\log n)^{*}$ | $O(1)^{*}$ |

<sub>* amortised</sub>

The two array rows show the trade at its starkest — each makes one operation free by making another
linear. **The binary heap's contribution is that no operation is linear**, at a cost of $O(1)$ space
per element and about twenty lines of code.

Against a balanced BST the heap wins `find_min` and, more importantly, wins the constants and the
memory everywhere — an array of keys against $n$ separately allocated three-field nodes. It loses
`search`, which a priority queue does not have.

> **Choose the ADT first, then the implementation.** Deciding you need "a heap" before deciding you
> need a priority queue is the wrong order, and it is how people end up using a heap for a problem
> that wanted a sorted list.

---

## 2. `heapq`

Python's standard library implements a binary min-heap over an ordinary list.

```python
import heapq

h = []
heapq.heappush(h, 5)          # O(log n)
heapq.heappush(h, 1)
smallest = h[0]               # O(1) - just index 0, no function call
x = heapq.heappop(h)          # O(log n)

heapq.heapify(a)              # O(n), in place - Lecture 11's build
heapq.heappushpop(h, x)       # push then pop, one sift
heapq.heapreplace(h, x)       # pop then push, one sift
heapq.merge(*iterables)       # lazy k-way merge of sorted inputs
heapq.nsmallest(k, it)        # bounded-heap top-k
```

The module docstring states the convention exactly:

> *Heaps are arrays for which `a[k] <= a[2*k+1]` and `a[k] <= a[2*k+2]` for all k, counting elements
> from 0.*

**Zero-indexed, and the raw list is the interface.** `h[0]` is the minimum, `len(h)` is the size, and
`heapq` provides functions rather than a class. That is unusual for a standard library and occasionally
inconvenient — nothing stops you corrupting the invariant — but it means a heap costs no more memory
than the list itself.

*(Verified on this machine: Python 3.14.2, `heapq` at `/usr/local/lib/python3.14/heapq.py`, with the
pure-Python implementations transparently replaced by the C extension `_heapq`.)*

### `heapq._siftup` is not sift-up

If you read the source, be warned about the naming.

```python
def _siftup(heap, pos):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    childpos = 2*pos + 1                       # leftmost child
    while childpos < endpos:                   # Bubble up the smaller child until hitting a leaf.
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos] < heap[rightpos]:
            childpos = rightpos
        heap[pos] = heap[childpos]             # move smaller child UP
        pos = childpos
        childpos = 2*pos + 1
    heap[pos] = newitem                        # newitem now sits at a leaf...
    _siftdown(heap, startpos, pos)             # ...and is sifted back up
```

**`heapq._siftup` is what this course calls `sift_down`**, named for the direction the *children*
move rather than the element. `_siftdown` is our `sift_up`. The names are inverted relative to CLRS
and to every lecture in this course.

More interesting is that the algorithm is genuinely different. Our `sift_down` compares the element
against the smaller child at each level and stops when it fits — **two comparisons per level**.
CPython's version does not compare against `newitem` at all on the way down. It bounces the smaller
child up unconditionally until it reaches a leaf — **one comparison per level** — and only then sifts
`newitem` back up from the leaf to its correct place.

The bet is that an element promoted from the bottom of a heap is usually large and will sink most of
the way back down, so the second pass is short. It pays:

| $n$, random | textbook sift-down | CPython bounce-to-leaf | saving |
| --- | --- | --- | --- |
| $1{,}000$ | 16,858 | 10,303 | **38.9%** |
| $10{,}000$ | 235,471 | 136,651 | **42.0%** |
| $100{,}000$ | 3,019,569 | 1,699,700 | **43.7%** |

*(Comparisons for a full build-then-drain, mean of 3 runs. Both variants verified to sort correctly.)*

**Forty per cent of the comparisons, for a rearrangement that changes no asymptotics.** This is the
kind of constant-factor work a standard library is expected to have done, and the kind you should not
attempt until you have measured. You are not examined on this variant; you are examined on knowing
that the textbook form is not the only form.

### Two things `heapq` will not do

**It is min-only.** For a max-heap the usual trick is to negate:

```python
h = [-x for x in xs]
heapq.heapify(h)
largest = -heapq.heappop(h)
```

*(Verified correct on integers.)* But negation is arithmetic, and **it fails for any key that is not
a number** — `-'apple'` raises `TypeError: bad operand type for unary -: 'str'`. For those, wrap the
key in a class with an inverted `__lt__`, or sort by a negated numeric field of a tuple.

**It has no `decrease_key`.** Which is section 3.

---

## 3. `decrease_key`, and Why It Is Awkward

Dijkstra's algorithm (Week 5) needs to *lower* the priority of an item already in the queue. The
operation is easy on paper — reduce the key, sift up — and the difficulty is entirely bookkeeping:
**you must find the item first, and finding an arbitrary item in a heap is $\Theta(n)$** (Lecture 10
§6). Doing an $O(\log n)$ sift after an $O(n)$ search is pointless.

There are two standard answers.

### Answer 1 — an index map

Maintain `pos: key -> index`, updated on every swap.

```python
def _swap(self, i, j):
    self.a[i], self.a[j] = self.a[j], self.a[i]
    self.pos[self.a[i][1]] = i
    self.pos[self.a[j][1]] = j        # every swap now costs two dict writes
```

Genuine $O(\log n)$ `decrease_key`, and the heap never holds stale entries. The cost is that **every
swap everywhere in the structure must maintain the map** — the invariant leaks into code that has
nothing to do with `decrease_key`, which is where the bugs live.

### Answer 2 — lazy deletion

Do not update anything. Push a second entry with the better priority and ignore the stale one when it
surfaces.

```python
def push(self, key, pri):
    if key in self.best and self.best[key] <= pri:
        return                                     # not an improvement
    self.best[key] = pri
    heapq.heappush(self.h, (pri, key))

def pop(self):
    while self.h:
        pri, key = heapq.heappop(self.h)
        if self.best.get(key) == pri:              # not stale
            del self.best[key]
            return key, pri
    raise IndexError("empty")
```

The heap may hold up to one entry per `decrease_key`, so it grows to $O(E)$ rather than $O(V)$ in
Dijkstra — $\log E = O(\log V)$ for any graph, so **the asymptotic bound is unchanged** and the
constant is small.

*(Verified: both implementations cross-checked against a brute-force reference over 300 randomised
trials of interleaved pushes with repeated keys, confirming identical output, correct final
priorities, and non-decreasing pop order. 0 failures.)*

**Answer 2 is what you should write.** It is shorter, it is local — the `pop` loop is the only place
that knows about staleness — and it is what almost every production Dijkstra does. Answer 1 is worth
implementing once, in PS 3 part D, so that the trade is yours rather than received.

> The general shape recurs: **when deleting from the middle is hard, mark instead of delete and clean
> up on the way past.** The same idea appears in garbage collectors, in log-structured storage, and in
> `SortedList`'s deletion path from Week 2.

---

## 4. Application: Top-$k$

"The 100 largest of ten million" is where heaps earn their place, and there are three approaches with
genuinely different complexities.

| strategy | time | space |
| --- | --- | --- |
| sort, take $k$ | $\Theta(n\log n)$ | $\Theta(n)$ |
| heapify, pop $k$ times | $\Theta(n + k\log n)$ | $\Theta(n)$ |
| **bounded heap of size $k$** | $\Theta(n\log k)$ | $\Theta(k)$ |

The third keeps a min-heap of the best $k$ seen so far; each new item is compared against the
smallest and replaces it or is discarded.

```python
def top_k(xs, k):
    h = []
    for x in xs:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:                 # O(1) test rejects almost everything
            heapq.heapreplace(h, x)    # one sift, not two
    return sorted(h, reverse=True)
```

Measured on $n = 1{,}000{,}000$ random floats:

| $k$ | sort | heapify + $k$ pops | bounded heap |
| --- | --- | --- | --- |
| 10 | 366.2 ms | 120.0 ms | **46.3 ms** |
| 1,000 | 346.1 ms | 113.5 ms | **51.5 ms** |
| 100,000 | 347.2 ms | 313.4 ms | **292.1 ms** |

*(All three verified to return identical results.)*

**At $k = 10$ the bounded heap is 7.9× faster than sorting; at $k = 100{,}000$ the advantage is
19%.** The $\log k$ in the bound is doing exactly what it says — when $k$ approaches $n$ the three
methods converge, and the specialised algorithm stops being worth its complexity.

Note also the space column, which the timings do not show: the bounded heap holds $k$ items. **It
works on a stream**, on data too large for memory, and on an input whose length you do not know. That
is usually the real reason to choose it.

This is what `heapq.nsmallest` and `nlargest` do internally, and it is why they take an iterable
rather than a sequence.

---

## 5. Application: Dijkstra's Algorithm

The priority queue is the engine of Dijkstra's shortest-path algorithm, which is Week 5's subject.
The shape of it, now, because it is the canonical use:

```python
def dijkstra(graph, source):
    dist = [INF] * len(graph); dist[source] = 0
    pq = [(0, source)]
    done = [False] * len(graph)
    while pq:
        d, u = heapq.heappop(pq)          # closest unfinalised vertex
        if done[u]:                       # stale entry - lazy deletion
            continue
        done[u] = True
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))    # "decrease_key"
    return dist
```

Every iteration asks *"which unfinalised vertex is nearest?"* — `extract_min`, $V$ times — and every
edge relaxation lowers a priority — $E$ of them. With a heap the total is
$O((V + E)\log V)$; with a linear scan for the minimum it is $\Theta(V^2 + E)$.

On random sparse graphs, this machine:

| $V$ | $E$ | binary heap | linear scan | speedup |
| --- | --- | --- | --- | --- |
| 1,000 | 5,000 | 3.2 ms | 49.5 ms | **15×** |
| 5,000 | 25,000 | 14.2 ms | 1,010.6 ms | **71×** |
| 20,000 | 100,000 | 113.6 ms | 16,175.2 ms | **142×** |

*(Both implementations verified to produce identical distance arrays at every size.)*

**The speedup grows with $V$**, which is what the difference between $V^2$ and $(V+E)\log V$ looks
like on a sparse graph. At $V = 20{,}000$ it is the difference between a tenth of a second and
sixteen seconds.

One caveat, so the table is not oversold: on a **dense** graph, $E \approx V^2$, and
$O((V+E)\log V) = O(V^2\log V)$ is *worse* than the array's $\Theta(V^2)$. The heap is the right
choice for sparse graphs, which is to say for almost every real one — road networks, social graphs,
and the internet all have $E = O(V)$ — but "use a heap for Dijkstra" is a statement about your graph,
not a law.

---

## 6. Application: Event-Driven Simulation and Scheduling

The other canonical use, and the one that explains the name.

A discrete-event simulation keeps a queue of pending events ordered by **time**, not by arrival. The
main loop is:

```python
while events:
    time, event = heapq.heappop(events)      # earliest pending event
    for new_time, new_event in handle(event, time):
        heapq.heappush(events, (new_time, new_event))
```

Processing an event can schedule further events at any future time, including times earlier than
events already queued. **A FIFO queue cannot express this and a sorted list costs $\Theta(n)$ per
insertion.** The priority queue is the data structure the problem is asking for.

The same structure is an OS scheduler — `(priority, task)`, pop the most urgent — and this is where
"priority queue" gets its name. Two practical notes that follow from the ADT rather than the heap:

- **Ties.** Python compares tuples element by element, so `(3, task_a)` and `(3, task_b)` fall through
  to comparing the tasks, which may raise `TypeError` for objects with no ordering. The standard fix
  is a monotonic counter: push `(priority, count, task)`. The counter is unique, so the third element
  is never reached — and because it increases, **equal priorities come out in insertion order**,
  making the queue stable for free.
- **Starvation.** A pure priority queue will never run a low-priority task if high-priority ones keep
  arriving. Real schedulers age priorities upward over time. That is a policy decision, not a data
  structure one, and it is worth noticing that the data structure will not warn you.

---

## 7. When the Heap Is the Wrong Answer

Week 2's lecture 09 ended by measuring a case where the sophisticated structure lost. The same
discipline applies here.

**Merging $k$ sorted lists.** `heapq.merge` is $O(N\log k)$ and streams lazily; concatenating and
calling `sorted()` is $O(N\log N)$ and materialises everything. The asymptotics favour `merge`
decisively. Measured on 100 lists of 10,000 items each:

| method | time |
| --- | --- |
| `heapq.merge(*lists)` | 580 ms |
| `sorted(itertools.chain(*lists))` | **238 ms** |

**The worse algorithm won by 2.4×.** The explanation is Timsort: it detects the 100 already-ascending
runs in the concatenated input and merges them in C, doing the same $O(N\log k)$ work as `heapq.merge`
but without executing Python bytecode per element.

The explanation is testable, so it was tested:

| `sorted()` input | time |
| --- | --- |
| the 100 sorted runs, concatenated | 282 ms |
| the identical data, shuffled | **625 ms** |
| (`heapq.merge` on the sorted lists, same run) | 659 ms |

Destroy the runs and `sorted()` slows by 2.2× to match `heapq.merge`, while `merge` itself is
unaffected. **The advantage was Timsort's run detection, exactly as claimed, and now it is verified
rather than asserted.**

So: use `heapq.merge` when the data does not fit in memory or you need results lazily — its $\Theta(k)$
space is the real argument. Use `sorted()` when it fits. **Neither the asymptotics nor the benchmark
alone would have told you that; you needed both, plus a hypothesis you could test.**

---

## 8. Where This Leaves Week 3

You have a structure that is a complete binary tree with no pointers, builds in $\Theta(n)$, and
answers "what is the smallest?" in $O(1)$. You have given up search entirely and paid for it in the
one column that a priority queue never reads.

**Week 4 changes subject to graphs**, and the connection is closer than it looks. A graph traversal is
a loop that repeatedly removes a vertex from a collection of pending vertices and adds its neighbours.
BFS uses a FIFO queue and DFS uses a stack; **Dijkstra uses the structure you built this week**, and
that single substitution is the difference between "fewest edges" and "least total weight."

Three data structures, one algorithm skeleton. That is the observation Week 4 opens with.

---

## 9. What to Do

- Read CLRS §6.5 (priority queues) and the `heapq` module documentation.
- **PS 3** is due Friday of Week 4. Part D implements both `decrease_key` strategies from §3.
- **Lab 3** compares heap sort and merge sort, including the locality effect from Lecture 11 §6.
- Week 4 begins graphs. Reread Lecture 10 §4 before then — **the adjacency list is another structure
  that replaces pointers with indices**, and the reasoning is the same.

---

*CS 102 · Week 3 · Lecture 12 · © CSE Department*

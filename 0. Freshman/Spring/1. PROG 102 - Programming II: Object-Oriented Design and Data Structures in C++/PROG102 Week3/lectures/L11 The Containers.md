# PROG 102 · Lecture 11
## The Containers

**Week 3 · Wednesday · 50 minutes**
**Reading:** *C++ Primer* Ch. 9, §11.1–11.3 · **Reference:** Stroustrup Ch. 31
**Assumes:** L10 (iterators and categories)

**Date:** Wednesday 10 February 2027 · 10:00–10:50 · Week 3

---

## 1. The Three Families

| Family | Members | Organising principle |
| --- | --- | --- |
| **Sequence** | `vector`, `deque`, `list`, `forward_list`, `array` | You control the order |
| **Associative** | `map`, `set`, `multimap`, `multiset` | Sorted by key |
| **Unordered associative** | `unordered_map`, `unordered_set`, … | Hashed by key |
| *Adaptors* | `stack`, `queue`, `priority_queue` | A restricted interface over another container |

---

## 2. `std::vector`

**The default. Use it unless you have a reason not to.**

A contiguous array that grows. It is `Stack<T>` from Week 2, done properly.

### 2.1 Growth

`push_back` is *amortised* $O(1)$: when the array is full, `vector` allocates a bigger one, moves
everything across, and frees the old. Measured on libstdc++:

```
  0 ->   1
  1 ->   2   (x2.0)
  2 ->   4   (x2.0)
  4 ->   8   (x2.0)
  ...
128 -> 256   (x2.0)
```

**A growth factor of exactly 2.** One million `push_back`s cause **21 capacity changes**, ending at
1,048,576 — that is $\log_2$ of a million, not a million.

*(The factor is implementation-defined. libstdc++ and libc++ use 2; MSVC uses 1.5. Any constant factor
> 1 gives amortised $O(1)$; the choice trades memory against reallocation count.)*

### 2.2 `reserve`

If you know the size in advance, say so:

```cpp
std::vector<int> v;
v.reserve(n);              // one allocation, no reallocation, no moves
for (int i = 0; i < n; ++i) v.push_back(i);
```

Measured:

| n | without `reserve` | with `reserve` | speedup |
| --- | --- | --- | --- |
| 100,000 | 0.88 ms | 0.19 ms | **4.59×** |
| 1,000,000 | 7.11 ms | 2.88 ms | **2.47×** |

**Free, one line, and it also stops iterators being invalidated** (§6). There is no reason not to when
you know the count.

### 2.3 `size()` vs `capacity()`

`size()` is how many elements exist; `capacity()` is how many fit before the next reallocation. Week
2's `Stack<T>` had exactly these two members for exactly this reason — you have already built this.

---

## 3. `std::list` and `std::deque`

**`std::list`** is a doubly linked list. $O(1)$ insertion and erasure *at a known position*, no random
access, and **every element is a separate allocation**.

**`std::deque`** is a double-ended queue: random access, $O(1)$ push at both ends, implemented as a
sequence of fixed-size blocks. It is not contiguous, so you cannot pass `&d[0]` to a C API.

### 3.1 Traversal, Measured

Summing 1,000,000 `int`s, 20 passes:

| Container | Time | Relative |
| --- | --- | --- |
| `vector` | 9.7 ms | 1.0× |
| `deque` | 10.6 ms | 1.1× |
| `list` | **61.2 ms** | **6.3×** |

**All three are $O(n)$.** The list is six times slower, and the complexity table cannot tell you that.

The reason is memory layout. A `vector`'s elements are adjacent, so one cache line fetch brings in 16
`int`s. A `list`'s nodes are separate allocations scattered across the heap, so each element costs a
potential cache miss — and a miss is roughly 200 cycles against 4 for an L1 hit. **Week 12 measures
this directly with `perf`.**

---

## 4. The Measurement That Contradicts the Table

Everyone learns that list insertion is $O(1)$ and vector insertion is $O(n)$. Here are both, measured.

### 4.1 Insert Keeping Sorted Order

Insert N random integers, each into its correct position:

| N | `vector` | `list` | ratio |
| --- | --- | --- | --- |
| 1,000 | 0.08 ms | 0.41 ms | 5.1× |
| 5,000 | 0.71 ms | 32.5 ms | 45.9× |
| 20,000 | 6.60 ms | 1,038 ms | 157× |
| 50,000 | 45.3 ms | 8,086 ms | **178×** |

**The vector wins, and the gap grows.** The list is doing $O(1)$ insertions and losing by two orders
of magnitude.

**Why:** to insert in order you must first *find* the position. In a `vector` that is
`std::lower_bound` — a binary search, $O(\log n)$, over contiguous memory. In a `list` it is a linear
walk, $O(n)$, chasing pointers through scattered heap.

The list's $O(1)$ insertion is real. **It is attached to an $O(n)$ cache-hostile search**, and the
search dominates.

### 4.2 Insert at a Position You Already Have

Now remove the search — 100,000 insertions at the front:

| Container | Time |
| --- | --- |
| `vector` | 446 ms |
| `list` | **3.5 ms** |

**The list wins by 128×.** Here the complexity table is exactly right: `vector::insert` at the front
moves every element, and `list::push_front` relinks two pointers.

### 4.3 The Actual Lesson

Both measurements are correct and they point opposite ways.

> **The complexity table describes the insertion. It says nothing about how you got the position.**

In real code you almost always had to search. That is why the practical advice is **use `vector` by
default** — including for workloads whose complexity table appears to favour a list.

Reach for `list` when you genuinely hold the position already: you are splicing, you are erasing during
a traversal you are already doing, or you need iterators that survive insertion (§6).

**This is the course thesis in container form.** The abstraction has a cost, the table quotes one cost,
and the machine charges you for another.

---

## 5. Associative Containers

### 5.1 `map` and `set` — Sorted

Balanced binary search trees (red-black in practice). $O(\log n)$ insert, find and erase, and
**iteration is in sorted key order**.

```cpp
std::map<std::string, int> counts;
counts["apple"] += 1;                     // inserts with value 0, then increments
for (const auto& [word, n] : counts) ...  // sorted by word
```

`map` requires `operator<` on the key — **which is why Lecture 04 §6.1 insisted your `operator<` be a
strict weak ordering.** A comparator that is not is undefined behaviour here, not merely a wrong order.

### 5.2 `unordered_map` and `unordered_set` — Hashed

Hash tables. **Average** $O(1)$ insert, find and erase; **worst case $O(n)$** if the hash function is
poor. Iteration order is unspecified.

### 5.3 Measured, 200,000 `int` Keys

| Operation | `map` | `unordered_map` | ratio |
| --- | --- | --- | --- |
| insert | 76.1 ms | 44.5 ms | 1.71× |
| **lookup** | 98.1 ms | **15.1 ms** | **6.50×** |

And the thing you pay for:

```
map           : 1 2 3 4 5
unordered_map : 3 2 4 1 5   <- no guarantee
```

> **Choose `unordered_map` unless you need ordering.** Lookup is six times faster. Choose `map` when
> you need sorted iteration, `lower_bound`/`upper_bound` range queries, or a key type that has `<` but
> no good hash.
>
> **`unordered_map` is not always the answer.** Its worst case is $O(n)$, it needs a hash for your key,
> and for small maps (a few dozen entries) a sorted `vector` often beats both.

### 5.4 Use the Member `find`

From L10 §5.1, now measured. Searching a 100,000-element `std::set`:

| | Time (2,000 lookups) |
| --- | --- |
| `std::find(s.begin(), s.end(), k)` | 2,119 ms |
| `s.find(k)` | **0.3 ms** |

**A factor of about 6,000.** `std::find` walks the range linearly — it has no way to know the container
is sorted. `s.find` descends the tree.

**When a container offers a member with an algorithm's name, use the member.**

---

## 6. Iterator Invalidation

Every container has rules about which operations invalidate existing iterators. Getting this wrong
produces a use-after-free that ASan reports and nothing else will.

```cpp
std::vector<int> v{1,2,3,4};
auto it = v.begin();
v.push_back(5);        // may reallocate
*it;                   // undefined behaviour
```

```
ERROR: AddressSanitizer: heap-use-after-free
READ of size 4 ... freed by thread T0 here
```

The `push_back` reallocated, freed the old array, and `it` still points into it.

Meanwhile:

```cpp
std::list<int> l{1,2,3,4};
auto it = l.begin();
l.push_back(5); l.push_front(0);
*it;                   // still 1 -- verified, still valid
```

### 6.1 The Rules Worth Memorising

| Container | Insertion invalidates | Erasure invalidates |
| --- | --- | --- |
| `vector` | **all**, if it reallocates; otherwise those after the point | those at or after the point |
| `deque` | **all** iterators (references survive for end insertions) | those at or after, generally all |
| `list`, `forward_list` | **none** | only the erased element |
| `map`, `set` | **none** | only the erased element |
| `unordered_*` | **all**, if it rehashes | only the erased element |

**Two practical consequences:**

- **Never hold a `vector` iterator across a `push_back`.** Use an index if you must hold something.
- **`reserve` up front** removes the reallocation and therefore the invalidation.

> **Node-based containers not invalidating is a real reason to choose them**, and it is a better reason
> than the $O(1)$ insertion that §4 showed you usually cannot cash in.

---

## 7. Container Adaptors

`stack`, `queue` and `priority_queue` are not containers. They are **wrappers that restrict an existing
container's interface**:

```cpp
std::stack<int> s;                                  // uses deque by default
std::stack<int, std::vector<int>> sv;               // ...or a vector
s.push(1); s.top(); s.pop();                        // and nothing else
```

**There is no `begin()`, no `end()`, no iteration.** That is the point: the adaptor exists to *remove*
operations, so that code using a stack cannot accidentally index into it.

`priority_queue` is a binary heap — `top()` is the largest element, `push` and `pop` are $O(\log n)$.
It is the structure CS 102 Week 3 asked you to build.

> **This is the Adapter pattern**, which you will meet by name in **Week 7**. The standard library used
> it before the Gang of Four wrote it down.

---

## 8. Choosing

A decision procedure that is right most of the time:

1. **`vector`.** Start here. Change only for a reason you can name.
2. Need lookup by key? **`unordered_map`** — unless you need sorted iteration or range queries, then
   **`map`**.
3. Need push and pop at *both* ends? **`deque`**.
4. Need iterators that survive insertion, or splicing, or you genuinely already hold the position?
   **`list`**.
5. Need a fixed size known at compile time? **`std::array`** — zero overhead over a C array (Week 2
   §L08 §5).
6. Want to forbid indexing? **an adaptor.**

**Then measure**, because §4 is what happens when you reason from the table alone.

---

## 9. Summary

| Idea | The point |
| --- | --- |
| `vector` is the default | Contiguous, cache-friendly, amortised $O(1)$ append |
| Growth factor 2 | 1M `push_back`s = **21** reallocations |
| `reserve` | 4.59× at 100k, 2.47× at 1M — and stops invalidation |
| Traversal | list is **6.3×** slower than vector at the same $O(n)$ |
| Sorted insertion | vector wins by **178×** — the search dominates |
| Known-position insertion | list wins by **128×** — the table was right here |
| `map` vs `unordered_map` | lookup **6.5×** faster unordered; ordering is what you pay for |
| Member `find` | **~6,000×** faster than `std::find` on a set |
| Invalidation | `vector` push_back → use-after-free, verified; `list` survives |
| Adaptors | Restrict an interface; no iteration by design |

---

## 10. Exercises

**1.** Reproduce the growth-factor table on your machine. **What factor does your standard library
use?** How many reallocations for one million `push_back`s?

**2.** Measure `reserve` at n = 10⁴, 10⁵, 10⁶. **Does the speedup grow or shrink with n?** Explain the
trend.

**3.** Reproduce §4.1 for at least four values of N and confirm the ratio grows. Then **change the
list version to insert at a known position** and reproduce §4.2. Report both.

**4.** Measure `map` against `unordered_map` for insert and lookup at 200,000 keys. Then repeat with
**`std::string` keys**. Does the ratio change? Why might it?

**5.** Write the `vector` invalidation bug and catch it with `-fsanitize=address`. Then add a
`reserve` large enough and show the bug disappears. **Is the code now correct?**

**6.** Time `std::find` against `s.find` on a `std::set` of 100,000 elements. Report the ratio.

**7.** You need a collection of 10,000 records, looked up by string ID, iterated in ID order once a
day, with occasional insertion. **Choose a container and defend it in three sentences.**

---

## 11. Next

**Lecture 12** covers the algorithms that operate on all of this — `sort`, `find`, `transform`,
`accumulate` — and ends with `std::vector<bool>`, the standard library's most instructive mistake.

---

*PROG 102 · Week 3 · Lecture 11 · © CSE Department*

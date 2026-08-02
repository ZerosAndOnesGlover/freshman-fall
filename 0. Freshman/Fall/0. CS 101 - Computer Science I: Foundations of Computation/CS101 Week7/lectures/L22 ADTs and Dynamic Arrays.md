# CS 101 · Lecture 22 (Week 7, Lecture 1)
## Abstract Data Types and Python Lists as Dynamic Arrays

**Week 7 · Wednesday**
*"An Abstract Data Type is a mathematical specification of a data structure — it defines what operations are possible and what they mean, without specifying how they are implemented." — CS 101*

---

## 0. The Second Half of the Course Begins

Weeks 0–6 built your foundation: computation, types, control flow, functions, recursion, algorithms, and the mathematics of complexity. Starting today, we build **data structures** — the organized ways of storing data that make efficient algorithms possible.

This is not a new subject bolted onto the first six weeks. It is the natural next question: now that you can analyze *how fast* an algorithm is, you need to understand *why* certain operations are fast or slow — and that always comes down to how data is organized in memory.

---

## 1. What Is an Abstract Data Type?

An **Abstract Data Type (ADT)** is a specification of:
1. **What data** the structure holds
2. **What operations** are available
3. **What each operation guarantees** (its behavior/contract) — without saying *how* it's implemented

The word "abstract" is key: an ADT separates **interface** from **implementation**. You can implement a Stack ADT using an array. You can also implement it using a linked list. Both satisfy the *same* specification — "push adds to the top, pop removes from the top, LIFO order" — but the internal memory layout is completely different.

**Why does this separation matter?**
- You can **change the implementation** without changing any code that uses the ADT (as long as the interface stays the same)
- You can **reason about correctness** using only the specification, without worrying about implementation details
- You can **choose the implementation** that best fits your performance requirements

This is one of the most powerful ideas in computer science — and it's the organizing principle for the next three weeks.

### Example: The Stack ADT (Preview — full treatment on Friday)

**Specification:**
- `push(x)`: add x to the top
- `pop()`: remove and return the top element
- `peek()`: return (without removing) the top element
- `is_empty()`: return True if the stack has no elements
- **Invariant:** Last In, First Out (LIFO)

This says nothing about arrays, linked lists, or memory. It's a pure mathematical contract.

---

## 2. Python Lists — What They Actually Are

You've used Python lists constantly since Week 1. Today we open the hood.

**A Python list is NOT a generic "array" in the C sense.** It is a **dynamic array** — a resizable array of *pointers* to objects, with automatic growth management.

```
Python list [10, "hello", 3.14, [1,2,3]]:

┌─────────────────────────────────────┐
│  Header: size=4, capacity=8          │
├───────┬───────┬───────┬───────┬──────┤
│  ptr  │  ptr  │  ptr  │  ptr  │ (unused
│   ↓   │   ↓   │   ↓   │   ↓   │  capacity)
└───────┴───────┴───────┴───────┴──────┘
    ↓       ↓       ↓       ↓
   10   "hello"   3.14   [1,2,3]
  (int)  (str)   (float)  (list)
```

Each slot in the underlying array holds a **reference** (pointer) to an object elsewhere in memory — not the object's data directly. This is why a Python list can hold mixed types: `[1, "two", 3.0]` is perfectly valid, because every slot is just a pointer, regardless of what it points to.

### Why "Dynamic"?

The underlying array has a fixed **capacity** at any given moment, but Python automatically **resizes** it when needed:

```python
import sys

lst = []
prev_size = sys.getsizeof(lst)
for i in range(20):
    lst.append(i)
    size = sys.getsizeof(lst)
    if size != prev_size:
        print(f"After {i+1} appends: capacity changed. New size: {size} bytes")
        prev_size = size
```

Running this reveals that Python doesn't resize on *every* append — it **over-allocates**, growing the capacity in chunks (roughly by a factor, not by exactly 1 each time). This is the same "doubling strategy" you implemented in PS6's `DynamicArray` and analyzed with amortized analysis.

---

## 3. The Complexity of Every List Operation

This table is the single most important reference in this course going forward. Memorize it.

| Operation | Complexity | Why |
|-----------|-----------|-----|
| `lst[i]` (index access) | O(1) | Direct pointer arithmetic: `base_address + i * pointer_size` |
| `lst[i] = x` (index assignment) | O(1) | Same — direct memory write |
| `len(lst)` | O(1) | Python stores the size as metadata; no counting needed |
| `lst.append(x)` | O(1) amortized | Usually just writes to unused capacity; occasional O(n) resize |
| `lst.pop()` (remove last) | O(1) | No shifting needed — just decrement size |
| `lst.pop(0)` (remove first) | O(n) | **Must shift every remaining element left by one position** |
| `lst.insert(0, x)` (insert at front) | O(n) | **Must shift every existing element right by one position** |
| `x in lst` (membership test) | O(n) | Must scan linearly — no shortcuts without additional structure |
| `lst.index(x)` | O(n) | Same reasoning as membership test |
| `lst[i:j]` (slicing) | O(j-i) | Must copy each element in the range to a new list |
| `lst1 + lst2` (concatenation) | O(len(lst1) + len(lst2)) | Must copy every element of both lists |
| `lst.sort()` | O(n log n) | Timsort (Week 5) |
| `lst.reverse()` | O(n) | Must touch every element |

**The critical asymmetry:** operations at the **end** of a list (`append`, `pop()`) are O(1) amortized. Operations at the **beginning** (`insert(0, x)`, `pop(0)`) are O(n). This is not an accident — it follows directly from how the array is laid out in contiguous memory.

```python
# Demonstrating the asymmetry:
import time

lst = list(range(100_000))

t0 = time.perf_counter()
lst.append(1)          # O(1) amortized
t1 = time.perf_counter()

t2 = time.perf_counter()
lst.insert(0, 1)        # O(n) — must shift 100,000 elements!
t3 = time.perf_counter()

print(f"append: {(t1-t0)*1e6:.2f} μs")
print(f"insert(0,x): {(t3-t2)*1e6:.2f} μs")
# insert(0,x) will be orders of magnitude slower
```

---

## 4. Why Index Access Is O(1) — The Memory Model in Detail

Understanding *why* `lst[i]` is O(1) requires understanding contiguous memory layout.

The underlying C array backing a Python list stores pointers at **consecutive memory addresses**. If the array starts at memory address `A`, and each pointer takes `P` bytes (typically 8 bytes on a 64-bit system), then the pointer for index `i` is located at address:

```
address(lst[i]) = A + i * P
```

This is **one multiplication and one addition** — regardless of how large `i` is or how large the list is. This is precisely why it's O(1): the cost doesn't grow with `n`.

Compare this to a **linked list** (Thursday's topic): to reach the i-th element, you must follow `i` pointers one at a time, starting from the head — there is no way to "jump" directly to an arbitrary position. That's O(n).

This single fact — contiguous memory enables O(1) random access, but makes front-insertion expensive — is the central tradeoff that defines the entire landscape of linear data structures. Every choice you make between array-based and linked structures comes back to this.

---

## 5. Why `insert(0, x)` and `pop(0)` Are O(n) — Precisely

```python
lst = [10, 20, 30, 40, 50]
lst.insert(0, 99)
# Before: [10, 20, 30, 40, 50]
# After:  [99, 10, 20, 30, 40, 50]
```

To make room for `99` at index 0, Python must:
1. Shift `50` from index 4 to index 5
2. Shift `40` from index 3 to index 4
3. Shift `30` from index 2 to index 3
4. Shift `20` from index 1 to index 2
5. Shift `10` from index 0 to index 1
6. Write `99` to index 0

That's **n shifts** for a list of n elements — O(n). The same logic in reverse applies to `pop(0)`: removing the first element requires shifting everything else left by one position.

**This is why, if your algorithm frequently adds/removes from the front of a collection, a plain Python list is the wrong data structure.** We'll introduce `collections.deque` on Friday — specifically designed to make front operations O(1).

---

## 6. The `list` vs. Array — A Terminology Note

In many other languages (C, Java), an "array" is a **fixed-size**, contiguous block of memory holding elements of the **same type**, stored directly (not as pointers).

```c
// C array — elements stored directly, contiguously, fixed size:
int arr[5] = {10, 20, 30, 40, 50};
// Memory: [10][20][30][40][50] — each int takes exactly 4 bytes, directly stored
```

Python's `list` is different in two ways:
1. **Dynamic size** — it grows and shrinks automatically
2. **Heterogeneous, pointer-based storage** — each slot holds a pointer to a Python object, not the raw value

This flexibility costs performance (extra indirection, larger memory footprint) but gains tremendous convenience (mixed types, automatic resizing). We'll see in PROG 101 (C) and CS 201 (Computer Architecture) exactly how "real" arrays work at the hardware level, and why the tradeoff Python makes is deliberate.

---

## 7. Tuples — The Immutable Sibling

```python
t = (1, 2, 3)
```

A **tuple** is like a list, but **immutable** — once created, it cannot be changed. This has consequences:

| Property | list | tuple |
|----------|------|-------|
| Mutable? | Yes | No |
| Can append/remove? | Yes | No |
| Can be a dict key? | No | Yes (if all elements are hashable) |
| Memory overhead | Higher (must support resizing) | Lower (fixed size, no growth machinery) |
| Typical use | Homogeneous, changing collections | Fixed-size records, function returns |

```python
# Tuples are perfect for representing fixed structure:
point = (3, 4)              # (x, y) — always exactly 2 elements
rgb = (255, 128, 0)          # (r, g, b) — always exactly 3

# Tuples can be dict keys (lists cannot):
distances = {(0,0): 0, (1,1): 1.41}
# {[0,0]: 0}  # TypeError! Lists are unhashable (mutable)
```

**Why can't lists be dictionary keys?** Because dictionary keys must be **hashable** — their hash value must never change during their lifetime (Week 8 will cover hashing in depth). Since lists are mutable, their contents (and thus their "identity" for hashing purposes) could change after being used as a key, which would break the hash table's internal consistency. Tuples, being immutable, don't have this problem.

---

## 8. Choosing Between List Operations — A Decision Framework

```
Do you need to add/remove from the END frequently?
    → list.append() / list.pop() — both O(1) amortized. Use plain list.

Do you need to add/remove from the FRONT frequently?
    → Plain list is O(n) for both. Use collections.deque instead (Friday's lecture).

Do you need fast random access by index?
    → list is O(1). This is a list's core strength.

Do you need fast membership testing (`x in collection`)?
    → list is O(n). Consider a set or dict instead (Week 8) for O(1) average case.

Do you need an immutable, hashable sequence?
    → Use a tuple.
```

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Abstract Data Type | Specification of behavior, independent of implementation |
| Python list | A dynamic array of pointers — not a "raw" array |
| Index access O(1) | Direct address computation: `base + i * pointer_size` |
| `append`/`pop()` O(1) amortized | End operations avoid shifting |
| `insert(0,x)`/`pop(0)` O(n) | Front operations require shifting every other element |
| Tuple | Immutable sibling of list; hashable; used for fixed-structure records |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Run this and explain the pattern in the output.

```python
import sys
xs = []
prev = sys.getsizeof(xs)
for i in range(120):
    xs.append(i)
    size = sys.getsizeof(xs)
    if size != prev:
        print(len(xs), size)
        prev = size
```

**2. (Explain.)** Explain from the memory model in §4 why `xs[i]` is Θ(1) for any `i`, while `xs.insert(0, v)` is Θ(n). Then predict roughly how much slower `insert(0, v)` is than `append(v)` on a 100,000-element list, and check by timing.

**3. (Build.)** Give the complexity of each operation and rewrite the function to be Θ(n).

```python
def reverse_into(xs):
    out = []
    for x in xs:
        out.insert(0, x)
    return out
```

**4. (Stretch.)** Lists and tuples both store references contiguously. Give three concrete consequences of the difference in mutability, at least one of which is about performance rather than semantics.


### Answers

**1.** The resizes happen at lengths **1, 5, 9, 17, 25, 33, 41, 53, 65, 77, 93, 109, …** — the underlying capacity growing 4, 8, 16, 24, 32, 40, 52, 64, 76, 92, 108.

Two observations. First, **reallocation is rare and gets rarer**: the gaps between resizes widen as the list grows. That is what makes `append` O(1) amortised — the expensive copy is spread over an increasing number of cheap appends.

Second, CPython does **not** double. The growth rule is roughly `new = old + old//8 + constant`, a factor of about 1.125 plus a floor. Any factor greater than 1 gives the O(1) amortised bound; a smaller factor means more frequent copying (a larger constant) but far less wasted memory. Doubling can leave nearly 50% of the allocation unused, which for a process holding thousands of lists is a real cost.

Note `sys.getsizeof([])` is 56 bytes on a 64-bit build — the list *object header* — and each slot adds 8 bytes for a pointer. The list stores **references**, never the objects themselves, which is why a list of a million integers occupies 8 MB of pointers plus whatever the integers cost separately.

**2.** **`xs[i]` is Θ(1)** because a list is a contiguous block of equally sized pointer slots. The address of slot `i` is `base + i * 8`, one multiply and one add, regardless of `i` or of the list's length. Nothing is traversed. This is *random access*, and it is the defining property of an array.

**`insert(0, v)` is Θ(n)** because inserting at the front requires every existing element to move one slot right to make room. There is no way around it: the elements must remain contiguous, so `n` pointer copies happen (as a single `memmove`, but still linear).

**Prediction:** `append` is O(1) amortised, `insert(0, …)` copies 100,000 pointers, so expect a difference of *roughly three orders of magnitude* — the ratio should scale with the list length rather than being a fixed factor.

```python
import timeit
timeit.timeit('a.insert(0,1)', setup='a=list(range(100000))', number=20000)
timeit.timeit('a.append(1)',   setup='a=list(range(100000))', number=20000)
```

On a typical machine this shows `insert(0, …)` well over 1000× slower. Repeat with a 10,000-element list and the ratio drops by roughly 10× — confirming the cost is linear in length, not a constant penalty. That scaling check is the part worth doing: a fixed ratio would mean you had measured overhead, not complexity.

**3.** `insert(0, x)` is Θ(len(out)) and it runs n times, so the total is 0 + 1 + … + (n−1) = **Θ(n²)**.

Three Θ(n) rewrites, in increasing order of preference:

```python
def reverse_into(xs):          # append then reverse
    out = []
    for x in xs:
        out.append(x)
    out.reverse()
    return out

def reverse_into(xs):          # slice
    return xs[::-1]

def reverse_into(xs):          # explicit and general
    return list(reversed(xs))
```

All three are Θ(n) because `append` is amortised O(1) and `reverse` is a single linear pass of swaps.

The pattern to internalise: **an O(n) operation inside a loop over n elements is O(n²)**, and front insertion is the most common instance. Whenever you find yourself building a list by repeatedly inserting at position 0, either append and reverse once at the end, or reach for `collections.deque`, whose `appendleft` genuinely is O(1) because it is not backed by a contiguous array. L24 covers that structure.

**4.** **1. Hashability (semantics).** A tuple of hashable elements is hashable and can be a dict key or set member; a list cannot. This is not an arbitrary restriction — a hash table locates entries by hash, so a key whose hash could change after insertion would become unfindable. Immutability is the precondition for hashability, which L25 §6 develops.

**2. Safe sharing (semantics).** A tuple can be a default argument, a module-level constant, or shared between threads without defensive copying, because no caller can alter it. The mutable-default bug of L11 simply cannot occur with a tuple default.

**3. Size and allocation (performance).** A tuple is allocated at exactly its final size, with no growth slack — `sys.getsizeof((1,2,3))` is smaller than `sys.getsizeof([1,2,3])`, because the list carries spare capacity plus a separate pointer to its element array. Tuples are also *constructed* faster: a constant tuple is built once at compile time and stored in the code object, so `for x in (1,2,3)` allocates nothing per iteration while `for x in [1,2,3]` rebuilds the list each time. CPython additionally keeps free lists of small tuples for reuse.

What is **not** a difference: element access. `t[i]` and `xs[i]` are both Θ(1) and equally fast — both are contiguous pointer arrays. Immutability buys the three properties above, not faster indexing.



---

## Reading

- **Guttag, Ch. 5.1–5.2** — Lists and mutability
- **Python docs — Time Complexity:** https://wiki.python.org/moin/TimeComplexity (bookmark this — you will reference it for the rest of your CS career)

---

*CS 101 · Week 7 · Lecture 22 (Wed) · © CSE Department*

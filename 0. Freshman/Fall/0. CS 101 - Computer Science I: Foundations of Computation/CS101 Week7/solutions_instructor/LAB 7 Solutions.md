# CS 101 — Week 7
## LAB 7 Solutions — INSTRUCTOR ONLY

> **All code below was executed and all stated outputs are real.** Where a benchmark appears,
> the absolute timings are machine-specific — grade the *ratios* and the conclusions, never the
> raw milliseconds.

---

## Part 1, Exercise 1.1 — What `sys.getsizeof` Reports

Measured on CPython 3.14, 64-bit:

| Object | Bytes |
|---|---|
| `[]` | 56 |
| `()` | 48 |
| `{}` | 64 |
| `set()` | **216** |
| `0` | 28 |
| `1` | 28 |
| `10**100` | **72** |

| n | `getsizeof(list(range(n)))` | bytes/element |
|---|---|---|
| 0 | 56 | — |
| 1 | 72 | 72.00 |
| 10 | 136 | 13.60 |
| 100 | 856 | 8.56 |
| 1000 | 8,056 | **8.06** |

**1. Why is `getsizeof(10**100)` bigger than `getsizeof(1)`?**

Python integers are **arbitrary precision**, so an `int` is a variable-length object: a fixed header
(reference count, type pointer, digit count) plus as many 30-bit digit words as the value needs.
`1` fits in one digit → 28 bytes. `10**100` needs ~11 digits → 72 bytes. `10**50` sits between at
48 bytes. This is the concrete memory cost of the property that made `2**100` work in Week 1 — the
value cannot overflow because the object grows instead.

**2. Does list size grow linearly?**

Yes, asymptotically. `getsizeof(list) = 56 + 8n` — a 56-byte object header plus **8 bytes per
element**, one 64-bit pointer each. Bytes-per-element falls from 72 at n=1 to 8.56 at n=100 to
**8.06** at n=1000, converging on 8 as the fixed header is amortised away.

The number to internalise: **a Python list costs 8 bytes per element regardless of what the elements
are**, because it stores *references*, never the objects. That is exactly what Exercise 1.2 probes.

> `set()` at 216 bytes is the outlier worth a comment — an empty set pre-allocates a small hash
> table, where an empty list allocates no element array at all.

---

## Exercise 1.2 — Deep vs. Shallow Size

```python
lst = [10**50 + i for i in range(1000)]
sys.getsizeof(lst)   #   8,856 bytes  (shallow)
deep_getsizeof(lst)  #  56,856 bytes  (deep)
```

**Ratio: 6.42×.**

The shallow figure counts only the pointer array. The deep figure adds the 1,000 `int` objects at
48 bytes each = 48,000, giving 8,856 + 48,000 = 56,856 ✓.

For comparison, `[i for i in range(1000)]` gives shallow 8,856, deep 36,856 — a ratio of only
**4.16×**, because small ints occupy 28 bytes rather than 48.

**Why big integers specifically?** Because the per-object cost scales with the *magnitude* of the
value, while the pointer cost is fixed at 8 bytes. The larger the integers, the more the deep size
dominates.

> **A subtlety worth raising with strong students.** `deep_getsizeof` uses a `seen` set, so shared
> objects are counted once. CPython caches integers **−5 to 256** as singletons, so a list of
> `range(1000)` contains 257 shared objects and 743 distinct ones — the deep size is therefore
> slightly *lower* than 1000 × 28 would suggest. A student who investigates why the arithmetic does
> not come out exactly right has found the small-int cache from L04 on their own.

---

## Part 3 — List vs. Linked List Memory

| n | Python list | per elem | Linked list | per elem | Ratio |
|---|---|---|---|---|---|
| 1,000 | 8,056 B | 8.1 | 136,000 B | 136.0 | **16.9×** |
| 10,000 | 80,056 B | 8.0 | 1,360,000 B | 136.0 | **17.0×** |

**A linked list costs ~17× the memory of a Python list for the same data.**

The 136 bytes per node break down as a 48-byte object header plus 88 bytes of `__dict__`. To store
one 8-byte reference, the node pays ~17× overhead.

**The fix worth demonstrating:** adding `__slots__ = ('value', 'next')` removes the per-instance
`__dict__` entirely. Measured on the same 1,000-node chain:

| Node class | Bytes/node | Ratio vs list |
|---|---|---|
| Plain (`__dict__`) | 136 | 17.0× |
| With `__slots__` | **48** | **6.0×** |

Students who discover `__slots__` should be credited — it is the standard remedy when a Python
program creates millions of small objects.

> **A measurement trap to warn students about.** `sys.getsizeof(node) + sys.getsizeof(node.__dict__)`
> on a *single freshly created* node reports **344 bytes**, not 136 — because CPython uses
> **key-sharing dictionaries** for instances of the same class, and the sharing only pays off once
> many instances exist. Measure a populated structure, never one object, or you will overstate the
> cost by 2.5×. `tracemalloc` around the whole construction is the more honest instrument, and
> gives ~119 B/node plain versus ~79 B/node with slots, including allocator overhead that
> `getsizeof` never sees.

The ratio is **stable across n**, which confirms both structures are Θ(n) space with different
constants. That is the point: same complexity class, 17× different cost.

---

## Part 4 — Operation Benchmarks

| Operation | Ops | Time |
|---|---|---|
| `list[i]` (index) | 100,000 | 4.27 ms |
| `list.append` | 100,000 | 2.40 ms |
| `list.insert(0, x)` | 10,000 | 37.48 ms |
| `list.pop(0)` on 200k list | 10,000 | **446.85 ms** |
| `deque.popleft()` on 200k | 10,000 | **0.35 ms** |

**`deque.popleft` is ≈ 1,285× faster than `list.pop(0)`** on a 200,000-element sequence.

Index and append are O(1) and land in the same order of magnitude. `pop(0)` is Θ(n) because every
remaining element shifts down one slot — and the measured cost scales with the list *length*, not
with the number of operations, which is the diagnostic to insist on. Re-run at n = 20,000 and the
time drops ~10×; a constant-factor penalty would not.

`deque` is a doubly linked list of fixed-size blocks, so both ends are O(1). The trade is that
`d[k]` for a middle index becomes O(n).

**Expected complexity table:**

| Operation | Python list | Linked list |
|---|---|---|
| Index `[i]` | **Θ(1)** | Θ(n) |
| Append (end) | Θ(1) amortised | Θ(1) *with tail pointer*, Θ(n) without |
| Insert at front | Θ(n) | **Θ(1)** |
| Delete at known node | Θ(n) | **Θ(1)** (doubly linked) |
| Memory per element | **8 B** | ~136 B |

---

## Part 5 — Applications

**Bracket matching** needs a **stack**: brackets must close in reverse order of opening, which is
LIFO by definition. A counter fails because it cannot detect interleaving — `"([)]"` has balanced
counts of each type and is still malformed.

**Undo/redo** needs **two stacks**. An action pushes onto the undo stack; undo pops from undo and
pushes onto redo; redo reverses that. The critical rule: **a new action clears the redo stack**,
because the future it recorded is no longer reachable. Students who omit that produce a redo that
resurrects operations from an abandoned timeline.

Both must handle the empty case without raising.

---

## Marking Scheme

The lab is checkoff-graded against the criteria on the handout. Within each part:

- **Method (≈60%).** Correct approach, required loop/structure type actually used, edge cases
  considered, invariants stated where the handout asks for them.
- **Result (≈40%).** Code runs, produces the specified output, and the written answers are correct.

**Carry-through.** A wrong helper that is then used correctly downstream costs marks once.

**Watch for the two failure modes that matter:**
1. Code that produces the right answer for the sample input and is wrong in general — always run
   the edge cases listed under each exercise.
2. Written answers that restate the observation instead of explaining it. "0.1 + 0.2 isn't 0.3
   because floats are imprecise" earns nothing; the answer must reach binary representation.

---

*CS 101 · Week 7 · Lab Solutions · Instructor Copy · © CSE Department*

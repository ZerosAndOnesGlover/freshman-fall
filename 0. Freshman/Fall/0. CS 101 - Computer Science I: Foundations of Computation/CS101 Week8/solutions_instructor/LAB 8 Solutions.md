# CS 101 — Week 8
## LAB 8 Solutions — INSTRUCTOR ONLY

> **All code below was executed and all stated outputs are real.** Where a benchmark appears,
> the absolute timings are machine-specific — grade the *ratios* and the conclusions, never the
> raw milliseconds.

---

## Part 1 — Both Hash Table Variants

Requirements to check: a real hash function (not `hash()` alone — the point is to build one),
resize on load factor, and instrumentation counters (`total_comparisons`, `total_probes`) that the
later parts depend on.

**The inner loop of `put` must scan for an existing key before appending**, or duplicate keys
accumulate and `get` returns the stale first one.

---

## Part 2 — Load Factor vs. Performance

Table size 1,000; keys `key0 … keyN`; auto-resize disabled.

| Load factor | Chaining: avg comparisons | Max chain | Open addressing: avg probes | Theory ½(1 + 1/(1−α)) |
|---|---|---|---|---|
| 0.25 | 1.000 | 1 | 1.000 | 1.167 |
| 0.50 | 1.080 | 2 | **4.780** | 1.500 |
| 0.75 | 1.216 | 3 | **48.107** | 2.500 |
| 0.90 | 1.201 | 3 | **64.367** | 5.500 |
| 1.00 | 1.198 | 3 | n/a | — |
| 2.00 | 1.670 | 4 | n/a | — |
| 4.00 | 2.697 | 7 | n/a | — |
| 8.00 | 4.547 | 11 | n/a | — |

### Chaining behaves exactly as predicted

Average comparisons grow roughly as **1 + α/2**, degrading *gracefully*, and α > 1 is perfectly
legal — at α = 8 a lookup still costs only ~4.5 comparisons. Max chain length grows like
Θ(log n / log log n), reaching 11 at α = 8. This is why chaining is the forgiving choice.

### Open addressing appears to be catastrophically broken — and the reason is the lesson

At α = 0.75 the theory predicts 2.5 probes and the measurement gives **48.1** — a 21× blowup. The
table is *not* full, so this is not the α → 1 collapse.

**The cause is primary clustering driven by a hash that preserves key locality.** Print the buckets:

```
djb2("key0".."key11") % 1000  ->  [894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 847, 848]
```

Sequential keys land in **consecutive buckets**. Since djb2 computes `h*33 + ord(c)`, two keys
differing only in the final character produce hashes differing by 1. Linear probing then walks
straight into the neighbouring occupied slots, runs merge, and probe sequences grow without bound.

**The fix is a finalising avalanche mix**, not a different probing scheme:

```python
def mixed(s):
    h = djb2(s)
    h ^= (h >> 16)
    h = (h * 0x45d9f3b) & 0xFFFFFFFF
    h ^= (h >> 16)
    return h
```

Re-measured with the same table, same keys, same probing:

| Load factor | djb2 (raw) | djb2 + avalanche | Theory |
|---|---|---|---|
| 0.25 | 1.000 | **1.156** | 1.167 |
| 0.50 | 4.780 | **1.444** | 1.500 |
| 0.75 | 48.107 | **2.273** | 2.500 |
| 0.90 | 64.367 | **5.044** | 5.500 |

With the mix, measurement tracks theory to within 10% at every load factor.

> **This is the single most valuable result in the lab.** The theoretical formula
> ½(1 + 1/(1−α)) assumes **uniform hashing**; a hash that clusters violates the assumption, and the
> formula's prediction becomes meaningless while the *chaining* formula stays accurate. Chaining
> only cares how many keys share a bucket; open addressing also cares **where the buckets are**.
>
> This is exactly the bug Java's `HashMap` shipped with, and why it now applies
> `h ^= (h >>> 16)` before masking. Students who diagnose the clustering themselves — by printing
> the bucket indices — have done real performance engineering. Those who conclude "open addressing
> is bad" have drawn the wrong lesson and should be sent back to the hash function.

**Expected answer to "which is better?":** neither, unconditionally. Chaining tolerates a mediocre
hash and high load. Open addressing is faster below α ≈ 0.7 *given a well-mixed hash*, because
contiguous probes are cache-friendly where chain-walking is pointer chasing.

---

## Part 3 — Amortised O(1) Insertion

Insert n keys into a table that doubles at α = 0.75 and plot cumulative work.

**Expected shape:** a staircase. Individual insertions are O(1) except at resize points, where the
cost spikes to Θ(n) as every key is rehashed. The spikes occur at geometrically spaced sizes, so
their *total* is bounded: rehashing at capacities 1, 2, 4, … sums to < 2n across n insertions.
Total work is O(n), hence **O(1) amortised**.

The verification students should produce is that **cumulative time is linear in n** even though
individual times are not. Plot cumulative work against n and look for a straight line; plot
per-operation time and look for the spikes. Both plots are needed — either alone tells half the
story.

**Amortised is not average.** It is a worst-case guarantee over any sequence of n operations, with
no probability involved. A single insertion can still cost Θ(n), which is why hash tables are a
poor fit for hard real-time systems.

---

## Part 4 — Dict vs. List Membership

| n | `x in list` | `x in set` | Ratio |
|---|---|---|---|
| 1,000 | 12.586 ms | 0.0348 ms | **362×** |
| 100,000 | 1,393.126 ms | 0.0385 ms | **36,166×** |

(1,000 lookups each, worst-case element.)

**The set time barely moves** — 0.0348 → 0.0385 ms for a 100× larger collection — confirming Θ(1).
The list time scales by ~111×, confirming Θ(n). The ratio grows *linearly with n*, which is the
signature of comparing an O(n) operation against an O(1) one.

This is the largest single speedup available in the course: converting a list to a set before a
membership-heavy loop turns Θ(n·m) into Θ(n + m).

**When the list is still right:** unhashable elements; order or duplicates matter; the collection is
tiny and checked once (building the set costs Θ(n) and allocates); or you need indexing.

---

## Part 5 — The Three Patterns

- **Counting** — `Counter(items)` or `d[k] = d.get(k, 0) + 1`. Θ(n).
- **Grouping** — `defaultdict(list)`, appending each item under its computed key. The anagram
  problem uses `"".join(sorted(word))` as the key. Θ(n · k log k).
- **Two-sum** — one pass, storing each value's index and looking up the complement **before**
  inserting the current element, so an element cannot pair with itself. Θ(n).

---

## Part 6 — The `__hash__`/`__eq__` Contract

**Defining `__eq__` alone makes the class unhashable:**

```
TypeError: cannot use 'P' as a set element (unhashable type: 'P')
```

Python sets `__hash__ = None` when you define `__eq__`, deliberately. The default hash is
identity-based, so two objects that are now `==` would hash differently, land in different buckets,
and become unfindable. Python fails loudly rather than let you build a silently broken set.

**Adding a consistent `__hash__` fixes it:**

```python
def __hash__(self):
    return hash(self.x)      # hash exactly the fields __eq__ compares
```

`Q(1) in {Q(1)}` → `True`. ✓

**The mutation hazard — demonstrate this one live:**

```python
q = Q(1)
s = {q}
q.x = 99
q in s      # False
len(s)      # 1
```

**The object is still in the set and can no longer be found — not even by itself.** It was filed
under `hash(1)` and now reports `hash(99)`, so the lookup probes the wrong bucket. The set is not
corrupt; it is doing exactly what it was told.

The rule: **anything used as a dict key or set member must be immutable in the fields its hash
depends on.** The robust fix is to make the class immutable outright:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float
```

`frozen=True` generates `__eq__` and `__hash__` together *and* blocks attribute assignment, so the
hazard is eliminated rather than merely documented. This is the right default for value objects.

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

*CS 101 · Week 8 · Lab Solutions · Instructor Copy · © CSE Department*

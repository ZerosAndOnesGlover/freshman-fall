# CS 101 · Lab 8
## Building a Hash Table From Scratch

**Date:** Tuesday 24 November 2026 · 15:00–16:50 · Lab Section (Week 9) — covers Week 8 (L25–L27)
*Duration: 2 hours · 100 points via TA checkoff, part of the Labs component (10%)*

**Tools used:** Weeks 0–8 — the hash tables of L26, dict/set patterns of L27, `random.randint` (L17),
`time.perf_counter` (as L20 and L25 use it). Everything goes in **one file**, `hash_table.py`: importing
your own modules is not something this course has taught.

---

## Objectives

By the end of this lab, you will:
- [ ] Implement a complete hash table using chaining, from scratch
- [ ] Implement a complete hash table using open addressing (linear probing), from scratch
- [ ] Measure load factor's effect on performance
- [ ] Apply the dict lookup pattern to two-sum
- [ ] Investigate the `__hash__`/`__eq__` contract with a custom class

---

## Setup

```bash
mkdir -p "$CS101/week8"
cd "$CS101/week8"
```

---

*(Revised 2026-09-26: the parts added up to about 130 minutes. Part 3 (amortized insertion timing — Problem
Set 6 B2 simulated the same thing) was removed; Part 4 keeps only `two_sum`; reflection Q3–Q4 went. Part
numbers are unchanged.)*

## Part 1: Build Both Hash Table Variants (40 minutes)

Create `hash_table.py`. Implement BOTH collision-resolution strategies from lecture.

```python
#!/usr/bin/env python3
"""
hash_table.py
CS 101 — Week 8, Lab 8

Two complete hash table implementations: chaining and open addressing.

Student: ____________________________
Date: ______________________________
"""


class ChainedHashTable:
    """
    Hash table using separate chaining for collision resolution.
    Automatically resizes (doubles) when load factor exceeds 0.75.
    """

    def __init__(self, initial_size=8):
        self._size = initial_size
        self._buckets = [[] for _ in range(self._size)]
        self._count = 0
        self._max_load_factor = 0.75

        # Instrumentation for this lab:
        self.total_comparisons = 0     # incremented on every key comparison
        self.resize_count = 0

    def _index(self, key, size=None):
        size = size if size is not None else self._size
        return hash(key) % size

    def load_factor(self):
        return self._count / self._size

    def _resize(self):
        """Double the bucket array and re-insert every element. O(n)."""
        old_buckets = self._buckets
        self._size *= 2
        self._buckets = [[] for _ in range(self._size)]
        self.resize_count += 1

        # TODO: re-insert every (key, value) from old_buckets into self._buckets
        # using the NEW size for index computation
        for chain in old_buckets:
            for key, value in chain:
                idx = self._index(key)
                self._buckets[idx].append((key, value))

    def put(self, key, value):
        """
        Insert or update key -> value. Resize if load factor exceeds threshold.
        """
        idx = self._index(key)
        chain = self._buckets[idx]

        # TODO: scan the chain for an existing key (update case)
        # increment self.total_comparisons for EACH comparison made
        for i, (existing_key, existing_value) in enumerate(chain):
            self.total_comparisons += 1
            if existing_key == key:
                chain[i] = (key, value)
                return

        # TODO: not found — append new entry, increment count, check resize
        chain.append((key, value))
        self._count += 1

        if self.load_factor() > self._max_load_factor:
            self._resize()

    def get(self, key):
        """Retrieve value for key. Raise KeyError if not found."""
        idx = self._index(key)
        chain = self._buckets[idx]

        # TODO: scan the chain, incrementing self.total_comparisons each time
        for existing_key, existing_value in chain:
            self.total_comparisons += 1
            if existing_key == key:
                return existing_value

        raise KeyError(key)

    def contains(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def __len__(self):
        return self._count

    def max_chain_length(self):
        """Return the length of the longest chain — a diagnostic tool."""
        return max(len(chain) for chain in self._buckets)


class OpenAddressingHashTable:
    """
    Hash table using linear probing for collision resolution.
    Automatically resizes (doubles) when load factor exceeds 0.5
    (open addressing needs a LOWER threshold than chaining, since
    performance degrades faster as the table fills up).
    """

    _EMPTY = object()
    _DELETED = object()

    def __init__(self, initial_size=8):
        self._size = initial_size
        self._keys = [self._EMPTY] * self._size
        self._values = [None] * self._size
        self._count = 0
        self._max_load_factor = 0.5

        self.total_probes = 0
        self.resize_count = 0

    def _index(self, key, size=None):
        size = size if size is not None else self._size
        return hash(key) % size

    def load_factor(self):
        return self._count / self._size

    def _resize(self):
        """Double the table and re-insert every element."""
        old_keys = self._keys
        old_values = self._values
        self._size *= 2
        self._keys = [self._EMPTY] * self._size
        self._values = [None] * self._size
        self._count = 0
        self.resize_count += 1

        # TODO: re-insert every valid (non-empty, non-deleted) key-value pair
        for k, v in zip(old_keys, old_values):
            if k is not self._EMPTY and k is not self._DELETED:
                self.put(k, v)   # reuse put() — it will use the NEW size

    def put(self, key, value):
        """Insert or update key -> value using linear probing."""
        if self.load_factor() >= self._max_load_factor:
            self._resize()

        idx = self._index(key)
        start_idx = idx

        # TODO: probe until finding an EMPTY/DELETED slot or the existing key
        # increment self.total_probes for each slot examined
        while self._keys[idx] is not self._EMPTY and self._keys[idx] is not self._DELETED:
            self.total_probes += 1
            if self._keys[idx] == key:
                self._values[idx] = value
                return
            idx = (idx + 1) % self._size
            if idx == start_idx:
                raise Exception("Hash table is full!")

        self._keys[idx] = key
        self._values[idx] = value
        self._count += 1

    def get(self, key):
        """Retrieve value for key using linear probing. Raise KeyError if not found."""
        idx = self._index(key)
        start_idx = idx

        # TODO: probe until finding the key or an EMPTY slot (meaning: not present)
        while self._keys[idx] is not self._EMPTY:
            self.total_probes += 1
            if self._keys[idx] is not self._DELETED and self._keys[idx] == key:
                return self._values[idx]
            idx = (idx + 1) % self._size
            if idx == start_idx:
                break

        raise KeyError(key)

    def contains(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def remove(self, key):
        idx = self._index(key)
        start_idx = idx

        while self._keys[idx] is not self._EMPTY:
            if self._keys[idx] is not self._DELETED and self._keys[idx] == key:
                self._keys[idx] = self._DELETED
                self._count -= 1
                return
            idx = (idx + 1) % self._size
            if idx == start_idx:
                break

        raise KeyError(key)

    def __len__(self):
        return self._count


def run_tests():
    """Verify both implementations are correct."""

    # ChainedHashTable
    cht = ChainedHashTable(initial_size=4)
    cht.put("apple", 1)
    cht.put("banana", 2)
    cht.put("cherry", 3)
    assert cht.get("apple") == 1
    assert cht.get("banana") == 2
    assert cht.contains("date") == False
    assert len(cht) == 3
    cht.put("apple", 100)   # update
    assert cht.get("apple") == 100
    assert len(cht) == 3    # still 3, not 4
    print("✓ ChainedHashTable basic operations")

    # Force a resize and verify data integrity:
    cht2 = ChainedHashTable(initial_size=4)
    for i in range(50):
        cht2.put(f"key{i}", i)
    assert len(cht2) == 50
    assert cht2.resize_count > 0, "Should have resized at least once by n=50"
    for i in range(50):
        assert cht2.get(f"key{i}") == i, f"Lost data for key{i} after resize!"
    print(f"✓ ChainedHashTable resize integrity (resized {cht2.resize_count} times)")

    # OpenAddressingHashTable
    oht = OpenAddressingHashTable(initial_size=8)
    oht.put("apple", 1)
    oht.put("banana", 2)
    oht.put("cherry", 3)
    assert oht.get("apple") == 1
    assert oht.contains("date") == False
    oht.remove("banana")
    assert len(oht) == 2
    try:
        oht.get("banana")
        assert False, "should have raised KeyError"
    except KeyError:
        pass
    print("✓ OpenAddressingHashTable basic operations + tombstone removal")

    oht2 = OpenAddressingHashTable(initial_size=4)
    for i in range(50):
        oht2.put(f"key{i}", i)
    assert len(oht2) == 50
    for i in range(50):
        assert oht2.get(f"key{i}") == i, f"Lost data for key{i} after resize!"
    print(f"✓ OpenAddressingHashTable resize integrity (resized {oht2.resize_count} times)")

    print("\n🎉 All hash table tests passed!")


if __name__ == "__main__":
    run_tests()
```

Run it: `python3 hash_table.py`

---

## Part 2: Load Factor vs. Performance — Empirical Investigation (30 minutes)

Add this section to the **bottom** of `hash_table.py` (instead of a separate `load_factor_experiment.py`):

```python
#!/usr/bin/env python3
"""
load_factor_experiment.py
CS 101 — Week 8, Lab 8

Empirically measure how load factor affects average comparisons/probes per lookup.
"""

import random


def measure_chained_at_load_factor(target_load_factor, table_size=1000, num_lookups=1000):
    """
    Build a ChainedHashTable, disable auto-resize, fill it to the target
    load factor, then measure average comparisons per successful lookup.
    """
    ht = ChainedHashTable(initial_size=table_size)
    ht._max_load_factor = 999  # effectively disable auto-resize for this experiment

    num_entries = int(target_load_factor * table_size)
    keys = [f"key{i}" for i in range(num_entries)]
    for k in keys:
        ht.put(k, 1)

    # Measure average comparisons per lookup (successful lookups only)
    ht.total_comparisons = 0
    sample_keys = [keys[random.randint(0, len(keys) - 1)] for _ in range(num_lookups)]
    for k in sample_keys:
        ht.get(k)

    avg_comparisons = ht.total_comparisons / len(sample_keys)
    return avg_comparisons, ht.max_chain_length()


def measure_open_addressing_at_load_factor(target_load_factor, table_size=1000, num_lookups=1000):
    """Same experiment, for open addressing."""
    ht = OpenAddressingHashTable(initial_size=table_size)
    ht._max_load_factor = 999  # disable auto-resize

    num_entries = int(target_load_factor * table_size)
    keys = [f"key{i}" for i in range(num_entries)]
    for k in keys:
        ht.put(k, 1)

    ht.total_probes = 0
    sample_keys = [keys[random.randint(0, len(keys) - 1)] for _ in range(num_lookups)]
    for k in sample_keys:
        ht.get(k)

    avg_probes = ht.total_probes / len(sample_keys)
    return avg_probes


print("=" * 65)
print("CHAINING: Load Factor vs. Average Comparisons per Lookup")
print("=" * 65)
print(f"{'Load Factor':>12} {'Avg Comparisons':>18} {'Max Chain Length':>18}")

for lf in [0.25, 0.5, 0.75, 1.0, 2.0, 4.0, 8.0]:
    avg_comp, max_chain = measure_chained_at_load_factor(lf)
    print(f"{lf:12.2f} {avg_comp:18.3f} {max_chain:18}")

print()
print("=" * 65)
print("OPEN ADDRESSING: Load Factor vs. Average Probes per Lookup")
print("=" * 65)
print(f"{'Load Factor':>12} {'Avg Probes':>18}")

# NOTE: open addressing CANNOT exceed load factor 1.0 (no room left)!
for lf in [0.25, 0.5, 0.7, 0.9, 0.95]:
    avg_probes = measure_open_addressing_at_load_factor(lf)
    print(f"{lf:12.2f} {avg_probes:18.3f}")
```

Run it: `python3 load_factor_experiment.py`

**Record in `LAB 8 Hash Tables from Scratch.md`:**
1. For chaining, does average comparisons grow roughly linearly with load factor? Does this match the theoretical prediction ("average chain length ≈ load factor")?
2. For open addressing, what happens to average probes as load factor approaches 0.9–0.95? Does it grow linearly, or does it seem to accelerate?
3. Based on this data, explain why Python's real dict implementation (open addressing) keeps its load factor threshold below 2/3, while a chaining-based table (like conceptually similar to Java's HashMap) can tolerate a higher threshold before resizing.

---

## Part 4: Apply the Patterns — Two-Sum (10 minutes)

Add this section to the **bottom** of `hash_table.py` (instead of a separate `dict_patterns.py`):

```python
#!/usr/bin/env python3
"""
dict_patterns.py
CS 101 — Week 8, Lab 8

Apply this week's lookup pattern to two-sum in O(n).
"""


def two_sum(nums, target):
    """
    Return indices (i, j) of two numbers summing to target, or None.
    O(n) using the complement-lookup pattern.
    """
    # TODO: implement using a dict mapping value -> index
    pass


assert two_sum([2, 7, 11, 15], 9) == (0, 1)
assert two_sum([3, 2, 4], 6)       == (1, 2)
assert two_sum([1, 2, 3], 100)     == None
print("✓ two_sum")


print("\n🎉 two_sum passed!")
```

---

## Part 5: The `__hash__`/`__eq__` Contract — Investigation (10 minutes)

Add this section to the **bottom** of `hash_table.py` (instead of a separate `hash_contract_investigation.py`):

```python
#!/usr/bin/env python3
"""
hash_contract_investigation.py
CS 101 — Week 8, Lab 8

Investigate what happens when the __hash__/__eq__ contract is violated
or correctly implemented.
"""


class GoodPoint:
    """Correctly implements both __eq__ and __hash__."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, GoodPoint) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"GoodPoint({self.x},{self.y})"


class BadPoint:
    """Defines __eq__ but NOT __hash__ — Python makes this unhashable."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, BadPoint) and self.x == other.x and self.y == other.y


# Investigate GoodPoint:
p1 = GoodPoint(1, 2)
p2 = GoodPoint(1, 2)   # different object, same value

print(f"p1 == p2: {p1 == p2}")
print(f"hash(p1) == hash(p2): {hash(p1) == hash(p2)}")

s = {p1, p2}
print(f"set({{p1, p2}}) has length: {len(s)}  (should be 1 — they're 'the same' by value)")

d = {p1: "first"}
print(f"p2 in d: {p2 in d}")   # True! Even though p2 is a DIFFERENT object.
print(f"d[p2]: {d[p2]}")        # "first" — found via p1's stored value!

# Investigate BadPoint:
print("\n--- BadPoint ---")
bp1 = BadPoint(1, 2)
try:
    hash(bp1)
    print("BadPoint is hashable (unexpected!)")
except TypeError as e:
    print(f"BadPoint is UNHASHABLE, as expected: {e}")

try:
    s2 = {bp1}
    print("Managed to put BadPoint in a set (unexpected!)")
except TypeError as e:
    print(f"Cannot put BadPoint in a set: {e}")
```

Run it and **record in `LAB 8 Hash Tables from Scratch.md`:**
1. Why does `d[p2]` successfully return `"first"` even though `p2` is a different object from `p1`?
2. Why does Python refuse to let `BadPoint` be hashed at all, rather than just letting it behave unpredictably?

---

## Part 6: Commit and Reflection (10 minutes)

```bash
cd "$CS101/week8"
git add .
git commit -m "Week 8 Lab: hash tables from scratch, load factor experiments, dict patterns"
git push
```

### Reflection in `LAB 8 Hash Tables from Scratch.md`:

**Q1.** You implemented BOTH chaining and open addressing. If you had to choose one for a general-purpose hash table implementation, which would you pick, and why? Reference your load factor experiment data.

**Q2.** In `_resize()` for `ChainedHashTable`, why is it WRONG to simply copy the old `_buckets` list into a bigger array (e.g., `self._buckets = old_buckets + [[] for _ in range(extra)]`)? What specifically breaks?

---

## TA Checkoff Criteria

| Part | Points | Show your TA |
|---|---|---|
| 1 | 40 | Both hash tables implemented; `run_tests()` passes including resize integrity |
| 2 | 25 | Load-factor table with the recorded analysis |
| 4 | 15 | `two_sum` passes its asserts |
| 5 | 20 | Contract investigation output with both questions answered |
| **Total** | **100** | Reflection answered and work committed (required) |

---

*CS 101 · Week 8 · Lab 8 · Tuesday 24 November 2026 · © CSE Department*

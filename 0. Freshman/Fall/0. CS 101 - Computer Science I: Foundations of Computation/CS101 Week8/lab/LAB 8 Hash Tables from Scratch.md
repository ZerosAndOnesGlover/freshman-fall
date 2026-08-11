# CS 101 · Lab 8
## Building a Hash Table From Scratch

**Tuesday of Week 9 · Lab Section** — sat after this week's Wed–Fri lectures, and covers Week 8.
*Duration: 2 hours · Graded on completion (TA checkoff)*

---

## Objectives

By the end of this lab, you will:
- [ ] Implement a complete hash table using chaining, from scratch
- [ ] Implement a complete hash table using open addressing (linear probing), from scratch
- [ ] Empirically measure and visualize load factor's effect on performance
- [ ] Verify amortized O(1) insertion via resizing, directly
- [ ] Benchmark dict/set vs. list for membership testing at scale
- [ ] Apply dict/set patterns to solve 3 real algorithmic problems
- [ ] Investigate the `__hash__`/`__eq__` contract with a custom class

---

## Setup

```bash
cd ~/cs101
mkdir week8 && cd week8
pip install matplotlib --user   # if not already installed
```

---

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

Create `load_factor_experiment.py`:

```python
#!/usr/bin/env python3
"""
load_factor_experiment.py
CS 101 — Week 8, Lab 8

Empirically measure how load factor affects average comparisons/probes per lookup.
"""

from hash_table import ChainedHashTable, OpenAddressingHashTable
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
    sample_keys = random.sample(keys, min(num_lookups, len(keys)))
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
    sample_keys = random.sample(keys, min(num_lookups, len(keys)))
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

## Part 3: Verifying Amortized O(1) Insertion (20 minutes)

Create `amortized_insertion_test.py`:

```python
#!/usr/bin/env python3
"""
amortized_insertion_test.py
CS 101 — Week 8, Lab 8

Verify that hash table insertion is O(1) amortized, despite occasional
O(n) resize operations — the same pattern as PS6's DynamicArray.
"""

from hash_table import ChainedHashTable
import time


def measure_insertion_times(n):
    """Insert n items one at a time, recording the time for EACH insertion."""
    ht = ChainedHashTable(initial_size=8)
    times = []

    for i in range(n):
        start = time.perf_counter()
        ht.put(f"key{i}", i)
        times.append(time.perf_counter() - start)

    return times, ht.resize_count


n = 10000
times, resize_count = measure_insertion_times(n)

avg_time = sum(times) / len(times)
max_time = max(times)
total_time = sum(times)

print(f"Total insertions: {n}")
print(f"Resize events: {resize_count}")
print(f"Average time per insertion: {avg_time*1e6:.3f} μs")
print(f"MAXIMUM single insertion time: {max_time*1e6:.3f} μs  (this was a resize event)")
print(f"Ratio (max/avg): {max_time/avg_time:.1f}x")
print(f"\nTotal time for all {n} insertions: {total_time*1000:.2f} ms")
print(f"This confirms O(1) AMORTIZED cost: {total_time/n*1e6:.3f} μs per insertion on average,")
print(f"even though {resize_count} individual insertions were much more expensive (the resizes).")
```

**Record in `LAB 8 Hash Tables from Scratch.md`:** How does the ratio of max-to-average insertion time compare to what you found for `DynamicArray` in PS6? Is the underlying mathematical reason the same?

---

## Part 4: Dict vs. List Membership Benchmark (20 minutes)

Create `membership_benchmark.py`:

```python
#!/usr/bin/env python3
"""
membership_benchmark.py
CS 101 — Week 8, Lab 8

The single most important practical lesson of this week: measure the
real-world cost difference between list and set/dict membership testing.
"""

import time
import random


def benchmark_membership(sizes):
    print(f"{'n':>10} {'list (μs)':>15} {'set (μs)':>15} {'speedup':>10}")

    for n in sizes:
        data = list(range(n))
        data_set = set(data)

        # Worst case: search for an element NOT present (must scan everything for list)
        target = -1

        # Time list membership (average over several repeats for stability)
        repeats = max(1, min(20, 1_000_000 // max(n, 1)))
        t0 = time.perf_counter()
        for _ in range(repeats):
            target in data
        t_list = (time.perf_counter() - t0) / repeats

        t0 = time.perf_counter()
        for _ in range(repeats):
            target in data_set
        t_set = (time.perf_counter() - t0) / repeats

        speedup = t_list / t_set if t_set > 0 else float('inf')
        print(f"{n:10} {t_list*1e6:15.3f} {t_set*1e6:15.4f} {speedup:9.0f}x")


benchmark_membership([100, 1000, 10000, 100000, 1000000])
```

Run it: `python3 membership_benchmark.py`

**Record in `LAB 8 Hash Tables from Scratch.md`:** At n=1,000,000, what is the approximate speedup factor? Does this match the theoretical prediction (list O(n), set O(1) — so the speedup should scale roughly linearly with n)?

---

## Part 5: Apply the Patterns — Three Real Problems (20 minutes)

Create `dict_patterns.py`:

```python
#!/usr/bin/env python3
"""
dict_patterns.py
CS 101 — Week 8, Lab 8

Apply this week's patterns to solve three problems, each in O(n).
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


def first_unique_char(s):
    """
    Return the first character in s that appears exactly once, or None.
    O(n), two-pass (count, then scan in order).
    """
    # TODO: implement
    pass


assert first_unique_char("swiss")      == 'w'
assert first_unique_char("aabbcc")     == None
assert first_unique_char("statistics") == 'a'
print("✓ first_unique_char")


def group_anagrams(words):
    """
    Group words that are anagrams of each other.

    Key insight: two words are anagrams iff their SORTED character
    sequences are identical. Use the sorted string as a dict key.

    Returns a list of lists (each inner list is a group of anagrams).
    Order of groups and order within groups should follow first appearance.

    Examples:
        group_anagrams(["eat","tea","tan","ate","nat","bat"])
        → [["eat","tea","ate"], ["tan","nat"], ["bat"]]
    """
    groups = {}   # maps sorted-tuple -> list of original words
    order = []    # track first-appearance order of each group's key

    # TODO: for each word, compute its sorted-character key,
    # append to the appropriate group (creating it if new)

    return [groups[key] for key in order]


result = group_anagrams(["eat","tea","tan","ate","nat","bat"])
assert sorted(result[0]) == sorted(["eat","tea","ate"])
assert sorted(result[1]) == sorted(["tan","nat"])
assert result[2] == ["bat"]
print("✓ group_anagrams")

print("\n🎉 All pattern applications passed!")
```

---

## Part 6: The `__hash__`/`__eq__` Contract — Investigation (10 minutes)

Create `hash_contract_investigation.py`:

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

## Part 7: Commit and Reflection (10 minutes)

```bash
cd ~/cs101/week8
git add .
git commit -m "Week 8 Lab: hash tables from scratch, load factor experiments, dict patterns"
git push
```

### Reflection in `LAB 8 Hash Tables from Scratch.md`:

**Q1.** You implemented BOTH chaining and open addressing. If you had to choose one for a general-purpose hash table implementation, which would you pick, and why? Reference your load factor experiment data.

**Q2.** In `_resize()` for `ChainedHashTable`, why is it WRONG to simply copy the old `_buckets` list into a bigger array (e.g., `self._buckets = old_buckets + [[] for _ in range(extra)]`)? What specifically breaks?

**Q3.** Your membership benchmark showed dramatic speedups for `set` over `list`. Given this, why doesn't Python just make ALL lists behave like sets internally? What would be lost?

**Q4.** The `OpenAddressingHashTable` uses a lower max load factor (0.5) than `ChainedHashTable` (0.75). Using your Part 2 data, justify why this different threshold makes engineering sense.

---

## TA Checkoff Criteria

Show your TA:
- [ ] `hash_table.py` — both classes fully implemented, `run_tests()` passes including resize integrity checks
- [ ] `load_factor_experiment.py` output with analysis in notes
- [ ] `amortized_insertion_test.py` output with comparison to PS6's DynamicArray
- [ ] `membership_benchmark.py` output showing dramatic speedup at large n
- [ ] `dict_patterns.py` — all 3 functions implemented and passing
- [ ] `hash_contract_investigation.py` output with both questions answered

---

## Bonus Challenges

**Bonus 1 — Robin Hood hashing:**
Research "Robin Hood hashing," a refinement of open addressing that reduces variance in probe sequence length by having "richer" (shorter probe distance) entries yield their slot to "poorer" (longer probe distance) entries during insertion. Implement it and compare average probe counts against your linear-probing version at high load factor.

**Bonus 2 — Custom hash function quality:**
Write a deliberately BAD hash function (e.g., `hash(key) = len(key)` for strings) and measure how badly it degrades your `ChainedHashTable`'s performance (via `max_chain_length()`) compared to Python's built-in `hash()`. This demonstrates concretely why hash function QUALITY, not just the collision-resolution strategy, matters enormously.

**Bonus 3 — Real memory comparison:**
Using `sys.getsizeof()` (from Week 7's lab), compare the actual memory footprint of your `ChainedHashTable` vs. `OpenAddressingHashTable` vs. Python's built-in `dict`, all holding the same 10,000 key-value pairs.

---

*CS 101 · Week 8 · Lab 8 · © CSE Department*

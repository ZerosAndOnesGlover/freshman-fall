# CS 101 · Problem Set 8 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** The reference `ps8.py` below was run; every assert passes.

*(Revised 2026-09-26: old A2, A4, B2(e), B3(a), B3(c) and B5(c) were removed from the set; old A3 is A2 and
old B3(b) is B3.)*

### Part A (24 points)

**A1 Hash Table Mechanics (14 pts).** 4 / 3 / 4 / 3.

**(a)** `hash([1,2,3])` raises `TypeError` because `list` is **mutable** and deliberately defines `__hash__ = None`. A hash table places an entry in a bucket determined by `hash(key)` *at insertion time*. If a key's contents could change afterwards, its hash would change, and the entry would sit in a bucket that no longer matches — permanently unreachable, since lookup probes the *new* hash's bucket. Tuples are immutable, so their hash is stable for life, making them safe keys. (A tuple containing a list is still unhashable — hashability is recursive.)

**(b)** Load factor `= 8/10 = **0.8**`. Since `0.8 > 0.75`, this **would** trigger a resize.

**(c)** In open addressing, lookup probes forward from the home bucket and stops at the first genuinely empty slot. Deleting by writing plain `None` breaks that chain. Concrete example, table size 5, linear probing, keys hashing as `A→1`, `B→1`, `C→1`:

- Insert A → slot 1. Insert B → slot 1 taken, probe → slot 2. Insert C → probe → slot 3.
- Delete B by writing `None` into slot 2.
- Look up C: probe slot 1 (A, not a match) → slot 2 is `None` → **conclude C is absent and stop**. But C is sitting in slot 3.

A **tombstone** marks slot 2 as "deleted, but the probe chain continues here", so lookup keeps going and finds C. Tombstones count as occupied for probing but as free for insertion.

**(d)** Open addressing degrades much more sharply near a full table: with all entries in the array itself, clustering makes the expected probe count blow up roughly as `1/(1−α)`, diverging as `α → 1`. Chaining degrades gracefully — at `α = 2` the average chain is just 2 links, still O(1) expected. So open addressing must resize earlier (Python uses ≈ 2/3) while chaining tolerates ≈ 0.75–1.0+.

**A2 Complexity (10 pts).** 4 / 3 / 3.
- **(a) O(n)** — building a set from each list is O(n), and set equality compares sizes then membership, O(n) expected. (The naive nested-loop comparison would be O(n²).)
- **(b) O(n)** — one pass to count into a dict (O(1) expected per insert), one pass over the dict to collect counts > 1.
- **(c) O(n + m)** — build a set from the smaller list, then scan the larger testing membership at O(1) expected each. Building from the *smaller* list minimises auxiliary space; the time bound is the same either way.

### Part B — reference `ps8.py` (76 points)

```python
from collections import defaultdict


# --- B1: ChainedHashTable from L26, extended ---
class ChainedHashTable:
    """
    A hash table using separate chaining for collision resolution.
    Each bucket is a list of (key, value) pairs.
    """

    def __init__(self, initial_size=8):
        self._size = initial_size
        self._buckets = [[] for _ in range(self._size)]
        self._count = 0

    def _index(self, key):
        return hash(key) % self._size

    def put(self, key, value):
        """
        Insert or update key -> value.

        Must check the ENTIRE chain at the target bucket, in case the
        key already exists (update) vs. is new (append).
        """
        idx = self._index(key)
        chain = self._buckets[idx]

        for i, (existing_key, existing_value) in enumerate(chain):
            if existing_key == key:
                chain[i] = (key, value)    # update existing
                return

        chain.append((key, value))         # new key
        self._count += 1

    def get(self, key):
        """Retrieve the value for key, or raise KeyError."""
        idx = self._index(key)
        chain = self._buckets[idx]

        for existing_key, existing_value in chain:
            if existing_key == key:
                return existing_value

        raise KeyError(key)

    def contains(self, key):
        idx = self._index(key)
        chain = self._buckets[idx]
        return any(existing_key == key for existing_key, _ in chain)

    def remove(self, key):
        idx = self._index(key)
        chain = self._buckets[idx]

        for i, (existing_key, existing_value) in enumerate(chain):
            if existing_key == key:
                del chain[i]
                self._count -= 1
                return

        raise KeyError(key)

    def __len__(self):
        return self._count

    def keys(self):
        """All keys, in bucket order. Theta(n + buckets)."""
        out = []
        for chain in self._buckets:
            for k, _ in chain:
                out.append(k)
        return out

    def values(self):
        """All values. Theta(n + buckets)."""
        out = []
        for chain in self._buckets:
            for _, v in chain:
                out.append(v)
        return out

    def items(self):
        """All (key, value) pairs. Theta(n + buckets)."""
        out = []
        for chain in self._buckets:
            for pair in chain:
                out.append(pair)
        return out

    def update(self, other):
        """put every pair of the dict `other`. O(k) average for k pairs."""
        for k, v in other.items():
            self.put(k, v)


t = ChainedHashTable()
t.update({"a": 1, "b": 2, "c": 3})
t.put("b", 20)
assert len(t) == 3 and sorted(t.keys()) == ["a", "b", "c"] and sorted(t.values()) == [1, 3, 20]
assert sorted(t.items()) == [("a", 1), ("b", 20), ("c", 3)]
assert ChainedHashTable().keys() == [] and t.contains("a") and not t.contains("z")


# --- B2: Faster versions with dict/set ---
def has_duplicate(lst):
    """True if any value repeats. Theta(n) with a set (vs Theta(n^2) comparing pairs)."""
    seen = set()
    for x in lst:
        if x in seen:
            return True
        seen.add(x)
    return False

def word_frequency(text):
    """dict word -> count, lower-cased. Theta(n)."""
    counts = {}
    for w in text.lower().split():
        counts[w] = counts.get(w, 0) + 1
    return counts

def is_anagram(s1, s2):
    """Same letters with the same counts, ignoring case and spaces. Theta(n)."""
    def counts(s):
        c = {}
        for ch in s.lower():
            if ch != " ":
                c[ch] = c.get(ch, 0) + 1
        return c
    return counts(s1) == counts(s2)

def longest_consecutive(nums):
    """Length of the longest run of consecutive integer values. Theta(n): each run is walked from its start only."""
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 not in values:           # x starts a run
            length = 1
            while x + length in values:
                length += 1
            if length > best:
                best = length
    return best

assert has_duplicate([1, 2, 3, 2]) and not has_duplicate([1, 2, 3]) and not has_duplicate([])
assert word_frequency("the cat the hat THE") == {"the": 3, "cat": 1, "hat": 1}
assert is_anagram("Listen", "Silent") and is_anagram("dormitory", "dirty room") and not is_anagram("abc", "abd")
assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4 and longest_consecutive([]) == 0 and longest_consecutive([5, 5, 6]) == 2


# --- B3: Two-sum pairs ---
def two_sum_all_pairs(nums, target):
    """Every (i, j), i < j, summing to target, sorted. Keeps a list of indices per value."""
    where = {}
    pairs = []
    for j, x in enumerate(nums):
        for i in where.get(target - x, []):
            pairs.append((i, j))
        if x not in where:
            where[x] = []
        where[x].append(j)
    pairs.sort()
    return pairs

assert two_sum_all_pairs([3, 3, 3], 6) == [(0, 1), (0, 2), (1, 2)]
assert two_sum_all_pairs([1, 5, 2, 4, 3], 6) == [(0, 1), (2, 3)]


# --- B4: Memoisation with a cache dict (L27 §7) ---
def fib_memo(n, cache, stats):
    """fib(n) with a cache dict; stats = [hits, misses]."""
    if n in cache:
        stats[0] += 1
        return cache[n]
    stats[1] += 1
    if n < 2:
        result = n
    else:
        result = fib_memo(n - 1, cache, stats) + fib_memo(n - 2, cache, stats)
    cache[n] = result
    return result

stats = [0, 0]
assert fib_memo(20, {}, stats) == 6765
print("fib(20): hits", stats[0], "misses", stats[1])
assert stats == [18, 21]


# --- B5: Set operations ---
def jaccard(a, b):
    """|a & b| / |a | b|; 1.0 for two empty sets."""
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)

def common_words(text1, text2):
    return set(text1.lower().split()) & set(text2.lower().split())

assert jaccard({1, 2, 3}, {2, 3, 4}) == 0.5 and jaccard(set(), set()) == 1.0
assert common_words("The cat sat", "the dog sat down") == {"the", "sat"}
print("all asserts passed")
```

Output:

```
fib(20): hits 18 misses 21
all asserts passed
```

**B4.** Misses = 21 = one per distinct `n` from 0 to 20; every later request for the same `n` is a hit (18).
Lab 4's naive `fib(20)` made 21,891 calls; the cached version makes 39.

**Marking.** B1 3 each. B2: 5/5/5/7 — `longest_consecutive` must start runs only at run starts (otherwise
Θ(n²)). B3: 14 — `two_sum_all_pairs([3, 3, 3], 6)` must give all three pairs. B4: 8 code, 6 explanation.
B5: 7/7. Missing cost statement or fewer than two asserts: −1 per function (max −5).

---

*CS 101 · Week 8 · Problem Set 8 · Due Friday 27 November 2026, 17:00 · © CSE Department*

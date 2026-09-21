# CS 101 · Problem Set 8
## Hash Tables, Dictionaries, and Sets

**Released:** Friday 20 November 2026, 10:00 (after L27) · Week 8
**Due:** Friday 27 November 2026, 17:00 · Week 9 — late penalty from 17:01
**Submission:** `ps8.py` (Part B) and your answer sheet (Part A) in `"$CS101/week8"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 3–4 hours
**Note:** Project 1 is due the same day. Finish Project 1's core by Tuesday 24 November, then do this set.

---

## What this problem set uses

Weeks 0–8, above all this week's: hash functions, buckets, `dict` and `set`, the `__hash__`/`__eq__`
contract (L25), chaining, open addressing and tombstones, load factor and resizing, and L26's
`ChainedHashTable` (L26), and the counting, grouping, membership, two-sum and memoisation patterns,
`defaultdict`, and set operators `& | - ^` (L25 §5, L27).

**Not needed and not expected:** decorators, dunder methods beyond `__init__`/`__len__`/`__hash__`/`__eq__`,
the two-pointer technique, `functools`.

---

## Part A: Written (36 points)

### A1: Hash Table Mechanics (12 points)

**(a)** Why does `hash([1, 2, 3])` raise `TypeError` while `hash((1, 2, 3))` works? Refer to mutability and
to why a dict needs a key's hash to stay fixed.
**(b)** A chained table has 10 buckets and 8 entries. What is its load factor? Does it trigger a resize at
L26's 0.75 threshold?
**(c)** What is a tombstone in open addressing? Give a small example (table size, keys, which slots they
land in) showing what goes wrong if deletion writes a plain empty marker instead.
**(d)** Why does an open-addressing table resize at a lower load factor than a chained one? (L26 §3, §5.)

### A2: The `__hash__`/`__eq__` Contract (10 points)

**(a)** State the contract: if `a == b`, what must be true of `hash(a)` and `hash(b)`? Is the converse required?
**(b)** Why does this class break the contract? Give two instances `a`, `b` with `a == b` but different hashes,
and a bug this causes in a dict or set.

```python
class BadCache:
    def __init__(self, key, value):
        self.key = key
        self.value = value
    def __eq__(self, other):
        return self.key == other.key            # equality uses key only
    def __hash__(self):
        return hash((self.key, self.value))     # hash uses key AND value
```

### A3: Costs (6 points)

State and justify the cost, in terms of the input sizes:
**(a)** Deciding whether two lists contain the same set of values, using sets.
**(b)** Finding every value that occurs more than once in a list of `n`, using a counting dict.
**(c)** Finding the values in both list A (size `n`) and list B (size `m`), using a set of the smaller one.

### A4: Choosing a Structure (8 points)

`list`, `set` or `dict` — and why, in one or two sentences:
**(a)** a shopping cart where the same item can be added twice and the order added is shown;
**(b)** the usernames currently logged in, checked constantly; **(c)** an English → French word table;
**(d)** a class roster in official order, occasionally checked for a name.

---

## Part B: Python (`ps8.py`) (64 points)

State each function's cost in its docstring and give it at least two `assert` tests.

### B1: Extending L26's Hash Table (12 points)

Copy `ChainedHashTable` from L26 into `ps8.py` and add:
**(a)** `keys()`, **(b)** `values()`, **(c)** `items()` — lists of the stored keys, values, `(key, value)` pairs;
**(d)** `update(other)` — `put` every pair of a Python dict `other`, overwriting existing keys.

### B2: Faster With a Dict or Set (18 points)

Each of these was quadratic, or impossible, with only lists:
**(a)** `has_duplicate(lst)` — Θ(n) with a set.
**(b)** `word_frequency(text)` — dict of lower-cased word → count. `"the cat the hat THE"` → `{"the": 3, "cat": 1, "hat": 1}`.
**(c)** `is_anagram(s1, s2)` — same letters with the same counts, ignoring case and spaces. `("dormitory", "dirty room")` → `True`.
**(d)** `longest_consecutive(nums)` — the longest run of consecutive **values** (not positions) in Θ(n): put
the numbers in a set, and only start counting at an `x` whose `x − 1` is absent. `[100, 4, 200, 1, 3, 2]` → `4`.
**(e)** `group_by_first_letter(words)` — with `defaultdict(list)` (L27 §3), returning a plain `dict`.

### B3: The Two-Sum Family (16 points)

**(a)** `two_sum(nums, target)` — L27 §5's Θ(n) version, returning `(i, j)` or `None`.
**(b)** `two_sum_all_pairs(nums, target)` — **every** `(i, j)` with `i < j`; keep a dict from value to the
list of indices seen so far. `([3, 3, 3], 6)` → `[(0, 1), (0, 2), (1, 2)]`.
**(c)** `four_sum_count(A, B, C, D)` — how many `(i, j, k, l)` give `A[i] + B[j] + C[k] + D[l] == 0`, in Θ(n²):
count every `a + b` in a dict, then look up `−(c + d)` for every `c, d`.
`([1, 2], [-2, -1], [-1, 2], [0, 2])` → `2`.

### B4: Memoisation, Counted (10 points)

Write `fib_memo(n, cache, stats)` in the style of L27 §7, where `stats` is a list `[hits, misses]` that the
function updates. Run `fib_memo(20, {}, stats)` and print the counts. Explain in a comment why the misses
equal the number of distinct sub-problems, and how many naive calls the cache saved (Lab 4 measured them).

### B5: Set Operations (8 points)

**(a)** `jaccard(a, b)` — `|a & b| / |a | b|`, and `1.0` for two empty sets. `({1, 2, 3}, {2, 3, 4})` → `0.5`.
**(b)** `common_words(text1, text2)` — lower-cased words in both, with `&`.
**(c)** `difference_report(a, b, name_a="A", name_b="B")` — print what is only in each, in both, and in exactly one,
using `-`, `&` and `^` (sorted for display).

---

## Grading Rubric

| Problem | Points |
|---------|--------|
| A1 Mechanics | 12 |
| A2 Contract | 10 |
| A3 Costs | 6 |
| A4 Choosing a structure | 8 |
| B1 Hash table | 12 |
| B2 Dict/set versions | 18 |
| B3 Two-sum family | 16 |
| B4 Memoisation | 10 |
| B5 Set operations | 8 |
| **Total** | **100** |

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** The reference `ps8.py` below was run; every assert passes.

### Part A (36 points)

**A1 Hash Table Mechanics (12 pts).** 3 pts each.

**(a)** `hash([1,2,3])` raises `TypeError` because `list` is **mutable** and deliberately defines `__hash__ = None`. A hash table places an entry in a bucket determined by `hash(key)` *at insertion time*. If a key's contents could change afterwards, its hash would change, and the entry would sit in a bucket that no longer matches — permanently unreachable, since lookup probes the *new* hash's bucket. Tuples are immutable, so their hash is stable for life, making them safe keys. (A tuple containing a list is still unhashable — hashability is recursive.)

**(b)** Load factor `= 8/10 = **0.8**`. Since `0.8 > 0.75`, this **would** trigger a resize.

**(c)** In open addressing, lookup probes forward from the home bucket and stops at the first genuinely empty slot. Deleting by writing plain `None` breaks that chain. Concrete example, table size 5, linear probing, keys hashing as `A→1`, `B→1`, `C→1`:

- Insert A → slot 1. Insert B → slot 1 taken, probe → slot 2. Insert C → probe → slot 3.
- Delete B by writing `None` into slot 2.
- Look up C: probe slot 1 (A, not a match) → slot 2 is `None` → **conclude C is absent and stop**. But C is sitting in slot 3.

A **tombstone** marks slot 2 as "deleted, but the probe chain continues here", so lookup keeps going and finds C. Tombstones count as occupied for probing but as free for insertion.

**(d)** Open addressing degrades much more sharply near a full table: with all entries in the array itself, clustering makes the expected probe count blow up roughly as `1/(1−α)`, diverging as `α → 1`. Chaining degrades gracefully — at `α = 2` the average chain is just 2 links, still O(1) expected. So open addressing must resize earlier (Python uses ≈ 2/3) while chaining tolerates ≈ 0.75–1.0+.

**A2 The `__hash__`/`__eq__` Contract (10 pts).**

**(a)** **If `a == b` then `hash(a) == hash(b)`.** The converse is **not** required — unequal objects may share a hash (that is a collision, which hash tables handle). Equal objects with different hashes is the fatal case, because the table would look in the wrong bucket.

**(b)** `BadCache` equates on `key` alone but hashes on `(key, value)`, so two objects can be equal while hashing differently. Verified:

```python
a = BadCache("x", 1)
b = BadCache("x", 2)
a == b                 # True
hash(a) == hash(b)     # False   <- contract broken
```

Consequences, both reproduced: `d = {a: "first"}` then `d[b]` raises **`KeyError`** even though `b == a` — the lookup hashes to a different bucket. And `len({a, b}) == 2`: the set stores two elements that compare equal, so `in`-tests become unreliable and duplicates silently accumulate. The fix is to hash on exactly the fields used for equality: `def __hash__(self): return hash(self.key)`.

*Grading: 4 pts (a) — must state the converse is not required. 6 pts (b) — 2 for the mismatched fields, 2 for concrete instances, 2 for a named consequence (KeyError or duplicate set members).*

**A3 Complexity (6 pts).** 2 pts each.
- **(a) O(n)** — building a set from each list is O(n), and set equality compares sizes then membership, O(n) expected. (The naive nested-loop comparison would be O(n²).)
- **(b) O(n)** — one pass to count into a dict (O(1) expected per insert), one pass over the dict to collect counts > 1.
- **(c) O(n + m)** — build a set from the smaller list, then scan the larger testing membership at O(1) expected each. Building from the *smaller* list minimises auxiliary space; the time bound is the same either way.

**A4 Design Justification (8 pts).** 2 pts each.
- **(a) `list`** — duplicates are meaningful ("2× apples") and insertion order matters for display; sets and dict keys both discard duplicates.
- **(b) `set`** — membership testing is the only operation, and it is O(1) expected; no values needed, no order needed.
- **(c) `dict`** — an explicit key→value mapping (English → French) is exactly what a dict models.
- **(d) `list`** — a fixed ordered roster. *(Accept a well-argued `dict`/`set` **companion** for fast containment, but the primary structure must preserve roster order; a bare `set` loses it and earns 0.)*

### Part B — reference `ps8.py` (64 points)

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

def group_by_first_letter(words):
    """dict letter -> words in first-appearance order, built with defaultdict(list)."""
    groups = defaultdict(list)
    for w in words:
        groups[w[0]].append(w)
    return dict(groups)

assert has_duplicate([1, 2, 3, 2]) and not has_duplicate([1, 2, 3]) and not has_duplicate([])
assert word_frequency("the cat the hat THE") == {"the": 3, "cat": 1, "hat": 1}
assert is_anagram("Listen", "Silent") and is_anagram("dormitory", "dirty room") and not is_anagram("abc", "abd")
assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4 and longest_consecutive([]) == 0 and longest_consecutive([5, 5, 6]) == 2
assert group_by_first_letter(["apple", "bat", "avocado", "cat", "bird"]) == {"a": ["apple", "avocado"], "b": ["bat", "bird"], "c": ["cat"]}


# --- B3: Two-sum family ---
def two_sum(nums, target):
    """(i, j), i < j, with nums[i] + nums[j] == target, or None. Theta(n) (L27)."""
    seen = {}
    for j, x in enumerate(nums):
        if target - x in seen:
            return (seen[target - x], j)
        seen[x] = j
    return None

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

def four_sum_count(A, B, C, D):
    """How many (i, j, k, l) have A[i] + B[j] + C[k] + D[l] == 0. Theta(n^2): count all a + b sums first."""
    sums = {}
    for a in A:
        for b in B:
            sums[a + b] = sums.get(a + b, 0) + 1
    count = 0
    for c in C:
        for d in D:
            count += sums.get(-(c + d), 0)
    return count

assert two_sum([2, 7, 11, 15], 9) == (0, 1) and two_sum([3, 2, 4], 6) == (1, 2) and two_sum([1, 2], 7) is None
assert two_sum_all_pairs([3, 3, 3], 6) == [(0, 1), (0, 2), (1, 2)]
assert two_sum_all_pairs([1, 5, 2, 4, 3], 6) == [(0, 1), (2, 3)]
assert four_sum_count([1, 2], [-2, -1], [-1, 2], [0, 2]) == 2


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

def difference_report(a, b, name_a="A", name_b="B"):
    print(f"Only in {name_a}: {sorted(a - b)}")
    print(f"Only in {name_b}: {sorted(b - a)}")
    print(f"In both:   {sorted(a & b)}")
    print(f"In exactly one: {sorted(a ^ b)}")

assert jaccard({1, 2, 3}, {2, 3, 4}) == 0.5 and jaccard(set(), set()) == 1.0
assert common_words("The cat sat", "the dog sat down") == {"the", "sat"}
difference_report({1, 2, 3, 4}, {3, 4, 5})
print("all asserts passed")
```

Output:

```
fib(20): hits 18 misses 21
Only in A: [1, 2]
Only in B: [5]
In both:   [3, 4]
In exactly one: [1, 2, 5]
all asserts passed
```

**B4.** Misses = 21 = one per distinct `n` from 0 to 20; every later request for the same `n` is a hit (18).
Lab 4's naive `fib(20)` made 21,891 calls; the cached version makes 39.

**Marking.** B1 3 each. B2: 3/3/4/5/3 — `longest_consecutive` must start runs only at run starts (otherwise
Θ(n²)). B3: 4/6/6 — `two_sum_all_pairs([3, 3, 3], 6)` must give all three pairs. B4: 6 code, 4 explanation.
B5: 2/2/4. Missing cost statement or fewer than two asserts: −1 per function (max −5).

---

*CS 101 · Week 8 · Problem Set 8 · Due Friday 27 November 2026, 17:00 · © CSE Department*

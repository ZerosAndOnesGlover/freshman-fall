# CS 101 — Problem Set 8
## Hash Tables, Dictionaries, and Sets

**Released:** Friday, Week 8
**Due:** Friday, Week 9 at 11:59 PM
**Submission:** Upload `ps8.py` and `PS 8 Hash Tables and Dictionaries.md`
**Weight:** Part of the 30% Problem Sets grade

**Note:** Project 1 is also due Friday of Week 9. Plan your time across both this week — do not leave either to the last two days.

---

## Overview

This problem set covers:
- Hash table internals: chaining, open addressing, load factor, resizing
- The `__hash__`/`__eq__` contract for custom classes
- Practical dict/set patterns: counting, grouping, membership, complement search
- Refactoring earlier algorithms (Weeks 2–7) to use dict/set for dramatic complexity improvements
- Choosing between list, set, and dict with justified reasoning

---

## Part A: Written Questions (`PS 8 Hash Tables and Dictionaries.md`)

### A1: Hash Table Mechanics (8 points)

**(a)** Explain, precisely, why `hash([1, 2, 3])` raises a `TypeError`, while `hash((1, 2, 3))` succeeds. Your answer must reference mutability and the reason dictionaries require stable hash values.

**(b)** A hash table has 10 buckets and currently stores 8 elements using chaining. What is its load factor? Would this trigger a resize under the 0.75 threshold used in lecture?

**(c)** Explain the purpose of a "tombstone" marker in open-addressing hash tables. Construct a small concrete example (with specific keys and a specific table size) showing what goes wrong if you use a plain `None`/empty marker instead of a tombstone after a deletion.

**(d)** Why does Python's open-addressing implementation use a LOWER maximum load factor threshold than a typical chaining implementation? Reference the performance curves you measured in Lab 8.

### A2: The `__hash__`/`__eq__` Contract (6 points)

**(a)** State the contract precisely: what MUST be true about `hash(a)` and `hash(b)` if `a == b`? Is the converse required?

**(b)** Consider this class:
```python
class BadCache:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, other):
        return self.key == other.key   # equality based on key ONLY

    def __hash__(self):
        return hash((self.key, self.value))   # hash based on key AND value!
```
Explain precisely why this class VIOLATES the hash/eq contract. Construct two specific instances `a` and `b` where `a == b` is True but `hash(a) == hash(b)` is False, and explain what bug this could cause if instances of `BadCache` were used as dictionary keys or set members.

### A3: Complexity Analysis (6 points)

For each of the following, state the time complexity (in terms of n = size of input) and briefly justify:

**(a)** Checking if two lists of the same length contain the exact same set of elements (ignoring order and duplicates), using a set-based approach.

**(b)** Finding all duplicate values in a list of n elements, using a dict to count occurrences.

**(c)** Given two lists A (size n) and B (size m), finding all elements present in BOTH lists, using a set built from the smaller list.

### A4: Design Justification (5 points)

For each scenario, state whether you would use a `list`, `set`, or `dict`, and justify in 1-2 sentences:

**(a)** Storing a shopping cart where items can be added multiple times (e.g., "2x apples") and the order items were added matters for display.

**(b)** Storing the set of all usernames currently logged into a system, where you frequently need to check "is user X logged in?"

**(c)** Storing a translation table mapping English words to their French equivalents.

**(d)** Storing the roll call of students in a class in the order they appear on the official roster (fixed, never reordered, occasionally checked for containment).

---

## Part B: Python Implementation (`ps8.py`)

### B1: Custom Hash Table Extensions (12 points)

Extend the `ChainedHashTable` from lab with these additional methods:

**(a)** `keys()` — return a list of all keys currently stored, in no particular guaranteed order. O(n).

**(b)** `values()` — return a list of all values currently stored. O(n).

**(c)** `items()` — return a list of (key, value) tuples for all entries. O(n).

**(d)** `update(other_dict)` — insert all key-value pairs from a Python `dict` into this hash table (overwriting existing keys). O(k) where k = len(other_dict), assuming O(1) average per insertion.

**(e)** `__contains__(self, key)` — implement so that `key in my_hash_table` works using Python's `in` operator directly (this is a "dunder" method — research how Python's `in` operator invokes `__contains__` if you haven't seen this yet).

---

### B2: Refactoring Earlier Algorithms With Dict/Set (16 points)

For each, implement the O(n) or O(n log n) version using dict/set, AND keep (or reference) the original slower version for comparison. State the complexity improvement in a comment.

**(a)** `has_duplicate_pair_fast(lst)` — from Week 2/PS2's number theory section spirit: O(n) using a set (compare to an O(n²) nested-loop version).

**(b)** `word_frequency_fast(text)` — from Week 3's lab: O(n) using a dict (the original was explicitly O(n²), forbidding dicts at the time).

**(c)** `is_anagram_fast(s1, s2)` — from Week 2's challenge: O(n) using frequency dicts (the original explicitly forbade dicts/sets/sorting).

**(d)** `find_missing_number(nums)` — given a list containing n distinct numbers from 0 to n (one number is missing), find the missing number in O(n) using a set. (Bonus insight to mention in a comment: this can also be solved in O(n) with NO extra space using the sum formula `n*(n+1)//2` — mention this alternative even though you should implement the set-based version as the primary solution.)

**(e)** `longest_consecutive_sequence(nums)` — given an unsorted list of integers, find the length of the longest run of consecutive integers (they don't need to be consecutive IN THE LIST, just consecutive in VALUE). O(n) using a set.
- `longest_consecutive_sequence([100, 4, 200, 1, 3, 2])` → `4` (the sequence 1,2,3,4)

**(f)** `group_by_first_letter(words)` — group a list of words by their first letter, using `defaultdict`. Return a regular dict (convert from defaultdict before returning) mapping letter → list of words, preserving first-appearance order within each group.

---

### B3: Two-Sum Family of Problems (12 points)

**(a)** `two_sum(nums, target)` — from lecture; return indices of two numbers summing to target, O(n).

**(b)** `three_sum_zero(nums)` — return ALL unique triplets (as sorted tuples) that sum to zero. This is harder than two-sum; a common approach: sort first (O(n log n)), then for each element, use two-pointer technique (like PS6's `all_triples_sum_to_zero_fast`) OR use a set-based approach for the inner search. Handle duplicate triplets correctly (return each unique triplet only once).
- `three_sum_zero([-1, 0, 1, 2, -1, -4])` → `[(-1, -1, 2), (-1, 0, 1)]` (order of triplets/tuples may vary, but each unique triplet appears exactly once)

**(c)** `two_sum_all_pairs(nums, target)` — return ALL pairs of INDICES (not just the first found) that sum to target. Handle the case where the same value appears multiple times correctly (e.g., `nums=[3,3,3], target=6` should find multiple valid index pairs).

**(d)** `four_sum_count(A, B, C, D)` — given four lists of equal length n, count how many tuples `(i,j,k,l)` exist such that `A[i]+B[j]+C[k]+D[l] == 0`. Naive approach is O(n⁴); using a dict to precompute all pairwise sums from A and B first, you can achieve O(n²).
- This is a genuinely important pattern: precompute a lookup table of partial sums, then probe it, rather than generating all n⁴ combinations directly.

---

### B4: A Simple LRU-Style Cache (10 points)

Implement a simplified caching decorator using a dict, without `functools.lru_cache`.

**(a)** `memoize(func)` — a decorator (you saw the concept in Week 3/8 lecture) that wraps `func`, caching results in a dict keyed by the arguments. Support only functions with a SINGLE hashable positional argument for simplicity.
```python
@memoize
def slow_square(x):
    import time; time.sleep(0.01)
    return x * x
```

**(b)** `memoize_with_stats(func)` — like `memoize`, but the wrapped function also exposes `.cache_hits` and `.cache_misses` counters (accessible as attributes on the wrapped function) so you can verify the cache is actually being used.

**(c)** Demonstrate `memoize_with_stats` on a recursive Fibonacci function, and print the resulting hit/miss counts for `fib(20)`. Verify the number of misses equals the number of UNIQUE subproblems (should be 21: fib(0) through fib(20)).

---

### B5: Set Theory Applications (10 points)

**(a)** `jaccard_similarity(set_a, set_b)` — return the Jaccard similarity coefficient: `|A ∩ B| / |A ∪ B|`. This is a standard measure of set similarity used in recommendation systems, plagiarism detection, and more.
- `jaccard_similarity({1,2,3}, {2,3,4})` → `0.5` (intersection={2,3}, size 2; union={1,2,3,4}, size 4)

**(b)** `find_common_words(text1, text2)` — return the set of words appearing in BOTH texts (case-insensitive), using set intersection.

**(c)** `symmetric_difference_report(set_a, set_b, name_a="A", name_b="B")` — print a formatted report showing: elements only in A, elements only in B, elements in both. Use set operations, not manual loops.

**(d)** `are_disjoint(set_a, set_b)` — return True if the sets share no elements. Do this in O(min(len(a), len(b))) — do NOT compute the full intersection if you can avoid it (hint: Python's `set.isdisjoint()` already does this efficiently — you may use it here, but explain in a comment why it can be faster than computing `len(a & b) == 0`).

---

## Grading Rubric

| Problem | Points | Key Criteria |
|---------|--------|--------------|
| A1 Hash table mechanics | 8 | All 4 parts correct and precise |
| A2 Hash/eq contract | 6 | Correct contract statement; valid violating example |
| A3 Complexity analysis | 6 | Correct complexity + justification for all 3 |
| A4 Design justification | 5 | Correct choice + reasoning for all 4 |
| B1 Hash table extensions | 12 | All 5 methods correct |
| B2 Refactoring | 16 | All 6 functions correct with complexity comments |
| B3 Two-sum family | 12 | All 4 correct, including duplicate handling in (b)/(c) |
| B4 Memoization | 10 | Both decorators work; stats correctly tracked |
| B5 Set theory | 10 | All 4 correct, using genuine set operations |
| **Total** | **85** | |
| Style/complexity rigor | up to 5 bonus | |

---

## Part C: Challenge Problems (Ungraded)

**C1: Consistent Hashing**
Research "consistent hashing" — a technique used in distributed systems (databases, CDNs) to minimize data movement when the number of servers (buckets) changes. Explain, in 300 words, how it differs from the simple `hash(key) % num_buckets` approach used in this week's lectures, and why that difference matters at scale.

**C2: Bloom Filters**
Research Bloom filters — a probabilistic data structure that can tell you "definitely not in the set" or "probably in the set" using far less memory than a real set, at the cost of allowing false positives (but never false negatives). Implement a simple Bloom filter using multiple hash functions and a bit array, and empirically measure its false-positive rate at various fill levels.

**C3: Perfect Hashing**
Research "perfect hash functions" — for a FIXED, known set of keys, it's possible to construct a hash function with ZERO collisions. Explain why this doesn't contradict the pigeonhole principle from Thursday's lecture (hint: the pigeonhole argument applies when the function must work for ANY possible key, not a fixed known set).

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading Rubric above.
> No errata found — all stated example values verified, including the 21-miss prediction in B4(c).

---

### Part A — Written (25 points)

**A1 Hash Table Mechanics (8 pts).** 2 pts each.

**(a)** `hash([1,2,3])` raises `TypeError` because `list` is **mutable** and deliberately defines `__hash__ = None`. A hash table places an entry in a bucket determined by `hash(key)` *at insertion time*. If a key's contents could change afterwards, its hash would change, and the entry would sit in a bucket that no longer matches — permanently unreachable, since lookup probes the *new* hash's bucket. Tuples are immutable, so their hash is stable for life, making them safe keys. (A tuple containing a list is still unhashable — hashability is recursive.)

**(b)** Load factor `= 8/10 = **0.8**`. Since `0.8 > 0.75`, this **would** trigger a resize.

**(c)** In open addressing, lookup probes forward from the home bucket and stops at the first genuinely empty slot. Deleting by writing plain `None` breaks that chain. Concrete example, table size 5, linear probing, keys hashing as `A→1`, `B→1`, `C→1`:

- Insert A → slot 1. Insert B → slot 1 taken, probe → slot 2. Insert C → probe → slot 3.
- Delete B by writing `None` into slot 2.
- Look up C: probe slot 1 (A, not a match) → slot 2 is `None` → **conclude C is absent and stop**. But C is sitting in slot 3.

A **tombstone** marks slot 2 as "deleted, but the probe chain continues here", so lookup keeps going and finds C. Tombstones count as occupied for probing but as free for insertion.

**(d)** Open addressing degrades much more sharply near a full table: with all entries in the array itself, clustering makes the expected probe count blow up roughly as `1/(1−α)`, diverging as `α → 1`. Chaining degrades gracefully — at `α = 2` the average chain is just 2 links, still O(1) expected. So open addressing must resize earlier (Python uses ≈ 2/3) while chaining tolerates ≈ 0.75–1.0+.

**A2 The `__hash__`/`__eq__` Contract (6 pts).**

**(a)** **If `a == b` then `hash(a) == hash(b)`.** The converse is **not** required — unequal objects may share a hash (that is a collision, which hash tables handle). Equal objects with different hashes is the fatal case, because the table would look in the wrong bucket.

**(b)** `BadCache` equates on `key` alone but hashes on `(key, value)`, so two objects can be equal while hashing differently. Verified:

```python
a = BadCache("x", 1)
b = BadCache("x", 2)
a == b                 # True
hash(a) == hash(b)     # False   <- contract broken
```

Consequences, both reproduced: `d = {a: "first"}` then `d[b]` raises **`KeyError`** even though `b == a` — the lookup hashes to a different bucket. And `len({a, b}) == 2`: the set stores two elements that compare equal, so `in`-tests become unreliable and duplicates silently accumulate. The fix is to hash on exactly the fields used for equality: `def __hash__(self): return hash(self.key)`.

*Grading: 2 pts (a) — must state the converse is not required. 4 pts (b) — 2 for identifying the mismatch of fields, 2 for concrete instances **plus** a named consequence (KeyError or duplicate set members).*

**A3 Complexity (6 pts).** 2 pts each.
- **(a) O(n)** — building a set from each list is O(n), and set equality compares sizes then membership, O(n) expected. (The naive nested-loop comparison would be O(n²).)
- **(b) O(n)** — one pass to count into a dict (O(1) expected per insert), one pass over the dict to collect counts > 1.
- **(c) O(n + m)** — build a set from the smaller list, then scan the larger testing membership at O(1) expected each. Building from the *smaller* list minimises auxiliary space; the time bound is the same either way.

**A4 Design Justification (5 pts).**
- **(a) `list`** — duplicates are meaningful ("2× apples") and insertion order matters for display; sets and dict keys both discard duplicates.
- **(b) `set`** — membership testing is the only operation, and it is O(1) expected; no values needed, no order needed.
- **(c) `dict`** — an explicit key→value mapping (English → French) is exactly what a dict models.
- **(d) `list`** — a fixed ordered roster. *(Accept a well-argued `dict`/`set` **companion** for fast containment, but the primary structure must preserve roster order; a bare `set` loses it and earns 0.)*

---

### Part B — Coding

**B1 Hash Table Extensions (12 pts).** ~2.4 pts each.
*(e) `__contains__` must return a **bool** and be reachable via the `in` operator. Verify with `key in table`, not just `table.__contains__(key)`. Note for graders: if a class defines `__iter__` but not `__contains__`, `in` silently falls back to linear iteration — correct results, wrong complexity. Probe whether `__contains__` is actually defined.*
*(d) `update` must **overwrite** existing keys, not skip or duplicate them.*

**B2 Refactoring With Dict/Set (16 pts).**

```python
def longest_consecutive_sequence(nums):          # O(n) — NOT O(n log n)
    s, best = set(nums), 0
    for x in s:
        if x - 1 not in s:                       # only expand from a run's start
            y = x
            while y + 1 in s: y += 1
            best = max(best, y - x + 1)
    return best
```

Verified: `[100,4,200,1,3,2]` → **4**; `[]` → 0; `[1,1,1]` → 1.

*(e) is the discriminating item. The `if x - 1 not in s` guard is what makes it O(n): without it, every element re-walks its whole run, giving O(n²) on input like `[1..n]`. A submission that sorts first is O(n log n) and earns partial credit only — the spec asks for O(n) using a set.*
*(d) Both approaches deserve mention: the set version is O(n) time / O(n) space; the sum formula `n(n+1)//2 − sum(nums)` is O(n) time / **O(1)** space. The comment is required by the spec.*
*(f) must return a plain `dict`, not the `defaultdict` — test `type(result) is dict`. Order within each group must follow first appearance.*

**B3 Two-Sum Family (12 pts).** 3 pts each. All verified.

```python
def three_sum_zero(nums):                        # O(n^2) after sorting
    a, out = sorted(nums), set()
    for i in range(len(a) - 2):
        if i > 0 and a[i] == a[i-1]: continue    # skip duplicate anchors
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            t = a[i] + a[lo] + a[hi]
            if t == 0:  out.add((a[i], a[lo], a[hi])); lo += 1; hi -= 1
            elif t < 0: lo += 1
            else:       hi -= 1
    return sorted(out)

def four_sum_count(A, B, C, D):                  # O(n^2), not O(n^4)
    ab = defaultdict(int)
    for x in A:
        for y in B: ab[x + y] += 1               # precompute all A+B sums
    return sum(ab[-(z + w)] for z in C for w in D)
```

Verified: `three_sum_zero([-1,0,1,2,-1,-4])` → `[(-1,-1,2), (-1,0,1)]`, matching the spec exactly. `two_sum_all_pairs([3,3,3], 6)` → `[(0,1), (0,2), (1,2)]` — all three index pairs. `four_sum_count([1,2],[-2,-1],[-1,2],[0,2])` → `2`.

*(b) Duplicate handling is the whole difficulty. Test specifically with the spec's input, which contains two `-1`s: a solution without the `a[i] == a[i-1]` skip (or without a de-duplicating set) returns `(-1,0,1)` twice.*
*(c) Must return **index** pairs, not value pairs, and must find all three for `[3,3,3]` — a dict-of-value→single-index approach finds only one and loses 2 of 3 points.*
*(d) A submission that nests four loops is correct but O(n⁴) — the point of the exercise is the pairwise-sum lookup table. Award 1 of 3.*

**B4 Memoization Cache (10 pts).**

```python
def memoize_with_stats(func):
    cache = {}
    def wrapper(x):
        if x in cache:
            wrapper.cache_hits += 1
            return cache[x]
        wrapper.cache_misses += 1
        cache[x] = func(x)
        return cache[x]
    wrapper.cache_hits = wrapper.cache_misses = 0
    return wrapper
```

Verified on memoized Fibonacci: `fib(20) = 6765`, **misses = 21**, hits = 18. The 21 misses are exactly `fib(0)…fib(20)` — one per unique subproblem, confirming the spec's stated expectation.

*The counters must be attributes **on the returned wrapper** (as above), not module-level globals — the spec requires `.cache_hits` / `.cache_misses` be reachable from the decorated function. A common error is incrementing before the cache check, which makes every call a "miss".*

**B5 Set Theory (10 pts).** 2.5 pts each. Verified: `jaccard_similarity({1,2,3},{2,3,4})` → `0.5`.

*(a) Guard the empty-union case — `jaccard(set(), set())` is 0/0. Convention: define it as 1.0 (identical sets) or raise; either is acceptable if documented. An unguarded `ZeroDivisionError` loses 1.*
*(d) `isdisjoint` can short-circuit on the **first** shared element and iterates the smaller set, so it is O(min(|a|,|b|)) and allocates nothing. `len(a & b) == 0` must materialise the entire intersection first — O(min) time but O(min) *space*, and no early exit. The comment explaining this is the graded part.*

---

*CS 101 · Week 8 · Problem Set 8 · Due Friday Week 9 · © CSE Department*

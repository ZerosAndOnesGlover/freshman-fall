# CS 101 · Lecture 25 (Week 8, Lecture 1)
## Hash Tables Fundamentals: The Idea Behind O(1) Lookup

**Week 8 · Wednesday**
*"A hash table doesn't search for your data — it computes where your data must be." — CS 101*

**Date:** Wednesday 18 November 2026 · 09:00–09:50 · Week 8

---

## 0. The Question That Ends the Course's First Data Structure Story

Since Week 1, you've used `x in lst` without asking what it costs. Week 7 gave you the honest answer: O(n) for both Python lists and linked lists — every membership test, every lookup, requires scanning.

Today we answer the question posed at the end of Week 7: **what would it take to check membership in O(1) instead of O(n)?** The answer — hash tables — underlies Python's `dict` and `set`, and is arguably the single most practically important data structure in all of computing.

---

## 1. The Core Insight: Compute the Location, Don't Search for It

Every structure you've built so far (arrays, linked lists) finds an element by **searching**: scanning forward until you find it, or reach the end. This is fundamentally O(n) because the position of any given value is not knowable in advance.

**A hash table's radical idea:** what if you could **compute** where an element belongs, directly from its value, without searching at all?

```
Array-based lookup:  "Is 'apple' in this collection?"
                     → scan index 0, 1, 2, 3, ... until found or exhausted. O(n).

Hash-table lookup:   "Is 'apple' in this collection?"
                     → compute hash('apple') → get a number, e.g. 738291
                     → compute 738291 % table_size → get an index, e.g. 5
                     → look ONLY at index 5. O(1) — if you're lucky (more on this Thursday).
```

This is the entire idea. Everything else in hash table design — collision resolution, load factors, resizing — exists to make that "if you're lucky" clause true almost all of the time.

---

## 2. What Is a Hash Function?

A **hash function** takes an object and returns an integer (called the **hash value** or **hash code**), deterministically:

```python
hash("apple")     # some large integer, e.g. -3223759340027881617
hash("apple")     # same call again — SAME integer (deterministic within a run)
hash(42)          # 42  (small ints hash to themselves)
hash(3.14)        # some integer derived from the float's bit representation
hash((1, 2, 3))   # tuples are hashable if all their elements are
hash([1, 2, 3])   # TypeError! Lists are NOT hashable (they're mutable)
```

**A well-designed hash function has three properties:**
1. **Deterministic:** the same input always produces the same output (within one program run)
2. **Fast to compute:** O(1) relative to the object's size, ideally
3. **Uniform distribution:** different inputs should be spread evenly across possible outputs, minimizing the chance that two different inputs land in the same "bucket"

### Why Are Lists Unhashable?

```python
>>> hash([1, 2, 3])
TypeError: unhashable type: 'list'
```

Recall from Week 7: lists are **mutable**. If a list could be hashed and used as a dictionary key, and then you mutated it (`lst.append(4)`), its hash value would need to change to reflect the new contents — but the dictionary has already placed it in a bucket based on the OLD hash. The dictionary's internal structure would become corrupted; you could search for the object and fail to find it, even though it's "in there."

**The rule:** an object is hashable if and only if it is immutable (or, more precisely, if its hash value never changes during its lifetime). This is why `tuple` is hashable but `list` is not; why `frozenset` is hashable but `set` is not; why strings, integers, and floats are all hashable.

```python
>>> hash({1, 2, 3})       # sets are also mutable — unhashable
TypeError: unhashable type: 'set'
>>> hash(frozenset({1,2,3}))  # frozenset is the immutable sibling of set
-7699079583225461316  # works!
```

---

## 3. The Bucket Array — A Hash Table's Underlying Structure

A hash table maintains an array of **buckets** (slots). To insert or look up a key:

```
1. Compute hash(key)
2. Compute index = hash(key) % number_of_buckets
3. Go directly to buckets[index]
```

```python
# A minimal illustration (not yet handling collisions — that's Thursday):

class TinyHashTable:
    def __init__(self, size=8):
        self.size = size
        self.buckets = [None] * size

    def _index(self, key):
        return hash(key) % self.size

    def put(self, key, value):
        idx = self._index(key)
        self.buckets[idx] = (key, value)   # simplistic — overwrites on collision!

    def get(self, key):
        idx = self._index(key)
        if self.buckets[idx] is None:
            raise KeyError(key)
        stored_key, stored_value = self.buckets[idx]
        if stored_key != key:
            raise KeyError(key)   # WRONG key at this index — a collision occurred!
        return stored_value


t = TinyHashTable()
t.put("apple", 1)
t.put("banana", 2)
print(t.get("apple"))    # 1
print(t.get("banana"))   # 2
```

This toy version has a serious bug waiting to happen: if two different keys hash to the same index (a **collision**), the second `put()` silently overwrites the first. Thursday's lecture builds the real solution.

---

## 4. Python's `dict` — What You've Actually Been Using

Every time you've written `d = {}`, `d[key] = value`, or `key in d`, you've been using a highly optimized hash table.

```python
d = {"apple": 1, "banana": 2, "cherry": 3}

d["apple"]           # O(1) average — direct hash-based lookup
d["date"] = 4         # O(1) average — insert
"apple" in d          # O(1) average — membership test (THIS is what Week 7 asked about!)
del d["banana"]       # O(1) average — removal
len(d)                 # O(1) — size tracked as metadata, like list's len()
```

**Compare to Week 7's list-based membership testing:**

```python
lst = ["apple", "banana", "cherry"]
"apple" in lst        # O(n) — must scan every element in the worst case

d = {"apple": 1, "banana": 1, "cherry": 1}
"apple" in d           # O(1) average — hash directly to the location
```

This single difference — O(n) vs O(1) average — is why converting a list to a set/dict before doing repeated membership tests is one of the most impactful, common optimizations in real Python code.

```python
import time

large_list = list(range(1_000_000))
large_set  = set(large_list)

target = 999_999   # worst case: last element (or absent)

t0 = time.perf_counter()
target in large_list
t1 = time.perf_counter()
print(f"List membership: {(t1-t0)*1000:.3f} ms")

t0 = time.perf_counter()
target in large_set
t1 = time.perf_counter()
print(f"Set membership:  {(t1-t0)*1000:.6f} ms")
# The set version will be orders of magnitude faster.
```

---

## 5. Python's `set` — A Dict With Only Keys

A `set` is, internally, implemented using the exact same hash table machinery as `dict` — it just doesn't store an associated value, only the keys themselves.

```python
s = {"apple", "banana", "cherry"}

"apple" in s          # O(1) average
s.add("date")          # O(1) average
s.remove("banana")     # O(1) average
len(s)                  # O(1)
```

### Set Operations — Mathematical Set Theory, Directly in Python

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b     # union:        {1, 2, 3, 4, 5, 6}
a & b     # intersection: {3, 4}
a - b     # difference:   {1, 2}     (in a but not in b)
a ^ b     # symmetric diff: {1, 2, 5, 6}   (in exactly one of a, b)

a.issubset(b)        # False
{1, 2}.issubset(a)   # True
a.issuperset({1, 2}) # True
```

Each of these operations runs in O(len(a) + len(b)) — proportional to the total size of the inputs, NOT the product (which would be the case if you naively checked every pair). This efficiency comes directly from O(1) average-case membership testing: checking "is this element of `a` also in `b`?" is O(1) per element, done once per element of `a`.

---

## 6. The Contract Between `__hash__` and `__eq__`

For custom objects to work correctly as dictionary keys or set members, Python requires a strict contract:

**If `a == b`, then `hash(a) == hash(b)` MUST also be true.**

(The reverse is not required — different objects CAN have the same hash, which is a **collision**, covered Thursday. But equal objects must never have different hashes.)

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))    # combine x and y into one hash


p1 = Point(1, 2)
p2 = Point(1, 2)

print(p1 == p2)              # True — same coordinates
print(hash(p1) == hash(p2))  # True — REQUIRED by the contract, and satisfied here

points = {p1, p2}
print(len(points))            # 1 — because p1 and p2 are treated as "the same" in a set
```

**What happens if you violate the contract (define `__eq__` but not `__hash__`)?**

```python
class BrokenPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, BrokenPoint) and self.x == other.x and self.y == other.y
    # No __hash__ defined!

p1 = BrokenPoint(1, 2)
print(p1 in {p1})   # True — using the SAME object works by identity fallback...

p2 = BrokenPoint(1, 2)
print(p1 == p2)         # True (equal by value)
print(p1 in {p2})       # ??? — UNRELIABLE! Depends on Python's default __hash__ behavior
```

**The rule in Python:** if you define `__eq__` without defining `__hash__`, Python automatically makes your class **unhashable** (sets `__hash__` to `None`) — this is a safety mechanism to prevent exactly the corruption scenario described above. You must explicitly define `__hash__` if you want your custom `__eq__`-having class to work in sets/dicts.

---

## 7. Common Errors and Misconceptions

**Error 1: Assuming dict/set lookups are ALWAYS O(1), no exceptions**
Dict/set operations are O(1) **average case**. The **worst case** is O(n) (Thursday explains exactly when this happens — pathological hash collisions). For virtually all practical purposes with good hash functions (which Python's built-in types have), average case is what you experience.

**Error 2: Using a mutable object as a key/set-member**
```python
d = {[1,2]: "value"}   # TypeError: unhashable type: 'list'
d = {(1,2): "value"}   # Fine — tuples are hashable (if their elements are)
```

**Error 3: Assuming dictionaries preserve NO order**
Since Python 3.7, dictionaries preserve **insertion order** as a language guarantee (this was an implementation detail in 3.6, made official in 3.7). This does not mean dicts are "sorted" — it means iterating a dict yields keys in the order they were first inserted.

```python
d = {}
d["z"] = 1
d["a"] = 2
d["m"] = 3
print(list(d.keys()))   # ['z', 'a', 'm'] — insertion order, NOT alphabetical
```

**Error 4: Forgetting that `dict.get()` avoids `KeyError`**
```python
d = {"a": 1}
d["b"]           # KeyError!
d.get("b")        # None — no error
d.get("b", 0)     # 0 — a default value if the key is missing
```

---

## 8. A First Application: Word Frequency Counting, Properly

Recall Week 3's lab, where `word_frequency` was implemented using **nested loops with no dictionaries** — an O(n²) approach (justified pedagogically at the time, since dicts hadn't been covered). Now, the correct approach:

```python
def word_frequency(text):
    """
    Return a dict mapping each word to its count.
    O(n) time — a dramatic improvement over the O(n²) nested-loop version.
    """
    words = text.lower().split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1   # O(1) average per word
    return counts


text = "the cat sat on the mat the cat ran"
print(word_frequency(text))
# {'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1, 'ran': 1}
```

**Complexity comparison:**
- Week 3's nested-loop version: O(n²) — for each word, scan all previous words to count occurrences
- This version: O(n) — one pass, O(1) average dict update per word

For a text with 100,000 words, that's the difference between roughly 10 billion operations and 100,000 operations — from potentially minutes to milliseconds.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Hash function | Deterministic mapping from object to integer; enables O(1) average lookup |
| Hashable | Object's hash never changes during its lifetime; requires immutability |
| `dict`/`set` | Python's built-in hash tables; O(1) average insert/lookup/delete |
| `hash`/`eq` contract | Equal objects MUST have equal hashes; violating this corrupts dict/set behavior |
| Insertion order | Python 3.7+ dicts preserve insertion order (a language guarantee) |
| `dict.get(key, default)` | Safe lookup without risking `KeyError` |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict the result and explain what it reveals about the hash contract.

```python
print(hash(1), hash(1.0), hash(True))
d = {1: 'int'}
d[1.0] = 'float'
d[True] = 'bool'
print(d)
print(hash(-1), hash(-2))
```

**2. (Explain.)** This class breaks when used in a set. Explain why, and give both correct fixes.

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)
```

**3. (Build.)** Write a hash function for strings that maps to a bucket index, and demonstrate why `sum(ord(c) for c in s) % size` is a poor choice.

**4. (Stretch.)** Python's `dict` preserves insertion order, guaranteed since 3.7, yet hash tables are conceptually unordered. Explain how CPython achieves this and what it gained.


### Answers

**1.** `1 1 1`, then `{1: 'bool'}`, then `-2 -2`.

**All three keys are the same key.** `1 == 1.0 == True` and their hashes agree, so the dict treats them as one entry: each assignment **overwrites the value but keeps the original key object**, which is why the result prints `1` rather than `True`. Python guarantees numeric types that compare equal hash equal, so that `d[1]` and `d[1.0]` cannot disagree.

This is the **hash contract**: *if `a == b` then `hash(a) == hash(b)`.* The converse need not hold — unequal objects may share a hash, which is a collision and is handled by the table.

`hash(-1) == hash(-2) == -2` is the curiosity. CPython's C-level hash function reserves `-1` as its **error sentinel**, so any object hashing to −1 is silently remapped to −2. It is a deliberate collision forced by the C API's convention of signalling failure with a return value, and it costs nothing — one extra collision in 2⁶⁴ possible hashes.

The practical warning: a dict keyed on mixed numeric types will silently merge entries you thought were distinct. If `1` and `True` must be different keys, they cannot both be dict keys.

**2.** It raises **`TypeError: unhashable type: 'Point'`**.

Defining `__eq__` sets `__hash__ = None` automatically. Python does this on purpose: the default `__hash__` is based on object identity, so two `Point`s that are now `==` would hash differently and land in different buckets — the object would be lost in the table, findable only by luck. Rather than let you build a silently broken set, Python makes the class unhashable and fails loudly.

**Fix 1 — make it hashable, consistently with `__eq__`:**

```python
    def __hash__(self):
        return hash((self.x, self.y))
```

Hash exactly the fields `__eq__` compares. This obliges you to treat those fields as **immutable** — mutating `x` after insertion changes the hash, and the object becomes unfindable in its own set.

**Fix 2 — make the whole class immutable and let Python do it:**

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float
```

`frozen=True` generates `__eq__` and `__hash__` together and blocks attribute assignment, so the mutation hazard is eliminated rather than merely documented. This is the better default for value objects.

**3.**

```python
def bucket(s, size):
    h = 5381
    for ch in s:
        h = (h * 33 + ord(ch)) & 0xFFFFFFFF   # djb2
    return h % size
```

The character-sum version fails on two counts.

**It ignores order.** `sum` is commutative, so every anagram collides: `"listen"`, `"silent"`, and `"enlist"` all land in the same bucket. For a dictionary of English words that is a large, systematically clustered set of collisions.

**Its range is far too narrow.** ASCII characters are ~97–122, so an 8-character lowercase word sums to somewhere between ~780 and ~980 — about 200 distinct values for the entire space of 8-letter words. With 1000 buckets, 800 of them are unreachable and the rest are heavily overloaded. Short strings cluster worse still.

djb2 fixes both by **multiplying by 33 before adding**, so each character's contribution is shifted into different bits by its position — order now matters, and one changed character cascades through the whole value. The multiplier being odd and coprime to the bucket count avoids systematic clustering.

Test any candidate empirically: hash a word list, count bucket occupancies, and compare against the uniform expectation. A good hash gives a roughly Poisson distribution; the character sum gives a visibly spiky one.

**4.** CPython splits the dict into **two arrays**. A dense `entries` array holds `(hash, key, value)` triples **in insertion order**, appended to as items are added. A sparse `indices` array — the actual hash table — holds small integers that are *positions into* `entries`, and it is what the hash is used to probe.

A lookup hashes the key, probes `indices` to get an index, and reads `entries[index]`. Iteration ignores the hash table entirely and simply walks `entries` front to back, which is why the order is insertion order.

The gain that motivated the design was **memory**, not ordering. Before this change (Raymond Hettinger's "compact dict", Python 3.6), the sparse table stored full 24-byte entries, so a table at 60% load wasted 40% of that space. Now the sparse array holds only indices — 1 byte each for small dicts, growing as needed — and the full entries live in a dense array with no waste. The result was **20–25% less memory per dict**, which matters enormously given that every Python object's attributes, every module namespace, and every keyword-argument call involves dicts.

Ordering fell out as a free side effect and was initially documented as an implementation detail; it was promoted to a language guarantee in 3.7 once it was clear every implementation would follow.

One cost: deletion leaves a tombstone in `entries`, so a dict that is heavily added-to and deleted-from accumulates dead slots until it is resized and compacted.



---

## Reading

- **Guttag, Ch. 5.4–5.5** — Dictionaries (if covered) or supplementary handout
- **Python docs — Data Model:** https://docs.python.org/3/reference/datamodel.html#object.__hash__ (the official `__hash__`/`__eq__` contract)

---

*CS 101 · Week 8 · Lecture 25 (Wed) · © CSE Department*

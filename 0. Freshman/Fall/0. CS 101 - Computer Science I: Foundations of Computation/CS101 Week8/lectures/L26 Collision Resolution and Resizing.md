# CS 101 · Lecture 26 (Week 8, Lecture 2)
## Collision Resolution, Load Factor, and Building a Hash Table From Scratch

**Week 8 · Thursday**
*"No hash function is perfect — collisions are not a bug, they are a mathematical certainty (pigeonhole principle). The engineering question is how gracefully you handle them." — CS 101*

---

## 0. The Problem Wednesday Left Unsolved

Wednesday's `TinyHashTable` silently overwrote data when two keys hashed to the same bucket index. This is a **collision** — and by the **pigeonhole principle** (which you may recognize from MATH 151), collisions are mathematically unavoidable once you have more possible keys than buckets. If you have 9 buckets and insert 10 keys, at least two must share a bucket — no hash function can prevent this.

Today: the two standard techniques for handling collisions correctly, plus the resizing strategy that keeps a hash table fast as it grows.

---

## 1. Collision Resolution Strategy 1: Chaining

**The idea:** instead of storing a single key-value pair per bucket, store a **list** (or linked list — connecting directly to Week 7!) of all key-value pairs that hash to that bucket.

```
Bucket 0: []
Bucket 1: [("apple", 1)]
Bucket 2: [("banana", 2), ("grape", 5)]   ← collision! both hash to bucket 2
Bucket 3: []
Bucket 4: [("cherry", 3)]
```

```python
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


# Tests:
ht = ChainedHashTable(initial_size=4)  # small size to force collisions quickly
ht.put("apple", 1)
ht.put("banana", 2)
ht.put("cherry", 3)
ht.put("date", 4)

print(ht.get("apple"))    # 1
print(ht.get("cherry"))   # 3
print(ht.contains("fig"))  # False
print(len(ht))              # 4

ht.put("apple", 100)   # update, not a new entry
print(ht.get("apple"))  # 100
print(len(ht))           # still 4
```

**Complexity with chaining:**
- **Average case:** O(1) — if collisions are rare (good hash function, reasonable load factor), each chain has approximately 0 or 1 elements
- **Worst case:** O(n) — if ALL keys hash to the same bucket (a pathologically bad hash function, or an adversarial attack — see the security note below), the chain degenerates into a single list you must scan entirely

---

## 2. Collision Resolution Strategy 2: Open Addressing (Linear Probing)

**The idea:** instead of storing a list at each bucket, store AT MOST one key-value pair per bucket. On a collision, **probe** (search) for the next available slot according to a fixed rule.

**Linear probing:** if bucket `i` is occupied, try `i+1`, then `i+2`, wrapping around, until an empty slot is found.

```python
class OpenAddressingHashTable:
    """
    A hash table using linear probing for collision resolution.
    Each bucket holds at most one (key, value) pair, or is empty.
    """

    _EMPTY = object()     # sentinel for "never used"
    _DELETED = object()   # sentinel for "used, then removed" (tombstone)

    def __init__(self, initial_size=8):
        self._size = initial_size
        self._keys = [self._EMPTY] * self._size
        self._values = [None] * self._size
        self._count = 0

    def _index(self, key):
        return hash(key) % self._size

    def put(self, key, value):
        idx = self._index(key)
        start_idx = idx

        while self._keys[idx] is not self._EMPTY and self._keys[idx] is not self._DELETED:
            if self._keys[idx] == key:
                self._values[idx] = value    # update existing
                return
            idx = (idx + 1) % self._size     # linear probe: try next slot
            if idx == start_idx:
                raise Exception("Hash table is full!")

        self._keys[idx] = key
        self._values[idx] = value
        self._count += 1

    def get(self, key):
        idx = self._index(key)
        start_idx = idx

        while self._keys[idx] is not self._EMPTY:
            if self._keys[idx] is not self._DELETED and self._keys[idx] == key:
                return self._values[idx]
            idx = (idx + 1) % self._size
            if idx == start_idx:
                break

        raise KeyError(key)

    def remove(self, key):
        idx = self._index(key)
        start_idx = idx

        while self._keys[idx] is not self._EMPTY:
            if self._keys[idx] is not self._DELETED and self._keys[idx] == key:
                self._keys[idx] = self._DELETED   # tombstone, NOT _EMPTY!
                self._count -= 1
                return
            idx = (idx + 1) % self._size
            if idx == start_idx:
                break

        raise KeyError(key)

    def __len__(self):
        return self._count


# Tests:
oht = OpenAddressingHashTable(initial_size=8)
oht.put("apple", 1)
oht.put("banana", 2)
oht.put("cherry", 3)
print(oht.get("apple"))    # 1
print(oht.get("banana"))   # 2
oht.remove("banana")
print(len(oht))             # 2
try:
    oht.get("banana")
except KeyError:
    print("banana correctly removed")
```

### Why Tombstones (`_DELETED`) Instead of Just `_EMPTY`?

This is a subtle but critical bug source. Consider: `apple` and `grape` both hash to index 2. `apple` is inserted first (at index 2), then `grape` collides and probes to index 3.

If you later `remove("apple")` and simply mark index 2 as `_EMPTY` (not `_DELETED`), then searching for `grape` later would incorrectly stop at index 2 (seeing it's "empty") and never continue probing to index 3 — even though `grape` is still there! **The tombstone marker preserves the "probe chain"** so that searches continue past deleted slots, only stopping at genuinely never-used (`_EMPTY`) slots.

---

## 3. Load Factor — The Critical Health Metric

**Load factor** = (number of elements stored) / (number of buckets)

```
load_factor = count / size
```

- Load factor near 0: mostly empty table, few collisions, but wasted memory
- Load factor near 1 (chaining) or approaching 1 (open addressing): table is nearly full, collisions become frequent, performance degrades toward O(n)

**Why does high load factor hurt performance?**
- **Chaining:** average chain length = load factor. At load factor 1.0, you expect ~1 comparison per lookup on average (fine). At load factor 10 (10x more elements than buckets), you expect ~10 comparisons on average — 10x slower.
- **Open addressing:** performance degrades even faster as load factor approaches 1.0, because probe sequences get dramatically longer when the table is nearly full (there are few empty slots left to find).

**Python's CPython implementation** keeps dict/set load factor below roughly 2/3 (0.667) by automatically resizing whenever this threshold would be exceeded — this is why Python's dict/set maintain their O(1) average-case guarantee even as they grow arbitrarily large.

---

## 4. Resizing (Rehashing) — Keeping Load Factor Bounded

When load factor exceeds a threshold, the hash table **resizes**: allocate a larger bucket array (typically double or more), then **re-insert every existing element** (because `hash(key) % new_size` gives a DIFFERENT index than `hash(key) % old_size` — you cannot simply copy the old array).

```python
class ResizingChainedHashTable:
    """
    ChainedHashTable that automatically resizes when load factor exceeds 0.75.
    """

    def __init__(self, initial_size=8):
        self._size = initial_size
        self._buckets = [[] for _ in range(self._size)]
        self._count = 0
        self._max_load_factor = 0.75

    def _index(self, key, size=None):
        size = size if size is not None else self._size
        return hash(key) % size

    def _resize(self):
        """Double the bucket array size and re-insert every element. O(n)."""
        old_buckets = self._buckets
        self._size *= 2
        self._buckets = [[] for _ in range(self._size)]

        for chain in old_buckets:
            for key, value in chain:
                idx = self._index(key)          # recompute with NEW size!
                self._buckets[idx].append((key, value))

    def put(self, key, value):
        idx = self._index(key)
        chain = self._buckets[idx]

        for i, (existing_key, existing_value) in enumerate(chain):
            if existing_key == key:
                chain[i] = (key, value)
                return

        chain.append((key, value))
        self._count += 1

        if self._count / self._size > self._max_load_factor:
            self._resize()

    def get(self, key):
        idx = self._index(key)
        for existing_key, existing_value in self._buckets[idx]:
            if existing_key == key:
                return existing_value
        raise KeyError(key)

    def __len__(self):
        return self._count


# Demonstrate resizing in action:
ht = ResizingChainedHashTable(initial_size=4)
print(f"Initial size: {ht._size}")

for i in range(20):
    ht.put(f"key{i}", i)
    if ht._size != 4 and i < 5:   # print only the first resize event
        print(f"After inserting key{i}: resized to {ht._size} buckets")
```

### Amortized Analysis of Resizing (Connecting Back to Week 6!)

This is **exactly** the amortized analysis you did in PS6 for dynamic arrays. Doubling the bucket array means resizes happen exponentially rarely relative to the number of insertions. The total cost of all resize operations across n insertions is O(n) (each element is "moved" O(1) times on average across all resizes), so:

**Insertion into a hash table is O(1) amortized** — not O(1) for every single insertion (occasional resizes cost O(n)), but O(1) on average across any sequence of insertions. This is the same mathematical structure as PS6's `DynamicArray.append()`.

---

## 5. Comparing Chaining vs. Open Addressing

| Property | Chaining | Open Addressing |
|----------|----------|-------------------|
| Memory overhead | Higher (each bucket is a list/linked structure) | Lower (fixed-size arrays, no extra pointers) |
| Performance at high load factor | Degrades gracefully (chains get longer) | Degrades sharply (probe sequences get very long) |
| Deletion | Simple (just remove from the chain) | Requires tombstones (subtler correctness) |
| Cache performance | Worse (chains scatter in memory, like linked lists) | Better (arrays are contiguous — better cache locality) |
| Used by | Java's `HashMap` (as of Java 8, with a twist: long chains become balanced trees!) | Python's `dict`/`set` (CPython uses open addressing internally) |

**Fun fact:** Python's actual `dict` implementation uses **open addressing** with a clever probing sequence (not simple linear probing — it uses a pseudo-random probing sequence derived from the hash value, to avoid clustering). The chaining version in this lecture is pedagogically simpler to understand first, but CPython's real implementation is closer to Section 2's approach.

---

## 6. A Security Note: Hash-Flooding Attacks

If an attacker knows your hash function, they can potentially craft many different keys that all hash to the **same bucket**, deliberately degrading your hash table from O(1) average to O(n) worst case for every operation — a denial-of-service attack.

This is a real, historically significant vulnerability. Python (since version 3.3) defends against it using **hash randomization**: string and bytes hashing incorporates a random seed, generated fresh each time the Python interpreter starts, so an attacker cannot predict `hash("some_string")` across different runs of your program.

```python
import sys
print(sys.flags.hash_randomization)   # 1 (enabled by default)

# This is why hash("apple") gives a DIFFERENT value each time you restart Python,
# but the SAME value throughout one single run.
```

This connects directly to CS 190 (Ethics & Security) material on denial-of-service attacks, and to CS 301 (cryptographic hash functions, which have much stronger guarantees than the fast, "good enough" hash functions used in dict/set).

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Collision | Two different keys hashing to the same bucket — mathematically unavoidable (pigeonhole) |
| Chaining | Each bucket holds a list of colliding entries; simple, graceful degradation |
| Open addressing | Each bucket holds ≤1 entry; collisions trigger probing to find another slot |
| Tombstones | Special "deleted" marker needed for correct open-addressing removal |
| Load factor | count / size; the critical health metric for hash table performance |
| Resizing | Doubling the bucket array and rehashing everything when load factor exceeds a threshold |
| Amortized O(1) | Same mathematical structure as dynamic array resizing (Week 6/PS6) |
| Hash randomization | Python's defense against hash-flooding denial-of-service attacks |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** A table with 8 buckets uses chaining and `hash(k) % 8`. Insert keys hashing to 5, 13, 21, 3, 11. Show the final table, give the load factor, and state the worst-case lookup cost.

**2. (Explain.)** Compare chaining and linear probing on: memory use, cache behaviour, deletion, and behaviour as the load factor approaches 1. Say which each is better at.

**3. (Build.)** Implement `_resize()` for a chaining hash table. Explain why entries must be rehashed rather than copied, and give the amortised cost of insertion.

**4. (Stretch.)** Explain the hash-flooding attack of §6: how it works, why it was a practical vulnerability in 2011, and what the fix was.


### Answers

**1.** 5 % 8 = 5, 13 % 8 = 5, 21 % 8 = 5, 3 % 8 = 3, 11 % 8 = 3.

```
bucket 0: -
bucket 1: -
bucket 2: -
bucket 3: [3] -> [11]
bucket 4: -
bucket 5: [5] -> [13] -> [21]
bucket 6: -
bucket 7: -
```

**Load factor α = 5/8 = 0.625.** Worst-case lookup is **Θ(3)** — the length of the longest chain — and in general Θ(n) when every key collides.

The instructive part is that α = 0.625 is a perfectly healthy load factor, and the table is still badly distributed: six of eight buckets are empty while one holds three entries. **Load factor measures occupancy, not uniformity.** It tells you when to resize, but a low load factor is no protection against a hash function that clusters — here every key is ≡ 5 (mod 8), so resizing to 16 buckets would split them only if the new modulus separates them (5 % 16 = 5, 13 % 16 = 13, 21 % 16 = 5 — partially).

This is why table sizes are chosen as powers of two *with* a well-mixed hash, or as primes: the combination of hash quality and modulus must break up arithmetic progressions in the key space.

**2.** | | Chaining | Linear probing |
|---|---|---|
| **Memory** | Bucket array + a node per entry (pointer overhead) | One flat array, no per-entry overhead — **probing wins** |
| **Cache** | Each chain step is a pointer chase to arbitrary memory | Probes are **adjacent slots**, often the same cache line — **probing wins decisively** |
| **Deletion** | Unlink the node; simple and complete — **chaining wins** | Cannot just clear the slot: it would break probe chains for later keys. Needs a **tombstone**, which accumulates |
| **α → 1** | Degrades gracefully; average chain length is α, and α > 1 is legal | Degrades catastrophically — expected probes ≈ ½(1 + 1/(1−α)), so α = 0.9 costs ~5.5 probes and α = 0.99 costs ~50. **Chaining wins**, and probing *cannot* exceed α = 1 at all |

**Chaining** is more forgiving: tolerant of a mediocre hash function, tolerant of high load, and trivial to delete from. **Linear probing** is faster when kept below about α = 0.7, because contiguous memory beats pointer chasing by a wide margin on modern hardware — and it needs a good hash, because it suffers **primary clustering**, where runs of occupied slots merge and grow.

CPython's dict uses open addressing with a **pseudo-random probe sequence** derived from the full hash rather than linear probing, precisely to avoid clustering while keeping the flat-array memory win. It resizes at α = 2/3.

**3.**

```python
def _resize(self):
    old = self.buckets
    self.capacity *= 2
    self.buckets = [[] for _ in range(self.capacity)]
    self.size = 0
    for chain in old:
        for key, value in chain:
            self.put(key, value)   # recompute index

def put(self, key, value):
    if (self.size + 1) / self.capacity > 0.75:
        self._resize()
    ...
```

Entries must be **rehashed** because a key's bucket is `hash(key) % capacity`, and the capacity has changed. A key with hash 21 sits in bucket 5 when capacity is 8 and bucket 5 when capacity is 16 — but a key with hash 13 moves from bucket 5 to bucket 13. Copying chains wholesale would leave keys in buckets where lookup will never probe for them: they would be *in* the table and permanently unfindable, with no error to signal it. The hash values themselves do not change; the **mapping from hash to bucket** does.

**Amortised cost: O(1).** Resizing at capacity k costs Θ(k), and doubling means resizes occur at capacities 1, 2, 4, 8, …, so the total rehashing work across n insertions is 1 + 2 + 4 + … < 2n — the same geometric-series argument as dynamic array growth in L20. The individual insertion that triggers a resize is Θ(n), which is why hash tables are a poor fit for hard real-time systems even though their average is excellent.

Caching each entry's hash alongside it avoids recomputing `hash(key)` during a resize — worthwhile for string keys, and what CPython does.

**4.** **The attack.** A web server parsing form data or JSON puts every key into a dict. If the hash function is deterministic and public, an attacker can precompute thousands of distinct keys that all hash to the same bucket, then submit them in one request. Every insertion collides, each one scanning the growing chain, so inserting n keys costs Θ(n²) instead of Θ(n). A few hundred kilobytes of crafted POST data — well inside any request size limit — could occupy a CPU for **minutes**. A handful of such requests takes the server down: an asymmetric denial of service, cheap to send and expensive to process.

**Why 2011.** Klink and Wälde demonstrated it at 28C3 against PHP, Java, Python, Ruby, and ASP.NET simultaneously. Every one of them used a fixed, documented hash, so a single precomputed collision set worked against every deployment of that language on earth. It was a design flaw shared across an entire generation of runtimes, not a bug in one of them.

**The fix: hash randomisation.** Python 3.3+ mixes a **random per-process seed** into the hash of `str` and `bytes`, so the same string hashes differently in different runs. An attacker cannot precompute collisions without knowing the seed. Run `python3 -c "print(hash('a'))"` twice and you will see different values; `PYTHONHASHSEED=0` disables it for reproducible testing.

The wider lesson: **average-case analysis assumes inputs are not chosen adversarially.** When an attacker picks your input, the worst case is the case you get — the same reasoning that makes randomised quicksort pivots a security property, not just a performance one.



---

## Reading

- **CLRS, Ch. 11** — Hash Tables (the definitive formal treatment: direct addressing, chaining, open addressing, universal hashing)
- **Python docs — PEP 456:** hash randomization (optional, for the curious)

---

*CS 101 · Week 8 · Lecture 26 (Thu) · © CSE Department*

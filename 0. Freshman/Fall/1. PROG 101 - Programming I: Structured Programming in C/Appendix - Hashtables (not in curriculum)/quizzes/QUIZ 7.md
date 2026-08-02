# PROG 101 · Programming I: Structured Programming in C
## Appendix Quiz (Hash Tables)

> **⚠ Off-syllabus.** Hash tables are **not** in the PROG 101 curriculum — they are CS 101's
> Week 8 topic. This quiz accompanies the optional Hash Tables appendix and is **not part of
> the assessed curriculum**. Retained as elective material.

**Administered:** with the Hash Tables appendix (off-syllabus)
**Duration:** 10 minutes · Closed book · 20 points

---

## Section A: Multiple Choice (2 pts each)

**1.** What is the average-case time complexity of search, insert, and delete in a well-implemented hash table?

- (A) O(n)
- (B) O(log n)
- (C) O(1)
- (D) O(n log n)

---

**2.** Why are collisions in a hash table mathematically unavoidable, in general?

- (A) All hash functions are poorly designed
- (B) The pigeonhole principle: the space of possible keys exceeds the number of table slots
- (C) C's modulo operator is inherently unreliable
- (D) Collisions only happen with bad hash functions — good ones never collide

---

**3.** In an open-addressing hash table, why can't you simply set a deleted slot's key to `NULL`?

- (A) `NULL` is not a valid value for a `char *`
- (B) It would break the probe sequence for searching other keys that were pushed past this slot during insertion
- (C) `free()` requires the key to remain non-NULL
- (D) It causes a compiler warning

---

**4.** What is "primary clustering," and which probing strategy suffers from it most?

- (A) A property of separate chaining; happens when too many keys hash to bucket 0
- (B) A weakness of linear probing where full slots form growing runs that attract even more collisions
- (C) A property of double hashing that occurs only for prime table sizes
- (D) A general term for any collision, regardless of resolution strategy

---

**5.** Why should you never rely on the order in which `ht_foreach` (or equivalent) visits hash table entries?

- (A) It's technically undefined behavior to iterate a hash table at all
- (B) The order depends on internal hash values and bucket layout, not insertion order or any natural key ordering, and can change across resizes
- (C) `ht_foreach` visits entries in reverse insertion order, which is often mistaken for forward order
- (D) Iteration order is guaranteed alphabetical, so relying on it is fine

---

## Section B: Short Answer (2 pts each)

**6.** Why is `hash_naive_sum` (simply summing character values) a poor hash function, even though it satisfies the "deterministic" property? Give a concrete example.

```
Reason: _____________________________________________________________

Example: ____________________________________________________________
```

---

**7.** What is the "load factor" of a hash table, and why does separate chaining tolerate a load factor greater than 1 while open addressing cannot?

```
Load factor definition: _____________________________________________

Why chaining tolerates > 1: _________________________________________

Why open addressing cannot: _________________________________________
```

---

**8.** Trace what happens (in words, not code) when you `ht_insert` a key into a chaining-based hash table where that key's bucket already contains 2 other entries (a collision, but not with the same key). What data structure operation from a previous week does this directly reuse?

```
_____________________________________________________________________

_____________________________________________________________________
```

---

**9.** A hash table with separate chaining currently has 40 entries across 50 buckets (load factor 0.8), exceeding a 0.75 threshold. Describe, step by step, what happens during a resize.

```
Step 1: ______________________________________________________________

Step 2: ______________________________________________________________

Step 3: ______________________________________________________________

Why is this called "amortized O(1)" despite resizing being an O(n) operation? 
_______________________________________________________________________
```

---

**10.** You need a structure that supports fast lookup by key AND must always be iterable in sorted key order. Would you choose a hash table or a Binary Search Tree (Week 9)? Justify your answer in terms of the tradeoff involved.

```
Choice: ______________________________________________________________

Justification: _______________________________________________________
```

---

## Answer Key (Instructor Copy)

**1. (C) O(1)** — This is the entire point of hashing: a good hash function combined with adequate table sizing and collision handling gives constant average-case time for the three core operations, a significant improvement over the O(log n) of a balanced BST or the O(n) of a linked list/unsorted array.

**2. (B)** — By the pigeonhole principle, since the space of possible keys (e.g., all possible strings) vastly exceeds any finite table size, some distinct keys are mathematically guaranteed to map to the same bucket index. This is true regardless of how good the hash function is — good hash functions minimize *how often* collisions cluster unevenly, but cannot eliminate collisions entirely.

**3. (B)** — If key A hashes to slot 5, causing key B (which also hashes to slot 5) to be probed forward to slot 6, then later setting slot 5 to `NULL` upon deleting A would cause a search for B to incorrectly stop at slot 5 (mistaking it for "never occupied, key can't be here") rather than continuing to probe forward to slot 6 where B still resides. A tombstone marker distinguishes "was occupied, now deleted, keep probing past this" from "truly never occupied, stop here."

**4. (B)** — Primary clustering is specifically a weakness of linear probing: once a run of consecutive occupied slots forms, any new key that would have landed anywhere within that run gets pushed to the run's end, extending it further — runs tend to grow other runs, degrading average probe length disproportionately as the table fills.

**5. (B)** — A hash table's iteration order is a direct consequence of which bucket each key happens to hash into and how the internal array is laid out — it has no relationship to insertion order or the keys' natural ordering, and resizing (which changes the table size and therefore every key's bucket index via the modulus) can completely reshuffle the apparent order between two otherwise-identical states of the table.

**6.** Reason: it only accounts for the sum of character values, completely ignoring their order/position within the string — any strings that are anagrams of each other (rearrangements of the exact same characters) produce identical hash values, causing severe unnecessary clustering. Example: `"cat"`, `"act"`, and `"tac"` all sum to the same total (since addition is commutative), so all three collide at the same bucket despite being entirely different, unrelated keys in most applications.

**7.**
- Load factor definition: `count / size` — the ratio of stored entries to the number of table buckets/slots.
- Why chaining tolerates > 1: each bucket holds an independent linked list, so multiple entries per bucket simply means a longer list at that bucket — there is no hard capacity limit, only gradually degrading average performance as chains lengthen.
- Why open addressing cannot: every entry must occupy an actual slot directly within the table array itself; once every slot is filled, there is physically nowhere left to place (or even probe for) a new entry, so load factor can never reach or exceed 1.

**8.** In words: the new key's hash is computed, mapping to the already-occupied bucket. The hash table walks the existing 2-entry linked list at that bucket (checking each entry's key with `strcmp` to make sure it isn't an update to an existing key), and upon confirming it's genuinely a new key, inserts a new node at the front of that bucket's linked list (or at the end, depending on implementation choice), linking it to the existing 2 entries. This directly reuses **Week 7's linked list insert-at-front (or insert-at-end) operation**, applied independently within a single bucket's chain.

**9.**
- Step 1: Allocate a new, larger bucket array (conventionally double the previous size, or advance to the next prime in a precomputed list).
- Step 2: Iterate through every entry in every bucket of the OLD table.
- Step 3: For each entry, recompute its hash modulo the NEW (larger) table size, and reinsert it into the corresponding bucket of the new table; free the old bucket array once every entry has been migrated.
- Why amortized O(1): although any single resize operation costs O(n) (every existing entry must be rehashed), resizes happen increasingly rarely as the table grows (doubling means only O(log n) resizes ever occur across a sequence of n total insertions) — spreading (amortizing) that total O(n log n) resizing cost evenly across all n insertions yields an average of O(1) additional work per insertion, matching the same amortized argument used for Week 3's dynamic array doubling.

**10.** Choice: Binary Search Tree (BST). Justification: a hash table provides faster O(1) average-case lookup but offers absolutely no ordering guarantee — its iteration order is essentially arbitrary and can change on resize, making it fundamentally unsuitable for a requirement of sorted iteration. A BST sacrifices some lookup speed (O(log n) average instead of O(1)) but maintains the key ordering as an intrinsic structural property, allowing sorted iteration "for free" via inorder traversal (Week 9) — directly satisfying the stated requirement, which a hash table cannot satisfy no matter how it's implemented.

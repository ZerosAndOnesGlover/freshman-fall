# PROG 101 — this appendix: Hash Tables
## Hash Functions · Collision Resolution · The Third Great Data Structure

---

## Week Overview

this appendix completes your foundational trio of data structures: linked lists (Week 7), binary search trees (Week 9), and now hash tables — the structure that gives you average-case O(1) lookup by key, the same technique underlying every dictionary, map, and set you'll use in every language for the rest of your career. You will implement real, production-grade hash functions from scratch, understand why collisions are mathematically unavoidable, build both major collision-resolution strategies (chaining and open addressing), and apply your hash table to genuinely useful problems.

---

## Schedule

| Day | Event | Topic | Duration |
|-----|-------|-------|----------|
| Tuesday | Lecture 1 | Hash Functions and the Hashing Problem | 50 min |
| Wednesday | Lecture 2 | Collision Resolution: Chaining and Open Addressing | 50 min |
| Thursday | Lecture 3 | Building a Complete Hash Table and Applications | 50 min |
| Monday | **Lab 7** | Hash Functions + Generic Hash Table + Set/Applications | 2 hours |

---

## Files in This Package

```
PROG101_Week7/
├── README.md
├── lectures/
│   ├── Lecture 01 Hash Functions.md                 ← djb2, FNV-1a, collision inevitability, distribution testing
│   ├── Lecture 02 Collision Resolution.md            ← Chaining (Week 7 reuse!), linear/quadratic/double-hash probing, tombstones, resizing
│   └── Lecture 03 Hashtable Applications.md          ← Generic void* API, Set, word frequency, caching, iteration order
├── lab/
│   └── LAB 7 Hashtable.md                              ← Hash function distribution testing + complete generic hash table + Set + apps
├── assignments/
│   └── Problem Set 7.md                               ← 5 problems: open addressing (all 3 strategies), phone book, anagram grouping, hash algorithms (two-sum etc.), in-memory DB table
├── quizzes/
│   └── QUIZ 7.md                                       ← 10 questions + full answer key
└── resources/
    └── this appendix Hashtable Reference.md                    ← Hash function library, chaining/open-addressing patterns, complexity table, common bugs
```

---

## Learning Objectives

After this appendix, you will be able to:

- [ ] Implement djb2 and FNV-1a hash functions from scratch and explain their design
- [ ] Explain why hash collisions are mathematically unavoidable (pigeonhole principle)
- [ ] Empirically measure and compare hash function distribution quality
- [ ] Implement separate chaining, directly reusing Week 7's linked list operations
- [ ] Implement open addressing with linear probing, quadratic probing, and double hashing
- [ ] Explain why deletion in open addressing requires tombstones, not simple clearing
- [ ] Explain load factor and implement automatic resizing (rehashing) with amortized O(1) cost
- [ ] Design a generic C hash table API using `void *` values and opaque types
- [ ] Build a Set as a specialization of a hash table
- [ ] Apply hash tables to deduplication, frequency counting, and caching problems
- [ ] Explain why hash table iteration order is unspecified and must never be relied upon
- [ ] Choose correctly between a hash table and a BST based on ordering requirements

---

## Textbook Reading

| Lecture | Reference |
|---------|-----------|
| L1: Hash Functions | CLRS Ch. 11.1–11.3; Sedgewick & Wayne §3.4 |
| L2: Collision Resolution | CLRS Ch. 11.4 (Open Addressing); Sedgewick & Wayne §3.4 |
| L3: Applications | CLRS Ch. 11 (complete); Sedgewick & Wayne §3.5 |

---

## The Key Insights of This Week

### On Hash Functions
A hash function's job is not to avoid collisions (impossible, by the pigeonhole principle) but to spread keys as evenly as possible across the table, minimizing how badly collisions cluster. The difference between a naive sum-of-characters hash and djb2 isn't philosophical — it's measurable, and this week you measure it directly on real data.

### On Chaining
Separate chaining is not a new data structure to learn — it is an array of Week 7's linked lists, indexed by a hash function. Every operation you implement this week (insert-at-front, prev/cur deletion, free-the-list) is a technique you already know, applied inside a bucket. This is why the implementation, once you see it this way, requires almost no new conceptual work.

### On Load Factor and Resizing
The same amortized-O(1) argument from Week 3's dynamic array reappears here in a new guise: resizing costs O(n) any single time it happens, but happens rarely enough (halving in frequency each time, as the table doubles) that the average cost per operation, across the whole sequence, stays O(1). This is a genuinely recurring pattern in computer science — recognizing it here means you'll recognize it again in every future data structure course.

### On the Fundamental Tradeoff
Hash tables buy O(1) average lookup by giving up all ordering. BSTs keep ordering by accepting O(log n). There is no data structure that gives you both O(1) lookup AND maintained sort order — this isn't a limitation of your implementation, it's a fundamental tradeoff, and recognizing it is what separates "I can build a hash table" from "I understand when to use one."

---

## Common this appendix Mistakes

**Using a poor hash function and being surprised by clustering:**
```c
/* Summing characters — anagrams collide, catastrophic clustering on real data */
unsigned long hash_bad(const char *s) { unsigned long h=0; while(*s) h+=*s++; return h; }
```

**Forgetting to heap-copy keys:**
```c
ht_insert(ht, local_key_buffer, value);   /* dangling pointer if buffer is reused/freed */
/* FIX: new_entry->key = strdup(key); */
```

**Integer division in load factor checks:**
```c
if (ht->count / ht->size > 0.75)         /* WRONG: integer division truncates to 0 */
if ((double)ht->count / ht->size > 0.75) /* CORRECT */
```

**Using NULL instead of a tombstone for open-addressing deletion:**
```c
table[idx].key = NULL;   /* WRONG: breaks probe sequences for keys probed past this slot */
```

**Relying on hash table iteration order:**
```c
ht_foreach(ht, print_entry, NULL);   /* order is UNSPECIFIED — never depend on it */
```

**Losing entries during a naive resize (realloc without rehashing):**
```c
ht->buckets = realloc(ht->buckets, new_size * sizeof(Entry*));  /* WRONG alone —
    old entries are still at indices computed for the OLD size; must rehash every entry */
```

---

## Challenge Problems (Optional)

1. **Consistent hashing** — implement a simplified consistent hashing scheme (used in distributed systems like Cassandra and DynamoDB, previewed in Year 3's Database Systems course): map both keys and a set of "nodes" onto a circular hash space, and route each key to the nearest node clockwise. Demonstrate that adding/removing a node only reshuffles a small fraction of keys, unlike naive `hash(key) % num_nodes`.

2. **Cuckoo hashing** — implement cuckoo hashing, where each key has two possible slots (via two hash functions), and inserting a key that finds both slots occupied "kicks out" the existing occupant to its alternate slot, recursively. This achieves O(1) worst-case lookup (not just average case) at the cost of more complex insertion.

3. **A Bloom filter** — implement a Bloom filter: a space-efficient probabilistic structure that can definitively say "definitely not present" or "possibly present" (with a tunable false-positive rate) using a bit array and multiple hash functions, without storing the keys themselves at all.

4. **Perfect hashing for a static dictionary** — given a fixed, known-in-advance set of keys (e.g., all C keywords), construct a hash function with zero collisions for that specific set, achieving guaranteed O(1) worst-case lookup for static data.

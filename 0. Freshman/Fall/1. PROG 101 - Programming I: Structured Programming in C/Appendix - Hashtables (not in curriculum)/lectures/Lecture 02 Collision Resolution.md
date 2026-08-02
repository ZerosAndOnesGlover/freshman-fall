# PROG 101 · Programming I: Structured Programming in C
## Appendix · Lecture 2: Collision Resolution — Chaining and Open Addressing

---

## Lecture Goals

By the end of this lecture you will:
- Implement separate chaining using linked lists per bucket
- Implement open addressing with linear probing, quadratic probing, and double hashing
- Understand the tradeoffs between chaining and open addressing
- Understand load factor and why it drives resizing decisions
- Implement dynamic resizing (rehashing) to maintain O(1) average performance

---

## 1. Two Families of Collision Resolution

There are two fundamentally different strategies for handling the collisions that Lecture 1 established are unavoidable:

**Separate chaining:** each bucket holds a linked list (or another structure) of all keys that hash to that index. Collisions simply mean the list at that bucket has more than one entry.

**Open addressing:** all entries live directly in the table array itself (no separate structure per bucket). When a collision occurs, the algorithm *probes* — searches according to a defined sequence — for the next available slot.

```
Separate Chaining:                    Open Addressing:
table[0] → NULL                       table[0] = empty
table[1] → ["bob"]                    table[1] = "bob"
table[2] → NULL                       table[2] = empty
table[3] → ["alice"] → ["carol"]      table[3] = "alice"
table[4] → NULL                       table[4] = "carol"  ← probed here after
                                                              colliding at index 3
```

---

## 2. Separate Chaining — Implementation

Each bucket is a linked list (using exactly the Week 7 singly linked list pattern, specialized for key-value pairs):

```c
typedef struct Entry {
    char  *key;
    int    value;
    struct Entry *next;
} Entry;

typedef struct {
    Entry **buckets;    /* array of pointers to linked list heads */
    int     size;       /* number of buckets (table size) */
    int     count;       /* number of key-value pairs currently stored */
} HashTable;

HashTable *ht_create(int size) {
    HashTable *ht = malloc(sizeof(HashTable));
    ht->buckets = calloc(size, sizeof(Entry *));   /* all pointers start NULL */
    ht->size    = size;
    ht->count   = 0;
    return ht;
}

void ht_insert(HashTable *ht, const char *key, int value) {
    unsigned int index = hash_djb2(key) % ht->size;

    /* Check if the key already exists in this bucket's list — update if so */
    for (Entry *e = ht->buckets[index]; e != NULL; e = e->next) {
        if (strcmp(e->key, key) == 0) {
            e->value = value;   /* update existing entry */
            return;
        }
    }

    /* Not found — insert a new entry at the front of this bucket's list */
    Entry *new_entry = malloc(sizeof(Entry));
    new_entry->key   = strdup(key);   /* heap-copy the key string */
    new_entry->value = value;
    new_entry->next  = ht->buckets[index];   /* insert at front — Week 7's pattern */
    ht->buckets[index] = new_entry;
    ht->count++;
}

int ht_search(HashTable *ht, const char *key, int *out_value) {
    unsigned int index = hash_djb2(key) % ht->size;

    for (Entry *e = ht->buckets[index]; e != NULL; e = e->next) {
        if (strcmp(e->key, key) == 0) {
            *out_value = e->value;
            return 1;   /* found */
        }
    }
    return 0;   /* not found */
}

int ht_delete(HashTable *ht, const char *key) {
    unsigned int index = hash_djb2(key) % ht->size;

    Entry *prev = NULL;
    Entry *cur  = ht->buckets[index];

    while (cur != NULL) {
        if (strcmp(cur->key, key) == 0) {
            if (prev == NULL) {
                ht->buckets[index] = cur->next;   /* removing the head of this bucket */
            } else {
                prev->next = cur->next;            /* Week 7's deletion pattern exactly */
            }
            free(cur->key);
            free(cur);
            ht->count--;
            return 1;
        }
        prev = cur;
        cur  = cur->next;
    }
    return 0;   /* key not found */
}

void ht_free(HashTable *ht) {
    for (int i = 0; i < ht->size; i++) {
        Entry *cur = ht->buckets[i];
        while (cur != NULL) {
            Entry *next = cur->next;   /* Week 7's free-list pattern */
            free(cur->key);
            free(cur);
            cur = next;
        }
    }
    free(ht->buckets);
    free(ht);
}
```

**Notice:** every single operation here reuses a Week 7 linked-list pattern directly — insert-at-front, delete-by-value with prev/cur tracking, free-the-list. A hash table with chaining is, quite literally, "an array of linked lists, indexed by a hash function." This is why building it now, immediately after linked lists, makes the implementation almost effortless — you already know every technique it requires.

### Chaining's Worst Case

If every key happened to hash to the same bucket (a pathological hash function, or an adversarial attacker deliberately choosing colliding keys), chaining degrades to a single linked list — O(n) for every operation. This is why hash function quality (Lecture 1) matters so much: a good hash function makes this worst case exceedingly unlikely for realistic data.

---

## 3. Open Addressing — Linear Probing

In open addressing, there are no separate per-bucket structures — every entry lives directly in the table array. On a collision, you **probe** for the next open slot according to a defined sequence.

**Linear probing:** on collision, try the next slot, then the next, wrapping around at the end of the table:

```c
typedef struct {
    char *key;      /* NULL means this slot is empty */
    int   value;
    int   is_deleted;   /* tombstone — see below */
} Slot;

typedef struct {
    Slot *table;
    int   size;
    int   count;
} OpenHashTable;

OpenHashTable *oht_create(int size) {
    OpenHashTable *oht = malloc(sizeof(OpenHashTable));
    oht->table = calloc(size, sizeof(Slot));   /* all keys start NULL (empty) */
    oht->size  = size;
    oht->count = 0;
    return oht;
}

int oht_insert(OpenHashTable *oht, const char *key, int value) {
    if (oht->count >= oht->size) return -1;   /* table full — caller should resize first */

    unsigned int index = hash_djb2(key) % oht->size;
    unsigned int start = index;

    do {
        if (oht->table[index].key == NULL || oht->table[index].is_deleted) {
            /* found an empty (or tombstoned) slot — insert here */
            oht->table[index].key   = strdup(key);
            oht->table[index].value = value;
            oht->table[index].is_deleted = 0;
            oht->count++;
            return 0;
        }
        if (strcmp(oht->table[index].key, key) == 0) {
            oht->table[index].value = value;   /* key already exists — update */
            return 0;
        }
        index = (index + 1) % oht->size;   /* LINEAR PROBE: try the next slot */
    } while (index != start);

    return -1;   /* table is genuinely full (shouldn't happen if resizing is working) */
}

int oht_search(OpenHashTable *oht, const char *key, int *out_value) {
    unsigned int index = hash_djb2(key) % oht->size;
    unsigned int start = index;

    do {
        if (oht->table[index].key == NULL && !oht->table[index].is_deleted) {
            return 0;   /* hit a truly empty slot — key cannot be further along, stop */
        }
        if (oht->table[index].key != NULL && !oht->table[index].is_deleted &&
            strcmp(oht->table[index].key, key) == 0) {
            *out_value = oht->table[index].value;
            return 1;
        }
        index = (index + 1) % oht->size;
    } while (index != start);

    return 0;
}
```

### Why Deletion Needs Tombstones

If you simply set a slot's key to `NULL` on deletion, you break the probing sequence for search: imagine keys A, B, C all hash to index 5, so B and C were probed forward to indices 6 and 7. If you delete B (at index 6) by setting it to `NULL`, a later search for C (at index 7) would stop early at index 6 — mistaking the "hole" for "this key was never here" — and incorrectly report C as not found, even though it's still at index 7.

**The fix:** use a **tombstone** marker (`is_deleted = 1`) instead of truly clearing the slot. Search treats tombstones as "keep probing past this" (unlike a truly empty slot, which means "stop, definitely not here"), while insert treats tombstones as "this slot is available for reuse."

### Linear Probing's Weakness: Primary Clustering

Linear probing has a well-known weakness: once several consecutive slots fill up, that "run" of full slots tends to grow even faster (any new key hashing anywhere into that run gets pushed to the run's end), creating long clusters that degrade performance. This is called **primary clustering**.

---

## 4. Open Addressing — Quadratic Probing and Double Hashing

**Quadratic probing** breaks up the linear clustering by using a probe sequence based on squared offsets:

```c
/* Probe sequence: index, index+1, index+4, index+9, index+16, ... */
unsigned int index = (hash_djb2(key) + i * i) % oht->size;
/* where i = 0, 1, 2, 3, ... is the probe attempt number */
```

This spreads out collisions more than linear probing, avoiding the "runs grow runs" clustering effect, though it introduces its own subtler clustering pattern (secondary clustering — keys that collide at their initial hash follow the exact same probe sequence).

**Double hashing** uses a *second* independent hash function to determine the probe step size, which varies per key rather than being fixed:

```c
unsigned int hash1 = hash_djb2(key) % oht->size;
unsigned int hash2 = 1 + (hash_fnv1a(key) % (oht->size - 1));   /* must be non-zero */

/* Probe sequence: hash1, hash1+hash2, hash1+2*hash2, hash1+3*hash2, ... (mod size) */
unsigned int index = (hash1 + i * hash2) % oht->size;
```

Because the step size (`hash2`) itself depends on the key, two different keys that happen to collide at their initial slot will very likely follow **completely different** probe sequences from that point on — this is the best defense against clustering among the three open-addressing strategies, at the cost of computing a second hash function.

---

## 5. Chaining vs Open Addressing — Engineering Tradeoffs

| Factor | Separate Chaining | Open Addressing |
|--------|---------------------|-------------------|
| Extra memory per entry | One pointer (linked list node overhead) | None — entries live directly in the array |
| Cache performance | Poor (linked list nodes scattered on heap) | Excellent (contiguous array, better cache locality) |
| Handling load factor > 1 | Works fine (lists just get longer) | Impossible — table can never exceed 100% full |
| Deletion complexity | Simple (standard linked-list deletion) | Requires tombstones — more subtle |
| Worst-case degradation | O(n) if all keys collide (one giant list) | O(n) if probing degenerates into scanning most of the table |
| Implementation complexity | Simpler | More subtle (tombstones, probe sequence choice) |

**In practice:** many production hash table implementations (including Python's dict, prior to a certain version, and many others) use variants of open addressing for its superior cache performance, while others (including early Java's `HashMap`) use chaining for its simplicity and graceful degradation. Both are legitimate, widely-used engineering choices — this course implements **separate chaining** as the primary technique (Lab 7, PS7) because it builds directly and instructively on Week 7's linked list work, while this lecture ensures you understand open addressing's mechanics and tradeoffs as well.

---

## 6. Load Factor and Resizing

The **load factor** α is defined as:

```
α = count / size
```

- For **separate chaining**, α can exceed 1 (multiple entries per bucket is fine — lists just grow), but performance degrades linearly as α grows, since average chain length is α.
- For **open addressing**, α must always stay strictly less than 1 (the table cannot hold more entries than it has slots), and performance degrades sharply (non-linearly) as α approaches 1 — probe sequences get dramatically longer.

**The standard engineering response:** when the load factor crosses a threshold (commonly α > 0.75 for chaining, or α > 0.5–0.7 for open addressing), **resize** the table — allocate a new, larger array (conventionally double the size, similar to Week 3's dynamic array doubling strategy) and **rehash** every existing entry into the new table (their bucket indices change, since the modulus — the table size — changed).

```c
void ht_resize(HashTable *ht) {
    int old_size = ht->size;
    Entry **old_buckets = ht->buckets;

    ht->size    = old_size * 2;
    ht->buckets = calloc(ht->size, sizeof(Entry *));
    ht->count   = 0;   /* will be re-incremented as we reinsert everything below */

    for (int i = 0; i < old_size; i++) {
        Entry *cur = old_buckets[i];
        while (cur != NULL) {
            Entry *next = cur->next;               /* save before we relink cur */
            ht_insert(ht, cur->key, cur->value);   /* rehash into the new, larger table */
            free(cur->key);
            free(cur);
            cur = next;
        }
    }
    free(old_buckets);
}

/* Call this check at the top of ht_insert, before inserting the new entry: */
void ht_insert(HashTable *ht, const char *key, int value) {
    if ((double)(ht->count + 1) / ht->size > 0.75) {
        ht_resize(ht);
    }
    /* ... rest of insertion logic as before ... */
}
```

This is precisely the **amortized O(1)** argument from Week 3's dynamic array, applied to hash tables: resizing is an expensive O(n) operation, but it happens rarely enough (doubling means it happens only O(log n) times as the table grows to n entries) that the *average* cost per insertion, amortized over the whole sequence of insertions, remains O(1).

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** A chaining table has 8 buckets and uses `h % 8`. Insert keys with hashes 5, 13, 21, 3, 11. Draw the table, give the load factor, and state the worst-case lookup cost.

**2. (Explain.)** Explain why deletion in a linear-probing table cannot simply clear the slot. Describe the tombstone solution and its cost.

**3. (Build.)** Implement `resize()` for a chaining hash table. Explain why entries must be rehashed rather than copied, and give the amortised insertion cost.

**4. (Stretch.)** Compare chaining and open addressing on memory, cache behaviour, deletion, and behaviour as α → 1. Then explain why an attacker who can choose keys threatens both.


### Answers

**1.** 5 % 8 = 5, 13 % 8 = 5, 21 % 8 = 5, 3 % 8 = 3, 11 % 8 = 3.

```
[0] -
[1] -
[2] -
[3] -> 3 -> 11
[4] -
[5] -> 5 -> 13 -> 21
[6] -
[7] -
```

**Load factor α = 5/8 = 0.625.** Worst-case lookup is the longest chain, **3 comparisons**; in general it is O(n) when every key collides.

The instructive part is that α = 0.625 is a perfectly *healthy* load factor and the table is still badly distributed — six of eight buckets empty, one holding three entries. **Load factor measures occupancy, not uniformity.** It tells you when to resize and says nothing about whether the hash is any good.

Here every key is ≡ 5 (mod 8) or ≡ 3 (mod 8), which is the signature of keys carrying arithmetic structure that the modulus fails to break up. Resizing to 16 buckets helps only partially: 5 % 16 = 5 and 21 % 16 = 5 still collide, while 13 % 16 = 13 separates.

Two diagnostics worth running on a real table: the **longest chain** and the **empty-bucket fraction**. If the longest chain grows faster than log n while α stays low, the hash is the problem, not the size.

**2.** Linear probing finds a key by hashing to a home slot and scanning forward until it finds the key or **an empty slot**, which means "not present". Clearing a slot on deletion therefore inserts a false terminator into that probe sequence: any key that had probed *past* the deleted slot to reach its own position becomes **unreachable**. It is still in the table, and lookup reports it missing.

Example: keys A and B both hash to slot 3; A takes 3, B probes to 4. Delete A and clear slot 3, and searching for B stops at the now-empty slot 3 and concludes B is absent.

**The tombstone solution** marks the slot `DELETED` rather than `EMPTY`. Lookup treats a tombstone as "keep probing", so chains stay intact; insertion treats it as a free slot and may reuse it — but must still scan onward to confirm the key is not present further along, or duplicates appear.

**The cost** is that tombstones never shorten probe sequences. In a table with heavy churn — many inserts and deletes at a stable size — they accumulate until the table behaves as if it were nearly full, with lookups slowing toward O(n) even though the live count is low. The fix is to count tombstones as occupied when computing the load factor, and **rehash** when they pass a threshold, which purges them.

Chaining avoids all of this: unlink the node and the chain is intact. That is chaining's main engineering advantage, and it is why deletion-heavy workloads favour it.

**3.**

```c
static int ht_resize(HashTable *ht) {
    size_t ncap = ht->cap * 2;
    Entry **nbuckets = calloc(ncap, sizeof *nbuckets);
    if (!nbuckets) return 0;   /* keep the old table */

    for (size_t i = 0; i < ht->cap; i++) {
        Entry *e = ht->buckets[i];
        while (e) {
            Entry *next = e->next;              /* save before relinking */
            size_t b = e->hash % ncap;                  /* cached hash — no recompute */
            e->next = nbuckets[b];
            nbuckets[b] = e;                            /* move the node itself */
            e = next;
        }
    }
    free(ht->buckets);
    ht->buckets = nbuckets;
    ht->cap = ncap;
    return 1;
}
```

Entries must be **rehashed** because a key's bucket is `hash % cap`, and `cap` has changed. The hash value itself is unchanged — it is the **mapping from hash to bucket** that moves. Copying chains wholesale would leave keys in buckets that lookup will never probe: present in the table, permanently unfindable, with no error to signal it.

**Amortised cost: O(1) per insertion.** Resizing at capacity k costs Θ(k), and doubling puts resizes at capacities 1, 2, 4, 8, …, so the total rehashing across n insertions is 1 + 2 + 4 + … < 2n. The individual insertion that triggers a resize is Θ(n), which is why hash tables are a poor fit for hard real-time code.

Two details worth copying: **caching `e->hash` in the entry** avoids recomputing it for every key on every resize — significant for string keys. And **relinking the existing nodes** rather than allocating new ones means the resize performs no allocation beyond the bucket array, and cannot fail partway through leaving the table inconsistent.

**4.** | | Chaining | Open addressing |
|---|---|---|
| **Memory** | Bucket array + a node per entry (pointer + allocator overhead) | One flat array — **wins** |
| **Cache** | Each chain step is a pointer chase to arbitrary memory | Probes are adjacent slots, often the same cache line — **wins decisively** |
| **Deletion** | Unlink the node — simple, complete — **wins** | Needs tombstones, which accumulate |
| **α → 1** | Degrades gracefully; average chain is α, and α > 1 is legal — **wins** | Catastrophic: expected probes ≈ ½(1 + 1/(1−α)), so α = 0.9 costs ~5.5 and α = 0.99 costs ~50. Cannot exceed α = 1 at all |

**Chaining is forgiving** — tolerant of a mediocre hash and of high load. **Open addressing is faster** below about α = 0.7, because contiguous memory beats pointer chasing by a wide margin; it needs a good hash, since it suffers *primary clustering* where occupied runs merge and grow.

**An attacker who chooses keys defeats both.** With a deterministic, published hash, they precompute thousands of keys sharing a bucket and submit them together. Chaining degenerates to one long linked list; open addressing degenerates to one long probe run. Either way, inserting n crafted keys costs Θ(n²), and a few hundred kilobytes of form data can occupy a CPU for minutes — the **hash-flooding** denial of service demonstrated against PHP, Java, Python, and Ruby simultaneously in 2011.

The defence is not the resolution strategy but the hash: **randomise a per-process seed** so collisions cannot be precomputed, or use a keyed hash such as SipHash, which is what Python, Rust, and Perl now do. The general lesson from CS 101 L21 applies — average-case bounds assume inputs are not chosen adversarially.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Separate chaining** | Collision resolution using a linked list per bucket |
| **Open addressing** | Collision resolution storing all entries directly in the table, probing on collision |
| **Linear probing** | Open addressing probe sequence: try the next slot, sequentially |
| **Quadratic probing** | Open addressing probe sequence based on squared offsets |
| **Double hashing** | Open addressing using a second hash function to determine probe step size |
| **Primary clustering** | The tendency of linear probing to form growing runs of occupied slots |
| **Tombstone** | A marker for a deleted slot in open addressing, distinct from "never occupied" |
| **Load factor (α)** | Ratio of stored entries to table size |
| **Resizing / rehashing** | Growing the table and reinserting all entries when load factor crosses a threshold |

---

## Reading

- **CLRS Ch. 11.4** — Open Addressing
- **Sedgewick & Wayne §3.4** — Hash Tables (both chaining and open addressing covered with excellent diagrams)

---

*Next: Lecture 3 — Building a Complete Hash Table and Its Applications*

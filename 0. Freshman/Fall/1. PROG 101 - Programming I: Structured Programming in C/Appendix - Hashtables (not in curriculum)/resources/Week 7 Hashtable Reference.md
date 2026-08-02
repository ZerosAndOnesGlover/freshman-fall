# PROG 101 · this appendix Resources
## Hash Table Quick Reference · Hash Function Library · Common Bugs

---

## Part 1: Hash Function Reference

```c
/* djb2 — simple, fast, excellent real-world distribution */
unsigned long hash_djb2(const char *str) {
    unsigned long hash = 5381;
    int c;
    while ((c = *str++) != '\0') {
        hash = ((hash << 5) + hash) + (unsigned char)c;   /* hash * 33 + c */
    }
    return hash;
}

/* FNV-1a — alternates XOR and multiply, widely used in production */
unsigned long hash_fnv1a(const char *str) {
    unsigned long hash = 2166136261UL;
    int c;
    while ((c = *str++) != '\0') {
        hash ^= (unsigned char)c;
        hash *= 16777619UL;
    }
    return hash;
}

/* Integer bit-mixing hash (for non-string keys) */
unsigned int hash_int_mixed(int key) {
    unsigned int x = (unsigned int)key;
    x = ((x >> 16) ^ x) * 0x45d9f3b;
    x = ((x >> 16) ^ x) * 0x45d9f3b;
    x = (x >> 16) ^ x;
    return x;
}

/* Converting hash to table index — ALWAYS do this at the call site: */
unsigned int index = hash_djb2(key) % table_size;
```

### Prime Number Table Sizes (for resizing progressions)

```c
static const size_t PRIME_SIZES[] = {
    11, 23, 47, 97, 197, 397, 797, 1597, 3203, 6421,
    12853, 25717, 51437, 102877, 205759
};
```

Each roughly doubles the previous, while remaining prime — good practice for hash table bucket counts.

---

## Part 2: Separate Chaining — Complete Pattern

```c
typedef struct Entry {
    char  *key;
    void  *value;
    struct Entry *next;
} Entry;

typedef struct {
    Entry **buckets;
    size_t  size;
    size_t  count;
} HashTable;

/* INSERT pattern */
unsigned int idx = hash_djb2(key) % ht->size;
for (Entry *e = ht->buckets[idx]; e; e = e->next) {
    if (strcmp(e->key, key) == 0) { e->value = value; return; }  /* update */
}
Entry *new_e = malloc(sizeof(Entry));
new_e->key   = strdup(key);
new_e->value = value;
new_e->next  = ht->buckets[idx];
ht->buckets[idx] = new_e;
ht->count++;

/* SEARCH pattern */
unsigned int idx = hash_djb2(key) % ht->size;
for (Entry *e = ht->buckets[idx]; e; e = e->next)
    if (strcmp(e->key, key) == 0) return e->value;
return NULL;   /* not found */

/* DELETE pattern (Week 7's prev/cur linked list deletion, per-bucket) */
unsigned int idx = hash_djb2(key) % ht->size;
Entry *prev = NULL, *cur = ht->buckets[idx];
while (cur) {
    if (strcmp(cur->key, key) == 0) {
        if (prev) prev->next = cur->next;
        else      ht->buckets[idx] = cur->next;
        free(cur->key);
        free(cur);
        ht->count--;
        return true;
    }
    prev = cur;
    cur = cur->next;
}
return false;   /* not found */

/* FREE ALL pattern */
for (size_t i = 0; i < ht->size; i++) {
    Entry *cur = ht->buckets[i];
    while (cur) {
        Entry *next = cur->next;   /* save before freeing */
        free(cur->key);
        free(cur);
        cur = next;
    }
}
free(ht->buckets);
```

---

## Part 3: Open Addressing — Probe Sequence Reference

```c
/* Linear probing */
unsigned int probe_linear(unsigned int h, int i, size_t table_size) {
    return (h + (unsigned int)i) % table_size;
}

/* Quadratic probing */
unsigned int probe_quadratic(unsigned int h, int i, size_t table_size) {
    return (h + (unsigned int)(i * i)) % table_size;
}

/* Double hashing — requires a SECOND hash function */
unsigned int probe_double(unsigned int h1, unsigned int h2, int i, size_t table_size) {
    return (h1 + (unsigned int)i * h2) % table_size;
}
/* h2 must never be 0 — ensure with: h2 = 1 + (hash2(key) % (table_size - 1)); */
```

### Tombstone Discipline

```c
typedef struct {
    char *key;         /* NULL = never occupied */
    int   value;
    bool  is_deleted;  /* true = tombstone (was occupied, now removed) */
} Slot;

/* On SEARCH: stop probing ONLY at a truly-never-occupied slot (key==NULL && !is_deleted)
 * On INSERT: an available slot is (key==NULL) OR (is_deleted==true) — either can be reused
 * On DELETE: set is_deleted = true; do NOT set key to NULL */
```

---

## Part 4: Complexity Summary

| Structure | Search | Insert | Delete | Ordered iteration | Memory overhead |
|-----------|--------|--------|--------|---------------------|-------------------|
| Array (unsorted) | O(n) | O(1) | O(n) | No | None |
| Array (sorted) | O(log n) | O(n) | O(n) | Yes | None |
| Linked list | O(n) | O(1) front | O(n) | No | 1 pointer/node |
| BST (unbalanced) | O(log n) avg, O(n) worst | O(log n) avg | O(log n) avg | Yes (inorder) | 2 pointers/node |
| Hash table (chaining) | O(1) avg, O(n) worst | O(1) avg | O(1) avg | No | 1+ pointer/entry |
| Hash table (open addr.) | O(1) avg, O(n) worst | O(1) avg | O(1) avg | No | None (in-place) |

**The universal tradeoff:** hash tables win on raw average-case speed but sacrifice ordering entirely. BSTs give up some speed to keep data ordered. Choose based on what your application actually needs.

---

## Part 5: Common Hash Table Bugs

```c
/* BUG 1: Forgetting to heap-copy the key */
ht_insert(ht, local_buffer, value);   /* if local_buffer is later reused/freed,
                                          the stored key pointer is now invalid */
/* FIX: always strdup inside ht_insert */
new_entry->key = strdup(key);

/* BUG 2: Not checking for existing key before inserting (creates duplicates) */
/* Always scan the bucket's chain for a matching key BEFORE appending a new node */

/* BUG 3: Losing entries during resize (not reinserting into the NEW table) */
void bad_resize(HashTable *ht) {
    ht->size *= 2;
    ht->buckets = realloc(ht->buckets, ht->size * sizeof(Entry *));
    /* WRONG: existing entries are still in their OLD bucket indices,
       which no longer correspond to hash(key) % NEW_size — must
       rehash and reinsert every entry individually */
}

/* BUG 4: Memory leak on resize (old entries not freed after rehashing) */
/* When migrating entries to the new table, either relink the SAME node
   objects (no leak, but must be careful with the chain pointers) or
   create new nodes and free the old ones explicitly — don't do neither */

/* BUG 5: Off-by-one/wrong comparison in load factor check */
if (ht->count / ht->size > 0.75)   /* INTEGER DIVISION — always 0 or evaluates wrong! */
if ((double)ht->count / ht->size > 0.75)   /* CORRECT: cast before dividing */

/* BUG 6: Using NULL to mark deleted in open addressing (breaks probing) */
oht->table[idx].key = NULL;   /* WRONG for delete — use a tombstone flag instead */

/* BUG 7: Relying on hash table iteration order for anything */
/* ht_foreach order is unspecified and can change across resizes — never
   assume alphabetical, insertion, or any other particular order */

/* BUG 8: Signed/unsigned mismatch in hash % table_size */
int index = hash % table_size;   /* if hash is negative (e.g., from a poorly
                                     designed signed hash function), result
                                     can be negative — always use unsigned
                                     types for hash values and indices */
```

---

## Part 6: Debugging Hash Tables with GDB

```bash
gdb ./program
```

```
(gdb) break ht_insert
(gdb) run
(gdb) print key                    # see the key being inserted
(gdb) print index                  # see which bucket it hashes to
(gdb) print ht->buckets[index]     # see the existing chain at that bucket (if any)
(gdb) print *ht                    # see the whole HashTable struct (size, count)

# Walk a bucket's chain manually:
(gdb) set $e = ht->buckets[index]
(gdb) print *$e
(gdb) set $e = $e->next
(gdb) print *$e
# ... repeat until $e is NULL

# Check load factor manually:
(gdb) print (double)ht->count / ht->size
```

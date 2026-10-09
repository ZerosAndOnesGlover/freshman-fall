# PROG 101 · Programming I: Structured Programming in C
## Appendix · Lecture 3: Building a Complete Hash Table and Its Applications

*“We will never run out of things to program as long as there is a single program around.”* — Alan Perlis, "Epigrams on Programming" (1982), #100

**Reading:** CLRS Ch. 11 · Sedgewick & Wayne §3.5 *(details at the end of the lecture)*

---

## Lecture Goals

By the end of this lecture you will:
- Design a generic, reusable hash table API in C
- Build a hash-based Set as a specialization of a hash table
- Apply hash tables to solve real problems: word frequency, deduplication, caching
- Understand hash table iteration and its unordered nature
- Know the complexity guarantees and when a hash table is (and isn't) the right tool

---

## 1. From Concept to a Clean, Reusable API

Lecture 2 built a hash table with `int` values and `char *` keys, hardcoded to that specific type combination. A production-quality hash table API should be more general, while remaining honest about C's lack of generics (unlike Java's `HashMap<K,V>` or C++'s templates).

**The pragmatic C approach:** design the API around `void *` values (letting any pointer type be stored) while keeping `char *` string keys fixed — this covers the overwhelming majority of real use cases without the complexity of a fully generic key type.

```c
/* hashtable.h */
#ifndef HASHTABLE_H
#define HASHTABLE_H

#include <stddef.h>
#include <stdbool.h>

typedef struct HashTable HashTable;   /* opaque type — implementation hidden */

HashTable *ht_create(size_t initial_size);
void       ht_destroy(HashTable *ht, void (*free_value)(void *));
/* free_value: a function to free each stored value on destroy, or NULL
 * if values don't need freeing (e.g., they're stack values cast to void*,
 * or the caller manages their lifetime separately) */

bool ht_insert(HashTable *ht, const char *key, void *value);
void *ht_get(const HashTable *ht, const char *key);   /* NULL if not found */
bool ht_contains(const HashTable *ht, const char *key);
bool ht_remove(HashTable *ht, const char *key, void (*free_value)(void *));

size_t ht_count(const HashTable *ht);
double ht_load_factor(const HashTable *ht);

/* Iteration: call fn(key, value, user_data) for every entry.
 * Order is UNSPECIFIED — never rely on any particular iteration order. */
void ht_foreach(const HashTable *ht,
                void (*fn)(const char *key, void *value, void *user_data),
                void *user_data);

#endif
```

**Opaque type design:** notice `HashTable` is declared but never defined in the header — callers only ever handle a `HashTable *` and interact through the provided functions, never touching internal fields directly. This is C's version of encapsulation: the implementation (bucket array, chaining structure, hash function choice) can change freely without breaking any code that uses this header, as long as the function signatures stay the same. This is exactly the same principle behind your `FILE *` usage in Week 8 — you never touched a `FILE`'s internals, only called functions on the pointer.

### Storing Arbitrary Value Types with `void *`

```c
/* Storing integers: must heap-allocate since void* is a pointer, not a value */
int *score = malloc(sizeof(int));
*score = 95;
ht_insert(ht, "alice", score);

int *retrieved = (int *)ht_get(ht, "alice");
if (retrieved != NULL) {
    printf("Alice's score: %d\n", *retrieved);
}

/* Storing structs: same pattern */
typedef struct { char name[50]; int age; } Person;
Person *p = malloc(sizeof(Person));
strcpy(p->name, "Bob");
p->age = 30;
ht_insert(ht, "bob", p);

/* On destroy, provide a free function matching what you stored: */
ht_destroy(ht, free);   /* plain free() works for simple malloc'd values */
```

This `void *` pattern — heap-allocate the value, store the pointer, cast back on retrieval — is the standard C idiom for building generic containers, and you will see it again if you continue toward systems programming (it underlies much of the Linux kernel's internal generic data structures).

---

## 2. Building a Set on Top of a Hash Table

A **set** stores unique keys with no associated value — "is this key present, yes or no?" A set is trivially a hash table where you don't care about the value at all (or use a constant placeholder value):

```c
/* set.h */
#ifndef SET_H
#define SET_H

#include "hashtable.h"

typedef HashTable Set;   /* a Set IS a HashTable, used in a restricted way */

Set *set_create(size_t initial_size);
void set_destroy(Set *s);
bool set_add(Set *s, const char *item);         /* returns true if newly added */
bool set_contains(const Set *s, const char *item);
bool set_remove(Set *s, const char *item);
size_t set_size(const Set *s);

#endif
```

```c
/* set.c */
#include "set.h"

static char SET_PRESENT_MARKER;   /* a single shared dummy value */

Set *set_create(size_t initial_size) {
    return ht_create(initial_size);
}

void set_destroy(Set *s) {
    ht_destroy(s, NULL);   /* NULL: don't try to free the shared marker */
}

bool set_add(Set *s, const char *item) {
    if (ht_contains(s, item)) return false;   /* already present */
    ht_insert(s, item, &SET_PRESENT_MARKER);
    return true;
}

bool set_contains(const Set *s, const char *item) {
    return ht_contains(s, item);
}

bool set_remove(Set *s, const char *item) {
    return ht_remove(s, item, NULL);
}

size_t set_size(const Set *s) {
    return ht_count(s);
}
```

This is a clean illustration of an important design principle: **a set is not a fundamentally different data structure from a hash table — it's a hash table used with a particular discipline (values are irrelevant, only key presence matters).** Recognizing when one structure is a specialization of another (rather than building something entirely new) is a mark of mature engineering judgment.

### Application: Deduplication

```c
/* Remove duplicate strings from an array, preserving first-occurrence order */
int deduplicate(char *arr[], int n) {
    Set *seen = set_create(101);
    int write = 0;

    for (int read = 0; read < n; read++) {
        if (set_add(seen, arr[read])) {    /* true only if this was newly added */
            arr[write++] = arr[read];       /* keep it — first time we've seen it */
        }
    }

    set_destroy(seen);
    return write;   /* new length */
}
```

Without a hash table, deduplication would require an O(n²) nested-loop comparison (checking every element against every previous element) or an O(n log n) sort-then-scan. With a hash-based set, it's O(n) average case — a single pass, checking each element's presence in O(1) average time.

---

## 3. Application: Word Frequency Counter (Revisited)

Recall Week 8's word frequency counter, which used a linear-scan array (`find_or_add`, O(n) per lookup — O(n²) total for n distinct words). A hash table transforms this into O(n) average case total:

```c
void count_word(HashTable *ht, const char *word) {
    int *count = (int *)ht_get(ht, word);
    if (count != NULL) {
        (*count)++;                    /* word seen before — increment in place */
    } else {
        int *new_count = malloc(sizeof(int));
        *new_count = 1;
        ht_insert(ht, word, new_count);   /* first time seeing this word */
    }
}

/* Callback for ht_foreach */
void print_word_count(const char *key, void *value, void *user_data) {
    (void)user_data;
    int count = *(int *)value;
    printf("%-20s %d\n", key, count);
}

void print_all_counts(const HashTable *ht) {
    ht_foreach(ht, print_word_count, NULL);
}
```

Compare this directly to the Week 8 `find_or_add` implementation, which performed a linear scan through every previously-seen word on every single lookup. For a document with thousands of distinct words, this is the difference between a program that completes instantly and one that visibly takes seconds to process — the exact same underlying problem, solved with dramatically better asymptotic behavior once you have the right data structure.

---

## 4. Application: A Simple LRU-Style Cache (Preview)

A cache trades memory for speed: store the results of expensive computations, keyed by their input, so repeated requests for the same input are instant lookups instead of recomputation.

```c
typedef struct {
    HashTable *table;
    int        capacity;
} SimpleCache;

/* Simulate an expensive computation */
long expensive_computation(int n) {
    long result = 1;
    for (int i = 1; i <= n; i++) result *= i;   /* pretend this is slow */
    return result;
}

long cached_computation(SimpleCache *cache, int n) {
    char key[16];
    snprintf(key, sizeof(key), "%d", n);

    long *cached = (long *)ht_get(cache->table, key);
    if (cached != NULL) {
        printf("Cache HIT for %d\n", n);
        return *cached;
    }

    printf("Cache MISS for %d — computing...\n", n);
    long result = expensive_computation(n);

    long *stored = malloc(sizeof(long));
    *stored = result;
    ht_insert(cache->table, key, stored);

    return result;
}
```

This is a genuine, if simplified, preview of caching strategies used throughout real software systems — web servers cache database query results, compilers cache parsed files, your browser caches downloaded resources — and virtually all of them are built on exactly this hash-table-keyed-by-input pattern underneath, sometimes with additional eviction policies (like LRU — Least Recently Used) layered on top when the cache has a bounded size, a topic covered more fully in later systems courses.

---

## 5. Hash Table Iteration — Order Is Unspecified

Unlike an array or a sorted structure, **the order in which `ht_foreach` visits entries is not meaningful** — it depends entirely on the internal hash values and bucket layout, which has nothing to do with insertion order or any natural ordering of the keys:

```c
ht_insert(ht, "zebra", ...);
ht_insert(ht, "apple", ...);
ht_insert(ht, "mango", ...);

ht_foreach(ht, print_word_count, NULL);
/* Output order is UNPREDICTABLE — might print mango, zebra, apple,
 * or any other order, and this order can even change if the table resizes */
```

**Never write code that depends on hash table iteration order.** If you need sorted output, either (a) extract all keys into an array and sort that array separately, or (b) use a different structure entirely — a BST (Week 9) naturally maintains sorted order via inorder traversal, at the cost of O(log n) instead of O(1) average operations. This is a genuine, common engineering tradeoff: **hash tables optimize for lookup speed at the cost of any ordering guarantee; BSTs sacrifice some lookup speed to maintain ordering "for free."**

---

## 6. When to Use a Hash Table (and When Not To)

| Use a hash table when... | Use something else when... |
|---------------------------|------------------------------|
| You need fast lookup/insert/delete by an arbitrary key | You need sorted iteration order — use a BST |
| Key order doesn't matter | You need range queries ("all keys between X and Y") — use a BST |
| Average-case performance is acceptable (worst case is rare for good hash functions) | You need guaranteed worst-case performance — use a balanced tree |
| Memory overhead of chaining/probing is acceptable | Memory is extremely tight and predictable — arrays may be more compact |
| You're implementing a dictionary/map/set-like structure | You need a genuinely small, fixed set of keys — a simple array or switch may be simpler and just as fast in practice |

---

## 7. A Complete Worked Example: Counting Unique Visitors from a Log File

This ties together Week 8 (file I/O) and this appendix (hash tables) into a single realistic program:

```c
#include <stdio.h>
#include <string.h>
#include "hashtable.h"
#include "set.h"

int count_unique_ips(const char *log_filename) {
    FILE *fp = fopen(log_filename, "r");
    if (fp == NULL) {
        perror("fopen");
        return -1;
    }

    Set *unique_ips = set_create(1009);   /* a prime, comfortably larger than expected */
    char line[256];
    char ip[64];

    while (fgets(line, sizeof(line), fp) != NULL) {
        /* Assume log format: "IP_ADDRESS - - [timestamp] ..." */
        if (sscanf(line, "%63s", ip) == 1) {
            set_add(unique_ips, ip);   /* automatically deduplicates */
        }
    }

    int count = (int)set_size(unique_ips);

    set_destroy(unique_ips);
    fclose(fp);

    return count;
}

int main(void) {
    int unique = count_unique_ips("access.log");
    if (unique >= 0) {
        printf("Unique visitors: %d\n", unique);
    }
    return 0;
}
```

Without a hash-based set, counting unique IPs from a large log file would require either sorting the entire dataset first (O(n log n), and requiring the whole file in memory as a sortable array) or an O(n²) nested comparison. The hash-based approach processes the file in a single O(n) average-case pass, using only as much memory as there are genuinely unique IPs — a direct, practical payoff of everything built across this lecture sequence.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Explain why iterating this hash table yields keys in an order unrelated to insertion, and what the order actually depends on.

```c
for (size_t i = 0; i < ht->cap; i++)
    for (Entry *e = ht->buckets[i]; e; e = e->next)
        visit(e->key, e->value);
```

**2. (Explain.)** Explain the opaque-pointer pattern used by this API, and what it buys.

```c
/* hashtable.h */
typedef struct HashTable HashTable;
HashTable *ht_create(size_t initial_cap);
void       ht_destroy(HashTable *ht);
int        ht_put(HashTable *ht, const char *key, int value);
int        ht_get(const HashTable *ht, const char *key, int *out);
```

**3. (Build.)** Write a word-frequency counter using the hash table API: read a file, count each word, and print the ten most frequent. Explain the complexity and where a hash table is and is not the right tool.

**4. (Stretch.)** You must map integer keys 0–999 to values. Explain why a hash table is the wrong choice, and give the general rule for when hashing is worth its overhead.


### Answers

**1.** The loop walks **buckets in index order**, and a key's bucket is `hash(key) % cap` — a value with no relationship to when the key was inserted or to its natural ordering. So the output order depends on:

1. The **hash function** — change it and the order changes entirely.
2. The **current capacity** — the order after a resize differs from before, because every key's bucket is recomputed.
3. **Insertion order within a bucket** — with head insertion, colliding keys come out in reverse insertion order.
4. Under hash randomisation, the **process seed** — so the order differs between runs of the same program on the same data.

The practical rule: **hash table iteration order is unspecified, and you must not depend on it.** A test that asserts a particular output order will pass today and fail after an unrelated insertion triggers a resize.

If you need a deterministic order, collect the entries and **sort them** — O(n log n) on top of the O(n) walk — or use an ordered structure. CPython's dict preserves *insertion* order by keeping a separate dense entries array alongside the sparse index table, which is a deliberate design choice rather than something hashing gives you for free.

**2.** The header declares `struct HashTable` as a **tag only** — an *incomplete type*. Callers may hold `HashTable *` pointers, since every pointer has the same size regardless of what it points at, but they cannot declare a `HashTable` by value, use `sizeof`, or access any field. The full definition lives in `hashtable.c` and nowhere else.

**What it buys:**

1. **Genuine encapsulation.** Callers physically cannot reach inside and corrupt the invariants — not by convention, but because the compiler has no layout to work with. This is C's closest equivalent to `private`.
2. **Freedom to change the representation.** Switching from chaining to open addressing, adding a cached hash, or changing the growth policy requires **no recompilation of callers**, because nothing they compiled depended on the layout. Expose the struct and every field becomes part of your ABI.
3. **Faster builds and fewer header dependencies** — the header need not include whatever the implementation uses.

**The costs:** every instance must be heap-allocated by `ht_create`, since callers cannot size one; there is a pointer indirection on every access; and you must supply a `ht_destroy`, because callers cannot free the parts they cannot see. That last point makes the **ownership contract** explicit, which is a benefit disguised as a cost.

`FILE *` is exactly this pattern, which is why you have never seen inside a `FILE`. So are `pthread_mutex_t` in some implementations and most C library handles.

**3.**

```c
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_count_desc(const void *a, const void *b) {
    const Entry *x = *(const Entry * const *)a, *y = *(const Entry * const *)b;
    if (x->value != y->value) return (y->value > x->value) - (y->value < x->value);
    return strcmp(x->key, y->key);            /* stable tie-break */
}

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: %s FILE\n", argv[0]); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror(argv[1]); return 1; }

    HashTable *ht = ht_create(1024);
    char word[64];
    int c;
    size_t len = 0;

    while ((c = fgetc(f)) != EOF) {              /* int, not char */
        if (isalpha(c)) {
            if (len + 1 < sizeof word) word[len++] = (char)tolower(c);
        } else if (len) {
            word[len] = '\0';
            int n = 0;
            ht_get(ht, word, &n);
            ht_put(ht, word, n + 1);
            len = 0;
        }
    }
    if (len) { word[len] = '\0'; int n = 0; ht_get(ht, word, &n); ht_put(ht, word, n + 1); }
    fclose(f);

    Entry **all = ht_entries(ht);               /* n pointers, caller frees */
    size_t n = ht_size(ht);
    qsort(all, n, sizeof *all, by_count_desc);
    for (size_t i = 0; i < n && i < 10; i++)
        printf("%6d  %s\n", all[i]->value, all[i]->key);

    free(all);
    ht_destroy(ht);
    return 0;
}
```

**Complexity:** Θ(N) to read and count N words — each `ht_get`/`ht_put` is O(1) average — then Θ(n log n) to sort the n distinct words. Since n ≪ N for real text, counting dominates. The alternative of scanning a list for each word would be Θ(N·n).

The hash table is right here because the query is **exact match on a key**. It would be the *wrong* tool for "all words starting with 'pre'" — hashing destroys prefix structure, so that needs a trie — or for "the 10 most frequent" *without* materialising everything, which wants a heap. Note the final sort is necessary precisely because iteration order is unspecified.

For the top 10 specifically, a size-10 min-heap over the entries would be Θ(n log 10) instead of Θ(n log n) — worth it only when n is large.

**4.** Use a **plain array** of 1000 elements. The key *is* the index, so lookup is a single scaled address computation — genuinely O(1) with no hash to compute, no bucket to probe, no collision to resolve, and no pointer to chase. A hash table would compute `hash(k) % cap`, follow a chain or probe, and compare keys, to arrive at a slower version of `arr[k]`. It would also use more memory: an entry per key plus the bucket array, versus 4 KB of `int`s.

This is *direct addressing*, and it is what a hash table degenerates to when the key space is small and dense. Hashing exists to handle key spaces too large to index directly — all strings, all 64-bit integers, arbitrary structs — by compressing them into a manageable range, and that compression is the entire source of its cost and its collisions.

**The rule: use a hash table when the key space is much larger than the number of keys actually stored, and the keys cannot serve as array indices.** Concretely, prefer an array when keys are integers in a known bounded range with reasonable density — a bitmap or array indexed by key beats hashing every time.

Three other cases where hashing is wrong: **small n**, where a linear scan of 10 elements beats computing a hash; **ordered queries** — minimum, range, nearest, prefix — which hashing cannot answer at all, since it deliberately destroys ordering; and **adversarial keys** without a randomised seed, per Lecture 2. Ask what the queries are before choosing the structure.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Opaque type** | A type whose internal structure is hidden from users of the header, exposed only through functions |
| **Set** | A hash table specialization storing only keys (presence testing), no associated values |
| **Deduplication** | Removing duplicate entries from a collection, efficiently solvable via a hash-based set |
| **Cache** | A structure storing precomputed results keyed by input, avoiding redundant recomputation |
| **`void *` generic value pattern** | Storing heap-allocated values of any type behind a `void *`, cast back on retrieval |

---

## Reading

- **CLRS Ch. 11** — Hash Tables (complete chapter, including the mathematical analysis of expected chain length)
- **Sedgewick & Wayne §3.5** — Applications (symbol table use cases, directly relevant to this lecture)

---

*Next: Lab 7 — Building a Complete, Generic Hash Table Library*

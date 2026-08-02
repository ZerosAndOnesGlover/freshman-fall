# PROG 101 · Programming I: Structured Programming in C
## Appendix · Lab 7: Building a Complete, Generic Hash Table Library

**Graded: 20 points**
**Duration:** 2 hours
**Submission:** Push to Git, show TA before leaving

---

## Overview

- **Part 1:** Hash function implementation and distribution testing
- **Part 2:** Complete generic hash table with separate chaining (the main deliverable)
- **Part 3:** Build a Set and a word-frequency application on top of it

---

## Part 1: Hash Functions and Distribution Testing (5 pts)

Create `hashfuncs.h` and `hashfuncs.c`:

```c
#ifndef HASHFUNCS_H
#define HASHFUNCS_H

unsigned long hash_djb2(const char *str);
unsigned long hash_fnv1a(const char *str);
unsigned long hash_naive_sum(const char *str);   /* the deliberately bad one */

#endif
```

Implement all three exactly as shown in Lecture 1.

### Distribution Test

Create `distribution_test.c`. You are given (or must generate) a word list of at least 500 real English words (one per line — you may use `/usr/share/dict/words` on Linux/Mac if available, or construct your own list; a starter list is provided in `resources/wordlist.txt`).

```c
#define TABLE_SIZE 101   /* prime */

typedef struct {
    unsigned long (*fn)(const char *);
    const char *name;
} HashFnEntry;

void test_distribution(unsigned long (*hash_fn)(const char *), const char *name,
                       char words[][64], int n_words) {
    int bucket_counts[TABLE_SIZE] = {0};

    for (int i = 0; i < n_words; i++) {
        unsigned int idx = hash_fn(words[i]) % TABLE_SIZE;
        bucket_counts[idx]++;
    }

    int max_count = 0, empty_buckets = 0;
    long sum_sq_deviation = 0;
    double mean = (double)n_words / TABLE_SIZE;

    for (int i = 0; i < TABLE_SIZE; i++) {
        if (bucket_counts[i] > max_count) max_count = bucket_counts[i];
        if (bucket_counts[i] == 0) empty_buckets++;
        double dev = bucket_counts[i] - mean;
        sum_sq_deviation += (long)(dev * dev);
    }

    double variance = (double)sum_sq_deviation / TABLE_SIZE;

    printf("%-15s max_bucket=%-4d empty=%-4d variance=%.2f\n",
           name, max_count, empty_buckets, variance);
}
```

Run all three hash functions against your word list and print a comparison table. In `LAB 7 Hashtable.md`:

1. Which hash function has the lowest max bucket load? The lowest variance?
2. Test `hash_naive_sum` specifically on the anagram set `{"cat", "act", "tac"}` combined with 20 other random words — what happens, and why does this confirm the lecture's warning about naive sum hashing?
3. Based on your measurements, which hash function would you choose for a production hash table, and why?

---

## Part 2: Complete Generic Hash Table (10 pts)

Build the full `hashtable.h`/`hashtable.c` from Lecture 3, with separate chaining and automatic resizing.

### `hashtable.h`

```c
#ifndef HASHTABLE_H
#define HASHTABLE_H

#include <stddef.h>
#include <stdbool.h>

typedef struct HashTable HashTable;

HashTable *ht_create(size_t initial_size);
void       ht_destroy(HashTable *ht, void (*free_value)(void *));

bool   ht_insert(HashTable *ht, const char *key, void *value);
void  *ht_get(const HashTable *ht, const char *key);
bool   ht_contains(const HashTable *ht, const char *key);
bool   ht_remove(HashTable *ht, const char *key, void (*free_value)(void *));

size_t ht_count(const HashTable *ht);
double ht_load_factor(const HashTable *ht);

void ht_foreach(const HashTable *ht,
                void (*fn)(const char *key, void *value, void *user_data),
                void *user_data);

/* === Diagnostics (for testing/instrumentation) === */

/* Return the number of buckets (table size) currently allocated. */
size_t ht_bucket_count(const HashTable *ht);

/* Return the length of the longest chain in any single bucket
 * (useful for verifying distribution quality and resize behavior). */
int ht_max_chain_length(const HashTable *ht);

#endif
```

### Implementation Requirements

- Use `hash_djb2` from Part 1 as the internal hash function
- Automatic resize (double the bucket count) when load factor exceeds 0.75, exactly as shown in Lecture 2
- `ht_insert` on an existing key updates the value (does NOT create a duplicate entry) — if `free_value` semantics matter for the old value, that's the caller's responsibility to manage (document this clearly in your header comment)
- All string keys must be heap-copied (`strdup` or equivalent) — the caller's original key string is never assumed to outlive the insert call
- `ht_destroy` must free every key, every chain node, the bucket array, and the table struct itself — zero leaks
- Table sizes should be chosen from a small set of prime numbers as it grows (you may hardcode a short list of primes to cycle through on resize, e.g., 11, 23, 47, 97, 197, 397, 797, 1597, ... or compute the next prime programmatically — either is acceptable)

### `test_hashtable.c`

Write comprehensive tests:

```c
void test_basic_operations(void) {
    /* insert, get, contains, remove — verify correctness for a handful of keys */
}

void test_update_existing_key(void) {
    /* insert "x" -> value1, insert "x" -> value2, verify get("x") returns value2,
     * and verify ht_count did NOT increase on the second insert */
}

void test_collision_handling(void) {
    /* Deliberately insert keys you've confirmed collide (same hash % initial_size)
     * and verify ALL of them are retrievable correctly despite the collision */
}

void test_resize_behavior(void) {
    /* Insert enough keys to trigger at least 2 resizes.
     * Verify ht_bucket_count increased.
     * Verify EVERY previously-inserted key is STILL retrievable correctly
     * after the resize (this is the critical correctness property —
     * resizing must never lose or corrupt data).
     * Verify ht_load_factor stays below 0.75 after each resize. */
}

void test_deletion(void) {
    /* Insert several keys, delete one, verify:
     *   - ht_contains returns false for the deleted key
     *   - ht_count decreased by 1
     *   - all OTHER keys are still retrievable (deletion didn't corrupt the chain)
     * Also test: removing a non-existent key returns false, no crash. */
}

void test_foreach(void) {
    /* Insert N known keys with known values.
     * Use ht_foreach with a callback that accumulates into a counter/sum.
     * Verify every key was visited exactly once (e.g., sum of values matches
     * expected total, and a visited-count matches N). */
}

void test_empty_table(void) {
    /* Operations on a freshly created, empty table:
     *   ht_get returns NULL, ht_contains returns false,
     *   ht_remove returns false, ht_count is 0, no crashes. */
}
```

### Valgrind Requirement

```bash
valgrind --leak-check=full ./test_hashtable
```

Zero errors, zero leaks — including after resize operations (a common source of leaks if the old bucket array or old chain nodes aren't properly freed during rehashing).

---

## Part 3: Set and Word Frequency Application (5 pts)

### `set.h` / `set.c`

Implement the complete `Set` API from Lecture 3, built on top of your `hashtable.c`.

```c
#ifndef SET_H
#define SET_H

#include "hashtable.h"
#include <stdbool.h>

typedef HashTable Set;

Set   *set_create(size_t initial_size);
void   set_destroy(Set *s);
bool   set_add(Set *s, const char *item);
bool   set_contains(const Set *s, const char *item);
bool   set_remove(Set *s, const char *item);
size_t set_size(const Set *s);

/* Set algebra — bonus-worthy but implement if time allows */
Set *set_union(const Set *a, const Set *b);
Set *set_intersection(const Set *a, const Set *b);

#endif
```

### `word_frequency.c`

Reimplement Week 8's word frequency counter using your hash table instead of the O(n) linear-scan array. Take a text filename as `argv[1]`.

```c
void count_words_from_file(HashTable *ht, const char *filename);
void print_top_n_words(const HashTable *ht, int n);   /* extract, sort by count, print top n */
```

Requirements:
- `print_top_n_words` must extract all entries (via `ht_foreach` accumulating into an array), sort them by count descending (reuse your Week 9 sorting knowledge — a simple approach is fine here), then print the top n
- Demonstrate on a text file of at least 200 words, printing the top 10 most frequent words with counts
- Compare timing (informally, or using `clock()`/`time` command) against the Week 8 O(n)-lookup version on a large input, if you want to see the practical difference (optional but illuminating)

### Deduplication Demo

Using your `Set`, write a small demo that reads a file line-by-line and prints only unique lines (removing duplicates), preserving first-occurrence order — reusing the pattern from Lecture 3.

---

## Deliverables

```
week7/lab7/
├── hashfuncs.h
├── hashfuncs.c
├── distribution_test.c
├── wordlist.txt              # at least 500 words (provided or self-sourced)
├── hashtable.h
├── hashtable.c
├── test_hashtable.c
├── set.h
├── set.c
├── word_frequency.c
├── dedup_lines.c
├── sample_text.txt           # test fixture, 200+ words
├── Makefile
└── LAB 7 Hashtable.md
```

**Makefile:**
```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

all: distribution_test test_hashtable word_frequency dedup_lines

distribution_test: distribution_test.o hashfuncs.o
	$(CC) $(CFLAGS) -o $@ $^

test_hashtable: test_hashtable.o hashtable.o hashfuncs.o
	$(CC) $(CFLAGS) -o $@ $^

word_frequency: word_frequency.o hashtable.o hashfuncs.o
	$(CC) $(CFLAGS) -o $@ $^

dedup_lines: dedup_lines.o hashtable.o hashfuncs.o set.o
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f distribution_test test_hashtable word_frequency dedup_lines *.o

.PHONY: all clean
```

---

## Grading

| Part | Points | Criteria |
|------|--------|---------|
| 1: Hash functions + distribution test | 5 | All 3 implemented correctly, meaningful analysis in notes |
| 2: Hash table implementation | 6 | Correct chaining, correct resize, correct deletion with tombstone-free chaining |
| 2: Test suite | 3 | Comprehensive, especially resize correctness |
| 2: Valgrind clean | 1 | 0 errors, 0 leaks |
| 3: Set + applications | 5 | Correct Set API, working word frequency and dedup demos |
| **Total** | **20** | |
| Bonus: set_union/set_intersection | 2 | |

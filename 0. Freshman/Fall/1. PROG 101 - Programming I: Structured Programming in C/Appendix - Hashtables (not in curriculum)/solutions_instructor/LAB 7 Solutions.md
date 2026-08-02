# PROG 101 — this appendix
## LAB 7 Solutions — INSTRUCTOR ONLY

> **Every implementation below compiles under `gcc -Wall -Wextra -Werror -std=c11` and runs clean
> under `-fsanitize=address,undefined`.** Where the lab requires it, Valgrind output is quoted
> verbatim. Reject any submission that does not build warning-free — `-Werror` is not negotiable in
> this course.

---

## Part 1 — Hash Functions and Distribution Testing

The measurement students must produce, and the interpretation:

**A character sum is a bad hash for two independent reasons.**

1. **It ignores order.** Addition is commutative, so every anagram collides — `listen`, `silent`,
   and `enlist` all land in the same bucket. Verified: all three give `655` mod 1000, while djb2
   gives 636 / 796 / 716.
2. **Its range is far too narrow.** Lowercase ASCII is 97–122, so a 6-letter word sums to roughly
   580–730 — about 150 reachable buckets out of 1000, regardless of how many words you insert.

djb2 (`h = h*33 + c`, seeded 5381) fixes both: multiplying before adding makes each character's
contribution depend on its position, so order matters and one changed character cascades.

**The statistic to require is the variance-to-mean ratio of bucket counts.** Under ideal uniform
hashing the counts are Poisson, whose variance equals its mean, so a ratio near **1.0** indicates a
good hash. Comparing *average* chain length is useless — it equals α by definition for any hash
whatsoever, good or catastrophic. It is the **spread** that distinguishes them. Supporting checks:
empty-bucket fraction ≈ e^−α, and longest chain O(log n / log log n).

---

## Part 2 — `hashtable` Reference Implementation

Opaque `HashTable`, `char*` keys heap-copied, `void*` values, chaining, resize at α > 0.75.
**Valgrind-clean: 129 allocs, 129 frees, 0 errors.**

Verified resize trace and behaviour:

```
initial buckets=8
  count= 7 -> buckets  8->16
  count=13 -> buckets 16->32
  count=25 -> buckets 32->64
  final: count=40 buckets=64 load=0.625 maxchain=2

get("key7") = 700 ; get("nope") = NULL ; contains(key0)=1 contains(zzz)=0
update existing key: count 40 -> 40 (unchanged), value replaced
remove(key3)=1  remove(key3 again)=0  count=39
foreach visited 39 entries
empty table: count=0 load=0.00 maxchain=0 get=NULL remove=0
ht_destroy(NULL) safe
```

### Key implementation points

```c
static bool ht_resize(HashTable *h) {
    size_t ncap = h->nbuckets * 2;
    Entry **nb = calloc(ncap, sizeof *nb);
    if (!nb) return false;                    /* old table stays valid on failure */
    for (size_t i = 0; i < h->nbuckets; i++) {
        Entry *e = h->buckets[i];
        while (e) {
            Entry *next = e->next;            /* save before relinking */
            size_t b = e->hash % ncap;        /* CACHED hash — no recompute */
            e->next = nb[b]; nb[b] = e;       /* move the node itself */
            e = next;
        }
    }
    free(h->buckets); h->buckets = nb; h->nbuckets = ncap;
    return true;
}
```

- **Entries must be rehashed, not copied.** A key's bucket is `hash % nbuckets`, and `nbuckets` has
  changed. The hash value itself is unchanged; the *mapping from hash to bucket* is what moves.
  Copying chains wholesale leaves keys in buckets that lookup will never probe — present in the
  table, permanently unfindable, with no error.
- **Cache the hash in the entry.** Avoids recomputing `djb2(key)` for every key on every resize,
  and lets lookup compare integers before calling `strcmp`.
- **Relink existing nodes** rather than allocating new ones: the resize performs no per-entry
  allocation and cannot fail partway through leaving the table inconsistent.
- **Keys must be heap-copied** (`strdup` or equivalent) — the handout is explicit that the caller's
  string is not assumed to outlive the call. Storing the caller's pointer is a dangling-pointer bug
  that will pass every test using string literals and fail on a `char buf[]` reused in a loop.
- **`ht_insert` on an existing key updates in place** and must not increment `count`. Verified:
  count stayed at 40.

**Amortised O(1) insertion.** Resizing at capacity k costs Θ(k), and doubling puts resizes at
8, 16, 32, …, so total rehashing across n insertions is bounded by 2n. The individual insertion
that triggers a resize is Θ(n), which is why hash tables are a poor fit for hard real-time code.

### The Valgrind checklist for `ht_destroy`

Every one of these must be freed, and students routinely miss the middle two:

1. each entry's **key** string,
2. each **entry** node,
3. the **bucket array**,
4. the **table struct** itself.

`ht_destroy(NULL, free)` must be safe, and the `free_value` callback must be honoured — passing
`NULL` means the caller retains ownership of the values.

---

## Part 3 — Set and Word Frequency

A `Set` is a hash table with only keys — implement it **on top of** `HashTable` with a `NULL` or
sentinel value rather than duplicating the whole structure. A student who copy-pastes the hash table
to build the set has missed the reuse point of the exercise.

**Word frequency:** read with `fgetc` into a buffer, lowercase, split on non-alphabetic characters,
and use `ht_get`/`ht_insert` to accumulate counts. Θ(N) for N words, versus Θ(N·n) for a list scan.

- **`int c`, never `char c`, for `fgetc`** — the return range is 0–255 *plus* `EOF` (−1), which does
  not fit in a `char`, and byte 0xFF would compare equal to `EOF` and truncate the file early.
- Counts stored as `void*` need either heap-allocated `int`s (freed by `ht_destroy(ht, free)`) or
  the `intptr_t` cast trick — **document which**, because the ownership contract differs.
- Sorting the results requires collecting entries via `ht_foreach` into an array, then `qsort`.
  **Iteration order is unspecified** and depends on the hash function, the current capacity, and
  insertion order within each bucket, so the sort is not optional if the output must be stable.

**Deduplication demo:** inserting n items into a set and reporting the count is Θ(n) against Θ(n²)
for a list-based scan. The measured contrast is the payoff of the whole week.

---

## Marking Scheme

Points follow the allocation printed on the handout. Within each part:

- **Correctness (≈50%).** Passes the required test cases *and* the edge cases listed above.
- **Memory discipline (≈30%).** No leaks, no invalid reads/writes, every `malloc` checked, every
  owner documented. For labs with a Valgrind requirement this is pass/fail: **0 errors, 0 leaks.**
- **Method (≈20%).** Required technique actually used, bounds asserted, `const` applied where the
  function only reads.

**Automatic deductions, regardless of output:**
- Any compiler warning under `-Wall -Wextra`.
- Unchecked `malloc`/`realloc` return.
- `realloc` result assigned directly back to the original pointer (leaks the block on failure).
- A buffer function that can leave its output unterminated.

**Carry-through.** One wrong helper used consistently downstream costs marks once.

---

*PROG 101 · Appendix · Lab Solutions · Instructor Copy · © CSE Department*

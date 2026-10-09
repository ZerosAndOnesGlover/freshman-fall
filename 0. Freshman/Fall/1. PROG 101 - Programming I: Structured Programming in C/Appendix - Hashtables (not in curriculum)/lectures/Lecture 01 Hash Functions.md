# PROG 101 · Programming I: Structured Programming in C
## Appendix · Lecture 1: Hash Functions and the Hashing Problem

*“Associative arrays are very very useful things and if you are only going to have one data structure that's the one to have. Because you could build everything else with it if you want.”* — Brian Kernighan, "Coffee with Brian Kernighan", Computerphile (2018)

**Reading:** CLRS Ch. 11 · Sedgewick & Wayne, Algorithms 4th ed. *(details at the end of the lecture)*

---

## Lecture Goals

By the end of this lecture you will:
- Understand the problem a hash table solves and why it beats arrays and linked lists for lookup
- Implement several real hash functions from scratch and understand their design
- Know the properties that make a hash function "good"
- Understand collisions as an unavoidable mathematical consequence of hashing
- Compute a hash table index correctly and understand the role of table size

---

## 1. The Problem: Fast Lookup by Key

Every data structure you've built so far has a lookup weakness:

| Structure | Search by value | Search by index |
|-----------|-----------------|------------------|
| Array | O(n) linear scan (or O(log n) if sorted, via binary search) | O(1) |
| Linked list | O(n) linear scan | O(n) to reach position i |
| BST | O(log n) average, O(n) worst case | — |

What if you want O(1) average-case lookup **by an arbitrary key** — not a numeric index, but a string like `"alice"`, or an employee ID, or a product SKU — with the simplicity of an array access?

This is exactly what a **hash table** provides. The core idea: use a **hash function** to convert any key into an array index, then store (and retrieve) the value at that index. If the hash function is good and the table is sized appropriately, this gives O(1) average-case insert, search, and delete — a dramatic improvement over every structure you've built so far, for this specific access pattern.

```
              hash("alice")  →  index 7
"alice" ──────────────────────────────▶  table[7] = <alice's data>

              hash("bob")    →  index 2
"bob"   ──────────────────────────────▶  table[2] = <bob's data>
```

This is precisely how Python dictionaries, JavaScript objects, and virtually every "map"/"dictionary" type in every modern language work under the hood.

---

## 2. What a Hash Function Does

A **hash function** takes a key (of any type — a string, an integer, a struct) and produces a fixed-size integer, called the **hash value** or **hash code**:

```c
unsigned long hash_function(const char *key);
```

To turn this hash value into a valid array index for a table of size `TABLE_SIZE`, you take the modulo:

```c
unsigned int index = hash_function(key) % TABLE_SIZE;
```

The modulo operation compresses the (potentially enormous) hash value down into the range `[0, TABLE_SIZE - 1]` — a valid array index.

---

## 3. Properties of a Good Hash Function

**1. Deterministic:** the same key must always produce the same hash value, every time, in every run of the program. (Without this, you could never find a key you previously inserted.)

**2. Uniform distribution:** across the space of realistic keys your program will see, the hash values should spread out roughly evenly across the output range — avoiding clustering that causes many keys to collide (map to the same index).

**3. Fast to compute:** the hash function is computed on every insert, search, and delete — it must be cheap, ideally O(k) where k is the key's size (e.g., string length), not something dramatically more expensive.

**4. Avalanche effect (for cryptographic-quality hashes — not strictly required for hash tables, but a hallmark of good design):** a tiny change in the input (flipping one bit) should produce a dramatically different output hash. This helps avoid subtle clustering patterns for keys that are "similar" (e.g., `"item1"`, `"item2"`, `"item3"`).

---

## 4. Hashing Integers

The simplest possible hash function for an integer key is the identity function itself:

```c
unsigned int hash_int(int key) {
    return (unsigned int)key;   /* modulo TABLE_SIZE happens at the call site */
}
```

This works reasonably well **if** your keys are already well-distributed (e.g., random IDs). It works **poorly** if your keys have patterns that interact badly with your table size — for example, if all your keys are multiples of 16 and your table size is also a power of 2, every key collides into the same small set of buckets (because `(16k) % 2^m` only ever hits a fraction of the possible indices).

**This is exactly why table sizes are conventionally chosen to be prime numbers** — a prime table size avoids many of these pathological interactions with patterned integer keys, spreading them out more evenly regardless of the key's internal structure.

A slightly more robust integer hash mixes the bits further:
```c
unsigned int hash_int_mixed(int key) {
    unsigned int x = (unsigned int)key;
    x = ((x >> 16) ^ x) * 0x45d9f3b;
    x = ((x >> 16) ^ x) * 0x45d9f3b;
    x = (x >> 16) ^ x;
    return x;
}
```
This "bit-mixing" technique (a simplified version of a well-known integer hash finalizer) scrambles the input bits thoroughly, defending against patterned inputs that would defeat a naive identity hash.

---

## 5. Hashing Strings — Building It From Scratch

Strings are the most common key type in practice. Here are three real, widely-used string hash functions, each illustrating a different design idea.

### djb2 — Dan Bernstein's Classic Hash

```c
unsigned long hash_djb2(const char *str) {
    unsigned long hash = 5381;    /* a "magic" starting value, chosen empirically */
    int c;

    while ((c = *str++) != '\0') {
        hash = ((hash << 5) + hash) + (unsigned char)c;   /* hash * 33 + c */
    }
    return hash;
}
```

**Why `hash * 33`?** `(hash << 5) + hash` computes `hash * 32 + hash = hash * 33`. Multiplying by an odd number (33) and adding each character mixes the bits well across the whole hash value as the string is consumed, so that similar strings (e.g., "cat" vs "cats") produce very different hash values. This function is famous precisely because of its combination of simplicity and surprisingly good real-world distribution — it remains in wide use today (including inside real production hash table implementations) despite being trivially simple to write.

### FNV-1a — Fowler/Noll/Vo Hash

```c
unsigned long hash_fnv1a(const char *str) {
    unsigned long hash = 2166136261UL;   /* FNV offset basis */
    int c;

    while ((c = *str++) != '\0') {
        hash ^= (unsigned char)c;         /* XOR the byte in first */
        hash *= 16777619UL;               /* then multiply by the FNV prime */
    }
    return hash;
}
```

FNV-1a alternates XOR and multiplication, another well-studied technique for spreading bit patterns evenly. It is widely used in production systems (compilers, databases, networking code) because of its excellent speed-to-quality ratio.

### The Naive (Bad) Hash — For Contrast

```c
/* DO NOT USE — included only to illustrate what a POOR hash function looks like */
unsigned long hash_naive_sum(const char *str) {
    unsigned long hash = 0;
    while (*str) {
        hash += (unsigned char)(*str++);   /* just sums the character values */
    }
    return hash;
}
```

**Why this is bad:** anagrams collide. `"cat"` and `"act"` and `"tac"` all sum to the exact same value, since addition is commutative and order doesn't matter to a simple sum. In a real dataset with many similar/related strings, this causes severe clustering — defeating the entire purpose of hashing. This function is included specifically so you can *measure* how much worse it performs compared to djb2/FNV-1a in this week's lab.

---

## 6. Collisions Are Mathematically Unavoidable

A hash function maps a (typically enormous, even infinite) space of possible keys down into a small, fixed number of table slots (`TABLE_SIZE`). By the **pigeonhole principle**: if you have more possible keys than table slots (which is essentially always true — there are infinitely many possible strings, but a finite table), **some distinct keys must map to the same index.** This is called a **collision**, and it is not a bug or a sign of a bad hash function — it is an unavoidable mathematical consequence of compressing a large space into a small one.

```
hash("alice") % 10  →  3
hash("carol") % 10  →  3     ← COLLISION: different keys, same index
```

**The entire design challenge of a hash table is not "how do we avoid collisions" (impossible) but "how do we handle them gracefully when they occur."** This is the subject of Lecture 2.

### The Birthday Paradox Intuition

A useful intuition for how *quickly* collisions become likely: this is the same mathematics behind the famous "birthday paradox" (in a room of just 23 people, there's already a >50% chance two share a birthday, out of 365 possible days). Similarly, in a hash table, you don't need to fill anywhere close to `TABLE_SIZE` entries before collisions become likely — they start appearing quite early, well before the table is "full." This is precisely why a hash table's efficiency depends critically on how it handles collisions, not on avoiding them.

---

## 7. Measuring Distribution Quality

You can empirically test how well a hash function distributes keys by hashing a realistic dataset and counting how many keys land in each bucket:

```c
#define TABLE_SIZE 101   /* a prime number */

void test_distribution(unsigned long (*hash_fn)(const char *),
                       const char *keys[], int n_keys) {
    int bucket_counts[TABLE_SIZE] = {0};

    for (int i = 0; i < n_keys; i++) {
        unsigned int index = hash_fn(keys[i]) % TABLE_SIZE;
        bucket_counts[index]++;
    }

    int max_count = 0, empty_buckets = 0;
    for (int i = 0; i < TABLE_SIZE; i++) {
        if (bucket_counts[i] > max_count) max_count = bucket_counts[i];
        if (bucket_counts[i] == 0) empty_buckets++;
    }

    printf("Max bucket load: %d, Empty buckets: %d / %d\n",
           max_count, empty_buckets, TABLE_SIZE);
}
```

A good hash function on realistic data produces a low max bucket load (few keys piled into any single bucket) and few empty buckets (keys are spread evenly, not clustered into a subset of the table). You will perform exactly this measurement in this week's lab, comparing the naive sum hash against djb2 and FNV-1a on real data — the difference is dramatic and makes the abstract "good hash function" properties concrete and visible.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Hash these five words with both functions and compare the bucket distributions for `size = 1000`.

```c
unsigned charsum(const char *s) { unsigned h = 0; while (*s) h += (unsigned char)*s++; return h; }
unsigned djb2(const char *s)   { unsigned h = 5381; while (*s) h = h*33 + (unsigned char)*s++; return h; }
```

Words: `listen`, `silent`, `enlist`, `hello`, `world`.

**2. (Explain.)** State the three properties of a good hash function, and explain why "collisions are unavoidable" is a mathematical fact rather than an implementation weakness.

**3. (Build.)** Implement `djb2` and a modulo-based bucket index, then write a function that measures distribution quality over a word list. What statistic tells you the hash is good?

**4. (Stretch.)** Explain why table sizes are commonly chosen as either a prime or a power of two, what each choice requires of the hash function, and why `% nbuckets` with a power-of-two size can be catastrophic.


### Answers

**1.** | Word | `charsum % 1000` | `djb2 % 1000` |
|---|---|---|
| listen | **655** | 636 |
| silent | **655** | 796 |
| enlist | **655** | 716 |
| hello | 532 | 937 |
| world | 552 | 645 |

**All three anagrams collide under `charsum`** and none under `djb2`.

The cause is that addition is **commutative**, so a character sum cannot distinguish permutations. Every anagram class in the dictionary maps to one bucket — a large, systematic, and entirely predictable cluster.

`djb2` multiplies the running hash by 33 **before** adding each character, so a character's contribution depends on its position: the first character has been multiplied by 33ⁿ⁻¹ by the end. Order now matters, and a single changed character cascades through the whole value.

`charsum` has a second, independent defect: **range**. Lowercase ASCII is 97–122, so a 6-letter word sums to roughly 580–730 — about 150 reachable values out of 1000 buckets. Most of the table is unreachable no matter how many words you insert, so the load is concentrated regardless of the load factor.

The multiplier 33 is odd and coprime to any power-of-two table size, which is what keeps the low bits well mixed. Bernstein's choice of 5381 and 33 is empirical, and it remains a good default for short string keys.

**2.** **1. Deterministic.** The same key must always produce the same hash within a run. Without this a lookup cannot find what an insert stored.

**2. Uniform.** Keys should spread evenly across buckets, so no bucket carries a disproportionate share. Uniformity is what makes the *average* chain length α and therefore lookup O(1).

**3. Fast.** The hash is computed on every insert, lookup, and delete. A hash slower than the linear scan it replaces is pointless — which is why cryptographic hashes like SHA-256 are the wrong tool for a hash table.

(A fourth, the *avalanche* property — one input bit changing flips about half the output bits — is how uniformity is achieved in practice.)

**Collisions are unavoidable by the pigeonhole principle.** A hash function maps an infinite set of possible keys — all strings — onto a finite set of hash values (2³² for an `unsigned`), and then onto an even smaller set of buckets. Mapping infinitely many things into finitely many boxes forces some box to hold more than one. No cleverness escapes it; a collision-free hash over an unbounded key space is impossible in principle.

So a hash function's job is **not** to avoid collisions but to make them *rare and unpredictable*, and the table's job is to **resolve** the ones that occur (Lecture 2). The birthday paradox sharpens how rare "rare" can be: with 1000 buckets, a collision becomes more likely than not after only about 38 keys — which is why resolution is mandatory, not optional.

**3.**

```c
#include <stdlib.h>
#include <math.h>

unsigned djb2(const char *s) {
    unsigned h = 5381;
    while (*s) h = h * 33u + (unsigned char)*s++;
    return h;
}

size_t bucket(const char *s, size_t nbuckets) {
    return djb2(s) % nbuckets;
}

void report(char **words, size_t n, size_t nbuckets) {
    size_t *counts = calloc(nbuckets, sizeof *counts);
    if (!counts) return;
    for (size_t i = 0; i < n; i++) counts[bucket(words[i], nbuckets)]++;

    size_t empty = 0, longest = 0;
    double sumsq = 0;
    for (size_t b = 0; b < nbuckets; b++) {
        if (counts[b] == 0) empty++;
        if (counts[b] > longest) longest = counts[b];
        sumsq += (double)counts[b] * counts[b];
    }
    double alpha = (double)n / nbuckets;
    printf("alpha=%.2f  empty=%.1f%%  longest=%zu  var/mean=%.2f\n",
           alpha, 100.0 * empty / nbuckets, longest,
           (sumsq / nbuckets - alpha * alpha) / alpha);
    free(counts);
}
```

The statistic that matters is the **variance-to-mean ratio of the bucket counts**. Under ideal uniform hashing the counts follow a Poisson distribution, whose variance equals its mean — so a ratio near **1.0** indicates a good hash. `charsum` gives a ratio far above 1: a few enormous buckets and mostly empty ones.

Two supporting checks: the **empty-bucket fraction** should be about e^−α (≈ 37% at α = 1), and the **longest chain** should be O(log n / log log n), not O(n).

Comparing the *average* chain length is useless — it is α by definition for any hash whatsoever, good or catastrophic. It is the **spread** that distinguishes them.

**4.** **Prime size.** `h % p` for prime `p` mixes in contributions from *all* bits of `h`, because `p` shares no factors with any structure in the key space. It is forgiving of a mediocre hash — even a weak one distributes acceptably. The cost is that `%` on a variable is an integer division, typically 20–40 cycles, and it is on every operation.

**Power-of-two size.** `h % 2^k` compiles to `h & (2^k - 1)` — a single-cycle AND. Fast, and it makes resizing clean, since doubling redistributes each bucket into exactly two.

**The catastrophe** is that masking keeps only the **low k bits** and discards everything else. If the hash has poor entropy in its low bits, the table collapses. A hash returning the key itself, with keys that are all multiples of 16 (pointers, aligned offsets, IDs stepped by a constant), sends every key to the same handful of buckets — while the *same keys* with a prime modulus spread fine. Java's `HashMap` hit exactly this and now applies `h ^= (h >>> 16)` to fold the high bits down before masking.

So: **power-of-two sizes require a hash with good avalanche**, since only the low bits survive. Prime sizes tolerate a weaker hash but pay for the division.

Modern practice favours power-of-two plus a strong finalising mix — it is what CPython, Java, and Rust's `HashMap` all do — because a good hash is cheaper than a division and is needed for other reasons anyway. If you use a power-of-two table with a homemade hash, **test the low bits specifically**; that is where the failure hides.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Hash table** | A data structure providing average-case O(1) lookup, insert, delete by key |
| **Hash function** | A function converting a key into a fixed-size integer (the hash value) |
| **Hash value / hash code** | The integer output of a hash function |
| **Bucket / slot** | One position in the hash table's underlying array |
| **Collision** | Two distinct keys hashing to the same bucket index |
| **Load factor** | The ratio of stored elements to table size — a key measure of hash table efficiency |
| **Uniform distribution** | A hash function property: keys spread evenly across all buckets |
| **Pigeonhole principle** | The mathematical fact guaranteeing collisions are unavoidable when key space exceeds table size |

---

## Reading

- **CLRS Ch. 11** — Hash Tables (the rigorous mathematical treatment)
- **Sedgewick & Wayne, Algorithms 4th ed.** — §3.4 (Hash Tables) — excellent practical exposition
- djb2 hash: http://www.cse.yorku.ca/~oz/hash.html (Dan Bernstein's original writeup, classic reading)

---

*Next: Lecture 2 — Collision Resolution: Chaining and Open Addressing*

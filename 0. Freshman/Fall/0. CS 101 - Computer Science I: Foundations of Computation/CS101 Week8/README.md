# CS 101 · Week 8: Data Structures II — Hash Tables and Sets

---

## Contents

```
CS101_Week8/
│
├── README.md                                    ← You are here
│
├── lectures/
│   ├── L25 Hash Tables Fundamentals.md          ← Wed: the hashing idea, Python's dict/set,
│   │                                                 hashable vs unhashable, __hash__/__eq__
│   │                                                 contract, word frequency O(n) vs O(n²)
│   ├── L26 Collision Resolution and Resizing.md ← Thu: chaining, open addressing + tombstones,
│   │                                                 load factor, resizing, amortized O(1),
│   │                                                 hash-flooding security note
│   └── L27 Practical Dict and Set Mastery.md    ← Fri: counting/grouping/dedup/complement-
│                                                     search/anagram/memoization patterns,
│                                                     list vs set vs dict decision framework
│
├── lab/
│   ├── LAB 8 Hash Tables from Scratch.md         ← Tue of W9: build both hash table variants,
│   │                                                 load-factor experiments, amortized
│   │                                                 insertion verification, dict vs list
│   │                                                 benchmark, hash/eq contract investigation
│   └── hash_table_starter.py                    ← Lab starter — both variants + resize
│                                                     integrity test suite
│
├── assignments/
│   ├── QUIZ 8 Week 8 Wednesday.md                  ← In-class quiz (covers Week 7)
│   ├── PS 8 Hash Tables and Dictionaries.md      ← Problem Set 8 (due Friday Week 9)
│   └── ps8_starter.py                           ← Full scaffold: hash table extensions,
│                                                     6 refactored algorithms, two-sum family,
│                                                     memoization decorators, set theory
│
├── resources/
│   └── Reading Guide Week 8.md                   ← 3 experimentation sessions, complexity
│                                                      reference card, self-test, Project 1 +
│                                                      Week 9 reminder
│
└── solutions_instructor/
    └── LAB 8 Solutions.md                        ← Expected answers and marking notes
```

---

## Week 8 at a Glance

**Theme:** The most practically important data structure in computing. Every "how do I make this faster" question in real software eventually leads here — hash tables convert O(n) search into O(1) average lookup by computing locations instead of searching for them.

| Day | Event | Topic |
|-----|-------|-------|
| Wed | Lecture 25 + Quiz 8 | The hashing idea; Python dict/set; hashable vs unhashable; hash/eq contract |
| Thu | Lecture 26 | Collision resolution: chaining vs open addressing; load factor; resizing |
| Fri | Lecture 27 + PS8 released | Practical patterns: counting, grouping, complement search, memoization |
| Tue (W9) | Lab 8 (graded) | Build both hash table variants from scratch; empirical load-factor/speedup analysis |

**📌 Project 1 is due this Friday (end of Week 9)** — if you haven't started, begin immediately. See Week 7's `PROJECT 1 Data Analysis Tool.md`.

---

## Your To-Do List

### Before Wednesday
- [ ] Review Week 7 — Quiz 8 covers ADTs, dynamic arrays, linked lists, stacks/queues
- [ ] Skim CLRS Ch. 11.1 (direct-address tables) for conceptual warm-up

### Wednesday
- [ ] Quiz 8 (10 min — covers Week 7)
- [ ] Notes for L25

### Before Thursday
- [ ] REPL Session A from Reading Guide (hash determinism and randomization)
- [ ] Read CLRS Ch. 11.2–11.3 (chaining, hash functions)

### Thursday
- [ ] Notes for L26
- [ ] Read CLRS Ch. 11.4 (open addressing)

### Tuesday Lab, Week 9 (Required, Graded)
- [ ] Build both `ChainedHashTable` and `OpenAddressingHashTable` — full test suite passes
- [ ] Run load-factor experiments and record analysis
- [ ] Verify amortized O(1) insertion empirically
- [ ] Run the dict-vs-list membership benchmark
- [ ] Complete the `__hash__`/`__eq__` contract investigation
- [ ] TA checkoff

### Friday
- [ ] Notes for L27
- [ ] REPL Session B and C (measure speedup directly; build complement-search pattern)
- [ ] PS8 released — read completely

### Weekend
- [ ] Start PS8 — at minimum A1–A2 (written) and B2 (refactoring exercises)
- [ ] **Continue Project 1** — should be well underway by now; due end of next week

---

## The Central Ideas of Week 8

**1. Hash tables compute location instead of searching for it.**
`index = hash(key) % table_size` turns "where is this element?" from a search problem into an arithmetic problem — the foundation of O(1) average-case lookup.

**2. Collisions are mathematically guaranteed, not a design flaw.**
By the pigeonhole principle, once you have more possible keys than buckets, some must share a bucket. The engineering question is HOW you handle that gracefully — chaining (a list per bucket) or open addressing (probe for another slot).

**3. Load factor is THE critical health metric.**
Too high, and both chaining (longer chains) and open addressing (longer probe sequences) degrade toward O(n). Python's dict keeps load factor bounded via automatic resizing — the exact same amortized-O(1) mathematics as Week 6's dynamic array analysis.

**4. Hashability requires immutability — and a strict contract.**
If `a == b`, then `hash(a) == hash(b)` must hold, or dict/set behavior silently corrupts. This is why lists (mutable) are unhashable, while tuples (immutable) are — and why custom classes must define `__hash__` alongside `__eq__`.

**5. The master pattern: trade O(n) space for a collapse from O(n²)/O(n) to O(n)/O(1).**
Counting, grouping, deduplication, complement search, anagram detection, memoization — every pattern this week follows the same shape: build a hash-based lookup structure once, then every subsequent check is O(1) average instead of a re-scan.

**6. Dict/set are not a universal speedup.**
They solve "fast exact-match lookup" specifically. They do not help with finding max/min, maintaining sorted order, or range queries — those need different structures entirely (sorting, trees — later weeks).

---

## Quick Self-Check

Without notes:

1. What does a hash function do, and what three properties should it have?
2. Why is `hash([1,2,3])` an error?
3. State the `__hash__`/`__eq__` contract precisely.
4. What is a collision? Name the principle proving they're unavoidable.
5. Compare chaining and open addressing on: memory overhead, degradation at high load factor.
6. What is a tombstone, and why does open addressing need one but chaining doesn't?
7. What is load factor? What threshold does Python's dict use (roughly), and why is open addressing's threshold typically lower than chaining's?
8. State the "complement lookup" pattern and name two problems it solves.
9. Why is dict/set insertion described as O(1) "amortized" rather than simply O(1)?
10. Name two problems dict/set do NOT help solve faster.

*(Answers: 1. maps object→integer; deterministic, fast, uniform distribution. 2. lists are mutable — hash would become stale after mutation. 3. if a==b then hash(a)==hash(b) (converse not required). 4. two keys hashing to the same bucket; pigeonhole principle. 5. chaining: higher memory, graceful degradation; open addressing: lower memory/better cache locality, sharper degradation near load factor 1. 6. marks "deleted" distinctly from "never used," preserving probe sequences; chaining just removes from the list directly, no probe sequence to preserve. 7. count/size; ~2/3 for Python's real dict; open addressing degrades faster so needs a lower threshold (e.g. 0.5 in lab). 8. "has the complement of this value already been seen?"; two-sum, pair-with-difference-k. 9. occasional O(n) resizes are amortized across many O(1) insertions, same math as PS6's dynamic array. 10. finding max/min; maintaining sorted order / range queries.)*

---

## Algorithms and Patterns Introduced This Week

| Pattern/Structure | Complexity | Key Idea |
|--------------------|-----------|----------|
| Hash table (chaining) | O(1) avg, O(n) worst | List per bucket; graceful degradation |
| Hash table (open addressing) | O(1) avg, O(n) worst | ≤1 entry per bucket; probe on collision |
| Load-factor-triggered resize | O(1) amortized | Same math as Week 6/PS6 dynamic array |
| Counting pattern | O(n) | `counts[x] = counts.get(x,0)+1` |
| Grouping pattern | O(n) | `defaultdict(list)` keyed by shared property |
| Deduplication pattern | O(n) | `set` for O(1) average membership testing |
| Complement search | O(n) | "Have I seen target-x before?" — two-sum and relatives |
| Anagram detection | O(n) | Compare frequency dicts directly |
| Memoization | O(1) avg per check | Cache dict keyed on function arguments |

---

*CS 101 · Week 8 · © CSE Department*

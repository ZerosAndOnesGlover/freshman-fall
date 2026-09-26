# CS 101 · Problem Set 8
## Hash Tables, Dictionaries, and Sets

**Released:** Friday 20 November 2026, 10:00 (after L27) · Week 8
**Due:** Friday 27 November 2026, 17:00 · Week 9 — late penalty from 17:01
**Submission:** `ps8.py` (Part B) and your answer sheet (Part A) in `"$CS101/week8"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 2½–3 hours (Project 1 is due the same day)

*(Revised 2026-09-26: Lab 8 (Tuesday 24 November) investigates the `__hash__`/`__eq__` contract and writes
`two_sum`, so A2 and the basic `two_sum` left this set. A4, `group_by_first_letter`, `four_sum_count` and
`difference_report` were cut too, and the answer key moved out of this handout.)*
**Note:** Project 1 is due the same day. Finish Project 1's core by Tuesday 24 November, then do this set.

---

## What this problem set uses

Weeks 0–8, above all this week's: hash functions, buckets, `dict` and `set`, the `__hash__`/`__eq__`
contract (L25), chaining, open addressing and tombstones, load factor and resizing, and L26's
`ChainedHashTable` (L26), and the counting, grouping, membership, two-sum and memoisation patterns,
`defaultdict`, and set operators `& | - ^` (L25 §5, L27).

**Not needed and not expected:** decorators, dunder methods beyond `__init__`/`__len__`/`__hash__`/`__eq__`,
the two-pointer technique, `functools`.

---

## Part A: Written (24 points)

### A1: Hash Table Mechanics (14 points)

**(a)** Why does `hash([1, 2, 3])` raise `TypeError` while `hash((1, 2, 3))` works? Refer to mutability and
to why a dict needs a key's hash to stay fixed.
**(b)** A chained table has 10 buckets and 8 entries. What is its load factor? Does it trigger a resize at
L26's 0.75 threshold?
**(c)** What is a tombstone in open addressing? Give a small example (table size, keys, which slots they
land in) showing what goes wrong if deletion writes a plain empty marker instead.
**(d)** Why does an open-addressing table resize at a lower load factor than a chained one? (L26 §3, §5.)

### A2: Costs (10 points)

State and justify the cost, in terms of the input sizes:
**(a)** Deciding whether two lists contain the same set of values, using sets.
**(b)** Finding every value that occurs more than once in a list of `n`, using a counting dict.
**(c)** Finding the values in both list A (size `n`) and list B (size `m`), using a set of the smaller one.

---

## Part B: Python (`ps8.py`) (76 points)

State each function's cost in its docstring and give it at least two `assert` tests.

### B1: Extending L26's Hash Table (12 points)

Copy `ChainedHashTable` from L26 into `ps8.py` and add:
**(a)** `keys()`, **(b)** `values()`, **(c)** `items()` — lists of the stored keys, values, `(key, value)` pairs;
**(d)** `update(other)` — `put` every pair of a Python dict `other`, overwriting existing keys.

### B2: Faster With a Dict or Set (22 points)

Each of these was quadratic, or impossible, with only lists:
**(a)** `has_duplicate(lst)` — Θ(n) with a set.
**(b)** `word_frequency(text)` — dict of lower-cased word → count. `"the cat the hat THE"` → `{"the": 3, "cat": 1, "hat": 1}`.
**(c)** `is_anagram(s1, s2)` — same letters with the same counts, ignoring case and spaces. `("dormitory", "dirty room")` → `True`.
**(d)** `longest_consecutive(nums)` — the longest run of consecutive **values** (not positions) in Θ(n): put
the numbers in a set, and only start counting at an `x` whose `x − 1` is absent. `[100, 4, 200, 1, 3, 2]` → `4`.

### B3: Every Two-Sum Pair (14 points)

Lab 8 wrote L27 §5's `two_sum`, which returns one pair. Write `two_sum_all_pairs(nums, target)` — **every**
`(i, j)` with `i < j`; keep a dict from value to the list of indices seen so far.
`([3, 3, 3], 6)` → `[(0, 1), (0, 2), (1, 2)]`.

### B4: Memoisation, Counted (14 points)

Write `fib_memo(n, cache, stats)` in the style of L27 §7, where `stats` is a list `[hits, misses]` that the
function updates. Run `fib_memo(20, {}, stats)` and print the counts. Explain in a comment why the misses
equal the number of distinct sub-problems, and how many naive calls the cache saved (Lab 4 measured them).

### B5: Set Operations (14 points)

**(a)** `jaccard(a, b)` — `|a & b| / |a | b|`, and `1.0` for two empty sets. `({1, 2, 3}, {2, 3, 4})` → `0.5`.
**(b)** `common_words(text1, text2)` — lower-cased words in both, with `&`.

---

## Grading Rubric

| Problem | Points |
|---------|--------|
| A1 Mechanics | 14 |
| A2 Costs | 10 |
| B1 Hash table | 12 |
| B2 Dict/set versions | 22 |
| B3 Two-sum pairs | 14 |
| B4 Memoisation | 14 |
| B5 Set operations | 14 |
| **Total** | **100** |

---

*CS 101 · Week 8 · Problem Set 8 · Due Friday 27 November 2026, 17:00 · © CSE Department*

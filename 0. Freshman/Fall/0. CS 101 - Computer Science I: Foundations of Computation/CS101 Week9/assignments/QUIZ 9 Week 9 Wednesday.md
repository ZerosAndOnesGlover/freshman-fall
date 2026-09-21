# CS 101 · Quiz 9
## Week 9, Wednesday — In-Class Assessment

**Date:** Wednesday 25 November 2026 · 09:00–09:10 (start of L28) · Week 9
**Duration:** 10 minutes (first 10 minutes of Wednesday lecture)
**Format:** Written — closed book, closed notes
**Covers:** Week 8 material: hash tables, collision resolution, load factor, dict/set patterns

---

### Question 1 (2 points)

State the `__hash__` / `__eq__` contract precisely. Then explain in one sentence why violating it
causes a `set` to lose track of an object it already contains.

&nbsp;

&nbsp;

---

### Question 2 (2 points)

A hash table with 8 buckets uses chaining. Five keys hash to bucket indices 5, 5, 5, 3, 3.

(a) What is the load factor?

(b) What is the worst-case number of key comparisons for a successful lookup?

(c) The load factor is comfortably below 1. Explain, in one sentence, why this table is nevertheless
badly distributed.

&nbsp;

&nbsp;

---

### Question 3 (2 points)

Fill in the average-case complexity for each operation:

| Operation | Complexity |
|---|---|
| `x in some_set` | O(___) |
| `x in some_list` | O(___) |
| `d[k] = v` (dict insert) | O(___) amortised |
| `lst.insert(0, x)` | O(___) |

---

### Question 4 (2 points)

Why is dict/set insertion described as O(1) **amortised** rather than simply O(1)? Name the
operation responsible and state its cost when it occurs.

&nbsp;

&nbsp;

---

### Question 5 (2 points)

Name **two** distinct problems that a hash table does **not** make faster, and state what structure
or approach you would use instead for each.

&nbsp;

&nbsp;

---

**Total: 10 points**

---

### Answer Key (Instructor Copy — Do Not Distribute)

**1.** *If `a == b` then `hash(a) == hash(b)`.* (The converse need not hold — unequal objects may
share a hash; that is a collision.) Violating it means an object can be filed under one hash and
looked up under another, so the probe visits the wrong bucket and the object — though present —
is never found. Award 1 pt for the contract, 1 pt for the consequence.

**2.** (a) **5/8 = 0.625.** (b) **3** — the longest chain (bucket 5 holds three keys).
(c) Load factor measures *occupancy*, not *uniformity*: six of eight buckets are empty while one
holds three entries, so the hash is clustering. Full marks require the occupancy-vs-uniformity
distinction, not merely "the hash is bad".

**3.** `O(1)`, `O(n)`, `O(1)`, `O(n)`. Half a point each.

**4.** Because **resizing (rehashing)** occasionally occurs, costing **Θ(n)** for that one
insertion. Doubling makes resizes geometrically rare, so the total across n insertions is O(n) and
the per-operation average is O(1) — a worst-case guarantee over a *sequence*, not a probabilistic
average. Accept without the last clause; award the bonus half-mark for it.

**5.** Any two of: **finding min/max** (use a heap, or sort); **maintaining sorted order or range
queries** (sorted list + `bisect`, or a balanced tree); **prefix/substring matching** (a trie);
**unhashable elements such as lists** (sort and compare, or convert to tuples). 1 pt each — the
alternative structure is required for the mark.

*Common wrong answer:* "hash tables don't help when there are collisions." That is a performance
caveat, not a different problem class.

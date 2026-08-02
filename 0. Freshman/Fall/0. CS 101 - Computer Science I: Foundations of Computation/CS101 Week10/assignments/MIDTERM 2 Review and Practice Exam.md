# CS 101: Midterm 2 Review & Practice Exam
## Covers Weeks 6–9: Complexity Through Regular Expressions

**Midterm 2 Format:** 75 minutes, written, closed book. One handwritten cheat sheet (1 side of 8.5×11) allowed.
**Weight:** 15% of final grade
**Administered:** Week 10

---

## How to Use This Document

This is a diagnostic tool, not busywork. Work through it **closed-book and timed**, exactly as you
will sit the real exam. Then grade yourself honestly against the answer key at the end. Any section
scoring below 80% means re-reading that week's lectures *before* the exam, not after.

**Scope:** Weeks 6–9 only. Week 10 material (files, exceptions) is **not** examined — it appears on
the final.

| Week | Topic | Weight on this exam |
|---|---|---|
| 6 | Algorithm analysis, Big-O, recurrences | ~25% |
| 7 | ADTs, dynamic arrays, linked lists, stacks/queues | ~25% |
| 8 | Hash tables, collision resolution, dict/set patterns | ~25% |
| 9 | Strings, encoding, search, regular expressions | ~25% |

---

## Section 1: Complexity Analysis (20 points)

**1.1 (6 pts)** Give a tight Θ bound for each, and state the exact operation count where asked.

```python
# (a)                          # (b)                       # (c)
for i in range(n):             for i in range(n):          i = 1
    for j in range(n):             for j in range(i):      while i < n:
        work()                         work()                  work()
                                                               i *= 2
```

For (b), give the exact count, not just the class.

**1.2 (6 pts)** Solve each recurrence and name the Master Theorem case where it applies.

- (a) `T(n) = T(n/2) + Θ(1)`
- (b) `T(n) = 2T(n/2) + Θ(n)`
- (c) `T(n) = 2T(n−1) + Θ(1)`

**1.3 (4 pts)** Prove from the definition that `5n² + 30n + 100` is `O(n²)`. Give explicit `c` and
`n₀`.

**1.4 (4 pts)** You time an algorithm at n = 1000, 2000, 4000 and get 8 ms, 33 ms, 129 ms. Determine
the complexity class from the data and state the method.

---

## Section 2: Data Structures (20 points)

**2.1 (5 pts)** State the complexity of each, and for the two that differ, explain why.

| Operation | Python list | Linked list |
|---|---|---|
| index `[i]` | | |
| insert at front | | |
| append at end | | |

**2.2 (5 pts)** Explain why `list.append` is O(1) **amortised** rather than O(1). Include the
geometric-series argument and state what growing by a fixed amount instead would cost.

**2.3 (5 pts)** A queue implemented with a Python list and `pop(0)` is Θ(n) per dequeue. Name the
correct structure, state why it is O(1) at both ends, and name what it gives up.

**2.4 (5 pts)** Implement a queue using **two stacks** with O(1) amortised operations. Give the code
and a one-paragraph proof of the amortised bound.

---

## Section 3: Hash Tables (20 points)

**3.1 (5 pts)** State the `__hash__`/`__eq__` contract. Then explain, in terms of buckets, why
violating it makes an object unfindable in a set that contains it.

**3.2 (5 pts)** A table with 8 buckets and chaining receives keys hashing to 5, 13, 21, 3, 11.

- (a) Draw the table.
- (b) Give the load factor.
- (c) The load factor is 0.625 — comfortably healthy. Explain why this table is nonetheless badly
  distributed, and what metric would reveal it.

**3.3 (5 pts)** Compare chaining and open addressing on memory, cache behaviour, deletion, and
behaviour as α → 1. State which you would choose for α = 0.9 and why.

**3.4 (5 pts)** Explain the hash-flooding attack: how it works, why it was possible across many
languages simultaneously in 2011, and what fixed it.

---

## Section 4: Strings and Regular Expressions (20 points)

**4.1 (5 pts)** `len("café")` is 4, `len("café".encode("utf-8"))` is 5, and `len("👋🏽")` is 2.
Explain each.

**4.2 (5 pts)** Building a string with `+=` in a loop is Θ(n²), but a naive benchmark shows only a
~5× penalty.

- (a) State the exact number of character copies.
- (b) Name the CPython behaviour that hides it.
- (c) Describe a benchmark modification that reveals the true complexity.

**4.3 (5 pts)** For each, state what it returns and why:

```python
re.findall(r"<.+>",  "<a><b>")
re.match(r"world", "hello world")
re.fullmatch(r"\d{4}", "abc1234")
```

Then say which function must be used to validate a field, and give an input the wrong choice
accepts.

**4.4 (5 pts)** `^(a+)+$` takes ~1 second on 24 characters; `^a+$` handles 100,000 in ~1 ms.

- (a) Explain the mechanism.
- (b) Name the attack class.
- (c) Give the language-class reason regex cannot parse HTML.

---

## Section 5: Synthesis (20 points)

**5.1 (10 pts)** You are given a 2 GB log file and must report the 10 most frequent IP addresses.

- (a) Describe your approach and give its time and space complexity.
- (b) Name one data structure from Week 8 that is central, and say why.
- (c) State one thing that would make the naive approach fail on a file this size.

**5.2 (10 pts)** For each task, name the right tool and one wrong-but-tempting alternative, with a
one-sentence justification:

- (a) Test whether a value is in a collection of 100,000 items, repeatedly
- (b) Split `a,"b,c",d` into three fields
- (c) Find every four-digit year in a document
- (d) Parse a nested configuration file
- (e) Maintain items in sorted order with frequent insertions

---

## ANSWER KEY

*Work the paper before reading this.*

### Section 1

**1.1** (a) **Θ(n²)**, exactly n². (b) **Θ(n²)**, exactly **n(n−1)/2** — same class, half the
constant. (c) **Θ(log n)** — the counter is *multiplied*, so it reaches n in log₂n steps.

**1.2** (a) **Θ(log n)** — Master case 2 with a=1, b=2, f(n)=Θ(1)=Θ(n⁰), critical exponent n⁰.
(b) **Θ(n log n)** — Master case 2, a=b=2, critical exponent n matches f(n)=n. (c) **Θ(2ⁿ)** —
the Master Theorem **does not apply** (the subproblem is n−1, not n/b); unroll to get 2ⁿ−1.

**1.3** Take n₀ = 1. For n ≥ 1, n ≤ n² and 1 ≤ n², so 5n² + 30n + 100 ≤ 5n² + 30n² + 100n² = 135n².
So **c = 135, n₀ = 1**. Any valid pair earns full marks; a tighter one (c = 6, n₀ = 34) is equally
correct. **No marks without explicit constants.**

**1.4** Ratios 33/8 ≈ 4.1 and 129/33 ≈ 3.9 — both ≈ 4 = 2², so **Θ(n²)**. Method: for input doubling,
T(2n)/T(n) ≈ 2^k identifies Θ(n^k); take k = log₂(ratio).

### Section 2

**2.1** Index: **Θ(1)** list, **Θ(n)** linked. Insert at front: **Θ(n)** list, **Θ(1)** linked.
Append: **Θ(1) amortised** list, **Θ(1)** linked *with a tail pointer* (Θ(n) without).
The two that differ do so because a list is a **contiguous** block — the address of slot i is
`base + i·8`, so indexing is arithmetic, but making room at the front requires shifting everything.

**2.2** Growing to capacity k copies k elements; doubling puts resizes at 1, 2, 4, 8, …, so total
copying across n appends is 1+2+4+… < 2n — a geometric series bounded by twice its largest term.
Total O(n) for n appends, hence **O(1) amortised**. Growing by a **fixed** amount c gives an
arithmetic series ≈ n²/(2c), i.e. **O(n) amortised per append and O(n²) overall**.

**2.3** Use **`collections.deque`** — a doubly linked list of fixed-size blocks with pointers to
both ends, so `popleft`/`append` adjust an index within a block without shifting. It gives up
**O(1) random access**: `d[k]` for a middle index is O(n).

**2.4** Two stacks `_in` and `_out`; push onto `_in`; to pop, if `_out` is empty transfer everything
from `_in` (reversing order), then pop from `_out`.
*Amortised proof:* charge each enqueue 3 units — 1 to push, 2 held in credit. Each element moves
from `_in` to `_out` **at most once in its lifetime**, and that move costs 2 (a pop plus a push),
paid from the stored credit. Dequeue then costs 1. So every operation is O(1) amortised. **The
guard "transfer only when `_out` is empty" is what makes "at most once" true.**

### Section 3

**3.1** *If `a == b` then `hash(a) == hash(b)`* (the converse need not hold). Violating it means the
object was filed in the bucket for its old hash and is looked up in the bucket for its new one — the
probe visits the wrong bucket, finds nothing, and reports absence even though the object is present.

**3.2** (a) bucket 3 → [3, 11]; bucket 5 → [5, 13, 21]; all others empty. (b) **5/8 = 0.625**.
(c) Load factor measures **occupancy, not uniformity** — six of eight buckets are empty while one
holds three entries. The revealing metric is the **variance-to-mean ratio of bucket counts** (≈1
for a good hash), or equivalently the longest chain against log n.

**3.3** Memory: open addressing wins (one flat array, no per-entry pointers). Cache: open addressing
wins decisively (adjacent probes). Deletion: chaining wins (unlink; open addressing needs
tombstones that accumulate). α → 1: chaining degrades gracefully (average chain α, and α > 1 is
legal) while open addressing degrades catastrophically — expected probes ≈ ½(1 + 1/(1−α)), so
α = 0.9 costs ~5.5 probes and it cannot exceed α = 1 at all. **At α = 0.9 choose chaining.**

**3.4** With a deterministic, published hash, an attacker precomputes many keys colliding into one
bucket and submits them together; insertion degenerates to Θ(n²) and a few hundred KB of form data
occupies a CPU for minutes. It hit PHP, Java, Python, Ruby, and ASP.NET simultaneously in 2011
because all used fixed, documented hash functions, so **one precomputed collision set worked against
every deployment**. The fix is **hash randomisation** — a per-process random seed mixed into string
hashing, so collisions cannot be precomputed.

### Section 4

**4.1** A `str` is a sequence of **code points**; UTF-8 is **variable-width**, and `é` needs 2 bytes
— hence 4 vs 5. `"👋🏽"` is **two code points**, a base emoji plus a skin-tone modifier, rendered as
one glyph — so even `len` on the `str` disagrees with what a user calls "one character".

**4.2** (a) `1+2+…+n = n(n+1)/2`. (b) CPython **resizes the string in place when its refcount is 1**,
which the naive loop satisfies. (c) Keep a **live alias** (`keep.append(s)` each iteration) so the
refcount exceeds 1; measured 1.1 ms → 20 ms → 314 ms as n quadruples twice, i.e. ×16 ≈ 4².

**4.3** `['<a><b>']` — `.+` is **greedy**, running to the end and backtracking to the *last* `>`.
`None` — `re.match` anchors at position 0 and the text begins with `hello`. `None` — `fullmatch`
requires the **entire** string to match and `"abc1234"` has non-digits.
**Validation requires `fullmatch`**; `re.search(r"\d{4}", …)` accepts `"abc1234"` or
`"drop table; 1234"`.

**4.4** (a) `^(a+)+$` is **ambiguous** — a run of n a's can be partitioned among the outer
repetitions exponentially many ways, and when `$` fails the backtracking engine tries every one.
`^a+$` admits a single parse. (b) **ReDoS** — regular expression denial of service. (c) Regex
describes **regular languages**; HTML is **context-free**, and regular languages cannot count
unbounded nesting. This is a theorem, proved in CS 301.

### Section 5

**5.1** (a) Stream the file line by line, extract the IP with a regex or `split`, count in a
`Counter`, then `most_common(10)`. **Time Θ(N)** in the number of lines; **space Θ(k)** in the number
of *distinct* IPs — not the file size. (b) The **hash table** (`dict`/`Counter`): it turns "how many
times have I seen this IP" from an O(k) scan into an O(1) average lookup, so the whole pass is
linear instead of quadratic. (c) Reading with `.read()` or `.readlines()` loads all 2 GB into
memory. Iterating the file object is O(1) memory. *(Also accept: sorting all entries to find the
top 10 is Θ(k log k) where a size-10 heap is Θ(k log 10).)*

**5.2** (a) **`set`** — O(1) average membership; wrong-but-tempting: a `list`, which is O(n) per
check. (b) **`csv` module** — handles quoted delimiters; wrong: `.split(",")`, which returns four
fields. (c) **regex** `\b\d{4}\b`; wrong: a manual character loop, which is longer and buggier.
(d) **a real parser** (`json`, `configparser`, or a parser generator); wrong: regex, which cannot
handle nesting. (e) **a sorted list with `bisect`, or a heap** depending on the queries; wrong: a
`dict`/`set`, which destroys ordering entirely.

---

## Final Preparation Checklist

- [ ] Can you state Big-O formally and *prove* a bound with explicit constants?
- [ ] Can you apply the Master Theorem and say when it does **not** apply?
- [ ] Can you derive the amortised O(1) argument for dynamic arrays from scratch?
- [ ] Can you implement a queue from two stacks and prove the bound?
- [ ] Can you state the hash contract and explain what breaks without it?
- [ ] Do you know when chaining beats open addressing, and why?
- [ ] Can you explain why `len(str) != len(bytes)`?
- [ ] Do you know which `re` function validates, and why the others do not?
- [ ] Can you name the two hard limits of regular expressions?

*If any answer is "not confidently", that is where your revision time goes.*

---

*CS 101 · Midterm 2 Review · © CSE Department*

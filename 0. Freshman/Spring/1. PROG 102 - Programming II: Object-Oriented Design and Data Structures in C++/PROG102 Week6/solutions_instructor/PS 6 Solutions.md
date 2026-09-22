# PROG 102 · Problem Set 6 — Solutions and Marking Notes
## A Templated Doubly Linked List

**INSTRUCTOR COPY — not for distribution**

---

## Before Marking

**Reference environment:** g++ 13.3.0, x86-64 Linux. Structural results (`size`, `height`, error
messages) are exact; timings and the exact crash threshold are not.

**This is the heaviest problem set of the course so far** and it is the foundation of Project 1. Mark
Part A and B thoroughly — a student whose list or iterator is wrong here will be building Project 1 on
sand, and it is worth catching now.

---

> **Revised 2026-09-22.** C3 (BST height against insertion order, which needed `std::shuffle` and repeats Lecture 21 §3.2)
> was removed; its last sentence (what `std::map` adds) moved to C2. Re-weighted to keep 100.

## Part A — The List (36)

### A1 (10)

Sentinel node linking to itself; `insert` and `erase` with no branches:

```cpp
Node() : value(), prev(this), next(this) {}          // sentinel

iterator insert(const_iterator pos, T value) {
    Node* at = pos.node();
    Node* fresh = new Node(at->prev, at, std::move(value));
    at->prev->next = fresh;
    at->prev = fresh;
    ++count;
    return iterator(fresh);
}
```

*Marking: 4 the sentinel with self-links, 4 branch-free `insert`/`erase`, 2 the remaining members.*

**Search the submission for `if` inside `insert` and `erase`.** Any head/tail/empty special case means
the sentinel was added without being used — deduct 4 and show them the branch-free version.

**`end()` must be the sentinel**, not null. A null `end()` makes `--end()` impossible and A4's backward
traversal will not work.

### A2 (10)

Five members plus `noexcept` `swap`, copy-and-swap assignment.

*Marking: 2 destructor (`clear()` **then** `delete sentinel`), 2 deep copy constructor, 2 move
constructor, 2 copy-and-swap + `noexcept` swap.*

**Grep for `== &`.** A leftover self-assignment guard is a 2-point deduction.

### A3 (8) — the assessed trap

Without `o.init()`, the moved-from list keeps a pointer to the sentinel the new owner now uses. Both
destructors run:

```
ERROR: AddressSanitizer: heap-use-after-free   (or double-free)
```

**The moved-from object must be left as a *valid empty list*** — a fresh sentinel — not merely emptied.
A moved-from object must still be destructible and assignable (L18 §4.1), and for this class that means
it needs a sentinel of its own.

*Marking: 4 the transcript, 4 the explanation. **The explanation must say "valid empty list", not
"nulled out"** — nulling `sentinel` would make the destructor's `delete sentinel` fine but `begin()`
would then dereference null.*

### A4 (8)

Both element types, forward and backward, deep-copy independence, self-assignment.

Reference:

```
size=5 front=5 back=9
forward : 5 3 8 1 9
backward: 9 1 8 3 5
strings : alan ada grace
deep copy: s=3 s2=2
assign+self: 3
```

**Why `std::string` matters:** it is a `T` with its own resource and its own Rule of Five. It proves the
container assumed nothing about `T` beyond copy/move-constructibility — an implementation doing
anything bitwise would fail here and pass for `int`.

*Marking: 6 both types with all four operations, 2 the justification. The justification must be about
`T` owning a resource.*

---

## Part B — The Iterator (30)

### B1 (10)

`template <bool Const>` with `std::conditional_t` for `pointer`/`reference`, all five typedefs, both
increment and decrement forms, and the non-`explicit` `Iter<false>` → `Iter<true>` constructor.

*Marking: 3 the five typedefs, 3 the operators including post-forms, 2 the `Const` parameterisation,
2 the converting constructor.*

**A student who wrote two separate iterator classes** has satisfied the requirement but not the
question — award 8 and note the maintenance cost.

### B2 (6)

```
our category is bidirectional? yes
std::list's category matches?  yes
```

Removing a typedef gives a long error naming the missing member — typically 30–80 lines depending on
which one.

*Marking: 3 the `static_assert`s including the `std::list` comparison, 3 the removal experiment with a
line count and the identifying line.*

### B3 (8)

```
accumulate      = 26
*max_element    = 9
count_if even   = 1
find(8) ok      = yes
after reverse   : 9 1 8 3 5
copied to vector: 5 elements
```

*Marking: 8, roughly 1.3 per algorithm. **`reverse` is the one that catches a broken `operator--`** —
if their decrement is wrong, everything else passes and this hangs or corrupts.*

### B4 (6) — the assessed idea

```
error: no match for 'operator-' (operand types are 'List<int>::Iter<false>' and ...)
```

**Why this is correct:** `std::sort` requires random access; `it2 - it1` is part of that contract. A
list cannot provide it in $O(1)$. Providing it by looping would make an $O(n)$ operation wear $O(1)$
syntax, and `sort` would silently become $O(n^2 \log n)$ while appearing to work.

*Marking: 2 the error and quoted operator, 4 the explanation. **Full marks require the point about
syntax hiding cost.** "Because lists aren't random access" is 2 of the 4 — true, and it does not say
why that should stop the code compiling.*

---

## Part C — The BST (18)

### C1 (10)

Reference on `{5,3,8,1,4,7,9,3}`:

```
size=7 height=2 (edges, empty=-1)
inorder: 1 3 4 5 7 8 9
contains(4)=yes contains(6)=no
```

**7, not 8** — the duplicate is rejected.

*Marking: 4 the implementation, 2 size/height correct, 2 sorted traversal. **A student reporting height
3 has used the node-counting convention** — deduct 1 and point at the stated convention rather than
treating it as wrong in general.*

### C2 (8)

`std::string` and `std::greater<int>` both working.

**Zero of the five.** `unique_ptr` members already model the ownership, so the generated destructor and
move operations are correct and copying is correctly disabled. **The List needed all five because
nothing in the library owned its nodes; the BST needs none because `unique_ptr` does.**

*Marking: 3 both demonstrations, 3 the comparison. **The comparison is the assessed half** and must
identify *why* the two differ — the presence of a library type modelling the ownership.*

## Part D — The Bug at Scale (16)

### D1 (8)

| chain length | result |
| --- | --- |
| 1,000 | fine |
| 100,000 | fine |
| 500,000 | fine |
| 1,000,000 | **segfault** |

with `ulimit -s` = 8192 KB.

*Marking: 4 the table, 2 reporting their stack limit. **Thresholds will vary** — a student on a 16 MB
stack may not fail until 2,000,000. Mark that they found *a* threshold and reported the limit.*

### D2 (8)

```cpp
~Node() { auto n = std::move(next); while (n) n = std::move(n->next); }
```

5,000,000 destroys fine.

**(a) (3)** ASan reports a `SEGV` on an unknown address, with a stack trace of a thousand identical
frames. **It tells you where you died, not why**, and it is not a leak or an invalid access so nothing
is diagnosed. *(Accept `-fsanitize=address` reporting stack-overflow if their version does; the point is
that the diagnosis is unhelpful.)*

**(b) (3)** Expected substance:

> **Recursion whose depth is controlled by input data is a bug waiting for a large enough input.**

*Marking: 3 the fix verified at 5M, 3 for (a)+(b). **(b) must be general** — an answer about
`unique_ptr` specifically gets 1, because the same failure appears in recursive tree traversal,
recursive descent parsers, and anything else that recurses per element.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 36 |
| B | 30 |
| C | 18 |
| D | 16 |
| **Total** | **100** |

---

## What to Watch For

1. **Special cases in `insert`/`erase`** (A1). The sentinel was added but not used.
2. **A null `end()`** — backward traversal in A4 will not work.
3. **Move constructor without `o.init()`** (A2/A3) — some students fix A3's bug and leave A2's version
   broken.
4. **"Because lists aren't random access"** as the whole of B4.
5. **Claiming the C3 ratio is constant** when their own table shows drift.
6. **A `unique_ptr`-specific answer to D2(b).**

---

## Feeding Into Project 1

Project 1 is due Week 9 and this problem set is Parts 1 and 2 of it.

**Spend ten minutes per student confirming their `List<T>` and iterator actually work** before Week 7.
A broken iterator here becomes a broken BST iterator in Project 1 Part 2.2, which is substantially
harder to debug, and the student will not know which of the two is at fault.

The specific check: **does `std::reverse` work on their list?** It exercises `operator--`, the
converting constructor and `iterator`/`const_iterator` interop in one call, and it is the fastest way
to find out whether Part B is real.

---

*PROG 102 · Week 6 · PS 6 Solutions · © CSE Department*

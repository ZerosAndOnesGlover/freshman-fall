# PROG 102 · Project 1
## A Container Library

**Assigned:** Tuesday 2 March 2027, 10:00 (at L19) · Week 6
**Due:** Friday 26 March 2027, 17:00 · Week 9 — late penalty from 17:01
**Points:** 100 · 5% of the course grade

## What this project uses

Weeks 0–6 of PROG 102 — templates and the STL (Weeks 2–3), inheritance and exceptions as far as
Lecture 04 §4.2 and Lecture 06 §2.3 take them, `unique_ptr` and the Rule of Five (Week 5), the
sentinel list, iterators and the BST (Week 6) — plus CS 102 Weeks 1–2 for BST deletion, successors
and iterative traversal.

**Not needed and not expected:** `splice`, `unique`, `resize`/`assign`, a list merge sort, or the
named exception guarantees of Week 9 beyond the "strong guarantee" Lecture 06 already names.

---

## What This Is

A small container library: a **sequence container**, an **ordered associative container**, a **shared
iterator protocol**, and a **test suite** that demonstrates all of it works.

PS 6 is the foundation. A good `List<T>` and `BST<T>` from that problem set are most of Parts 1 and 2
here, and you are expected to reuse and improve them.

**What is new in this project** is everything around the containers: a real test suite, measured
comparisons against the STL, a written design rationale, and the requirement that your containers
survive inputs that break naive implementations.

---

## Ground Rules

- **C++17. `-Wall -Wextra -pedantic`, no warnings.**
- **Sanitizer-clean** under `-fsanitize=address,undefined`, except in tests that deliberately provoke
  a report (which must be marked as such).
- **You may not use** `std::list`, `std::forward_list`, `std::map`, `std::set`, `std::multimap` or
  `std::multiset` in the implementations. **You should use them in tests** as reference behaviour.
- `std::vector`, `std::string`, `std::unique_ptr` and `<algorithm>` are all permitted and encouraged.
- **Every file you submit must be yours.** Name collaborators; state any generative-tool use.

---

## Part 1 — The Sequence Container (22 pts)

**1.1** *(12)* `List<T>`: a templated doubly linked list with a sentinel node, the full Rule of Five,
and `insert`/`erase` with **no special cases**.

Beyond PS 6, add `remove_if(pred)` — `pred` is any callable, as in Lecture 12's algorithms — and
`reverse()`. **`reverse` must relink nodes, not copy values**, and neither may allocate.

**1.2** *(10)* `iterator` and `const_iterator` via `template <bool Const>`, satisfying
`iterator_traits`, with the converting constructor.

**Demonstrate at least eight distinct STL algorithms** working on your list.

---

## Part 2 — The Associative Container (28 pts)

**2.1** *(12)* `BST<T, Compare = std::less<T>>` with `unique_ptr` children, `insert`, `contains`,
`erase`, `inorder`, `height`, `size`.

**`erase` is the hard one.** Handle all three cases (no child, one child, two children), exactly as CS 102
Lecture 05 §5 does, and say in your write-up which successor strategy you chose.

**Height is in edges: empty = −1.**

**2.2** *(8)* A **bidirectional in-order iterator** for the BST, so that `begin()`/`end()` and
range-`for` work and STL algorithms apply.

This is genuinely harder than the list's: `operator++` must find the in-order successor (CS 102
Lecture 05 §4 with parent pointers; Lecture 04 exercise 4 with an explicit stack). **State in your
write-up whether you used parent pointers or an explicit stack, and what that cost you.**

**2.3** *(8)* Make the BST **copyable** — a deep clone — while keeping it movable.

**How many of the five did you need, and why is that different from PS 6's BST?**

---

## Part 3 — Robustness (18 pts)

**3.1** *(8)* **The destruction test.** Build a degenerate structure of **at least one million** nodes —
a sorted-input BST, or a `unique_ptr` chain — and destroy it.

**A naive recursive destructor will crash.** Show that yours does not, report your stack limit, and
describe your approach.

**3.2** *(6)* **Iterator invalidation.** Document, for each container, exactly which operations
invalidate which iterators — and **write a test for each claim.**

At least one test must demonstrate a *deliberate* invalidation caught by AddressSanitizer, clearly
marked.

**3.3** *(4)* **Exception safety.** Make an element type whose copy constructor throws on demand.
Show what happens to your list when a copy throws partway through.

You are not required to achieve the strong guarantee. **You are required to say which guarantee you
provide** and to have tested it. *(Week 9 is where this becomes the whole subject.)*

---

## Part 4 — Measurement (16 pts)

**4.1** *(8)* Benchmark `List<T>` against `std::list<T>` for: build, traverse, copy, and `reverse`.

**At least three runs each**, at a size where the times are not noise. Report absolute times and
interpret the differences honestly — **including any case where yours is faster, which usually means
you measured wrong.**

**4.2** *(8)* Benchmark `BST<T>` lookup against `std::map`, on **random** and **sorted** insertion
orders, for at least three sizes.

Your sorted-input numbers will be very bad. **Quantify how bad**, and state in two sentences what
`std::map` spends to avoid it.

---

## Part 5 — The Write-Up (16 pts)

`DESIGN.md`, and it is marked as writing.

**5.1** *(8)* **Design decisions.** For each of these, state what you chose and why:

- sentinel versus null-terminated;
- raw `prev`/`next` pointers versus `unique_ptr` links;
- BST iterator via parent pointers versus an explicit stack;
- what your containers deliberately **do not** provide.

The last one is the most important. **Name at least two operations you could have implemented and chose
not to, and justify each.**

**5.2** *(8)* **What the STL buys.** Having implemented both, write 300–500 words on what
`std::list` and `std::map` provide that yours do not, and what — if anything — yours does better.

**An honest answer that says "nothing" for the second half is worth full marks.** An answer that
invents an advantage is not.

---

## Deliverables

```
list.hpp        bst.hpp         iterator_support.hpp (if you factor it out)
tests.cpp       bench.cpp       DESIGN.md            README.md (how to build and run)
```

**A single command must build and run your tests.** A `Makefile` or a one-line script is fine; state it
in [[PROG102 Week6/README|README]].

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| 1 | 22 | The sequence container and its iterators |
| 2 | 28 | The associative container, in-order iteration, deep copy |
| 3 | 18 | Scale, invalidation, and exception behaviour |
| 4 | 16 | Measurement against the STL, interpreted honestly |
| 5 | 16 | The write-up |
| **Total** | **100** | |

---

## Late Policy

Projects are stricter than problem sets: **10% per day, and nothing accepted after 3 days.**

**Partial credit is generous.** A submission with Parts 1, 3 and 5 complete and Part 2 missing scores
far better than four half-finished parts. **Finish what you start**, and say in [[PROG102 Week6/README|README]] what is not
done — an accurate statement of scope costs you nothing and an inaccurate one costs a great deal.

---

## A Note on What Is Being Assessed

You are not being assessed on whether you can outperform `std::list`. You cannot, and Part 4 is designed
so that discovering this is worth marks.

**You are being assessed on whether you can build something to an interface contract and tell the truth
about it.** That means: the iterator category you declare is one you honour (Part 1.2), the
invalidation rules you document are ones you tested (3.2), the guarantee you claim is one you verified
(3.3), and the benchmark you report is one you understand (4.1).

Every one of those is a place where a plausible-looking lie would pass a casual read. **The whole
project is about not telling them.**

---

*PROG 102 · Week 6 · Project 1 · © CSE Department*

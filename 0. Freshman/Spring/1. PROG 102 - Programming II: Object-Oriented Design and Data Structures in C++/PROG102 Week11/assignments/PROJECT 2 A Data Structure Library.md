# PROG 102 · Project 2
## A Data Structure Library

**Assigned:** Tuesday 6 April 2027, 10:00 (at L34) · Week 11
**Due:** Friday 16 April 2027, 17:00 · Week 12 — late penalty from 17:01
**Points:** 100 · 5% of the course grade
**Demo and code review: Lab 12** *(a further 40 points, as part of the Labs component)*

## What this project uses

Everything through Week 11: your Project 1 containers, exception guarantees and `Fragile` (Week 9 and
Lab 9), the bounded queue and TSan (Week 10), lambdas, `std::function`, `constexpr` and `if constexpr`
(Week 11). BST deletion and successors are CS 102 Weeks 1–2.

**Not needed and not expected:** a list `sort()` (never taught), the testing framework and profiler
of Week 12. Benchmarking against the STL was Project 1's Part 4 and is not repeated.

---

## What This Is

**The capstone.** A templated data structure library with a full test suite and a written
design rationale.

**It is Project 1, finished.** You are expected to reuse and improve your Project 1 code — that is the
point of the ordering, not a shortcut. What is new is everything the last three weeks added:
exception guarantees you have tested, thread safety where it belongs, modern idioms, and a demo you
have to defend in Lab 12.

> **On the timescale.** This is due at the end of Week 12 and assigned now, which is short for a
> capstone. **It is short because you already have most of it.** A Project 1 that scored well is
> perhaps 60% of this. If Project 1 went badly, fixing it *is* the first task, and Part 1 gives you
> credit for doing so.

> **On the weight.** Directly 5%. But **Lab 12 is your demo of this project** (40 points of the labs
> component), and **the final exam draws Section C from it.** Treating it as a 5% throwaway is the
> most reliable way to have a bad Week 12.

---

## Ground Rules

- **C++17. `-Wall -Wextra -pedantic`, no warnings.**
- **Sanitizer-clean** under `-fsanitize=address,undefined`, and under `-fsanitize=thread` for Part 4,
  except in tests that deliberately provoke a report and are marked as such.
- **You may not use** `std::list`, `std::map`, `std::set` or `std::forward_list` in the
  implementations. Use them freely in tests as reference behaviour.
- **One command builds and runs everything.** State it in [[PROG102 Week11/README|README]].
- Name collaborators; state any generative-tool use.

---

## Part 1 — The Containers (26 pts)

**1.1** *(10)* `List<T>` — a templated doubly linked list with a sentinel, the full Rule of Five,
`iterator`/`const_iterator` satisfying `iterator_traits`, `remove_if` and `reverse`.

**1.2** *(10)* `Tree<T, Compare = std::less<T>>` — a BST with `unique_ptr` children, `insert`, `erase`,
`contains`, a **bidirectional in-order iterator**, and a deep copy.

**1.3** *(6)* If either of these is carried over from Project 1, **list what you changed and why** in
`DESIGN.md`.

**This is worth full marks for an honest "I fixed the following defects".** It is worth nothing for
"unchanged" if the Project 1 feedback said otherwise.

---

## Part 2 — Exception Safety, Established (26 pts)

**2.1** *(8)* Implement a throwing element type (`Fragile`) with a settable failure point and a live
counter.

**2.2** *(12)* For **at least four** operations across both containers, determine the guarantee **by
sweeping the failure point across every allocation and copy.**

Report a table per operation: failure point, state before, state after, leaked, guarantee observed.

**2.3** *(6)* State each operation's guarantee — **the weakest observed, not the best** — in
`CONTRACTS.md`, alongside preconditions and postconditions for every public function.

---

## Part 3 — Modern C++ (18 pts)

**3.1** *(6)* Provide algorithm-friendly interfaces: your containers must work with at least **eight**
STL algorithms, demonstrated.

**Include one that correctly refuses your iterator**, with the error, and explain why that is right.

**3.2** *(6)* Use, and justify in one line each: a **lambda** with a non-trivial capture, `if
constexpr`, **structured bindings**, and a `constexpr` computation proved compile-time by a
`static_assert`.

**3.3** *(6)* Provide a `for_each`-style member taking a callable **as a template parameter**, and one
taking `std::function`. **Say which you would ship**, using Lab 11's measurements.

---

## Part 4 — Concurrency (16 pts)

**4.1** *(10)* Provide **one** thread-safe container — a bounded queue is the expected choice — with
blocking `push`/`pop`, a shutdown mechanism, and correct condition-variable usage.

Test with at least 3 producers and 3 consumers, **TSan-clean**. State the command that worked.

**4.2** *(6)* Your `List` and `Tree` are **not** thread-safe.

- **(a)** *(3)* **Document that** — precisely. "Not thread-safe" is not precise enough; say what a
  caller may and may not do concurrently.
- **(b)** *(3)* Demonstrate a race on one of them under TSan, in a test clearly marked as a deliberate
  failure.

---

## Part 5 — The Write-Up (14 pts)

`DESIGN.md`.

**5.1** *(7)* **Decisions.** For each: what you chose and why — sentinel vs null; raw vs `unique_ptr`
links; the BST iterator's mechanism; and **at least two operations you deliberately did not provide.**

**5.2** *(7)* **What you would do differently.** 300–500 words.

Having built this twice — Project 1 and now — what would you change if you started again? **Be
specific and be honest.** "Nothing" earns nothing.

---

## Deliverables

```
list.hpp    tree.hpp    queue.hpp    fragile.hpp
tests.cpp   DESIGN.md      CONTRACTS.md   README.md
```

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| 1 | 26 | The containers, and honest reporting of what changed |
| 2 | 26 | Guarantees established by evidence |
| 3 | 18 | Modern C++, used where it helps |
| 4 | 16 | Thread safety where it belongs, and documented where it is absent |
| 5 | 14 | The write-up |
| **Total** | **100** | |

---

## Late Policy

**10% per day; nothing after 3 days.** The final exam is Thursday 22 April and no extensions are
available beyond that.

**Partial credit is generous. Finish what you start** and state in [[PROG102 Week11/README|README]] what is incomplete. An
accurate scope statement costs nothing; an inaccurate one costs a great deal.

---

## What Is Being Assessed

**You are being assessed on whether you can build to a contract and tell the truth about it**: the
iterator category you declare is one you honour (3.1), the guarantee you claim is one you swept for
(2.2), and the thread safety you document is one you tested (4.2).

**Part 5.2 is where that becomes explicit.** You have now built this library twice. The most valuable
thing you can write is an accurate account of what you got wrong the first time — and that is worth
7 marks precisely because it is uncomfortable.

---

*PROG 102 · Week 11 · Project 2 · © CSE Department*

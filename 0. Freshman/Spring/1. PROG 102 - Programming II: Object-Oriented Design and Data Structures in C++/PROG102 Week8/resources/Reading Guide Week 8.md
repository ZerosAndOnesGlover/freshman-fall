# PROG 102 · Week 8 · Reading Guide
## Behavioural Patterns, and Reproducing the Measurements

---

## What to Read

| Source | Sections | Why |
| --- | --- | --- |
| **Gang of Four** | **Ch. 5** — Observer, Strategy, Command, Template Method, State | The week's patterns |
| **Gang of Four** | **Ch. 6** (Conclusion) | Short, and the honest part of the book |
| **Meyers, *Effective Modern C++*** | **Items 31–34** | Lambdas. **Read these before Week 11** |
| **cppreference** | `std::function`, `std::weak_ptr` | The two library types this week depends on |

> **Read Gang of Four Chapter 6.** It is four pages, almost nobody reads it, and it contains the
> authors' own account of what patterns are for and where they expect the idea to fail. It is a much
> more modest document than the catalogue's reputation suggests.

---

## Chapter 5 — The Patterns

**Observer:**

1. The book's *Consequences* section lists "unexpected updates". **Read it against Lecture 25 §6's five
   unsolved problems** — how many does the book name?
2. The book discusses **push vs pull**. Which does it prefer, and why? Compare with L25 §5.
3. The book has no answer for the dangling observer. **Was that reasonable in 1994?** *(What would they
   have used instead of `weak_ptr`?)*

**Strategy:**

4. The book's *Consequences* mention "clients must be aware of different strategies". **Is that true of
   `std::sort`'s comparator?** Argue it.
5. Find where the book compares Strategy with **Template Method**. Restate the difference in your own
   words, then check against L26 §5.2.

**Command:**

6. The book lists five things Command enables. **Which of them can a bare lambda do, and which need a
   real object?** This is Lecture 27 §3.4's argument and the book gives you the raw material.

**Template Method:**

7. The book calls this "the Hollywood Principle". **Find one example in the C++ standard library.**

**State:**

8. The book notes State and Strategy have identical structure. **What distinguishes them?** *(The
   answer is not in the code.)*
9. *Consequences* raises where to put the transition logic. **Compare with L27 §1.1's objection about
   distributed transitions.**

---

## Reproducing This Week's Measurements

**g++ 13.3.0, x86-64 Linux.** Structural results exact; timings are not.

### L25 §3–4 — The dangling observer, and the fix

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address observer.cpp -o obs
./obs        # raw pointers  -> stack-use-after-scope
./obs x      # weak_ptr      -> clean, and pruned
```

**Expect:** `stack-use-after-scope` in `Subject::set`; then registered counts of 2 → 2 (stale) → 1
(pruned).

### L26 §3 — Four ways to express a strategy

```
g++ -std=c++17 -O2 -Wall -Wextra strategy_cost.cpp -o sc && ./sc
```

**Expect**, on 2,000,000 ints:

| | |
| --- | --- |
| virtual Strategy | 165.7–167.6 ms |
| **`std::function`** | **287.5–304.1 ms** |
| lambda | 159.9–160.9 ms |
| default `operator<` | 149.9–151.2 ms |

**Write down your prediction first.** Most people rank `std::function` second or third; it is last.

### L26 §4, L27 §1 — Command, Template Method, State

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined behavioural.cpp -o beh && ./beh
```

### L27 §3.2 — Command, both eras

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined modern.cpp -o mod && ./mod
```

**Expect:** identical behaviour, and **20 lines / 4 types** against **8 lines / 2 types**.

---

## The Result Worth Sitting With

This week's benchmark says something that sounds contradictory until you look at the mechanism.

> **`std::function` — the modern, general, "functional" way to hold a callable — is the slowest of the
> four**, and it is slower than the 1994 virtual-call pattern it supposedly replaces.

And yet Lecture 27 argues that **lambdas made Strategy obsolete**. Both are true, and the resolution is
that *lambda* and *`std::function`* are not the same thing:

- A **lambda passed as a template parameter** has a concrete type. It inlines. It is the fastest of the
  four.
- A **lambda stored in a `std::function`** has been type-erased. It cannot inline. It is the slowest.

**The same lambda, in two containers, differing by 1.85×.**

This matters beyond the number, because it is the third time this course has met the same mechanism:

| Week | Erased how | Cost |
| --- | --- | --- |
| **3** | `qsort`'s function pointer | ~2× `std::sort` |
| **4** | a virtual call | ~2 ns; and it blocks inlining |
| **8** | `std::function`'s type erasure | 1.85× a lambda |

> **A callable whose type is unknown at compile time cannot be inlined, and in a hot loop that costs
> roughly a factor of two.** The spelling changes every decade; the mechanism does not.

---

## Before Week 9

1. Lectures 25–27 read; **GoF Chapter 6** read.
2. **Project 1 due Friday.** This week's problem set is short precisely so that it is not competing.
3. Week 9 is **exception safety** — the three guarantees, `noexcept`, and why RAII is what makes any of
   it tractable. It answers the question Lab 8 ends on: *what should `publish` do when a handler
   throws?*
4. **Meyers Items 31–34** if you have time. Week 11 is lambdas properly, and this week has given you a
   reason to care about how they are stored.

---

*PROG 102 · Week 8 · Reading Guide · © CSE Department*

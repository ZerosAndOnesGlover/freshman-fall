# PROG 102 · Problem Set 9
## Making a Container Exception-Safe

**Week 9 · Released Friday Week 9 · Due Friday Week 10, 17:00 · 100 points**
**Covers:** Lectures 28–30

> **Midterm 2 is in Week 10** and covers Weeks 5–9. This problem set is the best revision available for
> the last third of it — **do it early in the week**, not the night before it is due.

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Deliverables:** `container.hpp`, `fragile.hpp`, `safety_tests.cpp`, `costs.cpp`, `CONTRACTS.md`,
`ANSWERS.md`. Name collaborators and state any generative-tool use.

**Use your Week 6 `List<T>` or Project 1's container.** You may not start from `std::vector`.

---

## Part A — What Exceptions Cost (20 pts)

**A1.** *(8)* Measure the **happy path**: identical source compiled with and without exception support.

```
g++ -std=c++17 -O2 -c work.cpp -o with.o
g++ -std=c++17 -O2 -fno-exceptions -DNO_EXC -c work.cpp -o without.o
```

Report **times** (at least three runs, functions in a separate translation unit so they cannot be
inlined away) **and `size` output for both objects.**

**A2.** *(4)* Measure the **throwing path** over at least 100,000 throws. Report microseconds per throw
and express it as a multiple of a normal call.

**A3.** *(8)* Answer all three:

- **(a)** *(3)* "C++ exceptions are zero-cost." **Which part of your data supports it and which part
  refutes it?**
- **(b)** *(3)* From your numbers, give a concrete rule about when exceptions are the wrong mechanism.
  **Use your measurement, not a slogan.**
- **(c)** *(2)* A first attempt at A1 compared an exception-throwing function against an error-code
  function with an out-parameter, and reported 1.5×. **Why is that not an answer to A1's question?**

---

## Part B — Determining Your Guarantee (30 pts)

**B1.** *(8)* Implement `Fragile` — an element type that throws on the *n*-th copy, with *n* settable,
and a live-object counter so you can detect leaks.

**Verify it works** before using it to test anything.

**B2.** *(14)* For **three** operations on your container — at minimum an insertion, an assignment, and
one of your choosing — determine the guarantee **by testing**.

For each operation, **sweep the failure point across every copy it performs.** For each *n*, record:

| n | state before | state after | leaked? | guarantee at this n |
| --- | --- | --- | --- | --- |

**B3.** *(8)* From your tables, state each operation's guarantee.

- **(a)** *(4)* **It is the weakest observed, not the best.** Report all three, and flag any operation
  where the weakest and the best differ.
- **(b)** *(4)* Did any of them differ from what you expected before testing? **Report your prior**,
  and if you were right for all three, say what you would have to test to be *sure* rather than lucky.

---

## Part C — Upgrading to Strong (26 pts)

**C1.** *(10)* Take one operation that came out **basic** and give it the **strong** guarantee using
L29 §4.1's recipe — risky work on a copy, commit with a `noexcept` swap.

**Re-run your B2 sweep** and show it is now strong at every *n*.

**C2.** *(8)* Measure what that cost: time and peak memory, for the operation on a container of at
least 10,000 elements, before and after.

**C3.** *(8)* Answer both:

- **(a)** *(4)* `std::vector::push_back` is strong but `std::vector::insert` in the middle is only
  basic. **Explain why**, using your C2 numbers.
- **(b)** *(4)* Give a concrete operation in your own container where strong would be the **wrong**
  choice, and justify it.

---

## Part D — `noexcept` and Contracts (24 pts)

**D1.** *(6)* Write a `noexcept` function that throws. Report the **compiler warning** and the
**runtime behaviour**, and confirm that a surrounding `catch (...)` does not run.

**D2.** *(6)* Take a class with a move constructor. Count moves and copies during `vector` growth
**with and without** `noexcept` on it. Report both.

**Then state, in one sentence, what a missing `noexcept` silently costs.**

**D3.** *(6)* For each of the following, decide **assertion or exception** and justify in one sentence:

1. an index past the end of an internal buffer, in a private helper;
2. a configuration file that will not parse;
3. a negative capacity passed to your container's constructor;
4. a container invariant (`size <= capacity`) checked at the end of `insert`;
5. a network read that times out.

**D4.** *(6)* `CONTRACTS.md`: write the full contract for **every public function** of your container —
precondition, postcondition, and exception guarantee.

Then find **one function whose contract you could not state cleanly**, and say in three sentences what
that tells you about the design.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 20 | What exceptions cost, on all three axes |
| B | 30 | Determining a guarantee by evidence rather than assertion |
| C | 26 | Upgrading to strong, and what it costs |
| D | 24 | `noexcept`, assertions, and writing the contract down |
| **Total** | **100** | |

**Where the marks actually are:** B is the largest part and it is entirely measurement. **B3(a) is the
one to get right** — reporting the weakest observed guarantee rather than the best is the difference
between documentation and marketing.

---

## Submission Checklist

1. Clean build; sanitizer-clean except where tests deliberately provoke reports.
2. A1 compares **identical source**, two build configurations.
3. B2 **sweeps** every failure point, not just the first.
4. B3(a) reports the **weakest** guarantee per operation.
5. D4 covers **every** public function.
6. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 9 · Problem Set 9 · © CSE Department*

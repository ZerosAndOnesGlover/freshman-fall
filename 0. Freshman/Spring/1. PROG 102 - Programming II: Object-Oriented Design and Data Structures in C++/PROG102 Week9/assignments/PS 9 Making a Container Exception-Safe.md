# PROG 102 · Problem Set 9
## Making a Container Exception-Safe

**Released:** Friday 26 March 2027, 10:00 · Week 9 (after Thursday's L30)
**Due:** Friday 2 April 2027, 17:00 · Week 10 — late penalty from 17:01
**Points:** 100 · counts toward the Problem Sets component (30%, lowest one dropped)
**Expected time:** about 4 hours

## What this problem set uses

Weeks 0–9: move semantics and `noexcept` moves (Week 5), your Week 6 container, exceptions and
unwinding (L28), the three guarantees and the copy-then-swap recipe (L29), `noexcept`, assertions and
contracts (L30) — and **Lab 9's `Fragile` element and failure sweep** (Monday 29 March), whose result
Part B starts from.

**Not needed and not expected:** threads (Week 10). The cost of exceptions is Lecture 28 §5's
measurement and is not re-measured here.

> **Midterm 2 is Tuesday 30 March, 18:00–19:30** (Week 10), and covers Weeks 5–9. This problem set is the best revision available for
> the last third of it — **do it early in the week**, not the night before it is due.

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Deliverables:** `container.hpp`, `fragile.hpp`, `safety_tests.cpp`, `CONTRACTS.md`,
`ANSWERS.md`. Name collaborators and state any generative-tool use.

**Use your Week 6 `List<T>` or Project 1's container.** You may not start from `std::vector`.

---

## Part A — What Exceptions Cost (12 pts)

**A1.** *(12)* Using Lecture 28 §5's measurements (happy path, throwing path, code size), answer all three:

- **(a)** *(5)* "C++ exceptions are zero-cost." **Which part of the data supports it and which part
  refutes it?**
- **(b)** *(4)* From those numbers, give a concrete rule about when exceptions are the wrong mechanism.
  **Use the measurement, not a slogan.**
- **(c)** *(3)* A first attempt at that measurement compared an exception-throwing function against an error-code
  function with an out-parameter, and reported 1.5×. **Why is that not an answer to whether exceptions cost anything when nothing throws?**

---

## Part B — Upgrading to Strong (38 pts)

**B1.** *(16)* Take one operation that came out **basic** in Lab 9 Part D and give it the **strong** guarantee using
L29 §4.1's recipe — risky work on a copy, commit with a `noexcept` swap.

**Re-run Lab 9's Part C sweep** on it and show it is now strong at every *n*.

**B2.** *(10)* Measure what that cost: time, and the number of element copies (your `Fragile` counter), for the operation on a container of at
least 10,000 elements, before and after.

**B3.** *(12)* Answer both:

- **(a)** *(6)* `std::vector::push_back` is strong but `std::vector::insert` in the middle is only
  basic. **Explain why**, using your B2 numbers.
- **(b)** *(6)* Give a concrete operation in your own container where strong would be the **wrong**
  choice, and justify it.

---

## Part C — `noexcept` and Contracts (50 pts)

**C1.** *(10)* Write a `noexcept` function that throws. Report the **compiler warning** and the
**runtime behaviour**, and confirm that a surrounding `catch (...)` does not run.

**C2.** *(12)* Take a class with a move constructor. Count moves and copies during `vector` growth
**with and without** `noexcept` on it. Report both.

**Then state, in one sentence, what a missing `noexcept` silently costs.**

**C3.** *(12)* For each of the following, decide **assertion or exception** and justify in one sentence:

1. an index past the end of an internal buffer, in a private helper;
2. a configuration file that will not parse;
3. a negative capacity passed to your container's constructor;
4. a container invariant (`size <= capacity`) checked at the end of `insert`;
5. a network read that times out.

**C4.** *(16)* `CONTRACTS.md`: write the full contract for **every public function** of your container —
precondition, postcondition, and exception guarantee.

Then find **one function whose contract you could not state cleanly**, and say in three sentences what
that tells you about the design.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 12 | What exceptions cost, read from the lecture's data |
| B | 38 | Upgrading to strong, and what it costs |
| C | 50 | `noexcept`, assertions, and writing the contract down |
| **Total** | **100** | |

**Where the marks actually are:** C4 — a contract for every public function — is the largest single
item, and the function you cannot state cleanly is worth more than the ones you can.

---

## Submission Checklist

1. Clean build; sanitizer-clean except where tests deliberately provoke reports.
2. B1 re-runs the full sweep and shows strong at **every** *n*.
3. C4 covers **every** public function.
4. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 9 · Problem Set 9 · © CSE Department*

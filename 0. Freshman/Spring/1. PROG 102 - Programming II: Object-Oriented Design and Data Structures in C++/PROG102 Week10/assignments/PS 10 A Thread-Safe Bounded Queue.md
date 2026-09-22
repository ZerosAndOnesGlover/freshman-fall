# PROG 102 · Problem Set 10
## A Thread-Safe Bounded Queue

**Released:** Friday 2 April 2027, 10:00 · Week 10 (after Thursday's L33)
**Due:** Friday 9 April 2027, 17:00 · Week 11 — late penalty from 17:01
**Points:** 100 · counts toward the Problem Sets component (30%, lowest one dropped)
**Expected time:** about 4 hours

## What this problem set uses

Weeks 0–10: templates and move semantics (Weeks 2 and 5), capture lambdas as far as Lecture 25 §4's
box (the predicate form of `wait` needs one), threads and races (L31), mutexes, deadlock,
`scoped_lock` and condition variables (L32), atomics and the bounded queue (L33).

**Not needed and not expected:** memory orderings beyond L33 §1.3's signpost; timing races or
`shared_ptr` sharing — Lectures 31 §3 and 33 §2 measured those, and Lab 10 repeats the race.

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -pthread -g -fsanitize=thread prog.cpp -o prog
setarch $(uname -m) -R ./prog          # if TSan will not start
```

**Every concurrent program in this set must be run under ThreadSanitizer**, and you must state the
command that worked.

**Deliverables:** `queue.hpp`, `queue_tests.cpp`, `races.cpp`, `costs.cpp`, `ANSWERS.md`.
Name collaborators and state any generative-tool use.

---

## Part A — The Bounded Queue (60 pts)

**A1.** *(24)* Implement `BoundedQueue<T>`:

```cpp
void push(T value);            // blocks while full
bool pop(T& out);              // blocks while empty; false if closed and drained
void close();                  // wakes every waiter
```

Requirements: a fixed capacity; **two** condition variables; the predicate form of `wait`; a shutdown
flag; and `notify_all` in `close()`.

**A2.** *(12)* Test it with **at least 3 producers and 3 consumers**, 20,000 items each, three runs.

Every item must be consumed exactly once. **Run it under TSan and report the result.**

**A3.** *(12)* Break it three ways, one at a time. For each, report what happens and **how long it took
you to notice**:

- **(a)** *(4)* remove the shutdown flag;
- **(b)** *(4)* change `close()` to `notify_one`;
- **(c)** *(4)* use `wait(lk)` without the predicate.

*(For (c), three consumers makes a stolen wakeup much easier to provoke than one.)*

**A4.** *(12)* Answer both:

- **(a)** *(6)* Your `pop` is `bool pop(T&)` rather than `T pop()`. **Give two reasons**, at least one
  about exception safety.
- **(b)** *(6)* Add `bool empty() const`. **Write a program using `if (!q.empty()) q.pop();` that
  fails**, and explain why the fix is an interface change rather than more locking.

---

## Part B — Deadlock (40 pts)

**B1.** *(12)* Write two threads that lock two mutexes in opposite orders. **Demonstrate the deadlock**
under a timeout and report the exit code.

**B2.** *(14)* Fix it **two ways** — consistent ordering, and `std::scoped_lock` — and show both
completing.

For `scoped_lock`, **deliberately pass the mutexes in opposite orders** in the two threads and confirm
it still works.

**B3.** *(14)* Answer both:

- **(a)** *(7)* Name the four conditions required for deadlock, and say which one each of your two fixes
  breaks.
- **(b)** *(7)* Does ThreadSanitizer detect your deadlock? **Run it and report.** Then say what that
  tells you about the limits of the tool.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 60 | A correct bounded queue, and three ways it breaks |
| B | 40 | Deadlock, its fixes, and what TSan cannot see |
| **Total** | **100** | |

---

## Submission Checklist

1. Every concurrent program run under TSan; **the working command stated.**
2. A2 is TSan-clean.
3. B2's `scoped_lock` version passes the mutexes in opposite orders.
4. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 10 · Problem Set 10 · © CSE Department*

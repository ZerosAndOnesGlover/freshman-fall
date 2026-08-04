# PROG 102 · Problem Set 10
## A Thread-Safe Bounded Queue

**Week 10 · Released Friday Week 10 · Due Friday Week 11, 17:00 · 100 points**
**Covers:** Lectures 31–33

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

## Part A — Races, Measured (24 pts)

**A1.** *(8)* Four threads, one million `++` each on a shared `long`. Expected 4,000,000.

Run **five times at `-O0` and five times at `-O2`.** Report all ten results.

**A2.** *(6)* Your `-O2` results will differ in character from your `-O0` results.

- **(a)** *(3)* Describe the difference.
- **(b)** *(3)* Compile the increment loop at both levels and **inspect the assembly**. Paste the `-O2`
  version and explain what the compiler did — **and why it was allowed to.**

**A3.** *(4)* Declare the counter `volatile` and repeat at `-O2`, five runs.

**Report the results and whether TSan still reports a race.** Then state in two sentences what
`volatile` actually did.

**A4.** *(6)* Run the `-O2` version under TSan.

**Does it report a race on a run that produced the correct answer?** Explain why that behaviour is what
you want, in two sentences.

---

## Part B — The Bounded Queue (34 pts)

**B1.** *(14)* Implement `BoundedQueue<T>`:

```cpp
void push(T value);            // blocks while full
bool pop(T& out);              // blocks while empty; false if closed and drained
void close();                  // wakes every waiter
```

Requirements: a fixed capacity; **two** condition variables; the predicate form of `wait`; a shutdown
flag; and `notify_all` in `close()`.

**B2.** *(8)* Test it with **at least 3 producers and 3 consumers**, 20,000 items each, three runs.

Every item must be consumed exactly once. **Run it under TSan and report the result.**

**B3.** *(6)* Break it three ways, one at a time. For each, report what happens and **how long it took
you to notice**:

- **(a)** *(2)* remove the shutdown flag;
- **(b)** *(2)* change `close()` to `notify_one`;
- **(c)** *(2)* use `wait(lk)` without the predicate.

*(For (c), three consumers makes a stolen wakeup much easier to provoke than one.)*

**B4.** *(6)* Answer both:

- **(a)** *(3)* Your `pop` is `bool pop(T&)` rather than `T pop()`. **Give two reasons**, at least one
  about exception safety.
- **(b)** *(3)* Add `bool empty() const`. **Write a program using `if (!q.empty()) q.pop();` that
  fails**, and explain why the fix is an interface change rather than more locking.

---

## Part C — What Sharing Costs (24 pts)

**C1.** *(8)* Measure a shared counter three ways — unsynchronised, `std::atomic`, `std::mutex` — four
threads, one million each, three runs.

Report results **and** times. **Two of the three are correct; state which is faster and by how much.**

**C2.** *(10)* Reproduce Lecture 33 §2's `shared_ptr` measurement, 5,000,000 copies:

- single-threaded;
- after any `std::thread` has been created and joined;
- four threads sharing **one** control block.

Report **ns per copy** for all three.

Then: *(4 of the 10)* **there are two jumps.** Explain each — one is not contention.

**C3.** *(6)* Repeat the four-thread case with each thread holding its **own** `shared_ptr` to its
**own** object.

**Report the per-copy time** and explain the difference from C2's third row in two sentences.

---

## Part D — Deadlock (18 pts)

**D1.** *(6)* Write two threads that lock two mutexes in opposite orders. **Demonstrate the deadlock**
under a timeout and report the exit code.

**D2.** *(6)* Fix it **two ways** — consistent ordering, and `std::scoped_lock` — and show both
completing.

For `scoped_lock`, **deliberately pass the mutexes in opposite orders** in the two threads and confirm
it still works.

**D3.** *(6)* Answer both:

- **(a)** *(3)* Name the four conditions required for deadlock, and say which one each of your two fixes
  breaks.
- **(b)** *(3)* Does ThreadSanitizer detect your deadlock? **Run it and report.** Then say what that
  tells you about the limits of the tool.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 24 | Races measured, and why `-O2` changes their character |
| B | 34 | A correct bounded queue, and three ways it breaks |
| C | 24 | What synchronisation and sharing cost |
| D | 18 | Deadlock, its fixes, and what TSan cannot see |
| **Total** | **100** | |

---

## Submission Checklist

1. Every concurrent program run under TSan; **the working command stated.**
2. A1 reports **ten** runs.
3. A2(b) includes the actual assembly.
4. B2 is TSan-clean.
5. C2 reports **three** figures and explains **both** jumps.
6. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 10 · Problem Set 10 · © CSE Department*

# PROG 102 · Quiz 11
## Week 11 · Tuesday, start of lecture · 15 minutes · 20 points

**Date:** Tuesday 6 April 2027 · 10:00–10:15 (start of L34) · Week 11

**Covers Week 10** — Lectures 31–33: threads, races, mutexes, deadlock, condition variables, atomics.

**Closed book. No devices.** Answer on this sheet.

Name: ________________________  Section: ______  Date: ____________

---

**Q1.** *(4)* Four threads each increment a shared `long` one million times. Expected 4,000,000.

At `-O0` the result is about 1,100,000. At `-O2` it is usually **exactly 4,000,000**, occasionally
3,000,000.

**(a)** *(2)* Why does `-O2` usually give the right answer?

**(b)** *(2)* Why was the compiler **allowed** to do that?

<br><br><br>

---

**Q2.** *(3)* Declaring the counter `volatile` changes the `-O2` result to about 1,100,000, and
ThreadSanitizer still reports races.

**(a)** *(2)* What did `volatile` actually do?

**(b)** *(1)* Did it make the program more correct?

<br><br><br>

---

**Q3.** *(3)* Two threads lock two mutexes in opposite orders and the program hangs.

**(a)** *(1)* Name the failure.

**(b)** *(2)* Give **two** fixes.

<br><br><br>

---

**Q4.** *(3)* `cv.wait(lk, predicate)` versus `cv.wait(lk)`.

**Give two distinct reasons the predicate form is required.**

<br><br><br>

---

**Q5.** *(3)* A thread-safe queue offers `bool empty()` and `void pop()`, each individually
thread-safe.

**(a)** *(2)* Why is `if (!q.empty()) q.pop();` still a bug?

**(b)** *(1)* Why can more locking inside those two functions not fix it?

<br><br><br>

---

**Q6.** *(2)* Measured `shared_ptr` copies: **5.5 ns** single-threaded, **17 ns** after any thread has
existed, **57 ns** with four threads sharing one control block.

**Which of the two jumps is *not* contention, and what is it?**

<br><br>

---

**Q7.** *(2)* Your repaired program runs ThreadSanitizer-clean.

**Does that prove it has no data races? One sentence.**

<br><br>

---

**Total: 20 points**

*PROG 102 · Week 11 · Quiz 11 · © CSE Department*

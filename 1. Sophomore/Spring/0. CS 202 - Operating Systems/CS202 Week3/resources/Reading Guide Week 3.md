# CS 202 · Reading Guide · Week 3
## OSTEP's concurrency chapters, the xv6 book on locking, and one paper about futexes

---

**The curriculum names no reading for Week 3.** OSTEP's concurrency part is the natural text, and it is the best in the book. **It is also more than a week's reading**, so this guide says which chapters are this week, which are Week 4, and which you already know from PROG 201.

| Source | Now? | Why |
|---|---|---|
| **OSTEP 26. Concurrency: An Introduction** | **Read** | The race, the critical section, atomicity. **L10 §1–§3** |
| 27. Interlude: Thread API | *Skim* | `pthread_create`, mutexes, CVs — **PROG 201 Week 3 covered this** |
| **28. Locks** | **Read twice** | Interrupts, test-and-set, CAS, spinning, yielding, futexes. **L10 §4–§6 and L11** |
| 29. Lock-based Concurrent Data Structures | *Skim* | Counters and lists; §29.1's approximate counter is L10 §7 |
| **30. Condition Variables** | **Read** | The bounded buffer, `while` not `if`, two CVs. **L12 §1–§3** |
| **31. Semaphores** | **Read** | Semaphores, readers–writers, dining philosophers. **L12 §4–§7** |
| 32. Common Concurrency Problems | **Week 4** | Deadlock. Read it next week |
| **xv6 book, Ch. 4 "Locking"** | **Read** | xv6's spinlocks, why `acquire` disables interrupts, lock ordering |
| **xv6 book, Ch. 5, the sections on sleep and wakeup** | **Read** | xv6's condition variable, and the lost-wakeup problem it avoids |
| **Drepper, U. — "Futexes Are Tricky"** (2011) | **Read §1–§6** | L11 §2's mutex is his; the paper shows two wrong versions first. Free online |

**If you have three hours this week:** OSTEP 28, then 30, then the xv6 book's Chapter 4, then Drepper §1–§6.

---

## OSTEP Chapter 26 — the race

1. OSTEP's `x86.py` simulator lets you choose where interrupts land. **Find the smallest interrupt interval that loses an update** on the two-thread counter, and relate it to L10 §2's one-CPU measurement.
2. OSTEP defines *indeterminate* programs. **Is `race.c` with 1,000 increments indeterminate?** It lost nothing on the reference machine. Argue both sides.

---

## OSTEP Chapter 28 — locks

3. §28.6 builds a lock from test-and-set and §28.9 from compare-and-swap. **Which of L10 §3's three properties does each guarantee, and which does neither?**
4. §28.10 describes *load-linked / store-conditional*. **x86 does not have it.** What does ARM call it, and why can it avoid a problem CAS has? *(Look up the ABA problem.)*
5. §28.13 says spinning on a single CPU is wasteful. **L11 §5 measured it**: 8.1 µs per operation spinning against 3.1 µs sleeping, with four threads on one CPU. Predict before reading whether the order reverses on four CPUs.
6. §28.14 describes Linux's futex-based mutex and quotes its source. **Match its 31-bit counter trick to Drepper's three states** in L11 §2. Are they the same idea?

---

## OSTEP Chapter 30 — condition variables

7. Figure 30.7's first broken bounded buffer uses `if`. **Describe the interleaving that breaks it with two consumers.** L12 §2 counted 254–372 occurrences in 300,000 items.
8. Figure 30.10's second version uses `while` but one CV. **Describe the interleaving that puts every thread to sleep.** L12 §3's program deadlocked after as few as two items.
9. OSTEP says Mesa semantics make `while` necessary and Hoare semantics would not. **Why does no widely used system provide Hoare semantics?**

---

## OSTEP Chapter 31 — semaphores

10. **Build a condition variable from semaphores.** OSTEP says it is harder than it looks; say where the difficulty is.
11. §31.6's readers–writer lock can starve writers. **L12 §6 measured it: zero acquisitions in four seconds.** Modify OSTEP's version so writers cannot starve, and say what it costs readers.
12. §31.7's dining philosophers deadlock. **Name the four conditions for deadlock** (next week's topic) and say which one each of L12 §5's two fixes breaks.

---

## The xv6 book — Chapter 4, and sleep/wakeup

13. The book lists xv6's locks. **Which lock does `sched()` require its caller to hold across `swtch`**, and why is it released by a different process from the one that acquired it?
14. `sleep(chan, lk)` takes a lock argument. **Describe the lost wakeup** that would happen if it did not — a process checks a condition, decides to sleep, and `wakeup` runs in between.

---

## Where to Go Deeper

| Source | Topic | When |
|---|---|---|
| **Silberschatz**, Ch. 6–7 | Synchronization tools and classic problems, including the **sleeping barber** | **This week** — OSTEP does not cover the sleeping barber |
| **Love**, Ch. 9–10 | Kernel synchronization: spinlocks, mutexes, RCU, per-CPU variables | For L10 §7's remark about per-CPU counters |
| `man 2 futex`, `man 7 futex` | The system call, and the design | **Before Lab 3** |
| **Herlihy & Shavit**, *The Art of Multiprocessor Programming* | Why TTAS beats TAS; lock-free data structures | Optional; Ch. 7 is L11 §4 |

**The man page you must have read before Lab 3:** `futex(2)`, the description of `FUTEX_WAIT` — in particular what it does if the value has already changed.

---

## The One Habit This Guide Is Trying To Build

**Assume the interleaving you did not think of will happen, and measure how often.**

Questions 7 and 8 are the deliberate cases. Each broken bounded buffer looks correct when read top to bottom, and each fails in a specific interleaving that a careful reader can find. **The measurement tells you something the reading cannot: how rare it is.** 300 failures in 300,000 items is rare enough to pass a quick test and common enough to corrupt a production system every few seconds. A concurrency bug's frequency is a fact about the machine, the load and the code together — and "I ran it and it worked" is evidence of almost nothing.

---

*CS 202 · Week 3 · Reading Guide · © CSE Department*

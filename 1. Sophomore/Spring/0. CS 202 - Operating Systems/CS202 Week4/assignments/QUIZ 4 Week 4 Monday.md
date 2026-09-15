# CS 202 · Quiz 4
## Administered: Monday, Week 4 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 3** — races, atomic instructions, spinlocks and futexes, condition variables, semaphores.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **Midterm 1 is this evening**, 18:00–19:15, VNC 100, covering Weeks 0–3. Every question here is
> fair game for it — which makes the key worth reading carefully before six o'clock.

---

**Q1.** Two threads each run `counter++` ten million times with no lock. Why can the result be far less than twenty million even when both threads are pinned to one CPU?

&nbsp;

&nbsp;

---

**Q2.** Name the x86 instruction that compare-and-swap compiles to, and say what its prefix is for.

&nbsp;

&nbsp;

---

**Q3.** Why does xv6's `acquire` disable interrupts before taking a spinlock?

&nbsp;

&nbsp;

---

**Q4.** `FUTEX_WAIT(addr, val)` checks something before it sleeps. What, and what would go wrong without it?

&nbsp;

&nbsp;

---

**Q5.** Drepper's futex mutex uses the values 0, 1 and 2. What does each mean, and when does `unlock` make a system call?

&nbsp;

&nbsp;

---

**Q6.** A consumer waits with `if (count == 0) pthread_cond_wait(...)`. Why is that wrong even though the producer signals only after adding an item?

&nbsp;

&nbsp;

---

**Q7.** Four threads contend for a lock on **one** CPU. Should the lock spin or sleep, and why?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** `counter++` is **load, add, store**. If the timer preempts a thread between its load and its store, the other thread runs a whole slice of increments, and the first thread then **stores its stale value plus one — erasing all of them**. Measured: 37% lost on one CPU.

---

**Q2.** **`lock cmpxchg`.** The **`lock` prefix** holds the memory exclusively for the length of the instruction, so that the compare and the exchange are atomic even with other CPUs using the same memory.

---

**Q3.** If an interrupt handler on the same CPU tried to acquire a lock that CPU already holds, **it would spin forever** — the holder is the code the interrupt suspended, which cannot run until the handler returns. **A one-CPU deadlock with no second thread.**

---

**Q4.** It checks that **`*addr` still equals `val`**, atomically with going to sleep. Without it, a thread could decide to sleep because the lock is held, the holder could release and send its wake-up to nobody, and **the thread would then sleep on a free lock and never be woken** — a lost wake-up.

---

**Q5.** **0** unlocked; **1** locked, nobody waiting; **2** locked, and someone may be waiting. **`unlock` makes a system call only if the value it replaced was 2** — i.e. only if a thread might be asleep. Uncontended: none.

---

**Q6.** Mesa semantics: **being signalled is not the same as running.** Between the signal and the woken consumer re-acquiring the mutex, **another consumer can take the item**, and the woken one finds the buffer empty. (Spurious wake-ups also exist.) **Re-test in a `while`.** Measured: 254–372 empty wake-ups per 300,000 items.

---

**Q7.** **Sleep.** On one CPU, if the lock is held, **the holder is not running** — the waiter is using the only CPU — so spinning cannot shorten the wait, only waste the slice. Measured: spinning 8.1 µs per operation against 3.1 µs sleeping.

---

### What to Do With Your Score

There is no score. Instead, before six o'clock:

| If you missed | Reread |
|---|---|
| Q1 | L10 §1–§2 |
| Q2, Q3 | L10 §5–§6 |
| **Q4, Q5** | **L11 §3** — and trace the three-state lock by hand once |
| Q6 | L12 §2–§3 |
| Q7 | L11 §6 |

---

*CS 202 · Week 4 · Quiz 4 · covers Week 3 · ungraded*

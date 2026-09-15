# CS 202 · Quiz 5
## Administered: Monday, Week 5 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 4** — the four conditions, resource-allocation graphs, diagnosing a deadlock, prevention, the Banker's algorithm, detection, livelock.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **PS 4 is due Friday**, and **Lab 4 is tomorrow afternoon**. Q3 and Q4 are PS 4 in miniature.

---

**Q1.** Name Coffman's four conditions. For **one** of them, say how a program can make it impossible.

&nbsp;

&nbsp;

---

**Q2.** A resource-allocation graph contains a cycle. **When does that prove a deadlock, and when does it not?**

&nbsp;

&nbsp;

---

**Q3.** Three processes share one resource type with **10 units**; **2 are available**.

| | Allocation | Max |
|---|---:|---:|
| P0 | 4 | 7 |
| P1 | 1 | 3 |
| P2 | 3 | 9 |

Is the state safe? If so, give a safe sequence. **Should the Banker grant P2 a request for 1 unit?**

&nbsp;

&nbsp;

&nbsp;

---

**Q4.** The deadlock-detection algorithm looks almost identical to the Banker's safety check. **Name the two differences.**

&nbsp;

&nbsp;

---

**Q5.** A multithreaded server has stopped responding. Every thread shows state `S` and `wchan futex_do_wait` in `/proc`. **What else in `/proc/<tid>/` tells you which lock each thread is waiting for?** And why can you not simply attach `gdb` on the lab machines?

&nbsp;

&nbsp;

---

**Q6.** Two threads each take one lock, `trylock` the other, and on failure release and retry at once. **Neither ever blocks. What goes wrong, and what is the cheapest fix?**

&nbsp;

&nbsp;

---

**Q7.** Why does Linux's hung-task detector **not** report two user threads deadlocked on mutexes?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **Mutual exclusion, hold and wait, no preemption, circular wait.** Any one: **circular wait** — take locks in one global order; **hold and wait** — acquire everything at once, or hold nothing while waiting; **no preemption** — `trylock` the second, release the first on failure; **mutual exclusion** — make the resource shareable (read-only data, per-thread copies).

---

**Q2.** **With one instance of each resource** — every mutex — **a cycle is a deadlock.** **With several instances it is not proof**: a process outside the cycle may hold a unit that one inside needs, and release it.

---

**Q3.** Need: P0 **3**, P1 **2**, P2 **6**. Work = 2 → **P1** finishes (Work 3) → **P0** (Work 7) → **P2** (Work 10). **Safe: ⟨P1, P0, P2⟩.**

**Grant P2 one unit?** Available 1; P2's need becomes 5. Nobody's need fits in 1: P0 needs 3, P1 needs 2. **Unsafe — refuse it, although the unit is free.**

---

**Q4.** Detection compares against each process's **current request**, not its maximum remaining **need**; and it treats a process **holding nothing** as finished from the start.

---

**Q5.** **`/proc/<tid>/syscall`**: system call **202** (`futex`) and its first argument — **the address of the mutex** the thread is waiting on. Match those addresses against the locks and their owners. **`ptrace_scope` is 1**: a process may be traced only by its ancestor, so `gdb -p` is refused — `gdb` must start the program.

---

**Q6.** **Livelock**: the threads keep colliding in step — take, fail, release, retry — busy and making almost no progress. Measured in L15: 32 failed attempts per success. **Cheapest fix: take the locks in one order**, so nobody needs to retry; **or random back-off**, which breaks the symmetry.

---

**Q7.** It reports only tasks in **uninterruptible sleep, state `D`**, for more than 120 seconds. **Mutex waiters sleep in state `S`**, like any idle program — so to the kernel a deadlocked program looks like one waiting for input.

---

### What to Do With Your Score

There is no score. Instead, before Friday:

| If you missed | Reread |
|---|---|
| Q1 | L13 §2, L14 §1 |
| Q2 | L13 §3 |
| **Q3** | **L14 §3–§4** — and work the textbook example by hand before PS 4 Q1 |
| Q4 | L15 §1 |
| Q5 | L13 §4–§5 — **Lab 4 is exactly this** |
| Q6 | L15 §4 |
| Q7 | L15 §3 |

---

*CS 202 · Week 5 · Quiz 5 · covers Week 4 · ungraded*

# CS 202 · Midterm Examination 1
## Operating Systems

---

**Week 4 · Monday 18:00–19:15 · VNC 100 · 75 minutes**
**Covers Weeks 0–3** — the kernel boundary and system calls, processes and the context switch, CPU scheduling, and synchronization.
**Weight: 12.5% of the course grade**

**Permitted:** one handwritten sheet, **one side**. No calculators, no devices.
**Total: 100 marks** — five questions of 20 marks each. **Budget fifteen minutes a question.**

**Name:** _________________________________ **Student ID:** ___________________

---

> **Answer all five questions.** Marks are shown per part. Where a part asks you to *explain* or
> *justify*, a correct answer with no reasoning earns roughly half.
>
> **The arithmetic is designed to be done by hand.** Show your working: a right method with a slip
> earns most of the marks; a bare number that is wrong earns none.
>
> **Q5 is the synthesis question.** Attempt it even if you are short of time — partial arguments
> score.

---

## Q1 · The Kernel Boundary (20 marks)

**(a) [4]** Where does an x86-64 CPU keep the current privilege level, and what is its value while an ordinary Linux program runs? **A Linux program executes `hlt`.** Say what the CPU does and what Linux then does to the program.

**(b) [5]** State **three** things the `SYSCALL` instruction does, and **one** important thing it does **not** do. Then explain why Linux's system-call convention passes the fourth argument in `r10` rather than `rcx`.

**(c) [6]** A program reads an 8 MiB file — 8 × 2²⁰ bytes — to the end with `read()`. **Assume every `read()` call costs 600 ns, whatever the buffer size**, and that a final call returns 0.

- How many `read()` calls, and how much time, with a **1-byte** buffer?
- How many calls, and how much time, with a **4,096-byte** buffer?
- Rewritten to use `fgetc`, one byte per call, the program makes almost exactly as many `read()` calls as the 4,096-byte version. **Why?**

**(d) [5]** On the reference machine, `clock_gettime` cost 18.5 ns and `getppid` about 590 ns, although both appear in section 2 of the manual. **Explain the difference.** Then explain why a system call number that does not exist — which returns `ENOSYS` — cost almost as much as `getppid`.

---

## Q2 · Processes and the Context Switch (20 marks)

**(a) [4]** In xv6, a shell forks a child and calls `wait`; the child runs and calls `exit`. **List every state the child's `struct proc` passes through**, from the moment its slot is claimed to the moment the slot is free again, and name the function that causes each transition.

**(b) [5]** xv6's `swtch` saves only `ebp`, `ebx`, `esi`, `edi` and a return address. **Where are the process's user-mode `eax`, `ecx` and `edx`** when it has been switched away from? Answer separately for a process that entered the kernel through **a timer interrupt** and one that entered through **a system call**.

**(c) [6]** Two processes pass one byte back and forth through two pipes for **100,000 rounds**, taking **0.60 s**. Each round makes two `write` calls and two `read` calls, and the program counts **200,000 context switches**. The same `write` and `read` pair, in one process with no switch, costs **1,500 ns**.

- Estimate the cost of one context switch. Show your working.
- Is your estimate an **upper bound** or a **lower bound** on the cost of the switch alone? Justify.

**(d) [5]** Two xv6 processes on **one CPU** each add 0.25 to a `double`, ten million times, and print the result. **Each should print 2,500,000.** One prints **4,212,345**. **What does the other print, exactly?** Explain.

---

## Q3 · Scheduling (20 marks)

**(a) [6]** Four jobs, times in milliseconds:

| Job | Arrival | CPU burst |
|---|---:|---:|
| A | 0 | 8 |
| B | 1 | 4 |
| C | 2 | 9 |
| D | 3 | 5 |

For **FCFS** and for **SRTF** (shortest remaining time first, preemptive), give the schedule and the **average turnaround time** and **average response time**. *(Response time: first run minus arrival.)*

**(b) [4]** **Without computing its full schedule**, say whether **round robin with a 4 ms quantum** on the same jobs will have a higher or lower average turnaround than SRTF, and a higher or lower average response time than FCFS. Justify each in one or two sentences.

**(c) [5]** Three CPU-bound processes share one CPU under Linux's fair scheduler, at **nice 0, 5 and 10**, whose weights are **1,024, 335 and 110**.

- What share of the CPU does each receive?
- The nice-10 process is moved into **its own cgroup**, of equal CPU weight to the cgroup the other two are in. **Roughly what share does it receive now, and why?**

**(d) [5]** Three periodic tasks, each with deadline equal to period: **1 ms every 4 ms, 2 ms every 5 ms, 2 ms every 10 ms.**

- Compute the utilisation and the Liu–Layland bound for three tasks (2¹ᐟ³ ≈ 1.26). **What does the bound let you conclude?**
- Under **rate-monotonic** scheduling, use response-time analysis to find the worst-case response time of the 10 ms task. **Is the set schedulable?**

---

## Q4 · Synchronization (20 marks)

**(a) [5]** `balance` is 100. Thread T1 runs `balance += 20;` and thread T2 runs `balance += 30;`, with no lock. **Give an interleaving, instruction by instruction, that produces a wrong final balance.** List every final value the program can print.

**(b) [6]** A lock is Drepper's three-state futex mutex (0 free, 1 held, 2 held and someone may be waiting). **Thread T1 locks it. While T1 holds it, T2 and then T3 try to lock it.** Then T1 unlocks; T2 acquires, and later unlocks; T3 acquires, and later unlocks.

- Give the value of the lock word **after each of those eight events**.
- **How many `futex` system calls** are made in total? **Which one was unnecessary**, and why does the lock accept making it?

**(c) [5]** A bounded buffer with one producer and several consumers.

- Consumers wait with `if (count == 0) pthread_cond_wait(&not_empty, &m);`. **What goes wrong, and how?**
- Instead, producers and consumers share **one** condition variable, and everyone waits in a `while` loop and uses `pthread_cond_signal`. **What goes wrong, and how?**

**(d) [4]** For each, say whether a lock should **spin** or **sleep**, with one reason:

- four threads contending for a lock on **one** CPU;
- a lock held for a few nanoseconds, on an 8-CPU machine, whose holder is always running;
- a spinlock inside xv6's kernel, held with interrupts disabled.

---

## Q5 · Synthesis: A System Call That Watches Processes (20 marks)

You add a system call to xv6:

```c
int procstat(int pid, struct pstat *buf);    // copy one process's pid, state, name and CPU ticks
```

`struct proc` gains a field `uint ticks`, **the number of timer ticks the process has been charged**. A monitoring program calls `procstat` for every process — up to 64 — **once every millisecond**.

**(a) [5]** **Where in xv6 would you increment `ticks`**, on what event, and for which process? `procstat` may run on another CPU at the same moment. **Which lock must `procstat` hold while it reads the process's fields**, and what could the monitor see without it?

**(b) [5]** `buf` is a pointer supplied by the user. **What must the kernel check before copying into it**, and which xv6 function already performs that check? **What could a malicious caller achieve** if the check were missing?

**(c) [5]** Suppose each system call costs **600 ns**. **How much CPU time per second** does the monitor spend in system calls with one call per process, for 64 processes? How much with **a single call that returns all 64 at once**? **Name one cost of the single-call design** that the per-process design does not have.

**(d) [5]** A scheduler is written that always runs the runnable process with the **fewest** `ticks`. **Describe how a process could arrange to use a large share of the CPU while being charged almost no ticks**, and propose a fix.

---

**End of examination.** Check that your name and student ID are on the first page.

---

*CS 202 · Midterm 1 · Weeks 0–3 · © CSE Department*

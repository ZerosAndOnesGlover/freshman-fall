# PROG 201 · Systems Programming in C
## Week 2: Pipes, FIFOs, and IPC Mechanisms

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101; CS 201 as co-requisite
**Assessment for this course (overall):** Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%
**This week's deliverables:** PS 2 (due Friday of Week 3) and **Quiz 2** (Tuesday, covers Week 1).
**Lab 1 is sat on the Monday of this week**; **Lab 2 covers this week and is sat on the Monday of Week 3**.

---

### Why This Week Exists

Because "shared memory is the fastest IPC mechanism" is in every textbook, and on this machine it is **six times slower than a pipe**.

Week 1 gave you one way for two processes to exchange bytes, and Lab 1 built a pipeline out of it. This week is the other four ways, what each one guarantees, and — the part that takes a lab to believe — **what each one actually costs.**

Three ideas:

1. **Every mechanism is a trade of guarantees against speed, and the guarantees are specific enough to quote.** A pipe promises that writes of ≤ 4,096 bytes never interleave. A message queue promises whole messages, in priority order, and caps you at ten of them. Shared memory promises nothing at all and hands you the memory.
2. **The kernel was never the expensive part.** What shared memory removes is a copy — 118 ns for a page. What it does not remove is the wakeup, which is 3 µs. Get that backwards and you will write something slower than the thing you replaced.
3. **Look up the limit before you commit to the mechanism.** Sixteen pages. Ten messages of 8 KB. These decide designs, and they are four minutes of reading away.

By Monday of Week 3 you will have measured all four and found the crossover yourself.

---

### Learning Objectives

By the end of Week 2, you should be able to:

1. Say what a pipe's capacity actually is — **sixteen buffers, not 65,536 bytes** — and predict what a 4,097-byte write does to it.
2. State the `PIPE_BUF` guarantee exactly, including what it does and does not cover, and where the constant is declared.
3. Explain why an 8 KB record can pass 8,000 tests and corrupt in production.
4. Create and use a FIFO, and predict the behaviour of all four combinations of `O_RDONLY`/`O_WRONLY` and blocking/non-blocking.
5. Diagnose the FIFO server's spurious-EOF problem and apply the write-end fix.
6. Use a POSIX message queue: boundaries, priorities, the receive-buffer rule, and the limits.
7. Explain kernel persistence and find a leaked IPC object from the shell.
8. Set up POSIX shared memory correctly — `shm_open`, `ftruncate`, `mmap` — and say which omission gives `SIGBUS` rather than `SIGSEGV`.
9. Choose between `MAP_SHARED|MAP_ANONYMOUS` and `shm_open`, for a stated reason.
10. Use a semaphore as a lock **and** as a signal, and place a `sem_t` where two processes can both see it.
11. **Quantify what an unguarded shared counter loses** and fix it.
12. Explain the producer-consumer ring, why one producer needs no mutex, and which lock ordering deadlocks.
13. **Predict which mechanism wins for a given message size, and justify it with the per-message and per-byte costs.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L07 Pipes as a Ring of Pages and FIFOs]] | Capacity **measured as sixteen slots**; the four blocking cases; `PIPE_BUF` and **99% tearing that a fast reader hides**; FIFOs, the rendezvous `open`, and the server's EOF trap |
| [[L08 Message Queues and Shared Memory]] | Message boundaries and priorities; the receive-buffer rule; **10 × 8 KB is the ceiling**; kernel persistence; `shm_open`/`ftruncate`/`mmap`; `MAP_SHARED` vs `MAP_PRIVATE`; the `SIGBUS` trap |
| [[L09 Semaphores and Choosing a Mechanism]] | The counter as lock and as signal; **64.7% of updates lost** without one; 19.3 ns uncontended against 3.3 µs contended; the producer-consumer ring; **the benchmark, and why the textbook claim is wrong** |
| [[LAB 2 IPC Performance Benchmark]] | Measure all four, find the crossover. **Monday of Week 3** |
| `lab/bench.c`, `lab/Makefile` | The skeleton — two worked examples and five TODOs |
| [[PS 2 A Producer Consumer Pipeline]] | The same pipeline over a pipe and over shared memory, measured and accounted for. Due **Friday of Week 3** |
| [[PROG201 Week2/assignments/QUIZ 2 Week 2 Tuesday\|QUIZ 2 Week 2 Tuesday]] | Ten minutes, covers **Week 1**, answer key printed |
| [[PROG201 Week2/resources/Reading Guide Week 2\|Reading Guide Week 2]] | APUE Ch. 15 with its System V bias flagged, and the four man pages that are better than the book |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**You are not choosing a mechanism. You are choosing which guarantees to buy and what to pay for them.**

Laid out as the week measured it:

| | pipe | POSIX mq | shared memory |
| --- | --- | --- | --- |
| Boundaries | ≤ 4,096 bytes only | **yes, always** | none |
| Ordering | FIFO | FIFO **within a priority** | none |
| Mutual exclusion | free | free | **yours to build** |
| Notification | free | free | **yours to build** |
| Cleanup | free | `mq_unlink`, or it leaks | `shm_unlink`, or it leaks |
| Ceiling | 16 pages | **10 × 8 KB** | your RAM |
| 4 KB throughput | **3,680 MiB/s** | 2,786 MiB/s | 574 MiB/s *(one slot)* |
| 256 KB throughput | 2,510 MiB/s | **unavailable** | **14,432 MiB/s** |

Every "free" in that table is the kernel doing work for you, and every one of them is a system call you are paying for. **Shared memory is the row with no frees, which is why it is both the fastest and the one you will get wrong.**

---

### Assessment Reminder

**Labs and quizzes carry no weight** and are still required. **Quiz 2 is at the start of Tuesday's lecture and covers Week 1**; the answer key is printed in the paper and you mark it yourself before leaving.

> **Two labs touch this week.** **Lab 1** — Week 1's pipeline — is sat on the **Monday of this week**.
> **Lab 2** covers this week and is sat on the **Monday of Week 3**. The lab is on a Monday and this
> course's lectures are Tuesday to Thursday, so a lab is always sat the week after the one it covers.

Both are tracked in [[_PROG 201 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 1's `pipe()` is this week's whole first lecture.** L06 §4's EOF rule becomes L07 §3 and §6; L05 §5's "two system calls are not one" is L09 §2 with a shared counter instead of a file offset — the same bug, and this time you lose 64.7% instead of 95%. L05's 1.25 µs system call is the number that explains every row of L09's benchmark. **Week 0 L03's `EINTR` rule** returns in L09 §3, and the answer is the same loop.

**Sideways:** **CS 201 Week 2 is on x86-64 assembly this week**, and the two courses meet at `sem_wait`: the atomic decrement L09 §1 depends on is a single instruction with a `lock` prefix, and CS 201 is where you will see it. The 118 ns `memcpy` of a page is CS 201's cache hierarchy.

**Forward:** **Week 3 is the same ring with threads instead of processes** — the semaphores become condition variables and the shared region becomes ordinary memory, and the reasoning does not change. **Week 4 is `mmap` in its own right**, which is L08 §5 with the page tables underneath it. **Week 5's server hands connections to workers through exactly Lab 2's ring.** **PS 2's records are Project 2's frames.**

---

*PROG 201 · Week 2 · © CSE Department*

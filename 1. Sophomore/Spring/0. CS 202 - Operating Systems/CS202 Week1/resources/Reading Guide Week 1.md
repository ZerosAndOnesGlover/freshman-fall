# CS 202 · Reading Guide · Week 1
## OSTEP Chapters 4–6, the xv6 book's Chapter 1, and one C file

---

**The curriculum names no reading for Week 1** — Week 0's "OSTEP Ch. 1–6" ran into it — so this guide does. Most of it you have half-read already: **Week 0's guide sent you to Chapters 4 and 5 as "Week 1, skim now".** Now read them properly.

| Source | Now? | Why |
|---|---|---|
| **OSTEP 4. The Abstraction: The Process** | **Read** | States, the process list, and **xv6's `struct proc` printed as Figure 4.5**. This is L04 and L05 §1 |
| OSTEP 5. Interlude: Process API | *Skim again* | `fork`, `exec`, `wait` — PROG 201 Week 0 went deeper. **Read §5.4, on why `fork` and `exec` are separate**, because L06 §5 is the other side of it |
| **OSTEP 6. Limited Direct Execution, §6.3** | **Read again** | Switching between processes: the timer interrupt and the saved context. **This is L05** |
| **xv6 book, Ch. 1 "Operating system organization"** | **Read** | How xv6 starts its first process; the process as an address space and a thread |
| **xv6 book, Ch. 5 "Scheduling", the sections on context switching** | **Read** | `swtch`, `sched`, `scheduler`. Leave sleep and wakeup for Week 3 |
| **`proc.c` in xv6** | **Read** `allocproc`, `fork`, `exit`, `wait`, `scheduler`, `sched`, `yield` | 534 lines in total; these seven functions are about 200 of them |

**If you have three hours this week:** OSTEP 4, then `proc.c`'s seven functions with L06 §5 open beside them, then `swtch.S`, then OSTEP 6.3.

---

## OSTEP Chapter 4 — the process as a data structure

**Questions to hold while reading:**

1. OSTEP names three states: *running*, *ready*, *blocked*. xv6 has six and Linux reports at least seven. **Map each of xv6's six onto OSTEP's three**, and say which two of xv6's have no OSTEP counterpart and why xv6 needs them.
2. Figure 4.5 prints xv6's `struct context` and `struct proc`. **The version in the book is not quite the x86 one you built** — compare field by field with `proc.h`. What is different, and does any difference matter to the lecture?
3. §4.3 says an early OS loaded the whole program into memory before running it, and a modern one loads *lazily*. **Which line of L06 §3's `rss.c` table is lazy loading's cousin?** What is being deferred, and until when?
4. OSTEP's homework runs `process-run.py`, a simulator of processes doing CPU work and I/O. **Run it with `-l 3:0,5:100,5:100,5:100 -S SWITCH_ON_IO -I IO_RUN_LATER -c -p`** — one process that only does I/O, three that only compute — and explain the output. Then change `IO_RUN_LATER` to `IO_RUN_IMMEDIATE`. Which policy would you prefer, and what does it cost the three that compute?

---

## `proc.c` — the chapter this week is really built on

Read with L06 §5 open. **Do not read `sleep` and `wakeup` closely yet** — they take a lock in a way that makes sense only after Week 3.

5. `allocproc` pushes the address of `trapret` onto the new kernel stack, and sets `context->eip` to `forkret`. **Draw the new process's kernel stack** after `allocproc` returns, top to bottom, with the size of each piece. *(The sizes are in L05 §3.)*
6. `fork` does `*np->tf = *curproc->tf;` and then `np->tf->eax = 0;`. **What would the child see if the second line were missing?** Be precise: which value, from which call?
7. `exit` calls `sched()` and has a `panic("zombie exit")` after it. **Under what circumstances could that panic ever run?** What would have to be wrong elsewhere?
8. `wait` frees the child's kernel stack with `kfree(p->kstack)`. **Why can `exit` not do that itself?** One sentence.
9. `scheduler` loops over all `NPROC` entries looking for `RUNNABLE`. **With 64 slots this is cheap; with Linux's 51,142 allowed threads it would not be.** What would you change first? *(Week 2 answers it properly.)*

---

## `swtch.S` — twenty-nine lines, four of them the point

10. `swtch` pushes `ebp`, `ebx`, `esi`, `edi` and nothing else. **Where are `eax`, `ecx` and `edx` saved** when a process is switched away from in the middle of a user computation? There are two different answers depending on whether the switch began with a timer interrupt or with a system call. Give both.
11. After `movl %edx, %esp`, the next `popl` reads from **a different process's kernel stack**. At what instant, precisely, does "the current process" change? Is it the same instant at which `myproc()` would start returning the new process?

---

## OSTEP §6.3 — taking the CPU back

12. OSTEP's timeline figure shows the context switch as **two register saves**: one by the hardware into the kernel stack on the timer interrupt, one by the OS into the process structure. **Name the xv6 code that does each.** Which of them saves user registers, and which saves kernel registers?
13. OSTEP's measurement aside puts a context switch in the microseconds. **L05 §5 measured about 1.6 µs** on the reference machine — but the ping-pong it used does a `write` and a `read` for every switch. **How did L05 separate the two costs?** What assumption does that subtraction make?

---

## Where to Go Deeper

| Source | Topic | When |
|---|---|---|
| **Silberschatz**, Ch. 3 | Processes, the PCB, IPC | **This week** — broader on IPC than OSTEP |
| **Love**, Ch. 3 | Process management in Linux: `task_struct`, `clone`, `fork`, exit | **This week**, for L04 §5 and L06 §5 |
| **Love**, Ch. 4 (the scheduler's context-switch section only) | `context_switch()`, `switch_to()` | For L05 §4; the rest is Week 2 |
| `man 5 proc` | Every file under `/proc/<pid>` | Reference for L04 and Lab 1 |
| `man 7 capabilities` | The capability sets | For L04 §4 |

**The man pages you should have read by Friday:** `proc(5)` — at least the `stat`, `status` and `maps` entries — `capabilities(7)`, `credentials(7)`, `clone(2)`.

---

## The One Habit This Guide Is Trying To Build

**When a textbook describes a mechanism, find the lines that implement it.**

Question 6 is the deliberate case. "`fork` returns twice" is a sentence you have known for a year. **The reason is a structure copy and one assignment to `eax`**, and until you have seen those two lines the sentence is something you remember rather than something you understand. xv6 is small enough that this is possible for every mechanism in the course, and that is the entire reason it is on the syllabus.

---

*CS 202 · Week 1 · Reading Guide · © CSE Department*

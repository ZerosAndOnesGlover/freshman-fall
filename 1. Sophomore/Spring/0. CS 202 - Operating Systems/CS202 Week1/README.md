# CS 202 · Operating Systems
## Week 1: Processes and Process Management

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 201, PROG 201
**Assessment for this course (overall):** Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%
**This week's deliverables:** PS 0 due **Friday**, PS 1 released **Wednesday**, **Quiz 1** at the start of **Monday's** lecture (covers Week 0).
**No lab session this week.** Lab 0 was sat on the Friday that closed Week 0; **Lab 1 covers this week and is sat on the Tuesday of Week 2.**

---

### Why This Week Exists

Because L03 left a process in the kernel with its registers saved in a trap frame — and never said what happens if the kernel decides not to return to it.

**This week is the kernel deciding.** A process is not a program and not a running thing; it is **a record the kernel keeps**, and most of the time it is not running at all — it is waiting in a table while something else uses the CPU. The whole of Week 1 is three questions about that record: **what is in it, how the kernel moves a process into and out of the CPU, and what memory map the process believes it has.**

Every answer is short in xv6 and measurable in Linux. **The context switch in xv6 is twenty-nine lines of assembly and saves four registers.** Linux's saves six. The interesting part is what neither of them saves, and what happens when a kernel forgets something — which xv6 does, and which you will see on Tuesday of next week as two processes getting each other's floating-point answers.

---

### Learning Objectives

By the end of Week 1, you should be able to:

1. **Name every field of xv6's `struct proc`** and say which week each belongs to.
2. Explain why Linux's `task_struct` holds pointers to `mm_struct`, `files_struct` and `cred`, and **what sharing those pointers makes a thread**.
3. **Measure a kernel structure's size without loading anything** — compile against the headers and read the symbol table.
4. Read `/proc/<pid>/status` and `stat`, and **parse `stat` correctly** when the command name contains spaces and parentheses.
5. Distinguish real, effective, saved and filesystem UIDs; explain set-user-ID; **say what a file capability grants and why `ping` drops it**.
6. Draw xv6's state machine and name the function behind each transition; **put a Linux process in each of R, S, D, T, t and Z on purpose**.
7. **Distinguish voluntary from involuntary context switches**, and read what kind of process something is from the two counters.
8. **Trace xv6's context switch** from the timer interrupt through `yield`, `sched`, `swtch` and the scheduler to the next process's `iret`.
9. **Explain why `swtch` saves only callee-saved registers**, and compare xv6's 20-byte context with Linux's 56-byte frame.
10. **Measure the cost of a context switch**, say what the measurement includes, and explain why it is higher across two CPUs.
11. **Say how Linux saves FPU state today, how the curriculum says it does, and what xv6 does** — with the measured consequence.
12. Read `/proc/<pid>/maps`; explain ASLR from three runs; **show that address space is not memory**.
13. Walk xv6's `allocproc`, `fork`, `exit` and `wait`, and **say why a new process starts by pretending to resume**.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L04 The Process and What the Kernel Keeps]] | xv6's 124-byte `struct proc`, field by field; **Linux's 9,920-byte `task_struct`**, measured without loading a module; `/proc` and its parsing trap; four UIDs; **41 capabilities, and `ping` holding one for under a second**; threads 5.6× cheaper than processes |
| [[L05 States and the Context Switch]] | Six states in xv6, seven in Linux, all produced on purpose; **1 running of 343**; hog 0/4,788 against sleeper 4,748/0; `swtch.S` in full; **1.6 µs per switch, 2.1 µs across CPUs**; FPU state is 1,088 bytes; **xv6's two FPU users sum to exactly 40,000,000** |
| [[L06 Address Spaces and a Process from fork to wait]] | The map from `main` to the stack; **ASLR in three runs and `0x555555555180` without it**; **256 MiB mapped, RSS unmoved**; `exec` and the one-page stack; `allocproc`, `fork`, `exit`, `wait`; IPC through the kernel |
| [[CS202 Week1/assignments/QUIZ 1 Week 1 Monday\|QUIZ 1 Week 1 Monday]] | Ten minutes, covers **Week 0**, answer key printed |
| [[PS 1 A Process Manager]] | Write `pm`, which reads the process table through `/proc`; measure what it shows; design xv6's missing FPU save. Due **Friday of Week 2** |
| `assignments/ps1/worker.c`, `test.pm` | The program `pm` manages, and the script it must run |
| [[LAB 1 Reading the Process Table]] | Maps, RSS, states, somebody else's `/proc`, and xv6's own table. **Tuesday of Week 2** |
| `lab/spin.c`, `lab/fpu.c` | Two xv6 user programs |
| [[CS202 Week1/resources/Reading Guide Week 1\|Reading Guide Week 1]] | OSTEP 4–6, the xv6 book's Chapters 1 and 5, and seven functions of `proc.c` |
| `resources/*.c`, `resources/tsize/` | Every program whose output appears in the lectures |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**State the kernel does not save is state that processes share.**

A context switch is a list of what to save, and everything not on the list is left in the CPU for the next process to find. **xv6's list has four registers on it.** For integer code that is enough, because the rest are in the trap frame or are the caller's responsibility. For floating-point code it is not — and two processes, each adding 0.5 twenty million times, should each have finished at 20,000,000 and finished at 39,552,364 and 447,636: **wrong answers that sum to exactly both right answers together**, because between them they did every addition into one register. On two CPUs it happened once in forty checkpoints instead of forty times.

Nothing crashed. Nothing was reported. **That is what a missing piece of isolation looks like from inside**: not an error, but two programs quietly computing each other's results. Linux saves 1,088 bytes of FPU state at every switch for exactly this reason — and stopped doing it lazily when lazily-saved state turned out to be readable by the next process, which is the same failure with an attacker in it.

---

### Assessment Reminder

**PS 0 is due Friday at 17:00. PS 1 is released Wednesday.**

**Labs and quizzes carry no weight** and are still required. **Quiz 1 is at the start of Monday's lecture and covers Week 0**; the answer key is printed in the paper.

> **There is no lab session in Week 1.** Lab 0 was sat on the Friday before this week; **Lab 1
> covers this week and is sat on the Tuesday of Week 2**, after all three of this week's lectures.

Both are tracked in [[_CS 202 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 0's L03 built the trap frame** that L05's context switch leaves on the kernel stack; **Week 0's `int13` fork** — the `int $64` with `eax = 1` — is L06's `fork` from the other side. **PROG 201 Weeks 0–1** are the user's view of every structure here: its zombies are L06's `exit`, its `fork` cost is L04 §6's comparison, its descriptor table is `ofile[16]`. **CS 201's calling convention** is why `swtch` saves four registers and not eight.

**Sideways:** **MATH 251's Week 1** is conditional probability; next week's scheduler is judged by averages of waiting times over distributions of job lengths, and L05's switch cost is one term in them.

**Forward:** **Week 2 is the one line of xv6 this week skipped** — the scheduler's loop, which picks the first `RUNNABLE` process it finds. PS 2 replaces it in simulation with MLFQ and CFS. **Week 3 explains the `ptable.lock`** that every function in L06 §5 acquires. **Week 5 is the page table** that `pgdir` points to and `copyuvm` copies. **Project 1, in Week 7, adds system calls and a scheduler to the `proc.c` you read this week.**

---

*CS 202 · Week 1 · © CSE Department*

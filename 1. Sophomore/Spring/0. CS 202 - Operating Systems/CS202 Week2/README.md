# CS 202 · Operating Systems
## Week 2: CPU Scheduling

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 201, PROG 201
**Assessment for this course (overall):** Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%
**This week's deliverables:** PS 1 due **Friday**, PS 2 released **Wednesday**, **Quiz 2** at the start of **Monday's** lecture (covers Week 1).
**Lab 1 is sat on the Tuesday of this week**; **Lab 2 covers this week and is sat on the Tuesday of Week 3.**

---

### Why This Week Exists

Because Week 1 built a mechanism that switches from one process to another in 1.6 µs, and never said which one.

**A scheduler is a policy, and every policy is an argument about what "good" means.** Fastest average finish? Quickest reaction to a keystroke? A fair share for everyone? A guarantee that a brake controller never misses? **These goals conflict**, and this week measures the conflict in a simulator you will extend, then measures what the kernel on your machine actually decided.

That second half has surprises. **Every textbook describes a scheduler this kernel no longer uses.** The priority settings you can change do exactly what their tables say, to a tenth of a percent — within a group. The ones you cannot change are refused for a reason worth understanding. And **one setting that is switched on does nothing at all**, which you will find by measuring the thing it promises.

---

### Learning Objectives

By the end of Week 2, you should be able to:

1. Define turnaround, response and waiting time, and **show with numbers how optimising one hurts another**.
2. Explain the convoy effect, **prove SJF optimal by an exchange argument**, and say what SRTF adds.
3. **Read a round-robin quantum sweep**: say where RR becomes FCFS and what a short quantum costs.
4. State MLFQ's five rules; **demonstrate gaming and starvation, and the rule that fixes each**.
5. Explain proportional share, CFS's `vruntime` and weight table, and **predict a nice value's CPU share** — then check it on Linux.
6. Say **what Linux 7.0 runs instead of CFS**, show the evidence in the headers and `/proc/<pid>/sched`, and measure its slice.
7. **Explain why autogroup does nothing on the lab machines**, and how a cgroup weight lets a nice-19 process take half a CPU.
8. Apply the **Liu–Layland bound** and **response-time analysis** to a periodic task set; say why EDF succeeds where RM misses, and why RM is used anyway.
9. **List Linux's scheduling classes in order**, and say which an unprivileged account may use and why the rest are refused.
10. **Account for wake-up latency** in terms of timer slack and CPU idle states, with measurements.
11. Read xv6's scheduler and **name three things it lacks** that Project 1 will add.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L07 What a Scheduler Is For and the Classic Policies]] | Metrics; **FCFS 110 ms against SJF 50 ms** on the convoy; the exchange proof; SRTF; **the RR quantum sweep**; an editor waiting 10.0 ms under FCFS and 1.3 under RR; **xv6 is round robin at 100.1 ticks per second** |
| [[L08 MLFQ Fair Share and What Linux Runs Now]] | MLFQ at **0.4 ms** per keystroke; **gaming: 241 against 400, reversed by one rule**; starvation 900 → 422 with the boost; **Linux's nice shares within 0.2 points of the table**; **EEVDF, not CFS**, from the headers; **3.00 ms slices** for 2, 3 or 4 hogs; **autogroup on and inert; a nice-19 hog at 58%** |
| [[L09 Real Time and What Linux Lets You Ask For]] | RM above its bound with no misses; **RM missing at 7 ms where EDF does not**; Linux's classes; **`SCHED_FIFO`, `SCHED_DEADLINE` and negative nice refused**; the 95% real-time cap; **latency: 50 µs of slack, 4 µs of waking, and 90 µs more on an idle CPU** |
| [[CS202 Week2/assignments/QUIZ 2 Week 2 Monday\|QUIZ 2 Week 2 Monday]] | Ten minutes, covers **Week 1**, answer key printed |
| [[PS 2 Simulating MLFQ and a Fair Scheduler]] | Finish `schedsim`'s MLFQ and fair policies to exact expected output; sweep the allotment and the boost; compare the model with the machine. Due **Friday of Week 3** |
| `assignments/ps2/schedsim.c`, `assignments/ps2/workloads/` | The simulator skeleton — four policies done, two for you — and seven workloads |
| [[LAB 2 Priorities Policies and Who Is Allowed]] | `nice` measured; `chrt` refused; groups; slices; latency. **Tuesday of Week 3** |
| `lab/hog.c`, `lab/cpushare.sh` | A CPU hog, and a script that measures CPU shares from `/proc` |
| [[CS202 Week2/resources/Reading Guide Week 2\|Reading Guide Week 2]] | OSTEP 7–9, Silberschatz §5.6, and a caution about "what Linux does" |
| `resources/*.c` | `share.c`, `slice.c`, `lat.c`, `rtsim.c` — every Linux and real-time number in the lectures |
| `solutions_instructor/` | Instructor only — including the reference simulator |

---

### The One Thing to Take From This Week

**A scheduler's knobs are only meaningful inside the structure that contains them.**

`nice` is the proof. Measured on its own, it is perfect: nice 1 gave 44.4% where the table says 44.5%, nice 10 gave 9.7% where it says 9.7%. **Then the same nice-19 process, moved into its own cgroup, took 58% of a CPU from a nice-0 process** — not because `nice` broke, but because the kernel divides the CPU between groups first and only then among the tasks inside each. **And autogroup, whose whole purpose is that division, is switched on and does nothing** here, because these processes already sit below a CPU group.

It is the pattern of Weeks 0 and 1 in a new place: **a setting you can read is not a setting that operates.** The only way to know which is to predict what it should do, and measure.

---

### Assessment Reminder

**PS 1 is due Friday at 17:00. PS 2 is released Wednesday.**

**Labs and quizzes carry no weight** and are still required. **Quiz 2 is at the start of Monday's lecture and covers Week 1**; the answer key is printed in the paper.

> **Two labs touch this week.** **Lab 1** — Week 1's process table — is sat on the **Tuesday of this
> week**. **Lab 2** covers this week and is sat on the **Tuesday of Week 3**.
>
> **Midterm 1 is announced in Week 3** and sat on the Monday of Week 4, covering Weeks 0–3. This
> week is on it.

Both are tracked in [[_CS 202 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 1's voluntary and involuntary counters** are MLFQ's input — a process that blocks early is a process that gives up the CPU voluntarily. **Week 1's 1.6 µs context switch** is the cost L07's quantum sweep ignores and PS 2 Q5 asks you to put back. **Week 0's privilege boundary** is why `SCHED_FIFO` is refused: it is a request to take the CPU from every other user.

**Sideways:** **MATH 251** is at conditional probability and random variables this week; a scheduler's average waiting time is an expectation over a distribution of job lengths, and lottery scheduling is a sampling problem. **ECE 211's** periodic signals are the same model as L09's periodic tasks.

**Forward:** **Week 3's locks** are what a scheduler must never be caught holding when it switches — xv6's `ptable.lock`, acquired in every line of L07 §8's loop, is the first one you will read. **Week 6's thrashing** is a scheduling problem in disguise: processes runnable but unable to make progress. **Project 1 in Week 7 adds priorities, accounting and a scheduler of your choice to xv6**, measured with the simulator you finish in PS 2.

---

*CS 202 · Week 2 · © CSE Department*

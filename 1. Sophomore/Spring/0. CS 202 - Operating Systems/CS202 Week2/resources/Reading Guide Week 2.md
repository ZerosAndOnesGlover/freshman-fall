# CS 202 · Reading Guide · Week 2
## OSTEP Chapters 7–9, and what Linux does now

---

**The curriculum names no reading for Week 2.** OSTEP's scheduling chapters are the obvious one, and they are short. **One caution before you start**: every textbook this course uses describes Linux's *Completely Fair Scheduler*, and the reference machine's kernel no longer uses CFS's selection rule. L08 §6 shows the evidence. Read the chapters for the ideas — which are still right — and read L08 for what the kernel in front of you actually does.

| Source | Now? | Why |
|---|---|---|
| **OSTEP 7. Scheduling: Introduction** | **Read** | Metrics, FCFS, SJF, STCF, round robin, I/O. **This is L07** |
| **OSTEP 8. Scheduling: The Multi-Level Feedback Queue** | **Read** | The five rules, gaming, starvation, the boost. **This is L08 §1–§3** |
| **OSTEP 9. Scheduling: Proportional Share** | **Read** | Lottery, stride, and **the section on Linux's CFS**. L08 §4–§5 |
| OSTEP 10. Multiprocessor Scheduling | *Skim* | Cache affinity and per-CPU queues. Worth knowing exists; not examined this week |
| **xv6 book, Ch. 5 "Scheduling"** | **Re-read the scheduling sections** | You read the context switch last week; now read what calls it |
| **Silberschatz, Ch. 5 §5.6** | **Read** | Real-time scheduling: rate-monotonic and EDF. **L09 §1–§2** |

**If you have three hours this week:** OSTEP 8, then 7, then the CFS section of 9, then Silberschatz §5.6.

---

## OSTEP Chapter 7 — the assumptions, dropped one at a time

OSTEP starts with five assumptions — jobs run for the same time, arrive together, run to completion, use only CPU, and have known lengths — and relaxes them in order. **Keep a list of which assumption each policy needs.**

1. For each of FIFO, SJF, STCF and RR, **which of OSTEP's five assumptions does the policy still depend on?** Which policy depends on the one no OS can provide?
2. OSTEP's Figure 7.7 shows round robin's response time against a quantum. **Reproduce the shape with `schedsim rr:Q < convoy.txt`** for the quanta in L07 §6, and say what the figure leaves out that L07's table includes.
3. §7.8 "Incorporating I/O" treats each CPU burst of an I/O job as a separate job. **Why does this make STCF favour interactive jobs automatically?** Would round robin?

---

## OSTEP Chapter 8 — MLFQ

The chapter builds MLFQ from rules and breaks each version. Read it with `schedsim` open.

4. OSTEP's first version of Rule 4 lets a job keep its priority if it gives up the CPU before its slice ends. **Construct the attack** in `schedsim`'s workload format, then check it against `gamer.txt` in the PS 2 workloads. How close was yours?
5. The priority boost (Rule 5) solves two problems. **Name both.** L08 measures one; describe a workload for the other.
6. OSTEP calls the boost interval *S* a "voo-doo constant". **What goes wrong if *S* is too large, and what goes wrong if it is too small?** Give a number for each extreme on `starve.txt`.
7. §8.5 mentions that Solaris's MLFQ is configured by a table of 60 priority levels. **What would you have to measure on a real workload to choose that table well?**

---

## OSTEP Chapter 9 — proportional share, and CFS

8. Lottery scheduling is probabilistic. **For two jobs with 75 and 25 tickets, how many lotteries until the 25-ticket job has had within 5% of its share with high probability?** (The chapter's Figure 9.2 gives the shape; an estimate is fine.)
9. Stride scheduling is deterministic. **Why is it harder than lottery to add a new job to a running stride scheduler?** What would the new job's pass value have to be?
10. **Read OSTEP's CFS section closely.** It describes `sched_latency`, `min_granularity`, weights and `vruntime`. Now look at `/proc/self/sched` on the reference machine (L08 §6): **which of those names appear, and which field does not appear in OSTEP at all?**
11. OSTEP says CFS uses a red-black tree so that finding the next job is O(log *n*). **Why is a heap not good enough?** *(What else must the scheduler do with the set of runnable jobs?)*

---

## Silberschatz §5.6 — real time

12. **State the Liu–Layland bound for rate-monotonic scheduling** and compute it for *n* = 1, 2, 3 and as *n* → ∞.
13. The bound is *sufficient*, not *necessary*. **L09 §2 has a task set above the bound that rate-monotonic schedules without a miss.** Before reading it, construct one of your own and check it with `rtsim`.
14. **Why does EDF not need a bound below 1**, and why do systems use rate-monotonic anyway? Give one practical reason and one reason about what happens under overload.

---

## Where to Go Deeper

| Source | Topic | When |
|---|---|---|
| **Love**, Ch. 4 | Process scheduling in Linux — CFS as of 2.6.34 | For the design and the vocabulary. **The selection rule has since changed**; L08 §6 |
| `man 7 sched` | Every Linux scheduling policy, its priorities and its permissions | **Before Lab 2** |
| `man 1 chrt`, `man 1 nice`, `man 2 sched_setattr` | Changing policy and priority | **Before Lab 2** |
| `Documentation/scheduler/sched-design-CFS.rst` and `sched-eevdf.rst` in the kernel source | CFS and its replacement, by their authors | Optional — the source is not on the lab image; read online |
| **Liu, C.L. & Layland, J.W.** (1973), "Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment", *JACM* | The paper behind the bound | Optional, and short |

**The man page you must have read before Lab 2:** `sched(7)`, the section on privileges and resource limits. Lab 2's first surprise is in it.

---

## The One Habit This Guide Is Trying To Build

**When a book says what "Linux does", check which Linux.**

OSTEP, Silberschatz and Love all describe CFS, and all were right when written. The kernel on the reference machine selects tasks by a different rule, and the evidence is one `grep` of its headers and one `cat` of `/proc/self/sched`. **Books describe the design that was current when they were written; the machine is always current.** Week 1 found the same thing with the FPU. It will not be the last time.

---

*CS 202 · Week 2 · Reading Guide · © CSE Department*

# CS 202 · Quiz 3
## Administered: Monday, Week 3 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 2** — scheduling metrics and policies, MLFQ, proportional share, Linux's scheduler, and real-time scheduling.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.
>
> Do not look at the key first. It costs you the only thing the exercise is for.

---

**Q1.** Three jobs arrive together needing 100, 10 and 10 ms. Give the average turnaround under FCFS (in that order) and under SJF.

&nbsp;

&nbsp;

---

**Q2.** Round robin's quantum is made very large. What policy does it become?

&nbsp;

&nbsp;

---

**Q3.** MLFQ's naive Rule 4 let a job keep its priority if it blocked before its quantum ended. How is that gamed, and what is the fix?

&nbsp;

&nbsp;

---

**Q4.** Two CPU hogs share one CPU; one is nice 0 (weight 1,024) and one is nice 10 (weight 110). What share does the nice-10 hog get?

&nbsp;

&nbsp;

---

**Q5.** Name the scheduling algorithm the reference machine's Linux actually uses in its fair class, and one measured way its slices differ from a latency-divided model.

&nbsp;

&nbsp;

---

**Q6.** Why does `chrt -f 10 ./prog` fail for an ordinary user, and why is raising your own nice value allowed?

&nbsp;

&nbsp;

---

**Q7.** Two periodic tasks, 2 ms every 5 and 4 ms every 7, have utilisation 0.971. Which of rate-monotonic and EDF schedules them without a miss?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **FCFS: 110 ms** — finishes at 100, 110, 120. **SJF: 50 ms** — finishes at 10, 20, 120.

---

**Q2.** **FCFS.** No job ever uses up its quantum, so none is ever preempted. At a 100 ms quantum on that workload the numbers are identical.

---

**Q3.** **Block just before the quantum ends** — for 1 ms after every 9 of a 10 ms quantum — and stay at top priority forever while computing. A gaming job finished in 241 ms against an honest one's 400. **Fix: charge the allotment for CPU used at a level, however many times the job blocked.** The honest job then finished first, 263 against 415.

---

**Q4.** 110 / (1024 + 110) = **9.7%**. Measured on the reference machine: 9.5–9.7%.

---

**Q5.** **EEVDF** — Earliest Eligible Virtual Deadline First — since Linux 6.6. **Its slice stayed at 3.00 ms whether two, three or four hogs competed**; a model that divides a latency target among jobs would shorten it as jobs are added.

---

**Q6.** **`SCHED_FIFO` needs `RLIMIT_RTPRIO` > 0 or `CAP_SYS_NICE`**, and an ordinary account has `ulimit -r` = 0. A FIFO task outranks every fair-class task, so allowing it would let one user take a CPU from all others. **Raising your own nice costs only yourself.**

---

**Q7.** **EDF.** Rate-monotonic misses at *t* = 7: task 1's second release preempts task 2 one millisecond before it finishes. EDF schedules any such set with *U* ≤ 1.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L07 §3–§6 |
| **Q3** | **L08 §2** — the principle recurs in Week 12 |
| Q4, Q5 | L08 §4 and §6 |
| Q6 | L09 §5 |
| Q7 | L09 §2–§3 |

**Midterm 1 is next Monday evening and covers Weeks 0–3.** Every question on this quiz is fair game for it.

---

*CS 202 · Week 3 · Quiz 3 · covers Week 2 · ungraded*

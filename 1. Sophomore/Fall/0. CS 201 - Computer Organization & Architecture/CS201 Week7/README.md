# CS 201 · Computer Organization & Architecture
## Week 7: I/O Systems and Storage

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), ECE 110 (digital logic)
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **PROJECT 1 assigned (10%, due Week 9)**, PS 7 (due Week 8 Friday), Lab 7 *(sat Tuesday of Week 8)*, and **Quiz 7 on Monday, covering Week 6**.

> ⚠️ **Project 1 is assigned this week and is worth 10%.** It is three weeks of work and the failure
> mode is starting in Week 9. Milestones are in the specification — **have one program running end to
> end by Friday.**

---

### Why This Week Exists

Because Week 6's cost table stopped at 1.9 μs, and the world does not.

This week supplies the bottom of the ladder — and the bottom is a long way down. **An `fsync` costs about three million times an L1 hit**, on the same machine, measured this week. Everything about how storage systems are built follows from that spread: the page cache, read-ahead, group commit, log-structured writing, B-trees with hundreds of children.

**It is also the week where the hardware changed under the software.** Half the material — elevator scheduling, defragmentation, seek-avoidance — was written for a mechanical constraint that the machine in front of you does not have. **Deciding which of those ideas survive on their own merits is the interesting part**, and the lecture says plainly which numbers are measured here and which are cited.

---

### Learning Objectives

By the end of Week 7, you should be able to:

1. Decompose a disk access into seek, rotation and transfer, and compute each.
2. Explain why large requests are nearly free on a disk, and name three designs that exploit it.
3. Explain why flash cannot overwrite in place, and what the FTL does about it.
4. Define write amplification and wear levelling, and compute a drive's usable host writes.
5. Compare polling, interrupts and DMA, and say when each is right.
6. Explain why DMA needs pinned pages and scatter-gather lists.
7. Distinguish latency, IOPS and throughput, and apply Little's Law.
8. **Say whether a storage measurement describes the device or the page cache.**
9. Explain what `fsync` costs and why databases batch commits.
10. Trace FCFS, SSTF, SCAN, C-SCAN and LOOK, and explain SSTF's starvation.
11. Explain why Linux schedules NVMe with `none`.
12. **Report a measurement from a shared machine with its variance.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L22 The I O Path Controllers Interrupts and DMA.md` | The cost ladder's bottom, the device as a computer, DMA, and the page cache at 63× |
| `lectures/L23 Disks and SSDs.md` | The mechanical model, flash and the FTL, and this machine's measured curve |
| `lectures/L24 Storage Performance and Scheduling.md` | IOPS vs throughput, Little's Law, tail latency, the schedulers, and why Linux uses none |
| `assignments/PROJECT 1 Mini-CPU Simulator.md` | **10%, due Week 9.** Build the machine you have spent seven weeks observing |
| `assignments/PS 7 Disk Scheduling and Storage Performance.md` | The mechanical model, flash, a scheduler simulator, and your own device |
| `assignments/QUIZ 7 Week 7 Monday.md` | Ten minutes on Week 6. **Unmarked — key in the paper** |
| `lab/LAB 7 Benchmarking Storage.md` | `O_DIRECT`, sequential vs random, the page cache, and what durability costs |
| `resources/Reading Guide Week 7.md` | CS:APP §6.1 and §10, and which of its numbers to distrust |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Find out whether you are measuring the device or the page cache. They differ by 63×.**

```
buffered, cached 4K random :   398063 IOPS     2.51 us/op
O_DIRECT 4K random (device):     6345 IOPS   157.60 us/op
```

*(Measured.)* **The only difference is whether the data happened to be in DRAM.**

And the number that explains database architecture:

```
200 x 4K write, no fsync   :     6.0 us/write
200 x 4K write + fsync each:  3876.3 us/write
```

*(Measured — 645×.)* A system committing 10 000 transactions per second has a 100 μs budget per transaction. **One `fsync` costs 3900 μs.** Durability is not a flag you set; it is a constraint you design around, and **group commit is the answer the whole industry converged on.**

---

### Assessment Reminder

**Labs and quizzes carry no weight**; the four weighted components already total 100%. Both remain required.

**Quiz 7 is Monday**, covering Week 6. **Lab 7 is sat Tuesday of Week 8.**

**A note on the hardware.** The lab machines have an NVMe SSD and **no rotating disk**. Every SSD figure this week is measured; **every HDD figure is cited from manufacturer specifications and says so.** You cannot reproduce the disk numbers here, and knowing the difference between a number you measured and a number you were told is part of the point.

---

### Connections

**Back:** **Week 6's page cache** is the same structure, backed by files instead of swap — and a major page fault is now a number rather than a category. **Week 4's hierarchy** extends outward by two more levels. **Week 6's `mmap`** is how a file becomes memory, and this week explains what happens when you touch a page of it.

**Forward:** **Week 8's networks** are the other direction data travels, with a similar latency story and a worse tail. **Week 11's roofline** needs the distinction between latency-bound and throughput-bound that Little's Law formalises here. **Project 2 in Week 12** extends Project 1 with the cache from Week 4.

**Sideways:** **PROG 201 is writing to files and sockets this term** and CS 202 next semester implements the page cache, the block layer and the scheduler. **OSTEP chapters 37–38 and 44** are that course's treatment and are better than the textbook's.

---

*CS 201 · Week 7 · © CSE Department*

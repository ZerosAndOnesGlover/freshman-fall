# CS 201 · Computer Organization & Architecture
## Week 7 · Lecture 3 of 3
### Storage Performance and I/O Scheduling

*“Around computers it is difficult to find the correct unit of time to measure progress. Some cathedrals took a century to complete. Can you imagine the grandeur and scope of a program that would take as long?”* — Alan Perlis, "Epigrams on Programming" (1982), #28

---

**Reading:** CS:APP §6.1.5, §10.6 · **Previous:** L23, disks and SSDs

**Coursework:** 📝 **PS 6** due today 17:00 · 📊 **Quiz 8** Mon of Week 8 · 🔬 **Lab 7** Tue of Week 8 15:00–16:50 · 📝 **PS 8** released Wed of Week 8, due Fri of Week 9 17:00

---

## 1. Three Numbers, and They Are Not Interchangeable

| Metric | Definition | Unit |
|---|---|---|
| **Latency** | Time for **one** operation to complete | μs, ms |
| **IOPS** | Operations completed **per second** | ops/s |
| **Throughput** | Bytes moved per second | MB/s |

**These are related but not derivable from one another**, and confusing them is the most common error in storage work.

$$\text{throughput} = \text{IOPS} \times \text{block size}$$

From the measured table:

| block | IOPS | throughput |
|---:|---:|---:|
| 4 KiB | 12 746 | 49.8 MiB/s |
| 1 MiB | 1 884 | 1884 MiB/s |

**The 4 KiB case does 6.8× more operations and moves 38× less data.** Which number is "better" depends entirely on what you are doing — a database doing point lookups cares about IOPS; a video pipeline cares about throughput; an interactive application cares about neither and only about **tail latency**.

### Little's Law

$$\text{concurrency} = \text{throughput} \times \text{latency}$$

A device at 12 746 IOPS with 157 μs latency is running at $12746 \times 0.000157 \approx 2$ operations in flight.

**This is why queue depth is the missing variable.** A single-threaded benchmark holds concurrency at ~1 and therefore **measures latency, not capability.** An NVMe drive with dozens of flash channels needs many outstanding requests to show what it can do — which is exactly what the measurements in L23 do *not* do, and why they should be read as latency figures.

---

## 2. Averages Lie

A storage system's mean latency is nearly useless. **What users experience is the tail.**

| Percentile | Meaning |
|---|---|
| p50 | Half of requests are faster |
| p99 | **1 in 100 is slower** |
| p99.9 | 1 in 1000 |

**If a page load makes 100 storage requests and waits for all of them, the p99 is what the user sees**, not the median — because with 100 requests, hitting the 1% case at least once is near-certain.

**Tail latency on flash has specific causes**, all from L23: garbage collection pausing to relocate valid pages, wear-levelling relocations, and the drive's internal write cache filling. **A drive that is fast on an empty benchmark can be far slower when full and fragmented.**

---

## 3. Ordering Requests

Given a queue of pending requests, in what order should they be served?

**On a rotating disk this question is worth an order of magnitude**, because the arm's position determines the cost of the next request.

| Algorithm | Rule | Problem |
|---|---|---|
| **FCFS** | Serve in arrival order | Ignores geometry. Arm thrashes |
| **SSTF** | Shortest seek time first — nearest track next | **Starvation**: a distant request may wait forever while nearby ones keep arriving |
| **SCAN** *(elevator)* | Sweep to one end serving everything, then reverse | No starvation. **Middle tracks get served twice as often** as edges |
| **C-SCAN** | Sweep one way only, then jump back without serving | Uniform waiting time — fairer, at the cost of the return trip |
| **LOOK / C-LOOK** | As SCAN/C-SCAN, but reverse at the **last request** rather than the physical end | Strictly better; what real implementations use |

**Work an example.** Head at track 53; queue 98, 183, 37, 122, 14, 124, 65, 67; disk 0–199.

| Algorithm | Service order | Head movement |
|---|---|---:|
| **FCFS** | 98, 183, 37, 122, 14, 124, 65, 67 | **640** |
| **SSTF** | 65, 67, 37, 14, 98, 122, 124, 183 | **236** |
| **SCAN** *(down first)* | 37, 14, **0**, 65, 67, 98, 122, 124, 183 | **236** |
| **SCAN** *(up first)* | 65, 67, 98, 122, 124, 183, **199**, 37, 14 | **331** |
| **LOOK** *(down first)* | 37, 14, 65, 67, 98, 122, 124, 183 | **208** |
| **C-SCAN** *(up)* | 65, 67, 98, 122, 124, 183, **199 → 0**, 14, 37 | **382** |

*(All computed; PS 7 asks you to derive them.)*

**The direction matters as much as the algorithm.** SCAN downward costs 236 and upward costs 331 on the identical queue — because going up first means travelling to track 199 and all the way back for two low requests. **A textbook that quotes "SCAN = 236" has silently chosen a direction.**

**LOOK beats SCAN in every case** — 208 against 236 — by reversing at the last *request* rather than the physical end of the disk. It is strictly better and is what real implementations use; SCAN is taught because the invariant is easier to state.

**C-SCAN is the most expensive here at 382**, and that is the point: it buys **uniform waiting time** by refusing to serve on the return sweep. Under SCAN, a track in the middle is visited twice per cycle and a track at the edge once. **C-SCAN pays travel to make the wait fair**, which is the same trade as SCAN over SSTF, one level further along.

**SSTF's problem is not efficiency, it is fairness.** It is greedy and unbounded — under a steady stream of nearby requests, a far one never runs. **SCAN gives up a little efficiency for a bounded waiting time**, and that trade is the entire reason it won.

---

## 4. What Linux Actually Does Now

```
$ cat /sys/block/nvme0n1/queue/scheduler
[none] mq-deadline
```

*(Verified on this machine.)*

**The scheduler is `none`.** No reordering at all.

**This is not an oversight.** On flash there is no arm to optimise, and the drive has far better information about its own internal parallelism than the kernel does. **Reordering in the kernel would add latency and destroy the sequentiality the FTL wants.** So the kernel passes requests straight through, in multiple hardware queues, one per CPU — the `blk-mq` design.

`mq-deadline` remains available, and is still the right choice for rotating disks, where it enforces a deadline to prevent the starvation SSTF suffers from.

> **This is the week's clearest case of hardware changing software.** Decades of scheduling
> literature — SSTF, SCAN, C-LOOK, anticipatory scheduling — was written for a mechanical constraint
> that most machines no longer have. **The algorithms are still worth knowing**, both because
> rotating disks persist in bulk storage and because *the reasoning* transfers: the same
> fairness-against-efficiency argument reappears in CPU scheduling, network queueing and lock
> acquisition. **But the default on your laptop is to do nothing at all**, and knowing why is the
> point.

---

## 5. The Whole Ladder

Everything the course has measured, in one place:

| Event | Time | Cycles @3.2 GHz | Measured in |
|---|---:|---:|---|
| L1 cache hit | 1.2 ns | 4 | Week 4 |
| L2 hit | 3.4 ns | 12 | Week 4 |
| L3 hit | 12.1 ns | 41 | Week 4 |
| DRAM access | 137 ns | 438 | Week 4 |
| Minor page fault | 1.9 μs | ~6 200 | Week 6 |
| **Page-cache hit** | **2.5 μs** | **~8 000** | **Week 7** |
| **SSD 4 KiB read** | **~80–160 μs** | **~300 000** | **Week 7** |
| **`fsync`** | **~3.9 ms** | **~12 500 000** | **Week 7** |
| HDD seek + rotation | ~10 ms | ~32 000 000 | *cited* |

**Seven orders of magnitude, all on one machine.**

**The two adjacent rows worth staring at** are the page-cache hit at 2.5 μs and the device read at ~157 μs — **63× apart**, and the *only* difference is whether the data happened to be in DRAM. Everything the operating system does around storage exists to make the first row happen more often.

**And `fsync` at 3.9 ms against a 6 μs write** is 645×. **Durability is not a flag you set; it is a design constraint you build around.**

---

## 6. What to Take Away

1. **Latency, IOPS and throughput are three different questions.** 4 KiB gives 6.8× the IOPS and 38× less throughput than 1 MiB.
2. **Little's Law**: single-threaded benchmarks measure latency, not device capability.
3. **The tail is what users experience**, and flash tails come from garbage collection.
4. **FCFS, SSTF, SCAN, C-LOOK** — and SSTF's flaw is starvation, not inefficiency.
5. **Linux schedules NVMe with `none`**, because the drive knows better and there is no arm.
6. **Seven orders of magnitude** from L1 to `fsync`.
7. **The page cache is worth 63×; `fsync` costs 645×.**

---

## Exercises

1. A device sustains 50 000 IOPS at 4 KiB. Give its throughput. Another sustains 500 MB/s at 1 MiB. Give its IOPS. Which is better for a database doing point lookups?
2. Use Little's Law to find the concurrency needed for 100 000 IOPS at 200 μs latency. What does that tell you about single-threaded benchmarking?
3. Head at 53; queue 98, 183, 37, 122, 14, 124, 65, 67. Compute total head movement for FCFS, SSTF and SCAN (upward). Show the service order for each.
4. Construct a request stream that starves a specific request under SSTF. Then show SCAN's bound on waiting time.
5. Your service has a 5 ms median and a 200 ms p99. A page makes 50 independent storage requests and waits for all. Estimate what the user experiences, and explain why the median is irrelevant.
6. Explain why `none` is the right scheduler for NVMe but the wrong one for a 7200 rpm disk. Which property of the device decides it?
7. From §5's table: how many L1 hits fit in one `fsync`? How many DRAM accesses in one SSD read?

---

*Next week: computer networks — the other direction data travels.*

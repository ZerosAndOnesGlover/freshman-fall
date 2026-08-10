# CS 201 · Problem Set 7
## Disk Scheduling and Storage Performance

---

**Released:** Week 7, Wednesday · **Due:** Week 8, Friday 17:00
**Total: 100 points** · Submit one PDF plus a `.zip` of source, `PS7_{LastName}_{StudentID}.pdf`

> **Project 1 is also assigned this week and is due in Week 9.** Do not let this problem set crowd it
> out — Q3 here is deliberately smaller than PS 6's simulator for that reason.

---

### Q1: The Mechanical Model (18 points)

**(a) [4]** Give the three components of a rotating-disk access. For a 7200 rpm drive with a 9 ms average seek and 150 MB/s transfer, compute each for a **4 KiB** read and state what fraction is spent transferring data.

**(b) [3]** Derive average rotational latency for 5400, 7200 and 15 000 rpm. Explain why the average is **half** a revolution.

**(c) [4]** Repeat (a) for a **1 MiB** read. State the ratio of total time to (a), and draw the design conclusion about block sizes.

**(d) [4]** Sequential and random throughput on a disk differ by ~1000×. On the flash drive measured in Lab 7 the ratio at 1 MiB is **1.06×**. Name **two** system designs from the disk era that this change makes questionable, and **one** that it makes more relevant.

**(e) [3]** An SSD has no seek. Random 4 KiB is nonetheless **2.27×** slower than sequential *(measured)*. Give two reasons.

---

### Q2: Flash (16 points)

**(a) [4]** Define **page** and **erase block** and give typical sizes. State the rule that makes in-place overwrite impossible.

**(b) [4]** Explain what the **FTL** does and why the block-device abstraction of L22 §4 could not exist without it.

**(c) [4]** Define **write amplification**. A drive reports a factor of 4 and is rated for 300 TBW. How many terabytes may the host write? Show the arithmetic.

**(d) [4]** Explain **wear levelling**, and describe what would happen to a drive without it under a workload that rewrites one 4 KiB metadata block a thousand times a second.

---

### Q3: Simulate the Schedulers (26 points)

Write a program that, given a starting head position, a disk size and a request queue, reports the service order and total head movement for **FCFS, SSTF, SCAN, C-SCAN and LOOK**.

**(a) [12]** The implementation. SCAN and C-SCAN must take a direction argument.

**(b) [6]** Run it on head 53, disk 0–199, queue 98, 183, 37, 122, 14, 124, 65, 67.

Reference *(computed)*:

| Algorithm | Movement |
|---|---:|
| FCFS | 640 |
| SSTF | 236 |
| SCAN down | 236 |
| SCAN up | 331 |
| LOOK down | 208 |
| C-SCAN up | 382 |

**Reproduce these and show the service order for each.**

**(c) [4]** **SCAN costs 236 downward and 331 upward on the identical queue.** Explain the difference, and say what that implies about any textbook that quotes a single SCAN figure.

**(d) [4]** **Demonstrate SSTF starvation.** Construct a request stream — arriving over time, not all at once — in which one request is never served. Show the trace. Then state the bound SCAN provides and prove it informally.

---

### Q4: Measure Your Storage (24 points)

**(a) [4]** Report your device: model, size, and rotational flag. State whether the figures that follow are flash or disk.

**(b) [6]** Reproduce Lab 7 Part 2 — sequential and random `O_DIRECT` reads from 4 KiB to 1 MiB. Report the table.

Reference *(verified)*: 4 KiB gives 113.2 / 49.8 MiB/s; 1 MiB gives 2005.9 / 1884.0 MiB/s.

**(c) [4]** **Sequential throughput rises 18× from 4 KiB to 1 MiB.** Explain what is limiting the small-block case. Use Little's Law to argue that a single-threaded benchmark measures latency rather than device capability.

**(d) [5]** Measure the page cache: buffered cached reads against `O_DIRECT`.

Reference *(verified)*: **398 063 IOPS at 2.51 μs** against **6 345 IOPS at 157.6 μs** — **63×**.

Place both on the course's cost ladder alongside L1 (1.2 ns), DRAM (137 ns) and a minor page fault (1.9 μs).

**(e) [5]** Measure `fsync`.

Reference *(verified)*: **6.0 μs/write** without, **3876 μs/write** with — a **645×** ratio.

Then: a database commits 10 000 transactions per second and promises durability. **Show that one `fsync` per transaction is impossible**, and name the technique that keeps the promise anyway.

---

### Q5: Reading the Numbers (16 points)

**(a) [4]** A device does 50 000 IOPS at 4 KiB; another does 500 MB/s at 1 MiB. Give the missing metric for each. Which suits a key-value store doing point lookups, and which a video transcoder?

**(b) [4]** State **Little's Law**. Compute the concurrency needed to sustain 100 000 IOPS at 200 μs latency, and say what that means for benchmarking with one thread.

**(c) [4]** Your service has a 5 ms median and a 200 ms p99. A page issues 50 independent storage requests and waits for all of them. Estimate what the user experiences and explain why the median is the wrong number to quote.

**(d) [4]** `cat /sys/block/nvme0n1/queue/scheduler` reports `[none] mq-deadline` *(verified)*.

Explain why doing no scheduling is correct here, why it would be wrong on a 7200 rpm disk, and **what the decades of scheduling literature are still good for.**

---

## Marks

| | |
|---|---:|
| Q1 The Mechanical Model | 18 |
| Q2 Flash | 16 |
| Q3 Simulate the Schedulers | 26 |
| Q4 Measure Your Storage | 24 |
| Q5 Reading the Numbers | 16 |
| **Total** | **100** |

---

*CS 201 · Week 7 · Problem Set 7*

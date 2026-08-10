# CS 201 · Problem Set 7 — Solutions
## Instructor Only

---

> **Not for distribution.** SSD figures measured on the lab image (Samsung MZVLB256HAHQ NVMe).
> **HDD figures are cited, not measured — there is no rotating disk in the building.**

---

## Q1 (18) — The Mechanical Model

### (a) [4]

| | Time |
|---|---:|
| Seek | 9 ms |
| Rotational latency | 4.17 ms |
| Transfer of 4 KiB at 150 MB/s | **0.027 ms** |
| **Total** | **13.20 ms** |

$$\frac{0.027}{13.20} = \mathbf{0.21\%}$$

**About one part in five hundred is spent moving data.** The rest is waiting for machinery.

### (b) [3]

$$t = \frac{1}{2}\times\frac{60}{\text{rpm}} \text{ s}$$

| rpm | latency |
|---:|---:|
| 5400 | 5.56 ms |
| 7200 | **4.17 ms** |
| 15 000 | 2.00 ms |

**Half a revolution** because the target sector is equally likely to be anywhere on the track: uniformly distributed over $[0, T]$, mean $T/2$.

### (c) [4]

1 MiB at 150 MB/s = 6.99 ms transfer, so **total 20.16 ms**.

$$\frac{20.16}{13.20} = \mathbf{1.53\times \text{ the time for } 256\times \text{ the data}}$$

**Conclusion:** the fixed cost dominates so heavily that large blocks are nearly free. **This is why filesystems use large blocks, databases read ahead, and B-trees have hundreds of children per node** — every one is amortising a seek.

### (d) [4]

**[2] Two designs made questionable** — any two, argued:

- **Aggressive defragmentation**: contiguity was worth ~1000× on a disk and is worth ~1.06× at 1 MiB on flash. On an SSD it also *costs* write-amplification and wear.
- **Elevator I/O scheduling**: there is no arm to optimise; Linux uses `none` on NVMe.
- **B-tree fan-out tuned for seeks**: enormous nodes were justified by seek cost, not by comparison cost.
- **Sort-merge over hash join**: the preference for sequential passes was a seek-avoidance argument.

**[2] One made more relevant:** **log-structured writing.** Originally a seek-avoidance technique, it is now the FTL's preferred pattern — sequential writes minimise garbage collection and write amplification. **The technique survived; its justification changed completely.**

### (e) [3]

Two of:

- The controller **coalesces and prefetches** sequential requests, so fewer, larger internal operations serve them.
- **Internal parallelism across flash channels** is easier to exploit for a predictable stream.
- Sequential access has better **FTL mapping locality** — fewer translation-table lookups in the controller's own DRAM.

---

## Q2 (16) — Flash

### (a) [4]

**Page:** 4–16 KiB; the unit of read and **program**.
**Erase block:** 128–256 pages, 1–4 MiB; the unit of **erase**.

**The rule: a page can only be programmed if it has been erased, and erase works only on a whole block.** So overwriting one page in place would require reading, erasing and rewriting the entire surrounding block.

### (b) [4]

The **Flash Translation Layer** maps logical block addresses to physical flash pages and **never overwrites in place** — a write goes to an already-erased page and the map is updated; the old page is marked invalid and reclaimed later.

**Without it there is no block device.** L22's "array of numbered blocks that can be written in any order" is exactly what flash cannot natively provide. **The abstraction is maintained in the controller's own DRAM**, and forty years of software depends on the fiction.

### (c) [4]

**Write amplification** = flash bytes actually written ÷ host bytes requested. It arises because garbage collection must relocate still-valid pages to free a block.

$$\frac{300 \text{ TBW}}{4} = \mathbf{75 \text{ TB of host writes}}$$

### (d) [4]

**Wear levelling** spreads erases across all blocks so that no block reaches its erase limit first, by remapping logical addresses to different physical blocks over time.

**Without it:** the block holding that metadata would take every erase. At ~1000 cycles for TLC and 1000 writes/second, **the block dies in about a second of accumulated erases** — in practice within hours to days once the write amplification of the surrounding block is counted. **The drive would fail with 99.99% of its flash unused.**

---

## Q3 (26) — Simulate the Schedulers

### (a) [12]

**8** for correct FCFS, SSTF, SCAN and LOOK; **4** for C-SCAN and a working direction argument.

> Watch for SCAN implemented without travelling to the disk end — **that is LOOK.** Both are wanted,
> and a submission with only one of them scores half.

### (b) [6]

Head 53, disk 0–199, queue 98, 183, 37, 122, 14, 124, 65, 67. *(All computed.)*

| Algorithm | Service order | Movement |
|---|---|---:|
| **FCFS** | 98, 183, 37, 122, 14, 124, 65, 67 | **640** |
| **SSTF** | 65, 67, 37, 14, 98, 122, 124, 183 | **236** |
| **SCAN down** | 37, 14, **0**, 65, 67, 98, 122, 124, 183 | **236** |
| **SCAN up** | 65, 67, 98, 122, 124, 183, **199**, 37, 14 | **331** |
| **LOOK down** | 37, 14, 65, 67, 98, 122, 124, 183 | **208** |
| **C-SCAN up** | 65, 67, 98, 122, 124, 183, **199 → 0**, 14, 37 | **382** |

### (c) [4]

**[2]** Going up first means travelling to 199 and back down for just two requests (37 and 14), which are behind the head. Going down first reaches them immediately and then sweeps up in one pass. **Direction costs 95 tracks — 40% — on this queue.**

**[2]** **A quoted SCAN figure without a direction is incomplete.** Textbooks routinely give "236" and omit that it is the downward sweep. **Always state the direction, and prefer LOOK, which is strictly better** (208) because it reverses at the last request rather than the physical end.

### (d) [4]

**[2] Starvation trace.** Head at 50; a request for track 190 arrives. Then, every millisecond, a new request arrives for a track within ±5 of the head.

SSTF always serves the nearest, so it services the stream around track 50 forever. **Track 190 is never reached** — its wait is unbounded, and no finite time guarantees service.

**[2] SCAN's bound.** The head sweeps monotonically to one end and back, so **every track is visited at least once per full sweep.** The worst-case wait is one complete traversal — bounded by the disk size and the service rate, and independent of what arrives afterwards.

> **The marked insight: SSTF's flaw is fairness, not efficiency.** It matched SCAN at 236 tracks on
> this queue. It is rejected for its unbounded tail, which is the same argument that appears in CPU
> scheduling and network queueing.

---

## Q4 (24) — Measure Your Storage

### (a) [4]

Expected: `nvme0n1 238.5G 0 disk SAMSUNG MZVLB256HAHQ-000H1`, **`ROTA 0` — flash.**

**Full marks require the student to state which kind of device the following figures describe.**

### (b) [6]

| block | seq MiB/s | rand MiB/s | rand IOPS | seq/rand |
|---:|---:|---:|---:|---:|
| 4 KiB | 113.2 | 49.8 | 12 746 | 2.27× |
| 16 KiB | 555.7 | 197.2 | 12 623 | 2.82× |
| 64 KiB | 882.0 | 224.6 | 3 594 | 3.93× |
| 256 KiB | 1736.3 | 906.2 | 3 625 | 1.92× |
| 1 MiB | 2005.9 | 1884.0 | 1 884 | 1.06× |

*(Verified.)*

### (c) [4]

**[2]** **Per-request overhead**, not the device. Each `pread` costs a system call, a block-layer traversal, an NVMe submission and a completion interrupt — a fixed cost per request regardless of size. At 4 KiB that fixed cost dwarfs the transfer; at 1 MiB it is amortised. **If the device were the limit the curve would be flat.**

**[2] Little's Law:** concurrency = throughput × latency. At 12 746 IOPS and 157 μs, concurrency ≈ 2. **A single-threaded benchmark holds concurrency near 1 and therefore measures latency**, while an NVMe drive with dozens of flash channels needs many outstanding requests to reveal its capability.

### (d) [5]

**398 063 IOPS at 2.51 μs** against **6 345 IOPS at 157.6 μs** — **63×**. *(Verified.)*

| Event | Time |
|---|---:|
| L1 hit | 1.2 ns |
| DRAM | 137 ns |
| Minor page fault | 1.9 μs |
| **Page-cache hit** | **2.5 μs** |
| **SSD 4 KiB read** | **~157 μs** |

**The cached read sits just above the minor page fault** — both are dominated by the system call and kernel path rather than by any device, which is exactly why they are the same order of magnitude.

### (e) [5]

**[2]** 6.0 μs/write without `fsync`; 3876 μs/write with. **~3870 μs per `fsync` — 645×.** *(Verified.)*

**[3]** At 10 000 transactions/second the budget is **100 μs per transaction**. One `fsync` costs **3900 μs** — **39× the entire budget**, so a maximum of **~256 transactions/second** could be sustained — 39× short of the requirement.

**The technique is group commit** *(also accept: write-ahead log with batched flush)*: many transactions are written into a log buffer and made durable by **one** `fsync`. Each transaction waits a few milliseconds for the batch, and throughput rises by the batch factor. **Latency is traded for throughput, deliberately.**

---

## Q5 (16) — Reading the Numbers

### (a) [4]

**[1]** $50\,000 \times 4\text{ KiB} = \mathbf{195\text{ MiB/s}}$.
**[1]** $500 \text{ MB/s} \div 1\text{ MiB} = \mathbf{\approx 477 \text{ IOPS}}$.
**[2]** **The key-value store wants the first** — point lookups are small and numerous, so IOPS is the binding metric. **The transcoder wants the second** — large sequential reads, so throughput binds.

### (b) [4]

**[2]** **Concurrency = throughput × latency.**
**[1]** $100\,000 \times 200\times10^{-6} = \mathbf{20}$ operations in flight.
**[1]** **One thread cannot reach it.** A single-threaded benchmark has concurrency ≈ 1 and will report ~5000 IOPS on a device capable of 100 000 — **measuring latency and calling it capability.**

### (c) [4]

**[2]** With 50 independent requests, the chance that **none** hits the p99 is $0.99^{50} \approx 0.605$, so **about 39% of page loads contain at least one 200 ms request** — and since the page waits for all of them, that request sets the page's latency.

**[2]** **The median describes a single request; the user experiences the maximum of fifty.** Quoting 5 ms implies a fast page when nearly two in five are dominated by a 200 ms outlier. **Tail latency is the user-visible number whenever a request fans out.**

### (d) [4]

**[1]** **`none` is right for NVMe:** there is no arm, so there is no head movement to optimise; the drive's controller has far better information about its own internal parallelism; and kernel reordering would add latency while destroying the sequentiality the FTL wants.

**[1]** **Wrong for a 7200 rpm disk**, where head position dominates cost and reordering is worth an order of magnitude — and where `mq-deadline` additionally prevents the starvation Q3(d) demonstrates.

**[2] What the literature is still good for:** rotating disks persist in bulk and archival storage; and **the reasoning transfers** — the fairness-against-efficiency trade of SCAN over SSTF reappears in CPU scheduling, network queue management and lock acquisition. **The algorithms were about a mechanical constraint; the argument was not.**

---

## Mark Summary

| | |
|---|---:|
| Q1 | 18 |
| Q2 | 16 |
| Q3 | 26 |
| Q4 | 24 |
| Q5 | 16 |
| **Total** | **100** |

**Where the class loses marks, in order:**

1. **Q3(c)** — not noticing that SCAN's cost depends on direction.
2. **Q4(c)** — attributing the 18× rise to the device rather than to per-request overhead.
3. **Q5(c)** — computing a mean instead of reasoning about the maximum of 50 draws.
4. **Q3(d)** — a starvation "proof" with all requests arriving at once, which cannot starve anything.
5. **Q1(d)** — listing designs without saying *why* the ratio change affects them.

---

*CS 201 · Week 7 · PS 7 Solutions · Instructor Only*

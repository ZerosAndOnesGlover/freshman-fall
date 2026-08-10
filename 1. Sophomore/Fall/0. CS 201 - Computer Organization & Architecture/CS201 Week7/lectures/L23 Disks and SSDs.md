# CS 201 · Computer Organization & Architecture
## Week 7 · Lecture 2 of 3
### Disks and SSDs — What Is Under the Abstraction

---

**Reading:** CS:APP §6.1.2–6.1.5 · **Previous:** L22, the I/O path

---

## 1. The Rotating Disk

A hard disk is the last mechanical component in a computer, and its performance model is mechanical.

```
        ┌─────────────┐
        │  ╭───────╮  │   platters spinning at 5400–15000 rpm
        │  │ ○ ═══─┼──┼── arm + head, moving radially
        │  ╰───────╯  │
        └─────────────┘
```

**Three costs per access:**

| | What | Typical |
|---|---|---|
| **Seek time** | Move the arm to the right track | 4–10 ms |
| **Rotational latency** | Wait for the sector to come round | half a revolution — **~4.2 ms at 7200 rpm** |
| **Transfer time** | Read the bytes | ~0.05 ms for 4 KiB |

*(Cited from manufacturer specifications. **The lab machine has no rotating disk**, so nothing in this section is measured here.)*

$$\text{rotational latency at 7200 rpm} = \frac{1}{2} \times \frac{60\text{ s}}{7200} = 4.17\text{ ms}$$

**Read the transfer column against the other two.** Of ~10 ms to read 4 KiB, **about 0.5% is spent transferring data.** The rest is waiting for machinery to move.

**Two consequences follow immediately, and they shaped fifty years of software:**

**Sequential access is orders of magnitude faster than random**, because consecutive sectors need no seek at all. A disk that manages ~100 random IOPS will stream at 150 MB/s.

**Bigger requests are nearly free.** Reading 1 MiB costs the same seek as reading 4 KiB, plus a little transfer time. **This is why filesystems use large blocks, why databases read ahead, and why B-trees have hundreds of children per node** — every one of those designs is amortising a seek.

---

## 2. The SSD

No moving parts, so no seek and no rotation — but flash has its own constraints, and they are stranger.

**Flash is organised in a hierarchy:**

| Unit | Size | Operations |
|---|---|---|
| **Page** | 4–16 KiB | read, **program** (write) |
| **Erase block** | 128–256 pages, i.e. 1–4 MiB | **erase** |

**The rule that changes everything: a page can only be programmed if it is erased, and erase works only on a whole block.**

So overwriting one 4 KiB page in place would mean: read the entire 2 MiB block, erase it, write it all back with one page changed. **Absurd**, and it is not what happens.

### The Flash Translation Layer

**The controller never overwrites in place.** It writes the new data to a *different*, already-erased page and updates an internal map from logical block address to physical page. The old page is marked invalid and reclaimed later by garbage collection.

**The FTL is why an SSD can present the block abstraction at all** — L22's "array of numbered blocks" is entirely a fiction maintained in the controller's own DRAM.

**Two consequences you can observe:**

**Wear levelling.** Flash cells survive a finite number of erases — roughly $10^3$ for modern TLC, $10^5$ for older SLC. The FTL spreads writes across all blocks so no block wears out first. **Without it, a filesystem that rewrites one metadata block constantly would destroy a drive in weeks.**

**Write amplification.** To free a block, the controller must relocate any still-valid pages in it. **Writing 4 KiB can cause far more than 4 KiB of internal flash writes** — a ratio of 2–10× on a full, fragmented drive. This is why SSDs slow down when nearly full, and why `TRIM` exists: it tells the drive which blocks the filesystem no longer needs, so garbage collection can skip relocating them.

---

## 3. Measured: This Machine's SSD

Random and sequential reads with `O_DIRECT`, so the page cache is bypassed and these are genuine device numbers:

| block | sequential MiB/s | random MiB/s | random IOPS | seq/rand |
|---:|---:|---:|---:|---:|
| **4 KiB** | **113.2** | **49.8** | 12 746 | **2.27×** |
| 16 KiB | 555.7 | 197.2 | 12 623 | 2.82× |
| 64 KiB | 882.0 | 224.6 | 3 594 | 3.93× |
| 256 KiB | 1736.3 | 906.2 | 3 625 | 1.92× |
| **1 MiB** | **2005.9** | **1884.0** | 1 884 | **1.06×** |

*(All measured, `O_DIRECT`, single thread, queue depth 1.)*

**Three things to read off this.**

**Sequential throughput rises 18× from 4 KiB to 1 MiB** — 113 to 2006 MiB/s. **The device is not the limit at small block sizes; per-request overhead is.** Each request costs a fixed amount of software and protocol work, and at 4 KiB that overhead dominates the transfer.

**At 1 MiB, random is only 1.06× worse than sequential.** With no seek to pay, a request large enough to amortise the fixed cost performs the same wherever it lands. **This is the fundamental difference from a rotating disk**, where the gap stays at two orders of magnitude however large the request.

**But at 4 KiB random is still 2.27× worse.** Not zero. Flash has no seek, yet locality still helps — the controller can coalesce and prefetch sequential requests, and its own internal parallelism across chips is easier to exploit.

> **Queue depth matters more than anything here.** These figures are one request at a time. An NVMe
> drive has dozens of independent flash channels and is designed for **many outstanding requests** —
> the same drive at queue depth 32 would deliver several times these IOPS. **A single-threaded
> benchmark measures latency, not the device's capability**, and that distinction is Week 11's
> business.

---

## 4. Disk Against SSD

| | HDD *(cited)* | SSD *(measured here)* |
|---|---|---|
| Random 4 KiB | ~100 IOPS | **12 746 IOPS** |
| Sequential | ~150 MB/s | **2006 MiB/s** |
| Latency | ~10 ms | ~80–160 μs |
| Random : sequential | ~1000× | **1.06–3.9×** |
| Cost per TB | low | higher |
| Wear-out | mechanical failure | **finite erase cycles** |

**The random-to-sequential ratio is the row that changed the world.** On a disk, random access was so catastrophic that thirty years of systems design — B-trees, log-structured filesystems, sort-merge joins, defragmentation — existed largely to avoid it.

**On flash the ratio is small enough that many of those designs are no longer obviously right**, and some are actively harmful. **Log-structured writing, however, turned out to be more relevant than ever** — not to avoid seeks, but because sequential writing is exactly what the FTL wants.

---

## 5. RAID, Briefly

Combining several devices, for capacity, speed or safety.

| Level | Layout | Buys | Costs |
|---|---|---|---|
| **0** | Striped | Throughput, capacity | **Any failure loses everything** |
| **1** | Mirrored | Survives one failure; fast reads | Half the capacity |
| **5** | Striped + distributed parity | Survives one failure, ~$(n-1)/n$ capacity | **Slow small writes** — read-modify-write of parity |
| **6** | Two parity blocks | Survives two failures | Slower still |
| **10** | Mirrored, then striped | Fast and redundant | Half the capacity |

**RAID 5's small-write penalty is the one worth understanding.** Changing 4 KiB means reading the old data and the old parity, computing the new parity, and writing both — **four I/Os for one logical write.**

> **RAID is not a backup.** It protects against a *device* failing. It does not protect against
> deletion, corruption, ransomware, or the building burning down — all of which it faithfully
> replicates to every member.

---

## 6. What to Take Away

1. **A disk access is seek + rotation + transfer**, and transfer is ~0.5% of it.
2. **Flash cannot overwrite in place** — program a page, erase a block.
3. **The FTL maintains the block-device fiction**, and gives you wear levelling and write amplification.
4. **Sequential rises 18× from 4 KiB to 1 MiB** — per-request overhead, not the device.
5. **At 1 MiB, random ≈ sequential (1.06×) on flash.** On a disk that gap never closes.
6. **Small random access is still 2.27× worse**, so locality has not stopped mattering.
7. **Queue depth is the missing variable** in any single-threaded storage benchmark.

---

## Exercises

1. Compute rotational latency for 5400, 7200 and 15 000 rpm. Why is the average half a revolution rather than a whole one?
2. A 7200 rpm disk with a 9 ms seek reads 4 KiB. What fraction of the time is spent transferring data? Now for 1 MiB.
3. An SSD has 4 KiB pages and 2 MiB erase blocks. Explain why overwriting one page in place is impractical, and what the FTL does instead.
4. Define write amplification. A drive reports a factor of 4. What does that mean for its rated lifetime in host writes?
5. §3 shows sequential throughput rising 18× from 4 KiB to 1 MiB. If the device were the bottleneck, what would the curve look like instead?
6. At 1 MiB, random is 1.06× sequential; at 4 KiB it is 2.27×. Give two reasons flash still prefers sequential despite having no seek.
7. A RAID 5 array does four I/Os per small write. Derive that, and say which workload it makes RAID 5 unsuitable for.

---

*Next: L24 — IOPS, latency, throughput, and how the kernel orders requests.*

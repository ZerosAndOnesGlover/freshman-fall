# CS 201 · Lab 7 — Solutions and TA Notes
## Instructor Only

---

> **Unmarked.** Five checkpoints. All SSD figures measured on the lab image;
> **HDD figures are cited, since there is no rotating disk in the building.**

---

## Before the Session

**Say the hardware limitation out loud in the first two minutes.** The curriculum's week covers disks and SSDs; the room has only flash. **That is not a gap to hide** — it is a chance to make the distinction between a measured number and a cited one, which this course has been building toward all term.

**Disk space:** each student creates a 512 MiB file. Thirty students is 15 GB. **Check the machines have room**, and have them delete it at the end.

---

## Timing

| Part | Budget | Reality |
|---|---|---|
| 1 — test file | 10 min | 15 min. `O_DIRECT` alignment trips people |
| 2 — seq vs random | 30 min | 30 min |
| 3 — page cache | 25 min | 20 min |
| 4 — `fsync` | 20 min | 15 min. **The most memorable number** |
| 5 — schedulers | 15 min | 20 min |

---

## Part 1

**`O_DIRECT` is where the time goes.** Three requirements, all mandatory:

| Must be 4096-aligned | Consequence if not |
|---|---|
| The buffer address | `EINVAL` |
| The file offset | `EINVAL` |
| The length | `EINVAL` |

**`malloc` will not do** — it aligns to 16. `aligned_alloc(4096, n)` or `posix_memalign` is required.

**`EINVAL` from `pread` is the symptom**, and students will read it as a bug in their loop. Tell them in advance.

> Some filesystems reject `O_DIRECT` entirely — tmpfs among them. **The scratch directory is on ext4
> here and works.** If a student is working in `/dev/shm` it will fail; move them.

**✅ CHECKPOINT 1**

---

## Part 2

| block | seq MiB/s | rand MiB/s | rand IOPS | seq/rand |
|---:|---:|---:|---:|---:|
| 4 KiB | 113.2 | 49.8 | 12 746 | 2.27× |
| 16 KiB | 555.7 | 197.2 | 12 623 | 2.82× |
| 64 KiB | 882.0 | 224.6 | 3 594 | 3.93× |
| 256 KiB | 1736.3 | 906.2 | 3 625 | 1.92× |
| 1 MiB | 2005.9 | 1884.0 | 1 884 | 1.06× |

*(Verified.)*

**Answers:**

1. **Per-request overhead**, not the device — syscall, block layer, NVMe submission, completion. **If the device were the limit the curve would be flat.**
2. **A 1 MiB request amortises the fixed positioning cost**, and flash has no seek to pay in the first place. **On a 7200 rpm disk the ratio stays around 1000×** regardless of request size, because the seek is per-request and mechanical.
3. Two of: the controller **coalesces and prefetches** sequential streams; **internal channel parallelism** is easier to exploit predictably; **FTL mapping locality** means fewer translation lookups.
4. $12\,746 \times 4\text{ KiB} = 49.8$ MiB/s ✓ and $1884 \times 1\text{ MiB} = 1884$ MiB/s ✓.

**✅ CHECKPOINT 2**

---

## Part 3

```
buffered, cached 4K random :   398063 IOPS     2.51 us/op   1554.9 MiB/s
O_DIRECT 4K random (device):     6345 IOPS   157.60 us/op     24.8 MiB/s
page cache is 63x faster
```

*(Verified.)*

### 3.1

The cached read at **2.5 μs sits just above Week 6's minor page fault at 1.9 μs** — and that is the right answer: **both are dominated by the system call and kernel path, not by any device.** Neither number is about hardware.

### 3.2 — the variance

**This lab has measured both 6 345 IOPS (157 μs) and 12 746 IOPS (78 μs) on the same drive**, and students will see similar spread.

**Causes worth accepting:**

- **Other activity on the device** — this is a shared, running desktop system, not a quiet benchmark rig.
- **The drive's own DRAM cache and read-ahead**, which the first run may have partially populated.
- **Thermal or power state** of the controller.
- **Where the file physically landed**, and how fragmented the FTL's mapping is.

**How to report honestly:** run many times, report **median and range** rather than a single figure, and state the conditions. **A single number from a shared machine is not a measurement.**

> This is the most transferable part of the lab and it is worth five minutes. Week 11 makes it a
> discipline; here it arrives naturally because the variance is impossible to ignore.

**✅ CHECKPOINT 3**

---

## Part 4 — the one they remember

```
200 x 4K write, no fsync   :  0.0012 s  (   6.0 us/write)
200 x 4K write + fsync each:  0.7753 s  (3876.3 us/write)
fsync costs about 3870 us per call
```

*(Verified.)* **645×. Write it on the board.**

**Answers:**

1. **In the page cache** — the Week 6 structure, as a dirty page. **Not on the device.**
2. **Nothing of that write.** The page cache is DRAM.
3. Budget at 10 000 tps is **100 μs/transaction**; one `fsync` costs **3900 μs**, i.e. **39× the entire budget**, capping the system at ~256 tps. **The technique is group commit**: many transactions share one `fsync`, trading a few milliseconds of latency for throughput.
4. **`fdatasync` skips the metadata flush** — it omits updating inode fields such as `mtime` when they are not needed for retrieval. **Safe when the file's size and block map are unchanged**, i.e. overwriting existing data rather than extending the file.

**✅ CHECKPOINT 4**

---

## Part 5

| Algorithm | Movement |
|---|---:|
| FCFS | 640 |
| SSTF | 236 |
| SCAN down | 236 |
| SCAN up | 331 |
| LOOK down | 208 |
| C-SCAN up | 382 |

*(All computed.)*

**Answers:**

1. FCFS: $45+85+146+85+108+110+59+2 = 640$. SSTF order 65, 67, 37, 14, 98, 122, 124, 183 → 236.
2. **A quoted SCAN figure without a direction is incomplete** — 95 tracks, 40%, separate the two here. Textbooks routinely give 236 and omit that it is the downward sweep.
3. **C-SCAN buys uniform waiting time.** Under SCAN a middle track is visited twice per cycle and an edge track once; C-SCAN refuses to serve on the return so every track waits the same. **It pays travel for fairness** — the same trade as SCAN over SSTF, one step further.
4. **`none` is right because there is no arm**, the drive knows its own parallelism better than the kernel, and reordering would add latency and break the sequentiality the FTL prefers. **Wrong on a disk**, where head position dominates and reordering is worth an order of magnitude.
5. **Starvation.** A far request plus a steady stream of near ones is never served — the wait is unbounded. **SCAN bounds it at one full sweep**, because the head visits every track once per traversal regardless of arrivals.

> **Point 5 is the one to land.** SSTF matched SCAN at 236 here — it is not rejected for being slow.
> The fairness-against-efficiency argument recurs in CPU scheduling and network queueing, and this is
> where students meet it first.

**✅ CHECKPOINT 5**

---

## What Success Looks Like

1. Use `O_DIRECT` correctly and say what it bypasses.
2. Explain why small-block throughput is limited by software, not the device.
3. **Say whether a storage number describes the device or the page cache.** They differ by 63×.
4. State what `fsync` costs and why databases batch.
5. **Report a number from a shared machine with its variance**, not as a single figure.

Items 3 and 5 are the ones Week 11 assumes.

---

*CS 201 · Week 7 · Lab 7 Solutions · Instructor Only*

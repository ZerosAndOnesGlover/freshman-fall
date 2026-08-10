# CS 201 · Week 7 · Lab 7
## Benchmarking Storage — Sequential, Random, and the Page Cache

---

**When:** **Tuesday of Week 8**, 15:00–16:50, BH 210 — *after* Week 7's three lectures
**Covers:** Week 7 · **Assessment:** unmarked, checked off by the TA
**You need:** `gcc`, `lsblk`, about 1 GB of free disk space.

---

## Before You Start: What Hardware You Have

```bash
lsblk -d -o NAME,SIZE,ROTA,TYPE,MODEL
cat /sys/block/nvme0n1/queue/scheduler        # or sda, whichever you have
```

On the lab machines:

```
nvme0n1 238.5G    0 disk SAMSUNG MZVLB256HAHQ-000H1
[none] mq-deadline
```

*(Verified.)* **`ROTA 0` means non-rotational — this is flash, and there is no spinning disk in the room.**

**So every HDD figure in this week's lectures is cited, not measured**, and this lab cannot reproduce them. **That is worth knowing rather than papering over**: you will measure what you have, and take the disk numbers on trust from manufacturer specifications.

**Note the scheduler is `none`.** Part 4 asks why.

---

## Part 1 — Build a Test File (10 min)

You need a file larger than RAM's willingness to cache it whole, and you must be able to bypass the cache on demand.

```c
#define _GNU_SOURCE
#include <fcntl.h>
/* create a 512 MiB file of known contents, once */
int fd = open(path, O_RDWR|O_CREAT, 0644);
char *buf = aligned_alloc(4096, 1<<20);
memset(buf, 0xAB, 1<<20);
for (long i = 0; i < 512L<<20; i += 1<<20) write(fd, buf, 1<<20);
fsync(fd);
```

**Then reopen it with `O_DIRECT`:**

```c
fd = open(path, O_RDONLY|O_DIRECT);
```

**`O_DIRECT` bypasses the page cache entirely** — reads go to the device. It has strict requirements: **the buffer, the offset and the length must all be 4096-aligned**, which is why `aligned_alloc` appears above. A misaligned `pread` returns `EINVAL`, not a wrong answer.

> Dropping caches with `echo 3 > /proc/sys/vm/drop_caches` needs root and you do not have it.
> **`O_DIRECT` is the unprivileged way to measure the device**, and it is more precise anyway.

**✅ CHECKPOINT 1** — your test file, and one successful `O_DIRECT` read.

---

## Part 2 — Sequential Against Random (30 min)

Read the file with `pread`, at block sizes from 4 KiB to 1 MiB, sequentially and at random 4 KiB-aligned offsets.

| block | sequential MiB/s | random MiB/s | random IOPS | seq/rand |
|---:|---:|---:|---:|---:|
| **4 KiB** | **113.2** | **49.8** | 12 746 | **2.27×** |
| 16 KiB | 555.7 | 197.2 | 12 623 | 2.82× |
| 64 KiB | 882.0 | 224.6 | 3 594 | 3.93× |
| 256 KiB | 1736.3 | 906.2 | 3 625 | 1.92× |
| **1 MiB** | **2005.9** | **1884.0** | 1 884 | **1.06×** |

*(Verified, `O_DIRECT`, single thread.)*

**Answer:**

1. **Sequential throughput rises 18×** from 4 KiB to 1 MiB. If the *device* were the limit, what shape would this curve have instead? What is the limit at 4 KiB?
2. At **1 MiB** random is only **1.06×** worse than sequential. Explain, and say what the same ratio would be on a 7200 rpm disk.
3. At **4 KiB** random is still **2.27×** worse. Flash has no seek — **give two reasons locality still helps.**
4. Compute throughput from IOPS × block size for two rows and check it against the measured column.

**✅ CHECKPOINT 2** — your table and the four answers.

---

## Part 3 — The Page Cache (25 min)

Now read the same file **without** `O_DIRECT`, over a 64 MiB region small enough to stay cached, having warmed it first.

```
buffered, cached 4K random :   398063 IOPS     2.51 us/op   1554.9 MiB/s
O_DIRECT 4K random (device):     6345 IOPS   157.60 us/op     24.8 MiB/s
page cache is 63x faster
```

*(Verified.)*

### 3.1 Place it on the ladder

Put your two latencies into the course's cost table alongside Week 4's L1 (1.2 ns) and DRAM (137 ns), and Week 6's minor page fault (1.9 μs).

**Which of those is the cached read closest to, and why does that make sense?**

### 3.2 The variance you will see

The `O_DIRECT` figure moves between runs — this lab has measured both **6 345 IOPS (157 μs)** and **12 746 IOPS (78 μs)** on the same drive.

**Give two plausible causes.** *(Consider what else is on the device, and what the drive itself caches.)*

**Then say what you would do to report an honest number**, given that variance.

**✅ CHECKPOINT 3** — both figures, your ladder placement, and your answer on variance.

---

## Part 4 — What Durability Costs (20 min)

```c
int fd = open("./synctest.tmp", O_WRONLY|O_CREAT|O_TRUNC, 0644);
for (int i = 0; i < 200; i++) write(fd, buf, 4096);                 /* no fsync */
for (int i = 0; i < 200; i++) { write(fd, buf, 4096); fsync(fd); }  /* fsync each */
```

```
200 x 4K write, no fsync   :  0.0012 s  (   6.0 us/write)
200 x 4K write + fsync each:  0.7753 s  (3876.3 us/write)
fsync costs about 3870 us per call
```

*(Verified.)*

**A 4 KiB write costs 6 μs. Making it durable costs 3.9 ms — 645× more.**

**Answer:**

1. When `write()` returns successfully, **where is the data?** Name the Week 6 structure it is sitting in.
2. The machine loses power one millisecond after `write()` returns. What survives?
3. A database promises durability and commits 10 000 transactions per second. **Show that one `fsync` per transaction is impossible**, then name the technique that makes the promise keepable anyway.
4. `fdatasync` is often faster than `fsync`. What does it skip, and when is that safe?

**✅ CHECKPOINT 4** — your timings and the four answers.

---

## Part 5 — Why the Scheduler Does Nothing (15 min)

```bash
cat /sys/block/nvme0n1/queue/scheduler
[none] mq-deadline
```

*(Verified.)*

**The kernel is not reordering your requests at all.**

Work the classic example by hand. Head at track 53; pending 98, 183, 37, 122, 14, 124, 65, 67; disk 0–199.

| Algorithm | Movement |
|---|---:|
| FCFS | **640** |
| SSTF | **236** |
| SCAN, down first | **236** |
| SCAN, up first | **331** |
| LOOK, down first | **208** |
| C-SCAN, up | **382** |

*(All computed — derive at least FCFS, SSTF and one SCAN yourself.)*

**Answer:**

1. Derive FCFS and SSTF, showing the service order.
2. **SCAN costs 236 downward and 331 upward on the identical queue.** What does that tell you about textbook figures quoted without a direction?
3. **C-SCAN is the most expensive here.** What does it buy, and why is that worth paying for?
4. **Why is `none` correct for this NVMe drive and wrong for a 7200 rpm disk?** Name the device property that decides it.
5. SSTF's flaw is not inefficiency. Name it, construct a request stream that triggers it, and say how SCAN bounds it.

**✅ CHECKPOINT 5** — your derivations and the five answers.

---

## Before You Leave

| Task | Command |
|---|---|
| Identify the device | `lsblk -d -o NAME,SIZE,ROTA,TYPE,MODEL` |
| Rotational? | `cat /sys/block/DEV/queue/rotational` |
| Scheduler | `cat /sys/block/DEV/queue/scheduler` |
| Bypass the page cache | `open(path, O_RDONLY\|O_DIRECT)` + `aligned_alloc(4096, …)` |
| Force durability | `fsync(fd)` / `fdatasync(fd)` |
| Quick throughput check | `dd if=file of=/dev/null bs=1M count=512 iflag=direct` |

**The habit:** before optimising anything that touches storage, find out **whether you are measuring the device or the page cache.** They differ by 63×, and a benchmark that does not say which it measured has not said anything.

---

*CS 201 · Week 7 · Lab 7*

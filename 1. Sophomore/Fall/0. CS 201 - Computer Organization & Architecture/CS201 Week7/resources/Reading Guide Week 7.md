# CS 201 · Week 7 · Reading Guide
## Storage and I/O

---

**Set reading:** CS:APP **§6.1.2–6.1.5** (disks and SSDs) and **§10.1–10.6** (Unix I/O).
**Also:** `man 2 open` (the `O_DIRECT` section), `man 2 fsync`.
**Optional but excellent:** the Linux kernel documentation on `blk-mq`, and OSTEP chapters 37–38.

---

## A Warning About the Book's Numbers

**CS:APP's storage chapter is the most dated part of the book.** Its disk figures are sound; its SSD figures are from an era when a good SSD did 30 000 IOPS and cost more per gigabyte than DRAM does now.

**Read §6.1.3 for the *model* and ignore the constants.** The seek-plus-rotation-plus-transfer decomposition is permanent; the milliseconds attached to it are not, and the SSD sections have moved further still.

**Measure your own machine.** Lab 7 does exactly that, and the gap between the book's numbers and yours is itself worth noticing.

---

## Section by Section

| § | Topic | What to take from it |
|---|---|---|
| **6.1.2** | Disk storage | Geometry: platters, tracks, sectors. The mechanical model |
| **6.1.3** | **Disk capacity and access time** | **The three-term cost model.** The one durable thing in the chapter |
| **6.1.4** | Logical disk blocks | The block abstraction, and how the controller maintains it |
| **6.1.5** | Solid state disks | Read for the *structure* — pages, blocks, the FTL. **The numbers are stale** |
| **6.1.6** | Storage technology trends | The widening CPU–storage gap. Still true, more so |
| **10.1–10.3** | Unix I/O, files, `read`/`write` | Mostly PROG 201's material; read for the interface |
| **10.4–10.5** | File metadata, sharing files | How descriptors, file descriptions and inodes relate |
| **10.6** | **I/O redirection** | Skim — but note it is the same indirection idea as Week 6 |

---

## Questions to Read Against

**On §6.1.2–6.1.4**

1. Give the three components of a disk access. For a 7200 rpm drive with a 9 ms seek, what fraction of a 4 KiB read is spent actually transferring data?
2. Why is average rotational latency **half** a revolution and not a whole one?
3. §6.1.4 says the controller presents a logical block array. **What is it hiding on a disk? What is it hiding on an SSD?** The two answers are very different.
4. Reading 1 MiB costs only ~1.5× what reading 4 KiB costs on a disk. **Derive that**, then list three system designs it explains.

**On §6.1.5 — read the structure, not the constants**

5. Explain why an SSD cannot overwrite a page in place. What are the two units involved and how do they differ in size?
6. What is the FTL for? **Why could the block abstraction of §6.1.4 not exist on flash without it?**
7. Define write amplification and wear levelling. How does each affect a drive's rated lifetime?
8. **The book's SSD figures are roughly an order of magnitude behind current hardware.** Look up the datasheet for the drive in your machine and compare.

**On the wider question**

9. On a disk, sequential beats random by ~1000×. On the lab's flash, by 1.06× at 1 MiB. **Name two system designs that were built for the first ratio.**
10. `write()` returns success. Where is your data? What guarantees do you actually have?
11. `cat /sys/block/*/queue/scheduler` on your machine. **If it says `none`, work out why that is the right answer.**

> **Question 9 is the one worth thinking hardest about.** A large part of the systems canon —
> B-trees, defragmentation, elevator scheduling, sort-merge joins — is an answer to a constraint that
> most machines no longer have. **Deciding which of those ideas survive on their own merits is a
> genuinely open question**, and it is the kind of judgement this course is for.

---

## Reading Against the Machine

```bash
# 1. What do you actually have?
lsblk -d -o NAME,SIZE,ROTA,TYPE,MODEL
cat /sys/block/nvme0n1/queue/{rotational,scheduler,nr_requests}

# 2. Sequential throughput, the crude way
dd if=bigfile of=/dev/null bs=1M count=512 iflag=direct

# 3. The measurement that matters — Lab 7 Part 4
#    Time 200 x 4 KiB writes, then the same with fsync after each.
#    PREDICT the ratio before you run it.
```

**Item 3's answer, verified: 6.0 μs against 3876 μs — 645×.** Almost nobody predicts within an order of magnitude, and it is the number that explains why every database is built the way it is.

---

## Terminology You Should Own by Week 8

| | | |
|---|---|---|
| seek time | rotational latency | transfer time |
| track / sector / platter | logical block addressing | block device |
| flash page | erase block | FTL |
| wear levelling | write amplification | TRIM |
| polling / interrupt / DMA | interrupt coalescing | scatter-gather |
| page cache | write-back | `fsync` / `fdatasync` |
| `O_DIRECT` | IOPS | throughput vs latency |
| queue depth | Little's Law | tail latency, p99 |
| FCFS / SSTF / SCAN | C-SCAN / LOOK | starvation |
| RAID 0/1/5/6/10 | write penalty | `blk-mq` |

---

## If You Want More

**OSTEP chapters 37–38** *(free at ostep.org)* cover disks and RAID far better than CS:APP, with the parity arithmetic worked properly. **Chapter 44 covers flash and the FTL** and is current in a way the textbook is not.

**Jim Gray's "The Five-Minute Rule"** (1987, revisited 1997 and 2007) asks when it is economic to cache a page in memory rather than re-read it from disk. **The arithmetic is trivial and the framing is superb** — it is the clearest example in the literature of a design decision derived from price and latency rather than taste.

**`fio`** is the standard storage benchmarking tool, and it exists because writing a *correct* storage benchmark is much harder than it looks — queue depth, alignment, cache bypass, file layout and warm-up all matter. **Lab 7 has you write a small one by hand precisely so that `fio`'s options make sense later.**

---

*CS 201 · Week 7 · Reading Guide*

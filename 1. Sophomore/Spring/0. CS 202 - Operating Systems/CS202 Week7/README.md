# CS 202 · Operating Systems
## Week 7: File Systems I — Design and Implementation

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 201, PROG 201
**Assessment for this course (overall):** Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%
**This week's deliverables:** PS 6 due **Friday**, PS 7 released **Wednesday**, **Project 1 assigned Wednesday** (15%, due **Friday of Week 11**), **Quiz 7** at the start of **Monday's** lecture (covers Week 6).
**Lab 6 — last week's OOM killer — is sat on the Tuesday of this week; Lab 7 covers this week and is sat on the Tuesday of Week 8.**

> ### **Spring Break follows this week.** Nothing moves for it, and two things are due after it.
> **PS 7 is released this Wednesday and due the Friday of Week 8** — the week you come back.
> **Midterm 2 is the Monday of Week 8**, covering **Weeks 4–7**, and **Lab 7 is the Tuesday after
> that.** Starting PS 7 before the break is the difference between a calm Week 8 and a bad one.

---

### Why This Week Exists

Because everything so far has been memory, and memory forgets.

**A file system is the answer to two questions**: where on a disk are this file's bytes, and how does a name find them? **xv6 answers both in 1,000 blocks** — a superblock, a log, an inode table, a bitmap, and data — and the answer fits in one lecture. **ext4 answers them for a terabyte**, and every difference between the two is a scaling problem you can name.

**Between the program and the disk sits the page cache**, which makes a repeated read 58 times faster, guesses what you will read next, and — the part that matters — **lets `write()` return long before anything reaches the disk.** That last is a bargain: 1,300 times faster, in exchange for losing your data if the power fails. `fsync` is where you decline the bargain.

**This week you also start Project 1**, which is xv6 kernel work: system calls, a scheduler you choose, and the locks both need.

---

### Learning Objectives

By the end of Week 7, you should be able to:

1. Say what an **inode**, a **directory entry** and a **data block** each hold, and how a path becomes bytes.
2. Read xv6's **disk layout** from its superblock, and compute where inode *i* and block *b*'s bitmap bit live.
3. Explain **direct and indirect block addresses**, and derive a file-size limit from them.
4. Explain **links**, `nlink`, and why a file can outlive every name it had.
5. Explain what the **page cache** holds, and measure a cold read against a warm one.
6. Explain **readahead**, and measure the window growing.
7. Explain **write-back**: what `Dirty` means, what triggers a flush, and what a crash costs.
8. **Measure the cost of durability**, and say what `fsync`, `fdatasync`, `O_SYNC` and `O_DIRECT` each do.
9. Write the **safe update** sequence, and say why the directory `fsync` is not optional.
10. Explain **extents, block groups and indexed directories**, and why each exists.
11. Explain **sparse files**, and why size and block count are independent.
12. Read a real file system's structures with **`debugfs`**, without root and without mounting.

---

### This Week's Materials

| File | Purpose |
|---|---|
| [[L22 Files Inodes and Directories]] | Names, inodes and blocks; **xv6's layout — 59 metadata blocks of 1,000**; direct and indirect addresses, and **a 71,680-byte limit measured in xv6**; allocators that zero what they hand out; directories as files; links; **six disk reads for one byte** |
| [[L23 The Page Cache Write-Back and fsync]] | **Cold 93.9 µs against warm 1.61 µs**; readahead growing 16 → 64 KiB; **64 MiB "written" in 15 ms** with `Dirty` to match; **durability at 1,300× per small write**; `O_DIRECT` is not durability; the write–`fsync`–`rename`–`fsync` idiom; xv6's 15 KiB write-through cache |
| [[L24 Real File Systems on Disk]] | Block groups, **one extent for a 600 KiB file**, 256-byte inodes, indexed directories, **a 10 MiB file occupying nothing**, allocation policy and delayed allocation — all read out of an ext4 image with `debugfs`, no root |
| [[CS202 Week7/assignments/QUIZ 7 Week 7 Monday\|QUIZ 7 Week 7 Monday]] | Ten minutes, covers **Week 6**, answer key printed |
| [[PS 7 myfs a File System on a Disk Image]] | Build the file system: allocators, `bmap`, read and write, directories, links, `fsck`. Due **Friday of Week 8** — **and PS 8 extends it** |
| `assignments/ps7/myfs.c` | The skeleton: eleven functions to write, the driver provided |
| [[PROJECT 1 xv6 Kernel Features]] | **Assigned this week, due Friday of Week 11, 15%.** System calls, a scheduler, and the locks they need |
| [[LAB 7 Watching the Page Cache]] | `mincore` and `posix_fadvise` instead of `bpftrace`; readahead; write-back watched in `/proc/meminfo`; the safe update timed. **Tuesday of Week 8** |
| `lab/pcache.c`, `lab/durable.c` | Residency, readahead and read costs; the six ways to write 4 KiB |
| [[CS202 Week7/resources/Reading Guide Week 7\|Reading Guide Week 7]] | OSTEP 39–41, xv6 book Ch. 6, and the `debugfs` manual |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A file system is three arrays and a cache in front of them.**

The arrays — inodes, a bitmap, data blocks — are simple enough to build in an afternoon, which is what PS 7 asks. **Everything hard comes from the cache**: it makes reads free and writes instant, and it does that by lying about when your data is on the disk. **`fsync` is the one call that makes it tell the truth**, and it costs a thousand times more than the write did.

**Week 8 asks the next question**: what the disk looks like when the power fails between two writes that had to happen together.

---

### Assessment Reminder

**PS 6 is due Friday at 17:00. PS 7 is released Wednesday and is due the Friday of Week 8.**

**Project 1 is assigned Wednesday: 15% of the course, due Friday of Week 11 at 17:00.**

**Labs and quizzes carry no weight** and are still required. **Quiz 7 is at the start of Monday's lecture and covers Week 6.**

> **Two labs touch this week.** **Lab 6** — out of memory — is sat on the **Tuesday of this week**.
> **Lab 7** covers this week and is sat on the **Tuesday of Week 8**, the day after Midterm 2.

Both are tracked in [[_CS 202 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 6's reclaim** is what evicts the page cache; a cold read here is that week's major fault. **Week 5's `mmap`** and this week's `read` reach the same pages. **Week 3's locks** protect the buffer cache and the inode table — and Project 1 needs them.

**Sideways:** **PROG 201**'s buffered `stdio` is a second cache above this one; `fflush` is not `fsync`, and Lab 7 Part D shows the difference.

**Forward:** **Week 8** makes these writes crash-safe with a log — and **PS 8 adds one to the file system you write this week.** **Week 9's device driver** is what the block layer talks to. **Week 11's replicated log** is Week 8's journal, on five machines.

---

*CS 202 · Week 7 · © CSE Department*

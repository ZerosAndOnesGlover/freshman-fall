# CS 202 · Operating Systems
## Week 7 · Lecture 2 of 3
### The Page Cache, Write-Back, and `fsync`

*“It is easier to change the specification to fit the program than vice versa.”* — Alan Perlis, "Epigrams on Programming" (1982), #57

---

**Sat:** Wednesday of Week 7, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 39 §39.14–§39.18; Love Ch. 16 · **Next:** L24, how real file systems lay out a disk

**Coursework:** 📋 **Project 1** released today, due Fri of Week 11 17:00 · 📝 **PS 7** released today, due Fri of Week 8 17:00 · 📝 **PS 6** due Fri this week 17:00 · 📊 **Quiz 8** Mon of Week 8 · 📘 **Midterm 2** Mon of Week 8 18:00–19:15 · 🔬 **Lab 7** Tue of Week 8 15:00–16:50

---

## 1. Every File Read Goes Through Memory

**A file's blocks live on disk, and their copies live in the page cache** — the same frames Week 6 was reclaiming. `read()` is a copy out of that cache, and only a page that is *not* there costs a disk read.

`pcache.c` measures it on a 512 MiB file. **`posix_fadvise(POSIX_FADV_DONTNEED)` drops a file's pages** — an ordinary user's version of `drop_caches`, which needs root — and **`mincore()` reports which pages of a mapping are resident**:

```
big.bin: 512 MiB
after POSIX_FADV_DONTNEED               0 of 131072 pages resident ( 0.0%)
one 1-byte read, cold                 335.5 us   Cached +0 kB
after that one read                     4 of 131072 pages resident ( 0.0%)   first run: 4 pages = 16 KiB
sequential read, cold                 0.339 s =   1583 MB/s
after reading it all               131072 of 131072 pages resident (100.0%)
sequential read, warm                 0.068 s =   7910 MB/s
random 4 KiB reads, cold              93.91 us each =    10649 reads/s
random 4 KiB reads, warm               1.61 us each =   620337 reads/s
```

- **A cold random read costs 93.9 µs; a warm one 1.61 µs — 58 times less.** The warm read is a copy from memory and a system call; **the cold one is Week 6's major fault, by another name.**
- **Reading the whole file warmed all 131,072 pages**, and the second pass ran at **7.9 GB/s** — five times the SSD's 1.6 GB/s, because nothing touched the SSD.
- **The page cache is not separate memory.** Those 512 MiB are on Week 6's file LRU lists, and are dropped the moment something needs frames.

---

## 2. Readahead

**The one-byte read brought in four pages.** Reading page by page, `mincore` shows the window growing:

```
readahead, page by page            4 12 12 12 12 16 16 16 16 16 16 16
```

**16 KiB for the first read, then 48 KiB, then 64 KiB.** The kernel starts small — a program that reads one byte may want no more — and **grows the window as a sequential pattern continues**, to a maximum:

```
$ cat /sys/block/nvme0n1/queue/read_ahead_kb
128
```

**Readahead is why the sequential cold read reached 1.6 GB/s** while a cold random read takes 94 µs each: the sequential reader is never waiting for one page, because the kernel has already asked for the next ones. **A program that reads randomly defeats it** — and `posix_fadvise(POSIX_FADV_RANDOM)` exists to say so, turning readahead off so the kernel stops fetching pages that will not be used.

---

## 3. Writes Do Not Go To the Disk

**`write()` copies into the page cache, marks the pages dirty, and returns.** `durable.c`:

```
64 MiB buffered write:  0.015 s =  4602 MB/s, then fsync  0.041 s   Dirty 2108 -> 67644 kB
```

**Sixty-four megabytes "written" in 15 ms — 4.6 GB/s, three times what the disk can do** — because none of it had reached the disk. `/proc/meminfo`'s **`Dirty` rose by exactly the 64 MiB** that was written, and the `fsync` that followed took **41 ms**: the real cost, paid later.

**Who writes dirty pages back, and when:**

| Trigger | Setting here |
|---|---|
| a page has been dirty too long | `dirty_expire_centisecs` **1500** — 15 s |
| dirty memory exceeds a share of available memory | `dirty_background_ratio` **10%** — background write-back starts |
| dirty memory exceeds a larger share | `dirty_ratio` **20%** — **the writing process is made to wait** and write back itself |
| the program asks | `fsync`, `fdatasync`, `sync` |

**This is write-back caching, and it buys two things**: writes return at memory speed, and **repeated writes to the same block coalesce** — a block written a hundred times in ten seconds reaches the disk once.

---

## 4. What It Costs to Be Sure

**The same 4 KiB write, six ways** (200–2,000 writes each, NVMe SSD):

| How | Per write | Writes per second |
|---|---:|---:|
| buffered, no sync | **2.9 µs** | 345,949 |
| `O_DIRECT`, no sync | 27.9 µs | 35,863 |
| `fsync` after each write | **3,967 µs** | 252 |
| `fdatasync` after each write | 3,983 µs | 251 |
| `O_SYNC` | 4,064 µs | 246 |
| `O_DIRECT` + `fdatasync` | 3,682 µs | 272 |

**Durability costs a factor of 1,300.** Three things to read out of this table:

- **`O_DIRECT` alone is not durability.** It bypasses the page cache — 27.9 µs, ten times a buffered write — but the **drive's own write cache** still holds the data. Only the flush that `fdatasync` issues makes it durable, and that costs the same 3.7 ms as everything else.
- **`fdatasync` was no faster than `fsync` here**, although it may skip the inode update, because **the flush of the drive's cache dominates** both.
- **A database's commit is this line.** One `fsync` per transaction is 252 transactions per second on this machine; **group commit** — batching many transactions into one flush — is how real systems get past it, and it is why they measure durability in flushes, not bytes.

---

## 5. The Hazard

**Between `write()` returning and the page reaching the disk, the data exists only in RAM.** A crash in that window loses it — and the window is up to 15 seconds wide by default.

**Worse, the order is not what you wrote.** The kernel may write back page 900 before page 3, and the file system may write the file's data before or after the metadata that points to it. **A crash can therefore leave a file that exists but whose contents are someone else's old blocks.** That is Week 8's subject.

**The idiom that survives it**, used by every editor and package manager:

```c
fd = open("f.tmp", O_WRONLY | O_CREAT | O_TRUNC, 0644);
write(fd, data, len);
fsync(fd);                     /* the data is durable, under a temporary name */
close(fd);
rename("f.tmp", "f");          /* atomic: readers see the old file or the new one */
dirfd = open(".", O_RDONLY);
fsync(dirfd);                  /* the rename itself is durable */
```

**Both `fsync`s are needed**, and the second is the one people forget: **a durable file with no durable name is still lost.**

---

## 6. What xv6 Has Instead

**xv6 has a buffer cache, not a page cache**: `NBUF` = 30 blocks of 512 bytes — **15 KiB for the whole system** (`param.h`). `bread` finds a block in it or reads it from disk; `bwrite` writes it **through** to disk immediately, inside the file system's log (Week 8).

| | xv6 | Linux |
|---|---|---|
| Cache | 30 buffers, 15 KiB, LRU | the page cache: every free frame |
| Read | `bread`, one block | page cache + readahead to 128 KiB |
| Write | **write-through**, in a log | **write-back**, up to 15 s later |
| Durability | every system call commits | only when you ask |
| Cost of a small write | a disk write, always | **2.9 µs — or 3,967 µs if you ask** |

**xv6 is slow and never loses your data; Linux is fast and will, unless you say otherwise.** The two designs answer the same question differently, and `fsync` is where the answer is chosen.

---

## 7. What to Take Away

1. **Every read is a page-cache lookup**; only a miss reaches the disk — **93.9 µs against 1.61 µs**, measured.
2. **Readahead grows with the pattern**: 16 KiB for the first read, to a 128 KiB maximum here, which is what makes sequential reads fast.
3. **`write()` returns when the data is in memory**: 64 MiB "written" in 15 ms, with `Dirty` rising by exactly 64 MiB, and the `fsync` costing 41 ms.
4. **Write-back is triggered by age (15 s), by the 10% background ratio, by the 20% hard ratio, or by you.**
5. **Durability costs about 1,300× per small write** — 2.9 µs to 3,967 µs — and **`O_DIRECT` is not durability**: the drive's cache must still be flushed.
6. **The safe update is write, `fsync`, `rename`, `fsync` the directory.**
7. **xv6 writes through a 15 KiB buffer cache**, and pays the disk on every system call.

---

## Exercises

1. `posix_fadvise(POSIX_FADV_DONTNEED)` dropped the file's pages. **Why can an ordinary user do that, when `/proc/sys/vm/drop_caches` needs root?**
2. From §1's numbers: a program reads a 512 MiB file twice. **How long does each pass take** if the machine has 8 GiB free, and if it has 200 MiB free?
3. A logging service appends 100-byte records, 10,000 per second. **What does it cost with an `fsync` per record, and what are two ways to make it affordable** without giving up durability entirely?
4. **Why is the `fsync` of the *directory* needed** in §5's idiom? Construct the loss that happens without it.
5. xv6's buffer cache holds 30 blocks. **What happens to a program that reads a 50-block file twice**, and how does it differ from Linux?

---

*CS 202 · Week 7 · L23 · © CSE Department*

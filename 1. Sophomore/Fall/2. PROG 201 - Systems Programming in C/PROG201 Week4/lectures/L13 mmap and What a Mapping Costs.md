# PROG 201 · Systems Programming in C
## Week 4 · Lecture 1 of 3
### `mmap`, and What a Mapping Costs

---

**Reading:** APUE §14.8 · TLPI Ch. 49 · `man 2 mmap`, `man 2 madvise`, `man 5 proc` (the `maps` and `smaps` sections) · **Previous:** L12 · **Next:** L14 — where memory comes from

---

## 1. You Have Been Using This All Term

Week 2 §5 of L08 used `mmap` to get a shared region and moved on. This week it is the subject, because it is not a niche call for IPC — **it is how every program you have ever run gets its memory.**

`/proc/self/maps` for `cat`, which does nothing interesting:

```
5a1308e4e000-5a1308e50000 r--p 00000000 103:02 3818582   /usr/bin/cat
5a1308e50000-5a1308e55000 r-xp 00002000 103:02 3818582   /usr/bin/cat
5a1308e55000-5a1308e57000 r--p 00007000 103:02 3818582   /usr/bin/cat
5a1308e58000-5a1308e59000 rw-p 00009000 103:02 3818582   /usr/bin/cat
5a132cfbc000-5a132cfdd000 rw-p 00000000 00:00 0          [heap]
75c5bb600000-75c5bb628000 r--p 00000000 103:02 3821305   /usr/lib/.../libc.so.6
75c5bb628000-75c5bb7b0000 r-xp 00028000 103:02 3821305   /usr/lib/.../libc.so.6
```

**Every one of those lines is an `mmap`.** The program's own text, its read-only data, its writable data, the C library, the heap — the kernel built all of them by mapping a file (or nothing) into the address space, and the loader you will study in Week 8 made most of the calls. Reading that file is the fastest way to understand what a process actually is.

The columns: address range, permissions (`r`/`w`/`x` and `p` for private or `s` for shared), the file offset, the device and inode, and the path. Four `libc.so.6` lines with different permissions is one file mapped four times, once per ELF segment — Week 8's subject.

---

## 2. The Call

```c
void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
int   munmap(void *addr, size_t length);
```

`addr` is a hint and should be `NULL`. `length` is rounded up to a page. `prot` is a bitwise-or of `PROT_READ`, `PROT_WRITE`, `PROT_EXEC` or `PROT_NONE`. The interesting argument is `flags`, and exactly one of the first two is required:

| Flag | Meaning |
| --- | --- |
| **`MAP_PRIVATE`** | Copy-on-write. Your stores are yours alone and never reach the file |
| **`MAP_SHARED`** | Your stores go to the file and to everyone else mapping it |
| `MAP_ANONYMOUS` | No file. Zero-filled pages; `fd` must be −1 |
| `MAP_FIXED` | Put it exactly at `addr`, **destroying whatever was there**. Almost never what you want |
| `MAP_POPULATE` | Fault it all in now rather than on demand |
| `MAP_NORESERVE` | Do not account it against commit limits (§5) |

The four combinations of the first three are the whole design space:

| | file-backed | anonymous |
| --- | --- | --- |
| **`MAP_PRIVATE`** | a program's text and data; reading a file without `read` | **`malloc`'s memory** |
| **`MAP_SHARED`** | a file two processes both edit | Week 2's shared region |

**`MAP_PRIVATE` on a file is the case people get wrong.** `sharedmap.c`:

```
1. store through MAP_SHARED, then read(): "written through a pointer"
2. store through MAP_PRIVATE, then read(): "written through a pointer"
```

The second store *happened* — read it back through `q` and it is there — but the file still holds what the first one wrote. A private mapping is copy-on-write against the page cache: your write faults a private copy into existence and the file never learns about it. **Use `MAP_PRIVATE` to read a file and `MAP_SHARED` to edit one**, and note that `MAP_PRIVATE` writes are a silent no-op as far as anyone else is concerned.

---

## 3. Address Space Is Free; Memory Is Not

This is the single most important idea in the week, and `rss.c` makes it unmissable. It maps **4 GiB** on a machine with 7 GiB of RAM and 2 GiB free, then reads a gigabyte, then writes it:

```
at startup                                 VmSize        2 MiB   VmRSS      1 MiB
after mmap of 4 GiB, untouched             VmSize     4098 MiB   VmRSS      1 MiB
after READING every page of the first GiB  VmSize     4098 MiB   VmRSS      1 MiB
after WRITING every page of the first GiB  VmSize     4098 MiB   VmRSS   1025 MiB
after madvise(MADV_DONTNEED) on that GiB   VmSize     4098 MiB   VmRSS      1 MiB
   ... and the first byte now reads 0
after munmap                               VmSize        2 MiB   VmRSS      1 MiB
```

Four things, and each one is a rule:

**The `mmap` itself cost nothing.** `VmSize` went up by 4 GiB and `VmRSS` did not move. The kernel wrote down a range and its permissions — a `vm_area_struct` — and allocated no memory and built no page tables. This is why a process can map more than the machine has.

**Reading a gigabyte cost nothing either.** `VmRSS` is still 1 MiB after touching 262,144 pages. Every one of them was resolved to the **shared zero page**, one physical page of zeroes that the whole system maps read-only wherever an untouched anonymous page is read. A hundred processes reading fresh `mmap` memory share exactly one page of it.

**Writing is what costs.** The first store to each page faults, the kernel allocates a real page, zeroes it, and fixes the page table. RSS goes to 1,025 MiB — one gigabyte plus the megabyte we started with, exactly. **This is copy-on-write from Week 0 L01, and it is the same mechanism `fork` uses.**

**`MADV_DONTNEED` gives it back, and throws the data away.** RSS returns to 1 MiB and the first byte reads 0 again. The mapping is still there; the *contents* are gone, and the next read gets the zero page. This is how a long-running server returns memory to the system without unmapping — and it is a data-destroying call that people reach for expecting `MADV_FREE`'s laziness, so read `man 2 madvise` before you use it.

> **`VmSize` is nearly meaningless as a measure of a program's memory use, and it is the number `ps` puts in the `VSZ` column.** `VmRSS` (`ps`'s `RSS`) is closer, and even that double-counts shared pages. `/proc/pid/smaps_rollup` has `Pss` — proportional set size, with shared pages divided among their users — which is the one to quote.

---

## 4. Demand Paging, and How Many Pages a Fault Brings

A fault is not free. `faultcost.c` touches 256 MiB of fresh anonymous memory:

```
anonymous first touch : 65540 faults in 0.123 s ->   1880 ns per minor fault
the same pages again  : 0 faults in 0.001 s ->     18.7 ns per store
```

**A minor fault costs about 1.9 µs and a store to a page you already have costs 19 ns** — a factor of a hundred. The fault is not just bookkeeping: the kernel has to find a free page, **zero it** (you must not be given another process's data), and install a PTE.

Now the same question for a file-backed mapping. `faultcount.c` maps a 16 MiB file — 4,096 pages — and reads every page:

```
4096 pages
  file-backed, read each page   :     31 faults  (132.1 pages per fault)
  anonymous,  write each page   :   4096 faults  (1.0 pages per fault)
  anonymous,  read each page    :   4096 faults  (1.0 pages per fault)
```

**Anonymous mappings fault one page at a time. File-backed mappings fault in batches** — 132 pages per fault here. The kernel knows the page cache already holds the neighbours, so on a fault it maps a run of surrounding PTEs at once ("fault-around", tunable at `/sys/kernel/debug/fault_around_bytes`), and larger still when the page cache is holding the file in huge pages. The exact ratio is a kernel tuning decision and will differ on your machine; **the shape — batched for files, one at a time for anonymous — is the part to remember.**

### Cold files, and why readahead decides everything

Evict the file from the page cache first (`posix_fadvise(POSIX_FADV_DONTNEED)`) and walk 256 MiB two ways:

```
cold file-backed      : 2051 minor + 1 major faults in 0.174 s
                        readahead turned 65536 would-be major faults into 2051 minor ones
cold, random order    : 3340 minor + 2800 major faults in 1.575 s
                        ->    563 us per major fault
```

**Same file, same number of bytes, 8.5× the time** — the only difference is the order. Walking forward, the kernel's readahead sees the pattern and pulls the file in ahead of you, so almost nothing becomes a *major* fault (one that waits for the disk). Jumping around defeats it, and every jump that misses the cache costs half a millisecond.

**A major fault is a disk read wearing a page fault's clothes**, and it is three hundred times a minor fault. `getrusage`'s `ru_majflt`, or `/proc/pid/stat`, is where you find out whether your program is having them.

---

## 5. `mmap` Against `read`

Both get a file's bytes into your program. `readvsmap.c` sums every 4,096th byte of a warm 512 MiB file:

| how | seconds |
| --- | --- |
| `read()`, 4 KiB at a time | 0.181 |
| `read()`, 1 MiB at a time | 0.057 |
| `mmap`, touched on demand | **0.007** |
| `mmap` with `MAP_POPULATE` | **0.001** |

**Twenty-five times faster than a well-buffered `read`**, for this access pattern. And the reason is not that `mmap` is clever — it is that `read` **copies**. `read` finds the page in the page cache and copies it into your buffer; `mmap` maps the page cache page into your address space and you read it in place. The copy that Week 2 L09 found was *not* the cost of IPC is very much the cost here, because there is no wakeup to dominate it.

Be careful about the size of that number, though: this workload touches one byte per page. Sum **every** byte and the memory bandwidth dominates and the gap narrows sharply. The honest statement is:

**`mmap` wins when you would have copied and then not used most of what you copied**, or when you want random access without seeking. **`read` wins when you are streaming a file end to end into a small buffer, when the file may be huge or growing, or when you cannot afford a `SIGBUS`** (L14 §7).

For writing, `sharedmap.c` writes and syncs 64 MiB:

```
pwrite, 4 KiB at a time + fsync   :  0.086 s  (747 MiB/s)
memset through MAP_SHARED + msync :  0.068 s  (948 MiB/s)
```

1.3×, and the same reason: 16,384 system calls and 16,384 copies against a `memset` and one `msync`.

---

## 6. Telling the Kernel What You Are About To Do

`madvise` is a hint you give about your own access pattern. Four that earn their keep:

| Advice | Effect |
| --- | --- |
| `MADV_SEQUENTIAL` | Read ahead aggressively; drop pages behind you |
| `MADV_RANDOM` | Do not read ahead — it would be wasted |
| `MADV_WILLNEED` | Start pulling these pages in now, asynchronously |
| **`MADV_DONTNEED`** | **Discard now. Anonymous pages lose their contents** (§3) |
| `MADV_FREE` | May discard *later*, if memory is short; contents may or may not survive |
| `MADV_HUGEPAGE` | Try to back this with 2 MiB pages (L15 §5) |

The one to be careful with is the pair `MADV_DONTNEED` and `MADV_FREE`: on Linux the first destroys anonymous data immediately and the second is lazy, and code that means one and writes the other is a bug that only appears under memory pressure.

`MADV_RANDOM` on §4's random walk is not a micro-optimisation — it stops the kernel reading 128 KiB around every access you will never use.

---

## Summary

- **Every region of a process is an `mmap`.** `/proc/pid/maps` is the list, and reading it is the fastest way to see what a process is.
- `MAP_PRIVATE` is copy-on-write and **your writes never reach the file**; `MAP_SHARED` is the file.
- **Address space is free.** 4 GiB mapped cost 1 MiB of RSS; reading a gigabyte of it cost nothing because untouched anonymous pages resolve to the **shared zero page**; writing it cost exactly a gigabyte.
- `MADV_DONTNEED` returns the memory **and destroys the data**.
- A **minor fault is ~1.9 µs**; a store to a resident page is ~19 ns; a **major fault is ~563 µs**.
- **File-backed mappings fault in batches** (132 pages per fault here); anonymous ones fault one page at a time.
- Readahead decides everything on a cold file: the same 256 MiB took **0.17 s sequentially and 1.58 s in random order**.
- `mmap` beat a 1 MiB-buffered `read` by **8×** for sparse access, because `read` copies. It is not a general rule — for streaming, `read` is right.
- `VmSize` is nearly meaningless; `VmRSS` is better; `Pss` in `smaps_rollup` is the honest one.

---

## Exercises

1. Read `/proc/self/maps` from inside your own program and print it. Identify the line your `main` is in, the line your stack is in, and the line a `malloc(10)` came from.
2. Map a file `MAP_PRIVATE`, write to it, and `msync`. What does `man 2 msync` say should happen, and what does happen?
3. Repeat §3's experiment but with `MADV_FREE` instead of `MADV_DONTNEED`. Does RSS drop? Does the data survive? Now run something memory-hungry and check again.
4. Map 1 GiB anonymously **without** `MAP_NORESERVE` on a machine with less than that free. Does it succeed? Read `man 5 proc` on `overcommit_memory` and explain.
5. Time §5's comparison summing *every* byte rather than every 4,096th. How much of the 25× survives, and what does that tell you about where the time actually went?
6. Use `MADV_SEQUENTIAL` and then `MADV_RANDOM` on §4's two walks — the right advice for each, then the wrong one. Which of the four combinations is worst, and by how much?
7. `/proc/self/smaps_rollup` has `Rss`, `Pss`, `Shared_Clean` and `Private_Dirty`. Fork ten children that all sleep, and explain the difference between the parent's `Rss` and its `Pss`.

---

*PROG 201 · Week 4 · L13 · © CSE Department*

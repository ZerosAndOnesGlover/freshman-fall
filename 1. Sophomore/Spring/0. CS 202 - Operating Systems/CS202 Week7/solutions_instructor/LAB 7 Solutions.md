# CS 202 · Lab 7 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Tuesday of Week 8, 15:00–16:50, BH 210. **Unmarked** — checked off in the session.

**This is the first session after Spring Break, and the day after Midterm 2.** Expect a tired room and a queue of PS 7 questions. **PS 7 is due that Friday**, and PS 8 extends it — **keep ten minutes at the end for PS 7 triage**, and note who does not have `myfs` working.

**What the session is actually for.** Students believe `write()` writes. **Part C is where that belief is measured and loses.** Everything before it is instrumentation: teach `mincore` and `posix_fadvise` properly in Part B and the rest goes quickly.

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–10 | A | The two refusals are instant; do not let anyone try `sudo` |
| 10–35 | B | `dd if=/dev/urandom` of 512 MiB takes ~20 s — start it first, read the program while it runs |
| 35–60 | C | **The fsync table is the lab.** Q7 needs the `O_DIRECT` explanation to be said out loud |
| 60–80 | D | Most students write the four steps but forget the directory `fsync` |
| 80–100 | Checkoff, PS 7 questions | |

---

## Answers

Reference machine: i5-8250U, ext4 on NVMe with `noatime`, kernel 7.0.0-31, 7.5 GiB RAM. `read_ahead_kb` 128; `dirty_ratio` 20; `dirty_background_ratio` 10; `dirty_expire_centisecs` 1500.

### Q1 — the tool you cannot use

```
ERROR: bpftrace currently only supports running as the root user.
bash: /proc/sys/vm/drop_caches: Permission denied
```

**`bpftrace` needs to load BPF programs into the kernel and read kernel memory** — `CAP_BPF` and `CAP_PERFMON`, or root. **On a shared machine that is a kernel-read primitive for every student**, and the image does not grant it. *(`kernel.perf_event_paranoid` is 4 here too, which blocks the `perf` route.)*

**What the ordinary account has instead:** `mincore()` says **which pages of a file this process has mapped are resident**, and `posix_fadvise(POSIX_FADV_DONTNEED)` **drops a file's clean pages from the cache**. **Both act on a file you can open** — which is the reason they are allowed: they affect only data you may already read, and dropping clean pages costs no one their data.

**What is lost:** tracing **the kernel's own paths** — which function faulted, how long `filemap_fault` took, which process caused someone else's eviction. **Accept** any answer naming a per-kernel-function measurement.

### Q2 — the first read

```
after POSIX_FADV_DONTNEED               0 of 131072 pages resident ( 0.0%)
one 1-byte read, cold                 335.5 us   Cached +0 kB
after that one read                     4 of 131072 pages resident ( 0.0%)   first run: 4 pages = 16 KiB
```

**Four pages — 16 KiB — for a one-byte read**, against `read_ahead_kb` **128**.

**Why not 128 KiB:** 128 is the **maximum** window, not the initial one. **The kernel has no evidence yet that this is a sequential read** — a program that reads one byte may want nothing more — so it starts small and grows only as the pattern continues (Q3). **Accept** "128 is a cap, and readahead ramps".

*(The cold one-byte read took 129.8 µs in one run and 335.5 µs in another; both are "one disk read plus the fault path". Do not mark a number, mark the count of pages.)*

### Q3 — the ramp

```
readahead, page by page            4 12 12 12 12 16 16 16 16 16 16 16
```

**Resident pages after reading page 0, then 1, then 2, …: 4, then 12, then 16.**

**Reading page 0 brings 4.** **Reading page 1 — still inside the window — triggers the *next* window**, taking the total to 12 (an 8-page, 32 KiB window queued ahead). Pages 2–4 are already resident, so nothing more is fetched; **reading page 5 triggers the next**, to 16. **The kernel is tracking how far ahead it has read and refilling when the reader reaches the marker**, doubling the window as the sequential run continues.

**"When does it decide this is sequential?"** — at the **second** read that follows the first (the jump from 4 to 12). **Accept** any answer that identifies the growth as evidence-driven and notes the window is refilled ahead of the reader, not at the miss.

### Q4 — the four costs

| Read | Cost | Limited by |
|---|---|---|
| sequential cold | 0.279–0.339 s for 512 MiB = **1,583–1,921 MB/s** | **the SSD**, with readahead keeping it busy |
| sequential warm | 0.059–0.068 s = **7,910–9,091 MB/s** | **the CPU**: `memcpy` out of the page cache plus one system call per MiB |
| random 4 KiB cold | **93.9 µs** each | **the SSD's latency**, one page at a time, readahead useless |
| random 4 KiB warm | **1.61 µs** each | neither — a system call and a 4 KiB copy |

**Ratios: warm/cold sequential ≈ 5×; warm/cold random ≈ 58×.** **[The 58 is the number to remember: it is L19's major fault, from the file side.]**

### Q5 — where the cached data went

Reading the whole file, twice measured:

```
read 512 MiB: Cached 2283160 -> 2771204 kB (+488044), MemFree -490276, Inactive(file) 1075888 -> 1599964
read 512 MiB: Cached 2247036 -> 2771260 kB (+524224), MemFree -523760, Inactive(file) 1075692 -> 1599852
```

**Yes — `Cached` rose by 488–524 MB, essentially the whole 512 MiB, and `MemFree` fell by the same amount.** The shortfall in the first run is other processes' activity during the read, not a cap.

**Where it sits: `Inactive(file)` rose by ~524 MB** — Week 6's **inactive file list**. **These 512 MiB are the first thing reclaim will take** (L19 §2: clean file pages are dropped, not written), which is why the file stays cached only until something else needs the frames. **Accept** any answer that places the pages on the file LRU and calls them evictable.

### Q6 — 64 MiB in 15 ms

```
64 MiB buffered write:  0.015 s =  4602 MB/s, then fsync  0.041 s   Dirty 2108 -> 67644 kB
```

**4.6 GB/s is three times this SSD's write speed**, so none of it reached the disk: `write()` **copied into the page cache and marked the pages dirty** — `Dirty` rose by **65,536 kB, exactly the 64 MiB**.

**Without the `fsync`, it would have been written back** when **the oldest dirty page passed `dirty_expire_centisecs` = 15 s** (the flusher thread wakes on `dirty_writeback_centisecs` and writes what has expired), or sooner if dirty memory had crossed **`dirty_background_ratio` = 10%** of available memory — 64 MiB is far below that here — or if the file had been closed by the last opener with `O_SYNC` set, which it was not. **Accept 15 s with the setting named.**

### Q7 — the cost of durability

| How | Per write | Ratio to buffered |
|---|---:|---:|
| buffered, no sync | **2.9 µs** | 1 |
| `O_DIRECT`, no sync | 27.9 µs | 10 |
| `fsync` each | **3,967 µs** | **1,368** |
| `fdatasync` each | 3,983 µs | 1,373 |
| `O_SYNC` | 4,064 µs | 1,401 |
| `O_DIRECT` + `fdatasync` | 3,682 µs | 1,270 |

**Durability costs about 1,300×. [2 of the 3 marks are for saying which two different things are being paid for.]**

- **`O_DIRECT` bypasses the page cache** — the write goes to the device, so it costs a real I/O submission (27.9 µs) instead of a `memcpy` (2.9 µs). **It does not make anything durable**: the drive acknowledges into **its own volatile write cache.**
- **`fsync` waits for the drive to flush that cache** (a FLUSH/FUA command) **and for the file system's metadata**. That wait is the 3.7–4.1 ms, and it is why every row with a flush costs the same regardless of how the data got there.
- **`fdatasync` was not faster than `fsync`** here although it may skip an inode update: **the flush dominates.**

### Q8 — write-back, watched

Over 40 seconds, with the file kept until the end:

```
Dirty:12540   Writeback:0  t=1s
Dirty:264460  Writeback:0  t=5s
Dirty:263724  Writeback:0  t=10s
Dirty:265596  Writeback:0  t=15s
Dirty:3512    Writeback:0  t=20s
Dirty:2280    Writeback:196 t=24s
Dirty:792     Writeback:0  t=40s
```

- **`Dirty` sat at its peak — 264 MB — from about t = 2 s to t = 15 s**, then collapsed. **That interval is `dirty_expire_centisecs` = 1500 = 15 s**: nothing forced a flush, so the pages waited out their expiry.
- **`Dirty` is data waiting to be written; `Writeback` is data being written right now.** A page moves from one to the other when the flusher submits it, and leaves both when the device completes it.
- **`Writeback` reads 0 almost always** because **264 MB is submitted and completed in well under a second** on this SSD — the sampler simply misses the burst. Catching 196 kB at t = 24 s is luck. **Accept** "the window is too short to sample at 1 Hz"; **a student who samples at 0.05 s and catches it deserves the compliment.**
- **Students who delete the file before the flush** see `Dirty` fall immediately and conclude write-back is instant. **That is the mistake the handout warns about** — deleting discards dirty pages. Ask them what `rm` does to data that was never written.

### Q9 — the safe update

Reference `safeupdate.c` (in this folder), 1 MiB payload, three runs each:

```
write  0.33 ms   fsync file 3.48 ms   rename 0.06 ms   fsync dir 3.30 ms   total  7.17 ms
write  0.63 ms   fsync file 5.71 ms   rename 0.22 ms   fsync dir 3.81 ms   total 10.37 ms
write  0.63 ms   fsync file 3.89 ms   rename 0.22 ms   fsync dir 3.27 ms   total  8.01 ms
              (no directory fsync):                                        total  4.81-5.28 ms
```

**The two flushes are the cost**: writing 1 MiB takes 0.3–0.6 ms, `rename` is 0.06–0.26 ms, and **each `fsync` is 3.3–5.7 ms.** **Dropping the directory `fsync` saves 3.3–3.8 ms — about 40% of the total**, so yes, the difference is easily measurable.

**Why it is nevertheless required:** `rename` is a **metadata** change to the directory. After the file's own `fsync`, the data is durable under the name `data.tmp`. **If the machine loses power after the `rename` returns but before the directory's block reaches the disk, the disk still shows the old directory** — the new file exists, full and correct, **under a name nothing refers to**, and the target either still has its old contents or, if the old inode was freed, is gone. **A durable file with no durable name is lost.**

### Q10 — why `rename`, not `O_TRUNC`

**What a reader sees [2]:** with `O_TRUNC` + rewrite, **a concurrent reader can open the file mid-update** and read a truncated or half-written version — there is no instant at which the file is not the old one or the new one. With `rename`, the directory entry changes atomically: **every `open` gets one complete version.**

**What a crash causes [2]:** `O_TRUNC` **destroys the old contents before the new ones are durable.** A crash between the truncate and the flush leaves **a zero-length file — both versions gone.** This is the classic "config file is empty after a power cut", and it is why the rename idiom exists.

**Bonus, if a student raises it:** ext4's `auto_da_alloc` hides much of this by flushing data before a rename that replaces a file — **but it is a mitigation of a bug, not a guarantee**, and it does not apply to other file systems.

---

## Common Problems

| Symptom | Cause | Fix |
|---|---|---|
| `mincore` reports everything resident on a fresh file | the file was just written by `dd` — its pages are in the cache | `posix_fadvise(DONTNEED)` first, as `pcache` does |
| `POSIX_FADV_DONTNEED` drops nothing | the pages are **dirty** | `sync()` first; `pcache` does both |
| Cold and warm reads are the same speed | the file is smaller than free memory and stayed cached | 512 MiB minimum; check `Cached` |
| `O_DIRECT` open fails with `EINVAL` | unaligned buffer | `posix_memalign` to 4096 — `durable.c` shows it |
| Durability numbers are ~100 µs, not ~4 ms | the machine has a drive that ignores flushes, or the file is on tmpfs | check the filesystem: the lab must run on the real disk |

---

*CS 202 · Week 7 · Lab 7 Solutions · Instructor Only*

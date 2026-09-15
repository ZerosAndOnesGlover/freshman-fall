# CS 202 · Lab 5 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Tuesday of Week 6, 15:00–16:50, BH 210. **Unmarked** — checked off in the session.

**What the session is actually for.** Students have drawn page tables and read about copy-on-write. **They have never watched a flag change because of something they did.** Every `pmlab` line is a small experiment with a visible outcome; **the lab works if students predict each line before running it.** Insist on the prediction for Q6 and Q7 at least.

**The hidden frame numbers will disappoint some students** who read a tutorial that prints physical addresses. Part A makes the refusal the lesson; do not offer workarounds.

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–5 | Setup | Check that `man 5 proc_pid_pagemap` opens — it is the reference for the whole lab |
| 5–30 | A | Q1 needs `/proc/self/maps`' permission column beside `pmwalk`'s counts; show how to line them up |
| 30–45 | B | **Q4's "why is the read not exclusive"** is the zero page; let students find it |
| 45–65 | C | **Q8 is the best moment in the lab**: deleting one line adds a fault that has nothing to do with the four pages |
| 65–80 | D | Students assume the CPU tells the kernel about writes. Ask how |
| 80–95 | E | The swap offsets are zero too; the major-fault count is 0. Both surprise |
| 95–110 | F, checkoff | |

---

## Answers

All reference output from the reference machine: i5-8250U, Ubuntu 24.04.4, kernel **7.0.0-31**, 4 GiB swap file, transparent huge pages `madvise`.

### Q1 — libc's mappings

`pmwalk` on itself:

```
start           pages  present  swapped  exclusv  nonzero  mapping
73a42c400000       40       39        0        0        0  libc.so.6
73a42c428000      393      252        0        0        0  libc.so.6
73a42c5b1000       79       46        0        0        0  libc.so.6
73a42c600000        4        4        0        4        0  libc.so.6
73a42c604000        2        2        0        2        0  libc.so.6
```

- **The 393-page mapping is libc's code** — the `r-xp` line in `/proc/self/maps`, and by far the largest.
- **Not all of it is present** because code is paged in **on demand from the page cache**, like any file: a page appears in this process's table only when this process first executes something on it. `pmwalk` uses a few libc functions; **252 pages had been touched** — by the dynamic loader, `printf`, `fopen` and friends. *(Accept any number; a `sleep` showed 234.)*
- **None is exclusive** because **every process using libc maps the same frames** — the page cache's copy of the file. *(`present` here depends on whether the frame is in this process's table, not just in the page cache.)*
- **The last two are entirely exclusive** because they are libc's **writable data** — relocated GOT, `.data`, `.bss` — mapped `MAP_PRIVATE`. The loader **wrote** to every page of them at start-up, and a write to a private file page **gives the process its own copy**: copy-on-write, from a file rather than from `fork`. The 4-page one is `r--p` now — it is RELRO, made read-only **after** relocation wrote to it.

### Q2 — frame numbers

```
present pages with a nonzero frame number: 0
```

**Linux zeroes the frame number for any reader without `CAP_SYS_ADMIN`**, since 2015 — after **Rowhammer** showed that knowing which physical frames hold your own data lets you aim bit flips at neighbouring frames, including page tables. **A root process or one granted `CAP_SYS_ADMIN` sees them.** *(The manual page on the lab image does not mention this; L18 §7 does.)*

### Q3 — other processes

| Target | Result |
|---|---|
| `sleep`, started by this shell | readable |
| **`pipewire`, same user, not started by this shell** | **readable** |
| `init`, pid 1 | **`/proc/1/pagemap: Permission denied`** |

**`pagemap` needs a `PTRACE_MODE_READ` access check** (the manual says so). **Yama's `ptrace_scope` 1 restricts only *attaching*** — `PTRACE_MODE_ATTACH` — to descendants, so `gdb -p` was refused in Lab 4 while reading `/proc/<pid>/pagemap` of any process **of the same user** is allowed. **pid 1 belongs to root**, and the ordinary credential check refuses it.

### Q4 — `pmlab demand`

```
       mapped, nothing touched             -.d  -.d  -.d  -.d   faults 0
       read page 0                         P.d  -.d  -.d  -.d   faults 1
       wrote page 0                        Pxd  -.d  -.d  -.d   faults 1
       wrote page 1 (never read)           Pxd  Pxd  -.d  -.d   faults 1
```

- **Nothing touched**: no entries at all. Soft-dirty is set on the not-present entries because the region is new — **accept "new mappings start soft-dirty"**; the bit matters only after `clear_refs` (Part D).
- **Read page 0**: one fault; **present but not exclusive** — mapped to **the shared zero page**, a single read-only frame of zeros used by every process for reads of untouched anonymous memory.
- **Wrote page 0**: **a second fault**, because the zero page is mapped read-only. The kernel allocates a real frame, zeroes it, and maps it writable: now **exclusive**.
- **Wrote page 1**: **one fault** — a write fault on a not-present page goes straight to a new zeroed frame. **Read-then-write costs two faults; write alone costs one.**

### Q5 — `calloc` 100 MiB, read, then write

Measured with a short program:

```
calloc: 11 faults, RSS +88 kB
read all (sum 0): 25600 faults, RSS +0 kB
write all: 25600 faults, RSS +102400 kB
```

**25,600 faults for the read and no frames used** — every page maps the zero page; **25,600 more for the writes, and 100 MiB of frames.** `calloc` of 100 MiB uses `mmap`, whose memory is already zero, so `calloc` does not write it. **Accept** 25,600 and 25,600 with that reasoning; the 11 faults are `malloc`'s own bookkeeping.

### Q6 — `pmlab cow`, the child

```
parent wrote all four                      Pxd  Pxd  Pxd  Pxd   faults 4
child  after fork                          P.d  P.d  P.d  P.d   faults 0
child  read page 0                         P.d  P.d  P.d  P.d   faults 0
child  wrote page 1                        P.d  Pxd  P.d  P.d   faults 1
```

**`fork` copied the page table**, so every page is present in the child, **but each frame is now mapped by two processes** — neither is exclusive — and **both copies of each entry are read-only**. **A read needs no fault**; **a write to page 1 faults**, and the kernel copies that one page, giving the child an exclusive frame.

### Q7 — the parent after the child exits

```
parent child has exited; read page 1       Pxd  Pxd  Pxd  Pxd   faults 0
parent wrote page 1                        Pxd  Pxd  Pxd  Pxd   faults 1          (with the added step)
parent's page 1 still holds 7
```

- **Exclusive again, with no fault**: `exclusive` is computed from how many processes map the frame, and the child's mappings went away when it exited. **The parent's entries were not changed.**
- **The write does fault — one fault**, because the parent's entry is **still read-only** from the fork. **The kernel sees that only one process maps the frame and simply makes the entry writable again**, without copying. **Accept** "1 fault, no copy" with that reasoning; the key point is that *exclusive* describes the frame's sharing, not the entry's permission.

### Q8 — deleting `sink = 0`

Three runs, all:

```
parent child has exited; read page 1       Pxd  Pxd  Pxd  Pxd   faults 1
```

**The read "took" a fault — but not on page 1.** `sink` is a global in the program's `.bss`, which the parent had written before `fork`; **`fork` made that page copy-on-write in the parent too**, so the parent's first write to `sink` after the fork faulted. **Every writable private page was write-protected, not just the four the program watches** — stack, heap, `stdout`'s buffer. The `sink = 0` line takes that fault outside the measurement.

### Q9 — `pmlab dirty`

```
       wrote all four                      Pxd  Pxd  Pxd  Pxd   faults 4
       wrote 4 to /proc/self/clear_refs    Px.  Px.  Px.  Px.   faults 0
       read page 0                         Px.  Px.  Px.  Px.   faults 0
       wrote page 2                        Px.  Px.  Pxd  Px.   faults 1
       wrote page 2 again                  Px.  Px.  Pxd  Px.   faults 0
```

**`clear_refs` cleared soft-dirty on every page and write-protected every entry.** **The CPU sets its own dirty bit silently** and the kernel uses that bit for its own purposes (writeback, Week 6), so **the only way to be told about the next write is to make it fault.** The write to page 2 faulted, the kernel set soft-dirty and made the entry writable again, and **the second write went through without a fault.** The read of page 0 did not need write access.

*(Like Q8: `clear_refs` write-protected **every** page of the process, including `sink`'s and the stack's. The program takes those faults before printing. Students who read the comment should say so.)*

### Q10 — a checkpointing tool

1. **Save everything** once; **write `4` to `/proc/<pid>/clear_refs`**.
2. Let the process run.
3. **Read `pagemap`; save only pages with bit 55 set**; clear again; repeat.

**Each round saves only what changed**, while the process keeps running, and the final round — with the process stopped — is small. **This is CRIU's incremental dump, and the same idea underlies live migration** of containers and virtual machines (Week 10). **Accept** any scheme that clears, waits, and reads bit 55.

### Q11 — `pmlab pageout`

```
       wrote 'a' 'b' 'c' 'd' into the four  Pxd  Pxd  Pxd  Pxd   faults 0
       MADV_PAGEOUT on pages 0 and 1       S.d  S.d  Pxd  Pxd [page 0 swap type 0 offset 0] [page 1 swap type 0 offset 0]   faults 0
       read page 0 back                    Pxd  S.d  Pxd  Pxd [page 1 swap type 0 offset 0]   faults 1
page 0 holds 'a'
```

**Pages 0 and 1 became swapped**: not present, **not exclusive**, soft-dirty kept. **The swap type and offset read as zero**, for the same reason as the frame numbers (Q2): **where a page lives on the swap device is hidden from unprivileged readers too.** Consistent with Part A.

### Q12 — major or minor?

With majors counted as 1,000: **`faults 1`**, three runs in three. **A minor fault.** **The page's content was still in the swap cache**: `MADV_PAGEOUT` wrote it to swap and removed it from the page table, but **the frame had not yet been reused**, so the fault found it in memory and simply mapped it again. **A major fault happens only when the frame has been freed and given away** — under real memory pressure, which is Week 6.

### Q13 — the tables' share

Reference machine, during the build:

| Process | `VmPTE` | `VmRSS` | Tables as a share |
|---|---:|---:|---:|
| chrome | 3,224 kB | 293,948 kB | 1.1% |
| chrome | 2,928 kB | 505,468 kB | 0.6% |
| chrome | 2,244 kB | 383,644 kB | 0.6% |
| obsidian | 2,168 kB | 410,312 kB | 0.5% |
| gnome-shell | 1,876 kB | 351,164 kB | 0.5% |
| *this shell* | 60 kB | 3,984 kB | 1.5% |

**For dense memory, L16 §7 predicts about 0.2%** — 2 MiB of tables per gigabyte. **Every process here is above it**, because their memory is **not** dense: shared libraries, many small mappings, guard regions, and — for browsers — reserved address space with scattered pages. **A small process is far above** because its fixed tables dominate. **Accept** any list and a comparison with 0.2%.

---

## Common Problems

| Symptom | Cause | Fix |
|---|---|---|
| All columns zero in `pmwalk` for another process | the PID has exited, or is another user's | check `ps -p PID` |
| `pread: Invalid argument` | reading `[vsyscall]`, which has no `pagemap` entry | `pmwalk` skips it; students' own code must too |
| Q7's added write shows `faults 0` | added *before* the `sink = 0` line, so the parent's pages were written first | move it after the read |
| `pageout` shows no `S` | swap is off, or the pages were huge | `swapon --show`; `pmlab` calls `MADV_NOHUGEPAGE` |
| Q12 shows 1,001 | a genuine major fault: the machine was under memory pressure | accept it, and ask what changed |

---

*CS 202 · Week 5 · Lab 5 Solutions · Instructor Only*

# CS 201 · Computer Organization & Architecture
## Week 6 · Lecture 3 of 3
### Demand Paging, Copy-on-Write, and Replacement

*“Once you understand how to write a program get someone else to write it.”* — Alan Perlis, "Epigrams on Programming" (1982), #27

---

**Reading:** CS:APP §9.5, §9.7–9.8 · **Previous:** L20, the TLB

**Coursework:** 📝 **PS 5** due today 17:00 · 📊 **Quiz 7** Mon of Week 7 · 🔬 **Lab 6** Tue of Week 7 15:00–16:50 · 📝 **PS 7** released Wed of Week 7, due Fri of Week 8 17:00

---

## 1. Allocation Is a Promise, Not a Delivery

When the present bit in a PTE is 0, the hardware raises a **page fault**. The OS then decides what that meant — and "nothing is there yet" is the ordinary case, not an error.

```
start                              RSS=  1444 KiB  minor faults=74
after malloc(512 MiB)              RSS=  1580 KiB  minor faults=86
after touching every page          RSS=525864 KiB  minor faults=131157
```

*(Measured.)*

**`malloc(512 MiB)` increased resident memory by 136 KiB.** The allocation succeeded, the pointer is valid, and **essentially no physical memory was committed.** The kernel recorded a promise in the process's mapping list and stopped.

**Then the second line.** Touching one byte per page brought RSS to ~513 MiB and generated **131 071 minor faults**, against

$$512 \text{ MiB} / 4096 = \mathbf{131\,072 \text{ pages}}$$

**One fault per page, exact to within one.** Every page arrived individually, on first touch, because someone asked for it.

> **This is why "how much memory does my program use" is an ambiguous question.** *Virtual* size is
> what was promised. *Resident* size is what was delivered. `top` shows both, and they can differ by
> orders of magnitude.

---

## 2. Two Kinds of Fault

| | Cause | Cost |
|---|---|---|
| **Minor** | The page needs a frame, but no disk I/O — a fresh anonymous page, a page already in the page cache, or a COW copy | microseconds |
| **Major** | The data must be read from disk — swap, or a file page not yet cached | milliseconds |

**A minor fault is a few thousand cycles. A major fault is a few million.** Confusing them is how people conclude that "page faults are fine" or "page faults are catastrophic" — both are true, of different faults.

### What a minor fault actually costs

Touch every page of a 512 MiB mapping, then touch them all again:

```
first touch  (page fault each): 0.2578 s over 131072 pages = 1967 ns/page
second touch (already mapped) : 0.0025 s over 131072 pages =   19 ns/page
=> a minor page fault costs about 1948 ns (~6232 cycles at 3.2 GHz)
```

*(Measured; a second run gave 1887 ns / ~6038 cycles.)*

**About 1.9 μs — roughly 6000 cycles — for a fault that touches no disk at all.** Compare with Week 4's ladder: an L1 hit is 4 cycles and a DRAM access is 438. **A minor page fault costs about fourteen DRAM accesses**, and it is pure software: trap into the kernel, find the mapping, allocate a frame, zero it, install the PTE, return.

**The zeroing is not optional.** A fresh anonymous page must be zeroed before the process sees it, or it would leak whatever the previous owner left there. **Isolation has a price and this is where some of it is paid.**

---

## 3. Copy-on-Write

`fork()` must give the child a copy of the parent's entire address space. **Doing that literally would make `fork` unusable** — and the child usually calls `exec` immediately and discards all of it.

**So the copy is deferred.** Both processes' page tables point at the *same* frames, and every writable page is marked **read-only** in both. On the first write, the hardware faults; the kernel copies that one page, marks both copies writable, and returns.

```
parent before fork:   RSS=263596 KiB
fork() itself took    0.0043 s for a 256 MiB address space
child at birth:       RSS=263068 KiB   minor faults=14
child after writing:  RSS=263260 KiB   minor faults=65566 (+65536)
256 MiB / 4096 = 65536 pages
```

*(Measured.)*

**Read it in three steps.**

**`fork()` of a fully resident 256 MiB process took 4.3 ms** — and that is mostly page-table setup, not data copying. Copying 256 MiB would take far longer.

**The child was born having taken 14 faults.** It "has" 256 MiB. Nothing was copied.

**Writing one byte to every page cost exactly 65 536 additional minor faults** — and $256 \text{ MiB} / 4096 = 65\,536$. **One COW fault per page, to the page.**

> **Copy-on-write is why the Unix process model is affordable**, and it is a pure consequence of
> having an indirection layer with a permission bit per page. **The read-only marking is the whole
> mechanism** — the fault handler distinguishes "you may not write this" from "you may, but I must
> copy it first" by consulting the mapping, not the hardware.

---

## 4. Memory-Mapped Files

`mmap` makes a file's contents *be* a region of your address space. Reads fault pages in from the file; writes mark them dirty and are written back.

| | `read()`/`write()` | `mmap` |
|---|---|---|
| Copies | kernel page cache → your buffer | **none** — you address the page cache directly |
| Syscalls | one per call | one, at setup |
| Access | sequential-friendly | **random-access-friendly** |
| Cost model | explicit | **implicit — a load can now take milliseconds** |

**The last row is the trade.** With `mmap`, an ordinary `mov` may trigger a major fault and block for a disk read. **The code gives no indication that this is possible**, which is convenient until you are trying to reason about latency.

**This is also how executables are loaded.** Nobody reads your binary into memory — it is mapped, and pages arrive as execution reaches them. The `r-xp … /usr/lib/…/libc.so.6` lines in L19 §6 are exactly this, and it is why the same physical libc pages are shared by every process on the machine.

---

## 5. Replacement

When physical memory is exhausted, something must be evicted. **The optimal policy — evict the page that will be used furthest in the future — requires knowing the future**, so it exists only as a benchmark.

| Policy | Behaviour | Problem |
|---|---|---|
| **FIFO** | Evict the oldest | Ignores usage. Suffers **Belady's anomaly**: more frames can mean *more* faults |
| **LRU** | Evict least recently used | Good, but exact LRU needs a timestamp per access — **far too expensive in hardware** |
| **Clock** *(second-chance)* | Sweep a circular list; if the **A** bit is set, clear it and move on; if clear, evict | An LRU approximation using **one bit** — the A bit from L19 §5 |

**Clock is what real kernels use**, in elaborated forms. **It exists because of exactly which information the hardware provides**: the PTE has an accessed bit and nothing finer, so the algorithm is built around a single bit per page.

### Thrashing

If the combined working set exceeds physical memory, the system spends its time evicting pages that are about to be needed again. **Faults become major, each costing milliseconds, and throughput collapses.** The classic symptom is a machine that is 100% busy and making no progress.

**Linux's last resort is the OOM killer**, which chooses a process by a badness score and terminates it — on the grounds that one dead process is better than a machine that has stopped responding.

---

## 6. The Whole Week in One Table

| Event | Cost | Order |
|---|---|---|
| TLB hit | ~0 | — |
| L1 cache hit | 4 cycles | $10^0$ |
| DRAM access | 438 cycles | $10^2$ |
| **Minor page fault** | **~6000 cycles** | $10^3$ |
| Major page fault (SSD) | ~100 000+ cycles | $10^5$ |
| Major page fault (HDD) | ~10 000 000+ cycles | $10^7$ |

*(The first three measured in Week 4; the minor fault measured in §2.)*

**Seven orders of magnitude.** Week 7 measures the bottom two rows.

---

## 7. What to Take Away

1. **Allocation is a promise.** `malloc(512 MiB)` cost 136 KiB of RSS.
2. **Pages arrive on first touch**, one minor fault each — 131 071 faults for 131 072 pages.
3. **Minor faults cost ~6000 cycles**; major faults are thousands of times worse.
4. **COW makes `fork` affordable** — 4.3 ms for 256 MiB, and exactly one fault per page when written.
5. **`mmap` removes a copy and hides the cost model** — an ordinary load can block on disk.
6. **Clock approximates LRU with the one bit the hardware provides.**
7. **Thrashing is a working set that does not fit**, and the OOM killer is the last resort.

---

## Exercises

1. A program allocates 8 GB on a machine with 4 GB of RAM and no swap. `malloc` succeeds. Explain, and say exactly when it will fail instead.
2. From §2's numbers, how long would it take to fault in 16 GiB of anonymous memory? Would you notice it in a benchmark?
3. `fork` followed immediately by `exec` copies almost nothing. Trace which pages *are* copied and why.
4. A parent forks 10 children, each writing to 1% of a 1 GB region. How much physical memory is used in total? State your assumptions.
5. Give a program for which `mmap` is clearly better than `read()`, and one where it is clearly worse. Justify each in terms of the access pattern.
6. Explain Belady's anomaly, and say why LRU cannot exhibit it. *(Hint: consider what the set of resident pages looks like as the frame count grows.)*
7. Using §6's table, compute how many L1 hits fit in the time of one minor fault, and one major fault on an SSD.

---

*Next week: I/O and storage — where the bottom two rows of that table come from.*

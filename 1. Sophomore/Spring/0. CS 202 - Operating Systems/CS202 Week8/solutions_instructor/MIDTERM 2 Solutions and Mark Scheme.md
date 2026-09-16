# CS 202 · Midterm 2 — Solutions and Mark Scheme
## **INSTRUCTOR ONLY** · Do not distribute

---

**Monday of Week 8, 18:00–19:15, VNC 100. 75 minutes, 100 marks, 12.5%.** Covers Weeks 4–7.

**Every number in this scheme is produced by `midterm2_check.sh`** in this folder, which runs the Week 4 Banker reference and the Week 6 page-replacement reference on the paper's own inputs and asserts the rest of the arithmetic. **Run it before printing the paper.**

**Marking principle, as for Midterm 1:** the working carries the marks. **A correct table with an arithmetic slip loses 1**; a bare answer with no working earns at most half the part.

---

## Question 1 — Deadlock (20)

### (a) [5]

**Mutual exclusion, hold and wait, no preemption, circular wait. [2 — all four]**

**Cheapest to remove: circular wait [1].** **The one-line change: thread two takes A before B** — both threads take the locks in one global order. **[1]**

**What the others cost [1 for any two]:** *mutual exclusion* — the data would have to be shareable or duplicated per thread, which changes the program's meaning; *hold and wait* — acquire both locks atomically (a single `lock(&AB)`) or release the first while waiting, which costs concurrency or risks livelock; *no preemption* — `trylock` and release on failure, which **trades deadlock for livelock** (L15 §4).

### (b) [8]

**1. Need = Max − Allocation [1]:**

| | Need |
|---|---|
| P0 | 2 2 2 |
| P1 | 1 0 2 |
| P2 | 1 0 3 |
| P3 | 4 2 0 |

**Totals [1]:** Allocation columns sum to (8, 2, 4); plus Available (1, 1, 2) gives **(9, 3, 6)**.

**2. Safe [3].** Work = (1, 1, 2):

| Step | Process | Need fits? | Work after |
|---|---|---|---|
| 1 | **P1** | (1,0,2) ≤ (1,1,2) ✓ | (6, 2, 3) |
| 2 | **P2** | (1,0,3) ≤ (6,2,3) ✓ | (8, 3, 4) |
| 3 | **P3** | (4,2,0) ≤ (8,3,4) ✓ | (8, 3, 6) |
| 4 | **P0** | (2,2,2) ≤ (8,3,6) ✓ | (9, 3, 6) |

**Safe sequence ⟨P1, P2, P3, P0⟩** — the reference prints exactly this. *(Accept any valid sequence with its Work vectors; only P1 can go first, so all correct answers begin with P1.)*

**3. P3 requests (1, 1, 0): REFUSED [2].** It is within P3's need (4,2,0) and within Available (1,1,2), so the Banker pretends to grant it: Available becomes **(0, 0, 2)**, P3's need becomes (3, 1, 0). Now **no process's need fits**: P0 (2,2,2) ✗, P1 (1,0,2) ✗ (needs 1 of A, none free), P2 (1,0,3) ✗, P3 (3,1,0) ✗. **The state would be unsafe, so the request is denied although the resources are free.**

**4. P1 requests (1, 0, 2): GRANTED [1].** Available becomes **(0, 1, 0)**; P1's need becomes (0, 0, 0), so P1 can finish and release (6, 1, 3), after which the others proceed. *(Reference: `available now (0,1,0) state is SAFE`.)*

### (c) [4]

**Detection compares each process's *current request*, not its maximum remaining *need* [2]** — it asks what *has* happened, not what *could*.

**Detection treats a process holding nothing as finished from the start [2]** — it cannot be part of a cycle, and marking it finished prevents reporting a process that is merely *blocked by* the deadlock as part of it (PS 4 Q2(c)).

### (d) [3]

**Deadlock: every thread is in state `S`, asleep, with `wchan` showing `futex_do_wait`; the CPU is idle. Livelock: the threads are in state `R` and the CPU is busy. [2]**

**Fixes [1]:** deadlock — a global lock order (or detect and kill); livelock — **randomised back-off**, or the same lock order, which removes the need to retry at all.

---

## Question 2 — Address Translation (20)

### (a) [5]

`0x00C03004` = `0000 0000 11|00 0000 0011|0000 0000 0100`:

**Directory index 3, table index 3, offset 4. [3]**

**A TLB miss costs five memory accesses [2]:** four levels of page table (PGD, PUD, PMD, PTE) **and then the data itself.**

### (b) [6]

**64 pages, one per 2 MiB, inside one gigabyte [3]:** one PTE page covers 2 MiB, so **each page needs its own PTE page — 64** — and all 64 PTE pages are indexed by **one PMD page** (which covers 1 GiB). **65 pages = 260 KiB.**

**One dense gigabyte [2]:** 262,144 pages ÷ 512 entries = **512 PTE pages**, plus **one PMD page** = **513 pages = 2,052 KiB.**

**The sentence [1]:** the dense process uses **4,096 times as much memory** for eight times the table pages — **table cost follows the *spread* of the addresses, not their number.**

### (c) [5]

**Reach [2]:** 1,536 × 4 KiB = **6 MiB**; 1,536 × 2 MiB = **3 GiB**.

**At 95% [2]:** 0.95 × 1 + 0.05 × 20 = **1.95 ns** per access.

**Break-even [1]:** translation costs 8 ns when *h* × 1 + (1 − *h*) × 20 = 8 → *h* = **12/19 ≈ 63%**. *(Accept 0.63 or "about two thirds".)*

### (d) [4]

**A TLB shootdown [2]:** the kernel sends an inter-processor interrupt to every CPU that may hold the translation, and waits for each to flush it. **A cannot do it alone because a CPU's TLB is only reachable by that CPU** — there is no instruction to invalidate another core's entry.

**Skipped when [2]:** the other CPU is **not currently using that address space** — Linux marks it *lazy* — because it will flush when it switches back; measured in L17 §6, where a sleeping thread produced **no interrupts** while a busy one produced one per `munmap`.

---

## Question 3 — Demand Paging and Copy-on-Write (20)

### (a) [5]

**Three faults [2].**

| Step | Fault? | Page 0 is then |
|---|---|---|
| read page 0 | yes | **the shared zero page**, read-only, not exclusive |
| write page 0 | yes | **its own zeroed frame**, writable, exclusive |
| write page 1 | yes | (page 1) its own frame, in **one** fault |

**Page 1 is cheaper [3]:** a write to a page that has never been read goes straight to a private frame — **one fault**, where read-then-write costs **two**, because the read installs the shared zero page read-only and the write must then fault again to replace it.

### (b) [6]

**Writing every page [2]:** 1 GiB ÷ 4 KiB = **262,144 faults × 2.7 µs ≈ 0.71 s**, plus the 20 ms fork ≈ **0.73 s**.

**`exec` immediately [1]: 20 ms** — none of the pages is ever written, so none is ever copied.

**Eager copy [2]:** the `fork` itself would have to allocate and copy 1 GiB — **hundreds of milliseconds, paid by every fork**, including the ones that `exec`.

**Still better for the writing child [1]:** the same copying is done, but **spread over the pages actually written** and skipped entirely for pages that are not — and the child starts running after 20 ms instead of after the whole copy.

### (c) [5]

| Pages | For |
|---:|---|
| **1,028** | the user memory: 4,210,688 ÷ 4,096 |
| 2 | the user half's page tables (the first and second 4 MiB) |
| 1 | the page directory |
| **64** | the kernel's page tables, mapped into every process |
| 1 | the child's kernel stack |
| **1,096** | |

**[3] for the 1,028, [2] for accounting for the other 68.**

### (d) [4]

**`err 6` = 110₂: user, write, page not present [1]** — e.g. **writing past the end of the process's memory** (an array overrun beyond `sz`).

**`err 7` = 111₂: user, write, page present but not permitted [1]** — e.g. **writing to the guard page below the stack** (a stack overflow), or **to a kernel address**, both of which are present but lack `PTE_U`.

**[2] for the two distinct mistakes.**

---

## Question 4 — Replacement and Memory Pressure (20)

### (a) [8]

**String: 7 0 1 2 0 3 0 4 2 3 0 3, three frames.**

**FIFO — 10 faults [3]:**

| ref | 7 | 0 | 1 | 2 | 0 | 3 | 0 | 4 | 2 | 3 | 0 | 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | 7 | 7 | 7 | 2 | 2 | 2 | 0 | 0 | 0 | 3 | 3 | 3 |
| | | 0 | 0 | 0 | 0 | 3 | 3 | 3 | 2 | 2 | 2 | 2 |
| | | | 1 | 1 | 1 | 1 | 1 | 4 | 4 | 4 | 0 | 0 |
| fault | ✓ | ✓ | ✓ | ✓ | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |

**LRU — 9 faults [3].** **OPT — 7 faults [2].** *(All three verified by the Week 6 reference.)*

**Accept** any layout of the table that shows the victim at each fault. **Deduct 1** for a correct method with one arithmetic slip.

### (b) [4]

**No [1].** This string simply does not exhibit it; **FIFO is not a stack algorithm**, so *some* string does — 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 gives 9 faults with three frames and 10 with four. **[1]**

**LRU cannot [2]:** after any prefix, LRU holds exactly **the *n* most recently used distinct pages**, so its set with *n* frames is always a **subset** of its set with *n* + 1. A reference that hits with *n* frames therefore hits with *n* + 1, and faults cannot increase.

### (c) [4]

**Both are limited by the same disk [2]:** about 44,000 major faults in four seconds is **as fast as the SSD can fault**, so the *fault rate* is fixed. **Throughput is therefore decided by what fraction of reads fault.**

**Uniform: nearly every read misses** — 14,775 reads per second is roughly the fault rate itself. **Hot: 90% of reads land in a 32 MiB region that fits in the 64 MiB limit**, so only the remaining tenth faults, and throughput is about eleven times higher. **[1]**

**The working set explains the second number [1]:** the process's *resident* need is 32 MiB, not 256 MiB, and 32 MiB fits.

### (d) [4]

RAM + swap = 12 GiB = 12,288 MiB.

**A [1]:** 4,096 ÷ 12,288 = 333‰ → ⅔ × (1000 + 0 + 333) = **889**.
**B [1]:** 200 ÷ 12,288 = 16‰ → ⅔ × (1000 + 500 + 16) = **1,011**.

**B is killed [1]** — its adjustment outweighs A's four gigabytes.

**To protect B [1]:** lower its `oom_score_adj` (to 0, or negative with `CAP_SYS_RESOURCE`) — or raise A's. **Accept** "put A in a cgroup with a `MemoryMax`", which makes A's growth A's own problem.

---

## Question 5 — File Systems (20)

### (a) [5]

**Indirect block holds 512 ÷ 4 = 128 addresses [1]**, so the largest file is (12 + 128) × 512 = **71,680 bytes [2]**.

**20,000 bytes [2]:** ⌈20,000 ÷ 512⌉ = **40 data blocks**, and since 40 > 12 it also needs **the indirect block**: **41 blocks.**

### (b) [5]

**Six reads [3]:** the root inode; the root's data block (find `docs`); `docs`'s inode; `docs`'s data block (find `a.txt`); `a.txt`'s inode; the first data block.

**The second open [2]:** **all of them** are served from the page cache — and in Linux also from the **dentry cache**, which remembers the path-to-inode mapping so the directory blocks are not even re-scanned. **Accept** "the page cache" for 1 and "the dentry cache" for the second.

### (c) [5]

**8 GiB free [3]:** the first pass is cold — 10,000 × 93.9 µs ≈ **0.94 s**; the second finds those blocks cached — 10,000 × 1.61 µs ≈ **0.016 s**.

**200 MiB free [2]:** the 512 MiB file cannot stay cached, so **the second pass is cold too — about 0.94 s again.** The page cache is memory, and memory is what the machine does not have.

### (d) [5]

**10,000 × 3.9 ms = 39 s [1]; 100 flushes × 3.9 ms = 0.39 s [1]** — a hundredfold, at the cost of losing up to 100 records on a crash.

**The four steps [2]:** write the new contents to a temporary file; **`fsync` it**; **`rename` it over the target**; **`fsync` the directory**.

**Omitting the last [1]:** the rename is a metadata change that may not have reached the disk. **After a crash the directory can still show the old file — or neither name** — so the data is durable under a name that does not exist. **A durable file with no durable name is lost.**

---

## Total: 100

| Q | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Marks | 20 | 20 | 20 | 20 | 20 |

**Grade boundaries** are set after marking, as for Midterm 1. **Report Q4(a) and Q1(b) separately in the feedback**: they are the mechanical questions, and a cohort that loses marks there needs a revision session before the final.

---

*CS 202 · Week 8 · Midterm 2 Solutions · Instructor Only*

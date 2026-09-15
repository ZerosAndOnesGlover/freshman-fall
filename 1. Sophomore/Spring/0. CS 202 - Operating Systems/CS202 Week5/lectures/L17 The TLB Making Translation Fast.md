# CS 202 · Operating Systems
## Week 5 · Lecture 2 of 3
### The TLB: Making Translation Fast

---

**Sat:** Wednesday of Week 5, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 19; Ch. 23, Linux half · **Next:** L18, demand paging and physical memory

---

## 1. Five Memory Reads for One

L16 §6 left x86-64 with a four-level walk. **Done literally, one `mov` from memory costs five reads**: PGD entry, PUD entry, PMD entry, PTE, and finally the byte the program wanted. **A program would run at a fraction of its speed.**

**The fix is a cache.** The CPU keeps recent translations — virtual page number to frame number and permission bits — in a small, fast associative memory in the MMU: the **translation lookaside buffer**. On a **hit**, the translation costs almost nothing. On a **miss**, the CPU walks the tables in hardware, then caches the result.

**It works for the same reason every cache works: locality.** A program that uses a few dozen pages at a time hits the TLB almost every time. **The question for this lecture is how many pages "a few dozen" is on this machine, and what happens past it.**

---

## 2. The TLB on This CPU

**The CPU describes its TLBs through `cpuid` leaf 2.** `tlbinfo.c` prints the descriptor bytes, and Intel's SDM (Vol. 2A, Table 3-12) decodes them:

```
cpuid leaf 2 descriptor bytes: 63 03 76 ff b5 f0 c3
```

| Byte | Meaning | Entries | Reach |
|---|---|---:|---:|
| `03` | **data TLB, 4 KiB pages**, 4-way | **64** | **256 KiB** |
| `63` | data TLB, 2 MiB pages, 4-way; and 1 GiB pages | 32; 4 | 64 MiB; 4 GiB |
| `b5` | instruction TLB, 4 KiB pages, 8-way | 64 | 256 KiB |
| `76` | instruction TLB, 2 MiB pages, fully associative | 8 | 16 MiB |
| **`c3`** | **second-level TLB, shared by 4 KiB and 2 MiB pages**, 6-way; and 1 GiB | **1,536**; 16 | **6 MiB of 4 KiB pages, or 3 GiB of 2 MiB** |
| `ff`, `f0` | caches are described in leaf 4; 64-byte prefetching | | |

**Two levels, like the memory caches.** The first-level TLB answers in the same cycle; the second-level one (STLB) is slower but still much cheaper than a walk. **With 4 KiB pages, a program whose working set exceeds 6 MiB takes page walks.** With 2 MiB pages, it can reach 3 GiB first.

---

## 3. What a Miss Costs, Measured

`tlbcost.c` reads **the first byte of a random page**, twenty million times, from working sets of growing size — once with the kernel told not to use huge pages (`MADV_NOHUGEPAGE`), once asked to use them (`MADV_HUGEPAGE`). **Median of three runs**, pinned to one CPU:

| Working set | 4 KiB pages | 2 MiB pages | Gap | Backed by 2 MiB pages |
|---:|---:|---:|---:|---:|
| 1 MiB | 8.06 ns | 7.99 ns | 0.1 | none — too small |
| 4 MiB | **9.61 ns** | 8.01 ns | **1.6** | all |
| 16 MiB | 28.29 ns | 26.61 ns | 1.7 | all |
| 64 MiB | 33.20 ns | 28.59 ns | 4.6 | all |
| 256 MiB | 37.40 ns | 30.51 ns | 6.9 | all |
| 1 GiB | 42.35 ns | 30.62 ns | 11.7 | all |
| **2 GiB** | **50.02 ns** | **32.69 ns** | **17.3** | 1.63–1.78 GiB |

**Two effects are mixed here, and the table separates them:**

- **The jump from 4 to 16 MiB appears in both columns** — about 18 ns. **That is not the TLB.** L3 holds 6 MiB; past it, the byte itself is a cache miss. Huge pages cannot help.
- **The gap between the columns is translation.** At 4 MiB, 4 KiB pages have outgrown the 64-entry first-level TLB and are served by the STLB: **1.6 ns**. Past 6 MiB they need **page walks**, and the gap grows with the working set — because **the walk's own entries stop fitting in cache**. Two gigabytes of 4 KiB pages need 4 MiB of page-table entries, and a random walk misses on them. **At 2 GiB, a third of each access is translation.**
- **With 2 MiB pages the STLB covers 3 GiB**, so there are no walks at all: the column rises only with data-cache misses.

**Translation is cheap until the working set outgrows the TLB, and then it is not.**

---

## 4. Huge Pages

**A 2 MiB page is an entry one level up** — a PMD entry with the *page size* bit set, pointing at 512 contiguous frames instead of at a table. One TLB entry then covers 512 times as much.

**Linux does this automatically for anonymous memory: transparent huge pages.** On this machine it is set to `madvise`:

```
$ cat /sys/kernel/mm/transparent_hugepage/enabled
always [madvise] never
```

— **huge pages only where a program asks**, as `tlbcost` did. The kernel's own counters show how often it tried:

```
thp_fault_alloc 961
thp_fault_fallback 72
```

**Since boot, 72 of 1,033 attempts fell back to 4 KiB pages**, and the 2 GiB run above got only 1.63–1.78 GiB of huge pages. **A huge page needs 512 *contiguous* free frames**, and physical memory fragments; L18 §6 shows the allocator that has to find them.

**Huge pages cost something too**, which is why the default is not `always`:

- **Memory bloat**: touching one byte of a 2 MiB region commits 2 MiB.
- **Latency**: a fault zeroes 2 MiB at once, and finding contiguous frames may mean **compacting** memory first.
- **Sharing and paging out** work on 4 KiB pages; a huge page must often be split first.

**1 GiB pages exist too** (`pdpe1gb` in `/proc/cpuinfo`), through `hugetlbfs`, reserved in advance by the administrator. **Here `HugePages_Total` is 0.**

---

## 5. Context Switches: CR3, PCIDs, and Meltdown

**Each process has its own tables**, and the CPU finds them through one register, **`CR3`**. xv6 loads it on every switch into a process and back to the scheduler:

```c
lcr3(V2P(p->pgdir));  // switch to process's address space      vm.c:176, switchuvm
lcr3(V2P(kpgdir));    // switch to the kernel page table        vm.c:152, switchkvm
```

**The TLB now holds the old process's translations**, and using them would be a disaster. **There are two answers** (OSTEP 19.5):

1. **Flush it.** On x86 without PCIDs, loading `CR3` discards every TLB entry (except ones marked *global*). **xv6 does this**: every switch starts with an empty TLB.
2. **Tag each entry with an address-space identifier**, and keep them. x86's **PCID** is a 12-bit tag; this CPU has it (`pcid` in `/proc/cpuinfo`), and Linux uses it.

**What does switching address spaces cost, then?** `switchcost.c` passes one byte back and forth through pipes between **two threads** (one address space) or **two processes** (two), both pinned to one CPU so every hand-off is a context switch:

```
threads:   3096 ns per switch   processes:   3190 ns per switch
threads:   2984 ns per switch   processes:   3116 ns per switch
threads:   3107 ns per switch   processes:   3133 ns per switch
```

**Between 1% and 4% more** — the `CR3` load and a PCID lookup, lost in the noise of the pipe system calls around it. **With tagged TLBs, changing address spaces is nearly free.** Without them, the new process would pay a miss for every page it touched afresh.

**And Linux already changes `CR3` far more often than on switches.** This CPU is vulnerable to **Meltdown** (2018), which let a user program read kernel memory through a speculative-execution side channel:

```
$ cat /sys/devices/system/cpu/vulnerabilities/meltdown
Mitigation: PTI
```

**Page-table isolation gives every process two top-level tables**: a full one used in the kernel, and one for user mode with almost none of the kernel mapped. **Every system call and interrupt switches `CR3` twice.** Without PCIDs that would flush the TLB twice per system call; with them it is affordable. **L16 §5's "the kernel mapped into every process, so a trap needs no change of tables" is exactly the design Meltdown broke.**

---

## 6. TLB Shootdowns

**A thread's TLB is per CPU, but its page tables are shared by every thread in the process.** When one thread unmaps a page, **other CPUs running the same process may still cache the translation**, and would go on reading and writing a frame that may already belong to someone else. **The kernel must make them forget — and it cannot reach into another CPU's TLB.** It sends an **inter-processor interrupt**, and each receiving CPU flushes the entry itself: a **TLB shootdown**. The kernel counts them:

```
$ grep TLB /proc/interrupts
 TLB:      99394      95864     103137     103564     103531     101350     100332     100140   TLB shootdowns
```

`shootdown.c` maps a page, touches it and unmaps it 200,000 times, on CPU 2, with and without a second thread of the same process on CPU 3:

| Second thread | ns per map, touch, unmap | Shootdown interrupts | per round |
|---|---:|---:|---:|
| none | 5,897 · 5,900 | 170 · 19 | 0.00 |
| **busy on CPU 3** | **6,570 · 7,093** | **199,977 · 196,079** | **1.00 · 0.98** |
| asleep on CPU 3 | 6,089 · 6,598 | 41 · 939 | 0.00 |

- **With another thread running, every `munmap` sent an interrupt**, and the round cost **700–1,200 ns more — 11–20%**, for one other CPU. Every additional CPU running the process adds another interrupt.
- **With the other thread asleep, none were sent.** Its CPU had switched away from the process's tables; Linux marks such a CPU **lazy** and, instead of interrupting it, has it flush when it next switches back. **The sleeping-thread rounds were still slower than single-threaded** — by 3–12%, in two runs — and we did not isolate why.

**"One of the most expensive operations in the kernel" is relative.** A shootdown costs about a microsecond — **a thousand TLB hits** — and it lands on a CPU that was doing something else. **Programs that map and unmap memory constantly with many threads pay it constantly**, which is why allocators such as glibc's keep freed memory mapped instead of returning it at once.

**xv6 never needs one.** Its processes have one thread; a process changes its own tables only in its own system calls (`growproc` then reloads `CR3` with `switchuvm`), and **no other CPU can be running that address space.**

---

## 7. What to Take Away

1. **A TLB hit makes translation nearly free; a miss walks four levels.** This CPU has **64 + 1,536** entries for 4 KiB pages: **6 MiB of reach**.
2. **Measured, translation cost 1.6 ns per access at 4 MiB and 17 ns at 2 GiB** — a third of each access — once page walks miss the cache themselves. **Past 6 MiB of L3, data-cache misses dominate** either way.
3. **2 MiB pages reach 3 GiB of STLB and removed the walks.** Linux gives them to programs that ask; they need 512 contiguous frames, and 7% of attempts here fell back.
4. **Each address space has its own `CR3`.** xv6 flushes the TLB on every switch; **Linux tags entries with PCIDs**, and a process switch cost **1–4%** more than a thread switch.
5. **Meltdown gave every Linux process two top-level tables** and a `CR3` change on every system call, affordable only because of PCIDs.
6. **Changing shared page tables needs an interrupt to every other CPU running the process**: one per `munmap`, 11–20% of the round, measured — **and none for CPUs where the process is asleep.**

---

## Exercises

1. **Effective access time**: with a TLB hit costing 1 ns, a walk 20 ns, and a hit rate of 99%, what does translation add per access on average? At what hit rate does translation cost as much as the 8 ns access itself?
2. Why does the **gap** in §3's table grow from 4.6 ns at 64 MiB to 17.3 ns at 2 GiB, although both are far beyond the STLB's reach?
3. A program allocates 64 MiB and uses it randomly. **How many of its accesses can the TLB answer without a walk** with 4 KiB pages, and with 2 MiB pages?
4. **Without PCIDs**, how many TLB entries would a process refill after each switch if it touched 200 pages per slice? Using §3, estimate the cost.
5. A 16-thread program running on 8 CPUs unmaps one page. **How many shootdown interrupts does Linux send**, and what information does it need to decide?

---

*CS 202 · Week 5 · L17 · © CSE Department*

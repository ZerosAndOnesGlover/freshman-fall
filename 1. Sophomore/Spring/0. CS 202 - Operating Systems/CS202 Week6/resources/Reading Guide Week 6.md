# CS 202 · Reading Guide · Week 6
## Page Replacement and Swapping: OSTEP 21–23, Denning, and the OOM Killer

---

**The curriculum names no reading for Week 6.** The ideas this week are old — Belady's anomaly is from 1969, the working set from 1968 — and OSTEP covers them well. **Read OSTEP 22 before Wednesday**, with pencil and paper: its examples are exactly the ones PS 6 asks you to reproduce in code.

| Source | Now? | Why |
|---|---|---|
| **OSTEP 21. Beyond Physical Memory: Mechanisms** | **Read** | Swap space, the present bit, the page fault that goes to disk, and when to evict. **L19** |
| **OSTEP 22. Beyond Physical Memory: Policies** | **Read** | FIFO, random, OPT, LRU, Clock; Belady's anomaly; thrashing. **L20, PS 6** |
| OSTEP 23. Complete Virtual Memory Systems | *Read the VAX/VMS half* | Segmented FIFO with second-chance lists — Clock's cousin, and what Linux's lists descend from. **L20 §7** |
| Silberschatz, Ch. 10 §10.4–§10.6, §10.9 | *Reference* | Page-replacement algorithms with worked strings; frame allocation; **thrashing and the working-set model**. The worked string in §10.4 is PS 6 Q1's |
| **Denning, P. J. (1968), "The Working Set Model for Program Behavior"**, *CACM* 11(5) | *Optional, and short* | Where the working set and the explanation of thrashing come from. **L21 §1–§2** |
| `man 5 proc`, entries for `oom_score`, `oom_score_adj`, `clear_refs`, `smaps` | **Before Lab 6** | The files you read and write |

**If you have two hours:** OSTEP 22 with the simulator open, then OSTEP 21's §21.5–§21.7.

---

## OSTEP Chapter 21 — mechanisms

1. OSTEP's page-fault path goes to disk only when the page table entry says the page is in swap. **Where does the kernel keep a swapped-out page's location**, given that the entry's frame-number bits are meaningless for a page not in memory? *(Compare Lab 5's swap type and offset fields.)*
2. OSTEP computes the effective access time for a fault rate. **Redo its arithmetic with this machine's numbers** from L17 and L19: a memory access of about 10 ns and a major fault from the SSD. **What fault rate doubles the average access time?**
3. §21.7 describes a swap daemon that evicts when free memory falls below a **low watermark** and stops at a **high watermark**. **Why two thresholds, not one?** What happens when a program allocates faster than the daemon can evict? *(L19 §5 names it.)*

---

## OSTEP Chapter 22 — policies

4. **Work the chapter's FIFO, LRU and OPT examples by hand** before running `pagesim`. Then run them. **If your hand count differs from the program's, find out which is wrong.**
5. OSTEP shows Belady's anomaly for FIFO with the string 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5. **Explain in one paragraph why LRU and OPT cannot show it** — the property is called being a *stack algorithm*.
6. OSTEP's **80-20 workload** plot shows LRU well above random and close to OPT. **What property of the workload makes that true**, and what workload would make LRU no better than random? *(PS 5 Q3 met one.)*
7. Clock approximates LRU using one bit per page. **Who sets the bit, and who clears it?** Why is exact LRU — a timestamp on every access — impossible to implement in a kernel, although the simulator does it easily?
8. OSTEP defines **thrashing** in two sentences. **Before L21, predict the shape** of a curve of throughput against memory limit for a program whose working set is 256 MiB. Is it a gentle slope or a cliff?

---

## Denning (1968), if you read it

9. Denning defines the working set **W(t, τ)** as the pages referenced in the last τ time units. **L21 §1 measures one with `/proc/self/clear_refs`.** What does the choice of τ correspond to in that measurement?
10. Denning's argument is that **a process should run only if its working set fits**. **What does a modern Linux do instead** when the working sets of all processes do not fit? *(L21 §3–§5.)*

---

## Where to Go Deeper

| Source | Topic | When |
|---|---|---|
| **Love**, Ch. 16 "The Page Cache and Page Writeback" | File pages as evictable memory | For L19 §4 |
| Kernel documentation, `admin-guide/mm/multigen_lru.rst` (online) | Linux's multi-generational LRU, enabled on this kernel | For L20 §7 |
| `man 2 madvise`, `man 2 mlock` | Asking the kernel not to evict, or to evict now | For L19 and Lab 6 |
| `man 5 systemd.resource-control` — `MemoryMax=`, `MemorySwapMax=` | The limits Lab 6 runs under | **Before Lab 6** |
| `man 8 systemd-oomd` | The userspace killer that runs before the kernel's | For L21 §3 |

---

*CS 202 · Week 6 · Reading Guide · © CSE Department*

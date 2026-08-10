# CS 201 · Problem Set 6
## A Page Table Simulator

---

**Released:** Week 6, Wednesday · **Due:** Week 7, Friday 17:00
**Total: 100 points** · Submit one PDF plus a `.zip` of source, `PS6_{LastName}_{StudentID}.pdf`

> **Q3 is the centrepiece** — a working four-level page table with a TLB and a replacement policy.
> Q1 and Q2 are by hand; Q4 and Q5 want measurements from your own machine.

---

### Q1: Translation by Hand (18 points)

x86-64, 4 KiB pages, four levels of 9 bits.

**(a) [4]** Give the bit split of a 48-bit virtual address: which bits are PGD, PUD, PMD, PTE and offset. Show that they sum correctly.

**(b) [4]** For virtual address `0x00007f3c2a4b1000`, give the four table indices and the offset. Show your working.

**(c) [4]** Each table has 512 entries of 8 bytes. Show that a table is exactly one page, and explain why that is a design goal rather than a coincidence.

**(d) [3]** A flat single-level page table for a 48-bit space with 4 KiB pages and 8-byte entries: compute its size. Then compute it for 2 MiB pages. State what this tells you about huge pages beyond their TLB benefit.

**(e) [3]** A process maps 100 GB of address space but touches only 4 MB of it. Estimate how many page-table pages it needs, by level. Explain why the tree wins here.

---

### Q2: The PTE and Its Bits (14 points)

**(a) [4]** Name the purpose of each: **P**, **R/W**, **U/S**, **A**, **D**, **NX**.

**(b) [3]** **A** and **D** are set by hardware and cleared by the OS. Explain what the OS uses each for, and why the interface is this minimal.

**(c) [4]** Copy-on-write marks pages **read-only** in both parent and child even though both are logically writable.

Explain how the fault handler distinguishes "this process may not write here" from "this process may write here, but I must copy first". **The answer is not in the PTE — say where it is.**

**(d) [3]** In Week 3 you added a `.note.GNU-stack` directive and watched `readelf` report `GNU_STACK` change from `RWE` to `RW`. **Which bit of which structure does that ultimately control**, and at what granularity is it applied?

---

### Q3: Build the Simulator (38 points)

Write a C program simulating a four-level page table with a TLB.

```
./pagesim <trace-file> [--tlb N] [--frames M] [--policy fifo|clock]
```

The trace is one virtual address per line, in hex, optionally followed by `R` or `W`.

**(a) [12]** **Translation.** Implement the four-level walk with sparsely allocated tables — a level is created only when something below it is needed. Report, for a run:

- total accesses;
- page-table pages allocated, **by level**;
- the peak resident set in frames.

**(b) [8]** **The TLB.** Add a fully associative TLB of `N` entries with LRU replacement. Report hits, misses and hit rate.

Then **sweep `N` over 8, 16, 32, 64, 128, 256** on a trace with locality, and plot or tabulate the hit rate. **Identify the knee** and relate it to the trace's working set.

**(c) [10]** **Replacement.** With only `M` physical frames, implement **FIFO** and **Clock**. Clock must use a simulated **A** bit, set on access and cleared by the sweeping hand — not a timestamp.

Report fault counts for both, at `M` = 16, 64, 256, 1024.

**(d) [4]** **Belady's anomaly.** Construct a reference string on which **FIFO produces more faults with more frames**. Show the fault counts at both frame counts and explain the mechanism.

Then state why **LRU cannot** exhibit it. *(Consider the set of resident pages as the frame count grows.)*

**(e) [4]** **Validate against reality.** Generate a trace by instrumenting a real loop — a sequential array walk, and a random one — and run both through your simulator with a 64-entry TLB.

Compare the TLB hit rates with what Lab 6 Part 4 measured on hardware. **Where does your simulator disagree with the machine, and what is it not modelling?**

---

### Q4: Demand Paging, Measured (16 points)

**(a) [4]** Reproduce Lab 6 Part 2. Report RSS and minor faults at all three points, and check the fault increase against the page count.

Reference *(verified)*: `malloc(512 MiB)` grew RSS by **136 KiB**; touching every page produced **131 071** faults for **131 072** pages.

**(b) [4]** Measure the cost of one minor fault by timing first touch against second touch.

Reference *(verified)*: 1967 ns/page and 19 ns/page → **~1948 ns ≈ 6200 cycles**.

Express it as a multiple of a DRAM access (438 cycles) and of an L1 hit (4 cycles).

**(c) [4]** Reproduce the copy-on-write experiment. Report `fork` time, the child's faults at birth, and the increase after writing one byte per page.

Reference *(verified)*: 4.3 ms; **14** faults at birth; **+65 536** for **65 536** pages.

**(d) [4]** Estimate how long copying 256 MiB would actually take on your machine, using a bandwidth figure you measure. **Compare with the 4.3 ms `fork` took** and state what `fork` spent its time on instead.

---

### Q5: Translation Is a Separate Cost (14 points)

**(a) [6]** Reproduce Lab 6 Part 4: 512 pointers in a random chase, constant 32 KiB cache footprint, stride varying from 64 B to 64 KiB.

Report your table. Reference *(verified)*: **1.24 ns at 8 pages, 27.57 ns at 8192 pages.**

**(b) [4]** The data is L1-resident in every row. **Explain the 22×.** Then estimate the L1 dTLB size from where the cost first jumps, and state your reasoning.

**(c) [4]** Repeat a large random chase with and without `MADV_HUGEPAGE`.

Reference *(verified)*: **no benefit at any size** — ratios 1.00× to 1.06× from 1 MiB to 1 GiB.

**Explain the null result**, given that (a) shows translation costing 22×. Then **describe a benchmark that would show a huge-page benefit**, and say precisely what you changed.

---

## Marks

| | |
|---|---:|
| Q1 Translation by Hand | 18 |
| Q2 The PTE and Its Bits | 14 |
| Q3 Build the Simulator | 38 |
| Q4 Demand Paging, Measured | 16 |
| Q5 Translation Is a Separate Cost | 14 |
| **Total** | **100** |

---

*CS 201 · Week 6 · Problem Set 6*

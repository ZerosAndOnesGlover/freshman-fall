# CS 201 · Computer Organization & Architecture
## Week 6: Virtual Memory

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), ECE 110 (digital logic)
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** PS 6 (due Week 7 Friday), Lab 6 *(sat Tuesday of Week 7)*, and **Quiz 6 on Monday, covering Week 5**.

> **Midterm 1 was last week.** Papers are returned in Week 7. The two parts most often lost were the
> stack-alignment parity and the miss-level diagnosis — both recur this week, so the review is not
> a detour.

---

### Why This Week Exists

Because there is a translation step under every load and store in the course so far, and you have not seen it.

Week 2 read addresses out of instructions. Week 3 put a stack frame at one. Week 4 measured what it costs to fetch one. **None of those addresses were real.** Every one went through a four-level lookup first, and the machinery that does it explains things the previous five weeks could not:

- why a bad pointer faults instead of corrupting another process;
- why `fork` of a 256 MiB process takes 4 milliseconds;
- why `malloc` of half a gigabyte costs 136 kilobytes;
- why data that fits entirely in L1 cache can still be **22× slower** than it should be.

**That last one is the week's real finding**, and it is a genuine addition to Week 4's advice rather than a footnote to it.

---

### Learning Objectives

By the end of Week 6, you should be able to:

1. Explain what virtual memory buys — isolation, relocation, overcommit — and why isolation is the strongest.
2. Split a virtual address into four table indices and an offset, by hand.
3. Explain why the page-table index is 9 bits, deriving it rather than stating it.
4. Name the PTE's flag bits and say what the OS uses each for.
5. Explain W^X and where NX physically lives.
6. Read `/proc/PID/maps` and identify every region.
7. Define TLB reach and compute it.
8. **Demonstrate that cache residency and TLB reach are separate capacities.**
9. Distinguish minor from major faults and state the cost of each.
10. Explain demand paging, and why virtual size and resident size differ.
11. Explain copy-on-write from fault counts, and where the fault handler gets the information the PTE lacks.
12. Compare FIFO, LRU and Clock, and explain why Clock is what real kernels use.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L19 Virtual Memory and the Page Table.md` | The illusion, the four-level tree, the PTE bits, and a real address space |
| `lectures/L20 The TLB and the Cost of Translation.md` | Reach, the 22× isolation experiment, and huge pages that did nothing |
| `lectures/L21 Demand Paging Copy-on-Write and Replacement.md` | Faults measured at 6000 cycles, COW at one fault per page, Clock and thrashing |
| `assignments/PS 6 A Page Table Simulator.md` | Translation by hand, a four-level simulator with TLB and Clock, and Belady's anomaly |
| `assignments/QUIZ 6 Week 6 Monday.md` | Ten minutes on Week 5. **Unmarked — key in the paper** |
| `lab/LAB 6 Observing Page Faults.md` | `/proc`, demand paging, COW, and isolating the TLB from the cache |
| `resources/Reading Guide Week 6.md` | CS:APP Ch. 9, plus the man pages that are the real specification |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Cache residency and TLB reach are different capacities, and you must satisfy both.**

512 pointers — always 512 cache lines, always 32 KiB, always resident in a 32 KiB L1d. **The only variable is how many pages they are spread across:**

| pages spanned | 8 | 32 | 128 | 512 | 2048 | **8192** |
|---|---:|---:|---:|---:|---:|---:|
| ns/access | **1.24** | 4.28 | 12.68 | 14.57 | 15.77 | **27.57** |

**The data never left L1.** The first row's 1.24 ns is the same L1 latency Week 4 measured as 1.22 ns, arrived at independently two weeks later. **Everything above it is address translation.**

Week 4 taught you to count cache lines. **Count pages too.**

---

### Assessment Reminder

**Labs and quizzes carry no weight**; the four weighted components already total 100%. Both remain required.

**Quiz 6 is Monday**, covering Week 5, key in the paper.

**Lab 6 is sat on the Tuesday of Week 7** — the lab runs a week behind the lectures, deliberately, so that it follows all three of the week's sessions. See the syllabus for the full mapping.

**PS 6's simulator is the largest single piece of code in the course so far.** Start it early. The Clock implementation must use a simulated accessed bit rather than timestamps — a version built on timestamps is LRU and scores nothing for that part.

---

### Connections

**Back:** **Week 4's address split** into tag/index/offset is the same idea with a different block size — and this week's experiment is deliberately built to hold Week 4's variable constant. **Week 3's guard page** is now explicable: it is an unmapped page, and the fault is the enforcement. **Week 3's `GNU_STACK` flag** turns out to control the NX bit in every PTE of the stack region.

**Forward:** **Week 7's storage** supplies the bottom two rows of the cost table — major faults are disk reads, and this week's `mmap` is how a file becomes memory. **Week 9's ASLR** is the randomisation you will see in `/proc/self/maps`, and **W^X is why an attacker cannot simply write shellcode and jump to it.** **Week 10's TLB shootdown** is this week's coherence problem across cores.

**Sideways:** **PROG 201 is using `mmap`, `fork` and `brk` this term**, and CS 202 next semester implements everything in this week. **OSTEP chapters 13–24 are that course's textbook** — reading them now is not wasted effort.

---

*CS 201 · Week 6 · © CSE Department*

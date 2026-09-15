# CS 202 · Operating Systems
## Week 5: Memory Management — Physical and Virtual

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 201, PROG 201
**Assessment for this course (overall):** Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%
**This week's deliverables:** PS 4 due **Friday**, PS 5 released **Wednesday**, **Quiz 5** at the start of **Monday's** lecture (covers Week 4).
**Lab 4 — last week's deadlock — is sat on the Tuesday of this week; Lab 5 covers this week and is sat on the Tuesday of Week 6.**

---

### Why This Week Exists

Because every process on the machine believes it owns the same addresses, and something has to make that true on every single memory access.

**A local variable lives nearly 128 TiB above zero, in a machine with 7.7 GiB of memory; run the program again and it lives somewhere else.** The CPU translates every address, on every access, through tables the kernel builds — and the kernel uses that one indirection to isolate processes, to place them anywhere, to hand out memory only when it is used, and to make `fork` of a gigabyte cost 20 milliseconds. **This week is how the tables are laid out, how the translation is made fast enough to be invisible, and what the kernel does with a page fault.**

**Everything is measured.** How many pages an xv6 fork actually takes, and what each is for. What a TLB miss costs at 4 MiB and at 2 GiB. What changing address spaces costs when TLB entries are tagged. How many interrupts an `munmap` sends. And what the kernel will — and will not — tell an ordinary user about where their memory is.

---

### Learning Objectives

By the end of Week 5, you should be able to:

1. Explain what **virtual addresses** buy — isolation, relocation, sparseness — and why base-and-bounds and segments fall short.
2. **Split an address** into page number and offset, and into xv6's **10/10/12** and x86-64's **9/9/9/9/12** fields.
3. **Walk a two-level page table** by hand and in C, and say what `P`, `W`, `U`, `A` and `D` mean and who sets each.
4. **Account for the page-table memory** of a process, in xv6 and in Linux, including why every xv6 process pays 65 pages for the kernel.
5. Explain **canonical addresses**, where user space ends on x86-64, and why a five-level kernel runs with four levels here.
6. Explain the **TLB**, read this CPU's TLB sizes, and **explain a measured miss cost** — separating it from data-cache misses.
7. Say what **huge pages** save and cost, and how Linux decides to use them.
8. Explain **flushing versus tagging** the TLB on a context switch, what **PCIDs** changed, and why **Meltdown** made them essential.
9. Explain a **TLB shootdown**, measure one, and say when Linux can skip it.
10. Explain **demand paging, the zero page and copy-on-write**, and **measure each fault's cost**.
11. Decode an x86 **page-fault error code**, and say what Linux and xv6 each do with a fault.
12. Explain a **buddy allocator** from `/proc/buddyinfo`, and why **frame numbers are hidden** from users.

---

### This Week's Materials

| File | Purpose |
|---|---|
| [[L16 Address Spaces and Page Tables]] | Addresses that differ every run; base and bounds; pages and frames; **xv6's `walkpgdir`**; **a 1,096-page fork, every page accounted for**; x86-64's four levels and **the page above 2⁴⁷ you cannot map**; `VmPTE` measured |
| [[L17 The TLB Making Translation Fast]] | **This CPU's 64 + 1,536 TLB entries** from `cpuid`; **a miss costing 1.6 ns at 4 MiB and 17 ns at 2 GiB**; transparent huge pages; `CR3`, PCIDs and Meltdown — **a process switch 1–4% dearer than a thread switch**; **one shootdown per `munmap`**, and none to a sleeping thread |
| [[L18 Demand Paging Copy on Write and Physical Memory]] | **1.9 µs per first touch, 14 ns after**; four xv6 page faults decoded — **and a program overwriting its own code**; the zero page and copy-on-write **watched through `pagemap`**; **forking a gigabyte in 20 ms**; xv6's free list and **Linux's buddy allocator fragmenting**; why frame numbers are secret |
| [[CS202 Week5/assignments/QUIZ 5 Week 5 Monday\|QUIZ 5 Week 5 Monday]] | Ten minutes, covers **Week 4**, answer key printed |
| [[PS 5 A Two-Level Page Table and a TLB]] | A page table in simulated physical memory, a TLB per CPU, stale translations, and superpages. Due **Friday of Week 6** |
| `assignments/ps5/` | `pt2.c` with `TODO`s, and six traces |
| [[LAB 5 Reading the Page Map]] | `pagemap` read while pages are demand-allocated, shared by `fork`, tracked for writes and paged out. **Tuesday of Week 6** |
| `lab/pmwalk.c`, `lab/pmlab.c` | A per-mapping page census, and four pages watched through four experiments |
| [[CS202 Week5/resources/Reading Guide Week 5\|Reading Guide Week 5]] | OSTEP 13, 18–20 and 23; **xv6 book Chapter 2 with `vm.c` open** |
| `resources/*.c`, `nfree.patch` | Every lecture measurement — and **the one xv6 system call we added** to count free pages |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Translation is a cache problem, and allocation is a laziness problem.**

The page table makes every access possible; the TLB makes it cheap — **until the working set outgrows 1,536 entries, and a third of every access becomes page walking.** Huge pages, PCIDs and lazy shootdowns are all ways of keeping that cache warm.

**And Linux does no memory work until it has to.** `mmap` records a promise; the first touch pays; a read gets a shared page of zeros; `fork` shares everything and copies one page at a time as it is written. **xv6 does all of it at once**, which is why its page-fault handler can be three lines — and why Project 2 will ask you to make it lazy.

---

### Assessment Reminder

**PS 4 is due Friday at 17:00. PS 5 is released Wednesday.**

**Labs and quizzes carry no weight** and are still required. **Quiz 5 is at the start of Monday's lecture and covers Week 4.**

> **Two labs touch this week.** **Lab 4** — finding a deadlock — is sat on the **Tuesday of this
> week**. **Lab 5** covers this week and is sat on the **Tuesday of Week 6**.

Both are tracked in [[_CS 202 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 0's wall** is `PTE_U`, checked on every access. **Week 1's `fork` and `exec`** are where the page tables are copied and replaced; Lab 1 read `/proc/<pid>/maps`, the VMAs of L18 §2. **L10's `panic: remap`** was `mappages` refusing a page twice. **CS 201** built the memory hierarchy these tables sit in; its caches are why a TLB miss is sometimes 2 ns and sometimes 17.

**Sideways:** **PROG 201**'s `malloc` sits on top of L18's `mmap` and first-touch faults.

**Forward:** **Week 6** uses the accessed and dirty bits to choose what to evict, and turns Lab 5 Part E's voluntary page-out into involuntary swapping. **Project 2** adds lazy allocation or copy-on-write to xv6. **Week 10's hypervisor** adds a second layer of translation — the `ept` in `/proc/cpuinfo`. **Week 12** returns to Rowhammer and Meltdown as attacks.

---

*CS 202 · Week 5 · © CSE Department*

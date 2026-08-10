# CS 201 · Week 6 · Reading Guide
## CS:APP Chapter 9 — Virtual Memory

---

**Set reading:** Bryant & O'Hallaron, **§9.1–9.8**. §9.9 onward is dynamic memory allocation, which PROG 201 covers.
**Also:** `man 2 mmap`, `man 5 proc` (the `maps` and `smaps` sections). **Read the man pages; they are the specification.**

---

## Why This Chapter Is Different

Chapters 3 and 6 described things you could see — instructions in a disassembly, cache misses in a profile. **Nothing in this chapter appears in your code.** No instruction says "translate this address"; every load and store does it silently.

**`/proc` is the substitute for a disassembler**, and Lab 6 is two hours of using it. Read §9.1–9.4 before Tuesday and the lab becomes an experiment rather than a tutorial.

---

## Section by Section

| § | Topic | What to take from it |
|---|---|---|
| **9.1** | Physical and virtual addressing | The core distinction. Two pages |
| **9.2** | Address spaces | Why the virtual space can exceed physical memory |
| **9.3** | VM as a tool for caching | **The framing that makes the chapter click** — DRAM as a cache for disk, with the same vocabulary as Chapter 6 |
| **9.4** | VM as a tool for memory management | Sharing, and why linking is simple because of it |
| **9.5** | **VM as a tool for memory protection** | Per-page permission bits. This is NX and W^X |
| **9.6** | **Address translation** | The core mechanics. §9.6.2 is the TLB; §9.6.3 the multi-level table |
| **9.6.4** | An end-to-end example | **Work it fully by hand.** It is PS 6 Q1 in miniature |
| **9.7** | Case study: Core i7 / Linux | Real four-level tables. Compare with your own `/proc/self/maps` |
| **9.8** | **Memory mapping** | `mmap`, shared vs private, and **copy-on-write** |

---

## Questions to Read Against

**On §9.1–9.5**

1. §9.3 frames virtual memory as a cache. Complete the analogy: what is the "line", the "hit", the "miss", and the "miss penalty"? Compare each with Chapter 6.
2. Why is the page size 4 KiB rather than 64 bytes like a cache line, or 4 MiB? Give one cost of each extreme.
3. §9.5 gives permission bits per page. **Which one makes `W^X` possible**, and what did Week 3's Lab Part 5.1 do to it?

**On §9.6 — the mechanics**

4. Work §9.6.4's end-to-end example completely by hand, including the TLB lookup and the cache access.
5. A four-level walk costs four memory accesses. **Why is that acceptable in practice?** Give the number that makes it so.
6. **Why is the page-table index 9 bits?** Derive it from the page size and the entry size — do not just state it.
7. Define TLB **reach** and compute it for the book's figures. Compare with the 256 KiB this course measured.

**On §9.7–9.8**

8. §9.8 distinguishes `MAP_SHARED` from `MAP_PRIVATE`. Which one is copy-on-write, and what does the other do on a write?
9. `fork` is described as "copying" the address space. **What is actually copied, and what is not?**
10. Give one program for which `mmap` is clearly better than `read()`, and one where it is clearly worse.
11. §9.8 notes that an executable is *mapped*, not read. What does that buy when twenty processes run the same binary?

> **Question 6 is the one worth working out rather than reading.** Once you see that 9 bits falls out
> of $\log_2(4096/8)$, the whole structure stops looking arbitrary.

---

## Reading Against the Machine

```bash
# 1. Your own address space — do this before Tuesday
cat /proc/self/maps
getconf PAGESIZE

# 2. Virtual vs resident, live
/usr/bin/time -v ./yourprog 2>&1 | grep -E "Maximum resident|page faults"

# 3. Does malloc commit anything?
#    Allocate 512 MiB, print RSS from /proc/self/statm before and after.
#    PREDICT the answer first.
```

**Item 3 is the single most surprising measurement of the week.** *(The answer, verified: `malloc(512 MiB)` grew RSS by 136 KiB.)*

**And a caution the book does not give you.** CS:APP's Core i7 case study is from 2015 hardware with 4-level tables and specific TLB sizes. **Your machine may differ** — check `/proc/cpuinfo` and `getconf` rather than assuming. Some modern x86-64 parts have a fifth level (57-bit addresses), off by default.

---

## Terminology You Should Own by Week 7

| | | |
|---|---|---|
| virtual / physical address | page / frame | page table |
| PTE | multi-level page table | `cr3` |
| TLB | TLB reach | TLB shootdown |
| ASID / PCID | page fault | minor / major fault |
| demand paging | overcommit | resident set size |
| copy-on-write | memory-mapped file | `MAP_SHARED` / `MAP_PRIVATE` |
| swap | page replacement | Clock / second-chance |
| Belady's anomaly | thrashing | working set |
| guard page | ASLR | W^X / NX |

---

## If You Want More

**OSTEP** *(Operating Systems: Three Easy Pieces)*, free at ostep.org — **chapters 13–24 are virtualization of memory** and are the best treatment available for this material. **This is CS 202's textbook next semester**, so reading a few chapters now is not wasted.

**`man 5 proc`** is long and worth skimming once. `smaps` in particular gives per-mapping resident, shared and private byte counts — useful the first time someone asks "how much memory is this process *really* using", which turns out to be four different questions.

**Ulrich Drepper's memory paper**, §4, covers TLBs and virtual memory with the same rigour §3 brought to caches. If you read §3 for Week 4, §4 is the natural sequel.

---

*CS 201 · Week 6 · Reading Guide*

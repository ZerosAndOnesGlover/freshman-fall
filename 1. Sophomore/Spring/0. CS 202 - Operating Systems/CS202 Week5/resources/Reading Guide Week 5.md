# CS 202 · Reading Guide · Week 5
## Memory Management: OSTEP on Paging and the TLB, and xv6's Page Tables

---

**The curriculum names no reading for Week 5.** This is the heaviest reading week of the term so far, because the ideas are compact and the details matter. **Read OSTEP 18 and 19 before Wednesday**, and the xv6 chapter before PS 5.

| Source | Now? | Why |
|---|---|---|
| **OSTEP 13. The Abstraction: Address Spaces** | **Read** | Why every process gets the same addresses. **L16 §1** |
| OSTEP 15. Address Translation; 16. Segmentation | *Skim* | Base and bounds, and segments — what came before pages. **L16 §2** |
| **OSTEP 18. Paging: Introduction** | **Read** | Pages, frames, the page table, and what a flat table costs. **L16 §3–§5** |
| **OSTEP 19. Paging: Faster Translations (TLBs)** | **Read** | The TLB, its hit rate, context switches, ASIDs. **L17** |
| **OSTEP 20. Paging: Smaller Tables** | **Read §20.3–§20.4** | Multi-level page tables. **L16 §4–§6** |
| OSTEP 23. Complete Virtual Memory Systems | *Read the Linux half* | Demand zero, copy-on-write, huge pages, and the kernel's own mappings. **L17 §4, L18** |
| **xv6 book (x86, rev. 11), Ch. 2 "Page tables"** | **Read, with `mmu.h`, `memlayout.h` and `vm.c` open** | The two-level table you implement in PS 5. **L16 §4** |
| Silberschatz, Ch. 9 §9.3–§9.4; Ch. 10 §10.1–§10.3 | *Reference* | Paging and its structures; demand paging and copy-on-write, with more worked arithmetic than OSTEP |

**If you have two hours:** OSTEP 18 and 19, then xv6 Chapter 2's first half with `walkpgdir` open.

---

## OSTEP Chapters 13, 18 and 20

1. Chapter 13 lists three goals of virtual memory: transparency, efficiency and protection. **For each, name the part of an x86 page-table entry or of the MMU that serves it.**
2. OSTEP computes the size of a **flat page table** for a 32-bit address space with 4 KiB pages and 4-byte entries. **Reproduce the number.** Then compute it for x86-64's 48-bit addresses with 8-byte entries, and say why nobody builds that.
3. Chapter 20's two-level table saves memory only when the address space is **sparse**. **L16 §5 measures an xv6 process whose page tables are more than a twentieth of its size.** Before reading it, predict: what is using those pages, since the process itself is tiny?
4. Chapter 20 notes that a multi-level table makes a TLB miss **more** expensive. **How many memory accesses does a miss cost with xv6's two levels, and with x86-64's four?**

---

## OSTEP Chapter 19 — the TLB

5. OSTEP's array-access example gets a 70% hit rate from spatial locality. **Why does accessing a 2-D array in column order destroy it** when each column is longer than a page? *(PS 5 Q3 measures it.)*
6. On a context switch, the TLB holds the old process's translations. **Give OSTEP's two ways of dealing with that**, and say which one x86's **PCID** is. **L17 §5 measures what switching address spaces costs on this machine** — predict whether a switch between two processes will be much slower than one between two threads.
7. OSTEP mentions that with several CPUs, changing a page table requires telling the others. **Why can't a CPU simply check its own TLB entry against the page table** before using it?

---

## xv6 Chapter 2 — Page tables

Read `walkpgdir` and `mappages` in `vm.c` side by side with the book's description.

8. **What does `walkpgdir` do when the page table for an address does not exist and `alloc` is 0?** Find every caller that passes 0, and say why none of them wants a table created.
9. `walkpgdir` gives every page-directory entry **`PTE_P | PTE_W | PTE_U`**, even for kernel addresses. The comment says this is "overly generous". **Why is it nonetheless safe?**
10. **Every xv6 process's page directory maps the whole kernel** (`setupkvm`, `kmap[]`). Count the page tables that costs, from `memlayout.h`. **L16 §5 and PS 5 Q2 give the answer**; check yours.
11. Find where `exec` makes the **guard page** below the user stack. What happens if a program overflows its stack into it — and **what does xv6's `trap` do next?** *(L18 §2.)*

---

## Where to Go Deeper

| Source | Topic | When |
|---|---|---|
| **Love**, Ch. 12 "Memory Management" | Zones, the **buddy allocator**, slab | For L18 §6 |
| **Love**, Ch. 15 "The Process Address Space" | VMAs, `mm_struct`, page faults | For L18 §1–§2 |
| `man 5 proc_pid_pagemap` | The file Lab 5 reads, bit by bit | **Before Lab 5** |
| `man 2 madvise` — `MADV_HUGEPAGE`, `MADV_PAGEOUT` | Asking the kernel for huge pages, and for eviction | For L17 §4 and Lab 5 Part D |
| Kim et al. (2014), "Flipping Bits in Memory Without Accessing Them", *ISCA* | **Rowhammer** — why frame numbers became secret | *Optional*, for L18 §7 |
| Lipp et al. (2018), "Meltdown", *USENIX Security* | Why Linux keeps a second page table for every process | *Optional*, for L17 §5 |

---

*CS 202 · Week 5 · Reading Guide · © CSE Department*

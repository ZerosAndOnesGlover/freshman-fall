# CS 201 · Quiz 7
## Administered: Monday, Week 7 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 6** — virtual memory, the TLB, demand paging and copy-on-write.

**Instructions:** Closed notes. 10 minutes.

> **Unmarked, no weight.** Key below. Sit it closed-book first.

---

**Q1.** Why is the x86-64 page-table index 9 bits? Derive it.

&nbsp;

&nbsp;

---

**Q2.** How many memory accesses does one load take if the TLB misses and the tables are not cached?

&nbsp;

&nbsp;

---

**Q3.** Define TLB **reach**. Compute it for 64 entries at 4 KiB.

&nbsp;

&nbsp;

---

**Q4.** 512 pointers occupying 32 KiB of L1-resident cache lines cost 1.24 ns spread over 8 pages and 27.57 ns over 8192. The data never left L1. What changed?

&nbsp;

&nbsp;

---

**Q5.** `malloc(512 MiB)` increased resident memory by 136 KiB. Explain.

&nbsp;

&nbsp;

---

**Q6.** A child process writes one byte to each page of a shared 256 MiB region and takes exactly 65 536 minor faults. What caused them, and which PTE bit is responsible?

&nbsp;

&nbsp;

---

**Q7.** The PTE cannot distinguish a copy-on-write fault from a protection violation. Where does the kernel get that information?

&nbsp;

&nbsp;

---

<div style="page-break-after: always;"></div>

---

## Answer Key — Mark Your Own

**Q1.** A page is 4096 bytes and a page-table entry is 8 bytes, so a table holds $4096/8 = 512$ entries, and $\log_2 512 = \mathbf{9}$.

**The index width is a consequence of the page size and entry size**, not an independent design choice — and it is why every level of the table is itself exactly one page.

---

**Q2.** **Five.** Four to walk the four levels of the page table, plus one for the data itself.

*This is why the TLB exists: at Week 4's DRAM cost of 438 cycles, an uncached walk would make a single `mov` cost thousands of cycles.*

---

**Q3.** **Reach = entries × page size** — the amount of address space the TLB can cover at once.

$64 \times 4\text{ KiB} = \mathbf{256\text{ KiB}}$. *(With 2 MiB pages the same 64 entries reach 128 MiB.)*

---

**Q4.** **Only the number of pages.** The cache footprint was 32 KiB in every case and stayed L1-resident.

**The 22× is pure address translation**: 8 pages fit comfortably in the TLB; 8192 do not, so nearly every access needs an L2 TLB lookup or a page-table walk.

**Cache residency and TLB reach are separate capacities, and you must satisfy both.**

---

**Q5.** **Allocation is a promise, not a delivery.** The kernel recorded a mapping and committed almost no physical memory.

Pages arrive on **first touch**, one minor fault each — *measured: 131 071 faults for 131 072 pages*, at ~1900 ns apiece.

---

**Q6.** **Copy-on-write faults.** After `fork`, parent and child share every frame, and every writable page is marked **read-only in both**. The first write to each page traps; the kernel copies that one frame and marks it writable.

**The R/W bit** is responsible. $256 \text{ MiB} / 4096 = 65\,536$ pages, one fault each.

---

**Q7.** **From the kernel's own VMA** — the `vm_area_struct` describing that region, which records the *logical* permissions.

- VMA says read-only ⇒ genuine violation ⇒ `SIGSEGV`.
- VMA says writable, PTE says read-only ⇒ **copy-on-write**.

**The PTE says what the hardware may do; the VMA says what the program is allowed to do. COW lives in the gap.**

---

### What to Do With Your Score

| If you missed | Reread |
|---|---|
| Q1, Q2 | L19 §3–§4 |
| Q3, Q4 | L20 §1–§2 — **the week's central result** |
| Q5, Q6 | L21 §1 and §3 |
| Q7 | L21 §3, and PS 6 Q2(c) |

**Q4 is the one to be sure of.** It is a genuine addition to Week 4's advice, and Week 11 assumes you can tell a TLB problem from a cache problem.

---

*CS 201 · Week 7 · Quiz 7 · covers Week 6 · ungraded*

# CS 202 · Quiz 6
## Administered: Monday, Week 6 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 5** — page tables, the TLB, demand paging, copy-on-write, physical allocation.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **Lab 5 is tomorrow afternoon, and PS 5 is due Friday.** Q1, Q2 and Q5 are both of them in miniature.

---

**Q1.** Split the 32-bit address `0x00803004` into xv6's page-directory index, page-table index and offset.

&nbsp;

&nbsp;

---

**Q2.** How much memory would a **flat** page table for a 32-bit address space need, with 4 KiB pages and 4-byte entries? Why does xv6's two-level table usually need far less — and when would it need more?

&nbsp;

&nbsp;

---

**Q3.** A context switch loads a new value into `CR3`. **Without PCIDs, what happens to the TLB? With them?**

&nbsp;

&nbsp;

---

**Q4.** Thread A unmaps a page while thread B of the same process is running on another CPU. **What must the kernel do before the unmap is safe, and why can't it simply update B's TLB itself?**

&nbsp;

&nbsp;

---

**Q5.** A program maps a fresh anonymous page, **reads** a byte from it, then **writes** a byte to it. How many page faults does Linux take, and what is the page mapped to after each?

&nbsp;

&nbsp;

---

**Q6.** A shell with 50 MiB of memory forks, and the child immediately calls `exec`. **How much of the parent's memory does Linux copy? How much does xv6 copy?**

&nbsp;

&nbsp;

---

**Q7.** An xv6 program is killed with `trap 14 err 7`. **Give two different mistakes that would produce exactly that**, and one that would produce `err 6` instead.

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** `0x00803004` = `0000 0000 10|00 0000 0011| 0000 0000 0100`. **Directory index 2** (top 10 bits), **table index 3** (next 10), **offset 4**.

---

**Q2.** 2²⁰ entries × 4 bytes = **4 MiB per process.** A two-level table allocates a page table only for **4 MiB regions that contain a mapped page**, so a small program needs a directory and a few tables. **It needs more than flat only when nearly every 4 MiB region holds at least one page** — at worst 1,025 pages, one more than flat.

---

**Q3.** **Without PCIDs, loading `CR3` flushes the TLB** (except global entries): the new process refills it one miss at a time. **With PCIDs, entries are tagged by address space and kept**; the switch just changes which tag is current. Measured in L17: a process switch cost only 1–4% more than a thread switch.

---

**Q4.** **A TLB shootdown**: send an inter-processor interrupt to B's CPU, which flushes the entry itself, and wait for it. **One CPU cannot read or write another CPU's TLB** — it is inside that CPU. Until B's CPU flushes, B could still use the old translation to reach a frame that may be given away.

---

**Q5.** **Two faults.** The read maps **the shared zero page**, read-only. The write faults again, and the page gets **a new zeroed frame of its own**, writable. *(A write with no read first: one fault.)*

---

**Q6.** **Linux copies none of it**: `fork` copies page tables and marks pages read-only; `exec` discards them before anything is written. Only pages written between `fork` and `exec` — typically a few stack pages — are copied. **xv6 copies all 50 MiB** in `copyuvm`, then `exec` throws the copy away.

---

**Q7.** `err 7` = **present, write, user**. Any two of: **writing to the guard page** below the stack (a stack overflow); **writing to a kernel address**; writing to any other present page without `PTE_U` or `PTE_W`. **`err 6`** = not present, write, user: **writing past the end of the process's memory** — beyond `sz`.

---

### What to Do With Your Score

There is no score. Instead, before tomorrow's lab:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L16 §3–§5 — and do PS 5 Q2(b) |
| Q3 | L17 §5 |
| Q4 | L17 §6 |
| **Q5** | **L18 §3 — Lab 5 Part B is exactly this** |
| Q6 | L18 §4–§5 |
| Q7 | L18 §2 |

---

*CS 202 · Week 6 · Quiz 6 · covers Week 5 · ungraded*

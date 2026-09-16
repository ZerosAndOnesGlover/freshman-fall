# CS 202 · Operating Systems
# MIDTERM EXAMINATION 2

**Monday of Week 8 · 18:00–19:15 · VNC 100**
**75 minutes · 100 marks · 12.5% of the course**

---

**Name:** _________________________________ **Student ID:** ___________________ **Section:** ________

---

> **Covers Weeks 4–7**: deadlock; address translation; demand paging and copy-on-write; page
> replacement, working sets and the OOM killer; file systems and the page cache. **Nothing from
> Week 8 is on this paper.**
>
> **Permitted:** one handwritten sheet of A4, one side. **No calculators, no electronic devices.**
> All arithmetic is designed to be done by hand.
>
> **Answer all five questions.** Each is worth 20 marks. **Show your working** — a table with a
> wrong final number earns most of the marks; a bare number earns few.
>
> If a question seems to need something you were not given, **state your assumption and continue.**

---

## Question 1 — Deadlock (20 marks)

**(a) [5]** Name **Coffman's four conditions**. Two threads run this loop:

```c
/* thread one */                     /* thread two */
lock(&A);  lock(&B);                 lock(&B);  lock(&A);
   /* work */                           /* work */
unlock(&B); unlock(&A);              unlock(&A); unlock(&B);
```

**Which single condition is cheapest to remove here, and what is the one-line change?** Say what each of the other three would cost.

**(b) [8]** Four processes share three resource types. **Available = (1, 1, 2).**

| | Allocation | Max |
|---|---|---|
| P0 | 1 0 0 | 3 2 2 |
| P1 | 5 1 1 | 6 1 3 |
| P2 | 2 1 1 | 3 1 4 |
| P3 | 0 0 2 | 4 2 2 |

1. **Compute the Need matrix**, and give **the total of each resource type** in the system.
2. **Is the state safe?** If so, give a safe sequence and the *Work* vector after each step.
3. **P3 requests (1, 1, 0).** Does the Banker grant it? **Show the step of the check that decides.**
4. **Instead, P1 requests (1, 0, 2).** Grant or refuse, with the resulting Available.

**(c) [4]** The deadlock-**detection** algorithm and the Banker's **safety** check differ in exactly two ways. **Name both, and explain what each is for.**

**(d) [3]** A server stops making progress. **Give one observation from `/proc` that distinguishes deadlock from livelock**, and the cheapest fix for each.

---

## Question 2 — Address Translation (20 marks)

**(a) [5]** Split the 32-bit virtual address **`0x00C03004`** into xv6's page-directory index, page-table index and offset. Then say **how many memory accesses** an x86-64 TLB miss costs on this machine, and why.

**(b) [6]** A Linux process touches **64 pages, one in each 2 MiB region**, all inside one gigabyte of address space. **How many page-table pages does that need, at which levels, and how many kilobytes is that?** Then do the same for a process that touches **every page of one contiguous gigabyte**, and explain the difference in one sentence.

**(c) [5]** This CPU's second-level TLB holds **1,536 entries**. **What is its reach with 4 KiB pages, and with 2 MiB pages?** Then: a TLB hit costs 1 ns and a miss 20 ns. **What does translation add per access at a 95% hit rate**, and what hit rate would make translation cost as much as an 8 ns memory access?

**(d) [4]** Thread A calls `munmap` while thread B of the same process runs on another CPU. **What must the kernel do before the unmap is safe, and why can it not be done by A alone?** **Name one case in which Linux skips it**, and say why that is still correct.

---

## Question 3 — Demand Paging and Copy-on-Write (20 marks)

**(a) [5]** A program maps four fresh anonymous pages, then: **reads page 0; writes page 0; writes page 1.** **How many page faults**, and **what is page 0 mapped to after each step**? Why is the page-1 case cheaper?

**(b) [6]** A process with **1 GiB of touched anonymous memory** calls `fork`. Measured on the reference machine: `fork` takes **20 ms**, and a copy-on-write fault costs **2.7 µs**. **How long does the child take if it writes every page?** **How long if it calls `exec` immediately?** **What would the same `fork` cost if the kernel copied eagerly**, and why is the lazy version still better for the writing child?

**(c) [5]** An xv6 process of **4,210,688 bytes** forks, and the free list falls by **1,096 pages**. **Account for all 1,096**, given that xv6 maps the kernel into every process with 64 page tables and a directory, and gives each process a one-page kernel stack.

**(d) [4]** An xv6 program is killed with `trap 14 err 6`, and another with `trap 14 err 7`. **Decode both error codes** and give a distinct programming mistake that produces each.

---

## Question 4 — Replacement and Memory Pressure (20 marks)

**(a) [8]** The reference string is

```
7 0 1 2 0 3 0 4 2 3 0 3
```

**With three frames**, give the **number of page faults** for **FIFO**, **LRU** and **OPT**. Show the frame contents after each reference for **FIFO and LRU** (a table of three rows is fine). *(Loading into an empty frame counts as a fault.)*

**(b) [4]** With **four** frames, FIFO faults **fewer** times on this string. **Does that mean Belady's anomaly cannot occur for FIFO?** Explain, and **prove that LRU can never show it.**

**(c) [4]** A program with 256 MiB of memory is run under a 64 MiB limit. Reading **uniformly at random** it achieves 14,775 reads per second; reading with **90% of accesses in a 32 MiB region** it achieves 166,745. **Both faulted about 44,000 times per four seconds. Explain both numbers**, and say which one the *working set* explains.

**(d) [4]** A machine has **8 GiB of RAM and 4 GiB of swap**. Process A holds **4 GiB** with `oom_score_adj` 0; process B holds **200 MiB** with `oom_score_adj` 500. Badness is ⅔ × (1000 + adj + 1000 × RSS ÷ (RAM + swap)). **Compute both scores. Which is killed, and what would you change to protect it?**

---

## Question 5 — File Systems (20 marks)

**(a) [5]** A file system has **512-byte blocks**, inodes with **12 direct addresses and one indirect block**, and **4-byte** block addresses. **What is the largest file?** **How many blocks does a 20,000-byte file occupy on disk**, counting everything the file system must allocate for it?

**(b) [5]** Nothing is cached. **List the disk reads needed to read the first byte of `/docs/a.txt`**, saying what each is for. **Which one is removed if the file is opened a second time**, and by what?

**(c) [5]** On the reference machine a **cold** random 4 KiB read costs **93.9 µs** and a **warm** one **1.61 µs**. A program reads **10,000 random 4 KiB blocks** of a 512 MiB file, **twice**, on a machine with 8 GiB free. **How long does each pass take?** **What changes if the machine has 200 MiB free**, and why?

**(d) [5]** A service appends **10,000 records**, each one small write. A flush costs **3.9 ms**. **How long does it take with an `fsync` per record, and with one `fsync` per 100 records?** Then: **give the four steps of a crash-safe file replacement**, and say what is lost if the last step is omitted.

---

## Marks

| Question | Topic | Marks |
|---|---|---:|
| 1 | Deadlock | 20 |
| 2 | Address translation | 20 |
| 3 | Demand paging and copy-on-write | 20 |
| 4 | Replacement and memory pressure | 20 |
| 5 | File systems | 20 |
| | **Total** | **100** |

---

**END OF PAPER**

*CS 202 · Midterm 2 · Weeks 4–7 · © CSE Department*

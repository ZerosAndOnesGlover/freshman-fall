# CS 202 · Final Examination — Solutions and Mark Scheme
## **INSTRUCTOR ONLY** · Do not distribute

---

**Wednesday of finals week, 09:00–11:30, VNC 100. 150 minutes, 100 marks, 15%.** Comprehensive, Weeks 0–12.

**Every number in this scheme is produced by `final_check.sh`** in this folder, which runs the Week 4 Banker reference and the Week 6 page-replacement reference on the paper's own inputs, asserts the rest of the arithmetic, **and re-runs the Week 0 `sgdt` result that Q5(c)1 depends on**. **Run it before printing the paper.** All 29 checks must pass.

**Marking principle, as for both midterms:** the working carries the marks. **A correct method with an arithmetic slip loses 1**; a bare answer with no working earns at most half the part. **Orders of magnitude are accepted wherever the paper says so** — a student who writes "about a microsecond" for a system call has the fact the question is testing.

**A general note for this paper.** It is comprehensive, and the most common failure will be **answering a Week 12 question with a Week 12 fact when the question wants a Week 5 one**. Q1 and Q5(c) are deliberately cross-week. **Mark the reasoning, not the vocabulary.**

---

## Question 1 — One Mechanism, Several Times (20)

### (a) [9] — 3 marks per row: 1 interposition, 1 table, 1 cache-and-invalidation

| | Interposition point | Table | Cache, and what invalidates it |
|---|---|---|---|
| **(i)** | **the MMU**, on every load and store — **hardware, so it cannot be skipped** | **the page table** (`%cr3` → the four-level walk) | **the TLB**; invalidated by `invlpg`, by a `%cr3` write, and across CPUs by **a TLB shootdown IPI** |
| **(ii)** | **the `read` system call** and the block layer beneath it | **the inode** and its direct/indirect block pointers | **the page cache**; invalidated by a write from another node, by `POSIX_FADV_DONTNEED`, and by reclaim under memory pressure |
| **(iii)** | **the VM exit** — the CPU leaves guest mode | **the VMCS**, and the **EPT** for guest-physical addresses | **the EPT's own TLB entries**, tagged by VPID; invalidated by `invept`/`invvpid` |

**Give the mark for "the MMU" even without "on every access"** — but the phrase *complete mediation* or *cannot be skipped* earns the benefit of the doubt anywhere else in the question.

**Common wrong answer for (i):** "the page fault". **The page fault is what happens when the check fails**, not the check. **No mark**, but no penalty elsewhere.

### (b) [6]

1. **[2]** 16 MiB = **16,777,216 system calls**; at 1 µs each, **about 16.8 seconds** — accept "about 17 s" or "about 16 s".
2. **[2]** 16 MiB ÷ 64 KiB = **256 system calls**; **about 256 µs**, i.e. **a quarter of a millisecond**.
3. **[2]** **Ratio 65,536×** [1]. **The rule: amortise the crossing — each entry into the kernel has a fixed cost that has nothing to do with how much work you ask for, so ask for more per crossing** [1].

> **The measured version** (L03): the same 16 MiB took **14.213 s** at 1 byte and **0.0022 s** at
> 64 KiB — **6,400×**. **A student who quotes the measured figures instead of computing the
> idealised ones gets full marks**, and deserves a note.

### (c) [5]

**Order [2, all four correct]:**

> **TLB miss (≈ 17 ns) · page fault (≈ 2 µs) · VM exit (≈ 8 µs) · network round trip (≈ 23 ms)**

**The gaps [1 each, three gaps]:**

- **TLB miss → page fault** (~100×): a miss is **a hardware walk of a table that is present**; a fault is **a trap into software** that must allocate a page and update the table. The gap is the cost of involving the kernel at all.
- **Page fault → VM exit** (~4×): both are traps, but the exit **saves and restores a whole virtual CPU's state**, not one thread's.
- **VM exit → network round trip** (~3,000×): the first stays **on this machine**; the second crosses a wire and, more importantly, **puts the answer in the hands of a machine that may never reply** — which is why Week 11 counts round trips and nothing else.

---

## Question 2 — Concurrency and Deadlock (20)

### (a) [6]

**Mutual exclusion, hold and wait, no preemption, circular wait [2, all four].**

**The fix removes circular wait [1]: thread two takes `A` before `B` — a single global lock order [1].**

**`trylock` and retry trades deadlock for livelock [1]**: no thread holds while waiting, so nothing deadlocks, but all threads can repeatedly grab, fail and release in lockstep, making no progress.

**The measurement [1]:** PS 4 Q5 — **back-off was what made the difference**, and with fixed 50 µs back-off the reference reached **1.29M rounds/s at 0.01 failures per round**, while the naive retry loop made progress only by luck. **Accept any reference to the course's back-off measurement.**

### (b) [10]

**1. [3] Need = Max − Allocation:**

| | A | B | C |
|---|---|---|---|
| **P0** | 3 | 2 | 1 |
| **P1** | 1 | 2 | 2 |
| **P2** | 2 | 1 | 2 |
| **P3** | 2 | 1 | 1 |

*(1 mark per two correct rows; all four correct = 3.)*

**2. [4] The state is SAFE.** Work = Available = **(2, 1, 2)**:

| Step | Work | Who can run | Releases | Work after |
|---|---|---|---|---|
| 1 | (2,1,2) | **P2** — Need (2,1,2) ≤ (2,1,2) | (3,0,2) | **(5,1,4)** |
| 2 | (5,1,4) | **P3** — Need (2,1,1) | (0,1,1) | **(5,2,5)** |
| 3 | (5,2,5) | **P0** — Need (3,2,1) | (1,0,2) | **(6,2,7)** |
| 4 | (6,2,7) | **P1** — Need (1,2,2) | (2,1,1) | **(8,3,8)** |

**The reference prints `<P2, P3, P0, P1>`. Any valid sequence earns full marks** — `<P2, P3, P1, P0>` is also safe. **2 marks for a correct working table, 2 for a valid sequence.**

**Note that P2 is the only process that can run first**, which is worth saying in feedback: three of the four Needs exceed Available.

**3. [3] DENIED.** Marks: **1** for "refused", **2** for the reason.

**The reason is the whole point of the question.** The request **is** satisfiable — (2,1,0) ≤ Available (2,1,2) — so a naive allocator would grant it. **Pretend to grant it**: Available becomes (0,0,2), P0's Need becomes (1,1,1). Now **no process can run**: P0 needs (1,1,1), P1 (1,2,2), P2 (2,1,2), P3 (2,1,1), and none is ≤ (0,0,2). **The state would be unsafe, so the Banker's algorithm refuses a request it could satisfy.**

**A student who answers "denied because not enough available" has the right verdict and the wrong reason: 1 of 3.**

### (c) [4]

**Both are true because "safe" is not a statement about what is available now [1].** It is a statement that **there exists an order in which every process can finish** — and after P2's request is granted, P2 holds exactly its Max, so **P2 can run to completion with nothing further** and then releases (5,1,4), which is enough for everyone else. **Availability of zero is irrelevant if some process needs nothing more.** [2]

**The assumption [1]:** **every process declares its Max in advance and will release everything it holds within a finite time.** Neither is true of real programs, which is why no operating system runs the Banker's algorithm.

---

## Question 3 — Memory (20)

### (a) [10]

**1. [6] — 1 mark per cell.**

| Frames | FIFO | LRU | OPT |
|---|---|---|---|
| **3** | **15** | **12** | **9** |
| **4** | **10** | **8** | **8** |

*(20 references, 6 distinct pages. Compulsory misses are 6 and are included.)*

**2. [2] LRU and OPT tie at 4 frames, both at 8 [1].** With four frames and six distinct pages, **the string's reuse distance is almost always within four** — LRU's guess about the future (the past) is right nearly every time. **The gap between LRU and OPT is a measure of how surprising the string is, and at 4 frames this one is not surprising.** [1]

**3. [2] Belady's anomaly: for FIFO, more frames can cause *more* faults [1]** — the algorithm is not a stack algorithm, so the set of pages resident with *n* frames is not necessarily a subset of the set with *n*+1.

**To show it you need a different string [1].** The course's is `1 2 3 4 1 2 5 1 2 3 4 5`: **FIFO 3 frames = 9 faults, FIFO 4 frames = 10.** **Accept any correct anomaly string, or a correct description of the property one must have.**

### (b) [5]

**1. [3]** **4 KiB × 1,536 = 6 MiB [1]. 2 MiB × 1,536 = 3 GiB [1].** The point [1]: with 4 KiB pages the TLB covers **0.3%** of a 2 GiB working set; with 2 MiB pages it covers **all of it**.

**2. [2]** **At 4 MiB the working set nearly fits the 4 KiB reach** (6 MiB), so almost every access hits the TLB and there is nothing for huge pages to save — the course measured a gap of **1.6 ns**. **At 2 GiB, essentially every access misses**, and each miss is a multi-level walk whose own lines are also out of cache — measured at **17.3 ns**. **The cost of a mechanism is zero until the working set leaves the cache, and then it is the whole cost.**

### (c) [5]

**1. [3]** Throughput collapses — the course measured **21.7M reads/s unrestricted against 14,775/s at 64 MiB**, a factor of about **1,500**. **The collapse is abrupt [1] because the replaced page is the one about to be used [1]:** once the working set does not fit, each fault evicts a page needed shortly after, so **faults cause faults**. The system spends its time in the fault path and the disk, not in the program. **The knee is where the working set stops fitting, not where memory runs out** [1].

**2. [2] The two inputs: the process's memory footprint (RSS and swap, as a fraction of the total) and `oom_score_adj` [1].** **The administrator controls `oom_score_adj` [1]** — and the measured exchange rate on this machine was about **⅔ of a point per point of `adj`, against 6.7 points per 1% of RAM+swap**, so the knob is weak unless it is used at its extremes.

---

## Question 4 — Storage and Crash Consistency (20)

### (a) [8]

**1. [2]** 12 + 128 = **140 blocks** = **71,680 bytes** *(70 KiB)*. **1 for the block count, 1 for the bytes.**

**2. [3]** 11 + 128 + 128×128 = 11 + 128 + 16,384 = **16,523 data blocks** = **8,459,776 bytes** *(about 8.06 MiB)*.

**"Account for every block" [1 of the 3]:** the data above, **plus metadata: 1 indirect block + 1 double-indirect block + 128 second-level indirect blocks = 130 pointer blocks.** A maximal file therefore occupies **16,653 blocks** on disk.

**3. [3]** Inodes are packed into blocks — **`IPB = BSIZE / sizeof(struct dinode)` [1]**. Change the inode's size and `IPB` changes, so **the block containing inode *i* changes** and **every existing inode number now points at the wrong place** [1]: the file system is not merely incompatible, it is silently misread. And if the size no longer divides `BSIZE` evenly, **inodes straddle block boundaries** [1] — a read of one inode becomes two block reads, and `ialloc`'s arithmetic is wrong.

**Project 2's marking note applies here too:** a student who kept `NDIRECT = 12` and grew the inode gets **8,460,288 bytes**. **That is a different design, not an error — full marks if they say what it costs.**

### (b) [7]

**1. [3]** **Any order that writes the metadata before the data [1]**, e.g. **bitmap → inode → data**: a crash after the inode is written leaves **an inode pointing at a block whose contents are whatever was there before** [1].

**The worst inconsistency [1]: the file now contains someone else's deleted data** — a security failure, not merely a corrupt file. *(Accept also: bitmap says free while the inode points at the block, so the block is handed to a second file and two files share it — accept either, with the reason.)*

**2. [4]**
- **The rule [1]: the journal entry must be durable before the in-place write begins**, and the commit record must be durable before any of the transaction is applied — **write-ahead logging**.
- **The barrier [1]: `fsync`, and beneath it `FUA`/`FLUSH` to the device** — without a flush the drive's own cache reorders the writes and the rule is violated invisibly.
- **The steady-state cost [1]: every metadata block is written twice** (once to the journal, once in place); with `data=ordered` the data is written once, before the commit. The course measured the overlay/journal write path at **+21%** for scattered 4 KiB writes.
- **What `fsync` promises [1]: that the data and the metadata needed to find it have reached durable storage** — not that the directory entry is durable (that needs an `fsync` of the directory), and not that a drive lying about its cache has been caught.

### (c) [5]

**The experiment [3]:** run the operation under a harness that **interrupts it at a chosen point** — the course used a sweep over the number of block writes allowed before the device is cut off — **for every point from 0 to the end of the operation** [1], then **mount and check the file system** at each point [1], **varying the point across the whole range and checking the checker sees the whole invariant** [1].

**One way it reports success when the file system is broken [2]** — *any one of the course's three, all of which actually happened:*

- **The sweep covered a range the operation never reached**, so every crash point was before anything was written, and all of them passed.
- **`|| true` swallowed the checker's exit status**, so the harness reported zero failures regardless of what the checker found.
- **The checker was too weak** — it verified the file's contents but not the allocation bitmap, so **orphaned inodes and doubly-allocated blocks passed**.

**Full marks for any one of these, stated concretely.** **2 marks for naming a specific failure mode, 1 for "the checker might be wrong" alone.**

---

## Question 5 — Distribution and Protection (20)

### (a) [7]

**1. [2]** **3 of 5 [1]; tolerates 2 failures [1].**

**2. [2]** **Majority of 6 is 4 [1]; still tolerates 2 [1].** **The comment earns nothing extra but should be there:** adding a sixth node buys **no more fault tolerance** and makes every decision need one more vote — **even-sized clusters are strictly worse than the odd size below them.**

**3. [3]** **The majority side (3) elects a leader in a new, higher term and continues to commit [1]. The minority side (2) cannot reach 3 votes**, so its candidates time out and retry, incrementing their terms without ever winning [1].

**The old leader on the minority side may still believe it is leader** — so **there can be two leaders in the cluster at once** — **but never two in the same term, and only the majority side can commit anything** [1]. Raft's safety property is about **a term**, not about the wall clock.

**On healing:** the old leader sees a message carrying **a higher term** and **immediately steps down to follower.** The course's simulation measured this: **two leaders for 756 ticks, and the old leader stepped down 47 ticks after the heal.**

### (b) [6]

**1. [2]** Any coherent three lines, e.g. **protecting** the integrity of the machine and the confidentiality of my other files; **from** a program I ran, which has my full authority and has read the source of everything; **out of scope** physical access, an already-root attacker, and the firmware. **1 mark for naming an asset and an adversary, 1 for an explicit out-of-scope line** — the last is the one students omit, and it is the one that makes a model usable.

**2. [2]** *Any two, 1 each:* **read every file I can read** (it runs as my uid, and the filter permits `openat` because the loader needs it and **seccomp cannot inspect a path** — it sees only integers); **send my data anywhere** if the policy allows the network; **consume CPU up to the limit**; **observe timing side channels**, which no limit or filter touches; **exploit `gather_data_sampling`**, which this machine reports as **Vulnerable**.

**3. [2]** **No [1].** **The comparison that settles it [1]: 50 ns against a system call that costs about 840 ns on this machine — about 6%** — and against the alternative, which is a program with the full system call table available to it. **Accept any answer that puts the 50 ns next to a measured cost rather than treating it as large in isolation.**

### (c) [7]

**This question is Habit 1, and it is the one to read carefully rather than quickly.**

**1. [2]** **Run the instruction** — a three-line program executing `sgdt` (or `sidt`/`smsw`/`str`) in user mode [1]. **The claim is false if it succeeds and prints a non-zero kernel address** [1].

**The claim is false on this machine, and the cause is not the kernel:** the kernel *is* built with `CONFIG_X86_UMIP=y`, and **the CPU does not implement UMIP**, so the option does nothing. `final_check.sh` re-runs this. **A student who says "check `/boot/config-*`" has answered the wrong question — that confirms the configuration, which was never in doubt: no marks for the second mark, 1 for effort.**

**2. [2]** **Time a cheap system call with a short filter and with a long one, in the same process, with a control** [1]. **The claim is false if the two are the same** — which is what the course measured: **about +50 ns for 6 instructions and for 205, and the same for five stacked filters, because the cost is the check and not the rules** [1].

**3. [3]** **Run something that forks under the limit and count the children** [1] — `ps -u "$(id -u)" --no-headers | wc -l` alongside it is the evidence [1].

**The claim is false if the job fails at zero children**, which is what happens on this machine: **`RLIMIT_NPROC` counts every process of the real user ID, not the jail's**, and this account already has 134 processes and 1,068 threads, so a limit of 40 — or of 700 — is already exceeded before the job starts [1]. **The mechanism that does work is a cgroup's `pids.max`**, measured at exactly 19 children under a limit of 20.

**Award the third mark for identifying that the limit's *scope* is the user, however it is phrased.**

---

## Mark Distribution

| Q | Topic | Marks | Weeks |
|---|---|---:|---|
| 1 | One mechanism, several times | 20 | 0, 3, 5, 7, 10, 11 |
| 2 | Concurrency and deadlock | 20 | 2–4 |
| 3 | Memory | 20 | 5–6 |
| 4 | Storage and crash consistency | 20 | 7–8 |
| 5 | Distribution and protection | 20 | 11–12 |
| | **Total** | **100** | |

**Weeks 1 and 9 are not the subject of a question** — Week 1's context switch appears in Q1(c)'s price list and Week 9's device costs in Q1(a)(ii)'s block layer. **This was a deliberate choice and should be stated if a student asks**: the paper covers the mechanisms that generalise, not every week equally.

**If the cohort's Q5(c) marks are poor, that is worth knowing and not worth apologising for.** It is the only question on the paper that cannot be revised for by memorising, and it is the one the course was built to teach.

---

*CS 202 · Week 12 · Final Examination · Instructor Only*

# CS 201 · Quiz 8
## Administered: Monday, Week 8 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 7** — the I/O path, disks and SSDs, storage performance and scheduling.

**Instructions:** Closed notes. 10 minutes.

> **Unmarked, no weight.** Key below. Sit it closed-book first.

---

**Q1.** Give the three components of a rotating-disk access. Which dominates for a 4 KiB read?

&nbsp;

&nbsp;

---

**Q2.** Why can flash not overwrite a page in place? Name the two units involved.

&nbsp;

&nbsp;

---

**Q3.** Sequential SSD throughput rose 18× from 4 KiB to 1 MiB blocks. What was limiting the small-block case?

&nbsp;

&nbsp;

---

**Q4.** Cached 4 KiB reads ran at 2.51 μs; `O_DIRECT` reads at 157.6 μs. What is the only difference?

&nbsp;

&nbsp;

---

**Q5.** A 4 KiB write costs 6 μs; the same write plus `fsync` costs 3876 μs. What is `fsync` doing, and what does a database do about it?

&nbsp;

&nbsp;

---

**Q6.** State Little's Law. Why does a single-threaded storage benchmark understate a device?

&nbsp;

&nbsp;

---

**Q7.** `cat /sys/block/nvme0n1/queue/scheduler` prints `[none]`. Why is doing no scheduling correct here?

&nbsp;

&nbsp;

---

<div style="page-break-after: always;"></div>

---

## Answer Key — Mark Your Own

**Q1.** **Seek time, rotational latency, transfer time.**

For 4 KiB on a 7200 rpm drive with a 9 ms seek: 9 + 4.17 + 0.027 ms. **Seek dominates**, and transfer is about **0.21%** of the total — one part in five hundred spent actually moving data.

---

**Q2.** **A page can only be programmed if it has been erased, and erase operates on a whole block.**

**Page** 4–16 KiB (read/program); **erase block** 128–256 pages, 1–4 MiB (erase). Overwriting one page in place would mean reading, erasing and rewriting the entire surrounding block — so the **FTL** writes elsewhere and remaps instead.

---

**Q3.** **Per-request software overhead**, not the device — the system call, block layer, NVMe submission and completion interrupt are a fixed cost per request regardless of size.

**If the device were the limit, the curve would be flat.**

---

**Q4.** **Whether the data was already in DRAM.** The first is a page-cache hit; the second bypasses the cache and goes to the device. **63×**, and the code is otherwise identical.

*The cached figure sits just above Week 6's minor page fault at 1.9 μs — both are dominated by the syscall path, not by hardware.*

---

**Q5.** **`fsync` forces the kernel's dirty page-cache pages for that file out to the device**, and waits. Without it, a successful `write()` means only that the data reached DRAM.

**645×.** A database committing 10 000 transactions/second has a 100 μs budget each; one `fsync` is 3900 μs — 39× the budget. **The answer is group commit**: many transactions share a single `fsync`, trading latency for throughput.

---

**Q6.** **Concurrency = throughput × latency.**

A single thread holds concurrency near 1, so it can only ever measure $1/\text{latency}$ operations per second. **An NVMe drive with dozens of flash channels needs many outstanding requests to show its capability** — a one-thread benchmark measures latency and reports it as though it were throughput.

---

**Q7.** **There is no arm to optimise.** Reordering exists to minimise head movement, and flash has none. Beyond that, the drive's controller knows its own internal parallelism far better than the kernel does, and kernel reordering would add latency while breaking the sequentiality the FTL prefers.

*`mq-deadline` remains the right choice for a rotating disk, where head position dominates and reordering is worth an order of magnitude.*

---

### What to Do With Your Score

| If you missed | Reread |
|---|---|
| Q1, Q2 | L23 §1–§2 |
| Q3, Q6 | L23 §3, L24 §1 |
| **Q4, Q5** | **L22 §5 — the two numbers of the week** |
| Q7 | L24 §4 |

**Q4 and Q5 are the ones that recur.** Week 11 assumes you will ask "device or cache?" before optimising anything that touches storage.

---

*CS 201 · Week 8 · Quiz 8 · covers Week 7 · ungraded*

# CS 201 · Midterm 2 Revision Guide
## Weeks 5–9 · 75 minutes · 100 points · 12.5%

---

**Week 10, Monday, 18:00–19:15, VNC 100.**
**One handwritten A4 sheet, one side.** No calculator, no devices.

---

## What Is Examined

Five questions, one per week, evenly weighted at 20 each:

| | Week | Topic |
|---|---|---|
| Q1 | 5 | Pipelining, ILP, SIMD, Amdahl |
| Q2 | 6 | Virtual memory, TLB, paging, COW |
| Q3 | 7 | Storage, the page cache, `fsync` |
| Q4 | 8 | Networks, TCP, round trips |
| Q5 | 9 | Security, overflows, defenses |

**This is not a redo of Midterm 1.** Weeks 0–4 are assumed but not the subject — you will still need the stack frame (Q5), the cache line (Q2, Q3) and Amdahl (Q1), so do not forget them.

**About half the marks are "explain why".** The other half are small calculations with definite answers. Practise both.

---

## The Numbers Worth Memorising

Every one of these was *measured* in a lab or lecture, and the paper is built from them. Put the ones you cannot re-derive on your sheet.

| Fact | Value |
|---|---|
| Independent chains vs one | **4.00×** (latency → throughput) |
| AVX2 in-cache vs out | **4.51× → 1.07×** |
| TLB reach, 64 entries × 4 KiB | **256 KiB** |
| Same L1 data, 8 vs 8192 pages | **1.24 → 27.57 ns** |
| Minor page fault | **~6 200 cycles** |
| Page cache vs device (4 KiB) | **63×** (2.5 μs vs 157 μs) |
| `fsync` vs plain write | **645×** (3876 μs vs 6 μs) |
| Internet RTT / HTTPS page | **187 ms / 589 ms** |
| Nagle deadlock | **41 ms** (delayed-ACK timer) |
| libc `ret` gadgets | **~6 100** |

---

## The Six Ideas the Paper Rewards

**Every "why" question is one of these.** If you can state all six cold, you can answer most of the paper.

1. **Latency-bound vs throughput-bound.** One dependency chain hits latency; independent work hits throughput. (Q1)
2. **A fixed per-operation cost is amortised by operation size.** Cache lines, storage blocks, network messages — same shape three times. (Q1, Q3, Q4)
3. **Cache residency and TLB reach are separate capacities.** Data in L1 can still be slow. (Q2)
4. **Allocation is a promise; the page cache hides the device; `fsync` forces the truth.** (Q2, Q3)
5. **Every network optimisation removes a round trip; only a CDN shortens one.** (Q4)
6. **Defenses layer, and each motivated the next attack.** NX → ROP → CFI. (Q5)

---

## The Traps

Errors that recurred across five weeks of problem sets:

**Optimising the D1 miss rate.** An L1 miss served by L2 costs ~12 cycles; by DRAM, ~438. *Which level is missing* is the question, not how many. (Q1/Q3 territory)

**"Undefined behaviour means it wraps."** It means the compiler may assume it never happens — and delete your check. (Q5)

**Counting pages as though they were cache lines, or vice versa.** They are different capacities with different sizes. (Q2)

**Confusing coherence with consistency, or flow control with congestion control.** Per-location agreement vs cross-location ordering; receiver protection vs network protection. (Q1/Q4)

**"CET is on because `endbr64` is there."** Compiled in ≠ enforced. (Q5)

**Blaming Nagle alone for the 41 ms.** The 41 ms is the *other* side's delayed-ACK timer. (Q4)

---

## Worked Example — a full-mark answer

> **Q. Cached reads ran at 2.5 μs and `O_DIRECT` reads at 157 μs. What is the only difference?**

**Bare answer** *(≈1 of 4)*: "One uses the cache and one doesn't."

**Full-mark answer** *(4 of 4)*:

> Both issue the same 4 KiB read. The buffered read checks the **page cache** first and finds the
> data already in DRAM from a previous access, so it never touches the device — a DRAM-speed
> operation dominated by the system-call path, which is why it lands near the minor-page-fault cost
> of ~1.9 μs. The `O_DIRECT` read bypasses the page cache by design and goes to the SSD, paying the
> device's ~157 μs latency. **The only difference is whether the data was already resident in DRAM;
> the 63× is the gap between DRAM and the device.**

**What earns the marks:** naming the page cache, connecting it to the earlier latency ladder, and stating the cause of the gap — not just "cache is faster".

---

## A Revision Plan

**One week:**

| Day | Do |
|---|---|
| 1 | Re-read the five [[CS201 Week10/summary\|summary]] files (Weeks 5–9). Build your sheet from memory |
| 2 | Redo PS 5 (hazards, Amdahl) and PS 6 Q1 (translation) |
| 3 | Redo PS 7 Q4–Q5 (storage numbers) and PS 8 Q4 (Nagle) |
| 4 | Redo PS 9 Q1–Q2 (overflow, arms race) |
| 5 | The five quizzes (5–9), closed-book, 10 minutes each |
| 6 | The "six ideas" and "the numbers", cold |
| 7 | Light. Re-read your sheet. Sleep |

**Two days:** the five quizzes; the six ideas; the numbers table; and one calculation from each of Q1(e), Q3(e), Q4(e) — the Amdahl, `fsync` and Little's Law arithmetic, which are the most predictable marks on the paper.

---

## During the Exam

**Read all five questions first.** Each is 20 marks — do not overspend on your strongest.

**The calculations are free marks: Q1(e) Amdahl, Q3(e) `fsync` throughput, Q4(e) Little's Law.** Do them first and bank them.

**Show working.** A method with a slip keeps most marks; a bare number keeps none.

**"Explain in one sentence" means one.** Padding wastes the time you need for the calculations.

---

## What the Exam Is Testing

Not recall of numbers — the numbers are on your sheet. **Whether you can look at a measured result and say what the machine was doing to produce it.** Every question started as something measured in a lab. If you understood *why* each number came out as it did, the revision is mostly done.

---

*CS 201 · Midterm 2 Revision Guide · Weeks 5–9*

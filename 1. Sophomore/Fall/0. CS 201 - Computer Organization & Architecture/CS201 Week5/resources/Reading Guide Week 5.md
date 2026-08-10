# CS 201 · Week 5 · Reading Guide
## CS:APP Chapters 4 and 5 — Pipelining and Optimisation

---

**Set reading:** **§4.4–4.5** (pipelining) and **§5.7–5.10** (ILP, branches, SIMD). **§1.9.1** for Amdahl.
**Skip for now:** §4.1–4.3, the Y86-64 instruction set. It is a teaching ISA, and this course reads real x86-64.

---

## How to Read Chapter 4 in a Midterm Week

**Chapter 4 builds a pipelined processor from scratch in HCL.** That is a semester's work in ECE 311, and it is not what this week needs.

**Read §4.4 and §4.5 for the concepts** — stages, hazards, forwarding, prediction — and **skip the HCL implementation entirely**. If you find yourself reading logic equations, you have gone too far.

**Chapter 5 is the one that pays off.** §5.7 onward is written for programmers and connects directly to Lab 5.

---

## Section by Section

| § | Topic | What to take from it |
|---|---|---|
| **4.4** | General principles of pipelining | Latency against throughput. Why deeper is not automatically better |
| **4.5.1–4.5.3** | Hazards | The three classes. This is L16 §3 |
| **4.5.4** | Avoiding data hazards by forwarding | **The core idea.** Where a result becomes available |
| **4.5.5** | Load/use hazards and stalling | Why forwarding cannot fix this one |
| **4.5.6** | Exception handling | Skim — but note *why* it is hard once instructions execute out of order |
| **4.5.7–4.5.8** | Implementation | Skip unless curious |
| **5.7** | **Understanding modern processors** | Functional units, issue, latency vs throughput tables |
| **5.7.2** | **The latency/throughput bound** | Read carefully — this is L16 §5's 4.00× |
| **5.8** | Loop unrolling | Why it helps, and where it stops helping |
| **5.9** | **Multiple accumulators** | **This is Lab 5 Part 1.** The book measures the same effect |
| **5.10** | SIMD | The book uses intrinsics too |
| **1.9.1** | Amdahl's Law | Two pages, and one of the most quoted results in the field |

---

## Questions to Read Against

**On §4.4–4.5**

1. A 5-stage pipeline gives ~5× throughput. What stops a 50-stage pipeline giving 50×? Name two costs.
2. Explain why WAR and WAW hazards vanish under register renaming while RAW does not.
3. §4.5.5 gives the load/use hazard one stall cycle even with full forwarding. **Why can forwarding not eliminate it**, when it eliminates the ALU-to-ALU case entirely?
4. Exceptions become difficult once instructions complete out of order. What has to be true for the machine to report a *precise* exception?

**On §5.7 — the most useful section**

5. The book distinguishes **latency bound** from **throughput bound**. State each, and say which one a single accumulator chain hits.
6. Find the latency and issue figures for floating-point add and multiply in the book's tables. **Then predict Lab 5 Part 1's 4.00×** before doing the lab.
7. §5.7 describes register renaming and the reorder buffer. **Why must retirement be in order when execution is not?**

**On §5.8–5.9**

8. The book unrolls a loop and gets a modest gain, then adds multiple accumulators and gets a large one. **Which of the two is doing the work, and why?**
9. At what number of accumulators does the book's improvement stop? Relate that to the machine's issue width.

**On §5.10 and §1.9.1**

10. Why will a reduction not auto-vectorise without `-ffast-math`? Connect this to Week 1 §L06.
11. A program is 95% parallelisable. Compute the maximum speedup, then the speedup on 8 cores. Comment on the gap.
12. **State Gustafson's objection to Amdahl in one sentence**, and give a case where each framing is the more useful one.

> **Question 8 is the one that matters.** Students routinely credit unrolling for gains that actually
> came from breaking the dependency chain. The book's own data separates them.

---

## Reading Against the Machine

```bash
# 1. Latency vs throughput, in twenty lines — Lab 5 Part 1
#    Predict the ratio from the book's latency tables BEFORE measuring.

# 2. Does your loop vectorise, and if not, why not?
gcc -O3 -mavx2 -fopt-info-vec-missed -c yourfile.c

# 3. Did the compiler already remove your branch?
objdump -d -M intel prog | grep -E "cmov|jle|jg"
```

**Item 3 is the week's methodological point.** The famous sorted-vs-unsorted branch demonstration **no longer reproduces at default optimisation** — GCC emits `cmovg` and the ratio is 1.02× instead of 8×. **A benchmark that measures nothing is usually measuring the wrong thing**, and the disassembly is how you find out which.

---

## Terminology You Should Own by Week 6

| | | |
|---|---|---|
| latency vs throughput | pipeline stage | pipeline register |
| structural hazard | data hazard | control hazard |
| RAW / WAR / WAW | forwarding / bypassing | load-use hazard |
| stall / bubble | branch prediction | 2-bit saturating counter |
| misprediction penalty | speculation | return-address stack |
| register renaming | reservation station | reorder buffer |
| in-order retirement | superscalar | issue width |
| SIMD / vectorisation | intrinsics | horizontal sum |
| Amdahl's Law | serial fraction | compute-bound / memory-bound |

---

## If You Want More

**Agner Fog's instruction tables** give latency, throughput and port assignment for every instruction on every microarchitecture. **This is where "`addsd` is 4 cycles" comes from.** Look up one instruction now so you know how; Week 11 will need it.

**Modern Microprocessors: A 90-Minute Guide** (Jason Robert Carey Patterson) is the best short account of how a modern CPU is put together — pipelining, superscalar, out-of-order and SMT — and it is genuinely 90 minutes.

**The Spectre and Meltdown papers** (2018) are readable and are L17 §6 in full. **Read the Spectre abstract and §1 at least** — they are the clearest demonstration in the field's history that a performance mechanism can be a security boundary.

---

*CS 201 · Week 5 · Reading Guide*

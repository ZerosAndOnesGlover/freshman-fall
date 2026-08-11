# CS 201 · Final Exam · Revision Guide
## Covering Weeks 0–12 — comprehensive

---

## The Exam

| | |
|---|---|
| **When** | Finals week |
| **Duration** | **150 minutes** |
| **Covers** | **Weeks 0–12 — comprehensive** |
| **Weight** | **20%** of the course |
| **Total** | 100 points |
| **Allowed** | **Two handwritten pages** (both sides). No calculator, no devices. |

**Weighting.** Roughly: foundations and assembly (Weeks 0–3) a quarter; the memory hierarchy and performance (4–5, 11) a third; systems (6–8) a quarter; security and parallelism (9–10) the rest; frontiers (12) a few marks of synthesis. **Both midterms' material is examinable again** — this is comprehensive, not a third midterm.

**Character.** Half *do it* (decode an instruction, trace a frame, compute a miss rate, apply Amdahl), half *explain why* (why is this slow, why does this defense work, why did this benchmark lie). **A number with no working, or a claim with no mechanism, loses marks.** This has been true all term and is true here.

---

## The Two Pages — What to Put on Them

You get more space than the midterms (two pages, both sides). **Spend it on the things you re-derive wrongly under pressure, not on what you understand.**

**The latency ladder** — the single most useful thing to have written down:

| Event | ≈ cycles |
|---|---:|
| L1 / L2 / L3 hit | 4 / 12 / 41 |
| DRAM | 438 |
| Minor page fault | 6 200 |
| SSD 4 KiB read | 500 000 |
| `fsync` | 12 500 000 |
| Internet round trip | 600 000 000 |

**The formulas:** Amdahl $S = 1/((1-p)+p/s)$; cache capacity $S{\times}E{\times}B$; same-set stride $S{\times}B$; arithmetic intensity = flop/byte; Little's Law concurrency = throughput × latency; page-table index $\log_2(\text{page}/\text{entry}) = 9$.

**The register/ABI table** — six argument registers, caller/callee-saved split, alignment parity.

**IEEE 754 layout** — 1/8/23, bias 127, implicit leading 1, the reserved exponents.

**The signed/unsigned jumps** — `jl`/`jb`, `jg`/`ja`.

---

## The Topic Checklist

Tick each only when you can *do* it, not just recognise it.

**Weeks 0–3 — foundations and assembly**
- [ ] Decode a relative branch by hand (target from the *next* instruction).
- [ ] Dissect and reconstruct an IEEE 754 value.
- [ ] Explain why `x+1>x` compiles to `1` (signed UB) but not (unsigned).
- [ ] Read any addressing mode; know `lea` computes, does not load.
- [ ] Explain `cdq`, and why `x/8 ≠ x>>3`.
- [ ] Draw a stack frame; know 24 bytes reach the return address from a `buf[16]`.
- [ ] The alignment parity rule: each push flips it.

**Weeks 4–5, 11 — memory and performance**
- [ ] Compute cache capacity, split an address, find the same-set stride.
- [ ] Classify a miss (compulsory/capacity/conflict) and pick the fix.
- [ ] Explain 30× from loop order; **read D1 vs LLd miss rates and say which level.**
- [ ] Latency- vs throughput-bound; four accumulators = 4.00×.
- [ ] Amdahl as a budget; arithmetic intensity and the roofline.
- [ ] The method: measure → profile → diagnose → bound → fix → re-measure.

**Weeks 6–8 — systems**
- [ ] Translate an address (four 9-bit indices); why 9 bits.
- [ ] TLB reach = entries × page size; cache residency ≠ TLB reach.
- [ ] Demand paging (allocation is a promise); COW (the R/W bit).
- [ ] Disk = seek+rotation+transfer; flash and the FTL.
- [ ] Page cache vs device (63×); `fsync` (645×) and group commit.
- [ ] TCP: handshake, `TIME-WAIT`, byte stream / framing.
- [ ] Nagle + delayed ACK deadlock (41 ms); Little's Law on a server.

**Weeks 9–10, 12 — security, parallelism, frontiers**
- [ ] Buffer overflow, canary (`fs:0x28`), NX, ASLR — what each denies.
- [ ] ROP and why NX did not stop it; CET (compiled ≠ enforced).
- [ ] Integer-overflow allocation and the fix; format-string leak.
- [ ] MESI; why a shared counter scales negatively.
- [ ] False sharing (the 64-byte line); physical cores vs hyperthreads.
- [ ] Coherence vs consistency; SIMT, divergence, arithmetic intensity.
- [ ] RISC-V vs CISC; the generality-efficiency axis.

---

## The Six Ideas That Answer Most "Why" Questions

From L38 §4 — if you can state these cold, you can reason through most of the paper:

1. **Data movement is the bottleneck, not computation.**
2. **A fixed per-operation cost makes operation size the dominant variable.**
3. **The compiler runs equivalent code, not your code.**
4. **Know your bottleneck before you act** — which level, which resource.
5. **Every abstraction is a contract with a cost.**
6. **A benchmark is wrong until it survives the checklist** — and cross-checks against a model.

---

## A Revision Plan

**Two weeks:**

| Days | Do |
|---|---|
| 1–2 | Re-read all thirteen `summary.md` files. Build your two pages from memory |
| 3–4 | Weeks 0–3: redo PS 0–3 by hand, timed. Decode, dissect, trace a frame |
| 5–6 | Weeks 4–5, 11: the cache/roofline/profiling arc — PS 4, 5, 11 |
| 7–8 | Weeks 6–8: translation, storage numbers, TCP — PS 6, 7, 8 |
| 9–10 | Weeks 9–10: security and parallelism — PS 9, 10 |
| 11 | Both midterm papers, closed-book, full time |
| 12 | The eleven quizzes, ten minutes each |
| 13 | The six ideas and the latency ladder, cold |
| 14 | Light. Re-read your pages. Sleep |

**One week:** the two midterm papers under exam conditions; the six ideas; the latency ladder; and the checklist above, doing every item you cannot do without notes.

---

## During the Exam

**Read the whole paper first.** 150 minutes is generous but not infinite; know where the marks are before you start.

**Bank the calculations early** — Amdahl, cache geometry, Little's Law, miss rates, a branch target. They are the most certain marks and the least tiring.

**Show working.** A method with a slip keeps most marks. A bare number keeps none. This has not changed since Week 0.

**"Explain why" means the mechanism**, in a sentence or two. Not "it is faster" — *why* it is faster, in terms of what the machine does.

**If stuck, write what you know.** Partial mechanism earns partial marks. "This is memory-bound because its arithmetic intensity is low" is worth marks even if the arithmetic that follows goes wrong.

---

## What the Exam Is Really Testing

Whether you can look at a program, or a measured result, and **say what the machine is doing** — at whichever layer the question asks about. Every question descends from something the course measured. **If you understood why each number came out as it did, you have already done most of the revision.**

The machine is not a mystery any more. The exam is where you show it.

---

*CS 201 · Final Exam Revision Guide · Weeks 0–12*

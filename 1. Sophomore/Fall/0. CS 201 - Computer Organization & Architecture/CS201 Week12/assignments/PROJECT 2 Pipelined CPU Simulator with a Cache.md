# CS 201 · Project 2
## A Pipelined CPU Simulator with a Cache

---

**Assigned:** Week 10 · **Due:** Week 12 (completion period), Friday 17:00
**Weight: 10% of the course grade** · Individual work
**Submit:** a `.zip` of source plus a PDF report, `PROJ2_{LastName}_{StudentID}.pdf`
**Demo:** in the Week 12 lab session (Lab 12 — demo day)

> **This extends Project 1.** You built a *functional* simulator that gets the answers right; Project 2
> adds a *pipeline* that gets the *timing* right, and a *cache* that makes the timing realistic. **If
> your Project 1 kept decode separate from execute, as the spec urged, this is an extension; if it
> fused them, budget time to refactor.**

---

## What You Are Building

Project 1 answered *what* the machine computes. **Project 2 answers *how long* it takes** — by modelling the two mechanisms this course spent the most time on: the **pipeline** (Week 5) and the **cache** (Week 4).

**Cycle-accurate, not just functional.** Your simulator must report, for a given program, **how many cycles it takes** — and that number must reflect pipeline hazards and cache misses, not just the instruction count. **A simulator that runs the program correctly but reports one cycle per instruction has done the Project 1 half and none of the Project 2 half.**

---

## Required Functionality

### 1. The five-stage pipeline

Model **Fetch, Decode, Execute, Memory, Writeback** (Week 5 §L16) as distinct stages, with instructions in flight simultaneously.

- **Track each instruction through all five stages**, one stage per cycle in the ideal case.
- **Report total cycles and IPC** (instructions per cycle) for a program.
- In the absence of hazards, a stream of *N* independent instructions should complete in roughly *N + 4* cycles, not *5N* — **demonstrate this**; it is the whole point of pipelining.

### 2. Hazards

The pipeline must **stall correctly** (Week 5 §L16):

- **Data hazards (RAW):** an instruction needing a result not yet written. Implement **forwarding** where the result is available (ALU→ALU, no stall) and **stall** for the load-use hazard (one bubble).
- **Control hazards:** a branch whose target is unknown at fetch. Model a simple predictor (static "backward-taken", or a 2-bit counter) and a **misprediction penalty** (flush the wrong-path instructions — a few cycles).
- **Report hazard statistics:** stalls by cause, and branch mispredictions.

### 3. The cache (Week 4)

The Memory stage must go through a **configurable cache**, not straight to memory:

```
--cache <sets> <ways> <line-bytes>
```

- Implement a **set-associative cache** with LRU replacement.
- A **hit** costs 1 cycle; a **miss** costs a configurable **miss penalty** (default ~100 cycles, standing in for DRAM).
- **Report hits, misses, miss rate**, and the cycles lost to memory stalls.
- The cache geometry must be `S × E × B` as in Week 4 — verify a configuration's capacity.

### 4. Required demonstrations

Your simulator must be able to **show the course's own results on your own machine model**:

**(a)** A program of independent instructions completing in ≈ *N* + 4 cycles — pipelining works.
**(b)** A dependency chain running slower than independent instructions of the same count — the latency/throughput distinction (Week 5).
**(c)** A **cache-friendly vs cache-hostile** access pattern (e.g. row-major vs column-major array traversal) showing a large miss-rate and cycle-count difference — Week 4's central result, reproduced *in your simulator*.
**(d)** A branch-heavy program showing the misprediction penalty.

---

## Report — 30% of the project mark

**Six to eight pages.**

| Section | Must contain |
|---|---|
| **Design** | How you model stages, hazards, forwarding and the cache. What you reused from Project 1 and what you changed |
| **Pipelining** | Demonstration (a): *N* + 4 cycles for *N* independent instructions, with the numbers |
| **Hazards** | Demonstrations (b) and (d): a dependency chain and a branch-heavy program, with cycle counts and hazard statistics |
| **The cache** | Demonstration (c): row-major vs column-major, miss rates and cycles. **Compare with the real 7.45× / 50%→8% result from Week 11's matmul** and discuss how your model matches or diverges |
| **Validation** | How you know the timing is right — a hand-computed cycle count for a small program, matched against your simulator |
| **Limits** | What your model does *not* capture (out-of-order, superscalar, real DRAM timing) and how that would change the numbers |

**The cache section is the centrepiece.** Reproducing Week 4's cache-hostility result inside a simulator you built — and explaining where your simplified model agrees with and diverges from the real measurement — is the strongest evidence that you understood both the cache and your own model.

---

## Marking

| | |
|---|---:|
| **Pipeline** — five stages, correct cycle counting, IPC | **25** |
| **Hazards** — forwarding, stalls, branch prediction, statistics | **20** |
| **Cache** — set-associative, LRU, hit/miss timing, the four demonstrations | **25** |
| **Report** | **30** |
| **Total** | **100** |

### Bonus, up to +10 (capped at 100)

| | |
|---|---:|
| A second cache level (L1 + L2) with correct inclusive/exclusive behaviour | +4 |
| A visualisation of the pipeline (per-cycle stage occupancy diagram) | +3 |
| A configurable superscalar width (issue > 1 per cycle) | +3 |

---

## Advice

**Start from Project 1's decode.** If decode and execute were separate, the pipeline is an extension: each stage holds one instruction's state and passes it on. If they were fused, separate them first — it is worth a day.

**Get the pipeline counting cycles before adding hazards.** A correct ideal pipeline (demonstration (a)) is the foundation; hazards and the cache refine it. **A simulator that does (a) and (c) well beats one that attempts everything and validates nothing.**

**Validate against hand computation.** Take a 10-instruction program with one load-use hazard and one cache miss, work out the cycle count by hand, and match it. **A cycle count you cannot derive by hand is a cycle count you cannot trust** — which is Week 11's cross-check-against-theory, applied to your own tool.

**Reuse the course's numbers as your model's constants.** Miss penalty ~100 cycles (Week 4's DRAM), misprediction penalty ~15–20 (Week 5). Your simulator is a small model of the machine you have been measuring all term.

---

## Milestones

| By end of | Have working |
|---|---|
| **Week 10** | Project 1 refactored so decode and execute are separate stages |
| **Week 11** | The five-stage pipeline counting cycles; demonstration (a) |
| **Week 12** | Hazards, the cache, all four demonstrations, the report, and a working demo |

---

*CS 201 · Project 2 · assigned Week 10, due Week 12 · 10% · demo in Lab 12*

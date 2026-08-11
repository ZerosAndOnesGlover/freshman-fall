# CS 201 · Problem Set 12 — Solutions
## Instructor Only

---

> **Not for distribution.** The synthesis set — most answers are connections rather than calculations,
> so **reward correct linkage to specific earlier weeks**, not just plausible-sounding prose. The
> `add eax,[rdi]` fact in Q1 is verified; the frontier figures are cited.

---

## Q1 (16) — RISC-V and CISC

### (a) [4]

RISC-V equivalent of `add eax, [rdi]`:

```
lw    t0, 0(a0)      # load a[i] into a register
add   a1, a1, t0     # then add
```

**A RISC (load-store) design forbids memory operands on arithmetic instructions** — only explicit loads and stores touch memory, everything else is register-to-register. Hence the single CISC `add`-from-memory splits into two.

### (b) [4] — any three, each tied to a week

- **Fixed-length decode (Week 2):** every RISC-V instruction is the same size, so instruction boundaries are trivially parallel to find — the variable-length problem of Week 2 §L02 disappears.
- **Pipelining (Week 5):** simple, uniform instructions are easier to slot into the five stages with predictable timing; a load-op that both reads memory and computes complicates the pipeline.
- **Hardware simplicity:** a smaller, simpler decoder and control path means a smaller, faster, more verifiable chip — the transistors go to the datapath, not to decoding complexity.

### (c) [4]

**Open means anyone may implement it without licence or fee**, which turned the ISA into a *commons*. **The architectural consequence** — not merely legal — is the "Cambrian explosion": research groups, startups and established firms can build processors targeting the same software ecosystem without permission, so specialised implementations (embedded, vector, secure) proliferate. **A proprietary ISA gates who can innovate on the hardware; an open one does not.**

### (d) [4]

**Reconcile:** x86 chips translate CISC to RISC-like micro-ops *at run time, in hardware, on every instruction* — a decoder that costs area and power (Week 3 §L03). **RISC-V does the simplification at the ISA level, so the hardware never pays that translation cost.** Building a RISC ISA removes the decoder complexity that x86's backwards compatibility forces it to carry — you get the RISC-like execution engine without the CISC front end.

> Full marks require noting that x86's translation is a *runtime hardware cost* that a native RISC
> ISA avoids. "They're the same inside" alone misses the point.

---

## Q2 (20) — Domain-Specific Architectures

### (a) [6] — the axis, with a workload and a transistor-spend each

| Machine | Spends on | Workload |
|---|---|---|
| CPU | caches, prediction, OoO | general, branchy, latency-sensitive |
| GPU | thousands of simple cores | regular, massively parallel, high-intensity |
| TPU/NPU | multiply-accumulate arrays | neural-net inference/training |
| FPGA | reconfigurable logic | custom circuits, low volume |
| ASIC | one fixed circuit | one workload, enormous volume |

Left→right: more specialised, more efficient, less flexible.

### (b) [5]

**Discards: the large caches (Week 4) and the branch predictor + out-of-order machinery (Week 5).** It can because **neural-network computation is a fixed sequence of huge, regular matrix multiplies with essentially no data-dependent branches and a predictable, streaming access pattern** — so branch prediction has nothing to predict and large caches buy little over a well-fed systolic array. Every transistor saved goes to multiply-accumulate units.

### (c) [4]

**By refusing to spend anything on generality.** The 15–30× is not cleverer arithmetic; it is that a GPU still carries scheduling, caching and flexibility overhead the TPU deletes, so a far larger fraction of the TPU's transistors and power do the actual multiply-accumulates. **Efficiency bought with flexibility** — the generality-efficiency trade, stated as a number.

### (d) [5]

**Defend or challenge; reward the mechanism.** The strong defence: the GPU matched deep learning's matrix-multiply shape; the TPU matched it tighter; each won by fitting the workload — so "the architecture reflects the workload" is descriptively true of the whole frontier. **The Week-0 principle:** every abstraction/generality is a contract with a cost, so specialising removes the cost of serving workloads you do not have. A good *challenge* notes that extreme specialisation risks obsolescence when the workload shifts (a TPU tuned for one network shape is stranded when the shape changes) — flexibility has value the sentence understates.

---

## Q3 (14) — Two Different Machines

### (a) [5]

**Helps:** factoring (Shor), quantum-chemistry simulation, some search (Grover). **Does not:** general branchy code, serial algorithms, most of what a CPU does. **Distinguishing property:** problems with structure a superposition/entanglement can exploit for exponential or quadratic advantage — a narrow class. **Not "a faster CPU"** because it is a different *model of computation*: it does not execute instructions faster, it computes a different way, and is useless outside its class.

### (b) [5]

**Attacks the von Neumann bottleneck (Week 0) / the cost of moving data between compute and memory (Week 4).** Co-locating compute and memory means a "neuron" computes on data that is already local — no fetch across the bus, which Week 4 showed dominates. **Helps only certain workloads** because the model — sparse, event-driven, spike-based — suits pattern recognition and always-on sensing, not general computation; a machine shaped like a brain is good at brain-like tasks and poor at the rest.

### (c) [4]

**Quantum:** needs error-corrected qubits at scale (millions, from today's hundreds of noisy ones) — an engineering leap that may or may not arrive — *and* a workload important enough to justify it; uncertain because both the physics and the economics are open. **Neuromorphic:** needs a workload where its energy efficiency is decisive (always-on edge sensing is the candidate) and software/tooling that makes it programmable; uncertain because the general-purpose alternatives keep improving. **Reward any answer naming both a workload condition and an engineering condition.**

---

## Q4 (30) — The Whole Machine

### (a) [12] — 1 per operation-week pairing; ~2 per line

| Op | Week(s) | What the machine does |
|---|---|---|
| `char buf[256]` | 3, 9 | allocates a stack frame; the bound is what a later copy must respect |
| `open` | 6, 7 | sets up a file mapping; names a device 10⁵× slower than L1 |
| `read` | 6, 7 | page-cache hit (~2.5 μs) or a fault to the SSD (~157 μs) |
| `parse_and_sum` | 1, 2, 4, 5 | integer-overflow risk; a compiled loop; cache misses; a possible dependency chain |
| `snprintf` | 9 | a bounded format — the safe form (see (b)) |
| `send` | 8 | a framed byte stream over TCP; a round trip dwarfing all the above |

Accept reasonable week assignments; the *mechanism sentence* is the marked part.

### (b) [6]

**`sprintf` has no bound** — it writes as many bytes as the format produces, and if `total`'s string exceeds `out[64]` it overflows the stack buffer (Week 3's frame), potentially the return address (Week 9's overflow). **`snprintf(out, sizeof out, …)` bounds the write to the buffer.** With `sprintf`, an attacker who controls `total`'s magnitude could overflow `out` and, with defenses off, redirect control flow — the exact Week 9 mechanism.

### (c) [6]

**By latency, ascending:** `parse_and_sum` (CPU, ~μs) < `snprintf` (CPU) < `read` cached (~2.5 μs) or `open`/`close` (μs) ≪ `read` from device (~157 μs) ≪ **`send` — an internet round trip at ~187 ms.** **`send` dominates by three orders of magnitude** over everything else combined; the whole function's wall-clock time is essentially the network round trip. Justify with the ladder: 187 ms vs microseconds.

> The marked insight: the CPU work and even the disk are noise next to the network. Optimising
> `parse_and_sum` to nothing would not move the function's latency.

### (d) [6]

**Week-11 method.** Next measure: **profile to confirm `parse_and_sum` is the hotspot, then diagnose with cachegrind whether it is compute- or memory-bound** (D1/LLd miss rates), placing it on the roofline. The two bounds: **memory-bound** (poor access pattern — fix the layout, Week 4) or **compute-bound** (heavy per-byte work — vectorise/reduce flops, Week 5). **Amdahl ceiling:** at 80% of *CPU* time, deleting it entirely caps CPU speedup at $1/(1-0.8) = 5\times$ — **but note (c): CPU is a tiny fraction of wall-clock, so the *overall* payoff is negligible against the network.** A student who spots that this is a real trap — a large ceiling on a fraction that does not matter — earns full marks.

---

## Q5 (20) — What You Keep

### (a) [6]

**Ratios:** L1→DRAM ≈ **100×**; DRAM→SSD read ≈ **1000×**; SSD read→internet RTT ≈ **1000×**. *(4/438; 438/500 000; 500 000/600 000 000.)* **The ratios are more worth remembering because they are stable across hardware generations** — absolute cycle counts change with every clock and process node, but "DRAM is ~100× L1" and "the network is ~10⁶× a cache hit" have held for decades and shape every design decision regardless of the specific numbers.

### (b) [6] — three ideas, two weeks each

Any three of L38 §4, e.g.: **data movement dominates** (Weeks 4, 7, 8, 10, 11); **operation size is the variable** (Weeks 4, 7, 8); **the compiler runs equivalent code** (Weeks 0, 2, 5, 11); **know your bottleneck** (Weeks 4, 5, 7, 11); **abstractions cost** (Weeks 0, 2, 3, 6, 8, 10). Two distinct weeks required per idea.

### (c) [4]

Two of: Week 0's loop → `movabs`; Week 2's division → magic multiply; Week 5's `if` → `cmov`; Week 11's inlined-away profile. **General consequence: "what does the machine do?" is answered by the disassembly / a measurement, never by reading the source** — the source is what you *asked for*, not what runs.

### (d) [4]

**Speed of light:** transatlantic RTT (187 ms) is set by distance and physics, not engineering, so latency floors are permanent — implying that systems must be designed to *tolerate* latency (async, caching, locality, CDNs) rather than assume it away. **Data movement:** moving a byte has cost more than operating on one for forty years and increasingly so; every architecture in L37 is an attempt to move less data, so **designing for locality and minimal data movement will remain the central performance discipline** of the student's career. Reward either, argued with a design implication.

---

## Mark Summary

| | |
|---|---:|
| Q1 | 16 |
| Q2 | 20 |
| Q3 | 14 |
| Q4 | 30 |
| Q5 | 20 |
| **Total** | **100** |

**This set rewards synthesis.** The strongest answers connect the frontiers back to specific measured weeks; the weakest recite plausible generalities. **Q4(d) is the discriminating question** — spotting that an 80%-of-CPU hotspot has a negligible payoff against a network-dominated wall-clock is the whole course's "know your bottleneck" lesson at its sharpest.

---

*CS 201 · Week 12 · PS 12 Solutions · Instructor Only*

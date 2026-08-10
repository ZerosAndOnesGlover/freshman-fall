# CS 201 · Problem Set 5 — Solutions
## Instructor Only

---

> **Not for distribution.** All figures measured on the lab image (i5-8250U, GCC 13.3.0).

---

## Q1 (24) — Hazards in Instruction Sequences

### (a) [8] — 1 per correctly identified and typed hazard

**Sequence A**

| Instructions | Type |
|---|---|
| `mov rax,[rbx]` → `add rax,rcx` | **RAW** on `rax` — and specifically a **load-use** hazard |
| `add rax,rcx` → `mov [rdx],rax` | **RAW** on `rax` |

*`sub rcx,rdi` is independent of all three.*

**Sequence B**

| Instructions | Type |
|---|---|
| `imul rax,rbx` → `add rcx,rax` | **RAW** on `rax` |
| `imul rax,rbx` → `mov rbx,5` | **WAR** on `rbx` |
| `imul rax,rbx` → `mov rax,rdx` | **WAW** on `rax` |
| `add rcx,rax` → `mov rax,rdx` | **WAR** on `rax` |

> Accept a student who omits the second WAR; award the mark if the first three are right. **Deduct
> for calling the WAR/WAW pairs "dependencies" without qualification** — (b) is about exactly that.

### (b) [4]

**[2]** **True dependency: the RAW only.** It reflects the actual flow of a value from producer to consumer.

**WAR and WAW are naming artefacts** — they arise only because the ISA has 16 register *names*, so two unrelated values are forced to share one.

**[2]** **Register renaming** removes them: the hardware maps architectural names onto a much larger physical register file, so `mov rax,rdx` writes a *different* physical register than `imul` did.

**It cannot remove RAW** because the consumer genuinely needs the produced value — no amount of renaming creates the number earlier.

### (c) [6] — 2 each

1. **0 stalls.** Forwarding routes the ALU result from the end of E directly into the next instruction's E.
2. **1 stall.** A load's result is not available until the end of **M**, one stage later than an ALU result, so it cannot reach the immediately following E.
3. **0 stalls.** The independent instruction fills the gap; by the time `add` reaches E, the load has completed M.

**The difference between (1) and (2)** is *where in the pipeline the value becomes available*: end of E against end of M. Forwarding can move a value sideways in time but not backwards.

### (d) [6]

**[4]** Move the independent instruction into the load-use gap:

```
mov  rax, [rbx]
sub  rcx, rdi        ; independent -- fills the stall slot
add  rax, rcx        ; NOTE: now reads the UPDATED rcx
mov  [rdx], rax
```

> **This is a trap and it should be marked as one.** Moving `sub rcx,rdi` before `add rax,rcx`
> **changes the program** — `add` now uses the new `rcx`. A student who does this without noticing
> scores 2 of 6.
>
> The correct version needs a different filler, or must move `sub` *after* the `add`:
>
> ```
> mov  rax, [rbx]
> nop            ; or any instruction not writing rcx/rax
> add  rax, rcx
> mov  [rdx], rax
> sub  rcx, rdi
> ```

**[2] Saved: 1 cycle**, and the assumption is **full forwarding with a one-cycle load-use penalty** — i.e. the classic 5-stage model. **On the real out-of-order machine the reordering is unnecessary**, because the hardware does it anyway; award a bonus mention for noticing this.

---

## Q2 (20) — Dependency Chains, Measured

### (a) [6]

```
1 chain,  200000000 adds   0.4768 s   2.38 ns/add
4 chains, 200000000 adds   0.1191 s   0.60 ns/add
speedup 4.00x
```

*(Verified, reproducible to two decimals.)*

### (b) [5]

**Measured: 7.25×** *(verified — 0.4920 s against 0.0679 s).*

**Not 8×.** The shortfall is **floating-point add throughput**: this core can issue about two FP adds per cycle, so beyond a handful of chains the limit stops being dependency latency and becomes execution-unit throughput and issue width. Adding more accumulators past that point buys progressively less.

> Accept "issue width", "FP unit throughput" or "port contention". **Reject "cache" or "memory"** —
> the loop touches no memory.

### (c) [4]

**[2]** Measured **~3.21 GHz** *(verified: 2×10⁹ dependent iterations in 0.6230 s).*

**[2]** `/proc/cpuinfo` read **during** the run shows ~3399 MHz on the active core. **At idle it is meaningless** — the governor is `powersave` and unloaded cores drop to 400 MHz, so a reading taken before or after the benchmark describes a state the benchmark never ran in.

### (d) [5]

**[2]** $2.38 \text{ ns} \times 3.21 \text{ GHz} \approx \mathbf{7.6 \text{ cycles}}$ per addition.

**[3]** `addsd` latency is 4 cycles, so the chain alone predicts ~4. **The extra ~3.6 cycles are the rest of the loop** — at `-O1` the accumulator is not held purely in a register across iterations, and the loop counter increment, compare and branch are also in the path.

**Full marks for any answer that notices the gap and proposes a concrete cause**, then ideally checks it by disassembling. **A student who reports 7.6 cycles and asserts it equals the 4-cycle latency has not thought about it** — 2 of 5.

---

## Q3 (24) — Branch Prediction

### (a) [4]

**1.02×** *(verified).* Sorting made no measurable difference.

### (b) [5]

```
1213:  cmp    esi,0x7f
1216:  cmovg  rcx,rdx
```

*(Verified.)* **GCC performed if-conversion**, turning the `if` into a conditional move. **There is no branch, so there is nothing to mispredict.**

> This is the question that teaches the habit. **Full marks require quoting the instruction**, not
> just asserting "the compiler optimised it".

### (c) [5]

```
unsorted  0.2561 s
sorted    0.0319 s
ratio     8.03x
```

*(Verified; a second run gave 8.70×.)* A real `jle` is present at `0x1213`.

### (d) [6]

| Version | Time | Why |
|---|---:|---|
| Real branch, sorted | 0.0319 s | Branch predicted correctly nearly always; when not taken, the `add` is skipped entirely |
| Branchless `cmov` | 0.0590 s | Cannot mispredict, but **unconditionally performs the add and the select** every iteration |
| Real branch, unsorted | 0.2561 s | ~50% misprediction; each costs a full pipeline flush |

**[3] Why branchless loses to a predicted branch:** `cmov` pays for the work *every* iteration. A correctly predicted branch pays for it only when the condition holds — and here that is about half the time — with the prediction itself costing essentially nothing.

**[3] The rule:** **use `cmov` when the branch is unpredictable; use a branch when it is predictable.** The crossover is roughly where the expected misprediction cost exceeds the cost of the work `cmov` does unconditionally.

### (e) [4]

A defensible estimate:

- Branches executed: $32\,768 \times 2000 = 6.55 \times 10^7$.
- Extra time from misprediction: $0.2561 - 0.0319 = 0.2242$ s.
- Mispredictions at ~50% of a random condition: $\approx 3.28 \times 10^7$.
- Extra cycles: $0.2242 \text{ s} \times 3.21 \times 10^9 = 7.20 \times 10^8$.
- **Penalty $\approx 7.20\times10^8 / 3.28\times10^7 \approx \mathbf{22 \text{ cycles}}$.**

**Consistent with the 15–20 cycle figure for a ~14-stage pipeline.** Accept anything in the 12–30 range **with stated assumptions**; the assumptions are the marked part.

---

## Q4 (16) — Amdahl's Law

### (a) [4]

$$S = \frac{1}{(1-p) + p/s}, \qquad p = 0.3,\ s \to \infty \;\Rightarrow\; S = \frac{1}{0.7} = \mathbf{1.43\times}$$

**Making 30% of a program infinitely fast gains 43%.**

### (b) [4]

$$S = \frac{1}{0.6 + 0.4/4.5} = \frac{1}{0.689} = \mathbf{1.45\times}$$

**Comment:** a 4.5× improvement on 40% of runtime is a 45% overall gain. Whether that is worthwhile depends on the effort and on what else is available — **but a student should note that the remaining 60% is now the obvious target**, and that this is exactly why profiling precedes optimising.

### (c) [4]

$$50 = \frac{1}{(1-p) + p/64} \;\Rightarrow\; (1-p) + \frac{p}{64} = 0.02 \;\Rightarrow\; p\left(1 - \tfrac{1}{64}\right) = 0.98 \;\Rightarrow\; p = \mathbf{0.9956}$$

**99.56% of the program must parallelise.** Comment: extremely demanding — under half a percent of serial work, including all setup, I/O and result combination. **Realistic only for embarrassingly parallel workloads.**

### (d) [4]

**[2]** **Gustafson:** in practice, bigger machines are used on *bigger problems*, and the serial fraction typically shrinks as the problem grows. So the useful question is not "how much faster for this problem" but **"how much larger a problem in the same time"**.

**[2]** One situation each:

- **Amdahl** — a fixed-size latency-bound task: rendering one frame in 16 ms, compiling one file, responding to one request. The problem size is given.
- **Gustafson** — a simulation, a training run, a search: given more machine, you increase resolution, model size or the space searched. The problem grows to fit.

---

## Q5 (16) — SIMD and the Bottleneck

### (a) [6]

**4.51×** at $N = 2^{12}$ and **1.07×** at $N = 2^{22}$, outputs bit-identical at both. *(Verified.)*

Full sweep, for reference:

| $N$ | KiB/array | speedup |
|---:|---:|---:|
| $2^{12}$ | 16 | 4.51× |
| $2^{14}$ | 64 | 4.53× |
| $2^{16}$ | 256 | 2.78× |
| $2^{18}$ | 1024 | 2.65× |
| $2^{20}$ | 4096 | 1.37× |
| $2^{22}$ | 16384 | 1.07× |

### (b) [4]

**At $N = 2^{22}$:** three arrays × 16 MiB = **48 MiB**, eight times the 6 MiB L3. The loop is **memory-bandwidth-bound**; the arithmetic units are idle waiting for DRAM, and making them wider changes nothing.

**At $N = 2^{12}$:** three arrays × 16 KiB = **48 KiB**, resident in L1/L2. The memory system keeps up and the **vector units become the limit**, so widening them pays.

**A program is limited by one resource at a time. SIMD only helps if that resource is compute.**

### (c) [3]

Two of:

- Each iteration needs **two loads and a store**; load/store port throughput becomes the limit before the ALUs do.
- Loop overhead — pointer increments, the compare and the branch — does not vectorise.
- Even at 16 KiB there is real memory traffic; the arrays do not live in registers.

### (d) [3]

**[1]** **0** vector adds without `-ffast-math`; **4** with. *(Verified.)*

**[2]** **The objection:** vectorising a reduction means summing in a different order — partial sums per lane, then combined — and **floating-point addition is not associative** (Week 1 L06). The result would differ from what the source specifies, so the compiler refuses.

**What you give up:** the guarantee that the answer matches the serial order. `-ffast-math` grants associativity **globally**, which also silently disables compensated-summation algorithms — as Week 1's Lab 1 measured, where it made a Kahan sum bit-identical to a naive one.

> The best answers note that the hand-written vector reduction makes **exactly the same reordering**;
> the difference is that the programmer chose it deliberately and can bound the error.

---

## Mark Summary

| | |
|---|---:|
| Q1 | 24 |
| Q2 | 20 |
| Q3 | 24 |
| Q4 | 16 |
| Q5 | 16 |
| **Total** | **100** |

**Where the class loses marks, in order:**

1. **Q1(d)** — reordering into the stall slot in a way that changes the program.
2. **Q2(d)** — asserting the measured 7.6 cycles equals the 4-cycle `addsd` latency.
3. **Q3(b)** — saying "the compiler optimised it" without quoting `cmovg`.
4. **Q3(d)** — unable to explain why branchless *lost* to a predicted branch.
5. **Q5(d)** — knowing `-ffast-math` enables it but not what it gives away.

---

*CS 201 · Week 5 · PS 5 Solutions · Instructor Only*

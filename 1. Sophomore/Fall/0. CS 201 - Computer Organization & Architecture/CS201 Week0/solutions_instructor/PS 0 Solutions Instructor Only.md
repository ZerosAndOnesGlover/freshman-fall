# CS 201 · Problem Set 0 — Solutions
## Instructor Only

---

> **Not for distribution.** Marking notes are in blockquotes. Where a question admits several correct
> answers, the alternatives are listed — mark the reasoning, not the match to this page.

---

## Q1 (18) — The Layers

### (a) [6] — 0.5 per cell, twelve cells

| Layer | Hides | Costs |
|---|---|---|
| Gates over transistors | Analogue voltages, device physics | Switching delay and power per gate; you cannot exploit intermediate voltages |
| ISA over microarchitecture | Pipelining, caching, out-of-order execution | You cannot see or control *why* one instruction sequence is faster than an equivalent one |
| C over assembly | Register allocation, addressing modes, instruction selection | No control over which values stay in registers; the compiler may transform code beyond recognition |
| Python over C | Memory layout, allocation, machine types | ~46× on the Lecture 1 benchmark; no control over object representation |
| Virtual memory over physical memory | Where the data physically is; that RAM is shared and finite | TLB miss on translation; page faults; you cannot know if a "memory access" is a DRAM read or a disk read |

> Accept anything defensible. The common wrong answer is a "cost" that is really a *benefit stated
> negatively* ("costs you the ability to corrupt other processes"). Push back on that: the cost must
> be something a competent engineer would sometimes want.

### (b) [6]

**[3]** The ISA is a *specification the hardware is obliged to satisfy*, not a description of how any particular chip works. Intel and AMD implement x86-64 with almost nothing in common internally; both are correct because both honour the same contract.

**[3]** Consequence: **a binary compiled decades ago still runs.** If the ISA were merely a convention, every microarchitectural redesign — every new pipeline depth, every cache change — would risk breaking existing programs, and software would have to be recompiled or rewritten per chip.

> Also accept: emulation and virtualisation are possible because the contract is finite and written
> down; a compiler can target "x86-64" rather than "this specific CPU".

### (c) [6] — 2 per cost, with the scaling judgement

Any three of:

| Cost | Scales with |
|---|---|
| Bytecode fetch and dispatch per operation | Number of iterations |
| Dynamic type check on both operands | Number of iterations |
| Allocating a new integer object for each result | Number of iterations *(and size, once values exceed the small-int cache)* |
| Reference count increment/decrement | Number of iterations |
| `t` looked up by name in a frame/dict rather than held in a register | Number of iterations |
| Arbitrary-precision integer arithmetic rather than fixed 64-bit | **Size** of the numbers |

> Full marks require the scaling column to be *reasoned*, not guessed. The one genuinely
> size-dependent cost is arbitrary-precision arithmetic; a student who identifies that and
> distinguishes it from the per-iteration overheads has understood the question.

---

## Q2 (26) — Decoding by Hand

### (a) [6]

`eb 0a` at `0x1162`, two bytes long.

**[3]** At the moment the displacement is applied, `rip = 0x1164` — the address of the *next* instruction. `rip` is advanced during **fetch**, before execute, so by the time the jump's displacement is added the pointer has already moved past the jump itself.

**[3]** $\texttt{0x1164} + \texttt{0x0a} = \texttt{0x116e}$ ✓ — matches the listing.

> Deduct 3 if the student adds to `0x1162` and gets `0x116c`. This is *the* diagnostic error of the
> question, and it is worth a comment rather than only a mark.

### (b) [6]

`7e ee` at `0x1174`, two bytes.

**[2]** `0xee` as a signed 8-bit value: $238 - 256 = -18$.
**[2]** `rip` after fetch = `0x1176`.
**[2]** $\texttt{0x1176} - 18 = \texttt{0x1176} - \texttt{0x12} = \texttt{0x1164}$ ✓

### (c) [6]

```
1154:  c7 45 f8 00 00 00 00     mov DWORD PTR [rbp-0x8],0x0
115b:  c7 45 fc 01 00 00 00     mov DWORD PTR [rbp-0x4],0x1
```

**[2]** The two differ in exactly bytes 3 and 4 — `f8`/`fc` and `00`/`01` — and the two instructions differ in exactly the displacement and the immediate. So byte 3 is the displacement and bytes 4–7 are the immediate.

**[4]** Full account:

| Bytes | Role |
|---|---|
| `c7` | Opcode: move immediate into r/m32 |
| `45` | ModRM: addressing mode `[rbp + disp8]`, 32-bit operand |
| `f8` | disp8 = $-8$ *(`0xf8` = 248 − 256)* |
| `00 00 00 00` | imm32 = 0, little-endian |

> The *method* is the marked thing: inferring encoding structure by differencing two near-identical
> instructions. A student who reproduces an encoding table from the Intel manual without the
> differencing argument gets 4, not 6.
>
> Do not require the name "ModRM". "The byte that says the operand is at rbp plus a one-byte offset"
> earns the mark.

### (d) [8]

**[2] Variable-length advantage:** code density. Common short operations (`push rbp` = 1 byte, `ret` = 1 byte) cost one byte instead of four, so a given program occupies less memory and **more of it fits in the instruction cache** — a real performance effect, not just a disk-space one.

**[2] Fixed-length advantage:** the address of instruction *N+1* is known without decoding instruction *N*. Instruction boundaries are trivially parallel to find, and alignment is guaranteed.

**[4] Eight instructions per cycle:** fixed-length, and the argument must be about the *serial dependency*. With variable length, finding eight boundaries requires either decoding serially — which defeats the purpose — or speculatively decoding from many possible offsets and discarding the wrong ones, which costs area and power that grows sharply with issue width. Fixed length makes eight boundaries a matter of adding 4, 8, 12… to the current address.

> Accept a well-argued defence of variable-length that acknowledges the decode cost and appeals to
> instruction-cache pressure or a micro-op cache. That is a real position — it is roughly Intel's —
> and a student who argues it knowingly should not be penalised for disagreeing with the expected
> answer. Penalise only the answer that does not engage with the serial-boundary problem at all.

---

## Q3 (26) — Trace the Cycle

### (a) [14] — 2 per row, plus 2 for correct `rip` discipline throughout

`sum_to(3)`: `n = 3` at `[rbp-0x14]`, `total` at `[rbp-0x8]`, `i` at `[rbp-0x4]`. Entering at `0x1164` with `total = 0`, `i = 1`.

| # | Addr | Instruction | Fetch | Execute | `eax` | `total` | `i` | Branch |
|---|---|---|---|---|---:|---:|---:|---|
| 1 | `1164` | `mov eax,[rbp-0x4]` | 3 B, `rip`→`1167` | **read** `i` into `eax` | 1 | 0 | 1 | — |
| 2 | `1167` | `add [rbp-0x8],eax` | 3 B, `rip`→`116a` | **read** `total`, add, **write** back | 1 | **1** | 1 | — |
| 3 | `116a` | `add [rbp-0x4],0x1` | 4 B, `rip`→`116e` | **read** `i`, add 1, **write** back | 1 | 1 | **2** | — |
| 4 | `116e` | `mov eax,[rbp-0x4]` | 3 B, `rip`→`1171` | **read** `i` into `eax` | **2** | 1 | 2 | — |
| 5 | `1171` | `cmp eax,[rbp-0x14]` | 3 B, `rip`→`1174` | **read** `n`; compute $2-3=-1$, discard; SF=1, ZF=0, OF=0 | 2 | 1 | 2 | — |
| 6 | `1174` | `jle 1164` | 2 B, `rip`→`1176` | SF≠OF ⇒ less ⇒ **taken**; `rip` = `1176` − 18 = `1164` | 2 | 1 | 2 | **taken** |

> Row 5 is where marks are lost. `cmp` **discards its result** and keeps only the flags; a student
> who writes `eax = -1` has the central misconception of the question. Deduct the row.
>
> Row 6: accept "taken because 2 ≤ 3". Full credit for naming the flag condition, but do not require
> it — `jle`'s exact condition (ZF=1 or SF≠OF) is Week 2.

### (b) [6]

**[4]** The branch at `0x1174` executes **four** times: **3 taken**, **1 not taken**.

The tests occur with `i` = 1, 2, 3 (all ≤ 3, taken) and finally `i` = 4 (not taken).

**[2]** The not-taken case is the loop exit — a loop that runs *k* times tests *k*+1 times, because the condition must be evaluated once more to discover it has become false.

> Common error: answering "3 taken, 0 not taken" by forgetting the exit test, or "3 executions" by
> forgetting the entry test reached through the initial `jmp`. Either loses 2.

### (c) [6]

**[3] Counts for the whole call:**

| | |
|---|---:|
| Instructions executed | **31** |
| Data reads | **18** |
| Data writes | **9** |

Breakdown:

| Phase | Instructions | Reads | Writes |
|---|---:|---:|---:|
| Prologue (`endbr64` … `jmp`) | 7 | 0 | 3 |
| Entry test (`116e`–`1174`) | 3 | 2 | 0 |
| Body + test, ×3 | 18 | 15 | 6 |
| Epilogue (`1176`–`117a`) | 3 | 1 | 0 |
| **Total** | **31** | **18** | **9** |

> **Accept 20 reads / 10 writes** from a student who also counts the implicit stack traffic of
> `push rbp`, `pop rbp` and `ret`. Both conventions are defensible; what is *not* acceptable is
> counting them inconsistently. Ask for the convention to be stated.

**[3] What `-O2` removes:** all of it. With `total`, `i` and `n` in registers, every one of the 18 reads and 9 writes disappears:

| Variable | Reads | Writes |
|---|---:|---:|
| `total` | 4 | 4 |
| `i` | 10 | 4 |
| `n` | 4 | 1 |
| | **18** | **9** |

The loop becomes register-only arithmetic — which, together with the two-deep unroll, is why Lab 0 measures `-O2` at about 0.045 s against `-O0`'s 0.26 s on the hundred-million-iteration version.

---

## Q4 (16) — Cache Geometry

### (a) [4]

$$\text{L1d: } 64 \times 8 \times 64 = 32\,768 \text{ B} = 32\text{ KB} \checkmark$$
$$\text{L2: } 1024 \times 4 \times 64 = 262\,144 \text{ B} = 256\text{ KB} \checkmark$$
$$\text{L3: } 8192 \times 12 \times 64 = 6\,291\,456 \text{ B} = 6\text{ MB} \checkmark$$

### (b) [4]

**[2]** $64 / 4 = \mathbf{16}$ `int`s per line.
**[2]** One was asked for; **15** came along uninvited.

### (c) [4]

**[1]** Array size: $10^6 \times 4 = 4$ MB, which is $4\,000\,000 / 64 = \mathbf{62\,500}$ lines.

**[1] Program A (sequential):** touches each line once, in order — **62 500 line fetches**, each serving 16 accesses.

**[2] Program B (random):** with 4 MB exceeding L1 (32 KB) and L2 (256 KB), consecutive random accesses almost never hit the same line, so nearly every one of the **1 000 000** accesses misses at L1 — roughly **16× more line traffic** than A for identical algorithmic work.

**Assumption that must be stated:** the array is larger than L1 and L2. *(It does fit in the 6 MB L3, so B's misses are largely served from L3 at ~40 cycles rather than DRAM at 200+ — a student who notices this and bounds B's cost below the worst case deserves credit.)*

> This is Week 4's central experiment, asked a week early with no measurement. The mark is for the
> line-count reasoning, not for a precise number.

### (d) [4]

Access latency grows with size. Concretely, any two of:

- **Wire delay** — a physically larger array means longer wires from the decoder to the cells and back; at multi-GHz clocks, propagation across the array is a real fraction of the cycle.
- **Indexing and tag comparison** — more sets means a wider index decode; more ways means more tag comparators operating in parallel and a wider output multiplexer.
- **Power and area** — a large fast cache is expensive in both, and the budget is better spent elsewhere.

The hierarchy exists precisely because "large" and "fast" cannot be had in one structure: small-and-fast close to the core, large-and-slow further out.

---

## Q5 (14) — After Moore's Law

### (a) [5]

**[2] Moore's Law:** the number of transistors on an economically optimal chip doubles roughly every two years. An observation about *count*.

**[2] Dennard scaling:** as a transistor's dimensions shrink by a factor $k$, its voltage and current can shrink by $k$ too, so **power density stays constant** — permitting higher clocks at no thermal cost.

**[1] Dennard scaling ended** around 2005 *(leakage current dominates below ~1 V)*. **Moore's Law continued** roughly another decade.

### (b) [5] — any three, ~1.7 each

1. **Cores.** Four physical cores and eight hardware threads against one. Even at lower clock, aggregate throughput is several times higher on parallel work.
2. **Memory hierarchy.** 6 MB of shared L3 plus per-core L1/L2, with hardware prefetching. The P4's memory system was far weaker, and Lecture 3's 200-cycle DRAM figure is what that costs.
3. **Wider, smarter out-of-order execution.** More instructions issued per cycle, larger reorder window, far better branch prediction — the P4's NetBurst pipeline was 20–31 stages deep, making each misprediction ruinous.
4. **SIMD width.** AVX2 gives 256-bit vectors; the P4 had 128-bit SSE2. Up to 2× per instruction on vectorisable work.
5. **Process and power efficiency.** Far more work per watt, which is what allows sustained turbo rather than thermal throttling.

> Reject "it has a bigger cache" stated with no mechanism. Require the *why*.

### (c) [4]

**[2] A valid category**, e.g.:

- **Embarrassingly parallel workloads** — video encoding, ray tracing, batch scientific computation, servers handling independent requests.
- **Programs whose hot loop lives in someone else's library** — BLAS, ffmpeg, a database engine, a JIT.

**[2] The property:**

- For the parallel case: the work decomposes into independent tasks sharing little or no mutable state, so more cores yield more throughput with no change to the program.
- For the library case: the performance-critical code is *not yours*. It gets rewritten for each new microarchitecture by its maintainers, and you inherit the improvement by upgrading a dependency.

> The best answers note that these are the *same* observation from two sides: performance is still
> free when somebody or something else is doing the adapting. Award full marks for that framing
> however it is expressed.

---

## Mark Summary

| | |
|---|---:|
| Q1 | 18 |
| Q2 | 26 |
| Q3 | 26 |
| Q4 | 16 |
| Q5 | 14 |
| **Total** | **100** |

**Where the class will lose marks, in order:**

1. **Q2(a)/(b)** — adding the displacement to the current address instead of the next one.
2. **Q3(a) row 5** — believing `cmp` writes its result to `eax`.
3. **Q3(b)** — forgetting that a loop running *k* times tests *k*+1 times.
4. **Q1(a)** — giving a benefit dressed as a cost.

All four are worth naming in the Week 1 lecture; the first two recur throughout Weeks 2 and 3.

---

*CS 201 · Week 0 · PS 0 Solutions · Instructor Only*

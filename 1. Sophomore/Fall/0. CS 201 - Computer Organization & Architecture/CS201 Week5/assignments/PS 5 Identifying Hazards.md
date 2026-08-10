# CS 201 · Problem Set 5
## Hazards, Prediction, and the Limits of Parallelism

---

**Released:** Week 5, Wednesday · **Due:** Week 6, Friday 17:00
**Total: 100 points** · Submit one PDF plus a `.zip` of source, `PS5_{LastName}_{StudentID}.pdf`

> Q1 and Q4 are pen-and-paper. Q2, Q3 and Q5 need measurements from **your** machine, with the
> commands shown. Report what you observed, including disagreements with the lecture.

---

### Q1: Hazards in Instruction Sequences (24 points)

**(a) [8]** For each sequence, list every hazard, giving the two instructions involved and the type (RAW / WAR / WAW / control / structural).

**Sequence A**
```
mov  rax, [rbx]
add  rax, rcx
mov  [rdx], rax
sub  rcx, rdi
```

**Sequence B**
```
imul rax, rbx
mov  rbx, 5
add  rcx, rax
mov  rax, rdx
```

**(b) [4]** Of the hazards you found in B, state which are **true dependencies** and which are **naming artefacts**. Name the hardware mechanism that removes the artefacts, and explain in one sentence why it cannot remove the others.

**(c) [6]** In a classic 5-stage pipeline with full forwarding, give the stall cycles for:

1. `add rax, rbx` followed immediately by `sub rcx, rax`
2. `mov rax, [rbx]` followed immediately by `add rcx, rax`
3. `mov rax, [rbx]`, then one unrelated instruction, then `add rcx, rax`

Explain why (1) and (2) differ, in terms of the stage at which each result becomes available.

**(d) [6]** Rewrite Sequence A to reduce its stalls without changing what it computes. State how many cycles you saved and what assumption about the machine you relied on.

---

### Q2: Dependency Chains, Measured (20 points)

**(a) [6]** Build the one-chain and four-chain accumulator loops from Lab 5 Part 1 with $N = 2\times10^8$ at `-O1`. Report both times and the speedup.

Reference *(verified)*: 0.4768 s and 0.1191 s — **4.00×**.

**(b) [5]** Extend to **eight** chains. **Predict the speedup before measuring**, then report it.

Reference *(verified)*: **7.25×** — not 8×. Explain the shortfall in terms of a hardware limit.

**(c) [4]** Measure your machine's sustained clock using the dependent-`add` loop from Lab 5 Part 2. Report it, and cross-check against `/proc/cpuinfo` **while the loop is running**. Explain why a reading taken at idle is useless.

**(d) [5]** Using your measured clock, convert the one-chain time to cycles per addition. Compare with the latency of `addsd` on this microarchitecture (4 cycles) and account for any difference — consider what else is in the loop.

---

### Q3: Branch Prediction (24 points)

Build the threshold-sum benchmark: a 32 768-element array of random bytes 0–255, summing elements `>= 128`, repeated 2000 times, then the identical loop on the **sorted** array.

**(a) [4]** Compile at `-O1` and report unsorted against sorted.

**You will probably measure no difference.** Reference *(verified)*: **1.02×**.

**(b) [5]** Find out why. Disassemble and quote the relevant instruction.

Reference *(verified)*: GCC emits `cmovg rcx,rdx` — **there is no branch to mispredict.**

**(c) [5]** Rebuild with `-fno-if-conversion -fno-if-conversion2 -fno-tree-loop-if-convert` and repeat.

Reference *(verified)*: 0.2561 s unsorted, 0.0319 s sorted — **8.03×**. Confirm a real `jle` is now present.

**(d) [6]** You now have three measurements. Complete and explain:

| Version | Time | Why |
|---|---:|---|
| Real branch, sorted | 0.0319 s | |
| Branchless `cmov` | 0.0590 s | |
| Real branch, unsorted | 0.2561 s | |

**The branchless version is slower than the correctly predicted branch.** Explain, and state the general rule for when `cmov` is the right choice.

**(e) [4]** Estimate the misprediction penalty in cycles from your own numbers. State your assumptions: the misprediction rate on random data, the number of branches executed, and your measured clock.

---

### Q4: Amdahl's Law (16 points)

**(a) [4]** State the law. A program spends 30% of its time in a routine you make **infinitely** fast. What is the overall speedup?

**(b) [4]** You vectorise a loop at 4.5×. It accounts for 40% of runtime. Compute the overall speedup, and comment on whether the effort was worthwhile.

**(c) [4]** What parallel fraction is needed to reach a **50×** speedup on 64 cores? Solve for $p$ and comment on how realistic that is.

**(d) [4]** Gustafson objected that Amdahl assumes a fixed problem size. State his alternative framing, and give one concrete situation where each law is the more useful question to ask.

---

### Q5: SIMD and the Bottleneck (16 points)

**(a) [6]** Implement `c[i] = a[i]*b[i] + 1.0f` scalar and with AVX2 intrinsics. Verify the outputs are **bit-identical**, then report the speedup at $N = 2^{12}$ and $N = 2^{22}$.

Reference *(verified)*: **4.51×** and **1.07×**.

**(b) [4]** Explain the collapse. Your answer must reference the total bytes touched at each size and the relevant cache capacity.

**(c) [3]** AVX2 has **eight** `float` lanes but the best measured speedup was 4.5×. Give two reasons.

**(d) [3]** Compile `float s=0; for(...) s+=a[i];` at `-O3 -mavx2` and count vector adds in the disassembly. Then add `-ffast-math` and count again.

Reference *(verified)*: **0** without, **4** with.

Explain the compiler's objection, and state precisely what you give up by overriding it.

---

## Marks

| | |
|---|---:|
| Q1 Hazards in Instruction Sequences | 24 |
| Q2 Dependency Chains, Measured | 20 |
| Q3 Branch Prediction | 24 |
| Q4 Amdahl's Law | 16 |
| Q5 SIMD and the Bottleneck | 16 |
| **Total** | **100** |

---

*CS 201 · Week 5 · Problem Set 5*

# CS 201 · Problem Set 11
## A Measured 10× Speedup

---

**Released:** Week 11, Wednesday · **Due:** Week 12, Friday 17:00
**Total: 100 points** · Submit one PDF plus a `.zip` of source, `PS11_{LastName}_{StudentID}.pdf`

> **This problem set is a report on an optimisation you performed.** Q3 asks for a **10× measured
> speedup on a real program, achieved by analysis, not guessing** — and the marks are for the
> *method*, evidenced at every step, not for the final number alone.
>
> `perf` needs privileges the lab machines lack; use gprof and valgrind. Note where `perf` would help.

---

### Q1: The Method (18 points)

**(a) [4]** State the five steps of the performance-engineering method from L34 §6. For each, name a tool that performs it.

**(b) [4]** Give Knuth's full quote on premature optimisation. Explain how the second half changes the meaning of the famous first half, and what it licenses.

**(c) [4]** Distinguish a **sampling** profiler from an **instrumenting** one — mechanism, overhead, and accuracy. When is each the right choice?

**(d) [3]** Profiling a `-O2` build attributed 100% of the time to `main`. Explain why, and give the flag that fixes it and what it costs.

**(e) [3]** Callgrind showed `__mcount_internal` at ~11% of a profile. What is it, and what general fact about instrumenting profilers does its appearance demonstrate?

---

### Q2: The Roofline (20 points)

**(a) [6]** Define **arithmetic intensity**. Compute it (flop/byte, `double`) for: vector add `c=a+b`; SAXPY `y=a*x+y`; dot product. Classify each as compute- or memory-bound.

**(b) [4]** Draw the roofline: label both roofs, the ridge point, and the two regions. State the fix appropriate to each region.

**(c) [4]** A matrix multiply's arithmetic intensity **grows with $n$**. Show why (flops and bytes as functions of $n$), and explain why this makes a large matmul compute-bound while vector add is always memory-bound.

**(d) [6]** A naive matrix multiply had **LLd miss rate = D1 miss rate = 50%**; a loop reorder dropped both to 8%, for a **7.45×** speedup *(reference)*. Explain what the equality of the two rates means, which Week-4 result shares the signature, and why the fix is a memory-bound fix rather than a compute one.

---

### Q3: Your 10× Speedup (40 points)

**Choose a program with a genuine, diagnosable bottleneck** — the matrix multiply of Lab 11 is acceptable and recommended if you have no other; a program of your own is welcome. **Achieve at least a 10× speedup, and report the full method.**

**(a) [6]** **Baseline.** The unoptimised program, a correctness check, and its measured runtime (median of several runs, with the range).

**(b) [8]** **Profile.** Show the profile identifying the hotspot. State which function dominates and by how much. If inlining hid it, show how you recovered the boundaries.

**(c) [8]** **Diagnose.** Use cachegrind (or the disassembly) to determine *why* the hotspot is slow — compute-bound, memory-bound, branch-bound. **Place it on the roofline** and state the miss rates or the limiting resource.

**(d) [6]** **Bound.** Compute, with Amdahl, the maximum speedup available from your intended fix *before* you make it. State whether the numbers justify the work.

**(e) [8]** **Fix and re-measure.** Show the change, prove correctness is preserved (same result), and report the new runtime and speedup. **Re-profile: where is the time now?**

**(f) [4]** **Reflect.** Did the bottleneck move as Amdahl predicted? What is the *next* thing you would optimise, and what is its ceiling?

> **Every claim needs evidence.** A speedup with no profile, no diagnosis and no correctness check
> is worth a fraction of the marks. The report *is* the deliverable — the number is the easy part.

---

### Q4: Benchmark Honestly (22 points)

**(a) [6]** Reproduce the Week-0 constant-folding failure: a loop that reports 0.0000 s at `-O2`. Show the disassembly with the folded constant, then fix it so the loop survives, with disassembly proving it. Name what your fix prevented.

**(b) [6]** For **each** of these measured-nothing failures from the course, state (i) what the naive benchmark measured instead of the intended effect, and (ii) how you would fix the measurement:

1. A "disk benchmark" reporting 2.5 μs per 4 KiB read (Week 7).
2. A denormal-slowdown benchmark reporting 1.00× (Week 1).
3. A huge-pages benchmark reporting 1.00× (Week 6).

**(c) [5]** You measure 4.1 s and 5.3 s on two runs of the same program. Give three causes and describe how you would report the result honestly, with what statistics.

**(d) [5]** From L36 §6, the most-skipped checklist item is "does it match theory?". Take **one** measured result from earlier in the course, state the independent model it was cross-checked against, and explain why that cross-check makes the number trustworthy where a bare measurement would not.

---

## Marks

| | |
|---|---:|
| Q1 The Method | 18 |
| Q2 The Roofline | 20 |
| Q3 Your 10× Speedup | 40 |
| Q4 Benchmark Honestly | 22 |
| **Total** | **100** |

---

*CS 201 · Week 11 · Problem Set 11*

# CS 201 · Computer Organization & Architecture
## Week 11 · Lecture 3 of 3
### Benchmarking Honestly

---

**Reading:** CS:APP §5.13 · **Previous:** L35, the roofline

---

## 1. Almost Every Benchmark Is Wrong the First Time

This course has, again and again, produced a measurement that turned out to be measuring nothing — or the wrong thing. **That was not carelessness; it is the normal condition of benchmarking.** A benchmark is an experiment, and experiments have systematic errors. This lecture collects the failures the course actually hit and turns them into a checklist.

**The through-line: the number a naive benchmark produces is usually not the number you wanted.** Getting an honest measurement is a skill, and it is the last thing the machine-organisation half of this degree teaches you.

---

## 2. The Compiler Deleted Your Work

**Week 0, the first and purest case.** A hundred-million-iteration summing loop, compiled at `-O2`, reported **0.0000 seconds** — because the compiler computed the constant answer at compile time and emitted a single `movabs`:

```
1101:  movabs rdx,0x11c3793adb7080     ; = 5000000050000000, the answer
```

**The loop was not slow; it did not exist.** *(Measured, Week 0.)*

**The rule:** a benchmark must produce a result the compiler cannot predict, and consume it in a way the compiler cannot discard. Techniques you have used all term:

- Read an input the compiler cannot see at compile time (`argc`, a file).
- Store to a `volatile`, or pass the result to an opaque function.
- Compile the kernel in a separate translation unit (Week 3), or with `-fno-inline`.

**And the corollary, from Week 5:** the same trap hides real effects. The four-accumulator loop had to be built carefully so `-O2` did not fold *it* into a closed form, and the false-sharing counters in Week 10 needed `volatile` to make the writes actually happen.

---

## 3. You Measured the Setup, Not the Thing

**Week 7 and Week 8, the "device or cache?" family.** Two measurements that look identical differ by 63× (storage) or hide a handshake (network), because the naive version measured the wrong layer:

- A "disk benchmark" that actually hit the **page cache** — 2.5 μs instead of the device's 157 μs.
- A "throughput" number that was really the per-request **software overhead**, invisible until you varied the block size and saw it flatten.

**The rule:** know which layer you are measuring, and control it. `O_DIRECT` to reach the device; a warm-up pass to fill the cache if the cache is what you mean to measure; state which one you did.

---

## 4. You Measured a Value, Not the Effect

**Week 1, the denormal benchmark.** The first attempt at measuring denormal slowdown reported **1.00× — no effect at all** — because the test values decayed out of the denormal range within a few thousand iterations and spent the rest of the loop as fast, ordinary zeros:

```c
float x = FLT_MIN;
for (...) { x *= 0.999f; s += x; }   /* x is denormal for ~1% of the loop */
```

**The effect was real (34×, once measured correctly with an array that stayed denormal); the benchmark just did not exercise it.** *(Measured, Week 1.)*

**And Week 3's alignment bug, and Week 6's huge pages:** an ABI violation ran correctly through 30 levels of recursion because nothing hit the misaligned SSE instruction; huge pages showed 1.00× because the benchmark was DRAM-bound, not TLB-bound, so the thing being fixed was not the bottleneck.

**The rule:** a null result is a *claim requiring evidence*, not proof the effect is absent. Before believing "no difference", confirm the benchmark actually spent its time doing the thing you meant to measure — count the operations, print an intermediate, check the disassembly.

---

## 5. You Measured the Machine's Mood

**Week 4's cache figures and Week 5's clock.** A single run on a shared, throttling laptop is noise, not data:

- The CPU governor is `powersave` (Week 5) — idle cores sit at 400 MHz and turbo under load, so a clock read at rest is meaningless and a first run is cold.
- The `O_DIRECT` figure varied 2× between runs (Week 7) — the drive's own cache, other activity, thermal state.

**The rule:** warm up, run many times, and report **median and range**, not a single number. State the machine's state (governor, load, temperature) or pin it. **A single number from a shared machine has no error bar and therefore says nothing.**

---

## 6. The Checklist

Everything above, as questions to ask before believing a benchmark:

| Ask | Because | Course example |
|---|---|---|
| **Did the compiler delete it?** | Dead-code elimination, constant folding | Week 0: loop → `movabs` |
| **Is the result consumed?** | An unused result is dead code | Week 5: accumulator chains |
| **Which layer am I measuring?** | Cache vs device differ by 63× | Week 7, 8 |
| **Did the code exercise the effect?** | A null result may miss the case | Week 1: denormals |
| **Is the bottleneck the thing I changed?** | Fixing a non-bottleneck shows nothing | Week 6: huge pages |
| **Warm-up, repeats, variance?** | One run is noise | Week 4, 7 |
| **Is the machine in a known state?** | Governor, thermals, load | Week 5 |
| **Does it match theory?** | A number with no model is unfalsifiable | Week 1: 2²¹ absorption |

**The last row is the most important and the most skipped.** Every headline result in this course was *cross-checked against a prediction*: the absorption index was $2^{21}$ by derivation and $2^{21}$ by measurement; the cache cliffs matched `lscpu`; the fault count matched the page count. **A measurement that agrees with a model you computed independently is trustworthy; a number that agrees with nothing is a guess with extra decimal places.**

---

## 7. Why This Is the Last Lecture Before the Frontiers

Because it is the meta-skill the whole eleven weeks was teaching. **The course did not ask you to memorise that DRAM costs 438 cycles; it asked you to be the kind of engineer who measures it, checks it against a model, and distrusts a number that measures nothing.**

**Every "verified" and "measured" in these notes was a small act of this discipline.** The facts will change — clock speeds, cache sizes, the specific mitigations — but the method does not: **look at what the machine actually does, not what you assume it does, and prove it with a measurement you have reason to trust.**

---

## 8. What to Take Away

1. **Almost every benchmark is wrong the first time.** That is normal; getting it right is the skill.
2. **The compiler deletes unobserved work** — Week 0's loop became a constant.
3. **Know which layer you measure** — cache and device differ by 63×.
4. **A null result is a claim, not a proof** — the denormal benchmark measured zeros.
5. **One run on a shared machine is noise** — warm up, repeat, report the range.
6. **Cross-check against a model.** A number that matches an independent prediction is trustworthy; one that matches nothing is not.

---

## Exercises

1. A loop benchmark reports 0.0000 s at `-O2`. List three ways to make the work survive the optimiser, and say what each prevents.
2. A colleague's "SSD benchmark" reports 400 000 IOPS. What one thing would you check first, and what would confirm it was really measuring the device?
3. A denormal benchmark shows no slowdown. Describe how you would prove the loop actually spent its time in the denormal range.
4. You get 4.1 s on one run and 5.3 s on the next for the same program. Give three causes and say how you would report the result honestly.
5. Pick any "verified" number from an earlier week and describe the independent model it was cross-checked against. Why does that cross-check make it trustworthy?
6. Explain why "measure, don't guess" and "cross-check against theory" are not in tension — why you need both.

---

*Next week: architecture frontiers, the final project, and the road ahead.*

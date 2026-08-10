# CS 201 · Computer Organization & Architecture
## Week 5 · Lecture 2 of 3
### Branch Prediction and Out-of-Order Execution

---

**Reading:** CS:APP §4.5.5–4.5.8, §5.7 · **Previous:** L16, the pipeline and its hazards

---

## 1. The Problem With Branches

The pipeline must fetch an instruction every cycle. At a conditional branch, **the target is not known until the condition is evaluated in the Execute stage** — several cycles after fetch needed the answer.

Three options: stall until it is known (disastrous — branches are roughly one instruction in five), or predict and be right, or predict and be wrong.

**Modern CPUs predict, and they are startlingly good at it** — 95–99% accurate on typical code. The whole design is built on that accuracy, which is why the failures are expensive.

---

## 2. What a Misprediction Costs

Everything fetched after the branch was wrong. **Flush the pipeline and restart** — on a 14-stage machine, roughly **15–20 cycles**, during which the processor does nothing useful.

At one instruction per cycle that is fifteen to twenty instructions thrown away, per mistake.

---

## 3. Measured: 8× From Sorting the Data

The classic demonstration. Sum the elements of an array that exceed a threshold:

```c
for (int i = 0; i < N; i++)
    if (data[i] >= 128)
        sum += data[i];
```

with `data` holding random bytes 0–255. **Then sort the array and run exactly the same loop.**

```
unsorted  0.2561 s   sum=6298632000
sorted    0.0319 s   sum=6298632000
ratio     8.03x   (identical data, identical sum)
```

*(Measured; a second run gave 8.70×.)*

**Same data, same comparisons, same answer, 8× the time.**

**Why.** On sorted data the branch is taken for a long run of elements and then not taken for the rest — the predictor learns it immediately and is right essentially always. On shuffled data the condition is a coin flip, so the predictor is wrong about **half** the time, and each mistake costs a pipeline flush.

---

## 4. The Twist: the Compiler Deletes the Branch

**That measurement required an extra compiler flag**, and the reason is the more useful lesson.

Compiled normally at `-O1`, the same program shows:

```
ratio     1.02x
```

*(Measured.)* **Sorting made no difference at all.** Looking at why:

```
    1213:  cmp    esi,0x7f
    1216:  cmovg  rcx,rdx
```

*(Verified.)* **GCC turned the `if` into a `cmov`.** There is no branch, so there is nothing to mispredict — exactly the transformation L08 §6 described, applied without being asked.

The 8× figure comes from `-fno-if-conversion`, which forbids it:

```
    1213:  jle    1205
```

**Three-way comparison, all measured:**

| Version | Time | Why |
|---|---:|---|
| Real branch, **sorted** | **0.0319 s** | Predicted correctly; the skipped `add` costs nothing |
| Branchless `cmov` | 0.0590 s | Never mispredicts, but **always** does the work |
| Real branch, **unsorted** | **0.2561 s** | ~50% misprediction, ~8× penalty |

> **This is the `cmov` trade from Week 2, quantified.** A conditional move is a **large win** when the
> branch is unpredictable and a **2× loss** when it is predictable, because it evaluates both sides
> unconditionally. GCC guessed that this branch was unpredictable — and on the shuffled data it was
> right.
>
> **And note what this means for the famous demonstration:** it no longer reproduces on a modern
> compiler at default settings. If you had run it and seen 1.02×, the correct conclusion is not
> "branch prediction does not matter" — it is **"look at what was actually compiled."**

---

## 5. How Predictors Work

**Static prediction**, from the compiler or a fixed rule: backward branches are predicted taken (loops usually repeat), forward branches not taken. Simple, and roughly 60–70% accurate.

**Dynamic prediction** — what real hardware does — keeps a table indexed by branch address:

| Scheme | Mechanism | Weakness |
|---|---|---|
| 1-bit | Remember the last outcome | A loop mispredicts **twice** per execution — on entry and exit |
| **2-bit saturating** | Four states; two consecutive misses to change the prediction | The standard baseline. A loop mispredicts once |
| **Correlating / global history** | Index by branch address **and** the last $n$ branch outcomes | Catches patterns like "if A was taken, B usually is" |
| **Tournament** | Several predictors plus a meta-predictor choosing between them | What modern CPUs actually use |

**Two special cases worth knowing:**

**The return-address stack.** `ret` is an indirect jump, and indirect jumps are hard to predict — but returns are perfectly predictable *if* you remember where the matching `call` came from. Every CPU keeps a small hardware stack of return addresses, pushed on `call` and popped on `ret`. **This is why Week 3's deeply recursive `fib` was not a disaster** despite being nothing but calls and returns.

**Indirect branch predictors** handle jump tables, virtual calls and function pointers. These are the hardest cases, and the reason a `switch` compiled to a jump table (L09 §5.3) can be slower than a comparison chain despite executing fewer instructions.

---

## 6. Speculation, and Why It Is Dangerous

The processor does not merely *predict* the branch — it **executes** past it, on the assumption the prediction holds. If the prediction was right, the work is already done. If wrong, the results are discarded.

**Discarding architectural results is easy.** Undoing the *microarchitectural* side effects is not.

**Speculatively executed loads leave lines in the cache.** The register writes are rolled back; the cache state is not. An attacker who can measure cache timing — which Week 4 gave you every tool to do — can learn something about data the program was never supposed to reveal.

**That is Spectre**, and it is a direct consequence of this lecture. Meltdown is the same idea against the user/kernel boundary. Week 9 returns to it.

> **The deep point:** these are not implementation bugs. They are the *intended* behaviour of
> speculation colliding with a security model that assumed only architectural state was observable.
> **Performance and isolation turned out to be in tension**, and the mitigations cost real
> throughput — some workloads lost 10–30%.

---

## 7. Out-of-Order Execution

Prediction keeps the front end fed. **Out-of-order execution keeps the back end busy.**

```c
mov  rax, [rbx]      ; cache miss -- 438 cycles (Week 4)
add  rax, 1          ; must wait
imul rcx, rdx        ; independent -- why should this wait?
```

An in-order machine stalls all three. An out-of-order machine issues the `imul` while the load is outstanding.

**The mechanism:**

1. **Register renaming** maps architectural names onto a much larger physical file, removing WAR and WAW (L16 §3).
2. Instructions wait in a **reservation station** until their operands are ready.
3. They **execute in any order** as operands and functional units become available.
4. A **reorder buffer** retires them in program order, so the architectural state updates as written.

**Execution is out of order; retirement is in order.** That is what preserves the illusion the ISA promises — Week 0's contract, upheld by machinery the contract never mentions.

**Superscalar** adds the other dimension: multiple instructions issued *per cycle*. This machine can issue about four. Combined with out-of-order execution, that is where L16's 4.00× came from — four independent chains, four issue slots.

---

## 8. What This Means for Your Code

| Do | Why |
|---|---|
| Make branches predictable | Sorting bought 8×. Structure data so conditions run in streaks |
| Remove branches from hot unpredictable code | `cmov`, arithmetic, table lookup — but only when unpredictable |
| **Break dependency chains** | Multiple accumulators. Worth 4× (L16 §5) |
| Keep loop bodies independent | Gives the out-of-order engine something to overlap |
| Do not hand-schedule instructions | The hardware reorders anyway; you cannot see its window |

**And do not guess which of these applies.** The `cmov` result above is the case in point — the compiler had already made the choice, and measuring the source-level change would have told you nothing.

---

## 9. What to Take Away

1. **Branches are ~20% of instructions** and their target is unknown at fetch.
2. **Prediction is 95–99% accurate**; a miss costs 15–20 cycles.
3. **Sorting the data was worth 8×** on identical work — but only with a real branch.
4. **GCC had already made it branchless**, giving 1.02×. Check what compiled before concluding.
5. **`cmov` wins on unpredictable branches and loses ~2× on predictable ones.**
6. **A return-address stack** makes `ret` predictable; indirect branches remain hard.
7. **Speculation leaves cache traces**, which is Spectre.
8. **Out-of-order execution, in-order retirement** — the ISA contract preserved by invisible machinery.

---

## Exercises

1. A branch is mispredicted 5% of the time on a 14-stage pipeline with a 17-cycle penalty. What is the average cost per branch, and what is the effective IPC if branches are 20% of instructions?
2. A 1-bit predictor on a loop executing 1000 iterations, run 100 times. How many mispredictions? Now with a 2-bit saturating predictor.
3. §4 shows `cmov` losing to a correctly predicted branch. Give the break-even misprediction rate, stating your assumptions about branch cost and the work `cmov` performs unconditionally.
4. Why is `ret` predictable when general indirect jumps are not? What breaks the return-address stack?
5. Explain why Spectre cannot be fixed by simply discarding speculative results more carefully.

---

*Next: L18 — SIMD, and the law that limits all of this.*

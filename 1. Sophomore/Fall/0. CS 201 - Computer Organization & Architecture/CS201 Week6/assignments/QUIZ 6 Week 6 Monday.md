# CS 201 · Quiz 6
## Administered: Monday, Week 6 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 5** — pipelining, hazards, branch prediction, out-of-order execution, SIMD and Amdahl.

**Instructions:** Closed notes. 10 minutes.

> **Unmarked, no weight.** Key below. Sit it closed-book first.

---

**Q1.** Does pipelining improve latency, throughput, or both? Explain in one sentence.

&nbsp;

&nbsp;

---

**Q2.** Which of RAW, WAR and WAW is a true dependency? What removes the others?

&nbsp;

&nbsp;

---

**Q3.** Forwarding makes ALU-to-ALU dependencies free but leaves the load-use hazard costing a cycle. Why?

&nbsp;

&nbsp;

---

**Q4.** Four independent accumulator chains ran 4.00× faster than one, on identical arithmetic. Why?

&nbsp;

&nbsp;

---

**Q5.** Sorting an array made a summing loop 8× faster — but only after a compiler flag was added. What had GCC done, and what was the unflagged ratio?

&nbsp;

&nbsp;

---

**Q6.** The same AVX2 loop gave 4.51× at 16 KiB per array and 1.07× at 16 MiB. Explain.

&nbsp;

&nbsp;

---

**Q7.** You speed up a routine by 4.5×. It is 40% of runtime. What is the overall speedup?

&nbsp;

&nbsp;

---

<div style="page-break-after: always;"></div>

---

## Answer Key — Mark Your Own

**Q1.** **Throughput only.** Each instruction still takes all five stages end to end; overlapping them means one *completes* per cycle rather than one every five.

---

**Q2.** **RAW is the true dependency** — it reflects the actual flow of a value from producer to consumer.

**WAR and WAW are naming artefacts**, arising only because the ISA has 16 register *names*. **Register renaming** removes them by mapping those names onto a much larger physical register file. It cannot remove RAW, because no amount of renaming produces the value earlier.

---

**Q3.** **A load's result is not available until the end of the M stage** — one stage later than an ALU result, which is ready at the end of E.

Forwarding can route a value sideways in time but not backwards, so the consumer's E stage must wait one cycle.

---

**Q4.** The single chain is **latency-bound**: each `addsd` must complete before the next can start. Four independent chains are **throughput-bound**: the out-of-order engine issues them in parallel across multiple execution units.

*Measured: 0.4768 s against 0.1191 s — exactly 4.00×. Eight chains give 7.25×, not 8×, as the limit moves to FP issue throughput.*

---

**Q5.** **GCC had performed if-conversion**, emitting `cmovg` — so there was no branch to mispredict and the ratio was **1.02×**.

The 8.03× appears only with `-fno-if-conversion`, which forces a real `jle`.

*The three-way result is worth remembering: predicted branch 0.0319 s, branchless `cmov` 0.0590 s, mispredicted branch 0.2561 s. **`cmov` is a large win on an unpredictable branch and a 2× loss on a predictable one.***

---

**Q6.** At 16 KiB per array the three arrays total 48 KiB and live in **L1/L2**; the memory system keeps up and the **vector units are the limit**, so widening them pays.

At 16 MiB they total 48 MiB against a **6 MiB L3** — the loop is **memory-bandwidth-bound**, the arithmetic units are idle waiting for DRAM, and making them wider changes nothing.

**A program is limited by one resource at a time. SIMD only helps if that resource is compute.**

---

**Q7.**

$$S = \frac{1}{0.6 + \frac{0.4}{4.5}} = \frac{1}{0.689} = \mathbf{1.45\times}$$

**A 4.5× win on 40% of the runtime is a 45% improvement.** This is the standard disappointment, and it is arithmetic rather than bad luck.

---

### What to Do With Your Score

| If you missed | Reread |
|---|---|
| Q1, Q2, Q3 | L16 §1–§4 |
| Q4 | L16 §5 |
| Q5 | L17 §3–§4 |
| Q6, Q7 | L18 §3 and §5 |

**Q5 and Q6 are the two that recur.** Both are instances of the same discipline — **find out what is actually limiting the program before you change anything** — which is the whole of Week 11.

---

*CS 201 · Week 6 · Quiz 6 · covers Week 5 · ungraded*

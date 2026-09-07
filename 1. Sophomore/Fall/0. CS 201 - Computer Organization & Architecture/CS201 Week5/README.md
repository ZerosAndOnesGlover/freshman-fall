# CS 201 · Computer Organization & Architecture
## Week 5: Pipelining, Instruction-Level Parallelism — and Midterm 1

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), ECE 110 (digital logic)
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **MIDTERM 1 (Monday evening)**, PS 5 (due Week 6 Friday), Lab 5, and **Quiz 5 on Monday, covering Week 4**.

---

## ⚠️ Midterm 1 — Monday, 18:00–19:15, VNC 100

**Covers Weeks 0–4. 100 points, 12.5% of the course grade. 75 minutes.**
**One handwritten A4 sheet, one side.** No calculator, no devices.

**Read [[CS201 Week5/resources/MIDTERM 1 Revision Guide|MIDTERM 1 Revision Guide]] before anything else this week.** It lists the six errors that recurred across four weeks of problem sets, gives a worked example of a full-mark answer, and tells you what is worth putting on your sheet.

The paper's largest section is **Q4, the memory hierarchy, at 24 marks** — Week 4, the most recent material. Do not let recency fool you into revising Week 0 hardest.

---

### Why This Week Exists

Because Week 4 explained why the processor spends most of its time waiting, and this week is about what it does *while* waiting — and what you can do to give it more to work with.

Three mechanisms, in increasing order of your control:

**Pipelining and out-of-order execution** happen whether you ask or not. The CPU overlaps independent work aggressively — **but it cannot invent independence that is not there.** Four accumulator chains ran exactly 4.00× faster than one, on identical arithmetic.

**Branch prediction** is 95–99% accurate and invisible until it fails. Sorting an array made an identical loop **8× faster** — though getting that measurement required stopping the compiler from removing the branch first.

**SIMD** is parallelism you declare. AVX2 gave **4.5×** — and then **1.07×** on the same instructions, once the arrays outgrew the cache.

**That last pair is the week's real lesson**, and it is the bridge from Week 4 to Week 11.

---

### Learning Objectives

By the end of Week 5, you should be able to:

1. Explain why pipelining improves throughput but not latency.
2. Identify structural, data and control hazards, and classify data hazards as RAW, WAR or WAW.
3. Explain which hazards register renaming removes, and why it cannot remove RAW.
4. Explain forwarding, and why the load-use hazard still costs a cycle.
5. **Measure the difference between latency-bound and throughput-bound code.**
6. State the misprediction penalty and estimate it from your own measurements.
7. Say when a conditional move beats a branch, and when it loses.
8. Describe out-of-order execution and why retirement must be in order.
9. Explain how speculation leaks information, and why Spectre is not a simple bug.
10. Write an AVX2 intrinsic loop, verify it, and measure it.
11. **Determine whether a loop is compute-bound or memory-bound before optimising it.**
12. Apply Amdahl's Law, and state Gustafson's objection.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[CS201 Week5/resources/MIDTERM 1 Revision Guide\|MIDTERM 1 Revision Guide]] | **Read first.** Six recurring errors, a worked full-mark answer, a revision plan |
| [[CS201 Week5/assignments/MIDTERM 1\|MIDTERM 1]] | The paper. Weeks 0–4, 100 points, 75 minutes |
| [[L16 The Pipeline and Its Hazards]] | Stages, hazards, forwarding, and 4.00× from breaking a chain |
| [[L17 Branch Prediction and Out-of-Order Execution]] | 8× from sorting — and why it took a compiler flag to see it |
| [[L18 SIMD and Amdahls Law]] | AVX2 from 4.5× to 1.07×, and the law that caps everything |
| [[PS 5 Identifying Hazards]] | Hazard analysis, dependency chains, prediction, Amdahl, SIMD |
| [[CS201 Week5/assignments/QUIZ 5 Week 5 Monday\|QUIZ 5 Week 5 Monday]] | Ten minutes on Week 4 — deliberately drawn from the paper's biggest section |
| [[LAB 5 Vectorising a Loop with AVX Intrinsics]] | Break a chain, vectorise by hand, then watch the speedup vanish |
| [[CS201 Week5/resources/Reading Guide Week 5\|Reading Guide Week 5]] | CS:APP §4.4–4.5 and §5.7–5.10, and what to skip in a midterm week |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A program is limited by one resource at a time, and every technique here only helps if it is the right one.**

The same AVX2 loop, unchanged, measured **4.51×** at 16 KiB per array and **1.07×** at 16 MiB. Identical instructions, identical work per element. At the small size the vector units were the limit; at the large size the loop was waiting for DRAM and the width of the arithmetic was irrelevant.

The same pattern appears twice more this week. **`cmov` is a large win on an unpredictable branch and a 2× loss on a predictable one.** **Four accumulators are worth 4.00× and eight are worth 7.25×**, because the limit moves from dependency latency to issue throughput.

**Amdahl puts a number on the disappointment:** a 4.5× win on 40% of the runtime is 1.45× overall.

---

### Assessment Reminder

**Labs and quizzes carry no weight**; the four weighted components already total 100%. Both remain required.

**Quiz 5 is Monday morning; the midterm is Monday evening.** The quiz covers Week 4 and is drawn deliberately from Q4's territory — treat it as the last diagnostic before the paper.

**PS 5 is due in Week 6**, so it does not compete with midterm revision. Q3 asks you to reproduce a famous benchmark, fail to reproduce it, and find out why — **the failure is the question**.

---

### Connections

**Back:** **Week 4** established that the processor waits; this week is what it does meanwhile, and the AVX sweep is a direct continuation of the memory-bound story. **Week 2's `cmov`** gets its cost/benefit measured. **Week 1's non-associativity** is why reductions will not vectorise. **Week 3's `ret`** is predictable only because of a dedicated return-address stack.

**Forward:** **Week 9's Spectre** is L17 §6 in full. **Week 10's multi-core** adds parallelism across cores to this week's parallelism within one. **Week 11 is this week made systematic** — the roofline model names the compute-bound/memory-bound distinction you measured in Lab 5, and Amdahl becomes the rule for choosing what to optimise at all.

**Sideways:** PROG 201's concurrency work is Amdahl's Law with threads instead of vector lanes, and the same ceiling.

---

*CS 201 · Week 5 · © CSE Department*

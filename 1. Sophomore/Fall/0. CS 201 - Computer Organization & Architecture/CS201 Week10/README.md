# CS 201 · Computer Organization & Architecture
## Week 10: Multi-Core, the GPU — and Midterm 2

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), ECE 110 (digital logic)
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **MIDTERM 2 (Monday evening)**, PS 10 (due Week 11 Friday), Lab 10 *(sat Tuesday of Week 11)*, and **Quiz 10 on Monday, covering Week 9**.

---

## ⚠️ Midterm 2 — Monday, 18:00–19:15, VNC 100

**Covers Weeks 5–9. 100 points, 12.5% of the course grade. 75 minutes.**
**One handwritten A4 sheet, one side.** No calculator, no devices.

**Read [[CS201 Week10/resources/MIDTERM 2 Revision Guide|MIDTERM 2 Revision Guide]] first.** It gives the six ideas the paper rewards, the ten numbers worth memorising, and the traps — and it is one question per week, evenly weighted, so no single week can be skipped.

---

### Why This Week Exists

Because Week 0 said the free lunch ended in 2005 and performance now comes from parallelism — and this is the week that parallelism turns out to be hard.

The multi-core machine is not a fast single core with more of it. It has private caches that must be kept **coherent**, a memory model that reorders your writes as **other cores can observe**, and a 64-byte line that makes threads **share data they never named**. Get any of these wrong and adding cores makes the program *slower* — which this week measures directly.

The GPU is the other answer: not a few fast cores but thousands of weak ones, winning on exactly the workloads — dense matrix multiply — that drove the whole post-Moore specialisation. **Both are the same lesson the course has taught all term: the bottleneck is data movement, and you must know your hardware to place data well.**

---

### Learning Objectives

By the end of Week 10, you should be able to:

1. State the coherence problem and why private caches create it.
2. Give the MESI states and trace them through a shared-write sequence.
3. Explain why a shared counter scales *negatively*, from the protocol.
4. Distinguish coherence from consistency, and give a store-load reordering.
5. Recognise **false sharing** from addresses, and fix it with alignment.
6. Explain NUMA and the first-touch rule.
7. Distinguish physical cores from hyperthreads, and predict where scaling stops.
8. Apply Amdahl's Law to threads.
9. Explain SIMT, warps and warp divergence.
10. Explain coalesced access and arithmetic intensity, and say when a GPU wins.
11. **Write multi-core code that scales: partition, private state, combine once.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[CS201 Week10/resources/MIDTERM 2 Revision Guide\|MIDTERM 2 Revision Guide]] | **Read first.** Six ideas, ten numbers, the traps, a plan |
| [[CS201 Week10/assignments/MIDTERM 2\|MIDTERM 2]] | The paper. Weeks 5–9, 100 points, 75 minutes |
| [[L31 Cache Coherence and the MESI Protocol]] | MESI, the negatively-scaling counter, coherence vs consistency |
| [[L32 False Sharing NUMA and Writing Code That Scales]] | False sharing measured, NUMA, Amdahl, the scaling rules |
| [[L33 The GPU and the SIMT Model]] | SIMT, divergence, coalescing, arithmetic intensity — conceptual, no GPU here |
| [[PS 10 Parallelism and Coherence]] | MESI, measured scaling, false sharing, the design, the GPU |
| [[CS201 Week10/assignments/QUIZ 10 Week 10 Monday\|QUIZ 10 Week 10 Monday]] | Ten minutes on Week 9 — samples the midterm's Week-9 part |
| [[LAB 10 Parallel Reduction and False Sharing]] | Scaling, contention, false sharing on the CPU; a GPU reduction to read |
| [[CS201 Week10/resources/Reading Guide Week 10\|Reading Guide Week 10]] | Patterson & Hennessy §5.10 and §6, and what the machine cannot show |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**On a multi-core machine, the bottleneck is a cache line moving between cores — not the arithmetic.**

Three measurements, all on this 4-core chip:

- **A single shared atomic counter did 64 M ops/s on one thread and ~20 M on two** — adding a core made it 3× slower, because the line bounces on every increment.
- **Four *separate* per-thread counters cost 1.45×** when they shared a 64-byte line — false sharing, contention with no shared variable, fixed by 56 bytes of padding.
- **An embarrassingly parallel workload scaled 3.90× on 4 cores and *fell* to 3.59× at 8 threads**, because there are only 4 physical cores.

**None of this is visible in the source or in Big-O.** It lives in the 64-byte line and the physical core count, and the way to write code that scales is always the same: **partition the work, give each partition private state, and combine once at the end.**

---

### Assessment Reminder

**Labs and quizzes carry no weight**; the four weighted components already total 100%. Both remain required.

**Quiz 10 is Monday morning; Midterm 2 is Monday evening**, covering Weeks 5–9. **Lab 10 is sat Tuesday of Week 11.**

**A note on hardware.** The lab machines have **no GPU** (`nvcc`/`nvidia-smi` absent) and **one NUMA node**, so L33 and the NUMA material are conceptual with cited figures, and Lab 10 runs its reduction on the CPU with the CUDA version provided to *read*. Everything measured is on the CPU. **Knowing which figures are measured and which are cited is, by now, part of the course.**

---

### Connections

**Back:** **Week 4's 64-byte line** is what makes false sharing possible. **Week 5's Amdahl and multiple accumulators** return as thread scaling and the private-partials design. **Week 5's roofline** is the GPU's arithmetic-intensity test. **Week 5's out-of-order execution** was one core reordering itself; consistency is reordering *other cores can see*.

**Forward:** **Week 11 makes all of this a method** — profile, find the bottleneck, and by now the bottleneck might be a bouncing line. **Week 12's domain-specific architectures** are the GPU's story generalised. **CS 202 (OS)** implements coherence-aware scheduling and NUMA placement; **CS 211 and PROG 202** cover the memory models formally.

---

*CS 201 · Week 10 · © CSE Department*

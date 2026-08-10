# CS 201 · Computer Organization & Architecture
## Week 4: Memory Hierarchy and Caches

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), ECE 110 (digital logic)
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** PS 4 (due Week 5 Friday), Lab 4, and **Quiz 4 on Monday, covering Week 3**.

> ⚠️ **MIDTERM 1 is next week — Week 5, covering Weeks 0–4.** This week is on it, and it is the week
> students most often underestimate. 12.5% of the course grade.

---

### Why This Week Exists

Because this is where the answer stops being in the source code.

For three weeks, "what does this compile to?" has answered your questions. **This week two loops compile to nearly identical instructions and differ by 30× in runtime.** Same work, same answer, same instruction count. The only difference is which addresses are touched in which order, and nothing in C expresses that.

**And the gap is not small.** A DRAM access on this machine costs about **107 L1 hits** — measured, not quoted. For any program whose data does not fit in cache, the processor spends most of its cycles waiting. Reducing memory traffic beats reducing instruction count, usually by a wide margin.

The week ends somewhere more uncomfortable: **the obvious explanation for a 3.29× speedup turns out to be wrong.** Blocking the transpose makes its L1 miss rate slightly *worse*. Finding out where the time really went is the skill this week is actually teaching.

---

### Learning Objectives

By the end of Week 4, you should be able to:

1. Explain why the hierarchy exists, in terms of what SRAM and DRAM each cost.
2. State this machine's latencies in cycles, and the DRAM-to-L1 ratio.
3. **Measure** cache sizes with a pointer chase, and read the cliffs.
4. Explain why memory moves in 64-byte lines, and count lines rather than bytes.
5. Distinguish temporal from spatial locality and name the lever each gives you.
6. Compute capacity from $S \times E \times B$, and split an address into tag / set index / offset.
7. Distinguish direct-mapped, set-associative and fully associative.
8. Classify a miss as compulsory, capacity or conflict — **and choose the intervention that matches**.
9. Explain write-back and write-allocate, and why writing an array reads it.
10. Apply blocking, derive a tile size, and measure the result.
11. **Read D1 and LLd miss rates and say which level is the bottleneck.**
12. **Recognise a null result as evidence rather than failure.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L13 The Memory Hierarchy Measured.md` | The staircase, the 107× ratio, the 64-byte line, and 30× from loop order |
| `lectures/L14 Cache Organisation Lines Sets and Ways.md` | $S$/$E$/$B$, the address split, three miss types, writes — and a fix that does not work |
| `lectures/L15 Locality as Leverage.md` | Blocking the transpose, where the speedup really comes from, and the control |
| `assignments/PS 4 Matrix Transpose Optimisation.md` | Measure the cliffs, block the transpose, diagnose the level, test a fix that fails |
| `assignments/QUIZ 4 Week 4 Monday.md` | Ten minutes on Week 3. **Unmarked — key in the paper.** Good midterm practice |
| `lab/LAB 4 Measuring Cache Effects.md` | Find the cache sizes with a stopwatch; then find out why blocking works |
| `resources/Reading Guide Week 4.md` | CS:APP Ch. 6, plus Drepper, and what cachegrind cannot see |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Diagnose the level before you choose the intervention.**

Blocking the transpose gave 3.29×. The D1 miss rate went **up**, 41.5% → 42.5%. The last-level miss rate **collapsed**, 41.5% → 13.5% — a 3.07× reduction in trips to DRAM, which is where the speedup came from.

An L1 miss caught by L2 costs ~12 cycles. One that reaches DRAM costs ~438. **Both appear identically in "D1 miss rate"**, and optimising that number would have told you this program got worse.

Then the same technique at $N = 512$, where everything fits in L3: **1.35×, and the last-level miss counts identical to four significant figures.** Blocking removes capacity misses; there were none to remove. **That null result is what makes the first one believable.**

---

### Assessment Reminder

**Labs and quizzes carry no weight**; the four weighted components already total 100%. Both remain required.

**Quiz 4 is Monday**, covering Week 3, key in the paper. **It is a fair sample of Midterm 1's style** — use it that way.

**PS 4 is almost entirely measurement.** Report what your machine did, including where it disagrees with the lecture. One question asks you to apply a standard fix and discover it does not help; **saying so is the correct answer** and is worth full marks.

**A note on tools:** `perf` is blocked on the lab image (`perf_event_paranoid = 4`, which needs root to change). The lab uses `valgrind --tool=cachegrind` throughout, which needs no privileges and is deterministic — but simulates no prefetching, no TLB and no out-of-order execution. **Where it disagrees with the stopwatch, the stopwatch wins.**

---

### Connections

**Back:** **Week 0's von Neumann bottleneck** stops being a historical note and becomes a number. **ECE 110's SRAM/DRAM week** explains why one is fast and small and the other slow and large. **Week 2's `lea`-heavy loops** are the ones whose instruction counts turn out not to predict runtime.

**Forward:** **Week 5's pipeline** is what the CPU does *while* waiting for memory, and Amdahl's Law explains why hiding it only goes so far. **Week 6's virtual memory** adds the TLB, which is a cache with the same $S$/$E$/$B$ structure over a different thing. **Week 10's cache coherence** is this week with four cores fighting over the same lines. **Week 11 is this week as a discipline** — profile, diagnose, intervene, re-measure.

**Sideways:** PROG 201's `mmap` and page cache work is the same hierarchy one level further out, with disk as the slow level.

---

*CS 201 · Week 4 · © CSE Department*

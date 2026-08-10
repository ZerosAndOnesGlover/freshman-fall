# CS 201 · Problem Set 4
## Matrix Transpose Optimisation — Exploiting Cache Locality

---

**Released:** Week 4, Wednesday · **Due:** Week 5, Friday 17:00
**Total: 100 points** · Submit one PDF plus a `.zip` of source, `PS4_{LastName}_{StudentID}.pdf`

> **This problem set is mostly measurement.** Every number you report must come from a run on your own
> machine, with the command shown. Report what you measured, including results that disagree with the
> lecture — machines differ, and a well-documented disagreement is worth full marks.
>
> **`perf` is blocked on the lab image** (`perf_event_paranoid = 4`). Use `valgrind --tool=cachegrind`.

---

### Q1: Cache Geometry (16 points)

**(a) [4]** Run `lscpu -C`. Report $S$, $E$, $B$ for L1d, L2 and L3, and **verify each capacity** from $S \times E \times B$.

**(b) [4]** For your L1d, split a 64-bit address into tag / set index / offset. Give the bit widths, and the set index and tag for address `0x7fff8a3c40`.

**(c) [4]** What byte stride causes every access to map to the **same L1d set**? Derive it from $S$ and $B$, and say what array dimension in `double`s would produce it.

**(d) [4]** Classify each as compulsory, capacity or conflict, with one sentence each:

1. The first read of a freshly allocated 1 GiB buffer.
2. Alternating between two 8 KiB arrays that happen to be 32 KiB apart in memory, on a direct-mapped 32 KiB cache.
3. Summing a 100 MiB array once, sequentially.
4. Repeatedly traversing a 10 MiB linked list in random order.

---

### Q2: Finding the Cliffs (20 points)

Build the pointer-chase benchmark from Lab 4 Part 2 and run it from 4 KiB to 32 MiB.

**(a) [6]** Report your table. **Identify the three working-set sizes at which the latency rises**, and compare each against your Q1(a) capacities. State how close they are.

**(b) [4]** Convert your four plateau latencies to **cycles**, stating the clock you used. Compare against the canonical 4 / 12 / 40 / 200+.

**(c) [4]** Compute the ratio of your DRAM latency to your L1 latency. Then express it as "one DRAM access costs about $N$ L1 hits", and say what that implies for a program whose working set does not fit in L3.

**(d) [6]** Replace the random cycle with a **sequential** one and re-run.

Expected on the lab machine *(verified)*:

| KiB | random | sequential |
|---:|---:|---:|
| 4 | 1.22 | 1.39 |
| 32 | 1.22 | 1.19 |
| 256 | 5.67 | 1.21 |
| 2048 | 14.83 | 1.33 |
| 8192 | 81.81 | 1.52 |
| 32768 | 128.94 | **1.55** |

**The staircase vanishes entirely.** At 32 MiB the sequential version is **83× faster than the random one on the same working set.**

Explain the mechanism. Then answer the harder question: **if the hardware can hide DRAM latency this completely, why does any of the rest of this problem set matter?**

---

### Q3: The Transpose (34 points)

Implement both transposes for `double`, $N = 2048$:

```c
void naive(void);              /* B[j*N+i] = A[i*N+j] */
void blocked(int b);           /* tiled, block size b */
```

**(a) [8]** Both implementations, plus a correctness check that `blocked(b)` agrees with `naive()` elementwise for every $b$ you test.

**(b) [6]** Time naive and blocked for $b \in \{8, 16, 32, 64\}$. Report a table with speedups. Reference values *(verified)*: naive 0.0608 s; $b=32$ gives 3.29×; $b=64$ gives 3.58×.

**(c) [6]** **Derive** the largest $b$ for which two $b \times b$ `double` tiles fit in your L1d, showing the arithmetic. Compare with your measured optimum and account for any difference.

**(d) [8]** Run cachegrind on naive and on your best $b$:

```bash
valgrind --tool=cachegrind --cache-sim=yes --cachegrind-out-file=/dev/null ./transpose 0
```

Report **D1 miss rate and LLd miss rate for both.**

You should find that **blocking makes the D1 miss rate slightly worse while the LLd miss rate collapses.** Reference *(verified)*: D1 41.5% → 42.5%; LLd 41.5% → 13.5%.

**Explain how a program can get 3.29× faster while its L1 miss rate rises.** Your answer must distinguish an L1 miss served by L2 from one served by DRAM.

**(e) [6]** In the naive run, LLd misses (5 244 472) are within 0.005% of D1 misses (5 244 694).

State what that means about the contribution of L2 and L3 to the naive version, and what it tells you about where to aim an optimisation.

---

### Q4: The Control (16 points)

Repeat Q3 at $N = 512$, where both matrices are 2 MiB and both fit in a 6 MiB L3.

**(a) [4]** Report wall-clock for naive and blocked. Reference *(verified)*: 0.0035 s and 0.0026 s — only **1.35×**.

**(b) [4]** Report LLd misses for both. Reference *(verified)*: **66 989 and 66 993** — identical to four significant figures.

**(c) [4]** What kind of miss are those ~67 000, and **why can no reordering of the loops reduce them?**

**(d) [4]** A classmate says the $N=512$ result shows blocking "does not really work". **Rebut it.** Explain why this result makes the $N=2048$ finding *more* believable rather than less, and name the general principle about interventions and the conditions under which they apply.

---

### Q5: Layout (14 points)

**(a) [5]** You have `struct particle { double x, y, z, vx, vy, vz; int id; char name[32]; };` and an array of 1 000 000 of them. A physics step reads and writes only `x, y, z, vx, vy, vz`.

Compute how many 64-byte lines the step touches with this layout, and how many it would touch under **struct-of-arrays**. State the ratio.

**(b) [4]** Give one concrete disadvantage of the struct-of-arrays layout, in terms other than performance.

**(c) [5]** A `double A[512][512]` traversed by column collides in L1 on every access.

**Show the stride arithmetic** — the byte stride between successive accesses, and why it maps every access to the same L1d set.

**Then test the standard fix.** Pad the row length to 513 and measure both wall clock and cachegrind's D1 miss rate.

Reference *(verified)*: D1 miss rate moves **95.0% → 93.7%**, and the padded version ran **marginally slower** (0.1324 s → 0.1347 s).

**The fix does not work here. Explain why**, in terms of which of the three miss types is actually dominating, and what `LLd miss rate = 0.6%` tells you about where those misses are being served from.

State the general principle this illustrates about choosing an intervention.

---

## Marks

| | |
|---|---:|
| Q1 Cache Geometry | 16 |
| Q2 Finding the Cliffs | 20 |
| Q3 The Transpose | 34 |
| Q4 The Control | 16 |
| Q5 Layout | 14 |
| **Total** | **100** |

---

*CS 201 · Week 4 · Problem Set 4*

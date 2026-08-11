# CS 201 · Week 11 · Reading Guide
## Performance Engineering

---

**Set reading:** CS:APP **Chapter 5** in full — "Optimizing Program Performance". This is the book's best-written chapter and the direct source for the whole week.
**Also:** the gprof and valgrind/callgrind manuals; the `perf` tutorial (for when you have a machine you own).
**Optional:** Williams, Waterman & Patterson, *"Roofline: An Insightful Visual Performance Model"* (2009) — the original paper, and short.

---

## The One Chapter to Read Properly

**CS:APP Chapter 5 is where this whole course's method is written down**, and it is worth reading twice. It works a single example — a vector-summing routine — from naive code to near-peak performance, applying every technique in order and *measuring each step*. **That worked example is Lab 11 and PS 11 in the book's own words.**

**Read it as a narrative, not a reference.** The order in which the authors apply the optimisations *is* the lesson: eliminate obvious waste, then break dependency chains, then use multiple accumulators, then vectorise — measuring after each, and stopping when the profile says the bottleneck has moved.

---

## Section by Section

| § | Topic | What to take from it |
|---|---|---|
| **5.1** | Optimizing compilers | What `-O2`/`-O3` do and *why they cannot do everything* — aliasing, side effects |
| **5.2** | Expressing program performance | CPE (cycles per element) — the book's unit of measure |
| **5.3** | Program example | The running example; follow it to the end |
| **5.4** | Eliminating loop inefficiencies | The free wins — hoisting, strength reduction |
| **5.5** | Reducing procedure calls | And why the compiler often does it for you |
| **5.6** | Eliminating memory references | Keep the accumulator in a register — Week 3 |
| **5.7** | **Understanding modern processors** | Latency vs throughput bounds — Week 5, and the roofline's compute roof |
| **5.8** | Loop unrolling | Why, and where it stops helping |
| **5.9** | **Enhancing parallelism** | **Multiple accumulators** — Week 5's 4.00×, in the book |
| **5.11** | Some limiting factors | Register spilling, branch prediction |
| **5.12** | Understanding memory performance | Load/store, the memory bound — Week 4 |
| **5.13** | **Life in the real world: performance improvement** | **The method, stated.** Profiling, Amdahl, honest measurement |
| **5.14** | Identifying and eliminating bottlenecks | gprof, the iterative loop |

---

## Questions to Read Against

**On §5.1, §5.13**

1. §5.1 says the compiler cannot optimise across a possible pointer alias. Give an example, and say what `restrict` promises.
2. §5.13/§5.14 describe the profile-and-optimise loop. State the five steps and which two beginners skip.
3. Knuth's premature-optimisation quote is in the folklore. Give it in full and explain what its *second half* licenses.

**On §5.7–5.9 — the processor**

4. Distinguish the **latency bound** from the **throughput bound**. Which does a single accumulator hit, and which do four accumulators reach? (Week 5 measured 4.00×.)
5. The book unrolls a loop and gets a small gain, then adds accumulators and gets a large one. **Which change did the real work, and why?**
6. At what accumulator count does the book's improvement stop? Relate it to the machine's issue width.

**On §5.12 and the roofline (beyond the book)**

7. Define arithmetic intensity. Compute it for vector add and for a large matrix multiply, and say which roof each is under.
8. A loop reorder gave 7.45× with identical flops. Which roof does that move you along, and what measurement confirms it?
9. The book's routine reaches near-peak. Sketch where it sits on a roofline before and after optimisation.

**On honest measurement**

10. Why does profiling a `-O2` build often attribute everything to `main`? Give the fix and its cost.
11. A benchmark reports 0.0000 s. What almost certainly happened, and how do you make the work survive?
12. Why is a null result ("no difference") a claim requiring evidence rather than a proof?

> **Question 5 is the one the chapter is really about.** Unrolling gets the credit in folklore;
> breaking the dependency chain does the work. The book's data separates them, and so should you.

---

## Reading Against the Machine

```bash
# 1. Profile a program and find the hotspot (Lab 11 Part 2)
gcc -O2 -pg -fno-inline prog.c -lm && ./a.out && gprof -b a.out gmon.out

# 2. Diagnose WHY it's slow — is it memory-bound?
valgrind --tool=cachegrind --cache-sim=yes ./prog     # D1 and LLd miss rates

# 3. The 7.45x loop reorder (Lab 11 Part 4)
#    Measure ijk vs ikj matmul; confirm the miss rate drops 50% -> 8%.
```

**Two tool notes for this machine:**
- **`perf` is unavailable** (privileges). Chapter 5 assumes it; substitute gprof + cachegrind. **On your own machine, learn `perf stat -d` and `perf record`/`report`** — they are what the industry uses.
- **Profile a build close to what ships** (`-O2 -fno-inline`), not the `-O0` debug build, which is hot in different places.

---

## Terminology You Should Own by Week 12

| | | |
|---|---|---|
| profiling | sampling vs instrumenting | gprof / perf / callgrind |
| hotspot | self vs cumulative time | call graph |
| Amdahl's Law | critical path | premature optimisation |
| cycles per element (CPE) | latency bound | throughput bound |
| loop unrolling | multiple accumulators | strength reduction |
| arithmetic intensity | roofline | ridge point |
| compute-bound | memory-bound | bandwidth ceiling |
| `-O2`/`-O3`/`-march=native` | `restrict` / aliasing | dead-code elimination |
| warm-up | variance / median | cross-check against theory |

---

## If You Want More

**The Roofline paper** (Williams et al., 2009) is six pages and introduces the model exactly as L35 uses it. **Read it** — it is one of the most practically useful papers in computer architecture, and it names the compute/memory distinction you have been measuring since Week 4.

**Brendan Gregg's *Systems Performance*** and his flame-graph work are the modern professional's toolkit. **Flame graphs** — a visualisation of sampled stacks — are the single most useful profiling output there is; his site has interactive examples worth an hour.

**Agner Fog's optimisation manuals** are the deep reference: instruction latencies, microarchitecture details, and hand-optimisation techniques. **You will not need them often**, but when a hotspot is genuinely instruction-bound, this is where the answer is.

**Denis Bakhvalov's *Performance Analysis and Tuning on Modern CPUs*** (free PDF) is the best current book-length treatment, and it is `perf`-centric — the right thing to read once you have a machine where `perf` works.

---

*CS 201 · Week 11 · Reading Guide*

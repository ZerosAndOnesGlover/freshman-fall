# PROG 201 · Lab 9
## Roofline Analysis — Finding Your Machine's Two Ceilings
### Covers Week 9 · sat **Monday of Week 10**, 15:00–16:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 9 and is sat in Week 10.** Lab *N* is sat on the Monday of Week *N+1*.
>
> **Project 1 and PS 8 were both due last Friday.** Marked Project 1 feedback comes back in Week 11.
> **PS 9 is due this Friday** — it is the optimisation exercise, and Part D of this lab is its
> method.
>
> **Unmarked.** The TA checks your work off in the session.

**What you are building:** a two-number model of your own machine, and then the judgement to use it.

By the end you will know, for the laptop in front of you, **how fast it can move data and how fast it can do arithmetic** — and you will have three kernels plotted against those ceilings, one of which is finished, one of which is not, and one of which is impossible.

**The impossible one is the lab.** A point above the roofline cannot exist, so when you produce one — and you will, in Part B — you have found a bug in your measurement rather than a fact about your machine.

---

## 0. Setup (5 minutes)

```bash
mkdir -p "$PROG201/week9/lab9"        # $PROG201 is set in ~/.bashrc -- see Lab 0
cd "$PROG201/week9/lab9"
cp "$ACADEMICS/1. Sophomore/Fall/2. PROG 201 - Systems Programming in C/PROG201 Week9/lab/"{roof.c,cache.c,sprof.c,target.c,vecbench.c,Makefile} .

make
./roof
```

The skeleton builds clean and reports placeholder ceilings of 1.00:

```
=== the two ceilings ===
  memory bandwidth       1.00 GB/s
  arithmetic peak        1.00 GFLOP/s
  ridge point            1.00 flops/byte
```

**Read `KEEP()` at the top of `roof.c` before you start.** It is one line of inline assembly that tells the compiler a value has escaped. Remove it from a loop and GCC deletes the loop, and the loop then takes zero seconds — which this course has now done to itself in three separate weeks.

---

## 1. Part A — Your Machine's Memory (20 min)

`cache.c` is provided complete. Run it:

```bash
./cache
```

It does two things. A **random pointer chase** over buffers of increasing size, which measures *latency* at each level of the hierarchy; and a **strided scan**, which shows you the cache line.

Ours:

```
=== latency against working-set size ===
         8 KiB         1.49 ns
        32 KiB         1.53
       128 KiB         3.13
       256 KiB         4.40
         1 MiB        11.84
         4 MiB        16.00
        16 MiB       107.68
       256 MiB       141.44

=== stride: 64 MiB of int ===
    stride   bytes   ns/element
         1       4         1.09
         4      16         2.01
        16      64         6.33
        32     128        14.52
        64     256        14.50
```

**Compare your step positions with what the machine says about itself:**

```bash
lscpu | grep -i cache
```

Q1 and Q3 are about these two tables. **Note the stride at which the second one stops rising** — it is not where you would expect from the cache line alone.

---

## 2. Part B — The Two Ceilings (35 min)

**TODO 1 — memory bandwidth.** Stream 256 MiB and report GB/s.

**Write the obvious loop first:**

```c
for (size_t i = 0; i < n; i++) s += a[i];
```

Run it. **Write the number down** — Q2 needs it. Then look at the kernel table `./roof` prints underneath, and find the row reporting **more than 100% of its roof.**

A kernel cannot exceed the roofline. The roofline is `min(peak, AI × bandwidth)` and it is an upper bound, so a point above it means one of three inputs is wrong: the flop count, the byte count, or **the ceiling itself**.

Then fix it. The hint, and it is the whole of Part B: **`s += a[i]` is a dependency chain.** Every iteration waits for the previous one's addition. You are measuring floating-point add latency, not memory bandwidth. Use **eight independent accumulators**, and `KEEP()` all of them.

Ours, before and after:

| | GB/s |
| --- | --- |
| one accumulator | **6.28** |
| eight accumulators | **13.71** |

**TODO 2 — arithmetic peak.** Independent FMAs, no memory at all, eight accumulators for the same reason. Each FMA is two flops.

Ours: **13.50 GFLOP/s**, giving a **ridge point of 0.98 flops per byte.**

**Write your ridge point down and say what it means in one sentence.** It is the single most useful number about your machine: below that arithmetic intensity, nothing you write can be anything but memory-bound.

---

## 3. Part C — The Kernels (25 min)

The kernels are provided. With correct ceilings, `./roof` gives:

```
  kernel                 AI      GFLOP/s         GB/s  % of roof
  sum (1 acc)         0.125         0.77         6.17        45%
  axpy                0.083         1.13        13.55        99%
  copy                0.000         0.00        10.78          -
  poly(deg 16)        4.000         2.47         0.62        18%
  poly4(deg 16)       4.000         7.14         1.79        53%
  poly(deg 64)       16.000         2.59         0.16        19%
  poly4(deg 64)       16.00         7.08         0.44        52%
```

**Sketch the roofline on paper** — log AI across, log GFLOP/s up, the slanted bandwidth line meeting the flat arithmetic line at your ridge point — and mark all seven points.

Three things to work out, and Q4–Q6 ask for them:

- **`axpy` is at 99%.** What, if anything, would you do to make it faster?
- **`poly(deg 16)` and `poly4(deg 16)` have identical arithmetic intensity and differ by 2.9×.** The roofline model cannot express the difference. What is it?
- **`sum (1 acc)` is at 45%** for exactly the reason your first TODO 1 was wrong. Say so in one sentence.

---

## 4. Part D — Two Ways to Be Wrong (15 min)

**(a) The compiler deletes your benchmark.**

Remove the `KEEP(s0)` … `KEEP(s7)` line from your bandwidth loop and re-run:

```bash
./roof | head -3
```

Then confirm it is not a timing fluke:

```bash
objdump -d roof | sed -n '/<bandwidth>:/,/ret/p' | wc -l
```

Q7. **This is not a hypothetical** — L30 §5 lists three times this course did it to itself.

**(b) `-O2` does not vectorise; `-O3` does.**

```bash
make vecbench
./vb_O2 16777216    # 64 MiB of int: out of cache
./vb_O3 16777216
./vb_O2 4096        # 16 KiB: fits in L1
./vb_O3 4096
```

Ours:

| | 64 MiB | 16 KiB |
| --- | --- | --- |
| `-O2` | 8.37 GB/s | 9.68 GB/s |
| `-O3` | **14.53 GB/s** | **46.28 GB/s** |

**Compare the 64 MiB `-O3` figure with your bandwidth ceiling from Part B.** Q8.

**If you have time**, profile something with the sampling profiler from L28:

```bash
./target
```

and then rebuild it without `-rdynamic` and look at what the profile becomes.

---

## 5. Questions

Answer in the answer sheet. Three or four sentences each unless stated.

**Q1.** Give your four latency plateaus and the sizes at which they change. Compare with `lscpu`'s cache sizes — do the steps land where they should? What is your L1-to-DRAM ratio?

**Q2.** Give your bandwidth with one accumulator and with eight. Explain the difference, and say what a single-accumulator loop is actually measuring.

**Q3.** Your stride table stops rising at some stride. Say where, give the byte distance, and explain why it is **not** the cache line size. *(Something in the hardware gives up at that point.)*

**Q4.** `axpy` is at 99% of its roof. Name two things that would make it faster and one thing that definitely would not, and say why for each.

**Q5.** `poly` and `poly4` have the same arithmetic intensity and the same flop count, and differ by about 3×. Explain, using two numbers about an FMA that you can look up.

**Q6.** *(Two sentences.)* State one thing the roofline model tells you that a profiler does not, and one thing a profiler tells you that the roofline does not.

**Q7.** Report what happened when you removed `KEEP`. Give the reported bandwidth, the `objdump` evidence, and say why a benchmark reporting an impossible number is more useful than one reporting a plausible wrong one.

**Q8.** Compare your `-O3` 64 MiB figure with your Part B ceiling. What does the comparison tell you about what `-O2` was doing wrong, and why is the 16 KiB gap so much larger than the 64 MiB one?

---

## 6. Checkoff

Show the TA:

- [ ] `./cache` output, and your L1-to-DRAM ratio said out loud.
- [ ] Your **wrong** bandwidth number and the roofline row above 100% that revealed it, then the fixed version.
- [ ] Your roofline sketch with all seven kernels on it.
- [ ] Your written answers to **Q2, Q5 and Q7**.

**If you finish early:** compute the arithmetic intensity of a naive *n*×*n* matrix multiply and of a tiled one, put both on your roofline, and then write the tiled version and see whether it lands where you predicted. That is the exercise the roofline paper was written for.

**Take with you:** **PS 9 is due Friday** and asks for a 5× speedup by analysis — Parts B and C are how you decide *what* to change, and L28 §7's method is how you decide *whether it worked*. Week 10 is security, where the thing being optimised is somebody else's program and the goal is different.

---

*PROG 201 · Week 9 · Lab 9 · © CSE Department*

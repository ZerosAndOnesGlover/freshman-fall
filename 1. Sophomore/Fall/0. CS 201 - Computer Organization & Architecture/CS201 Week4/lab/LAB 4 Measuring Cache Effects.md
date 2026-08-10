# CS 201 · Week 4 · Lab 4
## Measuring Cache Effects with Cachegrind

---

**When:** Tuesday 15:00–16:50, BH 210 · **Assessment:** unmarked, checked off by the TA
**You need:** `gcc`, `valgrind`, `lscpu`. **`perf` is optional — see the note below.**

---

## Before You Start: `perf` on the Lab Machines

The curriculum lists `perf` for this lab. **On the lab image it is blocked:**

```bash
$ cat /proc/sys/kernel/perf_event_paranoid
4
```

At level 4, unprivileged users get no hardware counters at all — `perf stat -e cache-misses` fails with a permissions message rather than a result. Enabling it needs root:

```bash
sudo sysctl kernel.perf_event_paranoid=1     # will not work without admin rights
```

**So this lab uses `valgrind --tool=cachegrind` throughout.** Cachegrind needs no privileges, works identically everywhere, and **simulates** the cache rather than counting real events — which has its own advantages (perfectly reproducible) and its own limits (no prefetching, no TLB, no out-of-order effects).

**Where the two disagree, the stopwatch is the referee.** Part 5 is built around exactly that.

---

## Part 1 — Ask the Machine Its Geometry (10 min)

```bash
lscpu -C
```

```
NAME ONE-SIZE ALL-SIZE WAYS TYPE        LEVEL SETS COHERENCY-SIZE
L1d       32K     128K    8 Data            1   64             64
L1i       32K     128K    8 Instruction     1   64             64
L2       256K       1M    4 Unified         2 1024             64
L3         6M       6M   12 Unified         3 8192             64
```

**Verify all three capacities** from $S \times E \times B$. Then answer:

1. How many bits of a physical address are the offset? The set index? *(L1d.)*
2. What byte stride causes every access to land in the **same L1d set**?
3. L1d is 32 KiB per core and there are four cores. Why is `ALL-SIZE` 128K but `ONE-SIZE` the number that matters for your program?

**✅ CHECKPOINT 1** — three verified capacities and your three answers.

---

## Part 2 — Find the Cache Sizes with a Stopwatch (30 min)

You are going to rediscover the numbers from Part 1 **without looking at them**, using only timing.

The trick is a **pointer chase**: each load's address comes from the previous load, so the CPU cannot prefetch and cannot overlap accesses. You measure true latency.

```c
/* chase.c — see the handout repo for the full listing */
for (long kb = 4; kb <= 32768; kb *= 2) {
    long n = kb*1024/sizeof(void*);
    void **p = aligned_alloc(64, n*sizeof(void*));
    /* build a RANDOM cycle through all n slots */
    /* ... shuffle indices, then p[idx[i]] = &p[idx[(i+1)%n]] ... */
    void **q = p;
    for (long i = 0; i < n; i++) q = (void**)*q;      /* warm */
    double t0 = now();
    for (long i = 0; i < reps; i++) q = (void**)*q;   /* measure */
    double t1 = now();
    printf("%8ld KiB   %7.2f ns\n", kb, (t1-t0)*1e9/reps);
}
```

Expected on the lab machine:

| KiB | ns | KiB | ns |
|---:|---:|---:|---:|
| 4 | 1.22 | 512 | 9.27 |
| 8 | 1.22 | 1024 | 12.12 |
| 16 | 1.19 | 2048 | 14.83 |
| **32** | **1.22** | 4096 | 30.39 |
| 64 | 2.50 | **8192** | **81.81** |
| 128 | 3.40 | 16384 | 113.54 |
| 256 | 5.67 | 32768 | 128.94 |

*(Verified.)*

### 2.1 Read the cliffs

**Plot it, or just read the column.** Identify the working-set size at which the cost first rises. **That is your L1d size — and you did not look it up.**

Do the same for the second and third rises. Compare all three against Part 1.

### 2.2 Convert to cycles

The lab machines turbo to 3.4 GHz. Convert your four plateau values to cycles and compare with the canonical figures every textbook quotes: **L1 ≈ 4, L2 ≈ 12, L3 ≈ 40, DRAM ≈ 200+.**

### 2.3 Why the random cycle

Replace the random permutation with a **sequential** cycle (`p[i] = &p[i+1]`) and re-run.

**The staircase largely disappears.** Explain why — what does the hardware do with a predictable address sequence that it cannot do with a random one?

**✅ CHECKPOINT 2** — your table, the three cliffs identified, cycle conversions, and the sequential-cycle result.

---

## Part 3 — Measure the Cache Line (20 min)

Walk a 256 MiB `int` array touching every $s$-th element:

```c
for (long i = 0; i < N; i += s) a[i]++;
```

| stride (ints) | bytes | ns/access |
|---:|---:|---:|
| 1 | 4 | 0.85 |
| 2 | 8 | 1.18 |
| 4 | 16 | 2.30 |
| 8 | 32 | 5.94 |
| **16** | **64** | **11.06** |
| 32 | 128 | 18.32 |
| 64 | 256 | 19.42 |

*(Verified.)*

**The cost per access climbs until stride 16 and then flattens.** $16 \times 4 = 64$ bytes.

**Answer:** why does it stop climbing there? What are you paying for at stride 8 that you are *also* paying at stride 4, and what fraction of it are you using in each case?

**✅ CHECKPOINT 3** — your stride table and the explanation of the plateau.

---

## Part 4 — Thirty Times From Two Lines (15 min)

```c
for (int i=0;i<N;i++) for (int j=0;j<N;j++) s += m[i*N+j];   /* row-major */
for (int j=0;j<N;j++) for (int i=0;i<N;i++) s += m[i*N+j];   /* col-major */
```

$N = 4096$, `int`:

```
row-major (i,j)   0.0086 s   sum=16777216
col-major (j,i)   0.3099 s   sum=16777216
ratio             35.98x
```

*(Verified. A second run gave 28.71×.)*

**Identical work. Identical answer.** Now confirm the instructions are also nearly identical:

```bash
gcc -O1 -S -masm=intel -o rowcol.s rowcol.c
```

Find both loops and compare. **The difference is not in the code.**

**✅ CHECKPOINT 4** — both timings and the observation from the assembly.

---

## Part 5 — Where the Speedup Really Comes From (35 min)

This is the part that matters.

### 5.1 Time it

$N = 2048$ `double` transpose, naive against blocked:

```
naive            0.0608 s   (1.00x)
blocked b=8      0.0250 s   (2.43x)
blocked b=16     0.0230 s   (2.65x)
blocked b=32     0.0185 s   (3.29x)
blocked b=64     0.0170 s   (3.58x)
```

*(Verified.)*

### 5.2 Now find out why — and be surprised

```bash
valgrind --tool=cachegrind --cache-sim=yes --cachegrind-out-file=/dev/null ./transpose 0
valgrind --tool=cachegrind --cache-sim=yes --cachegrind-out-file=/dev/null ./transpose 32
```

| | D1 miss rate | LLd miss rate |
|---|---:|---:|
| naive | 41.5% | **41.5%** |
| blocked $b=32$ | **42.5%** | **13.5%** |

*(Verified.)*

**Blocking made the L1 miss rate worse.** Sit with that before reading on.

**Answer:**

1. If L1 misses went *up*, where did a 3.29× speedup come from?
2. In the naive run, LLd misses (5 244 472) almost exactly equal D1 misses (5 244 694). What does that tell you about what L2 and L3 were contributing?
3. An L1 miss served by L2 costs ~12 cycles; one served by DRAM costs ~438. **Both appear in the same "D1 miss rate".** What does that imply about using D1 miss rate as your optimisation target?

### 5.3 The control

Rebuild with `N = 512` — both matrices are 2 MiB, so both fit in the 6 MiB L3 — and repeat.

```
naive          0.0035 s        LLd misses 66,989
blocked b=32   0.0026 s        LLd misses 66,993
```

*(Verified.)*

**Only 1.35× faster, and the LLd miss counts are the same to four significant figures.**

**Explain both.** What kind of miss are those 66 989, and why does no reordering reduce them? Why is this result *evidence that the $N=2048$ finding is real* rather than a disappointment?

**✅ CHECKPOINT 5** — both cachegrind runs, both timings, the control at $N=512$, and your three answers from 5.2.

---

## Before You Leave

| Task | Command |
|---|---|
| Cache geometry | `lscpu -C` |
| Simulate the cache | `valgrind --tool=cachegrind --cache-sim=yes ./prog` |
| Per-line annotation | `cg_annotate cachegrind.out.PID` |
| Real counters *(needs privileges)* | `perf stat -e cache-misses,LLC-load-misses ./prog` |
| Check whether perf will work | `cat /proc/sys/kernel/perf_event_paranoid` |

**The habit this lab builds:** when something is slow, ask *which level* is missing before you change anything. The D1 miss rate alone would have told you blocking made this program worse.

---

*CS 201 · Week 4 · Lab 4*

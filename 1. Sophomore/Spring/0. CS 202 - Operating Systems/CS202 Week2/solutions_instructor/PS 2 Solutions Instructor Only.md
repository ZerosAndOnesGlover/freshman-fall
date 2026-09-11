# CS 202 · Problem Set 2 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for PS 2.** Q1 and Q2 have exact expected output, and students who match it have implemented the rules as specified. **Students who do not match must be marked on their diagnosis, not only their output**: a one-millisecond difference that the student traces to "I charged the allotment after blocking instead of before" has understood Rule 4 better than one who matched by trial and error. Q3–Q5 are about reading tables and explaining them; **a correct table with no mechanism earns half.**

**The reference simulator** is `solutions_instructor/schedsim reference (do not distribute).c`. It was built from the same source as the student skeleton, and the skeleton's FCFS, SJF, SRTF and round-robin output is byte-identical to the reference's on `convoy`, `late` and `mixed`.

---

## Q1: MLFQ (30 points)

### The five `TODO`s, as the reference fills them

```c
/* preemption (step 3) */
case MLFQ: preempt = cand->level < cur->level || cur->quantum_used >= level_quantum(cur->level); break;

/* ordering (better) */
case MLFQ: return a->level != b->level ? a->level < b->level : a->seq < b->seq;

/* boost (step 2) */
if (policy == MLFQ && mlfq_boost > 0 && t > 0 && t % mlfq_boost == 0)
    for (int i = 0; i < njobs; i++)
        if (jobs[i].state != DONE) { jobs[i].level = 0; jobs[i].allot = 0; }

/* demotion (step 6) -- charged BEFORE the blocking check */
if (policy == MLFQ && j->used < j->cpu && j->allot >= mlfq_allot && j->level < mlfq_n - 1) {
    j->level++;
    j->allot = 0;
    demoted = 1;
}

/* naive rule, inside the blocking branch */
if (policy == MLFQ && mlfq_naive) { j->allot = 0; if (demoted) { j->level--; } }
```

### Reference output

```
$ ./schedsim mlfq:3:10:20:0 < workloads/mixed.txt
policy mlfq:3:10:20:0
job      arrival   cpu  finish turnaround response waiting wait/rdy
batch          0   300     330        330        0      30     30.0
edit           0    30     302        302       10      11      0.4
average turnaround 316.0 ms, average response 5.0 ms, 60 context switches, CPU busy 330 of 330 ms

$ ./schedsim mlfq:3:10:20:0:naive < workloads/gamer.txt
honest         0   200     400        400        0     200    200.0
gamer          0   200     241        241       10      19      0.8
average turnaround 320.5 ms, average response 5.0 ms, 46 context switches, CPU busy 400 of 400 ms

$ ./schedsim mlfq:3:10:20:0 < workloads/gamer.txt
honest         0   200     263        263        0      63     63.0
gamer          0   200     415        415       10     193      8.4
average turnaround 339.0 ms, average response 5.0 ms, 19 context switches, CPU busy 400 of 415 ms

$ ./schedsim mlfq:3:10:20:0:naive < workloads/starve.txt
long           0   100     900        900        0     800    800.0
i1             0   400     819        819       10      20      0.1
i2             0   400     820        820       11      21      0.1
average turnaround 846.3 ms, average response 7.0 ms, 802 context switches, CPU busy 900 of 900 ms

$ ./schedsim mlfq:3:10:20:100:naive < workloads/starve.txt
long           0   100     422        422        0     322    322.0
i1             0   400     899        899       10     100      0.2
i2             0   400     900        900       11     101      0.3
average turnaround 740.3 ms, average response 7.0 ms, 809 context switches, CPU busy 900 of 900 ms
```

### The mistakes that produce near-misses, and what each looks like

| Mistake | Symptom | Worth |
|---|---|---:|
| **Demotion checked only when the job did not block** | `starve.txt` without `:naive` shows the long job starving exactly as with `:naive` — a job blocking every millisecond is never charged. **The reference's first draft had this bug**, caught by exactly that symptom | half of the affected runs, full if diagnosed |
| Boost at *t* = 0 as well | usually invisible; changes nothing on these workloads | no deduction |
| Boost resets `level` but not `allot` | `starve.txt` with *S* = 100 gives the long job fewer ms per boost | half of that run |
| Quantum not doubled per level | `mixed.txt` batch turnaround and switch count differ | half of that run |
| Preempting only on quantum expiry, not on a higher-priority arrival | `mixed.txt` editor wait rises towards RR's 1.3 ms | half of that run |

---

## Q2: A Fair Scheduler (25 points)

### (a) [15] The `TODO`s, and the output

```c
/* ordering */
case FAIR: return a->vruntime != b->vruntime ? a->vruntime < b->vruntime : a->seq < b->seq;

/* arrival */
if (policy == FAIR) j->vruntime = min_vruntime();

/* wake-up: sleeper placement */
if (policy == FAIR) {
    double floor = min_vruntime() - fair_l / 2.0;
    if (j->vruntime < floor) j->vruntime = floor;
}

/* charge */
cur->vruntime += 1024.0 / cur->weight;

/* preemption */
case FAIR: {
    long total = 0;
    for (int i = 0; i < njobs; i++)
        if (jobs[i].state == READY || jobs[i].state == RUNNING) total += jobs[i].weight;
    double ideal = (double)fair_l * cur->weight / total;
    if (ideal < fair_g) ideal = fair_g;
    preempt = (cur->slice_used >= ideal && cand->vruntime < cur->vruntime)
           || (cand->wakeups > 0 && cand->seq >= woke_seq && cand->vruntime + fair_g < cur->vruntime);
    break;
}
```

```
$ ./schedsim fair:20:1 < workloads/nices.txt
n0             0   300     432        432        0     132    132.0
n5             0   300     697        697       14     397    397.0
n10            0   300     900        900       19     600    600.0
average turnaround 676.3 ms, average response 11.0 ms, 84 context switches, CPU busy 900 of 900 ms

$ ./schedsim fair:20:1 < workloads/mixed.txt
edit           0    30     301        301       10      10      0.3
average turnaround 315.5 ms, average response 5.0 ms, 60 context switches, CPU busy 330 of 330 ms
```

**The `woke_seq` test** — "has this job just woken, this millisecond?" — is the detail most students get wrong. **Without it, any ready job with less `vruntime` preempts at any time**, and `nices.txt` gives more switches and slightly different finish times. **Accept an equivalent test** (a per-job "woke this tick" flag) if the output matches.

**Marking:** 9 for `nices.txt`, 6 for `mixed.txt`.

### (b) [5] No wake-up preemption

```
batch          0   300     329        329        0      29     29.0
edit           0    30     330        330       10      39      1.3
average turnaround 329.5 ms, average response 5.0 ms, 59 context switches, CPU busy 330 of 330 ms
```

**Identical to `rr:10`, line for line.** With two jobs of equal weight the fair slice is 20 × 1024 / 2048 = **10 ms**, and with nothing else to trigger a switch, ordering by `vruntime` alternates the two jobs exactly as a FIFO queue does. **The fair scheduler's advantage for the editor came entirely from wake-up preemption.**

**Marking:** 2 for the wait (1.3 ms), 3 for "round robin with a 10 ms quantum" with the slice arithmetic.

### (c) [5] No sleeper placement

**`mixed.txt` does not change** — the editor still waits 0.3 ms per keystroke. **The editor sleeps only 9 ms at a time**, so its `vruntime` never falls more than about 10 ms behind the batch job's, and the floor at `min_vruntime − L/2` = 10 ms below never binds. **Removing a limit nobody reaches changes nothing.**

**`burst.txt` changes**:

| | Batch finishes | Napper finishes | Napper's total wait | Switches |
|---|---:|---:|---:|---:|
| with placement | **811** | 900 | 200 ms | 43 |
| **without** | **900** | **800** | 100 ms | 24 |

**The napper sleeps 200 ms, and during that time the batch job's `vruntime` rises by 200 ms and the napper's does not.** Without the floor, the napper wakes **200 ms "behind"** and — being always the smallest — runs its whole 100 ms burst without interruption, then sleeps and banks another 200. **The batch job is locked out for each burst**, and finishes last. With the floor, the napper wakes at most 10 ms behind, gets a short head start, and then shares.

**On a real machine**, a process that had slept for an hour would wake with an hour's credit and **could hold the CPU against every other task for up to an hour of its own computation.** Sleeper placement caps what sleeping is worth.

**Marking:** 2 for explaining why `mixed.txt` is unchanged, 2 for `burst.txt`'s mechanism, 1 for the hour.

---

## Q3: Choosing the Allotment (15 points)

Reference, `mlfq:3:10:A:0`:

| *A* | `gamer.txt`: honest | `gamer.txt`: gamer | `mixed.txt`: batch | `mixed.txt`: editor wait |
|---:|---:|---:|---:|---:|
| 5 | 245 | 417 | 315 | **5.5 ms** |
| 10 | 254 | 416 | 322 | 3.4 ms |
| **20** | 263 | 415 | 330 | **0.4 ms** |
| 50 | 317 | 409 | 330 | 0.5 ms |
| 100 | 335 | 407 | 330 | 0.6 ms |
| 1000 | 371 | 403 | 329 | 1.3 ms |

### (a) [6]

**The gamer never finishes first.** The honest job's lead **shrinks** as *A* grows — 172 ms at *A* = 5, 32 ms at *A* = 1000 — but never reverses.

- **Small *A*:** both jobs are charged for every millisecond, and sink quickly to the bottom level, where they share 40 ms quanta. The gamer gives up each quantum after 9 ms plus 1 ms of I/O it did not need, so it gets less CPU per turn than the honest job and finishes far behind.
- **Large *A* — larger than either job's 200 ms total:** nobody is ever demoted. **MLFQ is round robin with a 10 ms quantum at the top level.** The gamer still blocks after 9 ms of every turn, so it still loses a millisecond of CPU per turn to I/O — but everything runs at the same level, so the gap is only those milliseconds.

**Under the final Rule 4 gaming never pays**, because the resource consumed is charged whatever the job does in between. **A student who writes "the gamer wins at large *A*" has not run it**; deduct 3.

### (b) [5]

**Yes, a small allotment hurts the editor**: 5.5 ms per keystroke at *A* = 5 against 0.4 at *A* = 20. **The editor uses 1 ms per keystroke, and the allotment is cumulative** — at *A* = 5 it is demoted after five keystrokes, and after ten it is at the bottom **beside the batch job**, where each keystroke waits for the batch job's 40 ms quantum to end. **At *A* = 1000 neither job is ever demoted**, MLFQ is RR with 10 ms quanta, and the editor waits 1.3 ms — exactly L07's `rr:10`.

### (c) [4]

**Between 20 and 50 ms.** Large enough that an interactive job's short bursts do not sink it during a burst of typing (the editor's wait is 0.4–0.5 ms there), small enough that a CPU-bound job is identified within a couple of quanta and gaming gains nothing. **Any recommendation argued from both tables earns full marks**; one argued from only one table earns 2.

---

## Q4: The Voodoo Constant (15 points)

Reference, `mlfq:3:10:20:S:naive` on `starve.txt`:

| *S* | Long job: turnaround | Long job: waiting | i1 wait/rdy | i2 wait/rdy |
|---:|---:|---:|---:|---:|
| 0 (never) | **900** | **800** | 0.1 | 0.1 |
| 25 | **122** | 22 | 0.2 | 0.3 |
| 50 | 222 | 122 | 0.2 | 0.3 |
| 100 | 422 | 322 | 0.2 | 0.3 |
| 200 | 822 | 722 | 0.2 | 0.3 |
| 400 | 900 | 800 | 0.1 | 0.2 |

### (a) [7]

The long job gets **its 20 ms allotment at the top after every boost**, and nothing in between. **It finishes after about 100 / 20 = 5 boosts**: at *S* = 25 that is 122 ms; at 50, 222; at 100, 422; at 200, 822. **At *S* = 400 there are too few boosts before the interactive jobs finish at ~820 ms**, and the long job finishes at 900 as if there were none. The interactive jobs' wait barely moves — 0.1 to 0.3 ms — because the long job only ever takes 20 ms at a time from them.

**The plot is a straight line** of slope ≈ 4 from *S* = 25 to 200, then flat at 900.

### (b) [4]

**As *S* → the quantum and below, every job is back at the top almost continuously**, so no job stays demoted and **MLFQ becomes round robin at the top level**. It loses exactly what made it useful — the separation of long and short jobs — and the batch job in `mixed.txt` would compete with the editor on equal terms. *(At *S* = 25 on this workload the long job already gets 20 of every 25 ms when it wants them.)*

### (c) [4]

**Non-naive, *S* = 0:**

```
long           0   100     182        182        0      82     82.0
i1             0   400     899        899       10     100      0.2
i2             0   400     900        900       11     101      0.3
```

**The long job does not starve: 182 ms.** Under the final Rule 4 **the interactive jobs are charged for their milliseconds too**, so after 20 ms of CPU each they sink level by level, and everyone ends up at the bottom sharing round robin. **Starvation needed the naive rule's reset.**

**The boost is still needed** when a job **changes behaviour**: a job that was CPU-bound for a long time sits at the bottom level, and if it becomes interactive — an editor process that has just finished a long spell-check — it stays at the bottom, behind any CPU hogs, until something moves it up. `schedsim` cannot express a change of behaviour mid-job; **a clear description earns full marks.**

---

## Q5: The Model Against the Machine (15 points)

### (a) [5]

Reference, Linux (`share.c`) against the fair model on two-job workloads (`a 0 300 0`, `b 0 300 k`), B's share while both ran:

| B's nice | Linux | `fair:20:1` | Weights |
|---:|---:|---:|---:|
| 1 | 44.4% | 43.5% | 44.5% |
| 5 | 24.6% | 24.1% | 24.7% |
| 10 | 9.5% | 9.4% | 9.7% |
| 19 | 1.3% | **1.6%** | 1.4% |

**Nearly the same, and they should be**: both charge `vruntime` by the same weight table. **The model gives nice 19 slightly more** because of `fair_g`: its slice is at least 1 ms, and in 1 ms steps a job with weight 15 is never charged a fraction of a slice. A student who attributes differences to the 1 ms time step earns full marks.

### (b) [5]

**The model's slice** for *n* equal jobs is 20 / *n*, at least 1 ms: **10, 6.7 and 5 ms** for 2, 3 and 4 jobs — **it shrinks.** **Linux's measured run length was 3.00 ms for 2, 3 and 4 hogs** — **it does not**, and only the time waiting grew.

**What changed:** the model divides a fixed latency target among the runnable jobs, which is how CFS computed slices. **Linux 7.0's EEVDF gives each task its own slice** (`se.slice`, 2.8 ms) and orders tasks by a virtual deadline computed from it, so adding tasks lengthens the wait rather than shortening the slice. **Full marks require naming EEVDF or per-task slices**; "Linux uses a different algorithm" alone earns 2.

### (c) [5]

**Any two of**, each with a direction:

| Not modelled | Effect on the results |
|---|---|
| **Context-switch cost** — 1.6 µs plus lost cache warmth (Week 1) | penalises policies with many switches: `rr:1`, MLFQ's 802-switch `starve.txt` run; favours longer quanta in L07's sweep |
| **Several CPUs** | the long job in `starve.txt` would run on another CPU and never starve; MLFQ's and fair's advantages for the editor shrink when there is spare capacity |
| **Timer granularity** — decisions only on a 1 ms tick, and slack on wake-ups | wake-up preemption's 0.3 ms becomes up to a tick; latency figures rise |
| **Unpredictable I/O times** | the editor's 9 ms is exact here; real think times vary, which weakens MLFQ's inference from past behaviour |
| **Kernel work and interrupts** | steals time from every job; turnarounds all rise, proportionally more for short ones |

**Marking:** 2½ per item — 1 for the omission, 1½ for a defensible direction tied to a specific result.

---

*CS 202 · Week 2 · PS 2 Solutions · Instructor Only*

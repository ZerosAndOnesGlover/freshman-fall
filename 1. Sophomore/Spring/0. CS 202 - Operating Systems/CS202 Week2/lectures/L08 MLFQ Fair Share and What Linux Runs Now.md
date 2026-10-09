# CS 202 · Operating Systems
## Week 2 · Lecture 2 of 3
### MLFQ, Fair Share, and What Linux Runs Now

*“To our dismay, users who had been enduring several hour waits between jobs run under batch processing were suddenly restless when response times were more than a second.”* — Fernando J. Corbató, on CTSS, "On Building Systems That Will Fail", Turing Award Lecture (1991)

---

**Sat:** Wednesday of Week 2, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 8 and 9 · **Next:** L09, real time and what Linux lets you ask for

**Coursework:** 📝 **PS 2** released today, due Fri of Week 3 17:00 · 📝 **PS 1** due Fri this week 17:00 · 📊 **Quiz 3** Mon of Week 3 · 🔬 **Lab 2** Tue of Week 3 15:00–16:50 · 📘 **Midterm 1** Mon of Week 4 18:00–19:15

---

## 1. Learn a Job's Length by Watching It

L07 ended with two findings in tension. **SJF is optimal and needs job lengths nobody has. Round robin needs nothing and treats an editor like a compiler.** The *multi-level feedback queue* — first built for CTSS in 1962, and the ancestor of the schedulers in BSD, Solaris and Windows — resolves the tension by **observing** what SJF would have to be told.

**The rules**, in OSTEP's final form:

| Rule | |
|---|---|
| **1** | If A has higher priority than B, A runs |
| **2** | If A and B have the same priority, they run round robin, with that level's quantum |
| **3** | A new job starts at the highest priority |
| **4** | Once a job has used its **allotment** of CPU time at a level — **however many times it gave up the CPU along the way** — it moves down one level |
| **5** | Every *S* ms, move every job back to the top |

**The idea is Rule 4.** A job that computes for long stretches uses up its allotment and sinks; a job that runs for a moment and blocks barely touches its allotment and stays at the top. **Long jobs end up at the bottom and short ones at the top — SJF's order, discovered rather than declared.** Lower levels get longer quanta, so the jobs that sink also switch less.

`schedsim` with three levels, quanta of 10, 20 and 40 ms, and a 20 ms allotment per level, on L07 §7's editor-and-batch workload:

| Policy | Editor: wait per keystroke | Batch: turnaround | Switches |
|---|---:|---:|---:|
| FCFS | 10.0 ms | 300 | 1 |
| RR, 10 ms | 1.3 ms | 329 | 59 |
| RR, 50 ms | 8.5 ms | 305 | 11 |
| **MLFQ** | **0.4 ms** | **330** | 60 |

```
bbbbbbbbbbebbbbbbbbbbebbbbbbbbbebbbbbbbbbebbbbbbbbbebbbbbbbbbebbbbbbbbbebbbbbbbb
```

**The batch job sank to the bottom within 40 ms; the editor never left the top.** Every time a keystroke arrives, it outranks the batch job and runs at once. **MLFQ got the editor's wait below any round robin's without knowing anything about either job.**

---

## 2. Gaming the Scheduler

OSTEP's first version of Rule 4 was different, and simpler: **a job that gives up the CPU before its quantum ends keeps its priority**, and its allotment starts again. That rewards interactivity — and anyone who reads the rule can exploit it.

**`gamer.txt`**: an honest job that computes for 200 ms, and a job that computes for 200 ms **but blocks for 1 ms after every 9** — just before its 10 ms quantum would run out.

| Rule 4 | Honest job: turnaround | Gamer: turnaround | Gamer's wait per turn |
|---|---:|---:|---:|
| **reset on blocking** (OSTEP's first version) | **400** | **241** | 0.8 ms |
| **charge the allotment regardless** (the final version) | **263** | **415** | 8.4 ms |

**Under the naive rule the gamer finished in 241 ms and the honest job took 400** — the gamer ran as a top-priority "interactive" job for essentially all its 200 ms while doing exactly the same computation. **Under the final rule the order reverses**: the gamer's blocks do not reset anything, it sinks as fast as the honest job, and the extra second of I/O it inflicted on itself now only costs it.

> **Every scheduling policy that rewards a behaviour is a policy that pays people to fake it.**
> Rule 4's final form works because it charges for the resource actually consumed — CPU time —
> rather than for a behaviour correlated with it. Week 12's security reasoning starts here.

---

## 3. Starvation, and the Boost

**`starve.txt`**: one long job needing 100 ms, and two interactive jobs that each run 1 ms, block 1 ms, and repeat — **arranged so that between them the CPU is never idle.** Under OSTEP's naive rules the interactive jobs stay at the top forever:

| Boost every | Long job: turnaround | Long job: time waiting | Interactive jobs: turnaround |
|---|---:|---:|---:|
| **never** | **900** | **800** | 819, 820 |
| **100 ms** | **422** | **322** | 899, 900 |

**Without a boost, the long job ran for its first 20 ms, sank, and then did not run again until both interactive jobs had finished** — 800 ms of waiting for 80 ms of work. **That is starvation**: not a crash, not a deadlock, just a job that is always runnable and never chosen.

**With a boost every 100 ms**, the long job returns to the top periodically and gets a turn. It finishes in 422 ms; the interactive jobs finish 80 ms later, which is exactly the CPU the long job took. **The boost costs the favoured jobs precisely what it gives the starved one.**

**The boost solves a second problem too**: a job that was CPU-bound and becomes interactive — a compiler that finishes and hands control to an editor in the same process — is stuck at the bottom until something moves it up. The boost does.

**How often?** OSTEP calls *S* a *voodoo constant*: too large and long jobs starve for long periods; too small and interactive jobs lose their advantage. **PS 2 Q4 sweeps it.**

---

## 4. A Different Question: Shares, Not Priorities

MLFQ decides who runs **first**. A **proportional-share** scheduler decides what **fraction** each job gets, and never lets any job's fraction fall to zero. Two classic designs, and then the one that ran Linux for sixteen years:

- **Lottery** (Waldspurger & Weihl, 1994): each job holds tickets; each quantum, draw one at random. A job with 25% of the tickets gets about 25% of the CPU — on average, eventually.
- **Stride**: the deterministic version. Each job has a *pass* value; always run the lowest; add a *stride* inversely proportional to its tickets each time it runs.
- **CFS** (Linux 2.6.23, 2007): stride with the pass measured in **virtual runtime**.

**The CFS rule:** every task has a `vruntime`. When a task runs for Δ, charge it

> `vruntime += Δ × 1024 / weight`

and **always run the runnable task with the smallest `vruntime`**. A task with twice the weight is charged half as much per millisecond, so it can run twice as long before it stops being the smallest. **Its share of the CPU is its weight over the total.**

**The weight comes from `nice`**, through a fixed table: nice 0 is **1,024**, and **each step divides the weight by about 1.25** — nice 1 is 820, nice 5 is 335, nice 10 is 110, nice 19 is 15. The design goal was that **one step of nice changes a task's CPU share by about 10%**, whatever the other nice values are.

### Measured on the reference machine

`share.c` runs two CPU hogs on one CPU for four seconds, with the second hog given a different nice value or scheduling class, and reads each one's CPU time from `/proc`:

| Hog B | A's share | B's share | **Weights predict for B** |
|---|---:|---:|---:|
| nice 0 | 50.0% | 50.0% | 50.0% |
| nice 1 | 55.6% | **44.4%** | 820 / 1844 = **44.5%** |
| nice 5 | 75.4% | **24.6%** | 335 / 1359 = **24.7%** |
| nice 10 | 90.5% | **9.5%** | 110 / 1134 = **9.7%** |
| nice 19 | 98.7% | **1.3%** | 15 / 1039 = **1.4%** |
| `SCHED_BATCH`, nice 0 | 50.0% | 50.0% | 50.0% — batch changes preemption, not share |
| `SCHED_IDLE` | 99.7% | **0.3%** | 3 / 1027 = **0.3%** |

**Every row within 0.2 percentage points of the weight table.** The kernel's arithmetic is exactly what the design says. `SCHED_IDLE` is not a separate queue that runs only when nothing else will — it is a fair-class task with a weight of 3, which in practice amounts to nearly the same thing.

### The fair model in `schedsim`

`schedsim fair:L:G` models this: slices of *L* × weight / total weight, at least *G*; new jobs placed at the current minimum `vruntime`; a waking job placed no more than *L*/2 behind, and allowed to preempt at once if it is well behind the running job. On three equal jobs at nice 0, 5 and 10, it finishes them at **432, 697 and 900 ms** — shares close to the table's 70 / 23 / 8. **On the editor workload it gets the editor's wait to 0.3 ms**, slightly better than MLFQ, **without any priority levels at all**: a job that sleeps most of the time simply has less `vruntime` than a job that never sleeps.

---

## 5. Why a Red-Black Tree

CFS keeps runnable tasks in a **red-black tree ordered by `vruntime`**. OSTEP asks why, and the answer is in what the scheduler has to do:

| Operation | When | Heap | Balanced tree |
|---|---|---|---|
| find the smallest | every scheduling decision | O(1) | O(1) with a cached leftmost node |
| insert | a task wakes or is preempted | O(log *n*) | O(log *n*) |
| **remove an arbitrary task** | **a task blocks, exits, changes priority or moves to another CPU** | **O(*n*) to find it** | **O(log *n*)** |

**The third row decides it.** Tasks leave the runnable set from anywhere in the order — not only the front — and a heap cannot find an arbitrary element without searching. xv6's scheduler, by comparison, scans all 64 slots on every decision (L07 §8), which is O(*n*) and entirely reasonable for *n* = 64.

---

## 6. What Linux 7.0 Actually Runs: EEVDF

**Every textbook this course uses describes CFS. The reference machine does not select tasks the way CFS does**, and it is worth seeing the evidence before hearing the claim.

**The task's scheduling record**, from the reference machine's `include/linux/sched.h`:

```c
struct sched_entity {
    struct load_weight  load;
    struct rb_node      run_node;
    u64                 deadline;
    u64                 min_vruntime;
    ...
    u64                 vruntime;
    /* Approximated virtual lag: */
    s64                 vlag;
    /* 'Protected' deadline, to give out minimum quantums: */
    u64                 vprot;
    u64                 slice;
    ...
};
```

**`deadline`, `vlag` and `slice` are not CFS.** They belong to **EEVDF — *Earliest Eligible Virtual Deadline First*** — a 1995 algorithm by Stoica and Abdel-Wahab, which replaced CFS's selection rule in **Linux 6.6**. The fair class, `vruntime` and the weight table all remain; what changed is how the next task is picked:

1. A task is **eligible** if it has received no more than its fair share so far — its *lag*, the service it is owed, is not negative.
2. Each task has a **virtual deadline**: roughly, its `vruntime` plus its requested slice scaled by its weight.
3. **Among eligible tasks, run the one with the earliest virtual deadline.**

**The practical difference is latency.** CFS decided *when* a task ran purely from how much it had had; EEVDF also lets a task **ask for a shorter slice**, and a task with a shorter slice gets an earlier deadline and runs sooner — without getting more CPU overall.

**The kernel shows its per-task state** in `/proc/<pid>/sched`:

```
se.vruntime                                  :      14997556.890847
se.load.weight                               :              1048576
policy                                       :                    0
prio                                         :                  120
se.slice                                     :              2800000
```

`se.load.weight` is 1,024 × 1,024 — the nice-0 weight, stored with ten extra bits of precision. `prio` 120 is nice 0 on the kernel's internal scale, where 100–139 are the fair class. **`se.slice` is 2,800,000 ns: 2.8 ms.**

### Measuring the slice

`slice.c` puts *N* CPU hogs on one CPU. Each watches the clock in a tight loop, and treats any jump of more than 100 µs as time it was not running:

| Hogs on one CPU | Preemptions of hog 0 in 3 s | **Run length**, median | **Time off the CPU**, median |
|---:|---:|---:|---:|
| 2 | 507 | **3.00 ms** | 3.00 ms |
| 3 | 342 | **3.00 ms** | 6.00 ms |
| 4 | 250 | **3.00 ms** | 9.00 ms |

**The run length does not change as hogs are added. The wait does**, by exactly one slice per extra hog. Each hog gets a 3 ms slice and waits for everyone else's.

**3.00 rather than 2.8** because the kernel checks whether the running task has overrun its slice on the **timer tick**, and `CONFIG_HZ` is 1000 — so 2.8 ms of slice is noticed at the third millisecond. The p10–p90 range was 2.99–3.00 ms, which is as sharp as a scheduling measurement gets.

> **Compare the model.** `schedsim`'s fair policy gives each job *L* × weight / total, so its
> slices **shrink** as jobs are added. The kernel's did not. PS 2 Q5 asks you to explain the
> difference — which is one of the reasons Linux changed.

---

## 7. Groups, and a Setting That Does Nothing

Weights divide a CPU among tasks. **Linux also divides it among *groups* of tasks, first**, and then among the tasks inside each group. Two mechanisms do the grouping, and on the reference machine one of them is switched on and has no effect.

### Autogroup: enabled, and inert here

```
$ cat /proc/sys/kernel/sched_autogroup_enabled
1
$ cat /proc/self/autogroup
/autogroup-104502 nice 0
```

**Autogroup** puts every session in its own scheduling group, so that a `make -j8` in one terminal cannot drown out a video player started from another. With it working, two hogs in **different sessions** should split the CPU 50/50 whatever their nice values.

`share.c` tried it — the nice-19 hog called `setsid()` first:

| Hog B | B's share |
|---|---:|
| nice 19, same session | 1.3% |
| **nice 19, its own session** | **1.3%** |

**No difference.** The setting is on, each process reports an autogroup, and nothing happens. **The reason is where these processes live in the cgroup tree:**

```
$ cat /proc/self/cgroup
0::/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.gnome.Terminal.slice/vte-spawn-….scope
```

The CPU controller is enabled from the root down to `user@1000.service`, which makes `app.slice` a CPU group of its own. **Autogroups apply only to tasks in the root CPU group.** Every task started from this desktop is in `app.slice`'s group instead, so the kernel never consults its autogroup. **This is L02 §5's pattern again — a configured protection that does not operate — and it was found the same way: by measuring the thing the setting promises.**

### cgroup weights: they override nice

`systemd-run` can start a program in a new cgroup with a CPU weight. Starting the nice-19 hog that way, next to a nice-0 hog in the terminal:

```
$ systemd-run --user --scope -p CPUWeight=100 taskset -c 6 nice -n 19 ./hog
```

| While the scope ran | |
|---|---|
| `app.slice`'s `cgroup.subtree_control` | **`cpu memory pids`** — it was `memory pids` before |
| the terminal's slice `cpu.weight` | 100 |
| the new scope's `cpu.weight` | 100 |
| **nice-19 hog's share** | **58%** |

**Asking for a CPU weight made systemd switch the CPU controller on in `app.slice`**, which split the terminal's slice and the new scope into two groups of equal weight. **The kernel divided the CPU between the groups first — roughly half each — and only then among the tasks inside.** The nice-19 hog was alone in its group, so its nice value compared it with nobody. When the scope exited, the controller was switched off again.

> **`nice` ranks a task against the other tasks in its group. It says nothing about other
> groups.** On a machine where every service, container and desktop application is in its own
> cgroup — which is every modern Linux machine — the cgroup weights decide who gets the CPU, and
> nice decides only within them. Lab 2 has you reproduce both halves of this section.

---

## 8. What to Take Away

1. **MLFQ learns a job's length by watching it**: long jobs sink, short ones stay. On the editor workload it cut the wait per keystroke to 0.4 ms.
2. **Charge the resource, not the behaviour.** The naive Rule 4 let a gaming job finish in 241 ms against an honest one's 400; the final rule reversed it.
3. **Starvation is always-runnable, never-chosen**, and the boost fixed it — 900 ms to 422 — at exactly the cost of the favoured jobs.
4. **Proportional share gives fractions, not orders.** CFS charges `vruntime` in inverse proportion to weight, and each nice step is ×1.25.
5. **Linux's shares matched the weight table to 0.2 percentage points**, nice 1 through nice 19 and `SCHED_IDLE`.
6. **Linux 7.0 runs EEVDF, not CFS**: same weights and `vruntime`, selection by earliest eligible virtual deadline. **The measured slice was 3.00 ms whether two or four hogs competed.**
7. **CPU is divided among groups first.** Autogroup is enabled and inert here because these tasks are not in the root CPU group; a cgroup weight let a nice-19 hog take 58%.

---

## Exercises

1. Run `mlfq:3:10:20:0` on `gamer.txt` with the gamer blocking after 19 ms instead of 9 (edit the workload). Does it still win under the naive rule? Explain from the level quanta.
2. Using the weight table, what share does a nice-0 task get against **three** nice-5 tasks on one CPU? Check it with `share.c` modified for four hogs.
3. `slice.c` measured the time off the CPU as exactly one slice per other hog. **What would it measure if one of the other hogs were nice 19?** Predict, then run it.
4. Find your own terminal's cgroup with `cat /proc/self/cgroup`, and walk up the tree reading `cgroup.subtree_control` at each level. **Is autogroup live on your machine?** Test it with `share.c`.
5. EEVDF lets a task request a shorter slice through `sched_setattr`'s `sched_runtime` field for a `SCHED_NORMAL` task. Read `man 2 sched_setattr`. What does a shorter slice buy a task, and what does it not?

---

*CS 202 · Week 2 · L08 · © CSE Department*

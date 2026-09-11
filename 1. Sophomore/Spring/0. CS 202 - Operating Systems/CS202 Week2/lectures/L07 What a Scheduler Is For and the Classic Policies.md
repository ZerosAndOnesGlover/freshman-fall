# CS 202 · Operating Systems
## Week 2 · Lecture 1 of 3
### What a Scheduler Is For, and the Classic Policies

---

**Sat:** Monday of Week 2, 09:00–09:50, VNC 101, **after Quiz 2** · **Reading:** OSTEP Ch. 7 · **Next:** L08, MLFQ and fair share

---

## 1. The Question

Week 1 built the mechanism: save one process's registers, load another's, 1.6 µs. **It never said which one.** That is the scheduler's job, and it is a policy — replaceable, arguable, and measured by numbers that disagree with each other.

**The choice is smaller than it looks.** L01 counted 1,425 threads on the reference machine; L05 found **one** running and 261 asleep. The scheduler chooses only among the *runnable* ones — usually a handful per CPU — and it chooses again every few milliseconds, every time something blocks, and every time something wakes.

Two questions, then, and the whole week is their answers:

1. **Which** runnable task runs next?
2. **For how long**, before the scheduler is asked again?

---

## 2. What "Good" Means — Four Numbers That Disagree

For a job that arrives at time *T*<sub>arrival</sub>, first runs at *T*<sub>first run</sub>, and finishes at *T*<sub>completion</sub>:

| Metric | Definition | Who cares |
|---|---|---|
| **Turnaround time** | *T*<sub>completion</sub> − *T*<sub>arrival</sub> | batch work: compiles, simulations, backups |
| **Response time** | *T*<sub>first run</sub> − *T*<sub>arrival</sub> | anyone at a keyboard |
| **Waiting time** | time spent runnable but not running | both — it is the part the scheduler controls |
| **Throughput** | jobs finished per unit time | the machine's owner |

And a fifth that is not a number: **fairness** — does every job get a reasonable share, or can some wait forever?

**They conflict, and this lecture shows how.** A policy that minimises turnaround starves long jobs; a policy that minimises response pays in turnaround and in context switches. **There is no best scheduler — only a best scheduler for a stated goal.**

> **The numbers in this lecture come from `schedsim`**, a discrete-time simulator that advances
> in 1 ms steps and treats a context switch as free. PS 2 has you build its two hardest policies.
> **It is a model**: real switches cost 1.6 µs and lose cache warmth, and real jobs do not announce
> their length. Each simplification is dropped, one at a time, as OSTEP drops its assumptions.

---

## 3. First Come, First Served — and the Convoy

The simplest policy: **run jobs in the order they arrived, each to completion.** Fair in the everyday sense, trivial to implement, and on this workload terrible:

```
A 0 100        three jobs arrive at time 0:
B 0 10         one needs 100 ms of CPU,
C 0 10         two need 10 ms each
```

```
$ ./schedsim fcfs < convoy.txt
average turnaround 110.0 ms, average response 70.0 ms, 2 context switches
AAAAAAAAAA...(100 A)...AAAABBBBBBBBBBCCCCCCCCCC
```

**A finishes at 100, B at 110, C at 120: average turnaround 110 ms.** Two jobs that needed 10 ms each spent ninety of their milliseconds waiting behind one that did not need them to. This is the **convoy effect** — the same thing that happens at a supermarket till behind one very full trolley.

---

## 4. Shortest Job First Is Optimal — and Here Is Why

Run the shortest job first:

```
$ ./schedsim sjf < convoy.txt
average turnaround 50.0 ms, average response 10.0 ms, 2 context switches
BBBBBBBBBBCCCCCCCCCCAAAA...(100 A)...
```

**B finishes at 10, C at 20, A at 120: average turnaround 50 ms** — less than half of FCFS, with the same jobs, the same total work, and the same number of switches.

**SJF is provably optimal for average turnaround** when all jobs are present at once. The argument is an exchange:

- Suppose some schedule runs a longer job *L* immediately before a shorter job *S*.
- Swap them. *S* now finishes earlier by *L*'s length; *L* finishes later by *S*'s length; **every other job's completion time is unchanged.**
- The total changes by *S* − *L* < 0. **The swap strictly improves the sum.**
- So any schedule with a long job before a short one can be improved, and the only schedule that cannot is shortest-first.

**The argument depends on all jobs being there at the start.** Let the short jobs arrive 10 ms late:

```
A 0 100
B 10 10
C 10 10
```

| Policy | Avg turnaround | Avg response | What happened |
|---|---:|---:|---|
| FCFS | 103.3 ms | 63.3 ms | A runs to completion |
| **SJF** | **103.3 ms** | **63.3 ms** | **identical** — A was already running when B arrived, and SJF never interrupts |
| **SRTF** | **50.0 ms** | **3.3 ms** | B arrives, has less remaining than A, and **preempts** it |

**Shortest Remaining Time First** is SJF made preemptive: whenever a job arrives, compare its length with the *remaining* time of the running job, and switch if it is shorter. **It is optimal for average turnaround with arrivals** — the exchange argument, applied at every instant.

---

## 5. The Catch: Nobody Knows How Long a Job Is

SJF and SRTF need the one number a real operating system never has. A process does not say how long it will compute before it blocks, and it could not know if it tried.

**Classic systems estimated it from history**, with an exponential average of the length of each process's CPU bursts:

> τ<sub>n+1</sub> = α · t<sub>n</sub> + (1 − α) · τ<sub>n</sub>

where *t*<sub>n</sub> is the burst just finished, τ<sub>n</sub> the previous estimate, and α — commonly ½ — how much the recent past outweighs the distant one. **It works when behaviour is stable and fails when it changes**, which is exactly when it matters.

**Tomorrow's MLFQ is a different answer to the same problem**: rather than *predict* a job's length, **observe how it behaves and let that decide its priority**. A job that keeps using its whole slice is treated as long; a job that keeps blocking early is treated as short. No estimate, no formula — and, as L08 measures, a new way to be gamed.

---

## 6. Round Robin — Response Time, Bought With Turnaround

Give each job a fixed **quantum**, run it for that long or until it blocks, then move it to the back of the queue:

```
$ ./schedsim rr:1 < convoy.txt
average turnaround 59.7 ms, average response 1.0 ms, 30 context switches
ABCABCABCABCABCABCABCABCABCABCAAAAAAAA...
```

**Every job runs within 1 ms of arriving.** Round robin is the first policy here built for *response*, and it achieves it without knowing anything about the jobs. The price shows in the sweep:

| Quantum | Avg turnaround | Avg response | Context switches |
|---:|---:|---:|---:|
| 1 ms | 59.7 ms | **1.0 ms** | **30** |
| 2 ms | 59.3 ms | 2.0 ms | 15 |
| 5 ms | 58.3 ms | 5.0 ms | 6 |
| 10 ms | **56.7 ms** | 10.0 ms | 3 |
| 20 ms | 63.3 ms | 16.7 ms | 3 |
| 50 ms | 83.3 ms | 36.7 ms | 3 |
| 100 ms | 110.0 ms | 70.0 ms | 2 |

**Two things to read off it.**

- **At a quantum of 100 ms, round robin *is* FCFS** — no job ever uses up its quantum, so nothing is ever preempted, and the numbers match §3 exactly. At the other end, every job gets a turn almost immediately. **The quantum slides one policy into the other.**
- **Response improves as the quantum shrinks; switches grow in inverse proportion.** The simulator counts switches as free. **They are not**: L05 measured 1.6 µs each, and the loss of cache and TLB warmth that the measurement could not see is often worse. A 1 ms quantum spends most of its benefit on switching.

**Real kernels therefore choose quanta of a few milliseconds** — long enough that switching is a small fraction of each slice, short enough that nobody at a keyboard notices. L08 measures Linux's at exactly 3.00 ms.

---

## 7. The Workload That Breaks Every Policy So Far

Real machines run two kinds of job at once. **`mixed.txt`** has a 300 ms batch job and an editor that needs 1 ms of CPU for each keystroke and then waits 9 ms for the next:

```
batch 0 300
edit  0 30 1 9           # 30 ms of CPU in total: 1 ms bursts, 9 ms of I/O between
```

The number that matters for the editor is **how long each keystroke waits for the CPU** — the `wait/rdy` column, average wait each time it becomes runnable:

| Policy | Editor: wait per keystroke | Editor: turnaround | Batch: turnaround | Switches |
|---|---:|---:|---:|---:|
| FCFS | **10.0 ms** — and 300 ms before the first | 591 | **300** | 1 |
| RR, 10 ms quantum | 1.3 ms | 330 | 329 | 59 |
| RR, 50 ms quantum | **8.5 ms** | 546 | 305 | 11 |

**FCFS is perfect for the batch job and unusable for the editor.** Round robin with a short quantum is good for both, at the cost of 59 switches. **Lengthen the quantum to help the batch job and the editor waits almost as badly as under FCFS**, because every keystroke that arrives during the batch job's 50 ms turn waits for it to end.

**The trouble is that round robin treats both jobs the same.** The editor only ever wants a millisecond; the batch job always wants the whole quantum. **A policy that could tell them apart could give the editor the CPU the instant it wakes and let the batch job run in long, cheap slices the rest of the time.** L08 builds two — and on this same workload they get the editor's wait down to **0.4 ms** and **0.3 ms**.

---

## 8. xv6's Policy, Which You Now Recognise

`scheduler()` in `proc.c`, the part that chooses:

```c
for(;;){
  sti();
  acquire(&ptable.lock);
  for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
    if(p->state != RUNNABLE)
      continue;
    c->proc = p;
    switchuvm(p);
    p->state = RUNNING;
    swtch(&(c->scheduler), p->context);
    switchkvm();
    c->proc = 0;
  }
  release(&ptable.lock);
}
```

**This is round robin**, in the order of slots in the process table: run the first `RUNNABLE` process, and when it comes back, carry on down the table from the slot after it. **The quantum is the timer tick** — `trap()` calls `yield()` on every timer interrupt (L05 §3) — and measured from the host, **xv6 under QEMU takes 100.1 ticks per second: a 10 ms quantum.**

**What xv6's policy does not have** is the rest of this week:

- **no priorities** — a CPU hog and an interactive shell are treated identically;
- **no accounting** — xv6 does not record how much CPU any process has used, so no policy that depends on history is even possible without adding it;
- **no preemption on wake-up** — a process that becomes runnable waits for the current process's tick to end and for the table scan to reach it.

**Project 1, in Week 7, adds the accounting and a scheduler of your choice.**

---

## 9. What to Take Away

1. **A scheduler answers which and for how long**, choosing among runnable tasks — a handful, not 1,425.
2. **Turnaround, response, waiting, throughput and fairness conflict.** There is no best policy, only a best policy for a goal.
3. **FCFS suffers the convoy**: 110 ms average turnaround where SJF gets 50.
4. **SJF is optimal for turnaround by an exchange argument**, and SRTF extends it to arrivals — but both need job lengths no OS knows.
5. **Round robin buys response with turnaround and switches**; at a large enough quantum it becomes FCFS, and at a small one it spends its benefit on switching.
6. **Interactive and batch jobs want opposite things**, and treating them identically serves neither well.
7. **xv6 is round robin with a 10 ms tick**, no priorities and no accounting.

---

## Exercises

1. Run `schedsim` on `convoy.txt` with `srtf`. Why is it identical to `sjf` here, and different on `late.txt`?
2. Prove the exchange argument of §4 fails for average *response* time: construct three jobs for which SJF does not minimise it.
3. In the quantum sweep, turnaround is *lowest* at 10 ms, not at 1 ms. Explain why, using the timeline for `rr:10`.
4. Add a context-switch cost to `schedsim`: each switch consumes 1 ms of idle time. Re-run the quantum sweep. Where is the best quantum now?
5. xv6's scheduler always starts its scan at `ptable.proc[0]` after releasing and re-acquiring the lock. Is it truly round robin? Construct a situation in which a process in slot 0 runs more often than a process in slot 63.

---

*CS 202 · Week 2 · L07 · © CSE Department*

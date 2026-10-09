# CS 202 · Operating Systems
## Week 2 · Lecture 3 of 3
### Real Time, and What Linux Lets You Ask For

*“At the end of about a week, I called back and said, "I need something to compare this to. Could I please have a microsecond?"”* — Grace Hopper, interview on *60 Minutes* (24 August 1986)

---

**Sat:** Friday of Week 2, 09:00–09:50, VNC 101 · **Reading:** Silberschatz §5.6; `man 7 sched` · **Next:** Week 3, locks

**Coursework:** 📝 **PS 1** due today 17:00 · 📊 **Quiz 3** Mon of Week 3 · 🔬 **Lab 2** Tue of Week 3 15:00–16:50 · 📝 **PS 3** released Wed of Week 3, due Fri of Week 4 17:00 · 📘 **Midterm 1** Mon of Week 4 18:00–19:15

---

## 1. Deadlines, Not Averages

Everything so far optimised an **average** — turnaround, response, share. A **real-time** system has a different requirement: **each job must finish by its deadline, every time**. An anti-lock brake controller that computes the right answer 2 ms late, once in a million times, has failed.

The standard model is **periodic tasks**. Each task *i* is released every *P*<sub>i</sub> ms and needs *C*<sub>i</sub> ms of CPU before its next release — its deadline is its period. The fraction of the CPU it needs is its **utilisation**, *U*<sub>i</sub> = *C*<sub>i</sub> / *P*<sub>i</sub>, and the set's utilisation is the sum.

- **Hard real time**: a missed deadline is a failure. Brakes, pacemakers, flight control.
- **Soft real time**: a missed deadline is a degradation. Audio that clicks, a video frame dropped.

**Utilisation above 1 can never work.** Below 1, whether it works depends on the policy — and the two classic policies differ in exactly the way this lecture measures.

`rtsim.c` simulates periodic tasks on one CPU, all released at time 0, for one **hyperperiod** — the least common multiple of the periods, after which the pattern repeats — and reports every miss.

---

## 2. Rate-Monotonic: Fixed Priorities by Period

**Rate-monotonic scheduling (RM)** gives each task a fixed priority: **the shorter its period, the higher its priority.** Priorities never change, which makes RM simple to implement — every real-time operating system can do it — and easy to reason about.

**Liu and Layland proved in 1973** that *n* tasks are always schedulable under RM if

> *U* ≤ *n* (2<sup>1/n</sup> − 1)

| *n* | 1 | 2 | 3 | 4 | → ∞ |
|---|---:|---:|---:|---:|---:|
| **bound** | 1.000 | **0.828** | **0.780** | 0.757 | ln 2 ≈ 0.693 |

**The bound is sufficient, not necessary.** A task set above it may still be schedulable. `rtsim` on three tasks — 1 ms every 4, 2 ms every 6, 3 ms every 12:

```
$ ./rtsim rm "1/4 2/6 3/12"
RM: 3 tasks, utilisation 0.833, Liu-Layland RM bound 0.780, hyperperiod 12 ms
  first 12 ms: 1223132213..
  deadline misses in one hyperperiod: 0
```

**Utilisation 0.833, above the bound of 0.780, and no misses.** The bound could not promise this; the exact test can. **Response-time analysis** finds the worst-case finishing time *R* of each task by iterating *R* = *C*<sub>i</sub> + Σ ⌈*R* / *P*<sub>j</sub>⌉ *C*<sub>j</sub> over every higher-priority task *j*. For task 3:

| Iteration | *R* | 3 + ⌈*R*/4⌉·1 + ⌈*R*/6⌉·2 |
|---|---:|---:|
| start | 3 | 3 + 1 + 2 = 6 |
| | 6 | 3 + 2 + 2 = 7 |
| | 7 | 3 + 2 + 4 = 9 |
| | 9 | 3 + 3 + 4 = 10 |
| | 10 | 3 + 3 + 4 = **10** — converged |

**Task 3 finishes by 10 ms at worst, within its 12 ms deadline.** The simulation's timeline agrees: task 3's last millisecond is at *t* = 9.

**Now a set RM cannot schedule** — 2 ms every 5, and 4 ms every 7, utilisation 0.971:

```
$ ./rtsim rm "2/5 4/7"
RM: 2 tasks, utilisation 0.971, Liu-Layland RM bound 0.828, hyperperiod 35 ms
  t=7: task 2 missed its deadline with 1 ms left
  first 35 ms: 1122211222112.21122211222112221122.
  deadline misses in one hyperperiod: 1
```

**Task 2 misses at 7 ms, one millisecond short.** Task 1 is released again at 5 and, having the shorter period, takes the CPU back from task 2 just as task 2 is about to finish. The response-time iteration shows it: *R* = 4 → 4 + ⌈4/5⌉·2 = 6 → 4 + ⌈6/5⌉·2 = **8 > 7**.

---

## 3. Earliest Deadline First: Priorities That Change

**EDF** ignores periods and **always runs the task whose current deadline is soonest.** Priorities change at every release. The same task set:

```
$ ./rtsim edf "2/5 4/7"
EDF: 2 tasks, utilisation 0.971, Liu-Layland RM bound 0.828, hyperperiod 35 ms
  first 35 ms: 1122221122221121122211222211221122.
  deadline misses in one hyperperiod: 0
```

**No misses.** At *t* = 5, task 1's new deadline is 10 and task 2's is still 7, so task 2 keeps the CPU and finishes at 6.

**For independent, preemptible periodic tasks with deadlines equal to periods, EDF is optimal: it schedules every set with *U* ≤ 1.** No bound below 1, no response-time analysis. So why does anyone use rate-monotonic?

| | RM | EDF |
|---|---|---|
| Implementation | fixed priorities — every RTOS and interrupt controller has them | priorities recomputed at every release |
| **Under overload** (*U* > 1, briefly) | **the lowest-priority tasks miss; the important ones do not** | **misses can cascade**: a late task's deadline is soonest, so it keeps the CPU while every other task falls behind too |
| Guarantee | sufficient bound 0.69–1.0; exact test by iteration | exact: *U* ≤ 1 |

**The overload row is usually why.** A system designer can put the brake controller at the top of an RM system and know that whatever else goes wrong, it will not be the one to miss.

---

## 4. Linux's Scheduling Classes

Linux does not run one policy. It runs **classes**, strictly ordered: **a runnable task in a higher class always runs before any task in a lower one.** From the top:

| Class | Policies | Priority | What it is for |
|---|---|---|---|
| *stop* | *(internal)* | — | the kernel's own per-CPU work that must preempt everything |
| **deadline** | `SCHED_DEADLINE` | by deadline | **EDF**, with a *runtime*, *deadline* and *period* per task — §3, in the kernel |
| **real-time** | `SCHED_FIFO`, `SCHED_RR` | **1–99** | **fixed priorities** — §2's model. FIFO runs until it blocks; RR adds a quantum |
| **fair** | `SCHED_NORMAL`, `SCHED_BATCH` | nice −20 to 19 | everything else: L08's EEVDF |
| *ext* | `SCHED_EXT` | set by the loaded policy | **a scheduler written as a BPF program**, loaded at run time (Linux 6.12; `CONFIG_SCHED_CLASS_EXT=y` here) |
| **idle** | `SCHED_IDLE` | weight 3 | work that should use only otherwise-idle time |

```
$ chrt -m
SCHED_OTHER min/max priority    : 0/0
SCHED_FIFO min/max priority     : 1/99
SCHED_RR min/max priority       : 1/99
SCHED_BATCH min/max priority    : 0/0
SCHED_IDLE min/max priority     : 0/0
SCHED_DEADLINE min/max priority : 0/0
```

**`SCHED_RR`'s quantum is 100 ms** here (`/proc/sys/kernel/sched_rr_timeslice_ms`) — thirty times the fair class's slice, because real-time tasks are expected to block long before it matters.

---

## 5. What an Ordinary Account May Ask For

**Try each class from a student account on the reference machine:**

```
$ chrt -f 10 ./hog
chrt: failed to set pid 0's policy: Operation not permitted
$ chrt -r 10 ./hog
chrt: failed to set pid 0's policy: Operation not permitted
$ chrt -d --sched-runtime 1000000 --sched-deadline 10000000 --sched-period 10000000 0 ./hog
chrt: failed to set pid 0's policy: Operation not permitted
$ chrt -b 0 ./hog                  # SCHED_BATCH
$ chrt -i 0 ./hog                  # SCHED_IDLE
$ nice -n 10 ./hog
$ nice -n -5 ./hog
nice: cannot set niceness: Permission denied
```

| Request | Allowed? | Why |
|---|---|---|
| **`SCHED_FIFO`, `SCHED_RR`** | **no** — `EPERM` | `ulimit -r` (`RLIMIT_RTPRIO`) is **0** |
| **`SCHED_DEADLINE`** | **no** — `EPERM` | needs `CAP_SYS_NICE` |
| `SCHED_BATCH`, `SCHED_IDLE` | yes | asking for *less* is always allowed |
| nice +10 | yes | lowering your own priority is always allowed |
| **nice −5** | **no** | `ulimit -e` (`RLIMIT_NICE`) is **0** |

**The asymmetry is the point.** A `SCHED_FIFO` task at priority 99 in an infinite loop outranks **every** fair-class task on its CPU — including the shell you would use to kill it. **Any account that could do that could take a CPU away from every other user.** So the permission to raise priority is a privilege, and the permission to lower it is not.

**Even root's real-time tasks are fenced in:**

```
$ cat /proc/sys/kernel/sched_rt_runtime_us /proc/sys/kernel/sched_rt_period_us
950000
1000000
```

**Real-time tasks may use at most 950 ms of every 1,000 ms** on a CPU. The remaining 5% goes to the fair class, whatever the real-time tasks want — enough to run a shell and kill the runaway. **It is a deliberate violation of the real-time contract**, chosen because a hung machine is worse than a late task.

> **This is why Lab 2 cannot demonstrate `SCHED_FIFO` or `SCHED_DEADLINE` running.** It
> demonstrates the refusal instead, and measures the classes an account may use. The
> syllabus records the substitution.

---

## 6. Latency: How Late Is "Now"?

Real-time policy is about who runs first. **Latency is how long it takes for "first" to happen.** `lat.c` asks to wake up every millisecond, 3,000 times, and records how late each wake-up was — alone on a CPU, and with three CPU hogs competing:

| Situation | Median lateness | p99 | Max |
|---|---:|---:|---:|
| **no competition** | **0.144 ms** | 0.232 ms | 2.455 ms |
| 3 hogs, nice 0 | **0.054 ms** | 0.063 ms | 3.989 ms |
| 3 hogs, nice 19 | 0.054 ms | 0.065 ms | 2.374 ms |
| 3 hogs, `SCHED_IDLE` | 0.054 ms | 0.061 ms | 0.391 ms |

**Two results that look wrong.** Three hogs at nice 0 did not make the sleeper later — and **the sleeper was nearly three times later when nothing else was running at all.**

### Timer slack: 50 µs, on purpose

```
$ cat /proc/self/timerslack_ns
50000
```

**The kernel deliberately lets every timer fire up to 50 µs late**, so that timers due close together can be served by one wake-up — which saves power. A process may reduce its own slack with `prctl(PR_SET_TIMERSLACK)`. The same experiment with slack set to 1 ns:

| Situation | Median, 50 µs slack | **Median, 1 ns slack** | p99, 1 ns slack |
|---|---:|---:|---:|
| no competition | 0.144 ms | **0.093 ms** | 0.192 ms |
| 3 hogs, nice 0 | 0.054 ms | **0.004 ms** | 0.047 ms |
| 3 hogs, nice 19 | 0.054 ms | **0.004 ms** | 0.010 ms |
| 3 hogs, `SCHED_IDLE` | 0.054 ms | **0.004 ms** | 0.009 ms |

**Exactly 50 µs came off every busy-CPU median**: 54 µs was 50 µs of slack and 4 µs of actually waking up.

### An idle CPU is asleep

The remaining 90 µs in the no-competition row is the CPU itself. **An idle CPU does not spin; it enters a power-saving state**, and waking from a deep one takes time:

```
$ for s in /sys/devices/system/cpu/cpu7/cpuidle/state*; do …; done
state1   C1     latency    2 us
state2   C1E    latency   10 us
state3   C3     latency   70 us
state4   C6     latency   85 us
state6   C8     latency  200 us
state8   C10    latency  890 us
```

**With hogs on the CPU, it never goes idle, so there is nothing to wake from.** Alone, it sleeps between the 1 ms wake-ups — in states whose exit latency is tens to hundreds of microseconds. **The fastest way to be woken promptly on this machine is to have somebody else keeping the CPU busy**, which is why latency-sensitive systems disable deep idle states.

**And the hogs cost nothing because of L08 §4:** a task that sleeps for a millisecond at a time has far less `vruntime` than a hog, so when it wakes it is eligible with an early deadline and preempts the hog at once. **The p99 column shows the difference the hogs' priority makes** — 47 µs at nice 0, 10 µs at nice 19 — in the rare cases where the sleeper had to wait for the hog's current slice to be checked.

**The maxima of 2–4 ms are not explained by this experiment.** They happen a few times in 3,000 wake-ups, with and without competition; finding their cause would need tracing the kernel, which the account cannot do. They are reported, not rounded away.

---

## 7. What xv6 Has, and What Project 1 Adds

xv6's scheduler (L07 §8) is round robin with a 10 ms tick, **no classes, no priorities, no accounting, and no preemption on wake-up**. A process that wakes waits for the running process's tick to end and for the table scan to reach it — **up to 10 ms of latency** on a machine where Linux measured 4 µs.

**Project 1**, assigned in Week 7, has you add to xv6: a system call to set a process's priority, **the accounting that any history-based policy needs**, and a scheduler that uses them — MLFQ, lottery, or a fair scheduler — measured with the tools you built in PS 2.

---

## 8. What to Take Away

1. **Real-time means every deadline, not a good average**; utilisation over 1 never works.
2. **Rate-monotonic**: fixed priority by period, schedulable below *n*(2<sup>1/n</sup> − 1) — and sometimes above it, which response-time analysis decides. `1/4 2/6 3/12` at 0.833 had no misses.
3. **EDF schedules anything with *U* ≤ 1** — `2/5 4/7` at 0.971, where RM missed at 7 ms — but can cascade under overload, which is why RM is used anyway.
4. **Linux runs classes in strict order**: deadline, real-time, fair, idle — and now BPF-defined ones.
5. **Asking for more CPU is a privilege and asking for less is not.** `SCHED_FIFO`, `SCHED_RR`, `SCHED_DEADLINE` and negative nice were all refused; real-time tasks are capped at 95% even for root.
6. **Latency on this machine was 50 µs of deliberate timer slack plus 4 µs of waking**, and **an idle CPU added 90 µs** from its sleep states.

---

## Exercises

1. Find the largest *C* for which `rtsim rm "1/4 2/6 C/12"` has no misses. Check your answer by response-time analysis before running it.
2. Construct a three-task set with *U* ≤ 1 that EDF schedules and RM does not, where **the task that misses under RM has the longest period.** Is that always the task that misses?
3. `SCHED_RR`'s quantum is 100 ms and EEVDF's slice 2.8 ms. Why would it be a mistake for a real-time round-robin quantum to be as short as the fair class's?
4. Run `lat.c` with `taskset` pinning it to a CPU that is doing heavy work in *another* program on your machine (a browser tab playing video, say). What changes, and why?
5. Read `man 7 sched` on `SCHED_DEADLINE`'s admission control. Given `sched_rt_runtime_us` = 950,000, **what is the largest total utilisation of deadline tasks the kernel will admit on one CPU?**

---

*CS 202 · Week 2 · L09 · © CSE Department*

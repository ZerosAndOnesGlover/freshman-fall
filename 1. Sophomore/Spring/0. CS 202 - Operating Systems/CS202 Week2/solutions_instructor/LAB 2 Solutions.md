# CS 202 · Lab 2 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Tuesday of Week 3, 15:00–16:50, BH 210. **Unmarked** — checked off in the session.

**What the session is actually for.** Students arrive believing that `nice` sets priority and that `chrt` makes things real-time. They leave having measured `nice` doing exactly what its weight table says — **within a group** — and having met three things the scheduler will not do for them: raise priority, run real-time, and honour an autogroup setting that is switched on.

**Q5 is the one that changes how students think.** A nice-19 process getting more CPU than a nice-0 one, reproducibly, is the most counter-intuitive thing in the week, and it is true on every modern desktop.

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–5 | Setup | Check `nproc`; on a 4-CPU laptop use CPUs 2 and 3 |
| 5–25 | A — `nice` | Remind them to `pkill -x hog` before Part B |
| 25–40 | B — refusals | Fast. Ask each student why lowering nice is allowed |
| 40–60 | C — groups | **The path walk is where students get lost.** Do one on the projector |
| 60–75 | D — slices | |
| 75–100 | E — latency | Students with laptops on battery may see very different idle-state behaviour. That is a finding, not a failure |
| 100–110 | Checkoff | `pgrep -x hog` must be empty |

---

## Answers

All reference figures from the reference machine: i5-8250U, Ubuntu 24.04.4, kernel 7.0, running the lab's commands as written.

### Q1 — `nice` shares

| B's nice | A's ticks | B's ticks | B's share | **Weights predict** |
|---:|---:|---:|---:|---:|
| 0 | 200 | 200 | 49.9% | 50.0% |
| 1 | 222 | 178 | **44.4%** | 44.5% |
| 5 | 301 | 99 | **24.7%** | 24.7% |
| 10 | 362 | 39 | **9.7%** | 9.7% |
| 19 | 395 | 6 | **1.4%** | 1.4% |

**Worst row: 0.1 percentage points.** *(cpushare.sh's percentages sum to 99.8–99.9% because its denominator has a tiny constant added to avoid division by zero.)*

### Q2 — undoing `renice`

```
renice: failed to set priority for 1706837 (process ID): Permission denied
ulimit -e: 0
```

**`RLIMIT_NICE` is 0**, so an unprivileged process may only raise its nice value. **If lowering were unrestricted**, any user could set every one of their processes to nice −20 — a weight of 88,761 against 1,024 — and take about 99% of a CPU from every other user's nice-0 work on it. **Raising your own nice only costs yourself**, so it needs no permission.

### Q3 — policies and refusals

```
chrt: failed to set pid 0's policy: Operation not permitted     (chrt -f 10)
chrt: failed to set pid 0's policy: Operation not permitted     (chrt -d ...)
ulimit -r: 0
```

`SCHED_IDLE` against nice 0: **399 ticks against 1 — 0.2%**, implying a weight of about 1,024 × 1/399 ≈ **2.6**, consistent with the kernel's weight of **3** for idle tasks within the resolution of a 4-second, 100-tick-per-second measurement.

`sched_rt_runtime_us` / `sched_rt_period_us` = **950,000 / 1,000,000**: **real-time tasks together may use at most 95% of each second on a CPU.** It applies to root too because **a runaway `SCHED_FIFO` task outranks every fair-class task, including the shell an administrator would use to kill it** — the 5% reserve is what keeps the machine recoverable.

### Q4 — autogroup

```
/proc/1707087/autogroup:/autogroup-104559 nice 0
/proc/1707082/autogroup:/autogroup-104557 nice 0
pid 1707082  nice   0  ...  395 ticks   98.5%
pid 1707087  nice  19  ...    6 ticks    1.4%
```

**Different autogroups; no change in share.** The reference path walk:

```
/sys/fs/cgroup:                                              cpu memory pids
/sys/fs/cgroup/user.slice:                                   cpu memory pids
/sys/fs/cgroup/user.slice/user-1000.slice:                   cpu memory pids
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service: cpu memory pids
.../user@1000.service/app.slice:                             memory pids
.../app.slice/app-org.gnome.Terminal.slice:                  memory pids
```

**`user@1000.service` is the deepest cgroup that enables `cpu` for its children**, so **`app.slice` is a CPU group**, and every process started from the desktop is inside it. **Autogroups apply only to tasks in the root CPU group**; these tasks are not in it, so the kernel never uses their autogroup. **Student paths in BH 210 will differ** — logged in over SSH, or on a console, the chain ends in a `session-N.scope` — but the reasoning is the same: find where `cpu` stops being enabled, and whether the task is below a CPU group.

**Accept** a student whose machine *does* show autogroup working, if they show that their task is in the root CPU group. That is a correct and better answer.

### Q5 — a cgroup weight beats `nice`

```
B cgroup: /user.slice/user-1000.slice/user@1000.service/app.slice/run-rb32ee182a543444e9a97ca46cbf70039.scope
parent subtree_control during: cpu memory pids
pid 1707133  nice   0  ...  168 ticks   42.1%
pid 1707136  nice  19  ...  231 ticks   57.8%
parent subtree_control after: memory pids
```

**The three sentences:** asking systemd for a `CPUWeight` made it **enable the `cpu` controller in `app.slice`**, which turned the terminal's slice and the new scope into two separate CPU groups of equal weight (100 each). **The kernel divides a CPU between groups first**, so each group got about half, and **the nice-19 hog was the only task in its group**, so its nice value compared it with nothing. On a machine where every service is its own cgroup, **`nice` decides only among the tasks inside one service**, and the cgroup weights decide everything else.

**Why 57.8% rather than 50%:** the terminal's slice contains other tasks — the shell running `cpushare.sh`, the terminal emulator — which take a little of A's group's half. **Accept any reasonable explanation of the imbalance, or none**; the half-and-half shape is what is required.

### Q6 — slices

| Hogs | Run length, median | Time off CPU, median |
|---:|---:|---:|
| 2 | 3.00 ms | 3.00 ms |
| 3 | 3.00 ms | 6.00 ms |
| 4 | 3.00 ms | 9.00 ms |

**The run length does not depend on the number of hogs; the time off the CPU does**, by one slice per extra hog. `se.slice` is 2.8 ms and **`CONFIG_HZ=1000`**: the kernel checks whether the running task has used its slice on the 1 ms tick, so 2.8 ms of slice is noticed at the third tick.

### Q7 — latency

Reference, `./lat` and `./lat slack`:

| | Median, 50 µs slack | p99 | Median, 1 ns slack | p99 |
|---|---:|---:|---:|---:|
| no competition | 0.144 ms | 0.232 ms | 0.093 ms | 0.192 ms |
| 3 hogs, nice 0 | 0.054 ms | 0.063 ms | 0.004 ms | 0.047 ms |
| 3 hogs, nice 19 | 0.054 ms | 0.065 ms | 0.004 ms | 0.010 ms |
| 3 hogs, `SCHED_IDLE` | 0.054 ms | 0.061 ms | 0.004 ms | 0.009 ms |

**Busy-CPU median:** 54 µs = **50 µs of timer slack** (`timerslack_ns` = 50,000, which lets the kernel batch nearby timers) **plus about 4 µs** to actually wake. With slack at 1 ns, only the 4 µs remains.

**No-competition median is later** because **an idle CPU goes to sleep**. The `cpuidle` listing shows states down to C10 with **890 µs** of exit latency; between 1 ms wake-ups the idle CPU enters states costing tens to hundreds of microseconds to leave. **With hogs running, the CPU is never idle, so there is nothing to leave.**

*(Maxima of 2–4 ms appear in every row, a few times in 3,000. Their cause is not identifiable without kernel tracing; students should report them, not explain them away.)*

### Q8 — hogs do not delay the sleeper

The sleeper runs for microseconds and sleeps for a millisecond, so **its `vruntime` stays far below the hogs'**. When it wakes it is **eligible with an early virtual deadline, and preempts the running hog at once** — the hogs' nice value makes no difference to that. **The p99 shows the only effect**: in rare cases the sleeper waits for a hog's current slice to be checked, and a nice-0 hog is harder to displace than a nice-19 or idle one (47 µs against 9–10 µs, with slack at 1 ns).

---

## Common Problems

| Symptom | Cause | Fix |
|---|---|---|
| `cpushare.sh` shows one PID twice | `$A` and `$B` captured the same process — typically a hog started before `cd`, which failed with `taskset: failed to execute ./hog` | check both `$A` and `$B` exist: `ps -p $A,$B` |
| Both hogs at ~100% | not pinned to the same CPU; `taskset` missing on one | `taskset -cp $A $B` |
| `systemd-run: Failed to start transient scope unit: ... Access denied` | no user systemd instance — logged in over some SSH configurations | skip Q5's measurement; answer from the lecture |
| Part C's nice-19 hog gets ~50% even with `setsid` | **autogroup is live on this machine** — the task is in the root CPU group | excellent: have the student show the path walk proving it |
| `slice` numbers all ~0 | fewer than 8 CPUs — CPU 7 does not exist, `sched_setaffinity` failed silently | edit `#define CPU` in `slice.c` and `lat.c` |
| A forgotten `hog` at the end | | `pkill -x hog` |

---

*CS 202 · Week 2 · Lab 2 Solutions · Instructor Only*

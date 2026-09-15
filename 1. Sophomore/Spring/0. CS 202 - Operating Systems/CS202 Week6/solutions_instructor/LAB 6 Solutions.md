# CS 202 · Lab 6 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Tuesday of Week 7, 15:00–16:50, BH 210. **Unmarked** — checked off in the session.

**What the session is actually for.** Students have read that "the OOM killer picks a victim". **This lab makes them cause a kill, watch the accounting, and find out that their own session is already marked more killable than a system service.** The intended shape is: promises are cheap (Parts A–C), use is not (D), and the choice of victim is a policy you can read and partly set (E–F).

> ### ⚠️ Safety — read before the session
>
> **`hog` must never run outside a scope.** If a student drops the `systemd-run` prefix, the kernel
> will reclaim from the whole session; `systemd-oomd` may then kill their desktop, and on a shared
> machine other people's work. **Check the first `hog` command of every pair at the bench.**
>
> **Keep runs short.** `oomctl` shows a 50% pressure limit over 20 s on `user@1000.service`.
>
> **If a session dies**, nothing is lost that was not unsaved: `systemd-oomd` kills the app cgroup,
> and the student logs back in. Say so before they start, so nobody panics.

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–10 | A | The `echo` refusal is instant; the arithmetic of `CommitLimit` is the point |
| 10–25 | B | Q3's 8,000 GiB is the moment the lab lands. Let them say it out loud |
| 25–35 | C | Students expect 256; ask what else is mapped |
| 35–65 | **D** | **The busiest part.** Watch for missing scopes; `journalctl --user` needs no root |
| 65–85 | E | Q8's arithmetic: two points on each line is enough |
| 85–95 | F | `oomctl` needs no root either |
| 95–110 | Checkoff | |

---

## Answers

Reference machine: i5-8250U, 7.5 GiB RAM, **4 GiB swap file on NVMe**, Ubuntu 24.04.4, kernel 7.0.0-31, `systemd 255`, `systemd-oomd` active.

### Q1 — the settings you cannot change

```
0
50
bash: /proc/sys/vm/overcommit_memory: Permission denied
MemTotal:        7879208 kB
SwapTotal:       4194300 kB
CommitLimit:     8133904 kB
Committed_AS:   19215756 kB
```

**Mode 0, ratio 50, and the write is refused** — these are system-wide settings and need root; a shared lab image will not give it.

**The arithmetic:** `CommitLimit` = swap + RAM × ratio% = 4,194,300 + 7,879,208 × 0.5 = **8,133,904 kB.** ✓

**`Committed_AS` is 19.2 GiB — more than twice the limit.** In **mode 2** the next `malloc` on the machine would fail, and in fact **most of what is running could not have started**. **In mode 0 the limit is not consulted at all**: `Committed_AS` is bookkeeping. **Accept** any answer that says mode 0 does not enforce it.

### Q2 — what the heuristic refuses

```
      11 GiB: mmap ok        mmap NORESERVE ok        malloc ok
      12 GiB: mmap Cannot allocate memory  mmap NORESERVE ok        malloc refused
```

**Largest accepted 11 GiB, smallest refused 12 GiB**, and **RAM + swap = 7.5 + 4 = 11.5 GiB.** The heuristic refuses a single request larger than everything the machine could ever provide.

**`MAP_NORESERVE` is always accepted.** It tells the kernel the program knows it may not be able to use the memory — **sparse arrays, address-space reservations, guard regions**, the 64 GiB mapping of L16 §7. **Accept** any of those.

### Q3 — and what it does not refuse

**8,000 GiB mapped in 8 GiB pieces**, and `Committed_AS` rose to **8,407,823,756 kB ≈ 7.8 TiB**.

**In one sentence:** *mode 0 checks each request on its own against total memory plus swap, and never checks the sum.* **[Full marks for that sentence.]**

**Why sensible:** a single absurd request is almost always a bug — a negative size, an overflow — and refusing it turns a later crash into an honest `ENOMEM`. **The sum cannot be checked without refusing the programs that legitimately map far more than they use** (L18 §1's gigabyte; every JVM; every sanitiser).

### Q4 — `RLIMIT_AS`

```
RLIMIT_AS 262144 kB: malloc(1 MiB) succeeded 252 times, then errno Cannot allocate memory
RLIMIT_AS 1048576 kB: malloc(1 MiB) succeeded 1017 times, then errno Cannot allocate memory
```

**252, not 256**, because `RLIMIT_AS` counts **the whole address space**: the program, libc and ld.so (about 2 MiB of mappings), the stack, glibc's arenas — and, because each 1 MiB `malloc` is above the mmap threshold, **each allocation is its own mapping with its own rounding.** The 1 GiB run leaves a similar few MiB unaccounted. **Accept** 4–7 MiB of overhead with any of those reasons.

**A program it would break:** anything using `MAP_NORESERVE` for a large reservation — a sparse array, a JVM heap reservation, an address-space sanitiser's shadow map, or L16 §7's 64 GiB region touched 64 times. **The limit counts address space, not memory.**

### Q5 — the first kill

```
16 MiB
32 MiB
48 MiB
Killed
hog exit status 137
low 0 high 0 max 41 oom 1 oom_kill 1 oom_group_kill 0
peak 67108864
```

- **Last report 48 MiB; status 137 = 128 + 9, `SIGKILL`** — the process did not choose to exit and could not have caught it.
- **Killed before 64 MiB of its own data** because the limit covers **everything charged to the scope**: `hog`'s text and libc pages, the shell, the page cache for anything they read, and the kernel's per-process structures. **`peak` is exactly 67,108,864 = 64 MiB.**
- **`max 41`**: the scope hit its limit 41 times, each time reclaiming to make room — **most of the run was already reclaim**; **`oom 1` / `oom_kill 1`**: one allocation could not be satisfied even after reclaim, and one process was killed.

### Q6 — swap

| Run | Result |
|---|---|
| `MemoryMax=64M`, `MemorySwapMax=32M` | reached **80 MiB**, then killed; **swap peak 33,456,128 ≈ 32 MiB** |
| `MemoryMax=64M`, swap unlimited, `hog 128` | **finished**: `0.12 s, 17 major faults`; **swap peak 69,271,552 ≈ 66 MB** |

**`MemoryMax` limits memory; `MemorySwapMax` limits swap; the process dies when it cannot get either.** With 32 MiB of swap the scope's ceiling was about 96 MiB, and `hog` died a little under it.

**Did the second swap? Yes** — the swap peak says 66 MB, and `memory.events` counts `max` hits. **Why so fast:** swapping **out** is a sequential write to an NVMe SSD, and `hog` never reads its old pages back. **Only 17 major faults happened.** *(Compare L19 §3: reading pages back is what costs 90 µs each.)* **Accept** "it only wrote, never read".

### Q7 — the default policy

```
Killed
right after
Terminated
systemd-run exit status 143
```

**The kernel killed only `hog`** (the "Killed" line). **systemd then stopped the whole unit** — `OOMPolicy=stop` is the default — sending `SIGTERM` to the shell: hence "Terminated", **the missing "two seconds later"**, and exit status **143 = 128 + 15**.

**Why reasonable:** for a service, **a surviving half of a service is worse than a stopped one** — the supervisor can restart it cleanly. `OOMPolicy=continue` exists for cases like this lab, where the rest of the unit is doing the observing.

### Q8 — the badness score

From `oomscore`:

| adj | score |
|---:|---:|
| 1000 | 1333 |
| 500 | 1000 |
| 200 | 800 |
| 100 | 733 |

| adj 0, RSS | % of RAM+swap | score |
|---:|---:|---:|
| 1,616 kB | 0.0 | 733 |
| 1,050,192 kB | 8.7 | 791 |
| 2,098,768 kB | 17.4 | 849 |
| 3,147,344 kB | 26.1 | 907 |

**One point of adj adds ⅔ of a point** — (1333 − 733)/900 = 0.667 — **and each 1% of RAM+swap resident adds 6.7 points**: (907 − 733)/26.1 = 6.67. **[Full marks for both slopes with the arithmetic shown.]** *(The overall offset — 733 for a process holding nothing — is not something we established; students should not invent a mechanism for it.)*

**Which process would die:** on the reference machine, **Chrome renderers, at `oom_score` 875–888**, with `oom_score_adj` 300 and 130–376 MiB resident. **Accept** whatever their own machine shows, with the reason: highest score = most memory, adjusted.

### Q9 — the floor, and who set it

**The lowest reachable value was 100, and 0 was refused with `EACCES`.**

```
$ cat /proc/$(pgrep -u $USER -x systemd)/oom_score_adj
100
$ grep OOMScoreAdjust /usr/lib/systemd/system/user@.service
OOMScoreAdjust=100
```

**The user's own systemd manager runs at adj 100, set by pid 1 — a privileged writer — and every process in the session inherits it.** An unprivileged process may **raise** its adjustment but not lower it past the floor set for it: **you may volunteer to die sooner, never later.** *(Root, or `CAP_SYS_RESOURCE`, can.)*

**Chrome's renderers set 300** because a renderer is the most disposable part of a browser: **losing a tab beats losing the browser**, and the process holding the most memory is usually a renderer anyway.

**Kernel threads score 0** — they have no memory of their own (no `mm`), so their badness is zero and the killer skips them. Killing `kswapd` would be absurd.

### Q10 — `systemd-oomd`

```
Swap Used Limit: 90.00%
Default Memory Pressure Limit: 60.00%
Default Memory Pressure Duration: 20s
Memory Pressure Monitored CGroups:
	Path: /user.slice/user-1000.slice/user@1000.service
		Memory Pressure Limit: 50.00%
```

**It watches cgroups' memory pressure and swap use, and kills a whole cgroup — the one with the worst pressure — when a limit is exceeded for the duration.** Here it monitors **the student's entire desktop session**.

**The situation the kernel's killer misses:** a machine whose working sets do not fit **thrashes** (L21 §2) — every allocation eventually succeeds, because reclaim always finds *something* to evict, so **no allocation ever fails and the OOM killer never runs** — while the machine does 90 µs of disk work per access and is unusable for minutes. **Pressure detects it**: `some` counts time with at least one task stalled on memory, `full` time with all of them stalled, so **a number that is high while the CPU is idle is exactly the signature of thrashing.**

---

## Common Problems

| Symptom | Cause | Fix |
|---|---|---|
| `systemd-run: Failed to start transient scope: Access denied` | ran without `--user` | add `--user` |
| Scope exits 143 with no `memory.events` output | forgot `-p OOMPolicy=continue` | add it (that is Q7) |
| `hog` finishes at 256 MiB with no kill | `MemorySwapMax` not set, and swap is large | set `-p MemorySwapMax=0` |
| The session becomes unresponsive | ran `hog` or `thrash` without a scope | wait; `systemd-oomd` ends it. Then add the scope |
| `oom_score` values differ wildly from the table | different RAM or swap | the **slopes** are what is marked |

---

*CS 202 · Week 6 · Lab 6 Solutions · Instructor Only*

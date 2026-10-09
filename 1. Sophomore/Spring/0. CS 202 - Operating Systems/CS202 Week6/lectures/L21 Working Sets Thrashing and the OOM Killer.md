# CS 202 · Operating Systems
## Week 6 · Lecture 3 of 3
### Working Sets, Thrashing, and the OOM Killer

*“If a program manipulates a large amount of data, it does so in a small number of ways.”* — Alan Perlis, "Epigrams on Programming" (1982), #5

---

**Sat:** Friday of Week 6, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 22 §22.10–§22.11; Denning (1968) · **Next:** Week 7, file systems

**Coursework:** 📝 **PS 5** due today 17:00 · 📊 **Quiz 7** Mon of Week 7 · 🔬 **Lab 6** Tue of Week 7 15:00–16:50 · 📋 **Project 1** released Wed of Week 7, due Fri of Week 11 17:00 · 📝 **PS 7** released Wed of Week 7, due Fri of Week 8 17:00 · 📘 **Midterm 2** Mon of Week 8 18:00–19:15

---

## 1. The Working Set

L20's fault curves all had a knee, and the knee was the **working set**: Denning's *W(t, τ)* — the set of pages a process referenced in the last τ units of time. **Give a process its working set and it runs at memory speed; give it less and it faults.**

**A process can measure its own.** Writing `1` to `/proc/self/clear_refs` clears the referenced bit on every one of its pages; `Referenced` in `/proc/self/smaps_rollup` then counts the pages touched since. `wss.c`:

```
touched 256 MiB:            Rss  263600 kB  Referenced  263480 kB
after clear_refs 1:         Rss  263732 kB  Referenced       4 kB
read the first 64 MiB:      Rss  263732 kB  Referenced   65652 kB
cleared, wrote 16 MiB:      Rss  263732 kB  Referenced   16436 kB
```

**Resident memory stayed at 257 MiB throughout; the working set was 64 MiB, then 16 MiB.** The difference is exactly what a replacement policy exploits — and what `top`'s RSS column cannot show you. **τ is the interval between the two `clear_refs` writes**: a working set is meaningless without one.

---

## 2. Thrashing, Measured

**`thrash.c` fills 256 MiB and then reads random pages for four seconds**, inside a scope with a memory limit:

```bash
systemd-run --user --scope -p MemoryMax=192M ./thrash 256 4 uniform
```

**`uniform` reads any of the 65,536 pages; `hot` sends 90% of its reads to one eighth of them** — a 32 MiB working set inside a 256 MiB allocation.

| Limit | uniform: reads/s | major faults | hot: reads/s | major faults |
|---|---:|---:|---:|---:|
| none | **21,693,889** | 0 | **45,495,703** | 0 |
| 384 MiB | 21,927,700 | 0 | 44,918,381 | 0 |
| 256 MiB | 1,227,630 | 28,534 | 13,601,882 | 18,964 |
| 224 MiB | 76,276 | 39,411 | 924,720 | 43,254 |
| 192 MiB | 42,178 | 42,870 | 441,008 | 41,383 |
| 128 MiB | 22,724 | 45,829 | 224,017 | 41,099 |
| **64 MiB** | **14,775** | 44,362 | **166,745** | 44,852 |

**Three things to see:**

- **The cliff is not gentle.** Between a limit that fits and one 12% too small, throughput fell **18-fold**; by 64 MiB it was **1,470 times** slower than unconstrained. **The program's instructions did not change; only how often a read waited 90 µs.**
- **The major-fault count barely moves below 224 MiB** — around 43,000 in four seconds either way. **The disk is the limit**: the machine cannot fault faster, so throughput is simply the fault rate. *(That is why the last rows look almost flat: they are all "as fast as the SSD allows".)*
- **Locality is worth more than memory.** At **the same 64 MiB limit**, the `hot` pattern ran **11 times faster** than `uniform` — because most of its reads hit its 32 MiB working set, which fits. **A process thrashes when its working set does not fit, not when its allocation does not.**

**This is why a thrashing machine feels dead**: every process is runnable, the CPU is idle, and everything is waiting for the same disk.

---

## 3. What a System Can Do About It

- **Give the process less to do**: Denning's own answer — **suspend some processes entirely** so the rest have their working sets. Unix systems used to swap whole processes out; Linux does not.
- **Contain it**: a **cgroup limit** makes one program's appetite its own problem — it reclaims at its own limit instead of pushing everything else out. **That is how every experiment in this week runs.**
- **Notice it**: **pressure stall information** (L19 §4) is the only signal that separates "slow because busy" from "slow because thrashing".
- **Act on it before the kernel must**: `systemd-oomd` reads pressure and kills a whole cgroup while the machine is still responsive:

```
$ systemctl is-active systemd-oomd
active
$ oomctl
Swap Used Limit: 90.00%
Default Memory Pressure Limit: 60.00%
Default Memory Pressure Duration: 20s
Memory Pressure Monitored CGroups:
	Path: /user.slice/user-1000.slice/user@1000.service
		Memory Pressure Limit: 50.00%
```

**Your whole desktop session is one monitored cgroup**, with a 50% pressure limit over 20 seconds. **A program that thrashes for half a minute can get things in your session killed** — which is why Lab 6 runs everything inside small scopes and keeps every run short.

---

## 4. Promises: Overcommit

**Before anything is used, it is promised.** Linux has three policies, in `/proc/sys/vm/overcommit_memory`:

| Mode | Rule |
|---|---|
| **0** — heuristic *(the default, and this machine)* | refuse an allocation that is obviously absurd; allow the rest |
| 1 — always | never refuse |
| 2 — strict | refuse once total commitments exceed `CommitLimit` = swap + RAM × `overcommit_ratio`% |

**What "obviously absurd" means, measured** (`overcommit.c`, RAM + swap = 11.5 GiB):

```
      4 GiB: mmap ok        mmap NORESERVE ok        malloc ok
     11 GiB: mmap ok        mmap NORESERVE ok        malloc ok
     12 GiB: mmap Cannot allocate memory  mmap NORESERVE ok        malloc refused
   1024 GiB: mmap Cannot allocate memory  mmap NORESERVE ok        malloc refused
  8 GiB mappings, kept: 8000 GiB mapped before a refusal
```

- **A single mapping larger than RAM plus swap is refused**; 11 GiB was allowed and 12 GiB was not.
- **The same memory in pieces is not**: a thousand 8 GiB mappings succeeded — **8 TB of promises on an 8 GiB machine.** The heuristic checks each request against the total, and never the total against itself.
- **`MAP_NORESERVE` is always allowed**: the program is saying it knows.
- **`Committed_AS` was 19.4 GiB against a `CommitLimit` of 8.1 GiB** before any of this. **In mode 0 the limit is not enforced** — it is bookkeeping. In mode 2 it would be, and most of the machine's programs would fail to start.

**What an ordinary user *can* limit is their own address space**, with `RLIMIT_AS`:

```
RLIMIT_AS 262144 kB: malloc(1 MiB) succeeded 252 times, then errno Cannot allocate memory
```

**252, not 256**: the program's own code, libraries, stack and allocator arenas are in the address space too. **It limits mappings, not use** — so it also refuses L18 §1's gigabyte mapped for free.

---

## 5. The OOM Killer

**When reclaim cannot free a page, something must die.** The kernel scores every process — its *badness* — and kills the worst. `oomscore.c` moves its own score around:

```
MemTotal 7879208 kB + SwapTotal 4194300 kB = 12073508 kB
inherited adj 200, score 800
  set adj  1000: ok       adj now  1000  score  1333
  set adj   500: ok       adj now   500  score  1000
  set adj   200: ok       adj now   200  score   800
  set adj   100: ok       adj now   100  score   733
  set adj     0: REFUSED  adj now   100  score   733
  adj 0, RSS     1624 kB (0.0% of RAM+swap): score 733
  adj 0, RSS  1050200 kB (8.7% of RAM+swap): score 791
  adj 0, RSS  2098776 kB (17.4% of RAM+swap): score 849
  adj 0, RSS  3147344 kB (26.1% of RAM+swap): score 907
```

**The score is linear in two things**: each point of `oom_score_adj` adds **⅔ of a point**, and **each 1% of RAM+swap held adds 6.7 points**. *(The overall scale — why a bare process scores 733 rather than 0 — we did not establish; what matters is that the killer compares scores, and the ordering is by memory held, adjusted.)*

**So the OOM killer chooses the process using the most memory**, with a thumb on the scale:

- **`oom_score_adj` runs from −1000 to 1000**, and is inherited. −1000 means never.
- **A process can raise its own but not lower it below a floor.** Here the floor is **100**, set for the whole session by `user@.service`'s `OOMScoreAdjust=100` — so **everything you run is already marked more killable than a system service.**
- **Programs opt in to dying.** On this machine the highest scores are **Chrome's renderer processes at adj 300** — a browser tab is a better victim than the browser.
- **Kernel threads score 0** and are never chosen.

> **The curriculum describes badness as "proportional to memory usage, inversely proportional to
> niceness and runtime".** That was Linux's rule **until 2.6.36 (2010)**, when the heuristic — which
> also weighed how long a process had run, whether it was root's, and how many children it had —
> was replaced by the measurement above: **memory, plus `oom_score_adj`, and nothing else.** The
> older rule is history worth knowing, not this kernel's behaviour.

---

## 6. A Kill, Observed

Inside a scope with 64 MiB and no swap, `hog` allocates and fills 1 MiB at a time:

```
$ systemd-run --user --scope -p MemoryMax=64M -p MemorySwapMax=0 -p OOMPolicy=continue sh -c '...'
48 MiB
Killed
hog exit status 137
low 0 high 0 max 41 oom 1 oom_kill 1 oom_group_kill 0
peak 67108864
```

- **It died at about 48 MiB**, not 64: the scope's 64 MiB also holds `hog`'s code, its libraries, and the shell.
- **Exit status 137** = 128 + 9: **`SIGKILL`**. There is no catching it and no cleanup.
- **`max 41`** — the limit was hit 41 times, each forcing reclaim first, before one allocation could not be satisfied at all; **`oom_kill 1`** is the kill itself.
- **`journalctl --user`**: *"A process of this unit has been killed by the OOM killer."*

**With 32 MiB of swap allowed** the same `hog` reached about 80 MiB before dying; **with swap unlimited** it finished all 128 MiB in 0.12 s, having written 69 MB to swap. **The limit decides when; swap decides how long the dying takes.**

**And `OOMPolicy=continue` above is not the default.** Without it, systemd's default `stop` **terminates the rest of the unit** once the kernel kills one of its processes: the shell in the scope printed one more line and then got `SIGTERM`. **For a service that is right — a half-killed service is worse than a stopped one.**

---

## 7. What to Take Away

1. **The working set is what a process touched recently**, not what it holds. Measured with `clear_refs` and `Referenced`: 16 MiB of a 257 MiB process.
2. **Thrashing is a cliff.** 12% too little memory cost 18× throughput; 75% too little cost **1,470×** — and the fault count stopped rising because **the disk was the limit.**
3. **Locality beats capacity**: at the same 64 MiB limit, a 32 MiB working set ran **11× faster** than a uniform one.
4. **Overcommit mode 0 refuses only absurd single requests** — 12 GiB, not 8 TB in pieces — and `Committed_AS` is bookkeeping. **`RLIMIT_AS` is the limit a user can actually set**, and it limits address space, not use.
5. **The OOM killer scores by memory held plus `oom_score_adj`**, measured linear; your session already carries a floor of 100, and Chrome volunteers its tabs at 300.
6. **A kill is `SIGKILL`**, recorded in `memory.events` and the journal — **and systemd stops the rest of the unit by default.**
7. **`systemd-oomd` acts on pressure before the kernel must**, because a machine can be unusable long before an allocation actually fails.

---

## Exercises

1. Using §1's method, **design a measurement of a program's working set at τ = 1 s** without changing the program. *(Whose `clear_refs` would you write to, and what would you read?)*
2. In §2, why does `uniform` at a 256 MiB limit fault **28,534** times, while at 224 MiB it faults **39,411** — but at 64 MiB only **44,362**, hardly more? What limits the top of that column?
3. A server has 8 GiB of RAM, no swap, and runs 20 identical processes, each with a 500 MiB working set. **What happens, and what is the smallest change that fixes it?** Give two different fixes.
4. `Committed_AS` is 19.4 GiB on an 7.5 GiB machine. **Write down two different programs that inflate it without ever using the memory**, and say whether mode 2 would break either.
5. You are packaging a database that must not be killed, and a batch job that may be. **What do you set, on each, and what can an unprivileged user not do?**

---

*CS 202 · Week 6 · L21 · © CSE Department*

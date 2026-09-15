# CS 202 · Lab 6
## Out of Memory
### Week 6 · sat **Tuesday of Week 7**, 15:00–16:50, BH 210 · **unmarked, checked off in the session**

---

> **This lab covers Week 6** and is sat on the **Tuesday of Week 7**. Lab *N* is always sat in
> Week *N+1*.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.

**What you are doing:** running out of memory on purpose — safely — and finding out who decides what happens next. **Three different mechanisms answer**: the kernel's overcommit policy when memory is *promised*, the kernel's OOM killer when it is *used*, and a userspace daemon that acts before either.

**The curriculum asks you to "experiment with overcommit settings".** On BH 210 **you cannot change them** — they are system-wide and need root. Part A measures that refusal; Parts B and C experiment with what the settings *do*, and with the limits you **can** set.

> ### ⚠️ Never run `hog` outside a memory-limited scope
>
> On a shared machine, a program that eats all memory makes the kernel kill **something** — possibly
> your desktop session, possibly another student's work. **Every `hog` in this lab runs inside
> `systemd-run --user --scope -p MemoryMax=…`**, where the OOM killer can see only your scope.
> **Keep every experiment short**: `systemd-oomd` watches the memory pressure of your whole session
> (Part F), and a scope that thrashes for twenty seconds can get your session's processes killed.

---

## 0. Setup (5 minutes)

```bash
W6="$ACADEMICS/1. Sophomore/Spring/0. CS 202 - Operating Systems/CS202 Week6"
mkdir -p "$CS202/week6/lab6" && cd "$CS202/week6/lab6"
cp "$W6/lab/hog.c" "$W6/lab/overcommit.c" "$W6/lab/oomscore.c" .
for p in hog overcommit oomscore; do gcc -O2 -Wall -Wextra -o $p $p.c; done
```

---

## 1. Part A — The Settings You Cannot Change (10 min)

```bash
cat /proc/sys/vm/overcommit_memory /proc/sys/vm/overcommit_ratio
echo 2 > /proc/sys/vm/overcommit_memory
grep -E 'MemTotal|SwapTotal|CommitLimit|Committed_AS' /proc/meminfo
```

`overcommit_memory` has three modes: **0** heuristic, **1** always allow, **2** strict accounting — refuse any allocation that would take the system's total commitments past `CommitLimit` = swap + RAM × `overcommit_ratio`%.

**Q1.** Report the mode, the ratio, and the error from the `echo`. **Compare `Committed_AS` with `CommitLimit`.** In mode 2, what would that comparison mean for the next program that called `malloc`? **Why is it harmless in mode 0?** Using `CommitLimit`'s formula, check the value you see.

---

## 2. Part B — What the Heuristic Refuses (15 min)

```bash
./overcommit
```

It tries single anonymous mappings of growing size — plain, with `MAP_NORESERVE`, and through `malloc` — then maps 8 GiB at a time without freeing, 1,000 times.

**Q2.** **What is the largest single mapping accepted, and the smallest refused?** Relate the boundary to the numbers in Part A. **What does `MAP_NORESERVE` change, and why would a program ask for it?** *(`man 2 mmap`.)*

**Q3.** The 8 GiB loop: **how much did it get, and what did `Committed_AS` become?** From Q2 and Q3 together, **state in one sentence what mode 0's heuristic actually checks.** Why is that a sensible check to make, even though it lets the total go anywhere?

---

## 3. Part C — A Limit You Can Set (10 min)

`RLIMIT_AS` limits a process's **address space** — every mapping, used or not. Any user may lower it for their own processes:

```bash
( ulimit -v 262144;  ./overcommit x )        # 256 MiB
( ulimit -v 1048576; ./overcommit x )        # 1 GiB
```

**Q4.** Report both. **Why did `malloc` succeed fewer than 256 times under a 256 MiB limit?** *(What else is in the address space? `cat /proc/self/maps | wc -l`.)* **Give one program this limit would break although it would never actually use much memory** — think of Part B's `MAP_NORESERVE`, or of L18's gigabyte mapped for free.

---

## 4. Part D — The OOM Killer, in a Box (30 min)

**A scope with 64 MiB and no swap:**

```bash
systemd-run --user --scope -p MemoryMax=64M -p MemorySwapMax=0 -p OOMPolicy=continue sh -c '
  ./hog 256; echo "hog exit status $?"
  CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
  cat $CG/memory.events; echo "peak $(cat $CG/memory.peak)"'
journalctl --user -n 5 --no-pager | grep -i oom
```

**Q5.** **At what size did `hog` report last, and with what exit status?** Explain the status. Why was it killed **before** it reached 64 MiB of its own data? Explain the `oom` and `oom_kill` lines of `memory.events`, and what `max` counts.

**Now allow some swap:**

```bash
systemd-run --user --scope -p MemoryMax=64M -p MemorySwapMax=32M -p OOMPolicy=continue sh -c '
  ./hog 256; echo "hog exit status $?"
  CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
  grep oom_kill $CG/memory.events; echo "swap peak $(cat $CG/memory.swap.peak)"'
systemd-run --user --scope -p MemoryMax=64M -p OOMPolicy=continue sh -c '/usr/bin/time -f "%e s, %F major faults" ./hog 128'
```

**Q6.** **How far did `hog` get with 32 MiB of swap, and did the second — with unlimited swap — finish?** Explain both from `MemoryMax` and `MemorySwapMax`. **Did the second run swap?** How can you tell, and why was it so fast when swapping is slow?

**Finally, the default policy:**

```bash
systemd-run --user --scope -p MemoryMax=64M -p MemorySwapMax=0 sh -c './hog 256 > /dev/null; echo "right after"; sleep 2; echo "two seconds later"'
echo "systemd-run exit status $?"
```

**Q7.** **Which lines printed?** The kernel killed only `hog`. **What killed the shell**, and why is that a reasonable default for a service? *(`man 5 systemd.service`, `OOMPolicy=`.)*

---

## 5. Part E — Who Would Die (20 min)

```bash
./oomscore
```

**Q8.** Report the output. **Find the relationship between `oom_score`, `oom_score_adj` and resident memory** from your own numbers: how many points does one unit of adj add, and how many does each 1% of RAM+swap in resident memory add? **Which process on the machine would the OOM killer choose if it ran now?**

```bash
for d in /proc/[0-9]*; do s=$(cat $d/oom_score 2>/dev/null) && echo "$s $(cat $d/oom_score_adj 2>/dev/null) $(cat $d/comm 2>/dev/null)"; done | sort -n | tail -5
cat /proc/$(pgrep -u $USER -x systemd)/oom_score_adj
grep OOMScoreAdjust /usr/lib/systemd/system/user@.service
```

**Q9.** **How low could `oomscore` set its own adjustment, and why not lower?** Who set that floor, and how did your shell inherit it? **Why do browser renderer processes set their own adjustment higher than the default?** Which processes have a score of 0, and why can the killer never choose them?

---

## 6. Part F — The Killer Before the Killer (10 min)

```bash
systemctl is-active systemd-oomd
oomctl | head -20
cat /proc/pressure/memory
```

**Q10.** **What does `systemd-oomd` monitor, what are its limits, and which cgroup is it watching on your behalf?** The kernel's OOM killer acts only when an allocation cannot be satisfied. **Describe a situation in which a machine is unusable for minutes without ever reaching that point** — and explain how pressure stall information (`some`, `full`) detects it. *(L21 §3.)*

---

## 7. Checkoff

Show the TA:

- [ ] Your Part A refusal and your answer to **Q1**.
- [ ] Part D's first scope output, with `memory.events`, and your answers to **Q5 and Q7**.
- [ ] Your derived relationship for **Q8**.
- [ ] Your written answers to **Q3, Q6 and Q10**.

**Take with you:** **PS 6** simulates the choice the kernel makes long before any of this — which page to evict — and **Week 7** turns to the biggest evictable memory on the machine: the page cache.

---

*CS 202 · Week 6 · Lab 6 · © CSE Department*

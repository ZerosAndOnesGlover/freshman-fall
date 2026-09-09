# PROG 201 · Systems Programming in C
## Week 11 · Lecture 2 of 3
### Cgroups and Resource Control

---

**Reading:** `man 7 cgroups` · kernel docs `Documentation/admin-guide/cgroup-v2.rst` · `man 1 systemd-run`, `man 5 systemd.resource-control` · **Previous:** L34 — namespaces · **Next:** L36 — images, OverlayFS, and the security boundary

---

## 1. Namespaces Hide, Cgroups Limit

Last lecture built the *isolation* half of a container: private views of PIDs, the network, the filesystem. Isolation answers "what can this process **see**?" It says nothing about "how much can this process **use**?" A process alone in its PID namespace can still allocate all of RAM, spawn until the machine's fork limit, and peg every core. Namespaces do not limit resources.

The other half is **cgroups** — control groups. A cgroup is a set of processes with **limits and accounting** attached: this group may use at most 100 MB of memory, at most 200 processes, this share of CPU. Where a namespace is a private *view*, a cgroup is a *budget*. A real container is the intersection: namespaces for isolation, cgroups for resource control. Docker's `--memory` and `--cpus` flags are cgroup settings; nothing more.

---

## 2. Cgroup v2: One Unified Tree

Cgroups are a filesystem. On this machine (and every modern one) it is **cgroup v2**, mounted once at `/sys/fs/cgroup`:

```
$ mount | grep cgroup
cgroup2 on /sys/fs/cgroup type cgroup2 (rw,nosuid,nodev,noexec,relatime)
```

v1 had a separate hierarchy per controller (one tree for memory, another for cpu, ...), which was a decade-long mistake — a process could sit in inconsistent places in different trees. **v2 is a single tree**, and each directory is a cgroup. You create one by making a directory; you configure it by writing files in it:

```
/sys/fs/cgroup/
├── cgroup.controllers        <- which controllers are available here
├── cgroup.subtree_control    <- which are enabled for children
├── memory.max                <- the memory limit (bytes, or "max")
├── memory.current            <- current usage (read-only accounting)
├── pids.max                  <- max number of processes
├── pids.current
├── cpu.max                   <- "quota period" in microseconds
└── user.slice/ system.slice/ ...
```

To limit a process you write its PID into `cgroup.procs` of the target cgroup and write the limits into `memory.max`, `pids.max`, and so on. **A process is always in exactly one cgroup**; moving it means writing its PID into another's `cgroup.procs`.

---

## 3. Delegation: Who May Write These Files

Here is the subtlety that decides whether an unprivileged container can limit itself. Writing to `/sys/fs/cgroup/...` needs write permission on those files, which are **root-owned** at the top. An ordinary user cannot just create a cgroup at the root.

But systemd **delegates** a subtree to each logged-in user, under `/sys/fs/cgroup/user.slice/user-<uid>.slice/user@<uid>.service/`, and **that** subtree is yours to write. Measured on this machine:

```
$ cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/cgroup.controllers
memory pids                                <- memory and pids ARE delegated
```

So an unprivileged user *can* create cgroups and set memory and pids limits — within the delegated subtree, for the controllers systemd handed down. The clean way to do it is to let systemd create the scope for you:

```
$ systemd-run --user --scope -p MemoryMax=100M -p MemorySwapMax=0 ./hog
```

This makes a transient cgroup, applies the limits, and runs the program in it — no manual filesystem poking, no root.

---

## 4. Measuring the Memory Limit

`hog.c` allocates and **touches** memory 10 MB at a time (touching matters — the kernel only commits a page when written, so `malloc` alone would not count against `memory.current`). Unconstrained it runs away; under a 100 MB cap:

```
$ systemd-run --user --scope -p MemoryMax=100M -p MemorySwapMax=0 ./hog
Running scope as unit: run-r4f1....scope
  allocated 10 MB   (touched)
  allocated 20 MB
  ...
  allocated 90 MB
Killed
$ echo $?
137
```

**Return code 137 = 128 + 9 = killed by signal 9 (SIGKILL).** With swap also capped at zero, the memory cgroup's out-of-memory killer fires the instant the group's usage would exceed 100 MB: there is no more room and nowhere to swap, so the kernel kills a process *in that cgroup* — not a global OOM, a **cgroup-local** one. The host and every other process are untouched. This is the mechanism behind "the container got OOM-killed": Docker sets `memory.max`, your process exceeds it, the cgroup OOM killer ends it, and you see exit 137.

Note *which* number told the truth. `137` is not an error in the program — the program was correct and was allocating exactly as written. **The exit code is a fact about the limit, not a fact about the bug**, the same discipline as Week 10: a measurement that produces something surprising is first a fact about the measurement. Here the surprising thing (a sudden SIGKILL at 90 MB) is precisely the limit working.

---

## 5. Measuring the Process Limit

`pids.max` caps the number of processes — the defence against a fork bomb. Under a limit of 20:

```
$ systemd-run --user --scope -p TasksMax=20 ./forkbomb
...
fork: Resource temporarily unavailable          <- EAGAIN at the 20th
```

The 20th `fork` returns **EAGAIN** ("Resource temporarily unavailable"), not a crash — the cgroup refuses to create the 21st task and `fork` fails cleanly. A fork bomb inside such a cgroup exhausts *its own* budget of 20 and stops, while the host keeps running. Without the limit the same program would climb toward the host's `pid_max` and take the machine down with it. **`pids.max` turns a machine-killer into a self-limiting nuisance.**

---

## 6. What a Container Costs to Start

If a container is just a process with namespaces and a cgroup, starting one should be cheap — much cheaper than booting a VM. `cost.c` measures the startup path directly, averaged over many iterations, timing from just before `clone`/`fork` to the child being ready:

| Startup path | Mean latency | Relative |
| --- | --- | --- |
| `fork` + `wait` (baseline process) | **139.2 µs** | 1.0× |
| `clone`, no new namespaces | **119.4 µs** | 0.86× |
| `clone` + **6 namespaces** (the container) | **1001.5 µs** | **7.2×** |

Three things to read off this. First, **a bare `clone` is not more expensive than `fork`** — it is marginally *cheaper* here (fewer defaults to set up), so the flags argument is not itself a cost. Second, **the six namespaces cost about 0.9 ms** — the kernel has to allocate and populate six new namespace structures, and that is where the time goes. Third, and the point of the table: **~1 ms to start a fully-namespaced container**, against the **seconds** a virtual machine needs to boot a kernel and userland (next lecture). Three orders of magnitude. This single number — startup in milliseconds, not seconds — is why the industry moved from VMs to containers for packaging and scaling services.

**A caveat this course insists on:** 1 ms is the *namespace* cost, on a machine where `mount` inside the userns is blocked, so it excludes the overlay-filesystem setup and the `pivot_root` a real runtime does. It is the floor, honestly labelled — the cost of the isolation primitive itself, not of a production container image. The build record says exactly what the number does and does not include.

---

## Summary

- **Namespaces isolate (a private view); cgroups limit (a budget).** A real container is both. Namespaces alone do not stop a process using all of RAM or forking without bound.
- **Cgroup v2 is one unified tree at `/sys/fs/cgroup`** — each directory a cgroup, configured by writing files (`memory.max`, `pids.max`, `cpu.max`); a process is always in exactly one.
- **Delegation** lets an unprivileged user control a subtree: `memory` and `pids` are delegated to `user@1000.service`, so `systemd-run --user --scope -p MemoryMax=...` sets limits with no root.
- **Measured — memory:** a 100 MB cap with no swap makes the hog **cgroup-OOM-killed at ~90 MB, exit 137** (128+SIGKILL); the host is untouched.
- **Measured — pids:** a 20-task cap makes the 21st `fork` fail with **EAGAIN**; a fork bomb self-limits instead of killing the machine.
- **Measured — startup:** fork 139 µs, bare clone 119 µs, **clone + 6 namespaces 1001 µs (~1 ms)** — three orders of magnitude below a VM boot, and the reason containers won.

---

## Exercises

1. Read `cgroup.controllers` at the root and in your delegated user subtree. Which controllers are delegated to you, and which are not? Why can you limit memory but perhaps not cpu?
2. Run `hog` under `-p MemoryMax=50M` and again under `-p MemoryMax=200M`. At what `memory.current` does each die, and what exit code? Watch `memory.current` while it runs.
3. Why does `hog` *touch* each allocation instead of only `malloc`-ing it? Change it to `malloc` without touching and explain what `memory.current` does.
4. Set `MemoryMax=100M` but leave swap uncapped. Does the program still get killed at 100 MB, or does it get slow first? What does swap change about the limit?
5. Run a fork bomb under `TasksMax=20`. Which errno does `fork` return at the limit? Confirm the host is unaffected while it runs.
6. Reproduce the startup table with `cost.c`. Which single flag added to `clone` costs the most? Time each namespace flag separately.
7. `systemd-run --user --scope` creates a cgroup for you. Find that cgroup under `/sys/fs/cgroup/user.slice/...` while the program runs and read its `memory.max` directly. Does it match what you passed?

---

*PROG 201 · Week 11 · L35 · © CSE Department*

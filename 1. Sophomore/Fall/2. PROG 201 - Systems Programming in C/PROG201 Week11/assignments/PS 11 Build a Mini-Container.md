# PS 11 · Build a Mini-Container

**PROG 201 · Week 11 · Containers and Virtualization**
**Released:** Week 11, Wednesday · **Due:** Week 12, Friday 17:00
**Weight:** 8% of course grade · **Submit:** `container.c`, `Makefile`, `report.md`
**Reference machine:** all figures measured on the lab reference machine (`uname -r` = `7.0.0-30-generic`, Ubuntu 24.04, cgroup v2, `apparmor_restrict_unprivileged_userns=1`). State yours if different.

---

## Overview

The lab handed you a mini-container with the flags filled in. This problem set has you **build one from an empty file** and then **characterise its boundary quantitatively** — what the isolation enforces, what it does not, and what it costs. The deliverable is a working `container.c` plus a report whose every number names the program that produced it.

You may reuse `hog`, `sec` and `cost` from lab as measurement tools; the container itself you write yourself.

---

## Part A — `container.c` (40 pts)

Write, from scratch, a program `container CMD [ARGS...]` that runs `CMD` in a new set of namespaces. Requirements:

1. **`clone`** the child with `CLONE_NEWUSER | CLONE_NEWPID | CLONE_NEWNS | CLONE_NEWUTS | CLONE_NEWNET | CLONE_NEWIPC | SIGCHLD`. Give it a heap or static stack of at least 1 MiB.
2. **uid/gid mapping** — the parent writes, to `/proc/<child>/…`: `uid_map` = `"0 <uid> 1"`, then `setgroups` = `"deny"`, then `gid_map` = `"0 <gid> 1"`. Use a **pipe** to make the child wait until the maps are written before it does anything (a child that races ahead sees uid 65534).
3. The child **`execvp`s** `CMD`. Before exec, it should *attempt* `sethostname` and a private `/proc` mount, reporting — not ignoring — any error.
4. Exit with the child's exit status.

**It must handle** the argument-less error case (`usage:`), a failed `clone` (print `strerror`), and a failed `exec` (print which command, return 127).

Deliver `container.c` and a `Makefile` (`-Wall -Wextra`, must build **warning-clean**, must **not** commit the binary).

## Part B — Prove and quantify the isolation (35 pts)

Run your container and record, each number naming the producing command:

1. **PID namespace.** `./container sh -c 'echo $$'` and `./container getpid_prog` (or `echo $$`). Show the child is **PID 1**. From a second terminal, find its **host** PID (`ps`/`pgrep`). Report both and explain the one-process-two-PIDs fact.
2. **Network namespace.** `./container ip -o link show` versus host `ip -o link show`. Report the interface count inside and out, and the state of the container's single interface.
3. **Shared kernel.** `./container uname -r` versus host `uname -r`. Report both. In one sentence, why must they be equal, and what does that forbid a container from doing?
4. **The deviation.** Record the exact errno from `sethostname` and from `mount` inside your container. Read `/proc/sys/kernel/apparmor_restrict_unprivileged_userns`. Explain why a uid-0-in-namespace process is refused these, and identify which isolation still holds and why (L34 §5).

## Part C — Limits and cost (25 pts)

1. **Memory cap.** `systemd-run --user --scope -p MemoryMax=100M -p MemorySwapMax=0 ./hog`. Report the kill point (MiB) and exit code; decode the code; explain *cgroup-local* OOM and why the host survives.
2. **Process cap (choose one).** Either run a bounded fork loop under `-p TasksMax=N` and report the errno at the limit, **or** explain from the cgroup docs how `pids.max` would stop a fork bomb and what `fork` returns at the cap.
3. **Startup cost.** Run `cost`. Report the three figures (fork, bare clone, clone+6ns). State how much the namespaces add and compare the container figure to a VM boot (order of magnitude).
4. **seccomp.** Run `sec`. Report `getpid`'s return and errno after the filter; state why no privilege was needed.

---

## Report (`report.md`)

Structure it Part A / B / C. **Every measured figure must name the program or command that produced it** (course rule). A result that is an error code — EPERM, exit 137, EAGAIN — is a finding to record and interpret, never a failure to hide: *a measurement that produces something impossible or forbidden is first a fact about the measurement.* Where this machine blocks an operation (mount, overlay), say so precisely and state what it would do where permitted.

## Grading (100 pts)

| Part | Points |
| --- | --- |
| A — `container.c` correct, robust, warning-clean, binary not committed | 40 |
| B — PID/net/kernel isolation measured + host comparison; deviation errno + AppArmor explanation | 35 |
| C — memory 137, cost table, seccomp, all attributed | 25 |

**Academic integrity.** Write `container.c` yourself. You may consult `man 2 clone`, `man 7 user_namespaces`, and the lab skeleton's *structure*, but not copy a classmate's or a runtime's source. Cite any man page or doc you lean on.

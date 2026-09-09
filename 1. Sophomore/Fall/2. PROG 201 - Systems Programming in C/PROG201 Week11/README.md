# PROG 201 · Systems Programming in C
## Week 11: Containers and Virtualization

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101; CS 201 as co-requisite
**Assessment for this course (overall):** Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%
**This week's deliverables:** PS 10 (due Friday), PS 11 (released Wednesday, due Friday of Week 12) and **Quiz 11** (Tuesday, covers Week 10).
**Lab 10 is sat on the Monday of this week**; **Lab 11 covers this week and is sat on the Monday of Week 12.**

> ### **No container runtime is installed — and that is the syllabus, not a gap.**
> `docker`, `podman`, `runc`, `lxc`, and the `newuidmap`/`newgidmap`/`fuse-overlayfs` helpers are all
> absent from a student account, so the week is the **primitives** those tools assemble: `clone`,
> namespaces, cgroups, OverlayFS, seccomp. You build a container in ~80 lines of C. On this machine
> `apparmor_restrict_unprivileged_userns` = 1, which strips capabilities from unprivileged user
> namespaces — so namespace *creation* works but `mount`/`sethostname` inside are refused. That
> boundary is measured, not hidden; [[PROG 201 Scheduling Notes]] §22 records every substitution.

---

### Why This Week Exists

Because Week 10 showed that any program may harbour every bug an attacker wants, and the question the industry answered is: *how do you run code you cannot fully trust, densely, and cheaply?* Not a virtual machine per program — a **container**: an ordinary process given restricted views and a budget, sharing the one host kernel. This week you build one from the system calls up, and you measure exactly what the isolation enforces and what it costs.

The whole week is: **a container is a process, not a machine.** Everything follows — the millisecond startup, the shared kernel, the weaker-than-a-VM boundary, and the reason a stripped capability set (here, imposed by AppArmor; in Docker, by policy) is the last line of defence.

Three ideas:

1. **Namespaces isolate a view; cgroups limit a budget; seccomp/capabilities shrink the reach.** A container is the composition, and each part is separately measurable.
2. **`CLONE_NEWUSER` is the key** — it needs no privilege and carries the other namespaces, which is the whole basis of rootless containers.
3. **A container shares the host kernel** (`uname -r` is identical inside and out), which is simultaneously why it is cheap and why its isolation is weaker than a VM's.

---

### Learning Objectives

By the end of Week 11, you should be able to:

1. Name the seven namespaces and the global resource each virtualises.
2. Explain why `CLONE_NEWUSER` lets an unprivileged user create the other namespaces in one `clone`.
3. **Build a mini-container** with `clone`, write its uid/gid maps, and run a command as PID 1.
4. Measure PID and network isolation, and explain why they hold when `mount`/`sethostname` do not.
5. Explain the AppArmor unprivileged-userns restriction and why it produces a capability-less root.
6. Describe cgroup v2 — the unified tree, controllers, and delegation.
7. **Impose a memory limit** and read a cgroup-local OOM kill (exit 137) and a `pids.max` EAGAIN.
8. Measure container startup (~1 ms) and compare it to a VM boot (seconds), from the shared-kernel fact.
9. Explain OverlayFS layers (lower/upper/work/merged, copy-up, whiteouts) and `pivot_root`.
10. Contrast containers and VMs and locate the isolation boundary in each.
11. **Apply a seccomp-BPF filter** unprivileged, and explain `PR_SET_NO_NEW_PRIVS` and capabilities.
12. Recognise "a namespace created is not a capability granted" as this week's "present but not working."

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L34 Namespaces and Building a Container]] | The seven namespaces; `clone`/`unshare`/`setns`; **`CLONE_NEWUSER` carrying the other five** where each alone EPERMs; the parent writing uid/gid maps; **the child measured as PID 1 (host PID 1251803)** and **its netns showing only `lo`, DOWN**; and **`mount`/`sethostname` refused to a capability-stripped namespace-root** — the fifth "present but not working" |
| [[L35 Cgroups and Resource Control]] | Namespaces isolate, cgroups limit; **cgroup v2's unified tree**; **delegation** (memory + pids to `user@1000.service`); **a 100 MB cap OOM-killing the hog at ~90 MB, exit 137**; **`pids.max` turning a fork bomb into EAGAIN**; **startup measured — fork 139 µs, clone 119 µs, clone+6ns 1001 µs** |
| [[L36 Images OverlayFS and the Security Boundary]] | **OverlayFS layers** (copy-up, whiteouts) and `pivot_root`, **measured to EPERM** here; **containers vs VMs** with `uname -r` identical inside and out proving one shared kernel; the syscall-surface boundary; **seccomp-BPF blocking `getpid` unprivileged**; capabilities and how AppArmor applies the container playbook to userns itself |
| [[LAB 11 Run a Program in an Isolated Environment]] | Complete the mini-container, then measure the boundary — PID 1, only `lo`, mount EPERM, OOM 137, seccomp EPERM. **Monday of Week 12** |
| `lab/minic.c` (3 TODOs), `lab/hog.c`, `lab/sec.c`, `lab/cost.c`, `lab/Makefile` | The container skeleton and the measurement tools |
| [[PS 11 Build a Mini-Container]] | Build `container.c` from scratch and characterise its boundary quantitatively. Due **Friday of Week 12** |
| `assignments/ps11/` | `container.c` starter and Makefile |
| [[PROG201 Week11/assignments/QUIZ 11 Week 11 Tuesday\|QUIZ 11 Week 11 Tuesday]] | Ten minutes, covers **Week 10**, answer key printed |
| [[PROG201 Week11/resources/Reading Guide Week 11\|Reading Guide Week 11]] | `man 7 namespaces`/`user_namespaces`/`cgroups`, `man 2 clone`/`seccomp`, the overlayfs docs |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A container is a process with restricted views and a budget — measure each part and you have measured the container.**

| Ingredient | Mechanism | Measured on this machine |
| --- | --- | --- |
| **Isolation — PID** | `CLONE_NEWPID` | child is **PID 1** (host PID 1251803) — one process, two PIDs |
| **Isolation — network** | `CLONE_NEWNET` | **only `lo`, DOWN** vs the host's three interfaces |
| **Isolation — user** | `CLONE_NEWUSER` | **uid 0 inside**, maps to real uid outside — rootless |
| **Isolation — mount/UTS** | `CLONE_NEWNS`/`NEWUTS` | **created but EPERM to use** — capabilities stripped by AppArmor |
| **Shared kernel** | (no virtualisation) | `uname -r` **identical** inside and out |
| **Limit — memory** | cgroup `memory.max` | 100 MB cap → **OOM-killed ~90 MB, exit 137** |
| **Limit — processes** | cgroup `pids.max` | 21st `fork` → **EAGAIN** |
| **Startup cost** | `clone` + 6 namespaces | **~1 ms** vs a VM's seconds — 1000× |
| **Security — syscalls** | seccomp-BPF | `getpid` → **EPERM**, `write` allowed, **unprivileged** |

**Read the mount/UTS row against the rest.** The namespaces are all *created* successfully — the `clone` returns, the child is PID 1, the network is isolated — and yet the privileged *operations* inside two of them are refused, because being root in a user namespace is not the same as holding the capabilities. This is Week 3's `PRIO_INHERIT`, Week 8's lazy binding, and Week 10's inert CET again, at the OS-isolation layer: **a mechanism that is present is not a mechanism that is working**, and the way you tell is that you tried to use it and recorded the errno.

---

### Assessment Reminder

**Labs and quizzes carry no weight** and are still required. **Quiz 11 is at the start of Tuesday's lecture and covers Week 10.** **PS 10 is due this Friday.**

> **Lab 10** — Week 10's fuzzing lab — is sat on the **Monday of this week**. **Lab 11** covers this
> week and is sat on the **Monday of Week 12**. There is no midterm this week.

Both are tracked in [[_PROG 201 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 10** is why this week exists — containers wrap the untrusted program whose bugs you just exploited; **seccomp** is the OS-level answer to "narrow the attack surface." **Week 4's `mprotect`/NX and ASLR** were per-process defences; namespaces are per-*view* isolation. **Week 3's `PRIO_INHERIT`** is the template for the mount/sethostname EPERM. **Week 7's mount and filesystem** material is what OverlayFS layers and `pivot_root` build on.

**Sideways:** **CS 201** on privilege levels and the user/kernel boundary is the hardware underneath the shared-kernel argument — a container never crosses it the way a VM's guest does.

**Forward:** **Week 12's synthesis project** is a service you must ship as an artifact that runs the same everywhere — which is the practical reason containers exist, and the mini-container here is its minimal ancestor. The security discipline of Week 10 plus the isolation of Week 11 is the whole "run untrusted code safely" story the course closes on.

---

*PROG 201 · Week 11 · © CSE Department*

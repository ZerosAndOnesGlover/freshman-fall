# LAB 11 · Run a Program in an Isolated Environment

**PROG 201 · Week 11 · Containers and Virtualization**
**Covers:** Week 11 · sat **Monday of Week 12**, 15:00–16:50, BH 215 · **unmarked, checked off in the session**
**Time:** one lab session · **Submit:** `minic.c` completed, plus `lab11.md` with your measurements

---

## Goal

Build the isolation half of a container by hand — a process in fresh namespaces — and then **measure the boundary**: what the isolation gives you, and where, on this machine, it stops. You will finish a mini-container, confirm its process is PID 1 with an isolated network stack, watch a memory limit kill a runaway, and watch a seccomp filter deny a single syscall. No Docker: `docker`, `podman`, `runc` and `lxc` are **not installed**, which is the point — you are building the primitives they hide.

By the end you can explain, with numbers you measured, why a container starts in a millisecond, why it shares the host's kernel, and why "root inside the container" is not root on the host.

---

## Part 0 — Build

```
$ make
```

`minic.c` has three `TODO`s and will not isolate anything until you complete them. The rest builds clean.

---

## Part 1 — Complete the mini-container (`minic.c`)

The skeleton clones a child and, in the parent, writes the child's uid/gid maps. Three things are missing:

- **TODO 1** — the `clone` **flags**. The child must get a fresh **user, PID, mount, UTS, network and IPC** namespace. Recall from L34 that `CLONE_NEWUSER` must be in the *same* `clone` call — it is what lets an unprivileged user create the rest.
- **TODO 2** — write the child's `uid_map` so container-uid 0 maps to your real uid (`"0 <uid> 1"`), then `setgroups` = `"deny"`, then `gid_map`. Order matters: `setgroups`/`deny` **before** `gid_map`.
- **TODO 3** — in the child, print `getpid()` and `getuid()` so you can see you are PID 1 and uid 0.

Build and run:

```
$ ./minic sh -c 'echo hello from inside; id -u'
[container] I am PID ___          <- fill in what you see
[container] uid = ___
hello from inside
0
```

**Record:** what PID does the child report? What uid? On the host (another terminal), `ps aux | grep minic` — what is the child's *host* PID? Explain why they differ.

## Part 2 — Prove the isolation is real

**PID namespace.** Inside the container run `echo $$` (the shell's PID). It should be a small number. Then:

```
$ ./minic ip -o link show
```

**Record:** how many network interfaces does the container see, and what state is the one interface in? Compare with `ip -o link show` on the host. This is the network namespace — a container starts with no connectivity.

## Part 3 — Where the isolation stops (the deviation)

`minic` tries to `sethostname` and to mount a private `/proc`. On this machine both fail.

```
$ ./minic hostname
mount /proc: Permission denied
...
```

**Record:** the exact error from `sethostname` and from `mount`. Then read the reason:

```
$ cat /proc/sys/kernel/apparmor_restrict_unprivileged_userns
1
```

**Explain in two sentences:** you are uid 0 inside the user namespace, so why are `mount` and `sethostname` refused? (L34 §5.) Which parts of the isolation still work despite this, and why — what makes PID and network isolation different from `mount`?

## Part 4 — A resource limit (memory)

Namespaces isolate but do not limit. `hog` allocates and touches memory forever. Run it capped:

```
$ systemd-run --user --scope -p MemoryMax=100M -p MemorySwapMax=0 ./hog
...
$ echo $?
```

**Record:** at roughly how many MiB is it killed, and what exit code? Decode the exit code (128 + signal). Explain why *only* the hog dies and the host is fine — what is a *cgroup-local* OOM kill?

## Part 5 — Shrinking the syscall surface (seccomp)

```
$ ./sec
write() still works (this printf)
getpid() after filter -> ___, errno=___
```

**Record:** what does `getpid()` return after the filter, and what errno? Which syscall was allowed, which denied? Note that `sec` needs **no privilege** — explain why a process is allowed to restrict *itself* (what does `PR_SET_NO_NEW_PRIVS` guarantee?).

## Part 6 — What isolation costs (optional, for the writeup)

```
$ ./cost
fork+wait                          :  ___ us
clone (no namespaces)              :  ___ us
clone + 6 namespaces (a container) :  ___ us
```

**Record** the three numbers. How much do the six namespaces add over a bare `clone`? Compare your container-startup figure to the "seconds" a virtual machine takes to boot (L36) — how many orders of magnitude?

---

## What to submit

1. **`minic.c`** — completed, compiling clean.
2. **`lab11.md`** — your measured numbers for Parts 1–6 and the short explanations asked in bold, each naming the program that produced the figure.

## Grading (100 pts)

| Part | Points |
| --- | --- |
| P1 — mini-container completed, PID 1 + uid 0 shown, host-vs-container PID explained | 25 |
| P2 — PID + network isolation measured, host comparison | 15 |
| P3 — mount/sethostname EPERM recorded, AppArmor restriction explained | 20 |
| P4 — memory cap: kill point + exit 137 decoded, cgroup-local OOM explained | 20 |
| P5 — seccomp: getpid EPERM recorded, no_new_privs explained | 10 |
| P6 — startup costs measured and compared to a VM | 10 |

**Every number must name the program that produced it.** A measurement that returns EPERM or exit 137 is a *result*, not a failure — record it and say what it means.

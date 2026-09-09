# PROG 201 · Lab 11 Solutions
## Run a Program in an Isolated Environment — Instructor Only

---

**Do not distribute.** These are the completed `minic.c` and the expected measurements.

**Machine these numbers came from:** Ubuntu 24.04, glibc 2.39, Linux 7.0.0-30, cgroup v2,
`apparmor_restrict_unprivileged_userns` = **1**. Startup and OOM numbers vary a little run to run;
the *shape* (PID 1, only `lo`, mount EPERM, exit 137) is invariant on this configuration.

> **No container runtime is installed** — `docker`, `podman`, `runc`, `lxc`, `newuidmap`/`newgidmap`
> and `fuse-overlayfs` are all absent from a student account. This is deliberate: the lab is the
> primitives. `unshare(1)`, `nsenter`, `lsns`, `capsh` and `systemd-run --user` **are** present.
> [[PROG 201 Scheduling Notes]] §22 records the substitutions.

---

## The three TODOs, completed

**TODO 1 — the flags:**
```c
int flags = CLONE_NEWUSER | CLONE_NEWPID | CLONE_NEWNS |
            CLONE_NEWUTS | CLONE_NEWNET | CLONE_NEWIPC | SIGCHLD;
```
`CLONE_NEWUSER` must be present; it is what makes the unprivileged clone succeed. Drop it and the
`clone` returns **EPERM** — the standalone-namespace failure from L34 §3.

**TODO 2 — the maps (parent, after `clone`, in this order):**
```c
char line[64];
snprintf(line, sizeof line, "0 %d 1", getuid());
writemap(pid, "uid_map", line);
writemap(pid, "setgroups", "deny");        /* MUST precede gid_map */
snprintf(line, sizeof line, "0 %d 1", getgid());
writemap(pid, "gid_map", line);
```
`setgroups`=`deny` before `gid_map` is mandatory since Linux 3.19 (closes a group-based
access-check bypass); omit it and the `gid_map` write fails with EPERM.

**TODO 3 — the child prints identity:**
```c
printf("[container] I am PID %d\n", getpid());
printf("[container] uid = %d (root inside the user namespace)\n", getuid());
fflush(stdout);      /* before execvp replaces us */
```

The completed file is [[minic.c]] with the lab's TODO comments replaced by the above; it is the same
as the PS 11 reference `container.c` below minus the argument plumbing.

---

## Expected measurements

**Part 1 — identity.**
```
$ ./minic sh -c 'echo shell-pid $$; id -u'
sethostname: Operation not permitted
mount /proc: Permission denied
[container] I am PID 1
[container] uid = 0 (root inside the user namespace)
shell-pid 1
0
```
Child reports **PID 1**; its **host** PID (from `pgrep -a minic` in another terminal) is a large
number such as **1251803**. One process, two PIDs — the PID namespace renumbers from 1 inside while
the host keeps its global PID. Grading: full marks require *both* numbers and the explanation that
they are the same process seen from two namespaces.

**Part 2 — isolation.**
```
$ ./minic ip -o link show
1: lo: <LOOPBACK> mtu 65536 ... state DOWN ...
```
**One** interface (`lo`), state **DOWN**, vs the host's three (`lo`, `enp0s31f6`, `wlp61s0`). The
container has no route to anywhere until a veth pair is wired in (not possible here — needs
`CAP_NET_ADMIN` on the host side). `echo $$` inside → `1`.

**Part 3 — the deviation (the point of the lab).**
```
sethostname("container") -> Operation not permitted   (EPERM)
mount("proc", "/proc", ...) -> Permission denied       (EACCES/EPERM)
$ cat /proc/sys/kernel/apparmor_restrict_unprivileged_userns
1
```
Model answer: *We are uid 0 in the user namespace, but Ubuntu's AppArmor restriction hands out
unprivileged user namespaces with their capabilities stripped, so `CAP_SYS_ADMIN`-gated operations
(`mount`, `sethostname`) are refused even to namespace-root. PID and network isolation still hold
because they are properties of the namespace's **existence**, enforced by the kernel at creation,
not operations we must perform afterwards.* This is the fifth "present but not working" finding of
the course (Week 3 PRIO_INHERIT, Week 8 lazy binding, Week 10 ASLR-without-PIE, Week 10 inert CET).

**Part 4 — memory.**
```
$ systemd-run --user --scope -p MemoryMax=100M -p MemorySwapMax=0 ./hog
Running scope as unit: run-rXXXX.scope
touched 64 MiB
Killed
$ echo $?
137
```
Killed near **~90 MiB touched** (the exact point drifts with the runtime's own footprint in the
scope); **137 = 128 + 9 (SIGKILL)**. Cgroup-local OOM: only a process *in that cgroup* is a
candidate, so the host and shell are untouched. Grading: the exit code must be *decoded*, not just
quoted.

**Part 5 — seccomp.**
```
$ ./sec
write() still works (this printf)
getpid() after filter -> -1, errno=Operation not permitted
```
`write` allowed, `getpid` → **-1 / EPERM**. No privilege needed because a process may always narrow
its *own* rights; `PR_SET_NO_NEW_PRIVS` guarantees the filter cannot be used to gain privilege
through a later `execve` of a setuid binary, which is the precondition the kernel requires.

**Part 6 — cost (optional).**
```
$ ./cost
fork+wait                          :  139.2 us
clone (no namespaces)              :  119.4 us
clone + 6 namespaces (a container) : 1001.5 us
```
Namespaces add **~880 µs** over a bare clone. Container startup **~1 ms** vs a VM's **~seconds**:
about **three orders of magnitude**. Accept any figures of the same order; the comparison and the
"namespaces are the cost, not the clone" reading are what earn the marks.

---

## Common student errors

- **Child races the maps** → `id -u` prints **65534** (nobody). Cause: no pipe sync, child runs
  before the parent writes `uid_map`. The pipe in the skeleton is there precisely to prevent this;
  if they removed it, that is the bug.
- **`gid_map` write fails** → they wrote `gid_map` before `setgroups`=`deny`. Order matters.
- **"mount succeeded!" claimed** → almost always they read a *stale* `/proc` (the host's, inherited)
  and mistook host processes for a successful private mount. On this machine the mount **fails**;
  the correct writeup records the EPERM.
- **Reporting the EPERM as "the lab is broken."** It is the graded finding. Dock nothing for the
  errno; dock for not explaining it.
- **Committing the compiled `minic`/`hog`/`sec`/`cost`.** Build products are not submitted.

---

*PROG 201 · Week 11 · Lab 11 Solutions · Instructor Only*

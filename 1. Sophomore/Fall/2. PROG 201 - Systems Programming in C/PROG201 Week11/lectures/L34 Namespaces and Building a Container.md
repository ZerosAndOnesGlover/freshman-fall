# PROG 201 · Systems Programming in C
## Week 11 · Lecture 1 of 3
### Namespaces, and Building a Container from Them

*“Systems have sub-systems and sub-systems have sub-systems and so on ad infinitum - which is why we're always starting over.”* — Alan Perlis, "Epigrams on Programming" (1982), #52

---

**Reading:** TLPI Ch. 28 (`clone`), Ch. 30 · `man 7 namespaces`, `man 7 user_namespaces`, `man 2 clone`, `man 2 unshare`, `man 2 setns` · **Previous:** L33 · **Next:** L35 — cgroups and resource control

**Coursework:** 📊 **Quiz 11** today · 📝 **PS 11** released Wed this week, due Fri of Week 12 17:00 · 📝 **PS 10** due Fri this week 17:00 · 🔬 **Lab 11** Mon of Week 12 15:00–16:50

---

## 1. A Container Is a Process

The one sentence to carry out of this week: **a container is not a virtual machine — it is an ordinary Linux process (or a few) with a restricted view of the system.** It runs on the host's kernel, is scheduled by the host's scheduler, and shows up in the host's process table. What makes it a "container" is that it has been given private *views* of a handful of global resources.

Those private views are **namespaces**. There are seven kinds, and each one virtualises one global thing:

| Namespace | `clone` flag | Private view of |
| --- | --- | --- |
| **PID** | `CLONE_NEWPID` | process IDs — the first process is PID 1 and cannot see others |
| **Network** | `CLONE_NEWNET` | interfaces, routes, ports — its own stack |
| **Mount** | `CLONE_NEWNS` | the filesystem tree — its own mounts |
| **UTS** | `CLONE_NEWUTS` | the hostname and domain name |
| **IPC** | `CLONE_NEWIPC` | System V IPC and POSIX message queues |
| **User** | `CLONE_NEWUSER` | user and group IDs — root inside, unprivileged outside |
| **Cgroup** | `CLONE_NEWCGROUP` | the cgroup tree root |

**Every process is already in seven namespaces** — the host's. You can see them:

```
$ ls -l /proc/self/ns/
pid  -> pid:[4026531836]
net  -> net:[4026531833]
mnt  -> mnt:[4026531832]
user -> user:[4026531837]
...
```

Those inode numbers *are* the namespaces. Two processes with the same number for a type share that namespace; a container is a process with **different** numbers. `lsns` lists them all:

```
$ lsns -t net
        NS TYPE NPROCS    PID USER   COMMAND
4026531833 net     161 257543 ...    /usr/bin/pipewire     <- 161 processes, one namespace
```

**Docker is not installed on these machines** (nor podman, lxc or runc), which is convenient, because it means the whole week is the primitives rather than a tool that hides them. Docker is `clone` plus cgroups plus an overlay filesystem, and you are about to build the first of those by hand.

---

## 2. The Three System Calls

**`clone`** is `fork` with a flags argument. Where `fork` copies everything, `clone` lets you choose — including which namespaces the child gets fresh:

```c
int flags = CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWUTS | SIGCHLD;
pid_t pid = clone(child_fn, stack_top, flags, arg);
```

The child runs `child_fn` in the new namespaces. This is what a container runtime calls; it is `fork`+`exec` with the namespace flags added.

**`unshare`** moves the *calling* process into new namespaces without a fork — `unshare(CLONE_NEWNS)` gives you a private mount namespace right here. The `unshare(1)` command is a thin wrapper.

**`setns`** does the opposite: it moves you *into an existing* namespace, given a file descriptor to `/proc/<pid>/ns/<type>`. This is how `docker exec` and `nsenter` get a shell inside a running container — they open the container's namespace files and `setns` into them.

Three verbs: **make new** (`clone`, `unshare`), **join existing** (`setns`).

---

## 3. The User Namespace Is the Key That Unlocks the Rest

Creating most namespaces needs `CAP_SYS_ADMIN` — normally root. But there is one exception that changes everything: **`CLONE_NEWUSER` needs no privilege**, and inside a new user namespace you are **root** — with all capabilities *within that namespace*.

So the unprivileged idiom is to create the user namespace **in the same `clone` call** as the others:

```c
int flags = CLONE_NEWUSER | CLONE_NEWPID | CLONE_NEWNET |
            CLONE_NEWNS | CLONE_NEWUTS | CLONE_NEWIPC | SIGCHLD;
pid_t pid = clone(child, stack_top, flags, arg);
```

Measured: this **succeeds for an ordinary user**, where each of the others *alone* fails:

```
CLONE_NEWUSER                          -> OK
CLONE_NEWPID   (alone)                 -> Operation not permitted
CLONE_NEWUSER|PID|NET|NS|UTS|IPC       -> OK       <- the user namespace carries the rest
```

The catch is identity. Inside the new user namespace, before you set up a mapping, your uid shows as **65534** (`nobody`) — you are root in the namespace but mapped to nobody outside. To become a usable root-in-container, the **parent** writes a mapping into `/proc/<child>/uid_map`:

```c
/* map container uid 0 to our real uid, one id */
snprintf(line, ..., "0 %d 1", getuid());        /* "0 1000 1" */
write("/proc/<pid>/uid_map", line);
write("/proc/<pid>/setgroups", "deny");         /* required before gid_map */
write("/proc/<pid>/gid_map", "0 <gid> 1");
```

Now the child sees itself as uid 0, and every file it creates is owned, on the host, by *your* uid. **This is rootless containers** — how Podman and modern Docker run without a daemon and without real root, and it is the single most important security improvement in the container world in the last decade.

---

## 4. What the Mini-Container Actually Does

`minic.c` (PS 11) is about eighty lines: `clone` with the six flags, write the maps from the parent, and in the child `sethostname`, mount a private `/proc`, and `exec` the command. Run it:

```
$ ./minic sh -c 'echo "PID $$"; id -u'
[container] I am PID 1
[container] uid = 0 (root inside the user namespace)
PID 1
uid=0
```

**The child is PID 1** — its own PID namespace. Confirmed from both sides: the child's `getpid()` is 1, and the parent's `clone()` returned the child's *host* PID, `1251803`. **One process, two PIDs**, which is exactly what a PID namespace is.

The network namespace is genuinely isolated. Inside, via netlink:

```
$ ./minic ip -o link show
1: lo: <LOOPBACK> ... state DOWN            <- only loopback, and it is down
```

against the host's three interfaces. **A fresh network namespace has one interface, `lo`, and it is down** — a container starts with no connectivity until something wires it up (a veth pair to the host, which is what Docker's bridge does).

---

## 5. Namespace Creation Versus Privilege Within It

Here is where this machine teaches a lesson the curriculum does not plan for, and it is worth the whole lecture. **Creating the namespaces works. Doing privileged things inside them does not:**

```
sethostname("box")             -> Operation not permitted
mount("proc", "/proc", ...)    -> Permission denied
mount(NULL, "/", MS_PRIVATE)   -> Permission denied
```

You are uid 0 in the user namespace, and yet `sethostname` and `mount` are refused. The reason is **`/proc/sys/kernel/apparmor_restrict_unprivileged_userns`, which is 1** on Ubuntu 24.04: after the Spectre/container-escape decade, the distribution decided that **an unprivileged user namespace should be able to exist but should not carry real capabilities**, because unprivileged userns has been the root cause of a long list of kernel privilege-escalation bugs (it is a large, complex attack surface reachable by any user). So you get root-in-namespace with its capabilities stripped by an AppArmor mediation.

The consequence for the mini-container is precise: the **kernel-enforced isolation works** — PID 1, an isolated network stack — because those are properties of the namespace itself. The **userspace setup that makes the isolation cosmetically complete does not** — you cannot remount `/proc`, so `ps` inside still shows the host's processes through the inherited mount, and you cannot set the hostname.

**This is the same shape the course has now met four times:** a mechanism that is present but not fully working — Week 3's `PRIO_INHERIT`, Week 8's lazy binding, Week 10's inert CET markers, and now capabilities inside a restricted user namespace. On a machine where the restriction is off (or run as real root, or with the `newuidmap` setuid helpers), `minic` does everything; here, it does the half the kernel enforces directly. **The build record documents exactly which half, and why**, and PS 11 asks you to measure the boundary rather than pretend it is not there.

---

## Summary

- **A container is a process with private views of global resources** — it runs on the host kernel, not a guest one.
- **Seven namespaces**, one per global thing: PID, net, mount, UTS, IPC, user, cgroup. Every process is already in the host's seven; a container has different ones. `/proc/self/ns/` shows the inode numbers.
- **`clone` makes new namespaces, `unshare` moves you into new ones, `setns` joins existing ones** — the last is how `docker exec` works.
- **`CLONE_NEWUSER` needs no privilege and carries the rest**: created together in one `clone`, an ordinary user gets all six namespaces where each alone would fail. The parent writes `uid_map`/`gid_map` to become usable root inside — **rootless containers**.
- **Measured:** the child is **PID 1** (host PID 1251803), and its network namespace has **only `lo`, down**.
- **On this machine, capabilities inside the unprivileged user namespace are stripped** (`apparmor_restrict_unprivileged_userns=1`), so `sethostname` and `mount` are EPERM even as uid 0. The kernel-enforced isolation (PID, net) works; the userspace setup (a fresh `/proc`, the hostname) does not — a fifth "present but not working" finding.

---

## Exercises

1. Print `/proc/self/ns/*` for your shell and for a `unshare --user` child. Which inode numbers changed?
2. Build the mini-container and confirm the child is PID 1 from *both* sides — its own `getpid` and the parent's `clone` return value. Why are they different?
3. Run `ip link` inside the network namespace and on the host. What is the one interface, and what state is it in? What would you have to build for the container to reach the network?
4. Write the `uid_map` as `0 <uid> 1` and then as a range. What does the container see for `id -u` in each case, and what owns a file it creates, on the host?
5. Try `sethostname` and `mount` inside your container and record the exact errno. Read `apparmor_restrict_unprivileged_userns` and explain why you are a capability-less root.
6. Use `nsenter -t <pid> -a` (or `setns` in C) to get a second shell into a running container. Which namespace files did it open?
7. Compare `unshare --user --map-root-user` on this machine (it fails at `uid_map`) with the `clone` + parent-writes-map approach (it works). What is different about who writes the map?

---

*PROG 201 · Week 11 · L34 · © CSE Department*

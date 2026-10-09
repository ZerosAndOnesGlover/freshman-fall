# PROG 201 · Systems Programming in C
## Week 11 · Lecture 3 of 3
### Images, OverlayFS, and the Security Boundary

*“You can't trust code that you did not totally create yourself. (Especially code from companies that employ people like me.) No amount of source-level verification or scrutiny will protect you from using untrusted code.”* — Ken Thompson, "Reflections on Trusting Trust", Turing Award Lecture (1984)

---

**Reading:** `man 8 mount` (overlay) · kernel docs `Documentation/filesystems/overlayfs.rst` · `man 2 seccomp`, `man 2 pivot_root` · `man 7 capabilities` · **Previous:** L35 — cgroups · **Next:** Lab 11, PS 11

**Coursework:** 📝 **PS 10** due Fri this week 17:00 · 🔬 **Lab 11** Mon of Week 12 15:00–16:50

---

## 1. Where the Filesystem Comes From

A container needs a filesystem — a `/`, a `/bin/sh`, libraries. It would be wasteful to give each container a full private copy of a distribution: a hundred containers of the same image would be a hundred identical gigabytes. The trick is **layers**: a read-only base image shared by all, plus a thin writable layer per container where its changes go. The mechanism is a **union filesystem**, and on Linux it is **OverlayFS**.

OverlayFS stacks directories. You give it a **lowerdir** (read-only, the image), an **upperdir** (writable, this container's changes), a **workdir** (scratch it needs), and a **merged** mountpoint that shows the union:

```
mount -t overlay overlay \
  -o lowerdir=/image,upperdir=/box/upper,workdir=/box/work \
  /box/merged
```

Reads come from `upperdir` if present, else fall through to `lowerdir`. Writes go to `upperdir`. Deleting a file from the lower layer writes a **whiteout** marker in the upper — the file is gone from the merged view but the read-only lower is never touched. This is **copy-up on write**: the base stays pristine and shared; only the delta is per-container. It is exactly how a Docker image's layers stack, and why `docker commit` is cheap — it freezes the upper layer into a new lower one.

**Measured on this machine:** creating an overlay mount as an ordinary user fails —

```
$ mount -t overlay overlay -o lowerdir=... /box/merged
mount: only root can use "--options" option        (must be superuser to use mount)
```

— and inside the unprivileged user namespace it is EPERM as well, the same `apparmor_restrict_unprivileged_userns` boundary from L34: even as uid 0 in the namespace, `mount` is refused. So on **this** image, the mini-container runs the command against the **host's** root filesystem (the mount namespace is created but not re-populated), and the overlay layering is presented as the mechanism a runtime uses where mount is permitted (real root, the restriction off, or the setuid `newuidmap`/`fuse-overlayfs` helpers, none of which are installed here). The build record records that the layering step is described-and-measured-to-EPERM rather than run — the honest state on this machine.

The final assembly step, once you *can* mount, is **`pivot_root`**: it swaps the process's root directory to the merged overlay and detaches the old one, so the container truly sees the image as `/` with no path back to the host tree. `pivot_root` needs `CAP_SYS_ADMIN` in the mount namespace — the same capability that is stripped here.

---

## 2. Containers Versus Virtual Machines

Now the comparison the whole week builds toward. Both isolate workloads; they draw the line in completely different places.

```
   CONTAINERS                          VIRTUAL MACHINES

  ┌──────┐ ┌──────┐                  ┌──────────┐ ┌──────────┐
  │ app  │ │ app  │                  │   app    │ │   app    │
  │ libs │ │ libs │                  │  libs    │ │  libs    │
  └──────┘ └──────┘                  │ guest OS │ │ guest OS │
  ┌──────────────┐                   │  kernel  │ │  kernel  │
  │ ONE host     │  <- shared        └──────────┘ └──────────┘
  │   kernel     │                   ┌──────────────────────┐
  └──────────────┘                   │      hypervisor      │
  ┌──────────────┐                   ┌──────────────────────┐
  │   hardware   │                   │  host kernel + HW     │
  └──────────────┘                   └──────────────────────┘
```

A **VM** virtualises the *hardware*. The hypervisor (KVM, using the CPU's VT-x/AMD-V extensions) presents virtual CPUs, memory, and devices; each guest boots its **own kernel**. Isolation is near-total — a guest can run a different OS entirely — and the boundary is the hardware virtualisation, which is very hard to cross. The cost is that each VM carries a whole kernel and userland and takes **seconds** to boot.

A **container** shares the host kernel. The proof is one command, run inside the mini-container and on the host:

```
$ uname -r          # inside the container
7.0.0-30-generic
$ uname -r          # on the host
7.0.0-30-generic        <- identical: there is only ONE kernel
```

**Same kernel, inside and out.** A container cannot run a different kernel, cannot load its own kernel modules, and — the crucial security consequence — **every container's system calls are served by the one host kernel.** This is why L35's startup number was ~1 ms and a VM's is seconds: the container skips the entire boot.

The trade-off is the security boundary. A VM escape means defeating hardware virtualisation. A **container escape means finding one bug in the host kernel's system-call surface** — and every container reaches that same surface. Sharing the kernel is what makes containers cheap and what makes them a weaker isolation boundary than a VM. You choose per workload: containers to pack many instances of trusted-ish code densely; VMs (or the two combined, containers *inside* VMs, which is what cloud providers do) when the boundary must hold against hostile code.

---

## 3. Shrinking the Attack Surface: seccomp

If the danger is the system-call surface, the defence is to **narrow it**: forbid a container from calling syscalls it does not need, so a kernel bug in an unused syscall is unreachable. The mechanism is **seccomp-BPF** — a small BPF program, attached to the process, that the kernel runs on *every* system call to decide allow / deny / kill.

Crucially, **seccomp needs no privilege** — any process may voluntarily restrict itself, as long as it first sets `no_new_privs` (so it cannot use the restriction to trick a setuid program). `sec.c` demonstrates it unprivileged: allow everything, but return EPERM for `getpid`:

```c
prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
/* BPF: default ALLOW; if nr == __NR_getpid -> ERRNO(EPERM) */
prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
```

```
$ ./sec
write() before filter: ok
after filter:
  write("hello")  -> ok                         (allowed)
  getpid()        -> -1, errno = Operation not permitted   (blocked)
```

**`write` still works; `getpid` is now denied to this process** — the kernel intercepted the syscall and returned EPERM without ever entering `getpid`'s implementation. This works with no root and no user namespace. Docker ships a default seccomp profile that blocks ~44 dangerous syscalls (`mount`, `kexec_load`, `ptrace`, `bpf`, ...); that profile is exactly this mechanism with a longer allow/deny list. seccomp is the single most effective hardening a container has, precisely because it shrinks the shared surface that L36's whole argument is about.

The companion is **capabilities**: root is not one privilege but ~40 (`CAP_NET_ADMIN`, `CAP_SYS_MODULE`, `CAP_SYS_ADMIN`, ...), and a container is normally given a small subset and stripped of the rest, so "root inside the container" cannot load modules or reconfigure the host network. On this machine the AppArmor userns restriction is *doing exactly this* — it hands the container a user namespace with its capabilities already stripped, which is why L34's `mount` and `sethostname` were EPERM. The distribution applied the container-hardening playbook to unprivileged user namespaces themselves.

---

## 4. The Week in One Picture

A container is the composition of everything measured this week:

- **Namespaces** (L34) — private views: PID 1, only `lo`, a would-be private mount. *Isolation.* Measured: PID and net work; mount/UTS are EPERM here.
- **Cgroups** (L35) — budgets: memory (OOM at 137), pids (EAGAIN), cpu. *Resource control.* Measured: delegated and working.
- **Overlay + pivot_root** (L36) — a layered, per-container root from a shared image. *Packaging.* Measured to EPERM here; the mechanism described.
- **seccomp + capabilities** (L36) — a narrowed syscall surface and a reduced root. *Security.* Measured: seccomp works unprivileged.

None of it is a virtual machine. All of it is one host kernel, serving processes that have been given restricted views, budgets, and a smaller reach — which is the entire idea, and why it starts in a millisecond and why the kernel it shares is both its efficiency and its risk.

---

## Summary

- **Images are layers.** OverlayFS unions a read-only `lowerdir` (shared image) with a writable `upperdir` (per-container delta); writes copy-up, deletes leave whiteouts, the base stays pristine — Docker's layers exactly. **Measured:** `mount -t overlay` needs root and is EPERM in the unprivileged userns here, so the mini-container runs against the host root; layering is the described mechanism. **`pivot_root`** finishes the job where mount is allowed.
- **Container vs VM:** a VM virtualises hardware and boots its **own kernel** (near-total isolation, seconds to boot); a container **shares the host kernel** (~1 ms, weaker boundary). **Measured:** `uname -r` is identical inside and out — one kernel.
- **The container security boundary is the host's syscall surface** — an escape is one host-kernel bug, reachable by every container. A VM escape is defeating hardware virtualisation.
- **seccomp-BPF narrows that surface** with no privilege: **measured**, `write` allowed and `getpid` → EPERM in the same process after `PR_SET_NO_NEW_PRIVS`. **Capabilities** split root into ~40 pieces; the AppArmor userns restriction is that playbook applied to user namespaces, and the reason L34's mount/sethostname were EPERM.

---

## Exercises

1. Build a two-layer overlay by hand (as root, or explain the exact EPERM you get unprivileged). Create a file in `merged`, then find it in `upperdir` and confirm `lowerdir` is untouched. Delete a lower file and find the whiteout.
2. Why is `docker commit` cheap? Relate it to which overlay layer becomes a new lowerdir.
3. Run `uname -r` inside the mini-container and on the host. Explain in one sentence why they must be equal and what that implies for running a different OS in a container.
4. Draw the container and VM stacks and mark, on each, exactly where the isolation boundary is. For each, state what an attacker must defeat to escape.
5. Extend `sec.c` to also block `open`. Confirm `write` still works and `open` now fails. Why must `PR_SET_NO_NEW_PRIVS` come first?
6. Read Docker's default seccomp profile (or its list of blocked syscalls). Pick three blocked calls and explain what host damage each could do.
7. List the capabilities a default Docker container keeps and three it drops. For each dropped one, name the host operation it would have allowed. How does this relate to the userns restriction on this machine?

---

*PROG 201 · Week 11 · L36 · © CSE Department*

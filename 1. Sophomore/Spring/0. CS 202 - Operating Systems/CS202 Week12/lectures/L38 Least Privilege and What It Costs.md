# CS 202 · Operating Systems
## Week 12 · Lecture 2 of 3
### Least Privilege, and What It Costs

---

**Sat:** Wednesday of Week 12, 09:00–09:50, VNC 101 · **Reading:** Saltzer & Schroeder §I.A; `man 2 seccomp`, `man 7 capabilities` · **Next:** L39, what this course was about

---

## §1 · The One Principle That Scales

**Saltzer and Schroeder, 1975, eight design principles.** Seven are good advice. One is the reason this lecture exists:

> **Least privilege:** every program and every user should operate using the least set of privileges
> necessary to complete the job.

**Why it is different from the others:** every other defence in L37 tries to stop the bug. Least privilege **assumes the bug wins** and asks what the attacker gets. It is the only principle whose value does not depend on your code being correct — which is fortunate, because your code is not correct.

**The test of whether a system follows it is a counting exercise.** For each component, ask: *what could this do if it were completely hostile?* On the reference machine, for `/usr/bin/passwd`, the answer is **anything at all**, because it runs as root. That is the state of the art from 1975, and this lecture is about the four mechanisms Linux has added since to do better.

---

## §2 · setuid: The Mechanism That Cannot Say "A Little"

**`passwd` needs to write `/etc/shadow`, which is mode 0640 root:shadow.** You are not root. So the file carries a bit:

```
-rwsr-xr-x root /usr/bin/passwd
   ^
   the setuid bit: on execve, the effective uid becomes the file's owner
```

**The program runs as root. Not "as root for the purpose of writing one file" — as root.** It can also load a kernel module, read every file on the machine, and kill any process. It does not want any of that; the kernel has no way to offer less.

**What that costs, measured:** 18 such programs on this machine (L37 §2), each a complete compromise if it is wrong. **`pkexec` was wrong for twelve years.**

**And the bit is sticky in a way that matters for §4.** If a sandboxed process could still gain privilege through `execve` of a setuid binary, every sandbox would be escapable by running `/usr/bin/su`. The kernel's answer is a per-process flag:

```c
prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
```

**Once set, it is inherited by children and can never be unset**, and `execve` of a setuid binary silently declines to raise the uid. **The kernel refuses to install an unprivileged seccomp filter without it** — which tells you the kernel developers considered a sandbox that does not set it to be broken by construction.

---

## §3 · Capabilities: Root, Cut Into Forty Pieces

**Linux split root's authority into individual bits.** `ping` needs to open a raw socket — `CAP_NET_RAW` — and nothing else:

```bash
getcap -r /usr/bin /usr/sbin /usr/lib
/usr/bin/ping                       cap_net_raw=ep
/usr/bin/mtr-packet                 cap_net_raw=ep
.../gst-ptp-helper                  cap_net_bind_service,cap_net_admin,cap_sys_nice=ep
.../snapd/snap-confine              cap_chown,cap_dac_override,cap_dac_read_search,cap_fowner,
                                    cap_setgid,cap_setuid,cap_sys_chroot,cap_sys_ptrace,
                                    cap_sys_admin,cap_sys_resource=p
```

**`ping` used to be setuid root.** Now it is not on the setuid list at all, and a bug in it yields the ability to send raw packets rather than the ability to do everything. **That is least privilege working, in production, on this machine.**

**The `e` and `p` are the interesting part.** Every process has capability *sets*, visible for your own shell:

```bash
grep Cap /proc/self/status
CapInh: 0000000000000000     # inheritable: passed across execve
CapPrm: 0000000000000000     # permitted:   may be raised into effective
CapEff: 0000000000000000     # effective:   checked right now
CapBnd: 000001ffffffffff     # bounding:    the ceiling; can only ever be lowered
```

**This shell has none of the 41 capabilities and a bounding set containing all of them** — the ceiling is high, the current holding is zero. A privileged program *drops* capabilities by removing them from the permitted set, and drops them permanently by removing them from the bounding set.

**Now the honest assessment, because capabilities are often oversold.** **`CAP_SYS_ADMIN` is on that list of 41**, and it governs `mount`, `setns`, `pivot_root`, `bpf`, and roughly thirty other unrelated things. It is called "the new root" for good reason. **`snap-confine` above holds it.** Splitting root into forty pieces helps only if the pieces are small, and one of them is not.

**And `CAP_DAC_OVERRIDE` — also held by `snap-confine` — means "ignore file permission bits entirely".** A program with that capability and a path-handling bug is, for practical purposes, root.

---

## §4 · seccomp: Taking Away System Calls, and What It Costs

**Capabilities restrict what a privileged program may do. Seccomp restricts what *any* program may do**, by filtering system calls with a BPF program the process installs on itself. It is the mechanism underneath Chrome's renderer sandbox, systemd's `SystemCallFilter=`, Docker's default profile and every serverless runtime you have used.

**The filter is a BPF program over a small struct**: the architecture, the system call number, and the six arguments as raw integers. It returns `ALLOW`, `ERRNO`, `TRAP`, `KILL_THREAD` or `KILL_PROCESS`. **It is installed once and can never be removed** — only added to, and every filter installed must pass.

```c
struct sock_filter f[] = {
	BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
	BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, SYS_write, 0, 1),
	BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),
	BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
};
prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
syscall(SYS_seccomp, SECCOMP_SET_MODE_FILTER, 0, &prog);
```

**`jailed.c` runs exactly that.** The `printf` before the filter works; the `write` after it does not:

```
before the filter: this line is a write()
Bad system call (core dumped)        exit status 159 = 128 + 31 = SIGSYS
```

**`SIGSYS`, not `SIGKILL`.** The distinction is useful: a program killed by signal 31 was killed *by policy*, and a supervisor can say so instead of reporting a mysterious crash.

### What it costs

**Every system call now runs a BPF program before it does anything.** That is a real cost and it is worth knowing, because "just sandbox it" is advice with a price.

`seccost.c` measures a `getppid()` — the cheapest system call there is — with and without a filter, **in the same process**, taking the minimum of five batches of 200,000, and reporting the **median of the difference across 15 runs**:

| Filter | Cost per system call |
|---|---|
| **Control: no filter, measured twice** | **−3.4 ns** *(that is, nothing)* |
| 1 filter, 6 instructions | **+51.0 ns** |
| 1 filter, 15 instructions | **+51.9 ns** |
| 1 filter, 55 instructions | **+49.1 ns** |
| 1 filter, **205 instructions** | **+52.7 ns** |
| **5 filters stacked**, 15 instructions each | **+48.9 ns** |

**Read that table twice.** A 205-instruction filter costs the same as a 6-instruction one. **Five stacked filters cost the same as one.** The cost is not the rules — **the cost is the check**: the branch on the syscall entry path that notices this task has a filter at all, plus the fixed cost of entering the BPF machinery. The rules themselves are JIT-compiled to native code (`net.core.bpf_jit_enable = 1` here) and are lost in the noise.

**The engineering consequence is the opposite of most people's intuition: write the filter you actually want.** There is no reason to economise on rules. There is every reason to avoid a filter on a hot path that does not need one — 50 ns on a base cost of about **800 ns**, which is what a system call costs on this machine with Meltdown and Spectre mitigations enabled, is **6%**.

> **Why the base is 800 ns and not 80.** Look at `/sys/devices/system/cpu/vulnerabilities/` on this
> machine: **PTI** for Meltdown (a page-table switch on every entry — Week 5's CR3 write, and the
> TLB cost that follows), **IBRS** for Spectre v2 and retbleed, **clear-CPU-buffers** for MDS and
> MMIO stale data, and **IBPB before exit to userspace** for vmscape. **Every one of those is paid
> on the system call path.** The security of this machine is the reason its system calls are slow,
> and you measured the result in Week 0 without knowing what it was made of.

### The first measurement said the filter made system calls faster

**It did not.** The first harness ran one timed loop with no filter, installed the filter, ran another, and reported 1,044 ns before and 868 ns after. **A seccomp filter cannot make a system call 17% faster**, so the harness was measuring something else — **the CPU's frequency ramp**. An idle laptop runs the first loop at a low clock and speeds up. The fix was a warm-up pass, the minimum of several batches rather than the mean, and a **control that measures the baseline twice and reports −3.4 ns.** **A control that returns zero is the cheapest way to find out that your instrument works** — and it is the check that was missing from three broken harnesses earlier in this course.

---

## §5 · The Allowlist You Cannot Write From Memory

**Now the practical problem.** A sandbox needs a list of permitted system calls. Write one for this program:

```c
int main(void) { printf("nothing to see here\n"); return 0; }
```

**A reasonable list**: `write`, `exit_group`, `brk`, `mmap`, `munmap`, `mprotect`, `fstat`, `execve`, `arch_prctl`, `openat`, `close`, `read`, `pread64`, `access`, `set_tid_address`, `set_robust_list`, `prlimit64`, `getrandom`, `futex`. That is generous — it already includes everything the dynamic loader does, because **the loader runs inside the sandbox too**, before `main`.

**It is still wrong. The program dies with `SIGSYS` before printing anything.**

```bash
strace -c ./victim quiet
...
  0.44    0.000006           6         1           rseq
```

**`rseq`.** Restartable sequences — a mechanism glibc registers at start-up so that per-CPU data structures can be updated without atomics. **It appears in no program's source code.** It appeared in glibc 2.35, which means an allowlist that worked on Ubuntu 20.04 kills every process on 24.04.

**With `SYS_rseq` added, the same jail runs `/bin/echo hi` successfully.**

**This is the practical lesson of the whole lecture.** Least privilege is the right principle and **the policy cannot be written from first principles** — it has to be *derived*, from tracing the program on the system it will run on, and re-derived when the libc changes. A policy that is too tight is an outage; a policy that is too loose is theatre. Every real sandbox (systemd's `@system-service` set, Docker's 60-odd denied calls) is a curated list maintained by people who got paged.

**And note what the filter can and cannot see.** It gets the system call number and the arguments **as integers**. It cannot follow a pointer — there is no way to write "allow `openat` only under `/tmp`", because the path is behind a pointer that another thread could change after the check and before the use. **That is a TOCTOU race, and it is why seccomp deliberately refuses to dereference anything.** Path-based policy needs a different mechanism, which is §7's.

---

## §6 · Limits: Two Mechanisms for One Job, and Only One Works

**Denial of service is the third leg of the triad** and the one students forget. A program that cannot read your files but can consume all the memory has still ruined your afternoon. **Week 6 met this as the OOM killer**; here it is as policy.

**`setrlimit` is the old mechanism**, per-process, inherited across `fork` and `execve`. Four of them matter, and `jail.c` sets them:

| Limit | What it caps | Measured, in the jail |
|---|---|---|
| `RLIMIT_CPU` | CPU seconds | **`-t 1` on a spin loop: killed by `SIGXCPU` after 0.999s of CPU** |
| `RLIMIT_AS` | address space | **`-m 64`: `malloc` failed after 61 MiB** |
| `RLIMIT_NOFILE` | open descriptors | **`-f 32`: `open` failed after 29** (three were already open) |
| `RLIMIT_NPROC` | processes | **see below** |

**Two details in those numbers.**

**`SIGXCPU`, not `SIGKILL` — but only because of how the limit was set.** `RLIMIT_CPU` sends `SIGXCPU` at the *soft* limit, which a program may catch to checkpoint its work, and `SIGKILL` at the *hard* limit. Setting both to 1 second turns the warning into an execution, and the first version of `jail.c` did exactly that and reported `SIGKILL`. **Soft 1, hard 2 gives the program its warning.**

**61 MiB, not 64.** `RLIMIT_AS` caps the *address space*, and the program's code, libc, stack and allocator metadata are in that address space before `main` starts. The gap is the tax.

**And now `RLIMIT_NPROC`, which does not do what it appears to do:**

```
-p 100  fork failed after 0 children
-p 300  fork failed after 0 children
-p 700  fork failed after 0 children
```

**Zero children, at every limit.** `RLIMIT_NPROC` is not a limit on this process's children. **It is a limit on the number of processes belonging to this *real user ID*, checked at every `fork` anywhere** — and this account already owns **134 processes and 1,068 threads**. The jail sets a limit of 700 and the check fails immediately, because the desktop session is already over it.

**The cgroup does the job correctly:**

```bash
mkdir /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/w12test
echo 20 > .../w12test/pids.max
echo $BASHPID > .../w12test/cgroup.procs && exec ./victim fork
fork failed after 19 children: Resource temporarily unavailable
```

**Exactly 19 children, then refusal** — 19 plus the parent is 20. **The cgroup counts the thing you asked about; the rlimit counts the user.** This user's delegated controllers are `cpu memory pids`, the same mechanism Week 6 used for `memory.max` to provoke the OOM killer.

**The general point, and it applies far beyond this example:** when two mechanisms appear to do the same job, **one of them usually has a scope you did not check.** The rlimit is a 1980s interface whose unit is the user; the cgroup is a 2010s interface whose unit is the group of processes you nominated. Only the second composes.

---

## §7 · The Mechanisms This Machine Will Not Let Us Use

**Namespaces are how containers are built** — a process gets its own view of PIDs, mounts, network interfaces, or user IDs. **On this machine, unprivileged namespaces are refused:**

```bash
unshare -Ur id
unshare: write failed /proc/self/uid_map: Operation not permitted
unshare -m true
unshare: unshare failed: Operation not permitted

cat /proc/sys/kernel/apparmor_restrict_unprivileged_userns    # 1
```

**Ubuntu 24.04 restricts unprivileged user namespaces through AppArmor**, because they have been the source of a long series of local privilege escalations: a user namespace hands you `CAP_SYS_ADMIN` *inside* it, and every kernel interface that did not carefully distinguish "root in a namespace" from "root" became an escalation. **The mitigation is to take away the mechanism** — which is a real security decision with a real cost, and the cost is that **this course cannot demonstrate containers on this machine.** Week 10 met the same wall from the other side, and said so.

**Mandatory access control is the other mechanism, and it is running.** AppArmor confines programs by *path-based profiles* the administrator writes, which the user cannot override — the "mandatory" part. It is what enforces the namespace restriction above. **We cannot enumerate the profiles** (`aa-status` needs root: *"sudo: a password is required"*), so this lecture states what it does and does not pretend to have measured its contents.

**Three more restrictions this account runs under, all measured**, and all relevant to L37's information leaks:

| Restriction | Setting | Effect, tested |
|---|---|---|
| `kptr_restrict` | 1 | **`/proc/kallsyms` shows every symbol at address `0000000000000000`** |
| `yama/ptrace_scope` | 1 | **`PTRACE_ATTACH` to a non-descendant: `Operation not permitted`** — one of your own processes cannot read another's memory |
| `perf_event_paranoid` | **4** | `perf` is unusable for this account — **the reason Week 6's and Week 7's labs used `/proc` and `mincore` instead** |
| `unprivileged_bpf_disabled` | **2** | **the reason Week 7's lab could not use `bpftrace`** |

**Two of this course's syllabus deviations are entries in that table.** The tools the curriculum assumed were not missing from the image — **they were disabled on purpose, for exactly the reasons this lecture is about.**

---

## §8 · Putting It Together

**PS 12 asks you to build `jail`**, which is every mechanism in this lecture in one program, in the right order:

```c
pid = fork();
if (pid == 0) {
	set_limit(RLIMIT_CPU,  t, t + 1);   /* limits first: they survive execve  */
	set_limit(RLIMIT_AS,   m);
	set_limit(RLIMIT_NOFILE, f);
	set_limit(RLIMIT_CORE, 0);          /* no core dump: it would hold secrets */
	prctl(PR_SET_NO_NEW_PRIVS, 1, ...); /* before seccomp, and required by it   */
	install_filter(policy);             /* execve must be allowed: it is next   */
	execvp(cmd, args);
}
wait4(pid, &status, 0, &ru);            /* report signal vs exit, and SIGSYS    */
```

**The order is not arbitrary.** Limits before the filter, because `setrlimit` is not in the allowlist. `NO_NEW_PRIVS` before seccomp, because the kernel demands it. **The filter before `execve`, which means `execve` itself must be permitted** — a filter installed after `execve` would require the sandboxed program's cooperation, and a hostile program will not cooperate.

**And what it does not do**, which is Q5 of the problem set and the honest end of this lecture:

- **It does not stop the program reading your files.** It runs as you. `-s strict` permits `openat`, because the loader needs it and seccomp cannot inspect the path.
- **It does not stop a side channel.** L37 §6's timing ladder is unaffected by any of this.
- **It does not stop `gather_data_sampling`**, which this machine reports as **`Vulnerable`** — a speculative-execution flaw with no mitigation active, in the same directory where every other flaw says `Mitigation:`.
- **It does not stop `sgdt`.** L39 will show that the kernel address leak from Week 0 still works, in Week 12, under every protection in this lecture.

**Least privilege makes the blast radius smaller. It does not make it zero, and a sandbox sold as though it did is worse than none**, because someone will put something valuable inside it.

---

### What You Should Be Able to Do

1. **State least privilege**, and explain why it is the only principle that does not assume your code is correct.
2. **Compare setuid, capabilities and seccomp** by what each can express — and say why `CAP_SYS_ADMIN` undermines the capability argument.
3. **Explain `NO_NEW_PRIVS`**, and why the kernel refuses an unprivileged filter without it.
4. **Quote the cost of a seccomp filter** — about 50 ns, independent of length and count — and say what that implies for how you write one.
5. **Explain why an allowlist must be derived by tracing**, using `rseq` as the example.
6. **Say why `RLIMIT_NPROC` fails at zero children here** and a cgroup's `pids.max` does not.
7. **Say what a sandbox does not protect against**, in four specific items.

---

*CS 202 · Week 12 · L38 · © CSE Department*

# CS 202 · Problem Set 12 — Solutions and Mark Scheme
## **INSTRUCTOR ONLY** · Do not distribute

---

**Released Week 12 Wednesday; due Friday of the completion period, 17:00. 100 marks.**

**The reference is `jail reference (do not distribute).c`** in this folder, with `victims.c` in `assignments/ps12/`. It compiles warning-clean under `gcc -O2 -Wall -Wextra` and every figure below is from it, on the reference machine.

**Marking principle.** This problem set is **measurement plus judgment**, and the judgment questions (Q4(c), Q5) are where the marks separate. **A working `jail` with no numbers is worth about half.**

---

## Question 1 — The Limits (25)

### (a) [12]

```c
static void set_limits(rlim_t cpu, rlim_t mem, rlim_t files, rlim_t procs)
{
	if (cpu) { struct rlimit r = { cpu, cpu + 1 }; setrlimit(RLIMIT_CPU, &r); }
	if (mem)   set_limit(RLIMIT_AS,     mem);
	if (files) set_limit(RLIMIT_NOFILE, files);
	if (procs) set_limit(RLIMIT_NPROC,  procs);
	set_limit(RLIMIT_CORE, 0);
}
```

**3 marks per limit correctly set and conditional; `RLIMIT_CORE` unconditional.** **Deduct 2** for a program that ignores `setrlimit`'s return value entirely — the child must not exec if a limit could not be set.

### (b) [5]

**Soft = `cpu`, hard = `cpu + 1` [3].** At the soft limit the kernel sends **`SIGXCPU`**, which is catchable; at the hard limit, **`SIGKILL`**, which is not. **Setting both equal turns the warning into an execution** and the program never gets its chance.

**What a handler would do [2]:** checkpoint — flush buffers, write partial results, record where to resume. **Not** "free memory" or "print a message" alone.

> **The reference had this bug.** Its first version set both to the same value and reported
> `SIGKILL`; the transcript is in the build notes. **A student who reports `SIGKILL` and explains
> why gets 4 of 5.**

### (c) [8] — 2 per run, 2 for the two explanations

| Run | Reference result |
|---|---|
| `./jail -t 1 ./victim spin` | **killed by `SIGXCPU` (24) after 0.999 s of CPU**, 1.237 s wall |
| `./jail -m 64 ./victim grab` | **`malloc` failed after 61 MiB**; peak RSS 64,216 KiB |
| `./jail -f 32 ./victim open` | **`open` failed after 29 descriptors**, `EMFILE` |

**The two gaps [2]:**

- **61 MiB, not 64:** `RLIMIT_AS` limits the **whole address space** — the program's text, libc, the stack, thread stacks and the allocator's own metadata are all in it before `main` runs. **The 3 MiB is the process itself.**
- **29 descriptors, not 32:** **0, 1 and 2 are already open.** `RLIMIT_NOFILE` is a ceiling on the descriptor *number*, so the first `open` returns 3 and the last one possible is 31.

**A student who says "rounding" or "overhead" without identifying what the overhead is: 1 of the 2.**

---

## Question 2 — The Filter (30)

### (a) [8]

**The attack [4]:** without `NO_NEW_PRIVS`, a sandboxed process can **`execve` a setuid-root binary** and come back with privileges the sandbox never granted. **A program on this machine: `/usr/bin/sudo`, `/usr/bin/su`, `/usr/bin/passwd`, `/usr/bin/pkexec`** — any of the 18. *(Accept `mount`, `newgrp`, etc.)*

**Once set it cannot be unset, and it is inherited across `fork` and `execve` [2].**

**What the kernel does if you omit it [2]: `seccomp(SECCOMP_SET_MODE_FILTER, ...)` fails with `EACCES`** for an unprivileged caller. **The filter is not installed at all** — and a program that does not check the return value **runs completely unsandboxed while believing it is confined.** Worth a note in feedback wherever the student's code ignores the result.

### (b) [14]

**The filter [10]:**

```c
BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, arch)),
BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),
BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
  /* for i in 0..n-1: */
BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, allow[i], n - i, 0),
BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),
BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
```

| Item | Marks |
|---|---:|
| the architecture check, **before** the number check | **3** |
| the allowlist comparisons with correct jump offsets | **4** |
| `KILL_PROCESS` default, `ALLOW` reached only by a match | **2** |
| `NO_NEW_PRIVS` then `SECCOMP_SET_MODE_FILTER`, return values checked | **1** |

**Why the architecture check must come first [included above, but say it in feedback]:** system call **numbers differ between x86-64 and i386**, so a 32-bit process could invoke `open` with the number the filter believes is `read`.

**Testing [4]:** the student must show they can tell a working filter from a broken one — `-s none` runs, a `SYS_write`-only filter kills at the first `printf`. **A submission that shows only "it works" scores 2.**

### (c) [8]

**The missing call is `rseq` [3].** Restartable sequences; **glibc registers one per thread at start-up** so per-CPU data can be updated without atomics.

**Why it is in no program's source [2]:** **the C library makes it before `main`**, on the programmer's behalf. It appeared in **glibc 2.35**, so an allowlist that worked on Ubuntu 20.04 kills every process on 24.04.

**The implication [3]:** **a sandbox policy must be derived by tracing the program on the system it will run on, and re-derived when libc, the compiler or the distribution changes.** It cannot be written from first principles, because it is not a property of the program alone. *(Credit any answer that reaches "the policy depends on the platform, not just the program".)*

**The demonstrations:** `./jail -s strict /bin/echo hi` prints `hi` and exits 0; `./jail -s strict ./victim socket` is **killed by `SIGSYS`**; `./jail -s net ./victim socket` prints `socket() = 3`.

---

## Question 3 — What It Costs (15)

### (a) [10]

**Reference figures — median of the difference across 15 runs, `taskset -c 2`:**

| Filter | Cost per system call |
|---|---|
| **Control: no filter, twice** | **−3.4 ns** |
| 1 filter, 6 instructions | **+51.0 ns** |
| 1 filter, 15 instructions | **+51.9 ns** |
| 1 filter, 55 instructions | **+49.1 ns** |
| 1 filter, 205 instructions | **+52.7 ns** |
| 5 filters, 15 instructions each | **+48.9 ns** |

**Marks:** 4 for a harness that measures **within one process** and takes a minimum rather than a mean; **3 for the control**; 3 for the four figures. **Any figure in the 30–80 ns range is correct** — the machine's state varies.

> **The control is not a formality and the rubric should be enforced.** Without it the natural harness
> reports the filter making system calls **faster** (1,044 ns → 868 ns), which is CPU frequency ramp.
> **A submission with no control is capped at 5 of 10** even if its numbers happen to be right.

### (b) [5]

**The cost does not depend on the filter's length, nor on how many filters are stacked [2].**

**The explanation [2]: the cost is the check, not the rules.** Entering the seccomp path at all — the test on the syscall entry that this task has a filter, plus the call into the BPF machinery — dominates; **the rules are JIT-compiled to native code** (`net.core.bpf_jit_enable = 1`) and a 205-instruction walk is lost in the noise.

**The percentage and the judgment [1]: about 50 ns on roughly 840 ns is ~6%**, and a student should accept it for a network-facing service. **Full credit for "no" if they compare it against a specific measured budget** — e.g. a service whose per-request cost is dominated by a 23 ms network round trip, where 50 ns is invisible.

---

## Question 4 — The Limit That Does Not Limit (15)

### (a) [5]

**Both fail identically: `fork failed after 0 children: Resource temporarily unavailable`.** Neither 100 nor 700 lets a single child be created.

### (b) [5]

**`RLIMIT_NPROC` limits the number of processes belonging to the *real user ID*, checked at every `fork` anywhere on the system [3]** — not the children of this process, and not a group.

**The evidence [2]:** this account already owns **134 processes and 1,068 threads**. *(The kernel's counter is per-user and counts tasks, so the thread figure is the relevant one.)* **Any limit below that is already exceeded before the jail starts.**

**Accept "it counts the user's processes, and I already have more than that" with the numbers.** **Without the numbers: 3 of 5.**

### (c) [5]

**The cgroup [3]:**

```bash
CG=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/myjail
mkdir "$CG"; echo 20 > "$CG/pids.max"
( echo $BASHPID > "$CG/cgroup.procs"; exec ./victim fork )
fork failed after 19 children
```

**Exactly 19 children plus the parent is 20.** *(The delegated controllers here are `cpu memory pids`; `memory.max` is what Week 6 used.)*

**The general lesson [2]:** **when two mechanisms appear to do the same job, one of them usually has a scope you did not check.** The rlimit's unit is the **user**; the cgroup's is **the set of processes you nominated**. Only the second composes, which is why every container runtime uses cgroups and none uses `RLIMIT_NPROC`.

---

## Question 5 — What It Does Not Do (15)

**Four items, 3 marks each, plus 3 for the closing argument.** **One of the 3 per item is for evidence from the machine** — a command and its output, not an assertion.

**The four the question steers toward:**

1. **It reads your files.** The jail does not change uid; `-s strict` permits `openat` because the loader needs it, and **seccomp cannot filter on a path** — it sees the pointer as an integer, and checking the string would be a TOCTOU race. *Evidence:* `./jail -s strict cat ~/.bash_history`.
2. **The timing channel is untouched.** *Evidence:* `./jail -s strict ./timing hot` produces the same ladder — **about 2.5 ns per byte over a 1.25 ns noise floor**.
3. **`gather_data_sampling: Vulnerable`.** *Evidence:* `grep . /sys/devices/system/cpu/vulnerabilities/*` — **the only line in that directory that is neither `Mitigation:` nor `Not affected`**. No sandbox addresses a speculative-execution flaw in the silicon.
4. **`sgdt` still leaks a kernel address.** *Evidence:* `./jail -s strict ./sgdt` prints a GDT base such as `0xfffffe397b808000`, **under every protection in the course**, because the instruction is unprivileged on a CPU without UMIP.

**Accept other well-evidenced items:** it can exhaust the CPU up to the limit; it can write to any file it can open; it inherits the parent's descriptors unless closed; **`-s net` gives it the whole network**.

**The closing argument [3].** **Both answers earn full marks; the undefended one earns none.**

- **A good "yes":** the list is finite and known, whereas an unsandboxed program's list is the whole system call table. Q3 measured the price at 6%. **A defence that reduces the blast radius for 6% is worth having even though it is not a boundary.**
- **A good "no":** *for a specific setting* — if the data the attacker wants is in the user's own files, which the jail does not protect, then the jail buys nothing against this threat model and **its real cost is that someone will now put something valuable inside it.** **This is the answer the course wants to see defended, and it should be marked generously.**

**Penalise only the answer that treats the sandbox as a boundary** — "it is safe now" — which contradicts the student's own four items.

---

## Marks

| Q | Topic | Marks |
|---|---|---:|
| 1 | The limits | 25 |
| 2 | The filter | 30 |
| 3 | What it costs | 15 |
| 4 | The limit that does not limit | 15 |
| 5 | What it does not do | 15 |
| | **Total** | **100** |

---

*CS 202 · Week 12 · PS 12 Solutions · Instructor Only*

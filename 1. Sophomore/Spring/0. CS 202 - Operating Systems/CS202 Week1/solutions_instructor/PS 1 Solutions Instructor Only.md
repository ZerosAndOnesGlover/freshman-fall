# CS 202 · Problem Set 1 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for PS 1.** Q1 is the first program in the course that reads the kernel's process table rather than asking the kernel to do something. **The marks are for reading it correctly** — parsing `stat` from the last `)`, knowing that a zombie has no `VmRSS`, and getting the zombie-then-reaped rule right — not for features beyond the specification. A clean 200-line `pm` that passes `test.pm` is full marks; a 600-line one with colour and a parser for quoted arguments is not worth more.

**Every measured answer below was produced on the reference machine:** Intel i5-8250U, Ubuntu 24.04.4, kernel 7.0, GCC 13.3.0. Student numbers will differ in magnitude and must not differ in shape.

---

## Q1: `pm` (40 points)

### Reference solution

```c
/* pm.c: a user-space process manager. CS 202 PS 1 — reference solution. */
#define _GNU_SOURCE
#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define MAXJOBS 32
#define MAXARGS 32

struct job {
    char name[32];
    pid_t pid;
    int reaped;
    int status;             /* valid once reaped */
    struct rusage ru;       /* valid once reaped */
};

static struct job jobs[MAXJOBS];
static int njobs;
static long hz;

static struct job *find(const char *name)
{
    for (int i = 0; i < njobs; i++)
        if (!strcmp(jobs[i].name, name))
            return &jobs[i];
    printf("pm: no job named %s\n", name);
    return 0;
}

/* Fields 3, 14 and 15 of /proc/<pid>/stat. The command name, field 2, is in
 * parentheses and may contain spaces and parentheses: parse from the LAST ')'. */
static int read_stat(pid_t pid, char *state, unsigned long *ticks)
{
    char path[64], buf[1024];
    snprintf(path, sizeof path, "/proc/%d/stat", (int)pid);
    FILE *f = fopen(path, "r");
    if (!f)
        return -1;
    size_t n = fread(buf, 1, sizeof buf - 1, f);
    fclose(f);
    buf[n] = 0;
    char *p = strrchr(buf, ')');
    unsigned long ut, st;
    if (!p || sscanf(p + 2, "%c %*d %*d %*d %*d %*d %*u %*u %*u %*u %*u %lu %lu",
                     state, &ut, &st) != 3)
        return -1;
    *ticks = ut + st;
    return 0;
}

/* One numeric field of /proc/<pid>/status, or -1 if absent (a zombie has no VmRSS). */
static long status_field(pid_t pid, const char *key)
{
    char path[64], line[256];
    size_t klen = strlen(key);
    long v = -1;
    snprintf(path, sizeof path, "/proc/%d/status", (int)pid);
    FILE *f = fopen(path, "r");
    if (!f)
        return -1;
    while (fgets(line, sizeof line, f))
        if (!strncmp(line, key, klen) && line[klen] == ':') {
            v = strtol(line + klen + 1, 0, 10);
            break;
        }
    fclose(f);
    return v;
}

static void describe_exit(int status, char *out, size_t len)
{
    if (WIFEXITED(status))
        snprintf(out, len, "exited %d", WEXITSTATUS(status));
    else if (WIFSIGNALED(status))
        snprintf(out, len, "killed SIG%s%s", sigabbrev_np(WTERMSIG(status)),
                 WCOREDUMP(status) ? " (core)" : "");
    else
        snprintf(out, len, "status 0x%x", status);
}

static void reap(struct job *j, int options)
{
    if (j->reaped)
        return;
    pid_t r = wait4(j->pid, &j->status, options, &j->ru);
    if (r == j->pid)
        j->reaped = 1;
    else if (r < 0 && errno != EINTR)
        perror("wait4");
}

static void cmd_start(char **argv)
{
    if (!argv[0] || !argv[1]) { printf("pm: start <name> <program> [args...]\n"); return; }
    if (njobs == MAXJOBS)     { printf("pm: job table full\n"); return; }
    fflush(stdout);                        /* do not hand the child our buffered output */
    pid_t p = fork();
    if (p < 0) { perror("fork"); return; }
    if (p == 0) {
        execvp(argv[1], argv + 1);
        perror("execvp");
        _exit(127);
    }
    struct job *j = &jobs[njobs++];
    memset(j, 0, sizeof *j);
    snprintf(j->name, sizeof j->name, "%s", argv[0]);
    j->pid = p;
    printf("pm: started %s as pid %d\n", j->name, (int)p);
}

static void cmd_list(void)
{
    printf("%-8s %8s %-5s %8s %9s %9s %9s  %s\n",
           "NAME", "PID", "STATE", "CPU(s)", "RSS(kB)", "VOLUNTARY", "INVOLUNT", "EXIT");
    for (int i = 0; i < njobs; i++) {
        struct job *j = &jobs[i];
        char state;
        unsigned long ticks;
        if (j->reaped) {
            char how[48];
            describe_exit(j->status, how, sizeof how);
            double cpu = j->ru.ru_utime.tv_sec + j->ru.ru_utime.tv_usec * 1e-6
                       + j->ru.ru_stime.tv_sec + j->ru.ru_stime.tv_usec * 1e-6;
            printf("%-8s %8d %-5s %8.2f %9s %9ld %9ld  %s\n", j->name, (int)j->pid, "-",
                   cpu, "-", j->ru.ru_nvcsw, j->ru.ru_nivcsw, how);
        } else if (read_stat(j->pid, &state, &ticks) == 0) {
            long rss = status_field(j->pid, "VmRSS");
            char rssbuf[24] = "-";
            if (rss >= 0)
                snprintf(rssbuf, sizeof rssbuf, "%ld", rss);
            printf("%-8s %8d %-5c %8.2f %9s %9ld %9ld  %s\n", j->name, (int)j->pid, state,
                   (double)ticks / hz, rssbuf,
                   status_field(j->pid, "voluntary_ctxt_switches"),
                   status_field(j->pid, "nonvoluntary_ctxt_switches"),
                   state == 'Z' ? "(zombie: reaping)" : "");
            if (state == 'Z')
                reap(j, 0);
        } else {
            printf("%-8s %8d %-5s  (no /proc entry)\n", j->name, (int)j->pid, "?");
        }
    }
}

static void cmd_signal(const char *name, int sig)
{
    struct job *j = name ? find(name) : 0;
    if (!j) return;
    if (j->reaped) { printf("pm: %s has already exited\n", j->name); return; }
    if (kill(j->pid, sig) < 0) perror("kill");
}

static void cmd_kill(const char *name)
{
    struct job *j = name ? find(name) : 0;
    if (!j || j->reaped) return;
    kill(j->pid, SIGCONT);                 /* a stopped process cannot act on SIGTERM */
    kill(j->pid, SIGTERM);
    for (int i = 0; i < 100 && !j->reaped; i++) {
        usleep(10000);
        reap(j, WNOHANG);
    }
    if (!j->reaped) {
        kill(j->pid, SIGKILL);
        reap(j, 0);
    }
}

static void cmd_wait(void)
{
    for (int i = 0; i < njobs; i++) {
        if (jobs[i].reaped) continue;
        reap(&jobs[i], 0);
        char how[48];
        describe_exit(jobs[i].status, how, sizeof how);
        printf("pm: %s (pid %d) %s\n", jobs[i].name, (int)jobs[i].pid, how);
    }
}

int main(void)
{
    char line[1024];
    hz = sysconf(_SC_CLK_TCK);
    while (fgets(line, sizeof line, stdin)) {
        char *argv[MAXARGS + 1];
        int argc = 0;
        for (char *t = strtok(line, " \t\n"); t && argc < MAXARGS; t = strtok(0, " \t\n"))
            argv[argc++] = t;
        argv[argc] = 0;
        if (argc == 0 || argv[0][0] == '#') continue;
        printf("pm> %s", argv[0]);
        for (int i = 1; i < argc; i++) printf(" %s", argv[i]);
        printf("\n");

        if      (!strcmp(argv[0], "start")) cmd_start(argv + 1);
        else if (!strcmp(argv[0], "list"))  cmd_list();
        else if (!strcmp(argv[0], "stop"))  cmd_signal(argv[1], SIGSTOP);
        else if (!strcmp(argv[0], "cont"))  cmd_signal(argv[1], SIGCONT);
        else if (!strcmp(argv[0], "kill"))  cmd_kill(argv[1]);
        else if (!strcmp(argv[0], "sleep")) sleep(argc > 1 ? (unsigned)atoi(argv[1]) : 1);
        else if (!strcmp(argv[0], "wait"))  cmd_wait();
        else if (!strcmp(argv[0], "quit"))  break;
        else printf("pm: unknown command %s\n", argv[0]);
        fflush(stdout);
    }
    for (int i = 0; i < njobs; i++)
        if (!jobs[i].reaped) { kill(jobs[i].pid, SIGKILL); reap(&jobs[i], 0); }
    return 0;
}
```

### Reference output of `./pm < test.pm`

```
pm> start hog taskset -c 5 ./worker hog
pm: started hog as pid 1695908
pm> start tick taskset -c 5 ./worker tick
pm: started tick as pid 1695909
pm> start mem ./worker mem 64
pm: started mem as pid 1695910
pm> start three ./worker exit 3
pm: started three as pid 1695911
pm> start crash ./worker crash
pm: started crash as pid 1695912
pm> start nope ./no-such-program
pm: started nope as pid 1695913
execvp: No such file or directory
pm> sleep 3
pm> list
NAME          PID STATE   CPU(s)   RSS(kB) VOLUNTARY  INVOLUNT  EXIT
hog       1695908 R         2.98      1156         0      2882
tick      1695909 S         0.00      1284      2843         2
mem       1695910 S         0.02     66952         1         0
three     1695911 Z         0.00         -         2         0  (zombie: reaping)
crash     1695912 Z         0.00         -         4         0  (zombie: reaping)
nope      1695913 Z         0.00         -         1         0  (zombie: reaping)
pm> stop hog
pm> sleep 2
pm> list
NAME          PID STATE   CPU(s)   RSS(kB) VOLUNTARY  INVOLUNT  EXIT
hog       1695908 T         2.99      1156         1      2882
tick      1695909 S         0.05      1284      4576         2
mem       1695910 S         0.02     66952         1         0
three     1695911 -         0.00         -         2         0  exited 3
crash     1695912 -         0.00         -         4         0  killed SIGSEGV (core)
nope      1695913 -         0.00         -         1         0  exited 127
pm> cont hog
pm> kill hog
pm> kill tick
pm> kill mem
pm> list
NAME          PID STATE   CPU(s)   RSS(kB) VOLUNTARY  INVOLUNT  EXIT
hog       1695908 -         2.99         -         2      2883  killed SIGTERM
tick      1695909 -         0.06         -      4584         2  killed SIGTERM
mem       1695910 -         0.02         -         1         0  killed SIGTERM
three     1695911 -         0.00         -         2         0  exited 3
crash     1695912 -         0.00         -         4         0  killed SIGSEGV (core)
nope      1695913 -         0.00         -         1         0  exited 127
...
```

After `quit`, `pgrep -x worker` prints nothing.

**Notes for markers:**

- **`taskset` does not appear in the process table**: `taskset` sets the affinity and then `exec`s `worker`, so the PID `pm` recorded is `worker`'s. A student who says "`pm` is managing `taskset`" has misunderstood `exec` — PROG 201 L01 §7.
- **`(core)` on `crash`** depends on the machine's `core_pattern` and `ulimit -c`. Accept its presence or absence.
- **`nope` shows `exited 127`**, and the child's `perror` line appears in the output. Both are correct.
- **`execvp` failing in the child must end in `_exit(127)`, not `exit`** — an `exit` would flush `pm`'s inherited stdio buffer a second time. Students who forgot `fflush` before `fork` *and* used `exit` will show duplicated `pm>` lines; the requirement exists to catch this.

### Common errors, and deductions

| Error | Symptom | Deduct |
|---|---|---:|
| Splits `stat` on spaces from the start | works on the test; wrong for a name with a space. **Test it**: `start x ./worker hog` after `prctl(PR_SET_NAME, "a) b")` in a patched worker, or simply read the parser | 4 |
| Reaps in a `SIGCHLD` handler | zombies never appear in `list`; the zombie rule fails | 8 |
| Reads `VmRSS` of a zombie and prints 0 | a zombie has **no** `VmRSS` line; printing 0 is a guess presented as a measurement | 2 |
| `kill` sends `SIGTERM` to a stopped process and waits | a stopped process never handles `SIGTERM`; escalates to `SIGKILL` only after the full second. Correct but slow — **accept** if it still escalates | 0 |
| No `fflush` before `fork` | duplicated `pm>` lines when output is a pipe | 4 |
| `system("ps …")` or `popen` | prohibited | 12 |
| Workers survive `quit` | orphaned `hog` burning a CPU after the script ends | 4 |

---

## Q2: Reading What the Kernel Counted (20 points)

### (a) [6]

Reference, first `list` after three seconds:

| | State | CPU s | Voluntary | Involuntary |
|---|---|---:|---:|---:|
| `hog` | **R** | **2.98** | **0** | **2,882** |
| `tick` | **S** | **0.00** | **2,843** | **2** |

**Prediction marks** go to a student who predicts the hog near 3 s of CPU with a large involuntary count, and the ticker near zero CPU with a large voluntary count — **or who predicts otherwise and explains the discrepancy.**

### (b) [6]

- **`hog` never blocks**, so it never gives up the CPU voluntarily. **Every switch away from it is a preemption** — by the timer at the end of its slice, or when `tick` wakes and the scheduler lets it run. ~2,900 in 3 s is about once per millisecond: exactly as often as `tick` wakes up.
- **`tick` blocks in `usleep` every millisecond**, giving the CPU up voluntarily each time. It almost never has it taken away, because it runs for a few microseconds and blocks again long before any timeslice ends.
- **A timer interrupt causes an involuntary switch. `usleep` causes a voluntary one.**

**The best answers notice that the two large numbers are nearly equal** — 2,882 and 2,843 — and explain why: most of the hog's preemptions *are* `tick` waking up and being given the CPU.

### (c) [4]

- First interval: 2,843 voluntary in 3 s ≈ **948 / s**.
- Second interval: (4,576 − 2,843) in 2 s ≈ **867 / s**.

**Roughly the same, and slightly lower.** Stopping the hog **made little difference to `tick`**, and it should not have made much: `tick` spends almost all its time asleep, and when it wakes it gets the CPU promptly whether or not a hog is present, because the scheduler favours a task that has used little CPU (Week 2). **Neither rate is 1,000/s** because `usleep(1000)` sleeps *at least* 1 ms, plus the timer slack Linux adds to sleeping tasks (`/proc/<pid>/timerslack_ns`, 50 µs by default), plus the time to be scheduled.

**Accept** any argued explanation of the small difference; **require** the observation that it is small.

### (d) [4]

- With the page-touching loop: **RSS 66,952 kB** — 64 MiB plus the program.
- With `memset(p, 1, n)` at `-O2`: **RSS 1,424 kB.**

**GCC removed the `memset`.** The buffer is written and never read, so the write is a *dead store*; GCC knows `malloc` returns fresh memory no one else can see, and deletes both. **No page is ever touched, so none is ever allocated** — L06 §3's `VmSize`-against-`VmRSS` distinction, caused by the compiler rather than the program. `worker.c`'s volatile read-back forces the writes to be observable.

**This is the reference machine's own first draft of `worker.c`**, which is why the question exists. Award full marks for "the compiler optimised the `memset` away because nothing reads the memory"; award 2 for "RSS is small because memory is allocated lazily" without saying why the lazy pages were never touched.

---

## Q3: The Cost of a Switch (15 points)

### (a) [6]

Reference:

```
baseline: one write+read pair with no other process: 1438 ns
CPUs 2 and 2: 1.224 s for 200000 rounds; 400009 switches (2.00 per round); 0.575 s of that is the calls; 1622 ns per switch
CPUs 2 and 3: 1.431 s for 200000 rounds; 399890 switches (2.00 per round); 0.575 s of that is the calls; 2139 ns per switch
```

**By hand**, one CPU: calls = 2 × 200,000 × 1,438 ns = 0.5752 s. (1.224 − 0.5752) s ÷ 400,009 = **1.622 µs**. Two CPUs: (1.431 − 0.5752) ÷ 399,890 = **2.140 µs**. Both agree with the program to rounding.

**Marking:** 2 for the output with machine details, 4 for the arithmetic shown.

### (b) [5]

**The assumption:** a `write` + `read` pair costs the same when the `read` blocks and the `write` wakes someone as when neither does. **It is false, and violating it makes the estimate too high** — the ping-pong's calls do *more* work than the baseline's (putting a task to sleep, waking another, enqueueing it), and all of that extra work is attributed to "the switch".

**A better baseline:** make the baseline's calls do the same kind of work without switching — for example, a `read` with a timeout that always expires (`poll` on an empty pipe with a zero timeout, then a `write` that wakes nobody), or measure `futex` wake with no waiter. **Accept any proposal that makes the baseline's calls block-and-wake-shaped without an actual switch**, or an argument that it cannot be done exactly. **Also accept** "report the whole cost of switch-plus-wakeup as the figure of interest", if argued: that is what L05 §5 says.

### (c) [4]

- **On two CPUs**, after each side writes it immediately reads, finds nothing, and **sleeps** — a voluntary switch — and its CPU goes idle. The other side is woken on its own CPU. **Nobody is ever preempted**, because nobody is ever competing for a CPU.
- **On one CPU**, when A writes, B becomes runnable **on A's CPU**. The scheduler often decides B should run *now* — B has used very little CPU, and waking tasks are favoured — so **A is preempted before it reaches its own `read`**: an involuntary switch for A. Then B writes, wakes A, and the same thing happens the other way. About half the switches come out involuntary.

**Marking:** 2 + 2. "Wakeup preemption" by name is not required; the mechanism is.

---

## Q4: xv6 and the FPU (15 points)

### (a) [5]

Reference, one CPU, two runs. **Each process should reach `x*2 = 20,000,000`.**

| Run | Parent `x*2` | Child `x*2` | Sum |
|---|---:|---:|---:|
| 1 | 447,636 | 39,552,364 | **40,000,000** |
| 2 | 213,688 | 39,786,312 | **40,000,000** |

*(On the console the two lines interleave character by character, because xv6's `printf` writes one byte per system call. Students must untangle them.)*

**The sum is exact because both processes were adding into the same register.** During the loop `x` is held in the **x87 register stack** — `ST(0)` — which belongs to the CPU, not to either process. xv6's context switch saves four integer registers and **nothing from the FPU**. When the timer switched processes, the incoming process continued its `x = x + 0.5` **on the outgoing process's value**. Every one of the 40 million half-additions happened, into one accumulator; how they are split between the two final answers depends only on when the last switch fell.

**Marking:** 2 for correct numbers and sums, 3 for "one shared x87 register, not saved by `swtch`". **Deduct 2** if the student attributes it to "memory corruption" or "a race on a shared variable" — the processes share no memory at all.

### (b) [6]

A good design — **accept any design that is correct and defended:**

- **Field:** `char fpu[512]` in `struct proc`, **aligned to 16 bytes** (`fxsave` requires it) — or a pointer to a separately `kalloc`ed page, which gets alignment for free and keeps `struct proc` small. **512 bytes** is the `fxsave` area on the i386 target, which covers x87 and SSE.
- **Where:**
  - *Option A — in the scheduler path.* **Save** in `sched()` immediately **before** `swtch(&p->context, mycpu()->scheduler)` with `fxsave`; **restore** in `scheduler()` immediately **after** `switchuvm(p)` and before `swtch(&(c->scheduler), p->context)`, with `fxrstor`. Simple: every switch saves and restores.
  - *Option B — at the trap boundary.* Save on entry from user mode in `alltraps`/`trap()`, restore in `trapret` before `iret`. Correct even if the kernel itself someday uses the FPU, and it is where Linux does the restore; but it pays on every system call, not just every switch.
- **`fork`** must **copy the parent's FPU area into the child**, alongside `*np->tf = *curproc->tf;` — the child resumes mid-computation with the parent's registers, and an FPU register is a register.
- **A new process from `userinit` or `exec`** needs a **clean FPU state**: `fninit` once, then `fxsave` into the new process's area — or copy a pristine area saved at boot. Otherwise it inherits whatever was last in the hardware. **`exec` should reset it too**, for the same reason it resets the user registers.

**Marking:** 1 field and size, 2 save/restore location with defence, 1 `fork`, 2 initialisation — `exec` resetting it earns the second of those.

**Worth a remark if a student raises it:** xv6 also runs on several CPUs, and a process that last saved its FPU state on CPU 0 may be restored on CPU 1 — which is fine, because the state is in `struct proc`, not in the CPU. Linux's "skip the restore if this CPU still holds our state" optimisation (L05 §6) is exactly the case where that is *not* fine unless it records which CPU.

### (c) [4]

- **Advantage of lazy:** a process that does not use the FPU between two switches **never pays** to save or restore 1,088 bytes — and most processes, most of the time, are not doing floating point. Only a switch *into* an FPU user paid, and only once.
- **Why abandoned** — accept either, **require one security answer:**
  - **Security: LazyFP (2018).** Under lazy switching the previous process's FPU registers were still loaded when the next process ran, marked unavailable by `CR0.TS`. The first FPU instruction faulted — **but speculatively executed first**, and could leak the previous process's register contents, including AES keys handled with SSE, through a cache side channel.
  - **Performance:** modern CPUs save only changed components with `XSAVEOPT`, so eager saving became cheap; and SSE/AVX are now used everywhere — `memcpy` and `strlen` in glibc use vector registers — so almost every process touches the FPU state anyway, and the lazy trap was nearly always taken.

**Marking:** 2 + 2.

---

## Q5: Who a Process Is (10 points)

### (a) [4]

Reference:

```
-rwxr-xr-x root /usr/bin/ping           (getcap: cap_net_raw=ep)
-rwsr-xr-x root /usr/bin/passwd
```

While `ping` runs:

```
CapPrm: 0000000000000000
CapEff: 0000000000000000
```

**A student who reads the capabilities within the first few milliseconds, before `ping` has opened its socket, may see `CapPrm: 0000000000002000`** — bit 13, `cap_net_raw`. That is correct, and better than the reference answer if they explain it.

### (b) [6]

| | `passwd` (set-user-ID root) | `ping` (file capability, then dropped) |
|---|---|---|
| **How much** | **all of root** — effective UID 0, every capability | **one capability**, `cap_net_raw`: open raw sockets |
| **For how long** | **the whole run** | **until its socket is open** — measured `CapPrm` 0 well within a second |
| **A memory-corruption bug after the first second** | runs as root: read `/etc/shadow`, load a module, anything | runs as user 1000 **with no capabilities**: it can do what any program of that user can, and nothing more — **dropping from the permitted set cannot be undone** |

**The point the marks are for:** the file capability limits *how much*; dropping it limits *how long*; together they turn a root compromise into an ordinary-user compromise. **Using the measured `CapPrm` value is required for full marks** — it is the evidence that the second limit is real and not merely available.

**Marking:** 2 for how much, 2 for how long with the measurement, 2 for consequences of a bug.

---

*CS 202 · Week 1 · PS 1 Solutions · Instructor Only*

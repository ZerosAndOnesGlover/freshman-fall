# PROG 201 · Lab 0 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Friday of Week 0, 15:00–16:50, BH 215. **Unmarked** — checked off in the session.

**What the session is actually for.** Every student arrives able to call `fork()`. The three things they cannot do yet, and which this lab exists to teach by failure, are:

1. reaping **more than one** child per `SIGCHLD`,
2. waiting for a signal **without a race**,
3. noticing that the signal mask **survives `exec`**.

Part C's bug (3) is the one they will not find alone. Budget ten minutes for it and let them struggle for five first — the symptom (a healthy child ignoring `SIGTERM`) is so counter-intuitive that the explanation lands hard once they have it.

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–10 | Toolchain | Walk the room. `manpages-dev` is the missing package; `apt install manpages-dev` |
| 10–40 | A — start and reap | Most students are fine here. Push them to actually break `reap()` for Q1 |
| 40–65 | B — restart policy | Watch for `fork()` inside the handler |
| 65–100 | C — shutdown | **The mask bug.** See below |
| 100–110 | D + checkoff | `top` reading 0.0% is the tell that the loop is right |

---

## Reference Solution

Complete, and tested on Ubuntu 24.04 / GCC 13.3.0 / glibc 2.39. This is the file to paste on the projector at 100 minutes, not before.

```c
/* supervisor.c — LAB 0 reference solution.
 *
 *   ./supervisor <name>:<mode> ...
 *
 * Starts one ./flaky per argument, restarts it when it dies, gives up on a
 * child that dies MAX_RESTARTS times inside WINDOW seconds, and shuts the whole
 * set down on SIGTERM/SIGINT: SIGTERM, then SIGKILL to whatever is left after
 * GRACE seconds.
 */
#define _GNU_SOURCE
#include <errno.h>
#include <poll.h>
#include <stdarg.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/wait.h>

#define MAX_CHILDREN 16
#define MAX_RESTARTS 5          /* restarts allowed ... */
#define WINDOW       10.0       /* ... inside this many seconds */
#define GRACE        2.0        /* seconds between SIGTERM and SIGKILL */

struct child {
    char        *name;
    char        *mode;
    pid_t        pid;           /* 0 = not running */
    int          restarts;      /* inside the current window */
    double       window_start;
    int          gave_up;
};

static struct child kids[MAX_CHILDREN];
static int          nkids;
static sigset_t     orig_mask;      /* the mask we had before blocking anything */

/* --- signal handlers: flags only ------------------------------------------ */

static volatile sig_atomic_t child_died = 0;
static volatile sig_atomic_t stop_now   = 0;

static void on_sigchld(int sig) { (void) sig; child_died = 1; }
static void on_stop(int sig)    { (void) sig; stop_now   = 1; }

/* --- helpers -------------------------------------------------------------- */

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + 1e-9 * t.tv_nsec;
}

static void logf_(const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    fprintf(stderr, "[sup %8.3f] ", now());
    vfprintf(stderr, fmt, ap);
    va_end(ap);
    fflush(stderr);
}

static void start(struct child *c)
{
    fflush(NULL);                                   /* L01 §6: flush before fork */
    pid_t p = fork();
    if (p < 0) { logf_("fork(%s) failed: %s\n", c->name, strerror(errno)); return; }
    if (p == 0) {
        /* The mask is inherited across fork AND exec (L01 §7). Restore it, or
         * every child runs with SIGTERM blocked and cannot be stopped. */
        sigprocmask(SIG_SETMASK, &orig_mask, NULL);
        char *argv[] = { "./flaky", c->name, c->mode, NULL };
        execv(argv[0], argv);
        _exit(127);                                 /* exec failed: 127, as a shell does */
    }
    c->pid = p;
    logf_("started %-6s pid %d (mode %s)\n", c->name, (int) p, c->mode);
}

static struct child *by_pid(pid_t p)
{
    for (int i = 0; i < nkids; i++) if (kids[i].pid == p) return &kids[i];
    return NULL;
}

static int running(void)
{
    int n = 0;
    for (int i = 0; i < nkids; i++) if (kids[i].pid > 0) n++;
    return n;
}

/* Reap every child that is ready. Returns the number reaped. */
static int reap_1(int restart, int block);
static int reap(int restart) { return reap_1(restart, 0); }

static int reap_1(int restart, int block)
{
    int st, n = 0;
    pid_t p;
    while ((p = waitpid(-1, &st, block ? 0 : WNOHANG)) > 0) {
        n++;
        struct child *c = by_pid(p);
        if (!c) { logf_("reaped unknown pid %d\n", (int) p); continue; }
        c->pid = 0;

        if (WIFEXITED(st))
            logf_("%-6s pid %d exited, status %d\n", c->name, (int) p, WEXITSTATUS(st));
        else if (WIFSIGNALED(st))
            logf_("%-6s pid %d killed by signal %d (%s)%s\n", c->name, (int) p,
                  WTERMSIG(st), strsignal(WTERMSIG(st)), WCOREDUMP(st) ? ", core" : "");

        if (!restart) continue;

        double t = now();
        if (t - c->window_start > WINDOW) { c->window_start = t; c->restarts = 0; }
        if (++c->restarts > MAX_RESTARTS) {
            c->gave_up = 1;
            logf_("%-6s crash-looped %d times in %.0fs — giving up\n",
                  c->name, c->restarts - 1, WINDOW);
            continue;
        }
        start(c);
    }
    return n;
}

static int all_gone(void)
{
    for (int i = 0; i < nkids; i++) if (kids[i].pid > 0) return 0;
    return 1;
}

/* --- main ----------------------------------------------------------------- */

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s <name>:<mode> ...\n", argv[0]); return 2; }

    for (int i = 1; i < argc && nkids < MAX_CHILDREN; i++) {
        char *colon = strchr(argv[i], ':');
        if (!colon) { fprintf(stderr, "bad spec '%s'\n", argv[i]); return 2; }
        *colon = '\0';
        kids[nkids].name = argv[i];
        kids[nkids].mode = colon + 1;
        kids[nkids].window_start = now();
        nkids++;
    }

    /* Block first, install second: nothing can be delivered before we are ready. */
    sigset_t block, orig;
    sigemptyset(&block);
    sigaddset(&block, SIGCHLD);
    sigaddset(&block, SIGTERM);
    sigaddset(&block, SIGINT);
    sigprocmask(SIG_BLOCK, &block, &orig);
    orig_mask = orig;

    struct sigaction sa;
    memset(&sa, 0, sizeof sa);
    sa.sa_handler = on_sigchld;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;
    if (sigaction(SIGCHLD, &sa, NULL) < 0) { perror("sigaction"); return 1; }
    sa.sa_handler = on_stop;
    sa.sa_flags = 0;
    if (sigaction(SIGTERM, &sa, NULL) < 0) { perror("sigaction"); return 1; }
    if (sigaction(SIGINT,  &sa, NULL) < 0) { perror("sigaction"); return 1; }

    for (int i = 0; i < nkids; i++) start(&kids[i]);

    /* Supervise. SIGCHLD is blocked except inside sigsuspend, so the flag
     * cannot be set between the test and the wait. */
    while (!stop_now) {
        if (child_died) { child_died = 0; reap(1); }
        int live = 0;
        for (int i = 0; i < nkids; i++) if (kids[i].pid > 0 || !kids[i].gave_up) live++;
        if (live == 0) { logf_("nothing left to supervise\n"); break; }
        sigsuspend(&orig);
    }

    if (stop_now) logf_("shutdown requested\n");

    /* Graceful stop: SIGTERM, wait up to GRACE, then SIGKILL. */
    for (int i = 0; i < nkids; i++)
        if (kids[i].pid > 0) { logf_("SIGTERM -> %s\n", kids[i].name); kill(kids[i].pid, SIGTERM); }

    double deadline = now() + GRACE;
    while (!all_gone() && now() < deadline) {
        if (child_died) { child_died = 0; reap(0); }
        struct timespec ts = { 0, 50 * 1000 * 1000 };
        sigset_t idle = orig;
        ppoll(NULL, 0, &ts, &idle);          /* unblock + sleep, atomically */
    }
    reap(0);

    for (int i = 0; i < nkids; i++)
        if (kids[i].pid > 0) {
            logf_("%s ignored SIGTERM — SIGKILL\n", kids[i].name);
            kill(kids[i].pid, SIGKILL);
        }
    while (!all_gone() && reap_1(0, 1) > 0)
        ;                                   /* blocking now: SIGKILL cannot be ignored */

    logf_("all children stopped (%d still marked running)\n", running());
    return 0;
}
```

---

## The Three Lines That Are the Lab

**1. The reaping loop.**

```c
while ((p = waitpid(-1, &st, block ? 0 : WNOHANG)) > 0) { ... }
```

Not `if`. Not one `waitpid`. **`SIGCHLD` does not queue** (L03 §3), so a delivery means "at least one child died". Part A's Q1 makes them measure it: with a one-shot reap and three children exiting together, they typically reap one and leave two zombies — and the count varies run to run, which is the most useful part of the observation.

**2. Block before installing, and `sigsuspend` to wait.**

```c
sigprocmask(SIG_BLOCK, &block, &orig);   /* before the first start() */
...
while (!stop_now) {
    if (child_died) { child_died = 0; reap(1); }
    sigsuspend(&orig);
}
```

The flag is only ever *set* while `SIGCHLD` is blocked outside `sigsuspend`, so the test-then-wait window of L03 §7 does not exist. Students who use `pause()` here will pass the lab and hang in Part D's Q7 — which is the intended sequence.

**3. Restoring the mask in the child.**

```c
if (p == 0) {
    sigprocmask(SIG_SETMASK, &orig_mask, NULL);   /* ← Part C's bug */
    execv(...);
}
```

---

## Part C: The Bug, and How to Run the Discussion

**Symptom:** the `ok` child ignores `SIGTERM` exactly like the `hang` child does, and both need `SIGKILL`.

**Cause:** the supervisor blocks `SIGCHLD`, `SIGTERM` and `SIGINT` before forking. The mask is inherited across `fork` **and preserved across `exec`** (L01 §7), so `flaky` starts life with `SIGTERM` blocked. The signal is delivered and stays *pending*, forever, because nothing in `flaky` ever unblocks it.

**This is not a toy.** It is a known class of production bug: a service manager that leaks its mask into every service it starts, which then cannot be shut down cleanly. `systemd` resets the mask explicitly in `spawn`; `posix_spawn` takes `POSIX_SPAWN_SETSIGMASK` for exactly this reason.

**Make them prove it, do not just tell them:**

```bash
$ grep SigBlk /proc/$(pgrep -x flaky)/status
SigBlk:	0000000000014002
```

**Bit *n−1* is signal *n*.** `0x14002` = bits 1, 14 and 16 = signals **2, 15 and 17** = `SIGINT`, `SIGTERM`, `SIGCHLD` — exactly the three the supervisor blocked. Walk them through that arithmetic on the board; decoding a hex signal mask by hand takes three minutes and it is on the Midterm.

After the fix, the same command prints `SigBlk: 0000000000000000`. Both values above were measured on the reference machine, from the buggy and fixed builds of this lab's solution.

**A second thing worth pointing at in the same output:** `flaky` in `hang` mode shows `SigIgn: 0000000000004000` — bit 14, `SIGTERM` — which is how the child announces, in `/proc`, that it will not honour a polite request. Real supervisors cannot read that in advance, which is why the SIGKILL escalation exists.

**Q4 model answer.** `sigprocmask(SIG_BLOCK, ...)` in the parent created it; `exec` does not clear the mask because the mask is a property of the *process*, not of the program image — `exec` resets signal *handlers* (the functions are gone) but a mask is just a bitmask in the kernel's task structure and there is nothing about it that a new program image invalidates. One-line fix as above.

**Q5 model answer.** `kill(-pgid, SIGTERM)` reaches the child's *own* children too. `flaky` has none, but a supervised worker that forks (a web server with worker processes, say) leaves grandchildren running when you signal only the direct child. Every real supervisor uses `setpgid()` in the child and signals the group. **Accept anything that identifies grandchildren.**

---

## Part D: Q7, the Race

The broken version:

```c
while (!stop_now)
    pause();
```

`SIGTERM` arriving between the test and the `pause()` sets `stop_now`, runs the handler, and returns — and then `pause()` blocks waiting for a signal that has already been delivered. The supervisor hangs until another signal arrives, which for an idle supervisor with one healthy child is up to thirty seconds away (the next `SIGCHLD`), and in a real daemon may be never.

**Reproducing it on demand** — students often cannot make it fail:

```c
while (!stop_now) {
    /* widen the window deliberately */
    struct timespec t = { 0, 100 * 1000 * 1000 };
    nanosleep(&t, NULL);
    pause();
}
```

With a 100 ms window, one `kill -TERM` in ten or so lands inside it. **This is the lesson worth stating out loud:** the correct and incorrect programs are indistinguishable on any run where the timing does not happen to bite, so "I tested it" is not evidence. It is the same argument as the `malloc`-in-a-handler experiment in L03 §4, arriving from the other direction.

---

## Common Failures, in Frequency Order

| What they wrote | What happens | What to say |
|---|---|---|
| `fork()` in the `SIGCHLD` handler | Usually works, occasionally forks from inside a `malloc` | "What is the handler allowed to call? Check `man 7 signal-safety`" |
| `printf` in the handler | Usually works | Same. Then show them L03 §4's corruption count |
| One `waitpid` per delivery | Zombies under load only | Part A Q1 is the demonstration; make them run it |
| `while(1) { reap(); usleep(1000); }` | Works, 100% correct output, 3% CPU | "What is this process doing 999 µs out of every 1000?" |
| No `WNOHANG` in the handler | Handler blocks; program freezes | `strace -p` shows it parked in `wait4` |
| `signal()` instead of `sigaction()` | Works on Linux | "Name the three things you did not specify" (L03 §2) |
| Forgetting `fflush(NULL)` before `fork` | Duplicated log lines | PS 0 Q1(b) is the same bug |
| Reaping into `by_pid()` without clearing `c->pid` | Restart loop restarts the wrong child | Trace one iteration on paper |

---

## Checkoff Standard

Check off a student whose supervisor:

- restarts a crashing child and **gives up** on a flapping one,
- shuts down cleanly with **no `flaky` left in `pgrep`**,
- shows **~0.0% CPU** in `top` while idle,
- has **no unsafe call in any handler**.

Written answers to Q1, Q4 and Q7 are required for the checkoff; three or four sentences each. **Do not require Q2, Q3, Q5 or Q6 in writing** — they are there for the students who finish early, and Q2 in particular (exponential backoff) is a Week 12 design conversation rather than a Week 0 one.

**A student who cannot finish Part C in the session** should be checked off on A and B and told to bring C to Monday's office hours. It is Week 0; nobody has written a signal handler before, and the point of the bug is that it is hard.

---

*PROG 201 · Week 0 · Lab 0 Solutions · Instructor Only · © CSE Department*

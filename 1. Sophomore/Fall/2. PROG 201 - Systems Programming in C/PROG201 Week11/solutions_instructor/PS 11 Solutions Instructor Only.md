# PROG 201 · PS 11 Solutions
## Build a Mini-Container — Instructor Only

---

**Do not distribute.** Reference `container.c`, the expected report figures, and the rubric notes.

**Machine:** Ubuntu 24.04, glibc 2.39, Linux 7.0.0-30, cgroup v2, `apparmor_restrict_unprivileged_userns` = 1.

---

## Reference `container.c` (do not distribute)

```c
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sched.h>
#include <signal.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <sys/mount.h>

static char child_stack[1 << 20];
struct args { char **argv; int p[2]; };

static int child(void *arg)
{
    struct args *a = arg;
    char c;
    close(a->p[1]);
    if (read(a->p[0], &c, 1) != 0) { }    /* block until parent writes maps */

    if (sethostname("container", 9) < 0) perror("sethostname");
    if (mount("none", "/", NULL, MS_REC | MS_PRIVATE, NULL) < 0) perror("mount private");
    if (mount("proc", "/proc", "proc", 0, NULL) < 0) perror("mount /proc");

    printf("[container] PID %d, uid %d\n", getpid(), getuid());
    fflush(stdout);
    execvp(a->argv[0], a->argv);
    fprintf(stderr, "exec %s: %s\n", a->argv[0], strerror(errno));
    return 127;
}

static void wmap(pid_t pid, const char *f, const char *line)
{
    char path[64]; snprintf(path, sizeof path, "/proc/%d/%s", pid, f);
    int fd = open(path, O_WRONLY);
    if (fd < 0 || write(fd, line, strlen(line)) < 0)
        fprintf(stderr, "write %s: %s\n", path, strerror(errno));
    if (fd >= 0) close(fd);
}

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s cmd [args...]\n", argv[0]); return 2; }
    struct args a = { .argv = argv + 1 };
    if (pipe(a.p) < 0) { perror("pipe"); return 1; }

    int flags = CLONE_NEWUSER | CLONE_NEWPID | CLONE_NEWNS |
                CLONE_NEWUTS | CLONE_NEWNET | CLONE_NEWIPC | SIGCHLD;
    pid_t pid = clone(child, child_stack + sizeof child_stack, flags, &a);
    if (pid < 0) { fprintf(stderr, "clone: %s\n", strerror(errno)); return 1; }

    char line[64];
    snprintf(line, sizeof line, "0 %d 1", getuid()); wmap(pid, "uid_map", line);
    wmap(pid, "setgroups", "deny");
    snprintf(line, sizeof line, "0 %d 1", getgid()); wmap(pid, "gid_map", line);

    close(a.p[1]); close(a.p[0]);            /* release the child */

    int st; waitpid(pid, &st, 0);
    return WIFEXITED(st) ? WEXITSTATUS(st) : 1;
}
```

Builds warning-clean under `-Wall -Wextra -O2 -std=gnu11`. Any structurally equivalent solution is
fine; the four gradable properties are (a) `CLONE_NEWUSER` present with the other five, (b) the
pipe-sync so the child does not race the maps, (c) `setgroups`=`deny` **before** `gid_map`, (d)
child exit status propagated.

---

## Expected report figures (Parts B & C)

| Measurement | Producing command | Expected |
| --- | --- | --- |
| container self-PID | `./container sh -c 'echo $$'` | **1** |
| host PID of child | `pgrep -a container` | large, e.g. **1251803** |
| interfaces inside | `./container ip -o link show` | **1** (`lo`, DOWN) |
| interfaces host | `ip -o link show` | **3** (`lo`, `enp0s31f6`, `wlp61s0`) |
| kernel inside / host | `./container uname -r` / `uname -r` | **identical**, `7.0.0-30-generic` |
| `sethostname` errno | inside container | **EPERM** |
| `mount` errno | inside container | **EACCES/EPERM** |
| userns restriction | `cat /proc/sys/.../apparmor_restrict_unprivileged_userns` | **1** |
| memory kill point / code | `systemd-run --user --scope -p MemoryMax=100M -p MemorySwapMax=0 ./hog; echo $?` | **~90 MiB, 137** |
| pids limit errno | fork loop under `-p TasksMax=20` | **EAGAIN** at the cap |
| startup: fork / clone / +6ns | `./cost` | **139 / 119 / 1002 µs** |
| seccomp getpid | `./sec` | **-1, EPERM** |

Accept same-order figures for the timings and the OOM point (both drift). The **kernel-identical**,
**one-interface**, **EPERM-on-mount**, and **exit-137** results are categorical and must be present.

---

## Grading notes (100 pts)

**Part A (40).** −10 if `CLONE_NEWUSER` is created in a separate call from the rest (works by luck
only as root; on a student account it EPERMs — if their binary runs, they likely tested as root,
flag it). −10 no pipe sync (child sees uid 65534; often they "fix" it by sleeping — do not accept a
`sleep`, that is a race not a fix). −5 `gid_map` before `setgroups`. −5 warnings. **−0** for the
mount/sethostname EPERM appearing — that is correct behaviour here. Auto-zero the binary-in-repo,
per course policy, but grade the source.

**Part B (35).** Each of PID / net / kernel worth ~8; the deviation explanation worth ~11. Full
marks on the deviation require: uid-0-yet-refused stated, AppArmor named, and the *distinction*
between namespace existence (enforced, works) and privileged operations within (stripped, fail).

**Part C (25).** Memory 137 decoded (10), cost table with the VM comparison (8), seccomp EPERM with
the no_new_privs reason (7). Either pids form (measured or explained-from-docs) is accepted.

**The recurring-theme credit.** A report that connects the mount EPERM to the Week 3/8/10 "present
but not working" thread — a namespace created is not a capability granted — has understood the week.
Note it; it is the intended synthesis.

## Common errors

- **Tested as root** (sudo) → everything "works", no EPERM reported. Tell: `id -u` outside is 0, or
  the report shows a successful hostname change. That is not the assignment; the unprivileged
  boundary is.
- **`sleep` instead of a pipe** → intermittent uid-65534. Race, not a fix.
- **Claiming a private `/proc`** → they read the inherited host `/proc`. Ask them to `ls /proc/1` —
  it is the host's init, proving the mount did *not* happen.
- **Missing attribution on figures** → each number must name its command (course rule); dock per the
  report rubric.

---

*PROG 201 · Week 11 · PS 11 Solutions · Instructor Only*

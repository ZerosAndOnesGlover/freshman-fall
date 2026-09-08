# PROG 201 · Lab 6 Solutions
## Adding Job Control — Instructor Only

---

**Do not distribute.** Part A(b) — the shell hanging on Ctrl-Z — is the lab's opening and is spoiled by reading the fix.

**Machine these numbers came from:** Linux 7.0.0-30-generic, gcc 13.3.0 (Ubuntu 24.04). Everything in this lab needs a **controlling terminal**; the reference session transcripts below were driven over a pseudo-terminal with `pty.fork()`, which behaves identically to a student sitting at BH 215.

---

## 1. The Five TODOs

The scaffolding — the tokeniser, the parser, `run`, `cd`, `exit`, the startup sequence, and `groups.c`/`ttyctl.c`/`groupsig.c` — is provided.

```c
static struct job *job_add(pid_t pgid, pid_t *pids, int nproc, const char *line)
{
    for (int i = 0; i < MAXJOB; i++)
        if (jobs[i].state == JOB_FREE) {
            memset(&jobs[i], 0, sizeof jobs[i]);
            jobs[i].id = next_id++; jobs[i].pgid = pgid;
            jobs[i].state = JOB_RUNNING; jobs[i].nproc = nproc;
            jobs[i].npid = nproc;
            for (int k = 0; k < nproc; k++) jobs[i].pid[k] = pids[k];
            snprintf(jobs[i].cmdline, sizeof jobs[i].cmdline, "%s", line);
            return &jobs[i];
        }
    return NULL;
}

static struct job *job_by_pid(pid_t p)
{
    for (int i = 0; i < MAXJOB; i++)
        if (jobs[i].state != JOB_FREE)
            for (int k = 0; k < jobs[i].npid; k++)
                if (jobs[i].pid[k] == p) return &jobs[i];
    return NULL;
}

static void reap(int block_for_pgid)
{
    for (;;) {
        int st;
        pid_t p = waitpid(-1, &st, WUNTRACED | WCONTINUED | (block_for_pgid ? 0 : WNOHANG));
        if (p <= 0) break;
        /* NOT getpgid(p): p has just been reaped and no longer exists. */
        struct job *j = job_by_pid(p);
        if (!j) continue;
        pid_t pg = j->pgid;
        if (WIFSTOPPED(st)) {
            j->state = JOB_STOPPED;
            printf("\n[%d]+  %-22s %s\n", j->id, "Stopped", j->cmdline);
            if (block_for_pgid == pg) return;
        } else if (WIFCONTINUED(st)) {
            j->state = JOB_RUNNING;
        } else {
            if (--j->nproc == 0) {
                if (j->state == JOB_RUNNING && block_for_pgid != pg)
                    printf("[%d]+  %-22s %s\n", j->id, "Done", j->cmdline);
                j->state = JOB_FREE;
                if (block_for_pgid == pg) return;
            }
        }
    }
}

static void wait_foreground(struct job *j)
{
    reap(j->pgid);                                   /* blocks until it stops or dies */
    signal(SIGTTOU, SIG_IGN);
    tcsetpgrp(shell_tty, shell_pgid);                /* take the terminal back */
    tcsetattr(shell_tty, TCSADRAIN, &shell_modes);
    signal(SIGTTOU, SIG_DFL);
}

/* ---- inside builtin() ---- */

    if (!strcmp(a[0], "jobs")) {
        for (int i = 0; i < MAXJOB; i++)
            if (jobs[i].state != JOB_FREE)
                printf("[%d]%c  %-22s %s\n", jobs[i].id,
                       jobs[i] .id == (job_recent(0) ? job_recent(0)->id : -1) ? '+' : '-',
                       jobs[i].state == JOB_STOPPED ? "Stopped" : "Running", jobs[i].cmdline);
        return 1;
    }
    if (!strcmp(a[0], "fg") || !strcmp(a[0], "bg")) {
        int fg = !strcmp(a[0], "fg");
        struct job *j = a[1] ? job_by_id(atoi(a[1] + (a[1][0] == '%'))) : job_recent(!fg);
        if (!j) { fprintf(stderr, "%s: no such job\n", a[0]); return 1; }
        printf("%s\n", j->cmdline);
        if (fg) {
            signal(SIGTTOU, SIG_IGN);
            tcsetpgrp(shell_tty, j->pgid);
            signal(SIGTTOU, SIG_DFL);
        }
        j->state = JOB_RUNNING;
        kill(-j->pgid, SIGCONT);
        if (fg) wait_foreground(j);
        return 1;
    }
    if (!strcmp(a[0], "kill")) {
        if (!a[1]) { fprintf(stderr, "kill: usage: kill %%job\n"); return 1; }
        struct job *j = job_by_id(atoi(a[1] + (a[1][0] == '%')));
        if (!j) { fprintf(stderr, "kill: no such job\n"); return 1; }
        kill(-j->pgid, SIGTERM); kill(-j->pgid, SIGCONT);
        return 1;
    }

/* ---- the end of run() ---- */

    if (c->background) {
        printf("[%d] %d\n", j->id, pgid);
    } else {
        signal(SIGTTOU, SIG_IGN);
        tcsetpgrp(shell_tty, pgid);
        signal(SIGTTOU, SIG_DFL);
        wait_foreground(j);
    }```

The skeleton's `(void) job_by_pid; (void) job_by_id; ...` line in `main` should be deleted once all five are done; a submission that still has it and still builds warning-free has not used one of the helpers.

Builds clean under `gcc -Wall -Wextra -O2 -g -std=c11 -o tsh tsh.c`.

---

## 2. Where Students Get Stuck

| # | Symptom | Cause | What to say |
| --- | --- | --- | --- |
| 1 | Ctrl-Z still hangs after TODO 2 | `WUNTRACED` omitted, or `WNOHANG` left on the blocking path | "What are the three cases `waitpid` can report?" |
| 2 | `jobs` lists a job that is definitely dead | `getpgid(p)` after `waitpid` — **the lab's set-piece bug** | Let them find it. Q4 |
| 3 | `fg` prints the command line and hangs | `wait_foreground` reaps with the wrong pgid, or `reap(0)` | Have them print what `reap` is blocking on |
| 4 | The shell stops itself when a job finishes | `tcsetpgrp` without `SIGTTOU` ignored | `ps -o stat` shows the shell as `T`. L20 §4 |
| 5 | `cat` in the foreground stops immediately | TODO 5 not done — the job is in the background, so `SIGTTIN` | This is `ttyctl`'s first row happening to them |
| 6 | Two-stage pipeline reports `Done` twice, or never | `nproc` not decremented per process, or decremented per job | `sleep 5 \| cat` is one job and two processes |
| 7 | `fg` on a `cat &` does nothing, sometimes | `SIGCONT` before `tcsetpgrp` — Part D(a), arriving early | Congratulate them; it is Q6 |

**Symptom 2 is the one to protect.** If a student asks why `jobs` will not clear, ask what `p` refers to after `waitpid` has returned it, and let them get there. It is the best twenty seconds in the session.

---

## 3. Reference Output

**`groups`** — the four rows of L20 §2:

```
the shell's child      pid=1092347 ppid=1092345 pgid=1092347 sid=1092347 tcpgrp=1092347  <- foreground
  fork, nothing else   pid=1092348 ppid=1092347 pgid=1092347 sid=1092347 tcpgrp=1092347  <- foreground
  after setpgid(0,0)   pid=1092349 ppid=1092347 pgid=1092349 sid=1092347 tcpgrp=1092347
  after setsid()       pid=1092350 ppid=1092347 pgid=1092350 sid=1092350 tcpgrp=-1
  pipeline stage 0     pid=1092351 ppid=1092347 pgid=1092351 sid=1092347 tcpgrp=1092347
  pipeline stage 1     pid=1092352 ppid=1092347 pgid=1092351 sid=1092347 tcpgrp=1092347
```

**`ttyctl`** — three operations, three answers:

```
TOSTOP is clear by default

a process group that is NOT the foreground one:
  read() from the terminal                   STOPPED by Stopped (tty input)
  (background wrote this)
  write() to the terminal                    exited 0
  tcsetattr() on the terminal                STOPPED by Stopped (tty output)

now with TOSTOP set:
  write() to the terminal                    STOPPED by Stopped (tty output)
```

**`groupsig`** — the minus sign:

```
kill(1092546, SIGINT)   -- one process by pid:
  A[0] pid 1092545: still running
  A[1] pid 1092546: Interrupt
  A[2] pid 1092547: still running

kill(-1092545, SIGINT)  -- the whole group:
  A[0] pid 1092545: Interrupt
  A[1] pid 1092546: already reaped
  A[2] pid 1092547: Interrupt
  B    pid 1092548: still running   <- a different group, untouched
```

**The finished shell**, driven over a pty:

```
tsh> sleep 30 &
[1] 1093018
tsh> jobs
[1]+  Running                sleep 30 &
tsh> sleep 30
^Z
[2]+  Stopped                sleep 30
tsh> jobs
[1]-  Running                sleep 30 &
[2]+  Stopped                sleep 30
tsh> bg
sleep 30
tsh> jobs
[1]-  Running                sleep 30 &
[2]+  Running                sleep 30
tsh> kill %1
tsh> jobs
[2]+  Running                sleep 30
[1]+  Done                   sleep 30 &
```

Note the last two lines: **`Done` arrives after the `jobs` output**, because reaping happens at the top of the next loop iteration. `bash` does the same thing, and a student who reports it as a bug should be shown `bash` doing it.

---

## 4. Answers

**Q1 — `setsid()`.**

It changed `pgid`, `sid` and **`tcpgrp`, which became −1**: the new session has **no controlling terminal**, so `/dev/tty` cannot be opened and `tcgetpgrp` has nothing to report.

A program that wants exactly that: **any daemon** — `sshd`, `cron`, `systemd` units. It cannot be killed by a Ctrl-C, cannot be hung up on when a terminal closes, and cannot accidentally read somebody's keystrokes.

**Q2 — the missing flag.**

**`WUNTRACED`.** Without it, `waitpid` does not return when a child *stops* — a stop is not a termination, and the default `waitpid` reports only terminations. So the shell sits in `waitpid` for a process that is in state `T` and is never going to exit, and neither process is misbehaving.

The shell could not tell anything had happened because **nothing was delivered to it**: `SIGTSTP` went to the foreground process group, which — at that point in the lab — was the shell's own group, and the shell ignores it. The child stopped because it was in the same group. Full marks need "the shell got no notification", not just "it was waiting".

**Q3 — three operations, three reasons.**

- **`read` is forbidden** because two processes competing for one keyboard is unusable — there is no sensible way to split keystrokes. `SIGTTIN`.
- **`write` is allowed** because the alternative — stopping every background job the moment it prints anything — is worse in practice than interleaved output. `TOSTOP` exists for people who disagree.
- **`tcsetattr` is always forbidden** because a background process changing the terminal's mode changes it for the foreground process too, which is unambiguously wrong. `SIGTTOU`, regardless of `TOSTOP`.

Three marks, one each. A student who says "they are all about not interfering with the foreground process" has the idea but not the question.

**Q4 — `getpgid` after `waitpid`.**

`waitpid` returning `p` means **`p` has been reaped and no longer exists**, so `getpgid(p)` fails with `ESRCH` and returns −1. The job lookup fails, the job is never marked done, and `jobs` lists it for ever — while the process is genuinely gone.

The general rule: **after `waitpid` returns, the status is the only thing you still know about that process.**

The same class from an earlier week: **`stat`-then-`open`** (PS 5 Q3(a)), or **`lseek`-then-`write`** (Week 1 L05 §5) — a **TOCTTOU** race, where the thing you asked about changes between the question and the use. Accept either, or "two system calls are not one".

**Q5 — the command line.**

The copy is made in `main` **before** `tokenize` runs, because `tokenize` writes NULs into the buffer in place to terminate each word. Without it, `jobs` would print only the **first word** — `printf("%s", line)` stops at the first NUL, so `sleep 20 | cat` becomes `sleep`.

**Q6 — Part D(a), `SIGCONT` before `tcsetpgrp`.**

Expected report: `fg` on a job stopped by `SIGTTIN` **sometimes appears to do nothing** — the job continues, immediately tries to read the terminal, is still in the background at that instant, gets `SIGTTIN` again and stops. Sometimes it works, because the `tcsetpgrp` landed before the job got scheduled.

**Intermittent because it is a race between the shell's next instruction and the continued process being scheduled.** On a loaded machine it fails more often; on an idle one it may never fail, which is what makes it a genuinely nasty bug. Full marks need the word "race" and the reason the window exists.

**Q7 — Part D(b), the `setpgid` race.**

**"I could not reproduce it" is the expected answer and is worth full marks with the explanation.** The window is between `fork` returning in the child and the parent's `setpgid` executing, and on this machine the parent almost always wins.

The race: if only the **child** calls `setpgid`, the parent may `tcsetpgrp` to a group that does not exist yet. If only the **parent** calls it, the child may reach `execvp` first — and `setpgid` on a process that has already `exec`ed fails with `EACCES`, so the program runs in the shell's own group and a Ctrl-C then kills the shell too.

Both processes call it because **whichever runs first makes it true**, and the other's call is a harmless no-op or a harmless failure. APUE §9.4 says exactly this.

**Q8 — what delivers Ctrl-C.**

**The terminal driver**, which sends `SIGINT` to every process in the terminal's foreground process group — `kill(-tpgid, SIGINT)`, in effect. The shell ignores the signal and is not in that group, so it neither receives it nor has to forward it.

---

## 5. Checkoff

The four boxes are in the lab sheet. In practice:

- **Watch them press Ctrl-Z on the unmodified skeleton first.** The lab does not work as a lecture; the hang is what makes `WUNTRACED` memorable.
- **`ps -o pid,ppid,pgid,sid,tpgid,stat,wchan,comm`** should be on the board for the whole session. Point students at it rather than at their source, every time.
- **Q4 out loud.** If they hit the bug and fixed it by switching to `job_by_pid`, ask why the old version failed — some will have changed it by trial and error.
- The extension (warn on exit with stopped jobs, then `disown`) is a good twenty minutes and connects directly to L20 §6.

**Timing.** Setup 5, Part A 20, Part B 35, Part C 30, Part D 15 — 105 against 110. **Part D is the one to drop** if the room is behind; both breakages are described in the lectures with the same conclusions.

---

*PROG 201 · Week 6 · Lab 6 Solutions · Instructor Only · © CSE Department*

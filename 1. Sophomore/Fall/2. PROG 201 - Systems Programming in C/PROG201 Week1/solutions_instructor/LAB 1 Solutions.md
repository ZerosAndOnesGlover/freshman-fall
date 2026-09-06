# PROG 201 · Lab 1 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Monday of Week 2, 15:00–16:50, BH 215. **Unmarked** — checked off in the session.

**The one thing this lab teaches.** Not `pipe()` — that is one call and nobody struggles with it. It is this:

> **A pipe reports EOF only when the last write-end descriptor, in every process, is closed.**

Everything that goes wrong in this room for the next two hours is that sentence. Budget your attention accordingly: Part A is fifteen minutes of typing and forty-five of debugging, and the debugging is the lab.

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–5 | Setup | `make`, `./compare.sh` — everything fails, as it should |
| 5–35 | A: two stages | Most will get output. Some will hang |
| 35–60 | A: the hang | **Teach `ps -o wchan` here, once, to the whole room** |
| 60–85 | B: N stages | The `in` invariant is the trick; point at it rather than explaining it |
| 85–105 | C: break it | The three-row table in Q5 is the payoff |
| 105–110 | D + checkoff | |

---

## Reference Solution

```c
/* pipeline.c — LAB 1 reference solution.
 *
 *   ./pipeline ls -1 /etc : grep host : wc -l
 *
 * Runs the stages connected by pipes, exactly as a shell does. No shell is
 * involved: every pipe(), fork(), dup2() and close() is here.
 */
#define _GNU_SOURCE
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

#define MAX_STAGES 16

int main(int argc, char **argv)
{
    char **stage[MAX_STAGES];
    int nstages = 0;

    /* Split argv on ":" — each run of words is one stage's argv. */
    stage[nstages++] = &argv[1];
    for (int i = 1; i < argc; i++)
        if (!strcmp(argv[i], ":")) {
            argv[i] = NULL;                      /* terminate the previous stage */
            if (nstages == MAX_STAGES) { fprintf(stderr, "too many stages\n"); return 2; }
            stage[nstages++] = &argv[i + 1];
        }
    if (argc < 2) { fprintf(stderr, "usage: %s cmd args : cmd args : ...\n", argv[0]); return 2; }

    pid_t pid[MAX_STAGES];
    int in = STDIN_FILENO;                       /* what this stage reads from */

    for (int s = 0; s < nstages; s++) {
        int fd[2] = { -1, -1 };
        int last = (s == nstages - 1);

        if (!last && pipe(fd) < 0) { perror("pipe"); return 1; }

        fflush(NULL);
        if ((pid[s] = fork()) < 0) { perror("fork"); return 1; }

        if (pid[s] == 0) {
            /* child: wire stdin and stdout, then close every descriptor that
             * is not one of them — a pipe with a writer still open never
             * reports EOF, and the writer that hangs the pipeline is usually
             * a forgotten copy in some other process. */
            if (in != STDIN_FILENO)  { dup2(in, STDIN_FILENO);   close(in); }
            if (!last)               { close(fd[0]);
                                       dup2(fd[1], STDOUT_FILENO); close(fd[1]); }
            execvp(stage[s][0], stage[s]);
            fprintf(stderr, "%s: %s\n", stage[s][0], strerror(errno));
            _exit(127);
        }

        /* parent: hand the read end to the next stage and drop everything else */
        if (in != STDIN_FILENO) close(in);
        if (!last) { close(fd[1]); in = fd[0]; }
    }

    int status, rc = 0;
    for (int s = 0; s < nstages; s++) {
        waitpid(pid[s], &status, 0);
        if (s == nstages - 1)                    /* a shell reports the LAST stage */
            rc = WIFEXITED(status) ? WEXITSTATUS(status) : 128 + WTERMSIG(status);
    }
    return rc;
}
```

**Verified:** `./compare.sh` passes all eight checks against the reference — one stage, two, three, empty output, 2,073 lines of input, early exit, exit status, and command-not-found.

---

## The Loop Invariant, and How To Teach It

Do not explain the whole loop. Write this on the board and stop:

```
in = the descriptor the NEXT stage should read from
```

It starts as `STDIN_FILENO`. Each iteration:

1. make a pipe (unless last),
2. fork; the child dups `in` onto 0 and `fd[1]` onto 1, closes everything else, execs,
3. the parent closes `in` (it has been handed on) and `fd[1]` (the child has it), then sets `in = fd[0]`.

**Students who are stuck on N stages are almost always keeping a stage's read end alive one iteration too long.** The invariant tells them where the `close` goes without you writing their code.

---

## Q2: The Hang, and the Diagnosis

Reproduced deliberately by deleting the parent's `close(fd[1])`:

```
$ timeout 5 ./pipeline_bug ls -1 /etc : wc -l
(nothing)                                        rc=124
$ ps -o pid,stat,wchan:20,comm -C wc
    PID STAT WCHAN                COMMAND
 415630 S    anon_pipe_read       wc
```

**`WCHAN` is the kernel function the process is blocked in.** `anon_pipe_read` says, with no ambiguity, "waiting to read from a pipe" — and since `ls` has finished and exited, the only reason there is no EOF is that somebody still holds the write end. That somebody is the parent, which never uses it.

**Teach the general move, not the specific bug:** when a program hangs, the first question is *where*, and `ps -o wchan` answers it in one line without gdb, without prints, and without recompiling. It works on any stuck process on the machine, including one you did not write.

**Model answer to Q2:** the parent (the `pipeline` process itself) holds `fd[1]`. `ls` exited and closed its copy, but the pipe still has a writer, so `wc`'s `read` cannot return 0. The parent is simultaneously blocked in `waitpid` for `wc`. **Neither process is buggy in isolation; the deadlock is between them.**

---

## Q3: `head` and `SIGPIPE`

`ls -1 /usr/bin` produces **2,073** lines here; `head -3` prints three and exits, closing its read end. `ls` writes on, fills the 64 KB pipe, and the next `write` to a pipe with no reader raises **`SIGPIPE`**, sent by the kernel, whose default action terminates `ls`.

**The shell does not treat this as an error** because it is the mechanism, not a failure: it is how `yes | head -1` terminates at all, and how a pipeline stops reading a 10 GB file the moment the consumer has had enough. `bash` reports the *last* stage's status, and `head` exited 0.

A student who says "`ls` exits early because the pipe is full" is half right and should be pushed to name the signal.

---

## Q4: Exit Status

```
$ ./pipeline true : false ; echo $?
1
```

`waitpid` gives `0x0000` for `true` and `0x0100` for `false`. The pipeline's status is the **last** stage's: `WIFEXITED` true, `WEXITSTATUS` 1. The first stage's status is read and discarded — **but it must still be read**, or the stage becomes a zombie (W0 L02 §2). A student whose loop `break`s after the last stage has left one zombie per pipeline, which `ps` will show them.

*(Worth mentioning: `bash`'s `PIPESTATUS` array exists precisely because the single status throws information away, and `set -o pipefail` changes the rule. Both are one `waitpid` loop away from what they just wrote.)*

---

## Q5: The Three Breakages — the answer table

| Change | What is actually open | Hangs? |
|---|---|---|
| **(a)** parent keeps `fd[1]` | **Two** write-end descriptors: the writing child's, and the parent's — and the parent never exits, because it is in `waitpid` | **Yes.** Measured: `rc=124` under `timeout`, `wc` in `anon_pipe_read` |
| **(b)** middle child keeps `fd[0]` | An extra copy of a **read** end. Read-end copies do not hold EOF open | **No.** Measured: `ls -1 /etc : grep host : wc -l` → `6`, correct. It leaks one descriptor per stage, and enough stages reach `EMFILE` |
| **(c)** child dups `fd[1]` onto 1 and keeps `fd[1]` | **Two** write-end descriptors — but **both in the same process**, so both close when that stage exits | **No.** Measured: correct output, and still correct with a stage that lives four seconds. The leak is into the exec'd program, not into the pipeline's lifetime |

**Do not let the room conclude that (b) and (c) are therefore fine.** They are both bugs; they are
bugs of a different kind, and the measurement is what separates them:

- **(a)** breaks the pipeline, always, because a descriptor survives in a process that outlives the writer.
- **(c)** hands a writable pipe descriptor to a program that never asked for one — a leak in the L06 §4 sense — and becomes a hang the moment that program forks something that lingers.
- **(b)** is a plain resource leak, invisible until the twentieth stage.

**Students will predict "hang" for all three**, because "close everything or it hangs" is the rule
they were given. Making them run it is the point of Part C: the rule is a *consequence*, and the
actual rule is the one sentence at the top of these notes. **A descriptor only holds EOF open if it
is on the write end and it is in a process that keeps running.**

---

## Q6/Q7: Measurement

```
$ strace -f -c -e trace=pipe2,clone,dup2,close,execve,wait4 ./pipeline ls -1 /etc : grep host : wc -l
```

Expect: 2 `pipe2`, 3 `clone`, 4 `dup2` (one per non-terminal stdin, one per non-terminal stdout), 3 `execve`, 3 `wait4`, and a dozen `close`.

**`bash` makes more calls** for the same pipeline: it also `dup2`s to save and restore its own descriptors, sets up process groups (`setpgid`), and manipulates the terminal. **That is Week 6's material arriving early**, and it is a good moment to say so — the extra calls are exactly the difference between a pipeline and a shell.

**Q7:** timings match within noise because the work is `ls` and `wc`, not the plumbing. The setup is a few dozen system calls at ~1.25 µs each (L05 §2) — **tens of microseconds against tens of milliseconds of actual work.** The lesson: the machinery of process creation is not where pipeline performance goes, which is why nobody optimises it and why Week 5's server can afford a fork per connection until it very suddenly cannot.

---

## Common Failures, in Frequency Order

| What they wrote | Symptom | What to say |
|---|---|---|
| Parent never closes `fd[1]` | Hangs at the last stage | Q2. Make them run `ps -o wchan` themselves |
| Child closes `fd[1]` *before* the `dup2` | "Bad file descriptor", or silence | "What order do the two calls have to be in?" |
| `close(in)` when `in == STDIN_FILENO` | First stage loses its stdin | The skeleton's `if (in != STDIN_FILENO)` guard is there for this |
| Only the last stage reaped | Zombies accumulate | `ps` shows them; W0 L02 §2 |
| `execvp` result checked with `if (execvp(...) < 0)` | Works, but misleading | Nothing after a successful exec runs; the `if` is noise |
| Redirecting stdout in the **last** stage | Output vanishes | The last stage inherits the terminal deliberately |
| Using `system()` or `popen()` | Passes `compare.sh` | **Not the lab.** Ask them to show you the `pipe()` call |

---

## Checkoff Standard

- [ ] `./compare.sh` printing **all checks passed**
- [ ] The Part C(a) hang reproduced, diagnosed with `ps -o wchan`, and fixed live
- [ ] Written answers to **Q2, Q3, Q5**

**A student who finishes early** should be sent to add `<` and `>` to their pipeline — which is PS 1 Q1, and the point where Lab 1 becomes Project 1.

---

*PROG 201 · Week 1 · Lab 1 Solutions · Instructor Only · © CSE Department*

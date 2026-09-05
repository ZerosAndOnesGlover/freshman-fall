# PROG 201 · Problem Set 0
## Processes, Waiting, and Signals

---

**Released:** Week 0, Wednesday · **Due:** Week 1, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS0_{LastName}_{StudentID}.pdf`, plus your `.c` files in a tarball `PS0_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.
>
> **Q1 and Q2 are to be answered by hand first.** Write your prediction down, then run it, then
> report both — a wrong prediction honestly reported and explained is worth full marks; a right
> answer with no prediction is worth half. **Q3, Q4 and Q5 require output from your own machine**,
> and marks there depend on you having run it. State your `gcc --version` and `uname -r`.
>
> Every program you submit compiles clean under `gcc -Wall -Wextra -O2 -std=c11`. Warnings cost
> marks in this course from PS 0 onwards, because in systems code a warning is usually the bug.

---

### Q1: Reading `fork()` (20 points)

**(a) [4]** How many processes does this create, including the original? Draw the tree, labelling each node with which `fork()` call created it.

```c
int main(void) { fork(); fork(); fork(); printf("x\n"); return 0; }
```

**(b) [6]** Now move the `printf` to the front:

```c
int main(void) { printf("x\n"); fork(); fork(); fork(); return 0; }
```

Run it twice — `./q1b` to your terminal, and `./q1b | cat` to a pipe — and count the `x`s each time. **One of them prints eight.** Explain the difference in terms of what `fork()` copies and how `stdout` is buffered in each case, and give the one-line fix that makes them agree.

**(c) [4]** Predict the output of this, then run it. Explain the *order* you observed, and say whether that order is guaranteed:

```c
int main(void) {
    pid_t p = fork();
    printf("%d: fork returned %d\n", getpid(), p);
    return 0;
}
```

**(d) [6]** This is a real bug from a real code review. Say what it does, why, and how to fix it in one line:

```c
pid_t p = fork();
if (p == 0) {
    execv("/usr/bin/helper", argv);
}
waitpid(p, &status, 0);
log_result(status);
```

*(There are two defects. One is a missing check; the other only shows itself when `/usr/bin/helper` does not exist, and it is the more interesting of the two.)*

---

### Q2: The Status Word (18 points)

**(a) [6]** For each raw `status` value returned by `waitpid`, state how the child ended and what `WEXITSTATUS` or `WTERMSIG` gives. **Do this by hand**, from the bit layout, before you check it:

| Raw | How it ended | Value |
|---|---|---|
| `0x0000` | | |
| `0x0100` | | |
| `0xff00` | | |
| `0x0006` | | |
| `0x0086` | | |

**(b) [4]** A student writes `printf("child returned %d\n", WEXITSTATUS(status));` with no other check. Give a concrete scenario in which this prints a number that means nothing, and say what the number will be.

**(c) [4]** Explain why `exit(256)` and `exit(0)` are indistinguishable to the parent. What is the largest exit status a program can usefully return, and where in the encoding does the limit come from?

**(d) [4]** `$?` is 137 after a process is killed by `SIGKILL`. Where does 137 come from, and is the arithmetic done by the kernel or by the shell? Justify from the raw status value, not from memory.

---

### Q3: Zombies, Orphans, and the Process Table (22 points)

**(a) [6]** Write `zombies.c`: fork three children that exit immediately, sleep for two seconds without reaping, and print the output of `ps -o pid,ppid,stat,rss,vsz --ppid <your pid>`. Include the output. **Explain the `RSS` and `VSZ` columns** — say what a zombie is still holding and what it has already given back.

**(b) [5]** Reap them and show that `/proc/<pid>` is gone. Then explain, in two or three sentences, why the kernel cannot simply discard the exit status at `exit()` and skip the zombie state entirely.

**(c) [5]** Write `orphan.c`: a parent that forks and exits immediately, and a child that sleeps two seconds and then prints `getppid()`. **Report the PID you get and identify what process it is** (`ps -o pid,comm= -p <that pid>`, and `tr '\0' ' ' < /proc/<pid>/cmdline`).

APUE says an orphan is adopted by `init`, PID 1. **If your answer is not 1, explain the mechanism** that produced the number you got — one sentence and the name of the `prctl` flag involved is enough.

**(d) [6]** A server forks a worker per request and never reaps. `ulimit -u` on your machine is *N*.

- State your *N*.
- After how many requests does `fork()` start failing, and with what `errno`?
- **Which processes are affected when it does** — only the server, or more? Justify from what `RLIMIT_NPROC` is a limit *on*.
- Give the two ways to stop this happening, and say what the cheaper one costs you.

---

### Q4: Signals Do Not Queue (22 points)

**(a) [8]** Write `count.c`: install a handler for `SIGUSR1` with `sigaction`, **block it**, fork a child that sends *N* signals with `kill()`, wait for the child, then unblock and count how many times the handler ran.

Report your counts for *N* = 10, 1,000 and 20,000 in a table. **Then change `SIGUSR1` to `SIGRTMIN` and do it again.** Explain both columns, and explain any point at which the real-time column stops matching *N* — name the limit and give its value on your machine (`ulimit -i`).

**(b) [4]** Your `count.c` handler increments a counter. What must the counter's type and qualifiers be, and what does each of them buy you? Say specifically what `volatile` prevents the compiler from doing.

**(c) [6]** Here is a plausible `SIGCHLD` handler. It has **four** defects — one of them is a bug only under load, one corrupts an unrelated part of the program, and one is undefined behaviour that will usually appear to work. Name each, say what symptom it produces, and rewrite it:

```c
void on_sigchld(int sig)
{
    int status;
    pid_t p = waitpid(-1, &status, 0);
    printf("child %d exited with %d\n", p, WEXITSTATUS(status));
}
```

**(d) [4]** `write(2)` is async-signal-safe and `fwrite(3)` is not, although `fwrite` calls `write`. Explain the difference in one paragraph. Then explain why the fact that a `printf` in a handler *usually works* makes it a worse bug rather than a lesser one.

---

### Q5: What the `fork`/`exec` Split Costs and Buys (18 points)

**(a) [6]** Reproduce the measurement from L01 §5 on your own machine: time `fork()`+`_exit()`+`waitpid()` with the parent holding 1 MB, 64 MB, 256 MB and 1024 MB resident. Report a table and the per-megabyte cost.

**Copy-on-write means no page is copied.** Explain, then, what *is* being copied, and why the cost is proportional to the parent's resident size rather than constant.

**(b) [6]** Add `posix_spawn` and report the same table for launching `/bin/true`. At which parent size does the difference become larger than a factor of two, and what exactly is the saved work?

**(c) [6]** A shell must, between the fork and the exec, be able to: redirect three descriptors, set the child's process group, reset the signal mask, and change directory — arbitrary combinations, chosen at runtime by the user's command line.

Argue in one paragraph whether that is achievable with a single `spawn`-style call, and what the API would have to look like if it were. Then say which of the two designs — `fork`+`exec`, or a parameterised `spawn` — you would choose for a language runtime that must also work on Windows, and why. **There is no expected answer here; the marks are for the argument.**

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Reading `fork()` | 20 |
| 2 | The status word | 18 |
| 3 | Zombies, orphans, the process table | 22 |
| 4 | Signals do not queue | 22 |
| 5 | What the split costs and buys | 18 |
| | **Total** | **100** |

**Late work:** `COURSE POLICIES.md` applies. **The lowest problem set of the term is dropped**, which is there for the week you are ill, not for the week you forgot.

---

*PROG 201 · Week 0 · PS 0 · © CSE Department*

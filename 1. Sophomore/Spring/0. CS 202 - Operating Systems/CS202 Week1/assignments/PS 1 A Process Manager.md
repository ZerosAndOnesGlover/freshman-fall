# CS 202 · Problem Set 1
## A Process Manager, and What It Can See

---

**Released:** Week 1, Wednesday · **Due:** Week 2, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS1_{LastName}_{StudentID}.pdf`, plus your `.c` files in a tarball `PS1_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.
>
> **Every measured answer requires output from your own machine.** State your CPU model,
> `uname -r` and `gcc --version` at the top. Where a question says **predict first**, write the
> prediction down before running anything, and report both.
>
> Every program you submit compiles clean under `gcc -O2 -Wall -Wextra`.

**Files provided** in `assignments/ps1/`:

| File | What it is |
|---|---|
| `worker.c` | A program for your manager to manage: `hog`, `tick`, `mem <MiB>`, `exit <n>`, `crash` |
| `test.pm` | A test script. Your manager must run it unchanged: `./pm < test.pm` |

---

### Q1: `pm`, a User-Space Process Manager (40 points)

Write `pm.c`. It reads **one command per line from standard input**, echoes each command it runs, and manages a table of up to 32 named jobs.

| Command | Behaviour |
|---|---|
| `start <name> <program> [args…]` | `fork` and `exec` the program; remember it under `<name>`; print its PID |
| `list` | one line per job — see below |
| `stop <name>` | send `SIGSTOP` |
| `cont <name>` | send `SIGCONT` |
| `kill <name>` | send `SIGTERM`; if the job has not exited within one second, `SIGKILL` it. **Either way, reap it** |
| `sleep <seconds>` | pause — so scripts can let time pass |
| `wait` | wait for every job that has not been reaped, and report how each ended |
| `quit` | `SIGKILL` every job still alive, reap them all, exit |

**`list` prints, for every job:**

| Column | For a live job — read from `/proc/<pid>/` | For a reaped job |
|---|---|---|
| name, PID | from your table | from your table |
| **state** | field 3 of `stat` | `-` |
| **CPU seconds** | (`utime` + `stime`) from `stat`, divided by `sysconf(_SC_CLK_TCK)` | from the `struct rusage` that `wait4` returned |
| **RSS in kB** | `VmRSS` from `status`, or `-` if absent | `-` |
| **voluntary / involuntary switches** | the two `ctxt_switches` lines of `status` | from `wait4`'s `rusage` |
| **how it ended** | blank — or `(zombie)` if the state is `Z` | `exited N`, or `killed SIG…`, with `(core)` if a core was dumped |

**The zombie rule, which is the point of the question:** `list` must **display a job that has exited but not been reaped as a zombie**, from its `/proc` entry — and only *then* reap it. So a job that exits between two `list` commands appears once as `Z` and from the next `list` on as `exited N`.

**Requirements:**

- **Parse `stat` from the last `)`** (L04 §3). A job named `a) b` must not break your parser.
- **`fflush(stdout)` before every `fork`** (PROG 201 L01 §6). Your test output must not contain duplicated lines.
- A program that does not exist must be reported as `exited 127`, not crash `pm`.
- **No zombie and no orphaned worker may survive `quit`.** After `./pm < test.pm`, `pgrep -x worker` must print nothing.
- You may not call `system`, `popen`, or run `ps`. Everything comes from `/proc` and `wait4`.

**Submit:** `pm.c`, and the complete output of `./pm < test.pm`.

**Marking:** 10 for `start` and `quit`; 12 for `list` from `/proc`, including the parser; 8 for the zombie rule; 6 for `kill`'s escalation; 4 for clean output with no duplicated lines and no survivors.

---

### Q2: Reading What the Kernel Counted (20 points)

`test.pm` starts `hog` and `tick` **pinned to the same CPU** with `taskset -c 5`, lets three seconds pass, lists, stops the hog, lets two more seconds pass, and lists again.

**(a) [6] Predict first.** Before running the script, predict for `hog` and for `tick` in the first `list`: the state, the CPU seconds to one decimal place, and which of the two switch counters will be large and which near zero. Then run it and report both.

**(b) [6]** Explain the switch counters. **Why is each process's pair so lopsided, and why in opposite directions?** Say which kind of switch a timer interrupt causes, and which kind `usleep` causes.

**(c) [4]** In the **second** `list`, after `stop hog`, `tick`'s voluntary count should have grown by roughly the same amount per second as before. **Did it?** Report the rate in both intervals. Then: did stopping the hog make any difference to `tick`? Should it have? *(Think about what `tick` spends its time doing.)*

**(d) [4]** `mem` asked for 64 MiB. Report its RSS. **Then change `worker.c`'s memory loop to a single `memset(p, 1, n)`, rebuild with `-O2`, and run the script again.** Report RSS again and explain it. *(Read the comment in `worker.c` only after you have a theory.)*

---

### Q3: The Cost of a Switch (15 points)

**(a) [6]** Run `ctxsw.c` from the Week 1 resources. Report its three lines. Then compute, from its own figures, **the per-switch cost on one CPU and on two**, and check it agrees with what the program printed.

**(b) [5]** The program estimates a switch by **subtracting** the time of an equivalent `write` + `read` in a single process. **State the assumption this makes**, and say whether violating it makes the estimate too high or too low. Suggest one change to the baseline that would make the assumption more nearly true.

**(c) [4]** On two CPUs, every switch was voluntary; on one CPU, about half were involuntary. **Explain both.** Which task preempts which on one CPU, and why does that not happen on two?

---

### Q4: xv6 and the FPU (15 points)

Build `fpu.c` into xv6 and **boot with one CPU**: `make qemu-nox CPUS=1`. Run `fpu` twice.

**(a) [5]** Report both processes' final values for both runs. **Add each pair.** Explain precisely what the sum tells you about where the variable `x` lived during the loop, and what the timer interrupt did to it.

**(b) [6] Design the fix.** Without writing the code, specify:

- **which fields** you would add to `struct proc`, and how large — look up the size of the area `fxsave` writes on the i386 target;
- **where in xv6** you would save the FPU state, and where you would restore it — name the function or file and say *before* or *after* which existing line;
- **what `fork` must do** with the new field, and why;
- **whether a newly created process needs any FPU state initialised**, and with what.

A design that saves in `swtch` and one that saves in `trap` are both defensible; **defend yours.**

**(c) [4]** Linux saves FPU state **eagerly** at every switch (L05 §6) and restores it only on return to user space. The curriculum describes the older **lazy** scheme, which saved nothing until a process first used the FPU and trapped. **Give one advantage lazy switching had**, and **one reason it was abandoned** — one of them must be about security.

---

### Q5: Who a Process Is (10 points)

**(a) [4]** `ls -l /usr/bin/passwd` and `getcap /usr/bin/ping`. Report both. Then run `ping -c 3 127.0.0.1` and, **while it runs**, read `CapPrm` and `CapEff` from its `/proc/<pid>/status`. Report them.

**(b) [6]** Both `passwd` and `ping` need privilege a normal user lacks. **Compare the two designs** — set-user-ID root, and a file capability followed by dropping it — in terms of **how much** privilege each grants, **for how long**, and **what a memory-corruption bug in each program could do** after its first second of running. Your answer must use the values you measured in (a).

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | `pm`, a user-space process manager | 40 |
| 2 | Reading what the kernel counted | 20 |
| 3 | The cost of a switch | 15 |
| 4 | xv6 and the FPU | 15 |
| 5 | Who a process is | 10 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of the term is dropped.**

---

*CS 202 · Week 1 · PS 1 · © CSE Department*

# CS 202 · Problem Set 12
## A Cage You Can Trust

---

**Released:** Week 12, Wednesday · **Due:** **Friday of the completion period, 17:00** · **100 marks**
**Skeleton:** `assignments/ps12/jail.c` and `assignments/ps12/victims.c`
**Submit:** `jail.c` and a report, `PS12_{LastName}_{StudentID}.pdf`

> **This is the last problem set.** It is due on the same day as Project 2, and the lowest problem
> set of the term is dropped — [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] and the Week 0
> syllabus both say so. **If you are short of time, Project 2 is worth 15% and this is worth a
> fraction of 30%. Do the arithmetic before you choose.**

---

## What You Are Building

**`jail` runs a program with less authority than you have.** It sets resource limits, installs a seccomp filter, execs the command, and reports how it ended.

```bash
./jail -t 5 -m 128 -f 32 -s strict ./untrusted
```

**Four TODOs in the skeleton.** None is long — the reference is about 180 lines including the filter. **The marks are for knowing why each piece is where it is, and for measuring what it does.**

---

## Question 1 — The Limits (25 marks)

**Implement `set_limits`** for `RLIMIT_AS`, `RLIMIT_NOFILE`, `RLIMIT_NPROC`, `RLIMIT_CORE` and `RLIMIT_CPU`.

**(a) [12]** Four limits, set only when the option was given, with `RLIMIT_CORE` always 0.

**(b) [5]** **`RLIMIT_CPU` is not like the others.** The kernel sends `SIGXCPU` at the soft limit and `SIGKILL` at the hard one. **Set them so the program receives the catchable signal**, and say in your report what a program would sensibly do in a `SIGXCPU` handler.

**(c) [8]** **Run `victims.c` under each limit and report the number**, not the fact:

| Run | Report |
|---|---|
| `./jail -t 1 ./victim spin` | which signal, and after how much CPU time |
| `./jail -m 64 ./victim grab` | **how many MiB `malloc` got before it failed** |
| `./jail -f 32 ./victim open` | **how many descriptors opened before `EMFILE`** |

**Two of those three numbers are not the number you asked for.** Explain both gaps. *(The reference measured 61 MiB for a 64 MiB limit and 29 descriptors for a limit of 32.)*

---

## Question 2 — The Filter (30 marks)

**(a) [8]** **Why must `PR_SET_NO_NEW_PRIVS` be set before the filter?** Give the concrete attack it prevents — name a program on this machine that would otherwise be the escape — and say what the kernel does if you omit it.

**(b) [14]** **Implement `install_filter`.** Check the architecture first, then compare the system call number against the allowlist, kill anything else with `SECCOMP_RET_KILL_PROCESS`.

> **The jump offsets are the whole exercise.** A `BPF_JUMP` skips *n* instructions from the one
> after itself when the comparison is true. **A filter with a wrong offset kills everything, which
> is indistinguishable at a distance from a filter that is working very well.** Test with `-s none`
> first, then with a filter whose allowlist is `SYS_write` only, and confirm you can make the
> difference visible.

**(c) [8]** **The allowlist in the skeleton is wrong**: a program run under `-s strict` dies before `main`. **Find the missing call by tracing**, add it, and report:

- **which call it is**, and what it is for;
- **why it appears in no program's source code**;
- **what that implies about writing a sandbox policy for a machine you have not tested on.**

Then show `./jail -s strict /bin/echo hi` printing `hi`, and `./jail -s strict ./victim socket` being killed.

---

## Question 3 — What It Costs (15 marks)

**Measure the cost of the filter, per system call.**

**(a) [10]** Time a cheap system call (`getppid` is the usual choice) **in one process**, before and after installing a filter. Report **ns per call** for: no filter, a short filter, a filter of **200-odd** instructions, and **five filters stacked**.

> **Your harness must include a control**: the same measurement twice with nothing changed between
> them, which must come out at approximately zero. **A submission without a control cannot score
> more than half of this question**, and the reason is in L38 §4 — the first version of the
> reference harness reported that a seccomp filter made system calls 17% *faster*.

**(b) [5]** **Two of your numbers should surprise you.** State what the cost does *not* depend on, and give the explanation. Then express the cost as a percentage of a system call on this machine, and say whether you would accept it for a network-facing service.

---

## Question 4 — The Limit That Does Not Limit (15 marks)

**Run `./jail -p 100 ./victim fork` and then `./jail -p 700 ./victim fork`.**

**(a) [5]** **Report what happens, and how many children were created in each case.**

**(b) [5]** **Explain it.** `ps -u "$(id -u)" --no-headers | wc -l` and the same with `-L` are the evidence. **What, exactly, is `RLIMIT_NPROC` counting?**

**(c) [5]** **Do the same job with a cgroup** — `pids.max` in a directory you create under `/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/` — and report the number of children. **State the general lesson about two mechanisms that appear to do the same job.**

---

## Question 5 — What It Does Not Do (15 marks)

**Your jail is now a real sandbox.** In **no more than one page**, give **four things a hostile program under `./jail -s strict` can still do**, each with evidence from this machine rather than assertion.

**One mark of the five per item is for the evidence.** Between them your four should cover: something about the files the program can still reach; something about a channel the filter cannot see; something in `/sys/devices/system/cpu/vulnerabilities/`; and something an unprivileged instruction still discloses. **L37 §6, L38 §8 and L39 §3 each hand you one.**

**Then answer the question the course has been circling for thirteen weeks:** *given that the list above is not empty, is the sandbox worth building?* **A defensible "yes" and a defensible "no" both earn full marks; an undefended one earns none.**

---

## What to Hand In

```bash
gcc -O2 -Wall -Wextra -o jail jail.c        # must compile without warnings
```

**Your report must contain every number the questions ask for**, and the commands that produced them. **A claim without its command is not a measurement.**

| Question | Topic | Marks |
|---|---|---:|
| 1 | The limits | 25 |
| 2 | The filter | 30 |
| 3 | What it costs | 15 |
| 4 | The limit that does not limit | 15 |
| 5 | What it does not do | 15 |
| | **Total** | **100** |

---

## Where to Look

| For | Read |
|---|---|
| the order — limits, `NO_NEW_PRIVS`, filter, `execve` | **L38 §8** |
| what `NO_NEW_PRIVS` prevents | **L38 §2** |
| the filter's shape, and `SIGSYS` | **L38 §4** |
| why the allowlist cannot be written from memory | **L38 §5** |
| rlimits against cgroups | **L38 §6** |
| a control that returns zero | **L38 §4**, and L39 §4 |
| what a sandbox does not cover | **L37 §6**, L38 §8, **L39 §3** |
| the manuals | `man 2 seccomp`, `man 2 setrlimit`, `man 7 capabilities`, `man 2 prctl` |

---

*CS 202 · Week 12 · PS 12 · © CSE Department*

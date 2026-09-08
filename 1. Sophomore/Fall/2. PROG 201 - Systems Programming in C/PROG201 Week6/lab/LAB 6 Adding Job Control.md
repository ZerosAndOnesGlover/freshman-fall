# PROG 201 · Lab 6
## Adding Job Control — `jobs`, `fg`, `bg`, and Ctrl-Z
### Covers Week 6 · sat **Monday of Week 7**, 15:00–16:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 6 and is sat in Week 7.** Lab *N* is sat on the Monday of Week *N+1*.
> Labs are back on Mondays from here — Lab 5 was the term's only Friday one, because the Monday of
> Week 6 was Fall Break.
>
> **Project 1 was assigned on the Friday of Week 6 and is due in Week 9.** It is a complete shell,
> and this lab is one of its five parts. Keep what you write today.
>
> **Unmarked.** The TA checks your work off in the session.

**What you are building:** the part of a shell that Ctrl-Z proves you do not have.

You are given a working shell — pipelines, redirection, background jobs, and a pipeline that is correctly one process group. It has no job table, no `jobs`, no `fg`, no `bg`, and it never gives the terminal to a job. **The first thing you will do is press Ctrl-Z and watch it hang**, and everything after that is fixing the reason.

---

## 0. Setup (5 minutes)

```bash
mkdir -p "$PROG201/week6/lab6"        # $PROG201 is set in ~/.bashrc -- see Lab 0
cd "$PROG201/week6/lab6"
cp "$ACADEMICS/1. Sophomore/Fall/2. PROG 201 - Systems Programming in C/PROG201 Week6/lab/"{tsh.c,groups.c,ttyctl.c,groupsig.c,Makefile} .

make
./tsh
```

The shell works:

```
tsh> ls /etc | wc -l
253
tsh> echo a b c > /tmp/x ; cat /tmp/x       # (no ';' -- run them separately)
tsh> sleep 5 &
[?] 1109468
```

The `[?]` is where a job number will go once you have a job table.

**`groups`, `ttyctl` and `groupsig` are the three experiments from L20**, provided complete. Part A runs them.

---

## 1. Part A — What the Shell Cannot See (20 min)

**(a)** Run the three experiments and keep their output. They must be run **on a terminal**; if you are in a pipe or a redirect, `/dev/tty` will not be what you expect.

```bash
./groups
./ttyctl
./groupsig
```

Three things to write down, because Q1–Q3 ask for them:

- from `groups`: what `setsid()` did to the last column, and what the two pipeline stages have in common;
- from `ttyctl`: which of `read`, `write` and `tcsetattr` a background group is allowed to do;
- from `groupsig`: what the minus sign did.

**(b)** Now the shell. Start a long foreground command and press **Ctrl-Z**:

```
tsh> sleep 30
^Z
```

**The shell hangs.** Nothing prints, the prompt does not come back, and Ctrl-C does not help. In another terminal:

```bash
ps -o pid,pgid,stat,comm -t $(tty | sed 's|/dev/||')
```

You will find `sleep` in state `T` — stopped — and your shell in `S`, waiting. **Both processes are behaving correctly.** Q2 asks you to say what is missing, and it is one flag.

Kill it (`kill %1` from the other shell, or `pkill tsh`) before moving on.

---

## 2. Part B — The Job Table and Seeing a Stop (35 min)

**TODO 1 — `job_add` and `job_by_pid`.** A free slot, the next id, the pgid, **every pid**, the process count, and a copy of the command line.

`job_by_pid` looks up by **pid, not pgid**, and TODO 2 is where that matters. L21 §5 explains it; if you would rather find out for yourself, write `job_by_pgid` instead and come back when `jobs` will not stop listing a job you killed.

**TODO 2 — `reap`.** Replace the placeholder. The `waitpid` needs `WUNTRACED | WCONTINUED`, and the three cases are `WIFSTOPPED`, `WIFCONTINUED`, and everything else.

Two details that are easy to miss:

- **A job is done when its *last* process ends**, not its first. `sleep 5 | cat` is two processes and one job.
- **Do not print `Done` for the job you are waiting for.** `ls` finishing in the foreground is not an event; `sleep 5 &` finishing is.

Now Ctrl-Z should report:

```
tsh> sleep 30
^Z
[1]+  Stopped                sleep 30
tsh>
```

**The prompt comes back.** The job is still stopped and you cannot get it back yet — that is Part C.

**TODO 3 — `jobs`.** Walk the table and print. `+` marks the most recent job, `-` the one before it.

```
tsh> sleep 30 &
[1] 1109468
tsh> sleep 40
^Z
[2]+  Stopped                sleep 40
tsh> jobs
[1]-  Running                sleep 30 &
[2]+  Stopped                sleep 40
```

---

## 3. Part C — Handing Over the Terminal (30 min)

**TODO 5 — the two `tcsetpgrp` calls.** One in `run`, before waiting for a foreground job; one in `wait_foreground`, to take the terminal back afterwards. **Both need `SIGTTOU` ignored around them** (L20 §4), and `wait_foreground` also restores `shell_modes`.

Do this before TODO 4, because `fg` without it does not work and you will not be able to tell which of the two is wrong.

Check it with something that reads the terminal:

```
tsh> cat
hello
hello
^C
tsh>
```

**Before TODO 5, that `cat` is in the background**, so it gets `SIGTTIN` and stops the moment it reads — `ttyctl`'s first row, happening to your own shell. Afterwards it works, and Ctrl-C reaches `cat` and not the shell.

**TODO 4 — `fg` and `bg`.** They share everything except two lines. The ordering inside `fg` is the part to get right:

```
give the terminal to the job     <- BEFORE
send SIGCONT
wait for it
```

L21 §6 says why. With a job stopped by `SIGTTIN` — `cat &` — the wrong order looks like `fg` doing nothing at all, intermittently.

Then `kill %n`: `SIGTERM` to the group **and then `SIGCONT`**, because a stopped process cannot die until it runs.

The whole thing:

```
tsh> sleep 20 | cat | cat &
[1] 1109500
tsh> jobs
[1]+  Running                sleep 20 | cat | cat &
tsh> sleep 20 | cat
^C
tsh> echo still alive
still alive
tsh> kill %1
tsh> jobs
[1]+  Done                   sleep 20 | cat | cat &
```

---

## 4. Part D — Two Deliberate Breakages (15 min)

Each of these is a one-line change. Make it, observe, and put it back.

**(a)** In `fg`, move the `kill(-pgid, SIGCONT)` **before** the `tcsetpgrp`. Then:

```
tsh> cat &
[1]+  Stopped                cat &
tsh> fg
```

Run it several times. Q6.

**(b)** In `run`, delete the **parent's** `setpgid(k, pgid)`, leaving only the child's. Then run a foreground command in a loop and watch for one that ends up in the wrong group:

```
tsh> sleep 0.01
```

a hundred times, checking `getpgid`. Q7 — and the honest answer may be "I could not reproduce it", which is the point.

---

## 5. Questions

Answer in the answer sheet. Three or four sentences each unless stated.

**Q1.** From `groups`: `setsid()` changed three columns and one of them became −1. Say which, what it means, and give one program that wants exactly that.

**Q2.** In Part A(b) the shell hung and both processes were behaving correctly. Name the missing flag, say what `waitpid` does without it when a child stops, and say why the shell could not tell that anything had happened.

**Q3.** From `ttyctl`: a background process group may `write` to the terminal but may not `read` from it or call `tcsetattr`. Give the reason for each of the three, in one sentence each. *(They are three different reasons.)*

**Q4.** Your `job_by_pid` looks up by pid. Explain what goes wrong with `getpgid(p)` after `waitpid` has returned `p`, and give the general rule. Then name the bug from an earlier week that is the same class.

**Q5.** `jobs` prints a command line that your tokeniser has already chopped into NUL-terminated words. Where did the copy come from, and what would `jobs` print without it?

**Q6.** Report what Part D(a) did, over several runs. Explain why the order matters, and why the symptom is intermittent rather than deterministic.

**Q7.** Report Part D(b). If you could not reproduce a failure, say so — then explain what the race is, why it is hard to hit, and why every real shell calls `setpgid` in both processes anyway.

**Q8.** *(One sentence.)* Your shell ignores `SIGINT` and `SIGTSTP` and has no handler for either, yet Ctrl-C and Ctrl-Z both work. Say what actually delivers them.

---

## 6. Checkoff

Show the TA:

- [ ] Ctrl-Z on a foreground job, reported, then `fg` bringing it back.
- [ ] A three-stage background pipeline in `jobs` as **one** job, and `kill %1` clearing it.
- [ ] `cat` in the foreground reading from the terminal, and Ctrl-C reaching it rather than the shell.
- [ ] Your written answers to **Q2, Q4 and Q8**.

**If you finish early:** implement the "there are stopped jobs" warning on `exit`, then exit anyway and find out what happened to them (L20 §6). Then add `disown` and do it again.

**Take with you:** this is one of the five parts of **Project 1**, due Week 9. The other four are the parser, the executor, the redirections and the builtins — you have written all of them at least once. Week 7's filesystem is what `cd` and `>` are actually talking to.

---

*PROG 201 · Week 6 · Lab 6 · © CSE Department*

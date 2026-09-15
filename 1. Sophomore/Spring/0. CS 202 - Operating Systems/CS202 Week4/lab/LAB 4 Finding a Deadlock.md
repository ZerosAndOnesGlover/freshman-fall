# CS 202 · Lab 4
## Finding a Deadlock
### Week 4 · sat **Tuesday of Week 5**, 15:00–16:50, BH 210 · **unmarked, checked off in the session**

---

> **This lab covers Week 4** and is sat on the **Tuesday of Week 5**. Lab *N* is always sat in
> Week *N+1*.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.

**What you are doing:** making a program hang, and then proving — from evidence, not from reading the source — exactly which threads are waiting for which locks, held by whom. **Three ways**: from `/proc` with no debugger, from `gdb`, and by deliberately making the program unable to deadlock and measuring that it does not.

**The curriculum asks you to "detect it with gdb".** On BH 210 you can — but not by attaching to a running program. Part C finds out why, and what to do instead.

---

## 0. Setup (5 minutes)

```bash
W4="$ACADEMICS/1. Sophomore/Spring/0. CS 202 - Operating Systems/CS202 Week4"
mkdir -p "$CS202/week4/lab4" && cd "$CS202/week4/lab4"
cp "$W4/lab/abba.c" "$W4/resources/errchk.c" .
gcc -O0 -g -Wall -Wextra -pthread -o abba abba.c
gcc -O2 -Wall -Wextra -pthread -o errchk errchk.c
echo 'set debuginfod enabled off' >> ~/.gdbinit     # stops gdb asking a question on every start
```

**`abba.c` is compiled with `-O0 -g`** so that `gdb` can show source lines and variables. Read it before running it — it is 100 lines, and the watchdog at the bottom is the part you will lean on.

---

## 1. Part A — Make It Hang (15 min)

```bash
./abba 0
```

It prints `DEADLOCK after N rounds`, a line per thread from `/proc`, and the owners of both locks, then exits.

**Q1.** Run it twenty times with no work and twenty with `./abba 1000`, recording only the round count:

```bash
for i in $(seq 20); do ./abba 0 | head -1; done
for i in $(seq 20); do ./abba 1000 | head -1; done
```

**Report both sets and their medians.** Explain why holding the first lock for longer makes the deadlock come *sooner*. Did any run deadlock after **0** rounds? What had to happen for that?

---

## 2. Part B — Diagnose It Without a Debugger (25 min)

Look at one run's `/proc` lines again:

```
  task …: state R, wchan 0                syscall 0 0x4 …
  task …: state S, wchan futex_do_wait    syscall 202 0x…080 0x80 0x2 …
  task …: state S, wchan futex_do_wait    syscall 202 0x…040 0x80 0x2 …
  &A = 0x…040, &B = 0x…080
  A is owned by TID …, B by TID …
```

**Q2.** For **your** run, fill in this table from the output — not from the source:

| Task (TID) | State | Asleep in which system call? | Waiting on the futex at address | …which is lock | Owns lock |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

Then **draw the wait-for graph** (L13 §3) and circle the cycle. **Explain each of the three arguments** `0x…, 0x80, 0x2` of the `futex` call, using `man 2 futex` and L11 §3.

**Q3.** The first task is in state `R` and syscall 0. **What is it doing?** *(Read `main`.)* Why is this thread not part of the deadlock?

**Now do it from outside the program**, as you would for a process you did not write:

```bash
./abba 0 wait > /dev/null &
P=$!; sleep 3
for t in /proc/$P/task/*; do echo "$(basename $t): $(cut -d' ' -f3 $t/stat 2>/dev/null) $(cat $t/wchan) $(cut -d' ' -f1-4 $t/syscall)"; done
```

**Q4.** Does the outside view give you the same cycle? **What can it not tell you** that the program's own printout could? *(Where did the lock owners come from?)* Leave the process running for Part C.

---

## 3. Part C — Diagnose It with `gdb` (25 min)

**First, the way you cannot:**

```bash
gdb -q -p $P -batch -ex 'info threads'
cat /proc/sys/kernel/yama/ptrace_scope
kill $P
```

**Q5.** Report the error and the value of `ptrace_scope`. **Explain in two sentences** what the setting protects, and why attaching to your *own* running process is refused anyway.

**Now the way you can: start the program under `gdb`.**

```bash
gdb -q ./abba
(gdb) run 0
```

Wait for `DEADLOCK after …` — the watchdog prints it — then **press Ctrl-C** and:

```
(gdb) info threads
(gdb) thread apply all bt
(gdb) print A.__data.__owner
(gdb) print B.__data.__owner
```

**Q6.** From the backtraces, give for each worker thread: **its LWP number, the function and source line it is blocked at, and the lock it is waiting for.** Match the LWPs with the owner fields and write the cycle out in full. **Which one line of `abba.c` would you change to make this deadlock impossible**, and to what?

---

## 4. Part D — Make It Impossible, and Measure That (20 min)

Make the change you proposed in Q6: **both threads acquire A before B.** Then, since the program now never deadlocks, change the watchdog so that it runs for **30 seconds**, reports a deadlock only if a whole second passes with no progress, and otherwise prints the total rounds and **the slowest second's** rounds. Build and run it with both amounts of work.

**Q7.** Report both runs. **Which of L13 §2's four conditions did your one-line change remove?** Is thirty seconds without a deadlock a *proof* that there can be none? If not, what is — write the argument in three sentences.

**Finally, misuse a lock on purpose:**

```bash
./errchk
```

**Q8.** Report the three lines. **Would an error-checking mutex have caught `abba`'s deadlock?** Would a robust one? Say exactly what information each would need, and why a single mutex cannot have it.

---

## 5. Checkoff

Show the TA:

- [ ] Your Q2 table and wait-for graph, from your own run's `/proc` output.
- [ ] A `gdb` session stopped in the deadlock, with `thread apply all bt` on screen.
- [ ] Your fixed `abba` running thirty seconds without deadlock.
- [ ] Your written answers to **Q2, Q6 and Q7**.

**Take with you:** **PS 4** turns Part B's table into an algorithm — detection with several instances of each resource — and asks when it is worth running.

---

*CS 202 · Week 4 · Lab 4 · © CSE Department*

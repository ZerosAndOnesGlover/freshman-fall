# PROG 201 · Lab 0
## The Process Supervisor
### Week 0 · sat **Friday of Week 0**, 17:00–18:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 0** and is sat on the **Friday that closes the ten-day Week 0**, after all
> three of this week's lectures. From Lab 1 onwards this course's labs are on **Mondays and cover
> the previous week** — Lab *N* is sat on the Monday of Week *N+1*. There is **no lab in Week 1**.
>
> **17:00 is late, and it is late for a reason.** Three Year 2 courses hold their Week 0 lab on the
> same Friday — CS 211 at 14:00–15:50 in BH 220, CS 201 at 15:00–16:50 in BH 210 — and 17:00 is the
> first slot that clears both. It happens once; every other lab in this course is a Monday
> afternoon.
>
> **Nothing here is marked.** The TA checks your work off in the session. [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]]
> costs you a letter grade after a second unexcused absence, which is the only enforcement there is
> and the only one needed.

**What you are building:** the smallest useful piece of production infrastructure there is. `systemd`, `supervisord`, `runit`, Docker's `containerd-shim` and Kubernetes' `kubelet` all contain the program you are about to write: **something that starts children, notices when they die, and starts them again — unless they are dying so fast that restarting them is pointless.**

By the end of the session you will have hit, in your own code, the three bugs that make this problem interesting: the reaping loop that reaps once, the race between checking a flag and waiting for it, and the child that cannot be stopped because it inherited a mask.

---

## 0. Before You Start — the Toolchain (10 minutes)

BH 215 runs **Ubuntu 24.04, GCC 13.3.0, glibc 2.39**. On your own machine, check:

```bash
gcc --version | head -1        # 13.x is fine, 11+ is fine
man 2 fork | head -5           # if this fails: sudo apt install manpages-dev
strace true 2>&1 | tail -3     # if this fails: sudo apt install strace
```

**`manpages-dev` is the one people are missing.** Without it `man 2 fork` shows you the shell builtin's page or nothing at all, and section 2 is half of this course.

**Where you work.** Not your home directory — your coursework for this course goes in the Academic
Registry, alongside its answer sheets, at
`5. Academic Registry/4. Submissions/Year2 Sophomore/Fall/2. PROG 201/`. Name that path once, in
`~/.bashrc` (the registry's [[4. Submissions/README|README]] has the block for every course):

```bash
export ACADEMICS=~/"Documents/1. Academics/0. Computer Science and Engineering (B.Sc)"
export PROG201="$ACADEMICS/5. Academic Registry/4. Submissions/Year2 Sophomore/Fall/2. PROG 201"
```

Create the directory and, like every other course, make it a repository of its own — it is kept out
of the vault's git repo deliberately, so you commit PROG 201 from inside `$PROG201`:

```bash
mkdir -p "$PROG201"
cd "$PROG201"
git init
```

Now get this lab's files. The skeletons ship with the course material; copy them across and build:

```bash
mkdir -p "$PROG201/week0/lab0"
cd "$PROG201/week0/lab0"
cp "$ACADEMICS/1. Sophomore/Fall/2. PROG 201 - Systems Programming in C/PROG201 Week0/lab/"{flaky.c,supervisor.c,Makefile} .

make                           # builds supervisor and flaky
./flaky test ok                # should print a line and sit for 30 seconds
```

**Quote every `"$PROG201"`.** The path contains spaces; unquoted it splits into five arguments.

---

## 1. The Thing To Be Supervised

`flaky.c` is given, and it is the whole zoo of ways a child can fail:

| Mode | What it does | What a supervisor must do |
|---|---|---|
| `ok` | Runs 30 s, exits 0 | Nothing. It is working |
| `exit` | Runs 1 s, exits **1** | Restart it |
| `crash` | Dereferences `NULL` after 1 s → **SIGSEGV** | Restart it, and say *how* it died |
| `hang` | **Ignores SIGTERM** and loops forever | Escalate to SIGKILL at shutdown |
| `flap` | Exits 1 **immediately**, every time | Restart it a few times, then **give up** |

**`flap` is the one that matters.** A supervisor with no give-up rule and a child that dies instantly is an infinite loop that forks as fast as the kernel allows — and each of those forks costs a PID from a pool of 25,571 (L02 §6). The restart policy is not a nicety; it is what stops your supervisor from being the outage.

---

## 2. What To Build

`supervisor.c` has six TODOs. Work through them in order — each one is testable on its own.

```
./supervisor web:ok db:crash cache:flap
```

**Required behaviour:**

1. Start one `./flaky <name> <mode>` per argument.
2. When a child dies, **report how**: exited with status *n*, or killed by signal *n*.
3. Restart it — **unless** it has died more than **5 times in 10 seconds**, in which case log that you are giving up and leave it dead.
4. When every child is dead or given up on, exit.
5. On **SIGTERM or SIGINT**: `SIGTERM` all survivors, wait **2 seconds**, `SIGKILL` whatever is left, reap it, exit cleanly. **No orphans, no zombies.**

**Constraints that are the actual lab:**

- **Handlers set flags. That is all they do.** No `printf`, no `fork`, no restart logic inside a handler (L03 §5).
- **`sigaction`, never `signal`** (L03 §2).
- **Reap in a loop with `WNOHANG`** (L02 §4, L03 §3).
- **The main loop must block, not spin.** A `while (1) {}` that burns a core is not a solution, and neither is `sleep(1)` — measure the CPU your supervisor uses with `top` and be able to say why it is 0.0%.

---

## 3. Part A — Start and Reap (30 min)

Do TODOs 1–4 and the first half of 5. Test with one healthy child:

```bash
./supervisor web:ok
```

**Check:** in another terminal, `ps -o pid,ppid,stat,comm --ppid $(pgrep supervisor)` shows one `flaky` in state `S`. After 30 seconds it exits, your supervisor reports `exited, status 0`, restarts it, and the PID changes.

**Then break it deliberately.** Comment out the loop in your `reap()` so that it reaps exactly once per `SIGCHLD`, and run:

```bash
./supervisor a:exit b:exit c:exit
```

**Q1.** All three die at almost the same moment. How many does the one-shot version reap, and how many zombies does `ps` show? Explain the number using L03 §3. *(Write down what you predicted before running it, then what happened.)*

---

## 4. Part B — The Restart Policy (25 min)

```bash
make demo-crash          # ./supervisor a:crash b:flap
```

**Expected shape** — this is the reference solution's output, trimmed:

```
[sup] started a      pid 404302 (mode crash)
[sup] started b      pid 404303 (mode flap)
[sup] b      pid 404303 exited, status 1
[sup] started b      pid 404304 (mode flap)
   ... four more, in under a millisecond ...
[sup] b      crash-looped 5 times in 10s — giving up
[sup] a      pid 404302 killed by signal 11 (Segmentation fault), core
[sup] started a      pid 404310 (mode crash)
   ... a restarts every ~1.15 s ...
[sup] a      crash-looped 5 times in 10s — giving up
[sup] nothing left to supervise
```

**Q2.** `b` used up its five restarts in **under a millisecond**; `a` took about six seconds. Both hit the same limit. What would a *time-based* backoff (wait 100 ms, 200 ms, 400 ms … before each restart) change about the first case, and what would it cost in the second?

**Q3.** The reference prints `killed by signal 11 (Segmentation fault), core`. Which macro told it there was a core file, and where did that core actually go? *(`cat /proc/sys/kernel/core_pattern` — on Ubuntu the answer is usually "into `apport`, which threw it away".)*

---

## 5. Part C — Shutting Down, and the Bug That Is Waiting for You (35 min)

```bash
./supervisor ok:ok h:hang        # in one terminal
kill -TERM $(pgrep -x supervisor)   # in another
```

**Required:** `ok` dies on the `SIGTERM`, `h` ignores it and is `SIGKILL`ed two seconds later, and the supervisor exits with nothing left behind. Check with `pgrep -a flaky` — it must print nothing.

**When you first run this, the healthy child will very likely survive the SIGTERM as well**, and your supervisor will `SIGKILL` both. That is not `flaky` misbehaving.

> **The hint, and only the hint.** The children were forked from a process that had just blocked
> `SIGCHLD`, `SIGTERM` and `SIGINT`. Read L01 §7 again, specifically the sentence about what
> survives `exec`.

**Q4.** State the bug precisely: which call created it, why `exec` did not clear it, and what the one-line fix is. Then verify with `grep SigBlk /proc/<child pid>/status` before and after — the value is a hex bitmask, and `SIGTERM` is signal 15, so you are looking at bit 14.

**Q5.** Your shutdown sends `SIGTERM` to each child individually. A shell sends it to the whole **process group** instead (`kill(-pgid, SIGTERM)`). Name one thing the process-group version gets right that yours does not. *(Think about what `flaky` would do if it had forked children of its own.)*

---

## 6. Part D — Prove the Main Loop Does Not Spin (10 min)

```bash
./supervisor web:ok &
top -b -n 3 -p $(pgrep -x supervisor) | tail -3
```

**Q6.** Report the `%CPU` figure. If it is not ~0.0, you are polling; find where. If it *is* 0.0, explain in one sentence what your process is doing between signals, and which state `ps -o stat` reports while it does it.

**Q7.** Now replace your wait with the broken version from L03 §7:

```c
while (!stop_now)
    pause();
```

Run `./supervisor web:ok`, and immediately `kill -TERM` it. Sometimes it exits; sometimes it hangs. **Explain the window.** Then put it back — and note that this is a bug you cannot find by testing, because the failing run looks exactly like the working one until it does not.

---

## 7. Checkoff

Show the TA:

- [ ] `./supervisor web:ok db:crash cache:flap` running, restarting `db`, and giving up on `cache`.
- [ ] `kill -TERM` producing a clean shutdown with `pgrep -a flaky` printing nothing afterwards.
- [ ] `top` showing ~0.0% CPU while idle.
- [ ] Your written answers to **Q1, Q4 and Q7** — three or four sentences each. These are the three that are actually about this week's lectures.

**Take with you:** everything in this lab reappears in **Week 6**, where the supervisor becomes a shell — the same `SIGCHLD` handler, the same `waitpid`/`WNOHANG` loop, plus process groups, terminal control and a parser. If your Lab 0 code is clean, Project 1 starts from it.

---

*PROG 201 · Week 0 · Lab 0 · © CSE Department*

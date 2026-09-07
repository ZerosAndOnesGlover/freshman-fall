# PROG 201 · Lab 3
## Priority Inversion, and What Actually Fixes It
### Covers Week 3 · sat **Monday of Week 4**, 15:00–16:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 3 and is sat in Week 4.** The lab is on Monday and this course's lectures
> are Tuesday to Thursday, so a lab can never be sat in the week it covers — Lab *N* is sat on the
> Monday of Week *N+1*. Every lab file states its own week; the file is authoritative.
>
> **Unmarked.** The TA checks your work off in the session.
>
> **Midterm 1 is the same day**, 18:00–19:30, covering Weeks 0–3 — this lab ends at 16:50 and the
> paper starts seventy minutes later. That is what the registry's calendar says and it is not a
> mistake in this file; [[PROG 201 Scheduling Notes]] records it. **Come to the lab having already
> revised.** This session is the last new material on the paper, and §5's questions are the shape
> its concurrency question takes.

**What you are building:** the bug that rebooted a spacecraft, and then the four-line fix that does not work.

In 1997 the Mars Pathfinder lander kept resetting itself because a low-priority task held a mutex that a high-priority task needed, and a medium-priority task kept preempting the low one. **You will reproduce that in about ninety lines and watch a half-second critical section turn into a hundred-second wait.** Then you will apply `PTHREAD_PRIO_INHERIT`, the documented fix, observe that every call succeeds and nothing changes, and work out why.

**Budget your time.** Every run in Part C takes about **a hundred seconds of wall clock**, including the ones where the reported wait is short — the program cannot exit until the starved thread finishes its work. Start each run, then read ahead while it goes.

---

## 0. Setup (5 minutes)

```bash
mkdir -p "$PROG201/week3/lab3"        # $PROG201 is set in ~/.bashrc -- see Lab 0
cd "$PROG201/week3/lab3"
cp "$ACADEMICS/1. Sophomore/Fall/2. PROG 201 - Systems Programming in C/PROG201 Week3/lab/"{inversion.c,rtcheck.c,Makefile} .

make
./inversion
```

The skeleton builds clean and does nothing useful yet:

```
calibration: 3000 work units take 0.487 s alone
no burners, L at nice 19, 1 chunk                high waited   -1.000 s
```

**That calibration line is the number everything else is measured against.** If yours is far from half a second, say so in your answers — every figure below will scale with it.

---

## 1. Part A — Find Out What This Machine Will Let You Do (10 min)

Before writing a line, run the diagnostic. It is provided complete; read it, then run it.

```bash
./rtcheck
```

Write down four things:

- your `RLIMIT_RTPRIO`,
- what `sched_setscheduler(SCHED_FIFO)` returned and why,
- whether `pthread_mutexattr_setprotocol(PTHREAD_PRIO_INHERIT)` **succeeded**,
- what the protocol reads back as.

**Two of those four will look like good news and one of them is a lie.** You will find out which in Part D. This is the week's habit, and it is the same one Week 2 ended on: *find the limit before you commit to the design.*

---

## 2. Part B — The Baseline (25 min)

**TODO 1 — `low`.** Pin, set nice to `low_nice`, then `chunks` times: take the lock, set `low_has_lock`, do `WORK_UNITS / chunks` of work, release the lock.

**TODO 2 — `high`.** Pin, set nice 0, spin on `sched_yield()` until `low_has_lock` is set, then time `pthread_mutex_lock` and store the elapsed time through `arg` (a `double *`).

> **Why the spin?** Without it, H may reach the mutex before L does, take it in zero time, and report a wait of nothing. The lab measures how long H waits *for L*, so L has to be in the critical section first. This is a measurement artefact, not a synchronisation technique — do not write `sched_yield` loops in real code.

```bash
./inversion
```

Expect the wait to be roughly the calibration figure. Ours:

```
calibration: 3000 work units take 0.495 s alone
no burners, L at nice 19, 1 chunk                high waited    0.495 s
```

**H waited exactly as long as L's critical section, and that is correct.** Nothing is wrong yet. A thread that wants a held lock waits for the holder; that is what a lock is. Note the number — it is the honest cost of the sharing, and Part C is everything on top of it.

---

## 3. Part C — The Inversion (25 min)

**TODO 3 — `medium`.** Pin, nice 0, and burn CPU in a loop until `stop` is set. It never touches the lock. Three of these are created.

```bash
./inversion m          # about 100 seconds.  Start it and keep reading.
```

Ours:

```
3 burners, L at nice 19, 1 chunk                 high waited  100.607 s
```

**Two hundred times the baseline.** While that runs, work out the arithmetic — you will need it for Q2.

Linux's CFS gives a thread CPU in proportion to a weight taken from its nice value. Nice 0 weighs **1,024**; nice 19 weighs **15**. On one CPU, with three nice-0 burners and one nice-19 lock holder, L gets

```
    15 / (15 + 3 x 1024)  =  0.49%  of the cpu
```

so a 0.49 s critical section takes 0.49 / 0.0049 ≈ 100 s. **Check that against your own two numbers.** If the prediction and the measurement agree, you have understood the mechanism rather than observed a symptom.

**And notice what H's priority bought it: nothing.** H is nice 0, the same as the burners. It is not losing a CPU race — it is asleep on a futex, and no amount of priority helps a thread that is not runnable.

---

## 4. Part D — The Fix That Does Not Work, and the Ones That Do (30 min)

**TODO 4.** In `main`, when `pi` is set, ask for `PTHREAD_PRIO_INHERIT` before `pthread_mutex_init`, and print `strerror(rc)` if the call fails.

```bash
./inversion m pi       # another 100 seconds
```

Ours:

```
3 burners, L at nice 19, 1 chunk                 high waited  100.607 s
3 burners + PRIO_INHERIT, L at nice 19, 1 chunk  high waited  100.392 s
```

**Nothing. And nothing told you so** — go back to your Part A notes: `setprotocol` returned 0, `pthread_mutex_init` returned 0, and the protocol reads back as `PRIO_INHERIT`. Q4 asks you to explain it, and Part A has the missing piece.

**TODO 5** is already done if you wrote TODO 1 as specified — the `chunks` loop. Now run the three fixes:

```bash
./inversion m nice0            # L at the same nice as the burners
./inversion m chunks=100       # a hundred short critical sections
./inversion m chunks=1000
./inversion m nice0 chunks=100
```

Ours. **Run each of the last three at least twice** — two of them are not stable, and the spread is Q6:

| configuration | H waited | vs the bug |
| --- | --- | --- |
| 3 burners, nice 19, 1 chunk | 100.607 s | — |
| 3 burners, nice 19, 1 chunk, **PRIO_INHERIT** | 100.392 s | **1.0×** |
| 3 burners, **nice 0**, 1 chunk | 1.946 / 1.947 / 1.941 s | 52× |
| 3 burners, nice 19, **100 chunks** | 0.534 / 0.487 / 0.899 s | ~170× |
| 3 burners, nice 19, **1000 chunks** | 0.403 / 0.261 / 1.681 s | ~200× |
| 3 burners, nice 0, 100 chunks | 0.012 / 0.012 / 0.015 s | ~7,500× |
| *no burners, for reference* | 0.489 / 0.495 / 0.488 s | |

**Two things in that table are strange.** One fix is reproducible to six milliseconds and another varies by a factor of six. And the fastest chunked runs are **below the baseline with no burners at all**. Q5 and Q6 are about both.

---

## 5. Questions

Answer in the answer sheet. Three or four sentences each unless stated.

**Q1.** In Part B, H waited about as long as L's whole critical section, and nothing was wrong. State, in one sentence, what a lock actually promises a waiter — and therefore what H is entitled to complain about and what it is not.

**Q2.** Give your calibration figure, your Part C figure, and the ratio. Then compute the CFS prediction from the weights in §3 and compare. If they disagree by more than about 20%, say what else was running on cpu 0.

**Q3.** H is nice 0 and so are the burners. Explain in two sentences why raising H's priority further — suppose you could — would not help it at all.

**Q4.** `PTHREAD_PRIO_INHERIT` was set, accepted, and read back correctly, and changed nothing. Explain why, using your Part A output. Your answer must name the thing that priority inheritance boosts and the reason this program has none of it.

**Q5.** Some chunked runs finish in **less time than the baseline with no burners at all**. Explain. *(Think about how many times H needs the lock, and when it becomes available.)*

**Q6.** The equal-priority fix reproduced to within 6 ms across three runs; the 1,000-chunk fix ranged from 0.261 s to 1.681 s. **Explain where the variance comes from**, in terms of what H is doing in each case — waiting, or racing. Then say which of the two you would rather have in a system with a deadline, and why the faster average is not automatically the answer.

**Q7.** A colleague proposes replacing the mutex with a `pthread_spinlock_t`, "so the high-priority thread does not have to sleep". Say what happens on a single CPU, in two sentences, and give the name for it.

**Q8.** *(One sentence.)* Everything in Part D was available before you wrote a line of Part C. Say what Part A would have told you about `PRIO_INHERIT` if you had read it as a prediction rather than as a formality.

---

## 6. Checkoff

Show the TA:

- [ ] `./inversion` and `./inversion m`, and the ratio between them said out loud.
- [ ] Your CFS arithmetic from Q2, on paper, next to the measurement.
- [ ] The `PRIO_INHERIT` run, and your explanation of why it did nothing.
- [ ] Your written answers to **Q4, Q6 and Q7**.

**If you finish early:** run `./inversion m` under `perf sched latency` or watch it live with `top -H -p $(pgrep inversion)` and find L in the thread list. Then set `chunks=10` and find the shortest critical section that still shows a visible inversion — that number is the practical meaning of "hold the lock briefly".

**Take with you:** this is the last new material on **Midterm 1**, which is tonight — Weeks 0–3, 18:00–19:30. The two things from this lab most likely to appear are Q4 — a mechanism that silently does nothing — and Q1's statement of what a lock actually promises.

---

*PROG 201 · Week 3 · Lab 3 · © CSE Department*

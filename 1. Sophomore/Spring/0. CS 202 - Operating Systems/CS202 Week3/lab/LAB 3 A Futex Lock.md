# CS 202 · Lab 3
## A Futex Lock
### Week 3 · sat **Tuesday of Week 4**, 15:00–16:50, BH 210 · **unmarked, checked off in the session**

---

> **This lab covers Week 3** and is sat on the **Tuesday of Week 4 — the day after Midterm 1.**
> Nothing in it is on the paper you sat last night; everything in it is on the final.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.

**What you are building:** the lock that `pthread_mutex_lock` is. Two versions of it, one that is correct and far too slow, and one that is correct and as fast as glibc's — and then a third, provided, that looks like a clever middle ground and hangs.

**By the end** you will have made a lock that takes fifty times fewer system calls than the obvious one, and you will be able to say exactly which single fact about `FUTEX_WAIT` makes that possible.

---

## 0. Setup (5 minutes)

```bash
W3="$ACADEMICS/1. Sophomore/Spring/0. CS 202 - Operating Systems/CS202 Week3"
mkdir -p "$CS202/week3/lab3" && cd "$CS202/week3/lab3"
cp "$W3/lab/flock.c" "$W3/resources/"{contend.c,locks.h} .
gcc -O2 -Wall -Wextra -pthread -o contend contend.c
gcc -O2 -Wall -Wextra -pthread -o flock flock.c
./flock eagain
```

`flock.c` contains three locks behind one interface — `lock()` and `unlock()` — selected on the command line. **One is complete (`buggy2`). Two have `TODO`s (`always2` and `drepper3`).** Read the whole file before you start; it is under 150 lines.

**Every measurement below reports two numbers: nanoseconds per lock-and-unlock, and how many `futex` system calls were made.** Always get the second from `strace -c`, never by assumption.

---

## 1. Part A — What glibc's Mutex Does (15 min)

```bash
strace -f -c -o one.txt ./contend mutex 1 4000000;  grep -E 'futex|total' one.txt
strace -f -c -o four.txt ./contend mutex 4 4000000; grep -E 'futex|total' four.txt
```

**Q1.** How many `futex` calls did four million uncontended lock–unlock pairs make? How many did the four-thread run make? **Express the second as a percentage of lock operations**, and say what that percentage tells you about where glibc's mutex spends its time.

---

## 2. Part B — The One Fact About `FUTEX_WAIT` (10 min)

`./flock eagain` stored 5 in the lock word and called `FUTEX_WAIT` saying *"sleep if the value is 7"*.

**Q2.** Report what it returned. Now read `man 2 futex` on `FUTEX_WAIT`. **Describe the lost wake-up that would happen if the kernel did not make this comparison** — which thread checks what, which thread releases the lock, and when the wake-up goes to nobody.

---

## 3. Part C — A Correct, Slow Lock (25 min)

Fill in `always2`'s `TODO`s: **two states** (0 free, 1 held). `lock()` loops exchanging 1 into the word and, if it was already 1, `FUTEX_WAIT`s expecting 1. `unlock()` stores 0 and **always** `FUTEX_WAKE`s one thread.

```bash
gcc -O2 -Wall -Wextra -pthread -o flock flock.c
taskset -c 3 ./flock uncontended always2 5000000
strace -c -o u.txt ./flock uncontended always2 1000000; grep futex u.txt
./flock contended always2 4 2000000
strace -f -c -o c.txt ./flock contended always2 4 2000000; grep futex c.txt
```

**Q3.** Report ns per round and `futex` calls, uncontended and contended. **Explain the uncontended figure from L03 §4's cost of a system call.** Is the lock correct? Is it usable?

---

## 4. Part D — Drepper's Three-State Lock (30 min)

Fill in `drepper3`'s `TODO`s: **0 free, 1 held with no waiters, 2 held and someone may be waiting** (L11 §3). Build and measure exactly as in Part C.

**Q4.** Tabulate Part C and Part D side by side: uncontended ns, uncontended `futex` calls, contended ns, contended `futex` calls. Then answer:

- **Why does a woken thread set the word to 2, not 1?** Give the case that breaks if it sets 1.
- **Your contended run's `strace` shows errors on some `futex` calls.** Which error, and why is it harmless?

**Checkpoint:** show the TA `drepper3` with **0** uncontended `futex` calls and a correct counter.

---

## 5. Part E — The Lock That Hangs (20 min)

`buggy2` is complete. It tries to avoid `always2`'s cost with only two states, by counting waiters in a plain `int` and waking only if the count is positive. **Read it, and predict before running whether it works.**

```bash
for i in 1 2 3 4 5; do timeout 60 ./flock contended buggy2 4 4000000; done
```

**Q5.** Report the five runs. **When it hangs, the program prints the lock's value and the waiter count.** Use them, and L10 §1, to explain **exactly** how threads come to be asleep forever with the lock free. Then say, in one sentence, **what Drepper's lock does with the information `buggy2` keeps in `waiters`.**

---

## 6. Checkoff

Show the TA:

- [ ] Your Part C / Part D table, with `drepper3` at 0 uncontended `futex` calls.
- [ ] One hung `buggy2` run, with its printed state.
- [ ] Your written answers to **Q2, Q4 and Q5** — three or four sentences each.

**Take with you:** **PS 3 Q1** builds a mutex from compare-and-swap without a futex, and asks what it must do instead of sleeping. The answer is not "spin".

---

*CS 202 · Week 3 · Lab 3 · © CSE Department*

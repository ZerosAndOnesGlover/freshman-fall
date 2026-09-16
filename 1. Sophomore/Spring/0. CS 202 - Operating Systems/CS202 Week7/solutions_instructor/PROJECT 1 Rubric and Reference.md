# CS 202 · Project 1 — Rubric, Reference and Marking Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Assigned Week 7 Wednesday; checkpoint in the Week 9 lab; due Friday of Week 11, 17:00. 15% of the course.**

**The reference implementation** is `solutions_instructor/lottery scheduler reference (do not distribute).patch` — 117 added lines across eight files, plus `assignments/pstat.h` (given to students) and a test program. **It was verified by applying it to a clean clone of the pinned commit with Lab 0's two `Makefile` changes, building, and running.** Apply it the same way when marking:

```bash
git clone https://github.com/mit-pdos/xv6-public.git check && cd check
git checkout eeb7b415dbcb12cc362d0783e41c3d1f44066b17
sed -i 's/-m32 -Werror/-m32 -Werror -Wno-error=array-bounds -Wno-error=infinite-recursion/' Makefile
sed -i 's/-smp $(CPUS)/-smp $(CPUS),sockets=$(CPUS),cores=1,threads=1/' Makefile
git apply STUDENT.patch && make qemu-nox CPUS=1
```

---

## The reference, in brief

**`proc.h`** gains two fields per process:

```c
  int tickets;                 // Lottery tickets (Project 1)
  int sched_ticks;             // Timer ticks this process has been run for
```

**`allocproc`** sets `tickets = 1` and `sched_ticks = 0`, so **every existing xv6 program keeps working and every process starts with an equal share.** *(Ticket inheritance then falls out of `fork`'s `*np = *p`-style copying only if the student copies the field explicitly — check for it: a child that resets to 1 is a marked-down Part A, not a failure.)*

**`scheduler()`** — the whole of Part B:

```c
    acquire(&ptable.lock);
    int total = 0;
    for(p = ptable.proc; p < &ptable.proc[NPROC]; p++)
      if(p->state == RUNNABLE)
        total += p->tickets;

    if(total > 0){
      int winner = nextrand() % total;
      int seen = 0;
      for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
        if(p->state != RUNNABLE)
          continue;
        seen += p->tickets;
        if(seen > winner){
          p->sched_ticks++;
          c->proc = p;
          switchuvm(p);
          p->state = RUNNING;
          swtch(&(c->scheduler), p->context);
          switchkvm();
          c->proc = 0;
          break;
        }
      }
    }
    release(&ptable.lock);
```

**Both the counting and the choosing happen under one acquisition of `ptable.lock`** — which is Part C's first question — and a three-line xorshift supplies the draw.

**`settickets` and `getpinfo`** live in `proc.c` (they need `ptable.lock`), with thin `sys_` wrappers in `sysproc.c`; `getpinfo` uses **`argptr`**, which is what makes a bad pointer return −1 instead of panicking the kernel.

---

## Reference measurements

**`lotto`** forks three children with 1, 2 and 4 tickets that spin until killed, sleeps a fixed number of ticks, then reports `getpinfo`.

**One CPU, 300-tick window, two runs:**

```
tickets 1: chosen 38 times, 12% of 302        tickets 1: chosen 44 times, 14% of 310
tickets 2: chosen 97 times, 32% of 302        tickets 2: chosen 97 times, 31% of 310
tickets 4: chosen 167 times, 55% of 302       tickets 4: chosen 169 times, 54% of 310
```

**Ideal is 14.3 / 28.6 / 57.1.** The reference lands within about two points, with run-to-run variation of a similar size — **which is what a student's correct implementation should look like.**

**Two CPUs, same program:**

```
tickets 1: chosen 124 times, 20% of 603
tickets 2: chosen 222 times, 36% of 603
tickets 4: chosen 257 times, 42% of 603
```

**Total selections roughly double** — two CPUs choosing — **and the 4-ticket process falls from 55% to 42%**, because with three runnable processes and two CPUs, **two of the three are running at any moment**: a single process cannot take more than about half of all selections however many tickets it holds. **Part D(b) is exactly this, and a student who reports it and explains it earns full marks even if their percentages differ.**

**`settickets(0)` returns −1**, as required.

---

## Marking

| Part | Item | Points | Look for |
|---|---|---:|---|
| **A** | `settickets` | 10 | validation of *n* < 1; the value visible in `getpinfo`; **inheritance across `fork`** |
| | `getpinfo` | 10 | **`argptr`** — a submission that dereferences the user pointer directly loses 5, even if it works |
| | `usertests` passes | 5 | run it; it takes about a minute |
| **B** | correct locked lottery | 25 | one lock acquisition covering total and choice; every `RUNNABLE` process reachable |
| | `ticks` accounting | 10 | incremented exactly where the switch happens |
| | xv6 still behaves | 10 | `usertests`, an interactive shell, `sleep 10` works |
| **C** | four written answers | 15 | 4 / 4 / 4 / 3 — see below |
| **D** | one CPU, two CPUs, overhead | 15 | 6 / 5 / 4 — **measurement and explanation, not a particular number** |

### Part C's answers

1. **`ptable.lock`.** Acquired in `scheduler` before counting; **released by the process that was switched to** — in `forkret` for a brand-new process, or after `sched()` returns in `yield`/`sleep`/`exit`. **The scheduler's own `release` runs only after control comes back through `swtch`.** A student who says "the scheduler releases it before switching" has not read `sched`.
2. **Releasing between the count and the choice:** another CPU can change the table in the gap — a process exits or blocks — so the total no longer matches the table being walked. **Concretely:** total counted as 7 with three runnable processes; the 4-ticket one exits; the draw returns 6; the walk sums 1 + 2 = 3 and **never crosses 6**, so no process is chosen and the scheduler spins with runnable work waiting. *(Or, in a version that falls back to "the last runnable process", the tickets are silently ignored.)*
3. **Unlocked `settickets`:** a torn or stale read of `p->tickets` — the sum can disagree with the values the walk sees, so `seen` may never reach `winner`, with the same result as (2). On x86 an aligned `int` write will not tear, so **accept "the ordering, not the tearing, is the problem"** as the better answer.
4. **`sti()` between iterations:** if no process is runnable, the scheduler loops forever with the lock released; **interrupts must be on or the timer that would wake a sleeping process never fires** — on one CPU, a machine with every process asleep would freeze permanently.

### Common failure modes

| Symptom | Cause | Marks |
|---|---|---|
| shell responds, `usertests` hangs at `sbrk` or `exec` | scheduler holds `ptable.lock` across `swtch` incorrectly — usually a second `acquire` | B: at most 10 |
| every process gets an equal share | `total` computed but the walk picks the first `RUNNABLE` | B: at most 15 |
| shares roughly right, `ticks` all zero | accounting outside the `if` that switches | −10 |
| `getpinfo` panics the kernel | user pointer dereferenced without `argptr` | A: −5, and note it in feedback |
| patch does not apply | wrong base, or new files not added | **A and B score 0** — the handout says so, and gives the check command |
| perfect 14.3 / 28.6 / 57.1 | almost certainly computed, not measured | ask for the raw `getpinfo` output; D at most half |

---

## Checkpoint (Week 9 lab)

**Show the TA:** `settickets(2)` followed by `getpinfo` printing 2 for that process, and `getpinfo(0)` returning −1. **Record who has it working** — students who miss this checkpoint are the ones who hand in nothing in Week 11, and a five-minute conversation in Week 9 is worth more than a reminder in Week 10.

---

*CS 202 · Week 7 · Project 1 Rubric · Instructor Only*

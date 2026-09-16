# CS 202 · Project 1
## xv6 Kernel Features: System Calls, a Scheduler, and the Locks They Need

---

**Assigned:** Week 7, Wednesday · **Due:** **Friday of Week 11, 17:00** · **15% of the course**
**Checkpoint:** Part A demonstrated in the **Week 9 lab session** — unmarked, but the TA records it
**Submit:** a patch against the pinned xv6 (`git diff` — see *What to hand in*), plus a report, `P1_{LastName}_{StudentID}.pdf`

> Collaboration: the kernel code and the report must be yours. **Discussing designs is fine; sharing
> code is not.** State at the top of your report: *"I worked on this project independently"* or name
> who you discussed what with. **Kernel code is easy to fingerprint**, and a lottery scheduler has
> few natural shapes.

---

## What You Are Building

**A scheduler you can steer from user space, and the interfaces to steer and observe it.** By the end:

- `settickets(int n)` — a process asks for a share of the CPU.
- `getpinfo(struct pstat *)` — a program reads the whole process table's scheduling state.
- **A lottery scheduler** in the kernel that gives a process CPU time in proportion to its tickets.
- **A report** that measures whether it does.

**Everything runs in the xv6 you have used since Lab 0** — the pinned commit, with Lab 0's two `Makefile` changes and nothing else.

---

## Part A — Two System Calls (25 points)

**`settickets(int n)`** sets the calling process's ticket count.

- **Returns 0** on success and **−1** if *n* < 1.
- The count is **inherited by children** — a `fork`ed child starts with its parent's tickets. *(Think about where in `proc.c` that has to happen, and what a new process's default must be so that nothing already in xv6 changes behaviour.)*

**`getpinfo(struct pstat *ps)`** fills in, for **every slot** of the process table:

```c
struct pstat {
  int inuse[NPROC];    // whether this slot is in use
  int pid[NPROC];      // the process's id
  int tickets[NPROC];  // how many tickets it holds
  int ticks[NPROC];    // how many times the scheduler has chosen it
};
```

`assignments/pstat.h` is provided — **use it unchanged**, in both the kernel and user programs.

- **Returns 0** on success and **−1** if the pointer is not a valid user address. **Use xv6's own argument-fetching machinery** (`argptr`) — do not dereference a user pointer directly. *(Week 0 §L02 and L18 §2: a system call that trusts a user pointer is a kernel bug.)*

**Marks:** 10 for `settickets` including inheritance and validation; 10 for `getpinfo` including the pointer check; **5 for a `usertests` run that still passes** (`make qemu-nox`, then `usertests`).

---

## Part B — The Lottery Scheduler (45 points)

Replace xv6's round-robin `scheduler()` with a **lottery**:

1. **Count the tickets of every `RUNNABLE` process.**
2. **Draw a random number** below that total. *(Write your own generator in the kernel — xv6 has none. A three-line xorshift is enough; say in your report why the quality of the generator does not matter much here, and what would make it matter.)*
3. **Walk the table, adding up tickets, and run the process that crosses the drawn number.**
4. **Count the choice** in that process's `ticks` field.

**Requirements:**

- **The count and the choice must see the same table.** Say in your report what can go wrong if the total is computed under the lock, the lock is released, and the winner is then chosen.
- **A process with more tickets must not be able to starve the others**: every `RUNNABLE` process must remain reachable by some draw.
- **xv6 must still work**: `usertests` passes, the shell is responsive, `sleep` and `wait` behave.
- **Do not change the timer or `yield`.** The scheduler decides *which* process runs, not for how long.

**Marks:** 25 for a correct, locked lottery; 10 for `ticks` accounting that matches what the scheduler did; 10 for `usertests` and interactive behaviour.

---

## Part C — The Locking (15 points)

**In your report**, answer with reference to your own code:

1. **Which lock protects the process table, and where is it acquired and released** in your scheduler? Follow one context switch from your `swtch` call to the point where the lock is released, and say **which code releases it** — it is not the scheduler.
2. **What breaks** if you compute the ticket total, release the lock, then draw and choose? Give a concrete interleaving with two CPUs.
3. **What breaks** if `settickets` writes `p->tickets` without the lock while the scheduler is summing?
4. xv6's scheduler runs with **interrupts enabled between iterations** (`sti()`). **Why is that necessary**, and what would happen on a single-CPU machine without it? *(L10 §6.)*

**Marks:** 4, 4, 4, 3.

---

## Part D — Does It Work? (15 points)

**Measure your scheduler.** Write a user program that forks three children with **1, 2 and 4 tickets**, has them spin, and after a fixed interval calls `getpinfo` and reports how often each was chosen — as counts **and as percentages of the three**.

**(a)** Run it on **one CPU** (`make qemu-nox CPUS=1`), at least twice. **Tabulate your results against the ideal shares** — 1/7, 2/7 and 4/7, i.e. 14.3%, 28.6%, 57.1%. **How close is it, and does it get closer with a longer interval?** Explain why a short run is not proportional even with a perfect lottery.

**(b)** Run the same program on **two CPUs**. **The shares change. Report them and explain why** — in particular, why the 4-ticket process cannot reach 57% however many tickets it holds. *(How many processes can run at once, and how many does one process need?)*

**(c)** **One measurement of overhead**: time something that involves many scheduling decisions — for example, the wall-clock time of your spinning program for a fixed number of iterations, or `usertests` — under your scheduler and under the original round robin. **Report both, say whether the difference is measurable**, and account for where the extra work is.

**Marks:** 6 for (a), 5 for (b), 4 for (c). **Marks are for measurement and explanation, not for a particular number** — an honest "my shares were 10/30/60 and here is why" earns full marks; an unexplained perfect table earns half.

---

## What to Hand In

```bash
cd ~/xv6-public                       # your working tree, from Lab 0
git diff > P1_{LastName}.patch        # every kernel change
```

**Also include** any new files (`pstat.h` is provided; your test program is not) in the patch — `git add -N` them first so `git diff` sees them.

**Your report** (PDF, 4–8 pages) contains Part C's four answers, Part D's tables and explanations, and **one paragraph on what you would do differently** — a design you rejected, a bug that took the longest, or a measurement that surprised you.

**The TA will apply your patch to a clean pinned xv6**, build it, run `usertests`, and run your Part D program. **A patch that does not apply or does not build scores zero for Parts A and B**, so check it:

```bash
git clone https://github.com/mit-pdos/xv6-public.git /tmp/check && cd /tmp/check
git checkout eeb7b415dbcb12cc362d0783e41c3d1f44066b17
sed -i 's/-m32 -Werror/-m32 -Werror -Wno-error=array-bounds -Wno-error=infinite-recursion/' Makefile
sed -i 's/-smp $(CPUS)/-smp $(CPUS),sockets=$(CPUS),cores=1,threads=1/' Makefile
git apply ~/P1_{LastName}.patch && make qemu-nox CPUS=1
```

---

## Milestones

| When | What |
|---|---|
| **Week 9 lab** | **Checkpoint: Part A works.** `settickets` and `getpinfo` compile, run, and validate their arguments. Show the TA |
| Week 10 | Part B running; `usertests` passing |
| **Week 11, Friday 17:00** | Everything, with the report |

**Start Part A in the week it is assigned.** Parts A and C are a few hours; **Part B is where the time goes**, and it is the part that breaks `usertests` in ways that take an evening to find.

---

## Marks

| Part | Topic | Points |
|---|---|---:|
| A | `settickets` and `getpinfo` | 25 |
| B | The lottery scheduler | 45 |
| C | The locking, explained | 15 |
| D | Measurement and explanation | 15 |
| | **Total** | **100** *(15% of the course)* |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies to projects as to problem sets. **There is no dropped project.**

---

## Where to Look

| For | Read |
|---|---|
| how a system call is added, end to end | **Week 0 L03**; `syscall.c`, `sysproc.c`, `usys.S` |
| copying a struct out to a user pointer | `argptr` in `syscall.c`; **L18 §2** on why |
| what the scheduler does now | **Week 2 L07**; `scheduler()` and `sched()` in `proc.c` |
| who releases `ptable.lock` after a switch | **Week 2 L06**; `forkret` and `sched` |
| why the table needs a lock at all | **Week 3 L10** |
| lottery scheduling as an idea | **OSTEP Ch. 9** |

---

*CS 202 · Week 7 · Project 1 · © CSE Department*

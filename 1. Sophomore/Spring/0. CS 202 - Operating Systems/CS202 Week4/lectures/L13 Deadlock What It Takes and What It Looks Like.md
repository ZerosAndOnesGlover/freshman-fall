# CS 202 · Operating Systems
## Week 4 · Lecture 1 of 3
### Deadlock: What It Takes, and What It Looks Like

---

**Sat:** Monday of Week 4, 09:00–09:50, VNC 101, **after Quiz 4** — and **Midterm 1 is this evening**, 18:00–19:15, VNC 100, on Weeks 0–3 · **Reading:** OSTEP Ch. 32 · **Next:** L14, prevention and the Banker's algorithm

> **Nothing in this week is on tonight's paper.** It covers Weeks 0–3. This lecture builds directly
> on Week 3, so it doubles as revision of locks — but if you are choosing between this and sleep,
> the paper does not need it.

---

## 1. A Deadlock, Measured

Week 3 met deadlock twice without naming it: five philosophers who each held one fork, and a bounded buffer whose threads were all asleep. **Here is the smallest one there is**: two threads, two locks, taken in opposite orders.

```c
/* thread one */                     /* thread two */
pthread_mutex_lock(&A);              pthread_mutex_lock(&B);
/* work */                           /* work */
pthread_mutex_lock(&B);              pthread_mutex_lock(&A);
/* ... */                            /* ... */
pthread_mutex_unlock(&B);            pthread_mutex_unlock(&A);
pthread_mutex_unlock(&A);            pthread_mutex_unlock(&B);
```

`abba.c` runs both in a loop and stops when no round has completed for a second. **Twenty runs, counting rounds before the deadlock**, on the reference machine:

| Work while holding the first lock | Rounds completed before deadlock, 20 runs |
|---|---|
| none | 400 274 336 32 **0** 687 424 433 216 658 143 531 507 523 110 331 357 30 437 959 |
| a 1,000-iteration loop | 18 631 **0** 15 13 2 16 **0** 4 2 1 4 16 12 16 7 11 12 4 1 |

**Every run deadlocked. The median is a few hundred rounds with no work, and about nine with a little.** Three runs deadlocked **before a single round completed**. Holding the first lock for longer widens the window in which the other thread can take the second, and the deadlock arrives sooner.

**The interleaving is simple**: thread one holds A and asks for B; thread two holds B and asks for A. **Each is waiting for something the other will release only after it gets what it is waiting for.** Neither can proceed, ever.

---

## 2. The Four Conditions

Coffman, Elphick and Shoshani showed in 1971 that a deadlock needs **all four** of these to hold at once:

| Condition | Means | In `abba.c` |
|---|---|---|
| **Mutual exclusion** | a resource can be held by only one thread at a time | a mutex, by definition |
| **Hold and wait** | a thread holds one resource while waiting for another | each thread holds its first lock while asking for its second |
| **No preemption** | a resource cannot be taken away; only its holder releases it | nothing takes a mutex from its owner |
| **Circular wait** | there is a cycle of threads, each waiting for a resource the next one holds | one waits for B held by two; two waits for A held by one |

**The value of the list is its converse: break any one condition and deadlock is impossible.** Week 3 already did it twice — ordering the philosophers' forks broke circular wait, and the waiter who handed out both forks at once broke hold-and-wait. **L14 is a systematic tour** of breaking each condition and what each costs.

---

## 3. Drawing It: the Resource-Allocation Graph

A **resource-allocation graph** has a node for every thread and every resource, and two kinds of edge:

- **request edge** `T → R`: thread *T* is waiting for resource *R*;
- **assignment edge** `R → T`: *R* is held by *T*.

`abba.c` at the moment it stops:

```
     ┌──────── holds ─────────┐
     │                        ▼
    [A]                    (one) ── wants ──▶ [B]
     ▲                                        │
     └─ wants ── (two) ◀─────── holds ────────┘
```

**Cycle: one → B → two → A → one.**

**With one instance of each resource — every mutex — a cycle in this graph *is* a deadlock**, and there is no deadlock without one. The graph can be collapsed to a **wait-for graph** with only threads as nodes: an edge *T*<sub>1</sub> → *T*<sub>2</sub> means "*T*<sub>1</sub> waits for something *T*<sub>2</sub> holds". Deadlock is then a cycle among threads.

**With several instances of a resource, a cycle is necessary but not sufficient.** Suppose there are two units of *R*<sub>1</sub>, held by *T*<sub>2</sub> and *T*<sub>4</sub>, and two units of *R*<sub>2</sub>, held by *T*<sub>1</sub> and *T*<sub>3</sub>. If *T*<sub>1</sub> wants *R*<sub>1</sub> and *T*<sub>3</sub> wants *R*<sub>2</sub>, the graph has a cycle *T*<sub>1</sub> → *R*<sub>1</sub> → *T*<sub>2</sub> → *R*<sub>2</sub> → *T*<sub>3</sub> → *R*<sub>1</sub>… **but if *T*<sub>4</sub> is not waiting for anything, it will finish and release its unit of *R*<sub>1</sub>, and *T*<sub>1</sub> can proceed.** Detecting deadlock with multiple instances needs an algorithm, not just a cycle — L15 gives it.

---

## 4. Seeing It from Outside: `/proc`

When `abba.c`'s watchdog fires, it reads each of its own threads' records from `/proc/self/task/<tid>/`:

```
  task 10561: state R, wchan 0                syscall 0 0x4 0x640f69b8d710 0x400 ...
  task 10562: state S, wchan futex_do_wait    syscall 202 0x640f5d48f080 0x80 0x2 ...
  task 10563: state S, wchan futex_do_wait    syscall 202 0x640f5d48f040 0x80 0x2 ...
  &A = 0x640f5d48f040, &B = 0x640f5d48f080
  A is owned by TID 10562, B by TID 10563
```

**Everything needed to draw §3's graph is here, without a debugger:**

| Field | Reads | Tells you |
|---|---|---|
| `state S` | `stat` | the thread is asleep, not spinning — a deadlock on sleeping locks burns no CPU |
| `wchan futex_do_wait` | `wchan` | **where in the kernel** it sleeps: in a futex wait |
| `syscall 202` | `syscall` | the system call it is inside — **202 is `futex`** on x86-64 |
| `0x640f5d48f080` | first argument | **the address of the futex word** — which is `&B` |
| `0x80` | second argument | `FUTEX_WAIT` with `FUTEX_PRIVATE_FLAG` |
| `0x2` | third argument | **"sleep if the value is 2"** — L11 §3's *locked, and someone may be waiting* |

**Task 10562 is asleep on B and owns A. Task 10563 is asleep on A and owns B.** That is the cycle, read from the kernel's own records. The owner fields come from glibc's `pthread_mutex_t`, which records the owning thread's ID in `__data.__owner` — an implementation detail, but a stable and very useful one.

> **`/proc` is how you diagnose a deadlock on a production machine** where you cannot restart the
> program under a debugger. `wchan` and `syscall` are readable for your own processes without any
> privilege, and every thread asleep in `futex` on an address owned by another asleep thread is a
> candidate for a cycle.

---

## 5. Seeing It from Inside: `gdb`

Run `abba` under `gdb`, and let the watchdog stop it with `SIGTRAP` when it deadlocks:

```
$ gdb -q -batch -ex run -ex 'info threads' -ex 'thread apply all bt 6' \
      -ex 'print A.__data.__owner' -ex 'print B.__data.__owner' --args ./abba 0 trap

  Id   Target Id                                Frame
* 1    Thread 0x7ffff7fa3740 (LWP 10819) "abba" __pthread_kill_implementation (...)
  2    Thread 0x7ffff7bff6c0 (LWP 10822) "abba" futex_wait (private=0, expected=2, futex_word=0x555555558080 <B>)
  3    Thread 0x7ffff73fe6c0 (LWP 10823) "abba" futex_wait (private=0, expected=2, futex_word=0x555555558040 <A>)

Thread 3 (LWP 10823):
#0  futex_wait (private=0, expected=2, futex_word=0x555555558040 <A>)
#1  __GI___lll_lock_wait (futex=futex@entry=0x555555558040 <A>, private=0)
#3  ___pthread_mutex_lock (mutex=0x555555558040 <A>)
#4  0x000055555555549a in two (arg=0x0) at abba.c:46

Thread 2 (LWP 10822):
#0  futex_wait (private=0, expected=2, futex_word=0x555555558080 <B>)
#3  ___pthread_mutex_lock (mutex=0x555555558080 <B>)
#4  0x000055555555541d in one (arg=0x0) at abba.c:32
$1 = 10822
$2 = 10823
```

**The debugger names what `/proc` gave as addresses.** Thread 2 (LWP 10822), in `one` at line 32, waits on `<B>`; thread 3 (LWP 10823), in `two` at line 46, waits on `<A>`; `A` is owned by 10822 and `B` by 10823. **The line numbers show which lock call in the source is part of the cycle** — which is the information you need to fix it.

**One restriction on the lab machines.** Attaching `gdb` to a program that is *already* running fails:

```
$ gdb -q -batch -p 10917 -ex 'info threads'
Could not attach to process.  If your uid matches the uid of the target
process, check the setting of /proc/sys/kernel/yama/ptrace_scope ...
```

**`kernel.yama.ptrace_scope` is 1**: a process may trace only its own descendants. Anyone could otherwise read the memory of every other program they own — a browser's, a password manager's. **So on these machines, start the program under `gdb`**, as above. Lab 4 does both, and uses `/proc` for the case where you cannot.

---

## 6. Deadlock Is Not the Only Way to Stop

Three different failures look alike from a distance — nothing gets done — and have different causes and different cures:

| | Threads are | Progress | Cure |
|---|---|---|---|
| **Deadlock** | **asleep**, each waiting on another in a cycle | **none, ever** | break a condition (L14), or detect and recover (L15) |
| **Livelock** | **running**, repeatedly backing off and retrying in step | **almost none**, while every CPU is busy | break the symmetry — L15 measures it |
| **Starvation** | some running and progressing; **one** waiting indefinitely | **for everyone else** | fairness — L12 §7's writer, L08 §3's boost |

**`abba.c`'s threads were in state `S`, burning no CPU.** A livelock shows the opposite signature: state `R`, 100% CPU, and a counter that barely moves. **The two are distinguishable from `/proc` in seconds**, and the distinction decides where to look.

---

## 7. What xv6 Does About It

**xv6 detects exactly one kind of deadlock**: a CPU trying to acquire a spinlock it already holds, which L10 §6 showed `acquire` turning into a panic. Add a second `acquire(&tickslock)` to `sys_uptime` in `sysproc.c`, and run a program that calls `uptime()`:

```
$ uptime
uptime: asking the kernel for the tick count
lapicid 0: panic: acquire
 80104692 8010582d 80104ab9 80105aad 8010585b 0 0 0 0 0
```

`addr2line -e kernel` turns the addresses into the call chain: **`acquire` ← `sys_uptime` ← `syscall` ← `trap` ← `alltraps`** — the system-call path from L03 §6, ending in the lock taken twice.

**A cycle between two different locks, on two CPUs, xv6 does not detect.** Both CPUs would spin in `acquire` forever with interrupts off, and the machine would simply stop. **xv6 relies on prevention instead** — on its authors taking locks in a consistent order — and records the rules as comments beside the code:

```c
// fs.c: "One must hold icache.lock while using any of those fields."
// fs.c: "Caller must hold ip->lock."
// ide.c: "You must hold idelock while manipulating queue."
// proc.c: "Enter scheduler.  Must hold only ptable.lock"
```

**A comment is a lock order that nothing checks.** Linux has a tool that checks it — L14 §2 — and it is not switched on in the kernel you are running.

---

## 8. What to Take Away

1. **Two threads taking two locks in opposite orders deadlocked in every run**, usually within a few hundred rounds; holding the first lock slightly longer brought it down to about nine.
2. **Deadlock needs mutual exclusion, hold-and-wait, no preemption and circular wait — all four.** Break one and it cannot happen.
3. **In a resource-allocation graph with single-instance resources, a cycle is a deadlock.** With several instances it is only a warning.
4. **`/proc/<pid>/task/*/` shows a deadlock without a debugger**: state `S`, `wchan` in `futex`, syscall 202 on the address of a mutex another sleeping thread owns.
5. **`gdb` names the locks and the source lines** — but on these machines it must start the program, because `ptrace_scope` is 1.
6. **Deadlock sleeps, livelock spins, starvation singles one out.** `/proc` tells them apart.
7. **xv6 panics on a lock taken twice by one CPU**, and prevents every other deadlock only by convention.

---

## Exercises

1. Run `abba.c` with work of 10, 100 and 10,000 iterations. Plot the median rounds before deadlock against the work. Is it inversely proportional? Why might it not be?
2. In §4's output, task 10561 is in state `R` and syscall 0. What is it doing, and why is it running rather than asleep?
3. Draw the resource-allocation graph for the five naive philosophers of L12 §6 at the moment they deadlock. How many cycles does it have?
4. Construct a three-thread, three-lock deadlock in which **no two threads** take the same pair of locks in opposite orders. Which of the four conditions does it satisfy that a two-lock check would miss?
5. xv6's `acquire` panics on a double acquire because it records `lk->cpu`. Why can it not also detect a two-lock cycle across CPUs the same way? What would it have to record, and when would it check?

---

*CS 202 · Week 4 · L13 · © CSE Department*

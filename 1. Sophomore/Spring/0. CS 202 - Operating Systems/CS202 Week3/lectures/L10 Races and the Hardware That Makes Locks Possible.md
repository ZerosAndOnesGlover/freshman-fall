# CS 202 · Operating Systems
## Week 3 · Lecture 1 of 3
### Races, and the Hardware That Makes Locks Possible

*“We shall occupy ourselves much more with the logical problems which arise, for example, when speed ratios are unknown, communication possibilities restricted etc.”* — Edsger W. Dijkstra, "Cooperating Sequential Processes" (EWD123, 1965)

---

**Sat:** Monday of Week 3, 09:00–09:50, VNC 101, **after Quiz 3** · **Reading:** OSTEP Ch. 26 and 28 · **Next:** L11, sleeping locks, futexes, and when to spin

**Coursework:** 📊 **Quiz 3** today · 🔬 **Lab 2** Tue this week 15:00–16:50 · 📝 **PS 3** released Wed this week, due Fri of Week 4 17:00 · 📝 **PS 2** due Fri this week 17:00 · 📘 **Midterm 1** Mon of Week 4 18:00–19:15

---

## 1. A Race, Measured

Two threads, one variable, ten million increments each. **No lock.** `race.c`, on the reference machine:

```
2 threads x 10000000: counter = 10011347, expected 20000000, lost 9988653 (49.9%)
4 threads x 10000000: counter = 10420162, expected 40000000, lost 29579838 (73.9%)
8 threads x 10000000: counter = 24937423, expected 80000000, lost 55062577 (68.8%)
```

**Half of all increments from two threads vanished.** Not a few — half. Nothing crashed, no error was reported, and the program's output is a plausible-looking number.

The reason is one line of C that is not one instruction. `counter++`, compiled with `-O2` and `counter` declared `volatile`:

```asm
mov    0x2cc1(%rip),%rax        # load counter into rax
add    $0x1,%rax                # add one
mov    %rax,0x2cb6(%rip)        # store it back
```

**Three instructions, and another thread can run between any two of them.** If thread A loads 41, thread B loads 41, both add one and both store 42, **two increments have produced one.** That interleaving is a **race condition**: the result depends on the timing of events nobody controls.

---

## 2. One CPU Does Not Save You

Put all the threads on one CPU with `taskset`, so that only one thread can ever run at a time:

```
2 threads x 10000000: counter = 12520809, expected 20000000, lost 7479191 (37.4%)
4 threads x 10000000: counter = 14037436, expected 40000000, lost 25962564 (64.9%)
8 threads x 10000000: counter = 17650867, expected 80000000, lost 62349133 (77.9%)
```

**Still over a third lost.** No two threads ever executed at the same instant — and that turns out not to matter. **Preemption is enough.** If the timer takes the CPU from thread A just after A has loaded the counter, thread B runs for a whole 3 ms slice (L08 §6) and adds a million; then A resumes and **stores its stale value plus one — erasing B's entire slice.** On one CPU a race loses less often, and each loss is enormous.

**And the race that passes every test:**

```
2 threads x 1000: counter = 2000, expected 2000, lost 0 (0.0%)
2 threads x 100000: counter = 111864, expected 200000, lost 88136 (44.1%)
```

**A thousand increments take less than a slice**, so the first thread finishes before the second starts and nothing is lost. Run the same code a hundred times longer and 44% disappears. **A test suite with small inputs would pass this program forever.**

---

## 3. What a Solution Must Guarantee

A **critical section** is a stretch of code that touches shared state and must not interleave with another stretch touching the same state. A correct way of protecting one — a **lock** — has to give three things:

| Property | Means | Without it |
|---|---|---|
| **Mutual exclusion** | at most one thread inside at a time | §1's lost updates |
| **Progress** | if nobody is inside and someone wants in, someone gets in | deadlock, livelock — Week 4 |
| **Bounded waiting** | a thread waiting to enter gets in eventually, after a bounded number of others | starvation — L12 §6 measures a writer waiting forever |

**And a fourth that is not about correctness at all: cost.** A lock is taken millions of times a second in a busy kernel. L11 measures what each kind costs, and the differences are a factor of forty.

---

## 4. The Obvious Solution, and Why It Is Not One

**On one CPU, a critical section cannot be interrupted if interrupts are off.** No timer interrupt means no preemption, which means no interleaving:

```c
cli();            /* disable interrupts */
counter++;
sti();            /* enable them again */
```

This is exactly how early single-CPU kernels protected their data, and it has three problems that each rule it out on its own:

1. **It is privileged.** L02 §3 measured `cli` killing a ring-3 process with `SIGSEGV`. User programs cannot use it — and if they could, a program that disabled interrupts and looped would own the machine.
2. **It does not work on more than one CPU.** Disabling interrupts on CPU 0 does nothing to stop a thread on CPU 1 from running the same three instructions at the same time.
3. **It loses interrupts.** A disk or network interrupt that arrives while they are off is delayed — and if they stay off long enough, lost.

**xv6 still disables interrupts inside the kernel — but for a different reason**, and alongside a real lock. §6 says why.

---

## 5. The Hardware Answer: Instructions That Cannot Be Split

**A lock needs one step that reads the old state and writes the new state with nothing in between** — not in software, where preemption can land anywhere, but in a single instruction that the CPU guarantees completes atomically, even with other CPUs watching the same memory. x86 has three:

| Primitive | Instruction | Does, atomically |
|---|---|---|
| **Test-and-set** | `xchg` with a memory operand | store a new value, return the old one |
| **Compare-and-swap** | `lock cmpxchg` | *if* memory equals `expected`, store `new`; say whether it did |
| **Fetch-and-add** | `lock xadd` | add to memory, return the old value |

**The `lock` prefix** is what makes `cmpxchg` and `xadd` atomic on a multi-processor: it tells the CPU to hold the memory exclusively for the length of the instruction. `xchg` with memory is atomic without it. The reference machine's compiler produced these from C11 `<stdatomic.h>`:

```
$ objdump -d lockcost | grep 'lock cmpxchg'
    1593:   lock cmpxchg %ecx,0x24(%rsp)
```

**Fetch-and-add alone is enough for a counter** — no lock at all:

| Uncontended, one thread | ns per increment |
|---|---:|
| `counter++`, no protection | **1.61** |
| `atomic_fetch_add` — one `lock xadd` | **5.41** |

**Atomic, and 3.4 times slower than the unprotected increment** — the price of an instruction that must coordinate with every other CPU's view of that memory.

---

## 6. A Spinlock, in Five Lines

**Test-and-set is enough to build a lock:**

```c
typedef struct { atomic_flag f; } tas_lock;

void tas_acquire(tas_lock *l)
{
    while (atomic_flag_test_and_set(&l->f))   /* set it; if it was already set, */
        cpu_relax();                           /* someone holds it: try again     */
}

void tas_release(tas_lock *l) { atomic_flag_clear(&l->f); }
```

**Mutual exclusion**: of all the threads that execute `test_and_set` while the flag is clear, exactly one sees *clear* returned — the atomic instruction guarantees it — and the rest see *set* and loop. **`cpu_relax()` is the `pause` instruction**, which tells the CPU the loop is waiting on another CPU, saving power and avoiding a costly misprediction on exit. The waiting thread **spins** — runs a tight loop — hence *spinlock*.

**xv6's spinlock is the same idea, and adds two things.** From `spinlock.c`:

```c
void
acquire(struct spinlock *lk)
{
  pushcli(); // disable interrupts to avoid deadlock.
  if(holding(lk))
    panic("acquire");

  // The xchg is atomic.
  while(xchg(&lk->locked, 1) != 0)
    ;
  ...
}
```

1. **`holding` → `panic`.** Acquiring a lock this CPU already holds would spin forever, waiting for itself. xv6 turns that silent hang into an immediate crash with a message — which is how you will find it in Project 1.
2. **`pushcli()` — interrupts off while any spinlock is held.** Suppose the kernel on CPU 0 holds the lock protecting the tick counter, and a timer interrupt arrives on CPU 0. The interrupt handler tries to acquire the same lock — **on the same CPU, which cannot release it until the handler returns.** Deadlock, on one CPU, with no other thread involved. **So xv6 disables interrupts before taking any spinlock, and restores them after releasing the last.** `pushcli` counts nesting, so taking three locks and releasing one does not turn interrupts back on.

**That is §4's technique returning — not as the lock, but as the protection against an interrupt handler meeting a lock its own CPU holds.**

---

## 7. Sharing Costs, Even With No Lock

Increment a counter 20 million times, split among threads, four ways:

| ns per increment | 1 thread | 2 threads | 4 threads | 8 threads |
|---|---:|---:|---:|---:|
| **one shared `counter++`, no lock** | 1.5 | 2.7 — **wrong** | 3.9 — **wrong** | 6.6 — **wrong** |
| **one shared `atomic_fetch_add`** | 7.4 | **29.2** | 32.1 | 31.3 |
| **a separate counter per thread**, summed at the end | 1.5 | 0.8 | 0.7 | **0.3** |

*(Time per increment is wall-clock time divided by all increments, so a perfectly parallel program shows the figure falling as threads are added.)*

**The per-thread counters scale perfectly** — eight threads, eight times the throughput. **The atomic counter is correct and gets four times *slower* going from one thread to two**, and adding more threads never recovers it. Every `lock xadd` writes to one memory location, and a write by one CPU invalidates every other CPU's cached copy of that cache line, which must then be fetched again before their next write. **The counter's cache line bounces between CPUs on every increment** — the false-sharing phenomenon CS 201 Week 10 measured, with the sharing now real.

> **The lesson under all of Week 3:** the fastest lock is not needing one. A per-CPU or
> per-thread counter summed occasionally is how the Linux kernel counts almost everything —
> packets, page faults, context switches. Locks are for state that genuinely must be shared.

---

## 8. What to Take Away

1. **`counter++` is three instructions**, and two threads lost 49.9% of their increments.
2. **One CPU is not safe**: preemption between load and store lost 37% — and each loss erased a whole slice of another thread's work.
3. **Races hide in small tests**: 1,000 increments lost nothing; 100,000 lost 44%.
4. **A lock must give mutual exclusion, progress and bounded waiting** — and be cheap.
5. **Disabling interrupts is privileged, single-CPU, and loses interrupts.** It is not a lock.
6. **Atomic instructions — `xchg`, `lock cmpxchg`, `lock xadd` — are what locks are built from.** A spinlock is test-and-set in a loop.
7. **xv6's `acquire` disables interrupts**, because an interrupt handler meeting a lock its own CPU holds is a deadlock with one thread.
8. **Sharing a cache line costs even without a lock**: an atomic counter got four times slower from one thread to two; per-thread counters scaled perfectly.

---

## Exercises

1. Compile `race.c` without `volatile` at `-O2` and run it with two threads. How many increments are lost now, and why? `objdump -d` the loop.
2. Rewrite `race.c`'s loop to use `atomic_fetch_add`. Verify it never loses an increment, and time it against the unprotected version.
3. In xv6's `acquire`, `pushcli()` comes *before* the `xchg` loop. What could go wrong if it came after?
4. xv6's `release` restores interrupts with `popcli()` only after clearing `locked`. Construct a sequence of events showing why the order matters.
5. `per-thread counters` scaled perfectly with the counters `padded` to 64 bytes each. Remove the padding and run it again. Explain the difference in terms of cache lines.

---

*CS 202 · Week 3 · L10 · © CSE Department*

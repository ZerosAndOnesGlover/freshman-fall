# CS 211 · Programming Languages & Compilers I
## Week 9 · Lecture 1 of 2
### What Concurrent Code Even Means

---

**Reading:** Adve & Boehm (2010) · Sewell et al., "x86-TSO" (2010) · Boehm, "Threads Cannot Be Implemented as a Library" (2005) · **Next:** L20, the models that take the problem away

---

## 1. The Question Weeks 4–8 Never Had to Ask

Every phase you have built assumes something so basic it has never been stated: **the program runs, one instruction after another, and each instruction sees the effects of the ones before it.**

Week 4's dataflow analysis is a claim about paths through a CFG. Week 5's liveness asks what the *future* reads. Week 6's collector stops the world and walks a heap that is not changing underneath it. Week 8's type system proves things about a program that is not being modified while it runs.

Start a second thread and every one of those assumptions needs re-examining, because a much earlier question has become unanswerable: **what does this program mean?**

Not "is it fast", not "is it correct" — *what are its possible results*. Weeks 0–8 had a single answer per input. This week the answer is a set, and the set is larger than almost anyone expects.

---

## 2. Sequential Consistency, and Why You Believe In It

Here is the model everyone reasons with, whether or not they have a name for it.

> **Sequential consistency** (Lamport, 1979): the result of any execution is the same as if the
> operations of all processors were executed in **some sequential order**, and the operations of
> each individual processor appear in that sequence in the order given by its program.

Two clauses. Instructions from one thread keep their program order, and all threads' instructions interleave into one global sequence. It is exactly the mental model of "the threads take turns, we just don't know whose turn it is".

Now use it. Two threads, two variables, both initially zero:

```
    Thread 0:  x = 1;  r1 = y;
    Thread 1:  y = 1;  r2 = x;
```

**Can both `r1` and `r2` end up zero?**

Under sequential consistency, no — and the argument takes one line. Some thread executes its store first. Whichever it is, that store precedes the *other* thread's load in the global order, so that load reads 1. There is no interleaving of four operations in which both loads see zero. Enumerate all six if you like; the outcome never appears.

**It is not a subtle result. It is not a close call. It is impossible.**

---

## 3. It Happens

```
$ gcc -O2 -pthread -o litmus litmus.c
$ ./litmus 200000
```

```
; ---- store-buffer litmus, 200000 iterations ----
  r1=0,r2=0         44   <- FORBIDDEN under sequential consistency
  r1=0,r2=1      94541
  r1=1,r2=0     105397
  r1=1,r2=1         18
  0.136 s   1474451 iters/s   0.0220% forbidden
```

**Forty-four times.** On this machine, in a fifth of a second.

One run proves nothing about a probabilistic effect, so here are eight more at 200,000 each:

```
71   16   20   15   31   25   11   19
```

**Between about 1 in 3,000 and 1 in 18,000**, and on a busy machine a single run gave 378. That spread is itself informative — the rate depends on load, on what else is scheduled, and on nothing you control.

The rate is the problem. **A bug that appears in one run in five thousand passes every test you will write and fails in production on a Tuesday** — and when it does, it will not reproduce.

Two details in that file matter, and both are the difference between measuring the effect and measuring nothing.

**The variables are on separate cache lines.**

```c
#define PAD _Alignas(64)
static PAD volatile int x;
static PAD volatile int y;
```

Remove that padding and the rate does not fall — it rises, by about a hundredfold:

| | forbidden per 500,000 |
|---|---|
| padded (separate lines) | 73 / 50 / 26 |
| **unpadded (shared line)** | **4574 / 8315 / 3258** |

*(This is worth pausing on: when writing this lecture I predicted the opposite, on the reasoning that coherence traffic would serialise the threads and close the window. Measuring it showed the reverse.)*

The mechanism runs the other way. Sharing a line makes it **ping-pong** between the two cores: each store invalidates the other core's copy, so the following load *misses* and takes far longer to complete — which widens the window during which the store is still sitting in the buffer. **False sharing does not hide the reordering; it amplifies it.**

So the padded number is the honest one to quote — a *conservative* figure for how often this is observable when your data is laid out sensibly. And the general point survives its own correction intact: **the layout of two variables changed the measured rate by two orders of magnitude**, and a number produced without checking that is a number about your allocator.

**The threads are created once**, not per iteration. The first version of `litmus.c` created two threads inside the loop and took over two minutes for 20,000 iterations — the measurement apparatus costing four orders of magnitude more than the thing measured.

---

## 4. Why: The Store Buffer

The processor does not write to memory. It writes to a **store buffer** — a small per-core queue — and continues. The write drains to cache later.

A load checks its own core's store buffer first (so a thread always sees its own writes, which is why single-threaded code is unaffected), and otherwise goes to cache. So:

```
Thread 0:  x = 1  ──► [store buffer 0]        r1 = y  ──► cache: y is still 0
Thread 1:  y = 1  ──► [store buffer 1]        r2 = x  ──► cache: x is still 0
```

Both stores are sitting in buffers. Both loads bypass them. Both read zero.

**The load was reordered before the store** — a **StoreLoad** reordering. And it is the *only* one x86 allows:

| reordering | allowed on x86-TSO? |
|---|---|
| Load then Load | no |
| Load then Store | no |
| Store then Store | no |
| **Store then Load** | **yes** |

x86 is called **strongly ordered**, and it deserves the name — ARM and POWER permit all four. But "strongly ordered" is not "sequentially consistent", and the gap between them is exactly wide enough to break the algorithm in §2.

Close it with a barrier:

```
$ ./litmus 500000 fence
  r1=0,r2=0          0   <- FORBIDDEN under sequential consistency
```

Zero. Three runs, 1.5 million iterations, not once. `atomic_thread_fence(memory_order_seq_cst)` compiles to an `mfence` (or a locked instruction), which drains the store buffer before the load may proceed.

> **This is the whole subject in one experiment.** The hardware provides something weaker than
> what you assume, the difference is invisible almost always, and there is an instruction that
> buys back the assumption at a price. Everything in L20 is a way of deciding where to put that
> instruction and who is responsible for remembering.

---

## 5. The Compiler Reorders Too, and It Is Worse

It would be convenient if this were a hardware problem, because then it would be someone else's. It is not.

```c
static int ready;
static int payload;

// reader
while (!ready)
    ;
printf("payload = %d\n", payload);
```

```
$ gcc -O0 -pthread -o hoist_O0 hoist.c ; timeout 5 ./hoist_O0   → terminated
$ gcc -O2 -pthread -o hoist_O2 hoist.c ; timeout 5 ./hoist_O2   → HUNG
$ gcc -O2 -pthread -DATOMIC -o hoist_at hoist.c ; ./hoist_at     → terminated
```

Look at what `-O2` emitted:

```
reader:
        movl    ready(%rip), %eax     # load ONCE, before the loop
        testl   %eax, %eax
        jne     .L5
.L6:
        jmp     .L6                   # an unconditional infinite loop
```

**`.L6: jmp .L6`.** The compiler wrote a loop that cannot exit.

And it was entitled to. `ready` is an ordinary `int`; nothing *in the loop* modifies it; loop-invariant code motion — **Week 5's own optimisation** — hoists the load out. Declare it `_Atomic` and the load stays inside:

```
.L5:
        movl    ready(%rip), %eax     # load INSIDE the loop
        testl   %eax, %eax
        je      .L5
```

> **No processor reordered anything in that program.** The hardware was the most strongly ordered
> mainstream architecture there is, and the program still hung — because the *compiler* is a
> source of reordering, and a far more aggressive one than any CPU. Boehm's 2005 paper is titled
> "Threads Cannot Be Implemented as a Library" for exactly this reason: a library cannot stop the
> compiler doing this, because the compiler does not know the library exists.

---

## 6. A Data Race Is Not "Sometimes Wrong". It Is Undefined.

Both programs above contain a **data race**: two threads access the same location, at least one writes, and nothing orders them.

In C, C++, Java, Go and Rust, the specification does not say a racy program produces an unpredictable value. It says — in C and C++ — that the program has **no defined behaviour at all**, which licenses the compiler to assume races never happen and optimise accordingly.

Watch what that licence buys:

```
$ gcc -O2 -pthread -o orders orders.c && ./orders 4 1000000
; ---- 4 threads x 1000000 increments; correct answer 4000000 ----
  plain            4000000      0.00%    0.000s
```

**The racy version got the right answer in zero seconds.** Here is why:

```
w_plain:
        movq    per_thread(%rip), %rax
        testq   %rax, %rax
        jle     .L2
        addq    %rax, plain_counter(%rip)     # the entire loop, as one add
```

The compiler replaced a million-iteration loop with a single addition. There is no race in the emitted code, because there is no loop. It is allowed to do this precisely *because* the source was racy: undefined behaviour means the compiler owes you nothing.

Now compile the identical source at `-O0`:

```
  plain            2251561     43.71%    <- WRONG
  plain            1465090     63.37%    <- WRONG
```

**Between 44% and 63% of the increments vanish.**

| | answer | time |
|---|---|---|
| `-O2` | **correct** | 0.000 s |
| `-O0` run 1 | 2251561 of 4000000 | 0.038 s |
| `-O0` run 2 | 1465090 of 4000000 | 0.032 s |

Same source. Same machine. **The optimiser "fixed" the bug by deleting it, and that is not a fix** — it is the defect changing shape. Turn optimisation down to debug the problem and the problem appears; turn it up and it hides.

*(For contrast, every non-racy row — `relaxed`, `acq_rel`, `seq_cst`, `mutex` — gives 4000000 at every optimisation level.)*

---

## 7. Memory Safety Does Not Help

It is tempting to file all of this under "C is dangerous". So run the same experiment somewhere with no undefined behaviour, no pointer arithmetic, and a garbage collector.

```
$ java Hoist plain
  reader is STILL SPINNING after 3 s -- the write is never observed

$ java Hoist volatile
  done
```

Java has the bug. So does Go, so does C#, so does Rust if you reach for `unsafe` or misuse `Ordering::Relaxed`.

**And note *when* it starts failing.** The loop runs interpreted at first and terminates fine; once C2 compiles the method — a few tens of milliseconds in — the read is hoisted and the loop becomes infinite. **The same program, in the same run, behaves differently before and after JIT compilation.** A test that finishes quickly passes. Production, which stays warm, hangs.

> **The Java Memory Model makes the same bargain C11 does**: without synchronisation, a thread is
> *not required* to observe another thread's writes. It differs in what it promises when you get
> it wrong — Java guarantees you will see *some* value that was actually written, never a
> fabricated one, which is what "memory safe" buys. **It does not promise you will see the right
> one, or any recent one, or ever.**

---

## 8. Happens-Before

Every model in L20 is defined in terms of one relation, so it is worth stating carefully now.

**Happens-before** is a *partial* order on memory operations, built from two rules:

1. **Program order.** Within a single thread, earlier operations happen-before later ones.
2. **Synchronisation edges.** Certain paired operations create an edge *between* threads: a `volatile` write and the read that observes it; unlocking a mutex and the next lock of it; starting a thread and the thread's first instruction; a thread's last instruction and a successful `join`; a release store and the acquire load that reads it.

If A happens-before B, **B is guaranteed to see A's effects**. If neither happens-before the other, the two are *concurrent*, and if they touch the same location and one writes, **that is the definition of a data race**.

Read §3 and §5 with that in hand:

- In the litmus test, `x = 1` and `r2 = x` are on different threads with **no edge between them**. Concurrent. Racy. The outcome you get is whatever the store buffer permits.
- In `hoist.c`, `ready = 1` and `while (!ready)` are concurrent, so no guarantee exists — and the compiler's hoist is a legal consequence, not a violation.

**Partial is the word to hold on to.** A total order would be sequential consistency, and nobody implements that. What the models give you instead is a *toolkit for adding edges where you need them*, and the entire discipline of concurrent programming is knowing which edges you need.

---

## 9. What to Take From This

1. **Weeks 4–8 all assumed one thread.** With two, the prior question — *what does this program mean* — stops having one answer.
2. **Sequential consistency is what everyone assumes**, and no mainstream processor implements it.
3. **The forbidden outcome happens 44 times in 200,000 iterations** — rare enough to pass every test, common enough to happen daily at scale.
4. **x86 allows exactly one reordering, StoreLoad**, and that one is enough. A `seq_cst` fence removed it: 0 in 1.5 million iterations.
5. **Measuring nothing because your layout hid the effect is not a null result** — the padding in `litmus.c` is load-bearing.
6. **The compiler reorders more aggressively than the hardware.** `-O2` emitted `.L6: jmp .L6`, on x86, with no CPU reordering involved.
7. **A data race is undefined behaviour, not unpredictability** — which is why `-O2` deleted a million-iteration loop and "fixed" the program, while `-O0` lost 63% of the updates.
8. **Memory safety does not help.** Java has the same bug, and it appears only after the JIT warms up.
9. **Happens-before is a partial order**, and every synchronisation primitive is a way of buying an edge in it.

**Next:** the models — C11's memory orders, the JMM, locks, channels, actors and STM — and what each one costs, measured.

---

*CS 211 · Week 9 · Lecture 19 · © CSE Department*

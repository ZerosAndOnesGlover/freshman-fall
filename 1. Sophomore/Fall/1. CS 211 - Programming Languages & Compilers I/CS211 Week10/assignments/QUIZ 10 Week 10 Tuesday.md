# CS 211 · Quiz 10

**Sat:** Tuesday of **Week 10**, first 10 minutes of lecture · TH 205
**Covers:** **Week 9** — concurrency, memory models, and data races
**Unmarked.** Recorded in [[_CS 211 Lab and Quiz Record]].

**The answer key is printed below the questions.** Do not look at it until you have written something for all six.

---

## Questions

**1.** *(2 min)* Two threads, `x` and `y` both initially 0:

```
Thread 0:  x = 1;  r1 = y;
Thread 1:  y = 1;  r2 = x;
```

**Prove `r1 == 0 && r2 == 0` is impossible under sequential consistency.** Then say what actually happens on x86, and why.

---

**2.** *(2 min)* At `-O2`, gcc compiled this reader thread into `.L6: jmp .L6` — an infinite loop:

```c
while (!ready)   /* ready is a plain int, set by another thread */
    ;
```

Name the optimisation responsible, the week you met it, and **why the compiler was entitled to do this.**

---

**3.** *(2 min)* The same racy counter, same source, two builds:

| | answer | time |
|---|---|---|
| `-O2` | 4000000 — correct | 0.000 s |
| `-O0` | 1465090 of 4000000 | 0.032 s |

Explain **both** rows. Then say why "it works at `-O2`" is a worse situation than "it fails at `-O0`".

---

**4.** *(1 min)* Define **happens-before**, and give three operations that create an edge in it.

---

**5.** *(2 min)* x86 permits exactly one of the four reorderings; ARM permits all four.

Name the one x86 permits. Then explain how a program can be **genuinely broken, pass every test on x86 forever, and fail on the first ARM build.**

---

**6.** *(1 min)* ThreadSanitizer finds in one run what testing will not find in a year.

Say what it checks that testing does not — and name its main limitation.

---
---

## Answer Key

**1.** Under sequential consistency, all four operations interleave into **one global order**, with each thread's operations in program order. **Some thread's store is first in that order.** That store therefore precedes the other thread's load, so that load reads 1. No interleaving has both loads reading 0.

**On x86 it happens anyway** — measured at 11 to 71 times per 200,000 iterations. The cause is the **store buffer**: a write retires into a per-core queue before it is visible to other cores, and the following load completes first. That is a **StoreLoad** reordering, the only one x86 permits.

*A `seq_cst` fence removes it — 0 in 1.5 million iterations — by draining the store buffer before the load may issue.*

---

**2.** **Loop-invariant code motion**, from **Week 5**.

The compiler was entitled to it because `ready` is an ordinary `int` written by another thread with no synchronisation — which is a **data race**, and a program with a data race has **undefined behaviour**. The compiler may therefore assume no other thread writes `ready`; under that assumption the load is loop-invariant and hoisting it is correct.

**The optimisation is not the bug.** The program was already broken before it ran.

---

**3.** **`-O2`:** the compiler replaced the entire million-iteration loop with a single `addq %rax, plain_counter(%rip)`. There is no race in the emitted code because there is no loop — licensed, again, by the source being racy and therefore undefined.

**`-O0`:** the loop is really there, three other threads are really interleaving with it, and read-modify-write updates are lost — here 63% of them.

**Why `-O2` is worse:** it removes the *evidence* while leaving the *defect*. The bug returns on a compiler upgrade, a different inlining decision, or a new call site — and the ordinary debugging move of turning optimisation down makes the problem appear, which invites the conclusion that `-O0` is at fault.

---

**4.** **Happens-before** is a **partial order** on memory operations. If A happens-before B, then B is guaranteed to observe A's effects; if neither orders the other, the two are **concurrent**, and if they touch the same location with at least one write, **that is a data race**.

Three edges *(any three)*: program order within one thread; a release store and the acquire load that reads it; unlocking a mutex and the next lock of it; `Thread.start()` and the new thread's first instruction; a thread's last instruction and a successful `join`; a `volatile` write and the read that sees it.

---

**5.** x86 permits **StoreLoad** only. It forbids LoadLoad, LoadStore and **StoreStore**.

The flag-and-payload handoff —

```c
payload = 42;
ready = 1;
```

— is broken by **StoreStore** reordering, which would let `ready` become visible before `payload`. **x86 forbids that, so the program works there by accident of the hardware**, not because it is correct. ARM permits it, so the bug appears on the first ARM build.

**No amount of x86 testing samples an outcome the x86 hardware cannot produce.** More runs, more cores and more load change nothing.

---

**6.** TSan tracks the **happens-before relation** during execution. It does not need the bad interleaving to occur — it observes two conflicting accesses with **no edge between them** and reports that, whatever order they actually happened in on that run. Testing samples *outcomes*, and the bad outcome appears about once in five thousand runs.

**Its main limitation:** it reports races on code paths it **actually executed**. It does not explore schedules and it says nothing about a path not taken. *(Also acceptable: the ~9× slowdown, which makes it a CI configuration rather than a default.)*

---

## How You Did

**6 correct** — you are ready for Week 10.
**4–5** — reread the section you missed before Thursday.
**0–3** — L19 and L20, properly, this week.

**Question 2 is the one that matters most**, and it is the week's actual result: **the compiler is a more aggressive reorderer than the processor.** If you attributed `jmp .L6` to the hardware, reread L19 §5 — the machine was the most strongly ordered mainstream ISA there is, and it reordered nothing.

---

*CS 211 · Week 10 · Quiz 10 · © CSE Department*

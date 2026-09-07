# CS 211 · Programming Languages & Compilers I
## Week 9: Concurrency in Programming Languages

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, CS 102, MATH 151
**Assessment for this course (overall):** Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%
**This week's deliverables:** Lab 9, PS 9, and Quiz 9 (Tuesday, covers Week 8).

> **Project 1 is due Week 11, Friday 17:00.** By the end of this week you should be running under
> `--gc=none`. If you are not, the Week 10 lab session is the last useful place to get help.

---

### Why This Week Exists

Because every phase you have built assumes something it never had to state: **the program runs one instruction at a time, and each sees the effects of the ones before it.**

Week 4's dataflow analysis is about paths through a CFG. Week 5's liveness asks what the future reads. Week 6's collector walks a heap that is not changing underneath it. Week 8's types prove things about a program nobody is editing while it runs.

Start a second thread and a much earlier question becomes unanswerable: **what does this program mean?** Not whether it is fast or correct — what its possible results *are*. Weeks 0–8 had one answer per input. Now it is a set, and the set is bigger than anyone expects.

Then it gets worse: the compiler turns out to be a more aggressive reorderer than the processor.

---

### Learning Objectives

By the end of Week 9, you should be able to:

1. State **sequential consistency** and prove a given outcome impossible under it.
2. Reproduce that outcome on real hardware, and explain the **store buffer** that causes it.
3. Give the four **reordering categories** and say which x86 permits and which ARM does.
4. Explain why a **cache-line layout** changes a measured rate by two orders of magnitude.
5. Recognise **compiler** reordering, and read the assembly that proves it.
6. Explain why a **data race is undefined behaviour**, and what that licenses the compiler to do.
7. Define **happens-before**, and identify which operations create edges.
8. Choose among **`relaxed`, `acquire`/`release` and `seq_cst`**, and say what each costs.
9. Say what **Java's `volatile`** guarantees and what **C's `volatile`** does not.
10. Explain what a **lock** provides beyond mutual exclusion.
11. Describe **actors, channels, STM and async/await**, and what each removes rather than manages.
12. Use **ThreadSanitizer**, and say why it finds what testing cannot.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L19 What Concurrent Code Even Means]] | Sequential consistency, **the impossible outcome measured**, the store buffer, x86-TSO, **the compiler's `jmp .L6`**, undefined behaviour, happens-before |
| [[L20 The Models That Take the Problem Away]] | Memory models as contracts, C11 orders **measured**, the JMM, x86 against ARM, locks, **actors measured**, STM, async/await, TSan |
| [[PS 9 A Mini Actor System]] | Reproduce the impossible, break the compiler's assumptions, then build request/reply, supervision and a pipeline |
| [[QUIZ 9 Week 9 Tuesday]] | **Covers Week 8.** Six questions, key printed below them |
| [[LAB 9 Memory Ordering Bugs You Can Reproduce]] | Four parts, one of which is about the machines we do not have |
| `lab/litmus.c` | The store-buffer test. **Padding and persistent threads are both load-bearing** |
| `lab/orders.c` | Five ways to count to four million; only one is wrong, and it is the fastest |
| `lab/hoist.c` · `Hoist.java` | The same bug in C and in a memory-safe language |
| `lab/actors.py` | Shared state removed rather than managed — and the lock relocated, not eliminated |
| [[CS211 Week9/resources/Reading Guide Week 9\|Reading Guide Week 9]] | Adve & Boehm 2010 · Boehm 2005 · x86-TSO · JMM · Armstrong ch. 2 |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**The compiler reorders more aggressively than the processor does.**

```c
while (!ready)      // ready is a plain int, written by another thread
    ;
```

```
$ gcc -O2 -pthread -S -o - hoist.c
reader:
        movl    ready(%rip), %eax     # load ONCE, before the loop
        testl   %eax, %eax
        jne     .L5
.L6:
        jmp     .L6                   # an unconditional infinite loop
```

**`.L6: jmp .L6`** — the compiler emitted a loop that cannot exit, on x86-64, the most strongly ordered mainstream architecture there is. **No processor reordered anything.**

And it was entitled to. `ready` is an ordinary `int`, nothing in the loop writes it, and **Week 5's own loop-invariant code motion** hoists the load out. The race made the program undefined; undefined licensed the assumption; the assumption made the loop infinite.

*The same licence, applied to `orders.c`, turned a million-iteration racy loop into a single `addq` and produced the **right** answer in 0.000 s — while the identical source at `-O0` lost 63% of its increments. **The optimiser did not fix the bug; it changed its shape.***

---

### Assessment Reminder

**Labs and quizzes carry no weight**, and both are required. **Quiz 9 is sat Tuesday and covers Week 8. Lab 9 is Friday and covers this week.**

Both are tracked in [[_CS 211 Lab and Quiz Record]]. **PS 9 is a weighted component** and goes in [[CS 211]].

**PS 9 is released Wednesday and due Friday of Week 10.** **Midterm 2 results** are returned this week; the mark scheme's grade guidance is in `solutions_instructor/`.

---

### Connections

**Back:** **Week 5's loop-invariant code motion is what hangs `hoist.c`** — your own optimisation, applied to a racy program, correctly. **Week 6's collector stopped the world** precisely to avoid everything in this week. **Week 8's soundness/incompleteness returns as undefined behaviour**, from the other side: there the checker refused a working program, here the compiler accepts a broken one and optimises it freely.

**Sideways:** **CS 201 Week 10** covers cache coherence and multi-core from the hardware side — the MESI protocol underneath L19 §4's store buffer, and the false sharing that L19 §3 measures at 100×.

**Forward:** **Week 10's domain-specific languages** are this week's lesson generalised: the actor model removed a class of bug by making it unwriteable, which is what a good DSL does on purpose. **Week 11's mini-compiler** is single-threaded, and now you know what that assumption was worth.

---

*CS 211 · Week 9 · © CSE Department*

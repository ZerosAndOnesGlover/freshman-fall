# CS 201 · Computer Organization & Architecture
## Week 12 · Lecture 3 of 3
### The Road Ahead

*“I've always been more interested in the future than in the past.”* — Grace Hopper, as quoted in *Reader's Digest* (October 1994)

---

**Reading:** Hennessy & Patterson, "A New Golden Age for Computer Architecture", *Communications of the ACM* 62(2), 2019 · **Previous:** L38, synthesis

**Coursework:** 📋 **Project 2** due today 17:00 · 📝 **PS 11** due today 17:00 · 📝 **PS 12** due today 17:00

---

## 1. Where This Course Sits in the Degree

CS 201 is a foundation course, and its whole purpose is to make everything above it comprehensible. **Here is what it holds up.**

**This semester, right now:**

- **PROG 201 (Systems Programming)** has been running alongside CS 201 and *assuming* it. Every `fork`, `mmap`, `epoll` and signal handler you wrote there stands on this course's stack frame, virtual memory and I/O. **The two were designed to interlock**, and if PROG 201 ever felt like magic, it was CS 201 you were missing.

**Next semester (Spring, Year 2):**

- **CS 202 (Operating Systems)** *implements* what CS 201 *observed*. You watched page faults in Week 6; CS 202 writes the fault handler. You saw the scheduler wake a thread in Week 8; CS 202 writes the scheduler. **You will build a small kernel (xv6) and extend it** — and every subsystem is a CS 201 topic seen from the inside.

**Year 3:**

- **ECE 311 (Computer Architecture II)** extends Weeks 5 and 10 — superscalar issue, speculative execution, the memory system — into the hardware designer's view. Where you *read* the pipeline, ECE 311 *builds* it.
- **CS 341 (Computer Security)** is Week 9 for a semester: formal cryptography, protocols, and exploitation in depth. The buffer overflow you saw is the first page.
- **CS 302 (Networks)** is Week 8 with the derivations — congestion control, routing, the full stack.
- **CS 321 (Databases)** lives on Week 7's storage and `fsync`, and the page cache, made into a transaction engine.
- **CS 331 (AI)** runs on the GPU and the matrix multiply of Weeks 10–11.
- **MATH 341 (Numerical Analysis)** is Week 1's floating point for a whole course.

**Every one of those courses assumes you can do what §L38 §6 listed.** CS 201 is the course they were all waiting for.

---

## 2. What to Actually Remember

You will forget the specific numbers — the cache sizes, the exact cycle counts, this machine's clock. **That is fine; they change every hardware generation anyway.** What should survive:

**The shape of the latency ladder.** Not "DRAM is 438 cycles" but "DRAM is ~100× an L1 hit, and the network is ~10⁶× that". The *ratios* are stable across decades; the absolute numbers are not.

**The method.** Measure, profile, diagnose, bound, fix, re-measure. This does not depend on any hardware fact and will be exactly as true in twenty years.

**The reflex to look.** When you want to know what the machine does, you reach for `objdump`, `perf`, `strace`, `/proc` — you do not guess. **That reflex is the single most valuable thing the course built**, and it transfers to every system you will ever touch, including ones that do not exist yet.

**The distrust of your own intuition about performance.** You were wrong about where the time went (Week 11), wrong about which fix would help (Weeks 4, 6), and wrong about what your benchmark measured (Weeks 0, 1). **Being reliably suspicious of your own performance intuition is what makes you trustworthy.**

---

## 3. How to Keep Learning This

Architecture is not a solved field you have now finished — it is, as the frontiers lecture argued, in a golden age. To keep up:

**Read the disassembly of code you write.** Compiler Explorer (godbolt.org) makes it a browser tab. **Do it idly, for functions you already understand** — the surprises are where the learning is, and you have all term shown that the compiler surprises you.

**Get a machine where `perf` works** and profile something real. The lab's missing `perf` was a constraint you worked around; on your own machine, `perf stat -d` and flame graphs are where professional performance work lives.

**Follow the hardware.** Each new CPU and GPU generation is a lecture in what the field decided mattered — read the launch analyses (Chips and Cheese, AnandTech's archives, the vendor microarchitecture disclosures). **You now have the vocabulary to read them.**

**Build something that has to be fast.** The method only becomes yours when a real deadline forces you to apply it — a game loop, a data pipeline, a server under load. **CS 201 gave you the tools; a hard performance problem is what turns them into skill.**

---

## 4. The Two Things That Will Not Change

Hardware will change beyond recognition. Twenty years from now the cache sizes, the core counts, maybe the whole von Neumann model may look quaint. **Two things will still be true.**

**The speed of light will not change.** Week 8's 187 ms transatlantic round trip is set by physics, not engineering, and no amount of progress shortens it. **Latency floors are permanent**, and the whole discipline of distributed systems exists because of them.

**Data movement will still cost more than computation.** The specific ratio will shift, but the *direction* — that moving a byte costs more than operating on one, and increasingly so — has held for forty years and will hold for forty more. **Every architecture in L37 is, at bottom, an attempt to move less data**, and that will remain the central problem of computer performance for your entire career.

---

## 5. A Closing Word

Week 0 promised that understanding what the computer actually does would make you "a fundamentally better programmer in every language". **You now know what happens when you run your code** — the layers it passes through, the costs at each, the machine underneath the abstraction. That knowledge does not sit in one language or one job; it is the ground the whole field stands on.

**The machine is no longer a mystery to you.** That is the entire point of the course, and it is yours to keep.

Go build something fast.

---

## What to Take Away

1. **CS 201 holds up the degree** — PROG 201 now, CS 202 next semester, and half of Year 3.
2. **Remember the ratios, not the numbers** — the latency ladder's shape outlives any hardware.
3. **Remember the method and the reflex to look** — they depend on no hardware fact.
4. **Distrust your performance intuition** — you were reliably wrong, and knowing it makes you reliable.
5. **The speed of light and the cost of data movement are permanent.** Everything else is negotiable.
6. **The machine is no longer a mystery.** Go build something fast.

---

*This is the last lecture. The final exam covers Weeks 0–12 — see the revision guide. Project 2 is due this week. And when the exam is over, read the Course Retrospective.*

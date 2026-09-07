# CS 201 · Computer Organization & Architecture
## Week 11: Performance Engineering

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), ECE 110 (digital logic)
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** PS 11 (due Week 12 Friday), Lab 11 *(sat Tuesday of Week 12)*, and **Quiz 11 on Monday, covering Week 10 — the last quiz of the course**.

> **Midterm 2 was last week.** Papers are returned this week. **Project 2 is assigned in Week 12**,
> and its optimisation half is exactly this week's method — Lab 11 is the template.

---

### Why This Week Exists

Because eleven weeks of measurement had a method behind them, and this is the week it becomes explicit and repeatable.

Every earlier week gave you a piece: count cache misses, find the dependency chain, ask "device or cache?", look for the bouncing line. **Performance engineering ties them into a loop — measure, profile, diagnose, bound, fix, re-measure — and its first law is that you are wrong about where the time goes.**

The proof is a program where `expensive` is 94% of the runtime and `cheap` is 0%, despite `cheap` being called twice as often. **Intuition blames the call count; the profiler names the truth.** And once the profile names the hotspot, the roofline model says *why* it is slow, and Amdahl's Law says *whether it is worth fixing* — the two steps beginners skip, and the difference between engineering and thrashing.

---

### Learning Objectives

By the end of Week 11, you should be able to:

1. State the profile-diagnose-bound-fix-remeasure method and a tool for each step.
2. Give Knuth's full quote and explain what its second half licenses.
3. Distinguish sampling from instrumenting profilers, and choose correctly.
4. Explain why `-O2` breaks a profiler and how to fix it.
5. Apply Amdahl's Law to a profile to bound the payoff *before* optimising.
6. Define arithmetic intensity and classify a kernel as compute- or memory-bound.
7. Read the roofline and choose the *kind* of fix from the roof you are under.
8. Diagnose a memory-bound hotspot with cachegrind and fix it by improving locality.
9. Order optimisation work: flags first, then targeted structural change.
10. **Recognise and fix a benchmark that measures nothing.**
11. Cross-check a measurement against an independent model.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L34 Measure First — Profiling and Amdahl in Practice]] | The method; the surprising profile; sampling vs instrumenting; the `-O2` trap; Amdahl as a budget |
| [[L35 The Roofline Model — Diagnosing the Bottleneck]] | Compute vs memory-bound, arithmetic intensity, and 7.45× from a loop reorder |
| [[L36 Benchmarking Honestly]] | The course's "measured nothing" failures collected into a checklist |
| [[PS 11 A Measured 10x Speedup]] | The method, the roofline, **a full optimisation report**, and honest benchmarking |
| [[CS201 Week11/assignments/QUIZ 11 Week 11 Monday\|QUIZ 11 Week 11 Monday]] | Ten minutes on Week 10 — the last quiz. **Unmarked, key in the paper** |
| [[LAB 11 Profile Diagnose Fix Remeasure]] | The capstone lab: the full loop on one program — the Project 2 template |
| [[CS201 Week11/resources/Reading Guide Week 11\|Reading Guide Week 11]] | CS:APP Chapter 5 in full, plus the roofline paper |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Measure, diagnose, bound — in that order — and never optimise what you have not measured.**

A profile said `expensive` was 94% and `cheap` was 0%, correcting the intuition that twice-the-calls meant twice-the-cost. Amdahl said even deleting `expensive` caps you at 16.7×, so the 6% "rest" is the real ceiling. The roofline said a matrix multiply was *memory-bound* — and a loop reorder that changed no arithmetic dropped its last-level miss rate from **50% to 8%** for a **7.45×** speedup, on top of the **5.7×** the compiler flags gave for free.

**16 seconds became 0.58 — a 28× improvement — and every step was a measurement.** Not one came from guessing, and the two that beginners skip (diagnose, bound) are what made the rest efficient.

---

### Assessment Reminder

**Labs and quizzes carry no weight**; the four weighted components already total 100%. Both remain required.

**Quiz 11 is Monday** — the course's last, covering Week 10. **Week 11's and Week 12's material are examined only on the final.** **Lab 11 is sat Tuesday of Week 12.**

**PS 11 is an optimisation report**, not a set of short answers: Q3 asks for a **measured 10× speedup achieved by analysis**, with the method evidenced at every step. **The marks are for the method — a speedup with no profile, diagnosis or correctness check is worth little.**

**A tool note:** `perf` needs privileges the lab machines lack, so this week uses **gprof** and **valgrind (callgrind/cachegrind)**. The method is identical; the notes say where `perf` would be better, and learning it is worthwhile on any machine you own.

---

### Connections

**Back:** **the whole course.** Week 4 (count misses), Week 5 (dependency chains, roofline, Amdahl), Week 7 ("device or cache?"), Week 10 (the bouncing line) — this week is the method that unifies them. **Week 0's constant-folded loop** is L36's first benchmarking failure.

**Forward:** **Project 2 (Week 12)** extends the Project 1 simulator with a cache, and its optimisation half is graded on exactly Lab 11's loop. **CS 341, CS 331** and every systems course assume you can profile before optimising.

**Sideways:** **CS 212 (Software Engineering)** this spring covers profiling and benchmarking as engineering practice; **PROG 201** has been building the systems whose performance this week measures.

---

*CS 201 · Week 11 · © CSE Department*

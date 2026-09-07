# CS 211 · Programming Languages & Compilers I
## Week 11: Language Implementation — A Complete Mini-Compiler

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, CS 102, MATH 151
**Assessment for this course (overall):** Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%
**This week's deliverables:** **PROJECT 1 (Friday 17:00)**, PS 10 (also Friday), Lab 11, and Quiz 11 (Tuesday, covers Week 10).

> ## ⚠ Project 1 is due Friday at 17:00 — 12.5% of the course.
>
> PS 10 is due the same day and is worth roughly 2.3%, with the lowest problem set dropped.
> **The arithmetic is not close.** Lab 11 on Friday afternoon is a legitimate place to finish the
> project report instead; tell the TA.

---

### Why This Week Exists

Because you have written eight phases and never once run them as a compiler.

Week 6 stopped at a register assignment and *interpreted* the TAC — right for studying garbage collection, wrong for producing a program. This week adds the ninth phase and the driver that ties the other eight together, and then the thing runs:

```
$ python3 cyanc.py gcd.cy 1071 462 --run
; ---- lli (JIT): exit code 21 = gcd(1071, 462) ----
```

**Twenty-one.** Machine code your compiler produced, on this processor.

And it gets there by **not writing a back end**. `llvmgen.py` emits LLVM IR and hands the rest to LLVM — which is the bargain the second half of the week is about, and the reason our compiler targets eight architectures without any of us knowing AVR assembly.

---

### Learning Objectives

By the end of Week 11, you should be able to:

1. Describe all **nine phases** and what each consumes and produces.
2. Explain what a **compiler driver** does, and that it is not a phase.
3. Read and write basic **LLVM IR** — `alloca`, `load`, `store`, `icmp`, `br`, `phi`.
4. Explain the **`alloca` + `mem2reg`** strategy and why real front ends use it.
5. Identify **φ-functions** in `mem2reg` output and match them to a CFG.
6. Name a constraint LLVM imposes that our TAC does not, and say why an interpreter cannot find it.
7. Compare an optimiser honestly, **including the caveats that make the comparison unfair**.
8. Explain LLVM's **m × n → m + n** argument, and name a cost of it.
9. Read a target's assembly and infer facts about its **instruction set**.
10. Say what a **JIT** knows that an AOT compiler cannot, and what it pays.
11. Use **differential testing** between two independent back ends.
12. State what your compiler still cannot do, and what closing each gap requires.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L23 The Whole Compiler in One Command]] | Nine phases, the `alloca` trick, **our optimiser against LLVM's**, where compile time really goes, and 11-of-11 differential agreement |
| [[L24 LLVM and the Compiler You Did Not Write]] | **Eight targets from one IR**, LLVM as libraries, pass pipelines, JIT against AOT, and what our compiler still cannot do |
| [[PS 11 Finish the Compiler]] | Typed IR, multiple functions, your own peephole pass, and **arrays, structs and the stack map** |
| [[QUIZ 11 Week 11 Tuesday]] | **Covers Week 10.** The last quiz of the term |
| [[LAB 11 A JIT for Your Own Compiler]] | Run the whole thing, watch `mem2reg` work, then target eight machines |
| `lab/cyanc.py` | **The driver.** Nine phases, `--emit`, `--run`, `-o`, `--times` |
| `lab/llvmgen.py` | Phase 9: TAC → LLVM IR. Read the docstring on `alloca` |
| `lab/lexer.py` … `regalloc.py` | Weeks 0–6, carried forward unchanged |
| `lab/runtime.py` · `collect.py` · `heap.py` | Week 6's interpreter — **the independent implementation the JIT is checked against** |
| `lab/gcd.cy` · `cls.cy` · `fold.cy` · `sc.cy` · `scale.cy` · `div.cy` | The test programs, from Weeks 4–5 |
| [[CS211 Week11/resources/Reading Guide Week 11\|Reading Guide Week 11]] | Lattner & Adve 2004 · AOSA ch. 11 · Kaleidoscope · the LLVM Language Reference |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**We wrote no back ends and got eight.**

```
$ llc -march=TARGET gcd.ll
```

| target | instructions | why |
|---|---|---|
| **aarch64** | **8** | hardware `sdiv`, then `msub` for the remainder |
| ppc64le | 10 | |
| sparcv9 | 11 | |
| x86-64 | 12 | |
| mips64 | 12 | |
| **riscv64** | **16** | **the base ISA has no divide** — `call __moddi3` |
| **wasm32** | **23** | structured control flow: `block`, `br_if`, not branches |
| **avr** | **124** | an 8-bit microcontroller doing 64-bit arithmetic |

**A fifteenfold spread, from identical input**, and every number is a fact about the target rather than about our compiler.

> That is LLVM's argument in one table: *m* languages × *n* targets becomes *m* + *n*. A new
> language gets every back end; a new back end gets every language. **The cost is that the IR
> becomes a compatibility surface** — it must express C's undefined behaviour, Rust's aliasing,
> Swift's reference counting and Java's memory model at once, which is why LLVM IR has `poison`,
> `noalias` and a specification that is genuinely hard.

---

### Assessment Reminder

**Labs and quizzes carry no weight**, and both are required. **Quiz 11 is Tuesday and covers Week 10 — it is the last quiz of the term.** Lab 11 is Friday.

**Project 1 is due Friday 17:00 and is 12.5% of the course**, recorded in [[CS 211]]. **PS 10 is due the same day.**

**PS 11 is released Wednesday and due Friday of Week 12** — with Thanksgiving recess in between, and **PS 12 due that same Friday**.

**Project 2 is also assigned this week** and is due Week 12, Friday — the spec is
[[PROJECT 2 A Compiler With Optimisation]]. **It extends Project 1
rather than replacing it**, which is what makes two weeks feasible; if Project 1 does not run,
its Part A is where to start.

---

### Connections

**Back:** **Week 4's dominance-frontier algorithm is what `mem2reg` runs** — we studied it and called it rather than writing it. **Weeks 4–5's optimiser is measured against LLVM's**, honestly. **Week 5's phase-ordering problem** is why `-O2` is 200 passes in a particular order. **Week 6's interpreter is the independent implementation** the JIT is differentially tested against. **Week 9's memory model reappears** in LLVM IR's atomics. **Week 9's branch-misprediction cost** is what a JIT's profile-guided layout is buying.

**Sideways:** **CS 201's x86-64** is one column of the target table; `L17 Branch Prediction` is why JIT speculation pays.

**Forward:** **Week 12 asks what all of this was for** — why there are so many languages and how to judge one. **PS 11 Part C** is where Weeks 5, 6 and 11 converge: arrays need a heap, a heap needs a collector, and a precise collector needs a stack map, which is a compiler output.

---

*CS 211 · Week 11 · © CSE Department*

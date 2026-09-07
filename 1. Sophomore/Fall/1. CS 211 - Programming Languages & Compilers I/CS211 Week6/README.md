# CS 211 · Programming Languages & Compilers I
## Week 6: Runtime Systems — Memory Management

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, CS 102, MATH 151
**Assessment for this course (overall):** Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%
**This week's deliverables:** Lab 6, PS 6, Quiz 6 (Tuesday, covers Week 5), and **Project 1 is assigned**.

---

### Why This Week Exists

Because `alloc` has been a promise since Week 4, and nothing in the compiler ever kept it.

Grep the whole pipeline for `free` and you get six hits, **all of them in the register allocator**. Registers are a scarce resource, and your compiler manages them exactly — Week 5 computed every value's lifetime and reused a register the moment its occupant died. The heap gets none of that. Two thousand lines, an `alloc` opcode, and no code anywhere that gives memory back.

**Nothing has broken because nothing has run.** Every phase so far produced a *representation*, and a representation cannot leak. So Week 6 builds the phase that can, and then has to answer the question that phase raises: **what is still pointing here?**

---

### Learning Objectives

By the end of Week 6, you should be able to:

1. Explain why **stack deallocation is free** and heap deallocation is not, in terms of lifetime nesting.
2. State the **two failure modes of manual `free`** and say why they are not symmetric.
3. Implement **reference counting** against a runtime's write hooks, and say why increment must precede decrement.
4. Explain why reference counting is **sound but incomplete**, and construct the counterexample.
5. Recognise that **only a prompt collector can measure a lifetime**, and identify a histogram that is measuring its own threshold.
6. Implement **tri-colour mark-and-sweep**, and state the invariant that makes it correct.
7. Derive a **root set** from liveness, and explain why the root set is a *compiler* output.
8. Predict what an **unsound def/use model** does to a collector, and distinguish it from an imprecise one.
9. Quantify the cost of **conservative rooting**, and say why peak footprint does not reveal it.
10. Distinguish **precise from conservative** collection, and explain why precision is what permits moving.
11. Explain the **generational hypothesis**, the **write barrier** that pays for it, and the **promotion hole** no barrier covers.
12. Read a real GC log, and **say what the number in it actually measures**.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L13 The Instruction Nothing Frees]] | Stack vs heap, manual `free`, reference counting **measured as the smallest-footprint collector here**, lifetimes, the cycle, **and the discovery that Cyan cannot express one** |
| [[L14 Roots Generations and the Cost of a Write Barrier]] | Roots from liveness, **Week 4's bug as a use-after-free**, conservative vs precise, generations, barriers, **the promotion hole**, four JVM collectors, **and a log that lies** |
| [[PS 6 Mark-and-Sweep Reachability and the Root Set]] | Mark bits, a **copying collector**, refcount leak detection, and a **heap-growth policy** |
| [[QUIZ 6 Week 6 Tuesday]] | **Covers Week 5.** Six questions, key printed below them |
| [[PROJECT 1 A Language Feature End to End]] | **Assigned this week, due Week 11.** One feature, all eight phases |
| [[LAB 6 Profiling Garbage Collection Pauses]] | Four collectors, four root policies, and the measurement that inverts the ranking |
| `lab/heap.py` | Pointers, objects, and every counter this week reads. **Read its docstring** — it explains why it is not the top of `runtime.py` |
| `lab/runtime.py` | The interpreter. Executes TAC, keeps a heap, and answers "what can this program still reach?" three different ways |
| `lab/collect.py` | `RefCount`, `MarkSweep`, `Generational` — and `Collector`, which is `--gc=none`, which is what you have been shipping |
| `lab/pauses.py` | Summarises a JVM `-Xlog:gc` stream. **Percentiles, not totals** |
| `lab/pycycle.py` | The same cycle leak, in CPython, on the interpreter you have used all term |
| `lab/Churn.java` | `churn.cy` at a scale the JVM notices |
| `lab/churn.cy` · `chain.cy` · `loiter.cy` · `victim.cy` | Objects that die young · objects that never die · an object that is dead but in scope · an object the wrong root set frees |
| `lab/cycle.cy` · `cyc_direct.cy` · `cyc_empty.cy` · `cyc_array.cy` | The cycle, and the three rules that used to prevent it |
| `lab/lexer.py` · `parser.py` · `tac.py` · `live.py` · `loops.py` · `opt.py` · `regalloc.py` | The pipeline so far, carried forward from Week 5, unchanged |
| `lab/typecheck.py` | **Changed this week.** `check_expr` takes an expected type — eleven lines, and reference counting stops being complete |
| [[CS211 Week6/resources/Reading Guide Week 6\|Reading Guide Week 6]] | Dragon §7.4–7.8 · Appel ch. 13 · GC Handbook ch. 5, 9, 11 · Ungar 1984 |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**The garbage collector's root set is Week 5's liveness analysis, and nothing checks it.**

Register allocation asked liveness *when may I reuse this register?* A collector asks it *what can the program still see?* Same analysis, same table, different consumer — and the consumer decides what a bug in it costs:

| Week 4's def/use model, consumed by | Symptom |
|---|---|
| dead-code elimination *(Week 5)* | one instruction deleted; wrong answer |
| **the root set** *(Week 6)* | **`#2` freed, then written through — use-after-free** |

```
$ python3 runtime.py victim.cy victim --gc=mark --threshold=4 --roots=live
; ---- victim() = 0 ----

$ python3 runtime.py victim.cy victim --gc=mark --threshold=4 --roots=week4
; ---- CRASH ----
  #2 was freed, and the program still has a pointer to it
```

**Same program, same collector, same threshold. One missing entry in a table.**

An imprecise analysis makes a slow program. **An unsound one makes an exploitable one**, and the compiler is the only thing that can be right about it — a collector cannot recompute its own roots, and there is no assertion that fires when they are wrong.

---

### Assessment Reminder

**Labs and quizzes carry no weight**, and both are required. **Quiz 6 is sat Tuesday and covers Week 5. Lab 6 is Friday and covers this week** — both of the week's lectures have already happened by then.

Both are tracked in [[_CS 211 Lab and Quiz Record]]. **PS 6 is a weighted component** and goes in [[CS 211]], as does **Project 1**, which is assigned this week and due Week 11.

**PS 6 is released Wednesday and due Friday of Week 7**, as every problem set in this course has been. *(The registry's [[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]] lists problem sets one week earlier than the papers do; the papers are correct and the calendar has been corrected — see [[Registry Reconciliation]] §8.)*

---

### Connections

**Back:** **Week 5's liveness is the stack map**, arriving as a root set for a consumer it was not written for. **Week 4's `Instr.uses` returns as a memory-safety bug** rather than a missing instruction. **Week 3's type information is what makes precise collection possible** — a `Ref` is a `Ref`, and L14 §5 is about the collectors that have to guess. **Week 1's fixed-point iteration** runs one last time, inside the marker.

**Sideways:** **CS 201 Week 9** reaches use-after-free from the attacker's side and finds `-fsanitize=address`. **CS 201's `L15 Locality as Leverage`** is why a 1 GB JVM heap runs 12% slower than a 128 MB one while doing 40% less collection — the same argument, delivered through a runtime flag.

**Forward:** **Week 7 removes the heap entirely.** The lambda calculus has no assignment, no objects and no memory model, and is Turing-complete anyway — everything fought over this week turns out to follow from one design decision Week 7 does not make. **Week 11's LLVM back end** needs a real stack map, and it is this table. **Project 1** is assigned now: if your feature allocates, §4 of the brief is where the marks are lost.

---

*CS 211 · Week 6 · © CSE Department*

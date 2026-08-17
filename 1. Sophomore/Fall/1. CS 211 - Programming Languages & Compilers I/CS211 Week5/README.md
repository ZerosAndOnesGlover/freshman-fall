# CS 211 · Programming Languages & Compilers I
## Week 5: Optimization — Loops and Data Flow

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, CS 102, MATH 151
**Assessment for this course (overall):** Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%
**This week's deliverables:** Lab 5, PS 5, and Quiz 5 (Tuesday, covers Week 4).

---

### Why This Week Exists

Because Week 4's optimiser is guessing, and this week you find out what that cost.

**Its dead-code pass deletes an instruction the program needs.** Three lines of Cyan are enough to show it, the compiler reports no error, and the surviving code writes through a register nothing ever loaded. The cause is a def/use model that decides what counts as a variable by *looking at the operand* rather than by knowing what the opcode means.

**Everything else this week is built on the analysis that replaces it.** Liveness gives honest dead-code elimination, and then gives the interference graph that register allocation is a colouring of. Get liveness wrong and you do not get a slow compiler — you get one that assigns two live values to the same register.

---

### Learning Objectives

By the end of Week 5, you should be able to:

1. Write a **def/use table** for an IR and explain why a shape-based heuristic cannot replace it.
2. Compute **live variables** as a backward, union dataflow analysis, at block and instruction level.
3. Compute **dominators** as a forward, intersection analysis, and say why *may* starts empty and *must* starts full.
4. Find **back edges and natural loops** in a CFG, and explain why the back end cannot ask the parser.
5. State the three **safety conditions for code motion**, and show that condition (1) hoists nothing from a `while` body.
6. Explain **speculation**, name the trap predicate, and predict which instructions LLVM will and will not hoist.
7. Describe **loop rotation** and say precisely what it does for the optimiser — and what it does not.
8. Detect **basic induction variables**, and explain why they are never one instruction.
9. Build an **interference graph** and run **Chaitin's algorithm** — simplify, spill, select.
10. Justify a **spill heuristic**, and connect loop depth to register assignment.
11. Read `-O0` through `-Os` output and explain why **instruction count is not a proxy for speed**.
12. Distinguish an optimiser bug that **loses an opportunity** from one that **loses a constraint**.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L11 Liveness Loops and Loop-Invariant Code Motion.md` | The Week 4 bug, the def/use table, liveness, dominators, natural loops, LICM, **the trap predicate measured against LLVM**, induction variables |
| `lectures/L12 Register Allocation Instruction Selection and the Pipeline.md` | Interference, **Chaitin optimal at k=7**, spill costs, instruction selection as maximal munch again, peephole, phase ordering, **`-O2` measured**, LTO |
| `assignments/PS 5 Liveness Loop-Invariant Code Motion and Register Allocation.md` | Relaxed LICM, Briggs' optimistic colouring, and two questions whose honest answer may be negative |
| `assignments/QUIZ 5 Week 5 Tuesday.md` | **Covers Week 4.** Six questions, key printed below them |
| `lab/LAB 5 Optimised and Unoptimised Assembly.md` | Reproduce the bug, then the four-cell hoisting table, then read `-O1` whole |
| `lab/live.py` | Liveness, the `SLOTS` def/use table, and DCE that is not guessing |
| `lab/loops.py` | Dominators, natural loops, LICM, induction variables |
| `lab/regalloc.py` | Interference graph, spill costing, Chaitin's algorithm |
| `lab/scale.cy` · `scale.c` · `div.cy` · `div.c` | The hoisting experiment, in both languages — **one operator apart** |
| `lab/nested.cy` · `coalesce.cy` · `drv.c` | The DCE bug, the move exception, and the timing driver |
| `lab/lexer.py` · `parser.py` · `typecheck.py` · `tac.py` · `opt.py` | The pipeline so far, carried forward from Week 4. **`tac.py` has changed** — `load`, `store`, `getfield` and `setfield` now print honestly, and `Instr.uses` is marked unsafe and superseded by `live.py` |
| `resources/Reading Guide Week 5.md` | Dragon §9.2.5, §9.5.3, §9.6, §8.8–8.9 · Appel ch. 11 · Chaitin 1982 |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Same loop. Same pass. One operator changed.**

| | unrotated | rotated |
|---|---|---|
| `k * 2 + 1` | hoisted, **unguarded** | hoisted, guarded |
| `100 / k` | **stays in the loop** | hoisted, guarded |

LLVM will lift a multiply out of a loop it might never enter, and refuses to do the same to a division. **The rule is not about loops at all** — it is whether executing the instruction unnecessarily can be observed. A multiply wastes a cycle. A division can turn a program that returns 0 into one that dies.

**Loop rotation is how a compiler buys the hoist without taking the bet.** It optimises nothing itself; it restructures the CFG so the guard exists. Run it alone and nothing moves.

*(All four cells reproducible with `opt`; commands in L11 §7 and Lab 5 Q8–Q10.)*

---

### Assessment Reminder

**Labs and quizzes carry no weight**, and both are required. **Quiz 5 is sat Tuesday and covers Week 4. Lab 5 is Friday and covers this week** — both of the week's lectures have already happened by then.

Both are tracked in `5. Academic Registry/2. Gradebook/Year2 Sophomore/Fall/_CS 211 Lab and Quiz Record.md`. **PS 5 is a weighted component** and goes in `CS 211.md`.

---

### Connections

**Back:** **Fixed-point iteration for the fourth and fifth time** — ε-closure (W1), FIRST/FOLLOW (W2), the folder (W4), now liveness and dominators. **Maximal munch returns from Week 1** as greedy instruction selection: longest token, largest tile, same algorithm. **L10's dataflow framework** is instantiated twice here, once in each direction.

**Sideways:** **CS 201's `L15 Locality as Leverage`** is the argument for loop fusion, from the hardware side. CS 201's sixteen registers are the `k` this week colours for.

**Forward:** **Week 6 leaves the compiler for the runtime** — your `alloc` instruction produces a pointer and nothing in the pipeline ever frees it. **Week 11 replaces our TAC with real LLVM IR** and every pass here happens again at production quality. **PS 5's LICM is a component of Project 1**, assigned next week.

---

*CS 211 · Week 5 · © CSE Department*

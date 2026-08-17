# CS 211 · Problem Set 5
## Liveness, Loop-Invariant Code Motion, and Register Allocation

**Released:** Wednesday, Week 5 · **Due:** Friday, Week 6, 17:00
**100 points · counts toward the Problem Sets component (30% of the final grade)**

**Submit:** `loops.py` and `regalloc.py` (your versions, runnable end to end) and `ps5.md` (written answers, tables, traces). Written answers inside code comments will not be marked.

Start from the Week 5 lab folder. `live.py` is given to you complete — **you may not change its `SLOTS` table**, because Part A asks you to justify it and Part D depends on it being right.

> **Project 1 is assigned next week and is due Week 11.** The LICM pass you write here is a
> component of it. Write it as though you will have to read it again in six weeks, because you will.

---

## Part A — Liveness and the Def/Use Model (18 points)

**A1.** *(4)* For each of the six opcodes below, state which slots hold variables that are **read**, which hold variables that are **written**, and which hold something that is not a variable at all. Give the non-variable's kind (operator, field name, type name, literal, label).

`copy` · `unary` · `load` · `store` · `getfield` · `alloc`

Check each answer against the corresponding `emit(...)` call in `tac.py`. **Cite the line number.**

**A2.** *(4)* Week 4's `Instr.uses` gets `store` wrong in the unsafe direction and `getfield` wrong in the safe direction.

- Explain both, in one sentence each.
- **Which is worse, and why?** Your answer must use the words *conservative* and *unsound* correctly.

**A3.** *(4)* Run the Week 4 optimiser on `nested.cy` and reproduce the 8 → 6 reduction. Then write the shortest Cyan function you can that **triggers the same bug and returns a wrong value** rather than merely corrupting memory. If you believe no such function exists, prove it.

**A4.** *(6)* Liveness is backward and merges with union; dominance is forward and merges with intersection.

- Fill in a four-row table: analysis, direction, merge, initial value.
- **Explain why a *may* analysis must start empty and a *must* analysis must start full.** What goes wrong if you swap them? Answer in terms of what the fixed point converges to, not in terms of the code.

---

## Part B — Dominators and Loops (18 points)

**B1.** *(5)* Compute the dominator sets for `scale.cy` **by hand**, showing each iteration. Then check against `python3 loops.py scale.cy scale`. Report the number of rounds to convergence and whether your hand computation agrees.

**B2.** *(4)* State the definition of a back edge, and of the natural loop it heads. Identify both in `scale`.

**B3.** *(4)* Write a Cyan function whose CFG contains a loop that **the parser never saw as a loop** — that is, one built from `if` and a backward jump rather than from `while`. If Cyan's grammar makes this impossible, say so and explain what feature would be needed, then argue whether a back-end loop finder is still worth having.

**B4.** *(5)* `basic_ivs` in `loops.py` looks for a binary operation whose result is copied back into one of its own operands, rather than for `i = i + c` directly.

- **Why?** Show the two-instruction TAC that `i = i + 1` actually lowers to.
- A detector matching `i = i + c` literally finds **zero** induction variables in every loop this compiler emits. Verify that claim by writing the naive version and running it on three loops. Report the counts.

---

## Part C — Loop-Invariant Code Motion (28 points)

**C1.** *(6)* `loops.py` reports `invariant=6 hoistable=0` on `scale.cy`. Explain the gap precisely, naming the blocks and the dominance relation that fails.

**C2.** *(10)* **Implement `licm_relaxed`.** L11 §6 notes that condition (1) — *the block dominates every loop exit* — may be relaxed when the destination is **dead after the loop**, because then no one can observe the extra execution.

- Implement it, using the liveness you have.
- Run it on `scale.cy`. **How many instructions now hoist?**
- Run it on `div.cy`. **How many? Is that the right answer?**

**C3.** *(6)* Compare your relaxed version against LLVM's LICM on `div.cy`, instruction by instruction.

- **Do they hoist the same set?** Answer yes or no, with the evidence.
- Whatever you found, the two of you reach that decision by **different rules**. Name both rules and say which instruction each one is deciding.
- **Now try to construct a Cyan program on which the relaxed condition changes observable behaviour** — give the input, the output before, and the output after. If you cannot, identify the line of `loops.py` that stopped you and state exactly what would happen if it were deleted. *(Read the note at the foot of this sheet before deciding which of those two you are writing up.)*

**C4.** *(6)* LLVM hoists `k * 2 + 1` out of an unrotated loop but refuses `100 / k`. Reproduce both (Lab 5 Q8–Q10) and paste the two IR fragments.

Then answer: **what single property of an instruction decides it?** Name LLVM's predicate. Give two more x86-64 instructions on each side of the line.

---

## Part D — Register Allocation (24 points)

**D1.** *(4)* Run `regalloc.py` on `scale.cy`. Report nodes, edges, and the five highest-degree variables. **State in one sentence what those five have in common** and what that implies about where register pressure comes from.

**D2.** *(6)* Produce the spill-count-versus-$k$ table. Independently compute the **maximum number of simultaneously live values** (Lab 5 Q6).

They agree at $k = 7$. **Explain why peak liveness is a lower bound on the registers needed by *any* allocator**, and state whether Chaitin being optimal here means it is optimal in general. Justify.

**D3.** *(8)* **Implement Briggs' optimistic colouring.** Instead of committing to a spill when every node has degree $\ge k$, push the node anyway and only spill during SELECT if no colour is actually free.

- Implement it alongside Chaitin's, selectable by a flag.
- **Find a Cyan function on which Briggs spills strictly fewer variables than Chaitin.** Report both traces.
- If you cannot find one after honest effort, report what you tried and **explain the structural property a graph needs** for optimism to pay off. *(A correct explanation earns full marks; a fabricated example earns zero.)*

**D4.** *(6)* The move exception in `interference()` changes nothing on `scale.cy` and changes the graph on `coalesce.cy`.

- Report both measurements.
- **Explain the difference in terms of copy sources and liveness.**
- Then: is omitting the exception incorrect, or merely wasteful? **Give the general principle** for telling those two kinds of optimiser defect apart. This is the most important two sentences in the problem set.

---

## Part E — Reading the Optimiser (12 points)

**E1.** *(6)* Reproduce the five-level table — instruction count beside runtime — for `scale.c`.

`-O2` emits far more instructions than `-O1` and runs faster; `-Os` matches `-O1`'s size and is slower than both. **Account for all three facts with one explanation.**

**E2.** *(6)* Read the `-O1` assembly and annotate every instruction with the Week 5 optimisation responsible for it, or with "none". Instructions you cannot attribute should be marked and explained rather than guessed.

Then: **which optimisation in this week's lectures is *not* visible anywhere in that listing, and why not?**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 18 | The def/use model, and why guessing from shape fails |
| B | 18 | Dominance, natural loops, induction variables |
| C | 28 | LICM, the safety conditions, and the trap predicate |
| D | 24 | Interference, Chaitin, Briggs, and optimal vs good |
| E | 12 | Reading a real optimiser's output |
| **Total** | **100** | |

---

## Reference Numbers

From the machine these notes were prepared on (Python 3.14, clang 18.1.3, x86-64 Linux). **Counts are deterministic; timings are not.**

| Measurement | Value |
| --- | --- |
| `opt.py` on `nested.cy` | 8 → 6 instructions *(the bug)* |
| `live.py` on `nested.cy` | 8 → 8 |
| `scale` dominators, rounds to fixed point | 2 |
| `scale` natural loops | 1, header `L0`, body `{L0, B2}` |
| `scale` invariant / hoistable | 6 / 0 |
| `scale` interference graph | 18 nodes, 69 edges |
| `scale` peak simultaneous live | 7 |
| `scale` zero-spill $k$ | 7 |
| `coalesce.cy` edges, with / without move exception | 1 / 2 |

`scale.c` by optimisation level, best of 5 over $2\times10^7$ elements:

| Level | instructions | runtime |
| --- | --- | --- |
| `-O0` | 28 | 45 ms |
| `-O1` | 15 | 13 ms |
| `-O2` | 57 | 8 ms |
| `-O3` | 57 | 7 ms |
| `-Os` | 15 | 14 ms |

**The checksum is identical at every level.** If yours is not, stop and find out why before doing anything else — you have found either a compiler bug or, far more likely, undefined behaviour in your test harness.

---

## A Note on Parts C3 and D3

Both ask you to look for something that may not exist, and both say so.

C3 asks you to break a relaxed safety condition, and the trap rule may stop you. D3 asks you to beat Chaitin with Briggs, and on small graphs you often cannot.

**In both, a careful negative result is worth full marks and a fabricated positive one is worth zero.** This is not generosity. An optimiser is a program whose entire job is to be right about claims of the form *"this transformation is safe"*, and the habit of reporting what you actually found — rather than what the question seemed to want — is the only thing standing between you and shipping a compiler that miscompiles one program in ten thousand.

---

*CS 211 · Week 5 · Problem Set 5 · © CSE Department*

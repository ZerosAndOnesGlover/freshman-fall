# CS 211 · Reading Guide · Week 5
## Optimization: Loops and Data Flow

**Read against a question.** The Dragon Book's chapter 9 is 130 pages and you do not need most of them this week. Each entry below says what to get out of the section and roughly what it costs.

---

## Before Tuesday (L11 — liveness, loops, LICM)

| Source | Section | Why | Pages |
|---|---|---|---|
| **Dragon** | **§9.2.5** | Live-variable analysis, stated properly. You met the framework in L10; this is the instance. | 4 |
| **Dragon** | **§9.6.1–9.6.2** | Dominators and natural loops. **The definitions in §9.6.2 are exactly what `loops.py` implements** — read them with the code open. | 8 |
| **Dragon** | **§9.5.3** | The three safety conditions for code motion. This is the section L11 §6 argues with. | 4 |
| **Appel** | **ch. 10** | The same material, shorter and more readable. If §9.6 does not land, come here first. | 15 |

**Skip for now:** §9.6.5 (dominance frontiers in depth) — Week 4 gave you what you need, and Week 11 returns to it.

---

## Before Thursday (L12 — allocation, selection, the pipeline)

| Source | Section | Why | Pages |
|---|---|---|---|
| **Dragon** | **§8.8.1–8.8.4** | Register allocation and assignment, including the interference graph. | 7 |
| **Appel** | **ch. 11** | **The best treatment of graph colouring in either book.** Chaitin's algorithm, spilling, and coalescing, with worked graphs. If you read one thing this week, this. | 20 |
| **Dragon** | **§8.9** | Instruction selection by tree rewriting. Read §8.9.1–8.9.3; the rest is optional. | 8 |
| **Dragon** | **§8.7** | Peephole optimisation. Short, and the examples are the point. | 4 |

---

## Papers, If You Want Them

Neither is required. Both are readable, and both are the actual source of what you are implementing.

- **Chaitin, G. (1982), "Register Allocation and Spilling via Graph Coloring."** *SIGPLAN Notices* 17(6). The original. Eight pages, and you will recognise every step.
- **Briggs, P., Cooper, K., Torczon, L. (1994), "Improving Register Allocation for Subscripted Variables."** The optimistic-colouring refinement PS 5 Part D asks you to implement.
- **Cytron et al. (1991)** on SSA construction is Week 4's paper, and is the one to read if φ-functions still feel like magic.

---

## LLVM Documentation

You will use `opt` seriously this week. Two pages are worth having open:

- **`llvm.org/docs/Passes.html`** — what each pass does. Look up `licm`, `loop-rotate`, `loop-simplify`, `mem2reg`, `indvars`.
- **`llvm.org/docs/NewPassManager.html`** — why `licm` must be written `loop-mssa(licm)`. **Read this after you have hit the error**, not before; it makes much more sense that way.

---

## The One Thing Worth Reading Twice

**Dragon §9.5.3, the three conditions on code motion.**

Read it, then run `python3 loops.py scale.cy scale` and watch it hoist nothing. The text and the measurement disagree with your intuition in the same direction, and reconciling them is L11 §6–7 and PS 5 Part C.

**The book does not tell you that condition (1) is unsatisfiable for a `while` loop.** It is true, it follows in two lines from the definitions, and noticing it is the difference between having read the section and having understood it.

---

## A Note on Chapter 9

Chapter 9 is the part of the Dragon Book where students most often stall, and the reason is that it presents a *framework* (§9.2–9.3) before the *instances* that motivate it (§9.5–9.6).

**If you are stuck, read §9.6.1 first** — dominators, concretely, with a picture — and go back to the framework once you have something to instantiate it with. L10 and L11 are deliberately ordered the other way round from the book for this reason.

---

*CS 211 · Week 5 · Reading Guide · © CSE Department*

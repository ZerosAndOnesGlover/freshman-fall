# CS 211 · Final Exam Revision Guide
## Weeks 0–12 · Tuesday 16 December, 09:00–11:30 · VNC 100

**150 marks, 150 minutes.** One handwritten sheet of A4, **both sides**. No devices.

**Seven questions.** Q1–Q4 (80) are the pipeline. Q5–Q6 (40) are the runtime and the theory. **Q7 (30) is synthesis.**

---

## The Fastest Useful Thing You Can Do

**Re-read the eleven quiz answer keys.** Quizzes 1–11 cover Weeks 0–10, they are already written out with reasoning, and between them they cover more than half of what this paper asks.

If you have four hours, spend the first ninety minutes there. Then read the two midterm mark schemes.

---

## What Is Actually Examinable

**The lectures and the labs.** Anything measured in a lab is fair; anything that appears only in the Dragon Book is not.

**You will not be asked to reproduce an exact figure.** You may be asked what a figure *showed* and why. "About one in ten thousand, because the store buffer window is small" is a full-marks answer; "0.0220%" alone is not.

**Weeks 0–3 are examined in Q1 only**, and lightly — Midterm 1 covered them properly. **Weeks 4–7 carry Q2–Q4 and much of Q7.** Do not neglect Week 12: it is not a question of its own but it supplies Q7(c).

---

## Section A · The Pipeline (80 marks)

### Q1 — Front end (Weeks 0–3), 20 marks

**Know cold:** writing a small CFG and arguing ambiguity; the maximal munch rule; why a left-recursive grammar breaks recursive descent and how to fix it; a type error with a line and column; **Hindley-Milner by hand on a two-binder term**.

**Practise Q1(e) specifically.** Infer `λf. λx. f (f x)` on paper until the unification steps are automatic. It is four marks and it is free once you have done it three times.

### Q2 — IR (Week 4), 20 marks

**Know cold:** lowering an `if` to TAC; the **three leader rules**; SSA and φ insertion; the dataflow table with **initial values**.

**Two things to prepare as sentences:**
1. Why a *may* analysis starts empty and a *must* starts full — **in terms of which fixed point is reached**, not in terms of the code.
2. The `store` def/use bug and its **three** consumers. Q2(d) is six marks and Q7(a) is ten more on the same material.

### Q3 — Optimisation and codegen (Weeks 5, 11), 20 marks

**Know cold:** why condition (1) hoists nothing from a `while` body; the **trap predicate** rule; peak liveness as a **lower** bound and colouring as NP-complete; `alloca` + `mem2reg`; the multi-target table.

**Rehearse the trap-predicate answer.** It is easy to answer vaguely and get half.

### Q4 — Semantics (Week 7), 20 marks

**Know cold:** reducing a term by hand, showing steps; capture and what each result *is*; `Y g = g (Y g)` and one reduction step; the encodings.

**Q4(d) is the one to prepare properly.** `zero`/`false`/`nil` are the same term, `mult`/`compose` are the same term, **those are different kinds of fact**, and **types separate neither** — a declaration does. That is the place this course revised its own claim, and it is on the paper.

---

## Section B (40 marks)

### Q5 — Memory and concurrency (Weeks 6, 9), 20 marks

**Know cold:** zero proves unreachable and positive proves nothing; the root set comes from **Week 5's liveness, written for register allocation**; write barrier and remembered set; **the promotion hole**; the store-buffer litmus test; `jmp .L6` and why the compiler was entitled to it.

**The promotion hole is the hardest single idea in Week 6.** If you can explain in three sentences why no write barrier can catch it, Q5(c) is free.

### Q6 — Types, proofs, macros (Weeks 8, 10), 20 marks

**Know cold:** `let` vs λ and generalisation; dictionary passing and *when* a missing instance is reported; the proof of `A → B → A` is `const`; why `A ∨ ¬A` has no proof; macro vs function; capture and `gensym`; why a total language cannot have `Y`.

---

## Q7 — Synthesis (30 marks)

**This is a fifth of the paper and it is the part people run out of time for. Prepare it in advance.**

**(a) The same table, three consumers.** Know the opcode, the slot, the three symptoms, and be ready to *rank them by severity with a justification*.

**(b) Silent failure.** Have **three** worked examples ready with their *mechanism of invisibility* — not "it gave a wrong answer" but *why nobody saw it*. And know **two instruments that agreed with a bug**: the printer that misreported a def, peak RSS that could not see retention, `0 == False`, a phase timer measuring `fork`, a cache line changing a rate 100×.

**Memorise one figure for this question**: the store-buffer outcome appears roughly **once in 3,000–18,000 iterations**. You need a number to argue that more tests is not the answer.

**(c) A language design argument.** Two guarantees, what each makes impossible, what it costs, **and who pays** — machine, programmer, or user. Then one guarantee that rejects correct programs, with an example. **There is no required conclusion**; a well-argued disagreement scores full marks.

---

## A Realistic Three-Evening Plan

**Evening one — mechanics.** Quizzes 1–11. Then, on paper: infer a type, lower an `if`, reduce three lambda terms, compute liveness on a four-block CFG. **Write them out.**

**Evening two — the prepared sentences.** Draft, in two or three sentences each: may/must initialisation; the trap predicate; the promotion hole; "the same function"; theorem vs collision; why types do not separate `zero` from `false`.

**Evening three — Q7.** Draft all three parts. Thirty marks, and it is the only part you can genuinely write in advance.

**Your A4 sheet, both sides.** Put on it what you cannot derive: leader rules, the dataflow table with initial values, the def/use table, Chaitin's phases, the Church encodings, `Y` and `Z`, the four reorderings, the C11 memory orders. **Do not put the arguments on it** — if you need to read the trap-predicate rule off a sheet you cannot apply it, and writing it out is most of how you learn it.

---

## What Is Not On This Paper

- Writing code. You will not be asked to write Python.
- Exact reproduction of lab measurements.
- LLVM IR syntax beyond reading it — you will not be asked to write valid IR from memory.
- Anything from CS 201, MATH 241 or PROG 201.
- Project 1 or Project 2, which are assessed on their own.

---

## If You Are Short of Time

In priority order:

1. **The eleven quiz keys.**
2. **Q7, drafted in advance** — 30 marks, and the only part you can prepare fully.
3. **Mechanical practice:** type inference, TAC lowering, beta reduction. Pure marks.
4. **The prepared sentences from Weeks 5 and 6.**

**Skip:** re-reading the lectures end to end. You have read them. Rehearsing the arguments out loud is worth more per minute at this stage.

---

*CS 211 · Week 12 · Final Exam Revision Guide · © CSE Department*

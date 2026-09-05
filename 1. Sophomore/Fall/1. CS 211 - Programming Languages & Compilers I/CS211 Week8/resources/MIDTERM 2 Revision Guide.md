# CS 211 · Midterm 2 Revision Guide
## Weeks 4–7 · Sat Week 8, Tuesday 28 October, 20:00–21:15

**75 marks, 75 minutes.** One handwritten sheet of A4, **one side**. No devices.

**Five questions, one per week plus a synthesis.** Q1 Week 4, Q2 Week 5, Q3 Week 6, Q4 Week 7, Q5 across all four.

---

## The Fastest Useful Thing You Can Do

**Re-read the four quiz answer keys.** Quiz 5, 6, 7 and 8 each cover the week before them, they are already written out with the reasoning, and between them they cover about half of what this paper asks.

If you have two hours, spend the first thirty minutes there.

---

## What Is Actually Examinable

The exam is written from the lectures and the labs, not from the reading. **Anything measured in a lab is fair; anything that only appears in the Dragon Book is not.**

You will not be asked to reproduce an exact figure. You may be asked what a figure *showed* and why — "roughly ten thousand reductions, because normal order re-computes `pred n` at every level" is a full-marks answer and "10384" on its own is not.

---

## Week 4 · Intermediate Representations

**Know cold:**

- Lowering a statement to TAC. Practise `a[i+1] = b.count * 2` and `return (a+b)*(a-1)` until it is mechanical.
- **The three leader rules**, and that rule 3 — the instruction after a terminator — is the one people forget.
- SSA, and inserting a φ at a join.
- **What a φ *is*:** a note recording which predecessor control came from. It is not executable, and the back end destroys it into copies.
- Dataflow's **two knobs**, and the settings for liveness, reaching definitions, available expressions and dominance.

**The part that separates answers:** *why* a **may** analysis starts empty and a **must** analysis starts full. Answer it in terms of which fixed point the iteration converges to, not in terms of the code. If you cannot say what goes wrong when you swap them, you do not have this yet.

---

## Week 5 · Optimisation

**Know cold:**

- The def/use table, and specifically that **`store` and `setfield` read their `dst`**.
- Liveness as backward + union; dominance as forward + intersection.
- Back edges and natural loops.
- The interference graph, and Chaitin's simplify/spill/select.

**Three things worth a sentence each, prepared in advance:**

1. **Why condition (1) hoists nothing from a `while` body.** Draw the header with the test in it. The body does not dominate the exit.
2. **Why LLVM hoists `k*2+1` and not `100/k`.** It is about the **trap predicate**, not about loops. Rehearse this one; it is easy to answer vaguely and get half.
3. **Conservative against unsound.** Be able to use both words correctly about `getfield` and `store` respectively, and say which is worse and why.

**And one number:** peak simultaneous liveness is a **lower** bound on registers. Colouring is NP-complete; Chaitin is a heuristic.

---

## Week 6 · Runtime Systems

**Know cold:**

- Reference counting: zero proves unreachable, **positive proves nothing**. Be able to draw a cycle.
- Tri-colour mark-and-sweep, and the invariant: no black object points to a white one.
- **Where the root set comes from** — Week 5's liveness, written for register allocation.
- Generations, the write barrier, the remembered set.

**The three parts most likely to be asked:**

1. **The root set is a compiler output and the collector cannot check it.** Know why that makes a wrong entry so dangerous.
2. **Peak live does not reveal retention.** Know why (the trigger fixes it) and what does (residency, objects scanned).
3. **The promotion hole.** An old-to-young pointer that no write created. This is the hardest single idea in Week 6 — if you can explain it in three sentences you can answer anything in Q3.

*The `--roots=week4` crash and the `--no-fixup` result are both worth being able to describe from memory: what happened, and why it was silent in one case and loud in the other.*

---

## Week 7 · The Lambda Calculus

**Know cold:**

- Reducing a term by hand, showing steps. **Practise this. It is three marks and it is free if you have done it ten times.**
- The three conventions: left-associative application, bodies extend rightwards, `λx y. e` is currying.
- Capture: `(λx y. x) y` gives a **constant function** correctly and **the identity** naively.
- `Y g = g (Y g)`, and one step of the reduction.
- Church encodings: numerals as for-loops, booleans as choices.

**The four things most likely to be asked:**

1. **What each capture result *is*** — described by behaviour, not by appearance.
2. **Why `Y` diverges under call-by-value** and what subterm loops.
3. **What "the same function" means**, such that `eta(Z) == Y` and different termination is not a contradiction. This is the one that separates the top of the cohort.
4. **`zero`, `false` and `nil` are the same term**, and `mult == compose` is a *different kind* of fact — theorem against collision.

---

## Q5 · The Synthesis Question

Fifteen marks, and it is the same argument four times.

| week | the silent failure |
|---|---|
| 4 | the folder turned −301 into −401 |
| 5 | dead-code elimination deleted a live `load` |
| 6 | the collector freed an object the next instruction wrote through |
| 7 | naive substitution turned a constant function into the identity |

**Prepare two things before you walk in.**

**First, the common root cause.** Three of those four trace to one table — the def/use model — and one entry in it. Know which three, know the entry, and be able to say how the *severity* changed as the consuming phase changed: an instruction deleted in Week 5, a use-after-free in Week 6.

**Second, the mechanism of invisibility for at least two of them.** Not "it gave a wrong answer" — *why nobody saw it*. Week 5's pass printed a **success** message and the dump asserted the opposite of the truth. Week 6's collector returned the **right answer** while corrupting the heap. Week 7's suite reported 23/23 because `0 == False`.

**Q5(c) asks you to argue.** There is no required conclusion. A well-argued answer that disagrees with the lectures scores full marks; a confident answer with no examples scores almost nothing.

---

## A Realistic Two-Evening Plan

**Evening one — mechanics.** Quiz 5–8 keys. Then, on paper: lower two statements to TAC; compute liveness on a four-block CFG; reduce three lambda terms. **Write them out.** Recognising these is not the same as producing them under time pressure.

**Evening two — arguments.** Draft, in two or three sentences each: the trap predicate rule; why peak live hides retention; the promotion hole; what "the same function" claims. Then draft the Q5 through-line.

**Your A4 sheet.** Put on it the things you cannot derive: the three leader rules, the dataflow table with initial values, the def/use table, Chaitin's three phases, the Church encodings, `Y`. **Do not put the arguments on it** — if you need to read the trap-predicate rule off a sheet you will not be able to apply it, and writing it out is most of how you learn it.

---

## What Is Not On This Paper

- Week 8. **Types, System F, type classes and Curry-Howard are not examinable here** — this paper covers Weeks 4–7 only.
- Project 1. It is assessed on its own.
- Anything from Weeks 0–3 as a topic in its own right. Midterm 1 covered those. You will still need Week 3's scope rule for Q4(b), because capture *is* that rule — but you will not be asked to write a parser.
- Exact reproduction of lab measurements.

---

## If You Are Short of Time

In priority order:

1. The four quiz keys.
2. Reducing lambda terms by hand, and lowering statements to TAC. Pure marks, and mechanical.
3. The three prepared sentences from Week 5 and the three from Week 6.
4. The Q5 through-line.

**Skip:** re-reading the lectures end to end. They are long, you have read them, and at this point rehearsing the arguments out loud is worth more per minute than reading them again.

---

*CS 211 · Week 8 · Midterm 2 Revision Guide · © CSE Department*

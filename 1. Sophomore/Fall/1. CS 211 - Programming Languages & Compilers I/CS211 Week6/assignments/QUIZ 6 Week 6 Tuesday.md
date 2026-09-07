# CS 211 · Quiz 6

**Sat:** Tuesday of **Week 6**, first 10 minutes of lecture · TH 205
**Covers:** **Week 5** — liveness, dominators and natural loops, loop-invariant code motion, register allocation, instruction selection, the pipeline
**Unmarked.** Recorded in [[_CS 211 Lab and Quiz Record]].

**The answer key is printed below the questions.** Do not look at it until you have written something for all six. The point of this quiz is to tell *you* what you do not know, twenty minutes before Week 6 starts building a garbage collector on top of it.

---

## Questions

**1.** *(2 min)* Here is one instruction:

```
    a[i] = v
```

Name **every variable it reads** and **every variable it writes**. Then say which of the three operand slots — `dst`, `a`, `b` — each one lives in.

---

**2.** *(2 min)* Liveness is **backward** and merges with **union**. Dominance is **forward** and merges with **intersection**.

One of the two starts with every set **empty**; the other starts with every set **full**. Say which is which, and give the one-sentence reason.

---

**3.** *(2 min)* Dragon §9.5.3's first safety condition for hoisting an instruction out of a loop is that its block **dominates every exit of the loop**.

L11 showed that this condition hoists **nothing** out of an ordinary `while` loop. Why not? Draw the two blocks you need to make the argument.

---

**4.** *(2 min)* LLVM will hoist `k * 2 + 1` out of a loop that might execute zero times, and refuses to hoist `100 / k` out of the same loop.

**State the rule that distinguishes them.** It is not a rule about loops.

---

**5.** *(1 min)* You build an interference graph with 18 nodes, and the largest set of variables simultaneously live at any point is 7.

For a machine with `k = 7` registers, Chaitin's algorithm colours it with no spills. **Is that guaranteed in general?** One sentence, and name the complexity result you are relying on.

---

**6.** *(1 min)* `-O2` emits **3.8× more instructions** than `-O1` for the same function, and the `-O2` binary runs **1.6× faster**.

Explain how both numbers can be true, and say what this tells you about using instruction count as a performance metric.

---
---

## Answer Key

**1.** `a[i] = v` lowers to `store`, which **reads three variables and writes none**.

| variable | slot | read or written |
| --- | --- | --- |
| `a` (the array) | `dst` | **read** — and written *through* |
| `i` (the index) | `a` | read |
| `v` (the value) | `b` | read |

**The array is in the `dst` slot and is a *use*, not a *def*.** That is the entry Week 4's `Instr.uses` was missing, and it is the whole of Week 5 §1–3: the instruction does not define `a`, it writes into the object `a` points at.

*Full credit requires naming `a` as a read. Saying "`store` defines `a`" is the exact error the week was about.*

---

**2.** **Liveness starts empty. Dominance starts full.**

Liveness is a **may** analysis: a variable is live if there exists *some* path to a use. Union grows the sets, so starting empty and growing converges to the *least* fixed point — the smallest set consistent with the equations, which is the correct answer for "does a path exist".

Dominance is a **must** analysis: a block dominates another if *every* path passes through it. Intersection shrinks the sets, so starting full and shrinking converges to the *greatest* fixed point.

*Swap them and both converge to the trivial answer — everything live, or nothing dominating.*

---

**3.** The condition requires the instruction's block to **dominate every exit of the loop**. In a `while` loop, the loop-exit test is in the **header**, and the body is what you want to hoist from.

```
        header:  if cond goto exit      <- the exit is HERE
           |
        body:    t = k * 2              <- and you want to hoist THIS
           |
        goto header
```

Control can leave the loop from the header **without ever entering the body**. So the body does not dominate the exit, and condition (1) fails for every instruction in it.

**This is not a defect in the rule.** The rule is protecting you from executing the body's instructions on a path where the source never would — which matters exactly when one of them can trap.

*Full credit for any answer that identifies the header's exit edge as the one the body does not dominate.*

---

**4.** **Whether executing the instruction unnecessarily can be observed.**

A multiply that did not need to happen wastes a cycle and produces a value nobody reads. A division that did not need to happen can **divide by zero**, and turn a program that returns a value into one that traps.

Hoisting is **speculation**: it executes an instruction on a path where the source program would not have. That is legal for instructions that cannot fault, and illegal for instructions that can.

*The rule is about the **trap predicate** of the instruction, not about loops, not about invariance, and not about how many times the loop runs. Loop rotation earns the hoist for the division by restructuring the CFG so that a guard exists — it does not change the rule.*

---

**5.** **No.** Graph colouring is **NP-complete** in general, and Chaitin's algorithm is a *heuristic*: repeatedly remove nodes of degree less than `k`, and if none exists, choose one to spill.

That it found a zero-spill colouring at exactly the peak simultaneous liveness is a **good result on that graph**, not a guarantee. There are graphs that are `k`-colourable which the heuristic spills on — that is what Briggs' optimistic colouring improves.

*Peak liveness is a **lower bound** on the registers needed. Chaitin achieving it means the bound was tight here.*

---

**6.** `-O2` runs vectorisation and aggressive unrolling. Both **add** instructions — a vectorised loop carries setup, a remainder loop, and alignment checks — while **reducing the number of instructions actually executed per element of data**, and improving how the CPU pipelines them.

Static instruction count measures the size of the code. Runtime is a function of the **dynamic** instruction count, the instruction mix, cache behaviour, and how well the code fills a superscalar pipeline. `-O2` trades more of the first for less of everything else.

**Instruction count is a measure of code size, and using it as a proxy for speed will mislead you in both directions.** `-Os` was 15 instructions and slower than `-O2`'s 57.

---

## How You Did

**6 correct** — you are ready for Week 6.
**4–5** — reread the section you missed before Thursday.
**0–3** — L11 and L12, properly, this week.

**Question 1 is the one that matters most for Week 6, and it is not close.** The def/use table you were asked about there is the table that supplies a garbage collector's root set. Get it wrong in Week 5 and you delete an instruction; get it wrong in Week 6 and you free memory the program is still using. If you missed Q1, do not wait — read L11 §3 before Thursday's lecture.

---

*CS 211 · Week 6 · Quiz 6 · © CSE Department*

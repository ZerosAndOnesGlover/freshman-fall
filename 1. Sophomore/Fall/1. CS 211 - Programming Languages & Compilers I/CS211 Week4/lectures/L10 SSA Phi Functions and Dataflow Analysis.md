# CS 211 · Programming Languages & Compilers I
## Week 4 · Lecture 2 of 2
### SSA, φ-Functions, and Dataflow Analysis

---

**Reading:** Dragon §6.2.4, §9.2–9.3 · LLVM Language Reference, *"Instruction Reference"* · **Next:** Week 5, L11 — loop optimisation and register allocation

---

## 1. The Question Every Optimisation Asks

```
    a = 1
    a = 2
    b = a + 1
```

**Which `a` does `b` use?** Obvious here. Now put the assignments in different basic blocks, behind a conditional, inside a loop — and answering it means tracing every path through the CFG.

**Nearly every optimisation needs this answer.** Constant propagation needs to know whether the `a` reaching this point is known. Dead-code elimination needs to know whether *any* later use reads this definition. **The relation between a use and the definitions that reach it is the fundamental query**, and on ordinary code it is expensive.

**SSA makes the answer free.**

---

## 2. Static Single Assignment

> **Every variable is assigned exactly once.**

Assign to `a` three times and you get `a₁`, `a₂`, `a₃`. Now a use names its definition directly — **there is nothing to trace, because the name *is* the answer.**

```
    a1 = 1
    a2 = 2
    b1 = a2 + 1
```

**"Static" is doing real work in that name.** The *instruction* appears once in the program text; it may *execute* a million times in a loop. **SSA constrains the text, not the execution.**

---

## 3. Where Control Flow Merges: φ

Straight-line code renames trivially. **Branches do not:**

```cyan
if c { a = 1; } else { a = 2; }
return a;
```

Which definition reaches the `return`? **Both, depending on the path.** SSA cannot name one, so it names the *choice*:

```
    a3 = phi(a1, a2)
    ret a3
```

**A φ-function takes one operand per incoming CFG edge** and yields whichever corresponds to the edge actually taken.

> **φ is not a real instruction and nothing executes it.** It is a *notation* recording that two
> values merge here. The back end removes it by inserting a copy at the end of each predecessor
> block — which is why φ must sit at the *top* of a block, before anything else.

---

## 4. Watching mem2reg Do It

`clang -O0` puts every local in memory (L09 §4): three `alloca`s, six `load`s, five `store`s for `gcd`. **LLVM's `mem2reg` pass promotes those to SSA registers.**

```
$ clang -S -emit-llvm -O0 -Xclang -disable-O0-optnone -o o0.ll gcd.c
$ opt -passes=mem2reg -S o0.ll
```

```llvm
define dso_local i32 @gcd(i32 noundef %0, i32 noundef %1) #0 {
  br label %3

3:                                     ; preds = %5, %2
  %.01 = phi i32 [ %1, %2 ], [ %6, %5 ]
  %.0  = phi i32 [ %0, %2 ], [ %.01, %5 ]
  %4 = icmp ne i32 %.01, 0
  br i1 %4, label %5, label %7

5:                                     ; preds = %3
  %6 = srem i32 %.0, %.01
  br label %3

7:                                     ; preds = %3
  ret i32 %.0
}
```

*(Measured, LLVM 18.1.3.)*

| | instructions | alloca | load | store | phi |
|---|---:|---:|---:|---:|---:|
| `-O0` | **23** | 3 | 6 | 5 | 0 |
| after `mem2reg` | **11** | **0** | **0** | **0** | **2** |

*(Measured.)*

**Every memory operation is gone**, replaced by two φ-nodes — one for `a`, one for `b`, the two variables that carry values around the loop.

**Read the first φ closely:**

```llvm
%.01 = phi i32 [ %1, %2 ], [ %6, %5 ]
```

*"If we arrived from block `%2` (the entry), take `%1` — the parameter `b`. If we arrived from block `%5` (the loop body), take `%6` — the result of `srem`."* **That is the loop-carried dependency, stated explicitly**, and it is exactly what a loop optimiser needs to know.

**This is why every serious compiler uses SSA.** LLVM, GCC's GIMPLE, the JVM's C2, V8's TurboFan, and Go's compiler are all SSA-based. **The transformation costs one pass and makes every subsequent analysis simpler.**

---

## 5. Dataflow Analysis

φ answers the question for *values*. **Dataflow analysis answers it for facts** — and it is one algorithm with a few parameters.

**The shape.** For each basic block $B$:

$$\text{out}[B] = f_B(\text{in}[B]) \qquad \text{in}[B] = \bigsqcup_{P \in \text{pred}(B)} \text{out}[P]$$

**Iterate to a fixed point.** Fourth appearance — after $\varepsilon$-closure, FIRST/FOLLOW, and L09 §6.

### Three analyses, one algorithm

| | Direction | Meets with | Answers |
|---|---|---|---|
| **Reaching definitions** | forward | union | *which assignments could have produced this value?* |
| **Live variables** | **backward** | union | *will this value be read again?* |
| **Available expressions** | forward | **intersection** | *has this expression already been computed?* |

**Change the direction and the merge operator and you have a different analysis.** The iteration is identical.

### Liveness, and why it is backward

> **A variable is *live* at a point if some path from there reads it before overwriting it.**

That is a statement about the *future*, so the information flows backwards:

$$\text{live-in}[B] = \text{use}[B] \cup (\text{live-out}[B] \setminus \text{def}[B])$$

*"Live coming in if you read it before writing it, or if it was live going out and you did not overwrite it."*

**Liveness is what L09 §5's dead-code pass was missing.** Our folder left `unused = 99` in place because it only removes temporaries; LLVM removed it because liveness proves nothing reads `unused` afterwards. **Week 5 implements it**, and it is also the input to register allocation — two variables can share a register exactly when they are never live at the same time.

### Union or intersection: the difference matters

**Reaching definitions uses union** — a definition reaches if it reaches along *any* path. **Available expressions uses intersection** — an expression is available only if it was computed along *every* path.

**Get that backwards and you generate wrong code.** Claiming an expression is available when one path skipped it means reusing a value that was never computed. **Union is the safe default for "might"; intersection is required for "must".**

---

## 6. Building SSA: Where the φ Go

Placing φ-nodes naively — one at every join for every variable — works and produces enormous amounts of garbage. **The right answer uses *dominance*.**

**$X$ dominates $Y$** if every path from entry to $Y$ passes through $X$.

**The dominance frontier of $X$** is the set of blocks that $X$ does *not* dominate but whose predecessors it does — **precisely the points where a definition in $X$ stops being the only one that could reach**, so a φ is needed exactly there.

**The algorithm:** for each variable, place φ-nodes at the dominance frontier of every block that defines it, iterating (because a φ is itself a definition). **This is *minimal* SSA**, and Cytron et al.'s 1991 paper giving it is why SSA became practical rather than a curiosity.

> **You will not implement dominance frontiers in this course** — it is the one piece of Week 4
> that CS 311 does properly. **What you must be able to do is read the φ-nodes LLVM produces and
> say why each one is there**, which is Lab 4.

---

## 7. What to Take Away

1. **Every optimisation asks which definition reaches this use.** SSA makes the answer part of the name.
2. **"Static" means the assignment appears once in the text**, not that it executes once.
3. **φ-functions record a merge**, take one operand per incoming edge, sit at the top of a block, and do not execute.
4. **mem2reg turns memory into SSA**: 23 instructions to 11 for `gcd`, all 11 memory operations replaced by 2 φ-nodes.
5. **A loop's φ-node states the loop-carried dependency explicitly.**
6. **Dataflow analysis is one algorithm** parameterised by direction and merge operator.
7. **Liveness is backward** because it is a claim about the future — and it is what dead-code elimination and register allocation both need.
8. **Union for "might", intersection for "must".** Confusing them produces wrong code, not slow code.
9. **φ-nodes go on the dominance frontier**, which is what makes SSA minimal.

---

## Exercises

1. Convert to SSA by hand: `a = 1; if c { a = 2; } b = a + 1;`. Where does the φ go, and how many operands has it?
2. `%.0 = phi i32 [ %0, %2 ], [ %.01, %5 ]` — the second φ in §4. **Say what each operand is** in terms of the original C, and why `%.01` rather than `%6` appears there.
3. A φ has one operand per **incoming edge**, not per predecessor block. **Construct a CFG where those differ.**
4. Run liveness by hand on `gcd`'s CFG (L09 §3). Which variables are live at the top of `L0`?
5. Available expressions uses intersection. **Give a CFG and an expression where using union instead would generate wrong code**, and say what wrong thing happens.
6. §6 says a φ is itself a definition, so placement must iterate. **Construct a case where placing one φ forces another.**
7. `mem2reg` turned 3 allocas into 0. **Give a C function with a local that `mem2reg` cannot promote**, and say why. *(Hint: what breaks the assumption that a variable lives in a register?)*

---

*Next week: with the CFG and dataflow in hand, Week 5 makes code faster on purpose — loop-invariant code motion, induction variables, and register allocation by graph colouring. **Midterm 1 is sat this week and covers Weeks 0–3.***

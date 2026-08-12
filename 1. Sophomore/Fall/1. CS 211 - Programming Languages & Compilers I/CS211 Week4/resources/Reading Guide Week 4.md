# CS 211 · Week 4 · Reading Guide
## Dragon Chapter 6, and your first LLVM reference

---

**Set reading:** Aho et al., **§6.1–6.4** (intermediate code), **§8.4** (basic blocks and flow graphs), **§9.2–9.3** (dataflow).
**Also set:** the **LLVM Language Reference**, *Instruction Reference* — the `phi`, `br`, `alloca`, `load` and `store` entries only. [llvm.org/docs/LangRef.html](https://llvm.org/docs/LangRef.html)
**Optional:** Appel, **Chapters 7–8**. Appel's IR is closer to ours than the Dragon's.

**§6.1–6.4 and §8.4 before Tuesday.** §9.2–9.3 after Thursday. **The midterm is Wednesday and none of this is on it** — read the Week 0–3 guides again instead if time is short.

---

## The Reading Priority This Week

**Your week is not mostly reading.** Midterm 1 is Wednesday, PS 4 is a substantial implementation, and Chapter 6 is long. **Read in this order and stop when you run out of time:**

1. **§8.4** — basic blocks and flow graphs. Six pages, and it is the whole of L09 §3.
2. **The LLVM `phi` entry** — one page, and it makes L10 concrete.
3. **§6.2** — three-address code. The instruction forms.
4. **§9.2** — dataflow analysis, the general framework.
5. Everything else.

---

## Section by Section

| § | What to take from it |
|---|---|
| **6.1** | Syntax-directed translation into IR. The book's notation is heavier than what you need; skim for the idea that translation is another attribute grammar |
| **6.2** | **Three-address code.** §6.2.1's instruction forms, §6.2.2's quadruples/triples representations. **Our `Instr` class is a quadruple** |
| **6.2.4** | **SSA, introduced.** Short — three pages — and the φ-function appears here |
| **6.4** | Boolean expressions and **short-circuit code**. §6.4.4 is `gen_shortcircuit` from L09 §2, written as translation rules |
| **6.6** | Backpatching. **Skip** — it is a technique for one-pass compilers, and ours is not |
| **8.4** | **Basic blocks and flow graphs.** §8.4.1's leader rules are the ones in L09 §3 |
| **9.2** | **The dataflow framework.** §9.2.1 reaching definitions, §9.2.5 live variables, §9.2.6 available expressions |
| **9.3** | Foundations — lattices and the meet operator. **Read for why union and intersection are the two choices**, and skip the lattice theory unless it interests you |

---

## Two Things Worth Getting Exactly Right

**§6.4.4's short-circuit translation.** The book gives it as `B.true` and `B.false` labels threaded through the translation. **Our version is simpler and does the same job**, and it is worth reading both — the book's approach generalises better to `if (a && b || c)` where the jump targets are known in advance.

**§9.2's table of the three analyses.** Direction, meet operator, transfer function, and the initial value. **Copy that table onto one page and you have Week 5's entire toolkit.** Note especially that the *initial value* differs — reaching definitions starts empty, available expressions starts with everything — and that this follows directly from union versus intersection.

---

## What the Dragon Book Does Not Give You

**Working code.** Chapter 6 is translation *schemes* in an attribute-grammar notation, not programs. **Appel Chapter 7 gives you real code** for the same material and is worth the hour if the Dragon's notation is not landing.

**Modern SSA.** §6.2.4 is three pages and predates SSA becoming universal. **The φ-placement algorithm — dominance frontiers — is not in the Dragon Book at the depth you would need to implement it.** L10 §6 gives you the idea; Cytron et al. (1991) is the paper, and CS 311 does it properly.

**Any sense of scale.** The book will not tell you that `mem2reg` turns 23 instructions into 11 on a five-line function, or that LLVM runs its pass pipeline dozens of times. **Run the commands in Lab 4; the numbers are the part that sticks.**

---

## Questions to Read Against

**On §6.2 and §6.4**

1. §6.2.2 contrasts quadruples with triples. **Which is our `Instr`**, and what would change if we used the other?
2. §6.4.4 threads `true` and `false` labels through boolean translation. **Our `gen_shortcircuit` uses one label and a copy.** Give an expression where the book's approach emits fewer instructions.
3. Cyan's `&&` must not evaluate its right operand. **Is that a rule about the grammar, the type system, or the semantics?** *(The Cyan Language Reference §4 answers it.)*

**On §8.4**

4. The leader rules identify block boundaries. **Do they detect unreachable code?** Construct an example and say what an extra pass would need to do.
5. §8.4.2 builds the flow graph from the blocks. **Which instruction kinds create more than one successor edge**, and which create none?

**On §9.2**

6. Reaching definitions uses **union**; available expressions uses **intersection**. **Give a two-path CFG and an expression where using union for availability generates wrong code.**
7. Liveness is a **backward** analysis. **Why can it not be computed forwards?** Answer in terms of what the question is asking about.
8. §9.2's algorithms all iterate to a fixed point. **Why does each terminate?** Name the quantity that changes monotonically.
9. **What does liveness let you do that our Week 4 dead-code pass cannot?** Point at `unused = 99` in L09 §5.

**On the LLVM reference**

10. The `phi` entry says operands must be paired with **incoming blocks**. **Why blocks rather than just values?**
11. `alloca` allocates on the stack. **Why does `clang -O0` emit one per local**, when `mem2reg` will immediately remove them?

---

## Two Things to Check on Your Own Machine

**1. That mem2reg does what L10 says.**

```bash
clang -S -emit-llvm -O0 -Xclang -disable-O0-optnone -o o0.ll gcd.c
opt -passes=mem2reg -S o0.ll
```

**Count instructions before and after.** The reference figures are **23 → 11**, with 3 allocas / 6 loads / 5 stores becoming **2 φ-nodes**.

**2. What a real optimiser does to a foldable function.**

```bash
clang -S -emit-llvm -O1 -o - fold.c
```

**One instruction: `ret i32 19`.** Our folder gets to five. **The difference is liveness**, and it is Week 5's opening subject.

---

*Next week's reading is Dragon §9.1, §9.4–9.6 and Chapter 8's register allocation, plus Appel Ch. 11 on graph colouring — which is the more readable of the two on that topic.*

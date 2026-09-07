# CS 211 · Programming Languages & Compilers I
## Week 4: Intermediate Representations and Code Generation

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, CS 102, MATH 151
**Assessment for this course (overall):** Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%
**This week's deliverables:** **MIDTERM 1** (Wednesday), Lab 4, PS 4, and Quiz 4 (Tuesday, covers Week 3).

> **MIDTERM 1 · Wednesday 20:00–21:15 · 75 marks · 12.5% of the course grade · covers Weeks 0–3.**
> One handwritten A4 sheet, one side. **This week's IR material is not examined on it.**

---

### Why This Week Exists

Because the AST is the wrong shape for everything that comes next.

**The tree hides control flow inside nesting.** An `if` inside a `while` is two levels of structure, and asking "what can run before this statement" means understanding both. **An IR makes control flow explicit, as a graph** — and every optimisation in Weeks 5 and 11 is a query against that graph.

This is also the week the course crosses over. **Weeks 0–3 asked what the program says. From here it asks what machine will run it**, and the midterm sits exactly on the seam.

---

### Learning Objectives

By the end of Week 4, you should be able to:

1. Explain why the back end leaves the AST.
2. Lower Cyan to three-address code, including all statements and expressions.
3. **Lower `&&` and `||` to branches**, and say what breaks if you do not.
4. Identify **leaders** and split an instruction list into basic blocks.
5. Build a **CFG** with predecessors and successors, and recognise a loop header.
6. Explain **SSA**, what *static* means, and what a **φ-function** records.
7. Read LLVM's φ-nodes and state the loop-carried dependency each one expresses.
8. Describe **dataflow analysis** as one algorithm parameterised by direction and merge operator.
9. Say why **liveness is backward**, and why "might" takes union and "must" takes intersection.
10. **Implement constant folding that matches your language's semantics**, and explain why an optimiser producing different answers is worse than one that crashes.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L09 Three-Address Code and the Control-Flow Graph]] | TAC, short-circuit lowering, basic blocks, our CFG against LLVM's, constant folding, fixed-point iteration |
| [[L10 SSA Phi Functions and Dataflow Analysis]] | SSA, φ, **mem2reg measured at 23→11 instructions**, dataflow as one algorithm, dominance frontiers |
| [[CS211 Week4/assignments/MIDTERM 1\|MIDTERM 1]] | **The paper.** 75 marks, Weeks 0–3 |
| [[PS 4 TAC Generation and Constant Folding]] | Lowering by hand, SSA by hand, and the IR generator |
| [[QUIZ 4 Week 4 Tuesday]] | **Covers Week 3.** Last calibration before the midterm |
| [[LAB 4 Building and Reading a CFG]] | Match our CFG to LLVM's, run mem2reg, then break the folder in the way that matters |
| `lab/tac.py` · `lab/opt.py` | The IR generator and the folder |
| `lab/gcd.cy` · `lab/gcd.c` · `lab/fold.cy` | The worked examples, in both languages |
| [[CS211 Week4/resources/MIDTERM 1 Revision Guide\|MIDTERM 1 Revision Guide]] | What to put on your one sheet, and twelve self-test questions |
| [[CS211 Week4/resources/Reading Guide Week 4\|Reading Guide Week 4]] | Dragon Ch. 6, §8.4, §9.2–9.3, and the LLVM Language Reference |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**An optimisation that produces a different answer is not a slow compiler. It is a wrong one.**

Change the constant folder's `/` from Cyan's truncating division to Python's floor division — a one-character edit — and `-7 / 2 * 100 + -7 % 2` folds to **`-401`** instead of the correct **`-301`**. *(Measured.)*

**No error appears.** The compiler is happy, the program runs, and it computes something the source never asked for. **Every test that does not exercise negative division passes.**

This is the failure mode that makes back ends hard. **A crash tells you immediately; a wrong constant tells whoever is unlucky, months later, in production.** It is also why L09 insists the folder implement *Cyan's* semantics rather than its host language's — and why the answer to Lab 4 Q15 is worth more than the code that provoked it.

---

### Assessment Reminder

**Labs and quizzes carry no weight**, and both are required. **Quiz 4 is sat Tuesday and covers Week 3. Midterm 1 is Wednesday evening.** **Lab 4 is Friday**, after the midterm, and is not examined on it.

Both the lab and the quiz are tracked in [[_CS 211 Lab and Quiz Record]]. **The midterm is a weighted component** and goes in [[CS 211]].

---

### Connections

**Back:** **Fixed-point iteration appears for the third time** — after ε-closure in Week 1 and FIRST/FOLLOW in Week 2. **PS 3's `e.ty` annotations are read here** to choose instructions: `+` on `int` and `+` on `string` become different opcodes.

**Sideways:** **CS 201 Week 5** covers pipelining and hazards, which is what the instructions this phase emits will run into. CS 201's `idiv` is why Cyan's `/` truncates, and therefore why this week's folder must too.

**Forward:** **Week 5 implements the liveness analysis** this week's dead-code pass was missing, and uses it for both DCE and register allocation. **Week 11 replaces our TAC with real LLVM IR** and hands it to `llc` — the CFG built here is the one that survives to the end of the course.

---

*CS 211 · Week 4 · © CSE Department*

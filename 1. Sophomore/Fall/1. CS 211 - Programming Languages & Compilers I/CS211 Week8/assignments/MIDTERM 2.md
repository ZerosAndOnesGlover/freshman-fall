# CS 211 · Midterm Examination 2
## Programming Languages & Compilers I

---

**Week 8 · Tuesday 28 October · 20:00–21:15 · 75 minutes**
**Covers Weeks 4–7** — intermediate representations, optimisation, runtime systems, and the lambda calculus.
**Weight: 12.5% of the course grade**

**Permitted:** one handwritten sheet of A4, **one side**. No devices.
**Total: 75 marks** — one mark per minute; budget accordingly.

**Name:** _________________________________ **Student ID:** ___________________

---

> **Answer all five questions.** Marks are shown per part. Where a question asks you to *explain*,
> a correct answer with no reasoning earns roughly half.
>
> **Q5 is the synthesis question** and is deliberately open. Attempt it even if you are short of
> time — a partial argument scores.
>
> Several questions ask for a number you measured in a lab or problem set. **An approximate figure
> with the right reasoning scores full marks; an exact figure with no reasoning does not.**

---

## Q1 · Intermediate Representations (15 marks)

**(a)** *(3)* Lower this statement to three-address code:

```cyan
a[i + 1] = b.count * 2;
```

State how many temporaries you used, and name the one instruction whose destination operand is **read** rather than written.

**(b)** *(3)* State the three rules that define a **leader**, and apply them: how many basic blocks does the following contain?

```
    t0 = x < y
    ifz t0 goto L2
    t1 = 1
    goto L3
L2:
    t1 = 2
L3:
    ret t1
```

**(c)** *(4)* Rewrite that fragment in **SSA form**, inserting a φ-function where one is needed.

Then answer: **a φ-function is not an executable instruction.** Say what it records, and what a back end must do with it before generating machine code.

**(d)** *(5)* Dataflow analysis is one algorithm with two knobs.

- Name both knobs and give their settings for **liveness**, **reaching definitions**, and **dominance**.
- One of those three is a *must* analysis. Say which, and explain why its sets must be initialised **full** rather than empty. Your answer should say what the fixed point converges to if you initialise it the other way.

---

## Q2 · Optimisation (15 marks)

**(a)** *(4)* Week 4's `Instr.uses` decided whether an operand was a variable by examining the operand. It was wrong in two directions.

- Give the opcode it treated **unsoundly** and say which slot it failed to inspect.
- Give an opcode it treated **conservatively** and say what it mistook for a variable.
- **Which is worse, and why?** Use the words *conservative* and *unsound* correctly.

**(b)** *(4)* Dragon §9.5.3's first condition for hoisting an instruction out of a loop is that its block **dominates every exit** of the loop.

Draw the two blocks needed to show that this condition hoists **nothing** out of an ordinary `while` loop, and identify the exit edge that defeats it.

**(c)** *(3)* LLVM hoists `k * 2 + 1` out of a loop that may execute zero times, and refuses to hoist `100 / k` out of the same loop.

State the rule that distinguishes them in one sentence. **It is not a rule about loops.**

**(d)** *(4)* A function's interference graph has 18 nodes, and the largest set of variables simultaneously live at any point is 7. Chaitin's algorithm colours it with 7 registers and no spills.

- Is a zero-spill colouring at `k` = peak liveness guaranteed in general? Name the complexity result you are relying on.
- Peak liveness is a **bound** on the registers required. Say which kind — upper or lower — and why.

---

## Q3 · Runtime Systems (15 marks)

**(a)** *(3)* An object's reference count is **zero**. What may a collector conclude? The count is **three**. What may it conclude?

Give a four-object heap in which the second conclusion is wrong, and say how many of the four a tracing collector would reclaim.

**(b)** *(4)* A tracing collector needs a **root set**.

- Name the compiler analysis that produces it and the week you wrote it.
- That analysis was written for a completely different purpose. Name the purpose, and state the one question both consumers are asking.
- The collector **cannot check the root set it is given**. Explain the consequence in one sentence.

**(c)** *(4)* Two root policies are measured on the same program with the same collector and threshold. Peak live memory is **identical**; one retains far more garbage.

- Explain how both can be true.
- Name a measurement that would expose the difference, and say what it measures.

**(d)** *(4)* A generational collector never scans the old generation during a minor collection.

- Name the mechanism that stops it freeing a young object an old object points to, and the set it maintains.
- There is one old-to-young pointer that mechanism **cannot** catch. Describe how it comes into existence, and say why no write barrier could ever see it.

---

## Q4 · The Lambda Calculus (15 marks)

**(a)** *(3)* Reduce to normal form, showing each step:

```
(λx y. y x) a (λz. z)
```

**(b)** *(4)* `(λx y. x) y` reduces in one step to `λy′. y` under capture-avoiding substitution, and to `λy. y` under naive substitution.

- Say what **function** each result is — not what it looks like.
- Name the phenomenon, and name the Week 3 concept it is an instance of.
- Explain in one sentence why this failure is more dangerous than a crash.

**(c)** *(4)* `Y = λf. (λx. f (x x)) (λx. f (x x))`.

- Reduce `Y g` by one step and state the equation it satisfies.
- Under **call-by-value** `Y` diverges. Explain why, naming the subterm that is repeatedly evaluated.
- `Z` is `Y` with one eta-expansion and it does not diverge. **Two terms that are the same function behave differently.** Say precisely what "the same function" is a claim about, so that this is not a contradiction.

**(d)** *(4)* In the Church encoding, `zero`, `false` and `nil` are the **same term**.

- Write the term.
- Explain in one sentence what a program has returned when it returns it.
- `mult` and `compose` are also the same term. **That one is a different kind of fact from the first.** Explain the difference.

---

## Q5 · Synthesis (15 marks)

Weeks 4 to 7 contain the same argument four times.

- Week 4's constant folder turned `−301` into `−401`.
- Week 5's dead-code pass deleted an instruction the program needed.
- Week 6's collector freed an object the next instruction wrote through.
- Week 7's naive substitution turned a constant function into the identity.

**(a)** *(5)* Each of those is a *silent* failure — the program ran and produced a plausible wrong answer. For **two** of them, state the specific mechanism by which the error was made invisible: what the developer would have seen, and what they would not have.

**(b)** *(5)* Three of the four trace to the same root cause, in the same table. Identify the table, state the entry that was wrong, and explain how the *severity* of that single mistake changed as the phase consuming it changed.

**(c)** *(5)* A colleague proposes that these are all testing failures, and that a sufficiently thorough test suite would have caught them.

**Argue for or against**, using at least two concrete examples from Weeks 4–7. A good answer will engage with the specific reasons each defect evaded observation, and will say what — if anything — would have been more effective than more tests.

---

## Mark Distribution

| Question | Topic | Marks |
|---|---|---|
| Q1 | Intermediate representations — Week 4 | 15 |
| Q2 | Optimisation — Week 5 | 15 |
| Q3 | Runtime systems — Week 6 | 15 |
| Q4 | The lambda calculus — Week 7 | 15 |
| Q5 | Synthesis — Weeks 4–7 | 15 |
| **Total** | | **75** |

---

**End of paper.**

*CS 211 · Midterm Examination 2 · © CSE Department*

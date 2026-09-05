# CS 211 · Final Examination
## Programming Languages & Compilers I

---

**Tuesday 16 December · 09:00–11:30 · 150 minutes · VNC 100**
**Comprehensive — Weeks 0–12.**
**Weight: 20% of the course grade**

**Permitted:** one handwritten sheet of A4, **both sides**. No devices.
**Total: 150 marks** — one mark per minute; budget accordingly.

**Name:** _________________________________ **Student ID:** ___________________

---

> **Answer all seven questions.** Marks are shown per part.
>
> **Section A (Q1–Q4, 80 marks)** is the pipeline, front to back. **Section B (Q5–Q6, 40 marks)**
> is the runtime and the theory. **Q7 (30 marks) is synthesis** and is deliberately open.
>
> Where a question asks for a measured figure, **the reasoning carries the marks**. An approximate
> number with a correct explanation scores full; an exact number alone does not.
>
> **Budget check:** if you are not starting Q5 by 10:20, move on. Q7 is 30 marks and is the part
> people run out of time for.

---

# Section A · The Pipeline (80 marks)

## Q1 · Front End (20 marks)

**(a)** *(4)* Give a context-free grammar for a language of comma-separated lists of integers, permitting the empty list. Then show your grammar is **unambiguous**, or give a string with two parse trees.

**(b)** *(4)* State the **maximal munch** rule. Give a token stream where it produces a different result from shortest-match, and name a *second* place in this course where the same greedy algorithm appears.

**(c)** *(4)* This grammar is not LL(1):

```
E → E + T | T
T → id
```

- Say precisely why.
- Rewrite it so a recursive-descent parser terminates.
- Your rewrite changes the **shape** of the parse tree. Say how associativity is recovered.

**(d)** *(4)* Give a Cyan program that lexes and parses successfully and is rejected by the type checker. State the rule it violates and the message you would want.

**(e)** *(4)* **Hindley-Milner.** Infer the principal type of `λf. λx. f (f x)`, showing the unification steps. Then say why `λx. x x` has no type, naming the check.

---

## Q2 · Intermediate Representations (20 marks)

**(a)** *(4)* Lower to three-address code:

```cyan
if a < b { c = a * 2; } else { c = b + 1; }
```

State how many basic blocks the result has, and name the three leader rules.

**(b)** *(5)* Convert your answer to **SSA**, inserting a φ where one is needed.

- Say what the φ records.
- A φ is **not executable**. Say what the back end does with it, and when.

**(c)** *(5)* Dataflow analysis is one algorithm with two knobs.

- Name both, and give the settings *and initial values* for **liveness**, **reaching definitions** and **dominance**.
- Explain why a *may* analysis starts empty and a *must* analysis starts full, **in terms of which fixed point is reached**.

**(d)** *(6)* Week 4's `Instr.uses` decided what an operand was by looking at its shape.

- Name the opcode it treated **unsoundly** and the slot it failed to inspect.
- That single mistake had three consumers in this course. **Name all three and the symptom in each.**
- State the general principle relating the *soundness* of an analysis to the *phase that consumes it*.

---

## Q3 · Optimisation and Code Generation (20 marks)

**(a)** *(4)* Draw the two blocks needed to show that Dragon §9.5.3's first condition hoists **nothing** from an ordinary `while` body, and identify the defeating edge.

**(b)** *(4)* LLVM hoists `k * 2 + 1` from a loop that may run zero times, and refuses to hoist `100 / k`. State the rule. **It is not a rule about loops.**

**(c)** *(4)* An interference graph has 20 nodes; peak simultaneous liveness is 6.

- Is peak liveness an upper or a lower bound on registers required? Why?
- Is a zero-spill colouring at *k* = 6 guaranteed? Name the complexity result.

**(d)** *(4)* `llvmgen.py` gives every variable an `alloca` and every access a `load` or `store`, producing deliberately poor IR.

- Why is this the right decision for a front end?
- Name the LLVM pass that repairs it and the **Week 4 algorithm** it runs.

**(e)** *(4)* From one IR, `llc` produced 8 instructions for aarch64 and 16 for riscv64, where the riscv64 output contains `call __moddi3`.

Explain **both** numbers in terms of the instruction sets, and state LLVM's *m* × *n* → *m* + *n* argument.

---

## Q4 · Semantics and Evaluation (20 marks)

**(a)** *(4)* Reduce to normal form, showing each step:

```
(λf. λx. f (f x)) (λy. y + 1) 3
```

*(Treat `+` and numerals as primitives.)*

**(b)** *(5)* `(λx y. x) y` reduces to `λy′. y` correctly and to `λy. y` under naive substitution.

- Say what **function** each result is.
- Name the phenomenon, and the Week 3 concept it is an instance of.
- Name **two** systems in this course where the same bug appears, one of them not a lambda calculus.

**(c)** *(5)* `Y g = g (Y g)`.

- Show one reduction step establishing it.
- Explain why `Y` diverges under call-by-value, naming the subterm.
- `Z` is `Y` eta-expanded and terminates. State precisely what "the same function" claims, such that this is not a contradiction.

**(d)** *(6)* In the Church encoding, `zero`, `false` and `nil` are the **same term**, and so are `mult` and `compose`.

- Write the shared term for the first group.
- **Those are two different kinds of fact.** Explain the difference.
- Running Hindley-Milner over these definitions **does not separate either group.** Explain why not, and name what does.

---

# Section B · Runtime and Theory (40 marks)

## Q5 · Memory and Concurrency (20 marks)

**(a)** *(4)* A reference count is zero; then three. What may a collector conclude in each case? Draw a heap where the second conclusion is wrong.

**(b)** *(4)* A tracing collector needs a **root set**.

- Name the analysis that produces it, the week you wrote it, and its **original purpose**.
- State the one question both consumers are asking.
- The collector cannot check what it is given. State the consequence.

**(c)** *(4)* A generational collector never scans the old generation during a minor collection.

- Name the mechanism that stops it freeing a young object an old one points to.
- Describe the one old-to-young pointer that mechanism **cannot** catch, and say why no write barrier could see it.

**(d)** *(4)* Two threads, `x` and `y` initially 0:

```
T0:  x = 1;  r1 = y;          T1:  y = 1;  r2 = x;
```

- Prove `r1 == r2 == 0` impossible under sequential consistency.
- It occurs on x86 roughly once in ten thousand iterations. Name the hardware cause and the reordering.

**(e)** *(4)* At `-O2`, gcc compiled a racy spin-wait into `.L6: jmp .L6`.

- Name the optimisation and the week you met it.
- State **why the compiler was entitled to do this**, using the phrase *undefined behaviour* correctly.

---

## Q6 · Types, Proofs and Metaprogramming (20 marks)

**(a)** *(4)* `let i = λx. x in i i` typechecks; `(λi. i i) (λx. x)` does not, and **both reduce to `λx. x`**.

- Name the property this demonstrates and say what it is incomplete *with respect to*.
- Explain the mechanism — what differs between the two in the type environment.

**(b)** *(4)* `member : Eq a => a -> [a] -> Bool` elaborates to `member : DictEq a -> a -> [a] -> Bool`.

- Say what a class, an instance and a constraint each become.
- `Eq [[Int]]` resolves to `(dEq_ListListInt (dEq_ListInt dEq_Int))` and nobody wrote that instance. Explain.
- Say **when** a missing instance is reported.

**(c)** *(4)* Under Curry-Howard, the proof of `A → B → A` is `λp q. p`.

- Name that function; you met it in Week 7 under a different name.
- `A ∨ ¬A` has **no** proof. Explain why, in terms of what a proof of a disjunction must *be*.
- Assuming it as an axiom makes every classical tautology provable. Say what `lem` then is in the proof term.

**(d)** *(4)* A macro can be `unless`; a function cannot.

- State the two differences between a macro and a function.
- `(swap-bad tmp z)` returns `(7 7)` rather than `(7 100)`. Name the bug and the fix.
- Name what the fix corresponds to in Week 7's substitution.

**(e)** *(4)* A total language cannot have `Y`.

- Explain, naming which of the occurs check and strong normalisation is the *mechanism* and which the *reason*.
- OCaml has recursion. How?

---

# Q7 · Synthesis (30 marks)

**(a)** *(10)* **The same table, three consumers.**

Week 4's def/use model was wrong in one entry. It fed dead-code elimination, register allocation and a garbage collector's root set.

- Give the symptom in each of the three.
- **Rank them by severity and justify the ranking.**
- State the general principle. It should be one sentence and should mention *soundness*.

**(b)** *(10)* **Silent failure.**

This course contained at least seven defects that produced a plausible wrong answer with no diagnostic: the constant folder; dead-code elimination; the collector's root set; the promotion fix-up; naive substitution; the racy spin-wait; and a test suite that passed because `0 == False`.

- Choose **three**. For each, state the *mechanism of invisibility* — what the developer saw and what they did not.
- **At least four of those seven were invisible because an instrument agreed with the bug.** Name two such instruments and what each was really measuring.
- Give the habit you would take from this, and say why "write more tests" is not sufficient. Use a measured figure.

**(c)** *(10)* **A language design argument.**

You are advising a team building a systems language for embedded and browser targets.

- Name **two** guarantees you would make the language enforce, and for **each**, say what it makes impossible, what it costs, and **who pays** — machine, programmer, or user.
- One of your guarantees will reject programs that are in fact correct. **Say which, give an example, and defend it.**
- Name the compilation target you would choose and justify it with evidence from this course.

*A well-argued answer that disagrees with the lectures scores full marks. A confident answer with no evidence scores very little.*

---

## Mark Distribution

| Question | Topic | Weeks | Marks |
|---|---|---|---|
| Q1 | Front end | 0–3 | 20 |
| Q2 | Intermediate representations | 4 | 20 |
| Q3 | Optimisation and code generation | 5, 11 | 20 |
| Q4 | Semantics and evaluation | 7 | 20 |
| Q5 | Memory and concurrency | 6, 9 | 20 |
| Q6 | Types, proofs, metaprogramming | 8, 10 | 20 |
| Q7 | Synthesis | all | 30 |
| **Total** | | | **150** |

---

**End of paper.**

*CS 211 · Final Examination · © CSE Department*

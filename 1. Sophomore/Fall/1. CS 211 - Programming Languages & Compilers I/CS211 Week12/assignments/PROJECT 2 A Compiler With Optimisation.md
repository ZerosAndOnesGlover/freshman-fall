# CS 211 · Project 2
## A Compiler With Optimisation

---

**Assigned:** Week 11 · **Due:** Week 12, Friday 17:00
**Weight: 12.5% of the course grade** · Individual work
**Submit:** a `.zip` of your compiler plus a PDF report, `PROJ2_{LastName}_{StudentID}.pdf`
**Demoed in Lab 12.**

> **This extends Project 1. It is not a new compiler.** If Project 1 works, this is two weeks of
> additions to it. If Project 1 does not work, **fix it first** — Part A is mostly Project 1
> finished, and it is worth more here than the feature was there.
>
> **Thanksgiving recess falls in the middle** (no classes Nov 24). Plan for eleven working days,
> not fourteen.

---

## What You Are Building

**A compiler that produces code, and makes it better.**

Project 1 added one language feature through the front end. Project 2 takes your compiler to the back: it must **emit LLVM IR, run, and optimise** — and you must be able to say what your optimiser did and prove it did not change the answer.

The scaffolding is in `CS211 Week11/lab`: `cyanc.py` drives nine phases and `llvmgen.py` lowers `int` and `bool`. **You are extending both.**

---

## Part A — It Compiles and Runs (30 marks)

**Required.** Everything else assumes it.

1. **Your Project 1 feature reaches machine code.** If it parses and type-checks but `llvmgen.py` refuses it, lower it. If it genuinely cannot be lowered without Part C, say so explicitly and lower everything else.
2. **Multiple functions**, so calls and recursion work. `llvmgen.py` currently emits one function.
3. **A test suite that runs in one command** and checks *answers*, not just exit status. At least **twelve** programs.
4. **Differential testing against `runtime.py`.** Every test must produce the same answer under the Week 6 interpreter and under `lli`. **Ship the script that checks this.**

*Part A alone, done properly, is a pass.*

---

## Part B — Optimisation (35 marks)

**At least three passes**, at least one of which operates on the CFG rather than on a straight-line list.

Suggested, in rough order of difficulty:

| pass | operates on | notes |
|---|---|---|
| constant folding + propagation | instruction list | you have this from Week 4 |
| dead-code elimination | liveness | you have this from Week 5 |
| common subexpression elimination | basic block, or CFG | value numbering is the usual route |
| loop-invariant code motion | natural loops | PS 5; **mind the trap predicate** |
| strength reduction | instruction list | `x * 2` → `x << 1` |
| tail-call elimination | CFG | turns recursion into a loop |

For **each** pass:

- **State the precondition** — what must be true for it to be safe.
- **Report instruction counts** before and after, on at least four programs.
- **Verify the answers are unchanged**, differentially, on every test.

And then, honestly:

- **Run `opt -O2` after your passes.** Report whether your work changed the final output at all.
- **It very often will not.** That is an expected and reportable finding, not a failure — but you must say so plainly rather than omitting the comparison.

---

## Part C — Choose One (20 marks)

Pick **one** and do it properly. A half-finished second one scores nothing.

**C1 · Heap data.** Arrays and structs in the back end: `malloc`, an object layout you write down, `getelementptr`, and bounds checking. Report what `-O2` does to your bounds checks.

**C2 · Closures.** First-class functions that capture their environment. Week 7 §12 is the design; the captured variables must be heap-allocated, and you must say why.

**C3 · A second back end.** Emit for a target LLVM does not give you free — a stack machine, a bytecode VM you also write, or WebAssembly text. Report the instruction counts against LLVM's for the same programs.

**C4 · Garbage collection at the IR level.** Port Week 6's collector so that compiled code can allocate and collect. You will need stack maps; L14 §2 says why the compiler is the only thing that can produce them.

---

## Part D — Report (15 marks)

**Six to ten pages.** Not a diary.

| | marks |
|---|---|
| What you built, and what it does not do | 3 |
| **Each optimisation: precondition, counts, and the correctness argument** | 5 |
| The `opt -O2` comparison, honestly reported | 3 |
| Your Part C choice: design, and what surprised you | 2 |
| **What is still wrong** | 2 |

**"What is still wrong" is worth 2 marks and is the strongest signal in the whole submission.** A precise account of a limitation you understand beats a claim of completeness that the marker disproves in five minutes — and this has decided grades in both directions every year.

---

## Marking

| Component | Marks |
|---|---|
| Part A — compiles, runs, differentially tested | 30 |
| Part B — three passes, measured and verified | 35 |
| Part C — one extension, done properly | 20 |
| Part D — report | 15 |
| **Total** | **100** |

### Bonus, up to +8 (capped at 100)

- **+4** — a pass of your own that `opt -O2` **does not** subsume, with the counts to prove it.
- **+2** — a fuzzer generating random programs and checking interpreter against JIT.
- **+2** — compile-time measurements of your own passes, profiled rather than guessed.

---

## Practical Advice

**Do Part A before touching Part B.** An optimiser on a compiler that does not run is unmarkable, and every year somebody submits one.

**Write the differential test script first.** It is twenty lines, it makes Part B safe to attempt, and it is the difference between "I think it still works" and knowing.

**Do not fight `opt -O2`.** You are not going to beat it, and Part B does not ask you to — it asks you to build passes, measure them, and say what happened. **The honest comparison is worth more marks than a flattering one.**

**Demo day is Lab 12.** Have something that runs from a clean checkout in one command. "It works on my machine, let me just…" is the most common way to lose the demo marks.

---

*CS 211 · Week 12 · Project 2 · © CSE Department*

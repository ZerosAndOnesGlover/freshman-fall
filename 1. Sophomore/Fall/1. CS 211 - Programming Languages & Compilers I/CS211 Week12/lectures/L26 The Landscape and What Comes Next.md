# CS 211 · Programming Languages & Compilers I
## Week 12 · Lecture 2 of 2
### The Landscape, and What Comes Next

*“Here is a language so far ahead of its time, that it was not only an improvement on its predecessors, but also on nearly all its successors.”* — C. A. R. Hoare, on ALGOL 60, "Hints on Programming Language Design" (1973)

---

**Reading:** Haas et al. (2017), "Bringing the Web up to Speed with WebAssembly" · Steele (1998), "Growing a Language" · **Next:** the final exam, and then whatever you build

**Coursework:** 📋 **Project 2** due Fri this week 17:00 · 📝 **PS 11** due Fri this week 17:00 · 📝 **PS 12** due Fri this week 17:00 · 🔬 **Lab 12** Fri this week 14:00–15:50 · 📕 **Final exam** Tue of finals week 09:00–11:30

---

## 1. Every Language Is Becoming the Same Language

Twenty years ago the paradigms were tribes. Now:

| feature | arrived in |
|---|---|
| **lambdas / closures** | Java 8 (2014), C++11, C# 3.0, Python 1.0, Go 1.0 |
| **type inference** | C++11 `auto`, Java 10 `var`, C# `var`, Go `:=` — all Week 8's algorithm, restricted |
| **pattern matching** | Java 21, Python 3.10, C# 8, Rust, Scala |
| **algebraic data types** | Rust, Swift, TypeScript unions, Java sealed interfaces |
| **`async`/`await`** | C# 5, Python 3.5, JavaScript ES2017, Rust 1.39, Swift 5.5 |
| **`Option`/nullable types** | Kotlin, Swift, C# 8, TypeScript `strictNullChecks`, Java `Optional` |
| **traits / type classes** | Rust traits, Swift protocols, Scala implicits, Java default methods |

**Every row is something this course covered**, and every row started in a research language and arrived in a production one fifteen to forty years later.

The convergence is real, and it is worth being precise about what converged. **Not the paradigms — the *checkable guarantees*.** What spread was: functions as values, types the compiler can infer, exhaustiveness the compiler can verify, and nullability the compiler can track. **The features that won are the ones a compiler can check**, which is a much narrower claim than "everyone became functional".

*Hoare's billion-dollar mistake is the clearest case. `Option` did not spread because it is elegant; it spread because the alternative is an error the compiler cannot see.*

---

## 2. WebAssembly

The most interesting thing in the landscape, and the one most directly continuous with Week 11.

**WebAssembly is a compilation target, not a language.** A portable binary format with a stack machine, structured control flow, linear memory, and a specification small enough to have been **formally verified** — which no mainstream bytecode before it was.

You have already produced some. Week 11's target table:

```
$ llc -march=wasm32 -filetype=asm gcd.ll
  wasm32      23 instructions      block / br_if / return
```

**Twenty-three instructions, from the language we invented.** And the reason it is 23 rather than x86-64's 12 is the interesting part: **WebAssembly has structured control flow** — `block`, `loop`, `br_if` — and no arbitrary jumps. The back end has to *reconstruct* the structure that Week 4's CFG deliberately threw away, an algorithm known as the relooper.

> **We can go one step further than Week 11 did, and one step less far than we would like.**
> `llc -march=wasm32 -filetype=obj` produces a valid wasm object here — 187 bytes. Linking it into
> a runnable module needs `wasm-ld`, which is not installed on these machines, and `node` (which
> *is* installed, and does run WebAssembly) therefore has nothing to load. **The missing piece is
> a linker, not a compiler.** Say that rather than implying we ran it, and note that PS 12 does
> not require you to.

Why it matters beyond browsers:

- **A universal target.** C, C++, Rust, Go, C#, Swift and Python all compile to it. Java's "write once, run anywhere" at a performance cost people would not pay; WebAssembly is the same promise with the cost mostly removed.
- **A sandbox by construction.** No ambient authority: a module gets linear memory and the imports it was given, and nothing else. WASI is the interface for giving it files and sockets deliberately.
- **Outside the browser.** Edge compute, plugin systems, database UDFs, and serverless — anywhere you want to run somebody else's code without trusting it.

**The honest limitations:** the GC proposal only recently landed, so garbage-collected languages long had to ship their own collector *inside* the module — which is Week 6's collector, compiled to WebAssembly, with the stack-map problem of Week 11's PS 11 Part C. Threads, exceptions and tail calls all arrived late for similar reasons.

---

## 3. Where Compilers Are Going

**Better diagnostics as a first-class goal.** Rust's error messages changed the industry's expectations, and Week 10 §L22.5 measured the underlying trade: the combinator grammar was 4 lines against 357, and its errors were unusable. **clang, rustc and GHC all hand-write their parsers to keep the diagnostic.** Elm, Rust and modern clang treat the error message as the product.

**Incremental and query-driven compilation.** `rustc` and the Roslyn compilers are structured as *queries with caching* rather than passes over a whole program, because an IDE recompiles on every keystroke. That is a genuine architectural break from the pipeline in Week 11's diagram — the same phases, arranged as a demand-driven graph.

**The language server.** LSP means the compiler front end is now a *service*: the same parser and type checker answer "what type is this", "where is this defined" and "rename this", live. **Your Week 3 symbol table and Week 8 inference are what a language server is made of.**

**Formal verification in production.** CompCert is a C compiler proved to preserve semantics. seL4 is an OS kernel with a machine-checked correctness proof. Both are Week 8 §L18.7's Curry-Howard correspondence, industrialised: the proof *is* a program, and the type checker *is* the proof checker.

**And machine learning, in two directions.** As a *consumer* of compilers — every ML framework is a compiler now (XLA, TorchInductor, TVM), doing Week 5's loop optimisations on tensor code. And as a *tool* inside them, for inlining and phase-ordering decisions, which is Week 5 §9's problem being attacked with search because nobody has a good rule.

---

## 4. What This Course Was

Twelve weeks, nine phases, and one program that runs:

```
source → tokens → AST → typed AST → TAC → CFG → optimised → liveness → registers → LLVM IR → 21
```

**The phases are the syllabus. The through-lines are the course.**

**Fixed-point iteration**, six times: ε-closure (W1), FIRST/FOLLOW (W2), constant folding (W4), liveness and dominators (W5), the marker (W6), unification (W8). *One algorithm, six problems.*

**One def/use table**, feeding dead-code elimination (W5), register allocation (W5), and the garbage collector's root set (W6) — and being wrong in all three at once, with the severity set by whichever phase consumed it.

**Sound and incomplete**, five times: liveness's *may* (W5), reference counting (W6), Hindley-Milner (W8), the C standard's refusal to define races (W9), and Rust's borrow checker (W12). *Every static analysis approximates, and always in the safe direction, because Week 7 §13 says exactness is undecidable.*

**Silent failure**, every single week: `−301` became `−401`; a live `load` was deleted; a reachable object was freed and the right answer printed; a constant function became the identity; `jmp .L6`; a boolean test suite passed because `0 == False`; a phase timer measured `fork`.

> **If one habit survives this course, make it that one.** Not "write more tests" — Week 9 measured
> a bug that appears once in five thousand runs. **Check the property, not a sample of the
> outcomes**, and be suspicious of a number that is plausible. Week 5's printer, Week 6's peak RSS,
> Week 7's `0 == False`, Week 9's cache line and Week 11's subprocess were all instruments
> agreeing with a bug.

---

## 5. What to Read Next

**If you liked the front end** — Aho et al. properly, cover to cover; Cooper & Torczon's *Engineering a Compiler*, which is better on the back end.

**If you liked types** — Pierce's *TAPL*, then *Advanced TAPL*. Then write something in Agda or Lean and find out what dependent types cost.

**If you liked the runtime** — the *Garbage Collection Handbook*, and then read HotSpot's or V8's source, which is more approachable than its size suggests.

**If you liked the theory** — Barendregt on the lambda calculus, Harper's *Practical Foundations for Programming Languages*, and Wadler on parametricity.

**If you want to build something** — write a language. Not a good one; a small one, finished. **You already have.** `cyanc.py` is 1,300 lines and produces working x86-64, and the difference between that and a language people use is mostly the parts this course listed and skipped: error recovery, debug information, a module system, and a standard library.

---

## 6. What to Take From This

1. **The paradigms converged, and what converged were the *checkable guarantees*** — not styles, but the features a compiler can verify.
2. **WebAssembly is Java's promise with the performance cost mostly removed**, and it is a sandbox by construction.
3. **Our compiler emits wasm32 in 23 instructions**, and the extra instructions are structured control flow being reconstructed from a CFG.
4. **We can produce a wasm object here but not link one** — `wasm-ld` is absent. A missing linker, not a missing compiler.
5. **Diagnostics became a first-class goal**, and Week 10 measured why that costs something.
6. **Compilers became services** — your Week 3 symbol table is what a language server is made of.
7. **Verified compilers are Curry-Howard industrialised.**
8. **Fixed-point iteration appeared six times; sound-and-incomplete five.**
9. **Every week contained a silent failure**, and the instrument agreed with the bug more often than not.
10. **You have written a compiler.** The gap to a real one is a list, and you can now read it.

**The final exam is comprehensive and covers Weeks 0–12.** [[CS211 Week12/resources/FINAL EXAM Revision Guide|FINAL EXAM Revision Guide]] says what is on it and in what proportion.

---

*CS 211 · Week 12 · Lecture 26 · © CSE Department*

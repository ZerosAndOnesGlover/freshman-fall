# CS 211 · Programming Languages & Compilers I
## Course Overview & Week-by-Week Road-map
### Year 2 · Fall · 4 credits (3 lecture + 1 lab)

---

## The Course

**You have used four languages in a year and never once asked who decided what they let you say.**

CS 211 asks that question and then answers it the only way that sticks: by building the thing. Over thirteen weeks you will write a complete compiler — lexer, parser, type checker, intermediate representation, optimiser, code generator — for a small language called **Cyan**, and by Week 11 it will emit LLVM IR that runs.

Along the way the course goes underneath the languages you already use. **Why does Haskell not need type annotations? Why does Java pause? Why can Rust free memory without a garbage collector, and why is `unsafe` a keyword rather than a compiler flag? What exactly is a closure, at the level of allocated bytes?** Each of those has a precise answer, and each answer is a design decision somebody made and could have made differently.

**Prerequisites:** CS 101, CS 102 and MATH 151. The last one is not decoration — Week 1 is regular languages and finite automata, Week 2 is grammars and pushdown automata, and both assume you have seen induction, sets and relations and are not frightened by a proof.

---

## Two Habits This Course Is Built Around

**1. Every phase is a translation, and you must be able to name both sides.**

A compiler is not a mysterious box. It is eight small translations in a row, each with an input representation and an output representation you can print and inspect:

```
source text → tokens → parse tree → AST → typed AST → TAC → SSA → LLVM IR → machine code
```

**At every point in this course you should be able to say which of those you are holding.** When something goes wrong — and in a compiler something always goes wrong — the debugging method is to print each representation in turn and find the first one that is not what you expected. That is not a tip; it is the whole method, and Weeks 1 through 5 are it applied eight times.

> The single most common failure mode in this course is debugging a compiler by reading the source
> program. The bug is never in the source program. The bug is in the phase that mangled it, and you
> find that phase by dumping representations, not by staring.

**2. A language design is a set of refusals.**

Every language is defined more by what it forbids than by what it allows. C refuses to check your array bounds and buys you speed. Haskell refuses to let you mutate and buys you equational reasoning. Rust refuses to let two references alias when one can write, and buys memory safety with no garbage collector. Python refuses almost nothing and buys expressiveness at a price you measured in CS 201 — 46× on a summation loop.

**A feature is never free, and "this language is better" is never a complete sentence.** By Week 12 you should be unable to say it without immediately naming what was given up.

---

## Assessment

| Component | Weight | Rule |
|---|---|---|
| **Problem Sets** | **30%** | PS 0–12, released Wednesday, due the following Friday 17:00. Lowest 1 dropped. |
| **Midterm 1** *(Week 4)* | **12.5%** | 75 minutes, covering **Weeks 0–3**. One handwritten sheet, one side. |
| **Midterm 2** *(Week 8)* | **12.5%** | 75 minutes, covering **Weeks 4–7**. Same format. |
| **Project 1** *(due Week 11)* | **12.5%** | The Cyan front end: source to typed IR. Assigned Week 6. |
| **Project 2** *(due Week 12)* | **12.5%** | The Cyan back end: optimisation and LLVM code generation. |
| **Final Exam** | **20%** | 150 minutes, comprehensive. Two handwritten pages. |
| **Total** | **100%** | |

**Labs and quizzes carry no weight.** The curriculum's assessment line — *Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%* — sums to 100% without them, and no percentage has been invented to fill the gap.

**They are still required.** The lab is checked off by the TA in the session, and [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second unexcused absence. That rule, not a mark, is what makes the lab non-optional — because a lab you can skip for a 2% grade cost is a lab you will skip in the week you are busiest, which is reliably the week the material is hardest.

**Quizzes** run ten minutes at the start of **Tuesday's** lecture in **Weeks 1–11**. **Quiz *N* covers Week *N−1*.** The answer key is printed in the paper, below the questions, so the feedback closes in the same sitting rather than three weeks later.

Both are recorded in [[_CS 211 Lab and Quiz Record]].

---

## Schedule

| | When | Where |
|---|---|---|
| **Lectures** | Tuesday & Thursday 08:30–09:45 | TH 205 |
| **Lab** | Friday 14:00–15:50 *(mandatory)* | BH 220 |
| **Office hours** | Monday 14:00–16:00, Friday 11:00–12:00 | TH 422 |

### Two lectures a week, not three — and they are longer

**CS 211 meets twice weekly for 75 minutes**, where CS 201 meets three times for 50. Same contact time, different shape, and the shape matters: **a 75-minute block is long enough to build something end to end in front of you**, which is why the lecture numbering runs L01–L26 rather than to L39.

Plan your reading accordingly. Two lectures a week means each one carries half a week of material rather than a third, and turning up to Thursday's lecture without having absorbed Tuesday's is a considerably worse idea here than it was in CS 201.

### The lab does *not* run a week behind

**Lab *N* covers Week *N* and is sat on the Friday of Week *N*.**

This is the opposite of CS 201, and the reason is nothing more than which days the timetable handed each course. Lectures are Tuesday and Thursday; the lab is Friday afternoon. **Both of the week's lectures have already happened by the time you walk into the lab**, so the lab needs no lead time and takes none.

| Lab | Covers | Sat on |
|---|---|---|
| **Lab 0** | Week 0 | **Friday of Week 0** — the Friday that closes the ten-day Week 0 |
| Lab *N* | Week *N* | **Friday of Week *N*** |
| Lab 12 | Week 12 | Friday of Week 12, and it is the lightning talks |

> **Do not carry CS 201's habit across.** The two courses run in the same term and disagree about
> this, deliberately and for good reason. CS 201's Tuesday lab would otherwise have had only
> Monday's lecture behind it; CS 211's Friday lab has the whole week. Every lab and quiz file in
> this course states both its day and its week in the header — if you are ever unsure, the file
> itself is authoritative.

**Quizzes** are sat at the start of **Tuesday's lecture in Week *N*** and cover **Week *N−1***, which is the same convention CS 201 uses on Mondays. There is no quiz in Week 0 — Quiz 1, in Week 1, covers this week.

**Instructor:** Prof. Chen Wei · c.wei@ist.edu · TH 422
**TA:** Ngozi Eze · neze@ist.edu · Mon 10:00–12:00 and Wed 14:00–16:00, plus Fri 16:00–17:00 straight after the lab

---

## The Spine: One Compiler, Thirteen Weeks

**This course has a spine, and almost every problem set is a vertebra.**

You will define one small language in Week 0 and then compile it, phase by phase, for the rest of the term:

| Week | What you add to `cyanc` | Representation you gain |
|---|---|---|
| **0** | The grammar itself | BNF, and a parse tree on paper |
| **1** | The lexer | tokens |
| **2** | The parser | parse tree → AST |
| **3** | Symbol table and type checker | typed AST |
| **4** | IR generation | three-address code, then a CFG |
| **5** | The optimiser | optimised TAC, allocated registers |
| **6** | The runtime | a heap, and a garbage collector for it |
| **11** | The back end | LLVM IR, and a JIT |

**Weeks 7 to 10 step off the spine deliberately** — lambda calculus, type systems, concurrency and metaprogramming are the theory that explains why the spine has the shape it does, and Week 11 returns to it carrying what they taught. Week 7's closures are the reason Week 6's GC has to trace an environment. Week 8's polymorphism is what your Week 3 type checker was too weak to express.

### Cyan

**Cyan** is the language. It is small enough to compile in a term and large enough to be interesting:

```
fn fib(n: int) -> int {
    if n < 2 { return n; }
    return fib(n - 1) + fib(n - 2);
}
```

Statically typed with inferred locals, first-class functions with closures, integers, booleans, strings, arrays and records. **Every one of those features earns its place**: closures give Week 7 something concrete to point at, heap-allocated records give Week 6's collector something to trace, and inference gives Week 3's Hindley-Milner a reason to exist rather than being a thing you read about.

Source files are `.cy`; the compiler you build is `cyanc`. The full grammar is fixed in **Lecture 2** and does not change afterwards — when Week 8 wants generics, you will extend it yourself, and that is Problem Set 8.

---

## Tools

Everything runs on Linux (Ubuntu 24.04 in BH 220).

| Tool | For | Weeks |
|---|---|---|
| `python3` | the compiler itself — `cyanc` is written in Python | 1–5, 10–11 |
| `flex` | generated lexers, to compare against your hand-written DFA | 1 |
| `bison` | generated LALR(1) parsers, to compare against recursive descent | 2 |
| `ghc` / `ghci` | Haskell, for type inference and the type-theory weeks | 3, 7, 8 |
| `gcc` | the garbage collector, and the C11 memory model | 6, 9 |
| `java` | a real generational collector to profile | 6 |
| `clang`, `opt`, `llc`, `lli` | LLVM IR — reading it, optimising it, running it | 4, 5, 11 |
| `swipl` | Prolog, for one lecture on the logic paradigm | 0 |

**Python is the implementation language for the compiler, and that is a deliberate choice.** Writing a compiler in a language with no types teaches you exactly why the language you are compiling has them. By Week 3 you will have been bitten by a `None` where an AST node should have been, and Week 3 is about the phase that would have caught it.

`cyanc` targets **LLVM IR**, not x86-64 directly. CS 201 taught you to read x86-64; this course is about the layer that decides what x86-64 to emit, and LLVM is where that decision actually lives in every production compiler you will ever use.

---

## Textbooks

**Aho, A., Lam, M., Sethi, R. & Ullman, J. — *Compilers: Principles, Techniques, and Tools*, 2nd ed. (Addison-Wesley, 2006).**
*Primary — "the Dragon Book". Complete and authoritative, and dense enough that you should read it against a specific question rather than front to back. The reading guides tell you which sections and why.*

**Appel, A. — *Modern Compiler Implementation in ML/Java/C* (Cambridge, 1998).**
*Secondary, and frankly the more readable of the two. Any language edition; the C edition is closest to what you already know. When the Dragon Book's treatment of a phase does not land, try Appel's.*

**Abelson, H. & Sussman, G. — *Structure and Interpretation of Computer Programs*, 2nd ed. (MIT Press, 1996).**
*"SICP". Not a compiler book — a book about what evaluation is, which turns out to be the same question. Chapters 1 and 4 are set reading in Weeks 0 and 7. Free at mitpress.mit.edu.*

**Pierce, B. — *Types and Programming Languages* (MIT Press, 2002).**
*"TAPL". The type theory in Weeks 3 and 8 comes from here. Rigorous, and worth the effort — this is the book that separates people who use type systems from people who understand them.*

---

## Week by Week

| Week | Topic | The question it answers |
|---|---|---|
| **0** | Languages, Syntax, and Grammars | Who decides what a program is allowed to say? |
| **1** | Lexical Analysis and Regular Languages | How does text become tokens, and why is a DFA enough? |
| **2** | Parsing — Top-Down and Bottom-Up | How does a flat token stream become a tree? |
| **3** | Semantic Analysis — Types and Symbol Tables | How does the compiler know `x` is an `int` when you never said so? |
| **4** | IR and Code Generation · **MIDTERM 1** | What does a compiler think a program *is*, in the middle? |
| **5** | Optimization — Loops and Data Flow | How does `-O2` make it faster without breaking it? |
| **6** | Runtime Systems — Memory Management · **Project 1 assigned** | Who frees the memory, and what does it cost to decide? |
| **7** | Functional Programming — Lambda Calculus | What is the smallest thing that can compute anything? |
| **8** | Type Systems in Depth · **MIDTERM 2** | How far can a type system go before it becomes a proof? |
| **9** | Concurrency in Programming Languages | What does concurrent code even *mean*? |
| **10** | DSLs and Metaprogramming | What if the program could write the program? |
| **11** | A Complete Mini-Compiler · **Project 1 due** | Does the whole thing actually run? |
| **12** | The Landscape of Programming Languages · **Project 2 due** | Given everything, what would *you* have designed? |

---

## What This Course Feeds

**Immediately:** CS 201 runs alongside it and the two meet constantly — CS 201's calling convention is what your Week 4 code generator has to obey, and CS 201's cache is why Week 5's loop optimisations are worth doing. PROG 201's memory layout is what Week 6's collector manages.

**Later:** **CS 311 (Programming Languages & Compilers II)** in Year 3 completes this compiler with a full optimising back end — the docx says so explicitly, so the code you write this term is code you will open again. CS 202 assumes Week 9's concurrency vocabulary. CS 341 (Computer Security) leans on Week 6 for memory safety.

---

## Deviations From the Curriculum

Recorded here so a reader meets them without needing `5. Build Records/`:

| What | Why |
|---|---|
| **26 lectures, not 39** | The docx does not give a lecture count; [[Year2 - Sophomore/ROOM ASSIGNMENTS\|ROOM ASSIGNMENTS]] and [[Year2 - Sophomore/FALL SCHEDULE\|FALL SCHEDULE]] both put CS 211 in a **Tue/Thu 08:30–09:45** slot. Two 75-minute lectures a week for thirteen weeks is 26, and inventing a third weekly lecture the timetable has no room for would have been worse than renumbering. |
| **The lab is sat in Week *N*, not Week *N+1*** | CS 201's lab lags because its Tuesday session precedes its own week's Wednesday and Friday lectures. CS 211's lab is Friday, after both lectures. Same reasoning, opposite answer. |
| **Week 9's lab uses x86-64, not a weakly-ordered processor** | The docx asks for memory-ordering bugs "on a weakly-ordered processor". BH 220 is x86-64, which is strongly ordered, and no ARM hardware is available. The lab instead uses C11 relaxed atomics to show *compiler* reordering on x86 — and then makes the architecture-dependence the lesson: the same program is correct here and broken on ARM, which is precisely why a memory *model* exists rather than a memory *rule*. |
| **Projects 1 and 2 are one compiler, not two** | The docx calls PS 11 "complete the multi-week compiler project" and gives Project 2 as "full compiler with optimization". Read together those describe one artefact built in two halves — front end due Week 11, back end due Week 12 — rather than two independent programs. The gradebook's 12.5% + 12.5% split is unchanged. |
| **The course language is named** | The docx says only "a small language". It is called Cyan here because thirteen weeks of material referring to "the small language" is unreadable, and because a fixed grammar is the one thing every week after this depends on. |

---

*CS 211 · Year 2 Fall · © CSE Department*

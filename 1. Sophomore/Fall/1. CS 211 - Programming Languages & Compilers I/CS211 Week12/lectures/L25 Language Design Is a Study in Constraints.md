# CS 211 · Programming Languages & Compilers I
## Week 12 · Lecture 1 of 2
### Language Design Is a Study in Constraints

*“Programming languages should be designed not by piling feature on top of feature, but by removing the weaknesses and restrictions that make additional features appear necessary.”* — *Revised Report on the Algorithmic Language Scheme*, Introduction

---

**Reading:** Hoare (1980), "The Emperor's Old Clothes" · Wirth (1995), "A Plea for Lean Software" · Gabriel (1991), "Worse Is Better" · **Next:** L26, the landscape and what comes after

**Coursework:** 📝 **PS 12** released Wed this week, due Fri this week 17:00 · 📋 **Project 2** due Fri this week 17:00 · 📝 **PS 11** due Fri this week 17:00 · 🔬 **Lab 12** Fri this week 14:00–15:50 · 📕 **Final exam** Tue of finals week 09:00–11:30

---

## 1. The Question the Whole Term Has Been Circling

Week 7 §13 established that every general-purpose language computes exactly the same set of functions. Church–Turing says the expressiveness question has one answer for all of them.

**So the interesting differences are somewhere else.** Twelve weeks have been finding out where, and this lecture collects the answer.

A language design is a set of **decisions about what to make impossible**. Every one of them buys something and costs something, and the costs are measurable — which is what the rest of this lecture does, on this machine, today.

---

## 2. The Safety Axis, Measured

One question, asked of four languages: read past the end of a four-element array.

```
$ ./bounds_c ; java Bounds ; python3 bounds.py ; node bounds.js
```

| language | `a[7]` |
|---|---|
| **C** | **a number** (`29291`, `30915`, …) — no diagnostic, program continued |
| **Java** | `ArrayIndexOutOfBoundsException: Index 7 out of bounds for length 4` |
| **Python** | `IndexError: list index out of range` |
| **JavaScript** | **`undefined`** — no error at all |

**Four different answers to the same question**, and each is a design decision rather than an accident.

**The C value changes between runs** — 29291 on one, 30915 on the next — because it is whatever happens to be four ints past the array on the stack. **If your number differs from the lecture's, that is the demonstration working.**

**And it is not "garbage".** It is *undefined behaviour*: the standard imposes no requirement on the program at all. Week 9 §6 met this exact clause from the other side, where it licensed the compiler to delete a million-iteration loop. Here it licenses reading someone else's stack.

**Java and Python check every access.** That check costs — a compare and a branch on each indexing operation — and buys the guarantee that the failure is *loud, immediate, and at the point of the mistake*.

**JavaScript is the interesting one.** It is memory-safe — nothing is corrupted, nothing leaks — and it reports nothing, because in JavaScript an absent property *is* a value, `undefined`. So the error propagates silently into arithmetic, and you discover it later as `NaN`.

> **"Safe" is not one property.** C is unsafe: the bug corrupts memory. JavaScript is memory-safe
> and *diagnostically* unsafe: the bug becomes a value and travels. Java and Python are both, at a
> per-access cost. **When someone says a language is safe, ask which of those they mean.**

---

## 3. The Performance Axis, Measured

The same naive recursive Fibonacci — no data structures, no library calls, just function calls and addition:

| | `fib(30)` | vs C | `fib(32)` | vs C |
|---|---|---|---|---|
| **C** (gcc -O2) | 0.004 s | 1× | 0.028 s | 1× |
| **Java** | 0.025 s | **6.3×** | 0.037 s | **1.3×** |
| **JavaScript** (node) | 0.037 s | 9.3× | 0.075 s | 2.7× |
| **Python** | 0.353 s | 88× | 0.551 s | 20× |

**Read the two "vs C" columns against each other.** Java is 6.3× slower at `fib(30)` and 1.3× slower at `fib(32)`. Nothing about the language changed. **The JIT warmed up.**

That is Week 11 §L24.4 arriving as a number: a JIT pays in startup and buys information, so any measurement short enough to be convenient is measuring the payment rather than the purchase. Week 9's `Hoist.java` showed the same thing from the other side — a loop that terminated while interpreted and hung once C2 compiled it.

> **Almost every "language X is N times slower than C" claim you will read is a warm-up artefact,
> a benchmark that fits in cache, or a library call in disguise.** The honest form of the claim
> names the workload, the input size and the runtime version — and even then it is about *this*
> program, not about the language.

---

## 4. The Expressiveness Axis, and Why It Looks Inverse

The same program, non-blank source lines:

| | lines | `fib(32)` |
|---|---|---|
| C | 18 | **0.028 s** |
| Java | 10 | 0.037 s |
| JavaScript | 6 | 0.075 s |
| **Python** | **5** | 0.551 s |

**Almost exactly inverse.** The shortest program is the slowest and the longest is the fastest.

It is tempting to read a law off that table. Do not, for two reasons.

**The measurement is confounded.** C's line count is inflated by `#include`s and explicit timing code that Python gets from one import. A fairer count would narrow the gap considerably.

**And the causation is not what it looks like.** Python is not slow *because* it is short. It is short and slow for the *same underlying reason*: values carry their types at run time, so the programmer does not write them down and the interpreter must check them. **One decision, two consequences** — and that is the shape of nearly every entry in the table below.

---

## 5. What Each Language Made Impossible

| language | the decision | bought | cost |
|---|---|---|---|
| **Fortran** (1957) | compile mathematics to competitive machine code | proved compilers could beat hand-written assembly | no recursion until 1990 |
| **COBOL** (1959) | readable by non-programmers | sixty years of production use | verbosity that became the joke |
| **Lisp** (1958) | code is data | macros, and Week 10 | parentheses, and dynamic typing |
| **ALGOL 60** (1960) | describe the language *formally* | BNF, block scope, and every language since | never widely deployed |
| **C** (1972) | trust the programmer, map to hardware | the systems language for fifty years | Week 6's use-after-free, Week 9's races |
| **Smalltalk** (1972) | everything is an object, everything is live | OOP, the IDE, the GUI | performance, and isolation from the OS |
| **ML** (1973) | make the type system infer | Week 8, and Hindley-Milner | rank-1 only, and a small user base |
| **Java** (1995) | portability and memory safety | the enterprise, and the JVM | Week 9's memory model, and verbosity |
| **Python** (1991) | readability first | the most-taught language on earth | Week 9's GIL, and 20× |
| **Rust** (2010) | memory safety **without** a collector | Week 6's bugs, refused at compile time | the borrow checker, and a learning cliff |

**Read down the "cost" column.** Every entry is something this course has measured or built.

The pattern worth taking away: **each language made one central decision and then paid for it everywhere else.** C's decision to trust the programmer is why it has no bounds check, why `a[7]` is undefined, why it is fast, and why memory-safety CVEs are the largest single category in the NVD. That is not four facts. It is one decision, seen from four directions.

---

## 6. Rust, Because It Is the Interesting Case

Every other row in that table trades safety against performance. Rust's claim is that the trade was **false** — that a sufficiently clever type system gets both.

You already know the mechanism. Week 6 §L14.12:

- Every value has exactly one **owner**; when the owner goes out of scope the value is freed, at a point the compiler knows statically.
- A **borrow** must not outlive what it borrows.
- Many shared borrows, or one mutable borrow, never both.

That last rule is doing double duty, and Week 9 is why. **A data race requires two threads accessing the same location with at least one writing** — and "one mutable borrow, or many shared ones" is precisely a prohibition on that. **The rule that eliminates use-after-free eliminates data races too**, which is why Rust advertises "fearless concurrency" and means something specific by it.

**And the cost is real**, in the same shape as Week 8's:

- **Sound and incomplete.** Programs a human knows are safe are rejected. A doubly-linked list — Week 7 §L13.8's cycle, again — does not satisfy single ownership, and is written with `Rc`/`Weak` or `unsafe`.
- **`Rc<RefCell<T>>` cycles leak**, exactly as Week 6 §8 says they must. Rust does not solve the cycle problem; it declines to have it in the common case and hands you reference counting for the rest.
- **The cost moved to the programmer.** Tracing costs machine time; ownership costs design time, and shows up as a compile error rather than a pause graph.

> **The honest summary is that Rust did not abolish the trade-off. It moved it** — from run time
> to compile time, and from the machine to the programmer. That is a very good trade for systems
> software and a poor one for a script you will run twice.

---

## 7. Three Design Principles, and Their Critics

**"Worse is better"** (Gabriel, 1991). The *New Jersey* style — C and Unix — prefers simplicity of *implementation* over completeness of *interface*. The *MIT* style — Lisp — prefers correctness and completeness even when the implementation suffers. Gabriel's uncomfortable observation is that the worse design **wins**, because it ships, spreads, and gets fixed in the field.

**"Everything should be as simple as possible, but no simpler."** Wirth built Pascal, Modula and Oberon on it, and Wirth's law — software gets slower faster than hardware gets faster — is the complaint of somebody who watched the industry choose otherwise.

**"There are two ways of constructing a software design"** (Hoare, 1980). One is to make it so simple there are obviously no deficiencies; the other so complicated there are no obvious deficiencies. Hoare's Turing Award lecture is also where he apologises for inventing the null reference — *"my billion-dollar mistake"* — which is a language design decision whose cost is still being paid, and which Week 8 §4's nominal declarations are one answer to.

**The critic worth reading against all three:** none of them predicted that the most-used languages of 2025 would be JavaScript and Python. Simplicity of implementation did not win; **availability** did. JavaScript won because it was in the browser, and Python won because it was in the tutorial.

---

## 8. How to Judge a Language

Not by which paradigm it belongs to. Twelve weeks suggest a better set of questions, and every one of them is something you can now answer for yourself.

1. **What does it make impossible, and is that the thing I keep getting wrong?**
2. **When does it tell me I am wrong** — at compile time (Week 8), at run time (§2), or never (§2 again)?
3. **What is the cost of its guarantee, and who pays it?** The machine, the programmer, or the person waiting?
4. **Can I see through it?** Weeks 4–11 were about reading what the compiler did. A language whose output you cannot inspect is one you cannot debug when it matters.
5. **What is its failure mode when I am wrong?** A crash, an exception, a wrong answer, or `undefined`.
6. **How much of it must I hold in my head at once?**

> **Question 5 is the one this course keeps returning to.** Week 4's folder gave a plausible wrong
> number. Week 5's optimiser deleted a live instruction. Week 6's collector freed a reachable
> object and printed the right answer anyway. Week 7's substitution turned a constant function
> into the identity. Week 9's compiler emitted `jmp .L6`. **Every one was silent**, and the
> languages that would have caught them are the ones that made the corresponding mistake
> impossible rather than merely discouraged.

---

## 9. What to Take From This

1. **Expressiveness is never the question** — Church–Turing settled it. The differences are in what is made impossible.
2. **"Safe" is at least two properties.** C corrupts memory; JavaScript returns `undefined` silently. Java and Python are loud, at a per-access cost.
3. **`a[7]` gives four different answers**, and each is a decision.
4. **Java is 6.3× C at `fib(30)` and 1.3× at `fib(32)`.** The language did not change; the JIT warmed up.
5. **Most "N times slower" claims are warm-up artefacts** or benchmarks in disguise.
6. **Source length ran inverse to speed**, and the causation is not what it looks like — Python is short *and* slow for one shared reason.
7. **Each language made one decision and paid for it everywhere**, and this course measured most of those costs.
8. **Rust moved the trade-off rather than abolishing it** — to compile time, and onto the programmer. Its aliasing rule kills use-after-free and data races with one mechanism.
9. **Availability beat elegance.** JavaScript won the browser; Python won the tutorial.
10. **Judge a language by its failure mode when you are wrong**, because you will be.

**Next:** where the landscape is actually going — the multiparadigm convergence, WebAssembly, and what the next ten years look like.

---

*CS 211 · Week 12 · Lecture 25 · © CSE Department*

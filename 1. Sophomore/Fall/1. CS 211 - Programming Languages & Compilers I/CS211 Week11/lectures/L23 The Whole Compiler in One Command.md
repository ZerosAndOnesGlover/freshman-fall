# CS 211 · Programming Languages & Compilers I
## Week 11 · Lecture 1 of 2
### The Whole Compiler, in One Command

*“Much of my work has come from being lazy. I didn't like writing programs, and so, when I was working on the IBM 701 (an early computer), writing programs for computing missile trajectories, I started work on a programming system to make it easier to write programs.”* — John Backus, on the origin of FORTRAN, IBM *Think* (1979)

---

**Reading:** Dragon §1.2–1.3 (revisit) · LLVM Language Reference, "Introduction" and "Instruction Reference" · **Next:** L24, JIT compilation and what LLVM is

**Coursework:** 📊 **Quiz 11** today · 📝 **PS 11** released Wed this week, due Fri of Week 12 17:00 · 📋 **Project 1** due Fri this week 17:00 · 📝 **PS 10** due Fri this week 17:00 · 🔬 **Lab 11** Fri this week 14:00–15:50

---

## 1. Eleven Weeks, One Driver

You have written eight phases and never once run them as a compiler. `cyanc.py` is the driver they were missing:

```
$ python3 cyanc.py gcd.cy
; ---- 0. lexer: 39 tokens ----
; ---- 1. parser: 1 declarations, 1 functions ----
; ---- 2. type checker: ok, 0 struct(s) ----
; ---- 3. TAC for gcd: 12 instructions ----
; ---- 4. CFG: 4 basic blocks, 4 edges ----
; ---- 5. our optimiser: 12 -> 11 instructions (8% removed) ----
; ---- 6. liveness: fixed point in 3 rounds, peak 2 simultaneously live ----
; ---- 7. interference graph: 6 nodes, 8 edges ----
; ---- 8. LLVM IR: 32 instructions (6 alloca, 17 load/store) ----
```

And then, because there is now a ninth phase:

```
$ python3 cyanc.py gcd.cy 1071 462 --run
; ---- lli (JIT): exit code 21 = gcd(1071, 462) ----
```

**Twenty-one.** `gcd(1071, 462) = 21`, computed by machine code that your compiler produced, on this processor.

`cyanc.py` contains **no compilation of its own**. It parses arguments, sequences phases and reports. That is what a compiler driver is: `gcc` is mostly this, and the program people mean when they say "the compiler" is `cc1`.

---

## 2. The Phase That Was Missing

Week 6 stopped at a register assignment and then *interpreted the TAC*, which was right for studying garbage collection and wrong for producing a program. The missing phase is code generation, and we are not going to write one.

```
cyan  ->  our 8 phases  ->  LLVM IR  ->  [ opt ]  ->  llc  ->  x86-64
                                      \-> lli (a JIT)
```

**LLVM IR** is a textual, target-independent assembly language with an unlimited supply of registers and explicit types. `llvmgen.py` emits it, and everything after that is somebody else's problem — which is the entire point of L24.

Here is what our compiler produces for `gcd`:

```llvm
define i64 @gcd(i64 %a.in, i64 %b.in) {
entry:
  %a.addr = alloca i64
  %b.addr = alloca i64
  ...
L0:
  %t0 = load i64, ptr %b.addr
  %t2 = icmp ne i64 %t0, 0
  ...
```

`llvm-as` accepts it. `clang` turns it into a binary. `lli` runs it.

---

## 3. The Trick: Refusing to Build SSA

LLVM IR is **SSA** — every register assigned exactly once. Our TAC is not: `a = a % b` reassigns `a`, and Week 4 needed φ-functions to model exactly that.

Constructing SSA in a front end is real work — dominance frontiers, φ placement, renaming. **So we do not do it.**

> **Every variable gets a stack slot (`alloca`), and every read and write becomes a `load` or a
> `store`.**

That is trivially correct, produces genuinely terrible IR, and is **exactly what clang does**. Look at the numbers for `gcd`: 32 instructions, **6 allocas, 17 loads and stores**, for a four-line function.

Then hand it to LLVM:

```
$ opt -passes=mem2reg -S gcd.ll
```

| | lines | alloca | load/store | phi |
|---|---|---|---|---|
| **our IR** | 42 | **6** | **17** | 0 |
| after `mem2reg` | 22 | **0** | **0** | **2** |
| after `-O2` | 20 | 0 | 0 | 3 |

**Every stack slot is gone and φ-functions have appeared.**

`mem2reg` promoted the memory to registers and inserted the φ-functions — using the **dominance-frontier algorithm from Week 4**, the one you studied and did not implement.

> **We are not avoiding the hard part. We are calling a library that does it.** That is a
> legitimate engineering decision and it is what every LLVM front end makes. The reason Week 4
> taught you the algorithm anyway is that you cannot read `mem2reg`'s output — or debug it when
> your IR is subtly wrong — without knowing what a φ is and where it belongs.

---

## 4. A Bug That Only Real Output Finds

The first version of `llvmgen.py` produced this:

```llvm
  store i64 %b.in, ptr %b.addr
fn_gcd:
  br label %L0
```

Our TAC lets control **fall through** into a label. LLVM does not: **every basic block must end with a terminator**, and falling off the end is not one. `llvm-as` rejected it immediately.

The fix is one line — the flag tracking "does this block still need a branch" has to start `True`, because the `entry` block is already open when the first label arrives.

**That bug could not have been found by the interpreter.** `runtime.py` was perfectly happy with fall-through, because fall-through is what its instruction loop does. The constraint exists in the *target*, and you do not meet the target's constraints until you emit something the target has to accept.

*The same is true of `Unsupported`: `llvmgen.py` refuses arrays and structs, loudly, because an `[int]` cannot be an `i64` and a real back end has to decide what a value **is**. The interpreter never had to — a Python object stood in for everything.*

---

## 5. Our Optimiser Against LLVM's

You wrote an optimiser in Weeks 4 and 5: constant folding, copy propagation, dead-code elimination, and in PS 5, loop-invariant code motion. Here it is on four programs, against LLVM on the IR generated from the same sources.

**Ours, on our TAC:**

| | before | after | removed |
|---|---|---|---|
| `gcd` | 12 | 11 | 8% |
| `cls` | 23 | 23 | **0%** |
| `fold` | 13 | 6 | 53% |
| `sc` | 6 | 5 | 16% |

**LLVM, on our IR:**

| | ours | `mem2reg` | `-O2` | removed |
|---|---|---|---|---|
| `gcd` | 32 | 11 | **9** | 72% |
| `cls` | 57 | 20 | **10** | **82%** |
| `fold` | 37 | 5 | **1** | **97%** |
| `sc` | 16 | 6 | **3** | 81% |

**`fold` becomes one instruction.** And the row to sit with is `cls`: **our optimiser removed nothing at all, and LLVM removed 82%.**

Two honesty notes, because this comparison is easy to overstate.

**The baselines are not the same.** Our TAC is dense; our LLVM IR is deliberately alloca-heavy, so a large part of LLVM's percentage is undoing damage we did on purpose. Comparing raw percentages flatters LLVM.

**But `cls` is not explained by that.** Our optimiser was handed 23 instructions of dense TAC and found **zero** to remove. That is a fact about our optimiser, not about baselines.

> **This is the week's honest result, and it is not a criticism of your work.** Three passes and a
> weekend against two decades and several hundred contributors — the surprise would be any other
> outcome. What Weeks 4 and 5 bought you is not a competitive optimiser. It is the ability to read
> `-O2` output and know what happened, which is the skill that survives.

---

## 6. Where the Time Actually Goes

```
$ python3 cyanc.py gcd.cy --times
  lex          0.175 ms   13.7%
  parse        0.342 ms   26.8%
  typecheck    0.089 ms    7.0%
  tac          0.072 ms    5.6%
  cfg          0.065 ms    5.1%
  opt          0.248 ms   19.4%
  live         0.091 ms    7.1%
  llvm         0.195 ms   15.3%
  total        1.276 ms
```

The front end dominates: **lexing and parsing are 40% of compile time**, which is why Weeks 1 and 2 spent so long on them and why real compilers care about parser performance.

**That table took three attempts to become true**, and the failures are more useful than the numbers.

**Attempt one** reported `llvm 4.54 ms, 82.4%`. Code generation appeared to dominate everything else combined.

**Attempt two** found that `compile_to_llvm` re-ran the parser and type checker internally, because it took *source* rather than the AST the driver already had. Fixed. Result: **80.5%.** Barely moved.

**Attempt three** found the real cause. `target_triple()` called `llvm-config` — **a subprocess** — on every invocation. Process creation costs milliseconds, which is more than every other phase of this compiler put together. Cached it, and the LLVM phase became **15.3%**.

> **The first measurement was about `fork` and `exec`.** It was reproducible, it was plausible, and
> it was a fact about process creation rather than about code generation. Weeks 5, 6, 7 and 9 each
> had a version of this — the printer that misreported a def, peak RSS that could not see
> retention, `0 == False` passing every boolean test, a cache line that changed a rate by 100×.
> **Profile before believing, and a subprocess is never free.**

---

## 7. Does It Actually Work?

An end-to-end compiler needs an end-to-end check, and we have one for free: **Week 6's interpreter runs the same programs.**

| call | interpreter | LLVM JIT | agree |
|---|---|---|---|
| `gcd(1071, 462)` | 21 | 21 | ✓ |
| `gcd(270, 192)` | 6 | 6 | ✓ |
| `gcd(17, 5)` | 1 | 1 | ✓ |
| `classify(250)` | 62 | 62 | ✓ |
| `classify(-5)` | 0 | 0 | ✓ |
| `classify(0)` | 1 | 1 | ✓ |
| `classify(99)` | 99 | 99 | ✓ |
| `fold f()` | 19 | 19 | ✓ |
| `sc f(1,1)` | 1 | 1 | ✓ |
| `sc f(1,0)` | 0 | 0 | ✓ |
| `sc f(0,1)` | 0 | 0 | ✓ |

**Eleven of eleven.** Two independent back ends — a Python interpreter over TAC and LLVM's x86-64 code generator — agreeing on every case.

This is **differential testing**, and Week 9 §8 recommended it for exactly this reason: you do not need an oracle if you have two implementations that should agree. Week 6's `--gc=none` against `--gc=mark` was the same move.

*(The first run of that table showed two disagreements. The cause was my test harness calling `sc.cy`'s function `g` when it is named `f`, so the compiler compiled the right thing and the comparison compared the wrong thing. **Check the harness before believing a mismatch** — and check it again before believing agreement.)*

---

## 8. What to Take From This

1. **A driver is not a compiler phase.** `cyanc.py` sequences and reports; `gcc` is mostly this.
2. **`gcd(1071, 462) = 21`, from machine code your compiler produced.**
3. **We refuse to build SSA**: `alloca` for everything, and `mem2reg` promotes it — Week 4's dominance-frontier algorithm, called as a library.
4. **6 allocas and 17 load/stores became 0 and 0, with φ-functions appearing** where Week 4 said they would.
5. **A fall-through into a label is legal in our TAC and illegal in LLVM.** The interpreter could never have found that; you meet the target's constraints only when you emit for the target.
6. **On `cls`, our optimiser removed 0% and LLVM removed 82%** — and the baselines differ, but 0% is 0%.
7. **What Weeks 4–5 bought is the ability to read `-O2` output**, not a competitive optimiser.
8. **The front end is 40% of compile time.**
9. **A phase-time table took three attempts to stop lying**, and the last lie was a subprocess.
10. **Eleven of eleven agree between the interpreter and the JIT** — differential testing, no oracle required.

**Next:** what LLVM actually is, why the same IR becomes x86-64, ARM64 and WebAssembly, and what a JIT does that an ahead-of-time compiler cannot.

---

*CS 211 · Week 11 · Lecture 23 · © CSE Department*

# CS 211 · Programming Languages & Compilers I
## Week 11 · Lecture 2 of 2
### LLVM, and the Compiler You Did Not Write

---

**Reading:** Lattner & Adve (2004), "LLVM: A Compilation Framework" · Lattner, *The Architecture of Open Source Applications* ch. 11 · LLVM's Kaleidoscope tutorial, ch. 1–4 · **Next:** L25, the landscape of programming languages

---

## 1. The Bargain

L23 stopped one phase short of machine code and then handed the problem to LLVM. This lecture is about what was on the other side of that handoff, and why the trade is so lopsided.

**The number of back ends we wrote is zero.** Here is what our `gcd` compiles to, from the *same IR*, with nothing changed but a flag:

```
$ llc -march=TARGET gcd.ll
```

| target | assembly instructions |
|---|---|
| **aarch64** | **8** |
| ppc64le | 10 |
| sparcv9 | 11 |
| **x86-64** | **12** |
| mips64 | 12 |
| **riscv64** | **16** |
| **wasm32** | **23** |
| **avr** | **124** |

**Eight architectures, one IR, a fifteenfold spread.** And the spread is not arbitrary — every number is a fact about the target:

- **aarch64 needs 8** because ARM has a hardware divide: `sdiv x9, x0, x1` then `msub x1, x9, x1, x0`. There is no remainder instruction, so the back end computes the quotient and multiplies back — a peephole idiom Week 5 §8 would recognise.
- **riscv64 needs 16** because the base RISC-V integer ISA **has no divide instruction at all**. The back end emits `call __moddi3`, a helper from the compiler runtime library.
- **wasm32 needs 23** because WebAssembly has **structured control flow** — `block`, `loop`, `br_if` — rather than arbitrary branches, so the back end must reconstruct structure our CFG had thrown away.
- **avr needs 124** because it is an 8-bit microcontroller being asked for a 64-bit modulo. Every `i64` operation becomes eight bytes of manual work.

> **That table is the argument for LLVM in one image.** Nobody in this room could write the AVR
> back end, and nobody needs to. We wrote a front end for a language we invented, and got eight
> code generators — including one for an 8-bit chip and one for a browser.

---

## 2. What LLVM Actually Is

Not a compiler. **A set of libraries organised around one data structure.**

```
   clang  ──┐                                  ┌──►  x86-64
   rustc  ──┤                                  ├──►  ARM64
   swiftc ──┼──►  LLVM IR  ──►  opt passes ──►─┼──►  RISC-V
   flang  ──┤                                  ├──►  WebAssembly
   cyanc  ──┘                                  └──►  AVR, GPU, …
```

The IR in the middle is the whole design. **Front ends and back ends do not know about each other**, and both only know the IR — so the matrix of *m* languages × *n* targets collapses into *m + n* pieces of work.

Consequences worth naming:

- **A new language gets every target for free.** Ours did, this week.
- **A new target gets every language for free.** Apple's M1 back end brought Rust and Swift with it.
- **An optimisation written once benefits everybody.** `mem2reg` promoted our terrible IR without knowing Cyan exists.

That is the thesis of Lattner and Adve's 2004 paper, and it is why LLVM displaced a great deal of what came before.

**The cost, and it is real:** the IR is now a compatibility surface. It has to be expressive enough for C's undefined behaviour, Rust's aliasing guarantees, Swift's reference counting and Fortran's arrays — which is why LLVM IR has `poison`, `undef`, `noalias`, and a specification that is genuinely difficult. **Week 9's memory model appears here too**: LLVM IR has `atomic` operations with the same orderings, because it has to be able to express what C11 and Java both mean.

---

## 3. `opt` Is a Pass Pipeline, and You Can Watch It

`opt` runs passes over the IR. You have already used it in Week 5 to watch LICM refuse to hoist a division.

```
$ opt -passes=mem2reg -S gcd.ll        # one pass
$ opt -O2 -S gcd.ll                    # the standard pipeline
```

The `-O2` pipeline is roughly 200 passes, and you have written versions of several: constant folding, dead-code elimination, copy propagation, LICM. What you have not written is the *ordering*, and Week 5 §9 already told you why that is hard — **phase ordering**, where the best sequence depends on the program.

On our IR:

| | our IR | `mem2reg` | `-O2` |
|---|---|---|---|
| `gcd` | 32 | 11 | **9** |
| `cls` | 57 | 20 | **10** |
| `fold` | 37 | 5 | **1** |

**`fold` becomes a single instruction.** The program computes a constant, and LLVM worked that out.

*Two-thirds of `mem2reg`'s reduction is undoing our own `alloca` decision, which we made on purpose. The honest reading of these numbers is in L23 §5.*

---

## 4. JIT: Compiling While the Program Runs

`lli` does not produce a file. It compiles the IR **into memory** and jumps to it:

```
$ python3 cyanc.py gcd.cy 1071 462 --run
; ---- lli (JIT): exit code 21 = gcd(1071, 462)   [37 ms] ----
```

The native binary runs the same computation in **4 ms** wall clock, but that comparison is meaningless: `gcd(1071, 462)` takes microseconds, and the 37 ms is JIT compilation plus process startup. **What a JIT costs is startup; what it buys is information.**

**The information is what an ahead-of-time compiler cannot have:**

- **The actual types.** A dynamically typed language sees `x + y` and cannot know it is integers. At run time it can observe that it has *always* been integers, compile the integer path, and guard it. This is why V8, PyPy and LuaJIT exist.
- **The actual branches.** Week 9 measured that a mispredicted branch costs 15–20 cycles; a JIT knows which way this branch actually went the last ten thousand times and lays out the code accordingly.
- **The actual call targets.** A virtual call that has only ever hit one implementation can be **inlined**, with a guard — *monomorphic inline caching*, and it is the single largest win in JIT compilation for object-oriented code.
- **The actual machine.** AOT builds for a baseline; a JIT knows whether AVX-512 is present.

**And what it pays:**

- **Compilation happens in the user's latency budget**, which is why every serious JIT is *tiered* — interpret first, compile the hot parts, optimise the very hot parts.
- **Speculation needs guards and deoptimisation.** When the assumption breaks, the JIT must reconstruct the interpreter's state mid-function and continue. That machinery is most of a JIT's complexity.
- **Warm-up.** Week 9 §7 measured this from the other side: `Hoist.java` terminated while interpreted and hung *once C2 compiled the loop*. The same program, in the same run, behaving differently before and after JIT compilation.

> **AOT and JIT are not competitors, they are different bets about when you know things.** AOT bets
> that static information is enough and buys predictability. JIT bets that dynamic information is
> worth more than the compile time and buys speculation. **Almost every modern runtime does both**
> — Java AOT-compiles with `jaotc`/Leyden and JITs with C2; .NET has ReadyToRun plus tiered JIT;
> V8 has Sparkplug, Maglev and TurboFan in a tier ladder.

---

## 5. What Your Compiler Is Missing

Being honest about the gap is more useful than a victory lap. `cyanc` compiles `int` and `bool`, and refuses everything else:

```python
raise Unsupported(
    f"'{op}' needs a heap and a collector at the IR level. "
    f"Week 6 built both for the interpreter; PS 11 Part C is "
    f"porting them to LLVM.")
```

**Arrays and structs are the honest hole.** `runtime.py` interpreted them because a Python object could stand in for any value; the moment you emit real code you must decide what a value **is**, and `[int]` is not an `i64`. It needs a heap layout, `malloc`, and — because Week 6 built one — a garbage collector that can find its roots. **A precise collector needs a stack map, and Week 6 §L14.2 established that the stack map is a compiler output.** That is PS 11 Part C, and it is where the last three weeks converge.

The rest of the gap, in rough order of size:

| missing | what it needs |
|---|---|
| arrays, structs | heap layout, `malloc`, GC roots via stack maps |
| closures | environment capture — Week 7 §12's argument, in your code generator |
| separate compilation | a module system, symbol visibility, a linker story |
| debug information | DWARF, so the debugger can map machine code to your source |
| error recovery | Week 2's parser stops at the first error; real ones continue |
| a standard library | anything at all |

**Debug information is the one people underestimate.** Every optimisation in Weeks 4, 5 and this lecture destroys the correspondence between source lines and machine instructions, and preserving a usable mapping *through* those transformations is a substantial engineering programme in its own right. It is why `-O2 -g` sometimes shows a debugger jumping around, and why "optimised build, useful stack trace" is a hard requirement rather than a free one.

---

## 6. The Course, in One Diagram

```
   source  ──0─►  tokens  ──1─►  AST  ──2─►  typed AST  ──3─►  TAC
                                                                │
                              4  build the CFG  ◄───────────────┘
                                     │
                   5  optimise ◄─────┤       (folding, DCE, LICM)
                                     │
                   6  liveness ◄─────┤       (registers … and GC roots)
                                     │
                   7  allocate ◄─────┤       (interference, colouring)
                                     │
                   8  LLVM IR  ◄─────┘
                        │
                        ├──►  opt  ──►  llc  ──►  machine code
                        └──►  lli  ──►  JIT
```

**Every arrow is a week**, and the through-lines matter more than the boxes:

- **Fixed-point iteration** — ε-closure (W1), FIRST/FOLLOW (W2), constant folding (W4), liveness and dominators (W5), the marker (W6), unification (W8).
- **The same def/use table** feeding dead-code elimination (W5), register allocation (W5) and the garbage collector's root set (W6) — and being *unsound* in all three when it was wrong.
- **Maximal munch** as lexing (W1) and as instruction selection (W5).
- **Sound and incomplete**, four times: liveness's *may* (W5), reference counting (W6), type inference (W8), and the C standard's refusal to define races (W9).
- **Undecidability** as the reason every analysis approximates (W7 §13) and every optimisation is conservative.

---

## 7. What to Take From This

1. **Eight targets, one IR, and we wrote no back ends** — 8 instructions on ARM64 to 124 on AVR.
2. **The spread is information about the targets**: RISC-V has no divide and calls `__moddi3`; WebAssembly needs structured control flow; AVR is 8 bits doing 64-bit arithmetic.
3. **LLVM is libraries around one data structure**, turning *m × n* into *m + n*.
4. **The cost is that the IR becomes a compatibility surface** — `poison`, `noalias`, atomics, and a hard specification.
5. **`-O2` is ~200 passes**, and you have written several; what you have not written is the ordering, which is Week 5's phase-ordering problem.
6. **`fold` optimises to one instruction.**
7. **A JIT buys information and pays in startup**: real types, real branch behaviour, real call targets, the real machine.
8. **Speculation needs guards and deoptimisation**, which is most of a JIT's complexity — and Week 9 measured the warm-up from the other side.
9. **Arrays and structs are the honest hole**, and closing it needs Week 6's collector plus a stack map, which is a compiler output.
10. **Debug information is the underestimated one** — every optimisation destroys the source correspondence you then have to preserve.

**Next week is the last**, and it asks what all of this was for: why there are so many languages, what they actually differ in, and how to judge one.

---

*CS 211 · Week 11 · Lecture 24 · © CSE Department*

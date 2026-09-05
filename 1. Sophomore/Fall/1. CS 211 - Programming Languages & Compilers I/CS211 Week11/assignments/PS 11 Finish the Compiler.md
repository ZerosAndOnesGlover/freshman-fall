# CS 211 · Problem Set 11
## Finish the Compiler

---

**Released:** Week 11, Wednesday · **Due:** Week 12, Friday 17:00
**100 points · counts toward the Problem Sets component (30% of the final grade)**

**Submit:** `llvmgen.py`, `cyanc.py` and any new modules (runnable end to end), plus `ps11.md`.

> **Thanksgiving recess falls between release and deadline** — no classes Nov 24. You have two
> calendar weeks and one teaching week. **PS 12 is also due that Friday.** Plan accordingly.
>
> **Project 1 was due last Friday.** If your feature is not finished, its marks are gone but its
> *code* is not — Part D lets you get value from it here.

---

## Part A — Reading the Output (18 points)

**A1.** *(5)* Run the whole compiler and report every phase:

```
python3 cyanc.py gcd.cy
python3 cyanc.py gcd.cy 1071 462 --run
```

- Give the nine phase lines and the JIT result.
- `cyanc.py` performs **no compilation of its own**. Say what it does instead, and name the equivalent program in a real toolchain.

**A2.** *(5)* `llvmgen.py` gives every variable an `alloca` and every access a `load` or `store`.

- Report the alloca and load/store counts for `gcd`, then run `opt -passes=mem2reg` and report them again.
- **φ-functions appear.** How many, and where? Match them against the CFG from `--emit=cfg`.
- **Name the Week 4 algorithm `mem2reg` is running**, and say why we did not implement it.

**A3.** *(4)* The first `llvmgen.py` emitted a block that fell through into a label, and `llvm-as` rejected it.

- Explain the rule it violated.
- **Why could `runtime.py` never have found this bug?** Your answer should be about where the constraint lives.

**A4.** *(4)* Compare compile-time phase costs:

```
python3 cyanc.py gcd.cy --times
```

- Report the table. Which phase dominates, and by how much?
- The first version of this table said `llvm 82.4%`. Two separate causes were found. **Name both**, and say which one mattered more.
- In one sentence: what does this say about profiling?

---

## Part B — Extend the Back End (34 points)

**B1.** *(8)* `llvmgen.py` emits `i64` for everything, including booleans.

- Emit `i1` for `bool`-typed values, using the type information Week 3's checker already computes.
- You will need `zext`/`trunc` at the boundaries. Say where.
- Verify all four `sc.cy` cases still agree with the interpreter, and report the instruction-count change.

**B2.** *(8)* **Multiple functions and calls.**

`compile_to_llvm` emits one function at a time. Emit them all, so that recursion and cross-calls work.

- Write a recursive `fact` and a mutually recursive `iseven`/`isodd` in Cyan.
- Compile and JIT both; verify against the interpreter for n = 0…10.
- Report the LLVM IR for one of them, and say what `-O2` did to it. *(Look for tail-call and inlining decisions.)*

**B3.** *(10)* **A peephole pass of your own, on LLVM IR.**

Write an `opt`-style pass — in Python over the textual IR, or as a `LLVMGen` post-pass — that performs at least three of:

- `add x, 0` → `x`; `mul x, 1` → `x`; `mul x, 2` → `shl x, 1`
- `icmp` immediately followed by `zext`/`icmp ne 0` → the original `icmp`
- removal of a `store` immediately followed by a `load` of the same slot

Then:

- Report instruction counts before and after on all four test programs.
- **Verify correctness against the interpreter for every program.**
- Run `opt -O2` **after** your pass and report whether your pass helped, hurt or made no difference to the final count. **Any of the three is a valid finding**; explain the one you get.

**B4.** *(8)* **The `alloca` question.**

We emit `alloca` everywhere and let `mem2reg` clean up. The alternative is to build SSA in the front end.

- Implement a limited version: for **temporaries only** (`t0`, `t1`, … — which are assigned exactly once by construction), emit SSA registers directly rather than stack slots.
- Report the instruction counts before `mem2reg` for all four programs.
- **After `-O2`, is the final code any different?** Report it, and say what that tells you about where effort is worth spending.

---

## Part C — Arrays and Structs (28 points)

This is the hole `llvmgen.py` announces and declines:

```
'load' needs a heap and a collector at the IR level.
```

**C1.** *(10)* **Heap allocation.**

- Declare `malloc` in the IR and lower `alloc` and `newarr` to calls to it.
- Choose an object layout and **write it down** — header, fields, and where the length of an array lives.
- Lower `getfield`, `setfield`, `load` and `store` using `getelementptr`.
- Get `cyc_empty.cy`'s `viaEmpty` or an equivalent program compiling, JITing, and agreeing with the interpreter.

**C2.** *(8)* **Bounds checking.**

- Add a bounds check to array `load` and `store`: compare against the length in the header and branch to a trap on failure.
- Report the instruction-count cost across your test programs.
- Run `opt -O2` and check whether LLVM **eliminates any of the checks**. Report how many and say why it could.

**C3.** *(10)* **The stack map.**

Week 6 built a collector whose root set came from Week 5's liveness. At the IR level, LLVM has `gc "statepoint-example"` and the `@llvm.gcroot` intrinsic for exactly this.

- Read enough of LLVM's *Garbage Collection with LLVM* document to say **what a front end must emit** for a precise collector.
- Emit `@llvm.gcroot` declarations for the heap-typed slots in one function, and show the IR.
- **You do not have to make collection work.** Explain, in a paragraph, what would still be missing — and connect it to L14 §2's claim that the collector cannot check the root set it is given.

---

## Part D — Written (20 points)

**D1.** *(6)* L23 §5 compares our optimiser with LLVM's: on `cls`, ours removed **0%** and LLVM removed **82%**.

- State the caveat that makes a raw percentage comparison unfair.
- **Explain why `cls` survives that caveat.**
- What did Weeks 4–5 actually buy you, if not a competitive optimiser? Answer in two sentences.

**D2.** *(6)* One IR, eight targets: 8 instructions on aarch64, 124 on AVR.

- Explain **three** of the eight figures in terms of the target's instruction set. *(riscv64, wasm32 and avr are the interesting ones.)*
- State LLVM's *m × n* → *m + n* argument.
- **Name a cost of that design.** It is not performance.

**D3.** *(8)* You are advising a team building a new language.

- Give two concrete reasons to target LLVM and two to target something else — a bytecode VM, JavaScript, or C source.
- **Name a real language that made each choice**, and what it cost them.
- Your language must run in a browser and on a microcontroller. **What do you do?** Use this week's target table.

---

## Reference Numbers

Measured on the machine these notes were prepared on (LLVM/clang 18.1.3, x86-64).

| Measurement | Value |
| --- | --- |
| `cyanc gcd.cy 1071 462 --run` | **exit code 21** |
| interpreter vs JIT, 11 calls | **11 agree, 0 disagree** |
| `gcd` our IR | 42 lines, **6 alloca, 17 load/store** |
| after `mem2reg` | 22 lines, **0 alloca, 0 load/store, 2 phi** |
| after `-O2` | 20 lines, 3 phi |
| our optimiser: `gcd`/`cls`/`fold`/`sc` | 8% / **0%** / 53% / 16% removed |
| LLVM `-O2` on the same: | 72% / **82%** / **97%** / 81% |
| `fold` at `-O2` | **1 instruction** |
| phase times (1.276 ms total) | parse 26.8%, opt 19.4%, llvm 15.3%, lex 13.7% |
| `llc` targets, `gcd` | aarch64 **8**, ppc64le 10, sparcv9 11, x86-64 12, mips64 12, riscv64 **16**, wasm32 **23**, avr **124** |

---

## A Note on Part C

**Part C is the hardest thing this course has asked for**, and it is deliberately at the end.

C1 alone is a real piece of compiler engineering: object layout, `getelementptr`, and the discovery that `getelementptr` does not dereference anything, which surprises everyone once. **C3 does not ask you to make garbage collection work** — it asks you to find out what a front end owes a precise collector, which is a reading exercise with a paragraph at the end.

If you are short of time, **C1 alone, done properly and verified against the interpreter, is worth more than all three attempted and none working.** Say what you did and what you did not.

---

*CS 211 · Week 11 · Problem Set 11 · © CSE Department*

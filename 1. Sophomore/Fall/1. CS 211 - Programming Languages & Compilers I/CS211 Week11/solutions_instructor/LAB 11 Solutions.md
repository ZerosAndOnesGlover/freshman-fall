# CS 211 · Lab 11 — Solutions
## Instructor Only

**Do not distribute.** Verified on LLVM/clang 18.1.3, x86-64, Python 3.14.2. Instruction counts are deterministic; JIT timings are not.

---

## Running the Lab

**Budget:** A 25, B 30, C 30, D 15 = 100 minutes against 110.

**This session is the afternoon Project 1 is due.** Open by saying that anyone unsubmitted should work on the project instead and will still be checked off. Mean it. **Then check, near the end, that everyone has actually submitted** — every year someone plans to do it at 16:55 and hits a problem at 16:50.

**Two predictable stalls.**

**Q4 will produce spurious mismatches** because students call `sc.cy`'s function `g`. It is `f`, and it takes two booleans. The lab says so; they will not read it. **Have the answer ready, and use it** — the harness being wrong rather than the compiler is the lesson, and L23 §7 records that this happened while writing the lecture too.

**Q9 needs `/tmp/gcd_o.ll` to exist**, which comes from Q7. If they skipped Q7 the loop prints eight `unsupported` lines and they conclude LLVM is broken.

---

## Part A — The Whole Thing, Once

**Q1.** The nine lines, as in L23 §1. `--emit=tac` gives 12 instructions for `gcd`; `--emit=cfg` gives 4 blocks and 4 edges.

**Q2.** **21** and **6**.

**Q3.** `file /tmp/gcd` reports `ELF 64-bit LSB pie executable, x86-64`. Exit code 21.

**Q4.** All should agree. The reference table (L23 §7) is 11 of 11.

**If a student reports a mismatch, check their function name and argument count before anything else.** `sc.cy` defines `f(a: bool, b: bool)`.

---

## Part B — What LLVM Does to Our IR

**Q5.** `gcd.ll`: **6 allocas, 17 load/stores** for a four-line function.

**Why terrible on purpose:** building SSA in a front end is real work — dominance frontiers, φ placement, renaming — and `mem2reg` does it for us. Emitting a stack slot per variable is trivially correct and is **what clang does**.

**Q6.**

| | lines | alloca | load/store | phi |
|---|---|---|---|---|
| ours | 42 | 6 | 17 | 0 |
| after `mem2reg` | 22 | **0** | **0** | **2** |

The φs are for `a` and `b` at the loop header `L0`. Exactly:

```llvm
L0:                                    ; preds = %cont6, %fn_gcd
  %b.addr.0 = phi i64 [ %b.in, %fn_gcd ], [ %t10, %cont6 ]
  %a.addr.0 = phi i64 [ %a.in, %fn_gcd ], [ %b.addr.0, %cont6 ]
```

Two predecessors — `fn_gcd` (the entry, carrying the parameters) and `cont6` (the loop body, carrying the updated values) — matching the CFG exactly.

**The Week 4 algorithm is SSA construction via dominance frontiers** (Cytron et al., 1991).

**Q7.**

| program | our TAC | our IR | `mem2reg` | `-O2` |
|---|---|---|---|---|
| `gcd` | 12 → 11 | 32 | 11 | **9** |
| `cls` | 23 → 23 | 57 | 20 | **10** |
| `fold` | 13 → 6 | 37 | 5 | **1** |

**`fold` becomes one instruction**, verbatim:

```llvm
define noundef i64 @f() local_unnamed_addr #0 {
entry:
  ret i64 19
}
```

The whole function computes a constant, and LLVM worked it out.

**Q8.** **The unfair part:** our TAC is dense; our LLVM IR is deliberately alloca-heavy. A large part of LLVM's percentage is undoing damage we chose to do, so comparing raw percentages flatters LLVM.

**Why `cls` survives it:** our optimiser was given 23 instructions of dense TAC — not our inflated IR — and removed **zero**. That is a fact about our optimiser and not about baselines.

*Push students who conclude "our optimiser is rubbish" toward L23 §5's closing point: three passes and a weekend against two decades. What Weeks 4–5 bought is the ability to read `-O2` output.*

---

## Part C — One IR, Many Machines

**Q9.** aarch64 **8**, ppc64le 10, sparcv9 11, x86-64 12, mips64 12, riscv64 **16**, wasm32 **23**, avr **124**.

**Q10.**

- **aarch64:** `sdiv x9, x0, x1` then `msub x1, x9, x1, x0`. ARM has divide but **no remainder instruction**, so the back end computes `q = a/b` then `a - q*b`. A peephole idiom, and Week 5 §8's material.
- **riscv64:** `call __moddi3`. **The RISC-V base integer ISA has no divide at all** — division is the optional `M` extension — so without it the back end calls a compiler-runtime helper. *(Students may know `rv64gc` includes `M`; the default `-march=riscv64` here does not.)*
- **wasm32:** WebAssembly has **structured** control flow — `block`, `loop`, `br_if` — and no arbitrary jumps. The back end must **reconstruct structure from our CFG**, which threw it away in Week 4. Accept "relooper" or "stackifier" if they know the term.

**Q11.** Every `i64` operation becomes eight bytes of manual work on registers that are 8 bits wide: load/store pairs, add-with-carry chains, and a called helper for the 64-bit modulo.

**Q12.** *(Discussion.)*

- *m* front ends × *n* back ends becomes *m* + *n*: neither side knows about the other, both know only the IR.
- **A cost that is not performance:** the IR becomes a **compatibility surface** that must express C's undefined behaviour, Rust's aliasing, Swift's ARC and Java's memory model at once — hence `poison`, `undef`, `noalias`, atomics, and a specification that is genuinely hard. *(Also acceptable: version churn, and being pinned to LLVM's release cadence.)*
- **Browser and microcontroller:** the table already answers it — `wasm32` and `avr` are both in it. Target LLVM and you have both.

---

## Part D — JIT

**Q13.** JIT ~37–45 ms; native ~4 ms.

**The comparison is meaningless** because `gcd(1071, 462)` takes microseconds. The 37 ms is **process startup plus JIT compilation of the module**, not the computation. Anyone presenting it as "the JIT is 9× slower" has measured `fork` and `exec`, which is the same error L23 §6 records in the phase-time table.

**Q14.** Four, with what each enables:

1. **Actual types** — a dynamic language can compile the integer path with a guard (V8, PyPy, LuaJIT).
2. **Actual branch behaviour** — code layout for the direction taken; Week 9 put a misprediction at 15–20 cycles.
3. **Actual call targets** — a monomorphic virtual call can be **inlined** with a guard. The largest single win for OO code.
4. **The actual machine** — AVX-512 if present, rather than a baseline build.

**Week 9's `Hoist.java` is (2) and warm-up generally:** the loop terminated while interpreted and hung once C2 compiled it. **What it says about testing: a fast test suite never gets the code hot**, so it tests a different program from the one that runs in production.

---

## If You Finish Early

**Q15.** `--emit=asm` calling `llc`. Straightforward.

**Q16.** The `Unsupported` message names the gap: a heap, `malloc`, an object layout, and — because Week 6 built a collector — stack maps for the roots. **PS 11 Part C.**

**Q17.** It does not currently work — `compile_to_llvm` emits only the selected function, so a call to another function has no definition. **PS 11 B2.** A student who fixes it here has done 8 marks of PS 11.

**Q18.** `-debug-pass-manager` lists well over a hundred passes. Recognisable ones: `SROA`/`mem2reg`, `InstCombine`, `GVN`, `LICM`, `SimplifyCFG`, `DCE`, `LoopUnroll`.

---

*CS 211 · Week 11 · Lab 11 Solutions · © CSE Department*

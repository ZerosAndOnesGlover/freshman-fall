# CS 211 · Problem Set 11 — Solutions and Mark Scheme
## Instructor Only

**Do not distribute.** Verified on LLVM/clang 18.1.3, x86-64.

> **Two problem sets fall on the same Friday** (PS 11 and PS 12), with Thanksgiving between
> release and deadline. **Part C is deliberately larger than the time available** and the brief
> says so — mark what is there.

---

## Part A — Reading the Output (18)

**A1.** *(5)* The nine phase lines and `exit code 21`. `cyanc.py` **sequences phases, parses arguments and reports** — it compiles nothing. The real-toolchain equivalent is **`gcc`/`clang` the driver**, as distinct from `cc1`.

**A2.** *(5)* 6 alloca / 17 load-store → **0 / 0 / 2 phi**. The φs are at `L0` for `a` and `b`, predecessors `fn_gcd` and `cont6`.

The algorithm is **SSA construction via dominance frontiers** (Cytron et al., 1991 — Week 4). We did not implement it because `mem2reg` does, and emitting one stack slot per variable is trivially correct; **clang does the same.**

*Full marks require matching the φ's incoming blocks against the CFG, not just counting them.*

**A3.** *(4)* **Every LLVM basic block must end with a terminator**; falling through into a label is not one. Our TAC permits fall-through — it is the interpreter's default.

**`runtime.py` could never find it because the constraint lives in the *target*.** An interpreter's instruction loop falls through by construction, so no interpreted program can violate a rule it does not have. You meet a target's constraints only when you emit for it.

**A4.** *(4)* parse 26.8%, opt 19.4%, llvm 15.3%, lex 13.7%; total 1.276 ms. **The front end (lex + parse) is ~40%.**

The two causes of the original `82.4%`: **(a)** `compile_to_llvm` re-ran parse and type-check from source instead of taking the AST; **(b)** `target_triple()` ran `llvm-config` as a **subprocess** on every call.

**(b) mattered far more** — fixing (a) alone moved it 82.4% → 80.5%.

The sentence: **profile before believing, and a subprocess is never free.** *(Full marks require identifying (b) as the dominant cause; a student naming only (a) has read the first fix and stopped.)*

---

## Part B — Extend the Back End (34)

**B1.** *(8)* `i1` for booleans, with `zext` at returns and `trunc`/`icmp ne 0` at uses. All four `sc.cy` cases must still agree with the interpreter. Expect a small reduction — the redundant `zext`/`icmp` pairs disappear.

**B2.** *(8)* Emit all functions, not one. Verify `fact` and `iseven`/`isodd` for n = 0…10 against the interpreter.

At `-O2` expect **inlining** of the small mutual pair and possibly **tail-call** conversion of `fact`. *Credit any student who finds `tail call` in the output and says what it means for stack depth.*

**B3.** *(10)* Three peephole rules, counts before and after, **and a correctness check against the interpreter on every program.**

**The marked part is the last bullet.** Running `opt -O2` after their pass will most often show **no difference in the final count** — LLVM already does all of these. **That is the expected finding and it is worth full marks**, provided they say so plainly rather than hiding it. A student who reports an improvement should be asked to show the counts.

**B4.** *(8)* SSA for temporaries only. Expect a substantial drop before `mem2reg` (temporaries are most of the allocas) and **essentially no difference after `-O2`**.

**The conclusion:** effort spent producing tidier IR that `mem2reg` was going to fix anyway is wasted; effort spent on things LLVM *cannot* recover — type information, aliasing facts, language-level invariants — is not. *(That is the professional version of this question and the reason it is here.)*

---

## Part C — Arrays and Structs (28)

**C1.** *(10)* `declare ptr @malloc(i64)`, a stated object layout, and `getelementptr` for field and element access.

**The universal stumbling block is that `getelementptr` does not dereference anything** — it computes an address. Every student meets this once; the error is a `load` of a `ptr` where the value was wanted, or vice versa.

Must compile, JIT, and agree with the interpreter on at least one program.

**C2.** *(8)* A length in the header, a compare, and a branch to a trap.

**LLVM will eliminate some checks** — where the index is a constant, or provably in range from a loop bound. Report how many and why. *(This is Week 5's dataflow reasoning, done by somebody else's compiler on our code.)*

**C3.** *(10 — a reading exercise with a paragraph)*

A front end must emit: **stack maps identifying which slots hold heap pointers at each safepoint** (`@llvm.gcroot`, or the `statepoint` intrinsics), and it must keep those roots in `alloca` slots rather than SSA registers so the collector can find and update them.

**What is still missing** should name at least: a collector runtime to call; safepoint placement; and the fact that **the collector cannot check the root set it is given** — L14 §2 — so a wrong stack map is a silent memory-safety bug with no assertion anywhere.

**Do not require working collection.** The paragraph is the mark.

---

## Part D — Written (20)

**D1.** *(6)* **The caveat:** our TAC is dense, our IR is deliberately alloca-heavy, so much of LLVM's percentage is undoing our own choice.

**Why `cls` survives it:** our optimiser was handed 23 instructions of **dense TAC** and removed **zero**.

**What Weeks 4–5 bought:** the ability to read `-O2` output and know what happened — and to write a front end whose IR LLVM can optimise. Not a competitive optimiser, which was never available in a term.

**D2.** *(6)* Three of: **riscv64** calls `__moddi3` because the base ISA has no divide; **wasm32** needs `block`/`br_if` because control flow is structured, so the back end reconstructs what our CFG discarded; **avr** is 8-bit doing 64-bit arithmetic; **aarch64** has `sdiv` but no remainder, hence `msub`.

*m* × *n* → *m* + *n*. **The cost:** the IR is a compatibility surface for every source language's semantics at once — `poison`, `noalias`, atomics, a hard specification. *(Accept: coupling to LLVM's release cadence and its C++ API churn.)*

**D3.** *(8)* Any coherent advice.

**For LLVM:** every back end free; a mature optimiser; a huge community. **Against:** an enormous dependency with a moving API, slow compile times, and an IR whose semantics you must understand precisely to avoid miscompilation.

**Real choices:** **Rust and Swift chose LLVM** and pay in build times and in tracking LLVM releases; **Go wrote its own back end** and gets fast compiles and fast bootstrapping at the cost of weaker optimisation; **Nim and early Haskell compiled to C** and got portability plus terrible debuggability; **TypeScript targets JavaScript**, which is a compilation target with a garbage collector already attached.

**Browser and microcontroller: LLVM already does both** — `wasm32` and `avr` are in the week's table. That is the answer the table exists to make available.

---

## Overall

**Expected distribution:** A should be high; B1–B2 are mechanical; **B3's honest "no difference" and B4's conclusion separate the class**, as does C3's paragraph.

**Two failure modes:**

1. **A B3 claiming their peephole pass improved on `-O2`.** Ask for the counts. LLVM does all three rules.
2. **A Part C that compiles but was never checked against the interpreter.** The differential check is free — `runtime.py` is in the folder — and is the whole reason the interpreter is still shipped.

---

*CS 211 · Week 11 · PS 11 Solutions · © CSE Department*

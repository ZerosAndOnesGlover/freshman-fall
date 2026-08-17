# CS 211 · Problem Set 5 — Solutions and Mark Scheme
## Instructor Only

**Do not distribute.** All counts verified against the Week 5 lab code.

---

## Part A — Liveness and the Def/Use Model (18)

**A1.** *(4 — half a mark per opcode for defs/uses, half for the non-variable slot)*

| opcode | writes | reads | not a variable |
|---|---|---|---|
| `copy` | `dst` | `a` | — |
| `unary` | `dst` | `b` | `a` is the **operator** |
| `load` | `dst` | `a`, `b` | — |
| `store` | — | `dst`, `a`, `b` | — *(and `a` may be an integer literal from an array-literal lowering)* |
| `getfield` | `dst` | `a` | `b` is the **field name** |
| `alloc` | `dst` | — | `a` is the **type name** |

Line citations should point at `tac.py`'s `emit` calls in `gen_stmt`/`gen_expr`. **Accept any consistent line numbering; reject answers with no citation** — the whole point of A1 is that the table is checkable against the generator.

**A2.** *(4)* `store` — `uses` never inspects `dst`, so the target array is invisible and the instruction computing it looks dead. **Unsound**: it removes code the program needs. `getfield` — `b` holds a field name that happens to be an identifier, so a non-existent variable is reported live. **Conservative**: it keeps code that could have gone.

**The `store` bug is worse.** A conservative analysis costs performance; an unsound one costs correctness. *(Full marks require both words used correctly. A common error is calling the `getfield` case "unsound because it's wrong" — it is wrong, but in the safe direction, and the distinction is the question.)*

**A3.** *(6)* Such a function **does** exist. The shortest is:

```cyan
fn f(m: [[int]]) -> int {
    m[0][1] = 7;
    return m[0][1];
}
```

The store writes through an undefined `t2`; the return reloads `m[0]` freshly into `t5` and reads element 1 of it, returning **the value that was there before**, not 7. *(Verified: 11 → 9 instructions, `t2 = m[t1]` deleted, `t5 = m[t4]` untouched.)*

*Mark generously on the exact program — several shapes work. Require that they explain **why the reload is not also folded away**, which is that the two `m[0]` computations are separate instructions and nothing in the Week 4 optimiser does common-subexpression elimination.*

**A4.** *(6 — 3 for the table, 3 for the argument)*

| analysis | direction | merge | initial |
|---|---|---|---|
| liveness | backward | ∪ | ∅ |
| reaching definitions | forward | ∪ | ∅ |
| available expressions | forward | ∩ | universe |
| dominators | forward | ∩ | universe |

A *may* analysis asks whether some path has a property, so it must start from "no path does" and **grow** as paths are discovered; starting full, it would converge to a fixed point that never shrinks below the initial over-approximation, and everything would be reported live. A *must* analysis asks whether all paths do, so it must start from "all do" and **shrink** as counterexamples appear.

**Both directions of error still reach *a* fixed point** — that is why the bug is dangerous. Swapping them does not hang; it silently returns the wrong answer. **Award the last mark only for noticing this.**

---

## Part B — Dominators and Loops (18)

**B1.** *(5)* Converges in **2 rounds**. Sets as printed by `loops.py`. Deduct for hand computations that omit the initialisation step.

**B2.** *(4)* Back edge: $n \to h$ with $h \in \text{DOM}[n]$. Natural loop: $h$ plus every node reaching $n$ without passing through $h$. In `scale`: back edge `B2 → L0`, loop `{L0, B2}`.

**B3.** *(4)* **Cyan has no `goto`, no `break` and no `continue`**, so within a single function every loop in the CFG comes from a `while`. Full marks for saying so and identifying `goto` (or labelled break) as the missing feature.

The second half is the real question. **Accept:** the back-end loop finder is still worth having because (a) the IR is shared with other front ends, (b) later passes create loops the parser never wrote, and (c) it is the same code for every source language. **Reject** "no, it's redundant" without engaging with (a)–(c).

**B4.** *(5)* `i = i + 1` lowers to:

```
    t11 = i + t10
    i   = t11
```

The naive detector finds **0** induction variables in every loop — verified on `scale.cy`, `div.cy` and the two-IV example. *(This is the actual history of `basic_ivs`: the first version returned an empty dict on every input and looked plausible doing it.)*

---

## Part C — Loop-Invariant Code Motion (28)

**C1.** *(6)* Six invariant instructions, all in `B2`; the only exit is `L0`; `B2 ∉ DOM[L0]`, so condition (1) fails for all six. **Zero hoistable is correct.**

**C2.** *(10)* With the relaxation, **all 6 hoist on `scale.cy`** and **both 2 hoist on `div.cy`**. *(Verified.)*

Is that right on `div.cy`? **Yes** — the two are the constants `100` and the loop's `1`, and neither can trap. The `sdiv` itself is never a candidate because `/` is not in `MOVABLE`.

*Mark the implementation, not the number: they must compute live-out of the whole loop (union of `OUT[b]` over blocks with successors outside it), not live-out of one block.*

**C3.** *(6)*

- **They hoist the same set** — neither moves the `sdiv`.
- **But for different reasons, and this is the mark.** Ours declines because `/` is absent from `MOVABLE` — a *trap* rule. LLVM's unrotated LICM declines because hoisting to the unguarded entry would speculate a faulting instruction — also a trap rule, but LLVM reaches it via `isSafeToSpeculativelyExecute` rather than an opcode allowlist. Meanwhile **our dominance condition (1) would have blocked it anyway**, and LLVM has already abandoned that condition. So: same outcome, two independent rules on our side, one on theirs.
- **The construction fails**, and the line that saves us is `MOVABLE` in `loops.py` — `/` and `%` are absent. Delete them into the set and the relaxed pass would hoist `100 / k` above the guard, so `scale(a, 0, 0)` returns 0 unoptimised and **traps** optimised.

*Full marks for a careful negative result naming the line. Zero for a fabricated program — check that any claimed counterexample actually runs.*

**C4.** *(6)* The predicate is **`isSafeToSpeculativelyExecute`**: may this instruction be executed when the original program would not have, with no observable effect?

Safe: `add`, `mul`, `and`, `lea`, `shl`, most bitwise ops. Unsafe: `sdiv`/`udiv` (divide by zero), `idiv` on `INT_MIN / -1` (overflow trap on x86), any load (may fault), anything with a side effect. **Accept two correct on each side.**

---

## Part D — Register Allocation (24)

**D1.** *(4)* 18 nodes, 69 edges. Top five: `a`, `k`, `n`, `s` at 15, `i` at 14. All live across the whole loop. **Pressure comes from long-lived values, not from expression count.**

**D2.** *(6)* Table as in the lecture; zero spills at $k = 7$; peak liveness 7.

Peak liveness is a lower bound **because those values must simultaneously exist**, and no assignment of fewer registers can hold them all — it is independent of algorithm. Chaitin matching it here does **not** generalise: colouring is NP-complete, the heuristic has no approximation guarantee, and one function proves nothing. *(Deduct for "so Chaitin is optimal".)*

**D3.** *(8)* Implementation 5, empirical result 3.

**Briggs frequently ties Chaitin on graphs this small**, and a careful negative result earns the full 3. The structural property: optimism pays when a node of degree $\ge k$ has neighbours that **share colours**, so fewer than $k$ distinct colours are actually taken. That needs a neighbourhood that is large but not a clique — Chaitin counts neighbours, Briggs counts *colours*.

**Reject any claimed win whose traces do not actually differ.** Ask to see both.

**D4.** *(6)* `scale.cy`: **69 edges and $k=7$ either way — no change**, because every copy there kills its source. `coalesce.cy`: **1 edge vs 2**, and `x`/`y` adjacency flips.

**Merely wasteful.** The principle, and this is the 2 marks that matter:

> **An optimiser defect that loses an *opportunity* is a performance bug. One that loses a
> *constraint* is a correctness bug.** Extra interference edges over-constrain and cost a
> register; missing ones under-constrain and miscompile. The two deserve completely
> different levels of alarm, and conflating them is how compilers ship miscompiles.

---

## Part E — Reading the Optimiser (12)

**E1.** *(6)* One explanation covering all three: **`-O1`, `-O2` and `-Os` optimise for different objectives.** `-O2` accepts a large instruction-count increase to vectorise, because throughput is its objective and the SIMD body processes eight elements per iteration. `-Os` has size as its objective and declines the same transformation, landing on `-O1`'s footprint and paying 1.75×. **Instruction count is not a proxy for speed in either direction.**

**E2.** *(6)* Annotation as in the Lab 5 solutions.

**The optimisation not visible: register allocation has no instruction of its own.** It shows up as the *absence* of loads and stores — `%eax` holds `s` across the whole loop and never spills. Accept also "spilling", "peephole" (arguably visible in `xorl`), or "instruction selection" if argued that `leal` is attributed to LICM instead. **The intended answer is register allocation, and the intended insight is that the passes which work best leave no trace.**

---

## Mark Distribution

| Part | Points |
|---|---|
| A | 18 |
| B | 18 |
| C | 28 |
| D | 24 |
| E | 12 |
| **Total** | **100** |

**Expect the median around 62.** The hard marks are A4's last point, C3's negative result, D3's structural explanation, and D4's principle. **C3 and D3 are where honest students separate from confident ones**, which is what the closing note on the sheet is for — quote it back at anyone who fabricates.

---

*CS 211 · Week 5 · PS 5 Solutions · Instructor Only · © CSE Department*

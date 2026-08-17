# CS 211 · Lab 5 — Solutions
## Instructor Only

**Do not distribute.** Timings vary by machine; instruction counts and graph sizes do not.

---

## Running the Lab

**Budget:** A 20, B 20, C 35, D 25, E 30 = 130 minutes against a 110-minute session. **Part E is the one to protect** — if the room is behind at 15:10, hand out the Q15/Q16 numbers and have them do Q17 only. Q17 is where the week lands.

**The predictable stall is Q7.** Students see `hoistable=0` and assume they have broken something. Have the answer ready: *the exit test is in the header, the body comes after it, so the body cannot dominate the exit.* Say it at the front of the room once someone raises a hand, because everyone hits it within a minute of each other.

---

## Part A

**Q1.** Deleted: `t1 = 0` and `t2 = m[t1]`. The surviving `t2[t3] = t0` writes through `t2`, which is now **never defined** — whatever is in that location.

**Q2.** Week 4's `Instr.uses` inspects only the `a` and `b` slots. `store` keeps its target array in **`dst`**, so the array never appears as a use, the `load` that computed it looks dead, and DCE removes it.

**Q3.** Week 4 prints `t2 = t3 store t0`; Week 5 prints `t2[t3] = t0`.

The Week 4 spelling **asserts that `t2` is defined here** — the exact opposite of the truth, on the exact instruction being mishandled. A student reading that dump would confirm the deletion as correct.

> **The intended lesson:** the syllabus's debugging method — dump every representation, find the
> first wrong one — is only as good as the dump. Accept any answer that reaches this. Push back on
> "the printer is cosmetic."

---

## Part B

**Q4.** Single block `fn_scale` for `nested.cy`; for `scale.cy` four blocks. `IN[fn_scale] = {a, k, n}`, `OUT = {}`.

**Q5.** Yes, and yes they should be. A parameter *not* live on entry means the function never reads it on any path — which is legal, and is exactly the analysis that lets a compiler warn about an unused parameter or drop it from the calling convention under LTO.

**Q6.** **7.** At `t5 = 1` in `B2`, with `{a, i, k, n, s, t4, t5}` live.

---

## Part C

**Q7.** Dominators as printed. The loop is header `L0`, body `{L0, B2}`, and the only exit is `L0` — the header carries the `ifz`. The six invariant instructions are all in `B2`. **`B2` does not dominate `L0`**, so condition (1) fails for every one of them.

**This is correct behaviour**, not a bug. Mark hard on students who call it a bug without checking the dominance relation.

**Q8.** `k * 2 + 1` lands in the **entry block**, above `br label %6`. **It is not guarded** — nothing tests `n` before it.

**Q9.** `%7 = sdiv i32 100, %2` stays inside the loop body. With `n = 0` the loop never runs, so the source never divides; hoisting it to the unguarded entry divides anyway, and with `k = 0` the optimised program traps where the original returns 0.

**Q10.**

| | unrotated | rotated |
|---|---|---|
| `k * 2 + 1` | hoisted, unguarded (entry block) | hoisted into guarded `.lr.ph` |
| `100 / k` | **stays in the loop** | hoisted into guarded `.lr.ph` |

Rotation alone hoists **nothing** — `%5 = mul`, `%6 = add` remain in the loop.

**One sentence:** rotation performs no optimisation; it restructures the CFG so that the guard exists, which makes hoisting non-speculative and therefore legal for instructions that can trap.

**Q11.** Adding `'/'` to `MOVABLE` still hoists **0** — the dominance condition catches it first. *(Verified.)*

**The expected answer:** the dominance rule is easier to trust because it is a property of the graph and is checked by the same code for every opcode; the trap rule requires a correct per-opcode judgement about what can fault, and is therefore a table that can be wrong. **The honest answer is that LLVM needs both**, because the dominance rule alone forbids the hoist that makes the optimisation worth having. Give full credit for either side argued from the measurement.

---

## Part D

**Q12.** 18 nodes, 69 edges. Highest degree: `a`, `k`, `n`, `s` (15), `i` (14). **They are all live across the entire loop** — the three parameters, the accumulator, and the counter — so every temporary in the body interferes with them.

Zero spills first at **k = 7**, matching Q6's peak liveness of 7 exactly.

**The match means Chaitin is optimal on this function.** Peak liveness is a hard lower bound for any allocator whatsoever, and the heuristic reached it. Do not let students generalise this to "Chaitin is optimal" — Q12 is one function.

**Q13.** At `k = 3` the first spill is `t1`, degree 4, cost 2, ratio 0.50.

The 10 is $10^{\text{loop depth}}$, standing in for an unknown trip count. It is not 2 because it must be large enough that **no number of outer-loop references outweighs one inner-loop reference** — with 2, a variable referenced three times outside a loop would outrank one referenced once inside, which is backwards.

**Q14.** On `scale.cy`: **69 edges and k = 7 both ways — no change.** Every `copy` in `scale` kills its source (`s = t9` where `t9` is used nowhere else), so `others -= uses(ins)` removes something that was not in the live set anyway.

On `coalesce.cy`: **1 edge with the exception, 2 without**, and `x`/`y` become adjacent without it.

**Merely wasteful, not incorrect.** Adding an edge that need not be there over-constrains the graph — it can cost a register, never correctness. **Removing** an edge that should be there assigns one register to two simultaneously-live values, which is a miscompile. *The general principle: an optimiser defect that loses an opportunity is a performance bug; one that loses a constraint is a correctness bug, and the two deserve completely different levels of alarm.*

---

## Part E

**Q15/Q16.**

| Level | instructions | runtime |
|---|---|---|
| `-O0` | 28 | 45 ms |
| `-O1` | 15 | 13 ms |
| `-O2` | 57 | 8 ms |
| `-O3` | 57 | 7 ms |
| `-Os` | 15 | 14 ms |

**The surprise is `-O2` at 57.** It vectorised: `grep xmm s-O2.s` shows `pmuludq`, `pshufd`, `movdqu` — eight elements per iteration, paid for with setup, an alignment test and a scalar remainder loop.

**`-Os` declined the vectorisation on size grounds** and lands exactly on `-O1`'s 15 instructions, 1.75× slower than `-O2`. These are different objectives, not different amounts of effort.

**The checksum column is the most important** because it is the only one that says the compiler was *correct*. Every other column is a performance claim; that one is a correctness claim, and without it the rest is meaningless — the fastest possible code computes nothing at all.

**Q17.**

```asm
        testl   %esi, %esi          # rotation guard
        jle     .LBB0_1
        leal    1(,%rdx,2), %ecx    # k*2+1: LICM + strength reduction + selection
        movl    %esi, %edx
        xorl    %esi, %esi          # peephole: shorter than movl $0
        xorl    %eax, %eax          # s = 0, and %eax holds s for the whole loop
.LBB0_3:
        movl    (%rdi,%rsi,4), %r8d # a[i]
        imull   %ecx, %r8d
        addl    %r8d, %eax
        incq    %rsi                # induction variable, step 1
        cmpq    %rsi, %rdx
        jne     .LBB0_3
        retq
```

`%eax` holds `s` across the entire loop and never touches memory — that is register allocation, and it is invisible precisely because it worked.

---

## Q18 / Q19 (early finishers)

**Q18** is PS 5 D3. Do not give the answer; the point is that on small graphs Briggs often ties Chaitin, and discovering that is worth more than being told.

**Q19** should show inner-loop references weighted 100 and outer 10. If a student's numbers are 10 and 1, their `find_loops` is only finding the outer loop — a good bug to have them chase.

---

## Sign-Off

Check for: Q1 with both instructions **named**; Q10's table with all four cells; Q12's comparison stated as *"7 and 7, so optimal here"*; Q16 with the two columns side by side.

**A student who reports Q14 as "no change" on `scale` and stops has done the measurement and missed the question.** Send them to `coalesce.cy`.

---

*CS 211 · Week 5 · Lab 5 Solutions · Instructor Only · © CSE Department*

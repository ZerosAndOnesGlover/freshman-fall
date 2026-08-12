# CS 211 · Lab 4
## Building and Reading a Control-Flow Graph

---

**Week 4 · Friday 14:00–15:50 · BH 220** — after both of this week's lectures.
**Unmarked.** The TA checks your work off in the session.
**Starter files:** `tac.py`, `opt.py`, `gcd.cy`, `gcd.c`, `fold.cy`, plus the Weeks 1–3 front end.

> **Midterm 1 was sat on Wednesday.** This lab is the first back-end content and is not examined on
> it.

---

## Why This Lab Exists

L09 claimed our CFG and LLVM's are the same graph for the same function. L10 claimed `mem2reg` replaces eleven memory operations with two φ-nodes. **Both are checkable in about four commands**, and you should not take either on trust.

The lab then does the thing that actually builds intuition: **you break the optimiser in a specific way and watch it produce wrong answers**, which is the failure mode that matters in a compiler and the one that is hardest to notice.

---

## Part 1 — TAC and Basic Blocks (25 minutes)

```bash
python3 tac.py gcd.cy
```

**Q1.** Record the TAC. **There is no `while` in it.** Name the three instructions the loop became, and say which one makes it a *loop* rather than a forward branch.

**Q2.** The CFG has four blocks. **For each, give its predecessors and successors.** Which block is the loop header, and what makes it one?

**Q3.** `L0` has two predecessors. **One is the function entry; the other is inside the loop.** Explain why that second edge is what Week 5 will use to detect that a loop exists at all.

### 1.1 Short-circuit lowering

```bash
printf 'fn f(a: bool, b: bool) -> bool { return a && b; }\n' > sc.cy
python3 tac.py sc.cy
```

**Q4.** `&&` produced a **branch**, not a binary operation. **Quote the instruction that skips the right operand**, and say what would break in a real program if `&&` were lowered as an ordinary operator.

**Q5.** Write, by hand, the TAC you expect for `a || b`. Then check. **Which instruction differs from the `&&` version, and why?**

---

## Part 2 — The Same Graph, in LLVM (25 minutes)

```bash
clang -S -emit-llvm -O0 -o - gcd.c | sed -n '/define/,/^}/p'
```

**Q6.** LLVM's function has four blocks too. **Match them to ours** — build a two-column table. LLVM prints `; preds = ...` on each block; confirm the predecessor sets agree with `tac.py`'s.

**Q7.** LLVM's `-O0` output contains three `alloca`, six `load` and five `store` instructions. **Ours contains none.** What is LLVM doing that we are not, and why does it do it at `-O0`?

### 2.1 mem2reg

```bash
clang -S -emit-llvm -O0 -Xclang -disable-O0-optnone -o o0.ll gcd.c
opt -passes=mem2reg -S o0.ll
```

**Q8.** Fill in the table:

| | instructions | alloca | load | store | phi |
|---|---:|---:|---:|---:|---:|
| `-O0` | | | | | |
| after `mem2reg` | | | | | |

**Q9.** Two φ-nodes appear. **For each, say which Cyan/C variable it corresponds to** and why *that* variable needed one.

**Q10.** Take the first φ:

```llvm
%.01 = phi i32 [ %1, %2 ], [ %6, %5 ]
```

**Translate it into English**, naming what `%1`, `%2`, `%6` and `%5` each are. Then say what fact about the loop this single line states.

---

## Part 3 — Constant Folding (25 minutes)

```bash
python3 opt.py fold.cy
```

**Q11.** Record the before and after instruction counts. **Which three assignments survive that LLVM's `-O1` removes?**

```bash
clang -S -emit-llvm -O1 -o - fold.c | sed -n '/define/,/^}/p'
```

**Q12.** LLVM produces a single instruction. **What would our dead-code pass need to be able to prove** in order to match it? Name the analysis, and the week it arrives.

### 3.1 The negative-literal trap

```bash
printf 'fn f() -> int {\n  let q = -7 / 2;\n  let r = -7 %% 2;\n  return q * 100 + r;\n}\n' > neg.cy
python3 opt.py neg.cy
```

**Q13.** It folds to `-301`. **Now break it**: in `opt.py`, remove the `unary` case from `const_fold` and rerun.

**How much folds now?** Explain, referring to `The Cyan Language Reference` §2 and what `-7` actually is at the token level.

**Restore it afterwards.**

### 3.2 Breaking the optimiser in the way that matters

**Q14.** In `opt.py`'s `FOLDABLE`, change the `/` entry to use Python's floor division:

```python
'/': lambda a, b: a // b if b else None,
```

Rerun `neg.cy`.

- **What does it fold to now?**
- **What does C say?** (`gcc` the equivalent and check.)
- **Did any error appear?**

**Q15.** That change made the compiler produce a **different answer** for a correct program, silently.

**Say why this class of bug is worse than a crash**, and how you would catch it. **Then restore the correct division.**

---

## Part 4 — Reading a Bigger CFG (15 minutes)

```bash
printf 'fn classify(n: int) -> int {\n  if n < 0 { return 0; }\n  if n == 0 { return 1; }\n  while n > 100 { n = n / 2; }\n  return n;\n}\n' > cls.cy
python3 tac.py cls.cy
```

**Q16.** **Draw the CFG on paper.** How many blocks, and how many have two successors?

**Q17.** Which blocks have **no** successors, and what do they all have in common?

**Q18.** Compile the C equivalent with `clang -S -emit-llvm -O0` and compare block counts. **If they differ, account for the difference** — it will be about entry blocks and empty labels, not about control flow.

---

## Before You Leave

The TA checks:

- [ ] **Part 1** — the four blocks with preds/succs; Q4's branch instruction quoted
- [ ] **Part 2** — the mem2reg table filled in (**23 → 11**, 11 memory ops → 2 φ); Q10 translated
- [ ] **Part 3** — Q13 run **and reverted**; **Q14 run and reverted**, with Q15 answered
- [ ] **Part 4** — the CFG drawn, with the two-successor blocks identified

**Q15 is the checkoff that matters.** A student who cannot say why a silently-wrong optimiser is worse than a crashing one has missed the point of the whole back end.

---

## If You Finish Early

**Implement `--dump-cfg` as a Graphviz file.** Emit `digraph { L0 -> L1; L0 -> B2; ... }` and render with `dot -Tpng`. Compare your picture against `opt -passes=dot-cfg`, which LLVM ships.

**Then the real exercise:** find a Cyan program where your CFG has an **unreachable block**. Does `tac.py` notice? Should it? What would LLVM do?

---

*Next: Week 5 — with the CFG built, loop-invariant code motion, induction variables, and register allocation by graph colouring.*

# CS 211 · Lab 5
## Optimised and Unoptimised Assembly

**Friday of Week 5 · 14:00–15:50 · BH 220 · covers Week 5**
**Unmarked and mandatory.** The TA checks you off in the session. `COURSE POLICIES.md` costs you a letter grade after a second unexcused absence.

**Bring:** a terminal. Everything is in this folder.

> **Lab 5 covers Week 5.** Both of this week's lectures have already happened. If you have not
> read L11 and L12, the first hour will be slow — §5 onward assumes you know what a back edge is.

---

## Setup

```bash
cd "CS211 Week5/lab"
python3 live.py scale.cy scale        # should print a liveness table
clang --version                       # 18.1.3 in BH 220
opt --version
```

If any of those fail, get the TA now rather than at 15:30.

---

## Part A — The Bug You Have Been Shipping (20 min)

**Q1.** Run Week 4's optimiser on the three-line program in `nested.cy`:

```bash
python3 opt.py nested.cy g
```

It goes from 8 instructions to 6. **Which two disappeared, and what does the surviving `store` now write through?**

**Q2.** Run `python3 live.py nested.cy g`. It removes nothing.

State, in one sentence, **why liveness keeps the `load` when the Week 4 pass did not.** Your answer must name the slot that Week 4's `Instr.uses` fails to inspect.

**Q3.** Open `tac.py` and find the `load` and `store` cases in `__repr__`. They are new this week. **Check out the Week 4 copy of `tac.py` and dump `nested.cy` again:**

```bash
python3 ../../"CS211 Week4"/lab/tac.py nested.cy g
```

The store prints differently. **Write down both spellings.** Which of the two would have let you find this bug by reading the dump, and what does that tell you about the debugging method the syllabus recommends?

---

## Part B — Liveness (20 min)

**Q4.** Run `python3 live.py scale.cy scale`. Record `IN` and `OUT` for every block.

**Q5.** `a`, `n` and `k` are parameters. **Are they in `IN` of the entry block? Should they be?** What would it mean if a parameter were *not* live on entry?

**Q6.** Add this to `live.py` and run it:

```python
peak = 0
for b in blocks:
    for ins, la in zip(b.instrs, live_points(b, OUT[b.name])):
        peak = max(peak, len(set(la) | defs(ins)))
print("peak simultaneous live:", peak)
```

**Record the number. You will need it in Q12.**

---

## Part C — Loops, LICM, and the One Operator That Matters (35 min)

**Q7.** `python3 loops.py scale.cy scale`. Record the dominator sets, the natural loop, and the two numbers on the `licm:` line.

**It reports 6 invariant instructions and 0 hoistable. Explain why**, in terms of which block dominates which. Do not call it a bug until you have.

**Q8.** Now LLVM, on the same loop in C:

```bash
clang -O0 -Xclang -disable-O0-optnone -S -emit-llvm scale.c -o s0.ll
opt -passes='mem2reg,loop-simplify,loop-mssa(licm)' -S s0.ll | grep -nE '^[a-z0-9._]+:|mul|add'
```

*(If you drop `loop-mssa(...)` `opt` will refuse with `LICM requires MemorySSA`. Try it once so you recognise the error.)*

**Where did `k * 2 + 1` end up? Is that block guarded by anything?**

**Q9.** Repeat Q8 on `div.c`, which is the same loop with `100 / k` instead:

```bash
clang -O0 -Xclang -disable-O0-optnone -S -emit-llvm div.c -o d0.ll
opt -passes='mem2reg,loop-simplify,loop-mssa(licm)' -S d0.ll | grep -nE '^[a-z0-9._]+:|sdiv'
```

**The division did not move. Why not?** Answer in terms of a program where `n = 0` and `k = 0`.

**Q10.** Add rotation and run both again:

```bash
opt -passes='mem2reg,loop-simplify,loop-mssa(loop-rotate,licm)' -S d0.ll | grep -nE '^[a-z0-9._]+:|sdiv'
```

Fill in the table:

| | unrotated | rotated |
|---|---|---|
| `k * 2 + 1` | | |
| `100 / k` | | |

**Then run rotation *without* LICM.** Does rotation hoist anything by itself? **State in one sentence what rotation actually does for the optimiser.**

**Q11.** Find the `MOVABLE` set in `loops.py`. `/` and `%` are missing. **Add `'/'` to it** and re-run `loops.py` on `div.cy`. Nothing hoists, because of Q7's dominance condition — so our compiler is saved by a *different* rule than LLVM's.

**Which of the two rules would you rather rely on, and why?** Two sentences.

---

## Part D — Register Allocation (25 min)

**Q12.** Run `python3 regalloc.py scale.cy scale 4`.

- How many nodes and edges?
- Which five variables have the highest degree, and what do they have in common?
- Read the bottom table. **At which `k` does spilling first reach zero?**
- **Compare that with your Q6 answer.** What does the match mean?

**Q13.** Change `k` on the command line to 3 and read the trace. **Which variable is spilled first, and what were its degree and cost?** Then find `spill_costs` in `regalloc.py` and explain where the number 10 comes from and why it is not 2.

**Q14.** In `interference()` there is a three-line special case for `copy` — the move exception. **Comment it out and re-run on `scale.cy`.**

**The edge count does not change. Neither does the zero-spill `k`.** Before reading on, predict why.

Now run both versions on `coalesce.cy`:

| | edges | `x` adjacent to `y`? |
|---|---|---|
| with the exception | | |
| without | | |

**It matters here and not in `scale`. What is different about the copy?** Your answer should be about whether the source of a copy is still live after it — and once you have it, go back and confirm it against every `copy` instruction in `scale`'s TAC dump.

**Finally: is the version with the exception removed *incorrect*, or just worse?** This distinction is the whole of L12 §2 — be precise, because the two words mean very different things about a compiler.

---

## Part E — What `-O2` Actually Does (30 min)

**Q15.** Emit assembly at five levels and count instructions:

```bash
for o in O0 O1 O2 O3 Os; do
  clang -$o -S scale.c -o s-$o.s
  echo "-$o $(grep -cE '^\s+[a-z]' s-$o.s)"
done
```

**Record all five. One of them should surprise you — say which and why.**

**Q16.** Now time them. `drv.c` is a driver; build and run each level:

```bash
for o in O0 O1 O2 O3 Os; do
  clang -$o -c scale.c -o sc.o
  clang -O2 drv.c sc.o -o drv
  printf "%-4s " -$o; ./drv
done
```

**Tabulate instruction count against runtime.** Then answer:

- `-O2` has roughly four times `-O1`'s instructions and is faster. **What did it spend them on?** (`grep xmm s-O2.s` will tell you.)
- `-Os` produces the same instruction count as `-O1`. **What did it decline to do, and on what grounds?**
- The checksum is identical in all five rows. **Why is that the most important column in the table?**

**Q17.** Read the `-O1` assembly, which is short enough to read whole:

```bash
sed -n '/^scale:/,/\.size/p' s-O1.s
```

**Point at, by line:**
- the guard that rotation introduced
- the instruction that is `k * 2 + 1`, hoisted out of the loop
- the induction variable update
- the register holding `s` across the whole loop

**Every optimisation from both of this week's lectures is in that listing.** That is the point of the lab.

---

## If You Finish Early

**Q18.** Implement Briggs' optimistic colouring in `regalloc.py`: instead of committing to a spill in the simplify phase, push the node anyway and only spill in SELECT if no colour is free. Find a function where it beats Chaitin. *(This is PS 5 Part D — starting it here is encouraged.)*

**Q19.** Write a Cyan function with two nested loops and check that `spill_costs` weights the inner one 100× and the outer 10×.

---

## Before You Leave

Show the TA:

1. Your Q1 answer — the two deleted instructions, named.
2. Your completed Q10 table, all four cells.
3. Your Q12 comparison of zero-spill `k` against peak liveness.
4. Your Q16 table, instruction count beside runtime.

---

*CS 211 · Week 5 · Lab 5 · © CSE Department*

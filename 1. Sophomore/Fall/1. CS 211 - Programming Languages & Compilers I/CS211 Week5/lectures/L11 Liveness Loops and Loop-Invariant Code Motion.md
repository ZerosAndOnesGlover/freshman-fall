# CS 211 · Programming Languages & Compilers I
## Week 5 · Lecture 1 of 2
### Liveness, Loops, and Loop-Invariant Code Motion

---

**Reading:** Dragon §9.2 (revisit), §9.5, §9.6.1–9.6.4 · **Next:** L12, register allocation and the pipeline

---

## 1. Week 4's Optimiser Deletes Code It Needs

Start with the bug, because it is yours and it has been in your compiler for a week.

`nested.cy` is three lines:

```cyan
fn g(m: [[int]]) -> int {
    m[0][1] = 7;
    return 0;
}
```

Run it through the Week 4 optimiser:

```
$ python3 opt.py nested.cy g
```

```
; ---- before: 8 instructions ----
fn_g:
    t0 = 7
    t1 = 0
    t2 = m[t1]
    t3 = 1
    t2[t3] = t0
    t4 = 0
    ret t4

; ---- after: 6 instructions ----
fn_g:
    t0 = 7
    t3 = 1
    t2[t3] = t0
    t4 = 0
    ret t4
```

**Look at what survived.** The store still writes into `t2`. The instruction that *computed* `t2` is gone.

`m[0][1] = 7` needs two steps: find the row `m[0]`, then store into element `1` of it. Dead-code elimination deleted the first one. The optimised program writes 7 through whatever happens to be in that register.

**No error. No warning.** The pass reported `round 1: dce changed the code` and was pleased with itself.

---

## 2. The Printer Was Lying Too

Before this week, that dump did not read the way you just read it. `store` had no case in `Instr.__repr__`, so it fell through to the generic binary form and printed:

```
    t2 = t3 store t0
```

**Which says `t2` is defined here.** It is not — it is *read*, and written *through*. The dump asserted the exact opposite of the truth, about the exact instruction that was being mishandled.

Week 5's `tac.py` adds the missing cases, and the same instruction now prints `t2[t3] = t0`.

> **The syllabus told you the debugging method is to dump each representation and find the first
> one that is wrong. That method is only as good as the dump.** A printer that misreports a def
> will hide a def bug for as long as you are willing to trust it. Fixing the printer is not
> cosmetic work you do when you have spare time; it is the instrument you are about to take
> measurements with.

---

## 3. The Root Cause: Guessing From Shape

Here is Week 4's `Instr.uses`:

```python
def uses(self):
    out = []
    for x in (self.a, self.b):
        if isinstance(x, str) and (x.startswith('t') or x.startswith('%')
                                   or x.isidentifier()):
            ...
```

It decides whether an operand is a variable by **looking at the operand**. That fails in two directions at once.

**It misses real uses.** `store` and `setfield` keep their target in the `dst` slot, and `uses` never looks at `dst`. So the array in `a[i] = v` is invisible, and the instruction that produced it looks dead. **This is the unsafe direction — it deletes live code**, which is what section 1 showed you.

**It invents fake ones.** `getfield` puts a *field name* in an operand slot. `alloc` puts a *type name* there. Both are identifiers, so `p.x` reports a use of a variable called `x` that does not exist anywhere in the program. This direction is merely conservative for DCE — a fake use keeps code alive, which is safe — but in L12 it will invent interference edges and cost you real registers.

**The fix is not a better heuristic.** It is to stop asking what an operand *looks like* and write down what each opcode *means*:

```python
SLOTS = {
    'copy':     (('dst',), ('a',)),
    'unary':    (('dst',), ('b',)),        # `a` is the operator, not a var
    'call':     (('dst',), ('b*',)),       # `a` is the callee name
    'load':     (('dst',), ('a', 'b')),
    'store':    ((),      ('dst', 'a', 'b')),   # writes THROUGH dst, reads it
    'getfield': (('dst',), ('a',)),        # `b` is the field name
    'setfield': ((),      ('dst', 'b')),   # `a` is the field name
    'alloc':    (('dst',), ()),            # `a` is the type name
    ...
}
```

Fifteen lines, one per opcode, and every analysis in this course from here to Week 11 reads it. `live.py` also ships `check_coverage`, which raises if the code contains an opcode the table does not mention — **an unknown opcode would otherwise get empty def and use sets, which is silently unsafe in exactly the way section 1 demonstrated.**

> **A table you can read is worth more than a rule you have to trust.** The rule was four lines
> and wrong in two directions. The table is fifteen lines and checkable by eye, opcode by opcode,
> against `tac.py`'s `emit` calls.

---

## 4. Liveness

**A variable is *live* at a point if some path from that point reads it before writing it.**

That is the whole definition, and notice it is a statement about the *future*, which is why the analysis runs backwards.

L10 gave you dataflow as one algorithm with two knobs — direction and merge. Liveness sets them to **backward** and **union**:

$$\text{OUT}[B] = \bigcup_{S \in \text{succ}(B)} \text{IN}[S]$$

$$\text{IN}[B] = \text{use}[B] \;\cup\; (\text{OUT}[B] - \text{def}[B])$$

where `use[B]` is read-before-written in `B`, and `def[B]` is written anywhere in `B`.

**Union, because liveness is a *may* property.** A variable is live if there *exists* a path to a use. One path is enough to make it live on all of them, so merging successors means taking everything any of them needs.

Start every set empty and grow. Fixed-point iteration for the fourth time this term — after ε-closure in Week 1, FIRST/FOLLOW in Week 2, and the folder in Week 4.

```
$ python3 live.py nested.cy g
```

```
; ---- liveness for g: fixed point after 2 rounds ----
fn_g       IN ['m']                              OUT []

; ---- dce: 8 -> 8 instructions (0 removed) ----
```

**Eight in, eight out.** The `load` is kept, because `t2` is live at the store that reads it. The same program, the same pass, a def/use model that is not guessing.

### Liveness at every instruction, not just every block

Block-level IN/OUT is what the fixed point computes, but optimisation needs the live set at *each instruction*. You get it by replaying the same transfer function one instruction at a time, backwards from `OUT[B]`:

```python
live = set(out_set)
for i in reversed(range(len(b.instrs))):
    points[i] = set(live)            # live-OUT of instruction i
    live = uses(ins) | (live - defs(ins))
```

**Same equation, finer grain.** This is the array L12 builds the interference graph from.

---

## 5. A Loop Is a Property of the Graph

The front end knew what a `while` was. The back end does not — Week 4 lowered it to labels and branches and threw the tree away.

So the optimiser has to *rediscover* loops, and the definition it uses is graph-theoretic:

**$d$ dominates $n$** when every path from entry to $n$ passes through $d$.

```
DOM[entry] = {entry}
DOM[B]     = {B} ∪ ⋂ DOM[P] for P ∈ pred(B)
```

**Intersection, and start from the universe** — because dominance is a *must* property, the mirror image of liveness. Compare the two and the pattern from L10 §7 is complete:

| | direction | merge | initial | why |
|---|---|---|---|---|
| **liveness** | backward | ∪ | ∅ | *may* — one path suffices |
| **dominators** | forward | ∩ | everything | *must* — all paths required |

**A back edge is an edge $n \to h$ where $h$ dominates $n$.** The **natural loop** it heads is $h$ together with every node that can reach $n$ without passing through $h$.

```
$ python3 loops.py scale.cy scale
```

```
; ---- dominators for scale (fixed point after 2) ----
fn_scale   dom by ['fn_scale']
L0         dom by ['L0', 'fn_scale']
B2         dom by ['B2', 'L0', 'fn_scale']
L1         dom by ['L0', 'L1', 'fn_scale']

; ---- 1 natural loop(s) ----
  <loop header=L0 body=['B2', 'L0'] exits=['L0']>
```

**Why bother, when the parser already knew?** Because this definition finds loops the parser never saw — loops built from `goto`, loops created by earlier optimisation passes, loops in IR that arrived from another front end entirely. A pass that pattern-matched on the AST's `While` node would find none of them, and would have to be rewritten for every language that shares the back end. **LLVM optimises code from C, Rust, Swift and Haskell with one loop analysis, and this is why.**

---

## 6. Loop-Invariant Code Motion, and the Condition That Hoists Nothing

An instruction is **invariant** in loop $L$ if every variable it reads is either defined nowhere in $L$, or defined exactly once in $L$ by an instruction already known invariant. Recursive, so iterate to a fixed point.

`scale.cy` has an obvious candidate:

```cyan
while i < n {
    let f = k * 2 + 1;          // k, 2 and 1 never change in the loop
    s = s + a[i] * f;
    i = i + 1;
}
```

Run it:

```
; ---- licm: 23 -> 23 in loop body ----
;  L0: body=['B2', 'L0'] invariant=6 hoistable=0
```

**Six invariant instructions. Zero hoisted.** That is not a bug. It is the textbook safety condition doing exactly what it says.

### The three conditions

To move an instruction to the preheader — Dragon §9.5.3, plus one:

1. **Its block dominates every exit of the loop.** Otherwise the loop might exit before reaching it, and hoisting makes it run when the source says it should not.
2. **Its destination has exactly one definition in the loop.** Otherwise "the" value is not well defined.
3. **It cannot trap.** Section 7.

**Condition 1 can never hold for a `while` body.** Look at the CFG again: the exit test is in the header `L0`, and the body `B2` comes after it. `B2` does not dominate `L0`. For *any* `while` loop, lowered this way, the body never dominates the exit — so textbook LICM hoists nothing at all.

That is a real and slightly alarming result, and it is the right one. **Condition 1 is a blanket ban on running code the program might not have run.** Applied literally to a bottom-tested loop, it bans everything.

---

## 7. Speculation, and the One Operator That Changes the Answer

So what do real compilers do? Measure it.

`scale.c` is the same loop in C. Compile it to unoptimised IR and run LICM by itself:

```
$ clang -O0 -Xclang -disable-O0-optnone -S -emit-llvm scale.c -o s0.ll
$ opt -passes='mem2reg,loop-simplify,loop-mssa(licm)' -S s0.ll
```

*(LICM must run inside the `loop-mssa` pass manager — `opt` hard-errors with*
*`LICM requires MemorySSA` otherwise.)*

```
  %4 = mul nsw i32 %2, 2
  %5 = add nsw i32 %4, 1
  br label %6
6:                                        ; preds = %8, %3
```

**LLVM hoisted it.** `k * 2 + 1` is now in the entry block, above the loop — and the loop was *not* rotated, so LLVM violated condition 1 on purpose.

Now change one operator. `div.cy` and `div.c` are the identical loop with `100 / k` in place of `k * 2 + 1`:

```
$ opt -passes='mem2reg,loop-simplify,loop-mssa(licm)' -S d0.ll
```

```
6:                                        ; preds = %4
  %7 = sdiv i32 100, %2
```

**The division stayed in the loop.** Same pass, same loop shape, same invariance — and LLVM refused.

### Why

If `n <= 0` the loop body never runs. Hoisting `100 / k` above the loop executes a division the source program never performs. If `k` is zero, **the optimised program dies where the original returned 0.**

A multiply cannot fail, so running it early costs at most a wasted instruction. A division can trap, so running it early can change a working program into a crashing one.

**That is the real rule, and it is not about loops at all:**

> An instruction may be hoisted past a condition that guards it only if executing it
> unnecessarily has no observable effect. LLVM calls this predicate
> `isSafeToSpeculativelyExecute`.

This is why `loops.py` has a `MOVABLE` set with `/` and `%` conspicuously absent. We arrived at that from the safety argument; LLVM arrived at it from the same place; **they are the same predicate**, and yours is now measured against theirs rather than asserted.

### Loop rotation: how to get the hoist without the bet

Add the rotation pass and run it again:

```
$ opt -passes='mem2reg,loop-simplify,loop-mssa(loop-rotate,licm)' -S d0.ll
```

```
  br i1 %4, label %.lr.ph, label %14
.lr.ph:                                   ; preds = %3
  %5 = sdiv i32 100, %2
  br label %6
```

**Now the division hoists.** Rotation rewrites the loop from *test-at-top* to *guard, then test-at-bottom*: an `if (i < n)` before the loop, a preheader `.lr.ph`, and a body whose test is at the end. The preheader is reached **only when the loop will run at least once** — so the hoisted division executes exactly when the original would have divided at least once. No speculation, no bet.

It also fixes condition 1 structurally. After rotation the body, the latch and the only exit are one block, which trivially dominates every exit.

**Rotation hoists nothing by itself.** Run it without LICM and `%5 = mul`, `%6 = add` are still sitting inside the loop. Rotation does not optimise; it makes optimisation *legal*. That distinction is L12's subject.

| | unrotated | rotated |
|---|---|---|
| `k * 2 + 1` | hoisted, **unguarded** | hoisted, guarded |
| `100 / k` | **stays in the loop** | hoisted, guarded |

*(One operator changed. Reproduce all four cells with the commands above; they are Lab 5 Q7–Q10.)*

---

## 8. Induction Variables

A **basic induction variable** is one updated by a constant step each pass: `i = i + 1`. Its value is an affine function of the iteration count, which is what makes several later optimisations possible.

**It is never one instruction.** Our TAC lowers `i = i + 1` to two:

```
    t11 = i + t10
    i = t11
```

because the right-hand side is generated before the assignment knows where it goes. So the detector has to look for *a binary op whose result is copied back into one of its own operands*. A version that matched `i = i + c` literally finds **no induction variable in any loop this compiler emits** — which is what the first draft of `basic_ivs` did, and it returned an empty dict on every input until it was measured against one.

```
$ python3 loops.py scale.cy scale
    basic induction variables: {'i': 1}
```

```cyan
while i < n { s = s + j;  i = i + 2;  j = j - 5; }
```

```
    basic induction variables: {'i': 2, 'j': -5}
```

**Strength reduction** is the payoff. A **derived** induction variable `j = i * 4` can be maintained incrementally — initialise `j = 4 * i₀` in the preheader, and replace the multiply with `j = j + 4` in the body. A multiply per iteration becomes an add. On the array indexing in `scale`, this is what turns `a[i]` into a pointer bump.

**Week 11 uses the same information for bounds-check elimination**: if `i` starts at 0, steps by 1, and the loop test is `i < n`, then `0 <= i < n` holds throughout and every bounds check in the body is provably redundant. **That is how a safe language gets to delete its safety checks without giving up safety** — the check is not skipped, it is *discharged*.

---

## 9. The Rest of the Loop Optimisations, Briefly

**Unrolling** copies the body $k$ times and steps the counter by $k$. Fewer test-and-branch pairs, more scheduling freedom, more instruction cache pressure. Needs a remainder loop when the trip count is not a multiple of $k$.

**Fusion** merges two loops over the same range into one: one traversal instead of two, so the data is touched once. **This is the CS 201 argument** — `L15 Locality as Leverage`, in compiler form.

**Fission** splits one loop into two. The exact opposite, and also sometimes right: it can cut register pressure, or separate a vectorisable part from an unvectorisable one.

> **That fusion and fission are both optimisations, and are inverses, tells you the important
> thing about this whole subject.** There is no ordering of transformations that is best for all
> programs. There is a *pipeline*, chosen by people, tuned on benchmarks, and defensible only
> against a particular idea of typical code. L12 §7.

---

## 10. Where This Lands

**Liveness is not one analysis you have now finished.** It is the input to register allocation, which is L12 and the reason this lecture had to come first. Your interference graph is only as correct as your def/use table — and section 1 is what an incorrect one produces.

**Summary of what was measured, and how to reproduce it:**

| Claim | Command |
|---|---|
| Week 4's DCE deletes a live `load` (8 → 6) | `python3 opt.py nested.cy g` |
| Liveness keeps all 8 | `python3 live.py nested.cy g` |
| One natural loop in `scale`, body `{L0, B2}` | `python3 loops.py scale.cy scale` |
| 6 invariant, 0 hoistable | same |
| `mul` hoists unrotated; `sdiv` does not | `opt -passes='mem2reg,loop-simplify,loop-mssa(licm)'` |
| `sdiv` hoists once rotated | add `loop-rotate` before `licm` |
| `{'i': 2, 'j': -5}` | `python3 loops.py` on the two-IV loop |

---

*CS 211 · Week 5 · Lecture 11 · © CSE Department*

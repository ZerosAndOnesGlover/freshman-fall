# CS 211 · Lab 4 · Solutions and Checkoff Notes
## Instructor Only

---

**Lab 4 is unmarked.** All figures measured with clang/opt 18.1.3 and Python 3.14.2.

> **Q15 is the checkoff that matters.** A student who cannot say why a silently-wrong optimiser is
> worse than a crashing one has missed the point of the back end.

---

## Part 1 — TAC and Basic Blocks

### Q1 — The loop became three instructions

```
L0:                      <- the label (jump target)
    ifz t1 goto L1       <- the exit test
    goto L0              <- the back edge
```

**The `goto L0` is what makes it a loop.** A label and a conditional exit alone describe a forward branch; the backward jump is the loop.

### Q2 — The four blocks

| Block | Preds | Succs |
|---|---|---|
| `fn_gcd` | — | `L0` |
| `L0` | `fn_gcd`, `B2` | `L1`, `B2` |
| `B2` | `L0` | `L0` |
| `L1` | `L0` | — |

**`L0` is the loop header** — it has a predecessor (`B2`) that is itself reachable from `L0`, i.e. it sits on a cycle, and it is the cycle's entry point.

### Q3 — The back edge

**An edge from `B2` to `L0` where `L0` dominates `B2`** is a *back edge*, and back edges are how loops are detected. Week 5 finds natural loops by locating back edges and taking the set of blocks that can reach the tail without passing through the header.

**Accept:** "the edge going backwards is what makes it a cycle rather than a chain."

### Q4 — `&&` is a branch

```
$ python3 tac.py sc.cy
fn_f:
    t0 = a
    ifz t0 goto L0
    t0 = b
L0:
    ret t0
```

*(Measured.)* **The instruction is `ifz t0 goto L0`** — if the left operand is false, skip the right entirely.

**What breaks otherwise:** every guard of the form `if p != null && p.x > 0` evaluates `p.x` even when `p` is null. **`&&` is not an operator that happens to short-circuit; short-circuiting is its definition** (`The Cyan Language Reference` §4).

### Q5 — `||`

**`iftrue t0 goto L0`** instead of `ifz`. The condition is inverted: `||` skips the right operand when the left is **true**.

---

## Part 2 — The Same Graph, in LLVM

### Q6 — The correspondence

| Ours | LLVM | Role |
|---|---|---|
| `fn_gcd` | `%2` (implicit entry) | entry |
| `L0` | `%6` | loop header, `preds = %9, %2` |
| `B2` | `%9` | body, `preds = %6` |
| `L1` | `%15` | exit, `preds = %6` |

**The predecessor sets agree exactly.**

### Q7 — Why `-O0` uses memory

**clang at `-O0` gives every local an `alloca` and accesses it through `load`/`store`.**

**Why:** `-O0` is meant to be fast to compile and faithful to debug. Every variable having a stable memory address means a debugger can read and *write* any local at any breakpoint, and the mapping from source variable to storage is trivial. **Promoting to registers is an optimisation, and `-O0` means "do not optimise".**

### Q8 — The table

| | instructions | alloca | load | store | phi |
|---|---:|---:|---:|---:|---:|
| `-O0` | **23** | 3 | 6 | 5 | 0 |
| after `mem2reg` | **11** | **0** | **0** | **0** | **2** |

*(Measured.)*

**Accept ±1 on the instruction counts** depending on whether the student counts the `br` in the entry block or blank lines.

### Q9 — The two φ-nodes

**One for `a`, one for `b`** — the two variables whose values differ between the first arrival at the loop header and subsequent ones. **`t` needs none**: it is assigned and consumed entirely within the body, so no value crosses a merge point.

### Q10 — Translating the φ

```llvm
%.01 = phi i32 [ %1, %2 ], [ %6, %5 ]
```

- `%1` — the parameter `b`
- `%2` — the entry block
- `%6` — the result of `srem` (`a % b`)
- `%5` — the loop body block

**English:** *"the value of `b` at the top of the loop is the original parameter if we came from the entry, or the result of `a % b` if we came round the loop."*

**The fact it states:** the **loop-carried dependency** for `b` — each iteration's `b` is the previous iteration's `a % b`.

---

## Part 3 — Constant Folding

### Q11

**13 instructions → 6.** Surviving that LLVM removes: **`a = 5`, `b = 20`, `unused = 99`.**

### Q12

**Liveness analysis** — Week 5. Our DCE removes only temporaries because it cannot prove a *named local* is never read again. Liveness proves exactly that.

### Q13 — Removing the unary case

**Nothing folds.** The output stays at 15 instructions:

```
    t0 = 7
    t1 = -t0
    t2 = 2
    t3 = t1 / t2
    ...
```

*(Measured.)*

**Why:** `The Cyan Language Reference` §2 gives `INT ::= [0-9]+` with **no sign**. So `-7` is two tokens and lowers to `unary(-, 7)`, not a constant. **A folder that handles only binary operators therefore folds nothing containing a negative number** — which in real code is a large fraction of expressions.

### Q14 — The sabotage

With `'/': lambda a, b: a // b`:

```
    q = -4          <- WRONG; correct is -3
    r = -1
    t10 = -401      <- WRONG; correct is -301
    ret t10
```

*(Measured. `gcc` confirms `q=-3 r=-1 combined=-301`.)*

**No error appears.** The compiler reports success, the fixed point is reached, and the program computes a different number.

**Worth pointing out at the bench:** only `q` changed — `r` is still `-1`, because the `%` lambda computes its own truncation and does not use the sabotaged `/`. **Partial corruption is more insidious than total**, since a test checking only `%` would pass.

### Q15 — Why this is the worst kind of bug

**Expected answer, and the checkoff standard:**

- **A crash is discovered by the person who caused it, immediately.** The compiler stops, names a file and a line, and nothing ships.
- **A wrong constant is discovered by a user, later, in a program that compiled cleanly and passed its tests.** By then the evidence is a wrong number with no connection to the compiler.
- **Every test that avoids negative division still passes**, so ordinary test coverage does not catch it. Coverage of the *compiler*'s code is 100% here — the folding path ran.

**How to catch it.** The technique is **differential testing**: compile the same program with and without the optimiser and check the outputs agree, over a large body of generated programs. **Random program generation plus differential testing is how real compiler bugs are found** — Csmith found hundreds in GCC and LLVM this way.

**Also accept:** metamorphic testing; running the optimiser's arithmetic against the language's own reference semantics; property-based testing over random integer pairs.

**A student who says "write more tests" has not answered.** Push for *what oracle* tells them the answer is wrong.

---

## Part 4 — Reading a Bigger CFG

### Q16 — `classify`

**8 basic blocks.** *(Measured.)*

**Three blocks have two successors:** `fn_classify` (the first `if`), `L1` (the second `if`), and `L4` (the `while` test).

### Q17 — Blocks with no successors

**`B1`, `B3`, and the final block** — every one ends in `ret`. **A `ret` transfers control out of the function**, so it has no successor within the CFG.

### Q18 — Against LLVM

Block counts will differ slightly. **The difference is bookkeeping, not control flow:** our IR emits a `fn_classify` label block containing only the label, and a separate `L3` block that is empty (the `if`'s join point with nothing after it). LLVM merges such blocks or never creates them.

**Accept any answer that identifies empty/label-only blocks as the difference** and confirms the *edges* correspond.

---

## Checkoff Summary

| Part | Minimum to pass |
|---|---|
| **1** | The four blocks with preds/succs; `ifz` quoted for `&&` |
| **2** | The table filled in (23 → 11, 2 φ); Q10 translated into English |
| **3** | Q13 run **and reverted**; **Q14 run and reverted**; Q15 naming an oracle |
| **4** | 8 blocks; the three two-successor blocks identified |

**Two reverts to verify before they leave:** the `unary` case in `const_fold` (Q13) and the `/` lambda (Q14). **A student leaving with the Q14 sabotage in place will do PS 4 against a compiler that silently computes wrong answers**, which is a memorable lesson but not the intended one.

---

*CS 211 · Lab 4 Solutions · Instructor Only*

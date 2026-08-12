# CS 211 · Problem Set 4
## TAC Generation and Constant Folding

---

**Released:** Week 4, Wednesday · **Due:** Week 5, Friday 17:00
**Total: 100 points** · Submit one PDF (`PS4_{LastName}_{StudentID}.pdf`) **and** `tac.py`, `opt.py`

> **Fourth vertebra**, and the first back-end one. It consumes the typed AST from PS 3 and emits
> three-address code. **Week 5's optimiser and Week 11's LLVM backend both read this IR**, so the
> instruction format you choose here is one you will live with.

---

### Q1: Lowering by Hand (18 points)

**(a) [6]** Translate to TAC, by hand:

```cyan
fn f(a: int, b: int) -> int {
    if a > b { return a - b; }
    return b - a;
}
```

Use the instruction forms from L09 §2. Number your instructions.

**(b) [6]** Draw the CFG for your answer. Give each block's predecessors and successors, and identify any block with two successors.

**(c) [6]** Now lower `return a && b;`.

**It must not be one instruction.** Show the branch, and state precisely which Cyan rule forces it — quote `The Cyan Language Reference`.

---

### Q2: Basic Blocks (14 points)

**(a) [6]** State the three rules for identifying **leaders** (Dragon §8.4).

**(b) [8]** Apply them to this instruction sequence, and give the resulting blocks:

```
 1    t0 = 0
 2    t1 = n < t0
 3    ifz t1 goto L2
 4    t2 = 0
 5    ret t2
 6  L2:
 7    t3 = n + t0
 8    goto L3
 9    t4 = 99
10  L3:
11    ret t3
```

**One instruction is unreachable.** Identify it, and say whether the leader rules alone are enough to notice.

---

### Q3: SSA and φ (18 points)

**(a) [5]** Convert to SSA by hand:

```
    a = 1
    if c goto L1
    a = 2
L1: b = a + 1
```

Where does the φ go, and how many operands does it take?

**(b) [5]** Explain what the word **static** is doing in "Static Single Assignment". A φ-node inside a loop may execute a million times — why is that not a violation?

**(c) [8]** `mem2reg` on `gcd` produces:

```llvm
%.01 = phi i32 [ %1, %2 ], [ %6, %5 ]
%.0  = phi i32 [ %0, %2 ], [ %.01, %5 ]
```

**Explain the second one.** Say what each of `%0`, `%2`, `%.01` and `%5` is, and why the second operand is `%.01` rather than `%6`. **This is the loop-carried dependency; state it in one sentence of English.**

---

### Q4: The IR Generator and Folder (42 points)

**Write `tac.py` and `opt.py`.**

#### `tac.py` requirements

1. **Three-address instructions** — a destination and at most two sources.
2. **All statements**: `let`, assignment (including `a[i] =` and `p.f =`), `if`/`else`, `while`, `return`, expression statements.
3. **All expressions**, including calls, indexing, field access, array literals and `new`.
4. **`&&` and `||` lower to branches.** Both must skip their right operand.
5. **`build_cfg`** returning basic blocks with `preds` and `succs` populated.
6. **A `--dump-tac` mode**, per `The Cyan Language Reference` §7.

#### `opt.py` requirements

7. **Constant folding**, including **unary minus** — Cyan has no negative literals, so `-7` is `unary(-, 7)` and a folder that skips it folds nothing containing a negative number.
8. **Cyan's arithmetic semantics, not Python's.** `-7 / 2` is `-3` and `-7 % 2` is `-1`.
9. **Copy propagation** and **dead-code elimination** over temporaries.
10. **Iteration to a fixed point**, with a log of which pass changed what.

#### Verification

| Input | Requirement |
|---|---|
| `gcd.cy` | 4 basic blocks; `L0` with two predecessors |
| `fold.cy` | folds to `ret 19`; 13 instructions down to 6 or fewer |
| `neg.cy` | folds to `-301` — **check against `gcc`** |
| `a && b` | a branch appears |
| `classify` (Lab 4 Part 4) | 8 basic blocks |

#### Marks

| | |
|---|---:|
| TAC for all statements and expressions | 12 |
| `&&` / `||` lowered as branches | 5 |
| `build_cfg` with correct preds and succs | 8 |
| Constant folding incl. unary, with Cyan's `/` and `%` | 9 |
| Copy propagation and DCE | 5 |
| Fixed-point iteration with a log | 3 |

---

### Q5: The Bug That Does Not Crash (8 points)

In Lab 4 Q14 you changed the folder's `/` to Python's floor division and it produced `-401` where the correct answer is `-301` — **with no error of any kind.**

**(a) [4]** Explain why an optimiser that produces a *different answer* is a worse failure than one that crashes. Refer to who discovers it and when.

**(b) [4]** **Propose a test that would have caught it.** Be concrete — say what you would run, against what oracle, and on which inputs. *(A good answer here is a real technique; the term for it is worth knowing.)*

---

## Marks

| Question | Topic | Points |
|---|---|---|
| Q1 | Lowering by hand | 18 |
| Q2 | Basic blocks | 14 |
| Q3 | SSA and φ | 18 |
| Q4 | The IR generator and folder | 42 |
| Q5 | The bug that does not crash | 8 |
| **Total** | | **100** |

---

*Quiz 5, at the start of Tuesday's lecture in Week 5, covers this week — TAC, basic blocks, the CFG, SSA, φ-functions, and dataflow analysis.*

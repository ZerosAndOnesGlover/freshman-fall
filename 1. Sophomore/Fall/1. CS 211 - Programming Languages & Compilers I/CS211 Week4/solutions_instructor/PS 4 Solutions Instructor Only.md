# CS 211 · Problem Set 4 · Solutions
## Instructor Only

---

> All IR output measured with the reference `tac.py` / `opt.py`; LLVM figures with clang/opt 18.1.3.

---

## Q1: Lowering by Hand (18)

### (a) [6]

```
 1  fn_f:
 2      t0 = a > b
 3      ifz t0 goto L0
 4      t1 = a - b
 5      ret t1
 6  L0:
 7      t2 = b - a
 8      ret t2
```

**Accept any equivalent** with a different label or temporary naming, and accept an extra `goto` after line 5 (unreachable but harmless).

**Mark scheme:** 4 for correct lowering, 2 for the conditional being inverted correctly (`ifz` jumping to the *else* path). **−2** for a version that falls through into the else branch.

### (b) [6]

| Block | Preds | Succs |
|---|---|---|
| `fn_f` | — | `L0`, *(fallthrough)* |
| *(fallthrough)* | `fn_f` | — |
| `L0` | `fn_f` | — |

**`fn_f` has two successors.** Both other blocks end in `ret` and have none.

**Mark scheme:** 4 for the blocks, 2 for identifying the two-successor block.

### (c) [6]

```
    t0 = a
    ifz t0 goto L0
    t0 = b
L0:
    ret t0
```

**The rule:** `The Cyan Language Reference` §4 — *"`&&` and `||` short-circuit"*, under Evaluation order. **Short-circuiting is part of the operator's definition**, not an optimisation.

**Mark scheme:** 4 for a correct branch-based lowering, 2 for quoting the reference. **A one-instruction `t = a && b` earns 0** — it is the failure the question exists to catch.

---

## Q2: Basic Blocks (14)

### (a) [6] The leader rules

An instruction is a leader if:

1. it is **the first instruction**;
2. it is **the target of a jump** (in our IR, a label);
3. it **immediately follows a jump**.

**2 each.**

### (b) [8]

**Leaders: 1, 4, 6, 9, 10.**

| Block | Instructions |
|---|---|
| B1 | 1–3 |
| B2 | 4–5 |
| B3 (`L2`) | 6–8 |
| B4 | 9 |
| B5 (`L3`) | 10–11 |

**Instruction 9 (`t4 = 99`) is unreachable** — it follows an unconditional `goto` and no jump targets it.

**Are the leader rules enough to notice?** **No.** Rule 3 makes 9 a leader and gives it its own block; that is all. **Detecting unreachability requires a graph reachability pass** from the entry block — the leader rules are local and cannot see that nothing points at B4.

**Mark scheme:** 4 for the blocks, 2 for identifying instruction 9, **2 for correctly saying the rules alone are not enough**. A student who says "yes, rule 3 catches it" earns 0 of that 2 — rule 3 *isolates* it without *identifying* it.

---

## Q3: SSA and φ (18)

### (a) [5]

```
    a1 = 1
    if c goto L1
    a2 = 2
L1: a3 = phi(a1, a2)
    b1 = a3 + 1
```

**The φ goes at the top of `L1`**, the join point, and takes **two operands** — one per incoming edge.

**Mark scheme:** 3 renaming, 2 for φ placement and operand count.

### (b) [5]

**"Static" refers to the program text.** Each assignment appears **once in the source of the IR**; SSA constrains the *written* form, not the *dynamic* execution.

**A φ inside a loop executes once per iteration** and that is not a violation, because it is still a single instruction in the text.

**Mark scheme:** 3 for the text/execution distinction, 2 for applying it to the loop case.

### (c) [8]

```llvm
%.0 = phi i32 [ %0, %2 ], [ %.01, %5 ]
```

- **`%0`** — the parameter `a`
- **`%2`** — the entry block
- **`%.01`** — the *other* φ, i.e. the value of `b` at the top of this iteration
- **`%5`** — the loop body block

**Why `%.01` and not `%6`:** the source is `a = t` where `t` was set to `b` at the *start* of the body. **So `a`'s next value is the current iteration's `b`, not the newly computed `a % b`.** `%6` is `srem` — that becomes the next `b`, which is what the *first* φ uses.

**The loop-carried dependency in English:** *"each iteration's `a` is the previous iteration's `b`."*

**Mark scheme:** 4 for the four operands, 2 for the `%.01` vs `%6` explanation, 2 for the English sentence.

**This is the hardest part of the set.** The `%.01` distinction requires tracing `t` through the source. **Award 5–6 for a student who identifies the operands correctly but muddles which φ feeds which.**

---

## Q4: The IR Generator and Folder (42)

`lab/tac.py` and `lab/opt.py` are the model answers, shipped as Lab 4 starters.

### Verification targets

| Input | Expected |
|---|---|
| `gcd.cy` | 4 blocks; `L0` preds = `fn_gcd`, `B2` |
| `fold.cy` | 13 → 6 instructions; `t7 = 19` |
| `neg.cy` | folds to `-301` |
| `a && b` | `ifz` appears |
| `classify` | 8 blocks |

*(All measured.)*

### Mark breakdown

| | | Notes |
|---|---:|---|
| TAC for all statements and expressions | 12 | Test `new`, array literals, field assignment |
| `&&` / `||` as branches | 5 | **Both**; `\|\|` needs the inverted test |
| `build_cfg` with preds and succs | 8 | `preds` populated is the half students skip |
| Folding incl. unary, with Cyan's `/` and `%` | 9 | **Check `-7 / 2` gives `-3`** |
| Copy propagation and DCE | 5 | |
| Fixed point with a log | 3 | |

**Five failure modes, in order of frequency:**

1. **`&&` lowered as a binary op.** Costs the 5 marks and is worth a written comment — it is a correctness bug, not a missing feature.
2. **Python's `//` in the folder.** Costs 4 of the 9. **Test with a negative dividend**; a folder tested only on positives looks perfect.
3. **Unary minus not folded.** Costs 3 of the 9. Symptom: `neg.cy` folds nothing.
4. **`preds` left empty.** Costs 4 of the 8. Everything downstream in Week 5 needs it.
5. **Folding across a label.** A student who does not clear the known-constants map at a label will fold a value from one branch into another. **This produces wrong code and costs 5** — check by folding a program with an `if` where the two branches assign different constants to the same variable.

**On failure mode 5**, the reference clears at every label:

```python
if ins.op == 'label':
    known.clear()          # a label may be a join point
```

**That is conservative** — it also clears at labels with a single predecessor, losing real opportunities. **A student who notices and does better using the CFG deserves a comment**; it is genuinely Week 5's material arriving early.

---

## Q5: The Bug That Does Not Crash (8)

### (a) [4]

**Expected points:**

- **A crash is found by the author, immediately**, with a file and line. Nothing ships.
- **A wrong constant is found by a user, later**, in a program that compiled cleanly and passed its tests. The symptom is a wrong number with no visible connection to the compiler.
- **Ordinary test coverage does not help** — the folding path executed successfully. Coverage of the compiler is complete; the *oracle* is what is missing.

**Mark scheme:** 2 for who-and-when, 2 for the observation about coverage versus oracle.

### (b) [4]

**The technique is differential testing.** Compile a large body of programs both with and without the optimiser and check the outputs agree.

**Full marks require naming an oracle** — the unoptimised build, another compiler, or a reference semantics. **Combining it with random program generation** (Csmith is the canonical tool, which found hundreds of real bugs in GCC and LLVM) earns full marks comfortably.

**Also accept:** metamorphic testing; property-based testing of the folder's arithmetic against the language's specified semantics.

**Mark scheme:** 2 for a testing strategy, 2 for identifying the oracle. **"Write more unit tests" earns 1** — the question asks what tells you the answer is wrong.

---

## Mark Distribution

| Question | Points | Common failure |
|---|---:|---|
| Q1 | 18 | `&&` lowered as one instruction |
| Q2 | 14 | Claiming the leader rules detect unreachability |
| Q3 | 18 | **The `%.01` vs `%6` distinction in (c)** |
| Q4 | 42 | Python's `//`; empty `preds`; folding across labels |
| Q5 | 8 | No oracle named |
| **Total** | **100** | |

**Q4 failure mode 2 is worth raising in class regardless of the marks.** A folder that is wrong only on negative dividends is the exact shape of the Lab 4 Q14 sabotage — and several students will have written it *accidentally* while having answered Q15 correctly about how dangerous it is.

---

*CS 211 · PS 4 Solutions · Instructor Only*

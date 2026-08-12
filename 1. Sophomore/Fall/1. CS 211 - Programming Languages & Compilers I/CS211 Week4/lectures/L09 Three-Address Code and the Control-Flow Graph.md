# CS 211 · Programming Languages & Compilers I
## Week 4 · Lecture 1 of 2
### Three-Address Code and the Control-Flow Graph

---

**Reading:** Dragon §6.1–6.4, §8.4 · **Next:** L10, SSA and dataflow analysis

---

## 1. The Front End Is Finished

Three weeks got you from characters to a typed tree. **The tree is the last representation that resembles what the programmer wrote**, and this week it stops being useful.

**Why leave the AST?** Because it is the wrong shape for the questions the back end asks.

| Question | On an AST | On an IR |
|---|---|---|
| *Is this expression computed twice?* | compare subtrees structurally | compare two instructions |
| *Is this variable still needed?* | walk the whole tree | scan forward from here |
| *Which code can reach this point?* | control flow is implicit in nesting | it is an edge in a graph |

**The AST hides control flow inside nested structure.** An `if` inside a `while` inside a function is three levels of nesting, and "which statements can run before this one" requires understanding all three. **An IR makes control flow explicit** — as a graph you can walk.

---

## 2. Three-Address Code

**Every instruction has at most three operands: a destination and two sources.**

```
t2 = t0 + t1
```

That is the whole format. Nested expressions are flattened by inventing temporaries:

```cyan
return b - 1;
```

```
    t6 = 1
    t7 = b - t6
    ret t7
```

**Cyan's `gcd`, compiled:**

```
$ python3 tac.py gcd.cy
```

```
fn_gcd:
L0:
    t0 = 0
    t1 = b != t0
    ifz t1 goto L1
    t = b
    t2 = a % b
    b = t2
    a = t
    goto L0
L1:
    ret a
```

*(Measured.)*

**Read what happened to the `while`.** There is no loop construct. There is a label, a conditional jump out, a body, and an unconditional jump back. **Structured control flow has become labels and gotos** — which is what the machine has, and the reason the IR looks like this.

### Short-circuit operators need care

`&&` must not evaluate its right operand when the left is false. **That is a control-flow fact hiding inside an expression**, and it forces a branch:

```python
def gen_shortcircuit(self, e):
    t = self.temp(); lend = self.label()
    l = self.gen_expr(e.lhs)
    self.emit('copy', dst=t, a=l)
    if e.op == '&&':
        self.emit('ifz', a=t, label=lend)     # false: skip the right operand
    else:
        self.emit('iftrue', a=t, label=lend)  # true: skip it
    r = self.gen_expr(e.rhs)
    self.emit('copy', dst=t, a=r)
    self.emit('label', label=lend)
    return t
```

**A student who lowers `&&` as an ordinary binary operator produces a compiler that evaluates both sides always** — and every `if p != null && p.x > 0` in the language becomes a crash. **This is the most common IR-generation bug**, and it type-checks perfectly.

---

## 3. Basic Blocks

**A basic block is a maximal run of instructions with one entry and one exit** — control enters at the top and leaves at the bottom, with no branches in between.

The Dragon Book's rule for finding them (§8.4) is three lines. **An instruction is a *leader* if:**

1. it is the first instruction, or
2. it is the target of a jump (in our IR: it is a label), or
3. it immediately follows a jump.

**Each leader begins a block that runs to just before the next leader.**

```
$ python3 tac.py gcd.cy
```

```
; ---- CFG: 4 basic blocks ----
fn_gcd  (preds: -)  ->  L0
L0  (preds: fn_gcd, B2)  ->  L1, B2
      t0 = 0
      t1 = b != t0
      ifz t1 goto L1
B2  (preds: L0)  ->  L0
      t = b
      t2 = a % b
      b = t2
      a = t
      goto L0
L1  (preds: L0)  ->  -
      ret a
```

*(Measured.)*

**The loop is now visible as a cycle in the graph.** `L0` has two predecessors — the function entry and `B2` — and two successors. **`L0` is the loop header**, and the fact that it has a predecessor *inside* the loop is what makes it one. Week 5 finds loops by looking for exactly this.

---

## 4. What a Real Compiler Produces for the Same Function

```c
int gcd(int a, int b) {
    while (b != 0) { int t = b; b = a % b; a = t; }
    return a;
}
```

```
$ clang -S -emit-llvm -O0 -o - gcd.c
```

```llvm
define dso_local i32 @gcd(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %0, ptr %3, align 4
  store i32 %1, ptr %4, align 4
  br label %6

6:                                    ; preds = %9, %2
  %7 = load i32, ptr %4, align 4
  %8 = icmp ne i32 %7, 0
  br i1 %8, label %9, label %15

9:                                    ; preds = %6
  %10 = load i32, ptr %4, align 4
  store i32 %10, ptr %5, align 4
  %11 = load i32, ptr %3, align 4
  %12 = load i32, ptr %4, align 4
  %13 = srem i32 %11, %12
  store i32 %13, ptr %4, align 4
  %14 = load i32, ptr %5, align 4
  store i32 %14, ptr %3, align 4
  br label %6

15:                                   ; preds = %6
  %16 = load i32, ptr %3, align 4
  ret i32 %16
}
```

*(Measured, clang 18.1.3.)*

**Compare it block for block against ours.**

| Ours | LLVM | |
|---|---|---|
| `L0` | `6` | loop header — **`preds = %9, %2`**, the same two predecessors |
| `B2` | `9` | body, branching back to the header |
| `L1` | `15` | exit |

**Identical shape.** LLVM prints predecessors in a comment for exactly the reason we print them: **the graph is the object of interest, and the instruction order is incidental.**

**One real difference: LLVM at `-O0` puts every variable in memory.** Three `alloca`s, six `load`s, five `store`s. Ours keeps them in named slots. **That difference is the entire subject of §5 of L10** — and it is where `phi` comes from.

---

## 5. Constant Folding, and Why It Is Not Cheating

```cyan
fn f() -> int {
    let a = 2 + 3;
    let b = a * 4;
    let unused = 99;
    return b - 1;
}
```

```
$ python3 opt.py fold.cy
```

```
; ---- before: 13 instructions ----      ; ---- after: 5 instructions ----
    t0 = 2                                   a = 5
    t1 = 3                                   b = 20
    t2 = t0 + t1                             unused = 99
    a = t2                                   t7 = 19
    t3 = 4                                   ret t7
    t4 = a * t3
    b = t4
    t5 = 99
    unused = t5
    t6 = 1
    t7 = b - t6
    ret t7
```

*(Measured.)* **Thirteen instructions to five**, and the answer is computed at compile time.

**clang agrees, and goes further:**

```
$ clang -S -emit-llvm -O1 -o - fold.c
define dso_local noundef i32 @f() local_unnamed_addr #0 {
  ret i32 19
}
```

**One instruction.** *(Measured.)* LLVM also removed `a`, `b` and `unused`, which our folder kept — because our dead-code pass only removes *temporaries*, and cannot yet prove a named local is dead. **That is Week 5's liveness analysis**, and the limitation is deliberate: you should feel the gap before the tool that closes it arrives.

> **This is CS 201 Week 0's folded loop, from the other side.** There you watched GCC delete a
> hundred-million-iteration loop and print the answer as a constant, and were told to read the
> disassembly rather than the source. **This week you are writing the code that does it.**

### The trap: your folder must match your language

Cyan has **no negative integer literals** — L03 §3. `-7` is unary minus applied to `7`. So:

```
    t0 = 7
    t1 = -t0        <- a 'unary' instruction, not a constant
    t3 = t1 / t2
```

**A folder that only handles binary operators folds none of this**, and every expression containing a negative number escapes optimisation entirely. Adding the unary case gives:

```
    q = -3
    r = -1
    t10 = -301
    ret t10
```

*(Measured — and C agrees: `q=-3 r=-1 combined=-301`.)*

**Note that the folder must implement Cyan's division, not Python's.** `-7 / 2` is `-3` in Cyan and `-4` in Python. **A folder written with Python's `//` silently changes the meaning of every program it optimises** — an optimisation that produces different answers is not an optimisation, and this is the single most dangerous class of compiler bug.

---

## 6. Fixed-Point Iteration, For the Third Time

```python
def optimise(code, rounds=10):
    for i in range(rounds):
        any_change = False
        for name, fn in (('fold', const_fold), ('copy', copy_prop),
                         ('dce', dead_code)):
            code, ch = fn(code)
            if ch: any_change = True
        if not any_change:
            break
```

**Keep applying transformations until nothing changes.** You have now seen this shape three times:

| Week | Where |
|---|---|
| **1** | $\varepsilon$-closure — keep adding reachable states |
| **2** | FIRST and FOLLOW — keep adding terminals |
| **4** | The optimiser — keep transforming |
| **5** | Every dataflow analysis |

**It is one of about five ideas this entire course runs on.** The reason it terminates here is that each pass strictly reduces something — instruction count, or the number of unfolded constants — and none can decrease forever.

**Passes must run repeatedly because they feed each other.** Folding creates dead code; eliminating dead code exposes more constants. **Running each once, in any order, leaves work on the table** — which is why real compilers run pass pipelines dozens of times.

---

## 7. What to Take Away

1. **The AST is the wrong shape for the back end**, because it hides control flow inside nesting.
2. **Three-address code has one destination and two sources**, and flattens expressions with temporaries.
3. **Structured control flow becomes labels and jumps** — there is no `while` in the IR.
4. **`&&` and `||` must compile to branches.** Lowering them as ordinary operators is the most common IR bug and it type-checks.
5. **Leaders define basic blocks**: first instruction, jump targets, and instructions after jumps.
6. **The CFG makes loops visible** as cycles, which is how Week 5 will find them.
7. **Our CFG and LLVM's are the same graph** for the same function — the difference at `-O0` is that LLVM keeps variables in memory.
8. **A constant folder must implement your language's semantics**, not its host language's. `-7 / 2` is `-3` in Cyan.
9. **Fixed-point iteration, again**, and passes must repeat because each enables the others.

---

## Exercises

1. Compile `fn f(a: int) -> int { if a > 0 { return 1; } return 2; }` to TAC by hand, then check with `tac.py`.
2. `gen_shortcircuit` emits a branch for `&&`. **Write the TAC for `a && b || c`** and confirm the operand evaluation order matches Cyan's left-to-right rule.
3. Our `gcd` CFG has four blocks; LLVM's has four. **Ours has a separate `fn_gcd` entry block containing only a label. Why does LLVM not?**
4. §5's folder keeps `unused = 99` and LLVM removes it. **What exactly would our dead-code pass need to know** to remove it safely?
5. Give a Cyan program where folding `/` at compile time would be **wrong**. *(Hint: `The Cyan Language Reference` §5.)*
6. The `%` folder is written `a - int(a / b) * b`. **Show it gives `-1` for `-7 % 2`**, and say what `a % b` would give if written with Python's `%` instead.
7. §6 claims each pass "strictly reduces something". **Is that true of copy propagation?** If not, why does the loop still terminate?

---

*Next: L10 — Static Single Assignment. Every variable assigned exactly once, φ-functions where control flow merges, and why LLVM's entire optimiser is built on it.*

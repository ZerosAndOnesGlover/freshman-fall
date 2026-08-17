# CS 211 · Programming Languages & Compilers I
## Week 5 · Lecture 2 of 2
### Register Allocation, Instruction Selection, and the Pipeline

---

**Reading:** Dragon §8.8, §8.9, §9.7 · Appel ch. 11 · **Next:** Week 6, runtime systems and garbage collection

---

## 1. Your Compiler Has Infinitely Many Registers

`tac.py` has emitted `t0, t1, t2, ...` since Week 4 and has never once reused a name. `scale` uses eighteen. A function of any size uses hundreds.

**x86-64 has sixteen general-purpose registers, and you may touch about thirteen** — the rest are spoken for by the stack pointer, the frame pointer, and the ABI. Everything else lives in memory, and memory is roughly two orders of magnitude further away.

So the last question of the middle end is: **which values get registers?**

---

## 2. The Reduction

Two variables can share a register exactly when they are never live at the same time. Draw that as a graph — **nodes are variables, an edge means "never share a register"** — and the question becomes:

> **Can this graph be coloured with $k$ colours, so that no edge joins two nodes of the same colour?**

That is graph colouring. It is one of Karp's original 21 NP-complete problems (1972), which sounds like the end of the story and is not, because **a compiler does not need optimal. It needs good, fast, and always correct.**

This is the single most cited example of a real compiler problem turning out to be a classical graph problem, and it is worth pausing on: nothing about registers is in the statement. Solve colouring and you have solved allocation.

### Building the graph

Interference is defined by liveness, so L11 is the input:

```python
for ins, live_after in zip(b.instrs, pts):
    for d in defs(ins):
        others = set(live_after)
        if ins.op == 'copy':
            others -= uses(ins)          # the move exception
        for v in others - {d}:
            graph[d].add(v); graph[v].add(d)
```

**When an instruction defines `d`, `d` interferes with everything still live afterwards** — those values must survive past the write, so they cannot be in the register being written.

**The move exception earns its keep.** For `x = y`, the two hold the *same value* at that point, so they may share a register even though both are live. Adding the edge anyway is not *incorrect* — it just wastes a register. Omitting it is what makes **coalescing** possible later.

**It only bites when the source of the copy is still live afterwards**, and on `scale` it never is: our TAC emits `s = t9` where `t9` dies at that instruction, so removing the exception entirely leaves the graph at 69 edges and the register count at 7 — *no change at all*. On `coalesce.cy`, where `let x = y;` is followed by a use of both, the exception is the difference between 1 edge and 2, and between `x` and `y` sharing a register and not. **Measure it on the function in front of you before claiming a pass did anything** — Lab 5 Q14.

> **This is why L11 §3 mattered.** A def/use table that misses a use produces a graph missing an
> edge, and a missing edge means two live values assigned the same register. That is not a slow
> program; it is a wrong one, and it will fail on one input in a thousand. **Register allocation
> is where an error in your def/use model stops being theoretical.**

```
$ python3 regalloc.py scale.cy scale 4
```

```
; ---- interference graph for scale: 18 nodes, 69 edges ----
  a      deg 15  cost   10  | f i s t0 t1 t10 t11 t2 t3 t4 t5 t6 t7 t8 t9
  f      deg  6  cost   20  | a i k n s t7
  i      deg 14  cost   41  | a f k n s t10 t2 t3 t4 t5 t6 t7 t8 t9
  ...
  t0     deg  3  cost    2  | a k n
```

**Read the degrees.** `a`, `k`, `n`, `s`, `i` have degree 14–15; the temporaries have degree 3–6. The parameters and the loop counter are live across the whole loop, so *every* temporary inside the body interferes with them. **Register pressure is created by long-lived values, not by the number of expressions** — which is why a function with fifty short-lived temps allocates fine and one with eight simultaneously-live locals does not.

---

## 3. Chaitin's Algorithm

Three phases, and the first is the insight.

**SIMPLIFY.** A node with fewer than $k$ neighbours **can always be coloured**, no matter what happens to the rest of the graph — its neighbours cannot use up all $k$ colours between them. So remove it and push it on a stack. Removing it drops its neighbours' degrees, which may make *them* trivially colourable.

**SPILL.** If every remaining node has degree $\ge k$, none is trivially safe. Choose one to keep in memory instead, remove it, and carry on. Which one you choose is the whole art — §4.

**SELECT.** Pop the stack. Give each node a colour none of its already-coloured neighbours is using. By construction one is free.

**Why simplify works is worth stating carefully.** Degrees only fall as nodes come out, so a graph where every node initially looks too constrained often colours fine once a few nodes are removed. Max degree is an upper bound on colours needed, and it is usually a terrible one.

```
;  simplify t0 (degree 3 < 4)
;  SPILL    t1 (degree 4, cost 2, ratio 0.50)
;  SPILL    a (degree 13, cost 10, ratio 0.77)
;  simplify t11 (degree 3 < 4)
;  ...
;  select   t7 -> r0
;  select   s -> r1
;  select   i -> r2
;  select   t4 -> r3
```

---

## 4. Choosing What to Spill

Every spilled variable costs a load before each use and a store after each def. **A spill inside a loop costs that once per iteration.**

We do not know trip counts, so compilers use the classical stand-in:

$$\text{cost}(v) = \sum_{\text{references}} 10^{\,\text{loop depth}}$$

Ten is arbitrary and universal. What matters is that it is *much* larger than one, so an inner-loop variable is never spilled to rescue an outer one. Then spill the node minimising $\text{cost}/\text{degree}$ — cheap to spill, and frees many edges.

**Notice what just happened: L11's loop finder decides L12's register assignment.** That is not an accident of our design, it is how every real allocator works, and it is the first place in this course where two analyses compose into a decision neither could make alone.

In the trace above, `t0` costs 2 (referenced twice, outside the loop) and `i` costs 41 (referenced repeatedly, inside). The allocator will spill `t0` a dozen times before it touches `i`.

---

## 5. How Many Registers Does This Function Need?

`regalloc.py` re-runs the allocator for every $k$:

```
;  k= 3  spilled  6
;  k= 4  spilled  4
;  k= 5  spilled  2
;  k= 6  spilled  1
;  k= 7  spilled  0
```

**Seven.** Now check that against something the allocator does not know about — the maximum number of values simultaneously live anywhere in the function:

```
max simultaneous live (incl. def): 7
at B2 :: t5 = 1
   ['a', 'i', 'k', 'n', 's', 't4', 't5']
```

**Seven, at instruction `t5 = 1`.** Those seven values all need to exist at that moment, so no allocator of any kind can use six registers without spilling. It is an information-theoretic floor.

**Chaitin hits it exactly.** A polynomial-time heuristic for an NP-complete problem, on this function, is *optimal* — not close to optimal, optimal.

> That will not always happen, and you should not learn the wrong lesson. What it does show is why
> a heuristic is the right engineering answer here. **The gap between "optimal" and "what Chaitin
> gives you" is usually small, and the gap between "compiles in 3 ms" and "compiles in 3 hours" is
> not.**

Briggs (1989) improved the spill phase by pushing nodes *optimistically* — a node with degree $\ge k$ may still find a free colour if its neighbours happen to share colours — and only spilling in SELECT if no colour is actually free. `colour()` in `regalloc.py` does Chaitin's version and marks the place where Briggs differs. **PS 5 Part D asks you to implement Briggs and measure the difference.**

---

## 6. Instruction Selection: Maximal Munch, Again

Register allocation assigns storage. **Instruction selection** decides which machine instructions compute the values — and a real ISA offers many ways to say the same thing.

```
t1 = k * 2
t2 = t1 + 1
```

Two TAC instructions. On x86-64, one machine instruction:

```asm
leal    1(,%rdx,2), %ecx        # ecx = rdx*2 + 1
```

`lea` computes `base + index*scale + displacement` and does not touch flags. **A naive one-TAC-instruction-to-one-machine-instruction translation would emit three instructions and be measurably worse.**

The standard formulation is **tree tiling**: express each machine instruction as a tree pattern with a cost, then cover the IR tree with tiles at minimum total cost. Dynamic programming solves it optimally per tree in linear time.

**And the greedy version is maximal munch — the same rule as your Week 1 lexer.** There, the longest token wins. Here, the largest tile wins. It is the same algorithm on a different input, and if you found it obvious in Week 1 you should find it obvious now.

> **Week 1 §4 warned you that maximal munch is a heuristic, not a theorem** — it is why `12abc` had
> to be a lexical error rather than two tokens. The same caveat applies here: greedy tiling is not
> guaranteed optimal, and that is the trade every production compiler makes.

---

## 7. Peephole Optimisation

The last pass, and the least sophisticated: **slide a small window over the final instruction stream and rewrite what you recognise.**

| Pattern | Becomes | Why |
|---|---|---|
| `mov %eax, %ebx` ; `mov %ebx, %eax` | `mov %eax, %ebx` | second is redundant |
| `add $0, %eax` | *(delete)* | identity |
| `imul $2, %eax` | `add %eax, %eax` | cheaper on most pipelines |
| `jmp L` ; `L:` | `L:` | jump to the next instruction |
| `mov $0, %eax` | `xor %eax, %eax` | shorter encoding, breaks dependency |

**Why does a serious compiler need this at all?** Because earlier passes are written independently, and independently reasonable decisions compose into locally silly code. **Peephole is where the seams between passes get sanded off**, and every optimiser has one no matter how principled the rest of it is.

`xorl %eax, %eax` appears twice in the `-O1` output of `scale`. That is peephole choosing the two-byte encoding over the five-byte `movl $0, %eax`.

---

## 8. The Pipeline, and Why It Is a *List*

L11 §7 measured something that should now look like the central fact of this lecture:

- **LICM alone**, on the division loop: the `sdiv` stays in the loop.
- **loop-rotate then LICM**: the `sdiv` hoists.
- **loop-rotate alone**: nothing is hoisted at all.

**Neither pass does the job. The order does.** Rotation performs no optimisation; it changes the shape of the CFG so that LICM's safety condition can be satisfied. Run them the other way round and you get nothing.

This is the **phase-ordering problem**, and it is unsolved in the strong sense:

- Constant folding creates opportunities for dead-code elimination.
- Dead-code elimination creates opportunities for constant folding.
- Inlining creates opportunities for everything, including more inlining.
- Register allocation can undo the scheduler's work; scheduling can undo the allocator's.

**There is no ordering that is best for all programs**, and no way to find the best ordering for a given program short of trying them. So production compilers ship a *fixed, hand-tuned list*, chosen by benchmarking against code somebody decided was representative. LLVM's is in `PassBuilderPipelines.cpp`, it runs to hundreds of lines, and it runs several passes more than once.

**That fusion and fission are inverses and both optimisations (L11 §9) is the same observation from the other end.** The pipeline encodes a *belief about typical code*, not a theorem.

---

## 9. What `-O2` Actually Costs and Buys

`scale.c`, one function, five optimisation levels. Instruction counts from the emitted assembly; runtime is best of 5 over a 20-million-element array; checksum identical in every row.

| Level | instructions | runtime |
|---|---|---|
| `-O0` | 28 | 45 ms |
| `-O1` | 15 | 13 ms |
| `-O2` | **57** | **8 ms** |
| `-O3` | 57 | 7 ms |
| `-Os` | 15 | 14 ms |

**Read the `-O2` row twice. It has nearly four times as many instructions as `-O1` and runs 1.6× faster.**

The extra instructions are SSE — `-O2` vectorised the loop, processing eight elements per iteration, and paid for it in setup code, an alignment check, and a scalar remainder loop. **"Optimised" does not mean "fewer instructions", and instruction count is not a proxy for speed.**

`-Os` is the control that proves the point: it produces exactly `-O1`'s 15 instructions and pays 1.75× `-O2`'s runtime, because it *refuses* the vectorisation on size grounds. **These are different objectives, not different amounts of effort.**

### The whole of L11 is visible in the `-O1` listing

```asm
        testl   %esi, %esi          # rotation guard: skip if n <= 0
        jle     .LBB0_1
        leal    1(,%rdx,2), %ecx    # k*2+1, HOISTED, and one instruction
        movl    %esi, %edx
        xorl    %esi, %esi
        xorl    %eax, %eax
.LBB0_3:
        movl    (%rdi,%rsi,4), %r8d # a[i]
        imull   %ecx, %r8d
        addl    %r8d, %eax          # s = s + ...
        incq    %rsi                # induction variable, step 1
        cmpq    %rsi, %rdx
        jne     .LBB0_3
        retq
```

**Six instructions in the loop body.** The `testl/jle` pair is the guard rotation introduced. The `leal` is `k * 2 + 1`, hoisted by LICM into the guarded preheader *and* strength-reduced into a single address computation. `incq`/`cmpq` is the induction variable. `%eax` accumulates `s` and never touches memory, because register allocation gave it a register for the whole loop.

**Every optimisation in this week's two lectures, in thirteen lines you can read.**

### Compile time

All five levels compiled this function in 0.02–0.03 s, which tells you nothing, because one function is not where compile time goes. **The real trade shows up at scale**: LLVM's `-O2` pipeline over a large translation unit runs hundreds of passes, several of them more than once, and Chromium's build time is measured in CPU-hours. **The trade is real, it is just not visible in a 9-line benchmark** — and a claim you cannot measure on your own machine is one you should be careful about repeating.

---

## 10. Link-Time Optimisation

Every optimisation this week stops at the edge of a translation unit. The compiler sees `scale.c`; it does not see the caller in `drv.c`, so it cannot inline `scale`, cannot know `k` is always 3, and cannot specialise on that.

**LTO defers code generation to link time.** `clang -flto` emits LLVM bitcode instead of object code, and the linker optimises across the whole program: cross-module inlining, whole-program dead-code elimination, devirtualisation.

**What it costs:** link times that can dominate the build, and much larger memory use, because the linker now holds the whole program's IR. ThinLTO is the industrial compromise — a summary-based approximation that keeps most of the benefit and parallelises.

**What it changes conceptually:** the boundary of "the program" moves. Separate compilation was a 1970s decision about machines with 64 KB of memory, and LTO is the admission that it costs real optimisation opportunities.

---

## 11. Where This Leaves the Compiler

You now have the middle end: **liveness, loops, LICM, induction variables, interference, allocation.** `cyanc` runs source → tokens → AST → typed AST → TAC → CFG → optimised TAC → allocated registers.

**Week 6 leaves the compiler and goes to the runtime**, because there is a question the middle end cannot answer: your `alloc` instruction produces a pointer, and nothing in the pipeline ever frees it. Who does, and what does it cost to decide?

**Week 11 replaces our TAC with real LLVM IR**, hands it to `llc`, and everything in this lecture happens again — properly, at production quality, and you will be able to read the passes by name because you have written the toy versions.

**Reproduce everything:**

| Claim | Command |
|---|---|
| 18 nodes, 69 edges; degrees | `python3 regalloc.py scale.cy scale 4` |
| Zero spills first at $k = 7$ | same, bottom table |
| Peak simultaneous liveness 7 | `live.py` + the snippet in Lab 5 Q12 |
| `-O2` has 57 instrs, `-O1` has 15 | `clang -O{1,2} -S scale.c` |
| `-O2` 8 ms vs `-O1` 13 ms | `drv.c`, best of 5 |
| `-Os` = `-O1` size, 14 ms | same |

---

*CS 211 · Week 5 · Lecture 12 · © CSE Department*

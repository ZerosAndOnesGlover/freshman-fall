# CS 201 · Computer Organization & Architecture
## Week 2 · Lecture 3 of 3
### Flags, Conditionals, and Control Flow

*“...our intellectual powers are rather geared to master static relations and... our powers to visualize processes evolving in time are relatively poorly developed.”* — Edsger W. Dijkstra, "Go To Statement Considered Harmful" (1968)

---

**Reading:** CS:APP §3.6 · **Previous:** L08, arithmetic

**Coursework:** 📝 **PS 1** due today 17:00 · 📊 **Quiz 3** Mon of Week 3 · 🔬 **Lab 2** Tue of Week 3 15:00–16:50 · 📝 **PS 3** released Wed of Week 3, due Fri of Week 4 17:00

---

## 1. The Flags Register

Almost every arithmetic and logical instruction writes four bits of hidden state:

| Flag | Name | Set when |
|---|---|---|
| **ZF** | Zero | result was zero |
| **SF** | Sign | result's top bit is 1 |
| **CF** | Carry | **unsigned** overflow — carry out of the top bit |
| **OF** | Overflow | **signed** overflow |

**CF and OF are independent.** You proved this in ECE 110 when you built the adder: all four combinations occur, and $\text{OF} = C_{in} \oplus C_{out}$. The hardware computes both on every `add` because it does not know which interpretation you meant. **The instruction that reads them decides whether the operands were signed.**

---

## 2. `cmp` and `test` Compute Nothing

```
cmp  a, b      ; computes a - b, DISCARDS it, keeps the flags
test a, b      ; computes a & b, DISCARDS it, keeps the flags
```

**Neither writes a general-purpose register.** This is the single most common misreading of x86-64 assembly, and it was Quiz 1's Q7.

`test edi,edi` is the idiomatic "is this zero?" — ANDing a value with itself does not change it, but it sets ZF if it is zero and SF if it is negative. **It is one byte shorter than `cmp edi,0`**, which is the only reason it is preferred.

---

## 3. The Conditional Jumps

Which flags a jump reads is determined by whether it is a **signed** or **unsigned** comparison. Getting this wrong is a real bug, not a style issue.

| Signed | Unsigned | Condition after `cmp a, b` |
|---|---|---|
| `je` / `jz` | same | $a = b$ — ZF |
| `jne` / `jnz` | same | $a \ne b$ |
| `jl` | `jb` | $a < b$ |
| `jle` | `jbe` | $a \le b$ |
| `jg` | `ja` | $a > b$ |
| `jge` | `jae` | $a \ge b$ |

**Mnemonics:** signed uses **l**ess/**g**reater; unsigned uses **b**elow/**a**bove. `jl` reads SF ≠ OF; `jb` reads CF. **Different flags entirely, for the same-looking source comparison.**

```c
if (a < b) ...   /* int  a, b      ->  jge (branch past)  */
if (a < b) ...   /* unsigned a, b  ->  jae                */
```

The compiler picks from the C types. **When you write assembly by hand, you pick — and nothing checks you.** This is Week 1's signed/unsigned bug at the instruction level.

---

## 4. One Comparison for a Range Check

The unsigned jumps enable an idiom worth recognising on sight.

```c
if (x >= 0 && x <= 6) ...
```

compiles to **one** comparison:

```
cmp    edi,0x6
ja     out_of_range
```

*(Verified — from the `switch` below.)*

**Why it works:** `ja` is *unsigned* above. If `x` is negative, its bit pattern as unsigned is enormous — greater than 6 — so `ja` is taken. If `x` is in $[0,6]$ it is not. **One instruction tests both bounds**, because the signed/unsigned reinterpretation from Week 1 L04 §6 folds the lower bound into the upper one.

You will see this everywhere once you know it: bounds checks, `switch` dispatch, character-class tests.

---

## 5. How a `switch` Actually Compiles

Three different strategies, chosen by the shape of the cases.

### 5.1 Arithmetic progression → no table at all

```c
switch (x) { case 0: return 10; case 1: return 20; /* … */ case 6: return 70; default: return -1; }
```

```
<sw>:  mov    eax,0xffffffff
       cmp    edi,0x6
       ja     ret
       lea    eax,[rdi+rdi*4+0x5]     ; (5x + 5)
       add    eax,eax                 ; * 2  ->  10x + 10
ret:   ret
```

*(Verified.)* **GCC noticed the results form the sequence $10x + 10$** and computed it. No table, no branches per case, four instructions total. Check: $x=0 \to 10$ ✓, $x=6 \to 70$ ✓.

### 5.2 Irregular values → a lookup table of *results*

Change the returns to something without a pattern — 17, 4, 99, 4, −8, 250, 3:

```
<sw2>:  mov    eax,0xffffffff
        cmp    edi,0x6
        ja     ret
        mov    edi,edi                     ; zero-extend to use as an index
        lea    rax,[rip+0x0]               ; address of the table
        mov    eax,DWORD PTR [rax+rdi*4]   ; one indexed load
ret:    ret
```

and in `.rodata`:

```
0000 11000000 04000000 63000000 04000000
0010 f8ffffff fa000000 03000000
```

*(Verified — `0x11` = 17, `0x04` = 4, `0x63` = 99, `0x04` = 4, `0xfffffff8` = −8, `0xfa` = 250, `0x03` = 3. All seven, little-endian.)*

**Still no branching between cases.** The seven results live in read-only data and one indexed load picks the right one. Note `mov edi,edi` — a 32-bit self-move whose only purpose is **zeroing the upper half of `rdi`** so it is safe as a 64-bit index. L03's rule again, doing necessary work.

### 5.3 Cases that are statements → a jump table

When the cases execute code rather than yielding values, the table holds **code locations**, and dispatch is an indirect jump:

```
<dispatch>:  cmp    edi,0x6
             ja     default
             lea    rdx,[rip+0x0]                ; address of the table
             mov    edi,edi                      ; zero-extend the index
             movsxd rax,DWORD PTR [rdx+rdi*4]    ; load a 32-bit signed offset
             add    rax,rdx                      ; offset + table base = target
             notrack jmp rax                     ; indirect jump
```

*(Verified.)*

**The table holds 32-bit signed offsets from the table's own address, not 64-bit absolute addresses.** Two reasons: it halves the table's size, and it contains no absolute addresses, so the whole thing works unchanged wherever the loader places the code — the same position-independence argument as L02 §5's relative branches.

The `notrack` prefix relates to Intel CET, the control-flow-integrity feature `endbr64` belongs to; it marks this indirect jump as one that need not land on an `endbr64`. Week 9 explains why that matters.

**The cost is one indirect branch**, which the predictor finds much harder than a direct one (Week 5).

### 5.4 Sparse cases → a comparison chain

```c
switch (x) { case 1: return 1; case 1000: return 2; default: return 0; }
```

```
<sparse>:  mov    eax,0x1
           cmp    edi,0x1
           je     ret
           xor    eax,eax
           cmp    edi,0x3e8      ; 1000
           sete   al
           add    eax,eax        ; 0 -> 0, 1 -> 2
ret:       ret
```

*(Verified.)* A table indexed 0…1000 for two live entries would waste 4 KB, so GCC emits comparisons — and then, characteristically, turns the second one branchless with `sete` and a doubling.

**The switch/if-else distinction is not about which you wrote; it is about the density of the case values.**

---

## 6. Loops Are Branches Backwards

There is no loop instruction worth using. Every loop is a conditional branch to an earlier address, and the compiler picks the arrangement.

**Rotated (the usual form)** — test at the bottom, one branch per iteration:

```
        jmp    .test          ; enter by jumping to the test
.body:  ...
.test:  cmp    ...
        jle    .body
```

You saw exactly this in Week 0's `sum_to`. The initial `jmp` runs once; every iteration after that costs a single backward branch. **A naive top-test arrangement costs two branches per iteration** — the test and an unconditional jump back.

**When the compiler can prove the loop runs at least once**, it drops the entry `jmp` entirely.

---

## 7. Reading Control Flow Fast

Given an unfamiliar listing:

1. **Find `ret`.** That is the end.
2. **Find backward branches.** Each is a loop; its target is the top of the body.
3. **Find `cmp`/`test` immediately before each `jcc`.** That pair is one source-level condition.
4. **Check signed vs unsigned** on the jump. `jl` versus `jb` tells you the C types.
5. **Look for `ja` after a `cmp` with a small constant.** That is a range check, §4.

**Do not read linearly.** Assembly listings are graphs printed in address order, and address order is not execution order.

---

## 8. What to Take Away

1. **Four flags: ZF, SF, CF, OF.** CF is unsigned overflow, OF is signed. Both are always computed.
2. **`cmp` and `test` write no register** — only flags.
3. **`jl` and `jb` read different flags.** Signed uses less/greater; unsigned uses below/above.
4. **`cmp x,N` + `ja` is a two-sided range check in one comparison.**
5. **A `switch` becomes arithmetic, a value table, a jump table, or a comparison chain** — the compiler picks by density and regularity.
6. **Loops are backward branches, usually bottom-tested** to cost one branch per iteration.

---

## Exercises

1. After `cmp eax, ebx` with `eax = 0x80000000` and `ebx = 1`, give ZF, SF, CF and OF. Then say whether `jl` and `jb` each branch, and why they disagree.
2. Write the two-instruction range check for $10 \le x \le 20$ using the §4 idiom. *(Hint: subtract first.)*
3. §5.1's `switch` compiled to $10x + 10$. Change one case value so GCC can no longer do this, predict which strategy it falls back to, then check.
4. In §5.2, why is `mov edi,edi` necessary? What would go wrong without it if `x` were, say, the result of a computation that left junk in the upper 32 bits?
5. A bottom-tested loop needs an entry `jmp` when the trip count might be zero. Write the C for a loop where the compiler can omit it, and one where it cannot.

---

*Next week: procedures, the stack, and the calling convention — where these registers came from and where they go.*

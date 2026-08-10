# CS 201 · Problem Set 3
## Recursion, the Stack, and the Calling Convention

---

**Released:** Week 3, Wednesday · **Due:** Week 4, Friday 17:00
**Total: 100 points** · Submit one PDF plus a `.zip` of source, `PS3_{LastName}_{StudentID}.pdf`

> **Q3 is the centrepiece** — recursive Fibonacci in x86-64 assembly, which must assemble, link and
> agree with a C reference. Everything else supports it.
>
> All assembly in Intel syntax via `nasm -f elf64`, with `.note.GNU-stack` in every `.asm` file.

---

### Q1: Reading a Frame (20 points)

This is `fib` at `-O0`:

```
   0:  endbr64
   4:  push   rbp
   5:  mov    rbp,rsp
   8:  push   rbx
   9:  sub    rsp,0x18
   d:  mov    QWORD PTR [rbp-0x18],rdi
  11:  cmp    QWORD PTR [rbp-0x18],0x1
  16:  jle    40
  18:  mov    rax,QWORD PTR [rbp-0x18]
  1c:  sub    rax,0x1
  20:  mov    rdi,rax
  23:  call   fib
  28:  mov    rbx,rax
  2b:  mov    rax,QWORD PTR [rbp-0x18]
  2f:  sub    rax,0x2
  33:  mov    rdi,rax
  36:  call   fib
  3b:  add    rax,rbx
  3e:  jmp    44
  40:  mov    rax,QWORD PTR [rbp-0x18]
  44:  mov    rbx,QWORD PTR [rbp-0x8]
  48:  leave
  49:  ret
```

**(a) [5]** Draw the frame as a table of offsets from `rbp`, from `rbp+8` down to `rbp-0x18`, naming what occupies each 8-byte slot. GDB reports the frame as **48 bytes** — account for every one.

**(b) [5]** Instruction `28` moves `rax` into `rbx`. **Explain precisely why**, referring to the calling convention and to instruction `36`. What would go wrong if it used `r10` instead, and for which value of `n` would you first see it?

**(c) [4]** Instruction `44` restores `rbx` from `[rbp-0x8]`, and there is no matching `pop rbx`. Where did `rbx` get pushed, and why can the restore be a `mov` rather than a `pop`?

**(d) [3]** `leave` is one instruction. Write the two it replaces, and say why using it is safe even though `rsp` has moved since the prologue.

**(e) [3]** Only three of the twenty-two instructions do arithmetic on `n`. What are the other nineteen for? Answer in one sentence, then say what `-O2` does about it.

---

### Q2: The Convention (18 points)

**(a) [4]** Give the register or stack location for every argument of:

```c
void f(int a, double b, int c, double d, long *e, int g, int h, double i);
```

**(b) [4]** Classify each as caller-saved or callee-saved: `rax`, `rbx`, `rcx`, `r9`, `r11`, `r12`, `rbp`, `rdi`.

Then state, in one sentence each, what obligation the classification places on **the caller** and on **the callee**.

**(c) [4]** A function receives nine arguments. Sketch what it sees at `[rsp]`, `[rsp+8]`, `[rsp+16]` and `[rsp+24]` on entry, before its prologue runs.

**(d) [3]** Stack arguments are pushed by the caller in **reverse** order, and the **caller** removes them afterwards. Explain how each of those two choices is necessary for `printf` to be implementable.

**(e) [3]** `nonleaf(int x) { return leaf(x) + leaf(x+1); }` where `leaf(x) = 2x+1` compiles at `-O1` to two instructions with no `call` at all. Give them, and say what the compiler did.

---

### Q3: Recursive Fibonacci in Assembly (36 points)

Write `asm_fib` in NASM. **Naive recursion — two recursive calls, no memoisation, no loop.**

```
long asm_fib(long n);      /* n in rdi, result in rax */
```

Supply a `driver.c` that compares it against a C reference for $n = 0 \ldots 20$ and prints `fib(30)`.

```bash
nasm -f elf64 -o fib.o fib.asm
gcc -O2 -no-pie -o driver driver.c fib.o
./driver
```

**(a) [14]** The implementation. It must be correct for $n = 0$ and $n = 1$, and agree with the C reference throughout.

**(b) [6]** **Justify your register choices in a comment block.** Which values must survive a `call`, which registers you put them in, and why those registers specifically.

**(c) [6]** **Show your alignment arithmetic.** State `rsp mod 16` at function entry, after each push, and immediately before each `call`. If you needed a `sub rsp, 8`, say which push count made it necessary.

**(d) [4]** Your base case should return **before** the prologue. Explain the saving, and quantify it: `fib(10)` makes **177** calls in total — how many of those hit the base case?

**(e) [6]** Deliberately break it in **two** ways, one at a time, and report what happens:

1. Hold the first recursive result in `r10` instead of a callee-saved register. Does it still compile? Does it still give the right answer? For which `n` does it first fail?
2. Remove your alignment `sub` (and its matching `add`). Run it. Then call this from inside the recursion and run it again:

```c
/* put this in driver.c */
void sse_probe(void) {
    double b[4] __attribute__((aligned(16))) = {1,2,3,4};
    double s = 0; for (int i = 0; i < 4; i++) s += b[i];
    printf("%.0f\n", s);          /* the printf is load-bearing -- see below */
}
```

**Expect the misaligned version to keep working**, at least at first. Report what you actually observed rather than what you expected.

Then answer: **why does misalignment so often not crash?** Your answer must name the specific kind of instruction that faults, and say what has to be true of the callee for it to be emitted.

Finally — if you drop the `printf` from `sse_probe`, the crash goes away again. Disassemble `sse_probe` both ways and explain. *(This is Week 0's Lab 4.1 in a new costume.)*

Report exactly what you observed in all cases, **including every case where the broken version still produced the right answer.** Those are the interesting results, not failures of the exercise — a bug that is silent on your machine today is the one that reaches production.

---

### Q4: Alignment and the Red Zone (14 points)

**(a) [4]** State the alignment rule precisely, in terms of `rsp` immediately before `call` and on entry to the callee. Then complete:

| Point | `rsp` mod 16 |
|---|---|
| before `call f` | |
| on entry to `f` | |
| after `f` pushes 3 registers | |
| what `f` must `sub` before its own `call` | |

**(b) [4]** `void h(void) { g(); }` compiles to `sub rsp,0x8` / `call g` / `add rsp,0x8` / `ret`. `h` has no locals. **What is the `sub` for?**

**(c) [3]** A misaligned `rsp` at a `call` produced `Segmentation fault` inside a *different*, correct function, on a `movaps` instruction. Explain the chain of cause and effect, and say why the crashing function is not the buggy one.

**(d) [3]** `int f(int x){ int a=x+1,b=x+2; return a*b; }` at `-O0` stores three locals below `rsp` with **no** `sub rsp`. Name the feature, give its size, and state the two conditions for using it.

---

### Q5: How Deep Can You Go? (12 points)

**(a) [4]** Your `asm_fib` frame is some number of bytes. State it, showing the arithmetic. With an 8 MB stack, how many frames fit?

**(b) [4]** Naive Fibonacci recurses to depth $n$ but makes $O(\varphi^n)$ calls. For `fib(50)`, estimate **both** the maximum stack depth and the number of calls. Which is the binding constraint, and why do students routinely confuse them?

**(c) [4]** A recursive-descent parser has the opposite profile: few calls, unbounded depth, on input an attacker controls.

Explain why that is a **denial-of-service vulnerability**, and describe the standard mitigation. Say what happens at the hardware level when the limit is exceeded — there is no bounds check in `call`, so what actually stops it?

---

## Marks

| | |
|---|---:|
| Q1 Reading a Frame | 20 |
| Q2 The Convention | 18 |
| Q3 Recursive Fibonacci in Assembly | 36 |
| Q4 Alignment and the Red Zone | 14 |
| Q5 How Deep Can You Go? | 12 |
| **Total** | **100** |

---

*CS 201 · Week 3 · Problem Set 3*

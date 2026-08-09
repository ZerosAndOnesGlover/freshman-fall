# CS 201 · Lab 0 — Solutions and TA Notes
## Instructor Only

---

> **Lab 0 is unmarked.** These notes exist so the TA can check the four checkpoints quickly and knows
> which failures are expected. Every command and every number below was run on the lab image
> (Ubuntu 24.04, GCC 13.3.0, binutils 2.42, GDB 15.1, Intel Core i5-8250U).

---

## Timing

| Part | Budget | Reality |
|---|---|---|
| 1 — toolchain | 10 min | 5 min unless `apt` is slow |
| 2 — compile and look | 25 min | **This runs long.** Most of the session's value is here |
| 3 — gdb | 30 min | 30 min; students who have never used gdb need shepherding |
| 4 — the constant fold | 25 min | 20 min, and it is the part they will remember |
| 5 — optional | — | Few will reach it |

**If you are short of time, cut Part 5 and then Part 3.2, in that order.** Do not cut Part 4; it is the point of the lab.

---

## Part 1 — Toolchain

Expected versions on the image:

```
gcc      13.3.0
objdump  2.42
gdb      15.1
valgrind 3.22.0
nasm     2.16.01
```

All five are on the lab image. Students on their own laptops may hit:

| Problem | Fix |
|---|---|
| `nasm: command not found` | `sudo apt update && sudo apt install nasm` |
| `E: Unable to locate package nasm` | `sudo apt update` first — the index is stale on fresh images |
| macOS laptop | `brew install nasm`, but warn them: macOS uses Mach-O, and `-f elf64` in §1.1 will not link. **Weeks 2–3 assume Linux/ELF.** Point them at the lab machines or a VM |
| WSL | Works fine. `perf` in later labs may not; not an issue today |

### 1.1 — the nasm smoke test

```
$ ./hello
hello, CS 201
```

If `ld` complains about a missing `_start`, they have written `main` instead — there is no libc here to call it.

**The point of the disassembly step**, which is easy to rush past: they wrote `mov rax, 1` and NASM emitted `mov eax,0x1`. *(Verified — also `mov rdx, 14` → `mov edx,0xe`, while `xor rdi, rdi` stays 64-bit.)* The 32-bit form zeroes the upper half, so the result is identical and the encoding is one byte shorter.

**This is L03 §4's zeroing rule, appearing before it is taught, in code the student wrote themselves.** Draw the room's attention to it — it is a cheap way to make Week 2 feel earned, and it sets up Part 4 by showing that even the assembler is not a literal transcription.

**✅ CHECKPOINT 1** — five version strings and `./hello` printing.

---

## Part 2 — Compile and Look

### 2.1 Expected answers

1. **`int total = 0;`** → `mov DWORD PTR [rbp-0x8],0x0` at `0x1154`.
2. **`total += i;`** → `mov eax,DWORD PTR [rbp-0x4]` then `add DWORD PTR [rbp-0x8],eax` — **two** instructions, `0x1164` and `0x1167`. Students who name only the `add` have missed that the value must be loaded into a register first, because x86-64 cannot add memory to memory.
3. **`i` is at `[rbp-0x4]`, `total` at `[rbp-0x8]`.** Both are on the **stack**, in the function's frame. At `-O0` GCC keeps nothing in registers across statements — that is what makes the debug experience predictable.
4. **`rbp` is the frame pointer**: a fixed anchor for the frame, so every local has a constant offset from it even as `rsp` moves. Week 3 is the full story.

> **Address drift is normal.** PIE means the disassembly addresses are file offsets, and `gdb` will
> show them relocated to `0x5555...`. Reassure them; it is the same code.

### 2.2 The interleaved listing

`objdump -S` requires `-g` **and** requires the source file to still be present at the recorded path. If a student moved `sum.c` after compiling, `-S` shows assembly with no source and looks broken. Recompile in place.

**✅ CHECKPOINT 2** — the interleaved listing plus four answers. Expect Q2 to be the wrong one.

---

## Part 3 — gdb

Real output from the lab image:

```
Breakpoint 1, sum_to (n=100) at sum.c:4
4           int total = 0;
=> 0x555555555154 <sum_to+11>:  movl   $0x0,-0x8(%rbp)
   0x55555555515b <sum_to+18>:  movl   $0x1,-0x4(%rbp)
   0x555555555162 <sum_to+25>:  jmp    0x55555555516e <sum_to+37>
   0x555555555164 <sum_to+27>:  mov    -0x4(%rbp),%eax
   0x555555555167 <sum_to+30>:  add    %eax,-0x8(%rbp)
   0x55555555516a <sum_to+33>:  addl   $0x1,-0x4(%rbp)
rdi            0x64                100
rsp            0x7fffffffd270      0x7fffffffd270
```

**Two things to draw attention to, out loud, to the whole room:**

**`rdi` holds 100.** They are looking at the calling convention three weeks before it is taught. Say so — it makes Week 3 land better.

**gdb prints AT&T, objdump was told Intel.** `movl $0x0,-0x8(%rbp)` and `mov DWORD PTR [rbp-0x8],0x0` are the same instruction. **Operand order is reversed.** This confuses people badly if nobody names it. `set disassembly-flavor intel` fixes it for the session; `echo 'set disassembly-flavor intel' >> ~/.gdbinit` makes it permanent, which is worth suggesting.

### 3.1 / 3.2

`total` climbs 0, 1, 3, 6, 10 — triangular numbers, which some will spot and which is a nice hook to the `-O2` unroll in Part 4.

**Common gdb problems:**

| Symptom | Cause |
|---|---|
| `No symbol table` | Compiled without `-g` |
| `print total` says "optimized out" | They are debugging `sum_O2`, not `sum_O0` |
| `stepi` seems to do nothing | It stepped one instruction; the C line has not changed. Have them run `x/i $pc` after each `stepi` |
| Breakpoint on line 6 never hits | Off-by-one in line numbering if they retyped the file. Use `break sum.c:6` after `list` |

**✅ CHECKPOINT 3** — they must be able to say that `jle` at the bottom jumps **backwards** to the top of the body, and roughly why (loop rotation: test at the bottom, one branch per iteration).

---

## Part 4 — The Constant Fold

### The `-O2` loop body

```
1270:   lea    rdx,[rdx+rax*2+0x1]
1275:   add    rax,0x2
1279:   cmp    rax,rcx
127c:   jne    1270
```

**Answer to "why `2*rax + 1`":** the loop is unrolled two deep. With `rax` = $i$, each pass adds $i + (i+1) = 2i + 1$, and `rax` advances by 2. Both additions of the original loop are folded into one `lea`, which computes an address expression without touching memory — the compiler's general-purpose three-input adder.

> Students often think `lea` is a memory access. It is not, and saying so clearly here saves
> confusion for the rest of the term.

### 4.1 — Measured on the lab image

| Build | Time | `movabs` in `main`? |
|---|---:|---|
| `-O0` | **0.2585 s** | no |
| `-O2` | **0.0000 s** | **yes** |

*(Verified. `-O0` median of three runs: 0.2641, 0.2584, 0.2574 s.)*

`main` at `-O2`:

```
10c0:   call   1070 <clock_gettime@plt>
10c5:   lea    rsi,[rsp+0x10]
10ca:   mov    edi,0x1
10cf:   call   1070 <clock_gettime@plt>
```

**Two instructions between the two clock reads**, and neither is the loop. Then:

```
1101:   movabs rdx,0x11c3793adb7080
```

```
$ python3 -c "print(0x11c3793adb7080)"
5000000050000000
```

**The answer, as an immediate operand.**

> Do not spoil this. Let them find the `movabs` themselves — the moment of realising the loop is
> simply *not there* is the one thing from this lab they will still remember in Week 11.

### 4.2 — Working fixes, all verified

Four that work, with measured times:

| Fix | Change | Time | `movabs` gone? |
|---|---|---:|---|
| **A** | `volatile long n = 100000000L;` | 0.0447 s | ✅ |
| **B** | `long n = 100000000L + (argc - 1);` *(and take `argc`)* | 0.0448 s | ✅ |
| **C** | Move `sum_to` to its own `.c` file, compile separately, link | 0.0452 s | ✅ |
| **D** | No source change: `gcc -O2 -fno-inline` | 0.0445 s | ✅ |

*(All four verified on the lab image.)*

A, B and C work by the same mechanism, and **that is the answer you are looking for** — not the specific edit. In each case the compiler can no longer prove `n`'s value at the point where the loop would be folded:

- **A** — `volatile` forbids assuming the value is stable, so it must be re-read.
- **B** — `argc` is unknown until run time.
- **C** — without LTO, the compiler cannot see inside `sum_to` while compiling `main`, nor see the call site while compiling `sum_to`.

**D is worth treating separately, and is the more interesting answer.** It changes no source at all. Inlining is what brings the loop body and the known value of `n` into the same place; forbid it and the two never meet, even though *both* facts are still available to the compiler. A student who finds D has discovered that the fold is not one optimisation but a **composition** of inlining and constant propagation, and that breaking either link is enough. Say so — it is the right way to think about optimisation passes generally, and Week 11 depends on it.

**Note the honest result: about 0.045 s, not zero.** The loop really does run. It is **~5.8× faster than `-O0`**, which is the unroll plus keeping everything in registers — exactly PS 0 Q3(c)'s 18 reads and 9 writes disappearing. Point out the connection if a student has already done the problem set.

**Fixes that do *not* work, which students will try:**

| Attempt | Measured | Why it fails |
|---|---|---|
| Making `n` `const` | 0.0000 s, `movabs` still there | Strengthens the compiler's case rather than weakening it |
| Marking `sum_to` `static` | 0.0000 s, `movabs` still there | Static gives the compiler *more* freedom, not less — it now knows there are no other callers |
| `printf("%ld", n)` before the loop | 0.0000 s, `movabs` still there | Printing a value does not make it unknown; GCC prints the constant *and* folds the loop |

*(All three verified — each still emits `movabs rdx,0x11c3793adb7080` in `main`.)*

**`static` is the instructive failure.** The intuition behind trying it — "restrict the compiler's view" — is exactly backwards, and it is worth saying why out loud: `static` narrows the *linker's* view, not the optimiser's.

**✅ CHECKPOINT 4** — constant-folded `main` shown, plus one working fix with the loop restored in the disassembly. **Accept any of A–D, or anything else that demonstrably removes the `movabs`** — require the disassembly, not just a changed timing number. A student who only reports "it takes 0.045 s now" has not shown the loop is back; make them look.

---

## Part 5 — Optional

```bash
gcc -O0 -S -masm=intel -o sum.s sum.c
```

Produces an 80-line `.s` file. The distinction worth drawing, if anyone gets here:

- **`gcc -S`** — the compiler's output: labels, `.cfi_*` directives, no addresses assigned yet.
- **`objdump -d`** — the linked binary: addresses resolved, directives gone.

Note that `gcc -S` writes `DWORD PTR -20[rbp]` where `objdump -M intel` writes `DWORD PTR [rbp-0x14]`. **Same operand, two spellings of Intel syntax**, and `-20` is decimal against `objdump`'s hex. Worth flagging so nobody thinks they are looking at different code.

---

## What Success Looks Like

A student leaving this lab should be able to, unprompted:

1. Compile with `-g` and disassemble one named function.
2. Set a breakpoint, run, and read a register.
3. Say that `gdb` and `objdump` may be showing them different syntaxes of the same instruction.
4. **Distrust the source as evidence of what the machine does.**

Item 4 is the only one that matters. The other three are muscle memory they will acquire anyway.

---

*CS 201 · Week 0 · Lab 0 Solutions · Instructor Only*

# CS 201 · Week 0 · Lab 0
## From C to Machine Code — Setting Up the Toolchain

---

**When:** **Friday of Week 0** (the Friday that closes the ten-day Week 0), 15:00–16:50, BH 210
**Covers:** Week 0 · **Bring:** nothing; the machines are set up except for one package
**Assessment:** unmarked, but **checked off by the TA before you leave.** See the syllabus.

---

## What This Lab Is For

Every later lab in this course assumes you can compile something, look at the machine code, and step through it. **This one is entirely about acquiring that reflex**, on a program small enough that nothing is confusing except the tools.

By the end you will have disassembled a function, matched the assembly to the C that produced it, stepped through it in `gdb`, and found a case where the compiler did something you would not have predicted.

**There is no report.** Show the TA your terminal at the checkpoints marked **✅ CHECKPOINT**.

---

## Part 1 — Confirm the Toolchain (10 min)

```bash
gcc --version
objdump --version
gdb --version
valgrind --version
nasm -v
```

On the lab machines you should see GCC 13.3, binutils 2.42, GDB 15.1, Valgrind 3.22, NASM 2.16.01.

**If you are on your own laptop, `nasm` is the one likely to be missing** — it is a separate assembler that nothing else depends on, so a normal build toolchain does not pull it in:

```bash
sudo apt update && sudo apt install nasm
```

You will not need it until Week 2, when you start *writing* assembly rather than reading it. Having it working now means Week 2 starts with the interesting part.

### 1.1 Prove nasm works

Write `hello.asm`:

```nasm
        global  _start
        section .text
_start: mov     rax, 1          ; write
        mov     rdi, 1          ; stdout
        mov     rsi, msg
        mov     rdx, 14
        syscall
        mov     rax, 60         ; exit
        xor     rdi, rdi
        syscall
        section .data
msg:    db      "hello, CS 201", 10
```

```bash
nasm -f elf64 -o hello.o hello.asm
ld -o hello hello.o
./hello                 # hello, CS 201
```

**No `gcc`, no libc, no `main`.** This is the smallest possible thing that runs on Linux: two system calls and fourteen bytes of text. Week 2 explains `syscall`; today it is just proof the assembler works.

**Then disassemble your own assembly and notice something:**

```bash
objdump -d --no-show-raw-insn -M intel hello | sed -n '/<_start>:/,/^$/p'
```

```
  401000:  mov    eax,0x1
  401005:  mov    edi,0x1
  40100a:  movabs rsi,0x402000
  401014:  mov    edx,0xe
  401019:  syscall
```

*(Verified.)* **You wrote `mov rax, 1` and NASM emitted `mov eax,0x1`.** It silently used the 32-bit form — because writing to a 32-bit register zeroes the upper 32 bits, so the result in `rax` is identical and the encoding is a byte shorter. Note also `mov rdx, 14` became `mov edx,0xe`, but `xor rdi, rdi` stayed 64-bit.

> Even the assembler, which is supposed to be a one-to-one transcription, is not quite one-to-one.
> Hold onto that for Part 4.

**✅ CHECKPOINT 1** — all five tools report a version, and `./hello` prints.

---

## Part 2 — Compile and Look (25 min)

Create `sum.c`:

```c
#include <stdio.h>

int sum_to(int n) {
    int total = 0;
    for (int i = 1; i <= n; i++)
        total += i;
    return total;
}

int main(void) {
    printf("%d\n", sum_to(100));
    return 0;
}
```

Build it twice, unoptimised and optimised:

```bash
gcc -O0 -g -o sum_O0 sum.c
gcc -O2    -o sum_O2 sum.c
./sum_O0    # 5050
./sum_O2    # 5050
```

Now look at what the compiler actually produced:

```bash
objdump -d -M intel sum_O0 | sed -n '/<sum_to>:/,/^$/p'
```

You should get sixteen instructions, matching the listing in **L02 §3**. If your addresses differ slightly that is fine — they depend on the link layout, not on your code.

### 2.1 Match assembly to source

Work through the listing and answer, in your notes:

1. Which instruction corresponds to `int total = 0;`?
2. Which one is `total += i;`?
3. Where does `i` live? Where does `total` live? Neither is in a register — where are they?
4. The listing begins with `push rbp` and `mov rbp,rsp`. What is `rbp` for? *(One sentence; Week 3 is the full answer.)*

### 2.2 The `-g` flag earns its keep

```bash
objdump -S -M intel sum_O0 | sed -n '/<sum_to>:/,/^$/p'
```

`-g` put debug information in the binary, and `-S` uses it to interleave the original C with the assembly. **Compare your answers from 2.1 against this.** Getting one wrong here is expected and is the point of doing it in that order.

**✅ CHECKPOINT 2** — show the interleaved listing and your four answers.

---

## Part 3 — Step Through It (30 min)

```bash
gdb ./sum_O0
```

Inside `gdb`:

```
(gdb) break sum_to
(gdb) run
(gdb) x/6i $pc          # next six instructions
(gdb) info registers rdi rsp rbp
```

You should see something close to:

```
Breakpoint 1, sum_to (n=100) at sum.c:4
4           int total = 0;
=> 0x555555555154 <sum_to+11>:  movl   $0x0,-0x8(%rbp)
   0x55555555515b <sum_to+18>:  movl   $0x1,-0x4(%rbp)
   0x555555555162 <sum_to+25>:  jmp    0x55555555516e <sum_to+37>
   ...
rdi            0x64                100
```

*(Verified — this is real output from the lab machine.)*

**Two things to notice immediately.**

**`rdi` holds `0x64`, which is 100** — the argument, in the register L03 §4 said it would be in. You have now seen the calling convention with your own eyes, three weeks before it is taught.

**`gdb` prints AT&T syntax** — `movl $0x0,-0x8(%rbp)` — while `objdump -M intel` printed `mov DWORD PTR [rbp-0x8],0x0`. **Same instruction, two notations.** Operands are in the opposite order. Week 2 covers this properly; for now, just be aware which one you are reading. If you prefer Intel everywhere:

```
(gdb) set disassembly-flavor intel
```

### 3.1 Watch the loop run

```
(gdb) break 6              # the `total += i;` line
(gdb) continue
(gdb) print total
(gdb) print i
(gdb) continue
(gdb) print total
```

Step it a few times and watch `total` climb: 0, 1, 3, 6, 10.

### 3.2 Step by instruction, not by line

```
(gdb) stepi
(gdb) x/i $pc
(gdb) info registers eax
```

`stepi` advances **one machine instruction**, not one line of C. Do it a dozen times around the loop and watch `rip` move between `0x…164` and `0x…174` — the loop rotation from L02 §3, happening in front of you.

**✅ CHECKPOINT 3** — demonstrate `stepi` around the loop and explain where the backward branch goes.

---

## Part 4 — The Compiler Does Not Do What You Think (25 min)

Now the optimised build:

```bash
objdump -d --no-show-raw-insn -M intel sum_O2 | sed -n '/<sum_to>:/,/^$/p'
```

**It is shorter, and the loop body is four instructions.** Find them. The interesting one is:

```
lea  edx,[rdx+rax*2+0x1]
```

`lea` — "load effective address" — computes an address but does not access memory; it just puts the computed value in the destination. So this is `edx = edx + 2*rax + 1`.

**Question: why `2*rax + 1`?** Work it out before reading on. *(With `rax` holding $i$, the loop is adding $i + (i+1)$ each time round — the compiler unrolled it two iterations deep and folded both additions into one instruction.)*

### 4.1 The part that should unsettle you

Write `bench.c`:

```c
#include <stdio.h>
#include <time.h>

long sum_to(long n) { long t = 0; for (long i = 1; i <= n; i++) t += i; return t; }

int main(void) {
    struct timespec a, b;
    long n = 100000000L;
    clock_gettime(CLOCK_MONOTONIC, &a);
    long r = sum_to(n);
    clock_gettime(CLOCK_MONOTONIC, &b);
    printf("result=%ld  %.4f s\n", r,
           (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) / 1e9);
    return 0;
}
```

```bash
gcc -O0 -o bench_O0 bench.c && ./bench_O0
gcc -O2 -o bench_O2 bench.c && ./bench_O2
```

On the lab machine: **`-O0` takes about 0.26 s. `-O2` reports 0.0000 s.**

That is not a fast loop. Find out what it is:

```bash
objdump -d --no-show-raw-insn -M intel bench_O2 | sed -n '/<main>:/,/ret/p'
```

Look for the two `call clock_gettime@plt` instructions. **How many instructions are between them?** Then find:

```
movabs rdx,0x11c3793adb7080
```

and convert it:

```bash
python3 -c "print(0x11c3793adb7080)"
```

**GCC computed the entire hundred-million-iteration loop at compile time and emitted the answer as a constant.** The loop is not in the program.

> **Why it was allowed to.** `n` is a local variable initialised to a literal and never modified, so
> its value is known at compile time. The C standard requires only that the program's *observable
> behaviour* be correct — and the observable behaviour here is a `printf` of 5000000050000000.
> How that number is arrived at is the compiler's business.
>
> **Why this matters beyond a party trick.** Every microbenchmark you will ever write is vulnerable
> to this. Week 11 is largely about measuring things that the compiler has not already deleted.

### 4.2 Defeat it

Change one thing so the loop actually runs at `-O2`, and prove it by disassembling again. There are several valid answers; find one and be ready to say why it works.

**✅ CHECKPOINT 4** — show the constant-folded `main`, and your fix with the loop restored.

---

## Part 5 — Optional, If You Have Time

```bash
gcc -O0 -S -masm=intel -o sum.s sum.c
less sum.s
```

`-S` stops after generating assembly, before assembling it. This is the compiler's *output*, whereas `objdump` shows you the *linked binary* — mostly the same instructions, but `sum.s` has labels and directives instead of addresses. Both views are useful; know which one you are looking at.

---

## Before You Leave

You should be able to do all of this without notes by Week 2:

| Task | Command |
|---|---|
| Compile with debug info | `gcc -O0 -g -o prog prog.c` |
| Disassemble one function | `objdump -d -M intel prog \| sed -n '/<fn>:/,/^$/p'` |
| Interleave C with assembly | `objdump -S -M intel prog` |
| Compiler's assembly output | `gcc -S -masm=intel -o prog.s prog.c` |
| Break and inspect | `gdb ./prog`, then `break fn`, `run`, `x/8i $pc` |
| One instruction at a time | `stepi` |

**The habit this lab is trying to build:** when you want to know what the machine does, *look*. Do not reason about it from the C. The next thirteen weeks assume you will look.

---

*CS 201 · Week 0 · Lab 0*

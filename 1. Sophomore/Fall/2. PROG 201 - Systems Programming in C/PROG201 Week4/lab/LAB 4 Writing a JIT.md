# PROG 201 · Lab 4
## Writing a JIT — Machine Code at Runtime
### Covers Week 4 · sat **Monday of Week 5**, 15:00–16:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 4 and is sat in Week 5.** The lab is on Monday and this course's lectures
> are Tuesday to Thursday, so a lab can never be sat in the week it covers — Lab *N* is sat on the
> Monday of Week *N+1*. Every lab file states its own week; the file is authoritative.
>
> **Unmarked.** The TA checks your work off in the session.
>
> **Midterm 1 was last Monday.** Nothing in this lab is on it. Marked papers are returned in
> Tuesday's lecture.

**What you are building:** a compiler. A small one — it compiles polynomials — but a real one, in the sense that it produces machine code at runtime and jumps to it.

By the end you will have written fifty-one bytes of x86-64 by hand, made a page executable, called into it, and measured what that bought you against an interpreter. **It bought 5.5×.** You will also find out that it bought nothing at all against the C compiler, and why that is the expected answer rather than a disappointment.

---

## 0. Setup (5 minutes)

```bash
mkdir -p "$PROG201/week4/lab4"        # $PROG201 is set in ~/.bashrc -- see Lab 0
cd "$PROG201/week4/lab4"
cp "$ACADEMICS/1. Sophomore/Fall/2. PROG 201 - Systems Programming in C/PROG201 Week4/lab/"{jit.c,Makefile} .

make
./jit
```

The skeleton builds clean and is honest about what it is not doing yet:

```
emitted 8 bytes: 48 c7 c0 00 00 00 00 c3
emit_const(42): f(0) = 0, f(999) = 0   (both should be 42)
```

**It is already generating and calling machine code** — eight bytes that put zero in `%rax` and return. Everything after this is filling in constants and adding instructions.

`make_runnable` is provided, and reading it is the five minutes that make Part C make sense.

---

## 1. Part A — A Function That Returns a Constant (20 min)

**TODO 1 — `emit_const`.** The placeholder writes `mov $0,%rax; ret`. Make it write `mov $k,%rax`.

The encoding is `48 c7 c0` followed by **four bytes of immediate, least significant first**. Do not write those four bytes by hand — `memcpy` the `int` in, which gets the byte order and the sign right for free.

```
emitted 8 bytes: 48 c7 c0 2a 00 00 00 c3
emit_const(42): f(0) = 42, f(999) = 42   (both should be 42)
```

`2a` is 42. Two questions to answer before moving on — Q1 and Q2 want them:

- Try `emit_const(-1)`. What are the four bytes, and why?
- The instruction is `mov $imm32,%rax` with a 64-bit register and a 32-bit immediate. What does the CPU do with the top 32 bits? Try `emit_const(-1)` and print the result as `%lx`.

**Check your bytes against the assembler.** This is the habit worth taking from the lab:

```bash
echo "48 c7 c0 2a 00 00 00 c3" | xxd -r -p > /tmp/code.bin
objdump -D -b binary -m i386:x86-64 /tmp/code.bin
```

If `objdump` disagrees with what you meant, `objdump` is right.

---

## 2. Part B — The Polynomial (30 min)

**TODO 2 — `emit_poly`.** Horner's method for `a[0] + a[1]x + ... + a[n]x^n`:

```
    acc = a[n]
    for i = n-1 down to 0:
        acc = acc * x + a[i]
```

In registers, with `x` kept in `%rcx` so that `%rax` can be the accumulator:

| C | assembly | bytes |
| --- | --- | --- |
| keep `x` | `mov %rdi,%rcx` | `48 89 f9` |
| `acc = a[n]` | `mov $a[n],%rax` | `48 c7 c0` + imm32 |
| `acc *= x` | `imul %rcx,%rax` | `48 0f af c1` |
| `acc += a[i]` | `add $a[i],%rax` | `48 05` + imm32 |
| return | `ret` | `c3` |

Fifty-one bytes for the fixed quartic. Expected:

```
emitted 51 bytes: 48 89 f9 48 c7 c0 01 00 00 00 48 0f af c1 48 05 02 00 00 00 ...
     x            jit       expected
    -3             43             43
    -2             13             13
    ...
     5            867            867
```

**Disassemble your 51 bytes and read them back.** If a coefficient looks wrong in `objdump`, it is wrong in your emitter, and finding it there is much faster than finding it in the results table.

> **Why `%rcx`?** Because the System V calling convention says `%rcx` is caller-saved — the caller does not expect it preserved — so a leaf function may use it freely. Clobber `%rbx` instead and your program will break in a way that has nothing to do with this lab. `man 7 x86-64-abi` if your machine has it; CS:APP §3.7 otherwise.

---

## 3. Part C — The Four Corners of W^X (25 min)

**TODO 3 — `part_c`.** Four experiments, each in a forked child so a fatal signal is a result rather than the end of your session. `try(name, body)` is provided; write four small `body` functions and call `try` four times.

1. Emit into a `PROT_READ|PROT_WRITE` page and **call it without `mprotect`.**
2. `mprotect` it to `PROT_READ|PROT_EXEC` and call it.
3. **Write one byte** to a page that is already `PROT_READ|PROT_EXEC`.
4. `mmap` with `PROT_READ|PROT_WRITE|PROT_EXEC` and call that.

```bash
./jit wx
```

Ours:

```
1. call a PROT_READ|PROT_WRITE page                Segmentation fault
2. call it after mprotect(PROT_READ|PROT_EXEC)     no signal
3. write to a PROT_READ|PROT_EXEC page             Segmentation fault
4. mmap PROT_READ|PROT_WRITE|PROT_EXEC and call it no signal
```

**Three of those are the machine protecting you and the fourth is not.** Q4 and Q5 are about which is which, and about what it means that the fourth one is allowed.

---

## 4. Part D — What Did It Buy? (20 min)

```bash
./jit bench
```

Three ways to evaluate the same polynomial fifty million times: your generated code, a C loop over the coefficient array, and a bytecode VM with a `switch` dispatch — the thing a JIT actually replaces. Ours, three runs:

| | ns each | vs the JIT |
| --- | --- | --- |
| JIT-compiled | 2.08 – 2.22 | — |
| C loop over the array | 2.08 – 2.09 | **0.94 – 1.01×** |
| bytecode VM | 11.38 – 11.63 | **5.1 – 5.6×** |

Two results, and the second is the one people are not expecting.

**The JIT beat the interpreter by 5.5×.** That is the dispatch: the VM reads an opcode, branches on it, increments a pointer, and does that for every operation. The generated code has none of those — the operations *are* the instructions.

**The JIT did not beat the C compiler.** It tied it. Q6 asks why, and the answer is not that your emitter is bad.

---

## 5. Questions

Answer in the answer sheet. Three or four sentences each unless stated.

**Q1.** Give the four immediate bytes for `emit_const(-1)` and say why they are in that order.

**Q2.** `mov $imm32,%rax` is a 64-bit operation with a 32-bit immediate. What happens to the top 32 bits of `%rax`, and what does `emit_const(-1)` therefore return? *(Print it as `%lx`. The answer is a fact about the instruction, not about C.)*

**Q3.** Your `emit_poly` uses `%rcx`. Name one register you must **not** use without saving it first, and say where that rule is written down.

**Q4.** Experiments 1 and 3 both died with `SIGSEGV`. Say what hardware mechanism stopped each one, and why they are *not* the same mechanism.

**Q5.** Experiment 4 succeeded. State what W^X is, say whether this machine enforces it, and then say — in one sentence — what that means for a program that keeps the discipline anyway.

**Q6.** The JIT tied the C loop. Explain why, given that the C loop has a loop and a memory access per coefficient and your code has neither. *(Look at what the compiler knew about `A` and `N` when it compiled `horner`.)*

**Q7.** The JIT beat the bytecode VM by about 5.5×. Give the two costs the generated code does not pay, and then say what it would take to make the VM close the gap without generating code. *(Look up "computed goto" or "threaded dispatch". Two sentences.)*

**Q8.** `make_runnable` calls `__builtin___clear_cache` and it does nothing at all on this machine. Say what it does elsewhere, and why leaving it out is a bug you would not find here.

---

## 6. Checkoff

Show the TA:

- [ ] `./jit` with all nine polynomial rows matching.
- [ ] Your 51 bytes disassembled with `objdump`, and one instruction pointed at and explained.
- [ ] `./jit wx` with all four rows, and Q4 answered out loud.
- [ ] Your written answers to **Q5, Q6 and Q7**.

**If you finish early:** emit `x*a + b` with `a` and `b` read from `argv`, so the compiler is genuinely compiling something it did not know at build time. Then try a conditional — `return x < 0 ? -x : x` — which needs `cmp`, a forward `jge` with a **relative** displacement, and the realisation that you have to know the length of the code you have not emitted yet. That problem is called backpatching and it is what every real assembler spends its time on.

**Take with you:** Week 8 is dynamic linking, where the GOT and PLT are the loader patching addresses into code at runtime for exactly the reasons your backpatching problem exists. Week 10's return-oriented programming is this lab's fourth W^X corner, used by somebody else.

---

*PROG 201 · Week 4 · Lab 4 · © CSE Department*

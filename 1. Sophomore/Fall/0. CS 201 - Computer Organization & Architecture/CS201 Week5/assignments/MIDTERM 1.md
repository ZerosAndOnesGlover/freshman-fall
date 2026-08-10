# CS 201 · MIDTERM EXAMINATION 1
## Computer Organization & Architecture

---

**Week 5, Monday · 18:00–19:15 · VNC 100**
**Duration: 75 minutes · Total: 100 points · Weight: 12.5% of the course grade**
**Covers: Weeks 0–4**

---

**Name:** _________________________________ **Student ID:** ___________________

---

> **Permitted:** one handwritten sheet of A4, **one side only**. Student ID on the desk.
> **Not permitted:** calculators, electronic devices, printed material, the textbook.
>
> **Answer all five questions.** Marks are shown per part. Show your working — a correct method with
> an arithmetic slip earns most of the marks; a bare number earns none.
>
> **Where a question asks you to explain, one or two sentences is the expected length.**

---

## Q1 — Representation (20 points)

**(a) [4]** In 8-bit two's complement, give the bit pattern and value of the most negative number, and the result of negating it. Explain in one sentence why the range is asymmetric.

**(b) [6]** These two functions differ only in the type of `x`:

```c
int      f(int x)      { return x + 1 > x; }
unsigned g(unsigned x) { return x + 1 > x; }
```

At `-O2`, GCC compiles `f` to `mov eax,0x1; ret` and `g` to a real comparison against `0xffffffff`.

Explain **both** code generations. Your answer must say what the C standard permits in each case.

**(c) [4]** Give the 32-bit IEEE 754 pattern for `1.5f`, in binary and hex. State $s$, the stored exponent, the unbiased exponent, and the mantissa.

**(d) [3]** A `float` has 23 stored mantissa bits but 24 bits of precision. Explain the discrepancy, and state the integer at which a `float` stops being able to count by ones.

**(e) [3]** `(a+b)+c` gives 1.0 and `a+(b+c)` gives 0.0, for $a = 10^{16}$, $b = -10^{16}$, $c = 1$.

Identify **which single addition** destroyed the information, and say what happened in it.

---

## Q2 — Assembly (22 points)

**(a) [4]** Give the four components of a general x86-64 memory operand and the only legal scale values.

For `long *p` in `rdi` and index `i` in `rcx`, write the operand for `p[i]`.

**(b) [4]** `lea rax, [rdi+rdi*4]` — state what it computes and how many memory accesses it performs. Then give a single `lea` that computes $9a$ from `a` in `rdi`.

**(c) [5]** After `cmp eax, ebx` with `eax = 0x80000000` and `ebx = 0x00000001`:

1. Give ZF, SF, CF and OF.
2. State whether `jl` branches and whether `jb` branches.
3. Explain in one sentence why they disagree.

**(d) [5]** `int div8(int x) { return x / 8; }` compiles to four instructions, while `x >> 3` compiles to one:

```
test   edi,edi
lea    eax,[rdi+0x7]
cmovns eax,edi
sar    eax,0x3
```

Explain what the bias of 7 is for and why it is applied only in one case. State what `unsigned x / 8` compiles to instead, and why.

**(e) [4]** `cmp edi, 0x6` followed by `ja` rejects both `x < 0` and `x > 6` with one comparison.

Explain the mechanism, and name the Week 1 concept it depends on.

---

## Q3 — Procedures and the Stack (20 points)

Consider `fib` at `-O0`:

```
   4:  push   rbp
   5:  mov    rbp,rsp
   8:  push   rbx
   9:  sub    rsp,0x18
   d:  mov    QWORD PTR [rbp-0x18],rdi
  ...
  23:  call   fib
  28:  mov    rbx,rax
  ...
  36:  call   fib
  3b:  add    rax,rbx
```

**(a) [4]** Draw the frame from `rbp+8` down to `rbp-0x18`, naming what occupies each 8-byte slot. GDB reports the frame as 48 bytes — account for all of them.

**(b) [5]** Instruction `28` moves `rax` into `rbx`. Explain **precisely why**, referring to instruction `36` and to the calling convention.

State what would happen if it used `r10` instead — would it assemble? would it be correct?

**(c) [4]** Name the six integer argument registers in order. State where argument 7 is on entry to the callee, and who removes it afterwards.

**(d) [4]** State the stack alignment rule in terms of `rsp` immediately before `call` and on entry to the callee.

A function pushes **two** callee-saved registers and then makes a call. How many bytes must it `sub` from `rsp` first? Justify with the parity.

**(e) [3]** `ret` transfers control to an address taken from the stack. State what validates that address. Name one defence that exists because nothing does.

---

## Q4 — The Memory Hierarchy (24 points)

**(a) [4]** A cache has $S = 64$ sets, $E = 8$ ways, $B = 64$-byte lines. Give its capacity, the number of offset bits and the number of set-index bits.

**(b) [4]** Derive the byte stride at which every access maps to the **same set** in the cache from (a). State the row length in `double`s that produces it.

**(c) [4]** Classify each miss as compulsory, capacity or conflict, one sentence each:

1. The first read of a freshly `malloc`ed 500 MiB buffer.
2. Repeatedly traversing a 20 MiB linked list in random order, on a machine with a 6 MiB L3.
3. Alternating between two 4 KiB arrays exactly 32 KiB apart, in a direct-mapped 32 KiB cache.

**(d) [6]** Two loops sum the same $N \times N$ `int` matrix:

```c
for (i…) for (j…) s += m[i*N+j];        for (j…) for (i…) s += m[i*N+j];
```

The second is measured **30× slower**. The compiled instructions are nearly identical.

Explain the difference. Your answer must refer to the cache line size and to how much of each fetched line is used.

**(e) [6]** A blocked matrix transpose runs **3.29× faster** than the naive version. Cachegrind reports:

| | D1 miss rate | LLd miss rate |
|---|---:|---:|
| naive | 41.5% | 41.5% |
| blocked | 42.5% | 13.5% |

1. **[3]** The L1 miss rate went **up**. Explain how the program can nonetheless be 3.29× faster.
2. **[3]** In the naive version LLd misses almost exactly equal D1 misses. State what that tells you about L2 and L3, and what it implies about where to aim an optimisation.

---

## Q5 — Synthesis (14 points)

**(a) [5]** A program's hot loop reads one 4-byte field from each element of an array of 100 000 structs, each 96 bytes.

1. How many 64-byte lines does the loop touch?
2. Propose a layout change and state how many lines it would touch instead.
3. Give one non-performance disadvantage of your change.

**(b) [5]** You are told a program is slow. You have `objdump`, `gdb`, `valgrind --tool=cachegrind` and a stopwatch.

Describe, in order, the **first three things you would measure** and what each would rule in or out. **Marks are for the order and the reasoning, not for naming tools.**

**(c) [4]** In Week 0 a hundred-million-iteration loop compiled at `-O2` to a single `movabs` of the answer, and the program reported 0.0000 seconds.

State what happened, and give the general lesson about benchmarking that follows from it.

---

## Marks

| | |
|---|---:|
| Q1 Representation | 20 |
| Q2 Assembly | 22 |
| Q3 Procedures and the Stack | 20 |
| Q4 The Memory Hierarchy | 24 |
| Q5 Synthesis | 14 |
| **Total** | **100** |

---

*CS 201 · Midterm Examination 1 · Weeks 0–4 · Year 2 Fall*

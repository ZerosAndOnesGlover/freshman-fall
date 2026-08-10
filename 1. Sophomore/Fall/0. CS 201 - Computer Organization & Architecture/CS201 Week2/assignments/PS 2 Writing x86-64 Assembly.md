# CS 201 · Problem Set 2
## Writing x86-64 Assembly

---

**Released:** Week 2, Wednesday · **Due:** Week 3, Friday 17:00
**Total: 100 points** · Submit one PDF plus a `.zip` of source, `PS2_{LastName}_{StudentID}.pdf`

> Collaboration: discussing approaches is fine. The write-up and the code must be yours.
>
> **Q1 and Q2 are by hand.** **Q3 is the assembly you write** — it must assemble, link and pass the
> tests. **Q4 and Q5 want a derivation and an investigation.**
>
> All assembly in **Intel syntax**, assembled with `nasm -f elf64`. Include the
> `.note.GNU-stack` directive in every `.asm` file you submit — Q3(f) asks why.

---

### Q1: Reading Operands (16 points)

**(a) [4]** Translate each into the other syntax:

| Intel | AT&T |
|---|---|
| `mov eax, DWORD PTR [rbx+rcx*4+8]` | |
| | `movq $42, -16(%rbp)` |
| `lea rdx, [rsi+rsi*2]` | |
| | `cmpl %esi, %edi` |

**(b) [4]** For an `int *p` in `rdi`, give the single addressing-mode operand for `p[7]`, and for a `long *q` in `rsi`, the operand for `q[i]` with `i` in `rcx`. State the displacement in decimal and explain where it comes from.

**(c) [4]** `p[i*4 + 3]` on an `int *` compiles to a `shl` followed by `mov eax,DWORD PTR [rsi+rdi*1+0xc]`, rather than one addressing mode. Say precisely which field of `[base + index*scale + disp]` cannot express it, and give the largest constant `k` for which `p[i*k]` still needs no extra instruction.

**(d) [4]** Give three `lea` instructions that compute $3a$, $9a$ and $10a$ from `a` in `rdi`. One of them needs a second instruction — say which and why.

---

### Q2: Flags and Branches (18 points)

**(a) [6]** After `cmp eax, ebx` with `eax = 0x80000000` and `ebx = 0x00000001`, give **ZF, SF, CF, OF**. Show the subtraction you performed to get them.

Then state whether `jl` branches, whether `jb` branches, and **explain why they disagree**.

**(b) [4]** `test edi, edi` is preferred over `cmp edi, 0`. Give both reasons — one about encoding, one about which flags end up set.

**(c) [4]** Write a range check for $10 \le x \le 20$, with `x` in `edi`, branching to `out` when out of range, using **one conditional branch only**. *(Hint: shift the range down to start at zero, then apply the §4 idiom from L09.)*

State how many instructions yours takes, and confirm it rejects negative `x` without a separate test.

**(d) [4]** `cmp edi, 0x6` followed by `ja` rejects both `x < 0` and `x > 6`. Explain the mechanism, and connect it to the signed/unsigned conversion rule from Week 1 L04 §6.

---

### Q3: Five Functions in Assembly (36 points)

Write each in NASM, Intel syntax, in one `funcs.asm`. Arguments arrive in `rdi`, `rsi`, …; the return value goes in `rax`. **Use only `rax`, `rcx`, `rdx`, `rsi`, `rdi`, `r8`–`r11`** — the others are callee-saved and Week 3's business.

Provide a `driver.c` that tests each, and include your output.

```bash
nasm -f elf64 -o funcs.o funcs.asm
gcc -O2 -no-pie -o driver driver.c funcs.o
./driver
```

**(a) [6] `int asm_sign(int x)`** — returns −1, 0 or +1. **Branchless.** Test on −9, −1, 0, 1, 9, `INT_MIN`, `INT_MAX`.

**(b) [6] `int asm_abs(int x)`** — absolute value, branchless, using the `sar`/`xor`/`sub` idiom. **Report what it returns for `INT_MIN` and explain why that is unavoidable.**

**(c) [6] `long asm_sum_to(long n)`** — returns $\sum_{i=1}^{n} i$, by looping. Must return 0 for $n \le 0$. Test on 0, 1, 100 and −5.

**(d) [6] `int asm_count_bits(unsigned x)`** — population count, by looping over the bits. Test on 0, 1, 255, `0xffffffff`.

**(e) [8] `int asm_divmod10(int x, int *rem)`** — return $x/10$ and write $x \bmod 10$ through `rem`. **You must use `cdq` and `idiv`.** Test on 12345, −12345, 7, −7, 0.

State which register holds the quotient after `idiv` and which holds the remainder.

**(f) [4]** Every `.asm` file must end with:

```nasm
        section .note.GNU-stack noalloc noexec nowrite progbits
```

Build once **without** it, capture the linker warning, and run `readelf -lW driver | grep GNU_STACK` both ways. **Report both results and state what security property the missing line silently removed.**

---

### Q4: Deriving a Magic Number (18 points)

L08 §4 showed that `x / 10` compiles to a multiply by `0x66666667` and a shift of 34, with a sign correction.

**(a) [4]** Verify that $\texttt{0x66666667} = \lfloor 2^{34}/10 \rfloor + 1$. Show the arithmetic.

**(b) [6]** Derive the equivalent constant for **division by 3**. Choose a shift $s$, compute $M = \lfloor 2^{s}/3 \rfloor + 1$, and **show that the shift you chose is large enough** — that is, that $\lfloor Mx / 2^{s} \rfloor = \lfloor x/3 \rfloor$ for all $x$ in $[0, 2^{31})$.

You may argue the bound algebraically or verify it exhaustively by program; say which you did.

**(c) [4]** Implement your division-by-3 in C using only `*`, `>>` and `-` on 64-bit types, and check it against `x / 3` for at least $-10^6$, $-3$, $-1$, 0, 1, 3, $10^6$ and `INT_MAX`.

**(d) [4]** The compiled `div10` ends with `sar edi,0x1f` and `sub eax,edi`. Explain what those two instructions do and **why floor division must be converted to truncation** for C.

---

### Q5: How Your `switch` Compiles (12 points)

Take this and compile it four ways, at `-O2`, changing only the case bodies:

```c
int f(int x) { switch (x) { case 0: … case 6: … default: … } }
```

**(a) [3]** Returns forming an arithmetic progression (10, 20, …, 70). Report the strategy GCC chose and the instructions.

**(b) [3]** Returns that are irregular (17, 4, 99, 4, −8, 250, 3). Dump `.rodata` with `objdump -s -j .rodata` and **decode all seven values by hand from the hex**, showing your working for the negative one.

**(c) [3]** Cases that call functions rather than return values. Identify the dispatch sequence and explain **why the table holds 32-bit offsets rather than 64-bit addresses.**

**(d) [3]** Cases `1` and `1000` only. Report the strategy and say what makes a jump table the wrong choice here.

---

## Marks

| | |
|---|---:|
| Q1 Reading Operands | 16 |
| Q2 Flags and Branches | 18 |
| Q3 Five Functions in Assembly | 36 |
| Q4 Deriving a Magic Number | 18 |
| Q5 How Your `switch` Compiles | 12 |
| **Total** | **100** |

---

*CS 201 · Week 2 · Problem Set 2*

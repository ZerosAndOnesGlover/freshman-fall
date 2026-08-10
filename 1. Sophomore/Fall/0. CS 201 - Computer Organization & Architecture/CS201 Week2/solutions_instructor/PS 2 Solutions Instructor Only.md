# CS 201 · Problem Set 2 — Solutions
## Instructor Only

---

> **Not for distribution.** All assembly below was assembled with `nasm -f elf64`, linked with
> `gcc -O2 -no-pie`, and run. All disassembly is from GCC 13.3.0 on the lab image.

---

## Q1 (16) — Reading Operands

### (a) [4] — 1 each

| Intel | AT&T |
|---|---|
| `mov eax, DWORD PTR [rbx+rcx*4+8]` | `movl 8(%rbx,%rcx,4), %eax` |
| `mov QWORD PTR [rbp-16], 42` | `movq $42, -16(%rbp)` |
| `lea rdx, [rsi+rsi*2]` | `leaq (%rsi,%rsi,2), %rdx` |
| `cmp edi, esi` | `cmpl %esi, %edi` |

> The `cmp` row is the discriminator: AT&T's `cmpl %esi,%edi` computes `edi - esi`, so the Intel form
> is `cmp edi, esi`. A student who writes `cmp esi, edi` has reversed it and will get Q2(a) wrong too.

### (b) [4]

**`p[7]` for `int *p` in `rdi`:** `DWORD PTR [rdi+0x1c]` — displacement **28**, because `7 × sizeof(int) = 7 × 4`.

**`q[i]` for `long *q` in `rsi`, `i` in `rcx`:** `QWORD PTR [rsi+rcx*8]` — scale **8** for `sizeof(long)`.

**Where it comes from:** C scales pointer arithmetic by the pointee size. In assembly there are no types, so that scaling is folded into the displacement (constant index) or the scale field (variable index).

### (c) [4]

**[2]** The **scale** field. It encodes only 1, 2, 4 or 8. `p[i*4]` on an `int*` is a stride of $4 \times 4 = 16$ bytes, which no scale can express, so an explicit `shl rsi,0x4` is emitted first.

**[2]** **$k = 2$.** For `int*`, the effective scale is $4k$, and $4k \in \{1,2,4,8\}$ requires $k \in \{1, 2\}$ (giving scale 4 and 8). $k=2$ is the largest.

### (d) [4]

```
lea eax, [rdi+rdi*2]        ; 3a
lea eax, [rdi+rdi*8]        ; 9a
lea eax, [rdi+rdi*4]        ; 5a  — then
add eax, eax                ;      10a
```

**$10a$ needs the second instruction**, because 10 is not of the form $1 + \text{scale}$ for scale ∈ {1,2,4,8}. The available one-instruction multipliers are 2, 3, 5 and 9.

> Accept `lea eax,[rax+rax]` or `shl eax,1` for the doubling. A student who spots that the available
> set is $\{2,3,5,9\}$ — one more than each valid scale — has understood the encoding.

---

## Q2 (18) — Flags and Branches

### (a) [6]

$\texttt{0x80000000} - \texttt{0x00000001}$: as unsigned, $2^{31} - 1 = \texttt{0x7FFFFFFF}$, no borrow.

| Flag | Value | Why |
|---|---|---|
| **ZF** | 0 | result is non-zero |
| **SF** | 0 | top bit of `0x7FFFFFFF` is 0 |
| **CF** | 0 | no borrow — as unsigned, $2^{31} > 1$ |
| **OF** | **1** | as signed, $-2^{31} - 1$ should be $-2^{31}-1$, which is not representable |

**`jl` branches** (SF ≠ OF: $0 \ne 1$). Signed: $-2147483648 < 1$. **True.**
**`jb` does not** (CF = 0). Unsigned: $2147483648 > 1$. **False.**

**They disagree because the same 32 bits mean $-2^{31}$ signed and $+2^{31}$ unsigned.** The bits are identical; the jump chooses the interpretation.

### (b) [4]

**[2] Encoding:** `test edi,edi` is 2 bytes; `cmp edi,0` is 3. The saving is per-occurrence and these are extremely common.

**[2] Flags:** `test` is a bitwise AND, so it **always clears CF and OF** and sets only ZF and SF. `cmp` with 0 computes a subtraction and sets all four. For a zero/sign test the AND is the more precise statement of intent, and clearing CF/OF is harmless.

### (c) [4]

```
sub    edi, 10          ; or:  lea eax, [rdi-10]
cmp    edi, 10
ja     out
```

**Three instructions, one conditional branch.**

After `sub edi,10` the range $[10,20]$ maps to $[0,10]$, and `ja 10` rejects everything outside it. **Negative `x` is rejected without a separate test**: $x = -1$ becomes $-11$, whose unsigned reading is $2^{32}-11$, far above 10.

> Accept the `lea` variant, which preserves `edi`. **Deduct 2 for two signed comparisons and two
> branches** — that works but misses the entire point of the question. Deduct 1 if the student does
> not confirm the negative case.

### (d) [4]

**[2]** `ja` is *unsigned* above, reading CF. A negative `x` reinterpreted as unsigned is $\ge 2^{31}$, which is greater than 6, so `ja` is taken. A value in $[0,6]$ is not. **One comparison enforces both bounds.**

**[2]** **Connection:** this is exactly Week 1 L04 §6's signed/unsigned conversion — the rule that made `strlen(s) - 1` enormous. Here the same reinterpretation is deliberate and useful: the lower bound is *folded into* the upper one because negatives become large.

> The best answers note that the bug and the idiom are the same mechanism, differing only in whether
> the programmer intended it.

---

## Q3 (36) — Five Functions in Assembly

All verified: assembled, linked and run.

### (a) [6] `asm_sign`

```nasm
asm_sign:
        xor     eax, eax
        test    edi, edi
        setg    al              ; 1 if x > 0
        mov     edx, edi
        sar     edx, 31         ; -1 if x < 0, else 0
        or      eax, edx
        ret
```

*(Verified: sign(−9) = −1, sign(0) = 0, sign(9) = 1.)*

The two halves cannot both be non-zero, so `or` combines them safely. Accept any branchless equivalent; deduct 2 for a version using `jcc`.

### (b) [6] `asm_abs`

```nasm
asm_abs:
        mov     eax, edi
        sar     edi, 31         ; mask: all ones if negative
        xor     eax, edi
        sub     eax, edi
        ret
```

*(Verified: abs(−5) = 5, abs(5) = 5, **abs(INT_MIN) = −2147483648**.)*

**`INT_MIN` returns itself, and this is unavoidable:** $|{-2^{31}}| = 2^{31}$ is not representable in a signed 32-bit int. Every implementation must return a wrong value, widen the type, or signal an error.

> **Require the "unavoidable" reasoning.** "My code has a bug" is 3 of 6 — the code is correct and the
> type is too small. This is PS 1 Q3(c) recurring deliberately.

### (c) [6] `asm_sum_to`

```nasm
asm_sum_to:
        xor     eax, eax
        mov     rcx, 1
.loop:  cmp     rcx, rdi
        jg      .done
        add     rax, rcx
        inc     rcx
        jmp     .loop
.done:  ret
```

*(Verified: sum_to(100) = 5050, sum_to(0) = 0, sum_to(−5) = 0.)*

The top-test arrangement handles $n \le 0$ for free. Accept a bottom-tested loop **only if** it guards the entry; a student whose version returns 1 for $n = 0$ loses 2.

### (d) [6] `asm_count_bits`

```nasm
asm_count_bits:
        xor     eax, eax
.next:  test    edi, edi
        jz      .done
        mov     edx, edi
        and     edx, 1
        add     eax, edx
        shr     edi, 1          ; shr, NOT sar
        jmp     .next
.done:  ret
```

*(Verified: 0 → 0, 255 → 8, 0xffffffff → 32.)*

> **`shr` versus `sar` is the trap.** With `sar`, a value with the top bit set shifts in ones forever
> and the loop never terminates. Any student whose program hangs on `0xffffffff` made exactly this
> mistake — worth naming in class, since it is L08 §1 in practice.

### (e) [8] `asm_divmod10`

```nasm
asm_divmod10:                   ; int asm_divmod10(int x, int *rem)
        mov     eax, edi
        cdq                     ; sign-extend eax into edx:eax
        mov     ecx, 10
        idiv    ecx             ; eax = quotient, edx = remainder
        mov     [rsi], edx
        ret
```

*(Verified against C:)*

| x | q | r | C `x/10`, `x%10` |
|---:|---:|---:|---|
| 12345 | 1234 | 5 | 1234, 5 |
| −12345 | −1234 | −5 | −1234, −5 |
| 7 | 0 | 7 | 0, 7 |
| −7 | 0 | −7 | 0, −7 |
| 0 | 0 | 0 | 0, 0 |

**Quotient in `eax`, remainder in `edx`.** Note the remainder takes the sign of the dividend — C's truncation-toward-zero rule.

**`idiv` cannot take an immediate**, so 10 must be loaded into a register first. Students who write `idiv 10` will get an assembler error; that is a fine way to learn it.

### (f) [4]

**[2] Without the directive:**

```
/usr/bin/ld: warning: funcs.o: missing .note.GNU-stack section implies executable stack
$ readelf -lW driver | grep GNU_STACK
  GNU_STACK  ...  RWE  0x10
```

**With it:** `GNU_STACK ... RW`. *(Both verified.)*

**[2] What was removed:** the **non-executable stack** (NX / DEP). With `RWE`, data written to the stack can be executed as code — precisely the condition classic stack-smashing shellcode requires, and precisely the defence Week 9 studies.

**One missing line in one assembly file removes the protection from the entire linked program**, because the linker takes the most permissive setting across all inputs. GCC emits the section automatically for C; NASM does not.

---

## Q4 (18) — Deriving a Magic Number

### (a) [4]

$$2^{34} = 17\,179\,869\,184, \qquad \left\lfloor \frac{2^{34}}{10} \right\rfloor = 1\,717\,986\,918, \qquad +1 = 1\,717\,986\,919 = \texttt{0x66666667}$$

*(Verified.)*

### (b) [6]

**GCC's own answer, for comparison:**

```
<div3>:  movsxd rax,edi
         sar    edi,0x1f
         imul   rax,rax,0x55555556
         shr    rax,0x20
         sub    eax,edi
```

*(Verified.)* So $s = 32$ and $M = \texttt{0x55555556} = 1\,431\,655\,766$.

**Check:** $\lfloor 2^{32}/3 \rfloor + 1 = 1\,431\,655\,765 + 1 = 1\,431\,655\,766$ ✓ *(verified)*.

**Why $s = 32$ suffices.** Write $M = (2^s + r)/3$ with $0 < r \le 3$. Then

$$\frac{Mx}{2^s} = \frac{x}{3} + \frac{rx}{3\cdot 2^s}$$

The error term is below 1 — so the floors agree — provided $rx < 3 \cdot 2^{s}$. With $r = 2$ here and $x < 2^{31}$, that needs $2^{32} < 3 \cdot 2^{32}$, which holds comfortably.

**Exhaustive check accepted and encouraged**: over $x \in [-1000, 1000]$ plus $\pm 10^6$, `INT_MAX` and `INT_MIN`, the emulation matched C's `x / 3` with **zero mismatches** *(verified)*.

> Accept either the algebraic bound or a stated exhaustive verification. **Require the student to say
> which they did** — an unstated "it works" is 3 of 6.

### (c) [4]

```c
int div3(int x) {
    long long p = (long long)x * 1431655766LL;
    return (int)(p >> 32) - (x >> 31);
}
```

*(Verified against `x / 3` for $-10^6$, $-3$, $-1$, 0, 1, 3, $10^6$, `INT_MAX` — all match.)*

### (d) [4]

**[2] What they do.** `sar edi,0x1f` fills `edi` with the sign bit: **$-1$ if `x` is negative, 0 otherwise.** `sub eax,edi` then **adds 1** when `x` is negative and does nothing otherwise.

**[2] Why.** The multiply-and-shift computes $\lfloor x/3 \rfloor$, which for negatives rounds **toward $-\infty$**: $\lfloor -7/3 \rfloor = -3$. **C requires truncation toward zero**: $-7/3 = -2$. Adding 1 for negative dividends converts one to the other.

This is the same correction as `div8`'s bias of $+7$ (L08 §5), arrived at differently: bias before the shift, or correct after it.

---

## Q5 (12) — How Your `switch` Compiles

### (a) [3]

**Strategy: arithmetic — no table at all.**

```
mov    eax,0xffffffff
cmp    edi,0x6
ja     ret
lea    eax,[rdi+rdi*4+0x5]     ; 5x + 5
add    eax,eax                 ; 10x + 10
```

*(Verified.)* GCC recognised the progression $10x + 10$ and computed it directly.

### (b) [3]

**Strategy: a lookup table of results**, plus one indexed load.

```
0000 11000000 04000000 63000000 04000000
0010 f8ffffff fa000000 03000000
```

Decoded little-endian: **17, 4, 99, 4, −8, 250, 3** ✓ matches the source.

**The negative one:** `f8 ff ff ff` → bytes reversed → `0xFFFFFFF8`. As two's complement, $\texttt{0xFFFFFFF8} = 4294967288 - 4294967296 = \mathbf{-8}$.

> Require the two's-complement step to be shown, not just the answer.

### (c) [3]

```
lea    rdx,[rip+0x0]                ; table base
mov    edi,edi                      ; zero-extend index
movsxd rax,DWORD PTR [rdx+rdi*4]    ; 32-bit signed offset
add    rax,rdx                      ; + base
notrack jmp rax
```

*(Verified.)*

**Why offsets, not addresses:** two reasons, and both are wanted.

1. **Half the size** — 4 bytes per entry instead of 8.
2. **Position independence** — the table contains no absolute addresses, so it is correct wherever the loader places the code. Same argument as relative branches (L02 §5), and it is what makes PIE and ASLR possible.

### (d) [3]

**Strategy: a comparison chain**, partly branchless.

```
mov    eax,0x1
cmp    edi,0x1
je     ret
xor    eax,eax
cmp    edi,0x3e8       ; 1000
sete   al
add    eax,eax
```

*(Verified.)*

**Why a jump table is wrong here:** it would need 1001 entries to cover indices 0…1000 for two live cases — **about 4 KB of mostly-default entries**, which wastes memory and, more importantly, pollutes the cache. Two comparisons are cheaper in both.

---

## Mark Summary

| | |
|---|---:|
| Q1 | 16 |
| Q2 | 18 |
| Q3 | 36 |
| Q4 | 18 |
| Q5 | 12 |
| **Total** | **100** |

**Where the class loses marks, in order:**

1. **Q3(d)** — using `sar` instead of `shr` in the bit-count loop, which hangs on `0xffffffff`.
2. **Q2(a)** — getting CF and OF the wrong way round, or reversing the `cmp` operands.
3. **Q3(b)** — calling the `INT_MIN` result a bug in their code.
4. **Q1(a)** — the `cmpl` row, from mis-reversing AT&T operands.
5. **Q4(b)** — asserting the shift is large enough without argument or verification.

Items 1 and 2 are worth ten minutes at the start of Week 3, since the calling convention lecture assumes both.

---

*CS 201 · Week 2 · PS 2 Solutions · Instructor Only*

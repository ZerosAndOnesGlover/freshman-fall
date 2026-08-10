# CS 201 · Lab 2 — Solutions and TA Notes
## Instructor Only

---

> **Unmarked.** Five checkpoints. Everything below was run on the lab image (GCC 13.3.0, binutils
> 2.42, NASM 2.16.01, i5-8250U).

---

## Timing

| Part | Budget | Reality |
|---|---|---|
| 1 — addressing modes | 20 min | 15 min |
| 2 — division | 25 min | 25 min. 2.2 is the memorable one |
| 3 — four switches | 25 min | **Runs long.** Cut (d) if needed |
| 4 — AT&T vs Intel | 10 min | 5 min |
| 5 — writing assembly | 30 min | **Protect this.** It is the point of the lab** |

**If short of time, cut Part 3(d) and Part 4's second half.** Part 5 must not be cut — it is the first time they write assembly, and Week 3 assumes they have.

---

## Part 1 — Addressing Modes

Expected listing is in the handout and matches exactly. *(Verified.)*

**Answers:**

1. **`p[3]` is `+0xc` because 3 × `sizeof(int)` = 12.** C scales pointer arithmetic; assembly does not. There are no types at this level, only bytes.
2. **`lea` over `add`:** (i) it writes a destination without reading it first, so `a+b` needs no preliminary `mov`; (ii) it does not touch the flags, so it can be scheduled freely between a `cmp` and its branch. *(Also acceptable: it runs on the AGUs, which are often idle.)*
3. **The scale field.** `i*4` on `int*` is a 16-byte stride; scale encodes only 1, 2, 4, 8.
4. **`objdump -r modes.o`** shows `R_X86_64_PC32  g-0x4` *(verified)*. The `[rip+0x0]` is a placeholder; the **linker** patches in the RIP-relative displacement to `g` once the final layout is known. The `-0x4` accounts for `rip` pointing past the instruction — L02 §5's rule, appearing in the relocation arithmetic.

> Q4 is the one worth dwelling on. Students think the compiler emits final addresses. It does not, and
> Week 3's linking discussion is easier if they have seen a relocation record once.

**✅ CHECKPOINT 1** — listing plus four answers.

---

## Part 2 — Division

### 2.1

```
-17>>3 = -3   -17/8 = -2   (-17+7)>>3 = -2
```

*(Verified.)*

**`sar` floors** (rounds toward $-\infty$): $-17/8 = -2.125 \to -3$. **C's `/` truncates toward zero**: $\to -2$. Adding $2^k - 1 = 7$ before shifting converts one to the other, for negatives only — hence the `cmovns` selecting between biased and unbiased.

**`udiv8` is `shr eax,0x3`, two instructions.** *(Verified.)* No sign case exists, so no correction is needed. **The practical lesson: if a quantity cannot be negative, say so in the type.**

### 2.2

$\texttt{0x66666667} = 1717986919 = \lfloor 2^{34}/10 \rfloor + 1$. *(Verified — `python3 -c "print(0x66666667, (1<<34)//10+1)"` prints the same number twice.)*

**The constant is a fixed-point reciprocal of 10**; the `sar rax,0x22` (shift 34) is the corresponding binary point. Together they compute $\lfloor x/10 \rfloor$.

**Sign correction:** `sar edi,0x1f` yields $-1$ for negative `x`, 0 otherwise; `sub eax,edi` adds 1 in the negative case, converting floor to truncation.

### 2.3

**`cdq` sign-extends `eax` into `edx:eax`**, because `idiv` divides the full 64-bit `edx:eax` pair by its operand.

**Omit it** and `edx` holds whatever was there before, so the dividend is $\texttt{edx} \times 2^{32} + \texttt{eax}$ rather than the value you meant.

**What happens next depends on the leftover, and that is the point.** Computing `100 / 7` with a deliberately planted `edx` *(all verified)*:

| leftover in `edx` | result |
|---|---|
| 0 | **14** — correct, by luck |
| 1 | **613566770** — silently wrong, exit status 0 |
| 15, 16, 100 | **`Floating point exception (core dumped)`**, status 136 |

**It faults only when the quotient will not fit in 32 bits.** A small leftover gives a plausible wrong number and no diagnostic at all; a large one crashes.

> **Correct the intuition if it comes up.** Students — and, in a first draft of these notes, I —
> expect the missing `cdq` to reliably crash. It does not. **The silent-wrong-answer case is the
> dangerous one**, and it is why `cdq` is not optional even when testing seems to pass.
>
> Also worth naming: `#DE` is reported as **"Floating point exception"** even though this is integer
> division. Students will hunt for a floating-point bug that does not exist.

**✅ CHECKPOINT 2** — three listings plus the magic-constant explanation.

---

## Part 3 — Four Switches

| | Strategy |
|---|---|
| **(a)** progression | **Arithmetic.** `lea eax,[rdi+rdi*4+0x5]; add eax,eax` — computes $10x+10$. No table |
| **(b)** irregular | **Result lookup table** in `.rodata`, one indexed load |
| **(c)** statements | **Jump table** of 32-bit relative offsets, `notrack jmp rax` |
| **(d)** sparse | **Comparison chain**, second test made branchless with `sete` |

*(All four verified.)*

**Decoding (b)'s table:**

```
0000 11000000 04000000 63000000 04000000
0010 f8ffffff fa000000 03000000
```

Little-endian 32-bit: `0x11`=17, `0x04`=4, `0x63`=99, `0x04`=4, `0xFFFFFFF8`=**−8**, `0xFA`=250, `0x03`=3. Matches the source.

**The negative entry is the teaching point.** `f8 ff ff ff` reversed is `0xFFFFFFF8`; as two's complement that is $-8$. Students will read it as a huge positive number.

**The `ja` range check:** `cmp edi,0x6` then `ja` rejects both bounds at once, because a negative `x` is huge as unsigned. **All four strategies begin this way** — the bounds check is independent of the dispatch method.

> If time is short, do (a) and (b) properly and simply *show* (c) and (d). The contrast that matters is
> arithmetic-vs-table; jump tables recur in Week 5's branch prediction discussion anyway.

**✅ CHECKPOINT 3** — four strategies named, `.rodata` decoded.

---

## Part 4 — AT&T and Intel

```
Intel:  cmp esi,edi        AT&T:  cmp %edi,%esi
        mov eax,edi               mov %edi,%eax
        cmovge eax,esi            cmovge %esi,%eax
```

*(Verified — identical bytes, two renderings.)*

**Rule:** Intel is `op dest, src`; AT&T is `op src, dest`. Everything else — the `%`, the `$`, the size suffix — is cosmetic by comparison.

**Push the `.gdbinit` line.** Students who do not set it will spend the rest of the term mentally reversing operands between GDB and their notes, and will make errors under exam conditions.

**✅ CHECKPOINT 4** — both listings, rule stated.

---

## Part 5 — Writing Assembly

```
max(3,7)=7 max(-4,-9)=-4
abs(-5)=5 abs(5)=5 abs(INT_MIN)=-2147483648
```

*(Verified.)*

**`abs(INT_MIN)` being negative is correct**, and is PS 1 Q3(c) reappearing in code the student wrote. Make the connection explicitly.

**Common build failures:**

| Symptom | Cause |
|---|---|
| `undefined reference to asm_max` | Forgot `global asm_max`, or a typo in the label |
| Relocation error linking | Dropped `-no-pie`. Required for this simple form |
| Segfault on return | Wrote to a callee-saved register (`rbx`, `r12`–`r15`) without restoring it |
| Garbage result | Returned in the wrong register — it must be `rax`/`eax` |
| Assembler error on `idiv 10` | `idiv` takes no immediate; load the divisor into a register |

### 5.1 — the executable stack

```
/usr/bin/ld: warning: funcs.o: missing .note.GNU-stack section implies executable stack
```

```
without:  GNU_STACK  ...  RWE  0x10
with:     GNU_STACK  ...  RW   0x10
```

*(Both verified.)*

**One missing line in one `.asm` file makes the whole program's stack executable**, because the linker takes the most permissive setting across all inputs. That is the NX defence, gone — and Week 9's stack-smashing lab depends on students understanding that NX is what normally stops it.

**GCC emits this section automatically for C. NASM does not.** Anyone hand-writing assembly must add it.

> **This is the best thirty seconds in the lab.** A warning most students would scroll past turns out
> to have disabled a mitigation across the entire binary. Make them run `readelf` both ways rather
> than taking your word for it.

### 5.2 — `asm_sign`

```nasm
asm_sign:
        xor     eax, eax
        test    edi, edi
        setg    al
        mov     edx, edi
        sar     edx, 31
        or      eax, edx
        ret
```

*(Verified: −9 → −1, 0 → 0, 9 → 1.)* The two halves are never both non-zero, so `or` is safe.

**✅ CHECKPOINT 5** — `./driver` running, `readelf` both ways, and a working `asm_sign`.

---

## What Success Looks Like

By the end a student should, without notes:

1. Disassemble a named function and identify each addressing mode.
2. Recognise a fixed-point reciprocal where they expected a division.
3. Name which of the four `switch` strategies a listing is using.
4. Write, assemble, link and call a small function from C.
5. **Know that a linker warning can mean a security property was silently dropped.**

Item 4 is the prerequisite for Week 3. Item 5 is the one they will still remember in Week 9.

---

*CS 201 · Week 2 · Lab 2 Solutions · Instructor Only*

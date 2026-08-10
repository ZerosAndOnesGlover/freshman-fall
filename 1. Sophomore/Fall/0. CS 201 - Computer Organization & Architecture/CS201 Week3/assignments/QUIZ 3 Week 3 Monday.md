# CS 201 · Quiz 3
## Administered: Monday, Week 3 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 2** — registers and operands, arithmetic, flags and control flow.

**Instructions:** Closed notes. 10 minutes.

> **Unmarked, no weight.** Key below. Sit it closed-book first.

---

**Q1.** Give the four components of a general x86-64 memory operand, and the only legal values of the scale.

&nbsp;

&nbsp;

---

**Q2.** For `int *p` in `rdi`, write the operand for `p[5]`. What is the displacement in decimal, and why?

&nbsp;

&nbsp;

---

**Q3.** `lea rax,[rdi+rdi*4]` — what does it compute, and how many memory accesses does it perform?

&nbsp;

&nbsp;

---

**Q4.** Why is `x / 8` four instructions when `x >> 3` is one?

&nbsp;

&nbsp;

---

**Q5.** `cmp eax, ebx` is followed by `jb`. Which flag does `jb` read, and what does that tell you about the C types of the operands?

&nbsp;

&nbsp;

---

**Q6.** What does `cdq` do, and what goes wrong if you omit it before `idiv`?

&nbsp;

&nbsp;

---

**Q7.** `cmp edi, 0x6` followed by `ja` rejects `x < 0` as well as `x > 6`. Why?

&nbsp;

&nbsp;

---

<div style="page-break-after: always;"></div>

---

## Answer Key — Mark Your Own

**Q1.** **`[base + index × scale + displacement]`.** Scale ∈ **{1, 2, 4, 8}** only — the sizes of `char`, `short`, `int`/`float`, and `long`/pointer/`double`.

---

**Q2.** **`DWORD PTR [rdi+0x14]`** — displacement **20**, because $5 \times \texttt{sizeof(int)} = 5 \times 4$.

**In assembly there are no types.** C scales pointer arithmetic for you; here it is folded into the displacement.

---

**Q3.** **`rax = rdi × 5`.** **Zero memory accesses.**

`lea` computes the address expression and stores the *value*. The brackets are the syntax of an address, not a load. It is the compiler's general three-input adder with a free shift.

---

**Q4.** **`/` truncates toward zero; `sar` rounds toward $-\infty$.**

They agree for non-negatives and differ for negatives: $-17 \gg 3 = -3$, but $-17/8 = -2$. So `/8` must bias the dividend by $2^3-1 = 7$ before shifting, and select between biased and unbiased with `test`/`cmovns`.

*Use `unsigned` where you can — `unsigned x / 8` is a single `shr`.*

---

**Q5.** **`jb` reads CF** — the carry flag, which is **unsigned** overflow.

So the operands were **unsigned** in the C source. A signed comparison would have compiled to `jl`, which reads SF ≠ OF. Different flags entirely, for source that looks identical.

---

**Q6.** **`cdq` sign-extends `eax` into `edx:eax`**, because `idiv` divides that full 64-bit pair.

**Omit it and the dividend is $\texttt{edx} \times 2^{32} + \texttt{eax}$**, using whatever was left in `edx`. *Measured for `100/7`:* leftover 0 gives 14 by luck, leftover 1 gives **613566770 with no error at all**, and 15 or more crashes with `Floating point exception`.

**It faults only when the quotient will not fit in 32 bits.** The silent wrong answer is the dangerous case.

---

**Q7.** **`ja` is an *unsigned* comparison.** A negative `x` reinterpreted as unsigned is at least $2^{31}$, which is greater than 6, so the branch is taken.

**One comparison enforces both bounds**, because the lower bound folds into the upper one. This is Week 1's signed/unsigned conversion — the same mechanism as the `strlen(s)-1` bug, used deliberately.

---

### What to Do With Your Score

| If you missed | Reread |
|---|---|
| Q1, Q2, Q3 | L07 §3–§5 |
| Q4, Q6 | L08 §3 and §5 |
| Q5, Q7 | L09 §3 and §4 |

**Q3 and Q6 are the ones that recur.** `lea` appears in nearly every listing from here on, and `cdq` is on PS 2 and Midterm 1.

---

*CS 201 · Week 3 · Quiz 3 · covers Week 2 · ungraded*

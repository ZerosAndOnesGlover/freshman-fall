# CS 201 · Computer Organization & Architecture
## Week 2 · Lecture 2 of 3
### Arithmetic, and What the Compiler Does Instead of Dividing

---

**Reading:** CS:APP §3.5 · **Previous:** L07, registers and operands

---

## 1. The Ordinary Instructions

| Instruction | Effect | Flags |
|---|---|---|
| `add dst, src` | `dst += src` | all |
| `sub dst, src` | `dst -= src` | all |
| `imul dst, src` | signed `dst *= src` | CF, OF |
| `neg dst` | `dst = -dst` | all |
| `inc` / `dec` | ±1 | all **except CF** |
| `and` / `or` / `xor` / `not` | bitwise | CF = OF = 0 |
| `shl` / `sal` | left shift | |
| `shr` | **logical** right shift — fills 0 | |
| `sar` | **arithmetic** right shift — fills sign | |
| `lea dst, [expr]` | `dst = expr` | **none** |

**Two of these are worth pausing on.**

**`shr` versus `sar`** is the signed/unsigned distinction in hardware. `shr` fills with zeros; `sar` replicates the sign bit. C picks between them from the *type* of the operand, which is why `>>` on a signed negative is not the same instruction as `>>` on an unsigned.

**`inc` does not set CF.** It is one byte shorter than `add reg,1`, but a loop that uses `inc` and then relies on the carry flag will read a stale value. This is a real bug class and the reason many compilers prefer `add` despite the extra byte.

---

## 2. Multiplication Has Three Forms

```
imul esi                 ; one operand:   edx:eax = eax * esi  (full 64-bit result)
imul eax, esi            ; two operands:  eax = eax * esi      (low half only)
imul eax, esi, 10        ; three operands: eax = esi * 10
```

**The one-operand form produces a double-width result** split across `edx:eax`, which is how you multiply two 32-bit numbers and keep all 64 bits. The two- and three-operand forms keep only the low half — which is exactly what C's `*` means, since the result type equals the operand type.

**`mul` (unsigned) and `imul` (signed) differ only in the high half.** The low 32 bits of a 32×32 product are identical regardless of signedness — a consequence of two's complement that ECE 110's multiplier already relied on. That is why C needs no separate unsigned multiply for its `*`.

---

## 3. Division Is the Expensive One

```
cdq                      ; sign-extend eax into edx:eax
idiv esi                 ; eax = edx:eax / esi ,  edx = remainder
```

```c
int divvar(int a, int b) { return a / b; }
```

```
<divvar>:  mov    eax,edi
           cdq
           idiv   esi
           ret
```

*(Verified.)*

**`idiv` divides the 64-bit value in `edx:eax`, not just `eax`.** So the dividend must be sign-extended first — that is what `cdq` does, filling `edx` with copies of `eax`'s sign bit.

**Forgetting `cdq` is the most common bug in hand-written division**, and its failure mode is worse than a crash. With a leftover value in `edx`, the dividend becomes $\texttt{edx} \times 2^{32} + \texttt{eax}$. Computing `100 / 7` with a planted `edx` *(verified)*:

| leftover `edx` | result |
|---|---|
| 0 | 14 — correct, by luck |
| 1 | **613566770 — silently wrong, no error** |
| 15 or more | `Floating point exception (core dumped)` |

**It faults only when the quotient will not fit in 32 bits.** Otherwise you get a plausible number and no diagnostic. *(And note the exception's name: integer division raises "floating point exception" too.)*

**`idiv` is slow.** On this microarchitecture it takes tens of cycles and is not pipelined, against one cycle for `add`. That difference is why the rest of this lecture exists.

---

## 4. Division by a Constant: the Compiler Does Not Divide

```c
int div10(int x) { return x / 10; }
```

You would expect `idiv`. You get this:

```
<div10>:  movsxd rax,edi
          sar    edi,0x1f
          imul   rax,rax,0x66666667
          sar    rax,0x22
          sub    eax,edi
          ret
```

*(Verified.)* **No division instruction anywhere.** A multiply, two shifts and a subtract.

**What it computes.** Dividing by 10 is multiplying by $1/10$. You cannot hold $1/10$ in an integer — but you can hold $\lfloor 2^{34}/10 \rfloor + 1$ and shift the product right by 34:

$$\texttt{0x66666667} = 1\,717\,986\,919 = \left\lfloor \frac{2^{34}}{10} \right\rfloor + 1$$

*(Verified — the magic constant is exactly that.)*

So `imul rax,rax,0x66666667` followed by `sar rax,0x22` (shift right 34) computes $\lfloor x/10 \rfloor$ for positives.

**The `sar edi,0x1f` and `sub eax,edi` are the sign correction.** `sar edi,31` is $-1$ for negative `x` and 0 otherwise; subtracting it adds 1 for negatives. That converts floor division into **truncation toward zero**, which is what C requires.

Checked against C's `x/10` for $-12345$, $-100$, $-7$, $-1$, 0, 1, 7, 100, 12345 and `INT_MAX`: **every one matches.** *(Verified.)*

> **The magic number is not magic.** It is a fixed-point reciprocal, and the shift amount is chosen so
> the error stays below one unit across the whole 32-bit range. Deriving the bound is a genuinely
> nice exercise and is PS 2 Q4.

**Modulo is the same trick plus a multiply-back:**

```
<mod10>:  ... imul rax,rax,0x66666667 ; sar rax,0x22 ; sub eax,edx
          lea    edx,[rax+rax*4]      ; q*5
          add    edx,edx              ; q*10
          sub    eax,edx              ; x - q*10
```

*(Verified.)* $x \bmod 10 = x - 10\lfloor x/10 \rfloor$, with the multiply by 10 done as `lea` + `add`. **Still no division.**

---

## 5. Why `x / 8` Is Not `x >> 3`

The Week 1 reading guide asked this. Here is the answer in instructions:

```c
int div8(int x) { return x / 8; }
int shr3(int x) { return x >> 3; }
```

```
<div8>:  test   edi,edi
         lea    eax,[rdi+0x7]
         cmovns eax,edi
         sar    eax,0x3
         ret

<shr3>:  mov    eax,edi
         sar    eax,0x3
         ret
```

*(Verified.)*

**`>>` is one shift. `/8` is four instructions.**

The difference is negative numbers. `sar` rounds **toward negative infinity**: $-17 \gg 3 = -3$ (since $-17/8 = -2.125$, floored to $-3$). But C's `/` must round **toward zero**: $-17/8 = -2$.

**The fix is to bias the dividend before shifting.** Adding $2^3 - 1 = 7$ to a negative value before shifting turns floor into truncation. So:

- `lea eax,[rdi+0x7]` — the biased version
- `test edi,edi` / `cmovns eax,edi` — use the unbiased version instead if `x` is non-negative
- `sar eax,0x3` — shift either way

**Two ways to read this.** Either "the compiler is wasteful", or "`>>` and `/` mean different things and you should use the one you mean." The second is right. **If you know the value is non-negative, say so** — make it `unsigned`, and:

```c
unsigned udiv8(unsigned x) { return x / 8; }   ->  shr eax,0x3
```

One instruction, because unsigned division has no sign case.

---

## 6. Branchless Conditionals

Two instruction families let you compute conditionally without branching.

**`setcc` writes a 0 or 1 byte:**

```c
int cmpset(int a, int b) { return a < b; }
```

```
<cmpset>:  xor    eax,eax
           cmp    edi,esi
           setl   al
           ret
```

*(Verified.)* `xor eax,eax` first because `setl` writes only `al` — the other 24 bits must be cleared separately. **This is L03's zeroing rule doing real work**: `xor eax,eax` clears all of `rax` in two bytes.

**`cmovcc` moves conditionally:**

```c
int maxi(int a, int b) { return a > b ? a : b; }
```

```
<maxi>:  cmp    esi,edi
         mov    eax,edi
         cmovge eax,esi
         ret
```

*(Verified.)* **No branch.** Both candidate values are computed, and the flags select one.

> **Why avoid branches?** A mispredicted branch costs 15–20 cycles (Week 5). A `cmov` costs one and
> never mispredicts. But `cmov` **always evaluates both sides**, so it is a loss when one side is
> expensive or would fault — you cannot `cmov` a pointer dereference that might be null. The compiler
> weighs this; when it guesses wrong, `__builtin_expect` or a rewrite is your lever.

---

## 7. What to Take Away

1. **`shr` is unsigned, `sar` is signed.** C chooses by type.
2. **`imul` has three forms**; only the one-operand form keeps the full double-width product.
3. **`idiv` needs `cdq` first** and divides `edx:eax`. Forgetting it faults.
4. **Division by a constant becomes a multiply by a fixed-point reciprocal.** `0x66666667` is $\lfloor 2^{34}/10\rfloor + 1$.
5. **`x / 8` is four instructions and `x >> 3` is one**, because `/` truncates toward zero and `sar` floors. Use `unsigned` when you can.
6. **`setcc` and `cmov` compute conditionally without branching**, at the cost of evaluating both sides.

---

## Exercises

1. Write the `cdq; idiv` sequence to compute `a % b`, and say which register holds the answer.
2. What happens if you run `idiv esi` without `cdq` when `eax` is positive and `edx` happens to hold `0xFFFFFFFF`? Be specific about the failure.
3. Derive the magic constant for division by 3 the way §4 derives it for 10. Pick a shift, compute the multiplier, and test it on $\pm 1$, $\pm 2$, $\pm 3$ and `INT_MAX`.
4. `div8` biases by 7 before shifting. Show that the bias for division by $2^k$ must be $2^k - 1$, and verify for $x = -17$, $k = 3$.
5. `maxi` compiles to `cmov`. Write a C function returning the max of two values where the compiler *cannot* use `cmov`, and explain what blocks it.

---

*Next: L09 — the flags, the conditional jumps, and how a `switch` really compiles.*

# CS 201 · Computer Organization & Architecture
## Week 2 · Lecture 1 of 3
### Registers, Operands, and the Two Syntaxes

---

**Reading:** CS:APP §3.1–3.4 · **Previous:** L06, floating-point non-associativity

---

## 1. The State You Are Programming

L03 listed the sixteen general-purpose registers. This week you use them, so here they are again with the roles that actually constrain you:

| Register | Role | Preserved across a call? |
|---|---|---|
| `rax` | Return value; implicit operand of `mul`, `div` | No — caller-saved |
| `rdi` `rsi` `rdx` `rcx` `r8` `r9` | Arguments 1–6, in that order | No |
| `r10` `r11` | Scratch | No |
| `rbx` `rbp` `r12`–`r15` | General use | **Yes — callee-saved** |
| `rsp` | Stack pointer | **Yes**, by definition |
| `rip` | Instruction pointer | Not writable directly |

**"Callee-saved" means: if you write to it, you must restore it before returning.** Week 3 makes the whole convention precise. For this week the practical rule is: **use `rax`, `rdi`, `rsi`, `rdx`, `rcx`, `r8`–`r11` freely; touch `rbx` or `r12`–`r15` only if you push and pop them.**

**Four widths, one register.** `rax` / `eax` / `ax` / `al`. And the rule from L03 that catches everybody: **a 32-bit write zeroes the upper 32 bits; a 16- or 8-bit write does not.**

You have already seen the assembler rely on this. In Lab 0 you wrote `mov rax, 1` and NASM emitted:

```
401000:  mov    eax,0x1
```

*(Verified.)* One byte shorter, identical result.

---

## 2. Two Syntaxes for One Machine

This is the single most common source of confusion in Week 2, so deal with it first.

The same function, disassembled twice from the same object file:

```
--- Intel (objdump -M intel) ---        --- AT&T (objdump, default) ---
  cmp    esi,edi                          cmp    %edi,%esi
  mov    eax,edi                          mov    %edi,%eax
  cmovge eax,esi                          cmovge %esi,%eax
```

*(Verified — same bytes, two renderings.)*

| | Intel | AT&T |
|---|---|---|
| Operand order | `op dest, src` | `op src, dest` |
| Registers | `rax` | `%rax` |
| Immediates | `42` | `$42` |
| Memory | `[rbx+rcx*4+8]` | `8(%rbx,%rcx,4)` |
| Size | from the operand, or `DWORD PTR` | suffix: `movl`, `movq` |
| Used by | NASM, Intel manuals, MSVC | GCC, GDB, GNU as |

**The operand order is reversed.** `mov %edi,%eax` copies `edi` into `eax`; `mov eax,edi` copies `edi` into `eax` as well. Same direction, opposite writing. **Read the syntax marker before you read the instruction.**

> **This course writes Intel** and passes `-M intel` to `objdump`. Set it permanently in GDB too:
>
> ```bash
> echo 'set disassembly-flavor intel' >> ~/.gdbinit
> ```
>
> **You must still be able to read AT&T.** It is what GCC emits, what most Linux documentation shows,
> and what you will meet in any kernel or libc source. Being fluent in one and able to decode the
> other is the realistic goal.

---

## 3. `mov` Is Not One Instruction

`mov` is the most frequent instruction in any program, and it is really a family. What varies is where the operands live.

```c
int reg(int a, int b) { return a + b; }        /* register operands */
int imm(int a)        { return a + 42; }       /* immediate         */
int direct(void)      { return g; }            /* global            */
int indirect(int *p)  { return *p; }           /* pointer           */
int base_off(int *p)  { return p[3]; }         /* base + offset     */
int scaled(int *p, long i) { return p[i]; }    /* base + index*scale*/
```

Compiled at `-O1`:

```
<reg>:       lea    eax,[rdi+rsi*1]
<imm>:       lea    eax,[rdi+0x2a]
<direct>:    mov    eax,DWORD PTR [rip+0x0]
<indirect>:  mov    eax,DWORD PTR [rdi]
<base_off>:  mov    eax,DWORD PTR [rdi+0xc]
<scaled>:    mov    eax,DWORD PTR [rdi+rsi*4]
```

*(All verified.)*

**Read `base_off` carefully.** `p[3]` on an `int*` became `[rdi+0xc]` — offset **12**, not 3. The scaling by `sizeof(int)` that C does for you is arithmetic the compiler folded into the address. **In assembly, pointer arithmetic is byte arithmetic. There are no types.**

**And `scaled`** shows the machine doing that scaling at run time: `[rdi+rsi*4]`, base plus index times four.

---

## 4. The General Addressing Mode

Every memory operand in x86-64 is one form:

$$\texttt{[base + index} \times \texttt{scale + displacement]}$$

| Component | May be | Notes |
|---|---|---|
| **base** | any 64-bit register | optional |
| **index** | any 64-bit register except `rsp` | optional |
| **scale** | 1, 2, 4 or 8 | only these four |
| **displacement** | 8- or 32-bit signed constant | optional |

**Scale is limited to 1, 2, 4, 8 because those are the sizes of `char`, `short`, `int`/`float` and `long`/pointer/`double`.** The addressing mode was designed around array indexing, and it shows.

When an index needs a different scale, the compiler must compute it separately:

```c
int full(int *p, long i) { return p[i*4 + 3]; }
```

```
<full>:  shl    rsi,0x4                        ; i * 16 — scale 16 is not available
         mov    eax,DWORD PTR [rsi+rdi*1+0xc]
```

*(Verified.)* `i*4` elements of 4 bytes is a stride of 16, which no scale field can encode, so it becomes an explicit shift. **Watching where the compiler stops being able to fold arithmetic into an address is a good habit** — it is often where a loop's cost is hiding.

---

## 5. `lea` — The Adder That Pretends to Be an Address

Notice that `reg` and `imm` above used **`lea`**, not `add`. `lea` — *load effective address* — computes the address expression and stores the **value**, without accessing memory at all.

So it is a three-input adder with a free shift:

```c
int lea_demo(int a, int b) { return a*5 + b; }
```

```
<lea_demo>:  lea    eax,[rdi+rdi*4]     ; a + a*4 = a*5
             add    eax,esi
```

*(Verified.)* Multiplication by 5, with no multiply instruction.

**Why compilers love it:**

- It reads **three** operands and a constant, where `add` reads two.
- It writes a destination **without touching the flags** — so it can be scheduled between a `cmp` and its `jcc`.
- It runs on the address-generation units, which are often idle while the ALUs are busy.

> **`lea` does not access memory.** Students consistently assume the brackets mean a load. They do
> not. The brackets are the *syntax* of an address expression; `lea` computes it and stops. You saw
> this in Week 0 with `lea rdx,[rdx+rax*2+0x1]` summing two loop iterations at once.

---

## 6. Reading Compiler Output Without Drowning

The listings you will meet are longer than these. Three habits:

**Find the shape first.** Locate `ret`, then the backward branches — those are loops. Ignore the bodies until you know the control flow.

**Track the arguments.** They arrive in `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`. At `-O0` they are spilled to the stack immediately; at `-O2` they stay in registers. Following argument 1 through the function is usually enough to orient yourself.

**Ignore the noise.** `endbr64` is a control-flow-integrity landing pad (Week 9). `nop WORD PTR [rax+rax*1+0x0]` is multi-byte padding to align the next branch target. Neither does anything to your data.

**Use the right optimisation level for the question.** `-O0` maps almost line-for-line to your C and is how you learn what an instruction does. `-O2` is what actually runs and is how you learn what the machine does. **They answer different questions; do not read one expecting the other.**

---

## 7. What to Take Away

1. **Sixteen registers, six of them argument slots, four callee-saved.** 32-bit writes zero the top half.
2. **Intel and AT&T reverse their operands.** Check which you are reading, every time.
3. **`[base + index*scale + disp]`** is the only memory operand form, and scale is 1/2/4/8.
4. **Pointer arithmetic is byte arithmetic.** `p[3]` on `int*` is `+12`.
5. **`lea` computes addresses and does not access memory** — it is the compiler's general adder.
6. **`-O0` to learn instructions, `-O2` to learn the machine.**

---

## Exercises

1. `mov ax, 5` and `mov eax, 5` differ in effect on `rax`. Write the two-instruction sequence that would let you set only the low 16 bits *and* be sure of the upper 48.
2. Rewrite `[rbx + rcx*4 + 8]` in AT&T syntax, and `16(%rax,%rdx,8)` in Intel.
3. `p[i*4 + 3]` needed an explicit `shl`. Give a different C expression that also cannot be folded into one addressing mode, and say which component runs out.
4. Give three distinct `lea` instructions that multiply a register by 3, 9 and 10 respectively. Only one of them needs a second instruction — which, and why?
5. Why is `rsp` forbidden as the *index* register but allowed as the *base*? *(Hint: think about the encoding, not the semantics.)*

---

*Next: L08 — the arithmetic instructions, and what the compiler does instead of dividing.*

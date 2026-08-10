# CS 201 · Week 2 · Lab 2
## Reading Compiler Output on Increasingly Complex C

---

**When:** Tuesday 15:00–16:50, BH 210 · **Assessment:** unmarked, checked off by the TA
**You need:** `gcc`, `objdump`, `nasm`, `gdb` — all from Lab 0.

---

## What This Lab Is For

Lecture told you what the instructions mean. **This lab is about reading them at speed**, on code you did not write, until the shape of a listing is something you see rather than decode.

The five parts get harder. Part 5 is the one that matters: you write assembly and call it from C.

---

## Part 1 — Every Addressing Mode, in One File (20 min)

```c
int g;
int reg(int a, int b)         { return a + b; }
int imm(int a)                { return a + 42; }
int direct(void)              { return g; }
int indirect(int *p)          { return *p; }
int base_off(int *p)          { return p[3]; }
int scaled(int *p, long i)    { return p[i]; }
int full(int *p, long i)      { return p[i*4 + 3]; }
int lea_demo(int a, int b)    { return a*5 + b; }
```

```bash
gcc -O1 -c -o modes.o modes.c
objdump -d --no-show-raw-insn -M intel modes.o
```

You should get:

```
<reg>:       lea    eax,[rdi+rsi*1]
<imm>:       lea    eax,[rdi+0x2a]
<direct>:    mov    eax,DWORD PTR [rip+0x0]
<indirect>:  mov    eax,DWORD PTR [rdi]
<base_off>:  mov    eax,DWORD PTR [rdi+0xc]
<scaled>:    mov    eax,DWORD PTR [rdi+rsi*4]
<full>:      shl    rsi,0x4
             mov    eax,DWORD PTR [rsi+rdi*1+0xc]
<lea_demo>:  lea    eax,[rdi+rdi*4]
             add    eax,esi
```

*(Verified.)*

**Answer in your notes:**

1. `base_off` returns `p[3]` but the offset is `0xc`. Why 12?
2. `reg` adds two registers and uses `lea`, not `add`. Give two reasons a compiler prefers `lea` here.
3. `full` needed an explicit `shl` before the load. Which part of the addressing mode ran out?
4. `direct` uses `[rip+0x0]` with an offset of zero. Run `objdump -r modes.o` and explain what fills it in.

**✅ CHECKPOINT 1** — the listing and your four answers.

---

## Part 2 — What the Compiler Does Instead of Dividing (25 min)

```c
int div8(int x)          { return x / 8; }
int shr3(int x)          { return x >> 3; }
unsigned udiv8(unsigned x){ return x / 8; }
int div10(int x)         { return x / 10; }
int mod10(int x)         { return x % 10; }
int divvar(int a, int b) { return a / b; }
```

```bash
gcc -O2 -c -o arith.o arith.c
objdump -d --no-show-raw-insn -M intel arith.o
```

### 2.1 One shift, or four instructions

`shr3` is two instructions; `div8` is four; `udiv8` is two. *(Verified.)*

Run this and explain the middle column:

```c
int x = -17;
printf("%d %d %d\n", x >> 3, x / 8, (x + 7) >> 3);
```

Output: `-3 -2 -2` *(verified)*. **Why does `/` need the bias and `>>` not?**

### 2.2 Find the division that is not there

`div10` contains **no** division instruction. Find `imul rax,rax,0x66666667` and `sar rax,0x22`.

```bash
python3 -c "print(0x66666667, (1<<34)//10 + 1)"
```

Both print `1717986919`. *(Verified.)* **State what the constant is and what the shift of 34 is for.**

Then find the two instructions doing the sign correction, and say what they add and when.

### 2.3 The only real division

`divvar` divides by a variable, so it must use `idiv`:

```
mov    eax,edi
cdq
idiv   esi
```

**What does `cdq` do, and what happens if you omit it?** Do not guess — you will find out in Part 5.

**✅ CHECKPOINT 2** — the three division listings and your explanation of the magic constant.

---

## Part 3 — Four Ways to Compile a `switch` (25 min)

Compile each and identify the strategy.

**(a) Arithmetic progression:**

```c
int sw(int x){ switch(x){ case 0:return 10; case 1:return 20; case 2:return 30;
    case 3:return 40; case 4:return 50; case 5:return 60; case 6:return 70;
    default:return -1; } }
```

**(b) Irregular values** — change the returns to 17, 4, 99, 4, −8, 250, 3.

**(c) Statements, not values:**

```c
extern void a(void),b(void),c(void),d(void),e(void),f(void),g(void);
void dispatch(int x){ switch(x){ case 0:a();break; /* … through */ case 6:g();break; } }
```

**(d) Sparse:**

```c
int sparse(int x){ switch(x){ case 1:return 1; case 1000:return 2; default:return 0; } }
```

For (b), dump the data section and decode it by hand:

```bash
objdump -s -j .rodata sw2.o
```

```
0000 11000000 04000000 63000000 04000000
0010 f8ffffff fa000000 03000000
```

*(Verified.)* **Seven little-endian 32-bit values. Read them off and check them against your source.**

**All four** begin with `cmp edi,0x6` (or similar) and `ja`. **Explain how one unsigned comparison checks both bounds.**

**✅ CHECKPOINT 3** — name the strategy for each of (a)–(d), and decode the `.rodata` table.

---

## Part 4 — AT&T and Intel (10 min)

```bash
objdump -d --no-show-raw-insn -M intel arith.o | sed -n '/<maxi>/,/ret/p'
objdump -d --no-show-raw-insn        arith.o | sed -n '/<maxi>/,/ret/p'
```

```
Intel:  cmp esi,edi      AT&T:  cmp %edi,%esi
        mov eax,edi             mov %edi,%eax
        cmovge eax,esi          cmovge %esi,%eax
```

*(Verified — identical bytes.)*

**Set GDB to Intel permanently** so you stop tripping over this:

```bash
echo 'set disassembly-flavor intel' >> ~/.gdbinit
```

**✅ CHECKPOINT 4** — both listings, and state the operand-order rule for each.

---

## Part 5 — Write Assembly and Call It From C (30 min)

The real exercise. Create `funcs.asm`:

```nasm
        global  asm_max, asm_abs
        section .text

; int asm_max(int a, int b)     args in edi, esi ; return in eax
asm_max:
        mov     eax, edi
        cmp     esi, eax
        cmovg   eax, esi
        ret

; int asm_abs(int x)            arg in edi ; return in eax
asm_abs:
        mov     eax, edi
        sar     edi, 31
        xor     eax, edi
        sub     eax, edi
        ret

        section .note.GNU-stack noalloc noexec nowrite progbits
```

and `driver.c`:

```c
#include <stdio.h>
#include <limits.h>
int asm_max(int, int);
int asm_abs(int);
int main(void) {
    printf("max(3,7)=%d max(-4,-9)=%d\n", asm_max(3,7), asm_max(-4,-9));
    printf("abs(-5)=%d abs(5)=%d abs(INT_MIN)=%d\n",
           asm_abs(-5), asm_abs(5), asm_abs(INT_MIN));
    return 0;
}
```

```bash
nasm -f elf64 -o funcs.o funcs.asm
gcc -O2 -no-pie -o driver driver.c funcs.o
./driver
```

```
max(3,7)=7 max(-4,-9)=-4
abs(-5)=5 abs(5)=5 abs(INT_MIN)=-2147483648
```

*(Verified.)*

**`abs(INT_MIN)` is negative, and that is correct** — it is PS 1 Q3(c) appearing in your own assembly. $|{\texttt{INT\_MIN}}|$ has no 32-bit representation.

### 5.1 The linker warning you must not ignore

**Omit the `.note.GNU-stack` line** and rebuild:

```
/usr/bin/ld: warning: funcs.o: missing .note.GNU-stack section implies executable stack
```

*(Verified.)* Check what it did:

```bash
readelf -lW driver | grep GNU_STACK
```

With the section: `GNU_STACK ... RW`. Without it: `RWE` — **an executable stack**, which is exactly the defence Week 9 spends a lecture on. **A missing one-line directive in your assembly file silently disabled a security mitigation for the entire program.**

Always include it. NASM does not add it for you; GCC does for C.

### 5.2 Write your own

Add `asm_sign(int x)` returning −1, 0 or +1, using `setg` and `sar`. Test it on −9, 0 and 9. *(A working version is in the PS 2 solutions if you get stuck — try first.)*

**✅ CHECKPOINT 5** — `./driver` running, the `readelf` output both ways, and your `asm_sign`.

---

## Before You Leave

| Skill | Command |
|---|---|
| Disassemble one function | `objdump -d -M intel prog.o \| sed -n '/<fn>:/,/^$/p'` |
| See a data table | `objdump -s -j .rodata prog.o` |
| See what the linker must fill in | `objdump -r prog.o` |
| Assemble and link NASM with C | `nasm -f elf64 -o f.o f.asm && gcc -no-pie -o p main.c f.o` |
| Check the stack is non-executable | `readelf -lW prog \| grep GNU_STACK` |

**The habit this lab builds:** you can now answer "what does this compile to?" by looking, in under a minute, for any function you can write.

---

*CS 201 · Week 2 · Lab 2*

# CS 201 · Computer Organization & Architecture
## Week 3 · Lecture 2 of 3
### The System V AMD64 Calling Convention

*“The nice thing about standards is that you have so many to choose from.”* — Andrew S. Tanenbaum, *Computer Networks*, 2nd ed. (1988)

---

**Reading:** CS:APP §3.7.3–3.7.5 · **Previous:** L10, `call`, `ret` and the frame

**Coursework:** 📝 **PS 3** released today, due Fri of Week 4 17:00 · 📝 **PS 2** due Fri this week 17:00 · 📊 **Quiz 4** Mon of Week 4 · 🔬 **Lab 3** Tue of Week 4 15:00–16:50 · 📘 **Midterm 1** Mon of Week 5 18:00–19:15

---

## 1. Why There Is a Convention At All

The hardware has no opinion about where arguments go. `call` pushes an address and jumps; everything else is agreement.

**The agreement is the ABI** — the Application Binary Interface. It is what allows a function compiled in 2015 by Clang to be called from a function compiled today by GCC, linked against a libc built by neither.

**Linux and macOS use System V AMD64. Windows uses a different one.** Same hardware, same instruction set, incompatible conventions — which is why cross-platform code cannot simply be relinked.

---

## 2. Arguments

**The first six integer or pointer arguments, in order:**

| # | Register |
|---|---|
| 1 | `rdi` |
| 2 | `rsi` |
| 3 | `rdx` |
| 4 | `rcx` |
| 5 | `r8` |
| 6 | `r9` |

**The first eight floating-point arguments** go in `xmm0`–`xmm7`, counted separately. So `f(int, double, int, double)` puts the ints in `rdi`, `rsi` and the doubles in `xmm0`, `xmm1` — **the two sequences do not interleave.**

**The return value** is in `rax` (or `xmm0` for floating point). A 128-bit return uses `rax:rdx`.

**For variadic functions**, `al` must hold the number of vector registers used. This is why `printf` is called with `mov eax,0x1` before it when there is one `double` argument — you have seen that instruction and it is not noise.

---

## 3. Arguments Beyond Six Go on the Stack

```c
int caller(void) { return many(1,2,3,4,5,6,7,8,9); }
```

```
<caller>:
   4:  sub    rsp,0x10
   8:  push   0x9
   a:  push   0x8
   c:  push   0x7
   e:  mov    r9d,0x6
  14:  mov    r8d,0x5
  1a:  mov    ecx,0x4
  1f:  mov    edx,0x3
  24:  mov    esi,0x2
  29:  mov    edi,0x1
  2e:  call   many
  33:  add    rsp,0x28
  37:  ret
```

*(Verified.)*

**Three things to read off this.**

**Arguments 7, 8, 9 are pushed in reverse order** — 9 first, then 8, then 7. Since the stack grows down, argument 7 ends up at the *lowest* address, so the callee finds them in ascending order at `[rsp+8]`, `[rsp+16]`, `[rsp+24]` after its own return address.

**The caller cleans up.** `add rsp,0x28` after the call removes all of it — 0x10 of padding plus three 8-byte arguments = 0x28. **The callee does not pop its stack arguments**, which is what makes variadic functions like `printf` possible: only the caller knows how many there were.

**Each stack argument occupies 8 bytes** even though these are 32-bit `int`s.

> **The `sub rsp,0x10` before the pushes is alignment**, not storage. Three pushes move `rsp` by 24,
> which would leave it misaligned at the `call`; the extra 16 corrects it. L12 §2 does the arithmetic.

---

## 4. Caller-Saved and Callee-Saved

This is the part people get wrong, so state it precisely.

| Registers | Class | Meaning |
|---|---|---|
| `rax` `rcx` `rdx` `rsi` `rdi` `r8`–`r11` | **Caller-saved** *(volatile)* | A callee may destroy these. If you need a value across a call, **you** save it |
| `rbx` `rbp` `r12` `r13` `r14` `r15` | **Callee-saved** *(non-volatile)* | A callee must leave these as it found them. Push and pop if you use them |
| `rsp` | Special | Must be restored exactly |

**The names describe whose job it is, not who does the pushing.**

- *Caller-saved*: the **caller** must save it, **if** it cares. Most of the time it does not, which is why these are cheap.
- *Callee-saved*: the **callee** must save it, **if** it uses it. A function that never touches `rbx` pushes nothing.

**Why have both?** A convention with only callee-saved registers forces every function to preserve everything, including registers the caller had nothing in. A convention with only caller-saved registers forces every call site to spill everything live. **Splitting the file lets the compiler put short-lived values in volatile registers and long-lived ones in non-volatile registers, and pay only for what it uses.**

### The rule in one example

`fib` at `-O0` (L10 §3) needed `fib(n-1)`'s result to survive a second `call`:

```
  23:  call   fib
  28:  mov    rbx,rax     ; rax is caller-saved -- move it somewhere safe
  36:  call   fib
  3b:  add    rax,rbx     ; rbx survived, because the callee is obliged
```

*(Verified.)* And so the prologue contains `push rbx` and the epilogue `mov rbx,[rbp-0x8]`. **The push exists because of the move, which exists because of the second call.**

---

## 5. What the Callee Sees on Entry

Immediately after `call` transfers control, before the prologue runs:

| Location | Contents |
|---|---|
| `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9` | arguments 1–6 |
| `xmm0`–`xmm7` | floating-point arguments |
| `[rsp]` | **return address** |
| `[rsp+8]`, `[rsp+16]`, … | arguments 7, 8, … |
| `rsp` | ≡ 8 (mod 16) — see L12 |

**`[rsp]` holds the return address.** Write to it and `ret` goes somewhere else. That sentence is Week 9's entire lecture, and it follows from nothing more than L10 §1.

---

## 6. Leaf Functions Pay Nothing

A function that calls nothing needs no frame at all:

```c
int leaf(int x) { return x*2 + 1; }
```

```
<leaf>:  endbr64
         lea    eax,[rdi+rdi*1+0x1]
         ret
```

*(Verified.)* **No push, no `sub rsp`, no `rbp`.** The argument is already in a register, the result goes in another, and nothing needs to survive anything.

And the caller of two such leaves may not call them at all:

```c
int nonleaf(int x) { return leaf(x) + leaf(x+1); }
```

```
<nonleaf>:  endbr64
            lea    eax,[rdi*4+0x4]
            ret
```

*(Verified.)* $(2x+1) + (2x+3) = 4x + 4$ — **both calls inlined and the arithmetic folded.** The calling convention costs nothing here because there is no call.

> **This is why "function call overhead" is a poor reason to write long functions.** For small
> functions the compiler removes the call. For large ones the overhead is negligible against the
> body. The cases where it genuinely matters — indirect calls the compiler cannot see through,
> calls across a shared-library boundary — are the ones you cannot fix by hand-inlining anyway.

---

## 7. What to Take Away

1. **The ABI is agreement, not hardware.** Linux and Windows differ on the same chip.
2. **`rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`**, then the stack. Floating point counts separately in `xmm0`–`xmm7`.
3. **Stack arguments are pushed in reverse** so the callee reads them ascending, and **the caller cleans up**.
4. **Caller-saved: `rax`, `rcx`, `rdx`, `rsi`, `rdi`, `r8`–`r11`. Callee-saved: `rbx`, `rbp`, `r12`–`r15`.**
5. **A value that must cross a call goes in a callee-saved register**, and the callee pays for it with a push.
6. **`[rsp]` at function entry is the return address.**
7. **Leaf functions may need no frame at all.**

---

## Exercises

1. `void f(int a, double b, int c, double d, int e)` — give the register for each argument.
2. A function needs three values across two calls. How many pushes does that cost, and which registers would you choose?
3. Argument 7 is at `[rsp+8]` on entry. Where is it after the prologue does `push rbp`? After a further `sub rsp,0x20`?
4. Explain, using §3, why a callee-pops convention would make `printf` impossible to implement.
5. `nonleaf` compiled to two instructions with no call. Write a version of it the compiler *cannot* reduce this way, and say what blocks it.

---

*Next: L12 — alignment, the red zone, and recursion in hand-written assembly.*

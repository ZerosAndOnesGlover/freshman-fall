# CS 201 · Problem Set 3 — Solutions
## Instructor Only

---

> **Not for distribution.** All assembly assembled with `nasm -f elf64`, linked `gcc -O2 -no-pie`,
> and run. All GDB output from the lab image.

---

## Q1 (20) — Reading a Frame

### (a) [5]

| Offset | Contents | Size |
|---|---|---:|
| `rbp+8` | return address (pushed by `call`) | 8 |
| `rbp+0` | saved `rbp` (caller's frame pointer) | 8 |
| `rbp-8` | saved `rbx` | 8 |
| `rbp-0x10` | *(padding / unused)* | 8 |
| `rbp-0x18` | `n`, the spilled argument | 8 |

$8 + 8 + 8 + 24 = \mathbf{48}$ ✓ — matching GDB's `frame at 0x…d1b0` / `called by frame at 0x…d1e0`, a difference of `0x30`. *(Verified.)*

> The `sub rsp,0x18` reserves 24 bytes for a single 8-byte local. **Accept "padding" or "alignment"
> for the middle slot** — GCC is keeping the frame a multiple of 16 and does not compact `-O0` frames.

### (b) [5]

**[3]** `fib(n-1)` returns in `rax`. `rax` is **caller-saved**, so the `call` at `36` may destroy it. The value must survive that call, so it is moved into `rbx`, which is **callee-saved** — the callee is obliged to restore it.

**[2] With `r10`:** `r10` is caller-saved too, so nothing preserves it. The program still assembles and links.

**First wrong answer at $n = 4$: it returns 2 where the correct value is 3.** *(Verified — $n = 0..3$ are still correct.)*

> **Why $n \le 3$ survives is worth a sentence in class.** The base cases return before touching
> `r10` at all, so the clobber only bites once a recursive call itself takes the non-base path — which
> first happens at $n = 4$. **A bug that passes your first four test cases** is the recurring theme of
> this problem set.

### (c) [4]

**[2]** Pushed at instruction `8`, immediately after `mov rbp,rsp`. So `rbx` sits at `rbp-8`.

**[2]** A `pop` would require `rsp` to be pointing at it, but `rsp` is 24 bytes lower after `sub rsp,0x18`. Restoring by `mov` from a known `rbp` offset works regardless of where `rsp` is — and `leave` then resets `rsp` from `rbp` anyway.

### (d) [3]

```
mov rsp, rbp
pop rbp
```

**[1]** Safe because `leave` **discards** whatever `rsp` was, restoring it from `rbp`. The frame pointer is a fixed anchor, so no accounting of intervening pushes and subs is needed. That is the whole reason to keep a frame pointer at `-O0`.

### (e) [3]

**[2]** Prologue, epilogue, and **spilling every value to the stack between statements** — `-O0` keeps nothing in registers across a statement boundary, which makes single-stepping predictable and the code slow.

**[1] At `-O2`:** the locals stay in registers, the frame pointer is dropped, and GCC additionally unrolls the recursion — the `-O2` `fib` pushes six callee-saved registers and reserves 0xc8 bytes. *(Verified.)*

---

## Q2 (18) — The Convention

### (a) [4] — 0.5 each

```c
void f(int a, double b, int c, double d, long *e, int g, int h, double i);
```

| Arg | Location |
|---|---|
| `a` (int) | `rdi` — integer #1 |
| `b` (double) | `xmm0` — SSE #1 |
| `c` (int) | `rsi` — integer #2 |
| `d` (double) | `xmm1` — SSE #2 |
| `e` (long*) | `rdx` — integer #3 |
| `g` (int) | `rcx` — integer #4 |
| `h` (int) | `r8` — integer #5 |
| `i` (double) | `xmm2` — SSE #3 |

> **The point of the question is that the two sequences do not interleave.** A student who assigns
> `b` to `rsi` has missed it entirely — deduct heavily. Note also that nothing goes on the stack here:
> five integer args and three SSE args are all within their respective limits.

### (b) [4]

**Caller-saved:** `rax`, `rcx`, `r9`, `r11`, `rdi`.
**Callee-saved:** `rbx`, `r12`, `rbp`.

**Caller's obligation:** if it needs a caller-saved register's value after a call, it must save it itself.
**Callee's obligation:** if it uses a callee-saved register, it must restore the original before returning.

### (c) [4]

| Location | Contents |
|---|---|
| `[rsp]` | **return address** |
| `[rsp+8]` | argument 7 |
| `[rsp+16]` | argument 8 |
| `[rsp+24]` | argument 9 |

Arguments 1–6 are in `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`. **Each stack argument occupies 8 bytes** regardless of declared type.

### (d) [3]

**Reverse push order** puts argument 7 at the lowest address, so the callee reads them upward from `[rsp+8]` — it can walk forward from a known start without knowing where the list ends.

**Caller cleanup** is necessary because **only the caller knows how many arguments it passed.** `printf` cannot pop them; it does not know the count until it has parsed the format string, and a callee-pops convention would need that count encoded in the `ret`.

> Both halves are required for full marks. Most students get the second and miss the first.

### (e) [3]

```
<nonleaf>:  endbr64
            lea    eax,[rdi*4+0x4]
            ret
```

*(Verified.)* **Both calls were inlined**, then the arithmetic folded: $(2x+1) + (2x+3) = 4x+4$. There is no `call`, no frame, and no calling convention cost at all.

---

## Q3 (36) — Recursive Fibonacci in Assembly

### (a) [14] — a correct reference implementation

```nasm
        global  asm_fib
        section .text
asm_fib:                        ; long asm_fib(long n)   rdi -> rax
        cmp     rdi, 1
        jle     .base           ; n <= 1 : return n, before any frame
        push    rbx             ; callee-saved: holds fib(n-1) across call 2
        push    r12             ; callee-saved: holds n
        sub     rsp, 8          ; realign (see (c))
        mov     r12, rdi
        lea     rdi, [r12-1]
        call    asm_fib
        mov     rbx, rax
        lea     rdi, [r12-2]
        call    asm_fib
        add     rax, rbx
        add     rsp, 8
        pop     r12
        pop     rbx
        ret
.base:  mov     rax, rdi
        ret
        section .note.GNU-stack noalloc noexec nowrite progbits
```

*(Verified — agrees with a C reference for $n = 0 \ldots 12$; $\text{fib}(12) = 144$, $\text{fib}(30) = 832\,040$.)*

**Marking:** 8 for correctness on the full range, 3 for handling $n \le 1$ including $n = 0$, 3 for a working build with `.note.GNU-stack`. **A version that loops rather than recursing scores 0** — the question is about the stack.

### (b) [6]

Two values must survive a `call`:

| Value | Register | Why |
|---|---|---|
| `fib(n-1)`'s result | `rbx` | returns in `rax`, which is caller-saved; the second `call` would destroy it |
| `n` | `r12` | arrives in `rdi`, which is caller-saved *and* is the argument register the recursive calls overwrite |

**Both are callee-saved, so both are pushed** — using them means inheriting the obligation to restore them.

> Accept any callee-saved pair (`rbx`, `rbp`, `r12`–`r15`). Accept also a version that spills `n` to
> the stack instead of `r12`. **Deduct 4 for any caller-saved choice**, even if the tests happen to
> pass — see (e)(1).

### (c) [6]

| Point | `rsp` mod 16 |
|---|---|
| before the caller's `call asm_fib` | 0 |
| on entry to `asm_fib` | 8 |
| after `push rbx` | 0 |
| after `push r12` | 8 |
| after `sub rsp, 8` | **0** ✓ |

**Two pushes is an even number, so they return `rsp` to its entry parity of 8 — still misaligned.** The `sub rsp,8` is what fixes it. An odd number of pushes would need no `sub`.

> The common error is asserting "two pushes = 16 bytes = still aligned". That is true of the *offset*
> and false of the *parity*, because entry alignment is 8, not 0.

### (d) [4]

**[2]** The base case needs no frame, no register saves and no alignment — `mov rax,rdi; ret` is two instructions against roughly twelve for the full prologue and epilogue.

**[2] Quantified.** For `fib(10)`, total calls $C(10) = 177$; base-case calls $B(n) = \text{fib}(n+1)$, so $B(10) = \text{fib}(11) = \mathbf{89}$.

**89 of 177 calls — 50.3% — are base cases.** Slightly over half of all calls skip the frame entirely.

### (e) [6] — 3 each

**1. `r10` instead of `rbx`.**

*(Verified.)* It **assembles and links cleanly**. It produces correct results for $n = 0, 1, 2, 3$ and **first fails at $n = 4$, returning 2 instead of 3.**

The clobber is real from the start, but only bites once a recursive call takes the non-base path, which first happens at $n=4$.

**2. Removing the alignment `sub`.**

*(Verified.)* It **does not crash.** Correct results through `fib(30)`, exit status 0 — and still no crash with a `printf` inside the recursion, or with a probe function holding a 16-byte-aligned array.

**Why misalignment is usually silent:** it faults only if the callee executes an **aligned SSE instruction** (`movaps`, `movapd`, …) on a **stack address**. Most functions never do. For one to be emitted, the callee must have a 16-byte-aligned stack object that the optimiser cannot eliminate.

**And the last twist:** with the `printf` removed from `sse_probe`, GCC optimises the whole body to `endbr64; ret` — the array is unused, so it does not exist, so there is no `movaps`, so there is no crash. *(Verified: four `movap*` instructions in the crashing build, zero in the silent one.)*

> **Full marks require honest reporting of the non-crash.** A student who writes "removing the sub
> caused a segfault" either did not run it or is telling you what they think you want. **Award the
> marks for the correct negative result**, and for the observation that an ABI violation can run
> correctly for years and fault when an unrelated function is recompiled.
>
> The `sse_probe` twist is Week 0 Lab Part 4 again: **your demonstration of a bug can itself be
> optimised away.**

---

## Q4 (14) — Alignment and the Red Zone

### (a) [4]

**Rule:** `rsp` ≡ 0 (mod 16) **immediately before `call` executes**. `call` then pushes 8, so **on entry to any function `rsp` ≡ 8 (mod 16)**.

| Point | mod 16 |
|---|---|
| before `call f` | **0** |
| on entry to `f` | **8** |
| after 3 pushes | **0** *(three pushes = 24 bytes; $8+24 = 32 \equiv 0$)* |
| `f` must `sub` before its own `call` | **0 — nothing** |

> The last row is the discriminator: an **odd** number of pushes leaves it aligned, an **even** number
> does not. Students reliably guess the opposite.

### (b) [4]

**The `sub rsp,0x8` allocates nothing.** `h` has no locals. It exists solely to convert the entry alignment of 8 back to 0 before calling `g`. Two instructions and eight bytes of stack spent purely on ABI compliance.

### (c) [3]

**Chain:** the caller left `rsp` ≡ 8 at the `call` → the callee's stack objects are misaligned → the compiler had emitted `movaps` because the ABI *promised* alignment → `movaps` on an address not a multiple of 16 raises a general-protection fault → `SIGSEGV`.

**The crashing function is not the buggy one.** It is correct and relies on a guarantee it was entitled to rely on. The bug is one frame down, and the diagnostic is `rsp & 15` at the call site — not anything visible in the faulting function.

### (d) [3]

**The red zone.** **128 bytes** below `rsp`. Two conditions:

1. The function must be a **leaf** — any `call` pushes a return address over it.
2. It must use **at most 128 bytes**.

*(Verified: `int f(int x){int a=x+1,b=x+2;return a*b;}` at `-O0` stores three locals at `[rbp-0x14]`, `[rbp-0x8]`, `[rbp-0x4]` with no `sub rsp` at all.)*

---

## Q5 (12) — How Deep Can You Go?

### (a) [4]

**32 bytes:** 8 (return address) + 8 (`push rbx`) + 8 (`push r12`) + 8 (`sub rsp,8`).

$$\frac{8 \times 1024 \times 1024}{32} = \mathbf{262\,144 \text{ frames}}$$

### (b) [4]

**[2] Depth:** 50. **Calls:** $C(n) = 2\,\text{fib}(n+1) - 1$, so $C(50) = 2 \times 20\,365\,011\,074 - 1 \approx 4.07 \times 10^{10}$.

**[2] Calls bind.** 50 frames is 1600 bytes — nothing. Forty billion calls at even 1 ns each is roughly **40 seconds**, and in practice far longer.

**Why students confuse them:** both are described as "how much recursion", and the word *depth* is used loosely for both. **They are different resources — depth consumes stack, call count consumes time — and an algorithm can be extreme in one and trivial in the other.** Naive Fibonacci is shallow and expensive; a recursive parser is cheap and deep.

### (c) [4]

**[2]** Attacker-controlled input controls the nesting depth — deeply nested parentheses, JSON, or XML. Each level costs a frame. **With no depth limit, the attacker chooses how much stack to consume**, and can exhaust it with a small input, crashing the process. Cheap for the attacker, fatal for the service.

**[1] Mitigation:** an explicit depth counter with a hard limit, rejecting input past it; or an iterative parser with an explicit heap-allocated stack.

**[2] At the hardware level:** there is **no bounds check in `call`.** `rsp` simply walks downward. Below the stack region the kernel keeps an unmapped **guard page**; touching it raises a page fault the kernel cannot satisfy, and it delivers `SIGSEGV`. **The guard page is the entire enforcement mechanism** — which is also why a single stack frame larger than the guard region can *skip over* it, the bug class known as stack clash.

---

## Mark Summary

| | |
|---|---:|
| Q1 | 20 |
| Q2 | 18 |
| Q3 | 36 |
| Q4 | 14 |
| Q5 | 12 |
| **Total** | **100** |

**Where the class loses marks, in order:**

1. **Q3(e)(2)** — reporting a crash that did not happen. Reward the honest negative result.
2. **Q4(a)** — getting push parity backwards, believing an even number of pushes preserves alignment.
3. **Q2(a)** — interleaving the integer and SSE argument sequences.
4. **Q3(c)** — confusing byte offset with alignment parity.
5. **Q1(b)** — describing `rbx` as "a spare register" rather than as callee-saved.

Items 1 and 2 are worth ten minutes in Week 4, and item 2 reappears on Midterm 1.

---

*CS 201 · Week 3 · PS 3 Solutions · Instructor Only*

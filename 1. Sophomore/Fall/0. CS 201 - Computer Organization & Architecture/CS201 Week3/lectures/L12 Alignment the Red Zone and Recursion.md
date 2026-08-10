# CS 201 · Computer Organization & Architecture
## Week 3 · Lecture 3 of 3
### Alignment, the Red Zone, and Recursion in Assembly

---

**Reading:** CS:APP §3.7.5–3.7.6 · **Previous:** L11, the System V ABI

---

## 1. The 16-Byte Rule

**System V requires `rsp` to be a multiple of 16 immediately *before* a `call` executes.**

Since `call` then pushes 8 bytes, it follows that **on entry to any function, `rsp ≡ 8 (mod 16)`.**

Watch a compiler obey it for no other reason:

```c
void h(void) { g(); }
```

```
<h>:  endbr64
      sub    rsp,0x8
      call   g
      add    rsp,0x8
      ret
```

*(Verified.)*

**That `sub rsp,0x8` allocates nothing.** `h` has no locals. It exists purely to turn the entry alignment of 8 back into 0 before calling `g`. Two instructions and eight bytes of stack, spent on arithmetic hygiene.

**The bookkeeping:**

| Point | `rsp` mod 16 |
|---|---|
| before `call h` | 0 |
| on entry to `h` | 8 |
| after `sub rsp,8` | **0** ✓ |
| on entry to `g` | 8 |

**Each `push` flips the parity.** An odd number of pushes needs a compensating `sub rsp,8`; an even number does not. In L11 §3 the caller pushed three arguments — odd — and paid `sub rsp,0x10` to fix it.

---

## 2. What Breaks Without It

The rule sounds bureaucratic until you violate it.

```nasm
good_call:
        sub     rsp, 8          ; entry 8 -> 0 : aligned
        call    uses_sse
        add     rsp, 8
        ret

bad_call:
        sub     rsp, 16         ; entry 8 -> 8 : STILL misaligned
        call    uses_sse
        add     rsp, 8
        ret
```

where `uses_sse` holds a 16-byte-aligned `double` array. Result:

```
good:
  ok, sum=10  (&buf=0x7ffd…, aligned16=1)
bad:
Segmentation fault (core dumped)      [status 139]
```

*(Verified.)*

**Why.** GCC compiled `uses_sse` with `movaps XMMWORD PTR [rsp],xmm0` — the *aligned* 16-byte SSE move, which **faults** if its address is not a multiple of 16. The compiler is entitled to emit it because the ABI promised alignment. `bad_call` broke the promise, and the fault surfaces inside a function that is perfectly correct.

> **This is the failure mode to remember: the crash is not where the bug is.** `uses_sse` is innocent
> and will appear at the top of your backtrace. The bug is in the caller, one frame down, and the
> only symptom is a `movaps` on an address ending in 8. Check `rsp & 15` at the `call`.

`movups` — the unaligned variant — never faults, and compilers use it where they cannot prove alignment. **The ABI's guarantee is exactly what lets them use the faster aligned form instead.**

### Misalignment is usually silent, and that is the worst part

**A misaligned `rsp` only faults if the callee actually executes an aligned SSE instruction on a stack address.** Most functions never do.

Removing the alignment `sub` from the recursive `asm_fib` in §4 produced **correct answers and exit status 0** — through 30 levels of recursion, and again with a `printf` inside the recursion. *(Verified.)* A probe function with a 16-byte-aligned local **also** failed to crash it, because GCC had optimised the probe's body away to `endbr64; ret` — the array was unused, so it did not exist.

The crash in the listing above happens only because `uses_sse` **prints** its result, so the array cannot be eliminated and `movaps XMMWORD PTR [rsp],xmm0` really is emitted. *(Four `movap*` instructions in the crashing build; zero in the silent one — verified.)*

> **Two lessons, and the second is Week 0's.** An ABI violation can run correctly for years and then
> fault when an unrelated function is recompiled with different optimisation. And **your attempt to
> demonstrate the bug can itself be optimised out of existence** — exactly what happened to the
> hundred-million-iteration loop in Lab 0.

---

## 3. The Red Zone

The 128 bytes **below** `rsp` are reserved for the current function. Nothing — not a signal handler, not the kernel — may write there. A **leaf** function can therefore use them as scratch without moving `rsp` at all.

```c
int f(int x) { int a = x+1, b = x+2; return a*b; }
```

At `-O0`, which normally spills everything:

```
<f>:  endbr64
      push   rbp
      mov    rbp,rsp
      mov    DWORD PTR [rbp-0x14],edi   ; x
      mov    DWORD PTR [rbp-0x8],eax    ; a
      mov    DWORD PTR [rbp-0x4],eax    ; b
      ...
      pop    rbp
      ret
```

*(Verified.)* **There is no `sub rsp`.** Three locals live at `[rbp-0x14]`, `[rbp-0x8]` and `[rbp-0x4]` — all *below* `rsp`, in the red zone. The function saves two instructions and touches the stack pointer only for `rbp`.

**Two conditions.** The function must be a **leaf** — any `call` would push a return address straight over the red zone. And it must stay within **128 bytes**.

> **The red zone does not exist on Windows**, and the kernel disables it for its own code
> (`-mno-red-zone`), because an interrupt handler runs on the same stack and would clobber it.
> Knowing it exists explains a class of otherwise baffling `-O0` listings.

---

## 4. Recursion, by Hand

Everything so far combines here. A naive recursive Fibonacci:

```nasm
; long asm_fib(long n)                  rdi -> rax
asm_fib:
        cmp     rdi, 1
        jle     .base                   ; n <= 1 : return n
        push    rbx                     ; callee-saved: fib(n-1) across call 2
        push    r12                     ; callee-saved: holds n
        sub     rsp, 8                  ; realign -- see below
        mov     r12, rdi
        lea     rdi, [r12-1]
        call    asm_fib
        mov     rbx, rax                ; must survive the next call
        lea     rdi, [r12-2]
        call    asm_fib
        add     rax, rbx
        add     rsp, 8
        pop     r12
        pop     rbx
        ret
.base:  mov     rax, rdi
        ret
```

*(Verified — matches a C reference for $n = 0 \ldots 12$; $\text{fib}(30) = 832\,040$.)*

**Four decisions, each forced by the ABI:**

**`rbx` and `r12`, not `rax` and `rdi`.** Both values must survive a `call`, and only callee-saved registers are guaranteed to. Using `r10` here would compile, run, and return wrong answers.

**They are pushed, because we use them.** Callee-saved means *we* now owe the same guarantee to our caller.

**`sub rsp, 8` is alignment.** On entry `rsp ≡ 8`; two pushes bring it to `≡ 8` again (each push flips parity, two pushes restore it), so 8 more are needed before the recursive `call`. Get this wrong and the fault appears somewhere in libc.

**The base case returns before the prologue.** `n ≤ 1` needs no frame, no saves, no alignment — just `mov rax,rdi; ret`. **Roughly half of all calls in a naive Fibonacci hit the base case**, so keeping it free is worth more than it looks.

---

## 5. What the Compiler Does Instead

`gcc -O2` on the same C function produces something unrecognisable — it begins:

```
push r15 ; push r14 ; push r13 ; push r12 ; push rbp ; push rbx
sub  rsp,0xc8
```

*(Verified.)* **Six callee-saved registers and 200 bytes of frame**, for a function whose source is one line. GCC has partially unrolled the recursion, computing several levels per call to cut the call count.

**Do not try to read it.** The point of showing it is calibration: your hand-written version is clearer and slower, the compiler's is faster and unreadable, and **both obey exactly the same ABI.** That is what makes them interoperable.

---

## 6. Depth Is the Real Limit

`asm_fib`'s frame is 8 (return address) + 16 (two pushes) + 8 (alignment) = **32 bytes**. With an 8 MB stack:

$$\frac{8 \times 1024 \times 1024}{32} = 262\,144 \text{ frames}$$

Naive Fibonacci recurses only to depth $n$, so that is never the constraint — but it makes $O(\varphi^n)$ **calls**, and `fib(50)` would take days. **Depth and call count are different costs**, and confusing them is a common error.

A recursive descent parser on attacker-controlled input has the opposite profile: few calls, unbounded depth. **That one is a denial-of-service bug**, and it is why production parsers impose a depth limit.

---

## 7. What to Take Away

1. **`rsp` ≡ 0 (mod 16) before `call`**, hence ≡ 8 on entry. Each push flips the parity.
2. **Violating it faults inside innocent code** — `movaps` on a misaligned address, in a function that is not the buggy one.
3. **The red zone is 128 bytes below `rsp`**, usable by leaf functions with no `sub rsp`.
4. **Values crossing a call go in callee-saved registers, which you must then push.**
5. **Return early from base cases**, before building a frame.
6. **Depth costs stack; call count costs time.** They are not the same limit.

---

## Exercises

1. A function pushes four callee-saved registers and needs 40 bytes of locals. What must `sub rsp, N` be for the call inside it to be aligned?
2. `bad_call` used `sub rsp,16` and crashed. Give two other `sub` values that would also crash, and two that would work.
3. Why can a function that calls `printf` not use the red zone, even for one byte?
4. Rewrite `asm_fib`'s base case to run *after* the prologue instead of before it. Count the extra instructions executed for `fib(10)`, given that it makes 177 calls.
5. `asm_fib` uses `r12` to hold `n`. Could it instead reload `n` from the stack each time and avoid one push? What would that cost, and when would it be the better trade?

---

*Next week: the memory hierarchy — where the time actually goes.*

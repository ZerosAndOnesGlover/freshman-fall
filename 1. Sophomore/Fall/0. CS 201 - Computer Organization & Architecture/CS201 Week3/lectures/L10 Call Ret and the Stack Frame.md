# CS 201 · Computer Organization & Architecture
## Week 3 · Lecture 1 of 3
### `call`, `ret`, and the Stack Frame

---

**Reading:** CS:APP §3.7.1–3.7.3 · **Previous:** L09, flags and control flow

---

## 1. Two Instructions, One Idea

```
call target     ≡    push rip_of_next_instruction
                     jmp target

ret             ≡    pop rip
```

**That is the entire mechanism.** `call` pushes the address of the following instruction and jumps; `ret` pops an address and jumps to it.

**Note what `ret` does *not* do.** It does not check that the popped value is a return address. It does not verify it points into your program. **It jumps to whatever eight bytes happen to be at `rsp`.** Every stack-smashing attack in Week 9 is built on that one sentence.

---

## 2. The Stack Grows Down

`rsp` always points at the **most recently pushed** item — the lowest occupied address.

```
   high addresses
   ┌─────────────────────┐
   │ caller's frame      │
   ├─────────────────────┤
   │ return address      │  <- pushed by `call`
   ├─────────────────────┤
   │ saved rbp           │  <- pushed by the prologue
   ├─────────────────────┤  <- rbp points here
   │ saved callee-saved  │
   ├─────────────────────┤
   │ local variables     │
   ├─────────────────────┤  <- rsp
   │ (unused)            │
   low addresses
```

**`push` subtracts 8 then stores; `pop` loads then adds 8.** Always 8 in x86-64, even pushing a 32-bit value.

---

## 3. A Real Frame, Built and Torn Down

```c
long fib(long n) { return n < 2 ? n : fib(n-1) + fib(n-2); }
```

At `-O0`:

```
<fib>:
   0:  endbr64
   4:  push   rbp                        ; save caller's frame pointer
   5:  mov    rbp,rsp                    ; establish ours
   8:  push   rbx                        ; save a callee-saved register
   9:  sub    rsp,0x18                   ; make room for locals
   d:  mov    QWORD PTR [rbp-0x18],rdi   ; spill the argument n
  11:  cmp    QWORD PTR [rbp-0x18],0x1
  16:  jle    40                         ; n <= 1 -> base case
  18:  mov    rax,QWORD PTR [rbp-0x18]
  1c:  sub    rax,0x1
  20:  mov    rdi,rax
  23:  call   fib                        ; fib(n-1)
  28:  mov    rbx,rax                    ; stash the result in rbx
  2b:  mov    rax,QWORD PTR [rbp-0x18]
  2f:  sub    rax,0x2
  33:  mov    rdi,rax
  36:  call   fib                        ; fib(n-2)
  3b:  add    rax,rbx                    ; combine
  3e:  jmp    44
  40:  mov    rax,QWORD PTR [rbp-0x18]   ; base case: return n
  44:  mov    rbx,QWORD PTR [rbp-0x8]    ; restore rbx
  48:  leave                             ; mov rsp,rbp ; pop rbp
  49:  ret
```

*(Verified.)*

**Read instruction `28` and ask why `rbx`.**

The result of `fib(n-1)` arrives in `rax`. It must survive until instruction `3b`. But instruction `36` is another `call`, and **`rax` is caller-saved — the callee may destroy it.** So the value is moved somewhere the callee is obliged to preserve. That is what `rbx` is for, and it is why the prologue pushed it.

**The whole caller/callee-saved distinction is visible in those three instructions.** L11 states the rule; this is the reason for it.

---

## 4. The Frame Pointer, and Why It Is Optional

`rbp` gives every local a **constant** offset — `n` is at `[rbp-0x18]` throughout, no matter how `rsp` moves. That makes debugging and unwinding easy.

It also costs a register and two instructions. So at `-O1` and above GCC drops it (`-fomit-frame-pointer` is the default) and addresses locals from `rsp` instead, accepting that the offsets change as the function pushes and pops.

| | Frame pointer | No frame pointer |
|---|---|---|
| Locals addressed from | `rbp`, fixed offsets | `rsp`, varying offsets |
| Registers available | 15 | 16 |
| Stack walking | trivial — follow the `rbp` chain | needs unwind tables |
| Default at | `-O0` | `-O1` and above |

**`leave`** is one byte and does `mov rsp,rbp; pop rbp` — tearing the frame down regardless of what `rsp` was doing.

> **Where the unwind tables live.** Without a frame pointer, GDB still produced a correct backtrace
> in Lab 3. It reads `.eh_frame` — DWARF unwind data the compiler emits precisely so the frame
> pointer can be omitted without losing debuggability. Those are the `.cfi_*` directives you saw in
> Week 0's `gcc -S` output.

---

## 5. Watching the Frames Stack Up

Break inside `fib(2)` reached from `fib(6)`:

```
(gdb) bt
#0  fib (n=2) at fibmain.c:2
#1  0x0000555555555171 in fib (n=3) at fibmain.c:2
#2  0x0000555555555171 in fib (n=4) at fibmain.c:2
#3  0x0000555555555171 in fib (n=5) at fibmain.c:2
#4  0x0000555555555171 in fib (n=6) at fibmain.c:2
#5  0x00005555555551a5 in main () at fibmain.c:3
```

*(Verified.)*

**Every recursive frame has the same return address, `0x555555555171`** — the instruction after the *second* `call fib`. Only `main`'s differs. Recursion is not special to the hardware; it is the same frame layout repeated, distinguished only by where `rsp` happens to be.

```
(gdb) info frame
Stack level 0, frame at 0x7fffffffd1b0:
 rip = 0x55555555515a in fib; saved rip = 0x555555555171
 called by frame at 0x7fffffffd1e0
 Saved registers:
  rbx at 0x7fffffffd198, rbp at 0x7fffffffd1a0, rip at 0x7fffffffd1a8
```

*(Verified.)* **Each frame is 48 bytes** — `0x7fffffffd1e0 - 0x7fffffffd1b0 = 0x30`. Account for them: 8 (return address) + 8 (saved `rbp`) + 8 (saved `rbx`) + 24 (`sub rsp,0x18`) = 48. ✓

**And note the addresses of the saved registers**, which is the layout of §2 made concrete:

| Address | Contents | Relative to `rbp` = `0x…d1a0` |
|---|---|---|
| `0x…d1a8` | return address | `rbp+8` |
| `0x…d1a0` | saved `rbp` | `rbp+0` |
| `0x…d198` | saved `rbx` | `rbp-8` |
| `0x…d188` | `n` | `rbp-0x18` |

---

## 6. Stack Overflow Is Just This, Repeated

Each frame costs 48 bytes here. The default thread stack on Linux is 8 MB:

$$\frac{8 \times 1024 \times 1024}{48} \approx 175\,000 \text{ frames}$$

**Recurse deeper than that and `rsp` walks off the end of the mapped region**, the hardware raises a page fault on an unmapped page, and the kernel delivers `SIGSEGV`. There is no bounds check in `call` — the guard page is the entire mechanism.

**This is why deep recursion is a memory-safety concern and not merely a style preference**, and why a recursive parser on attacker-controlled input is a denial-of-service bug.

---

## 7. What to Take Away

1. **`call` pushes the return address and jumps. `ret` pops an address and jumps.** No validation whatsoever.
2. **The stack grows down**; `rsp` points at the lowest occupied byte.
3. **The prologue** saves `rbp`, sets it, saves callee-saved registers, then makes room for locals.
4. **A value that must survive a call goes in a callee-saved register** — that is what `mov rbx,rax` is doing in `fib`.
5. **The frame pointer is optional** above `-O0`; `.eh_frame` keeps unwinding possible without it.
6. **Recursion is one frame layout repeated**, and the stack's size is the only limit.

---

## Exercises

1. Write `call target` and `ret` as explicit `push`/`pop`/`jmp` sequences. Which register does each implicitly modify, and by how much?
2. `fib`'s frame is 48 bytes but its locals need only 8 (`n`). Account for the other 40.
3. Why does the prologue `push rbx` *before* `sub rsp,0x18` rather than after? Would either order work?
4. Replace `mov rbx,rax` at instruction `28` with `mov r10,rax`. The code still assembles. What goes wrong, and on which input would you first notice?
5. `leave` is one byte and equivalent to two instructions. Give a situation in which a compiler must *not* use it.

---

*Next: L11 — the System V ABI, in full.*

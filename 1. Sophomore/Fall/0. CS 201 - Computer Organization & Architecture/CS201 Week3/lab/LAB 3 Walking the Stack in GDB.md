# CS 201 · Week 3 · Lab 3
## Walking the Stack in GDB

---

**When:** Tuesday 15:00–16:50, BH 210 · **Assessment:** unmarked, checked off by the TA
**You need:** `gcc`, `gdb`, `nasm`, `objdump`, and `set disassembly-flavor intel` in your `~/.gdbinit`.

---

## What This Lab Is For

You have read about the stack frame. **Today you look at one**, byte by byte, while it exists — find the return address in memory, find the saved registers, and change one of them to see what happens.

Part 5 is the one that matters for Week 9.

---

## Part 1 — Build the Subject (10 min)

```c
/* fibmain.c */
#include <stdio.h>
long fib(long n) { return n < 2 ? n : fib(n-1) + fib(n-2); }
int main(void) { printf("%ld\n", fib(6)); return 0; }
```

```bash
gcc -O0 -g -o fibmain fibmain.c
objdump -d --no-show-raw-insn -M intel fibmain | sed -n '/<fib>:/,/^$/p'
```

**Identify, in the listing:**

1. The prologue — three instructions.
2. Where `n` is stored, as an offset from `rbp`.
3. The two `call` instructions.
4. The instruction that saves `fib(n-1)`'s result, and **which register it uses**.
5. The epilogue.

**The interesting one is (4).** The result comes back in `rax`. It is immediately moved to `rbx`. **Why not just leave it in `rax`?**

**✅ CHECKPOINT 1** — the listing and your five answers.

---

## Part 2 — Five Frames Deep (25 min)

```bash
gdb -q ./fibmain
```

```
(gdb) break fib if n == 2
(gdb) run
(gdb) bt
```

```
#0  fib (n=2) at fibmain.c:2
#1  0x0000555555555171 in fib (n=3) at fibmain.c:2
#2  0x0000555555555171 in fib (n=4) at fibmain.c:2
#3  0x0000555555555171 in fib (n=5) at fibmain.c:2
#4  0x0000555555555171 in fib (n=6) at fibmain.c:2
#5  0x00005555555551a5 in main () at fibmain.c:3
```

*(Verified.)*

**Every recursive frame shows the same return address, `0x…171`. Only `main`'s differs.** Explain why in one sentence. *(Then find `0x…171` in your Part 1 listing — which instruction is it?)*

### 2.1 Anatomy of one frame

```
(gdb) info frame
```

```
Stack level 0, frame at 0x7fffffffd1b0:
 rip = 0x55555555515a in fib; saved rip = 0x555555555171
 called by frame at 0x7fffffffd1e0
 Saved registers:
  rbx at 0x7fffffffd198, rbp at 0x7fffffffd1a0, rip at 0x7fffffffd1a8
```

*(Verified — your addresses will differ; ASLR moves the stack every run.)*

**Compute the frame size** from "frame at" and "called by frame at". You should get **48 bytes**. Now account for all 48: return address, saved `rbp`, saved `rbx`, and the `sub rsp,0x18`.

### 2.2 Read the frame directly

```
(gdb) p $rsp
(gdb) p $rbp
(gdb) x/6gx $rsp
```

Match each 8-byte word against the layout:

| Offset | Should hold |
|---|---|
| `rbp+8` | return address |
| `rbp+0` | saved `rbp` (the caller's) |
| `rbp-8` | saved `rbx` |
| `rbp-0x18` | `n` |

```
(gdb) x/gx $rbp+8       # return address — compare with `bt`
(gdb) x/gx $rbp         # saved rbp — compare with frame #1's rbp
(gdb) x/gx $rbp-0x18    # n — should be 2
```

**✅ CHECKPOINT 2** — the backtrace, the frame size accounted for, and `n` read out of memory by address.

---

## Part 3 — Watch the Frames Build (20 min)

Restart, break at `fib`, and step by instruction through the prologue:

```
(gdb) delete
(gdb) break fib
(gdb) run
(gdb) p $rsp
(gdb) stepi           # push rbp
(gdb) p $rsp
(gdb) stepi           # mov rbp,rsp
(gdb) p $rbp
(gdb) stepi           # push rbx
(gdb) stepi           # sub rsp,0x18
(gdb) p $rsp
```

**Record `rsp` after each step.** It should fall by 8, 0, 8 and 24. Confirm the total against Part 2's 48-byte frame.

### 3.1 Alignment

At each `call` in the program, `rsp` must be ≡ 0 (mod 16).

```
(gdb) break *0x0000555555555123      # replace with YOUR address of the first `call fib`
(gdb) run
(gdb) p $rsp & 15
```

**It should print 0.** If it does not, you broke on the wrong instruction — the rule applies immediately *before* the `call` executes.

**✅ CHECKPOINT 3** — your four `rsp` values, and `$rsp & 15` at a call site.

---

## Part 4 — The Red Zone (15 min)

```c
int f(int x) { int a = x+1, b = x+2; return a*b; }
```

```bash
gcc -O0 -c -o lz.o lz.c
objdump -d --no-show-raw-insn -M intel lz.o
```

```
<f>:  endbr64
      push   rbp
      mov    rbp,rsp
      mov    DWORD PTR [rbp-0x14],edi
      mov    DWORD PTR [rbp-0x8],eax
      mov    DWORD PTR [rbp-0x4],eax
      ...
      pop    rbp
      ret
```

*(Verified.)*

**There is no `sub rsp`.** Three locals are being stored *below* `rsp`. **Why is that safe here?**

Now add a call:

```c
int g(int);
int f2(int x) { int a = x+1; return g(a) + a; }
```

Recompile and compare. **The `sub rsp` is back. Explain what changed.**

**✅ CHECKPOINT 4** — both listings and your explanation.

---

## Part 5 — Overwrite a Return Address (20 min)

> **This is a controlled experiment on your own program.** It is the mechanism Week 9 studies as an
> attack; today you do it deliberately, with a debugger, to prove the machine really does work the
> way L10 §1 says.

Break in `fib` and look at the return address:

```
(gdb) break fib if n == 2
(gdb) run
(gdb) x/gx $rbp+8
0x7fffffffd1a8:  0x0000555555555171
```

That is the address `ret` will jump to. **Change it:**

```
(gdb) set {long}($rbp+8) = 0xdeadbeef
(gdb) x/gx $rbp+8
(gdb) continue
```

You should get:

```
Program received signal SIGSEGV, Segmentation fault.
0x00000000deadbeef in ?? ()
```

**`rip` is now `0xdeadbeef`.** Nothing checked. `ret` popped eight bytes off the stack and jumped to them, exactly as advertised.

### 5.1 Make it land somewhere real

Restart and instead point the return address at a function that exists:

```
(gdb) break fib if n == 2
(gdb) run
(gdb) p &main
(gdb) set {long}($rbp+8) = <the address of main>
(gdb) continue
```

**The program re-enters `main`.** No crash, no warning — control flow simply went somewhere the source never says it could.

**Answer in your notes:**

1. What, if anything, in the hardware validates the value `ret` pops?
2. `fib`'s buffer is `n`, at `rbp-0x18`. If a function wrote 0x20 bytes into a local at that offset, which of the saved values would it reach first?
3. Week 9 calls the defence for this a *stack canary*. From what you have seen, where would you put one, and what would you check?

**✅ CHECKPOINT 5** — the `SIGSEGV` at `0xdeadbeef`, the redirect into `main`, and your three answers.

---

## Before You Leave

| Task | Command |
|---|---|
| Backtrace | `bt`, `bt full` |
| One frame's anatomy | `info frame` |
| Move between frames | `frame N`, `up`, `down` |
| Read stack memory | `x/8gx $rsp`, `x/gx $rbp+8` |
| Registers | `info registers rsp rbp rip` |
| One instruction | `stepi`, then `x/i $pc` |
| Break on an address | `break *0xADDRESS` |
| Write memory | `set {long}(ADDR) = VALUE` |

**The habit:** the stack is not an abstraction. It is a region of memory you can print, and every claim in this week's lectures is something you can check with `x/gx`.

---

*CS 201 · Week 3 · Lab 3*

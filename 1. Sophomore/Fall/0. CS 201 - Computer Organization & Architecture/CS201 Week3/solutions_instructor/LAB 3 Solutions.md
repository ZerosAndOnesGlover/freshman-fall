# CS 201 · Lab 3 — Solutions and TA Notes
## Instructor Only

---

> **Unmarked.** Five checkpoints. All GDB transcripts below are real output from the lab image.

---

## Timing

| Part | Budget | Reality |
|---|---|---|
| 1 — build and read | 10 min | 10 min |
| 2 — five frames deep | 25 min | 25 min. `info frame` is the payoff |
| 3 — watch frames build | 20 min | 20 min |
| 4 — red zone | 15 min | 10 min |
| 5 — overwrite the return address | 20 min | **Protect this one.** It is what Week 9 is built on |

**Cut Part 3.1 or Part 4 if short.** Never cut Part 5.

---

## Part 1

Answers:

1. **Prologue:** `push rbp` / `mov rbp,rsp` / `push rbx` — with `sub rsp,0x18` as the fourth.
2. **`n` is at `[rbp-0x18]`.**
3. `call` at `23` (computing `fib(n-1)`) and at `36` (`fib(n-2)`).
4. **`mov rbx,rax` at instruction `28` — it uses `rbx`.**
5. **Epilogue:** `mov rbx,[rbp-0x8]` / `leave` / `ret`.

**Why not leave it in `rax`:** `rax` is caller-saved, and instruction `36` is another `call` which may destroy it. `rbx` is callee-saved, so the callee is obliged to restore it. **This is the entire caller/callee-saved distinction, in one `mov`.**

**✅ CHECKPOINT 1** — listing plus five answers.

---

## Part 2

```
#0  fib (n=2) at fibmain.c:2
#1  0x0000555555555171 in fib (n=3) at fibmain.c:2
#2  0x0000555555555171 in fib (n=4) at fibmain.c:2
#3  0x0000555555555171 in fib (n=5) at fibmain.c:2
#4  0x0000555555555171 in fib (n=6) at fibmain.c:2
#5  0x00005555555551a5 in main () at fibmain.c:3
```

*(Verified.)*

**Why the same return address:** every recursive frame was created by the *same* `call` instruction — the second one, at offset `36`. `0x…171` is the instruction after it. Only `main`'s call site differs.

> Have them find `0x…171` in their Part 1 listing. Recognising that a return address is just "the
> instruction after a particular `call`" is the point.

### 2.1

```
Stack level 0, frame at 0x7fffffffd1b0:
 saved rip = 0x555555555171
 called by frame at 0x7fffffffd1e0
 Saved registers:
  rbx at 0x7fffffffd198, rbp at 0x7fffffffd1a0, rip at 0x7fffffffd1a8
```

*(Verified.)*

**Frame size:** `0x7fffffffd1e0 - 0x7fffffffd1b0 = 0x30 = 48`. Accounted: 8 return address + 8 saved `rbp` + 8 saved `rbx` + 24 (`sub rsp,0x18`).

**Addresses will differ every run — ASLR.** Say so before someone concludes their build is wrong.

### 2.2

With `rbp = 0x7fffffffd1a0`:

| Command | Expected |
|---|---|
| `x/gx $rbp+8` | `0x555555555171` — matches `bt` frame #1 |
| `x/gx $rbp` | caller's `rbp`, = frame #1's `rbp` |
| `x/gx $rbp-0x18` | **`0x2`** — the value of `n` |

**Reading `n` out of memory by address is the moment the frame stops being a diagram.**

**✅ CHECKPOINT 2** — backtrace, 48 bytes accounted, `n` read by address.

---

## Part 3

`rsp` deltas: **−8** (`push rbp`), **0** (`mov rbp,rsp`), **−8** (`push rbx`), **−24** (`sub rsp,0x18`). Total **−40**, plus the 8 pushed by `call` = **48** ✓ consistent with Part 2.

### 3.1

`p $rsp & 15` immediately before a `call` must print **0**.

**Common confusion:** they break *on* the `call` and get 0 (correct — the rule applies before it executes), or they break *after* and get 8. Both are informative; make them say which they did.

> Finding the address of the `call` is fiddly. `disassemble fib` then `break *ADDRESS` is the reliable
> route. `x/i $pc` after breaking confirms they landed on the right instruction.

**✅ CHECKPOINT 3** — four `rsp` values and an alignment check.

---

## Part 4

```
<f>:  push rbp ; mov rbp,rsp ; mov [rbp-0x14],edi ; mov [rbp-0x8],eax ; mov [rbp-0x4],eax ; ... ; pop rbp ; ret
```

*(Verified — no `sub rsp`.)*

**Why safe:** `f` is a **leaf**. The 128 bytes below `rsp` are the **red zone**, reserved for the current function; nothing — not signal handlers, not the kernel — may write there. Three `int`s fit easily.

**With a call added**, the `sub rsp` returns: `f2` is no longer a leaf, and `call g` would push a return address directly over the red-zone locals.

**✅ CHECKPOINT 4** — both listings and the leaf/non-leaf explanation.

---

## Part 5 — the important one

```
(gdb) x/gx $rbp+8
0x7fffffffd1a8:  0x0000555555555171
(gdb) set {long}($rbp+8) = 0xdeadbeef
(gdb) x/gx $rbp+8
0x7fffffffd1a8:  0x00000000deadbeef
(gdb) continue

Program received signal SIGSEGV, Segmentation fault.
0x00000000deadbeef in ?? ()
```

*(Verified — exactly this output.)*

**`rip` is `0xdeadbeef`.** No check, no warning. `ret` popped eight bytes and jumped to them.

### 5.1

Pointing it at `&main` re-enters `main` with no crash at all. **Control flow went somewhere the source says is impossible, and nothing objected.**

### Answers

1. **Nothing.** No hardware validation whatsoever. `ret` is `pop rip`. *(Intel CET's shadow stack, hinted at by `endbr64`, is a later addition that keeps a protected second copy — Week 9.)*
2. **The saved `rbx` at `rbp-8`, then the saved `rbp` at `rbp+0`, then the return address at `rbp+8`.** Writing 0x20 bytes from `rbp-0x18` reaches all three.
3. **A canary goes between the locals and the saved registers** — around `rbp-8`, below the saved `rbp`. It is written on entry and **checked immediately before `ret`**; a mismatch means something overflowed upward through it, and the program aborts rather than returning.

> **Do not skip the discussion after 5.1.** The whole of Week 9 is "an attacker supplies the bytes
> instead of GDB". Students who have done this by hand find that lecture obvious; students who have
> not find it magical.

**Safety note:** this is a controlled experiment on the student's own toy program, in a debugger. It teaches the mechanism a defence protects against. Frame it that way.

**✅ CHECKPOINT 5** — `SIGSEGV` at `0xdeadbeef`, the redirect into `main`, three answers.

---

## What Success Looks Like

1. Read a backtrace and say why recursive frames share a return address.
2. Account for a frame's size from `info frame`.
3. Print any local or saved register by address.
4. Explain the red zone and when it applies.
5. **State that `ret` jumps to unvalidated memory, having done it.**

Item 5 is the one Week 9 depends on.

---

*CS 201 · Week 3 · Lab 3 Solutions · Instructor Only*

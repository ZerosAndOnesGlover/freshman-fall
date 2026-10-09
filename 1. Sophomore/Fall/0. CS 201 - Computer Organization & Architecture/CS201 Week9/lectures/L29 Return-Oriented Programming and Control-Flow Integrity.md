# CS 201 · Computer Organization & Architecture
## Week 9 · Lecture 2 of 3
### Return-Oriented Programming, and Control-Flow Integrity

*“If you think technology can solve your security problems, then you don't understand the problems and you don't understand the technology.”* — Bruce Schneier, *Secrets and Lies*, preface to the 2015 edition

---

**Reading:** CS:APP §3.10.4 · **Previous:** L28, buffer overflows

**Coursework:** 📝 **PS 9** released today, due Fri of Week 10 17:00 · 📋 **Project 1** due Fri this week 17:00 · 📝 **PS 8** due Fri this week 17:00 · 📊 **Quiz 10** Mon of Week 10 · 📘 **Midterm 2** Mon of Week 10 18:00–19:15 · 🔬 **Lab 9** Tue of Week 10 15:00–16:50

---

## 1. The Attacker's Problem After NX

L28 ended with the classic stack smash defeated: **the stack is not executable, so injected bytes cannot run as code.**

**The attacker's response is elegant and it is the reason security is an arms race: if you cannot inject new code, reuse the code that is already there.** Every executable page in the process — the program, and especially libc — is full of instructions that are, by definition, allowed to execute. **NX does not stop you jumping to them.**

This is **code reuse**, and its general form is **Return-Oriented Programming.**

---

## 2. A Gadget Is Any Useful Instruction Ending in `ret`

The building block of ROP is the **gadget**: a short sequence of instructions that happens to be present in the binary and ends in `ret`.

```
pop rdi ; ret          <- loads rdi from the stack, then returns
pop rsi ; ret          <- loads rsi
add rax, rcx ; ret     <- does arithmetic
mov [rdi], rax ; ret   <- writes memory
```

**These are not functions anyone wrote.** They are fragments — often the tail end of a real function, or even bytes in the middle of an instruction reinterpreted at a different offset. The program is full of them because **every function ends in `ret`, and `ret` is one byte (`0xc3`).**

**How full?** Count the `ret` instructions, since each one is a potential gadget terminator:

| Binary | `ret` instructions |
|---|---:|
| `/bin/ls` | **203** |
| **libc** | **6123** |

*(Verified — `objdump -d | grep -c '\bret\b'`.)*

**Six thousand gadget endings in one library that every process links.** That is not a shortage. In practice, the set of gadgets in libc alone is **Turing-complete** — it can express arbitrary computation.

---

## 3. How a Chain Runs

Recall from Week 3 exactly what `ret` does: **pop eight bytes off the stack into `rip`, and jump.**

So if the attacker controls the stack — which a buffer overflow gives them — they control a *sequence* of return targets:

```
   stack (attacker-controlled, via the overflow)
   ┌──────────────────────┐
   │ addr of: pop rdi;ret │ <- ret jumps here
   ├──────────────────────┤
   │ value for rdi        │ <- pop rdi takes this...
   ├──────────────────────┤
   │ addr of: pop rsi;ret │ <- ...then its ret jumps here
   ├──────────────────────┤
   │ value for rsi        │
   ├──────────────────────┤
   │ addr of: system()    │ <- and finally here, with rdi/rsi set up
   └──────────────────────┘
```

**Each gadget's `ret` launches the next.** The overflow does not inject code — it injects a *list of addresses of existing code*, and the chain executes them in order. **The stack has become a program**, and the "instructions" are gadget addresses.

**A common special case is `ret2libc`:** skip the gadgets and return straight into a libc function like `system`, with the argument arranged on the stack. Simpler, and often enough.

> **This is why NX alone did not end memory-corruption attacks.** It stopped *new* code from running,
> and the attacker stopped needing new code. **Every defense motivates the next attack**, and ROP is
> the canonical example — L28's defense created exactly the technique L29 describes.

---

## 4. What Still Stops It

ROP needs two things, and the defenses attack both.

**It needs gadget addresses — and ASLR randomises them.** If libc is at a different address every run (Week 6, verified in L28 §5), the attacker does not know where the gadgets are. **This is why a memory-disclosure bug is worth so much**: leak one libc address and the whole library's gadget layout is de-randomised, because everything in it moves together. Memory *disclosure* (L30) and memory *corruption* (L28) are complementary, and a serious exploit usually chains one of each.

**It needs to redirect control — and Control-Flow Integrity checks where you are allowed to go.**

---

## 5. Control-Flow Integrity

The idea: **an indirect jump, call or return may only land on a target the original program actually intended.** ROP jumps to the *middle* of functions and to gadget tails — places no legitimate control transfer ever targets — so enforcing valid targets breaks it.

**x86-64 has hardware support, and you have already seen half of it.** Every function in your compiled binaries begins with `endbr64`:

```
$ objdump -d -M intel ./prog | grep -c endbr64
14
```

*(Verified.)* **`endbr64` is a landing pad.** Under Intel **CET's indirect-branch tracking**, an indirect call or jump *must* land on an `endbr64`, or the CPU faults. Gadgets in the middle of functions are not preceded by one, so a forward-edge code-reuse jump to them is rejected.

**The backward edge — `ret` — is protected by a shadow stack.** CET keeps a second, hardware-protected copy of every return address that ordinary writes cannot touch. On `ret`, the CPU compares the two; **if the overflow changed the return address on the normal stack, it no longer matches the shadow copy, and the CPU faults.** ROP's entire mechanism — controlling return targets through the stack — is defeated at the source.

> **A caution the machine forces.** `endbr64` landing pads are in your binaries *(verified, 14 of
> them)*, but this lab machine is an i5-8250U from 2017 and **predates hardware shadow-stack
> enforcement** — `grep shstk /proc/cpuinfo` finds nothing here. **So the instructions are present
> and the hardware may not be enforcing them.** This is the honest state of a deployed defense: the
> compiler emits it ahead of the hardware, and enforcement arrives across a fleet over years. Do not
> assume a mitigation is active because the code for it is there — **check.**

---

## 6. The Arms Race, Laid Out

The whole of Weeks 3, 6 and 9 in one ladder:

| Attack | Defense | Attack's response |
|---|---|---|
| Stack smash → inject code | **NX**: stack not executable | **Reuse existing code (ret2libc)** |
| ret2libc → known addresses | **ASLR**: randomise layout | **Leak an address, then compute** |
| ROP → chain gadgets | **CFI / CET**: valid targets only | JOP, sigreturn, data-only attacks… |
| Overwrite return address | **Stack canary**: detect the overwrite | **Leak the canary, or don't cross it** |

**Read it downward and it is thirty years of security research.** Each defense is real and each raised the cost of attack by orders of magnitude. **None is a final answer, and that is the nature of the field:** memory-safety attacks are defeated not by one mechanism but by *layers*, each of which the attacker must defeat simultaneously.

**The actual final answer is upstream.** A language that does not permit the bug — Rust's borrow checker, or a bounds-checked array — removes the vulnerability rather than raising its cost. **Every mitigation in this lecture is compensation for C's permission to write out of bounds**, and Week 12 returns to what that permission costs.

---

## 7. What to Take Away

1. **NX did not end code execution; it ended *new* code.** The attacker reuses existing code.
2. **A gadget is any useful instruction ending in `ret`**, and libc has 6123 of them.
3. **A ROP chain is a stack full of gadget addresses**, each `ret` launching the next — the stack becomes a program.
4. **ret2libc** returns straight into a library function, no gadgets needed.
5. **ASLR breaks ROP by hiding the gadgets**, which is why memory disclosure is worth so much.
6. **CET puts `endbr64` landing pads on the forward edge and a shadow stack on the backward edge** — but check whether the hardware enforces it.
7. **Defenses layer; the real fix is a language that forbids the bug.**

---

## Exercises

1. Why is `ret` (one byte, `0xc3`) so useful to an attacker? Relate it to what Week 3 said `ret` does.
2. libc has 6123 `ret` instructions. Explain why the *usable* gadget count can be even higher than that.
3. Sketch a three-gadget ROP chain that sets `rdi`, sets `rsi`, then calls a function. Draw the stack.
4. ASLR moves libc's base each run. Why does leaking a *single* libc address defeat it entirely?
5. `endbr64` appears at the start of every function. Explain how a shadow stack and landing pads defeat, respectively, the backward and forward edges of control flow.
6. This machine emits `endbr64` but may not enforce a shadow stack. How would you determine whether a given mitigation is actually active on a machine, rather than merely compiled in?

---

*Next: L30 — the bugs that leak memory, and the ones that are not on the stack at all.*

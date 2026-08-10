# CS 201 · Quiz 4
## Administered: Monday, Week 4 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 3** — `call`/`ret`, the stack frame, the System V ABI, alignment and the red zone.

**Instructions:** Closed notes. 10 minutes.

> **Unmarked, no weight.** Key below. Sit it closed-book first.
>
> **Midterm 1 is next week, covering Weeks 0–4.** This quiz is a fair sample of its style.

---

**Q1.** Write `call target` and `ret` as explicit push/pop/jump sequences.

&nbsp;

&nbsp;

---

**Q2.** Name the six integer argument registers, in order.

&nbsp;

&nbsp;

---

**Q3.** `fib` at `-O0` does `mov rbx, rax` immediately after a `call`. Why `rbx` rather than leaving the value in `rax`?

&nbsp;

&nbsp;

---

**Q4.** What is at `[rsp]` at the instant a function's first instruction executes?

&nbsp;

&nbsp;

---

**Q5.** What is `rsp mod 16` on entry to a function, and why is it not 0?

&nbsp;

&nbsp;

---

**Q6.** A leaf function stores three locals with no `sub rsp` at all. Name the feature and give its size.

&nbsp;

&nbsp;

---

**Q7.** Deep recursion eventually crashes. There is no bounds check in `call` — so what actually stops it?

&nbsp;

&nbsp;

---

<div style="page-break-after: always;"></div>

---

## Answer Key — Mark Your Own

**Q1.**

```
call target  ≡  push (address of next instruction) ; jmp target
ret          ≡  pop rip
```

**`ret` does not validate the popped value.** That is the whole of Lab 3 Part 5 and most of Week 9.

---

**Q2.** **`rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`.**

Floating-point arguments use `xmm0`–`xmm7` and are counted **separately** — the two sequences do not interleave. Arguments beyond six go on the stack.

---

**Q3.** **`rax` is caller-saved**, so the *next* `call` may destroy it. The value must survive that call, so it is moved to `rbx`, which is **callee-saved** — the callee is obliged to restore it.

*That is also why the prologue contains `push rbx`: using a callee-saved register means inheriting the obligation.*

*Measured consequence: using `r10` instead compiles and links cleanly, is correct for n = 0…3, and first fails at n = 4, returning 2 instead of 3.*

---

**Q4.** **The return address**, pushed by `call`.

Arguments 7, 8, 9… follow at `[rsp+8]`, `[rsp+16]`, `[rsp+24]`.

---

**Q5.** **`rsp` ≡ 8 (mod 16).**

The ABI requires `rsp` ≡ 0 (mod 16) *immediately before* `call` executes. `call` then pushes 8 bytes, so the callee starts 8 out of alignment. **Each subsequent push flips the parity** — so an odd number of pushes restores alignment and an even number does not.

---

**Q6.** **The red zone. 128 bytes** below `rsp`.

Reserved for the current function; nothing may write there. Two conditions: the function must be a **leaf** (any `call` pushes a return address over it), and it must use no more than 128 bytes.

---

**Q7.** **The guard page.**

`rsp` simply walks downward with no check. Below the stack region the kernel keeps an unmapped page; touching it raises a page fault the kernel cannot satisfy, and it delivers `SIGSEGV`.

*This is also why a single stack frame larger than the guard region can **skip over** it — the "stack clash" bug class.*

---

### What to Do With Your Score

| If you missed | Reread |
|---|---|
| Q1, Q4, Q7 | L10 §1 and §6 |
| Q2, Q3 | L11 §2 and §4 — **the most examinable pair this term** |
| Q5, Q6 | L12 §1 and §3 |

**Q3 and Q5 are the two most likely to appear on Midterm 1.** Q5's parity rule catches almost everyone the first time.

---

*CS 201 · Week 4 · Quiz 4 · covers Week 3 · ungraded*

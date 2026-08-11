# CS 201 · Quiz 10
## Administered: Monday, Week 10 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 9** — memory-safety attacks and their defenses.

**Instructions:** Closed notes. 10 minutes.

> **Unmarked, no weight.** Key below. Sit it closed-book first.
>
> **Midterm 2 is this evening, 18:00, VNC 100 — Weeks 5–9.** This quiz samples the Week 9 portion.

---

**Q1.** A `char buf[16]` sits at `rbp-0x10`. How many bytes of input reach the return address?

&nbsp;

&nbsp;

---

**Q2.** The stack canary is read from `fs:0x28`. Why not from an ordinary local variable?

&nbsp;

&nbsp;

---

**Q3.** NX made the stack non-executable and defeated code injection. What did attackers do instead?

&nbsp;

&nbsp;

---

**Q4.** Why does a single leaked libc address defeat ASLR for all of libc?

&nbsp;

&nbsp;

---

**Q5.** `malloc(count * size)` with attacker-controlled `count`. What is the bug and the fix?

&nbsp;

&nbsp;

---

**Q6.** `printf(user_string)` — what can an attacker read with it, and what can `%n` do?

&nbsp;

&nbsp;

---

**Q7.** A binary has `endbr64` pads, so a colleague says CET protects it. Why is that unsafe to assume?

&nbsp;

&nbsp;

---

<div style="page-break-after: always;"></div>

---

## Answer Key — Mark Your Own

**Q1.** **24 bytes.** `buf` occupies `rbp-0x10` to `rbp-0x1` (16 bytes), the saved `rbp` is the next 8, and the return address follows — 16 + 8 = 24.

---

**Q2.** **`fs:0x28` is thread-local storage** — unreachable through a stack overflow and randomised per process — so an attacker cannot read the value to reproduce it. **A normal local would be overwritten by the same overflow** that reaches the return address.

---

**Q3.** **Code reuse — ret2libc / ROP.** NX stops *new* code from running; it does not stop jumping to code that is already executable. Attackers chain existing instruction fragments ("gadgets", each ending in `ret`) — libc alone has ~6000.

---

**Q4.** **Everything in libc moves together as one unit.** ASLR randomises the base address, not the internal layout, so one leaked address reveals the base and hence the location of every function and gadget. This is why a memory-*disclosure* bug is as valuable as a corruption bug.

---

**Q5.** **Bug: `count * size` can overflow**, wrapping to a small value; `malloc` returns a tiny buffer the caller then overflows — a heap overflow. **Fix: `calloc(count, size)` or `__builtin_mul_overflow`**, which detect the overflow and refuse (return NULL).

---

**Q6.** **`%p`/`%x` read and print values off the stack** — including the canary and libc pointers, defeating both the canary and ASLR. **`%n` writes** the number of bytes printed so far to a pointer argument, turning the bug into an arbitrary memory write.

---

**Q7.** **`endbr64` being present means CET was *compiled in*, not that it is *enforced*.** Enforcement needs CPU support (a shadow stack), the kernel, and the process's opt-in. On older hardware — including this lab's 2017 CPU, which reports no `shstk` — the landing pads exist but nothing enforces them. **Verify with `/proc/cpuinfo`; do not assume.**

---

### Before Tonight

| If you missed | Reread |
|---|---|
| Q1, Q2 | L28 §2, §4 |
| Q3, Q4 | L29 §1–§4 |
| Q5, Q6 | L30 §2–§3 |
| Q7 | L29 §5 |

**The whole paper covers Weeks 5–9 — see the Midterm 2 revision guide** for the six ideas and the numbers table. **Q5 and Q7 above are the two Week-9 points most likely to appear.**

---

*CS 201 · Week 10 · Quiz 10 · covers Week 9 · ungraded*

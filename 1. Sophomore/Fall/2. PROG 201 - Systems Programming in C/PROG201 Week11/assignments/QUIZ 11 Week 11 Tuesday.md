# PROG 201 · Quiz 11
## Administered: Tuesday, Week 11 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 10** — memory-safety bugs, the exploit/defence pairs, and finding bugs before attackers do.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **PS 11 is due Friday** — build a mini-container and measure its boundary.

---

**Q1.** In one sentence: what is a stack buffer overflow, and which two things adjacent to a local array does overrunning it let an attacker reach?

&nbsp;

&nbsp;

---

**Q2.** A canary catches the overflow in Lab 10 but the same input walks straight through the un-hardened build. What is the canary, where does it sit, and how does the check know it was overwritten?

&nbsp;

&nbsp;

---

**Q3.** NX/no-execute makes the stack non-executable, so your shellcode-on-the-stack attack dies. What does ROP do instead, and what is a "gadget"?

&nbsp;

&nbsp;

---

**Q4.** Your ret2libc chain reaches `system()` and then crashes on a `movaps` instruction. Nothing is wrong with your addresses. What is the fix, and why is a *bare `ret`* the thing that fixes it?

&nbsp;

&nbsp;

---

**Q5.** ASLR is enabled system-wide (`randomize_va_space` = 2) and yet your exploit's hard-coded addresses work every run. Give the two reasons this can happen in the course setup.

&nbsp;

&nbsp;

---

**Q6.** A format string `printf(user_input)` with no arguments. What does an attacker read with `%p`, and what does `%n` let them do that is far worse?

&nbsp;

&nbsp;

---

**Q7.** libFuzzer finds the Lab 10 parser bugs in seconds; a week of hand-written test cases found none. What is coverage-guided fuzzing doing that your test cases were not, and what is the one-line lesson connecting it to the recurring "a mechanism present is not a mechanism working" theme?

&nbsp;

&nbsp;

---

&nbsp;

---
---

## Answer Key

**Q1.** A **stack buffer overflow** is writing past the end of a fixed-size local array so the write spills into adjacent stack memory. It reaches, going up the frame, the **saved registers / stack canary**, and — the prize — the **saved return address**, so controlling it means controlling where the function returns. *(L31 §1–§2.)*

---

**Q2.** The **stack canary** is a random value the compiler places **between the local buffers and the saved return address** at function entry (loaded from `%fs:0x28`), and checks just before `ret`. An overflow that reaches the return address must first overwrite the canary; the epilogue compares the on-stack value to the original and calls `__stack_chk_fail` (abort) if they differ. The un-hardened build was compiled `-fno-stack-protector`, so there is no canary to disturb — **the same input, one flag apart, is caught or not caught.** *(L31 §3.)*

---

**Q3.** **ROP — return-oriented programming** — chains together tiny snippets of *existing, already-executable* code instead of injecting new code, so NX (which only stops *new* code on the stack) is bypassed. A **gadget** is a short instruction sequence ending in `ret` (e.g. `pop rdi; ret`); the stack is filled with a sequence of gadget addresses and data, and each `ret` jumps to the next, letting you set up registers and call functions. *(L32 §1–§3.)*

---

**Q4.** Prepend a **bare `ret` gadget** before the call so the stack is realigned. `system()` (via glibc) uses SSE instructions like `movaps`, which **fault unless `rsp` is 16-byte aligned**; a ROP chain's returns can leave `rsp` off by 8. One extra `ret` consumes 8 bytes and restores 16-byte alignment — **the addresses were never wrong, the stack alignment was.** *(L32 §5.)*

---

**Q5.** Either (1) the binary is **not position-independent** (`-no-pie`), so the *executable itself* — including the `unlock`/`win` function and its gadgets — loads at a **fixed address** that ASLR does not touch (ASLR randomises the stack, heap, libraries, and PIE executables, not a non-PIE image); or (2) the course runs the target under **`setarch -R`**, which sets `ADDR_NO_RANDOMIZE` for that process only, disabling randomisation for the exercise **without** changing the machine-wide `randomize_va_space`. Both are the same lesson: **ASLR present is not ASLR protecting you** if the thing you jump to isn't randomised. *(L31 §5, L32 §4.)*

---

**Q6.** `%p` **reads** — it walks up the stack/registers printing whatever the varargs machinery *thinks* were arguments, leaking stack contents, canaries, and addresses (defeating ASLR). `%n` **writes** — it stores the number of bytes printed so far to the address in the corresponding argument slot, giving an attacker an **arbitrary memory write** from nothing but a format string. Read is bad; a controllable write is game over. *(L33 §1–§2.)*

---

**Q7.** Coverage-guided fuzzing **instruments every branch and keeps inputs that reach new code**, then mutates those — so it *searches* the input space toward unexplored paths instead of sampling points you already imagined; your hand tests only ever exercised the paths you already thought of. The lesson: **having tests is not the same as having tested the code that matters** — the same shape as "a mechanism present is not a mechanism working" (Week 3 PRIO_INHERIT, Week 8 lazy binding, Week 10 inert CET), and its companion, *a measurement that produces nothing — a green test suite over untested branches — is a fact about the measurement, not proof of correctness.* *(L33 §4–§5.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L31 §1–§3 — you built both halves in Lab 10 |
| Q3, Q4 | L32 §1–§5 — PS 10's working chain |
| Q5 | L31 §5, L32 §4 — the ASLR/PIE/`setarch` trio |
| Q6 | L33 §1–§2 |
| **Q7** | **L33 §4–§5** — the one that recurs |

**Q5 and Q7 are the ones that recur**, and Week 11 turns the same lens on containers: you will build isolation with `clone()`, and the way you will know it is real is by *measuring* what it stops — PID, network — and, just as importantly, measuring exactly where this machine's isolation is **present but not working** (`mount` and `sethostname` refused to a namespace-root whose capabilities have been stripped).

---

*PROG 201 · Week 11 · Quiz 11 · covers Week 10 · ungraded*

# CS 201 · Week 9 · Reading Guide
## Security — Attacks and Defenses

---

**Set reading:** CS:APP **§3.10** in full — especially §3.10.3 (buffer overflow) and §3.10.4 (thwarting attacks). Re-read **§2.3** (integer arithmetic) with security eyes.
**Also:** `man 3 printf` (the `%n` note), and the AddressSanitizer documentation.
**Optional:** Aleph One, *"Smashing the Stack for Fun and Profit"* (1996) — the foundational paper, and now a historical document.

---

## The Frame for This Reading

**This is a defensive course, and CS:APP treats it that way.** §3.10 exists so that you understand your programs well enough not to write the bug, and so the defenses make sense. **Read it to learn where C lets you shoot yourself, and how the toolchain now stops the bullet.**

Everything in this chapter reuses earlier material: the stack frame (§3.7, Week 3), the instruction set (Week 2), and virtual memory (Week 6). **If any of the attacks feel like magic, the gap is usually in one of those, not in the security content.**

---

## Section by Section

| § | Topic | What to take from it |
|---|---|---|
| **2.3** *(revisit)* | Integer arithmetic | Re-read as a source of vulnerabilities. `a * b` can wrap; L30 §2 |
| **3.10.1–3.10.2** | Pointers, GDB | Warm-up; you have done this since Week 0 |
| **3.10.3** | **Out-of-bounds writes and buffer overflow** | **The core.** The frame, the return address, the exploit |
| **3.10.4** | **Thwarting buffer overflow attacks** | **Canaries, NX, ASLR.** L28 in the book's words |
| **3.11** | Floating point in machine code | Not security; skip for this week |

**The book predates CET/CFI and treats ASan only lightly.** L29 and L30 fill both gaps — the book's defenses are canary, NX and ASLR; the lectures add control-flow integrity and the sanitizer.

---

## Questions to Read Against

**On §2.3 revisited**

1. `malloc(count * size)` with attacker-controlled `count`. Show the value at which the multiply wraps to a small number. What does the allocation then do?
2. Why does `calloc(count, size)` not have this bug? What does it check that `malloc(count*size)` cannot?

**On §3.10.3**

3. For a `char buf[N]` at a known frame offset, derive the number of bytes to the return address. Do it for the book's example and for L28's (`buf` at `rbp-0x10`).
4. The book's exploit injects code into the buffer. **Why does that specific technique no longer work?** Name the defense.
5. Getting the return address to point at chosen code is necessary but not sufficient for a working exploit. Give **two** further obstacles. *(One is in §3.10.4; one is from Week 3 §L12.)*

**On §3.10.4 — the defenses**

6. The canary is placed between the locals and the saved state. **Why there?** What overflow does that placement catch, and what does it miss?
7. ASLR randomises the stack, heap and library base each run. **What does a single leaked address cost the defense?**
8. NX makes the stack non-executable. State the attack it stops and the attack it does **not** stop (that is L29).

**Beyond the book**

9. A memory-*disclosure* bug leaks bytes but corrupts nothing. **Argue that it is as dangerous as a corruption bug**, naming the two defenses it defeats.
10. `-fsanitize=address` finds bugs the runtime defenses only *contain*. What is the difference between *finding* a bug in testing and *containing* it at runtime, and why do you want both?

> **Question 5 is the one that separates understanding from recitation.** Anyone can describe
> overwriting a return address; knowing why that is the *start* of the difficulty — null bytes, stack
> alignment, unknown addresses — is the real content.

---

## Reading Against the Machine

```bash
# 1. See the canary the compiler inserted by default
gcc -O0 -g -o vuln vuln.c
objdump -d -M intel vuln | grep fs:0x28

# 2. Watch ASLR
for i in 1 2 3; do ./prog_that_prints_&main; done      # different each time
setarch -R ./prog_that_prints_&main                    # frozen

# 3. THE important one — find a bug before it ships
gcc -O0 -g -fsanitize=address,undefined -Wall -Wextra yourcode.c
```

**Item 3 is the week's practical takeaway.** Add those flags to your own projects. *(Verified this week: ASan named a stack overflow at its exact line and a use-after-free at both the free and the misuse.)* **Nearly every attack in §3.10 began as a warning or a sanitizer report that nobody ran.**

**One honesty check the book cannot give you:** a defense being *compiled in* is not the same as it being *enforced*. This machine emits `endbr64` landing pads but its 2017 CPU does not enforce a CET shadow stack (`grep shstk /proc/cpuinfo` is empty). **Verify mitigations, do not assume them.**

---

## Terminology You Should Own by Week 10

| | | |
|---|---|---|
| buffer overflow | out-of-bounds write | stack smashing |
| return address | shellcode | code injection |
| stack canary | `__stack_chk_fail` | `fs:0x28` |
| NX / DEP / W^X | ASLR | PIE |
| code reuse | ret2libc | ROP gadget |
| CFI | CET | `endbr64` / shadow stack |
| integer overflow | checked multiply | format string |
| `%n` | use-after-free | double-free |
| heap metadata | TOCTOU race | AddressSanitizer |
| defence in depth | memory disclosure | trust boundary |

---

## If You Want More

**"Smashing the Stack for Fun and Profit"** (Aleph One, Phrack 49, 1996) is where this all began. **Read it as history** — its techniques are mostly defeated now, and seeing *why* each was defeated is the best summary of §3.10.4 there is.

**The OWASP Top Ten** is the web-application counterpart — injection, broken access control, and the rest. **Different bugs, same mindset**: trust no input, and think about what the code can do.

**Julia Evans' zines** on `strace`, `ss` and debugging are the friendliest introduction to the tools this course uses, and her post on AddressSanitizer is a good five-minute start.

**The Rust ownership model** is worth an hour even if you never write Rust, because it is the clearest example of *designing the vulnerability out* rather than mitigating it — which is the argument Week 12 closes on.

---

*CS 201 · Week 9 · Reading Guide*

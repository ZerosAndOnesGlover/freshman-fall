# CS 201 · Computer Organization & Architecture
## Week 9: Security — Attacks and Defenses

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), ECE 110 (digital logic)
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** PS 9 (due Week 10 Friday), Lab 9 *(sat Tuesday of Week 10)*, and **Quiz 9 on Monday, covering Week 8**.

> **Project 1 (mini-CPU simulator, 10%) was due last Friday.** If you have not submitted, it is now
> late — see the late policy in `COURSE POLICIES.md`.

---

### A Note on What This Week Is

**This is a defensive week.** You learn how memory-safety attacks work so that you can write code that is not vulnerable and understand the mitigations that protect the code you cannot rewrite.

**Every demonstration runs on a small program you compile yourself**, in the lab directory, with the defenses toggled so their effect is visible. Nothing targets a system you do not own. **The genuine takeaway is constructive: `-fsanitize=address` and `-Wall -Werror` find these bugs before they ship, and for your own code that is the whole answer.**

---

### Why This Week Exists

Because everything the course has built is also an attack surface, and you cannot defend what you do not understand.

A buffer overflow is Week 3's stack frame with one missing bounds check. ROP is Week 2's instruction set and Week 6's virtual memory turned against the program. A format-string leak is Week 8's data-versus-code confusion reading Week 3's stack. **Security is not a topic bolted on at the end — it is what the whole machine looks like to someone who wants to misuse it**, which is exactly why it comes after eight weeks of learning how the machine really works.

The week is also the course's clearest example of an **arms race**: every defense — NX, ASLR, canaries, CET — motivated the next attack, and the real resolution is upstream, in a language that forbids the bug rather than mitigating it.

---

### Learning Objectives

By the end of Week 9, you should be able to:

1. Explain a stack buffer overflow in terms of the frame layout, and derive the offset to the return address.
2. Recognise the stack canary in a disassembly and explain why it is read from `fs:0x28`.
3. Explain what NX, ASLR and the canary each deny an attacker — and that none fixes the bug.
4. Explain why code injection no longer works and what replaced it.
5. Explain ROP: gadgets, the chain, and why NX did not stop it.
6. Explain CET's landing pads and shadow stack, and **check whether a mitigation is enforced or merely compiled in.**
7. Recognise the integer-overflow allocation bug and fix it with a checked multiply.
8. Recognise a format-string vulnerability and explain the leak and the `%n` write.
9. Explain use-after-free, double-free and TOCTOU races as security bugs.
10. **Use AddressSanitizer and the compiler's warnings to find these bugs in testing.**
11. State the security mindset: trust no input, read what code can do, layer defenses.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L28 The Stack Under Attack.md` | The overflow, the canary, NX and ASLR — each measured, and how to write the bug out |
| `lectures/L29 Return-Oriented Programming and Control-Flow Integrity.md` | Gadgets, ROP, ret2libc, and CET — with the "compiled in ≠ enforced" caution |
| `lectures/L30 Integer Overflows Format Strings and the Security Mindset.md` | The bugs that are not on the stack, and the habit of thought behind all of them |
| `assignments/PS 9 Memory Safety and Its Defenses.md` | The defenses, the arms race, and **four vulnerable functions to fix and prove** |
| `assignments/QUIZ 9 Week 9 Monday.md` | Ten minutes on Week 8. **Unmarked — key in the paper** |
| `lab/LAB 9 Defenses at Work.md` | See the canary, watch an overwrite in GDB, and **find bugs with the sanitizer** |
| `resources/Reading Guide Week 9.md` | CS:APP §3.10, §2.3 revisited, and what the book predates |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**The cheapest place to stop an exploit is before it ships — and the tools are free.**

The runtime defenses are impressive: the canary aborts an overflow (`*** stack smashing detected ***`, verified); NX makes the stack non-executable; ASLR moves every address each run. **But those are for the binary you cannot fix.** For your own code:

```
$ gcc -fsanitize=address -g vuln.c && ./a.out "$(python3 -c 'print("A"*40)')"
ERROR: AddressSanitizer: stack-buffer-overflow
  [32, 48) 'buf' (line 3) <== Memory access at offset 48 overflows this variable
```

*(Verified.)* **It names the buffer, the line, and the exact overflowing byte.** Nearly every attack in this week began as a warning someone ignored or a sanitizer nobody ran. **`-Wall -Werror -fsanitize=address,undefined` turns most of Week 9 into a compile error.**

---

### Assessment Reminder

**Labs and quizzes carry no weight**; the four weighted components already total 100%. Both remain required.

**Quiz 9 is Monday**, covering Week 8. **Lab 9 is sat Tuesday of Week 10.**

**PS 9 is a fix-the-bug assignment.** Q3 gives you four vulnerable functions to **repair and prove repaired** with a sanitizer — the marked artefact is safe code with evidence, not an attack. **Midterm 2 is next week (Weeks 5–9)**; this week is on it.

---

### Connections

**Back:** **Week 3** is the whole foundation — the frame, `ret` jumping to unvalidated memory, and the alignment rule that makes exploits fiddly. **Week 1's integer overflow** becomes the heap-corruption bug. **Week 2's instruction set** is the gadget supply. **Week 6's NX bit and page tables** are the defenses. **Week 8's untrusted input** is where attacks arrive.

**Forward:** **Week 10's Spectre** — from Week 5 — is a hardware security flaw of the same family. **PROG 201's ROP and fuzzing labs** go deeper into exploitation. **CS 341 (Computer Security) in Year 3** is this week for a semester, with cryptography and protocols.

**Sideways:** **CS 290 (Ethics & Society II)** this spring covers the responsible-disclosure and accountability side of exactly these vulnerabilities.

---

*CS 201 · Week 9 · © CSE Department*

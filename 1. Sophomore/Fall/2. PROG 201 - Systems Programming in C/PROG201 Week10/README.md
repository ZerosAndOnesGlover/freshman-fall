# PROG 201 · Systems Programming in C
## Week 10: Security — Systems-Level Attacks and Mitigations

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101; CS 201 as co-requisite
**Assessment for this course (overall):** Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%
**This week's deliverables:** PS 9 (due Friday), PS 10 (released Wednesday, due Friday of Week 11) and **Quiz 10** (Tuesday, covers Week 9).
**Lab 9 is sat on the Monday of this week**; **Lab 10 covers this week and is sat on the Monday of Week 11.**

> ### **Everything this week is sandboxed, on binaries the course provides.**
> The targets are compiled with protections removed on purpose and run under `setarch -R`, which
> disables address randomisation **for that one process** — the machine-wide setting is never
> touched. None of it is a technique for a system you were not handed. The reason to build the
> attacks is that **a mitigation you have not watched fail is one you will misconfigure**, and
> [[PROG 201 Scheduling Notes]] records the sandbox and the four tools that had to be substituted.

---

### Why This Week Exists

Because Week 8 left a writable GOT and Week 1 left a `gets`, and this is the week where you see what an attacker does with them — and, more to the point, what each defence added over thirty years actually stops.

The whole week is a sequence of measured pairs: the **same** input, with a protection off and then on. An overflow that spawns a shell becomes an abort. Shellcode that runs becomes a SIGSEGV. A chain that works becomes a crash. **Those pairs are the argument** — you cannot reason about defence in depth from a diagram, only from watching each layer cost the attacker a separate capability.

Three ideas:

1. **A stack buffer and the return address are adjacent memory**, and every defence since 1996 is a different way to protect the eight bytes between them.
2. **Each mitigation forces the next attack.** NX forced code reuse (ROP); ASLR forced information leaks; and no single layer is enough while all of them together are genuinely hard.
3. **The cheapest exploit to defend against is the bug that never shipped** — so the developer's half of the week (sanitizers, fuzzing) matters more than the production half (canary, NX, ASLR, CFI), even though the production half is the famous part.

---

### Learning Objectives

By the end of Week 10, you should be able to:

1. Explain how a stack overflow reaches the saved return address, and find the offset.
2. Say what a stack canary protects, and what it does not (index writes, leaks, lower-frame targets).
3. Explain why NX stops shellcode and why that created ROP.
4. Explain why ASLR needs PIE, and what an information leak buys an attacker.
5. **Build a ROP chain** from gadgets, control a register, and reach a target — and know why it is NX-clean.
6. Diagnose the stack-alignment `movaps` crash and fix it with a `ret` gadget.
7. Describe ret2libc and the general four-part shape of an exploit.
8. Explain CFI and shadow stacks, and say why this CPU's CET markers are inert.
9. **Explain the format-string bug** as a read (`%p`) and a write (`%n`) primitive, and how the read defeats ASLR.
10. Recognise that heap bugs are silent without a sanitizer, and use AddressSanitizer to catch them.
11. **Fuzz a parser** with libFuzzer, and explain why coverage guidance beats random input.
12. Describe the modern development loop: warnings, sanitizers, fuzzing, mitigations.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L31 The Stack the Overflow and the Defences]] | The overflow and the offset; **the canary turning a shell into exit 134**; **NX turning shellcode into a SIGSEGV**; **ASLR missing non-PIE code** so the chain still works, and **PIE closing it**; how the four layers compose |
| [[L32 Return-Oriented Programming]] | Gadgets and why NX forced them; **a 40-line gadget finder** because ROPgadget isn't installed; **a CET-compiled libc with zero clean `pop rdi` gadgets**; **a measured 3-gadget chain spawning a shell, uid=1000**; the `movaps` alignment bug; ret2libc; **CFI catching a type-confused call**; the **inert CET markers** on this CPU |
| [[L33 Format Strings Heap Bugs and Finding Them]] | `%p` reads (defeats ASLR) and `%n` writes; **heap bugs that run silently** without a sanitizer; **ASan catching use-after-free and double-free** with both sites named; **libFuzzer replacing AFL**, coverage-guided, finding a planted bug at `parser.c:15` from 13 bytes; the modern loop |
| [[LAB 10 Fuzzing a Parser]] | Find three planted bugs by fuzzing; coverage-guided against dumb; what the sanitizer buys. **Monday of Week 11** |
| `lab/parser.c`, `lab/fuzz_parser.c`, `lab/run_one.c`, `lab/heap.c`, `lab/fmt.c`, `lab/Makefile` | The fuzzing target and the L33 demos |
| [[PS 10 A Working ROP Chain]] | Build a real ROP chain in the sandbox, then turn each defence back on and watch it work. Due **Friday of Week 11** |
| `assignments/ps10/` | `vuln.c`, the `gadget.py` finder, a 10-line `checksec.sh`, and the Makefile |
| [[PROG201 Week10/assignments/QUIZ 10 Week 10 Tuesday\|QUIZ 10 Week 10 Tuesday]] | Ten minutes, covers **Week 9**, answer key printed |
| [[PROG201 Week10/resources/Reading Guide Week 10\|Reading Guide Week 10]] | Aleph One, Shacham, CS:APP §3.10, and the defence docs |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Watch the defence fail before you trust it — every result this week is a measured pair.**

| Protection | Exploit with it OFF | Exploit with it ON |
| --- | --- | --- |
| **Stack canary** | shell (uid=1000) | `*** stack smashing detected ***`, exit 134 |
| **NX** (shellcode attack) | runs on an exec stack | **SIGSEGV**, exit 139 |
| **NX** (ROP attack) | shell — ROP is NX-clean | *unchanged* — NX does not touch ROP |
| **ASLR without PIE** | shell | **still a shell** — ASLR misses the code |
| **PIE + ASLR** | shell | SIGSEGV — the chain's addresses are wrong |
| **CFI** (indirect call) | jumps into `evil()` | "control flow integrity check … failed" |
| **Shadow stack** | shell | *would* catch it — **but this CPU has no CET**, so the `endbr64` markers are inert |

**Read the ASLR-without-PIE row and the shadow-stack row together.** They are the two that catch people: a defence can be *on* and do nothing (ASLR without PIE leaves the code fixed), and a defence can be *compiled in* and do nothing (CET markers with no hardware to enforce them). Both are the same lesson as Week 3's `PRIO_INHERIT` and Week 8's lazy binding — **a mechanism that is present is not the same as a mechanism that is working**, and the only way to tell is to run the thing it is supposed to stop.

---

### Assessment Reminder

**Labs and quizzes carry no weight** and are still required. **Quiz 10 is at the start of Tuesday's lecture and covers Week 9.** **PS 9 is due this Friday.**

> **Lab 9** — Week 9's roofline — is sat on the **Monday of this week**. **Lab 10** covers this week
> and is sat on the **Monday of Week 11**. There is no midterm this week.

Both are tracked in [[_PROG 201 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 1's `gets`** is the bug. **Week 4's NX and `mprotect`** are the defence ROP walks around, and **Week 8's writable GOT** is the `%n` write's favourite target. **Week 4's ASLR and PIE** are L31 §5, now from the attacker's side. **Week 3's `PRIO_INHERIT`** is the template for "present but inert" — here it is the CET markers.

**Sideways:** **CS 201 Week 10 is on the machine-level view of the stack** — the call/ret mechanism ROP subverts is its calling-convention lecture, read as an attack surface.

**Forward:** **Week 11's containers** are the isolation you wrap around a program you cannot trust not to have every bug this week exploited — namespaces and seccomp are defence in depth at the OS level. **Week 12's project** is a daemon that must survive hostile input, which is this week's developer loop applied end to end.

---

*PROG 201 · Week 10 · © CSE Department*

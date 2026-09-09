# PROG 201 · Reading Guide · Week 10
## Two 1990s papers everyone in security has read, and the modern defence docs

---

**This week's foundation is two short papers from the 1990s** that named the attacks, and a set of
current documentation that describes the defences. The papers are free, famous, and readable in an
evening each; read them for the *reasoning*, because the specific offsets are 30 years stale but the
structure is not.

| Source | Read? | Why |
|---|---|---|
| **Aleph One, *Smashing the Stack for Fun and Profit* (Phrack 49, 1996)** | **All of it** | The stack overflow, named. L31. Ignore the 32-bit details; keep the shape |
| **Shacham, *The Geometry of Innocent Flesh on the Bone* (CCS 2007)** | **§1–§3** | ROP, and the proof it is Turing-complete. L32 |
| **CS:APP §3.10.3–3.10.4** | **All of it** | Buffer overflows and the three defences, in the textbook's own attacklab framing |
| Roemer, Buchanan, Shacham & Savage, *Return-Oriented Programming* (2012) | Read | The survey. Gadgets, chains, and the defences as of a decade in |
| scut/team-teso, *Exploiting Format String Vulnerabilities* (2001) | **Read** | L33 §1. The `%n` write primitive, in full |
| The **AddressSanitizer** paper (Serebryany et al., 2012) | Skim | How the shadow memory and red-zones work. L33 §2 |
| The **libFuzzer** and **AFL** docs | Read one | Coverage-guided fuzzing. L33 §3, Lab 10 |

---

## Aleph One — read for the shape, not the addresses

1. The paper injects shellcode onto the stack and returns into it. **That attack no longer works** — which defence stopped it, and in what year did it become the default? *(L31 §4.)*
2. He finds the offset by trial and error with increasing padding. Compare with the cyclic-pattern method. What does a De Bruijn sequence give you that guessing does not?
3. The shellcode does `execve("/bin/sh")`. Write down the four things it has to set up for that syscall, and check them against the 23-byte shellcode in L31 §4.

## Shacham — read §1–§3 for the argument

4. §2 defines a gadget. Why must it end in `ret` specifically, and what plays the role of the program counter when a chain runs? *(L32 §1.)*
5. §3 argues Turing-completeness by exhibiting gadgets for load, store, arithmetic and branch. You do not need to follow every gadget — **state why "we removed the executable stack" does not stop any of it.**
6. The paper finds its gadgets in libc. L32 §2 found *zero* clean `pop rdi ; ret` gadgets in this machine's libc. What changed between 2007 and now, and what does that do to the difficulty of the attack?

## CS:APP §3.10 — the textbook version

7. Figure 3.40's stack layout. Draw your own for the course's `vuln`, with the offset you found in PS 10 Q1 marked.
8. The book's three protections are the randomisation, the non-executable stack, and the canary. **Which one does CS:APP not cover that this week does, and why does it matter more than the other three combined?** *(Hint: it is the one that makes the others moot when it is absent — the leak. And the one added since the book: CFI / shadow stack.)*

---

## The Defence Documentation

9. `gcc`'s `-fstack-protector`, `-fstack-protector-strong`, `-fstack-protector-all`. What does *strong* protect that plain does not, and why is *all* rarely used?
10. The **`-fcf-protection`** manual page and Intel CET. What are the two halves (shadow stack and indirect-branch tracking), and what does `endbr64` do — when the hardware supports it, and when it does not? *(L32 §5.)*
11. clang's **CFI** (`-fsanitize=cfi`) docs. Why does it need `-flto`, and what exactly does "control flow integrity check for type '...' failed" mean? *(L33 has the measured message.)*
12. `_FORTIFY_SOURCE` — levels 1, 2, 3. Which format-string and buffer functions does it harden, and why is it not a substitute for the compile-time `-Werror=format-security`?

---

## The Man Pages for This Week

| Page | The paragraph |
|---|---|
| **`man 1 setarch`** | `-R` / `--addr-no-randomize`. The one flag the whole sandbox rests on |
| **`man 3 printf`** | The `%n` note, and the warning about untrusted format strings |
| **`man 5 proc`** | `randomize_va_space`: 0, 1, 2 |
| `man 1 objdump` | `-d`, and reading the gadget bytes yourself |
| `man 7  elf` | `GNU_STACK`, `GNU_RELRO`, and the segment flags `checksec` reads |

**And two commands that answer most of the week:** `readelf -l BINARY` (the segment permissions — NX and RELRO live here) and `objdump -d BINARY | grep -c endbr64` (whether the CET markers are present, which they are, whether or not the CPU enforces them).

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **Nergal, *The advanced return-into-lib(c) exploits* (Phrack 58, 2001)** | ret2libc before ROP had a name |
| Bittau et al., *Hacking Blind* (BROP, 2014) | Building a ROP chain with **no** copy of the binary, by crashing and observing |
| Szekeres, Payer, Wei & Song, *SoK: Eternal War in Memory* (2013) | The best single map of every attack and every defence in this week |
| **pwn.college** and the **CS:APP attacklab** | Hands-on, staged, and exactly this week's shape. If you want more targets |
| Google **OSS-Fuzz** | Coverage-guided fuzzing run continuously on thousands of real projects |
| The **Pwnie Awards** and any CTF writeup archive | What these techniques look like against real, unsandboxed targets — read, do not reproduce |

---

## The Habit for This Week

**Watch the defence fail before you trust it.**

Every earlier week's habit was an instrument. This week's is a stance, and it is the reason the course teaches attacks at all:

- You do not understand a stack canary until you have seen the identical overflow it converts from a shell into an abort.
- You do not understand NX until you have watched shellcode SIGSEGV and then watched ROP walk around it.
- You do not understand why PIE matters until you have run the *same* exploit against a non-PIE binary (works) and a PIE one (fails).
- You do not understand a shadow stack until you know your own CPU is not enforcing one, and can say what would change if it were.

**A mitigation you have only read about is a mitigation you will misconfigure.** The measured pairs in these lectures — exploit-then-abort, shellcode-then-ROP, works-then-fails — are the whole argument, and the only way to build the judgement that decides, in real code, which protections you actually need on.

**And the ethics are part of the habit, not an appendix to it.** The sandbox, the course-supplied binary, and `setarch -R` are what make this legitimate; the same commands against a system you were not given are a crime, and the skill this week teaches is worth having precisely because it is used to *defend*.

---

*PROG 201 · Week 10 · Reading Guide · © CSE Department*

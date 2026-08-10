# CS 201 · Week 2 · Reading Guide
## CS:APP Chapter 3 — Machine-Level Representation of Programs

---

**Set reading:** Bryant & O'Hallaron, **§3.1–3.6**. §3.7 is Week 3.
**Reference:** Intel SDM Volume 2 — the instruction reference. **Do not read it; learn to look things up in it.**

---

## A Warning About the Book's Syntax

**CS:APP uses AT&T syntax throughout.** This course writes Intel. That is not the book being wrong — AT&T is what GCC emits, and CS:APP is a GCC-centric book.

**Do not fight it.** Read the book in AT&T, write Intel, and let Lab 2 Part 4 make the mapping automatic. The one rule that matters:

> **AT&T:** `op src, dest` · **Intel:** `op dest, src`

If you find yourself confused about which register a `mov` writes, check the syntax marker before anything else.

---

## Section by Section

| § | Topic | What to take from it |
|---|---|---|
| **3.1** | A historical perspective | Skim. Useful for why x86-64 looks the way it does |
| **3.2** | Program encodings | **Read §3.2.2 properly** — it is Lab 0's `objdump` workflow, written down |
| **3.3** | Data formats | The `b`/`w`/`l`/`q` suffixes. You need these to read the book's listings |
| **3.4.1** | Operand specifiers | **The core of L07.** Figure 3.3 is the addressing-mode table — copy it out by hand |
| **3.4.2** | Data movement | `mov`, `movz`, `movs`. The zero/sign-extension variants matter |
| **3.4.3** | Data movement example | Work through it |
| **3.4.4** | Pushing and popping | Week 3's material, but read it now — it makes the stack concrete |
| **3.5** | Arithmetic and logical | **L08.** Note §3.5.5 on special arithmetic (the double-width `imul`, `cqto`/`cdq`, `idiv`) |
| **3.6.1** | Condition codes | **L09 §1.** The four flags |
| **3.6.2** | Accessing condition codes | `setcc` |
| **3.6.3** | Jump instructions | The signed/unsigned jump split |
| **3.6.4–3.6.5** | Jump encodings, conditionals | PC-relative encoding — Week 0's `7e ee` again |
| **3.6.6** | Conditional moves | `cmov`, and **when it is a loss** |
| **3.6.7** | Loops | The rotated-loop form you saw in Week 0 |
| **3.6.8** | Switch statements | Jump tables. **The book shows one strategy; Lab 2 finds four** |

---

## Questions to Read Against

**On §3.4 — operands**

1. Figure 3.3 lists nine operand forms. Which of them can `lea` use, and which cannot? Why?
2. `movzbl` and `movsbl` both widen a byte to 32 bits. When does the choice change the answer? Give a concrete byte value.
3. Why does writing to `%eax` zero the upper 32 bits of `%rax`, while writing to `%ax` does not? *(The book states it; the reason is a design decision made in 2003. What was it trying to avoid?)*

**On §3.5 — arithmetic**

4. The book gives `imul` in one-, two- and three-operand forms. Which produces a 128-bit result, and where does it go?
5. **Compile `int f(int x){return x/7;}` at `-O2` and find no division.** Work out the magic constant the way L08 §4 does for 10, and check it.
6. Why does the book present `cqto` (AT&T) where the Intel manuals say `cqo`? Are they the same instruction?

**On §3.6 — control**

7. §3.6.1 says `cmp` and `test` set flags without storing a result. Which flags does `test` **always** clear, and why does that follow from what it computes?
8. For a signed comparison the book gives `jl` as SF^OF. Construct operand values where SF and OF differ, and confirm `jl` branches correctly.
9. §3.6.6 argues `cmov` is not always a win. Give the two conditions under which a branch beats a conditional move.
10. §3.6.8's jump table uses absolute addresses. **Lab 2 found GCC emitting 32-bit relative offsets instead.** Why the difference? *(Hint: what year is the book's example from, and what does PIE change?)*

> **Question 10 is the best one here.** It is a case where the textbook is right about the concept and
> out of date about the output, and noticing that gap is the whole skill this course is building.

---

## Reading Against the Machine

```bash
# 1. Every operand form in Figure 3.3 — write one C function per form and check
gcc -O1 -c -o modes.o modes.c && objdump -d -M intel modes.o

# 2. The instruction the book says exists — look it up in the SDM
#    Try: what does `setg` do when the operands were unsigned? Find the answer
#    in Intel SDM Vol. 2B under SETcc, not by guessing.

# 3. Find the division that is not there
gcc -O2 -c -o d.o d.c && objdump -d -M intel d.o | grep -A6 '<div7>'
```

**Item 2 is the skill.** By Week 3 you should be able to answer "what exactly does this instruction do to the flags?" by finding the page, not by experimenting. The SDM's instruction reference is alphabetical, and each entry has a "Flags Affected" section.

---

## Terminology You Should Own by Week 3

| | | |
|---|---|---|
| operand specifier | immediate / register / memory | effective address |
| base, index, scale, displacement | RIP-relative | relocation |
| `lea` | zero-extend vs sign-extend | operand size suffix |
| ZF, SF, CF, OF | signed vs unsigned jump | `setcc`, `cmov` |
| jump table | branch target | rotated loop |
| fixed-point reciprocal | magic number | truncation vs floor |

---

## If You Want More

**Intel SDM Volume 2** — the instruction set reference. Bookmark it. The entries for `IMUL`, `IDIV`, `LEA`, `SETcc` and `Jcc` are the ones you will actually open this term.

**Agner Fog's instruction tables** give latency and throughput per instruction per microarchitecture. Not needed yet; essential in Week 11. Skim now so you know it exists — it is where "`idiv` is slow" turns into a number.

**Matt Godbolt's Compiler Explorer** shows source and assembly side by side, live, for dozens of compilers. **Use it for exploration, not for the lab** — the point of Lab 2 is that you can do this with `objdump` on your own machine, which is where you will need it when there is no browser.

---

*CS 201 · Week 2 · Reading Guide*

# CS 201 · Project 1
## A Mini-CPU Simulator

---

**Assigned:** Week 7 · **Due:** Week 9, Friday 17:00
**Weight: 10% of the course grade** · Individual work
**Submit:** a `.zip` of source plus a PDF report, `PROJ1_{LastName}_{StudentID}.pdf`

> **This is the first of two projects.** Project 2, due Week 12, extends this one into a pipelined
> simulator with a cache. **Design for that now** — the marks for Project 2 assume you are building
> on this rather than restarting.

---

## What You Are Building

A **functional simulator** for a small subset of x86-64: it reads a program, executes it instruction by instruction, and produces exactly the architectural state a real CPU would.

**Functional, not timing.** It must get the *answers* right. Project 2 adds the pipeline that gets the *timing* right.

**Why this project.** Everything in Weeks 0–5 has been observation — you read what the compiler emitted and measured what the hardware did. **This is the first time you build the thing you have been observing**, and writing a fetch-decode-execute loop is the fastest way to find out which parts you actually understood.

---

## Required Functionality

### 1. Machine state

- **16 general-purpose 64-bit registers**, `rax` … `r15`, addressable at 64/32/16/8 bits.
- **`rip`**, and the four flags **ZF, SF, CF, OF**.
- **A flat memory**, at least 1 MiB, byte-addressable and little-endian.
- **A stack**, with `rsp` initialised near the top of memory.

**The 32-bit write rule from L03 §4 must be implemented**: writing a 32-bit register zeroes the upper 32 bits; 16- and 8-bit writes do not. **Marks are lost for getting this wrong**, and it is the single most common defect.

### 2. Instruction set

Enough to run real compiled code:

| Group | Instructions |
|---|---|
| **Move** | `mov` (reg/imm/mem, all four widths), `movzx`, `movsx`, `lea` |
| **Arithmetic** | `add`, `sub`, `imul`, `neg`, `inc`, `dec` |
| **Logic** | `and`, `or`, `xor`, `not`, `shl`, `shr`, `sar` |
| **Compare** | `cmp`, `test` |
| **Control** | `jmp`, `je`/`jne`, `jl`/`jle`/`jg`/`jge`, `jb`/`jbe`/`ja`/`jae` |
| **Procedure** | `call`, `ret`, `push`, `pop` |
| **Conditional** | `setcc`, `cmovcc` — at least two of each |
| **Halt** | `hlt`, ending the simulation |

**Addressing modes:** the full `[base + index*scale + disp]`, with scale ∈ {1,2,4,8}.

**`idiv` and `cdq` are optional** and carry bonus marks — see below.

### 3. Input format

**Choose one and document it.** Either is acceptable:

- **A simple textual assembly** you parse yourself, in Intel syntax. *(Easier; most people should do this.)*
- **Raw x86-64 machine code**, decoded from bytes. *(Much harder; see the bonus.)*

Your submission must include **at least six test programs** in your chosen format, one per group above.

### 4. Required output

```
$ ./cpusim program.asm --trace
```

- **`--trace`**: one line per instruction — `rip`, the instruction, and any register or flag that changed.
- **On halt**: final register file, flags, and a count of instructions executed.
- **`--stats`**: instruction counts by category, and the number of taken and not-taken branches.

---

## Verification — 20% of the project mark

**A simulator that runs is not a simulator that is right.** You must demonstrate correctness against the real machine.

**For at least four of your test programs:**

1. Assemble and run the same code natively — `nasm -f elf64` plus a small C driver, as in Lab 2.
2. Run it under your simulator.
3. **Compare the final register values** and show they match.

**Include the comparison in your report as a table.** A program whose native and simulated results differ, with an explanation of why, is worth more than one you quietly omitted.

> **The most productive test is the recursive Fibonacci from PS 3.** It exercises `call`, `ret`,
> `push`, `pop`, callee-saved registers, the stack and conditional branches simultaneously, and if
> your stack handling is wrong it will give you a specific wrong number rather than a crash.

---

## Report — 25% of the project mark

**Four to six pages.** Not a user manual.

| Section | What it must contain |
|---|---|
| **Design** | How you represent state, decode, and dispatch. Why you chose that structure |
| **The flags** | How you compute ZF, SF, CF and OF, **and how you tested them**. Which cases were hardest |
| **Verification** | Your native-vs-simulated table, and any discrepancy you found |
| **What surprised you** | At least one thing you believed before writing this that turned out to be wrong |
| **Toward Project 2** | Which parts you expect to change when a pipeline and cache are added |

**The "what surprised you" section is marked seriously.** Every previous cohort has had one — a flag computed backwards, `cmp` misunderstood as writing a register, the 32-bit zeroing rule, the direction of stack growth. **Naming yours is evidence of the thing this project is for.**

---

## Marking

| | |
|---|---:|
| **Correctness** — instructions execute correctly, all widths, flags right | **35** |
| **Coverage** — the required instruction set and addressing modes | **20** |
| **Verification** — native comparison, documented, at least four programs | **20** |
| **Report** | **25** |
| **Total** | **100** |

### Bonus, up to +10 (capped at 100)

| | |
|---|---:|
| Decode **real machine bytes** rather than text assembly | +6 |
| `idiv`/`cdq` correct, **including the missing-`cdq` failure mode** from L08 §3 | +2 |
| A working `--step` debugger with breakpoints and memory inspection | +2 |

---

## Milestones

You have three weeks. **The failure mode is leaving it to Week 9.**

| By end of | Have working |
|---|---|
| **Week 7** | Registers, memory, `mov`, `add`, `hlt`, and a trace. **One program running end to end** |
| **Week 8** | Flags, `cmp`, all the jumps, and your first native comparison |
| **Week 9** | `call`/`ret`/`push`/`pop`, `setcc`/`cmov`, the remaining tests, and the report |

**A simulator that does five instructions perfectly and is verified against hardware scores better than one that does thirty and was never checked.** Correctness and verification are 55 of the 100 marks.

---

## Practical Advice

**Write the trace output first.** You will read thousands of lines of it, and a good trace format is worth more than any other single decision.

**Test the flags in isolation.** They are where the marks and the bugs are. Write a table of operand pairs with expected ZF/SF/CF/OF — including `0x80000000 - 1` from Midterm Q2(c) — and assert against it.

**Do not optimise.** A `switch` on an opcode enum is correct and fast enough. Project 2 is where performance enters, and only for the simulated machine.

**Keep decode separate from execute.** Project 2 splits them across pipeline stages, and a simulator that fused them is a simulator you will rewrite.

---

*CS 201 · Project 1 · assigned Week 7, due Week 9 · 10%*

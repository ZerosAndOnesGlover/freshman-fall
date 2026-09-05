# CS 211 · Reading Guide · Week 11
## Language Implementation: A Complete Mini-Compiler

**Project 1 is due Friday.** Read nothing until it is submitted. What follows is short on purpose, and the LLVM Language Reference is a reference — you look things up in it, you do not read it.

---

## Before Tuesday (L23 — the whole compiler)

| Source | Section | Why | Pages |
|---|---|---|---|
| **Dragon** | **§1.2–1.3** | The phases, revisited now that you have written them. Twenty minutes, and it will read completely differently than it did in Week 0. | 8 |
| **LLVM Language Reference** | "Introduction", "Identifiers", "Instruction Reference" for `alloca`, `load`, `store`, `getelementptr`, `phi`, `icmp`, `br` | **Look these up as you read our IR**, not in advance. | — |

**Read our own output first.** `python3 cyanc.py gcd.cy --emit=llvm` is forty lines and you wrote the compiler that produced it; that is a better introduction to LLVM IR than any prose.

---

## Before Thursday (L24 — LLVM and JIT)

| Source | Section | Why | Pages |
|---|---|---|---|
| **Lattner (AOSA ch. 11)** | all | "LLVM," in *The Architecture of Open Source Applications*. **The best account of the m×n → m+n argument**, by the person who made it. Free at aosabook.org. | 14 |
| **Lattner & Adve (2004)** | §1–3 | The original paper. §2 is the IR's design rationale. | 10 |
| **LLVM Kaleidoscope tutorial** | ch. 1–4 | Building a small language front end, in the shape `llvmgen.py` already has. **Ch. 4 is the JIT** and is what Lab 11 is a Python-flavoured version of. | 20 |
| **LLVM** | "Garbage Collection with LLVM" | Only if you are attempting PS 11 Part C. It is the answer to "what does a front end owe a precise collector". | 8 |

---

## Papers, If You Want Them

- **Cytron et al. (1991)** — SSA construction and dominance frontiers. **This is what `mem2reg` runs**, and Week 4 assigned it once already. Worth a second look now that you can see its output.
- **Deutsch & Schiffman (1984)** — inline caching in Smalltalk-80. Where the central JIT idea comes from.
- **Hölzle, Chambers & Ungar (1991)** — polymorphic inline caches. The refinement every modern JIT uses.
- **Aycock (2003)**, "A Brief History of Just-In-Time." A readable survey, and it starts in 1960.

---

## The One Thing Worth Reading Twice

**Lattner, AOSA ch. 11, the section on the three-phase design.**

Read it, then run:

```bash
for t in aarch64 riscv64 wasm32 avr; do
  printf "%-9s " $t; llc -march=$t -filetype=asm -o /tmp/o.s /tmp/gcd_o.ll && grep -cE '^\s+[a-z]' /tmp/o.s
done
```

8, 16, 23, 124 — **from the IR your compiler emitted.**

The chapter makes the architectural argument. What it does not do is let you *feel* the asymmetry: we wrote a front end for a language we invented over eleven weeks, and received in exchange a code generator for an 8-bit microcontroller that none of us could have written and none of us needed to.

**Then read the assembly.** `riscv64` emits `call __moddi3` because the base RISC-V ISA has no divide instruction. That single line tells you more about what a back end does than the chapter does.

---

## A Note on Reading Your Own Compiler

The most valuable reading this week is not on this list. It is `cyanc.py --emit=` at each stage, on a program you wrote, watching one representation become the next.

Nine phases, eight of them yours:

```
source → tokens → AST → typed AST → TAC → CFG → optimised → liveness → registers → LLVM IR
```

**You have read about every one of these transformations in a textbook.** The difference between having read about them and understanding them is being able to point at a specific `%t7` in the IR and say which Cyan expression it came from, through five intermediate representations.

That skill is what the final exam tests, and it is what an employer means by "knows how compilers work". **It is also, more immediately, what Project 1's report is marked on.**

---

*CS 211 · Week 11 · Reading Guide · © CSE Department*

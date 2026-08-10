# CS 201 · Computer Organization & Architecture
## Course Overview & Week-by-Week Road-map
### Year 2 · Fall · 4 credits (3 lecture + 1 lab)

---

## The Course

**CS 201 answers the question every serious programmer eventually asks: what does the computer actually do when I run my code?**

You will descend from C into x86-64 assembly, and then further — into registers, the ALU, the cache, and the pipeline. By the end you will know **why floating-point arithmetic produces surprising results, why some loops run ten times faster than others, what a buffer overflow does at the binary level, and how a multi-core CPU keeps its caches consistent.**

**Prerequisites:** PROG 101 (C) and ECE 110 (digital logic). Both are assumed, not re-taught. ECE 110 built an ALU out of gates; this course starts one layer above that and never goes back down.

---

## Two Habits This Course Is Built Around

**1. Read the machine, do not imagine it.**

Every claim in this course about what the hardware does is checkable, and you will check it. `objdump` shows you the instructions the compiler actually emitted. `gdb` shows you the registers as they change. `perf` and `valgrind` count what really happened rather than what should have. **When a lecture asserts a number, the command that produced it is printed next to it.**

> The single most common failure mode in this course is arguing from a mental model of the compiler
> instead of from its output. The mental model is wrong more often than you would guess — Lab 0 ends
> with a case where GCC deletes a hundred-million-iteration loop entirely and prints the answer as a
> constant.

**2. The abstraction is a contract, and contracts have costs.**

Each layer — transistors, gates, ISA, C, Python — exists to hide the one below it. Hiding is not free. **Your job as an engineer is to know what each layer costs you and when the cost is worth paying**, which means being able to break through a layer when the price gets too high, and being able to say *why* you did.

---

## Assessment

| Component | Weight | Rule |
|---|---|---|
| **Problem Sets** | **35%** | PS 0–12, released Wednesday, due the following Friday 17:00. Lowest 1 dropped. |
| **Midterm 1** *(Week 5)* | **12.5%** | 75 minutes, covering **Weeks 0–4**. One handwritten sheet, one side. |
| **Midterm 2** *(Week 10)* | **12.5%** | 75 minutes, covering **Weeks 5–9**. Same format. |
| **Project 1** *(due Week 9)* | **10%** | Mini-CPU simulator. |
| **Project 2** *(due Week 12)* | **10%** | Full pipelined CPU simulator with a cache. |
| **Final Exam** | **20%** | 150 minutes, comprehensive. Two handwritten pages. |
| **Total** | **100%** | |

**Labs and quizzes carry no weight.** The curriculum's assessment line — *Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%* — sums to 100% without them, and no percentage has been invented to fill the gap.

**They are still required.** The lab is checked off by the TA in the session, and `COURSE POLICIES.md` costs you a letter grade after a second unexcused absence. That rule, not a mark, is what makes the lab non-optional — because a lab you can skip for a 2% grade cost is a lab you will skip in the week you are busiest, which is reliably the week the material is hardest.

**Quizzes** run ten minutes at the start of Monday's lecture in **Weeks 1–11**. **Quiz *N* covers Week *N−1*.** The answer key is printed in the paper, below the questions, so the feedback closes in the same sitting rather than three weeks later.

Both are recorded in `5. Academic Registry/2. Gradebook/Year2 Sophomore/Fall/_CS 201 Lab and Quiz Record.md`.

---

## Schedule

| | When | Where |
|---|---|---|
| **Lectures** | Monday, Wednesday, Friday 08:30–09:20 | VNC 101 |
| **Lab** | Tuesday 15:00–16:50 *(mandatory)* | BH 210 |
| **Office hours** | Monday 13:00–15:00, Wednesday 11:00–12:00 | TH 420 |

### The lab runs one week behind the lectures — deliberately

**Lab *N* covers Week *N* but is sat on the Tuesday of Week *N+1*.**

Lectures are Monday, Wednesday and Friday; the lab is Tuesday. A Tuesday lab in the same week would have had only Monday's lecture, and every lab in this course needs all three — Lab 4 uses Friday's blocking material, Lab 5 uses Friday's SIMD material. **So the lab deliberately lags by a week.**

| Lab | Covers | Sat on |
|---|---|---|
| **Lab 0** | Week 0 | **Friday of Week 0** — the Friday that closes the ten-day Week 0. Setup only, so it needs no lead time |
| Lab 1 | Week 1 | Tuesday of Week 2 |
| Lab *N* | Week *N* | Tuesday of Week *N+1* |
| Lab 11 | Week 11 | Tuesday of Week 12 |
| **Lab 12** | Week 12 | **Demo day**, in the completion period (Dec 8–12) |

**There is no lab session in Week 1** — Lab 0 was sat the Friday before, and Lab 1 waits for Week 1's lectures to finish.

**Quizzes do not lag.** Quiz *N* is sat at the start of **Monday's lecture in Week *N*** and covers **Week *N−1***, which is the same convention CS 102 used in Year 1. Every quiz and lab file states both its day and its week in the header; if you are ever unsure, the file itself is authoritative.

**Instructor:** Prof. Emmanuel Obi · e.obi@ist.edu · TH 420
**TA:** Felix Oduya · foduya@ist.edu · Mon 16:00–18:00 and Fri 15:00–17:00, BH 120

---

## Tools

Everything runs on Linux (Ubuntu 24.04 in BH 210). You will use:

| Tool | For | Preinstalled? |
|---|---|---|
| `gcc` | compiling, and `-S` for assembly output | ✅ |
| `objdump` | disassembling what was actually emitted | ✅ |
| `gdb` | stepping instructions, reading registers | ✅ |
| `perf` | cycle and cache-miss counts (Weeks 4, 11) | ✅ |
| `valgrind` | `cachegrind` for cache simulation, `memcheck` for memory errors | ✅ |
| `nasm` | hand-written assembly (Weeks 2–3) | ✅ 2.16.01 |

**Check the toolchain in Lab 0 regardless** — if you are working on your own machine rather than BH 210, `nasm` is the one that is usually missing (`sudo apt install nasm`).

Note that `gcc` and `objdump` default to **AT&T syntax** while `nasm` uses **Intel syntax**; Week 2 spends real time on the difference, and until then this course writes Intel and passes `-M intel` to `objdump`.

---

## Textbooks

**Bryant, R. & O'Hallaron, D. — *Computer Systems: A Programmer's Perspective*, 3rd ed. (Pearson, 2016).**
*Primary text — "CS:APP". The systems programmer's view of the machine rather than the hardware engineer's. Read every chapter; this course is built on it.*

**Patterson, D. & Hennessy, J. — *Computer Organization and Design (RISC-V Edition)*, 2nd ed. (Morgan Kaufmann, 2020).**
*Secondary. Broader on the hardware, and the RISC-V contrast is genuinely clarifying when x86-64's irregularity starts to feel arbitrary.*

**Intel 64 and IA-32 Architectures Software Developer's Manual** (free, intel.com).
*The authoritative ISA reference. You are not expected to read it; you are expected to be able to look something up in it by Week 3.*

**Hennessy, J. & Patterson, D. — *Computer Architecture: A Quantitative Approach*, 6th ed. (Morgan Kaufmann, 2017).**
*Graduate-level. For depth on pipelining and the memory hierarchy in Weeks 5 and 10.*

---

## Week by Week

| Week | Topic | The question it answers |
|---|---|---|
| **0** | From Transistors to Programs | What is actually underneath a program? |
| **1** | Data Representation — integers and IEEE 754 | Why is `0.1 + 0.2 != 0.3`, and what else is like that? |
| **2** | x86-64 Assembly Language | What instructions does the machine really have? |
| **3** | Procedures, the Stack, Calling Conventions | How does a function call work, mechanically? |
| **4** | Memory Hierarchy — caches | Why is one loop ten times faster than another? |
| **5** | Pipelining and ILP · **MIDTERM 1** | How does a CPU run more than one instruction at once? |
| **6** | Virtual Memory | How does every process get its own address space? |
| **7** | I/O Systems and Storage · **Project 1 assigned** | Why is the disk the slowest thing you will ever touch? |
| **8** | Computer Networks Fundamentals | How does a byte get to another machine? |
| **9** | Security — attacks and defenses · **Project 1 due** | How does a buffer overflow take control? |
| **10** | Multi-Core and GPU · **MIDTERM 2** | What breaks when two cores share memory? |
| **11** | Performance Engineering | How do you make it faster on purpose rather than by luck? |
| **12** | Architecture Frontiers · **Project 2 due** | Where does performance come from now that Moore's Law has stopped? |

---

## What This Course Feeds

**Immediately:** PROG 201 runs alongside it and assumes it — the process, the address space, and the calling convention are CS 201 material used as PROG 201 vocabulary. CS 202 in Spring assumes both.

**Later:** ECE 311 (Computer Architecture II) extends Weeks 5 and 10 into superscalar and speculative execution. CS 341 (Computer Security) extends Week 9 into formal cryptography and protocols. CS 302 (Networks) extends Week 8 into the whole stack.

---

## Deviations From the Curriculum

Recorded here so a reader meets them without needing `5. Build Records/`:

| What | Why |
|---|---|
| **Midterm 1 sits in Week 5, not a shared Week 6 exam week** | The curriculum docx places it in Week 5 covering Weeks 0–4, inside that week's own assignment list. The registry had stacked four courses' midterms into Week 6. The docx is authoritative for its own year, and the date — Oct 6 — did not change. |
| **Labs and quizzes are unweighted** | The docx's four components already reach 100%. Rather than invent a weight, CS 201 follows the ECE 110 and CS 102 precedent: required, recorded, unmarked. |
| **CUDA work in Week 10 is written for simulation first** | The docx lists CUDA, and BH 210 has no GPUs. Lab 10 runs against a CPU-side reference implementation with the CUDA path documented and tested separately; nothing in the assessed work requires hardware you do not have. |

---

*CS 201 · Year 2 Fall · © CSE Department*

# ECE 110 · Digital Logic
## Course Overview & Week-by-Week Road-map
### Digital Logic & Circuit Design · Year 1 · Spring · 3 credits (2 lecture + 1 lab)

---

## The Course

**ECE 110 builds the bridge between software and hardware.** You will design logic circuits — combinations of AND, OR, NOT, NAND, NOR gates — that compute functions, store bits, and form the building blocks of CPUs.

By the end you will understand **how an adder is built from gates, how a flip-flop stores one bit of state, and how a finite state machine is implemented in hardware.** This course is what makes computer architecture in Year 2 fully comprehensible.

**Prerequisites:** none. *(PHYS 141, taken concurrently, is helpful but not assumed.)*

---

## Two Habits This Course Is Built Around

**1. The truth table is the ground truth.**

A circuit that looks right is not a circuit that is right. Every design in this course is checked **exhaustively** — for a 4-input function that is 16 rows, and you check all 16. **Where exhaustive checking is infeasible you will be told what the argument replacing it is**, and why it is sound.

> Several of the most instructive bugs in the course — the SR latch's forbidden state, a K-map
> grouping that is correct but not minimal, a Verilog block that simulates differently from the
> hardware it describes — **are invisible to inspection and obvious to simulation.**

**2. Gates and delay are the cost.**

Every design question in digital logic reduces to two numbers: **how many gates**, and **how long is the longest path through them**. You will count both, every week, for every circuit you build.

> A ripple-carry adder is correct at any width. Its delay grows **linearly** with width, and that
> single fact is why real processors do not use one. **Correctness is the entry fee; cost is the
> subject.**

---

## Assessment

| Component | Weight | Rule |
|---|---|---|
| **Laboratory** | **25%** | 13 labs, Weeks 0–12. No drops — the lab is a third of the contact hours. |
| **Problem Sets** | **35%** | PS 0–11, released Thursday 14:30 after Lecture 2, due the following Thursday 13:00. Lowest 1 dropped. PS 12 is an ungraded self-check (answers Fri 16 Apr), because a due date after Week 12 would fall after the final. |
| **Midterm Exam** *(Thu 4 Mar, 18:00–19:15, Week 6)* | **25%** | 75 minutes, covering **Weeks 0–5**. One handwritten sheet, one side. |
| **Final Exam** *(Mon 19 Apr, 08:00–10:00)* | **15%** | 120 minutes, comprehensive. Two handwritten pages. |
| **Total** | **100%** | |

**Weekly quizzes are ungraded.** A short quiz runs at the start of Wednesday's lecture (13:00) in **Weeks 2–12**, covering the previous week. It carries no weight and exists so that you and I both find out what has not landed while there is still time.

> **Note on the registry.** The `MASTER TIMETABLE` breakdown above is authoritative for this course.
> The `ASSESSMENT CALENDAR` previously listed the final at 30%; that has been corrected to 15% to
> match. The curriculum docx specifies no weights for ECE 110.

---

## Schedule

| | When | Where |
|---|---|---|
| **Lecture 1** | Wednesday 13:00–14:15 | MEC 101 |
| **Lecture 2** | Thursday 13:00–14:15 | MEC 101 |
| **Lab** | Friday 14:00–15:50 *(mandatory)* | MEC 110 |

**The lab section is not optional and is not a drop-in.** Breadboards, logic gates and oscilloscopes are provided; the simulation work is done in Python and, from Week 10, in Verilog.

---

## Textbooks

**Harris, D. & Harris, S. — *Digital Design and Computer Architecture*, 2nd ed. (Morgan Kaufmann, 2012).**
*Primary text. The best bridge from gates to a working CPU, and the one Year 2 will assume you have read.*

**Mano, M. & Ciletti, M. — *Digital Design*, 5th ed. (Pearson, 2013).**
*Secondary. More traditional and more thorough on minimisation; use it when Harris moves too fast.*

---

## Week by Week

| Week | Topic | The question it answers |
|---|---|---|
| **0** | Number Systems — binary, octal, hex, conversions, BCD | How does a machine hold a number? |
| **1** | Boolean Algebra — axioms, theorems, De Morgan's Laws | What algebra do circuits obey? |
| **2** | Logic Gates — AND, OR, NOT, NAND, NOR, XOR, XNOR | What are the primitives? |
| **3** | Combinational Circuits — half adder, full adder, ripple-carry adder | How do you *add* with gates? |
| **4** | Karnaugh Maps and Logic Minimization | How do you make it smaller? |
| **5** | Decoders, Encoders, Multiplexers, Demultiplexers | What are the reusable blocks? |
| **6** | Arithmetic Logic Units — ALU design · **MIDTERM** | How do you build the part that computes? |
| **7** | Latches and Flip-Flops — SR, D, JK, T | How does a circuit *remember*? |
| **8** | Registers, Counters, and Shift Registers | How do you remember more than one bit? |
| **9** | Finite State Machines — Mealy and Moore | How does a circuit *decide over time*? |
| **10** | VHDL/Verilog — hardware description languages | How is this written down at scale? |
| **11** | Memory Circuits — SRAM, DRAM, ROM | Where do the bits actually live? |
| **12** | Programmable Logic — PLAs, FPGAs · Review · **FINAL** | How is logic built without a fab? |

---

## What This Course Is Not

**It is not a physics course.** Transistors appear only where they explain a digital behaviour you would otherwise have to memorise — why NAND is cheaper than AND, why a DRAM cell must be refreshed. **Analogue circuit analysis is not assessed.**

**It is not a programming course.** Verilog arrives in Week 10 as a *description* language. If you write it thinking in loops and variables you will describe hardware you did not intend, and Week 10 is largely about that trap.

---

## Where It Goes

| This course | Next |
|---|---|
| Gates, adders, ALU | **CS 201** — Computer Organization & Architecture *(Year 2, Fall)* |
| Flip-flops, FSMs, timing | **CS 201**, then **ECE 311** — Computer Architecture II |
| Signals behind the digital abstraction | **ECE 211** — Signals and Systems *(Year 2, Spring)* |
| Verilog, FPGAs | **CS 434** — Embedded Systems Engineering |

**CS 201 assumes this course.** It opens with an instruction set and a datapath, and the datapath is made of the blocks you build here.

---

## Academic Integrity

**Discuss problem sets; write them alone.** Lab work is done in pairs and **both partners submit their own report** — a shared report is a shared zero.

**Simulation output is evidence.** If you report that a circuit works, the table or waveform showing it must be in your submission. **An unsupported claim is marked as though the claim were false.**

---

*ECE 110 · Digital Logic & Circuit Design · Year 1 Spring*

# ECE 110 · Digital Logic
## Week 12 · Lecture 2 (Thursday)
### Review and the Road Ahead

*“The technology at the leading edge changes so rapidly that you have to keep current after you get out of school. I think probably the most important thing is having good fundamentals.”* — Gordon Moore, interview in *Ingenuity* 5(2) (2000)

**Date:** Thursday 15 April 2027 · 13:00–14:15 · Week 12

**Coursework:** 📝 **PS 11** due today 13:00 · 📝 **PS 12** released today 14:30 · 🔬 **Lab 12** Fri 16 Apr 14:00–15:50 · 📕 **Final exam** Mon 19 Apr 08:00–10:00

---

**Reading:** Harris & Harris, the Summary at the end of Chapters 1–5 | Mano & Ciletti — none
**The FINAL EXAM** is comprehensive, Weeks 0–12, 120 minutes, two handwritten pages. **The revision guide is in `resources/`.**

---

## 1. Thirteen Weeks In One Picture

$$\text{bits} \to \text{gates} \to \text{combinational blocks} \to \text{arithmetic} \to \text{memory} \to \text{machines} \to \text{silicon}$$

| weeks | you built |
|---|---|
| 0 | how a machine holds a number |
| 1–2 | the algebra, and gates that obey it |
| 3 | an adder |
| 4–5 | how to make it smaller, and the reusable blocks |
| 6 | **an ALU** |
| 7–8 | memory of one bit, then many |
| 9 | **a machine that decides over time** |
| 10 | how to describe all of it in text |
| 11–12 | where the bits live, and logic without a fab |

> **Weeks 6 and 9 together are a processor's two halves** — the datapath that computes and the
> control unit that decides. **CS 201 puts them together and calls the result a CPU.**

---

## 2. The One Question, Asked Every Week

**Almost every design decision in this course reduced to the same question: *which cost am I paying?***

| week | the trade |
|---|---|
| 0 | BCD: **37% more bits** for exact decimal |
| 2 | NAND rebuilds: **more transistors** for library uniformity |
| 3 | ripple adder: **cheap in area, unusable in time** |
| 4 | minimisation: 43 gates → 7 — **area only, no speed** |
| 5 | LUT vs gates: **design effort vs silicon** |
| 6 | carry-lookahead: **2× area for 10.8× speed** |
| 8 | synchronous counter: **gates for correctness and speed** |
| 11 | DRAM: **4.5% refresh overhead for 6× density** |
| 12 | FPGA: **~10× speed, ~20× area** for configurability |

> **Not one of those was answered by "which is better".** Every one was answered by measuring both
> costs and naming which was scarce. **That is the habit the course is actually teaching.**

---

## 3. The Numbers Worth Keeping

| | |
|---|---|
| CMOS: NOT 2, NAND/NOR 4, AND/OR 6, XOR 12 transistors | *AND costs more than NAND* |
| $t_{\text{ripple}} = 2N+1$ gate delays | *129 at 64 bits* |
| 64-bit CLA: **12** gate delays | *10.8× faster, 2× the area* |
| $T_{clk}\ge t_{cq}+t_{\text{logic}}+t_{su}$ | *376 MHz vs 3.13 GHz* |
| SRAM 6T, DRAM 1T, flip-flop ~20T | *the memory hierarchy in one row* |
| DRAM refresh: 7.81 μs/row, 4.5% | *rising with device size* |
| $2^{2^n}$ functions of $n$ variables | *$1.8\times10^{19}$ at $n=6$* |

---

## 4. Three Habits

**1. Check exhaustively.** A 4-bit adder has 512 input combinations and you checked all of them. **A circuit that passes four tests has passed four tests.** *(Lab 3: four bench readings is 0.78% of the input space.)*

**2. Suspect the checker.** Three times this term the *test* was wrong, not the design — a 1-bit loop counter that never terminated, a width mismatch that reported 240 phantom failures, an unpulsed reset that left the state undefined. **When your checker fires, check the checker first.**

**3. Name the cost you are paying.** Gate count is area. Critical path is speed. **They are different, they trade against each other, and a design decision without a named cost is a preference.**

---

## 5. Where This Goes

| this course | next |
|---|---|
| gates, adders, ALU, FSMs | **CS 201** — Computer Organization & Architecture *(Year 2, Fall)* |
| flip-flops, timing, memory | **CS 201**, then **ECE 311** — Computer Architecture II |
| the analogue truth under the abstraction | **ECE 211** — Signals and Systems *(Year 2, Spring)* |
| Verilog, FPGAs, the flow | **CS 434** — Embedded Systems Engineering |
| minimisation, covering, NP-hardness | **CS 301** — Theory of Computation |

> **CS 201 opens with an instruction set and a datapath, and the datapath is made of the blocks you
> built here.** The register file is Week 8. The ALU is Week 6. The control unit is Week 9. **The
> cache exists because of Week 11's 50× SRAM/DRAM gap.**
>
> **You will recognise all of it.**

---

## 6. What The Course Was Actually About

**Not gates. Gates are a week's material.**

> **It was about the fact that "it works" is the beginning of an engineering argument, not the end.**
>
> Your ripple adder worked. It was unusable. Your ripple counter worked, and glitched a decoder into
> corrupting memory. Your latch worked, and raced. Your Verilog simulated perfectly and described a
> different circuit from the one that would be built.
>
> **Every one of those was correct and inadequate**, and finding out required measuring something.

**That is the habit. The gate counts will fade.**

---

## 7. What To Take From This Lecture

1. **Weeks 6 and 9 are a processor's two halves.**
2. **Every week asked which cost you are paying.** None answered "which is better".
3. **Check exhaustively; suspect the checker; name the cost.**
4. **CS 201 is this course assembled**, and you will recognise every block.
5. **"It works" is where the argument starts.**

---

*Next: the FINAL EXAM. Revision guide in `resources/` — and read the Course Retrospective afterwards.*

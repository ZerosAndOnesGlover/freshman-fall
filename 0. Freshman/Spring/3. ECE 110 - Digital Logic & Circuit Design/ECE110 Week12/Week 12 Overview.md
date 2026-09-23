# ECE 110 · Digital Logic
## Week 12 · Overview
### Programmable Logic — PLAs, FPGAs · Review · **FINAL EXAM**

---

**Topic:** logic without a fab
**Reading:** Harris & Harris §5.6 | Mano & Ciletti §7.6–7.8
**Assessment this week:** PS 12 (released Thu 15 Apr 14:30 — **ungraded self-check**, answers Fri 16 Apr), Lab 12 (**Fri 16 Apr**, 14:00), **Quiz 11** *(Wed 14 Apr, 13:00 — covers Week 11, ungraded)*, and the **FINAL EXAM** *(Mon 19 Apr, 08:00–10:00)*

---

## ⚠ The Final Exam

**Monday 19 April 2027, 08:00–10:00 (finals week). 120 minutes. Comprehensive — Weeks 0–12. Two handwritten pages. No calculator. 15% of the course.**

**A full revision guide is in this week's `resources/` folder.** Topic map for all thirteen weeks, the errors that recurred, a two-page sheet plan, and a sample paper with worked answers.

**Also in `resources/`: a Course Retrospective.** Read it **after** the exam — it is not revision.

---

## The Last Idea

**Every circuit you have built has been either wired by hand or, in principle, etched into silicon. Both are permanent.**

**Programmable logic is a chip whose function is decided *after* manufacture** — by blowing fuses, or by loading a configuration into memory cells.

**And its basic cell is the lookup table**, which this course has now reached three separate times.

---

## The Two Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Wednesday | PLAs, PALs and FPGAs | Programmable AND/OR planes, then LUTs |
| **Lecture 2** | Thursday | Review and the Road Ahead | Thirteen weeks in one picture |

---

## PLA, PAL, ROM — Three Ways To Be Programmable

| | AND plane | OR plane |
|---|---|---|
| **ROM** | fixed (a full decoder) | **programmable** |
| **PLA** | **programmable** | **programmable** |
| **PAL** | **programmable** | fixed |

**The difference is what they cost as the input count grows.**

| $n$ in, $m$ out, $p$ terms | PLA | PAL | ROM |
|---|---:|---:|---:|
| 4, 4, 8 | 96 | 64 | 64 |
| 8, 8, 16 | 384 | 256 | **2 048** |
| 16, 8, 64 | 2 560 | 2 048 | **524 288** |

*(Verified.)*

> **A ROM grows as $2^n$ because it decodes every possible input.** A PLA grows with the number of
> **product terms you actually need**, so a function with few terms is dramatically cheaper.
>
> **This is the one place in the course where Week 4's minimisation pays off directly in the
> architecture** — fewer product terms is fewer rows in the AND plane.

---

## The FPGA

**An array of small lookup tables, each with a flip-flop, joined by programmable interconnect.**

| LUT inputs | bits stored | functions it can be |
|:-:|---:|---:|
| 4 | 16 | 65 536 |
| **6** | **64** | $1.8\times10^{19}$ |

*(Verified — that last figure is Week 1's $2^{2^n}$, met again.)*

**A 6-input LUT implements *any* function of six variables**, and functions of more inputs are split across a small tree:

| function | on 6-LUTs |
|---|---|
| 8-input | ~3 LUTs, 2 levels |
| 32-input | ~7 LUTs, 2 levels |

*(Verified.)*

### And the point the course has made three times

| function | literals | LUT cost |
|---|---:|---|
| $C+AB$ | 3 | **one 3-LUT** |
| $AB+AC+BC+\overline A\,\overline B\,\overline C$ | 11 | **one 3-LUT** |

*(Verified.)*

> **A LUT's cost is fixed by its input count, not by the function inside it.** Minimisation reduces
> gates; **an FPGA does not buy gates.** Its tools pack and route instead.

---

## The Flow

$$\text{HDL} \to \text{synthesis} \to \text{technology mapping} \to \text{placement} \to \text{routing} \to \text{bitstream}$$

**You wrote the first step in Week 10.** Steps 2–5 are **NP-hard in general**, so the tools use heuristics — **exactly what Week 4 said about Quine–McCluskey.**

**And real FPGAs contain dedicated carry chains**, because Week 3's ripple problem is universal enough to be worth hardening into silicon.

---

## This Week's Work

1. **Quiz 11** — Wed 14 Apr, covers Week 11. **Ungraded.** *The last quiz.*
2. **Lab 12** — map a design onto programmable logic and count the resources.
3. **PS 12** — PLA/PAL/ROM sizing, LUT mapping. **Ungraded**; answers released Friday 16 April.
4. **THE FINAL EXAM.** See the revision guide in `resources/`.

---

*Next: Wednesday — PLAs, PALs and FPGAs*

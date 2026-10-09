# ECE 110 · Digital Logic
## Week 12 · Lecture 1 (Wednesday)
### Programmable Logic — PLAs, PALs and FPGAs

*“With unit cost falling as the number of components per circuit rises, by 1975 economics may dictate squeezing as many as 65,000 components on a single silicon chip.”* — Gordon Moore, "Cramming more components onto integrated circuits" (1965)

**Date:** Wednesday 14 April 2027 · 13:00–14:15 · Week 12

**Coursework:** 📊 **Quiz 11** today 13:00–13:10 · 📝 **PS 11** due Thu 15 Apr 13:00 · 📝 **PS 12** released Thu 15 Apr 14:30 · 🔬 **Lab 12** Fri 16 Apr 14:00–15:50 · 📕 **Final exam** Mon 19 Apr 08:00–10:00

---

**Reading:** Harris & Harris §5.6 | Mano & Ciletti §7.6–7.8
**Quiz 11** — at the start of today's lecture. **Covers Week 11.** Ungraded. **The last quiz.**

---

## 1. The Problem With Custom Silicon

**A custom chip is fast, small and power-efficient. It also costs millions in mask sets and takes months**, and if you find a bug you do it all again.

**Programmable logic trades those properties away for one thing: the function is decided after manufacture.** You buy a generic part and configure it — in seconds, at your desk, as many times as you like.

> **You give up perhaps 10× in speed and 20× in area against custom silicon.** For anything built in
> small numbers, or still changing, that is obviously worth it.

---

## 2. The Two-Level Family

**Every circuit in Week 1's canonical form is a sum of products — an AND plane feeding an OR plane.** So make one or both planes programmable.

| device | AND plane | OR plane |
|---|---|---|
| **ROM** | fixed — a full decoder | **programmable** |
| **PLA** | **programmable** | **programmable** |
| **PAL** | **programmable** | fixed |

**A ROM decodes *every* input combination, so it needs $2^n$ word lines whether you use them or not.**

**A PLA generates only the product terms you ask for.**

| $n$ in, $m$ out, $p$ terms | PLA | PAL | ROM |
|---|---:|---:|---:|
| 4, 4, 8 | 96 | 64 | 64 |
| 8, 8, 16 | 384 | 256 | 2 048 |
| 10, 8, 32 | 896 | 640 | 8 192 |
| **16, 8, 64** | **2 560** | **2 048** | **524 288** |

*(Verified.)*

> **At 16 inputs the ROM is 200× the size of the PLA.** The ROM's cost is set by $2^n$; the PLA's by
> the product terms you actually need.
>
> **This is the one architecture in the course where Week 4's minimisation pays off directly** —
> fewer product terms is literally fewer rows in the AND plane. **A PAL with 8 product terms per
> output will not fit your function if you did not minimise it.**

**A PAL's fixed OR plane makes it cheaper and less flexible**; it dominated the 1980s, and **CPLDs** are essentially many PALs with programmable interconnect between them.

---

## 3. The FPGA

**A different idea entirely: instead of two big planes, thousands of tiny lookup tables.**

**A logic cell is roughly:**

- **a $k$-input LUT** — a $2^k$-bit memory addressed by the inputs
- **a flip-flop**
- **a multiplexer** choosing registered or combinational output

**Plus a programmable interconnect joining cells, and dedicated blocks — memories, multipliers, and carry chains.**

### The LUT

| $k$ | bits | functions implementable |
|:-:|---:|---:|
| 4 | 16 | 65 536 |
| 5 | 32 | $4.29\times10^9$ |
| **6** | **64** | $\mathbf{1.8\times10^{19}}$ |

*(Verified — and that last number is Week 1's $2^{2^n}$, arriving again.)*

**A 6-input LUT implements any function of six variables**, with no minimisation and no design effort. **You store the truth table.**

**Larger functions split across a tree:**

| function | on 6-LUTs |
|---|---|
| 8-input | ~3 LUTs, 2 levels |
| 16-input | ~4 LUTs, 2 levels |
| 32-input | ~7 LUTs, 2 levels |

*(Verified.)*

---

## 4. The Third Arrival At The Lookup Table

**Week 5:** a $2^{k-1}$:1 multiplexer with $0$, $1$, $x$ or $\overline x$ on its data inputs implements any $k$-variable function.

**Week 11:** a ROM is a decoder plus an OR plane — address in, stored word out.

**Week 12:** an FPGA's logic cell is a $k$-input LUT.

> **These are one object.** And each time, the same consequence:

| function | literals | LUT |
|---|---:|---|
| $C+AB$ | 3 | one 3-LUT |
| $AB+AC+BC+\overline A\,\overline B\,\overline C$ | 11 | **one 3-LUT** |

*(Verified.)*

**The cost does not depend on the function.** **Minimisation reduces gates, and an FPGA does not buy gates** — so its tools spend their effort on *packing* logic into as few cells as possible and *routing* between them.

---

## 5. The Flow

$$\text{HDL} \to \text{synthesis} \to \text{mapping} \to \text{placement} \to \text{routing} \to \text{bitstream}$$

| step | what it does |
|---|---|
| **synthesis** | your Verilog → a gate-level netlist |
| **technology mapping** | netlist → LUTs and flip-flops |
| **placement** | which physical cell holds which LUT |
| **routing** | configure the interconnect |
| **bitstream** | the configuration file loaded into the chip |

> **Steps 2–5 are NP-hard in general, so the tools use heuristics and do not guarantee optimality** —
> exactly what Week 4 said about Quine–McCluskey's covering step. **The same theoretical limit,
> reappearing at the top of the stack.**

**Routing is usually the binding constraint**, not logic capacity: a design can fail to fit because the wires will not reach, while half the LUTs sit idle.

---

## 6. Why FPGAs Have Hard Carry Chains

**A 32-bit ripple-carry adder is 160 gates** *(Week 3)*. **On a 6-LUT fabric it is roughly 64 LUTs** — and, built from generic interconnect, **slow**, because each carry crosses the programmable routing.

**So every serious FPGA has a dedicated carry chain in silicon**, bypassing the general interconnect.

> **Week 3's serial-dependency problem is universal enough that a general-purpose programmable
> device hardens a special case for it.** That is how important that one structure is.

---

## 7. What To Take From This Lecture

1. **Programmable logic trades speed and area for configurability after manufacture.**
2. **ROM / PLA / PAL differ in which plane is programmable.**
3. **A ROM costs $2^n$; a PLA costs product terms** — 200× apart at 16 inputs.
4. **PLAs are where Week 4's minimisation pays off architecturally.**
5. **An FPGA is LUTs + flip-flops + programmable interconnect.**
6. **A $k$-LUT implements any $k$-input function; cost is independent of the function.**
7. **The flow is HDL → synthesis → map → place → route**, and steps 2–5 are NP-hard.
8. **Hard carry chains exist because of Week 3.**

---

*Next: Thursday — Review and the Road Ahead*

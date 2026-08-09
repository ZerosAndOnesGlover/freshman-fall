# ECE 110 · Digital Logic
## Course Retrospective
### Read this **after** the final exam

---

> **This is not revision.** If the exam has not happened, close it. The revision guide in this folder
> is where your time should go.
>
> **Afterwards, it is worth fifteen minutes.**

---

## 1. What You Actually Built

**Thirteen weeks, and at no point did anything appear that you had not built from something earlier.**

| week | you built | out of |
|---|---|---|
| 0 | a number system | nothing |
| 1 | an algebra | two values |
| 2 | gates | transistors |
| 3 | **an adder** | XOR, AND, OR |
| 4 | smaller circuits | the same gates |
| 5 | decoders, muxes | gates |
| 6 | **an ALU** | an adder and a mux |
| 7 | **memory of one bit** | two gates and a loop |
| 8 | registers and counters | flip-flops |
| 9 | **a machine that decides** | flip-flops and logic |
| 10 | a way to write it down | — |
| 11 | where bits live | one transistor and a capacitor |
| 12 | logic without a fab | lookup tables |

> **Weeks 6 and 9 are a processor's two halves** — the datapath and the control unit. **CS 201 bolts
> them together and adds an instruction set.** You have already built the hard parts.

---

## 2. The Question The Course Kept Asking

**Almost nothing in this course had a right answer. Almost everything had a *cost*.**

| decision | spent | bought |
|---|---|---|
| BCD over binary | **37% more bits** | exact decimal fractions |
| NAND-only libraries | more transistors per gate | uniformity, cancelling inversions |
| carry-lookahead | **2× area** | **10.8× speed** |
| minimisation | design effort | **43 gates → 7** |
| LUT over gates | silicon | design effort, and free changes |
| synchronous over ripple counter | toggle logic | **no transient states**, log delay |
| DRAM over SRAM | **4.5% refresh overhead** | **6× density** |
| FPGA over custom silicon | ~10× speed, ~20× area | configurability after manufacture |

**Every row is a measurement you made.**

> **Not one of those was settled by asking which was better.** Each was settled by measuring both
> sides and naming which resource was scarce. **That is the engineering content of the course**, and
> the gates were the vehicle.

---

## 3. The Four Circuits That Were Correct And Inadequate

**This is the pattern worth remembering.**

**The ripple-carry adder** was correct at every width and took 129 gate delays at 64 bits — **7.75 clock periods**, so it could not be used.

**The ripple counter** counted perfectly and passed through `0110`, `0100`, `0000` on its way from `0111` to `1000`, **glitching any decoder watching it.**

**The SR latch** stored a bit and, on leaving its forbidden state, **settled to whichever value its faster gate chose.**

**Your Verilog** simulated correctly and, with an incomplete sensitivity list, **described a different circuit from the one that would be built.**

> **Every one of those passed the obvious test.** Finding the problem required measuring something
> the obvious test did not look at. **"It works" is where an engineering argument starts.**

---

## 4. Three Times The Test Was Wrong

**Worth its own section, because it happened more than the design being wrong.**

- **Week 2:** a 1-bit `reg` loop counter wrapped, so `a <= 1` never went false and the simulation **hung with no error.**
- **Week 3:** a 4-bit result compared against an unmasked integer reported **240 failures out of 512 on a completely correct adder.** Python, comparing masked, reported zero.
- **Week 9:** an asynchronous reset that was already asserted at time 0 **never fired**, leaving the state `x`.

> **In all three, two tools disagreed and the answer was that the *test* was broken.** When your
> checker fires, check the checker first. **This will save you more time in your career than any
> Boolean identity in this course.**

---

## 5. The Idea That Turned Up Three Times

**A lookup table.**

**Week 5:** a $2^{k-1}$:1 multiplexer with $0$, $1$, $x$ or $\overline x$ on its data inputs implements any $k$-variable function.
**Week 11:** a ROM is a decoder plus an OR plane.
**Week 12:** an FPGA's logic cell is a $k$-input LUT.

**Three routes, one object — and every time, the same consequence: its cost does not depend on the function inside it.**

$$C+AB \ (3 \text{ literals}) \quad\text{and}\quad AB+AC+BC+\overline A\,\overline B\,\overline C \ (11) \quad\text{are both one 3-LUT.}$$

> **Which is why an FPGA toolchain never runs Week 4's algorithm.** Minimisation reduces gates. **An
> FPGA does not buy gates.**

---

## 6. What The Course Did Not Tell You

**In the interest of honesty.**

- **Transistor-level design.** You were given CMOS transistor counts and told that inverting gates are cheaper. **Why** is a device physics course.
- **Real timing analysis.** You used one unit per gate. **Real static timing analysis** handles wire delay, which now dominates gate delay.
- **Power.** Not mentioned once, and it is the binding constraint in most modern designs. **Area and speed were the two costs here; power is the third.**
- **Verification at scale.** You checked 512 and 2048 cases exhaustively. **Real designs cannot be**, and formal methods and constrained-random verification exist for that reason. *(CS 412.)*

**These are not gaps to worry about. They are the next courses.**

---

## 7. Last Thing

**You started with a switch that is on or off, and finished with a machine that recognises a pattern in an unbounded stream and a description language that builds it for you.**

**Nothing magical happened in between.** Every step was two gates, or a flip-flop, or a mux — and every step had a cost you measured.

> **The gate counts will fade. The transistor numbers will fade.**
>
> **What should not fade: a circuit that works is not finished, the cost you are paying has a name,
> and when the checker fires you check the checker.**

**Good luck in CS 201. You will recognise the datapath.**

---

*ECE 110 · Digital Logic & Circuit Design · Course Retrospective*

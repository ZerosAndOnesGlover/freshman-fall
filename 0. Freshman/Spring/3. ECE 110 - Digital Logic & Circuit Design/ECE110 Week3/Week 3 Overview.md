# ECE 110 · Digital Logic
## Week 3 · Overview
### Combinational Circuits — Half Adder, Full Adder, Ripple-Carry Adder

---

**Topic:** how you *add* with gates
**Reading:** Harris & Harris §5.2.1 | Mano & Ciletti §4.3–4.5
**Assessment this week:** PS 3, Lab 3, **Quiz 2** *(Wednesday — covers Week 2, ungraded)*

---

## The Week The Course Turns Into Engineering

**Weeks 0–2 built vocabulary. This week builds a machine.**

By Friday you will have a circuit that adds two 4-bit numbers, and you will have **measured** two things about it: that it is correct on all 512 input combinations, and that it is **too slow**, in a way that gets worse as you make it wider.

> **Both halves matter.** A design that is correct and unusable is a design you have to understand
> well enough to replace — which is Week 6's job.

---

## The Two Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Wednesday | Half and Full Adders | Two gates, then five, and you can add one bit |
| **Lecture 2** | Thursday | The Ripple-Carry Adder and Its Delay | Correct at any width; linear in delay |

---

## Building Up

**Half adder** — adds two bits, produces sum and carry:

$$S = A\oplus B \qquad C = AB \qquad \textbf{2 gates}$$

**Full adder** — adds two bits *and* a carry-in, which is what you need for every column but the first:

$$S = A\oplus B\oplus C_{in} \qquad C_{out} = AB + (A\oplus B)C_{in} \qquad \textbf{5 gates}$$

*(Verified on all 8 input combinations, in Python and in Verilog.)*

**Ripple-carry adder** — $N$ full adders in a row, each one's carry-out feeding the next:

$$\textbf{5}N\textbf{ gates}$$

*(A 4-bit version verified on all **512** input combinations — every $A$, every $B$, both carry-ins — in both tools, zero failures.)*

---

## And Then The Bad News

**The carry has to travel.** Bit 3's output cannot settle until bit 2's carry has settled, which waits on bit 1, which waits on bit 0.

$$\boxed{\text{delay of an } N\text{-bit ripple-carry adder} = 2N+1 \text{ gate delays}}$$

*(Measured exactly, at $N = 2, 3, 4, 8, 16, 32, 64$.)*

| $N$ | gates | gate delays |
|---:|---:|---:|
| 4 | 20 | 9 |
| 8 | 40 | 17 |
| 16 | 80 | 33 |
| 32 | 160 | 65 |
| **64** | **320** | **129** |

> **A 64-bit ripple-carry adder is 129 gate delays deep.** At a plausible 20 ps per gate that is about
> **2.6 ns** — one addition, in a machine that is supposed to issue several per nanosecond.
>
> **This is Week 2's lesson arriving with consequences.** Gate count grows linearly and is fine.
> **Delay grows linearly and is fatal**, because delay is what sets the clock.

**Week 6's carry-lookahead adder spends more gates to make the delay logarithmic.** You cannot appreciate that trade until you have measured this one.

---

## Subtraction, Almost Free

**Week 0 said two's complement makes subtraction into addition. Here is the hardware.**

**Put one XOR on each $B$ input, driven by a `SUB` control line, and feed `SUB` into the carry-in:**

- `SUB = 0`: XOR passes $B$ through, carry-in 0 → **$A+B$**
- `SUB = 1`: XOR inverts $B$, carry-in 1 → **$A + \overline B + 1 = A - B$**

*(Verified on all 512 combinations of $A$, $B$ and `SUB`, in both tools.)*

**Cost: $N$ XOR gates.** One adder does both operations.

> **This is Week 1's XOR fact cashed in.** $B\oplus0 = B$ and $B\oplus1 = \overline B$ — XOR is a
> **controlled inverter**, and that is why the subtract line costs one gate per bit instead of a
> second adder.

**And the overflow flag from Week 0 is one more XOR:** $V = C_3 \oplus C_{out}$, the carries into and out of the sign bit. *(Verified against true signed arithmetic on all 256 signed pairs.)*

---

## This Week's Work

1. **Quiz 2** — Wednesday, covers Week 2. **Ungraded.**
2. **Lab 3** — build a 4-bit adder, verify all 512 cases, **measure the carry delay**.
3. **PS 3** — adder design, delay analysis, subtraction.

---

*Next: Wednesday — Half and Full Adders*

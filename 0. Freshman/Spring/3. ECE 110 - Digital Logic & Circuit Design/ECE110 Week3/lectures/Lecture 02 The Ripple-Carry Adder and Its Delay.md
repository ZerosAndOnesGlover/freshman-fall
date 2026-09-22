# ECE 110 · Digital Logic
## Week 3 · Lecture 2 (Thursday)
### The Ripple-Carry Adder and Its Delay

**Date:** Thursday 11 February 2027 · 13:00–14:15 · Week 3

---

**Reading:** Harris & Harris §5.2.1 | Mano & Ciletti §4.5
**PS 3** released today, due Thursday of Week 4.

---

## 1. Chain Them

**One full adder per bit. Each carry-out becomes the next carry-in.**

$$C_{in} \to \text{FA}_0 \to \text{FA}_1 \to \text{FA}_2 \to \text{FA}_3 \to C_{out}$$

**That is the whole design.** It is exactly how you add on paper — rightmost column first, carry to the left.

$$\textbf{Gate count} = 5N$$

**A 4-bit adder is 20 gates.** *(Verified correct against arithmetic on all **512** input combinations — every $A$, every $B$, both values of $C_{in}$ — in Python and independently as a structural Verilog netlist. Zero failures in both.)*

---

## 2. The Carry Has To Travel

**Bit 3 cannot produce its sum until it knows its carry-in, which is bit 2's carry-out, which needs bit 1's, which needs bit 0's.**

**Worst case, the carry ripples the entire width:**

$$1111 + 0001 = 10000$$

| bit | $A$ | $B$ | $S$ | carry out |
|---:|:-:|:-:|:-:|:-:|
| 0 | 1 | 1 | 0 | **1** |
| 1 | 1 | 0 | 0 | **1** |
| 2 | 1 | 0 | 0 | **1** |
| 3 | 1 | 0 | 0 | **1** |

*(Measured.)* **Every stage waits for the one below it.**

---

## 3. The Delay

**From yesterday: $C_{in}\to C_{out}$ through one full adder is 2 gate delays.** The first stage's carry needs 3 (its inputs must pass the first XOR), and the last sum bit needs one more XOR after its carry arrives.

$$\boxed{t_{RCA} = 2N+1 \text{ gate delays}}$$

*(Measured exactly at $N = 2, 3, 4, 8, 16, 32, 64$ — the formula fits every one.)*

| $N$ | gates | gate delays | at 20 ps/gate |
|---:|---:|---:|---:|
| 4 | 20 | 9 | 0.18 ns |
| 8 | 40 | 17 | 0.34 ns |
| 16 | 80 | 33 | 0.66 ns |
| 32 | 160 | 65 | 1.30 ns |
| **64** | **320** | **129** | **2.58 ns** |

> **A 64-bit ripple-carry adder takes about 2.6 nanoseconds to produce one sum.** A processor running
> at 3 GHz has a clock period of 0.33 ns. **The adder alone is nearly eight clock periods deep**,
> which means it cannot be used.

---

## 4. Which Cost Just Went Wrong

**Look at the two columns again.**

- **Gates: $5N$.** Linear, and completely fine — 320 gates is nothing.
- **Delay: $2N+1$.** Also linear, **and fatal.**

**They grow at the same rate and only one of them is a problem.**

> **This is why Week 2 insisted that gate count and critical path are different costs.** Here is the
> case that proves it: the adder is cheap in area and unusable in time, and no amount of counting
> gates would have told you.
>
> **Delay is what sets the clock**, and the clock is what the machine is sold on.

---

## 5. What Would Fix It

**The problem is that stage $k$ waits to be *told* its carry. But the carry is a function of the inputs — it could be computed directly.**

**Define, per bit:**

$$G_i = A_iB_i \quad\text{(generate: this bit makes a carry regardless)}$$
$$P_i = A_i\oplus B_i \quad\text{(propagate: this bit passes a carry through)}$$

**Then:**

$$C_{i+1} = G_i + P_iC_i$$

**Expand it and the recursion disappears:**

$$C_1 = G_0+P_0C_0$$
$$C_2 = G_1+P_1G_0+P_1P_0C_0$$
$$C_3 = G_2+P_2G_1+P_2P_1G_0+P_2P_1P_0C_0$$

**Every carry is now a two-level expression in the inputs — computable in 2 gate delays, all at once, in parallel.**

**That is the carry-lookahead adder, and it is Week 6's subject.** The cost is gates: the expressions grow, so real designs build them in blocks.

> **You are not expected to design one this week.** You are expected to see that the ripple-carry
> adder's problem is *structural* — a dependency chain — and that breaking the chain is what a faster
> adder has to do.

---

## 6. Subtraction For One Gate Per Bit

**Week 0: $A-B = A+\overline B+1$ in two's complement.**

**Week 1: $B\oplus0 = B$ and $B\oplus1 = \overline B$ — XOR is a controlled inverter.**

**Put them together.** One XOR on each $B$ input, both fed from a `SUB` line, and `SUB` also drives $C_{in}$:

| `SUB` | $B$ input becomes | carry-in | result |
|:-:|---|:-:|---|
| 0 | $B$ | 0 | $A+B$ |
| 1 | $\overline B$ | 1 | $A+\overline B+1 = A-B$ |

$$\textbf{Cost: } N \textbf{ XOR gates. One adder does both operations.}$$

*(Verified on all **512** combinations of $A$, $B$ and `SUB` at $N=4$, in Python and in Verilog.)*

### And the flags come nearly free

$$V = C_{N-1}\oplus C_{out} \qquad \textbf{(one XOR)}$$

**Week 0's overflow rule, built.** *(Verified against true signed arithmetic on all 256 signed pairs at $N=4$ — zero mismatches.)*

**Carry-out is already there.** So a 4-bit adder/subtractor with both flags is $20 + 4 + 1 = \textbf{25 gates}$.

---

## 7. What To Take From This Lecture

1. **$N$ full adders chained: $5N$ gates**, correct at any width.
2. **Verified on all 512 cases at $N=4$**, two independent tools.
3. **The carry must ripple**; worst case it crosses every stage.
4. **$t_{RCA} = 2N+1$ gate delays** — measured, not estimated.
5. **Gate count is linear and fine; delay is linear and fatal.** Different costs.
6. **Generate and propagate** break the dependency chain — Week 6.
7. **Subtraction costs $N$ XOR gates**, because XOR is a controlled inverter.
8. **$V = C_{N-1}\oplus C_{out}$** — one more gate.

---

*Next: Friday — Lab 3, build it and time it*

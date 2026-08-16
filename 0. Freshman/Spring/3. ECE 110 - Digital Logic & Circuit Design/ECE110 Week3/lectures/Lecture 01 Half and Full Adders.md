# ECE 110 · Digital Logic
## Week 3 · Lecture 1 (Wednesday)
### Half and Full Adders

**Date:** Wednesday 3 February 2027 · 13:00–14:15 · Week 3

---

**Reading:** Harris & Harris §5.2.1 | Mano & Ciletti §4.3–4.4
**Quiz 2** — at the start of today's lecture. **Covers Week 2.** Ungraded.

---

## 1. The Design Procedure

**Every combinational circuit in this course is built the same way:**

1. **State the problem in words.**
2. **Write the truth table.**
3. **Extract a Boolean expression** (Week 1's canonical forms).
4. **Minimise it** (algebra now; Karnaugh maps in Week 4).
5. **Draw the gates** (Week 2).
6. **Verify exhaustively.**

**Steps 2 and 6 are not optional and they are not the same step.** Step 2 says what you want; step 6 says what you built.

---

## 2. The Half Adder

**Add two bits. The result can be 0, 1 or 2 — so it needs two output bits.**

| $A$ | $B$ | $C$ | $S$ | value |
|:-:|:-:|:-:|:-:|:-:|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | **1** | 0 | 2 |

**Read the columns:**

$$\boxed{S = A\oplus B \qquad C = AB}$$

**$S$ is 1 when the inputs differ — that is XOR. $C$ is 1 only when both are 1 — that is AND.**

$$\textbf{2 gates.}$$

### Why it is only *half* an adder

**It has no carry-in.** In a multi-bit addition every column except the rightmost receives a carry from the column below, and a half adder has nowhere to put it.

---

## 3. The Full Adder

**Three inputs — $A$, $B$, $C_{in}$ — and the sum can be 0 to 3.**

| $A$ | $B$ | $C_{in}$ | $C_{out}$ | $S$ | value |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 0|0|0| 0 | 0 | 0 |
| 0|0|1| 0 | 1 | 1 |
| 0|1|0| 0 | 1 | 1 |
| 0|1|1| **1** | 0 | 2 |
| 1|0|0| 0 | 1 | 1 |
| 1|0|1| **1** | 0 | 2 |
| 1|1|0| **1** | 0 | 2 |
| 1|1|1| **1** | 1 | 3 |

*(Verified: $S + 2C_{out} = A+B+C_{in}$ on all eight rows.)*

### The sum

**$S$ is 1 on the rows with an *odd* number of 1s** — rows 1, 2, 4, 7. **That is exactly three-input XOR:**

$$\boxed{S = A\oplus B\oplus C_{in}}$$

**XOR is associative** *(verified in Week 1)*, so the three-input form is unambiguous.

### The carry

**$C_{out}$ is 1 when at least two inputs are 1** — a majority function:

$$C_{out} = AB + AC_{in} + BC_{in}$$

**But the cheaper form reuses the sum's first XOR:**

$$\boxed{C_{out} = AB + (A\oplus B)C_{in}}$$

*(Verified equal to the majority form on all eight rows.)*

**Why they are equal:** if $A$ and $B$ are both 1, $AB$ covers it. If exactly one is 1, then $A\oplus B = 1$ and the carry comes through only when $C_{in}=1$. If neither, no carry. **Every case accounted for.**

---

## 4. Two Half Adders Make A Full Adder

$$\text{HA}_1: \quad S_1 = A\oplus B, \quad C_1 = AB$$
$$\text{HA}_2: \quad S = S_1\oplus C_{in}, \quad C_2 = S_1 C_{in}$$
$$C_{out} = C_1 + C_2$$

$$\textbf{2 XOR} + \textbf{2 AND} + \textbf{1 OR} = \textbf{5 gates}$$

*(Verified exhaustively, in Python and independently as a structural Verilog module built from `xor`, `and` and `or` primitives.)*

**This is the standard construction and it is the one you will wire on Friday.**

---

## 5. Its Delay

**Track when each output settles, counting one unit per gate:**

| output | arrives at |
|---|---:|
| $S$ | **2 gate delays** *(XOR then XOR)* |
| $C_{out}$ | **3 gate delays** *(XOR, AND, OR)* |

*(Measured.)*

**But the number that will matter tomorrow is different:**

$$\textbf{from } C_{in} \textbf{ to } C_{out}: \quad \textbf{2 gate delays}$$

**Because $C_{in}$ enters at $\text{HA}_2$'s AND, then passes the OR.** It does not wait for the first XOR, which settled long before.

> **Remember this number.** In a chain of full adders the carry path is the only one that matters,
> and **2 gate delays per bit** is what tomorrow's linear growth is made of.

---

## 6. What To Take From This Lecture

1. **The six-step procedure**, and that stating the truth table and verifying the circuit are different steps.
2. **Half adder: $S=A\oplus B$, $C=AB$. Two gates.** No carry-in, hence "half".
3. **Full adder: $S = A\oplus B\oplus C_{in}$** — odd parity of three inputs.
4. **$C_{out} = AB + (A\oplus B)C_{in}$**, which reuses the sum's XOR and is cheaper than the majority form.
5. **Two half adders plus an OR: 5 gates.**
6. **$S$ at 2 gate delays, $C_{out}$ at 3 — but $C_{in}\to C_{out}$ is only 2**, and that is the number that decides tomorrow.

---

*Next: Thursday — The Ripple-Carry Adder and Its Delay*

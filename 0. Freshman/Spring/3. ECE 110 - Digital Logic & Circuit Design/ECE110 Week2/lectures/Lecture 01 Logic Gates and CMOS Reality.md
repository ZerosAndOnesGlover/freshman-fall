# ECE 110 · Digital Logic
## Week 2 · Lecture 1 (Wednesday)
### Logic Gates and CMOS Reality

---

**Reading:** Harris & Harris §1.5–1.6 | Mano & Ciletti §2.7–2.8
**Quiz 1** — at the start of today's lecture. **Covers Week 1.** Ungraded.

---

## 1. The Seven Gates

| gate | expression | 1 when |
|---|---|---|
| NOT | $\overline A$ | input is 0 |
| AND | $AB$ | both inputs 1 |
| OR | $A+B$ | at least one input 1 |
| NAND | $\overline{AB}$ | **not** both 1 |
| NOR | $\overline{A+B}$ | **neither** is 1 |
| XOR | $A\oplus B$ | inputs **differ** |
| XNOR | $\overline{A\oplus B}$ | inputs **agree** |

**NAND is not "AND then NOT" as a matter of construction.** It is a single gate, and in CMOS it is the cheaper one. Read on.

---

## 2. The Digital Abstraction

**A wire carries a voltage, which is continuous. A bit is discrete.** The bridge is a pair of thresholds:

$$V < V_{IL} \Rightarrow \text{logic } 0 \qquad V > V_{IH} \Rightarrow \text{logic } 1$$

**Between them is the forbidden region**, where the value is undefined. **A gate's job is to keep signals out of it** — inputs anywhere in the valid ranges produce outputs comfortably inside them, so noise picked up along a wire is *removed* rather than accumulated.

> **This is why digital circuits can be deep and analogue ones cannot.** Every gate restores the
> signal. A hundred gates in series still produce a clean 0 or 1; a hundred analogue amplifiers in
> series produce noise.
>
> **The entire rest of this course lives inside that abstraction**, and only Week 11's DRAM will make
> us look underneath it again.

**Noise margin** is how much slack you have: $NM_H = V_{OH}-V_{IH}$ and $NM_L = V_{IL}-V_{OL}$. **Bigger is more robust.**

---

## 3. Why NAND Is The Primitive

**Static CMOS builds a gate from two networks:** a pull-up of PMOS transistors to $V_{DD}$, and a pull-down of NMOS to ground. **The pull-down network computes the *complement* of what you want.**

**So inverting gates come out naturally, and non-inverting ones do not:**

| gate | transistors |
|---|---:|
| NOT | **2** |
| NAND (2-input) | **4** |
| NOR (2-input) | **4** |
| AND (2-input) | 6 |
| OR (2-input) | 6 |
| XOR (2-input) | 12 |

$$\text{AND} = \text{NAND} + \text{NOT} = 4 + 2 = 6$$

**AND is strictly more expensive than NAND.** So is OR than NOR.

> **Week 1 taught you an algebra whose primitives are AND, OR and NOT. Silicon's primitives are NAND
> and NOR.** Bridging that gap — taking a minimised AND/OR expression and realising it in NAND — is
> tomorrow's lecture and a skill you will use for the rest of the course.

**XOR at 12 transistors is expensive**, which is worth remembering when Week 3's adder needs two of them per bit.

---

## 4. Fan-In, Fan-Out, and Delay

**Fan-in** is how many inputs a gate has. **Wide gates are slow** — a 4-input NAND stacks four transistors in series, and the delay grows worse than linearly. **Real libraries stop at about 4 inputs** and build wider functions as trees.

**Fan-out** is how many gate inputs one output drives. **Each load adds capacitance, and capacitance adds delay.** An output driving 10 gates is slower than one driving 2.

**Propagation delay $t_{pd}$** is the time from an input change to a stable output. **The delay of a circuit is the delay along its longest path** — the *critical path* — not the sum of all gates.

> **Two circuits computing the same function can have very different delays**, and from Week 3 onward
> that is the number that decides designs. **Gate count is area; critical path is speed.** They are
> different costs and they frequently trade against each other.

---

## 5. Reading a Gate Two Ways

**De Morgan, from last week, applied to the symbol itself:**

$$\overline{AB} = \overline A + \overline B$$

**So a NAND gate is simultaneously:**

- an **AND** with an inverted output, and
- an **OR** with inverted inputs.

**Both are the same silicon.** Designers draw whichever reading makes the schematic clearer, and **push bubbles along wires** so that they cancel in pairs — two inversions on one wire are no inversion at all.

**This is the practical form of De Morgan**, and tomorrow it becomes a systematic conversion procedure.

---

## 6. What To Take From This Lecture

1. **Seven gates.** NAND and NOR are single gates, not compositions.
2. **The digital abstraction is thresholds plus restoration** — which is why circuits can be deep.
3. **CMOS makes inverting gates cheap:** NOT 2, NAND/NOR 4, AND/OR 6, XOR 12 transistors.
4. **AND costs more than NAND.** The algebra's primitives are not silicon's.
5. **Fan-in and fan-out both cost delay.**
6. **A circuit's delay is its critical path**, not its gate count.
7. **A NAND is an AND-with-bubbled-output and an OR-with-bubbled-inputs**, at once.

---

*Next: Thursday — Functional Completeness and Gate-Level Design*

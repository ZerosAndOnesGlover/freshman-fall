# ECE 110 · Digital Logic
## Problem Set 3 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All circuits verified exhaustively in Python and Icarus Verilog; all delays measured with a gate-level arrival-time model.

---

## Part A (5 pts each)

**A1 (5).** $S=A\oplus B$, $C=AB$. **2 gates.**

**A2 (5).** Standard 8-row table. **$S+2C_{out}=A+B+C_{in}$ on every row.** *(Verified.)*

**A3 (5).** **Equal**, verified on all 8 rows. Argument: if $A=B=1$ then $AB$ covers it; if exactly one is 1 then $A\oplus B=1$ and the carry passes only when $C_{in}=1$; if neither, no carry.

**The second form is preferred because $A\oplus B$ is already computed for the sum**, so it is shared rather than built again — 5 gates instead of 6.

**A4 (5).** Two half adders and **one OR**. **Why OR:** the two half-adder carries can never both be 1 — if $\text{HA}_1$ carries then $S_1=0$, so $\text{HA}_2$ cannot — so OR and XOR would both work here, and **OR is chosen because it is the cheaper gate** (6 transistors against 12).

*Marking: 3 diagram, **2 for the reason.** A student who says "OR because we want either carry" earns 2; one who notices the carries are mutually exclusive and picks OR on cost earns full marks.*

---

## Part B (6 pts each)

**B1 (6).** Four full adders chained. $4\times5 = \boxed{20\text{ gates}}$.

**B2 (6).**

| bit | $A$ | $B$ | $S$ | carry out |
|---:|:-:|:-:|:-:|:-:|
| 0 | 1 | 1 | 0 | **1** |
| 1 | 1 | 0 | 0 | **1** |
| 2 | 1 | 0 | 0 | **1** |
| 3 | 1 | 0 | 0 | **1** |

$$1111+0001 = 10000$$

*(Verified.)* **It is the worst case because the carry generated at bit 0 must propagate through every stage** — no stage can settle until the one below it has.

**B3 (6).** Stage 0's carry takes 3 (inputs must clear the first XOR); each later stage adds 2; the top sum bit adds 1.

$$t = 3+2(N-1) = \boxed{2N+1}$$

**At $N=4$: 9 gate delays.** *(Measured: $S_0$ at 2, $C_1$ at 3, $S_1$ at 4, $C_2$ at 5, $S_2$ at 6, $C_3$ at 7, $S_3$ at 8, $C_{out}$ at **9**.)*

**B4 (6).**

| $N$ | gates | delays | at 20 ps |
|---:|---:|---:|---:|
| 4 | 20 | 9 | 0.18 ns |
| 8 | 40 | 17 | 0.34 ns |
| 16 | 80 | 33 | 0.66 ns |
| 32 | 160 | 65 | 1.30 ns |
| 64 | 320 | 129 | **2.58 ns** |

$$2.58 / 0.333 = \boxed{7.7 \text{ clock periods}}$$

**B5 (6).** **Because they are budgeted against different limits.**

**320 gates is nothing** — a modern chip has billions, so linear growth in area is affordable to any width you like.

**Delay is measured against the clock period, which is fixed by the design target.** The adder sits on the critical path of nearly every instruction, so **2.58 ns against a 0.33 ns period means the machine cannot run at 3 GHz** — the number does not merely get worse, it crosses a hard threshold.

*Marking: 6. **Full marks require naming the thing delay is compared against** (the clock period). "Delay matters more" earns 2.*

---

## Part C (5 pts each)

**C1 (5).** One XOR per bit on the $B$ inputs, second input `SUB`:

| `SUB` | $B$ becomes | $C_{in}$ | result |
|:-:|---|:-:|---|
| 0 | $B\oplus0 = B$ | 0 | $A+B$ |
| 1 | $B\oplus1 = \overline B$ | 1 | $A+\overline B+1 = A-B$ |

*(Verified on all 512 combinations of $A$, $B$, `SUB` at $N=4$, in both tools.)*

**C2 (5).** **From the carry-in of the least significant full adder**, which is wired to the `SUB` line itself. **It is the same wire that selects subtraction** — that is why the $+1$ is free.

*Marking: 5. **"From the carry-in" alone earns 3; naming that it is the `SUB` line itself earns 5.***

**C3 (5).** $20 + 4\text{ (XOR for SUB)} + 1\text{ (XOR for }V) = \boxed{25\text{ gates}}$. **Carry-out needs no extra gate** — it is already an output.

**C4 (5).** $V = C_{N-1}\oplus C_{out}$, the carries **into and out of** the sign bit.

**$0111+0001$ signed** $= 7+1$: the carry into bit 3 is **1** (bits 0–2 generate a full ripple), the carry out of bit 3 is **0**.

$$V = 1\oplus0 = \boxed{1} \qquad\text{result } 1000 = -8, \text{ true answer } +8$$

*(Verified — and the rule matches true signed arithmetic on all 256 signed pairs at $N=4$.)*

**C5 (5).** Same bits $0111+0001 = 1000$.

| read as | value | correct? | flag to consult |
|---|---|---|---|
| **unsigned** | $7+1 = 8$ | ✓ | **carry-out** ($C=0$, so fine) |
| **signed** | $7+1 = -8$ | ✗ | **overflow** ($V=1$, so wrong) |

**The unsigned reader is right and the signed reader is wrong, from identical bits.** *(This is Week 0's Part C, now built in hardware.)*

---

## Part D (5 pts each)

**D1 (5).** $G_i = A_iB_i$ (**generate** — this bit produces a carry regardless of $C_i$); $P_i = A_i\oplus B_i$ (**propagate** — this bit passes an incoming carry through).

$$C_{i+1} = G_i + P_iC_i$$

**D2 (5).**

$$C_1 = G_0+P_0C_0$$
$$C_2 = G_1+P_1G_0+P_1P_0C_0$$
$$C_3 = G_2+P_2G_1+P_2P_1G_0+P_2P_1P_0C_0$$

*(Verified equal to the ripple carries on all 512 cases.)*

**Each is two levels — an AND layer then an OR — so $\mathbf{2}$ gate delays**, plus 1 to form $G$ and $P$. **Every carry in parallel, independent of $N$.**

**D3 (5).** **Because each stage's output is an input to the next** — the design contains a serial dependency chain of length $N$, and no circuit can produce an output faster than its longest dependency chain allows.

*Marking: 5. **"Because the carry ripples" earns 1** — that names the symptom. The answer must identify the serial dependency as the structural cause.*

**D4 (5).** **Area is being traded for speed.** Carry-lookahead uses more gates (the $G$/$P$ expressions grow with the block width) to reduce the critical path from linear to logarithmic. **Week 2's two costs, deliberately traded.**

**D5 (5).** **No — or not usefully.**

NAND is cheaper in **transistors**, which is an **area** measure. Delay is set by the **number of levels on the critical path**, and converting AND-OR to NAND-NAND leaves the level count unchanged *(Week 2, verified)*. **The chain is still $N$ stages long.**

> **The student has proposed an area optimisation for a delay problem.** Gate-level substitution
> cannot fix a structural dependency — only changing the structure can, which is what
> carry-lookahead does.

*Marking: 5. **Full marks require distinguishing the measure being optimised from the measure that is failing.***

---

## Marking Summary

| Part | Points |
|---|---|
| A | 20 |
| B | 30 |
| C | 25 |
| D | 25 |
| **Total** | **100** |

---

## The Five Errors To Expect

1. **A3:** treating the two $C_{out}$ forms as different circuits rather than one shared XOR.
2. **B3:** giving $2N$ or $2N+2$ — the boundary terms at stage 0 and the top sum bit.
3. **B5:** saying delay "matters more" without naming the clock period.
4. **C5:** assuming one of the two readings must be wrong for both.
5. **D5:** accepting the NAND proposal because NAND is cheaper.

---

*ECE 110 · Week 3 · PS 3 Solutions · Instructor Only*

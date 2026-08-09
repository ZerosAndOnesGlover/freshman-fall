# ECE 110 · Digital Logic
## Week 3 · Reference Sheet
### Adders

---

## The Design Procedure

**words → truth table → expression → minimise → gates → verify exhaustively**

**Stating the truth table and verifying the circuit are different steps.** The first says what you want; the second says what you built.

---

## Half Adder

$$S = A\oplus B \qquad C = AB \qquad \textbf{2 gates}$$

**No carry-in — hence "half".**

---

## Full Adder

$$S = A\oplus B\oplus C_{in} \qquad C_{out} = AB+(A\oplus B)C_{in}$$

**$S$ is the odd parity of the three inputs. $C_{out}$ is the majority function** — and

$$AB+AC_{in}+BC_{in} \;=\; AB+(A\oplus B)C_{in} \qquad\textbf{(verified)}$$

**The second form is used because $A\oplus B$ is already computed for the sum.**

### Built from two half adders + OR

$$\textbf{2 XOR} + \textbf{2 AND} + \textbf{1 OR} = \textbf{5 gates}$$

**Why OR and not XOR:** the two half-adder carries can never both be 1, so either works — **OR is chosen because it is cheaper** (6 transistors vs 12).

### Delays

| path | gate delays |
|---|---:|
| inputs → $S$ | 2 |
| inputs → $C_{out}$ | 3 |
| **$C_{in}$ → $C_{out}$** | **2** |

**The last one is what governs a chain.**

---

## Ripple-Carry Adder

**$N$ full adders, each carry-out feeding the next.**

$$\textbf{gates} = 5N \qquad\qquad \boxed{\textbf{delay} = 2N+1 \text{ gate delays}}$$

*(Correctness verified on all **512** cases at $N=4$ in Python and Verilog; the delay formula measured exactly at $N=2,3,4,8,16,32,64$.)*

**Arrival times, $N=4$:**

| $S_0$ | $C_1$ | $S_1$ | $C_2$ | $S_2$ | $C_3$ | $S_3$ | $C_{out}$ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 3 | 4 | 5 | 6 | 7 | 8 | **9** |

**Worst case: $1111+0001 = 10000$** — the carry crosses every stage.

### The cost table

| $N$ | gates | delays | at 20 ps |
|---:|---:|---:|---:|
| 4 | 20 | 9 | 0.18 ns |
| 8 | 40 | 17 | 0.34 ns |
| 16 | 80 | 33 | 0.66 ns |
| 32 | 160 | 65 | 1.30 ns |
| **64** | **320** | **129** | **2.58 ns** |

> **Both costs are linear in $N$; only one is a problem.** 320 gates is nothing. **2.58 ns against a
> 3 GHz clock's 0.33 ns period is 7.7 clock periods** — the adder cannot be used.
>
> **Gate count is budgeted against the chip; delay is budgeted against the clock.**

---

## Adder / Subtractor

**One XOR per $B$ bit, driven by `SUB`, with `SUB` also wired to $C_{in}$:**

| `SUB` | $B$ becomes | $C_{in}$ | result |
|:-:|---|:-:|---|
| 0 | $B$ | 0 | $A+B$ |
| 1 | $\overline B$ | 1 | $A+\overline B+1 = A-B$ |

$$\textbf{Cost: } N \textbf{ XOR gates}$$

*(Verified on all 512 combinations at $N=4$, both tools.)*

**The $+1$ is the `SUB` line itself, wired to the bottom carry-in** — that is why it is free.

**XOR is a controlled inverter:** $B\oplus0=B$, $B\oplus1=\overline B$. *(Week 1)*

### Flags

$$C = C_{out} \text{ (unsigned overflow)} \qquad \boxed{V = C_{N-1}\oplus C_{out}} \text{ (signed overflow)}$$

*(Verified against true signed arithmetic on all 256 signed pairs at $N=4$.)*

**4-bit adder/subtractor with both flags: $20+4+1 = 25$ gates.**

**Worked: $0111+0001$** → carry into bit 3 is 1, out is 0, so $V=1$; result $1000$. **Unsigned reads 8 and is right; signed reads $-8$ and is wrong.** *(Week 0's lesson, in hardware.)*

---

## Toward Carry-Lookahead *(Week 6)*

$$G_i = A_iB_i \quad\text{(generate)} \qquad P_i = A_i\oplus B_i \quad\text{(propagate)} \qquad C_{i+1}=G_i+P_iC_i$$

$$C_2 = G_1+P_1G_0+P_1P_0C_0 \qquad C_3 = G_2+P_2G_1+P_2P_1G_0+P_2P_1P_0C_0$$

*(Verified equal to the ripple carries on all 512 cases.)*

**Each carry is two levels deep and computed in parallel — delay independent of $N$.**

> **The ripple-carry adder is slow because of a *serial dependency chain*, not because its gates are
> slow.** Substituting cheaper gates cannot fix it; only changing the structure can. **Carry-lookahead
> trades area for speed.**

---

## Common Errors

1. **Using a half adder where a carry-in is needed.**
2. **Building $C_{out}$ as the majority form**, missing the shared XOR.
3. **Giving the delay as $2N$ or $2N+2$** — check the boundary terms.
4. **Using gate count as a proxy for speed.**
5. **Forgetting that `SUB` drives the carry-in as well as the XORs.**
6. **Assuming that if the signed reading is wrong, the unsigned one must be too.**
7. **Proposing a gate-level substitution to fix a structural delay problem.**

---

*ECE 110 · Week 3 · Reference Sheet*

# ECE 110 · Digital Logic
## Week 6 · Lecture 2 (Thursday)
### Carry-Lookahead and the Cost of Speed

---

**Reading:** Harris & Harris §5.2.1 | Mano & Ciletti §4.5
**PS 6** released today, due Thursday of Week 7. **The MIDTERM is this week.**

---

## 1. The Problem, Restated

**Week 3 measured it:**

$$t_{\text{ripple}} = 2N+1 \text{ gate delays}$$

**At 64 bits: 129 gate delays, about 2.58 ns, or 7.7 periods of a 3 GHz clock.** The adder alone cannot fit in a cycle.

**And Week 3 identified the cause: a serial dependency chain.** Stage $k$ waits to be *told* its carry.

> **No substitution of faster or cheaper gates fixes this.** The chain is $N$ long whatever it is
> made of. **Only changing the structure works.**

---

## 2. Generate and Propagate

**A bit position does one of three things to a carry.**

$$G_i = A_iB_i \qquad\text{\bf generate} — \text{produces a carry regardless of } C_i$$
$$P_i = A_i\oplus B_i \qquad\text{\bf propagate} — \text{passes an incoming carry through}$$

**Otherwise it kills the carry.** So:

$$C_{i+1} = G_i + P_iC_i$$

**Still recursive — but now expand it.**

$$C_1 = G_0+P_0C_0$$
$$C_2 = G_1+P_1G_0+P_1P_0C_0$$
$$C_3 = G_2+P_2G_1+P_2P_1G_0+P_2P_1P_0C_0$$
$$C_4 = G_3+P_3G_2+P_3P_2G_1+P_3P_2P_1G_0+P_3P_2P_1P_0C_0$$

*(Verified equal to the ripple carries on all 512 four-bit cases.)*

**Every carry is now a two-level AND-OR expression in the inputs.** **All four are computed simultaneously, in 2 gate delays, regardless of position.**

**Read $C_3$ aloud:** *"there is a carry into bit 3 if bit 2 generated one, or bit 1 generated one and bit 2 passed it, or bit 0 generated one and bits 1 and 2 both passed it, or a carry came in and all three passed it."* **That is the paper method, done in parallel instead of in sequence.**

---

## 3. Why Not Just Do 64 Bits At Once

**Because $C_{64}$ would be a 65-input OR of terms up to 65 literals long.** **Fan-in kills it** — Week 2 said wide gates are slow and libraries stop near 4 inputs.

**So build it hierarchically.** Each 4-bit block also produces **group** signals:

$$P_{\text{group}} = P_3P_2P_1P_0 \qquad G_{\text{group}} = G_3+P_3G_2+P_3P_2G_1+P_3P_2P_1G_0$$

**Then a second-level lookahead unit treats each block as if it were a single bit**, and a third level treats each group of blocks the same way. **A tree.**

---

## 4. Measured

**A hierarchical CLA with 4-bit blocks, built and checked, on the same one-unit-per-gate model as Week 3:**

| $N$ | ripple | **CLA** | speedup |
|---:|---:|---:|---:|
| 4 | 9 | **4** | 2.2× |
| 8 | 17 | **7** | 2.4× |
| 16 | 33 | **8** | 4.1× |
| 32 | 65 | **11** | 5.9× |
| **64** | **129** | **12** | **10.8×** |

*(All measured. Correctness verified on sampled 8-bit operands, zero failures.)*

**Ripple grows linearly. CLA grows roughly logarithmically** — doubling the width adds a level or two, not $2N$.

### The verdict at 64 bits

| | delay | vs a 0.33 ns clock |
|---|---:|---|
| ripple-carry | 2.58 ns | **7.7 periods — does not fit** |
| **carry-lookahead** | **0.24 ns** | **0.72 periods — fits** |

**That is the whole point of the week.**

---

## 5. What It Costs

**Roughly $2\times$ the gates** at 32–64 bits: the $G$/$P$ logic, the block lookahead units, and the hierarchy.

| | ripple | CLA |
|---|---:|---:|
| 64-bit gates | 320 | ~640 |
| 64-bit delay | 129 | **12** |

> **You are buying a 10× delay reduction for 2× the area.**
>
> **Week 2 named the two costs. Week 3 showed one of them failing. Week 4 reduced the other one.
> This is the week you trade them against each other deliberately** — and the trade is only obvious
> because you measured both.

**Real processors go further** — carry-select, carry-skip, parallel-prefix adders — all trading more area for less delay. **The principle does not change.**

---

## 6. What To Take From This Lecture

1. **The ripple adder is slow because of a serial dependency**, not slow gates.
2. **$G_i=A_iB_i$, $P_i=A_i\oplus B_i$, $C_{i+1}=G_i+P_iC_i$.**
3. **Expanded, every carry is two levels deep and computed in parallel.**
4. **Fan-in forbids doing 64 bits flat** — hence blocks and a tree.
5. **Measured: 129 → 12 gate delays at 64 bits, a 10.8× speedup.**
6. **The cost is about 2× the area.**
7. **A 64-bit CLA fits in a 3 GHz clock period; a ripple adder needs 7.7 of them.**

---

*Next: Friday — Lab 6, build the ALU. Then the midterm.*

# ECE 110 · Digital Logic
## Week 7 · Lecture 2 (Thursday)
### Flip-Flops and Timing

**Date:** Thursday 11 March 2027 · 13:00–14:15 · Week 7

---

**Reading:** Harris & Harris §3.2.3–3.2.5, §3.5 | Mano & Ciletti §5.3
**PS 7** released today, due Thursday of Week 8.

---

## 1. Latch vs Flip-Flop

> **A latch is level-sensitive: it responds while its enable is high.**
> **A flip-flop is edge-triggered: it responds only at the instant the clock changes.**

**That single difference is what makes large synchronous systems possible.** With edge triggering, every state element in the machine updates at the same instant, and between edges the combinational logic has the whole clock period to settle.

---

## 2. The Master–Slave D Flip-Flop

**Two gated D latches in series, on opposite clock phases:**

$$\text{master: transparent while } CLK=0 \qquad \text{slave: transparent while } CLK=1$$

**Trace it.** While the clock is low, the master follows $D$ and the slave holds. **On the rising edge** the master freezes and the slave becomes transparent — so the slave copies whatever the master captured at that instant.

**At no point are both transparent**, so **data can never flow straight through.**

*(Verified: a structural master–slave DFF built from NAND-gate latches, driven over 12 clock edges with $D$ deliberately changed while the clock was high — **zero failures**, and the output never moved between edges.)*

$$\boxed{Q^+ = D \text{, sampled at the rising edge}}$$

---

## 3. The JK Flip-Flop

**The SR latch's $S=R=1$ was forbidden. The JK asks: what if it did something useful instead?**

$$\boxed{Q^+ = J\overline Q + \overline KQ}$$

| $J$ | $K$ | $Q^+$ | |
|:-:|:-:|:-:|---|
| 0 | 0 | $Q$ | hold |
| 0 | 1 | 0 | reset |
| 1 | 0 | 1 | set |
| 1 | 1 | $\overline Q$ | **TOGGLE** |

*(Verified on all eight $(J,K,Q)$ combinations.)*

**The internal feedback of $Q$ and $\overline Q$ into the input gates is what makes $J=K=1$ toggle** rather than break — the forbidden combination has been redefined into the most useful one.

**A T flip-flop is a JK with $J$ and $K$ tied together:** $Q^+ = T\oplus Q$. *(Verified identical.)* **It is the counter's building block** — next week.

---

## 4. Characteristic and Excitation Tables

**Characteristic — what will the device do?**

$$D:\ Q^+=D \qquad JK:\ Q^+=J\overline Q+\overline KQ \qquad T:\ Q^+=T\oplus Q$$

**Excitation — what must I apply to get the transition I want?** *This is the one you use to design.*

| $Q\to Q^+$ | $D$ | $T$ | $J$ | $K$ |
|:-:|:-:|:-:|:-:|:-:|
| $0\to0$ | 0 | 0 | 0 | $\times$ |
| $0\to1$ | 1 | 1 | 1 | $\times$ |
| $1\to0$ | 0 | 1 | $\times$ | 1 |
| $1\to1$ | 1 | 0 | $\times$ | 0 |

*(Verified — the $\times$ entries are genuine don't-cares, i.e. both input values produce the wanted transition.)*

> **Half the JK table is don't-cares, and Week 4 told you what those are worth.** A JK-based state
> machine's next-state logic minimises further than the same machine built from D flip-flops.
>
> **That is the entire reason JK still exists.** D is simpler to reason about and is what you will
> almost always use; JK buys cheaper logic at the cost of a harder design.

---

## 5. Timing — The Part That Bites

**A flip-flop does not sample instantaneously. It needs the data to be still.**

| parameter | meaning |
|---|---|
| **$t_{su}$ (setup)** | $D$ must be stable **before** the edge |
| **$t_h$ (hold)** | $D$ must stay stable **after** the edge |
| **$t_{cq}$** | delay from the edge to $Q$ changing |

**The clock period must satisfy:**

$$\boxed{T_{clk} \;\ge\; t_{cq} + t_{\text{logic,max}} + t_{su}}$$

**This is why the critical path decides the clock speed**, and it is the formal version of Week 3's and Week 6's arithmetic. **A 64-bit ripple adder between two flip-flops forces $T_{clk} \ge 2.58$ ns; a carry-lookahead adder allows $T_{clk} \ge 0.24$ ns plus overheads.**

**Hold time is a separate hazard:** if the logic between two flip-flops is *too fast*, new data can arrive before the old was captured. **Hold violations cannot be fixed by slowing the clock** — you must add delay.

---

## 6. Metastability

**Violate setup or hold and the flip-flop may enter a state that is neither 0 nor 1**, and stay there for an unbounded time before resolving randomly.

**It cannot be eliminated.** Any circuit sampling a signal not derived from its own clock — a button, an input from another clock domain — **can be hit.**

**The engineering answer is a synchroniser: two flip-flops in series.** The first may go metastable; it is given a full clock period to resolve before the second samples it. **This reduces the failure probability to something acceptable; it does not reach zero.**

> **This is the only place in the course where the answer is a probability rather than a guarantee** —
> and it is worth knowing that such places exist.

---

## 7. What To Take From This Lecture

1. **Latch = level-sensitive; flip-flop = edge-triggered.**
2. **Master–slave: two latches on opposite phases, never both transparent.**
3. **JK redefines the forbidden combination as toggle.** $Q^+=J\overline Q+\overline KQ$.
4. **T flip-flop = JK with inputs tied.** $Q^+=T\oplus Q$.
5. **Excitation tables are what you design with**, and **JK's don't-cares make its logic cheaper**.
6. **$T_{clk}\ge t_{cq}+t_{\text{logic,max}}+t_{su}$** — the formal reason the critical path sets the clock.
7. **Hold violations need added delay, not a slower clock.**
8. **Metastability cannot be eliminated**, only made improbable with a synchroniser.

---

*Next: Friday — Lab 7, build a latch and catch it misbehaving*

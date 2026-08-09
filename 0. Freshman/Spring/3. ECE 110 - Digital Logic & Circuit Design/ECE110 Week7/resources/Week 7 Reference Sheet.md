# ECE 110 · Digital Logic
## Week 7 · Reference Sheet
### Latches, Flip-Flops, Timing

---

## Memory Requires Feedback

**A combinational circuit is a function; the same inputs always give the same outputs.** Remembering means giving *different* outputs for the *same* inputs. **Feedback is the only mechanism.**

**Consequence: you can no longer analyse by truth table.** You must settle the network to a fixed point — **and it may not have a unique one.**

---

## SR Latch (cross-coupled NOR)

$$Q=\overline{R+\overline Q} \qquad \overline Q=\overline{S+Q}$$

| $S$ | $R$ | $Q$ | $\overline Q$ | |
|:-:|:-:|:-:|:-:|---|
| 0|0| $Q_0$ | $\overline{Q_0}$ | **HOLD** |
| 0|1| 0 | 1 | reset |
| 1|0| 1 | 0 | set |
| 1|1| **0** | **0** | **FORBIDDEN** |

*(verified by iterating to a fixed point from both initial states)*

**Forbidden because both outputs go to 0** — $Q$ and $\overline Q$ stop being complementary.

### The race

**Dropping $S$ and $R$ to 0 together from $S=R=1$:**

| whichever gate settles first | final $Q$ |
|---|:-:|
| $Q$'s | **1** |
| $\overline Q$'s | **0** |

*(verified — same inputs, two outcomes)*

> **Decided by gate speed, not inputs.** **You cannot fix a race by being careful with the inputs.
> You make the bad input unreachable.**

---

## Gated D Latch

$$S=D\cdot EN \qquad R=\overline D\cdot EN$$

**$S$ and $R$ are complements when $EN=1$ and both 0 when $EN=0$, so $S=R=1$ is unreachable by construction.** *(verified)*

| $EN$ | |
|:-:|---|
| 1 | $Q$ follows $D$ — **transparent** |
| 0 | holds |

> **Transparency is the remaining problem.** If $Q$ can reach $D$, the state races round the loop an
> unpredictable number of times per enable pulse.

---

## Master–Slave D Flip-Flop

**Two gated D latches on opposite clock phases** — master transparent while $CLK=0$, slave while $CLK=1$. **Never both transparent, so data cannot flow straight through.**

$$\boxed{Q^+ = D \text{, sampled at the rising edge}}$$

*(verified: a structural NAND-gate master–slave DFF over 12 edges with $D$ changing while the clock was high — 0 failures, output never moved between edges)*

> **Latch = level-sensitive. Flip-flop = edge-triggered.** Edge triggering is what makes large
> synchronous systems possible: every state element updates at one instant, and the logic gets the
> whole period to settle.

---

## Characteristic Tables — what the device does

$$D:\ Q^+=D \qquad SR:\ Q^+=S+\overline RQ \qquad JK:\ Q^+=J\overline Q+\overline KQ \qquad T:\ Q^+=T\oplus Q$$

**JK:**

| $J$ | $K$ | $Q^+$ | |
|:-:|:-:|:-:|---|
| 0|0| $Q$ | hold |
| 0|1| 0 | reset |
| 1|0| 1 | set |
| 1|1| $\overline Q$ | **toggle** |

*(verified)* **JK redefines SR's forbidden combination as the most useful one.**

**T flip-flop = JK with $J,K$ tied.** *(verified identical)* **The counter's building block.**

---

## Excitation Tables — what you design with

| $Q\to Q^+$ | $D$ | $T$ | $J$ | $K$ |
|:-:|:-:|:-:|:-:|:-:|
| $0\to0$ | 0 | 0 | 0 | $\times$ |
| $0\to1$ | 1 | 1 | 1 | $\times$ |
| $1\to0$ | 0 | 1 | $\times$ | 1 |
| $1\to1$ | 1 | 0 | $\times$ | 0 |

*(verified — the $\times$ are genuine don't-cares)*

> **Half the JK table is don't-cares, and Week 4 priced those.** JK next-state logic minimises further
> than D. **That is the only reason JK survives** — D is simpler and is what you will usually use.

---

## Timing

| | |
|---|---|
| **$t_{su}$** | $D$ stable **before** the edge |
| **$t_h$** | $D$ stable **after** the edge |
| **$t_{cq}$** | edge to $Q$ changing |

$$\boxed{T_{clk} \ \ge\ t_{cq} + t_{\text{logic,max}} + t_{su}}$$

**With $t_{cq}=50$ ps, $t_{su}=30$ ps:**

| logic between flip-flops | $T_{min}$ | $f_{max}$ |
|---|---:|---:|
| 64-bit ripple adder (2.58 ns) | 2.66 ns | **376 MHz** |
| 64-bit CLA (0.24 ns) | 0.32 ns | **3.13 GHz** |

*(computed)* **An 8.3× difference in achievable clock speed** — the formal version of Weeks 3 and 6.

**Hold violations** happen when logic is *too fast*. **They cannot be fixed by slowing the clock** — you must add delay.

---

## Metastability

**Violate setup or hold and the output may sit between 0 and 1 for an unbounded time, resolving randomly.**

**Unavoidable** whenever sampling a signal not derived from your own clock — a button, another clock domain.

**Mitigation: a two-flip-flop synchroniser.** The first may go metastable and gets a full period to resolve before the second samples.

> **This reduces the failure probability; it does not reach zero.** The only place in the course
> where the answer is a probability.

---

## Common Errors

1. **Saying $S=R=1$ is forbidden "because the datasheet says so"** — it is because the outputs stop being complementary.
2. **Thinking a race can be avoided by careful input timing.**
3. **Confusing level-sensitive with edge-triggered.**
4. **Using a latch where a flip-flop is needed**, then being surprised by multiple updates per pulse.
5. **Forgetting $t_{su}$ in the clock-period budget.**
6. **Trying to fix a hold violation by slowing the clock.**
7. **Believing a synchroniser eliminates metastability.**

---

*ECE 110 · Week 7 · Reference Sheet*

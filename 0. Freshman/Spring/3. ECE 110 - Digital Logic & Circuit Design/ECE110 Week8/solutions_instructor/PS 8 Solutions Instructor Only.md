# ECE 110 · Digital Logic
## Problem Set 8 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All sequences and delays verified by simulation.

---

## Part A (5 pts each)

**A1 (5).** $D_i = \text{LOAD}\cdot\text{data}_i+\overline{\text{LOAD}}\cdot Q_i$ — **a 2:1 mux per bit**, all four flip-flops on one clock.

**A2 (5).** **Two hazards:**
1. **Clock skew** — the gated clock arrives later than the ungated one, so this register samples at a different instant from the rest of the design.
2. **Glitches** — any hazard on the LOAD signal appears as a spurious clock edge, and a flip-flop cannot distinguish that from a real one.

*Marking: 5, **both hazards named.** One earns 3.*

**A3 (5).** SISO (delay line), **SIPO (deserialiser)**, **PISO (serialiser)**, PIPO. **A UART is a PISO transmitting and a SIPO receiving.**

**A4 (5).**

| clock | out | state |
|:-:|:-:|:-:|
| 1 | **1** | `0101` |
| 2 | **1** | `0010` |
| 3 | **0** | `0001` |
| 4 | **1** | `0000` |

*(Verified.)*

---

## Part B (6 pts each)

**B1 (6).** Three D flip-flops, each with $\overline Q\to D$, each clocked by the previous stage's $Q$.

$$\boxed{\text{Zero gates.}}$$

*Marking: 4 diagram, **2 for the gate count being zero.** Students often invent gates that are not there.*

**B2 (6).**

$$\texttt{011} \to \texttt{010} \to \texttt{000} \to \texttt{100}$$

**Intermediate states actually taken: `010` (2) and `000` (0).** *(Verified.)*

**B3 (6).** **A decoder watching the counter sees those intermediate states and asserts the corresponding outputs.**

**Specific consequence:** the "count is 0" output fires briefly on **every** $2^k-1\to2^k$ transition, not just at 0. **If that output drives a memory write-enable or a device strobe, the system performs spurious writes** — a fault that appears only at speed and is invisible to single-stepping.

*Marking: 3 mechanism, **3 for a concrete consequence.***

**B4 (6).** $t_{\text{settle}} = N\cdot t_{cq}$.

**It resembles the ripple-carry adder of Week 3**, and for the same reason: **a serial dependency chain**, where stage $k$ cannot act until stage $k-1$ has.

**B5 (6).**

| $N$ | 4 | 8 | 16 | 32 |
|---|---|---|---|---|
| settle | $4t_{cq}$ | $8t_{cq}$ | $16t_{cq}$ | $32t_{cq}$ |

---

## Part C (6 pts each)

**C1 (6).** $T_0=1$, $T_1=Q_0$, $T_2=Q_0Q_1$, $T_3=Q_0Q_1Q_2$.

**In words: bit $k$ toggles exactly when every bit below it is 1** — which is what a carry is.

**C2 (6).** **All flip-flops share one clock and therefore update at the same instant.** The outputs move from one valid state to the next with no intermediate values — the toggle decisions were computed from the *old* state, before any of it changed.

**C3 (6).** $t_{cq}$ + AND-tree depth + $t_{su}$. **The tree is $O(\log N)$**, against the ripple counter's $O(N)$.

| $N$ | ripple | sync tree |
|---:|---:|---:|
| 4 | 4 | 2 |
| 32 | 32 | **5** |

**C4 (6).** **It costs the toggle logic** — an AND tree the ripple counter did not need at all.

$$\textbf{Area is being spent to buy speed and correctness.}$$

**Third instance of the trade:** Week 4 cut area, Week 6 spent area for adder speed, and here area buys both a shorter delay and the elimination of transient states.

**C5 (6).** Detect $10=\texttt{1010}$:

$$\boxed{\text{clear}=Q_3Q_1}$$

**Two gates suffice because no reachable count below 10 has both $Q_3$ and $Q_1$ set** — *(verified: the set of $n<10$ with both bits is empty)* — so the other two bits are **don't-cares** in the Week 4 sense.

*Marking: 3 equation, **3 for the don't-care justification.** An answer decoding all four bits is correct but earns 4.*

---

## Part D (5 pts each)

**D1 (5).** Four flip-flops in a ring, $Q_3\to D_0$:

$$\texttt{0001}\to\texttt{0010}\to\texttt{0100}\to\texttt{1000}\to\texttt{0001}$$

*(Verified.)* **Decode logic: none.** Each $Q_k$ *is* the "in state $k$" signal.

**D2 (5).**

| | flip-flops | states | decode |
|---|---:|---:|---|
| binary | 4 | 16 | needed |
| ring | 4 | 4 | **none** |

**Choose binary when states are many and flip-flops are scarce. Choose a ring when the states are few and the outputs are wanted one-hot anyway** — typical for a controller, and used in Week 9.

**D3 (5).** **It stays at `0000` forever** — no bit is set, so nothing circulates. **Likewise two set bits circulate as two forever.**

**This shows a reset is not optional:** the circuit has unreachable-from-power-up correct behaviour, and only an explicit initialisation guarantees a valid starting state.

**D4 (5).** **State 10 (`1010`) itself.** The counter reaches it, the detect fires, and the clear wipes it — so the outputs show `1010` for roughly one gate delay.

**Clean alternative: synchronous clear** — feed the detect into the next-state logic so that state 9 goes directly to 0 and **state 10 never exists.**

---

## Marking Summary

| Part | Points |
|---|---|
| A | 20 |
| B | 30 |
| C | 30 |
| D | 20 |
| **Total** | **100** |

---

## The Five Errors To Expect

1. **B1:** inventing gates in a ripple counter, which has none.
2. **B3:** naming the glitch without a consequence.
3. **C2:** "because they are synchronous" — restating, not explaining.
4. **C5:** decoding all four bits without noticing the don't-cares.
5. **D3:** not connecting the stuck ring counter to the need for reset.

---

*ECE 110 · Week 8 · PS 8 Solutions · Instructor Only*

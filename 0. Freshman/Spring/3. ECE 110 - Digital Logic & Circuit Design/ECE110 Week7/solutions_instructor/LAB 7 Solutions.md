# ECE 110 · Digital Logic
## Lab 7 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.**

---

## Part A — The SR Latch (30 pts)

### A1 (8), A2 (7)

**Standard behaviour.** The mark in A2 is for **demonstrating hold** — setting the latch, returning $S$ to 0, and showing $Q$ stays. **A student who never returns the input to 0 has not shown memory**, only combinational behaviour.

### A3 (5)

$$Q=0 \quad\text{and}\quad \overline Q=0 \qquad\textbf{both LEDs off}$$

**What is wrong:** the output named $\overline Q$ is not the complement of $Q$. **The circuit is violating its own labelling.**

*Marking: 3 observation, 2 explanation. **The explanation must be about complementarity.***

### A4 (5) — expect a boring table

**Most pairs will record the same value all ten times.** That is the honest result on one chip, and it is **not** evidence against the race.

*Marking: 5 for ten recorded trials, whatever they show.*

### A5 (5) — the point of the part

**On a different 74HC02, many pairs will get the opposite consistent answer.**

> **This is what makes the lesson land.** Within one chip the faster gate is reliably faster, so the
> race looks deterministic. **Across chips it is not** — and a design that works on your bench and
> fails on the customer's is precisely the failure mode being demonstrated.

**Expected conclusion:** the outcome is decided by **gate propagation delay**, a manufacturing property, **not by the inputs**.

*Marking: 3 for both tables, **2 for the conclusion.** If a pair happens to get the same answer on both chips, award full marks for correctly reporting that and noting it does not prove determinism — one extra sample is not a proof.*

> **Have two or three pairs read out their results.** A split across the room is the demonstration; if
> the whole room agrees, say plainly that this is what a race that has not yet bitten you looks like.

---

## Part B — The Gated D Latch (25 pts)

### B1 (10), B2 (8)

| $D$ | $EN$ | $S$ | $R$ |
|:-:|:-:|:-:|:-:|
| 0|0| 0 | 0 |
| 1|0| 0 | 0 |
| 0|1| 0 | 1 |
| 1|1| 1 | 0 |

**$S=R=1$ never appears.** With $EN=0$ both are 0; with $EN=1$ they are $D$ and $\overline D$, which are complements. *(Verified.)*

*Marking B2: 4 table, **4 for the argument.***

### B3 (7)

**Observed: with $EN=1$, $Q$ follows every change of $D$. With $EN=0$, $Q$ ignores $D$ entirely.**

**Why it is a problem when $Q$ feeds back to $D$:** the updated state travels round the loop and reaches the input **while the latch is still open**, so the circuit updates repeatedly within one enable pulse — **an unpredictable number of times**, set by loop delay versus pulse width.

---

## Part C — The Flip-Flop (25 pts)

### C1 (10), C2 (8)

**$Q$ changes only on the button press; changing $D$ between presses does nothing.**

**The one-sentence difference:** *the latch responds whenever it is enabled; the flip-flop responds only at the clock edge.*

### C3 (7) — $\overline Q$ back to $D$

**$Q$ toggles on every press: 0, 1, 0, 1, …**

$$\textbf{A T flip-flop} — \text{equivalently, a divide-by-2 counter.}$$

**Four of these chained make next week's 4-bit counter.**

*Marking: 4 observation, **3 for naming it.** "It toggles" earns 4; naming the T flip-flop or divide-by-2 earns 7.*

---

## Part D — Simulation (20 pts)

### D1 (10)

**Must be structural** — gated D latches from `nand` primitives, master on the inverted clock. **A behavioural `always @(posedge clk) q <= d;` earns 3 of 10**: it asserts edge triggering rather than building it.

### D2 (10)

$$\textbf{12 clock edges, 0 failures.}$$

**Both required checks pass:** $Q$ takes $D$'s value at each rising edge, **and** $Q$ does not move when $D$ changes while the clock is high. *(Measured, Icarus Verilog 12.0.)*

*Marking: 5 testbench, **5 for reporting BOTH checks.** A student who verifies only the sampling has not tested the property that distinguishes a flip-flop from a latch.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 30 |
| B | 25 |
| C | 25 |
| D | 20 |
| **Total** | **100** |

---

## Checkoff Checklist

1. **A2 demonstrates hold**, not just set and reset
2. A3 explains the fault in terms of complementarity
3. **A5 reports both chips' tables and draws the conclusion**
4. **B2 argues $S=R=1$ is unreachable**, not just tabulates
5. B3 connects transparency to the feedback case
6. **C3 names the T flip-flop / divide-by-2**
7. **D1 is structural**
8. **D2 checks both sampling and non-transparency**

---

## Note for the Debrief

**Run the A5 read-out first, publicly.**

> **Every one of you got a consistent answer on your own chip. Some of you got the opposite consistent
> answer on someone else's.** Same circuit, same inputs, same procedure.
>
> **The result is decided by which gate happens to be faster** — a manufacturing property you do not
> control and cannot see. **This is what a race condition is**, and it is the reason the rest of the
> course is disciplined about clocks rather than casual about them.

Then the arc of the fixes:

> **Three problems, three fixes, in order.** The forbidden state — fixed by *construction*, deriving
> $S$ and $R$ from one signal so the bad input cannot occur. Transparency — fixed by *structure*, two
> latches that are never open together. And the SR's wasted input combination — fixed by
> *redefinition*, so $J=K=1$ toggles.
>
> **None of the three was fixed by being careful.** That is the pattern worth taking away.

Then set up next week:

> **In Part C3 you wired $\overline Q$ back to $D$ and built a divide-by-2 counter without being told
> to.** Next week you chain four of them, and find out what that costs in delay — **because the same
> question as Week 3 comes back, in sequential clothing.**

---

*ECE 110 · Week 7 · Lab 7 Solutions · Instructor Only*

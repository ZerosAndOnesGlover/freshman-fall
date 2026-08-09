# ECE 110 · Digital Logic
## Problem Set 7 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Latch behaviour verified by iterating gate networks to a fixed point; the master–slave flip-flop verified structurally in Icarus Verilog.

---

## Part A (5 pts each)

**A1 (5).** Cross-coupled NOR; four rows: hold / reset / set / forbidden. *(Verified.)*

**A2 (5).** **Both outputs are driven to 0.** Since the second output is *named* $\overline Q$, the circuit is no longer complementary — **anything downstream relying on $Q$ and $\overline Q$ being opposites is broken.**

*Marking: 5. **"The datasheet forbids it" earns 0.** The answer is about the outputs.*

**A3 (5).** **Both gates try to go high, each held low by the other. Whichever is fractionally faster wins and locks the other low.**

| settles first | final $Q$ |
|---|:-:|
| $Q$'s gate | 1 |
| $\overline Q$'s gate | 0 |

*(Verified — identical inputs, two outcomes.)*

**The outcome is decided by gate delay — manufacturing spread, temperature, supply voltage — not by the inputs.**

**A4 (5).** **Because the race is a property of the circuit, not of the input sequence.** Any attempt to leave $S=R=1$ hits it, and you cannot control which of two nominally identical gates is faster.

**The fix is to make $S=R=1$ unreachable** — which is what the gated D latch does by deriving $S$ and $R$ from one signal.

---

## Part B (6 pts each)

**B1 (6).** $S=D\cdot EN$, $R=\overline D\cdot EN$.

**Proof:** if $EN=0$ then $S=R=0$. If $EN=1$ then $S=D$ and $R=\overline D$, which are complements. **In neither case can both be 1.** *(Verified over all $(D,EN)$.)*

**B2 (6).** **Transparency: while $EN=1$ the output tracks the input continuously**, rather than sampling it once.

**The problem when $Q$ can reach $D$:** the new state propagates round the loop and back to the input *while the latch is still open*, so the circuit updates an **unpredictable number of times** in one enable pulse — decided by loop delay against pulse width.

**B3 (6).** **Master transparent while $CLK=0$, slave while $CLK=1$.** On the rising edge the master freezes and the slave opens, so the slave copies what the master held at that instant.

**Data cannot flow straight through because the two are never transparent simultaneously** — there is always a closed latch in the path. *(Verified structurally over 12 edges, 0 failures.)*

**B4 (6).** **Latch:** $Q$ follows $D$ throughout every high enable window. **Flip-flop:** $Q$ changes only at rising edges, and ignores $D$ in between.

*Marking: 6. **The diagram must show at least one $D$ change during a high phase**, where the two devices visibly differ. Without that the diagram demonstrates nothing.*

**B5 (6).** **Level-sensitive responds while the enable is asserted; edge-triggered responds only at the instant the clock transitions.**

**Edge triggering makes large synchronous systems possible** because every state element updates at the same instant, so the combinational logic between them has the entire clock period to settle and the designer has exactly one timing constraint to satisfy.

---

## Part C (6 pts each)

**C1 (6).** $Q^+=J\overline Q+\overline KQ$; hold / reset / set / **toggle**. *(Verified on all 8 combinations.)*

**C2 (6).** **It redefines it as toggle.** Internal feedback of $Q$ and $\overline Q$ into the input gates means that with $J=K=1$ exactly one of the two paths is enabled at any moment — **the one that flips the state** — so the combination that broke the SR latch becomes its most useful input.

**C3 (6).** With $J=K=T$: $Q^+ = T\overline Q + \overline TQ = T\oplus Q$. *(Verified identical for all $(T,Q)$.)*

**C4 (6).**

| $Q\to Q^+$ | $D$ | $T$ | $J$ | $K$ |
|:-:|:-:|:-:|:-:|:-:|
| $0\to0$ | 0 | 0 | 0 | $\times$ |
| $0\to1$ | 1 | 1 | 1 | $\times$ |
| $1\to0$ | 0 | 1 | $\times$ | 1 |
| $1\to1$ | 1 | 0 | $\times$ | 0 |

*(Verified: each $\times$ is a genuine don't-care — both values give the wanted transition.)*

**C5 (6).** **Half the JK excitation table is don't-cares.** Week 4 showed that don't-cares enlarge K-map groups and cut literals — on "is this BCD digit $\ge5$?" they took 9 literals to 5.

**The same applies to next-state logic**, so a JK machine's input equations minimise further than the same machine's D equations. **That is the whole reason JK survives** despite D being simpler to reason about.

---

## Part D (5 pts each)

**D1 (5).** $t_{su}$ — data stable before the edge; $t_h$ — stable after; $t_{cq}$ — edge to output change.

**D2 (5).** $T_{clk}\ge t_{cq}+t_{\text{logic,max}}+t_{su}$.

**This is the formal statement of Weeks 3 and 6:** the *maximum* logic delay — the critical path — appears directly in the clock-period budget, which is why the ripple adder's $2N+1$ mattered and why carry-lookahead was worth $2\times$ the area.

**D3 (5).**

| logic | $T_{min}$ | $f_{max}$ |
|---|---:|---:|
| ripple, 2.58 ns | $0.05+2.58+0.03 = 2.66$ ns | **376 MHz** |
| CLA, 0.24 ns | $0.05+0.24+0.03 = 0.32$ ns | **3.13 GHz** |

*(Computed.)* **An 8.3× difference in achievable clock frequency.**

**D4 (5).** **A hold violation is data arriving at the next flip-flop *too early*** — before the previous edge's value was captured. **It depends on the delay from one flip-flop to the next, not on the clock period at all**, so a slower clock changes nothing.

**The fix is to add delay** — buffers on the fast path.

**D5 (5).** **Metastability:** a flip-flop whose setup or hold was violated may sit between valid levels for an unbounded time before resolving randomly.

**It occurs whenever a signal is sampled that is not derived from the sampling clock** — asynchronous inputs, other clock domains.

**A two-flip-flop synchroniser is a mitigation because it does not prevent the first flip-flop going metastable** — it gives it a full clock period to resolve before the second samples. **The probability of still being unresolved is small but non-zero**, so the failure rate is reduced, not eliminated.

*Marking: 5. **Full marks require the word "probability" or equivalent.***

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

1. **A2:** "because the datasheet says so."
2. **A4:** proposing careful input sequencing as the fix.
3. **B4:** a timing diagram with no $D$ change during a high phase.
4. **D4:** trying to fix a hold violation with a slower clock.
5. **D5:** claiming a synchroniser eliminates metastability.

---

*ECE 110 · Week 7 · PS 7 Solutions · Instructor Only*

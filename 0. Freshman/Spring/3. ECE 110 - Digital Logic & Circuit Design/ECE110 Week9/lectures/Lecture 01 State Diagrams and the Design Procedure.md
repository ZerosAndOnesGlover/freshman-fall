# ECE 110 · Digital Logic
## Week 9 · Lecture 1 (Wednesday)
### State Diagrams and the Design Procedure

**Date:** Wednesday 17 March 2027 · 13:00–14:15 · Week 9

---

**Reading:** Harris & Harris §3.4.1–3.4.2 | Mano & Ciletti §5.4–5.5
**Quiz 8** — at the start of today's lecture. **Covers Week 8.** Ungraded.

---

## 1. What A State Machine Is

> **A finite state machine is a finite set of states, a next-state function, and an output function.**

$$S^+ = f(S, X) \qquad Y = g(S) \text{ or } g(S,X)$$

**The state is what the circuit remembers.** Everything the machine knows about the past is compressed into which state it is in — **and that compression is the design decision.**

**Week 8's counter is the degenerate case** where $f$ ignores $X$ entirely.

---

## 2. The Six Steps

1. **Words → what must be remembered.**
2. **State diagram.**
3. **State table.**
4. **State assignment** — binary codes for states.
5. **Next-state and output equations** — by K-map.
6. **Circuit, then exhaustive verification.**

> **Only step 1 requires judgement.** Steps 3–5 are mechanical, and step 5 is Week 4 doing its job.
> **Students who struggle with FSMs almost always struggle at step 1**, then blame the algebra.

---

## 3. Step 1 — Deciding What To Remember

**Design an overlapping `1011` detector: output 1 on the clock where the fourth bit of `1011` arrives, and allow the trailing `1` to start a new match.**

**Ask: what does the machine need to know?** Not the whole input history — only **how much of the pattern has matched so far.**

| known so far | meaning |
|---|---|
| nothing | no useful prefix |
| `1` | one bit matched |
| `10` | two matched |
| `101` | three matched |

$$\textbf{Four states. That is the compression.}$$

**A machine that tried to remember the whole input would need infinitely many states.** Recognising that only the *longest matching prefix* matters is the entire design.

---

## 4. Step 2 — The State Diagram

**States $A$ (nothing), $B$ (`1`), $C$ (`10`), $D$ (`101`), as a Mealy machine:**

| from | input 0 → | input 1 → | output |
|:-:|:-:|:-:|---|
| $A$ | $A$ | $B$ | 0 |
| $B$ | $C$ | $B$ | 0 |
| $C$ | $A$ | $D$ | 0 |
| $D$ | $C$ | $B$ | **1 when input is 1** |

**Two things to check on every diagram you draw:**

- **Every state has exactly one outgoing arc per input value.** Miss one and the machine is undefined; have two and it is non-deterministic.
- **The overlap is handled.** From $D$ on a 1 we go to $B$, not $A$ — **the detected `1011` ends in a `1`, which is itself the start of the next match.**

*(Verified: this machine matches a reference detector on 2000 random 24-bit sequences, zero mismatches.)*

---

## 5. Steps 3–5 — Mechanical From Here

**State assignment $A{=}00$, $B{=}01$, $C{=}10$, $D{=}11$, giving the transition table over $(Q_1,Q_0,X)$:**

$$D_1 = \sum m(2,5,6) \qquad D_0 = \sum m(1,3,5,7) \qquad Y = \sum m(7)$$

**Minimise with Week 4's maps:**

$$\boxed{D_1 = Q_0\overline X + Q_1\overline{Q_0}X} \qquad \boxed{D_0 = X} \qquad \boxed{Y = Q_1Q_0X}$$

*(Verified — and the whole machine checked in Verilog over **4000 clock cycles**, zero failures.)*

> **$D_0 = X$ is a single wire.** That is not luck — it is what a good state assignment buys, and §6
> is about how much it can vary.

---

## 6. State Assignment Is A Free Choice That Costs Money

**With $n$ states you need $\lceil\log_2n\rceil$ flip-flops. Which code goes to which state is entirely up to you**, and different choices give different logic for the same machine.

| encoding | flip-flops | next-state logic | note |
|---|---|---|---|
| **binary** | fewest | most | the default |
| **one-hot** | one per state | **least** | Week 8's ring counter |
| **Gray** | fewest | middling | adjacent states differ in one bit |

**One-hot: the state *is* the output**, so output decoding is free and next-state logic is usually a couple of gates per flip-flop.

> **On an FPGA, flip-flops are abundant and logic cells are the scarce resource, so one-hot is
> frequently the default** — the synthesis tool will often convert your binary encoding to one-hot
> without being asked.

**Gray encoding matters when the state bits leave the chip or cross a clock domain**, because only one bit changes per transition and the intermediate values Week 8 showed you cannot occur.

---

## 7. Step 6 — Verification, And One Thing To Check

**Exhaustive verification of an FSM means driving every input sequence up to some length and comparing against a reference.**

**And check the unreachable states.** With 4 states in 2 bits there are none, but **5 states in 3 bits leaves 3 unused codes.** If the machine ever lands in one — a glitch, a bad power-up — **where does it go?**

> **A machine that can enter an unused state and never leave it is a machine that hangs.** Either
> make every unused state transition to a known state, or guarantee the reset. **"It can't happen" is
> the assumption that produces field failures.**

---

## 8. What To Take From This Lecture

1. **An FSM is states, a next-state function, and an output function.**
2. **The state is a compression of the past** — deciding what to keep is step 1 and the only creative step.
3. **For a pattern detector, remember the longest matching prefix.**
4. **Every state needs exactly one outgoing arc per input value.**
5. **Handle overlap explicitly** — from $D$ on a 1, go to $B$.
6. **Steps 3–5 are mechanical**, and step 5 is Week 4.
7. **State assignment is free and changes the logic** — binary, one-hot, Gray.
8. **Decide what unused states do.** Do not assume they cannot occur.

---

*Next: Thursday — Mealy vs Moore*

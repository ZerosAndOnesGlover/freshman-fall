# ECE 110 · Digital Logic
## Week 7 · Lecture 1 (Wednesday)
### Latches and the Forbidden State

**Date:** Wednesday 3 March 2027 · 13:00–14:15 · Week 7

---

**Reading:** Harris & Harris §3.2.1–3.2.2 | Mano & Ciletti §5.2
**Quiz 6** — at the start of today's lecture. **Covers Week 6.** Ungraded.

---

## 1. Memory Requires Feedback

**A combinational circuit is a function: same inputs, same outputs, always.** It cannot remember, because remembering means giving *different* outputs for the *same* inputs.

**Route an output back to an input and that changes.** The circuit's behaviour now depends on where it already is, and "where it already is" is **state**.

> **Feedback is not a trick added on top of combinational logic. It is the only mechanism there is.**
> Everything in the rest of this course — flip-flops, registers, counters, state machines, RAM — is
> feedback with increasingly careful discipline around it.

**And it costs you determinism.** A combinational circuit is analysed by a truth table. **A circuit with feedback has to be analysed by settling it**, and it may not settle to a unique answer.

---

## 2. The SR Latch

**Two cross-coupled NOR gates:**

$$Q = \overline{R + \overline Q} \qquad \overline Q = \overline{S + Q}$$

**Each output feeds the other's input. To find the state, iterate until nothing changes.**

| $S$ | $R$ | $Q$ | $\overline Q$ | behaviour |
|:-:|:-:|:-:|:-:|---|
| 0 | 0 | $Q_0$ | $\overline{Q_0}$ | **HOLD** |
| 0 | 1 | 0 | 1 | RESET |
| 1 | 0 | 1 | 0 | SET |
| 1 | 1 | **0** | **0** | **FORBIDDEN** |

*(All verified by iterating the network to a fixed point from both initial states.)*

**The hold row is the point of the whole circuit.** With both inputs at 0 the latch keeps whatever it had — **that is one bit of memory, built from two gates.**

---

## 3. Why $S=R=1$ Is Forbidden

**Both NOR gates see a 1 on an input, so both outputs go to 0.**

$$Q = 0 \quad\text{and}\quad \overline Q = 0$$

**The outputs are no longer complementary**, and the second output is named $\overline Q$ — the circuit is now lying about its own labelling. **Anything downstream that expects $Q$ and $\overline Q$ to be opposites is broken.**

### The race, which is the real problem

**Being in the forbidden state is survivable. *Leaving* it is not.**

**Drop $S$ and $R$ to 0 simultaneously from $S=R=1$.** Both gates now try to go high, each driven by the other's low output. **Whichever gate is fractionally faster wins**, and locks the other low.

| whichever settles first | final $Q$ |
|---|:-:|
| $Q$'s gate | $\mathbf 1$ |
| $\overline Q$'s gate | $\mathbf 0$ |

*(Verified — identical inputs, two different outcomes.)*

> **The final state is decided by manufacturing tolerances, temperature and supply voltage — not by
> the inputs.** This is a **race condition**, and it is the first circuit in this course whose output
> is not a function of its inputs.
>
> **You cannot fix a race by being careful with the inputs.** You fix it by making the bad input
> combination **unreachable**, which is §5.

---

## 4. Reading a Latch's Timing

**A latch has no clock. It responds whenever its inputs change**, after a propagation delay of two gates around the loop.

**That is both its virtue and its problem:** it is fast, and it is impossible to reason about in a large design, because "when did the state change?" has no clean answer.

---

## 5. The Gated D Latch

**Two fixes at once. Add an enable, and derive $S$ and $R$ from a single data input:**

$$S = D\cdot EN \qquad R = \overline D\cdot EN$$

**Now $S$ and $R$ can never both be 1** — they are complements whenever $EN=1$, and both 0 when $EN=0.$ *(Verified: the forbidden combination is unreachable by construction.)*

| $EN$ | behaviour |
|:-:|---|
| 1 | $Q$ **follows $D$** — transparent |
| 0 | $Q$ **holds** |

*(Verified over a driven sequence.)*

**The forbidden state is gone.** One problem remains.

### Transparency

**While $EN=1$, the output tracks the input continuously.** If $D$ wobbles during the enable window, $Q$ wobbles with it — and whatever the latch feeds sees every wobble.

> **In a system where a latch's output eventually reaches its own input** — a counter, a shift
> register, any state machine — **transparency means the state can race around the loop several times
> in one enable pulse.** The circuit updates an unpredictable number of times.

**That is tomorrow's problem, and the flip-flop is its solution.**

---

## 6. What To Take From This Lecture

1. **Memory requires feedback**, and feedback costs you the truth-table method.
2. **Two cross-coupled NOR gates hold one bit.**
3. **$S=R=1$ drives both outputs to 0** — $Q$ and $\overline Q$ stop being complementary.
4. **Leaving the forbidden state is a race**, decided by gate speed rather than by inputs.
5. **You fix a race by making the bad input unreachable**, not by being careful.
6. **The gated D latch does exactly that** with $S=D\cdot EN$, $R=\overline D\cdot EN$.
7. **It is still transparent**, and that is the remaining problem.

---

*Next: Thursday — Flip-Flops and Timing*

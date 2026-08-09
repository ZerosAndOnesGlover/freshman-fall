# ECE 110 · Digital Logic
## Week 9 · Reference Sheet
### Finite State Machines

---

## Definition

$$S^+ = f(S,X) \qquad\qquad Y = g(S) \ \text{[Moore]} \quad\text{or}\quad Y = g(S,X) \ \text{[Mealy]}$$

**The state is a compression of the past** — everything the machine knows, in one value.

---

## The Six Steps

1. **Words → what must be remembered**  ← *the only creative step*
2. **State diagram**
3. **State table**
4. **State assignment**
5. **Next-state and output equations** *(Week 4's K-maps)*
6. **Circuit + exhaustive verification**

**Check on every diagram: exactly one outgoing arc per state per input value.** Missing = undefined; duplicated = non-deterministic.

---

## Worked Example — Overlapping `1011` Detector

**What to remember: the longest matching prefix.** Four states.

| state | means | on 0 → | on 1 → | Mealy output |
|:-:|---|:-:|:-:|---|
| $A$ | nothing | $A$ | $B$ | 0 |
| $B$ | `1` | $C$ | $B$ | 0 |
| $C$ | `10` | $A$ | $D$ | 0 |
| $D$ | `101` | $C$ | $B$ | **1 on input 1** |

> **The overlap arc is $D \xrightarrow{1} B$, not $D \xrightarrow{1} A$** — the detected `1011` ends
> in a `1`, which starts the next match.

**With $A{=}00, B{=}01, C{=}10, D{=}11$:**

$$D_1 = \sum m(2,5,6) = Q_0\overline X + Q_1\overline{Q_0}X$$
$$D_0 = \sum m(1,3,5,7) = X$$
$$Y = \sum m(7) = Q_1Q_0X$$

*(verified in Verilog over 4000 cycles against a reference: 0 failures)*

$$\texttt{1011011011} \;\Rightarrow\; \texttt{0001001001}$$

*(verified — both Mealy and Moore match a reference on 2000 random 24-bit sequences)*

---

## Mealy vs Moore

| | Moore | Mealy |
|---|---|---|
| output | $g(S)$, on the **states** | $g(S,X)$, on the **arcs** |
| changes | at the clock edge | as soon as the input does |
| glitches | **no** | **possible** |
| states here | **5** | **4** |
| flip-flops here | 3 | **2** |

> **Mealy distinguishes with its output what Moore must distinguish with a state.**

**On timing:** the usual "Moore lags by one cycle" **depends on where the output is taken.** Read after the transition it is aligned with Mealy; read before, it lags. **State your convention.**

### Choosing

| use | when |
|---|---|
| **Moore** | the output drives anything edge-sensitive — a write-enable, a strobe. **Week 8's glitch corrupts memory.** |
| **Mealy** | fewer states matter, or the response must be same-cycle |
| **registered Mealy** | both — compute $g(S,X)$, then flip-flop it |

---

## State Assignment

**$\lceil\log_2 n\rceil$ flip-flops minimum; which code goes where is free and changes the logic.**

| encoding | flip-flops | logic | note |
|---|---|---|---|
| **binary** | fewest | most | default |
| **one-hot** | one per state | **least** | Week 8's ring counter; state *is* the output |
| **Gray** | fewest | middling | one bit changes per transition |

> **One-hot is often the FPGA default** — flip-flops are abundant there and logic cells are scarce
> *(Week 5)*. Tools frequently convert binary to one-hot unasked.

**Gray matters when state bits leave the chip or cross clock domains** — no intermediate values, so Week 8's transient problem cannot occur.

---

## Robustness

**Unused state codes:** 5 states in 3 bits leaves **3 unused**. **Decide what they do.**

> **A machine that can enter an unused state and never leave hangs.** Either give every unused code a
> transition to a known state, or guarantee the reset. **"It can't happen" produces field failures.**

**Reset is mandatory.** *(Week 8's ring counter stuck at `0000` is the same lesson.)*

> ⚠ **An asynchronous reset already asserted at time 0 never fires** — `always @(posedge rst)` needs
> a rising *edge*. The state stays `x`. **Pulse it: 0 → 1 → 0.** *(This cost a debugging session
> while preparing Week 9's simulation.)*

---

## Common Errors

1. **A state missing an outgoing arc** for some input value.
2. **Sending the overlap arc to the start state** instead of the correct prefix state.
3. **Trying to remember the input** rather than the prefix.
4. **Comparing Mealy and Moore outputs without stating the output convention.**
5. **Using Mealy for an edge-sensitive output.**
6. **Leaving unused state codes undefined.**
7. **An asynchronous reset that is never pulsed.**

---

*ECE 110 · Week 9 · Reference Sheet*

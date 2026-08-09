# ECE 110 · Digital Logic
## Week 8 · Reference Sheet
### Registers, Counters, Shift Registers

---

## Register

**$N$ flip-flops, one clock. All bits change together.**

**With load enable — a 2:1 mux per bit:**

$$D_i = \text{LOAD}\cdot\text{data}_i + \overline{\text{LOAD}}\cdot Q_i$$

> ⚠ **Gate the DATA, never the CLOCK.** `CLK · LOAD` creates a second clock with its own skew and
> glitch hazards — works in simulation, fails in silicon.

---

## Shift Register

**Flip-flops in series; everything moves one place per edge.**

**`1011` shifting right, serial-in 0:**

| clock | out | state |
|:-:|:-:|:-:|
| — | — | `1011` |
| 1 | 1 | `0101` |
| 2 | 1 | `0010` |
| 3 | 0 | `0001` |
| 4 | 1 | `0000` |

*(verified)*

| in → out | name | use |
|---|---|---|
| serial → serial | SISO | delay line |
| serial → parallel | **SIPO** | deserialiser (UART rx) |
| parallel → serial | **PISO** | serialiser (UART tx) |
| parallel → parallel | — | register with shift |

**Shift left = ×2, shift right = ÷2.** **Signed right shift must copy the sign bit** (arithmetic, not logical) — same idea as Week 0's sign extension.

---

## Ring and Johnson Counters

**Ring — last $Q$ back to first $D$:**

$$\texttt{0001}\to\texttt{0010}\to\texttt{0100}\to\texttt{1000}\to\texttt{0001}$$

*(verified)*

| | flip-flops | states | decode logic |
|---|---:|---:|---|
| binary counter | 4 | 16 | needed |
| **ring** | 4 | **4** | **none** |
| Johnson ($\overline Q$ fed back) | 4 | 8 | minimal |

> **A ring counter's state IS its one-hot output.** Expensive in flip-flops, free in gates — often
> the right trade for a controller.

**Powering up at `0000` leaves a ring counter stuck forever. Reset is not optional.**

---

## Ripple (Asynchronous) Counter

**Each flip-flop clocked by the previous one. $N$ flip-flops, ZERO gates.**

### Flaw 1 — transient states

**3-bit, going $3\to4$:**

| after | state | reads |
|---|:-:|---:|
| start | `011` | 3 |
| bit 0 | `010` | **2** |
| bit 1 | `000` | **0** |
| bit 2 | `100` | 4 |

*(verified)*

> **A decoder watching this glitches** — an output meant to fire only at 0 fires on every
> $2^k-1 \to 2^k$ transition. **If it drives a write-enable, that corrupts memory.**

### Flaw 2 — linear delay

$$t_{\text{settle}} = N\cdot t_{cq}$$

| $N$ | 4 | 8 | 16 | 32 |
|---|---|---|---|---|
| settle | $4t_{cq}$ | $8t_{cq}$ | $16t_{cq}$ | $32t_{cq}$ |

**This is Week 3's ripple-carry adder — a serial dependency chain.**

---

## Synchronous Counter

**One clock for all; logic decides who toggles.**

> **Bit $k$ toggles when every lower bit is 1** — which is what carrying means.

$$T_0=1 \qquad T_1=Q_0 \qquad T_2=Q_0Q_1 \qquad T_3=Q_0Q_1Q_2$$

*(verified: correct mod-16 sequence, all bits changing on the same edge)*

| $N$ | ripple | synchronous tree depth |
|---:|---:|---:|
| 4 | $4t_{cq}$ | 2 |
| 8 | $8t_{cq}$ | 3 |
| 16 | $16t_{cq}$ | 4 |
| 32 | $32t_{cq}$ | **5** |

*(verified)*

**No transient states. Logarithmic delay. Costs the toggle logic.**

> **Area bought speed AND correctness** — the third instance of the same trade (Week 4 cut area,
> Week 6 spent it for adder speed, Week 8 spends it for counter speed and glitch-freedom).

---

## Mod-N Counters

**Detect the state after the last one wanted, and clear.**

**Mod-10: detect $10 = \texttt{1010}$.**

$$\boxed{\text{clear} = Q_3Q_1}$$

**Two gates, not four** — no count below 10 has both bits set, so $Q_3Q_1$ identifies 10 uniquely among reachable states. *(verified)* **This is a Week 4 don't-care argument.**

**Sequence: $0,1,\ldots,9,0,\ldots$** *(verified)*

> **Asynchronous clear means the counter DOES briefly enter state 10** before being wiped — a
> spurious output pulse. **Synchronous clear** feeds the detect into the next-state logic so 9 goes
> directly to 0 and state 10 never exists.

---

## Common Errors

1. **Gating the clock** to make a load enable.
2. **Assuming a ripple counter's outputs are always a valid count.**
3. **Decoding a ripple counter** without expecting glitches.
4. **Forgetting reset**, especially on a ring counter.
5. **Logical instead of arithmetic right shift** on signed data.
6. **Decoding all four bits for mod-10** when two suffice — or relying on two without noting the assumption.
7. **Asynchronous clear** where a synchronous one is wanted.

---

*ECE 110 · Week 8 · Reference Sheet*

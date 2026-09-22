# ECE 110 · Digital Logic
## Week 8 · Lecture 1 (Wednesday)
### Registers and Shift Registers

**Date:** Wednesday 17 March 2027 · 13:00–14:15 · Week 8

---

**Reading:** Harris & Harris §3.3, §5.4.1 | Mano & Ciletti §6.1–6.2
**Quiz 7** — at the start of today's lecture. **Covers Week 7.** Ungraded.

---

## 1. The Register

> **$N$ flip-flops sharing one clock. That is the whole thing.**

$$Q^+_i = D_i \text{ for every } i, \text{ at the same edge}$$

**Because they share the clock, all $N$ bits change together** — the register is never half-updated, and downstream logic sees a clean transition.

### With a load enable

**Most registers should not update every cycle.** Add an enable:

$$D_i = \text{LOAD} \cdot \text{data}_i + \overline{\text{LOAD}}\cdot Q_i$$

**That is a 2:1 multiplexer per bit** — Week 5's block, recycled.

> **Do not build a load enable by gating the clock.** Feeding `CLK · LOAD` into the flip-flops
> creates a second, narrower clock with its own skew and glitch hazards, and it is one of the
> classic ways to make a design that works in simulation and fails in silicon. **Gate the data, not
> the clock.**

**A processor's register file is a stack of these** with decoders selecting which to write and multiplexers selecting which to read — every block from Week 5.

---

## 2. The Shift Register

> **$N$ flip-flops in series: each one's output is the next one's input.**

**Every clock edge, the whole contents move one place.**

**A 4-bit register holding `1011`, shifting right, serial-in 0:**

| clock | shifted out | state |
|:-:|:-:|:-:|
| — | — | `1011` |
| 1 | **1** | `0101` |
| 2 | **1** | `0010` |
| 3 | **0** | `0001` |
| 4 | **1** | `0000` |

*(Verified.)*

**Note the bits come out in order** — that is the point.

### The four modes

| in | out | called |
|---|---|---|
| serial | serial | SISO — a delay line |
| serial | parallel | **SIPO — deserialiser** |
| parallel | serial | **PISO — serialiser** |
| parallel | parallel | a register with shift |

**SIPO and PISO are how a serial link works.** A UART is a PISO on the transmit side and a SIPO on the receive side; **every byte you have ever sent over a serial port went through both.**

### Shifting is arithmetic

**Left shift multiplies by 2; right shift divides by 2** — Week 6's free ALU operation, now with state.

> **For signed values, a right shift must copy the sign bit** — an *arithmetic* shift, not a logical
> one. Shifting in 0 turns $-4$ into a large positive number. **Same distinction as Week 0's sign
> extension.**

---

## 3. The Ring Counter

**Feed the last output back to the first input.**

$$\texttt{0001}\to\texttt{0010}\to\texttt{0100}\to\texttt{1000}\to\texttt{0001}\to\cdots$$

*(Verified.)*

**Four flip-flops, four states, and *no logic at all*.** The state is already one-hot, so **the outputs need no decoding** — each flip-flop's $Q$ *is* the "we are in state $k$" signal.

| | flip-flops | states | decode logic |
|---|---:|---:|---|
| binary counter | 4 | 16 | needed |
| **ring counter** | 4 | **4** | **none** |

> **A ring counter is expensive in flip-flops and free in logic**, and that is often the right trade
> for a controller: the states are few, and the outputs are wanted one-hot anyway. **You will use
> this in Week 9.**

**A Johnson counter** feeds back $\overline Q$ instead, giving $2N$ states from $N$ flip-flops — half the density of binary, twice the ring, still cheap to decode.

---

## 4. Initialisation — The Thing Beginners Forget

**On power-up, a flip-flop's state is undefined.** A ring counter that starts at `0000` stays at `0000` forever; one that starts with two bits set circulates two bits forever.

**Every sequential circuit needs a reset**, and you must decide:

- **Asynchronous reset** — acts immediately, independent of the clock. Good for power-up.
- **Synchronous reset** — acts at the next edge. Cleaner timing, but useless if the clock is not running.

> **A design without a defined initial state is not finished.** In simulation the state shows as
> `x` and propagates everywhere, which is Verilog telling you the truth rather than being unhelpful.

---

## 5. What To Take From This Lecture

1. **A register is $N$ flip-flops on one clock** — all bits change together.
2. **A load enable is a 2:1 mux per bit. Gate the data, never the clock.**
3. **A shift register moves everything one place per edge.**
4. **SIPO and PISO are how serial links work.**
5. **Shifting is multiply/divide by 2**, and signed right shifts must copy the sign bit.
6. **A ring counter needs no decode logic** — expensive in flip-flops, free in gates.
7. **Every sequential circuit needs a reset.** Undefined initial state is a design defect.

---

*Next: Thursday — Counters, Ripple and Synchronous*

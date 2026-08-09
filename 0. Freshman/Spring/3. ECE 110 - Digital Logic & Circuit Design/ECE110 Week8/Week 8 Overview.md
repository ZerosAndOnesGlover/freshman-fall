# ECE 110 · Digital Logic
## Week 8 · Overview
### Registers, Counters, and Shift Registers

---

**Topic:** remembering more than one bit
**Reading:** Harris & Harris §3.3, §5.4 | Mano & Ciletti §6.1–6.4
**Assessment this week:** PS 8, Lab 8, **Quiz 7** *(Wednesday — covers Week 7, ungraded)*

---

## One Flip-Flop Is Not A Machine

**Week 7 gave you one bit of memory with a clean edge-triggered interface. This week you put them side by side and in series, and get the three structures every digital system is built from.**

| structure | flip-flops arranged | gives you |
|---|---|---|
| **Register** | in parallel, shared clock | store $N$ bits at once |
| **Shift register** | in series | move data one bit per clock |
| **Counter** | with next-state logic | a sequence of states |

**A processor's register file is the first. A serial link is the second. A program counter is the third.**

---

## The Two Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Wednesday | Registers and Shift Registers | Parallel and serial |
| **Lecture 2** | Thursday | Counters — Ripple and Synchronous | The same delay question as Week 3 |

---

## Week 3's Question, In Sequential Clothing

**There are two ways to build a counter, and the difference is exactly the difference between the ripple-carry and carry-lookahead adders.**

### Ripple (asynchronous) counter

**Each flip-flop is clocked by the previous one's output.** Simple — $N$ flip-flops and **no logic at all**.

**But the bits change in sequence, not together.** A 3-bit counter going $011 \to 100$:

| after | state | value |
|---|---|---:|
| start | `011` | 3 |
| bit 0 flips | `010` | **2** ← transient |
| bit 1 flips | `000` | **0** ← transient |
| bit 2 flips | `100` | 4 |

*(Verified.)*

> **The counter briefly reads 2, then 0, on its way from 3 to 4.** Anything watching it — a decoder,
> a comparator — **sees states that were never intended.** And the settling time is $N\cdot t_{cq}$,
> growing linearly with width.

### Synchronous counter

**All flip-flops share one clock; logic decides which should toggle.**

$$T_0=1,\quad T_1=Q_0,\quad T_2=Q_0Q_1,\quad T_3=Q_0Q_1Q_2$$

*(Verified: produces the correct mod-16 sequence.)*

**Every bit changes at the same edge, so there are no transient states**, and the delay is one $t_{cq}$ plus an AND tree — **logarithmic in width, not linear.**

| $N$ | ripple settle | synchronous logic depth |
|---:|---:|---:|
| 4 | $4\,t_{cq}$ | 2 |
| 8 | $8\,t_{cq}$ | 3 |
| 16 | $16\,t_{cq}$ | 4 |
| 32 | $32\,t_{cq}$ | **5** |

*(Verified.)*

**The cost is the toggle logic** — gates you did not need before.

> **This is Week 3 again: a serial dependency traded away for area.** You have now seen the same
> structural argument in combinational and in sequential form, and **that is the point of putting them
> in the same course.**

---

## Shift Registers

**Flip-flops in series: each clock, every bit moves one place.**

**A 4-bit register holding `1011`, shifting right with serial-in 0:**

$$\texttt{1011} \to \texttt{0101} \to \texttt{0010} \to \texttt{0001} \to \texttt{0000}$$

*(Verified.)*

**Uses:** serial-to-parallel conversion (every UART), multiply and divide by two, and delay lines.

### The ring counter

**Feed the last output back to the first input.** From `0001`:

$$\texttt{0001}\to\texttt{0010}\to\texttt{0100}\to\texttt{1000}\to\texttt{0001}$$

*(Verified.)*

**A 4-state counter using 4 flip-flops and *no decode logic whatsoever*** — the state *is* the one-hot output. **Expensive in flip-flops, free in logic**, and it is exactly how many controllers are built.

---

## This Week's Work

1. **Quiz 7** — Wednesday, covers Week 7. **Ungraded.**
2. **Lab 8** — build both counters and **observe the ripple counter's transients**.
3. **PS 8** — register design, counter design, mod-N counters.

---

*Next: Wednesday — Registers and Shift Registers*

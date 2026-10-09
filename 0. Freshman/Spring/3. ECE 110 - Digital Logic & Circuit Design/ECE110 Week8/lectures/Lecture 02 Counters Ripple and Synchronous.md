# ECE 110 · Digital Logic
## Week 8 · Lecture 2 (Thursday)
### Counters — Ripple and Synchronous

*“Musica est exercitium arithmeticae occultum nescientis se numerare animi. [Music is a hidden arithmetic exercise of the soul, which does not know that it is counting.]”* — Gottfried Wilhelm Leibniz, letter to Christian Goldbach (1712)

**Date:** Thursday 18 March 2027 · 13:00–14:15 · Week 8

**Coursework:** 📝 **PS 7** due today 13:00 · 📝 **PS 8** released today 14:30, due Thu 25 Mar 13:00 · 🔬 **Lab 8** Fri 19 Mar 14:00–15:50 · 📊 **Quiz 8** Wed 24 Mar 13:00–13:10

---

**Reading:** Harris & Harris §5.4.2 | Mano & Ciletti §6.3–6.4
**PS 8** released today, due Thursday of Week 9.

---

## 1. The Simplest Counter

**Week 7's Lab, Part C3: wire $\overline Q$ back to $D$ and the flip-flop toggles every clock — a divide-by-2.**

**Chain them: each flip-flop clocked by the previous one's output.** That is a **ripple counter**, and it costs $N$ flip-flops and **zero gates**.

**It counts correctly.** And it has two problems.

---

## 2. Problem One — Transient States

**The flip-flops do not change together.** Bit 1 cannot toggle until bit 0 has changed, which takes $t_{cq}$.

**Watch a 3-bit ripple counter go from 3 to 4:**

| after | state | reads as |
|---|:-:|---:|
| start | `011` | 3 |
| bit 0 flips | `010` | **2** |
| bit 1 flips | `000` | **0** |
| bit 2 flips | `100` | 4 |

*(Verified.)*

> **On its way from 3 to 4 the counter briefly reads 2, and then 0.** These are **transient states** —
> real, observable, and never intended.
>
> **A decoder watching this counter glitches**: an output meant to fire only at 0 fires spuriously
> on every $2^k-1 \to 2^k$ transition. **If that output is a write-enable, you have just corrupted
> memory.**

---

## 3. Problem Two — Linear Delay

**The settling time is $N \cdot t_{cq}$** — bit $N-1$ waits for every bit below it.

| $N$ | settle |
|---:|---:|
| 4 | $4\,t_{cq}$ |
| 8 | $8\,t_{cq}$ |
| 16 | $16\,t_{cq}$ |
| 32 | $32\,t_{cq}$ |

*(Verified.)*

**This is Week 3's ripple-carry adder, exactly.** A serial dependency chain, linear in width, and the clock period must accommodate the whole thing.

---

## 4. The Synchronous Counter

**Give every flip-flop the same clock, and use logic to decide which ones toggle.**

> **Bit $k$ toggles when every bit below it is 1** — which is exactly what carrying means.

$$T_0 = 1 \qquad T_1 = Q_0 \qquad T_2 = Q_0Q_1 \qquad T_3 = Q_0Q_1Q_2$$

*(Verified: produces the correct mod-16 sequence, and every bit changes at the same edge.)*

### What it fixes

**No transient states** — all flip-flops update simultaneously, so the counter goes from 3 to 4 with nothing in between.

**Delay is $t_{cq}$ + the AND tree + $t_{su}$**, and the tree is **logarithmic**:

| $N$ | ripple | synchronous tree depth |
|---:|---:|---:|
| 4 | $4\,t_{cq}$ | 2 |
| 8 | $8\,t_{cq}$ | 3 |
| 16 | $16\,t_{cq}$ | 4 |
| 32 | $32\,t_{cq}$ | **5** |

*(Verified.)*

### What it costs

**The toggle logic** — an AND tree that grows with width, where the ripple counter needed nothing.

> **Area bought speed and correctness.** **This is the third time in the course**: Week 4 minimised
> area, Week 6 spent area for adder speed, and now area buys a counter that is both faster and free
> of transient states. **The trade is the same one every time, and by now you should expect the
> question rather than be surprised by it.**

---

## 5. Counting To Something Other Than $2^N$

**A mod-10 (BCD) counter counts $0\ldots9$ and returns to 0.**

**Method: detect the state after the last one you want, and clear.** For mod-10, detect **10 = `1010`**.

$$\text{clear} = Q_3Q_1$$

**Two gates, not four.** *(Verified: no count below 10 has both $Q_3$ and $Q_1$ set, so $Q_3Q_1$ identifies 10 uniquely among the states that occur.)*

**Sequence produced: $1,2,\ldots,9,0,1,2,\ldots$** *(Verified.)*

> **This is a don't-care argument from Week 4**, and worth naming as one: you do not need to decode
> all four bits, because the counter can never be in states 11–15. **If it somehow were — a glitch, a
> bad power-up — the detect would fail**, which is why a robust design either decodes fully or
> guarantees the reset.

### Asynchronous clear is a hazard

**Detecting 10 and clearing asynchronously means the counter *does* briefly enter state 10** before being wiped — a very short spurious state on the outputs.

**The clean alternative is a synchronous clear**: the detect feeds the next-state logic so 9 goes directly to 0, and state 10 never exists.

---

## 6. What To Take From This Lecture

1. **A ripple counter is $N$ flip-flops and no gates** — and has two flaws.
2. **Transient states are real and observable**: $011\to010\to000\to100$.
3. **A decoder on a ripple counter glitches**, which can be catastrophic if it drives an enable.
4. **Ripple settling is $N\,t_{cq}$** — Week 3's serial dependency again.
5. **A synchronous counter toggles bit $k$ when all lower bits are 1.**
6. **It has no transient states and logarithmic delay**, at the cost of the toggle logic.
7. **Mod-N by detect-and-clear**; $Q_3Q_1$ suffices for mod-10 by a don't-care argument.
8. **Synchronous clear avoids the spurious state** that asynchronous clear creates.

---

*Next: Friday — Lab 8, and catching the transients*

# ECE 110 · Digital Logic
## Week 7 · Overview
### Latches and Flip-Flops — SR, D, JK, T

---

**Topic:** how a circuit remembers
**Reading:** Harris & Harris §3.2 | Mano & Ciletti §5.1–5.3
**Assessment this week:** PS 7 (released Thu 11 Mar 14:30, due Thu 18 Mar 13:00), Lab 7 (**Fri 12 Mar**, 14:00), **Quiz 6** *(Wed 10 Mar, 13:00 — covers Week 6, ungraded)*

---

## The Course Changes Here

**Everything through Week 6 was *combinational*: outputs depend only on present inputs.** Feed the same inputs in and you get the same outputs out, always.

**A circuit that remembers must do something a combinational circuit cannot: give different outputs for the same inputs**, depending on what happened earlier.

**There is exactly one way to get that, and it is feedback.** Route an output back to an input and the circuit has a state.

> **This is the second half of digital design and it is harder than the first**, because a
> combinational circuit is a function and a sequential circuit is a *machine*. Timing stops being
> something you measure afterwards and becomes something you must design for.

---

## The Two Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Wednesday | Latches and the Forbidden State | Feedback, and what it costs |
| **Lecture 2** | Thursday | Flip-Flops and Timing | Edges, setup and hold |

---

## The SR Latch, and Its Flaw

**Two cross-coupled NOR gates. That is the whole memory element.**

| $S$ | $R$ | behaviour |
|:-:|:-:|---|
| 0 | 0 | **hold** — the state persists |
| 0 | 1 | reset, $Q=0$ |
| 1 | 0 | set, $Q=1$ |
| 1 | 1 | **forbidden** |

*(All verified by iterating the gate network to a fixed point.)*

**Why $S=R=1$ is forbidden: both outputs go to 0**, so $Q$ and $\overline Q$ are **both 0** — not complementary, which breaks the one promise the circuit makes.

### And it is worse than that

**Leave the forbidden state by dropping $S$ and $R$ to 0 at the same instant, and the result depends on which gate is faster:**

| whichever settles first | final $Q$ |
|---|:-:|
| $Q$ | **1** |
| $\overline Q$ | **0** |

*(Verified — the same inputs give different answers.)*

> **That is a race**, and it is the first time in this course that a circuit's output is not
> determined by its inputs. **The rest of the week is about eliminating races**, and the D latch,
> the D flip-flop and the JK flip-flop are each a fix for one.

---

## The Fixes, In Order

| device | fixes | how |
|---|---|---|
| **Gated D latch** | the forbidden state | $S=D\cdot EN$, $R=\overline D\cdot EN$ — **$S=R=1$ becomes unreachable** |
| **D flip-flop** | transparency | master–slave: the state changes only on a clock **edge** |
| **JK flip-flop** | $S=R=1$ being useless | $J=K=1$ **toggles** instead of being forbidden |
| **T flip-flop** | — | a JK with $J$ and $K$ tied together |

*(Verified: the D latch's $S$ and $R$ cannot both be 1; a structural master–slave DFF built from NAND gates is edge-triggered and **not** transparent — 12 clock edges, zero failures.)*

---

## The Two Tables You Need

**Characteristic table — what the device does:**

$$D: Q^+ = D \qquad JK: Q^+ = J\overline Q + \overline KQ \qquad T: Q^+ = T\oplus Q$$

**Excitation table — what inputs produce a wanted transition:**

| $Q \to Q^+$ | $D$ | $T$ | $JK$ |
|:-:|:-:|:-:|:-:|
| $0\to0$ | 0 | 0 | $0\times$ |
| $0\to1$ | 1 | 1 | $1\times$ |
| $1\to0$ | 0 | 1 | $\times1$ |
| $1\to1$ | 1 | 0 | $\times0$ |

*(Verified.)*

> **Note the $\times$'s in the JK column — those are don't-cares**, and Week 4 told you exactly what
> don't-cares are worth. **JK-based state machines minimise better than D-based ones**, which is the
> only reason JK survives in a world where D is simpler.

---

## This Week's Work

1. **Quiz 6** — Wed 10 Mar, covers Week 6. **Ungraded.**
2. **Lab 7** — build a latch from gates, observe the forbidden state, then build a flip-flop.
3. **PS 7** — characteristic and excitation tables, timing.

---

*Next: Wednesday — Latches and the Forbidden State*

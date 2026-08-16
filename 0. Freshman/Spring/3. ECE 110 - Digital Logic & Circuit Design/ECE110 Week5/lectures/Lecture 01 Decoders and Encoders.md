# ECE 110 · Digital Logic
## Week 5 · Lecture 1 (Wednesday)
### Decoders and Encoders

**Date:** Wednesday 17 February 2027 · 13:00–14:15 · Week 5

---

**Reading:** Harris & Harris §2.8 | Mano & Ciletti §4.9–4.10
**Quiz 4** — at the start of today's lecture. **Covers Week 4.** Ungraded.

---

## 1. The Decoder

> **An $n$-to-$2^n$ decoder asserts exactly one output — the one named by its $n$-bit input.**

**2:4 decoder:**

| $S_1$ | $S_0$ | $Y_3$ | $Y_2$ | $Y_1$ | $Y_0$ |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 0|0| 0|0|0|**1** |
| 0|1| 0|0|**1**|0 |
| 1|0| 0|**1**|0|0 |
| 1|1| **1**|0|0|0 |

$$Y_0 = \overline{S_1}\,\overline{S_0} \quad Y_1 = \overline{S_1}S_0 \quad Y_2 = S_1\overline{S_0} \quad Y_3 = S_1S_0$$

*(Verified: exactly one output is high for every input.)*

**Those four expressions are the four minterms of two variables.** That is not a coincidence and §3 makes use of it.

### Cost, and the enable

| decoder | AND gates | inverters |
|---|---:|---:|
| 2:4 | 4 | 2 |
| 3:8 | 8 | 3 |
| 4:16 | 16 | 4 |

**An $n$-input decoder costs $2^n$ AND gates** — it grows exponentially, which is why decoders stay small and are built in trees when they must be large.

**Most decoders have an enable.** With `EN = 0` **every** output is low. *(Verified.)* **That is what makes chip-select logic work**, and it is what turns a decoder into a demultiplexer tomorrow.

---

## 2. The Encoder

> **A $2^n$-to-$n$ encoder does the reverse: given one asserted input, output its index.**

**4:2 encoder:** $A_1 = I_3+I_2$, $A_0 = I_3+I_1$.

### The two things wrong with it

**Give it two asserted inputs and the output is garbage** — $I_1$ and $I_2$ together produce $11$, which names $I_3$. *(Verified.)*

**Give it none and it outputs $00$** — **exactly what it outputs for $I_0$.** The circuit cannot distinguish "line 0" from "nothing at all".

---

## 3. The Priority Encoder

> **Reports the *highest-numbered* asserted input, and adds a **valid** output.**

| inputs | code | valid |
|---|:-:|:-:|
| `0110` | $2$ | 1 |
| `0001` | $0$ | 1 |
| `0000` | $0$ | **0** |

*(Verified.)*

**The valid bit is the entire fix.** With it, $\text{code}=0$ means "line 0" when valid is 1 and "nothing" when valid is 0.

> **This is the same design move as Week 0's overflow flag and Week 3's $V$ output:** a **status
> output** whose job is to tell you whether to believe the data output. **You will see it every time
> a circuit's output space is smaller than the situations it must represent.**

**Priority encoders are how interrupt controllers pick which device to service.**

---

## 4. A Decoder Plus An OR Gate Is A Universal Circuit

**The decoder outputs *are* the minterms.** So Week 1's canonical SOP has a direct hardware form:

$$F = \sum m(1,3,5,6,7) \;\Rightarrow\; \text{3:8 decoder, then OR together } Y_1,Y_3,Y_5,Y_6,Y_7$$

*(Verified equal to $C+AB$ on all eight inputs.)*

**No algebra. No map. Read the minterm list off the truth table and wire the OR.**

### And the catch

**It costs 8 AND gates plus a 5-input OR** to implement a function that minimises to **two gates**. **The decoder approach is fast to design and expensive to build.**

> **That trade — design effort against silicon — is the reason both approaches survive.** One-off
> control logic gets a decoder; something replicated a million times gets minimised properly.
>
> **A decoder with several ORs hanging off it is efficient**, though, because the decoder is shared:
> $m$ functions of the same $n$ inputs cost one decoder and $m$ OR gates. **That is a ROM**, and it is
> Week 11.

---

## 5. What To Take From This Lecture

1. **A decoder asserts exactly one output** — its outputs are the minterms.
2. **$2^n$ AND gates**: decoders grow exponentially, so they stay small or go in trees.
3. **The enable turns everything off**, and becomes the demux data input tomorrow.
4. **A plain encoder breaks on multiple inputs and cannot detect none.**
5. **A priority encoder fixes both, and the *valid* bit is the fix** — the same idea as an overflow flag.
6. **Decoder + OR implements any function directly from the minterm list** — fast to design, expensive to build.
7. **Sharing one decoder across many outputs is a ROM.**

---

*Next: Thursday — Multiplexers and Demultiplexers*

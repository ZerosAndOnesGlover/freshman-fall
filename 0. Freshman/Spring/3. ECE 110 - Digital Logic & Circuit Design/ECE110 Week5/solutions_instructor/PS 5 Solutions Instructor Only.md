# ECE 110 · Digital Logic
## Problem Set 5 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All designs verified exhaustively.

---

## Part A (5 pts each)

**A1 (5).** $Y_i = \text{EN}\cdot m_i$: $Y_0=E\overline{S_1}\,\overline{S_0}$, $Y_1=E\overline{S_1}S_0$, $Y_2=ES_1\overline{S_0}$, $Y_3=ES_1S_0$. **Exactly one output high when $E=1$; all low when $E=0$.** *(Verified.)*

**A2 (5).** $2^n$ AND gates, $n$ inverters.

| $n$ | ANDs | inverters |
|---:|---:|---:|
| 2 | 4 | 2 |
| 3 | 8 | 3 |
| 4 | 16 | 4 |

**Growth is exponential**, so large decoders are built as **trees of small ones** rather than flat.

**A3 (5).** Two 2:4 decoders share $S_1,S_0$. **$S_2$ enables the upper decoder and $\overline{S_2}$ the lower.** *(Verified: reproduces the 3:8 truth table exactly.)*

**The enables do the third bit of decoding** — which is the general trick for composing decoders.

**A4 (5).** $A_1=I_3+I_2$, $A_0=I_3+I_1$.

**Two failures:** (i) **two inputs high gives garbage** — $I_1,I_2$ together produce $11$, naming $I_3$; (ii) **no input high gives $00$**, which is also what $I_0$ gives. *(Verified.)*

---

## Part B (6 pts each)

**B1 (6).**

| $I_3$ | $I_2$ | $I_1$ | $I_0$ | $A_1$ | $A_0$ | valid |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 0|0|0|0| 0|0| **0** |
| 0|0|0|1| 0|0| 1 |
| 0|0|1|$\times$| 0|1| 1 |
| 0|1|$\times$|$\times$| 1|0| 1 |
| 1|$\times$|$\times$|$\times$| 1|1| 1 |

**B2 (6).** $A_1 = I_3+I_2$, $A_0 = I_3+I_2'I_1$ *(equivalently $I_3 + \overline{I_2}I_1$)*, $\text{valid}=I_3+I_2+I_1+I_0$.

**B3 (6).** It distinguishes **"$I_0$ is asserted"** from **"nothing is asserted"** — both give code $00$, and only the valid bit tells them apart. *(Verified.)*

**B4 (6).** **An interrupt controller.** Several devices can raise a request simultaneously; the priority encoder names the highest-priority one so the CPU services it first, and *valid* says whether any interrupt is pending at all.

**B5 (6).** **Both are status outputs that say whether to trust the data output.**

Overflow $V$ says the sum bits do not mean what they appear to; *valid* says the code bits do not name anything. **In both cases the data output alone is ambiguous, and the flag resolves it.**

> **The general pattern: whenever a circuit's output space is smaller than the set of situations it
> must represent, you need a status bit.**

*Marking: 6, **full marks require the general statement**, not just "both are flags".*

---

## Part C (6 pts each)

**C1 (6).** $Y=\overline{S_1}\,\overline{S_0}D_0+\overline{S_1}S_0D_1+S_1\overline{S_0}D_2+S_1S_0D_3$.

**The four product terms $\overline{S_1}\,\overline{S_0}$ … $S_1S_0$ are a 2:4 decoder** on the select lines; the mux ANDs each decoded line with its data input and ORs the results.

**C2 (6).** Two 4:1 muxes selected by $S_1S_0$, their outputs feeding a 2:1 mux selected by $S_2$. *(Or seven 2:1 muxes in a 3-level tree.)*

**C3 (6).** In a decoder, output $i$ is $\text{EN}\cdot m_i$. **Feed the data onto EN**: the selected output becomes the data, and every other output is $0\cdot\text{data}=0$. **That is exactly demultiplexing.** *(Verified.)*

**C4 (6).** $F=\sum m(1,2,4,7)$, $A,B$ selecting:

| sel $AB$ | data |
|:-:|:-:|
| 00 | $C$ |
| 01 | $\overline C$ |
| 10 | $\overline C$ |
| 11 | $C$ |

*(Verified.)*

$$\textbf{The function is PARITY} — F = A\oplus B\oplus C.$$

**C5 (6).** $F=\sum m(0,1,5,7,8,10,14,15)$ on an 8:1 mux, $A,B,C$ selecting, $D$ on the data:

| sel $ABC$ | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **data** | $1$ | $0$ | $D$ | $D$ | $\overline D$ | $\overline D$ | $0$ | $1$ |

*(Verified.)*

---

## Part D (5 pts each)

**D1 (5).** $F = x\cdot F|_{x=1}+\overline x\cdot F|_{x=0}$.

**D2 (5).** Put $k-1$ variables on the selects. **Each select combination fixes those $k-1$ variables, leaving a function of the one remaining variable $x$** — and there are only four such functions: $0$, $1$, $x$, $\overline x$. **Wire whichever one applies to that data input.** Shannon guarantees the reassembly is correct.

**D3 (5).** **8 AND gates + one 5-input OR** *(and $n$ inverters)*, against **2 gates** minimised.

**The decoder version is right when design time dominates** — one-off control logic, a design still changing, or when the same decoder is shared by several output functions *(which is a ROM)*.

**D4 (5).** **Minimisation stops mattering.**

A LUT holds $2^k$ bits regardless of the function. **$\sum m(1,3,5,6,7)$ minimises to 2 gates and $\sum m(0,3,5,6,7)$ to 11 literals — but both are one 8-bit LUT.** *(Verified.)* **On an FPGA you are buying tables, not gates.**

**D5 (5).** **The flat mux and the ripple-carry adder fail the same way, and the tree fixes it the same way.**

A flat 32:1 mux needs one enormous OR — high fan-in, slow. A ripple adder needs a chain of 32 dependent stages — long serial path. **Both are structural, and in both cases the fix is to restructure**: a tree for the mux, carry-lookahead for the adder. **Neither is fixed by cheaper gates.**

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

1. **A4:** naming only one of the two encoder failures.
2. **B5:** "both are flags" without the general statement about output spaces.
3. **C4:** deriving the data inputs algebraically and mis-signing $\overline C$; the reliable method is to fix $A,B$ and ask what $F$ does as $C$ varies.
4. **D3:** not mentioning the shared-decoder case.
5. **D5:** treating the two as unrelated.

---

*ECE 110 · Week 5 · PS 5 Solutions · Instructor Only*

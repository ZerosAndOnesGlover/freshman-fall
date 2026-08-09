# ECE 110 · Digital Logic
## Week 5 · Reference Sheet
### Decoders, Encoders, Multiplexers, Demultiplexers

---

## The Four Blocks

| block | in → out | does |
|---|---|---|
| **Decoder** | $n$ → $2^n$ | asserts **exactly one** output |
| **Encoder** | $2^n$ → $n$ | reports **which** input is asserted |
| **Mux** | $2^n$ data + $n$ sel → 1 | **chooses** |
| **Demux** | 1 data + $n$ sel → $2^n$ | **routes** |

**Decoder ↔ encoder are inverses. Mux ↔ demux are inverses.**

---

## Decoder

$$Y_0=\overline{S_1}\,\overline{S_0} \quad Y_1=\overline{S_1}S_0 \quad Y_2=S_1\overline{S_0} \quad Y_3=S_1S_0$$

**The outputs are the minterms.**

| $n$:$2^n$ | AND gates | inverters |
|---|---:|---:|
| 2:4 | 4 | 2 |
| 3:8 | 8 | 3 |
| 4:16 | 16 | 4 |

**Exponential growth** — large decoders are built as trees. **Enable low ⇒ every output low.** *(verified)*

**A 3:8 decoder = two 2:4 decoders + one inverter**, using the enables to select which half is live. *(verified)*

> ⚠ **Real parts are usually ACTIVE LOW** (74HC138). Combining active-low minterms needs a **NAND**,
> not an OR — De Morgan, from Week 1.

---

## Encoder and Priority Encoder

**Plain 4:2 encoder:** $A_1=I_3+I_2$, $A_0=I_3+I_1$.

**Two failures:**
- **two inputs high → garbage** ($I_1$ and $I_2$ give $11$, naming $I_3$)
- **no input high → $00$**, indistinguishable from $I_0$

**Priority encoder:** reports the **highest** asserted line and adds **valid**.

| input | code | valid |
|---|:-:|:-:|
| `0110` | 2 | 1 |
| `0001` | 0 | 1 |
| `0000` | 0 | **0** |

*(verified)*

> **The valid bit is the fix**, and it is the same design move as Week 0/3's overflow flag: **a status
> output telling you whether to believe the data output.** Needed whenever the output space is
> smaller than the set of situations.

**Used in interrupt controllers** — priority = which device is serviced first.

---

## Multiplexer

$$Y=\overline{S_1}\,\overline{S_0}D_0+\overline{S_1}S_0D_1+S_1\overline{S_0}D_2+S_1S_0D_3$$

**A mux is a decoder with data gating.** **A demux is a decoder using its enable as the data input** — same silicon. *(verified)*

**Muxes compose:** 8:1 = two 4:1 + one 2:1. **A tree of 2:1 muxes is $\log_2 w$ levels deep.**

---

## Shannon Expansion — The Week's Real Idea

$$\boxed{F = x\cdot F|_{x=1} + \overline x\cdot F|_{x=0}}$$

### A $2^k$:1 mux with all $k$ variables selecting

**Wire the data inputs to the truth-table column.** For $F=\sum m(1,3,5,6,7)$:

$$D_0\ldots D_7 = 0,1,0,1,0,1,1,1$$

### A $2^{k-1}$:1 mux — cheaper

**Put $k-1$ variables on the selects, the last on the data.** Each data input is $0$, $1$, $x$ or $\overline x$.

| $F=\sum m(1,3,5,6,7)$, $A,B$ select | data |
|:-:|:-:|
| 00 | $C$ |
| 01 | $C$ |
| 10 | $C$ |
| 11 | $1$ |

| $F=\sum m(1,2,4,7) = A\oplus B\oplus C$ | data |
|:-:|:-:|
| 00 | $C$ |
| 01 | $\overline C$ |
| 10 | $\overline C$ |
| 11 | $C$ |

*(both verified)*

> **A $2^{k-1}$:1 mux implements ANY $k$-variable function.** No map, no algebra.

---

## Why It Matters

**A mux used this way is a lookup table: you store the answer instead of computing it.**

**A LUT costs the same whatever function is in it.** Compare:

| function | minimal SOP | LUT |
|---|---|---|
| $\sum m(1,3,5,6,7)$ | $C+AB$ — **2 gates** | 8 bits |
| $\sum m(0,3,5,6,7)$ | $AB+AC+BC+\overline A\,\overline B\,\overline C$ — **11 literals** | 8 bits |

*(verified)*

> **One minterm changed and the gate implementation got four times worse. The LUT did not change
> size at all** — only its contents.
>
> **That is an FPGA.** Its cell is a 4–6 input LUT built as a mux tree with memory on the data
> inputs. **Programming it means writing those bits**, and it is why an FPGA flow does not need
> Week 4's minimisation. *(Week 12.)*

---

## Design Trade

| method | design effort | gates |
|---|---|---|
| minimised gates | high *(map, grouping)* | **lowest** |
| decoder + OR | low | 8 ANDs + 1 OR |
| mux / LUT | **lowest** | one block |

**Minimise when silicon is scarce. Use a universal block when your time is scarce or the design will change.**

---

## Structure Decides Delay

**A 32:1 mux flat needs a 32-input OR; as a tree of 2:1 muxes it is 5 levels.**

> **Compare Week 3:** the ripple-carry adder was linear because of a **serial dependency**; a mux
> tree is logarithmic because it is a **tree**. **Week 6 applies this to the adder.**

---

## Common Errors

1. **Forgetting real decoder outputs are active low** — needing NAND, not OR.
2. **Using a plain encoder** where two inputs can be high.
3. **Omitting the valid output** and being unable to tell "line 0" from "nothing".
4. **Putting all $k$ variables on the selects** when $k-1$ suffices.
5. **Deriving mux data inputs by algebra** instead of asking what $F$ does as the data variable varies.
6. **Expecting a flat wide mux to be as fast as a tree.**

---

*ECE 110 · Week 5 · Reference Sheet*

# ECE 110 · Digital Logic
## Week 12 · Reference Sheet
### Programmable Logic

---

## The Two-Level Family

| device | AND plane | OR plane |
|---|---|---|
| **ROM** | fixed (full decoder) | **programmable** |
| **PLA** | **programmable** | **programmable** |
| **PAL** | **programmable** | fixed |

**Sizing** ($n$ in, $m$ out, $p$ product terms):

$$\text{PLA} = 2np + pm \qquad \text{PAL} = 2np \qquad \text{ROM} = 2^n m$$

| $n,m,p$ | PLA | PAL | ROM |
|---|---:|---:|---:|
| 4, 4, 8 | 96 | 64 | 64 |
| 8, 8, 16 | 384 | 256 | 2 048 |
| 10, 8, 32 | 896 | 640 | 8 192 |
| **16, 8, 64** | **2 560** | **2 048** | **524 288** |

*(verified — 205× apart at $n=16$)*

> **A ROM decodes every input, so it grows as $2^n$. A PLA generates only the product terms you
> need.** **This is the one architecture where Week 4's minimisation pays off directly** — fewer
> product terms is fewer rows in the AND plane, and a PAL with 8 terms per output will not fit an
> unminimised function.

**CPLDs are many PALs with programmable interconnect.**

---

## The FPGA

**Logic cell = a $k$-input LUT + a flip-flop + an output mux.** Plus programmable interconnect and hard blocks (memories, multipliers, **carry chains**).

| $k$ | LUT bits | functions |
|:-:|---:|---:|
| 4 | 16 | 65 536 |
| 5 | 32 | $4.29\times10^9$ |
| **6** | **64** | $\mathbf{1.8\times10^{19}}$ |

*(verified — Week 1's $2^{2^n}$ again)*

**Bigger functions split across a tree:**

| function | on 6-LUTs |
|---|---|
| 8-input | ~3 LUTs, 2 levels |
| 16-input | ~4 LUTs, 2 levels |
| 32-input | ~7 LUTs, 2 levels |

*(verified)*

### Cost is function-independent

| function | literals | LUTs |
|---|---:|---|
| $C+AB$ | 3 | **one 3-LUT** |
| $AB+AC+BC+\overline A\,\overline B\,\overline C$ | 11 | **one 3-LUT** |

*(verified)*

> **Minimisation reduces gates; an FPGA does not buy gates.** Its tools **pack and route** instead.

---

## The Three Routes To A Lookup Table

| week | form |
|---|---|
| **5** | a $2^{k-1}$:1 mux with $0,1,x,\overline x$ on the data inputs |
| **11** | a ROM — decoder + OR plane |
| **12** | an FPGA logic cell |

**One object, three times.**

---

## The Flow

$$\text{HDL} \to \text{synthesis} \to \text{technology mapping} \to \text{placement} \to \text{routing} \to \text{bitstream}$$

| step | produces |
|---|---|
| synthesis | a gate-level netlist |
| mapping | LUTs and flip-flops |
| placement | which physical cell holds what |
| routing | the interconnect configuration |
| bitstream | the file loaded into the chip |

> **Steps 2–5 are NP-hard in general**, so tools use heuristics and do not guarantee optimality —
> **exactly what Week 4 said about Quine–McCluskey's covering step.**

**Routing is usually the binding constraint**, not logic capacity: a design can fail to fit while half the LUTs sit idle.

---

## Why Hard Carry Chains Exist

**A 32-bit ripple adder is 160 gates, or roughly 64 LUTs** — and slow through generic interconnect, because every carry crosses programmable routing.

> **So serious FPGAs put a dedicated carry chain in silicon.** **Week 3's serial-dependency problem
> is universal enough that a general-purpose device hardens a special case for it.**

---

## The Trade

| | speed | area | configurable |
|---|---|---|---|
| custom silicon | **best** | **best** | no — months and millions |
| FPGA | ~10× worse | ~20× worse | **yes, in seconds** |

**Right for small volumes and changing designs. Wrong for ten million units.**

---

## Common Errors

1. **Sizing a ROM as if it grew with product terms.**
2. **Thinking minimisation helps on an FPGA.**
3. **Assuming logic capacity is what makes a design fail to fit** — it is usually routing.
4. **Expecting the tools to be optimal.**
5. **Not recognising the ROM/mux/LUT as one object.**

---

*ECE 110 · Week 12 · Reference Sheet*

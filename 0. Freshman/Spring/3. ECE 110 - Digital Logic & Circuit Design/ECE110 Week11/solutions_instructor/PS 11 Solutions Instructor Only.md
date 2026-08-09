# ECE 110 · Digital Logic
## Problem Set 11 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All arithmetic verified.

---

## Part A (5 pts each)

**A1 (5).** Flip-flop ~20T, SRAM 6T, DRAM 1T.

**Memory is not built from flip-flops because the area is prohibitive:** 1 Gib of flip-flops is **21.5 billion transistors** for storage alone — more than most whole processors. *(Verified.)*

**A2 (5).** Two cross-coupled inverters plus two access transistors.

**The cross-coupled pair is Week 7's latch**, reduced to the smallest circuit that still holds a bit.

**A3 (5).** **The bit lines are driven hard and overpower the cell's inverters.**

**Sizing is a constraint because two requirements pull in opposite directions:** the write drivers must be strong enough to flip the cell, but the cell must be strong enough not to flip when merely *read*. **Get the ratio wrong in either direction and the cell fails.**

**A4 (5).** One access transistor, one capacitor. **The bit is the charge stored on the capacitor.**

---

## Part B (6 pts each)

**B1 (6).** **Reading connects the capacitor to the bit line and shares its charge**, so the stored charge is gone once sensed.

**The chip must write the value back immediately after every read** — automatically, as part of the access.

**B2 (6).**

$$\frac{64\text{ ms}}{8192} = \boxed{7.81\ \mu\text{s per row}}$$

**B3 (6).**

$$\frac{8192\times350\text{ ns}}{64\text{ ms}} = \frac{2.867\text{ ms}}{64\text{ ms}} = \boxed{4.5\%}$$

*(Verified.)*

**B4 (6).** **It buys a 6× density advantage.**

| 1 Gib | transistors |
|---|---:|
| SRAM | 6 442 450 944 |
| DRAM | **1 073 741 824** |

*(Verified.)* **Spending 4.5% of the time refreshing to use one sixth of the silicon is a good trade**, which is why main memory is DRAM.

**B5 (6).** **A gate restores its output to a full logic level regardless of how degraded its input was, so noise is discarded at every stage.**

**A DRAM cell restores nothing** — it is a capacitor slowly discharging, read as a millivolt-scale disturbance on a bit line and compared against a reference by an analogue sense amplifier.

**What maintains the abstraction: the refresh circuitry and the sense amplifiers** — engineering, not physics.

*Marking: 3 for the contrast, **3 for naming what holds the abstraction up.***

---

## Part C (6 pts each)

**C1 (6).** $2^{20} = \boxed{1\,048\,576}$ AND gates.

**C2 (6).** $1024\times1024$: a 10-bit row decoder (1024 gates) and a 10-bit column decoder (1024 gates) = $\boxed{2048}$.

$$\textbf{512× fewer.}$$

**C3 (6).**

| words | flat | square | saving |
|---:|---:|---:|---:|
| $2^{10}$ | 1 024 | 64 | 16× |
| $2^{16}$ | 65 536 | 512 | 128× |
| $2^{20}$ | 1 048 576 | 2 048 | **512×** |

*(Verified.)* **The advantage grows with size** — which is why every memory ever built is organised this way.

**C4 (6).** **Because the address is applied in two halves**, row then column, so the same pins carry both. **This halves the pin count**, and pins are one of the most expensive resources on a package.

**C5 (6).** **An access is: open the row, then select the column.** If the next access is in the **same row**, the row is already open and only the column select is needed.

**Consecutive addresses usually lie in the same row**, so they skip the row-open step. **This is the hardware basis of locality of reference.**

---

## Part D (5 pts each)

**D1 (5).** **A decoder driving a programmable OR plane** — Week 5's "one decoder shared by many OR gates".

**10-bit address, 8-bit word: $2^{10} = 1024$ decoder lines, $1024\times8 = \boxed{8192}$ stored bits.** *(Verified.)*

**D2 (5).** Mask ROM, PROM, EPROM, EEPROM/Flash.

$$\textbf{Flash / EEPROM} — \text{non-volatile and electrically erasable.}$$

**D3 (5).** **A three-state output is an output that has been electrically disconnected** — the driver is switched off entirely.

**It is not a third logic value** because nothing is being driven; the wire's voltage is whatever else on the bus determines, or floating if nothing does.

**Two devices driving one bus simultaneously with opposite values is a short circuit** between supply and ground through the two drivers — **large current, possible damage, and certainly invalid data.**

**D4 (5).** **$1\text{K}\times8$ from $1\text{K}\times4$:** two devices side by side sharing address and control, one supplying bits 7–4 and the other 3–0. **No extra logic.**

**$2\text{K}\times8$ from $1\text{K}\times8$:** two devices, with address bit $A_{10}$ driving a **1-to-2 decoder** that generates the two chip selects.

**Both use Week 5's blocks** — the second needs a decoder.

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

1. **A3:** naming only one side of the sizing constraint.
2. **B5:** describing the leak without saying what maintains the abstraction.
3. **C4:** answering "to save gates" rather than **pins**.
4. **D3:** calling a three-state output a third logic value.
5. **D4:** using a decoder for the width expansion, where none is needed.

---

*ECE 110 · Week 11 · PS 11 Solutions · Instructor Only*

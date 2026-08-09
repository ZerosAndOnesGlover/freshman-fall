# ECE 110 · Digital Logic
## Lab 11 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All arithmetic verified.

---

## Part A — The Cost Model (25 pts)

### A1 (10)

| capacity | flip-flops (20T) | SRAM (6T) | DRAM (1T) |
|---|---:|---:|---:|
| 1 Kib | 20 480 | 6 144 | 1 024 |
| 1 Mib | 20 971 520 | 6 291 456 | 1 048 576 |
| 1 Gib | **21 474 836 480** | 6 442 450 944 | **1 073 741 824** |

*(Verified.)*

### A2 (8)

**Exceeding $10^9$ transistors:**

| | bits | ≈ |
|---|---:|---|
| flip-flops | 50 000 000 | **6 MiB** |
| SRAM | 166 666 667 | **20 MiB** |
| DRAM | 1 000 000 000 | **119 MiB** |

*(Verified.)*

### A3 (7)

$$\text{SRAM:DRAM} = 6{:}1 \qquad \text{flip-flop:DRAM} \approx 20{:}1$$

**What it explains:** a real machine has **megabytes of SRAM cache and gigabytes of DRAM main memory** — the ratio of capacities mirrors the ratio of costs, and no amount of wanting fast memory changes the area arithmetic.

---

## Part B — The Refresh Budget (25 pts)

### B1 (10), B2 (8)

$$\frac{64\text{ ms}}{8192} = \mathbf{7.81\ \mu s} \qquad \frac{8192\times350\text{ ns}}{64\text{ ms}} = \mathbf{4.5\%}$$

*(Verified.)*

### B3 (7) — the part with the surprise

| rows | interval | overhead |
|---:|---:|---:|
| 8 192 | 7.81 μs | 4.5% |
| **65 536** | **0.98 μs** | **35.8%** |

*(Verified.)*

$$\textbf{The overhead RISES — eightfold, for an eightfold row count.}$$

**Why:** the retention window is fixed by physics, the number of rows to service in it has grown, and each refresh costs the same. **The fraction is $\text{rows}\times t_{RFC}/t_{ret}$, which is linear in rows.**

> **Most students predict it stays constant or falls.** It does neither, and 35.8% is clearly
> untenable — **which is exactly why real devices refresh multiple rows per command, bank their
> arrays, and exploit temperature-dependent retention.** The naive scaling does not work, and finding
> that out from the arithmetic is the point of the part.

*Marking: 4 numbers, **3 for the explanation.** A student who reports the numbers but predicts "constant" and does not notice the contradiction earns 4.*

---

## Part C — Organisation and a Verilog Model (25 pts)

### C1 (8)

| words | flat | square | saving |
|---:|---:|---:|---:|
| $2^{10}$ | 1 024 | 64 | 16× |
| $2^{16}$ | 65 536 | 512 | 128× |
| $2^{20}$ | 1 048 576 | 2 048 | 512× |

**The saving scales as roughly $2^{n/2}$** — it grows with size.

### C2 (10)

**Write all 16 locations, read back, 0 failures.** *(Reference implementation verified.)*

### C3 (7)

**As written — synchronous read, with `dout` registered — a synthesis tool infers a block RAM** on an FPGA, or a compiled memory macro in an ASIC flow.

**With `assign dout = mem[addr];` the read becomes asynchronous**, which most block RAMs cannot do — **so the tool falls back to building the array out of flip-flops and a large multiplexer**, i.e. a register file. **For 16×8 that is fine; for 1024×8 it is catastrophic.**

> **The one-line change decides whether you get a memory macro or a thousand flip-flops.** This is
> the practical face of Week 10's "know what gates your code becomes".

*Marking: 3 register-file/RAM distinction, **4 for the consequence of the asynchronous read.***

---

## Part D — A Real ROM (25 pts)

### D1 (15)

$2^n \bmod 13$ for $n=0\ldots7$:

| addr | value | bits |
|:-:|---:|:-:|
| 0 | 1 | `0001` |
| 1 | 2 | `0010` |
| 2 | 4 | `0100` |
| 3 | 8 | `1000` |
| 4 | 3 | `0011` |
| 5 | 6 | `0110` |
| 6 | 12 | `1100` |
| 7 | 11 | `1011` |

*(Verified.)*

**Note the 74HC138's active-low outputs** — the diode matrix must be arranged accordingly, and this is the same De Morgan point as Lab 5. **Expect some pairs to wire it inverted and read the complement.**

### D2 (5)

$$\textbf{13 diodes}, \text{ against } 8\times4 = 32 \text{ for an all-ones ROM.}$$

*(Verified.)*

### D3 (5)

**Week 5's decoder-plus-OR circuit.** The decoder is the 74HC138; **the OR plane is the diode matrix** — each diode ORs its word line onto an output bit line, with a pull-down resistor completing the wired-OR.

**The correspondence:** decoder line $i$ = minterm $i$; a diode at $(i,j)$ means "minterm $i$ contributes to output $j$"; **the stored word is the truth-table row.**

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 25 |
| C | 25 |
| D | 25 |
| **Total** | **100** |

---

## Checkoff Checklist

1. A2 gives all three capacities
2. **A3 connects the ratios to a real machine**
3. B2 shows the arithmetic
4. **B3 notices the overhead RISES and explains why**
5. C2 reports 0 failures
6. **C3 explains what an asynchronous read costs**
7. D2 gives 13 of 32
8. **D3 identifies the diode matrix as the OR plane**

---

## Note for the Debrief

**Ask for predictions on B3 before revealing the answer.**

> **Most of you predicted the refresh overhead would stay about the same as the device got bigger.**
> It goes from 4.5% to **35.8%** — because the retention window is set by physics and does not grow,
> while the number of rows to service inside it does.
>
> **A device that spent a third of its time refreshing would be useless**, which is why real DRAM
> refreshes many rows per command and banks its arrays. **You found the constraint that forces that
> design, from three numbers.**

Then close the week:

> **You built a ROM out of a decoder and thirteen diodes**, and it is the same circuit you drew in
> Week 5 when we said "a shared decoder with many ORs is a ROM".
>
> **That is the third time this course has arrived at the lookup table** — as a multiplexer with
> constants, as a decoder with an OR plane, and next week as an FPGA's basic cell. **Three routes,
> one idea, and its cost never depends on the function inside it.**

---

*ECE 110 · Week 11 · Lab 11 Solutions · Instructor Only*

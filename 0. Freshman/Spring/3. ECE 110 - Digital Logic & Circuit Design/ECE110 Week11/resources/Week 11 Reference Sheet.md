# ECE 110 · Digital Logic
## Week 11 · Reference Sheet
### Memory

---

## The Cost Table

| cell | transistors/bit | volatile | refresh | access |
|---|---:|:-:|:-:|---|
| **D flip-flop** | ~20 | yes | no | fastest |
| **SRAM** (6T) | **6** | yes | no | ~1 ns |
| **DRAM** (1T1C) | **1** | yes | **yes** | ~50 ns |
| **ROM / Flash** | ~1 | **no** | no | ~50–100 ns |

**1 Gib of storage:**

| | transistors |
|---|---:|
| flip-flops | 21 474 836 480 |
| SRAM | 6 442 450 944 |
| **DRAM** | **1 073 741 824** |

*(verified)*

**Exceeding one billion transistors:** flip-flops at **6 MiB**, SRAM at **20 MiB**, DRAM at **119 MiB**. *(verified)*

> **DRAM is 6× denser than SRAM and ~20× denser than a flip-flop.** That ratio is the memory
> hierarchy's entire reason for existing.

---

## SRAM — 6T

**Two cross-coupled inverters (Week 7's latch, minimised) + two access transistors.**

| | |
|---|---|
| **read** | precharge both bit lines, raise the word line, sense which falls |
| **write** | drive the bit lines hard and **overpower** the cell |

**Sizing matters:** drivers must beat the cell's inverters, but the cell must not flip when read.

**Static, fast, volatile. Caches and register files.**

---

## DRAM — 1T1C

**One transistor, one capacitor. The bit is charge.**

### Three complications

1. **Reads are destructive** — the charge is dumped onto the bit line and sensed against a reference. **Every read needs a write-back.**
2. **It leaks.** Retention ≈ **64 ms**.
3. **Hence refresh.**

$$\frac{64\text{ ms}}{8192\text{ rows}} = 7.81\ \mu\text{s per row}$$

$$\frac{8192\times350\text{ ns}}{64\text{ ms}} = \mathbf{4.5\%} \text{ of the time}$$

*(verified)*

### The overhead grows with the device

| rows | interval | overhead |
|---:|---:|---:|
| 8 192 | 7.81 μs | **4.5%** |
| 65 536 | 0.98 μs | **35.8%** |

*(verified)*

> **More rows, the same window, the same cost each — so the overhead rises.** Real devices refresh
> several rows per command and use binning and temperature-dependent retention to keep this
> manageable. **The naive scaling does not work**, which is why the arithmetic is worth doing.

---

## Where The Abstraction Leaks

**Week 2: every gate restores its signal, so noise never accumulates.**

**A DRAM cell restores nothing.** It is a draining bucket of charge, read by an analogue amplifier comparing millivolts.

> **The one place in the course where the digital abstraction is openly a fiction**, held up by
> refresh and sense amplifiers — **by engineering, not by physics.**

---

## Organisation — Why Memories Are Square

**Flat decoder for $2^n$ words: $2^n$ AND gates** *(Week 5)*.

| words | flat | square | saving |
|---:|---:|---:|---:|
| 1 024 | 1 024 | $32\times32$ → 64 | 16× |
| 65 536 | 65 536 | $256\times256$ → 512 | 128× |
| 1 048 576 | 1 048 576 | $1024\times1024$ → **2 048** | **512×** |

*(verified)* **The saving grows with size.**

**Hence: row address strobe + column address strobe.**

> **Consecutive addresses in the same row are faster — the row is already open.** This is the
> hardware fact underneath every "locality of reference" argument in CS 201.

---

## ROM

**A decoder driving a programmable OR plane** — Week 5's shared-decoder circuit.

**$n$-bit address, $w$-bit word: $2^n$ lines, $2^n\times w$ stored bits.** *(verified: 10-bit × 8-bit → 1024 lines, 8192 bits)*

**It is a lookup table** — the third route to the same idea, after Week 5's mux and before Week 12's FPGA cell. **Its cost does not depend on the function stored.**

| variant | programmed | erasable |
|---|---|---|
| Mask ROM | at manufacture | no |
| PROM | once, by the user | no |
| EPROM | electrically | UV |
| **EEPROM / Flash** | electrically | **electrically** |

**Flash is the non-volatile one** — firmware, SSDs.

---

## Interfaces

**address · data · chip select · write enable · output enable**

**Bidirectional buses need three-state buffers.**

> **A three-state output is NOT a third logic value — it is *no* value**, the driver switched off.
> **Two devices driving one bus is a short circuit**, so chip-select decoding must make that
> impossible.

**Wider words:** chips side by side. **More words:** chips stacked with a decoder on the high address bits. **Both are Week 5's blocks.**

---

## Common Errors

1. **Assuming memory is built from flip-flops.**
2. **Forgetting DRAM reads are destructive.**
3. **Treating refresh overhead as fixed** as capacity grows.
4. **Thinking a flat decoder is fine** at realistic sizes.
5. **Treating a three-state output as a logic value.**
6. **Missing that a ROM is Week 5's circuit.**

---

*ECE 110 · Week 11 · Reference Sheet*

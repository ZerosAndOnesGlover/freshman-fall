# ECE 110 · Digital Logic
## Week 11 · Lecture 1 (Wednesday)
### SRAM and DRAM

**Date:** Wednesday 7 April 2027 · 13:00–14:15 · Week 11

---

**Reading:** Harris & Harris §5.5.1–5.5.2 | Mano & Ciletti §7.1–7.3
**Quiz 10** — at the start of today's lecture. **Covers Week 10.** Ungraded.

---

## 1. Why Not Flip-Flops

**A D flip-flop is about 20 transistors.** It is fast, robust, and has a clean synchronous interface.

**A gigabit of them is 20 billion transistors — for storage alone.**

> **So memory is a different engineering problem from logic.** In logic you optimise the critical
> path; in memory you optimise **area per bit**, and you accept complications you would never
> tolerate in a datapath.

---

## 2. SRAM — Six Transistors

**Two cross-coupled inverters, plus two access transistors.**

**The cross-coupled pair is Week 7's latch**, reduced to the smallest circuit that still holds a bit: each inverter drives the other's input, so the pair is stable in exactly two states.

**The two access transistors connect the cell to a pair of bit lines when its word line is asserted.**

| operation | how |
|---|---|
| **read** | precharge both bit lines, raise the word line, and **sense which one falls** |
| **write** | drive the bit lines hard to the wanted value and raise the word line — **overpowering** the cell's inverters |

> **Writing works by brute force**: the drivers are made stronger than the cell's transistors. **The
> sizing ratio between them is a real design constraint**, and getting it wrong gives a cell that
> cannot be written or that flips when read.

### Its properties

**Static — no refresh.** **Fast — about 1 ns.** **Volatile — loses everything on power-down.**

**Six transistors per bit is why it is used for caches and register files and nowhere that needs gigabytes.**

---

## 3. DRAM — One Transistor and a Capacitor

**One access transistor, one capacitor. The bit *is* the charge on the capacitor.**

$$\textbf{One transistor per bit — six times denser than SRAM.}$$

**And three complications, all following from the same fact: a capacitor is not a latch.**

### Complication 1 — reading destroys the data

**Reading dumps the cell's charge onto the bit line**, and the resulting voltage change is tiny — a sense amplifier detects it against a reference.

**After the read, the cell is empty.** **Every read must be followed by a write-back**, which the chip does automatically and which is part of why DRAM timing is complicated.

### Complication 2 — it leaks

**The capacitor discharges through the access transistor even when it is off.** Within milliseconds the bit is gone.

**Standard retention: 64 ms.**

### Complication 3 — hence refresh

**Every row must be read and rewritten inside the retention window.** With 8192 rows:

$$\frac{64\text{ ms}}{8192} = 7.81\ \mu\text{s per row}$$

**A row must be refreshed every 7.8 microseconds, forever, or the data evaporates.**

**At a refresh cycle time of 350 ns:**

$$\frac{8192\times350\text{ ns}}{64\text{ ms}} = \mathbf{4.5\%}$$

*(Verified.)*

> **Roughly one twentieth of the memory's availability is spent remembering rather than working.**
> **That is the price of the 6× density**, and it is a price worth paying — which is why your machine
> has gigabytes of DRAM and megabytes of SRAM, not the other way round.

---

## 4. The Comparison

| | SRAM | DRAM |
|---|---|---|
| transistors/bit | 6 | **1** |
| refresh | no | **every 64 ms** |
| read | non-destructive | **destructive** |
| access time | **~1 ns** | ~50 ns |
| used for | caches, registers | main memory |

*(Verified transistor arithmetic.)*

> **The 50× access-time gap is the reason caches exist.** A processor that went to DRAM for every
> instruction would run at DRAM speed. **CS 201 spends a large fraction of its time on this one
> ratio.**

---

## 5. Where The Digital Abstraction Leaks

**Week 2 said a gate restores its signal, so noise never accumulates and you can reason in 0s and 1s.**

**A DRAM cell does not restore anything.** It is a bucket of charge, slowly draining, read by an analogue amplifier comparing millivolts against a reference.

> **This is the one place in the course where the digital abstraction is openly a fiction**, held up
> by refresh circuitry and sense amplifiers. **Everything above it — every gate, every flip-flop,
> every state machine — depends on that fiction being maintained**, and it is maintained by
> engineering rather than by physics.

---

## 6. What To Take From This Lecture

1. **A flip-flop is ~20 transistors** — far too many for bulk storage.
2. **SRAM is 6T: cross-coupled inverters (Week 7's latch) plus two access transistors.**
3. **Writing SRAM overpowers the cell**; the sizing ratio is a real constraint.
4. **DRAM is 1T1C — six times denser**, and the bit is charge.
5. **DRAM reads are destructive** and need a write-back.
6. **Refresh: every row within 64 ms; 7.81 μs per row for 8192 rows; about 4.5% of the time.**
7. **SRAM ~1 ns, DRAM ~50 ns** — the gap that makes caches necessary.
8. **DRAM is where the digital abstraction is openly maintained rather than free.**

---

*Next: Thursday — ROM and Memory Organisation*

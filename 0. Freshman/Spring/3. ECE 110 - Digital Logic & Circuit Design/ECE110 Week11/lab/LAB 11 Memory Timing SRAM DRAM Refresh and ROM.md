# ECE 110 · Digital Logic
## Lab 11: Memory — Timing, Refresh, and a ROM
### Week 11 Lab Session

---

**Duration:** 2 hours (Friday 14:00–15:50, MEC 110)
**Format:** Pairs. **Both partners submit their own report.**
**Graded on:** completion + correctness — **100 points**
**Tools:** Icarus Verilog, Python. **74HC138 + diode/resistor ROM matrix** for Part D.

---

## Overview

**Memory is mostly arithmetic and organisation**, so most of this lab is modelling and counting rather than wiring. Part D builds a real ROM out of a decoder and a diode matrix, which is genuinely how early ROMs were made.

---

## Part A — The Cost Model (25 pts)

**A1 (10 pts).** Write a script that tabulates, for capacities of 1 Kib, 1 Mib and 1 Gib, the transistor count for storage built from **flip-flops (20T)**, **SRAM (6T)** and **DRAM (1T)**.

**A2 (8 pts).** **At what capacity does a flip-flop implementation exceed one billion transistors?** At what capacity does SRAM?

**A3 (7 pts).** **State the density ratios** SRAM:DRAM and flip-flop:DRAM, and say in one sentence what those ratios explain about a real computer.

---

## Part B — The Refresh Budget (25 pts)

**B1 (10 pts).** For a device with **8192 rows** and **64 ms** retention, compute the interval between row refreshes.

**B2 (8 pts).** With **tRFC = 350 ns**, compute the fraction of time spent refreshing. **Show the arithmetic.**

**B3 (7 pts).** Repeat B1 and B2 for a device with **65 536 rows** at the same retention.

**Does the refresh overhead rise, fall, or stay the same as the device grows?** **Explain the result** — it may not be what you expected.

---

## Part C — Organisation and a Verilog Model (25 pts)

**C1 (8 pts).** Tabulate flat-decoder versus square-array decoder gate counts for $2^{10}$, $2^{16}$, $2^{20}$ words. **State how the saving scales.**

**C2 (10 pts).** Write a Verilog model of a **synchronous $16\times8$ RAM**:

```verilog
module ram16x8(output reg [7:0] dout, input [3:0] addr,
               input [7:0] din, input we, clk);
  reg [7:0] mem [0:15];
  always @(posedge clk) begin
    if (we) mem[addr] <= din;
    dout <= mem[addr];
  end
endmodule
```

**Testbench it: write a known pattern to all 16 locations, read them all back, and report failures.**

**C3 (7 pts).** **Is `mem` a register file or a RAM in this description?** What would a synthesis tool infer, and **what changes if you make the read asynchronous** (`assign dout = mem[addr];`)?

---

## Part D — A Real ROM (25 pts)

**D1 (15 pts).** Build an **$8\times4$ ROM** from a 74HC138 decoder and a diode matrix: a diode from decoder line $i$ to output bit $j$ stores a 1 at address $i$, bit $j$.

**Programme it with the first eight values of $2^n \bmod 13$**, and verify all eight addresses.

**D2 (5 pts).** **How many diodes did you use, and how many would a full $8\times4$ ROM need?**

**D3 (5 pts).** **Which Week 5 circuit is this?** Explain the correspondence explicitly, and say what the OR plane is made of here.

---

## Marking Summary

| Part | Points |
|---|---|
| A — the cost model | 25 |
| B — the refresh budget | 25 |
| C — organisation and a Verilog model | 25 |
| D — a real ROM | 25 |
| **Total** | **100** |

---

*ECE 110 · Week 11 · Lab 11*
